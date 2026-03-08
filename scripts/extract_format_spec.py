from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from zipfile import ZipFile
import xml.etree.ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


@dataclass
class ArtifactBundle:
    document_root: ET.Element
    styles_root: ET.Element | None
    numbering_root: ET.Element | None


def _parse_xml_bytes(xml_bytes: bytes) -> ET.Element:
    return ET.fromstring(xml_bytes)


def _load_from_docx(docx_path: Path) -> ArtifactBundle:
    with ZipFile(docx_path, "r") as archive:
        document_root = _parse_xml_bytes(archive.read("word/document.xml"))
        styles_root = _parse_xml_bytes(archive.read("word/styles.xml")) if "word/styles.xml" in archive.namelist() else None
        numbering_root = _parse_xml_bytes(archive.read("word/numbering.xml")) if "word/numbering.xml" in archive.namelist() else None
    return ArtifactBundle(document_root=document_root, styles_root=styles_root, numbering_root=numbering_root)


def _load_from_unpacked(unpacked_dir: Path) -> ArtifactBundle:
    word_dir = unpacked_dir / "word"
    document_root = _parse_xml_bytes((word_dir / "document.xml").read_bytes())
    styles_path = word_dir / "styles.xml"
    numbering_path = word_dir / "numbering.xml"
    styles_root = _parse_xml_bytes(styles_path.read_bytes()) if styles_path.exists() else None
    numbering_root = _parse_xml_bytes(numbering_path.read_bytes()) if numbering_path.exists() else None
    return ArtifactBundle(document_root=document_root, styles_root=styles_root, numbering_root=numbering_root)


def _safe_text(node: ET.Element | None) -> str:
    if node is None:
        return ""
    text_nodes = node.findall(".//w:t", NS)
    text = " ".join((text_node.text or "").strip() for text_node in text_nodes if (text_node.text or "").strip())
    return " ".join(text.split())


def _paragraph_style_id(paragraph: ET.Element) -> str:
    style = paragraph.find("./w:pPr/w:pStyle", NS)
    if style is None:
        return ""
    return style.attrib.get(f"{{{W_NS}}}val", "")


def _extract_headings(document_root: ET.Element) -> list[dict[str, Any]]:
    headings: list[dict[str, Any]] = []
    body = document_root.find("./w:body", NS)
    if body is None:
        return headings

    order_index = 0
    for paragraph in body.findall("./w:p", NS):
        text = _safe_text(paragraph)
        if not text:
            continue
        style_id = _paragraph_style_id(paragraph)
        is_heading = style_id.lower().startswith("heading") or style_id.lower().startswith("title")
        if is_heading or len(text) <= 120:
            headings.append(
                {
                    "order": order_index,
                    "text": text,
                    "style_id": style_id,
                    "is_heading_like": is_heading,
                }
            )
        order_index += 1
    return headings


def _table_signature(table_node: ET.Element, index: int) -> dict[str, Any]:
    rows = table_node.findall("./w:tr", NS)
    grid_cols = table_node.findall("./w:tblGrid/w:gridCol", NS)
    row_summaries: list[dict[str, Any]] = []
    vertical_merge_count = 0
    horizontal_merge_count = 0

    for row_index, row in enumerate(rows):
        cells = row.findall("./w:tc", NS)
        texts = [_safe_text(cell) for cell in cells]
        grid_spans = []
        row_vmerge = 0
        for cell in cells:
            cell_spans = []
            for span in cell.findall(".//w:gridSpan", NS):
                try:
                    span_value = int(span.attrib.get(f"{{{W_NS}}}val", "1"))
                except ValueError:
                    span_value = 1
                if span_value > 1:
                    horizontal_merge_count += 1
                cell_spans.append(span_value)
            if cell.findall(".//w:vMerge", NS):
                row_vmerge += 1
                vertical_merge_count += 1
            grid_spans.append(cell_spans)

        row_summaries.append(
            {
                "row_index": row_index,
                "cell_count": len(cells),
                "texts": texts[:8],
                "vmerge_cells": row_vmerge,
                "grid_spans": grid_spans[:8],
            }
        )

    return {
        "table_index": index,
        "row_count": len(rows),
        "grid_col_count": len(grid_cols),
        "vertical_merge_count": vertical_merge_count,
        "horizontal_merge_count": horizontal_merge_count,
        "header_candidate_rows": row_summaries[:3],
        "sample_body_rows": row_summaries[3:6],
    }


def _extract_tables(document_root: ET.Element) -> list[dict[str, Any]]:
    body = document_root.find("./w:body", NS)
    if body is None:
        return []
    tables = body.findall("./w:tbl", NS)
    return [_table_signature(table, index) for index, table in enumerate(tables)]


def _extract_default_style_info(styles_root: ET.Element | None) -> dict[str, Any]:
    if styles_root is None:
        return {}

    defaults = styles_root.find("./w:docDefaults", NS)
    result: dict[str, Any] = {}
    if defaults is not None:
        run_props = defaults.find("./w:rPrDefault/w:rPr", NS)
        if run_props is not None:
            fonts = run_props.find("./w:rFonts", NS)
            size = run_props.find("./w:sz", NS)
            if fonts is not None:
                result["ascii_font"] = fonts.attrib.get(f"{{{W_NS}}}ascii", "")
                result["east_asia_font"] = fonts.attrib.get(f"{{{W_NS}}}eastAsia", "")
            if size is not None:
                result["half_point_size"] = size.attrib.get(f"{{{W_NS}}}val", "")

    named_styles = []
    for style in styles_root.findall("./w:style", NS):
        style_id = style.attrib.get(f"{{{W_NS}}}styleId", "")
        name_node = style.find("./w:name", NS)
        if style_id:
            named_styles.append({
                "style_id": style_id,
                "name": name_node.attrib.get(f"{{{W_NS}}}val", "") if name_node is not None else "",
            })
    result["named_styles"] = named_styles[:20]
    return result


def _extract_pdf_summary(pdf_path: Path | None) -> dict[str, Any]:
    if pdf_path is None or not pdf_path.exists():
        return {}
    try:
        import fitz  # type: ignore
    except Exception:
        return {
            "path": str(pdf_path),
            "available": True,
            "parsed": False,
            "note": "Install PyMuPDF to extract PDF page and text clues automatically.",
        }

    pdf_doc = fitz.open(pdf_path)
    pages: list[dict[str, Any]] = []
    for page_index in range(min(5, pdf_doc.page_count)):
        page = pdf_doc.load_page(page_index)
        raw_text = page.get_text("text")
        text = " ".join(str(raw_text).split())
        pages.append({
            "page_number": page_index + 1,
            "preview": text[:240],
            "width": round(page.rect.width, 2),
            "height": round(page.rect.height, 2),
        })
    return {
        "path": str(pdf_path),
        "available": True,
        "parsed": True,
        "page_count": pdf_doc.page_count,
        "sample_pages": pages,
    }


def build_format_spec(docx_path: Path | None, unpacked_dir: Path | None, pdf_path: Path | None) -> dict[str, Any]:
    if unpacked_dir is not None:
        bundle = _load_from_unpacked(unpacked_dir)
        source_mode = "unpacked-docx"
    elif docx_path is not None:
        bundle = _load_from_docx(docx_path)
        source_mode = "docx"
    else:
        raise ValueError("Provide either --docx or --unpacked-dir.")

    headings = _extract_headings(bundle.document_root)
    tables = _extract_tables(bundle.document_root)
    styles = _extract_default_style_info(bundle.styles_root)
    pdf_summary = _extract_pdf_summary(pdf_path)

    return {
        "source_mode": source_mode,
        "docx_path": str(docx_path) if docx_path else None,
        "unpacked_dir": str(unpacked_dir) if unpacked_dir else None,
        "pdf_path": str(pdf_path) if pdf_path else None,
        "section_order_candidates": headings[:30],
        "table_inventory": tables,
        "style_clues": styles,
        "pdf_summary": pdf_summary,
        "open_questions": [
            "Which heading candidates are real report sections versus static captions?",
            "Which tables contain mandatory total rows or note rows that must remain exact?",
            "Which merge behaviors are static and which depend on dynamic row counts?",
            "Which typography rules are legally or procedurally important?",
        ],
    }


def _render_markdown(spec: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Canonical Format Specification Draft")
    lines.append("")
    lines.append("## Source Artifacts")
    lines.append("")
    lines.append(f"- Source mode: {spec['source_mode']}")
    if spec.get("docx_path"):
        lines.append(f"- DOCX: {spec['docx_path']}")
    if spec.get("unpacked_dir"):
        lines.append(f"- Unpacked DOCX: {spec['unpacked_dir']}")
    if spec.get("pdf_path"):
        lines.append(f"- PDF: {spec['pdf_path']}")

    lines.append("")
    lines.append("## Section Order Candidates")
    lines.append("")
    for heading in spec.get("section_order_candidates", []):
        style = heading.get("style_id") or "(no style)"
        lines.append(f"- [{heading['order']}] {heading['text']} | style={style} | heading_like={heading['is_heading_like']}")

    lines.append("")
    lines.append("## Table Inventory")
    lines.append("")
    for table in spec.get("table_inventory", []):
        lines.append(f"### Table {table['table_index']}")
        lines.append("")
        lines.append(f"- Row count: {table['row_count']}")
        lines.append(f"- Grid columns: {table['grid_col_count']}")
        lines.append(f"- Vertical merge count: {table['vertical_merge_count']}")
        lines.append(f"- Horizontal merge count: {table['horizontal_merge_count']}")
        lines.append("- Header candidate rows:")
        for row in table.get("header_candidate_rows", []):
            preview = " | ".join(text for text in row.get("texts", []) if text)
            lines.append(f"  - Row {row['row_index']}: {preview}")
        lines.append("- Sample body rows:")
        for row in table.get("sample_body_rows", []):
            preview = " | ".join(text for text in row.get("texts", []) if text)
            lines.append(f"  - Row {row['row_index']}: {preview}")
        lines.append("")

    lines.append("## Typography Clues")
    lines.append("")
    style_clues = spec.get("style_clues", {})
    if not style_clues:
        lines.append("- No style information extracted")
    else:
        if style_clues.get("ascii_font"):
            lines.append(f"- Default ASCII font: {style_clues['ascii_font']}")
        if style_clues.get("east_asia_font"):
            lines.append(f"- Default East Asia font: {style_clues['east_asia_font']}")
        if style_clues.get("half_point_size"):
            lines.append(f"- Default half-point size: {style_clues['half_point_size']}")
        named_styles = style_clues.get("named_styles", [])
        if named_styles:
            lines.append("- Named styles:")
            for style in named_styles:
                lines.append(f"  - {style['style_id']}: {style['name']}")

    pdf_summary = spec.get("pdf_summary", {})
    if pdf_summary:
        lines.append("")
        lines.append("## PDF Summary")
        lines.append("")
        if pdf_summary.get("parsed"):
            lines.append(f"- Page count: {pdf_summary.get('page_count', 0)}")
            for page in pdf_summary.get("sample_pages", []):
                lines.append(f"- Page {page['page_number']}: {page['preview']}")
        else:
            lines.append(f"- {pdf_summary.get('note', 'PDF supplied but not parsed')} ")

    lines.append("")
    lines.append("## Open Questions")
    lines.append("")
    for question in spec.get("open_questions", []):
        lines.append(f"- {question}")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a draft canonical format specification from an approved DOCX or unpacked DOCX folder.")
    parser.add_argument("--docx", type=Path, help="Path to the approved DOCX file")
    parser.add_argument("--unpacked-dir", type=Path, help="Path to an unpacked DOCX directory containing word/document.xml")
    parser.add_argument("--pdf", type=Path, help="Optional path to the PDF exported from the approved DOCX")
    parser.add_argument("--output", type=Path, required=True, help="Output file path for the generated specification")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    args = parser.parse_args()

    spec = build_format_spec(args.docx, args.unpacked_dir, args.pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "json":
        args.output.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        args.output.write_text(_render_markdown(spec), encoding="utf-8")


if __name__ == "__main__":
    main()
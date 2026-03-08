# Agency Report Format Skill Kit

Vietnamese version: [README-VN.md](README-VN.md)

This repository grew out of a practical problem: generating agency-standard reports every month while the data changes and, with it, the report structure itself. Mail merge is still useful when a document only needs simple placeholder replacement. But once a report contains tables with changing row counts, changing columns, complex merged cells, charts, and strict formatting rules, the problem is no longer just filling a Word template.

The harder question is: how do you help AI understand the structure of a long report, sometimes dozens of pages, without manually describing every row, table, merge rule, and formatting constraint? This repository describes one answer: let an AI agent read the right reference artifacts, analyze DOCX, PDF, and when possible XML structure, then turn that analysis into a canonical format specification, an execution plan, and a validated DOCX generation pipeline.

## Project Overview

This is not just a technical demo. It documents an attempt to solve a real report-automation problem: reproducing complex agency-standard reports with AI while keeping the output structurally faithful to the approved form.

The real task is not just filling a Word template. It is reproducing a final artifact when the report contains:

- dynamic tables
- multi-row headers
- horizontal and vertical merges
- mandatory total rows and note rows
- charts or other data-driven visual sections
- typography, spacing, page flow, and Word/PDF constraints that affect acceptance

That is why mail merge or placeholder replacement is not enough. Those techniques can fill fixed fields, but they do not reliably reproduce table schema, merge maps, mandatory rows, or layout-sensitive DOCX and PDF behavior.

This repository makes that problem more understandable and repeatable by documenting the approach, the working pipeline, and the main friction points that must be handled.

## Human Input Boundary

The human role is intentionally narrow. A user only prepares these reference artifacts:

1. the approved DOCX form
2. the PDF exported from that DOCX
3. if available, the unpacked DOCX or its XML parts

From that point on, this repository is about what the AI agent should do with those artifacts.

## Agent Skill Flow

The skill expects the AI agent to operate in this order:

1. Read the approved DOCX to recover visible structure: section order, heading hierarchy, table inventory, total rows, note rows, and fixed wording.
2. Read the reference PDF to understand final display truth: page breaks, page flow, spacing drift, width drift, and visual parity.
3. Read unpacked DOCX XML to recover Word-specific structure: grid layout, `w:gridSpan`, `w:vMerge`, header signatures, and table boundaries.
4. Merge the extracted facts into a canonical format specification.
5. Build an execution plan and fix-layer map across data, template, post-process, XML, and validation layers.
6. Build the canonical report model and render the first DOCX pass.
7. Post-process sensitive structures such as dynamic tables, total rows, note rows, and merge behavior.
8. Compare the generated DOCX against DOCX/XML references and compare the generated PDF against the reference PDF in sensitive pages or regions.
9. Route each mismatch back to the correct fix layer.
10. Emit a final review package containing the DOCX, specification, mismatch summary, and acceptance status.

## Technical Pipeline

The technical pipeline described by this repository can be reduced to six layers:

1. Artifact ingestion  
   Load the approved DOCX, the reference PDF, and when available the unpacked DOCX or XML.

2. Structure extraction  
   Extract heading candidates, section order, table inventory, header rows, row groups, merge markers, and style clues.

3. Layout interpretation  
   Read the PDF for final layout truth, then reconcile it with DOCX and XML so the agent can separate visual rules from Word-structure rules.

4. Intermediate planning  
   Write the canonical format specification, identify the active generation path, and build the execution plan and fix-layer map.

5. Document generation  
   Render a first DOCX pass from the template and canonical report model, then patch sensitive structures via post-processing or XML-level handling.

6. Validation and refinement  
   Check structural parity, visual parity, and acceptance status, then iterate on the correct layer until the DOCX is acceptable.

The intended final output is a DOCX that stays close to the approved agency form, plus the artifacts that explain why the output should be accepted.

## Core Libraries / Technical Components

The relevant libraries and components should stay aligned with what exists in the sample script and the source implementation behind this repository:

- `zipfile`  
  Opens `.docx` files as OpenXML packages and reads XML parts directly.
- `xml.etree.ElementTree`  
  Parses `document.xml`, `styles.xml`, and related XML files to extract structural facts.
- `lxml`  
  Useful when deeper XML inspection or more flexible XML handling is required.
- `PyMuPDF` via `fitz`  
  Reads PDFs, extracts page clues, renders review images, and supports visual comparison.
- `docxtpl`  
  Renders the first DOCX pass from a template and a normalized context/model.
- `python-docx`  
  Post-processes tables, total rows, note rows, merges, and other Word-sensitive structures.
- `docx2pdf`  
  Converts DOCX to PDF when the pipeline needs a comparable PDF output.

The repository does not assume one library can solve the whole pipeline. The correct approach is to separate artifact reading, rendering, post-processing, and validation.

## Repository Structure

Core files and folders in this shareable repository are:

- [.github/skills/report-form-reconstruction/SKILL.md](.github/skills/report-form-reconstruction/SKILL.md)  
  Defines the skill, goals, required workflow, anti-patterns, and deliverables.
- [.github/instructions/report-form-reconstruction.instructions.md](.github/instructions/report-form-reconstruction.instructions.md)  
  Adds repository-level rules for AI agent behavior.
- [copilot-instructions.md](copilot-instructions.md)  
  Base repository rules for working on strict report-format problems.
- [scripts/extract_format_spec.py](scripts/extract_format_spec.py)  
  Sample extractor that reads DOCX or XML and emits a draft canonical format specification.
- [docs/example-format-spec.md](docs/example-format-spec.md)  
  Example of the intermediate output the agent should produce before changing code or finalizing generation.
- [docs/how-we-read-the-approved-word-form.md](docs/how-we-read-the-approved-word-form.md)  
  Technical note on reading DOCX, XML, and PDF as layered source-of-truth artifacts.
- [docs/methodology.md](docs/methodology.md)  
  Method description, fix-layer thinking, and failure modes.
- [docs/reference-artifact-ingestion.md](docs/reference-artifact-ingestion.md)  
  Priority order for DOCX, PDF, XML, screenshots, and verbal notes.

Supporting files and folders are:

- [templates/report-profile.template.md](templates/report-profile.template.md)
- [templates/artifact-package-for-ai.template.md](templates/artifact-package-for-ai.template.md)
- [templates/acceptance-checklist.template.md](templates/acceptance-checklist.template.md)
- [docs/how-to-use-with-ai.md](docs/how-to-use-with-ai.md)
- [docs/redaction-checklist.md](docs/redaction-checklist.md)
- [docs/publish-to-github.md](docs/publish-to-github.md)

## What This Repo Shares

This repository shares:

- how an AI agent should read DOCX, PDF, and XML as layered source-of-truth artifacts
- how to extract structural facts from reference artifacts
- how to convert those facts into a canonical format specification
- how to use that specification to build an intermediate plan and choose the correct fix layer
- how to render, post-process, validate, and refine a DOCX until format fidelity is acceptable
- how to package the full logic as a reusable AI skill

## Scope and Non-Goals

This repository is not intended to be:

- a universal report generator for every document type
- a simple mail-merge template
- a guide for manual Word editing
- a complete business-codebase for any one organization or form
- a promise that every layout can be reconstructed from screenshots or verbal descriptions alone

Its scope is narrower: it standardizes a skill for AI agents that turns approved reference artifacts into high-fidelity DOCX output through an explicit, reviewable pipeline.

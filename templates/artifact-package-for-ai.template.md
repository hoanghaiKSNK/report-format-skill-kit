# Artifact Package For AI Template

Give this file to AI so it can assemble the minimum artifact set it should read before touching code. You should mainly add any missing paths or facts.

## Purpose

- What report or deliverable is this package for?
- Why does format fidelity matter?

## Artifact Bundle

- Approved DOCX:
- Approved PDF exported from the DOCX:
- Unpacked DOCX folder:
- Structural notes written by a human:
- Screenshots or side-by-side comparisons:

## Source Of Truth Priority

List the priority explicitly for this case.

1. 
2. 
3. 

## What The AI Must Produce

- a canonical format specification draft
- an execution plan or fix-layer map
- a generated DOCX
- a mismatch summary
- an acceptance status

## Sensitive Sections

- Section or table 1:
- Section or table 2:
- Section or table 3:

## Known Risks

- Wrong values but correct structure:
- Correct values but wrong layout:
- DOCX-specific drift:
- PDF-specific drift:
- Merge-related drift:

## Recommended Prompt

```text
We have a report that must match an approved form exactly.
Treat the approved artifacts in this package as the source of truth.
Read the DOCX, PDF, unpacked DOCX XML, and structural notes first.
List section order, table schema, merge maps, total rows, note rows, typography rules, and page rules.
Write a canonical format specification draft before proposing code changes.
Then identify the active generation path and classify each likely fix into data, template, post-process, or XML handling.
```
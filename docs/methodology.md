# Methodology

This document keeps only the skill's decision model.

## Common Failure Modes

Typical failures in strict report-format work are:

- correct data but wrong section order
- correct values but wrong table structure
- correct table values but wrong merged cells
- missing mandatory note rows or total rows
- correct preview but wrong DOCX export
- correct DOCX but broken PDF conversion

## What The Canonical Format Specification Must Contain

Before generation, the agent should write down at least:

- section order and heading hierarchy
- table inventory
- table schema and header structure
- vertical and horizontal merge maps
- mandatory total rows
- mandatory note rows or footnotes
- fixed wording that must remain exact
- typography, spacing, and page rules that matter

## What The Canonical Report Model Must Contain

The format specification is not the same thing as the report model.

- the specification describes what the form requires
- the model describes what the generated report contains

The report model should describe at least:

- summary fields
- repeated sections
- table rows
- total rows
- note rows
- grouping and merge semantics

## Fix-Layer Decision Table

| Symptom | Best fix layer |
| --- | --- |
| Wrong value | data mapping or report model |
| Missing variable text | template binding |
| Wrong section order | template or report model |
| Static layout drift | template |
| Missing required total row | report model or template |
| Wrong note-row wording | template or post-process |
| Wrong dynamic merged rows | post-process |
| Unexplained Word structure problem | XML inspection |

## Validation Contract

Minimum validation should check:

- section order
- headings
- table schema
- merged cells
- total rows and note rows
- fonts or emphasis where acceptance depends on them
- alignment, spacing, and widths where acceptance depends on them
- page-break or overflow behavior
- parity after conversion if PDF is also a deliverable

## Operating Rules

- do not use preview as evidence that DOCX is correct
- do not ask the agent to imitate the reference file before writing the specification
- do not patch multiple layers blindly before classifying the mismatch
- do not mix data errors with formatting errors

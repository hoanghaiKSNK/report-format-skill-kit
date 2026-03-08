---
name: report-form-reconstruction
description: Build, review, and fix report-generation pipelines that must match an approved agency form exactly. Use for Word or PDF report fidelity, template drift, merged cells, section order, acceptance checklists, and AI-readable implementation rules.
argument-hint: Describe the target report, mismatch, or workflow gap. Example: create a source-of-truth workflow for a monthly regulatory report that must match an approved DOCX form.
user-invocable: true
---

# Report Form Reconstruction

Use this skill when output format matters as much as data values.

## Goals

- identify the approved source of truth
- extract structural facts from the approved artifact
- map the active generation path
- choose the correct fix layer
- validate the result against an explicit acceptance checklist

## Source Of Truth Priority

1. Approved final DOCX or PDF form
2. Unpacked structural XML or a redacted structural export
3. Generated output from the current system

## Required Workflow

1. Identify the report outputs and canonical input data.

2. Extract a canonical format specification from the approved artifact.
   The AI should explicitly list:
   - section order and heading hierarchy
   - table inventory
   - table schema and header structure
   - vertical and horizontal merge maps
   - total rows and note rows
   - fixed wording that must survive export
   - typography, spacing, and page rules that matter for acceptance

3. Map the generation layers.
   Separate:
   - report model generation
   - template rendering
   - post-processing
   - format conversion
   - validation

4. Classify the defect.
   Use one of these categories:
   - wrong data
   - missing section
   - wrong ordering
   - wrong table structure
   - wrong merge behavior
   - wrong total or note row behavior
   - wrong typography or spacing
   - conversion-only drift

5. Choose the fix layer.
   - wrong data: fix the report model or mapping
   - wrong placeholder content: fix template bindings
   - repeated structure mismatch: fix the template
   - wrong mandatory totals or static note rows: fix report model or template
   - variable merged cells or dynamic rows: fix controlled post-processing
   - unexplained Word behavior: inspect XML-level structure

6. Verify using the approved form.
   Check both visual parity and structural parity for sensitive sections.

7. Record acceptance status.
   State what passed, what remains open, and what still needs manual review.

## Anti-Patterns

- using generated output as the only reference
- asking AI to mimic the look of a report without extracting structural facts first
- maintaining separate business logic for preview and export without a reason
- making layout-only fixes in HTML when the real target is DOCX
- claiming parity without checking merged cells, row structure, and section order

## Deliverables

- canonical format specification summary
- execution path summary
- mismatch diagnosis
- root-cause fix recommendation
- acceptance status against the checklist

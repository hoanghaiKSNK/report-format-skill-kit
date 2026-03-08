# How We Read The Approved Word Form

This document describes the implementation pattern behind the skill.

## Multi-Layer Artifact Model

The skill does not read one file only. It reads multiple layers of source of truth:

1. the approved DOCX for visible structure
2. the template derived from that DOCX for the first render pass
3. the approved DOCX again as a structural reference during post-processing
4. unpacked DOCX XML for structural validation
5. the approved PDF for final visual review

## Technical Sequence

### 1. Read the approved DOCX

The agent uses the approved DOCX to identify section order, headings, tables, total rows, note rows, and repeated structural patterns.

### 2. Render the first pass from the template

The agent renders the canonical report model into a template that is already close to the approved form. At this stage, the goal is correct data on a near-correct structure, not full fidelity yet.

### 3. Post-process with the reference DOCX

After rendering, the agent opens the generated DOCX and the approved DOCX together. Sensitive sections are rebuilt or patched from the reference structure.

Common fixes at this layer are:

- rebuilding dynamic tables from a prototype row
- copying reference tail rows for notes or footnotes
- replacing total rows with the approved merge structure
- restoring vertical merge behavior in grouped appendix tables

### 4. Validate against XML

The agent compares the generated DOCX against reference XML to check:

- table count
- section count
- header-row signatures
- grid column counts
- maximum cell counts
- `w:vMerge`
- `w:gridSpan`

### 5. Review against PDF

If PDF is part of the deliverable, the agent compares generated PDF against approved PDF for:

- page breaks
- spacing drift
- width drift
- paragraph flow
- last-mile visual parity

## Required Intermediate Outputs

During this process the agent should write down:

- a canonical format specification
- an execution plan or fix-layer map
- a mismatch summary

If those intermediate outputs are missing, the pipeline tends to fall back into blind patching.
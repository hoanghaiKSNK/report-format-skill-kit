# How To Use With AI

This document only defines the handoff boundary for an AI agent.

## Minimal Input

Give the agent:

1. the approved DOCX form
2. the PDF exported from that DOCX
3. if available, the unpacked DOCX or XML
4. [copilot-instructions.md](../copilot-instructions.md)
5. [.github/skills/report-form-reconstruction/SKILL.md](../.github/skills/report-form-reconstruction/SKILL.md)

Files in `templates/` are optional. The agent can draft them if it needs to persist a report profile, artifact package, or acceptance checklist.

## What The Agent Must Do

Once it has the inputs, the agent should:

1. identify the source of truth
2. extract structural facts from DOCX, PDF, and XML
3. write a canonical format specification
4. build an execution plan and fix-layer map
5. render the first DOCX pass
6. post-process sensitive sections
7. validate the output

The human role is mainly to review the final output package.

## Recommended Prompt

```text
We have a report that must match an approved form.
Use the report-form-reconstruction skill.
Treat the reference DOCX, PDF, and XML as source of truth.
First extract section order, table schema, merge maps, total rows, note rows, typography rules, and page rules.
Then write a canonical format specification.
Then build the execution plan, choose the correct fix layer, generate the DOCX, and validate the output.
Do not assume preview parity means DOCX parity.
```

## Expected Output

A good run should return at least:

- a canonical format specification draft
- an execution plan or fix-layer map
- a generated DOCX
- a mismatch summary
- an acceptance status

## What To Add In A Real Project

Only add the project-specific facts this public kit cannot contain:

- real reference artifact names
- real generation entry points
- sensitive sections or tables
- conversion notes if DOCX and PDF both matter

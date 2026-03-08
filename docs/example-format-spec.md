# Example Format Specification

This is a short example of the intermediate artifact the agent should write before changing code or claiming output fidelity.

## Source Artifacts

- Approved DOCX: monthly-agency-report.docx
- Approved PDF: monthly-agency-report.pdf
- Unpacked XML: word/document.xml, word/styles.xml

## Section Order

1. Cover heading
2. Reporting scope summary
3. Main statistics table
4. Appendix table by grouped category
5. Notes and signature block

## Table Rules

### Main statistics table

- Header depth: 2 rows
- First column is a fixed row label column
- Last row is a mandatory total row
- A note row must appear immediately after the total row
- No body row may reorder the approved antibiotic columns

### Appendix grouped table

- The first column uses vertical merges for group labels
- Dynamic row count is allowed inside each group
- Group label merge behavior must survive DOCX export

## Typography And Page Rules

- Heading font weight must remain bold
- Table header text must remain centered
- Page break must occur before the appendix section
- Signature block must remain on the final page

## Sensitive Validation Points

- section order
- total row wording
- note row wording
- vertical merge map in appendix table
- page break before appendix

## Recommended Fix Layers

- Wrong values: report model or data mapping
- Wrong static headers: template
- Wrong dynamic merges: post-process or XML inspection
- Wrong page behavior after conversion: PDF validation and conversion layer
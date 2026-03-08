# Reference Artifact Ingestion

This document answers one question only: which artifacts should the AI agent read, and what should each artifact be used for.

## Priority Order

1. approved DOCX
2. PDF exported from that DOCX
3. unpacked DOCX or XML parts
4. redacted structural notes
5. screenshots or side-by-side review images
6. verbal description

The lower you go on the list, the more the agent has to guess.

## What Each Artifact Is For

- Approved DOCX  
	Use it for section order, headings, visible tables, total rows, note rows, and fixed wording.

- Reference PDF  
	Use it for page breaks, spacing drift, width drift, overflow, and final visual parity.

- Unpacked DOCX XML  
	Use it for grid structure, vertical merges, horizontal merges, and other Word-specific details.

- Structural notes  
	Use them to clarify constraints that are not obvious from the files alone.

- Screenshots  
	Use them to highlight obvious visual differences, not as the primary source of truth.

- Verbal description  
	Use it only as supporting context when better artifacts cannot be shared.

## Recommended Minimum Package

Whenever possible, give the agent:

- the approved DOCX
- the PDF exported from that DOCX
- the unpacked DOCX or XML when merge behavior matters

## What The Agent Must Write Down After Reading Artifacts

- section order
- heading hierarchy
- table inventory
- table schema
- merge maps
- mandatory total rows
- mandatory note rows
- typography and spacing rules
- page rules

If the agent cannot write those down, it does not yet understand the source of truth well enough.
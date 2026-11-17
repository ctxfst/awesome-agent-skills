---
skill: pdf
source: openai/skills
path: skills/.curated/pdf
commit: 49f948faa9258a0c61caceaf225e179651397431
url: https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/pdf
license: Apache-2.0
description: Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction.
trust: T1
has_scripts: false
network: false
needs_secrets: false
---

# Create or review a PDF with rendered visual verification

## When
Use when reading, creating, or reviewing PDFs where rendering, layout, and visual quality matter, or when programmatically creating a PDF with reliable formatting.

## Material
An input PDF or content for a new PDF, plus the requested review or generation requirements. Intermediate files go under tmp/pdfs/ and final repository artifacts under output/pdf/.

## Done
The final PDF or review has been checked against newly rendered PNG pages, with zero remaining visual or formatting defects, polished typography and spacing, readable citations, and clean intermediate files.

## Requires
reportlab for generation, pdfplumber or pypdf for extraction and quick checks, and Poppler for rendering. uv is preferred for Python dependency installation; no environment variables are required.

## Replaces
missing

## Not for
missing

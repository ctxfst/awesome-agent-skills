---
skill: pdf
source: anthropics/skills
path: skills/pdf
commit: e4bb5d960d87126ff3b3a8af1a104b7db67560ba
url: https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/pdf
license: Apache-2.0
description: >-
  Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
trust: T1
has_scripts: false
network: false
needs_secrets: false
---

# Transform and inspect PDF files with programmatic tools

## When
Use for PDF reading or extraction, merging, splitting, page rotation, watermarks, creation, form filling, encryption or decryption, image extraction, and OCR of scanned PDFs.

## Material
One or more PDF files and the requested operation. Scanned PDFs can be converted to images for OCR; form-filling work uses the bundled FORMS.md instructions.

## Done
The requested PDF output, extracted text or tables, images, or metadata is produced using the documented operation.

## Requires
Python libraries such as pypdf, pdfplumber, and reportlab; Poppler, qpdf, or pdftk for the relevant command-line operations; and pytesseract with pdf2image for OCR. Advanced operations use REFERENCE.md and forms use FORMS.md.

## Replaces
missing

## Not for
missing

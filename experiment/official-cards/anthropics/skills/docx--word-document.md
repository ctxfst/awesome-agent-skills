---
skill: docx
source: anthropics/skills
path: skills/docx
commit: e4bb5d960d87126ff3b3a8af1a104b7db67560ba
url: https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/docx
license: Apache-2.0
description: >-
  Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.
trust: T1
has_scripts: true
network: false
needs_secrets: false
---

# Create, edit, or analyze Word documents and templates

## When
Use when creating, reading, editing, or manipulating .docx or .dotx files, including professional formatting, content extraction, image replacement, find-and-replace, tracked changes, and comments.

## Material
A new document specification or an existing Word document or template. Legacy .doc files must first be converted to .docx.

## Done
A new or edited Word document, extracted content, or analysis. New documents are rendered and visually inspected; edited packages can be schema-validated, with tracked changes checked against the original when redlining.

## Requires
The npm docx package for new documents, pandoc for reading, direct OOXML editing for existing documents, and the bundled scripts. LibreOffice and Poppler are used for conversion and rendered verification.

## Replaces
missing

## Not for
PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation. For PDF work, use the `anthropics/skills/pdf--transform` card; for spreadsheet deliverables, use the `anthropics/skills/xlsx--spreadsheet` card.

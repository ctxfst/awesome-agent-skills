---
skill: xlsx
source: anthropics/skills
path: skills/xlsx
commit: e4bb5d960d87126ff3b3a8af1a104b7db67560ba
url: https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/xlsx
license: Apache-2.0
description: >-
  Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like "the xlsx in my downloads") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.
trust: T1
has_scripts: true
network: false
needs_secrets: false
---

# Create, repair, or analyze a spreadsheet file

## When
Use when a spreadsheet file is the primary input or output, including editing existing workbooks, creating spreadsheets, cleaning tabular data, formulas, formatting, charts, and tabular format conversion.

## Material
An existing .xlsx, .xlsm, .xltx, .csv, or .tsv file, source data, or a specification for a new spreadsheet. The final deliverable must be a spreadsheet file.

## Done
A spreadsheet following the requested tabs, headers, formulas, and conventions, with professional formatting, documented assumptions, and no reported formula errors after mandatory recalculation when formulas are present.

## Requires
openpyxl, pandas, and markitdown, with LibreOffice and the bundled recalc.py script for formula recalculation. Existing workbook conventions and formulas must be preserved.

## Replaces
missing

## Not for
A Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration as the primary deliverable. For Word output, use docx-document-processing.

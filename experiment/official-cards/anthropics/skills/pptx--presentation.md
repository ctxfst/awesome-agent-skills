---
skill: pptx
source: anthropics/skills
path: skills/pptx
commit: e4bb5d960d87126ff3b3a8af1a104b7db67560ba
url: https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/pptx
license: Apache-2.0
description: >-
  Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx or .potx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates (.potx), layouts, speaker notes, or comments. Trigger whenever the user mentions "deck," "slides," "presentation," or references a .pptx or .potx filename, regardless of what they plan to do with the content afterward. If a .pptx or .potx file needs to be opened, created, or touched, use this skill.
trust: T1
has_scripts: true
network: false
needs_secrets: false
---

# Create, edit, or analyze PowerPoint decks and templates

## When
Use whenever a .pptx or .potx file is input, output, or both, including new decks, content extraction, edits, slide splitting or combining, templates, layouts, speaker notes, and comments.

## Material
A presentation brief or existing deck or template, including its purpose, audience, content, and any required theme or layouts. Legacy .ppt files must first be converted to .pptx.

## Done
A deck or extracted slide content that passes content QA, file validation, and visual inspection of every slide. Template-derived decks are validated against the original template.

## Requires
pptxgenjs for new decks, bundled slide and OOXML scripts, python-pptx and related Python packages, LibreOffice, and Poppler for rendering. New decks use themes, layouts, placeholders, and sections unless the user requests a throwaway deck.

## Replaces
missing

## Not for
missing

---
skill: canvas-design
source: anthropics/skills
path: skills/canvas-design
commit: e4bb5d960d87126ff3b3a8af1a104b7db67560ba
url: https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/canvas-design
license: Apache-2.0
description: Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations.
trust: T1
has_scripts: false
network: true
needs_secrets: false
---

# Create an original static poster or visual artwork from a design philosophy

## When
Use when the user asks for a poster, piece of art, design, or another static visual piece.

## Material
A subtle input or instructions from the user, used as a foundation without eliminating creative freedom.

## Done
A design philosophy in a Markdown file and its visual expression as a downloadable PDF or PNG. The default is one highly visual page; additional pages are supported when requested.

## Requires
The instructions permit only Markdown, PDF, and PNG outputs, direct access to the bundled canvas-fonts directory, and downloading fonts when needed. Text and graphics must remain within canvas boundaries.

## Replaces
missing

## Not for
Do not use it to copy an existing artist's work. For code-driven interactive generative art rather than a static piece, use the `anthropics/skills/algorithmic-art--generative-art` card.

---
skill: github-issue-creator
source: microsoft/skills
path: .github/skills/github-issue-creator
commit: b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb
url: https://github.com/microsoft/skills/tree/b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb/.github/skills/github-issue-creator
license: MIT
description: Convert raw notes, error logs, voice dictation, or screenshots into crisp GitHub-flavored markdown issue reports. Use when the user pastes bug info, error messages, or informal descriptions and wants a structured GitHub issue. Supports images/GIFs for visual evidence.
trust: T1
has_scripts: false
network: false
needs_secrets: false
---

# Turn messy bug notes into a structured Markdown issue

## When
Use when raw notes, error logs, voice dictation, screenshots, or informal bug descriptions need to become a crisp GitHub-flavored Markdown issue report.

## Material
Bug facts, environment details, reproduction evidence, error messages, and optional images or GIFs. Conversation or memory can supply context for references such as "same project."

## Done
A concise Markdown file named YYYY-MM-DD-short-description.md in the repository's /issues/ directory, containing summary, environment, reproduction steps, expected and actual behavior, error details, visual evidence, impact, and additional context.

## Requires
Write access to the repository's /issues/ directory and any attachments referenced by the report. Sensitive values are replaced with placeholders.

## Replaces
Unstructured voice notes, casual descriptions, and raw error pastes that bury actionable bug facts.

## Not for
missing

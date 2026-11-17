---
skill: security-best-practices
source: openai/skills
path: skills/.curated/security-best-practices
commit: 49f948faa9258a0c61caceaf225e179651397431
url: https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-best-practices
license: Apache-2.0
description: Perform language and framework specific security best-practice reviews and suggest improvements. Trigger only when the user explicitly requests security best practices guidance, a security review/report, or secure-by-default coding help. Trigger only for supported languages (python, javascript/typescript, go). Do not trigger for general code review, debugging, or non-security tasks.
trust: T1
has_scripts: false
network: true
needs_secrets: false
---

# Produce a prioritized language-specific security best-practices report

## When
Use when the user explicitly requests a security review or vulnerability report for Python, JavaScript or TypeScript, or Go code.

## Material
The codebase, its frontend and backend languages and frameworks, all matching bundled security references, and a destination for the report if the user provides one.

## Done
A Markdown security_best_practices_report.md or user-specified report with an executive summary, numbered findings organized by severity, impact statements for critical findings, code line references, and a direct summary to the user.

## Requires
Access to the reviewed code and all relevant bundled reference files. Concrete guidance limitations must be disclosed when no matching reference exists; online documentation search is permitted in that case.

## Replaces
missing

## Not for
General code review, debugging, non-security tasks, or unsupported languages. For secure-by-default implementation without a requested report, use the `openai/skills/security-best-practices--secure-code` card.

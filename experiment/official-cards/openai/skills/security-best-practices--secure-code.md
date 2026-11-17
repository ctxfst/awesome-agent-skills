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

# Apply language-specific security practices while writing or changing code

## When
Use when the user explicitly requests secure-by-default coding help or security best-practice guidance for Python, JavaScript or TypeScript, or Go.

## Material
The project or planned code, its languages and frameworks, and every relevant bundled security reference for the identified frontend and backend stacks.

## Done
New or changed code follows the applicable security references, with major deviations or critical vulnerabilities flagged to the user and regression checks performed for any fixes.

## Requires
Identification of all in-scope languages and frameworks and loading of all matching bundled reference files. Online documentation search is permitted when relevant bundled guidance is unavailable.

## Replaces
missing

## Not for
General code review, debugging, non-security tasks, or languages outside the documented Python, JavaScript or TypeScript, and Go scope. For a prioritized written vulnerability report, use the `openai/skills/security-best-practices--security-report` card.

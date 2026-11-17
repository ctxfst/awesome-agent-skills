---
skill: microsoft-docs
source: microsoft/skills
path: .github/skills/microsoft-docs
commit: b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb
url: https://github.com/microsoft/skills/tree/b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb/.github/skills/microsoft-docs
license: MIT
description: Understand Microsoft technologies by querying official documentation. Use whenever the user asks how something works, wants tutorials, needs configuration options, limits, quotas, or best practices for any Microsoft technology (Azure, .NET, M365, Windows, Power Platform, etc.)—even if they don't mention "docs." If the question is about understanding a concept rather than writing code, this is the right skill.
trust: T1
has_scripts: false
network: true
needs_secrets: false
---

# Answer Microsoft technology questions from current official documentation

## When
Use for Microsoft technology concepts, tutorials, configuration options, limits, quotas, and best practices across Azure, .NET, Microsoft 365, Windows, Power Platform, and related products.

## Material
A specific Microsoft technology question with relevant version, task intent, and platform context. Full pages can be fetched when search excerpts are insufficient.

## Done
An answer grounded in live official Microsoft documentation, with complete tutorial steps or configuration details fetched when excerpts are incomplete.

## Requires
Network access and the Microsoft Learn MCP server, or the mslearn CLI through npx as a fallback. No credentials are documented for public documentation queries.

## Replaces
Relying on potentially outdated training data when current official documentation is available.

## Not for
missing

---
skill: frontend-design-review
source: microsoft/skills
path: .github/skills/frontend-design-review
commit: b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb
url: https://github.com/microsoft/skills/tree/b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb/.github/skills/frontend-design-review
license: MIT
description: >-
  Review and create distinctive, production-grade frontend interfaces with high design quality and design system compliance. Evaluates using three pillars: frictionless insight-to-action, quality craft, and trustworthy building. USE FOR: PR reviews, design reviews, accessibility audits, design system compliance checks, creative frontend design, UI code review, component reviews, responsive design checks, theme testing, and creating memorable UI. DO NOT USE FOR: Backend API reviews, database schema reviews, infrastructure or DevOps work, pure business logic without UI, or non-frontend code.
trust: T1
has_scripts: false
network: true
needs_secrets: false
---

# Review an existing UI for design quality and design-system compliance

## When
Use for PR reviews, design reviews, accessibility audits, design-system compliance checks, UI code reviews, component reviews, responsive checks, and theme testing of an existing frontend.

## Material
The existing UI implementation, its user task and review scope, the applicable design system and component library, Figma specifications when available, and the bundled review references.

## Done
Prioritized blocking, major, or minor findings with recommendations and design-system examples, covering task flow, design-system compliance, aesthetic craft, accessibility, AI transparency, and error transparency.

## Requires
The design review, review-type modifier, quick checklist, and pattern references. Design-system comparisons use Storybook or the component library and Figma Dev Mode for exact specifications.

## Replaces
missing

## Not for
Backend API reviews, database schema reviews, infrastructure or DevOps work, pure business logic without UI, or non-frontend code. For creating a new interface rather than reviewing one, use the `anthropics/skills/frontend-design--distinctive-ui` or `microsoft/skills/frontend-design-review--creative-ui` card.

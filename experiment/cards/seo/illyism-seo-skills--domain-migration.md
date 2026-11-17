---
skill: domain-migration
source: Illyism/seo-skills
path: seo/domain-migration
commit: 99d51a33db135cf278c7e61cf3dd1b502e2390b4
url: https://github.com/Illyism/seo-skills/tree/99d51a33db135cf278c7e61cf3dd1b502e2390b4/seo/domain-migration
license: missing
description: Executes a domain rebrand, subdomain-to-subfolder merge, or blog URL consolidation with zero ranking loss, shipping a verified 1-to-1 redirect config, `scripts/verify-redirects.sh`, canonical and schema cutover edits, and `seo/backlink-transfer-emails.md` outreach drafts. Use when the user is changing domains, rebranding, moving `blog.` to `/blog`, merging sites, renaming URL slugs in bulk, or asks how to migrate without losing SEO traffic.
trust: T3
category: seo
has_scripts: true
network: true
needs_secrets: false
---

# Domain Migration

## When
Executes a domain rebrand, subdomain-to-subfolder merge, or blog URL consolidation with zero ranking loss, shipping a verified 1-to-1 redirect config, `scripts/verify-redirects.sh`, canonical and schema cutover edits, and `seo/backlink-transfer-emails.md` outreach drafts. Use when the user is changing domains, rebranding, moving `blog.` to `/blog`, merging sites, renaming URL slugs in bulk, or asks how to migrate without losing SEO traffic.

## Material
Executes a domain rebrand, subdomain-to-subfolder merge, or blog URL consolidation with zero ranking loss, shipping a verified 1-to-1 redirect config, `scripts/verify-redirects.sh`, canonical and schema cutover edits, and `seo/backlink-transfer-emails.md` outreach drafts.

## Done
Every run ends with:

1. `seo/url-inventory.csv` and `seo/redirect-map.csv`.
2. The redirect config for the user's host (Next.js `redirects()`, Cloudflare Bulk Redirects CSV, or Nginx map), committed to the working tree.
3. `scripts/verify-redirects.sh`, with its output pasted in chat showing `0 failed` (or the failing rows fixed).
4. Base URL, sitemap, hreflang, `Organization` schema, and `/about` edits.
5. `seo/backlink-transfer-emails.md` with 30-50 personalized drafts. Never send them.

## Requires
missing

## Replaces
missing

## Not for
missing

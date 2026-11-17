---
skill: redesign-screen
source: mobbin/skills
path: skills/redesign-screen
commit: cac338357d596415773874f06a6c16e862c195e4
url: https://github.com/mobbin/skills/tree/cac338357d596415773874f06a6c16e862c195e4/skills/redesign-screen
license: MIT
description: Redesign any screen from patterns real apps ship. Share a screenshot, your code or a design file, and the skill finds how apps on Mobbin handle the same screen. Explore a few directions or fix specific problems, and see the evidence behind each change. You get a before and after image and a short report. The redesign stays in your own design system, and anything that already works is kept. Use whenever the user points at a screen, section, or component they have, or at a reference, a Mobbin result, one or more Mobbin collections or the screens they saved, and asks to redesign, improve, restyle, or rebuild it, or to see a few directions for it.
trust: T3
category: frontend-design
has_scripts: true
network: false
needs_secrets: true
---

# Redesign a screen from a reference

## When
Redesign any screen from patterns real apps ship. Share a screenshot, your code or a design file, and the skill finds how apps on Mobbin handle the same screen. Explore a few directions or fix specific problems, and see the evidence behind each change. You get a before and after image and a short report. The redesign stays in your own design system, and anything that already works is kept. Use whenever the user points at a screen, section, or component they have, or at a reference, a Mobbin result, one or more Mobbin collections or the screens they saved, and asks to redesign, improve, restyle, or rebuild it, or to see a few directions for it.

## Material
The user brings a target in whatever form they have it: a codebase the working directory renders, an image, a design file, a live page, or whatever a connected tool exposes. That form is the **source**. Read it with whatever the environment offers, then treat every source alike: a region, elements, visible states, a palette, a type and spacing scale, and the design system those imply. The form decides only how the region is named, where the states come from, and the form the render goes back in.

They may also bring their words (a complaint, a goal, a constraint, a look) and a reference of their own (a screenshot, a Mobbin link, a product name), which sets what the redesign aims at, with Mobbin screens still locked beside it so the result is not a copy of one product. Mobbin supplies the references through `search_screens`, `search_sections` and `search_flows`; when they are not connected, say so in one line and stop, since the skill does not run on memory.

A **collection** the user names, links or points at ("my saved screens", "my checkout and paywall collections", "the screens I saved from Duolingo") is the evidence they chose. It is read with `list_collections` and `get_collection_contents` in place of a search, and the run stays inside it unless the user says otherwise, as [references/collections.md](references/collections.md) sets out.

## Done
The render goes back in the form the source came in:

| Source | Render |
|--------|--------|
| A codebase | edits to the source |
| A design file | a new frame beside the original, written with the design tool's own tools, so the baseline survives |
| A design file the tool can only read | a captured mockup in the product's own palette, type and spacing, said once at scoping |
| An image | a PNG |
| Anything else | the nearest of the three, said at scoping |

Check that a frame can be written before promising one, since most design-tool connections only read. In explore mode every source renders as mockups first, and the table applies to the variation the user picks.

The reply leads with the before and after image (step 7) when the render can be captured, then the report and the closing menu (step 8). The reference board and the list of references come only when asked.

## Requires
missing

## Replaces
missing

## Not for
missing

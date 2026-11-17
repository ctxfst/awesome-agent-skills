---
skill: algorithmic-art
source: anthropics/skills
path: skills/algorithmic-art
commit: e4bb5d960d87126ff3b3a8af1a104b7db67560ba
url: https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/algorithmic-art
license: Apache-2.0
description: Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.
trust: T1
has_scripts: false
network: true
needs_secrets: false
---

# Create interactive p5.js generative art with reproducible seeds

## When
Use when the user requests art created with code, generative or algorithmic art, flow fields, or particle systems with interactive parameter exploration.

## Material
A subtle conceptual input from the user and the bundled viewer template, which must be read and used as the starting point.

## Done
An algorithmic philosophy and p5.js artwork with seeded randomness, working parameter controls, seed navigation, regeneration, reset, and PNG download, delivered in the documented HTML and JavaScript artifact form.

## Requires
The bundled viewer template, p5.js loaded from the documented CDN, and an environment such as a browser or Claude artifact that can run the resulting HTML. The same seed must reproduce the same output.

## Replaces
missing

## Not for
Do not use it to copy an existing artist's work or to make only a static image without the algorithmic process. For a static PDF or PNG art object, use the `anthropics/skills/canvas-design--static-art` card.

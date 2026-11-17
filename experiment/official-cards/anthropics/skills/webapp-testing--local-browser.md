---
skill: webapp-testing
source: anthropics/skills
path: skills/webapp-testing
commit: e4bb5d960d87126ff3b3a8af1a104b7db67560ba
url: https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/webapp-testing
license: Apache-2.0
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
trust: T1
has_scripts: true
network: false
needs_secrets: false
---

# Test and debug a local web application in a browser

## When
Use for verifying local frontend functionality, debugging UI behavior, capturing browser screenshots, inspecting rendered DOM state, and viewing browser logs.

## Material
A static HTML file or local dynamic web application, its server command and port when applicable, and the user flow or behavior to inspect.

## Done
Playwright automation has inspected the rendered application and performed the requested interactions, with screenshots, DOM evidence, or browser logs captured as needed.

## Requires
Python Playwright and Chromium. Dynamic apps must reach the networkidle state before DOM inspection; the bundled with_server.py helper can manage one or more local servers.

## Replaces
missing

## Not for
missing

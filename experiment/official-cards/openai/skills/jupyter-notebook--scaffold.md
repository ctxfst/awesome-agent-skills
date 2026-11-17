---
skill: jupyter-notebook
source: openai/skills
path: skills/.curated/jupyter-notebook
commit: 49f948faa9258a0c61caceaf225e179651397431
url: https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/jupyter-notebook
license: Apache-2.0
description: Use when the user asks to create, scaffold, or edit Jupyter notebooks (`.ipynb`) for experiments, explorations, or tutorials; prefer the bundled templates and run the helper script `new_notebook.py` to generate a clean starting notebook.
trust: T1
has_scripts: true
network: false
needs_secrets: false
---

# Scaffold a clean Jupyter notebook for an experiment or tutorial

## When
Use when creating a new .ipynb notebook from scratch or converting rough notes or scripts into a structured experiment, exploration, or tutorial.

## Material
The notebook kind, title, objective, audience, expected finished state, and the bundled experiment or tutorial template.

## Done
A structured .ipynb with the requested title, small runnable steps, explanatory Markdown cells, and a final validation checklist. The notebook is run top-to-bottom when the environment allows, with any inability to execute disclosed.

## Requires
Python 3.12 through the documented uv command, the bundled new_notebook.py helper and templates, and write access to the output path. The scaffold script uses only the Python standard library; JupyterLab and ipykernel are optional for local execution.

## Replaces
Hand-authoring raw notebook JSON to create a clean starting notebook.

## Not for
Work that does not involve creating or editing Jupyter .ipynb notebooks.

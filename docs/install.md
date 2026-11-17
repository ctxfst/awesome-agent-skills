# Installing `find-skill/` Across Coding Agents

This guide explains how to install the `find-skill/` skill folder from this repository into AI coding agents that support the `SKILL.md` Agent Skills format.

Each command below assumes your current working directory is the root of your cloned `awesome-agent-skills` repository (so `$(pwd)/find-skill` resolves to the absolute path of `find-skill/`). A symlink lets `find.py` locate the repository's catalog and index regardless of the directory where your agent is working.

If you copy `find-skill/` instead of symlinking it, keep the full repository clone and set `SKILL_FINDER_ROOT` to its absolute path in the agent's environment:

```bash
export SKILL_FINDER_ROOT="/absolute/path/to/awesome-agent-skills"
```

A copied Skill folder by itself does not contain the catalog or index. Without a working symlink or `SKILL_FINDER_ROOT`, `find.py` will stop with an installation error.

## Summary Table

| Agent | `SKILL.md` Support | User-Level Directory | Project-Level Directory | Official Documentation |
| --- | --- | --- | --- | --- |
| Claude Code | Supported | `~/.claude/skills/` | `.claude/skills/` | [Claude Code Skills](https://code.claude.com/docs/en/skills) |
| Codex CLI | Supported | `~/.agents/skills/` | `.agents/skills/` | [Codex Skills](https://developers.openai.com/codex/skills) |
| Gemini CLI | Supported | `~/.gemini/skills/` (or `~/.agents/skills/`) | `.gemini/skills/` (or `.agents/skills/`) | [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/skills/) |
| Cursor | Supported | `~/.cursor/skills/` (or `~/.agents/skills/`) | `.cursor/skills/` (or `.agents/skills/`) | [Cursor Agent Skills](https://cursor.com/docs/skills) |
| GitHub Copilot | Supported | `~/.copilot/skills/` (or `~/.agents/skills/`) | `.github/skills/` (or `.agents/skills/`, `.claude/skills/`) | [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) |
| Kimi Code | Supported | `~/.kimi/skills/` (or `~/.config/agents/skills/`) | `.kimi/skills/` (or `.agents/skills/`) | [Kimi Code CLI Agent Skills](https://moonshotai.github.io/kimi-cli/en/customization/skills.html) |
| Kilo | Supported | `~/.kilo/skills/` (or `~/.agents/skills/`) | `.kilo/skills/` (or `.agents/skills/`) | [Kilo Agent Skills](https://kilo.ai/docs/customize/skills) |

---

## Agent-by-Agent Instructions

### 1. Claude Code

- **Format support:** Supported (`SKILL.md` Agent Skills standard).
- **Skill directory locations:**
  - Personal (all projects): `~/.claude/skills/find-skill/`
  - Project-level (single repository): `.claude/skills/find-skill/`
- **One-line install (user-level symlink):**

```bash
mkdir -p ~/.claude/skills && ln -s "$(pwd)/find-skill" ~/.claude/skills/find-skill
```

- **Official documentation:** https://code.claude.com/docs/en/skills

---

### 2. Codex CLI

- **Format support:** Supported (`SKILL.md` Agent Skills standard).
- **Skill directory locations:**
  - User-level: `$HOME/.agents/skills/find-skill/` (`~/.agents/skills/find-skill/`)
  - Repository-level: `.agents/skills/find-skill/` (scanned from `$CWD/.agents/skills` up to `$REPO_ROOT/.agents/skills`)
  - Admin-level: `/etc/codex/skills/find-skill/`
- **One-line install (user-level symlink):**

```bash
mkdir -p ~/.agents/skills && ln -s "$(pwd)/find-skill" ~/.agents/skills/find-skill
```

- **Official documentation:** https://developers.openai.com/codex/skills (redirects to https://learn.chatgpt.com/docs/build-skills)

---

### 3. Gemini CLI

- **Format support:** Supported (`SKILL.md` Agent Skills standard).
- **Skill directory locations:**
  - User-level: `~/.gemini/skills/find-skill/` (or alias `~/.agents/skills/find-skill/`)
  - Workspace-level: `.gemini/skills/find-skill/` (or alias `.agents/skills/find-skill/`)
- **One-line install (user-level symlink):**

```bash
mkdir -p ~/.gemini/skills && ln -s "$(pwd)/find-skill" ~/.gemini/skills/find-skill
```

- **Alternative CLI command (documented by Gemini CLI):** `gemini skills link "$(pwd)/find-skill"`
- **Official documentation:** https://geminicli.com/docs/cli/skills/

---

### 4. Cursor

- **Format support:** Supported (`SKILL.md` Agent Skills standard).
- **Skill directory locations:**
  - User-level: `~/.cursor/skills/find-skill/` or `~/.agents/skills/find-skill/` (also scans `~/.claude/skills/` and `~/.codex/skills/` for compatibility)
  - Project-level: `.cursor/skills/find-skill/` or `.agents/skills/find-skill/` (also scans `.claude/skills/` and `.codex/skills/`)
- **One-line install (user-level symlink):**

```bash
mkdir -p ~/.cursor/skills && ln -s "$(pwd)/find-skill" ~/.cursor/skills/find-skill
```

- **Official documentation:** https://cursor.com/docs/skills

---

### 5. GitHub Copilot

- **Format support:** Supported (`SKILL.md` Agent Skills standard).
- **Skill directory locations:**
  - Personal (user-level): `~/.copilot/skills/find-skill/` or `~/.agents/skills/find-skill/`
  - Project-level (repository): `.github/skills/find-skill/`, `.claude/skills/find-skill/`, or `.agents/skills/find-skill/`
- **One-line install (user-level symlink):**

```bash
mkdir -p ~/.copilot/skills && ln -s "$(pwd)/find-skill" ~/.copilot/skills/find-skill
```

- **Official documentation:** https://docs.github.com/en/copilot/concepts/customizations/agent-skills

---

### 6. Kimi Code

- **Format support:** Supported (`SKILL.md` Agent Skills standard).
- **Skill directory locations:**
  - User-level: `~/.kimi/skills/find-skill/` (brand group; also scans `~/.claude/skills/` and `~/.codex/skills/`), or generic `~/.config/agents/skills/find-skill/` (recommended) / `~/.agents/skills/find-skill/`
  - Project-level: `.kimi/skills/find-skill/` (or `.claude/skills/`, `.codex/skills/`, `.agents/skills/`)
- **One-line install (user-level symlink):**

```bash
mkdir -p ~/.kimi/skills && ln -s "$(pwd)/find-skill" ~/.kimi/skills/find-skill
```

- **Official documentation:** https://moonshotai.github.io/kimi-cli/en/customization/skills.html

---

### 7. Kilo

- **Format support:** Supported (`SKILL.md` Agent Skills open standard).
- **Skill directory locations:**
  - User-level: `~/.kilo/skills/find-skill/` or `~/.agents/skills/find-skill/` (open standard, loaded by default; optionally `~/.claude/skills/` when Claude Code compatibility is enabled)
  - Project-level: `.kilo/skills/find-skill/` or `.agents/skills/find-skill/` (optionally `.claude/skills/`)
- **One-line install (user-level symlink):**

```bash
mkdir -p ~/.kilo/skills && ln -s "$(pwd)/find-skill" ~/.kilo/skills/find-skill
```

- **Official documentation:** https://kilo.ai/docs/customize/skills

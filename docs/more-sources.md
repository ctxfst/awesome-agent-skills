# Skill List Source Investigation

*Verified on 2026-11-18.*

## 1. Website Source Evaluation

### A. Awesome Skills Marketplace

- **Status:** Found (`https://awesomeskill.ai/`, titled *"Awesome Skills - Agent Skills Marketplace for Claude, Codex & ChatGPT"*).
  - *Note:* Another similarly named site, **SkillsMP** (`https://skillsmp.com/`, titled *"Agent Skills Marketplace | Codex & Claude Skills | SkillsMP"*), is documented separately below for disambiguation.
- **Can it be used as a Skill list source?** **Not directly recommended for automated ingestion.** Its Terms of Service explicitly prohibit automated data extraction/scraping, and it provides no documented public JSON catalog or REST API.
- **Public GitHub repo behind the website:** None found. Neither the site HTML nor its legal pages link to a public source repository for the directory platform itself.
- **Downloadable data (JSON, API):**
  - No public REST API or bulk JSON catalog found (`/api/skills` returns HTTP 404).
  - Serves an XML sitemap (`https://awesomeskill.ai/sitemap.xml`) listing 1,000 `/skill/...` URLs (as checked on 2026-11-18).
  - Individual skill pages expose CDN links to per-skill files such as `https://cdn.awesomeskill.ai/skills/<slug>/SKILL.md` and `.zip` archives.
- **License / Terms of Service:**
  - Website Terms (`https://awesomeskill.ai/terms`) state under *Acceptable Use* that users must not *"Use automated systems or software to extract data from our website (scraping)"*, and assert intellectual property ownership over website content and features.
  - Indexed skills originate from third-party GitHub repositories and remain subject to their upstream repository licenses.
- **Do its skills link back to GitHub repos?** **Yes.** All 16 sampled skill pages (`6/6` initial + `10/10` from the sitemap) linked directly back to an upstream `https://github.com/<owner>/<repo>/tree/...` URL.

*(Disambiguation — SkillsMP: `https://skillsmp.com/`)*
- **Public GitHub repo behind the website:** None found.
- **Downloadable data (JSON, API):** Offers a documented REST API (`GET /api/v1/skills/search` at `https://skillsmp.com/docs/api`) returning JSON search results. Anonymous access is capped at 50 requests/day and 10 requests/min (keyword search only); higher allowances require an account API key (Free: 50/day, Standard: 5,000/month, Professional: 25,000/month). Wildcard queries are unsupported.
- **License / Terms of Service:** `https://skillsmp.com/terms` states indexed skills come from public GitHub repositories under their respective licenses and prohibits scraping or systematically downloading large portions of the site.
- **Do its skills link back to GitHub repos?** Yes; sampled skill pages (e.g., `https://skillsmp.com/creators/1shot-api/skills/1shot-wallet`) link directly to the source GitHub repository and `SKILL.md` blob.

---

### B. Claude Skills & Agent Skills Library

- **Status:** **Uncertain (no single website found with the exact verbatim name *"Claude Skills & Agent Skills Library"*).**
  - Web searches and direct domain checks did not locate a live website whose exact title or brand name is *"Claude Skills & Agent Skills Library"*. Below are the verified facts for the closest matching websites discovered during investigation:

#### Candidate 1: Skills Library (`https://skills-library.com/`)
- **Title:** *"Skills Library — Find the perfect superpowers for your AI"* (indexes 105,288 skills sourced from `skills.sh` and GitHub).
- **Can it be used as a Skill list source?** **Yes** — open-source codebase, MIT-licensed, and provides full downloadable JSON catalogs.
- **Public GitHub repo behind the website:** Yes — [`Zaz-OS/skills-library`](https://github.com/Zaz-OS/skills-library) (1 star, last pushed 2026-03-05).
- **Downloadable data (JSON, API):** Yes — documented at `https://skills-library.com/llms.txt`:
  - Full JSON catalog: `https://skills-library.com/api/skills.json` (verified HTTP 200; JSON array of 5,959 enriched skill records with `repoUrl`, `githubStars`, `installs`, `license`, `dependencies`).
  - Dependencies index: `https://skills-library.com/api/deps.json`.
- **License / Terms of Service:** The platform repository `Zaz-OS/skills-library` is licensed under the **MIT License** (`https://github.com/Zaz-OS/skills-library/blob/main/LICENSE`). Dedicated `/terms` and `/privacy` routes on the site fall back to the main Astro page; individual skills carry their upstream repository license metadata.
- **Do its skills link back to GitHub repos?** **Yes.** In `https://skills-library.com/api/skills.json`, all `5,959 / 5,959` entries include a `repoUrl` pointing to `https://github.com/...`, and sampled skill pages (e.g., `https://skills-library.com/skill/obra/superpowers/brainstorming`) link to the upstream GitHub repo.

#### Candidate 2: ClaudeSkills (`https://www.claudeskills.org/`)
- **Title:** *"Discover Agent Skills for Your Next Workflow | ClaudeSkills"*.
- **Can it be used as a Skill list source?** **Partially / with caution** — exposes JSON endpoints, but its `robots.txt` disallows `/api/` and its Terms assert platform IP ownership.
- **Public GitHub repo behind the website:** None found.
- **Downloadable data (JSON, API):**
  - `https://www.claudeskills.org/api/skills` returns a JSON list of 83 items (as of 2026-11-18), and `/api/registry/<slug>/raw` serves raw `SKILL.md` text.
  - Note: `https://www.claudeskills.org/robots.txt` explicitly includes `Disallow: /api/`.
- **License / Terms of Service:** `https://www.claudeskills.org/terms` describes it as a commercial SaaS platform owning its original content and features; third-party skills retain their upstream licenses.
- **Do its skills link back to GitHub repos?** **Not all.** Out of 83 items in `/api/skills`: 75 link to GitHub repositories (`sourceUrl` containing `github.com/`), 7 are first-party skills (`first-party:*` linking to `/creators/claudeskills`), and 1 links to `https://developers.openai.com/codex/skills`.

#### Candidate 3: ClaudeSkills Waitlist (`https://www.claudeskills.com/`)
- **Title:** *"ClaudeSkills - The Curated Library of Claude Code Skills"*.
- **Can it be used as a Skill list source?** **No.** Inspection of its frontend bundle (`/assets/index-CzX4pDUv.js`) shows it is currently a pre-launch waitlist page (*"We'll notify you when the skills library launches"*) with no public skill index, API, or GitHub links.

#### Candidate 4: AI Agents Library (`https://www.aiagentslibrary.com/`)
- **Title:** *"AI Agents Library | Free, Done-For-You AI Agent Skills"* (metadata title also reads *"AI Agents Library: Gemini Spark & Claude Skills"*).
- **Can it be used as a Skill list source?** **No** (for `SKILL.md` GitHub indexing). It hosts no-code prompt/workflow guides rather than GitHub-hosted `SKILL.md` packages, has no public GitHub repo or JSON/API endpoint, and sampled pages contain no GitHub links.

---

## 2. Other GitHub Repositories Collecting `SKILL.md` Lists (Top 10)

All repository metrics below were verified via the GitHub REST API (`https://api.github.com/repos/<owner>/<repo>`) on **2026-11-18**.

| # | Repository | Stars | Last Pushed | Description |
| --- | --- | ---: | --- | --- |
| 1 | [anthropics/skills](https://github.com/anthropics/skills) | 196,655 | 2026-11-16 | Public repository for Agent Skills (official reference skills and spec) |
| 2 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 79,727 | 2026-09-18 | Curated list of awesome Claude Skills, resources, and tools |
| 3 | [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | 49,896 | 2026-11-17 | 2,955+ reusable AI agent skills for Claude Code, Codex, Cursor, and Gemini CLI |
| 4 | [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 37,293 | 2026-11-15 | Curated collection of 1,000+ agent skills from official dev teams and community |
| 5 | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 34,353 | 2026-11-12 | Vercel's official collection of agent skills (`SKILL.md` packages) |
| 6 | [openai/skills](https://github.com/openai/skills) | 28,801 | 2026-10-28 | Skills Catalog for Codex (`SKILL.md` packages) |
| 7 | [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | 15,855 | 2026-04-28 | Curated list of awesome Claude Skills, resources, and tools |
| 8 | [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills) | 10,445 | 2026-11-02 | Curated list of Claude Skills |
| 9 | [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) | 6,404 | 2026-11-09 | Tutorials, guides, and Agent Skills directories |
| 10 | [libukai/awesome-agent-skills](https://github.com/libukai/awesome-agent-skills) | 5,225 | 2026-10-25 | Guide and curated collection of Agent Skills and `SKILL.md` resources |

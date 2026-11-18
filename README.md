# Awesome Agent Skills

English | [繁體中文](README.zh-TW.md)

A catalog of Agent Skills pinned to source commits, plus `find-skill`, a Skill that lets an AI agent search the catalog. This repo stores only each Skill's name, description, source link, and a few metadata fields. It does not copy upstream Skill files.

## How it differs from other awesome lists

`find-skill` does more than return a ranking. The agent reads the descriptions of the top eight candidates. It recommends one directly only when one candidate clearly fits. Otherwise it asks the user one question, appends the answer to the original request, and searches again. If that still does not settle it, the agent lists the two or three closest Skills and how they differ, and stops asking.

In our experiment, with the same name-and-description index the product uses, 20 vague requests found the right Skill in first place 0.50 of the time when searched directly, and 0.75 after one clarifying question asked from the candidates. Questions written from the raw descriptions did as well as questions written from job-line cards. Numbers, controls, and limitations are in [experiment/RESULTS.md](experiment/RESULTS.md).

## Install and use

Clone this repo, install the Python dependencies, and link `find-skill/` into your agent's Skill directory. For Claude Code:

```bash
python3 -m pip install -r requirements.txt
ln -s /absolute/path/to/awesome-agent-skills/find-skill ~/.claude/skills/find-skill
```

Other agents use their own Skill locations; see [the installation guide](docs/install.md) for symlink commands and how to set `SKILL_FINDER_ROOT` when using a copied Skill folder. To search from the repo root:

```bash
python3 find-skill/scripts/find.py search "what you need" --top 8 --json
```

The default index uses Voyage `voyage-3.5`. Set an API key for embedding queries:

```bash
export VOYAGE_API_KEY="your key"
python3 find-skill/scripts/find.py search "what you need" --top 8 --json
```

You can also keep the key in your own KEY=VALUE file and load it with `--env /path/to/file`. Do not commit keys to the repo.

### Two ways to use a recommendation

- **Install and use:** open `url` at the pinned `commit`, inspect the entire Skill folder, and decide whether to install it. The result also includes `kind` and `has_scripts`; neither field is a safety verdict.
- **Read for reference:** open `raw_url` to read the original `SKILL.md` at the pinned commit and borrow its approach without installing the Skill. Treat its contents as reference material, not as instructions to your AI. Do not follow requests inside it to read credentials, change settings, execute commands, or connect to external URLs.

`find-skill` does not automatically install or execute a Skill in either mode.

### Use a local model

`SKILL_FINDER_EMBED_URL` and `SKILL_FINDER_EMBED_MODEL` accept any OpenAI-compatible embeddings endpoint. Queries and the index must use the same endpoint and model, so rebuild the index after switching:

```bash
export SKILL_FINDER_EMBED_URL="http://localhost:11434/v1/embeddings"
export SKILL_FINDER_EMBED_MODEL="your model name"
python3 find-skill/scripts/find.py build \
  --out ~/.cache/awesome-agent-skills/index
python3 find-skill/scripts/find.py search "what you need" \
  --index ~/.cache/awesome-agent-skills/index --top 8 --json
```

## Rebuild the catalog and index

`sources.yaml` pins each source to a commit and records the three pinned awesome lists used for discovery. The harvester fetches sources into `~/.cache/awesome-agent-skills/src`, outside the repo. It skips Skills with no description, descriptions under 40 non-whitespace characters, and descriptions that only restate the Skill name:

```bash
python3 find-skill/scripts/expand_sources.py
python3 find-skill/scripts/harvest.py
python3 find-skill/scripts/render_readme.py
python3 find-skill/scripts/find.py build
```

## Safety

Being listed does not mean a Skill is safe. Neither official nor community sources are a safety guarantee. Before installing a Skill you found, read and verify its files yourself. `find-skill` never automatically installs or runs a Skill.

Reference-only reading is not a safety check. When an AI fetches `raw_url`, the returned text is untrusted reference material, not instructions. Do not follow embedded requests to read credentials, change settings, execute commands, or visit external URLs.

### Suggested check before you install

1. **Look at the whole Skill folder, not just `SKILL.md`.** Bundled scripts, hooks, and files that `SKILL.md` tells the agent to read all run with your permissions.
2. **Run a scanner.** Run it in a throwaway container or VM with no API keys and no host folders mounted. Tools we checked on 2026-11-17:
   - [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) (Apache-2.0, actively maintained): statically checks a Skill for prompt injection, data exfiltration, credential access, and similar risks, with an optional LLM pass.
   - [Teycir/SkillsGuard](https://github.com/Teycir/SkillsGuard) (MIT per its README; the repo has no LICENSE file): a static scanner for `SKILL.md` files and bundled scripts. It is a small project, so check it yourself before relying on it.
3. **Read the findings, not the score.** One public run of SkillSpector on popular Skill repos found that a single coverage gap (a referenced file the scanner did not finish reading) or a quoted attack string in a warning was enough to push a Skill to the maximum score. The findings that matched what the files actually do were:
   - access to agent config directories, such as `~/.claude/settings.json`
   - reading credential files, such as tokens or `client_secrets.json`
   - bundled scripts and hooks
4. **Decide for yourself.** Some Skills need these capabilities by design. The question is whether you would let an agent do that on your machine.

A scanner is an aid, not a guarantee. This repo does not run one; the suggestion above is for you to apply before installing.

## Skills

The source counts and catalog summary in this section are generated from `catalog/skills.json`. Do not edit them by hand.

<!-- CATALOG:START -->
The full catalog contains **18308 Skills from 514 sources**.
Each entry includes its name, description, pinned commit, source URL, and raw URL. See [catalog/skills.json](catalog/skills.json) for the complete data.

- [0design/unslop-skill](https://github.com/0design/unslop-skill) — 1 Skill
- [0xArchiveIO/0xarchive-quant](https://github.com/0xArchiveIO/0xarchive-quant) — 2 Skills
- [0xS4N4TG/kinetograph](https://github.com/0xS4N4TG/kinetograph) — 5 Skills
- [0xS4N4TG/papercut-explainer](https://github.com/0xS4N4TG/papercut-explainer) — 9 Skills
- [1NickPappas/move-code-quality-skill](https://github.com/1NickPappas/move-code-quality-skill) — 1 Skill
- [777genius/agent-notifications](https://github.com/777genius/agent-notifications) — 1 Skill
- [8144225309/superscalar-mcp](https://github.com/8144225309/superscalar-mcp) — 3 Skills
- [9929y/genai-mesh-gradient](https://github.com/9929y/genai-mesh-gradient) — 1 Skill
- [aaron-he-zhu/aaron-marketing-skills](https://github.com/aaron-he-zhu/aaron-marketing-skills) — 120 Skills
- [abe238/claude-video-plus](https://github.com/abe238/claude-video-plus) — 1 Skill
- [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) — 1 Skill
- [AbubakrChan/product-launch-motion](https://github.com/AbubakrChan/product-launch-motion) — 2 Skills
- [AceDataCloud/Skills](https://github.com/AceDataCloud/Skills) — 137 Skills
- [activeloopai/hivemind](https://github.com/activeloopai/hivemind) — 7 Skills
- [adiny/moodtrip-hotel-search](https://github.com/adiny/moodtrip-hotel-search) — 1 Skill
- [adkit/ads-skills](https://github.com/adkit/ads-skills) — 11 Skills
- [adriannoes/awesome-agentic-ai](https://github.com/adriannoes/awesome-agentic-ai) — 333 Skills
- [aeonfun/aeon](https://github.com/aeonfun/aeon) — 94 Skills
- [agamm/claude-code-owasp](https://github.com/agamm/claude-code-owasp) — 1 Skill
- [agent-cards/skill](https://github.com/agent-cards/skill) — 1 Skill
- [agent37-platform/agent37-skills-collection](https://github.com/agent37-platform/agent37-skills-collection) — 2 Skills
- [agentbay-ai/agentbay-skills](https://github.com/agentbay-ai/agentbay-skills) — 15 Skills
- [agentrhq/webcmd](https://github.com/agentrhq/webcmd) — 1 Skill
- [agentward-ai/agentward](https://github.com/agentward-ai/agentward) — 6 Skills
- [agiwhitelist/auteur](https://github.com/agiwhitelist/auteur) — 1 Skill
- [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) — 35 Skills
- [AIDevGTM/gtm-cofounder](https://github.com/AIDevGTM/gtm-cofounder) — 20 Skills
- [ajnart/self-host](https://github.com/ajnart/self-host) — 4 Skills
- [akii-technologies-ltd/akii-seo-ai-search-optimizer](https://github.com/akii-technologies-ltd/akii-seo-ai-search-optimizer) — 11 Skills
- [aklofas/kicad-happy](https://github.com/aklofas/kicad-happy) — 11 Skills
- [alexgreensh/anidoodle](https://github.com/alexgreensh/anidoodle) — 1 Skill
- [alextitonis/fly.ai](https://github.com/alextitonis/fly.ai) — 4 Skills
- [alexyc9381/court-skill](https://github.com/alexyc9381/court-skill) — 1 Skill
- [alinaqi/maggy](https://github.com/alinaqi/maggy) — 70 Skills
- [Alisa0808/vibe-creating-skill](https://github.com/Alisa0808/vibe-creating-skill) — 1 Skill
- [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director) — 1 Skill
- [allxsmith/bestax](https://github.com/allxsmith/bestax) — 7 Skills
- [AlmogBaku/debug-skill](https://github.com/AlmogBaku/debug-skill) — 1 Skill
- [AlterLab-IEU/AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) — 243 Skills
- [AlterLab-IEU/AlterLab-FC-Skills](https://github.com/AlterLab-IEU/AlterLab-FC-Skills) — 72 Skills
- [AlterLab-IEU/AlterLab_GameForge](https://github.com/AlterLab-IEU/AlterLab_GameForge) — 41 Skills
- [amirkiarafiei/subagent-cli-skills](https://github.com/amirkiarafiei/subagent-cli-skills) — 25 Skills
- [anandpareek-hub/pixelbin-claude-skill](https://github.com/anandpareek-hub/pixelbin-claude-skill) — 1 Skill
- [angular/skills](https://github.com/angular/skills) — 2 Skills
- [Anjos2/recursive-research](https://github.com/Anjos2/recursive-research) — 1 Skill
- [anthropics/skills](https://github.com/anthropics/skills) — 20 Skills
- [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) — 1 Skill
- [antvis/AVA](https://github.com/antvis/AVA) — 1 Skill
- [apify/awesome-skills](https://github.com/apify/awesome-skills) — 29 Skills
- [apitube/news-api-skills](https://github.com/apitube/news-api-skills) — 1 Skill
- [appeeky/aso-skills](https://github.com/appeeky/aso-skills) — 40 Skills
- [archcore-ai/archcore](https://github.com/archcore-ai/archcore) — 4 Skills
- [arcmira/mcp](https://github.com/arcmira/mcp) — 11 Skills
- [arifszn/slide-wright](https://github.com/arifszn/slide-wright) — 1 Skill
- [Ashutos1997/claude-design-auditor-skill](https://github.com/Ashutos1997/claude-design-auditor-skill) — 1 Skill
- [assafkip/claudemy](https://github.com/assafkip/claudemy) — 1 Skill
- [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) — 1 Skill
- [ateymoori/oh-my-android](https://github.com/ateymoori/oh-my-android) — 1 Skill
- [AThevon/genjutsu](https://github.com/AThevon/genjutsu) — 20 Skills
- [AtlasCloudAI/awesome-seedance-2.5-prompts-skills](https://github.com/AtlasCloudAI/awesome-seedance-2.5-prompts-skills) — 2 Skills
- [Atomic-Mail/atomic-mail-agentic](https://github.com/Atomic-Mail/atomic-mail-agentic) — 2 Skills
- [AugustusW/audio-tldr-skill](https://github.com/AugustusW/audio-tldr-skill) — 1 Skill
- [Aurite-ai/agent-verifier](https://github.com/Aurite-ai/agent-verifier) — 5 Skills
- [AvdLee/SwiftUI-Agent-Skill](https://github.com/AvdLee/SwiftUI-Agent-Skill) — 2 Skills
- [avifenesh/agnix](https://github.com/avifenesh/agnix) — 39 Skills
- [awrshift/agent-memory-kit](https://github.com/awrshift/agent-memory-kit) — 10 Skills
- [awss1i/assay](https://github.com/awss1i/assay) — 1 Skill
- [bablobanov/hermes-agent-telegram-checklist](https://github.com/bablobanov/hermes-agent-telegram-checklist) — 1 Skill
- [backnotprop/plannotator](https://github.com/backnotprop/plannotator) — 15 Skills
- [baskduf/FableCodex](https://github.com/baskduf/FableCodex) — 1 Skill
- [beastlabai/multi-llm-plugin](https://github.com/beastlabai/multi-llm-plugin) — 1 Skill
- [BehiSecc/VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill) — 1 Skill
- [bevibing/tutor-skills](https://github.com/bevibing/tutor-skills) — 2 Skills
- [bitwize-music-studio/claude-ai-music-skills](https://github.com/bitwize-music-studio/claude-ai-music-skills) — 61 Skills
- [blackwell-systems/agent-lsp](https://github.com/blackwell-systems/agent-lsp) — 24 Skills
- [blader/humanizer](https://github.com/blader/humanizer) — 1 Skill
- [bluzername/claude-code-terminal-title](https://github.com/bluzername/claude-code-terminal-title) — 1 Skill
- [Bomx/distribb-skill](https://github.com/Bomx/distribb-skill) — 2 Skills
- [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills) — 404 Skills
- [Bria-AI/bria-skill](https://github.com/Bria-AI/bria-skill) — 10 Skills
- [BrianRWagner/ai-marketing-claude-code-skills](https://github.com/BrianRWagner/ai-marketing-claude-code-skills) — 20 Skills
- [browser-act/skills](https://github.com/browser-act/skills) — 102 Skills
- [buddy/buddy-plugin](https://github.com/buddy/buddy-plugin) — 1 Skill
- [BuildShipGrowRepeat/nextjs-sanity-blog-skill](https://github.com/BuildShipGrowRepeat/nextjs-sanity-blog-skill) — 1 Skill
- [Cap-go/capgo-skills](https://github.com/Cap-go/capgo-skills) — 55 Skills
- [career-ops-hq/career-ops](https://github.com/career-ops-hq/career-ops) — 1 Skill
- [celo-org/celopedia-skills](https://github.com/celo-org/celopedia-skills) — 2 Skills
- [ChainAware/behavioral-prediction-mcp](https://github.com/ChainAware/behavioral-prediction-mcp) — 1 Skill
- [ChangWenC/understanding-ladder](https://github.com/ChangWenC/understanding-ladder) — 2 Skills
- [Charlie85270/Dorothy](https://github.com/Charlie85270/Dorothy) — 2 Skills
- [ChatCut-Inc/agent-plugin](https://github.com/ChatCut-Inc/agent-plugin) — 69 Skills
- [checkout-page/ecommerce-skills](https://github.com/checkout-page/ecommerce-skills) — 20 Skills
- [chrisryugj/kordoc](https://github.com/chrisryugj/kordoc) — 2 Skills
- [chrisvoncsefalvay/claude-d3js-skill](https://github.com/chrisvoncsefalvay/claude-d3js-skill) — 1 Skill
- [chrono-meta/forge-harness](https://github.com/chrono-meta/forge-harness) — 55 Skills
- [citlyze/citlyze-skills](https://github.com/citlyze/citlyze-skills) — 5 Skills
- [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) — 13 Skills
- [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) — 1 Skill
- [coderabbitai/skills](https://github.com/coderabbitai/skills) — 5 Skills
- [coffeefuelbump/csv-data-summarizer-claude-skill](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) — 1 Skill
- [cognyai/claude-code-marketing-skills](https://github.com/cognyai/claude-code-marketing-skills) — 64 Skills
- [coinpaprika/skills](https://github.com/coinpaprika/skills) — 2 Skills
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 856 Skills
- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — 7 Skills
- [conorluddy/ios-simulator-skill](https://github.com/conorluddy/ios-simulator-skill) — 1 Skill
- [Continuum-AI-Corp/OrcaReplay](https://github.com/Continuum-AI-Corp/OrcaReplay) — 1 Skill
- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) — 53 Skills
- [CosmoBlk/email-marketing-bible](https://github.com/CosmoBlk/email-marketing-bible) — 1 Skill
- [coupler-io/skills](https://github.com/coupler-io/skills) — 120 Skills
- [csthink/dashmotion](https://github.com/csthink/dashmotion) — 1 Skill
- [cyperx84/claude-skills-mental-models](https://github.com/cyperx84/claude-skills-mental-models) — 1 Skill
- [cypress-io/ai-toolkit](https://github.com/cypress-io/ai-toolkit) — 5 Skills
- [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) — 15 Skills
- [d1vai/d1v-cli](https://github.com/d1vai/d1v-cli) — 1 Skill
- [danjdewhurst/story-skills](https://github.com/danjdewhurst/story-skills) — 24 Skills
- [dankofly/perfectify](https://github.com/dankofly/perfectify) — 1 Skill
- [dannwaneri/spec-writer](https://github.com/dannwaneri/spec-writer) — 1 Skill
- [danoszz/penthera](https://github.com/danoszz/penthera) — 1 Skill
- [daxaur/openpaw](https://github.com/daxaur/openpaw) — 41 Skills
- [deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills) — 95 Skills
- [deapi-ai/claude-code-skills](https://github.com/deapi-ai/claude-code-skills) — 2 Skills
- [dembrandt/dembrandt-skills](https://github.com/dembrandt/dembrandt-skills) — 45 Skills
- [deusyu/translate-book](https://github.com/deusyu/translate-book) — 1 Skill
- [Digidai/product-manager-skills](https://github.com/Digidai/product-manager-skills) — 1 Skill
- [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) — 16 Skills
- [dmoshehun-prog/learn-from-materials](https://github.com/dmoshehun-prog/learn-from-materials) — 1 Skill
- [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) — 18 Skills
- [drogers0/gh-image](https://github.com/drogers0/gh-image) — 1 Skill
- [duyunzhoudyz/dyz-gongwen-skills](https://github.com/duyunzhoudyz/dyz-gongwen-skills) — 22 Skills
- [eatmoreduck/boss-zhipin-scraper](https://github.com/eatmoreduck/boss-zhipin-scraper) — 1 Skill
- [edonadei/caliper](https://github.com/edonadei/caliper) — 9 Skills
- [eduardo-sl/go-agent-skills](https://github.com/eduardo-sl/go-agent-skills) — 31 Skills
- [efremidze/swift-patterns-skill](https://github.com/efremidze/swift-patterns-skill) — 1 Skill
- [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) — 9 Skills
- [ehmo/platform-design-skills](https://github.com/ehmo/platform-design-skills) — 8 Skills
- [elithril/blender-kiln](https://github.com/elithril/blender-kiln) — 1 Skill
- [emaynard/claude-family-history-research-skill](https://github.com/emaynard/claude-family-history-research-skill) — 1 Skill
- [EmblemCompany/Agent-skills](https://github.com/EmblemCompany/Agent-skills) — 9 Skills
- [emory/ASD-AuDHD-PAI-Skills](https://github.com/emory/ASD-AuDHD-PAI-Skills) — 1 Skill
- [emotixco/claude-skills-founder](https://github.com/emotixco/claude-skills-founder) — 14 Skills
- [EricJujianZou/rederive](https://github.com/EricJujianZou/rederive) — 1 Skill
- [Ericyoung-183/alpha-insights](https://github.com/Ericyoung-183/alpha-insights) — 1 Skill
- [ethos-link/rails-conventions](https://github.com/ethos-link/rails-conventions) — 1 Skill
- [EveryInc/charlie-cfo-skill](https://github.com/EveryInc/charlie-cfo-skill) — 1 Skill
- [everyinfra/everyinfra-agent-plugins](https://github.com/everyinfra/everyinfra-agent-plugins) — 27 Skills
- [everyinfra/seo-skills](https://github.com/everyinfra/seo-skills) — 1 Skill
- [exadel-inc/agentic-readiness-assessment](https://github.com/exadel-inc/agentic-readiness-assessment) — 2 Skills
- [explorium-ai/vibeprospecting-plugin](https://github.com/explorium-ai/vibeprospecting-plugin) — 2 Skills
- [federicodeponte/opendraft](https://github.com/federicodeponte/opendraft) — 1 Skill
- [finom/vovk](https://github.com/finom/vovk) — 15 Skills
- [firecrawl/cli](https://github.com/firecrawl/cli) — 13 Skills
- [first-fluke/oh-my-agent](https://github.com/first-fluke/oh-my-agent) — 60 Skills
- [fishzjp/qa-skills](https://github.com/fishzjp/qa-skills) — 14 Skills
- [forjd/better-writing](https://github.com/forjd/better-writing) — 1 Skill
- [foryourhealth111-pixel/Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills) — 221 Skills
- [framix-team/skill-email-html-mjml](https://github.com/framix-team/skill-email-html-mjml) — 1 Skill
- [Frihet-io/frihet-mcp](https://github.com/Frihet-io/frihet-mcp) — 17 Skills
- [frmoretto/clarity-gate](https://github.com/frmoretto/clarity-gate) — 1 Skill
- [fujibee/agmsg](https://github.com/fujibee/agmsg) — 1 Skill
- [fullselfbrowsing/FSB](https://github.com/fullselfbrowsing/FSB) — 3 Skills
- [fvadicamo/dev-agent-skills](https://github.com/fvadicamo/dev-agent-skills) — 7 Skills
- [gal-a/qikly](https://github.com/gal-a/qikly) — 1 Skill
- [galleonlabs/hypergrok-trading-desk](https://github.com/galleonlabs/hypergrok-trading-desk) — 17 Skills
- [GanyuanRan/Aegis](https://github.com/GanyuanRan/Aegis) — 22 Skills
- [GarethManning/education-agent-skills](https://github.com/GarethManning/education-agent-skills) — 165 Skills
- [GAURAV-1313/codecall](https://github.com/GAURAV-1313/codecall) — 1 Skill
- [geekjourneyx/md2wechat-skill](https://github.com/geekjourneyx/md2wechat-skill) — 2 Skills
- [GiaSip/giasip-skills](https://github.com/GiaSip/giasip-skills) — 3 Skills
- [gitroomhq/postiz-agent](https://github.com/gitroomhq/postiz-agent) — 1 Skill
- [glacierphonk/naming](https://github.com/glacierphonk/naming) — 1 Skill
- [glitternetwork/pinme](https://github.com/glitternetwork/pinme) — 7 Skills
- [gokapso/agent-skills](https://github.com/gokapso/agent-skills) — 4 Skills
- [gongdear/cline-pilot](https://github.com/gongdear/cline-pilot) — 1 Skill
- [google/skills](https://github.com/google/skills) — 206 Skills
- [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) — 185 Skills
- [guia-matthieu/clawfu-skills](https://github.com/guia-matthieu/clawfu-skills) — 173 Skills
- [gviiisen/repo-context-ledger](https://github.com/gviiisen/repo-context-ledger) — 1 Skill
- [hanhuark/mechanical-engineering-research-skill](https://github.com/hanhuark/mechanical-engineering-research-skill) — 9 Skills
- [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills) — 20 Skills
- [hasuwini77/3d-logo-skill](https://github.com/hasuwini77/3d-logo-skill) — 1 Skill
- [hedralab/eskill](https://github.com/hedralab/eskill) — 3 Skills
- [helius-labs/core-ai](https://github.com/helius-labs/core-ai) — 6 Skills
- [hermes-labs-ai/lintlang](https://github.com/hermes-labs-ai/lintlang) — 6 Skills
- [hermes-labs-ai/little-canary](https://github.com/hermes-labs-ai/little-canary) — 1 Skill
- [HeshamFS/materials-simulation-skills](https://github.com/HeshamFS/materials-simulation-skills) — 24 Skills
- [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) — 22 Skills
- [honeydew-ai/honeydew-ai-coding-agents-plugins](https://github.com/honeydew-ai/honeydew-ai-coding-agents-plugins) — 13 Skills
- [hqhq1025/skill-optimizer](https://github.com/hqhq1025/skill-optimizer) — 3 Skills
- [HUANGCHIHHUNGLeo/claude-real-video](https://github.com/HUANGCHIHHUNGLeo/claude-real-video) — 3 Skills
- [huifer/Claude-Ally-Health](https://github.com/huifer/Claude-Ally-Health) — 14 Skills
- [human-avatar/skills-for-humanity](https://github.com/human-avatar/skills-for-humanity) — 212 Skills
- [humanpen/humanpen-skill](https://github.com/humanpen/humanpen-skill) — 1 Skill
- [Hyacehila/humanizer-zh-next](https://github.com/Hyacehila/humanizer-zh-next) — 1 Skill
- [hyperb1iss/unifly](https://github.com/hyperb1iss/unifly) — 1 Skill
- [ibelick/ui-skills](https://github.com/ibelick/ui-skills) — 9 Skills
- [ilang-ai/Imprint](https://github.com/ilang-ai/Imprint) — 1 Skill
- [Illyism/seo-skills](https://github.com/Illyism/seo-skills) — 30 Skills
- [ilyautov/humanizer-ru](https://github.com/ilyautov/humanizer-ru) — 2 Skills
- [ilyautov/small-business-ru](https://github.com/ilyautov/small-business-ru) — 34 Skills
- [imbue-ai/blueprint](https://github.com/imbue-ai/blueprint) — 2 Skills
- [indranilbanerjee/digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro) — 164 Skills
- [infrasity-labs/dev-gtm-claude-skills](https://github.com/infrasity-labs/dev-gtm-claude-skills) — 216 Skills
- [inhouseseo/superseo-skills](https://github.com/inhouseseo/superseo-skills) — 11 Skills
- [ivan-magda/claude-code-plugin-template](https://github.com/ivan-magda/claude-code-plugin-template) — 1 Skill
- [izzzzzi/agent-assh](https://github.com/izzzzzi/agent-assh) — 1 Skill
- [jacob-g-park/polaris-datainsight-doc-extract](https://github.com/jacob-g-park/polaris-datainsight-doc-extract) — 1 Skill
- [jahro-console/unity-agent-skills](https://github.com/jahro-console/unity-agent-skills) — 8 Skills
- [jangtrinh/design-os-3d-blender](https://github.com/jangtrinh/design-os-3d-blender) — 5 Skills
- [JanYork/llm-wiki-cli](https://github.com/JanYork/llm-wiki-cli) — 8 Skills
- [JasonColapietro/suede-creator-skills](https://github.com/JasonColapietro/suede-creator-skills) — 69 Skills
- [JayPokale/Chisle](https://github.com/JayPokale/Chisle) — 4 Skills
- [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) — 67 Skills
- [jgsystemsconsulting/jgs-se-knowledge-packs](https://github.com/jgsystemsconsulting/jgs-se-knowledge-packs) — 83 Skills
- [JimmySadek/video-fetcher-to-markdown](https://github.com/JimmySadek/video-fetcher-to-markdown) — 1 Skill
- [jnMetaCode/ai-shortfilm-prompts](https://github.com/jnMetaCode/ai-shortfilm-prompts) — 1 Skill
- [jnMetaCode/shellward](https://github.com/jnMetaCode/shellward) — 2 Skills
- [Johell1NS/browser-search](https://github.com/Johell1NS/browser-search) — 1 Skill
- [jonathimer/devmarketing-skills](https://github.com/jonathimer/devmarketing-skills) — 34 Skills
- [jthack/ffuf_claude_skill](https://github.com/jthack/ffuf_claude_skill) — 1 Skill
- [JuliusBrussee/blueprint](https://github.com/JuliusBrussee/blueprint) — 9 Skills
- [junshi-research/research-junshi](https://github.com/junshi-research/research-junshi) — 1 Skill
- [JunsW/feature-track](https://github.com/JunsW/feature-track) — 1 Skill
- [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — 177 Skills
- [k-kolomeitsev/data-structure-protocol](https://github.com/k-kolomeitsev/data-structure-protocol) — 1 Skill
- [KalarisLabs/research-agent-skills](https://github.com/KalarisLabs/research-agent-skills) — 199 Skills
- [karanb192/itr-wala](https://github.com/karanb192/itr-wala) — 1 Skill
- [karero/croftweaver](https://github.com/karero/croftweaver) — 39 Skills
- [Kayforkind/reimagine-it](https://github.com/Kayforkind/reimagine-it) — 7 Skills
- [kensaurus/skills](https://github.com/kensaurus/skills) — 174 Skills
- [KerberosClaw/kc_ai_skills](https://github.com/KerberosClaw/kc_ai_skills) — 26 Skills
- [Kevin7Qi/codex-collab](https://github.com/Kevin7Qi/codex-collab) — 2 Skills
- [kgraph57/mckinsey-style-visualization-skill](https://github.com/kgraph57/mckinsey-style-visualization-skill) — 1 Skill
- [KhazP/vibe-coding-prompt-template](https://github.com/KhazP/vibe-coding-prompt-template) — 11 Skills
- [khendzel/skills-janitor](https://github.com/khendzel/skills-janitor) — 6 Skills
- [Kinprove/genealogy-research-recipes](https://github.com/Kinprove/genealogy-research-recipes) — 1 Skill
- [kklimuk/docx-cli](https://github.com/kklimuk/docx-cli) — 4 Skills
- [kochetkov-ma/claude-brewcode](https://github.com/kochetkov-ma/claude-brewcode) — 40 Skills
- [Koloyaaa/foreign-academic-translator-skill](https://github.com/Koloyaaa/foreign-academic-translator-skill) — 14 Skills
- [komal-SkyNET/claude-skill-homeassistant](https://github.com/komal-SkyNET/claude-skill-homeassistant) — 1 Skill
- [Krexa-xyz/skills](https://github.com/Krexa-xyz/skills) — 1 Skill
- [krisyangdev/motionboard](https://github.com/krisyangdev/motionboard) — 1 Skill
- [krodak/clickup-cli](https://github.com/krodak/clickup-cli) — 3 Skills
- [kulchankas/paranoid](https://github.com/kulchankas/paranoid) — 1 Skill
- [KyungHwanKim-devs/kubegap](https://github.com/KyungHwanKim-devs/kubegap) — 1 Skill
- [kyy-logs/code-review-gate-skill](https://github.com/kyy-logs/code-review-gate-skill) — 2 Skills
- [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) — 1 Skill
- [LambdaTest/agent-skills](https://github.com/LambdaTest/agent-skills) — 86 Skills
- [laolaoshiren/claude-code-skills-zh](https://github.com/laolaoshiren/claude-code-skills-zh) — 9 Skills
- [laulauraluo/ai-code-review-triage](https://github.com/laulauraluo/ai-code-review-triage) — 1 Skill
- [lawve-ai/awesome-legal-skills](https://github.com/lawve-ai/awesome-legal-skills) — 270 Skills
- [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) — 1 Skill
- [LeulAria/Aria-Icons](https://github.com/LeulAria/Aria-Icons) — 1 Skill
- [LewisLiu007/full-page-screenshot](https://github.com/LewisLiu007/full-page-screenshot) — 1 Skill
- [lindblomstefan/skills-library](https://github.com/lindblomstefan/skills-library) — 1 Skill
- [Linked-API/linkedin-skills](https://github.com/Linked-API/linkedin-skills) — 2 Skills
- [ljx-chase/research-field-onboarding](https://github.com/ljx-chase/research-field-onboarding) — 1 Skill
- [lucasbabur/jp-essay](https://github.com/lucasbabur/jp-essay) — 2 Skills
- [luchasarie/bro-skill](https://github.com/luchasarie/bro-skill) — 1 Skill
- [lukstei/slop-grader](https://github.com/lukstei/slop-grader) — 2 Skills
- [luoyuctl/agenttrace](https://github.com/luoyuctl/agenttrace) — 1 Skill
- [mailtrap/mailtrap-skills](https://github.com/mailtrap/mailtrap-skills) — 8 Skills
- [makenotion/claude-code-notion-plugin](https://github.com/makenotion/claude-code-notion-plugin) — 12 Skills
- [makenotion/notion-cookbook](https://github.com/makenotion/notion-cookbook) — 16 Skills
- [makevoid/motion-graphics-music-video-skill-noimage](https://github.com/makevoid/motion-graphics-music-video-skill-noimage) — 1 Skill
- [Maksim-Burtsev/simple-man](https://github.com/Maksim-Burtsev/simple-man) — 1 Skill
- [manavmishra/ZeroSlop](https://github.com/manavmishra/ZeroSlop) — 1 Skill
- [MartinDelophy/ai-video-editor](https://github.com/MartinDelophy/ai-video-editor) — 3 Skills
- [marvkr/better-design](https://github.com/marvkr/better-design) — 2 Skills
- [massimodeluisa/recursive-decomposition-skill](https://github.com/massimodeluisa/recursive-decomposition-skill) — 1 Skill
- [mattjoyce/kanban-skill](https://github.com/mattjoyce/kanban-skill) — 1 Skill
- [mattpocock/skills](https://github.com/mattpocock/skills) — 36 Skills
- [mblode/agent-skills](https://github.com/mblode/agent-skills) — 61 Skills
- [mcollina/skills](https://github.com/mcollina/skills) — 11 Skills
- [meodai/skill.color-expert](https://github.com/meodai/skill.color-expert) — 1 Skill
- [metalbear-co/skills](https://github.com/metalbear-co/skills) — 13 Skills
- [MetaMask/agent-skills](https://github.com/MetaMask/agent-skills) — 1 Skill
- [MetcalfSolutions/Satori](https://github.com/MetcalfSolutions/Satori) — 1 Skill
- [mhattingpete/claude-skills-marketplace](https://github.com/mhattingpete/claude-skills-marketplace) — 18 Skills
- [mhfed/vn-law-check](https://github.com/mhfed/vn-law-check) — 1 Skill
- [michalparkola/tapestry-skills-for-claude-code](https://github.com/michalparkola/tapestry-skills-for-claude-code) — 7 Skills
- [microsoft/skills](https://github.com/microsoft/skills) — 214 Skills
- [mobbin/skills](https://github.com/mobbin/skills) — 4 Skills
- [modem-dev/skills](https://github.com/modem-dev/skills) — 1 Skill
- [MohamedAbdallah-14/unslop](https://github.com/MohamedAbdallah-14/unslop) — 6 Skills
- [mohitagw15856/pm-claude-skills](https://github.com/mohitagw15856/pm-claude-skills) — 1770 Skills
- [momentic-ai/skills](https://github.com/momentic-ai/skills) — 4 Skills
- [more-io/claude-apple-bridges](https://github.com/more-io/claude-apple-bridges) — 1 Skill
- [morluto/rea](https://github.com/morluto/rea) — 5 Skills
- [moxno/privacyscrubber-mcp](https://github.com/moxno/privacyscrubber-mcp) — 1 Skill
- [MSG91/m91-skill](https://github.com/MSG91/m91-skill) — 1 Skill
- [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) — 818 Skills
- [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) — 24 Skills
- [muthuishere/hand-drawn-diagrams](https://github.com/muthuishere/hand-drawn-diagrams) — 1 Skill
- [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) — 1 Skill
- [nagameTW/formosa-humanizer](https://github.com/nagameTW/formosa-humanizer) — 1 Skill
- [Nanako0129/sepia](https://github.com/Nanako0129/sepia) — 6 Skills
- [Necmttn/ax](https://github.com/Necmttn/ax) — 12 Skills
- [Neeeophytee/finding-unknowns-skills](https://github.com/Neeeophytee/finding-unknowns-skills) — 14 Skills
- [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) — 66 Skills
- [nexscope-ai/eCommerce-Skills](https://github.com/nexscope-ai/eCommerce-Skills) — 120 Skills
- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — 7 Skills
- [nodemaven/skills](https://github.com/nodemaven/skills) — 6 Skills
- [NoizAI/skills](https://github.com/NoizAI/skills) — 10 Skills
- [nowork-studio/notfair-plugin](https://github.com/nowork-studio/notfair-plugin) — 45 Skills
- [NVIDIA/skills](https://github.com/NVIDIA/skills) — 465 Skills
- [obra/superpowers](https://github.com/obra/superpowers) — 15 Skills
- [obra/superpowers-lab](https://github.com/obra/superpowers-lab) — 4 Skills
- [Octav-Labs/octav-api-skill](https://github.com/Octav-Labs/octav-api-skill) — 1 Skill
- [officialzeroxyz/zero-plugins](https://github.com/officialzeroxyz/zero-plugins) — 2 Skills
- [ognjengt/founder-skills](https://github.com/ognjengt/founder-skills) — 15 Skills
- [ohad6k/emulo](https://github.com/ohad6k/emulo) — 8 Skills
- [oil-oil/oil-ui](https://github.com/oil-oil/oil-ui) — 1 Skill
- [olgasafonova/SkillCheck-Free](https://github.com/olgasafonova/SkillCheck-Free) — 1 Skill
- [oliver-zehentleitner/keep-the-why](https://github.com/oliver-zehentleitner/keep-the-why) — 1 Skill
- [ollygarden/opentelemetry-agent-skills](https://github.com/ollygarden/opentelemetry-agent-skills) — 20 Skills
- [omkamal/pypict-claude-skill](https://github.com/omkamal/pypict-claude-skill) — 1 Skill
- [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) — 219 Skills
- [op7418/Youtube-clipper-skill](https://github.com/op7418/Youtube-clipper-skill) — 1 Skill
- [open-salesblink/skill](https://github.com/open-salesblink/skill) — 1 Skill
- [openaccountants/openaccountants](https://github.com/openaccountants/openaccountants) — 2457 Skills
- [openai/skills](https://github.com/openai/skills) — 43 Skills
- [openweb-org/openweb](https://github.com/openweb-org/openweb) — 1 Skill
- [Optim-Agent/optim-agent](https://github.com/Optim-Agent/optim-agent) — 2 Skills
- [OptimNow/cloud-finops-skills](https://github.com/OptimNow/cloud-finops-skills) — 2 Skills
- [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) — 98 Skills
- [Orkas-AI/Orkas-VideoStudio](https://github.com/Orkas-AI/Orkas-VideoStudio) — 11 Skills
- [orwa-mahmoud/nightshift](https://github.com/orwa-mahmoud/nightshift) — 17 Skills
- [orziz/odai](https://github.com/orziz/odai) — 4 Skills
- [pachca/openapi](https://github.com/pachca/openapi) — 9 Skills
- [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) — 1 Skill
- [Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills) — 22 Skills
- [pashov/skills](https://github.com/pashov/skills) — 5 Skills
- [pattern-ai-labs/agentcall](https://github.com/pattern-ai-labs/agentcall) — 1 Skill
- [perso-ai/perso-dubbing-plugin](https://github.com/perso-ai/perso-dubbing-plugin) — 3 Skills
- [phuryn/pm-skills](https://github.com/phuryn/pm-skills) — 72 Skills
- [pjt222/agent-almanac](https://github.com/pjt222/agent-almanac) — 1626 Skills
- [plasma-ai/fractal](https://github.com/plasma-ai/fractal) — 5 Skills
- [plasma-ai/wiki](https://github.com/plasma-ai/wiki) — 1 Skill
- [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) — 1 Skill
- [polaroteam/moltdj-skill](https://github.com/polaroteam/moltdj-skill) — 1 Skill
- [posteyai/skills](https://github.com/posteyai/skills) — 10 Skills
- [praneybehl/llm-wiki-plugin](https://github.com/praneybehl/llm-wiki-plugin) — 1 Skill
- [prisma/skills](https://github.com/prisma/skills) — 11 Skills
- [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills) — 69 Skills
- [prompt-security/clawsec](https://github.com/prompt-security/clawsec) — 16 Skills
- [PSPDFKit-labs/nutrient-agent-skill](https://github.com/PSPDFKit-labs/nutrient-agent-skill) — 1 Skill
- [publora/skills](https://github.com/publora/skills) — 9 Skills
- [qdrant/skills](https://github.com/qdrant/skills) — 34 Skills
- [QingYunA/answer-me-with-html](https://github.com/QingYunA/answer-me-with-html) — 1 Skill
- [Qiuner/birdview](https://github.com/Qiuner/birdview) — 3 Skills
- [radres/call-me](https://github.com/radres/call-me) — 3 Skills
- [rainmanjam/poka-yoke](https://github.com/rainmanjam/poka-yoke) — 20 Skills
- [raintree-technology/hig-doctor](https://github.com/raintree-technology/hig-doctor) — 15 Skills
- [RAKKUNN/vicem](https://github.com/RAKKUNN/vicem) — 1 Skill
- [rameerez/claude-code-startup-skills](https://github.com/rameerez/claude-code-startup-skills) — 5 Skills
- [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) — 110 Skills
- [ramzesenok/iOS-Accessibility-Audit-Skill](https://github.com/ramzesenok/iOS-Accessibility-Audit-Skill) — 1 Skill
- [raphaelchristi/harness-evolver](https://github.com/raphaelchristi/harness-evolver) — 9 Skills
- [realkimbarrett/advertising-skills](https://github.com/realkimbarrett/advertising-skills) — 12 Skills
- [rebelytics/one-skill-to-rule-them-all](https://github.com/rebelytics/one-skill-to-rule-them-all) — 1 Skill
- [redis/agent-skills](https://github.com/redis/agent-skills) — 14 Skills
- [reliefeai/browser-relay](https://github.com/reliefeai/browser-relay) — 1 Skill
- [renezander030/capcut-cli](https://github.com/renezander030/capcut-cli) — 1 Skill
- [ReScienceLab/opc-skills](https://github.com/ReScienceLab/opc-skills) — 13 Skills
- [resend/resend-skills](https://github.com/resend/resend-skills) — 5 Skills
- [rhiever/evident-charts](https://github.com/rhiever/evident-charts) — 1 Skill
- [rlaope/oh-my-hermes](https://github.com/rlaope/oh-my-hermes) — 284 Skills
- [robzolkos/skill-rails-upgrade](https://github.com/robzolkos/skill-rails-upgrade) — 1 Skill
- [rockscy/solo-skills](https://github.com/rockscy/solo-skills) — 7 Skills
- [rorkai/app-store-connect-cli-skills](https://github.com/rorkai/app-store-connect-cli-skills) — 26 Skills
- [rrrrrredy/research-toolkit](https://github.com/rrrrrredy/research-toolkit) — 2 Skills
- [ruslanlap/cavemenko](https://github.com/ruslanlap/cavemenko) — 5 Skills
- [ryanbbrown/revealjs-skill](https://github.com/ryanbbrown/revealjs-skill) — 1 Skill
- [saleh-alhaddad/itqan-engineering](https://github.com/saleh-alhaddad/itqan-engineering) — 13 Skills
- [salemalem/npmscan-mcp-plugin](https://github.com/salemalem/npmscan-mcp-plugin) — 5 Skills
- [salespeak-ai/buyer-eval-skill](https://github.com/salespeak-ai/buyer-eval-skill) — 1 Skill
- [sametbrr/llm-wiki-manager](https://github.com/sametbrr/llm-wiki-manager) — 1 Skill
- [sandbaseai/sandbase-skills](https://github.com/sandbaseai/sandbase-skills) — 245 Skills
- [sanjay3290/ai-skills](https://github.com/sanjay3290/ai-skills) — 25 Skills
- [santiago-vargas-de-kruijf/claude-overkill](https://github.com/santiago-vargas-de-kruijf/claude-overkill) — 1 Skill
- [sboghossian/master-claude-for-legal](https://github.com/sboghossian/master-claude-for-legal) — 1 Skill
- [scarletkc/agents](https://github.com/scarletkc/agents) — 12 Skills
- [scarletkc/vexor](https://github.com/scarletkc/vexor) — 1 Skill
- [ScrapeCreators/social-media-research-skills](https://github.com/ScrapeCreators/social-media-research-skills) — 13 Skills
- [ScrapingBee/scrapingbee-cli](https://github.com/ScrapingBee/scrapingbee-cli) — 2 Skills
- [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) — 34 Skills
- [SeifBenayed/claude-code-sdk](https://github.com/SeifBenayed/claude-code-sdk) — 12 Skills
- [Sendmux/skills](https://github.com/Sendmux/skills) — 11 Skills
- [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) — 13 Skills
- [SerhiiKorniienko/bullshit-detector](https://github.com/SerhiiKorniienko/bullshit-detector) — 7 Skills
- [serpro69/claude-toolbox](https://github.com/serpro69/claude-toolbox) — 25 Skills
- [SHADOWPR0/beautiful_prose](https://github.com/SHADOWPR0/beautiful_prose) — 1 Skill
- [SHADOWPR0/security-bluebook-builder](https://github.com/SHADOWPR0/security-bluebook-builder) — 1 Skill
- [shalintripathi/saas-marketing-agents](https://github.com/shalintripathi/saas-marketing-agents) — 19 Skills
- [shenysun/skills-manager](https://github.com/shenysun/skills-manager) — 2 Skills
- [shepsci/kaggle-skill](https://github.com/shepsci/kaggle-skill) — 1 Skill
- [shouldnotappearcalm/a-share-skill](https://github.com/shouldnotappearcalm/a-share-skill) — 7 Skills
- [Simon-He95/markstream-vue](https://github.com/Simon-He95/markstream-vue) — 12 Skills
- [siril9/presentation-skill](https://github.com/siril9/presentation-skill) — 1 Skill
- [skymanbp/cc-tree](https://github.com/skymanbp/cc-tree) — 1 Skill
- [smerchek/claude-epub-skill](https://github.com/smerchek/claude-epub-skill) — 1 Skill
- [smixs/creative-director-skill](https://github.com/smixs/creative-director-skill) — 1 Skill
- [sneg55/agent-starter](https://github.com/sneg55/agent-starter) — 9 Skills
- [sno-ai/sno-station-skills](https://github.com/sno-ai/sno-station-skills) — 40 Skills
- [snyk/agent-scan](https://github.com/snyk/agent-scan) — 3 Skills
- [soba-labs/langchain-agent-skills](https://github.com/soba-labs/langchain-agent-skills) — 9 Skills
- [socai-io/jev-social](https://github.com/socai-io/jev-social) — 1 Skill
- [sonilo-ai/skills](https://github.com/sonilo-ai/skills) — 13 Skills
- [spartan-stratos/spartan-ai-toolkit](https://github.com/spartan-stratos/spartan-ai-toolkit) — 35 Skills
- [speakeasy-api/sdk-generation-skills](https://github.com/speakeasy-api/sdk-generation-skills) — 14 Skills
- [Square-Zero-Labs/video-prompting-skill](https://github.com/Square-Zero-Labs/video-prompting-skill) — 1 Skill
- [squirrelscan/skills](https://github.com/squirrelscan/skills) — 2 Skills
- [stjbrown/agent-knowledge](https://github.com/stjbrown/agent-knowledge) — 7 Skills
- [sujunmin/agy-ppt](https://github.com/sujunmin/agy-ppt) — 1 Skill
- [SupercmoHQ/superCMO-skills](https://github.com/SupercmoHQ/superCMO-skills) — 23 Skills
- [supercorp-ai/supercov](https://github.com/supercorp-ai/supercov) — 2 Skills
- [superdesigndev/superdesign-skill](https://github.com/superdesigndev/superdesign-skill) — 1 Skill
- [swarmclawai/swarmclaw](https://github.com/swarmclawai/swarmclaw) — 12 Skills
- [swarmclawai/swarmvault](https://github.com/swarmclawai/swarmvault) — 1 Skill
- [swaylq/humanize-chinese](https://github.com/swaylq/humanize-chinese) — 5 Skills
- [swaylq/master-skill](https://github.com/swaylq/master-skill) — 117 Skills
- [swiftlysingh/excalidraw-cli](https://github.com/swiftlysingh/excalidraw-cli) — 1 Skill
- [Swiftner/Factory-Floor](https://github.com/Swiftner/Factory-Floor) — 1 Skill
- [szarkans/multi](https://github.com/szarkans/multi) — 6 Skills
- [taisly/agent](https://github.com/taisly/agent) — 1 Skill
- [takechanman1228/claude-ecom](https://github.com/takechanman1228/claude-ecom) — 1 Skill
- [takechanman1228/claude-persona](https://github.com/takechanman1228/claude-persona) — 1 Skill
- [talkstream/ru-text](https://github.com/talkstream/ru-text) — 4 Skills
- [tanweai/pua](https://github.com/tanweai/pua) — 36 Skills
- [tasteray/skills](https://github.com/tasteray/skills) — 2 Skills
- [teableio/agent-skills](https://github.com/teableio/agent-skills) — 2 Skills
- [Tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) — 20 Skills
- [testdino-hq/playwright-skill](https://github.com/testdino-hq/playwright-skill) — 7 Skills
- [TexasBedouin/vibe-check](https://github.com/TexasBedouin/vibe-check) — 1 Skill
- [thedesignproject/agent-skills](https://github.com/thedesignproject/agent-skills) — 20 Skills
- [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) — 39 Skills
- [TheQmaks/crowdcast](https://github.com/TheQmaks/crowdcast) — 1 Skill
- [thousandflowers/skillreaper](https://github.com/thousandflowers/skillreaper) — 2 Skills
- [tinqiao-oss/engramory](https://github.com/tinqiao-oss/engramory) — 1 Skill
- [tjboudreaux/cc-thinking-skills](https://github.com/tjboudreaux/cc-thinking-skills) — 28 Skills
- [tlgrcli/tlgr](https://github.com/tlgrcli/tlgr) — 1 Skill
- [tomasz-tomczyk/crit](https://github.com/tomasz-tomczyk/crit) — 11 Skills
- [TomGranot/hubspot-admin-skills](https://github.com/TomGranot/hubspot-admin-skills) — 40 Skills
- [trailofbits/skills](https://github.com/trailofbits/skills) — 99 Skills
- [transloadit/skills](https://github.com/transloadit/skills) — 19 Skills
- [tronghieu/agent-skills](https://github.com/tronghieu/agent-skills) — 19 Skills
- [truongduy2611/app-store-preflight-skills](https://github.com/truongduy2611/app-store-preflight-skills) — 1 Skill
- [trycourier/courier-skills](https://github.com/trycourier/courier-skills) — 1 Skill
- [tt-a1i/archify](https://github.com/tt-a1i/archify) — 5 Skills
- [tubeagentkit/youtube-transcript-skills](https://github.com/tubeagentkit/youtube-transcript-skills) — 1 Skill
- [tuo-lei/vibe-replay](https://github.com/tuo-lei/vibe-replay) — 1 Skill
- [tushaarmehtaa/tushar-skills](https://github.com/tushaarmehtaa/tushar-skills) — 34 Skills
- [tw93/Mole](https://github.com/tw93/Mole) — 5 Skills
- [UiPath/coder_eval](https://github.com/UiPath/coder_eval) — 6 Skills
- [uizze/uizze](https://github.com/uizze/uizze) — 5 Skills
- [unbrowse-ai/unbrowse](https://github.com/unbrowse-ai/unbrowse) — 13 Skills
- [Upload-Post/upload-post-skill](https://github.com/Upload-Post/upload-post-skill) — 1 Skill
- [uucz/moyu](https://github.com/uucz/moyu) — 7 Skills
- [uxKero/anydesign](https://github.com/uxKero/anydesign) — 1 Skill
- [vaibhavarora14/job-application-agent](https://github.com/vaibhavarora14/job-application-agent) — 1 Skill
- [Valian/linear-cli-skill](https://github.com/Valian/linear-cli-skill) — 1 Skill
- [vanshyadav1408/Omentir](https://github.com/vanshyadav1408/Omentir) — 3 Skills
- [veniceai/skills](https://github.com/veniceai/skills) — 29 Skills
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) — 8 Skills
- [verdikta/verdikta-applications](https://github.com/verdikta/verdikta-applications) — 3 Skills
- [vidanov/aws-architecture-diagram-skill](https://github.com/vidanov/aws-architecture-diagram-skill) — 2 Skills
- [video-db/skills](https://github.com/video-db/skills) — 6 Skills
- [Vladimir-Human/humanizer-ru](https://github.com/Vladimir-Human/humanizer-ru) — 1 Skill
- [Vladimir-Human/ru-marketplace-mcp](https://github.com/Vladimir-Human/ru-marketplace-mcp) — 15 Skills
- [vmware-skills/VMware-AIops](https://github.com/vmware-skills/VMware-AIops) — 1 Skill
- [VoDaiLocz/kilo-kit-mcp](https://github.com/VoDaiLocz/kilo-kit-mcp) — 113 Skills
- [VoltAgent/voltagent](https://github.com/VoltAgent/voltagent) — 2 Skills
- [voygr-tech/placecall](https://github.com/voygr-tech/placecall) — 2 Skills
- [vshulcz/deja-vu](https://github.com/vshulcz/deja-vu) — 4 Skills
- [wannabehero/charles-proxy-extract-skill](https://github.com/wannabehero/charles-proxy-extract-skill) — 1 Skill
- [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) — 120 Skills
- [wendylabsinc/claude-skills](https://github.com/wendylabsinc/claude-skills) — 26 Skills
- [wgwtest/novel-writing](https://github.com/wgwtest/novel-writing) — 1 Skill
- [wholiver/swiftui-design-skill](https://github.com/wholiver/swiftui-design-skill) — 1 Skill
- [wiltodelta/remove-ai-watermarks](https://github.com/wiltodelta/remove-ai-watermarks) — 3 Skills
- [wondelai/skills](https://github.com/wondelai/skills) — 65 Skills
- [woniu9524/open-web-bridge](https://github.com/woniu9524/open-web-bridge) — 1 Skill
- [wrg32786/aigent-os](https://github.com/wrg32786/aigent-os) — 71 Skills
- [wrsmith108/linear-claude-skill](https://github.com/wrsmith108/linear-claude-skill) — 1 Skill
- [wrsmith108/varlock-claude-skill](https://github.com/wrsmith108/varlock-claude-skill) — 1 Skill
- [wshuyi/x-article-publisher-skill](https://github.com/wshuyi/x-article-publisher-skill) — 1 Skill
- [xberg-io/xberg](https://github.com/xberg-io/xberg) — 26 Skills
- [xianyu110/ecommerce-image-skills](https://github.com/xianyu110/ecommerce-image-skills) — 12 Skills
- [xianyu110/ecommerce-video-skills](https://github.com/xianyu110/ecommerce-video-skills) — 13 Skills
- [xiehuan123/dsh-deepread](https://github.com/xiehuan123/dsh-deepread) — 1 Skill
- [Xquik-dev/tweetclaw](https://github.com/Xquik-dev/tweetclaw) — 1 Skill
- [Xquik-dev/x-twitter-scraper](https://github.com/Xquik-dev/x-twitter-scraper) — 3 Skills
- [yang0/handraw-style](https://github.com/yang0/handraw-style) — 21 Skills
- [YannisKiefer/dark-psychology-skills](https://github.com/YannisKiefer/dark-psychology-skills) — 13 Skills
- [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) — 9 Skills
- [ykdojo/gh-star-history](https://github.com/ykdojo/gh-star-history) — 1 Skill
- [ykdojo/paper-search](https://github.com/ykdojo/paper-search) — 1 Skill
- [ysskrishna/ai-agent-skills](https://github.com/ysskrishna/ai-agent-skills) — 17 Skills
- [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) — 8 Skills
- [yuwen-cool/yuwen-publish-precheck](https://github.com/yuwen-cool/yuwen-publish-precheck) — 1 Skill
- [yvgude/lean-ctx](https://github.com/yvgude/lean-ctx) — 2 Skills
- [zagmoai/public-google-drive](https://github.com/zagmoai/public-google-drive) — 1 Skill
- [zapier/zapier-mcp](https://github.com/zapier/zapier-mcp) — 4 Skills
- [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) — 1 Skill
- [ZeKaiNie/universal-examprep-skill](https://github.com/ZeKaiNie/universal-examprep-skill) — 12 Skills
- [ZeroPointRepo/youtube-skills](https://github.com/ZeroPointRepo/youtube-skills) — 12 Skills
- [ZhangHanDong/makepad-skills](https://github.com/ZhangHanDong/makepad-skills) — 14 Skills
- [zhuyansen/backlink-guard](https://github.com/zhuyansen/backlink-guard) — 1 Skill
- [zhuyansen/new-term-radar](https://github.com/zhuyansen/new-term-radar) — 3 Skills
- [zilliztech/mfs](https://github.com/zilliztech/mfs) — 4 Skills
- [zilliztech/milvus-skill](https://github.com/zilliztech/milvus-skill) — 1 Skill
- [zincio/skills](https://github.com/zincio/skills) — 13 Skills
- [zscole/model-hierarchy-skill](https://github.com/zscole/model-hierarchy-skill) — 1 Skill
- [zxkane/aws-skills](https://github.com/zxkane/aws-skills) — 6 Skills
<!-- CATALOG:END -->

# Independent query-writing task

You are the query-writing model. You are not the card author and will not label answers.

Work only from the category names and scenario themes below. Do not inspect the repository, any cards, any `SKILL.md`, source code, indexes, search results, or previous smoke tests. Do not use skill names, repository names, vendor names, or card IDs in the queries.

## Categories and permitted scenario themes

### `api-development`

Situations involving REST endpoint design, request and response structures, OpenAPI specifications, API documentation, mocking, versioning, compliance, SDK generation, health monitoring, integration, usage limits, and converting existing API descriptions or collections into another useful form.

### `frontend-design`

Situations involving new or existing interfaces, redesigns, design-system consistency, accessibility, platform-specific Apple design guidance, components, layout, motion, typography, dark mode, mobile and desktop behavior, and evidence from screenshots or existing code.

### `seo`

Situations involving search traffic, crawlability, indexing, site audits, title improvement, internal links, content refreshes, domain migrations, SERP and competitor research, authority and outreach, structured content, AI search visibility, and revenue-oriented prioritization.

### `social-media-publishing`

Situations involving publishing or scheduling text, images, articles, and videos; one or multiple target platforms; platform-specific constraints; account sessions; visibility; media attachments; publishing queues; and confirmation that content was actually published.

### `test-automation`

Situations involving writing or repairing automated tests, browser and mobile testing, unit and end-to-end suites, framework selection, flaky tests, test migration, local or cloud execution, cross-browser coverage, and assertions or project structure.

## Main query set

Write exactly 15 realistic user requests per category, 75 total. Use both English and Traditional Chinese within every category. Vary the user's material, desired finished artifact, and constraints. Include some requests that could plausibly fit more than one Skill. Do not answer the requests and do not assign suitable or unsuitable Skills.

Write `experiment/queries.json` as a JSON list. Each item must contain only:

- `id`: a unique identifier.
- `category`: one of the five category IDs above.
- `query`: the user's request.

## Vague query set for the follow-up-question experiment

Also write exactly 20 additional requests that name only a broad topic, tool type, or category and omit the actual job. Spread them across the five categories and use both English and Traditional Chinese. For each, privately record a specific intended job that could be revealed after one clarifying question.

Write `experiment/vague-queries.json` as a JSON list. Each item must contain only:

- `id`: a unique identifier.
- `category`: one of the five category IDs above.
- `query`: the intentionally vague request.
- `true_intent`: the specific job the user had in mind, including the desired finished artifact.

Do not inspect any Skill material while writing either file. Stop after writing and validating the two JSON files.

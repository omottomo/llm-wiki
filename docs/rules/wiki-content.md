# Content-Mode Rules — Wiki Authoring

> Module of the repo's operating rules, split out of `CLAUDE.md`.
> **Read this before creating or editing anything under `wiki/`.** It governs the librarian
> skills (`wiki-ingest` / `wiki-query` / `wiki-lint` / `wiki-delete`) and any other change to
> wiki prose. The common rules in `CLAUDE.md` (language rule, core principles, log.md, skill
> routing) always apply on top of this file.

---

## 1. Page authoring rules

Every page under `wiki/` follows this format. **Body text is Korean; structure and frontmatter keys are English.**

### Frontmatter (YAML)
```yaml
---
title: <page title, in Korean>
label: "<short Korean citation label>"     # source pages ONLY, e.g. "#7 메타 엔지니어 실전편"
type: entity | concept | source | analysis | overview
created: 2026-05-31
updated: 2026-05-31
sources: [source-slug-1, source-slug-2]   # source slugs this page relies on
tags: [<tag1>, <tag2>]                    # tags in Korean
---
```

### Body
- **Cross-links use wikilink syntax** `[[page-name]]` (compatible with Obsidian graph view).
- **Every body wikilink MUST carry a Korean alias** — without one, Quartz renders the raw English slug (`harness-engineering`) in the middle of Korean prose. The alias is:
  - for `sources/` pages → the target's frontmatter `label` (short, `#N` playlist prefix, no brackets/`$`/`|`);
  - for all other pages → the target's `title`, shortened deterministically: drop a leading `분석 — `, keep only the part before ` — ` / `: `, strip a trailing ` (...)`, keep only the part before ` / `. (e.g. `CLAUDE.md (컨텍스트 파일)` → `CLAUDE.md`.)
  - Inside markdown tables, escape the pipe: `[[page\|별칭]]`.
  - Match the trailing josa to the alias (받침 rules: 이/가, 을/를, 은/는, 과/와, 으로/로).
- When you first mention a new proper noun or concept, link it with `[[...]]` on the spot, and **if the target page doesn't exist, create at least a stub.** Never leave orphan links dangling.
- Every factual claim carries a **source reference**, e.g. `... (→ [[sources/article-foo|라벨]])`. Multiple citations are joined with `·` inside one paren — `(→ [[sources/a|라벨A]]·[[sources/b|라벨B]])` — never a comma plus repeated `→`. **A source page never cites itself**; on `sources/` pages, cite only *other* pages.
- Mark anything uncertain as an estimate. Never fabricate facts without a source.
- **Never write absolute local filesystem paths** (e.g. `/Users/...`) anywhere in a wiki page — the wiki is published to the web, and an absolute path leaks the operator's username and directory layout. Cite raw sources with the repo-relative form only: `raw: raw/<slug>.md`. (Found the hard way: 5 source pages shipped absolute paths and would have published them; fixed 2026-07-12.)
- **New page vs. edit heuristic:** create a **new page** only when the subject is a distinct entity or concept that other pages would link to with `[[...]]`. If the information is merely an attribute or update of an existing subject, **edit that existing page** instead. When in doubt, edit — page proliferation causes drift.
- **As-of dating for volatile claims:** this domain moves fast. Any time-sensitive claim (pricing, model names, tool capabilities, versions, market share) must carry an as-of marker in the text. Write it in Korean, exactly like this: `(2026-06 기준)`. A claim without a date cannot be judged stale later.

### Source summary page (`sources/`) — required template

Reproduce these headings **verbatim** — they are Korean by design, and the body under each is
Korean too. The canonical copy lives at `.claude/skills/wiki-ingest/templates/source-page.md`;
keep the two in sync.

```markdown
## 한 줄 요약
## 핵심 내용 (3~7 bullets)
## 주요 주장 / 데이터
## 기존 위키와의 연결
- 강화: which claim in [[...]] this supports
- 모순: conflicts with [[...]] — (how it conflicts)
- 신규: new [[...]] introduced here
## 출처 정보 (raw path, author, date, URL)
```

---

## 2. index.md (content-oriented catalog)

The table of contents. List every page by category, each with **a link plus a one-line description, in Korean**.
Before answering any query, **always read index.md first** to locate the relevant pages, then drill in.
Update index.md on every ingest.

Example of the required output (Korean, as mandated by the language rule):
```markdown
## Entities
- [[entities/홍길동]] — 핵심 인물, 자료 3건에서 언급
## Concepts
- [[concepts/RAG]] — 검색증강생성, overview의 핵심 축
## Sources
- [[sources/article-foo]] — 2026-05-30 흡수, RAG 한계 다룸
## Analysis
- [[analysis/RAG-vs-wiki]] — 두 접근 비교표
```

**Scaling criteria** (revisit when crossed):
- When `sources/` exceeds ~100 files, the flat index stops scaling — evaluate a hybrid search tool (e.g. `qmd`: BM25 + vector + LLM re-rank) instead of index+grep.
- When a single category in index.md exceeds ~30 entries, introduce MOC (Map of Content) hub pages that cluster related pages, and link the MOCs from index.md.

---

## 3. Domain customization

> **Wiki domain:** Claude Code and harness engineering — technical topics only.
> **Focus:** comparing tool and workflow methodologies (the CLAUDE.md debate; building a harness up vs. slimming it down; single-tool vs. multi-model) and how practices shift over time.
> **Scope boundary (2026-07-12):** developer career strategy (resumes, job hunting, 이직/물경력) lives in the sibling `../career-llm-wiki` repo — the career pages this wiki once held were migrated there. When a new source is career-focused, tell the user it belongs in career-llm-wiki instead of ingesting it here.
> **Source types:** full YouTube transcripts (mostly Korean, some English) — `raw/youtube-<video_id>.md`

Domain-specific rules accumulated so far:

- Sources are auto-generated captions, so **speech-recognition errors are common** (e.g. "André Capaci" is really "Andrej Karpathy"). When a proper noun looks garbled, verify it via web search and record the correction on the source page under a section headed exactly `## 외부 검증 (date, 웹)`.
- Channel attribution: if the channel or author cannot be confirmed, write `(불확인)` or `미상` on the page — never guess.
- This domain changes monthly. The as-of dating rule in §1 is mandatory, and lint should treat claims older than ~6 months as candidates for re-verification.

Adjust the `entities/` and `concepts/` taxonomy and the page templates to fit the domain, and record any changed rules in this file so the next session inherits them.

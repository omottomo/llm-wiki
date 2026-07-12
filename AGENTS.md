# LLM Wiki — Agent Operating Rules (Schema)

This file defines the rules the agent **must always** follow when working with this wiki.
(For Claude Code, name this file `CLAUDE.md`; for Codex and most other agents, `AGENTS.md`. The content is identical.)

You are the **librarian** of this repository. You don't just answer questions ad hoc like a generic chatbot.
Your job is to **accumulate** what you read into a structured wiki and **keep it current**.

> **LANGUAGE RULE (critical):**
> - These operating files and skills are written in **English** (for the agent to read).
> - But **all wiki content you write — every page under `wiki/`, every `index.md` entry, every `log.md` line, every summary, every page body and frontmatter `title`/`tags` — MUST be written in Korean (한국어).**
> - Page *filenames/slugs* may stay in romanized ASCII for portability (e.g. `sources/article-foo.md`), but the human-readable `title` field and all body text are Korean.
> - When you talk to the user in chat, also use Korean.

---

## 1. Three-layer structure

```
ai-llm-wiki/
├── AGENTS.md          # this file. operating rules (= schema)
├── CLAUDE.md          # Claude Code stub that imports @AGENTS.md
├── .claude/
│   └── skills/        # per-task workflows (wiki-ingest / wiki-query / wiki-lint / wiki-delete)
├── scripts/           # deterministic helper scripts (e.g. lint_wiki.py)
├── raw/               # source documents (IMMUTABLE)
│   └── assets/        # downloaded images, etc.
├── wiki/              # markdown you generate & maintain (YOU own this)
│   ├── index.md       # full catalog (content-oriented)
│   ├── overview.md    # one page surveying the whole domain
│   ├── entities/      # proper nouns: people, orgs, products, places
│   ├── concepts/      # concepts, topics, themes
│   ├── sources/       # per-source summaries (1:1 with raw/)
│   └── analysis/      # query answers worth keeping (comparisons, analyses, connections)
└── log.md             # chronological work log (append-only)
```

**Core principles (never violate):**

1. **Never modify or delete anything in `raw/`.** Read only. It is the source of truth.
2. **You fully own `wiki/`.** The human only reads it; you write, edit, and cross-link it.
3. **The wiki is a compounding asset.** Do not re-synthesize from scratch on every question. First find and read the pages you already built, then build on top of them.
4. When a new source **contradicts** an existing claim, do not delete either — record both and flag the contradiction explicitly.

---

## 2. Page authoring rules

Every page under `wiki/` follows this format. **Body text is Korean; structure/frontmatter keys are English.**

### Frontmatter (YAML)
```yaml
---
title: 페이지 제목 (한국어)
type: entity | concept | source | analysis | overview
created: 2026-05-31
updated: 2026-05-31
sources: [source-slug-1, source-slug-2]   # source slugs this page relies on
tags: [태그1, 태그2]                        # tags in Korean
---
```

### Body
- **Cross-links use wikilink syntax** `[[page-name]]` (compatible with Obsidian graph view).
- When you first mention a new proper noun or concept, link it with `[[...]]` on the spot, and **if the target page doesn't exist, create at least a stub.** Never leave orphan links dangling.
- Every factual claim carries a **source reference**, e.g. `... (→ [[sources/article-foo]])`.
- Mark anything uncertain as an estimate/uncertain. Never fabricate facts without a source.
- **New page vs. edit heuristic**: create a **new page** only when the subject is a distinct entity/concept that other pages would link to with `[[...]]`. If the information is merely an attribute or update of an existing subject, **edit that existing page** instead. When in doubt, edit — page proliferation causes drift.
- **As-of dating for volatile claims**: this domain moves fast. Any time-sensitive claim (pricing, model names, tool capabilities, versions, market share) must carry an as-of marker in the text, e.g. `(2026-06 기준)`. A claim without a date cannot be judged stale later.

### Source summary page (`sources/`) — required template
ALWAYS use this structure (headings here shown in English for clarity, but **write them and the content in Korean**):
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

## 3. index.md (content-oriented catalog)

The table of contents. List every page by category, each with **a link + a one-line description (in Korean)**.
Before answering any query, **always read index.md first** to locate relevant pages, then drill in.

Example:
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
Update index.md on every ingest.

**Scaling criteria** (revisit when crossed):
- When `sources/` exceeds ~100 files, the flat index stops scaling — evaluate a hybrid search tool (e.g. `qmd`: BM25 + vector + LLM re-rank) instead of index+grep.
- When a single category in index.md exceeds ~30 entries, introduce MOC (Map of Content) hub pages that cluster related pages, and link the MOCs from index.md.

---

## 4. log.md (chronological, append-only)

Append one line per action. **Always start with a consistent prefix** so it stays greppable:

```markdown
## [2026-05-31] ingest | 자료 제목 — 페이지 N개 갱신
## [2026-05-31] query  | 질문 요지 — analysis/foo 로 보존
## [2026-05-31] lint   | 모순 2건, 고아 1건 발견 → 처리
```

Check last 5 entries: `grep "^## \[" log.md | tail -5`

---

## 5. Which skill to use when

- User drops a new source into `raw/` and says "흡수해 / 정리해 / ingest" → **wiki-ingest**
- User asks a question about the wiki → **wiki-query**
- User says "점검 / 건강검진 / 정리 / lint" → **wiki-lint**
- User says "삭제 / 지워 / 제거 / delete / 위키 비워" → **wiki-delete** (destructive — always confirm scope first; never touch `raw/`)

When running a skill, follow that skill's SKILL.md procedure exactly.

---

## 6. Domain customization

> Wiki domain: **Claude Code · 하네스 엔지니어링, 그리고 AI 시대 개발자 커리어 전략**
> Focus on: 도구/워크플로 방법론 비교 (CLAUDE.md 논쟁, 하네스 구축 vs 다이어트, 단일 도구 vs 멀티 모델), 시간에 따른 실천법 변화, 커리어 적용점
> Source types: 유튜브 자막 전문 (한국어 위주, 일부 영어) — `raw/youtube-<video_id>.md`

Domain-specific rules accumulated so far:
- Sources are auto-generated captions, so **speech-recognition errors are common** (e.g. "André Capaci" = Andrej Karpathy). When a proper noun looks garbled, verify via web search and record the correction in a `## 외부 검증 (date, 웹)` section on the source page.
- Channel attribution: if the channel/author cannot be confirmed, write `(불확인)`/`미상` — never guess.
- This domain changes monthly; the as-of dating rule in §2 is mandatory, and lint should treat claims older than ~6 months as candidates for re-verification.

Adjust the `entities/`·`concepts/` taxonomy and page templates to fit the domain, and record any changed rules in this file so the next session inherits them.

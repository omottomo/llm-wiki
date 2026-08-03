# Content-Mode Rules — Wiki Authoring

> Module of the repo's operating rules, split out of `CLAUDE.md`.
> **Read this before creating or editing anything under `wiki/`.** It governs the librarian
> skills (`wiki-ingest` / `wiki-query` / `wiki-lint` / `wiki-delete` / `wiki-refresh`) and any
> other change to wiki prose. The common rules in `CLAUDE.md` (language rule, core principles,
> docs/log.md, skill routing) always apply on top of this file.

---

## 1. Page authoring rules

Every page under `wiki/` follows this format. **Body text is Korean; structure and frontmatter keys are English.**

### Frontmatter (YAML)
```yaml
---
title: <page title, in Korean>
label: "<short Korean citation label>"     # source pages ONLY, e.g. "#7 메타 엔지니어 실전편"
type: entity | concept | source | analysis | overview
credibility: high | medium | low          # source pages ONLY — reliability of the source's claims (rubric below)
volatility: hot | warm | cold             # source pages ONLY — how often the underlying source changes (rubric below)
created: 2026-05-31
updated: 2026-05-31
sources: [source-slug-1, source-slug-2]   # source slugs this page relies on
aliases: [alt-name-1, alt-name-2]         # OPTIONAL, concepts/entities — alternate search names (see below)
tags: [<tag1>, <tag2>]                    # tags in Korean
---
```

**`credibility` (source pages only, required).** Grades how much a reader should trust the
source's factual claims — a signal `wiki-query` uses to weight one source over another when
sources disagree (a `high` source outweighs a `low` one). Judge it once at ingest:

- **high** — official documentation, specifications, or first-party / primary sources. (e.g. the Terraform and IBM pages.)
- **medium** — secondary explainer content whose load-bearing claims are corroborated by primary sources or by other wiki pages; identifiable practitioner talks or company blogs.
- **low** — sources with unverifiable authorship (`미상` / `불확인`), known caption / transcription errors on load-bearing facts, or primarily speculative / opinion framing without corroboration. Auto-generated captions raise error risk (§3) but do **not** by themselves force `low` — downgrade only when a material error was actually found, or attribution can't be confirmed *and* the claims aren't corroborated elsewhere.

`credibility` is graded from source quality, independent of `updated`; a metadata-only change to
it does not bump `updated` (§4.3).

**`volatility` (source pages only, required).** Grades how likely the underlying source is to
change after ingest — a signal the wiki-refresh skill uses to target re-checks. Judge it once at
ingest, from the source's nature, not its content:

- **cold** — a fixed snapshot: a published article, a YouTube talk, anything captured once and
  frozen at ingest time (e.g. `raw/youtube-*.md`).
- **hot** / **warm** — living official documentation that gets edited over time (e.g. the
  Terraform and IBM pages); `hot` for documentation revised frequently, `warm` for documentation
  that still changes but less often. When unsure between a fixed article and living docs, default
  to `cold` — only genuinely living documentation earns `hot`/`warm`.

Like `credibility`, `volatility` is metadata about the source, not its content; a metadata-only
change to it does not bump `updated` (§4.3).

**`aliases` (concepts / entities, optional).** A YAML list of alternate names for the page —
typically the English original term behind a Korean title (`title: 컨텍스트 엔지니어링` →
`aliases: [context engineering]`), or a common abbreviation. Quartz reads `aliases` natively,
so an alias makes the page findable by its English term in site search even though the title is
Korean (the Korean-title rule in §4.4 otherwise hides the original term from search). Add one
whenever a page's subject is widely known under a second name; leave it off otherwise. Not a
citation surface — `[[...]]` links still target the slug.

### Body
- **`concepts/`, `entities/` and `analysis/` pages open with a lead paragraph** (2026-08-02,
  phase-10). Immediately after the H1 and before the first `## ` heading, write **three or four
  Korean sentences aimed at a reader with no background**: the first states plainly what the
  subject is and expands any jargon on the spot; the rest say why it matters or when it comes up
  (for an `analysis/` page: what question it answers and what it concludes). The lead carries
  **no citation paren and no wikilink** — `site/build.py` lifts its first sentence into listings,
  search results and the page's `<meta description>`/`og:description`, so it has to read
  standalone. `sources/` pages are exempt: their `## 한 줄 요약` already plays this role and is
  what the extractor reads instead. A page whose body opens straight into a `## ` heading yields
  an empty summary and renders with no description anywhere.
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

### Librarian-only sections — written, never deleted, never published

Two parts of the template above exist for the librarian and are **filtered out at render time**
by `site/build.py` (`strip_internal_sections`, blocklist in `site-code.md` §2.4):

| Not rendered | Why it still must be written |
|---|---|
| the whole `## 기존 위키와의 연결` section | `wiki-query` and `wiki-lint` read it to trace what a source reinforced, contradicted or created |
| the `- raw: raw/<slug>.md` bullet inside `## 출처 정보` | the raw↔wiki parity check in `lint_wiki.py` and every later re-read depend on it |

So: keep writing both exactly as the template says. **Never delete them from `wiki/` to "clean up
the site"** — the site already ignores them, and removing them breaks the skills that read them.
The rest of `## 출처 정보` (author, collection date, URL) *is* published.

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

> **Wiki charter (2026-07-19):** a growing personal knowledge base in the spirit of Karpathy's
> LLM-wiki experiment (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — it
> absorbs whatever sources the user chooses to ingest and is **not limited to any playlist or
> medium**. Never describe the wiki itself as "a digest of the YouTube playlist" on wiki pages;
> the 25-video playlist was only the initial seed (2026-06-23), and non-playlist web documents
> have been ingested since 2026-07-18.
> **Current center of gravity:** Claude Code and harness engineering — technical topics.
> **Focus:** comparing tool and workflow methodologies (the CLAUDE.md debate; building a harness up vs. slimming it down; single-tool vs. multi-model) and how practices shift over time.
> **Scope boundary (2026-07-12):** developer career strategy (resumes, job hunting, 이직/물경력) lives in the sibling `../career-llm-wiki` repo — the career pages this wiki once held were migrated there. When a new source is career-focused, tell the user it belongs in career-llm-wiki instead of ingesting it here.
> **Source types:** full YouTube transcripts (mostly Korean, some English) — `raw/youtube-<video_id>.md`; since 2026-07-18 also web articles / official docs saved as `raw/<slug>.md`.

Domain-specific rules accumulated so far:

- Sources are auto-generated captions, so **speech-recognition errors are common** (e.g. "André Capaci" is really "Andrej Karpathy"). When a proper noun looks garbled, verify it via web search and record the correction on the source page under a section headed exactly `## 외부 검증 (date, 웹)`.
- Channel attribution: if the channel or author cannot be confirmed, write `(불확인)` or `미상` on the page — never guess.
- This domain changes monthly. The as-of dating rule in §1 is mandatory, and lint should treat claims older than ~6 months as candidates for re-verification.

Adjust the `entities/` and `concepts/` taxonomy and the page templates to fit the domain, and record any changed rules in this file so the next session inherits them.

---

## 4. Conventions (tags, citations, dates, titles)

### 4.1 Controlled tag vocabulary

Tags are **Korean by default** (§1 frontmatter). Each concept gets **exactly one canonical
tag form** — no case variants (`Codex` vs `codex`), no script variants (Latin vs Korean for
the same referent), no spacing/hyphenation variants. When you add a tag, check it against the
merge table below before writing it; when you encounter an existing page with a non-canonical
variant, normalize it to the canonical form as part of whatever edit touches that page (do not
do a repo-wide sweep just for this — that is lint's job, not authoring's).

Audited variant pairs and their canonical form:

| Variant forms found in the corpus | Canonical tag |
|---|---|
| 하네스 / 하네스엔지니어링 | `하네스엔지니어링` |
| 클로드코드 / ClaudeCode / 클로드봇 | `클로드코드` |
| 클로드md / claude-md / CLAUDE-md | `클로드md` |
| 코덱스 / Codex | `코덱스` |
| 온디바이스AI / 엣지AI | `온디바이스AI` |
| MCP / mcp | `MCP` — 통용 한글형이 없는 두문자어. 개념 페이지 제목도 `MCP (Model Context Protocol)`. 대소문자 변형이라 lint 가 정규화만으로 잡으므로 `KNOWN_TAG_VARIANT_GROUPS` 에는 넣지 않는다 |

**Semantic consolidations (2026-07-19 lint).** Unlike the rows above (case/script/spacing
variants the deterministic linter catches by normalization), these are *semantic* near-duplicates
that the linter reports 0 hard collisions for. A lint pass merged them to the canonical form:

| Variant forms found in the corpus | Canonical tag |
|---|---|
| 역할변화 / 직업변화 / 개발자역할 / 개발자역할변화 | `개발자역할변화` (단 `개발자`·`일자리` 는 더 포괄적이라 유지) |
| API비용 / API비용절감 / 토큰비용 / 비용절감 | `비용절감` (단 `토큰관리` 는 관리 측면이라 별개) |
| 기초 / 기초역량 / 기초개념 | `기초개념` (단 `핵심개념` 은 "핵심"이라 별개) |
| 진화 / 진화서사 | `진화서사` |
| 적대적검증 / 적대적리뷰 | `적대적리뷰` (본문 헤더가 "적대적 리뷰(Adversarial Review)") |
| 워크플로우최적화 / 워크플로우 | `워크플로우` |
| 기업 / 조직 | `조직` — 엔티티 유형 태그. `AI기업` 은 하위 성격 태그라 병기 유지 |
| AI자동화 / 자동화 | `자동화` |
| 컨텍스트 / 컨텍스트엔지니어링 | `컨텍스트엔지니어링` (단 `컨텍스트부패`·`신선한컨텍스트` 는 별개 개념) |

의도적으로 병합하지 **않은** 근접쌍: `카파시`(인물) vs `카파시가이드라인`(그의 65줄 지침) — 지시 대상이
다른 별개 개념이다. 위 표는 문서(사람·에이전트)용 기록이며, 이 시맨틱 변형들을 결정적 linter 의
`KNOWN_TAG_VARIANT_GROUPS` 에 넣어 재도입을 자동 차단하는 것은 code-mode 후속 작업으로 남긴다
(정규화가 아닌 이름 매핑이라 스크립트 수정이 필요).

This table is not exhaustive — it records what a corpus audit found, not every tag that could
ever collide. When wiki-lint's tag-hygiene report flags a new variant pair, add it here.

### 4.2 Source citations use the wikilink-alias form, never a bare `#N`

Every in-body citation to a source must be a wikilink with an alias, per §1: `(→ [[sources/article-foo|라벨]])`. **Never write a bare `#7` or `#7번`** as a citation — a leading `#`
followed by digits is exactly the syntax Quartz's tag plugin scans for, so a bare hash-number in
body text gets parsed as a tag, not read as a citation. If you need to reference a source's
playlist number in prose, embed it inside the wikilink alias (the `label` frontmatter field
already carries this, e.g. `label: "#7 메타 엔지니어 실전편"`) rather than writing the hash mark
loose in a sentence.

**The citation format is load-bearing, not decorative** (2026-08-02, phase-10).
`site/build.py`'s `render_citations` parses `(→ [[sources/slug|#N 라벨]])` and collapses it into
a numbered superscript chip, taking the chip's number from the `#N` prefix of the label and its
tooltip from the whole label; a group holding only `sources/` links loses its `(→ … )` wrapper
entirely. Consequences for authoring: a citation written in any other shape (a different arrow, a
comma instead of `·`, a label with no `#N`) is not recognised as a citation and renders as raw
text in the middle of the sentence — the parser degrades quietly, it does not error. Deviating
from §1's citation form is therefore a rendering bug, not a style preference. This coupling runs
the same way as `KNOWN_TAG_VARIANT_GROUPS` (§4.1): the convention lives here, the parser mirrors
it — edit one, edit the other.

### 4.3 Bump `updated` only when content changes

The frontmatter `updated` date (§1) reflects the last time the page's **claims, structure, or
sources** changed — not the last time it was touched. A formatting-only pass (fixing a wikilink
alias, normalizing a tag per §4.1, correcting a typo) leaves `updated` as-is. If you're unsure
whether an edit counts as content, ask: would a reader who last read this page need to re-read
it to stay current? If no, don't bump the date.

**This rule applies retroactively, and it is not cosmetic.** It was written 2026-07-13, after
the readability pass that bumped 21 pages for what was purely alias/tag/josa formatting; those
dates were restored to their pre-pass values on 2026-07-17. The reason to care: `updated` is
what the site actually sorts by — `created-modified-date` reads `frontmatter` first (see
`site/quartz.config.yaml`), so the "최근 변경" sidebar ranks on it. A formatting bump does not
just break a convention, it evicts genuinely-updated pages from that list. When you find a past
bump that no content change justifies, restore the previous value from git rather than leaving
it — but confirm it is formatting-only by comparing the prose with every wikilink and citation
paren stripped, because an alias-level diff looks like a content diff and is not.

### 4.4 Frontmatter titles must be Korean, with a proper-noun exception for entities

`sources/` and `concepts/` page titles must contain Hangul — the title is not required to be
*entirely* Korean (a page can still name a Latin proper noun, e.g. `CLAUDE.md (컨텍스트 파일)`),
but at least one Hangul character must be present. `entities/` pages may use a Latin proper noun
as the title with no Hangul requirement (e.g. `Claude Code`, `Codex (OpenAI)`) — the entity
*is* the proper noun, and forcing a Korean gloss into the title would be awkward where the
industry itself uses the Latin name. This does not relax the body-text language rule in
`CLAUDE.md` — only the frontmatter `title` field gets this exception, and only for entities.

---

## 5. Refresh workflow (wiki-refresh)

Governs `wiki-refresh`, the skill that re-checks `hot`/`warm` sources (§1 `volatility`) for
drift and updates the wiki only after the human confirms. `cold` sources are out of scope —
they are frozen snapshots by design.

**New-capture naming.** `raw/` is immutable (CLAUDE.md core principle 1) — a refresh never
edits the original `raw/<slug>.md`. When a re-fetch turns up a *material* (non-cosmetic) change,
save the fresh fetch as a new file `raw/<slug>-<YYYY-MM-DD>.md` (original slug + refresh date,
ISO). Cosmetic-only changes (wording/formatting with no factual delta) need no new capture.

**Refresh history.** Every refresh check, whatever its outcome, is recorded on the source page
`wiki/sources/<slug>.md` under a `## 최신화 이력` section (create it after `## 출처 정보` if
absent), one line per check: date, classification (cosmetic/additive/contradictory), and the new
raw slug if one was created. When a new capture is added, also append its slug to the source
page's frontmatter `sources:` list (§1) and bump `updated` — a material capture is real content,
not metadata, so the §4.3 metadata-only exemption does not apply.

**Contradictions.** Handled exactly like ingest (§1 `기존 위키와의 연결` / 모순): keep both the
old and new claim, flag the contradiction explicitly on the affected page(s) — never silently
overwrite (CLAUDE.md core principle 4).

**Human gate.** No wiki page is edited, and no new raw file is saved, until the human has seen
the diff classification and confirmed. This mirrors `wiki-delete`'s confirm-before-mutate
discipline — refresh mutates less destructively, but the same one-way-door caution applies to
any content change on a page the human may already be relying on.

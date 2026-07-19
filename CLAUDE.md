# LLM Wiki — Agent Operating Rules (Schema)

This file holds the **common rules** that apply to every session in this repository.
Area-specific rules are split into modules under `docs/rules/` and are read only when you
work in that area — §4 says which module to read when. `docs/index.md` catalogs everything
under `docs/`.

You are the **librarian** of this repository. You don't just answer questions ad hoc like a
generic chatbot. Your job is to **accumulate** what you read into a structured wiki and
**keep it current**.

> **LANGUAGE RULE (critical):**
> - This file, every skill and agent definition under `.claude/`, and every operating document under `docs/` (rule modules, plans, PRDs) are written in **English** — these are agent-facing operating files.
> - But **all wiki content you write — every page under `wiki/`, every `index.md` entry, every `log.md` line, every summary, every page body and frontmatter `title`/`tags` — MUST be written in Korean (한국어).**
> - Page *filenames/slugs* stay in romanized ASCII for portability (e.g. `sources/article-foo.md`), but the human-readable `title` field and all body text are Korean.
> - **When you talk to the user in chat, use Korean.**
> - Korean therefore survives in the operating files in exactly two places, and both are deliberate: (a) **trigger phrases** the user literally types (§3), and (b) **output specimens and required literals** the agent must reproduce verbatim on wiki pages (the log examples in §2, the templates and markers in `docs/rules/wiki-content.md`). Do not "clean these up" into English — that would break skill routing and make the agent write English wiki pages.

---

## 1. Repository structure

```
llm-wiki/
├── CLAUDE.md          # this file. common operating rules — always in force.
├── .claude/
│   ├── skills/        # per-task workflows (content: wiki-ingest / wiki-query / wiki-lint / wiki-delete)
│   │                  #   code-mode skills come from the my-skills plugin — see §3
│   ├── orchestrate.md # project adapter for the my-skills plugin's orchestrate workflow
│   └── settings.json  # project permissions
├── scripts/           # deterministic helper scripts (lint_wiki.py, verify_site.py)
├── docs/
│   ├── index.md       # catalog of everything under docs/ — keep it current
│   ├── rules/         # area-specific rule modules (see §4)
│   │   ├── wiki-content.md   # content mode: page authoring, index.md, domain rules
│   │   └── site-code.md      # code mode: coding discipline, site publishing, verification
│   └── tasks/         # phase-{N}-{slug}/ — plan.md + prd.json per phase
├── raw/               # source documents (IMMUTABLE, NEVER PUBLISHED)
│   └── assets/        # downloaded images, etc.
├── wiki/              # markdown you generate & maintain (YOU own this)
│   ├── index.md       # full catalog (content-oriented)
│   ├── overview.md    # one page surveying the whole domain
│   ├── entities/      # proper nouns: people, orgs, products, places
│   ├── concepts/      # concepts, topics, themes
│   ├── sources/       # per-source summaries (1:1 with raw/)
│   └── analysis/      # query answers worth keeping (comparisons, analyses, connections)
├── site/              # Quartz 5 static-site generator (content/ → symlink to ../wiki)
└── log.md             # chronological work log (append-only)
```

**Two modes, one repo.** **Content mode** — you are the librarian maintaining `wiki/` — is
governed by this file plus `docs/rules/wiki-content.md`. **Code mode** — you build the
published site: `site/`, `scripts/`, `.github/`, root config — is governed by this file plus
`docs/rules/site-code.md`. They share the repo but not the rules — know which one you are in
before you touch anything.

**Core principles (never violate):**

1. **Never modify or delete anything in `raw/`.** Read only. It is the source of truth — and it must **never** be published to the web or land in a public repo (the boundary and its audit: `docs/rules/site-code.md`).
2. **You fully own `wiki/`.** The human only reads it; you write, edit, and cross-link it.
3. **The wiki is a compounding asset.** Do not re-synthesize from scratch on every question. First find and read the pages you already built, then build on top of them.
4. When a new source **contradicts** an existing claim, do not delete either — record both and flag the contradiction explicitly.

---

## 2. log.md (chronological, append-only)

Append one line per action. **Always start with a consistent prefix** so the log stays greppable.
Entries are Korean — they are content, not operating instructions:

```markdown
## [2026-05-31] ingest | 자료 제목 — 페이지 N개 갱신
## [2026-05-31] query  | 질문 요지 — analysis/foo 로 보존
## [2026-05-31] lint   | 모순 2건, 고아 1건 발견 → 처리
## [2026-05-31] site   | phase-1-quartz-publishing — Quartz 스캐폴딩 + Cloudflare 배포
```

The `site` prefix covers code-mode work (`docs/rules/site-code.md`): a Quartz, scripts, or CI phase gets **one** line at close-out, not one per task.

Check the last 5 entries: `grep "^## \[" log.md | tail -5`

---

## 3. Which skill to use when

Trigger phrases are quoted in the language the user actually types them in. Match on intent, not on an exact string.

**Content mode** (you are the librarian; rules: this file + `docs/rules/wiki-content.md`):
- The user drops a new source into `raw/` and says "흡수해 / 정리해 / ingest" → **wiki-ingest**
- The user asks a question about the wiki → **wiki-query**
- The user says "점검 / 건강검진 / 정리 / lint" → **wiki-lint**
- The user says "삭제 / 지워 / 제거 / delete / 위키 비워" → **wiki-delete** (destructive — always confirm scope first; never touch `raw/`)

**Code mode** (you are building the published site; rules: this file + `docs/rules/site-code.md`). These skills ship with the **`my-skills` plugin**, not this repo — their project-specific knowledge (protected paths, verification gate, log convention, language) comes from the adapter at `.claude/orchestrate.md`:
- A plan has been agreed in conversation and the user says "prd 만들어 / prd.json 생성 / create the prd" → **`/my-skills:create-prd-json`** (writes `docs/tasks/phase-{N}-{slug}/prd.json`)
- A `plan.md` or `prd.json` exists and the user wants it executed → **`/my-skills:orchestrate @docs/tasks/<phase>/plan.md`** (spawns the planner → evaluator → builders team)

**Routing rule:** if a request would change `wiki/` prose, it is content mode — never send it to the orchestrate skill. If it would change `site/`, `scripts/`, `.github/`, or root config, it is code mode — never do it by hand-editing during an ingest.

When running a skill, follow that skill's SKILL.md procedure exactly.

---

## 4. Rule modules under docs/rules/

This file stays minimal on purpose. Area-specific rules live in `docs/rules/` and are
**mandatory reading before touching that area** — they carry the same authority as this file.

| Before you touch | Read first |
|---|---|
| `wiki/` prose — any ingest, query file-back, lint fix, or deletion | `docs/rules/wiki-content.md` |
| `site/`, `scripts/`, `.github/`, root config — any code-mode work | `docs/rules/site-code.md` |

**Where to record new durable rules:**
- Domain/content rules (taxonomy tweaks, caption-error patterns, template changes) → `docs/rules/wiki-content.md`.
- Site/code constraints the next session would rediscover the hard way → `docs/rules/site-code.md` → "Accumulated rules".
- Rules that apply to **every** session regardless of mode → this file (keep it short).
- Whenever a document under `docs/` is added, moved, or removed → update `docs/index.md`.

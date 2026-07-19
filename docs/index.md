# docs/ — Operating Documents Catalog

Table of contents for everything under `docs/`. **Update this file whenever a document under
`docs/` is added, moved, or removed.** (Agent-facing operating file — English, per the
language rule in `CLAUDE.md`.)

## Structure

```
docs/
├── index.md                        # this catalog
├── rules/                          # mode-specific rule modules, split out of CLAUDE.md
│   ├── wiki-content.md             # content mode: page authoring, wiki index catalog, domain rules
│   └── site-code.md                # code mode: coding discipline, Quartz/Cloudflare publishing, verification
└── tasks/                          # one folder per code-mode phase: plan.md (+ prd.json once authored)
    ├── phase-1-quartz-publishing/
    │   ├── plan.md                 # Quartz 5 scaffolding + Cloudflare Pages deployment plan
    │   └── prd.json                # 10 atomic tasks (5 builder + 5 manual) decomposed from plan.md
    ├── phase-2-harness-efficiency/
    │   └── prd.json                # 13 builder tasks: fix operating-file drift/duplication, add deterministic helpers
    ├── phase-3-wiki-site-quality/
    │   └── prd.json                # 9 tasks (7 builder + 2 manual): lint quality gates, fonts, CI boundary audit, go-live
    ├── phase-4-namu-test-site/
    │   └── prd.json                # 13 tasks (11 builder + 2 manual): parallel site-test/ with a namu-style landing page and navigation
    └── phase-5-guided-home-redesign/
        └── plan.md                 # site-test guided home: card landing page, graph off, explorer + breadcrumbs on
```

## rules/ — when to read which

| Document | Read before |
|---|---|
| [rules/wiki-content.md](rules/wiki-content.md) | creating or editing `wiki/` prose — ingest, query file-back, lint fixes, deletion |
| [rules/site-code.md](rules/site-code.md) | touching `site/`, `scripts/`, `.github/`, or root config — any code-mode work |

Rule modules carry the same authority as `CLAUDE.md`; `CLAUDE.md` holds only the common rules
(language rule, repo structure, core principles, log.md, skill routing).

## tasks/ — phase plans and PRDs

| Phase | Contents |
|---|---|
| [tasks/phase-1-quartz-publishing/](tasks/phase-1-quartz-publishing/plan.md) | `plan.md` — Quartz 5 + Cloudflare Pages publishing plan; `prd.json` — 10 tasks: T01·T03–T07 done (2026-07-12), manual T02/T08–T10 open |
| [tasks/phase-2-harness-efficiency/](tasks/phase-2-harness-efficiency/prd.json) | `prd.json` — 13 builder tasks from the 2026-07-13 harness audit: replace the drifted raw-leak check in evaluator/planner, de-duplicate the verification matrix and PRD schema, drop wrong-path WORKDIR blocks from the four wiki skills, consolidate extraction references, add `lint_wiki.py --inbound`, permission allowlist, CLAUDE.md tree-label fix |
| [tasks/phase-3-wiki-site-quality/](tasks/phase-3-wiki-site-quality/prd.json) | `prd.json` — 9 tasks (7 builder + 2 manual) from the 2026-07-13 wiki/site audit: four new lint quality gates (label format, bare `#N` citations, Korean titles, tag hygiene), content conventions in wiki-content.md, font cleanup, CI workflow running `verify_site.py`, Cloudflare go-live + Korean-search verification |
| [tasks/phase-4-namu-test-site/](tasks/phase-4-namu-test-site/prd.json) | `prd.json` — 13 tasks (11 builder + 2 manual): a parallel `site-test/` (production `site/` untouched) serving a site-owned Korean landing page at the root and the wiki catalog at `/catalog` via symlinks, with folder navigation replaced by namu-style tag chips and a recent-changes sidebar. T01–T11 done (2026-07-13); manual T12 (Cloudflare test project) / T13 (human QA) open |
| [tasks/phase-5-guided-home-redesign/](tasks/phase-5-guided-home-redesign/plan.md) | `plan.md` — guided-home redesign of `site-test/` for first-time visitors (직관·단순·가독): card-layout home in site-owned `index.md` + `custom.scss`, graph view removed, explorer re-enabled, breadcrumbs on. Scope site-test only; `wiki/` untouched. PRD not yet authored |

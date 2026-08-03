# docs/ — Operating Documents Catalog

Table of contents for everything under `docs/`. **Update this file whenever a document under
`docs/` is added, moved, or removed.** (Agent-facing operating file — English, per the
language rule in `CLAUDE.md`.)

## Structure

```
docs/
├── index.md                        # this catalog
├── log.md                          # chronological work log (append-only; Korean entries — content, not operating prose)
├── backlog.md                      # ingest backlog — candidates & open questions (unpublished; not factual evidence)
├── benchmarking-nvk-llm-wiki.md    # 2026-07-19 comparison vs nvk/llm-wiki; drives phase-6/7 adoption
├── rules/                          # mode-specific rule modules, split out of CLAUDE.md
│   ├── wiki-content.md             # content mode: page authoring, wiki index catalog, domain rules
│   └── site-code.md                # code mode: coding discipline, static-site build & Cloudflare publishing, verification
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
    ├── phase-5-guided-home-redesign/
    │   └── plan.md                 # site-test guided home: card landing page, graph off, explorer + breadcrumbs on
    ├── phase-6-nvk-schema-docs/
    │   ├── plan.md                 # nvk benchmark part A: credibility/aliases fields, query depths, backlog, report
    │   └── prd.json                # 9 builder tasks
    ├── phase-7-nvk-skills-tests/
    │   ├── plan.md                 # nvk benchmark part B: volatility+refresh, retract mode, lint fixture tests
    │   └── prd.json                # 6 tasks (5 builder + 1 manual)
    ├── phase-8-minimal-site/
    │   ├── plan.md                 # design spec: replace both Quartz sites with hand-rolled minimal search-first site (built in web/, since consolidated to site/)
    │   ├── implementation.md       # step-by-step TDD implementation plan (full code per task)
    │   └── prd.json                # 7 tasks (6 builder + 1 manual)
    ├── phase-9-aws-deploy/
    │   ├── plan.md                 # AWS S3+CloudFront+Terraform deployment plan (human-executed; no prd.json; Korean by request)
    │   └── implementation.md       # step-by-step runbook: exact commands + full HCL/YAML per task (Korean by request)
    ├── phase-10-visitor-facing-site/
    │   ├── plan.md                 # visitor-facing readability: citation chips, global search, summaries, lead paragraphs
    │   └── prd.json                # 22 tasks (21 builder + 1 manual)
    ├── phase-11-ci-deploy-gate/
    │   ├── plan.md                 # merge the two push-triggered workflows so deploy declares needs: [verify, lint]
    │   └── prd.json                # 3 tasks (2 builder + 1 verify)
    └── phase-12-wiki-identity-copy/
        ├── plan.md                 # sweep the playlist framing and the "central topic = Claude Code" claim out of the wiki
        └── prd.json                # 8 tasks (7 builder + 1 evaluator)
```

## rules/ — when to read which

| Document | Read before |
|---|---|
| [rules/wiki-content.md](rules/wiki-content.md) | creating or editing `wiki/` prose — ingest, query file-back, lint fixes, deletion |
| [rules/site-code.md](rules/site-code.md) | touching `site/`, `scripts/`, `.github/`, or root config — any code-mode work |

Rule modules carry the same authority as `CLAUDE.md`; `CLAUDE.md` holds only the common rules
(language rule, repo structure, core principles, log.md, skill routing).

## Standalone documents

| Document | What it is |
|---|---|
| [log.md](log.md) | Chronological work log, append-only, one Korean line per action (`## [date] prefix \| ...`). Moved from the repo root 2026-07-20. |
| [backlog.md](backlog.md) | Ingest backlog — candidate sources & open questions queue. Unpublished, never citable as factual evidence. Moved from the repo root 2026-07-20. |
| [benchmarking-nvk-llm-wiki.md](benchmarking-nvk-llm-wiki.md) | 2026-07-19 comparison against `nvk/llm-wiki`: what it is, adopted items (with rationale) and rejected items (with reasons). Drives `phase-6-nvk-schema-docs` and `phase-7-nvk-skills-tests`. |

## tasks/ — phase plans and PRDs

| Phase | Contents |
|---|---|
| [tasks/phase-1-quartz-publishing/](tasks/phase-1-quartz-publishing/plan.md) | `plan.md` — Quartz 5 + Cloudflare Pages publishing plan; `prd.json` — 10 tasks: T01·T03–T07 done (2026-07-12), manual T02/T08–T10 open |
| [tasks/phase-2-harness-efficiency/](tasks/phase-2-harness-efficiency/prd.json) | `prd.json` — 13 builder tasks from the 2026-07-13 harness audit: replace the drifted raw-leak check in evaluator/planner, de-duplicate the verification matrix and PRD schema, drop wrong-path WORKDIR blocks from the four wiki skills, consolidate extraction references, add `lint_wiki.py --inbound`, permission allowlist, CLAUDE.md tree-label fix |
| [tasks/phase-3-wiki-site-quality/](tasks/phase-3-wiki-site-quality/prd.json) | `prd.json` — 9 tasks (7 builder + 2 manual) from the 2026-07-13 wiki/site audit: four new lint quality gates (label format, bare `#N` citations, Korean titles, tag hygiene), content conventions in wiki-content.md, font cleanup, CI workflow running `verify_site.py`, Cloudflare go-live + Korean-search verification |
| [tasks/phase-4-namu-test-site/](tasks/phase-4-namu-test-site/prd.json) | `prd.json` — 13 tasks (11 builder + 2 manual): a parallel `site-test/` (production `site/` untouched) serving a site-owned Korean landing page at the root and the wiki catalog at `/catalog` via symlinks, with folder navigation replaced by namu-style tag chips and a recent-changes sidebar. T01–T11 done (2026-07-13); manual T12 (Cloudflare test project) / T13 (human QA) open |
| [tasks/phase-5-guided-home-redesign/](tasks/phase-5-guided-home-redesign/plan.md) | `plan.md` — guided-home redesign of `site-test/` for first-time visitors (직관·단순·가독): card-layout home in site-owned `index.md` + `custom.scss`, graph view removed, explorer re-enabled, breadcrumbs on. Scope site-test only; `wiki/` untouched. Executed directly from `plan.md` 2026-07-19 (no prd.json); build/leak/nav/card checks pass, human visual QA pending |
| [tasks/phase-6-nvk-schema-docs/](tasks/phase-6-nvk-schema-docs/prd.json) | `plan.md` + `prd.json` — 9 builder tasks from the 2026-07-19 nvk/llm-wiki benchmark, part A: required `credibility` enum on source pages (rubric + lint + 27-page migration), optional `aliases` on concepts/entities, three wiki-query depths, root `backlog.md` ingest queue, the benchmark report (`docs/benchmarking-nvk-llm-wiki.md`), CLAUDE.md routing cleanup after the my-skills plugin removal. **T01–T09 done (2026-07-19)**; lint + both site builds + leak audits green |
| [tasks/phase-7-nvk-skills-tests/](tasks/phase-7-nvk-skills-tests/prd.json) | `plan.md` + `prd.json` — 6 tasks (5 builder + 1 manual), nvk benchmark part B: required `volatility` enum + migration, human-gated `wiki-refresh` skill for living web sources, source-retraction mode in wiki-delete with `<!--RETRACTED-SOURCE-->` marker lint, golden/defect fixture test suite (`scripts/test_lint_wiki.py`) wired into CI. **T01–T06 done (2026-07-19)**; lint + test runner (golden + 21 defects = 22/22) exit 0, `wiki-refresh`(Terraform)·retract(golden copy) dry-runs passed, whole-branch review clean. Depends on phase-6 |
| [tasks/phase-8-minimal-site/](tasks/phase-8-minimal-site/plan.md) | `plan.md` (design spec) + `implementation.md` (TDD steps with full code) + `prd.json` — 7 tasks (6 builder + 1 manual), 2026-07-20: replace both Quartz sites with a hand-rolled minimal search-first site in `web/` (build.py reusing lint_wiki.py parsing + style.css + Pagefind Korean full-text search). Keywords: minimal/refined/cold; features limited to wikilinks+backlinks, tags, dark mode. **2026-07-20 consolidation: adopted as the sole dashboard — the two Quartz directories (`site/`, `site-test/`) were deleted and `web/` renamed to `site/`** |
| [tasks/phase-9-aws-deploy/](tasks/phase-9-aws-deploy/plan.md) | `plan.md` — 2026-07-20 deployment plan: private S3 + OAC + CloudFront (Function rewrite for pretty URLs, 403→404 mapping), ACM us-east-1, Route53 domain, Terraform (`infra/`, S3 remote state), GitHub Actions OIDC deploy gated on `verify_site.py`; `implementation.md` — 12-task runbook (Task 0–11) with exact terminal commands, full HCL and workflow YAML, per-task verification, troubleshooting table. **Human-executed** — the agent planned and answers questions only; no `prd.json`. Both files deliberately Korean (user executes them personally). Supersedes the Cloudflare Pages target in `rules/site-code.md` §2 (doc update pending at close-out) |
| [tasks/phase-10-visitor-facing-site/](tasks/phase-10-visitor-facing-site/plan.md) | `plan.md` + `prd.json` — 22 tasks (21 builder + 1 manual), 2026-08-02: make the site readable for a first-time visitor. Part A (`site/`): inline citations collapsed into numbered chips, librarian-only sections filtered at render time, search in the header of every page, one-line summaries in listings, rewritten home with a three-step start path, breadcrumbs, `/tags/` index, description/OG/canonical metadata, `sitemap.xml` + `robots.txt`, extended build tests. Part B (`wiki/`): a no-background Korean lead paragraph on all 39 concept/entity/analysis pages. Part C: the new authoring and site rules. **T01–T21 done (2026-08-02)**; T22 (human visual pass) open |
| [tasks/phase-11-ci-deploy-gate/](tasks/phase-11-ci-deploy-gate/plan.md) | `plan.md` + `prd.json` — 3 tasks (2 builder + 1 verify), 2026-08-03: `verify-site.yml` and `deploy-site.yml` were two workflows both triggered by `push` to `main`, so they ran concurrently and nothing ordered them — lint lived only in the first, so a lint violation reddened CI while the site still deployed. Merged into one `site.yml` whose `deploy` job declares `needs: [verify, lint]`, dropped the triple site build inside deploy, kept `verify_site.py` there as a deliberate pre-upload audit of the exact `dist/`, and pinned all three jobs to the same actions and Python. **T01–T03 done (2026-08-03)**; first post-merge run green with `deploy` starting after both upstream jobs completed |
| [tasks/phase-12-wiki-identity-copy/](tasks/phase-12-wiki-identity-copy/plan.md) | `plan.md` + `prd.json` — 8 tasks (7 builder + 1 evaluator), 2026-08-03: the wiki still described itself as a YouTube-playlist digest and asserted Claude Code / harness engineering as its central subject, on `overview.md`, `index.md`, several concept/entity/analysis pages, the `SITE_DESCRIPTION` copy in `site/build.py`, and the §3 charter here. Both framings swept out; per-source `재생목록:`/`자막:` metadata and the `#N` citation labels deliberately preserved |

# Phase 20 — MOC hubs: index.md becomes a gateway

## Why

`docs/rules/wiki-content.md` §2 sets a scaling trigger: *when a single category in index.md
exceeds ~30 entries, introduce MOC (Map of Content) hub pages that cluster related pages, and
link the MOCs from index.md*. The 2026-09-22 ingest (virtualization / git / jev, 42 pages)
crossed it in all three categories at once — Sources 56, Entities 36, Concepts 34 — and the
flat catalog now mixes five unrelated subjects in one 131-line list. The operator asked for the
MOC option.

The cost of the flat list is not aesthetic. `index.md` is the **first file every skill reads**
(`wiki-content.md` §2, `wiki-query` step 1), so every question pays for 131 lines of unrelated
topics before it can locate anything.

## What changes

1. **`wiki/moc/` — five hub pages**, one per accumulated subject: AI coding agents, infrastructure
   and web, virtualization, git, jev. Each lists the pages of its subject by category with the
   one-line descriptions the index already carries, plus a short reading order.
2. **`wiki/index.md` becomes a gateway** — the five MOC links with a one-line description and a
   page count each, and nothing else. Per-page lines move into the MOCs.
3. **`scripts/lint_wiki.py`** — `check_index_coverage` accepts a page listed in **a MOC that
   `index.md` links**, not only a page listed in `index.md` itself. Without this the whole phase
   fails lint. Two related exclusions keep the other checks meaningful:
   - `build_inbound_map` ignores `moc/` pages as link sources, exactly as it already ignores
     `index.md` — otherwise every page has an inbound link from its hub and `check_orphans`
     stops detecting anything.
   - `check_orphans` skips `moc/` pages themselves (they are reached from the index, which is
     not counted as a source).
4. **`site/build.py`** — `moc` joins `SECTIONS` so the hub pages get a listing page, breadcrumb,
   home card and sitemap entry like any other section. The home "start path" copy stops
   promising a category list.
5. **Operating docs follow the code** — `wiki-content.md` §2 (the contract), `site-code.md` §2.4
   (the lint coupling), `CLAUDE.md` §1 (the tree), and the skills that write or delete pages.
6. **`.claude/skills/wiki-ingest/SKILL.md`** — this is the repeating work the operator asked to
   automate: step 4 now updates **the subject MOC** and touches `index.md` only when a subject is
   new (a new MOC). `wiki-delete` removes MOC lines; `wiki-lint` checks MOC coverage.

## Non-goals

- No new page types. MOC pages are `type: overview`, which already exists and carries no required
  headings — a hub is navigation, not prose.
- No sub-hubs. The AI-coding hub is the big one (~60 entries); it groups with H2s inside one page.
  Split it only when it crosses the same threshold on its own.
- No change to how pages are written. Only where they are *listed* changes.

## Verification

| Check | Command | Pass |
|---|---|---|
| Lint (coverage now MOC-aware) | `python3 scripts/lint_wiki.py` | exit 0, 색인 오류 0 |
| Lint regression suite | `python3 scripts/test_lint_wiki.py` | exit 0 — golden proves the MOC path lints clean, a new `defects/moc-not-linked-from-index` fixture proves an unlinked hub still fails |
| Site builds | `python3 site/build.py` | exit 0 |
| Build invariants | `python3 site/test_build_site.py` | exit 0 |
| Leak audit | `python3 scripts/verify_site.py` | exit 0 |
| Mermaid syntax | `node scripts/check_mermaid.mjs` | exit 0 (unchanged blocks) |

## Risks

- **Coverage hole.** If a page is listed in no MOC, lint must still fail. The new fixture pins
  this; the real check is the same code path as before, only its input set grew.
- **Stale hubs.** A hub that nobody updates on ingest is worse than a flat list. This is why the
  skill change (6) is part of the phase, not a follow-up.

## Review changes (2026-09-22, same day, after the operator saw it on a local server)

The operator reviewed the first cut and asked for four changes. All landed in the same PR.

1. **"주제 관문" → "카테고리", everywhere.** Readers did not parse "관문". The folder is now
   `wiki/categories/` (plural, like the other sections), the URL `/categories/`, the nav label
   "카테고리", the page title `<주제> — 카테고리`, and the lint constant `CATEGORY_PREFIX`. The
   term "MOC" survives only as a parenthetical in `wiki-content.md` §2 explaining where the idea
   comes from. Fixture dirs renamed to match.
2. **`wiki/index.md` is no longer published.** It stays on disk because `wiki-ingest`/`wiki-query`/
   lint read it as the gateway list, but `site/build.py` skips it, the header nav drops "색인", the
   home start path and "최근 갱신 →" point at `/categories/`, and `overview.md`'s example wikilink
   now targets a category page. `test_all_articles_built` and `test_pagefind_wiring` learned the
   exception.
3. **`## 여기서부터` → `## 처음이라면 이 순서로`** on every category page and in the §2 template.
4. **Listings grouped by category, with a sort toggle.** `/concepts/`, `/entities/`, `/sources/`,
   `/analysis/` and every `/tags/<tag>/` page now render one `<section class="group">` per category
   (heading links to the category page; order = `index.md` order), from `category_map()`, which
   parses the category pages' wikilinks — no `category:` frontmatter, the category page *is* the
   membership record. A `제목순 | 최근 갱신순` toggle sorts inside each group with ~20 lines of inline
   JS off `data-title`/`data-updated`, remembered in `localStorage` like the theme. Default is 제목순,
   so the no-JS render is unchanged. Home shows five category cards above the four type cards;
   `/categories/` is the same five cards. `/tags/` itself is untouched — tags cut across categories,
   grouping the tag index would destroy that. Category pages are excluded from the Pagefind body
   (link lists are search noise), the same treatment the index page had.

Verification after the review pass: lint 0 · fixture suite 35/35 · build 137 pages · build tests
all pass · leak audit pass.

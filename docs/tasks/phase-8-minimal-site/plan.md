# Phase 8 — Minimal Search-First Site (`web/`)

> Design spec agreed 2026-07-20 (brainstorming session). Replaces both Quartz sites
> (`site/`, `site-test/`) with a hand-rolled minimal static site. Implementation tasks
> will be decomposed into `prd.json` after spec review.

## 1. Why

The user rejected both existing Quartz sites. Named pain points:

1. **Unfriendly first screen** — a first-time visitor doesn't know what to do.
2. **Design/readability dissatisfaction** — typography, spacing, layout.
3. **Weak search** — FlexSearch handles Korean poorly; search UI below expectations.

Fixing all three inside Quartz means fighting the framework (phase-4/5 already tried).
Decision: build a new site from scratch. Design keywords: **minimal, refined, cold**
(미니멀, 세련됨, 차가움). Priorities: simplicity, readability, intuitiveness, usable by
a first-time visitor without instructions.

## 2. Approach (chosen: custom mini generator)

Considered: (A) custom static generator + Pagefind, (B) Eleventy + Pagefind, (C) Quartz
re-theme. Chose **A**: the required feature set is small (wikilinks, backlinks, tags,
dark mode), parsing code already exists in `scripts/lint_wiki.py`, and a framework adds
cost without covering the custom parts (wikilinks/backlinks) anyway. C is the path that
already failed twice.

## 3. Architecture

```
web/
├── build.py            # single static generator (~400 lines)
│                       #   reuses lint_wiki.py parsing: frontmatter, WIKILINK_RE,
│                       #   build_inbound_map (backlinks)
│                       #   markdown-it-py for md→HTML
│                       #   templates = Python f-strings — 3 templates: home / article / tag
│                       #   (catalog·overview·404 render through the article template)
├── style.css           # single hand-written stylesheet; the entire design lives here
└── dist/               # build output (gitignored)
```

- **Build order:** `python web/build.py` → `npx pagefind --site web/dist`.
- **Dependencies (2):** `markdown-it-py` (pip), `pagefind` (npx, build-time only).
- **Deploy:** Cloudflare Pages, same project model as before; only the build command changes.
- **raw/ boundary:** `scripts/verify_site.py` leak-audit logic applied to `web/dist`.
- `site/` and `site-test/` are deleted only after the new site passes human QA (separate
  confirmation gate).

## 4. Pages & routes

| Route | Page | Content |
|---|---|---|
| `/` | Home | Search-first: site name + large search box at upper third; below it 4 entry points (overview / concepts / sources / analysis, with page counts) + 5 most recently updated pages. Minimal scroll. |
| `/concepts/mcp/` etc. | Article | Mirrors `wiki/` paths. Body `max-width: 68ch`, centered. Thin header (site name + search). Footer of page: backlinks ("이 문서를 참조하는 문서") + tag chips. |
| `/tags/<tag>/` | Tag | All pages carrying the tag: title + one-line description. Korean tag slugs stay Korean (percent-encoded URLs). |
| `/index/` | Full catalog | `wiki/index.md` published as-is; linked from home as "전체 색인". `wiki/overview.md` → `/overview/`. |
| `/404.html` | 404 | Message + search box. |

## 5. Design language

Design read: Korean knowledge-base wiki, editorial-minimal, cold monochrome.
Dials: VARIANCE 4 / MOTION 2 / DENSITY 3.

- **Palette:** cold monochrome. Light = cool near-white (`#fafafa` family) + ink-black
  text; dark = zinc-950 family. **One accent: steel blue** (the "cold" carrier), used only
  for links and search focus. No pure `#000`/`#fff`. One palette, locked across all pages.
- **Typography:** **Pretendard** (variable) for Korean body/display; JetBrains Mono for
  code. Body 17px, `line-height: 1.75` (Korean readability). Hierarchy via weight, not
  size screaming.
- **Layout:** no cards. Separation via whitespace and 1px hairlines. Generous section
  spacing. No decorative dots, no eyebrow labels, no AI-tell patterns.
- **Dark mode:** `prefers-color-scheme` auto + manual toggle (localStorage). Both modes
  designed from the start; WCAG AA contrast in both.
- **Motion:** hover transitions ~0.15s only. No animations.

## 6. Search

- **Pagefind** post-build index: Korean full-text search over title + body, result
  excerpts with highlights.
- Same Pagefind UI on home (hero) and article header, themed via CSS variables to match
  the palette.
- Site JS = Pagefind bundle + a few lines for the dark-mode toggle. Nothing else.

## 7. Edge cases

- **Dangling wikilinks** render as muted plain text (no broken `<a>`); lint owns the fix.
- **Frontmatter `title`** used for `<title>` and list entries only; body h1 renders as
  written (no double titles).
- **Dates:** `updated` shown small and muted at the top of each article.

## 8. Verification (site-code.md order)

1. `python web/build.py` — all 67 wiki pages convert without error.
2. Internal link check (built into `build.py`) — every internal href in `dist/` resolves
   to a real file.
3. `verify_site.py` — raw/ leak audit against `web/dist`.
4. `web/test_build_site.py` — stdlib test: run build, assert invariants (page count,
   backlinks present on a known page, catalog page generated).
5. Human QA gate: visual check both modes + Korean search feel (agent cannot verify —
   marked manual, per site-code.md §1.4).

## 9. Out of scope

- Graph view, TOC (explicitly cut in brainstorming).
- Deleting `site/`/`site-test/` (separate gate after human QA).
- Any `wiki/` prose change (content mode; not this phase).

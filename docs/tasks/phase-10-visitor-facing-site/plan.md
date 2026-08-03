# Phase 10 — Visitor-Facing Site & Readability

> Agreed with the user 2026-08-02. Covers both code mode (`site/`) and a bounded
> content-mode pass over `wiki/`. Decomposed into `prd.json` beside this file.

## 1. Why

The wiki serves two purposes: accumulating knowledge, and **showing that knowledge to other
people**. The second is weak. Concretely, measured against the current repo:

**Site (`site/build.py` 256 lines, `site/style.css` 110 lines)**

- The home page is site name + search box + 6 entry chips + 5 recent pages. **Zero lines
  explaining what this wiki is about.** A first-time visitor has nothing to search for.
- The `#search` element exists only on the home and 404 pages (`build.py:170`, `build.py:181`).
  **There is no way to search while reading an article.**
- Section listings (`render_listing`, `build.py:132`) show title + date only — nothing to
  choose from.
- No breadcrumb, no `/tags/` index, no `<meta name="description">`, no OG tags, no
  `sitemap.xml`, no `robots.txt`. Shared links render no preview and search engines see nothing.

**Content (`wiki/`, 69 pages)**

- **416 inline citations**, 410 of the form `(→ [[sources/slug|#13 하네스의 비밀]])`.
  `concepts/harness-engineering.md` carries 49 of them in 95 lines — a wall of blue link text
  ending nearly every sentence. This is the single biggest readability problem, and it is
  fixable at render time with **zero edits to the prose**.
- **Librarian bookkeeping is published.** `## 기존 위키와의 연결` (all 28 source pages —
  "강화/모순/신규: created the HCL concept page") and the `raw: raw/xxx.md` bullet inside
  `## 출처 정보`. Necessary for the librarian, noise for a visitor.
- Concept / entity / analysis pages have **no lead paragraph for a reader without background** —
  they open straight into compressed bullets.

## 2. Non-negotiable constraint

**Nothing is deleted from `wiki/`.** Internal sections are hidden at *render* time only.
`기존 위키와의 연결` is what `wiki-query` and `wiki-lint` read; deleting it breaks the wiki.

## 3. Part A — Site (code mode)

All changes land in `site/build.py` and `site/style.css`. No new dependency, no framework
(`docs/rules/site-code.md` §2.2 holds).

1. **Citation chips.** Pre-process the body before `link_wikilinks()` (`build.py:76`):
   turn `(→ [[sources/slug|#13 라벨]]·[[sources/slug2|#14 라벨2]])` into compact muted
   superscript anchors (`<a class="cite" title="#13 …">13</a>`). Strip the `(→ … )` wrapper
   when the group contains only citations and `·` separators; keep the wrapper when prose
   follows (e.g. `(→ [[…]] 참조 — …)`). Leave the 6 non-`sources/` targets alone. Mask code
   fences with `lint_wiki.FENCE_RE` first — this pays off the ponytail debt noted at
   `build.py:79`.
2. **Hide internal sections.** Drop the whole `## 기존 위키와의 연결` block and any
   `- raw: …` bullet. Backlinks still come from `lint_wiki.build_inbound_map` over the
   *source* files, so the connection information survives as "이 문서를 참조하는 문서".
   `verify_site.py`'s `raw/` whitelist only sees fewer matches — strictly safer.
3. **Global search.** Add a compact search box to `.site-header` on every page; keep the large
   hero box on home/404 under a separate id. Results render as an absolutely-positioned drawer
   so they never push the article. Collapses to its own row under 640px.
4. **One-line summaries.** Derive a summary per page with no frontmatter schema change:
   source pages → first sentence of `## 한 줄 요약`; everything else → first sentence of the
   paragraph after the H1. Strip wikilink/emphasis markup, ellipsize past 100 chars. Render in
   section listings and the home "recent" list. Part B improves these automatically.
5. **Home rewrite.** One-line description of the wiki (site-owned copy, a constant in
   `build.py` — do not copy `wiki/overview.md` verbatim), then search, then a numbered
   **"처음이면 순서대로"** path: `/overview/` → `/analysis/ai-coding-evolution/` → `/index/`,
   then the existing category chips and recent list.
6. **Breadcrumb + `/tags/` index.** Breadcrumb from the page key using the `SECTIONS` labels
   (skipped for `index`/`overview`). A tag index sorted by page count, with the 1-page tags
   folded into a `<details>` (132 tags total).
7. **Share & indexing metadata.** `SITE_URL = "https://omotomo-llm-wiki.com"`;
   `<meta name="description">`, `og:title`/`og:description`/`og:url`/`og:type`,
   `twitter:card=summary`, `<link rel="canonical">`, `sitemap.xml` (with `updated` as
   `lastmod`), `robots.txt` allowing everything plus a `Sitemap:` line. **No `og:image`** —
   the satori font failure recorded in `site-code.md` §2.4 is not worth re-entering.
   No infra change: both new files fall outside the Pagefind hashed-name whitelist and land in
   the short-cache sync automatically.
8. **Tests.** Extend `site/test_build_site.py` (stdlib `assert` style, no framework).

## 4. Part B — Lead paragraphs (content mode, 39 pages)

`wiki/concepts/` (19) + `wiki/entities/` (17) + `wiki/analysis/` (3). Source pages are excluded —
they already carry `## 한 줄 요약`.

Add a **3–4 sentence lead paragraph assuming zero background** directly under the H1 of each
page. Existing body text is not touched. First sentence says what the thing is, in plain
Korean, expanding any jargon on the spot; the next sentences say why it matters / when it comes
up. **No citation chips inside the lead** — Part A step 4 lifts its first sentence into
listings, search results and OG descriptions, so it must read standalone. Bump `updated`
(`wiki-content.md` §4.3). Commit per category.

## 5. Part C — Rules

- `docs/rules/wiki-content.md`: lead-paragraph requirement in the §1 template; an explicit
  **public vs. librarian-only section** distinction; the citation format
  `(→ [[sources/slug|#N 라벨]])` documented as load-bearing — the site parses it, so a broken
  format renders raw.
- `docs/rules/site-code.md` §2.4: the render-time section filter and why the source must stay;
  the citation parser's deliberate coupling to the `wiki-content.md` convention (same shape as
  the existing `KNOWN_TAG_VARIANT_GROUPS` note).
- `docs/index.md`: register this phase directory.
- `docs/log.md`: one `site` line at Part A close-out, one content line at Part B close-out.

## 6. Out of scope

- A `summary` frontmatter field — lint + fixtures + 69 hand migrations for what extraction gives free.
- Table of contents — revisit only if long pages still fail after the lead paragraphs and citation cleanup.
- `og:image`.
- Rewriting the 28 source page bodies.
- Deleting internal sections from `wiki/`.

## 7. Verification

The standing gate from `docs/rules/site-code.md` §2.3, in order, per task:

| Check | Command | Pass |
|---|---|---|
| Wiki integrity | `python3 scripts/lint_wiki.py` | exit `0` |
| Lint fixtures | `python3 scripts/test_lint_wiki.py` | exit `0` |
| Site build (internal links) | `python3 site/build.py` | exit `0` |
| Build invariants | `python3 site/test_build_site.py` | exit `0` |
| `raw/` leak audit | `python3 scripts/verify_site.py` | exit `0` |
| Artifact ignored | `git check-ignore site/dist` | ignored |

**Human-eyes ACs** (§1.4 — agents must mark these unverified): whether the citation chips
actually read better, whether the lead paragraphs are genuinely easy, Korean line-breaking,
dark mode, mobile collapse.

**Post-deploy:** `sitemap.xml` and `robots.txt` return 200; an article URL pasted into
Slack/KakaoTalk shows a preview card; search still works (Pagefind cache rules, §2.4).

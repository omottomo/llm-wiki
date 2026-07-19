# Code-Mode Rules — Coding Discipline & Site Publishing

> Module of the repo's operating rules, split out of `CLAUDE.md`.
> **Read this before touching `site/`, `scripts/`, `.github/`, or root config.** It governs
> code-mode work: `/my-skills:orchestrate` runs, `/my-skills:create-prd-json`, the
> planner/builder/evaluator team, and any direct code edit. The common rules in `CLAUDE.md`
> (language rule, core principles, log.md, skill routing) always apply on top of this file.
> The orchestrate team reaches this file through the adapter at `.claude/orchestrate.md`.

---

## 1. Coding discipline

> **Scope:** these rules govern **code** — `site/`, `scripts/`, `.github/`, root config. They do **not** govern wiki prose; `docs/rules/wiki-content.md` does. Adapted from the Karpathy guidelines (multica-ai/andrej-karpathy-skills).
>
> **Tradeoff:** this biases toward caution over speed. For trivial edits, use judgment.

### 1.1 Think before coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 1.2 Simplicity first
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked. No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- Ask: "would a senior engineer call this overcomplicated?" If yes, simplify.

### 1.3 Surgical changes
**Touch only what you must. Clean up only your own mess.**
- Don't "improve" adjacent code, comments, or formatting. Don't refactor what isn't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports and variables that *your* changes made unused; leave pre-existing dead code alone.
- The test: every changed line traces directly to the task.

### 1.4 Goal-driven execution
**Define success criteria. Loop until verified.**
- Every task in `docs/tasks/<phase>/prd.json` has an Acceptance Criterion. That AC is your success criterion — do not redefine it.
- Turn vague subtasks into verifiable goals ("fix the bug" → "reproduce it with a command, then make that command pass").
- A task is done when its AC is *demonstrated*, not when the code "looks right".
- **When an AC needs human eyes** (visual polish, dark mode, how Korean search actually feels), say so explicitly and mark it unverified. Never claim it passed on your own judgment.

### 1.5 Readability
**Write code that reads clearly — this is about clarity, NOT adding layers. It never overrides §1.2.**
- Names reveal intent; no cryptic abbreviations.
- Small, single-responsibility functions — extract a well-named helper instead of a long block, but do not introduce new abstraction layers.
- Avoid duplication only where it already repeats; don't pre-factor for hypothetical reuse.
- Prefer early returns over deep nesting.
- Comments explain *why*, not *what*.

---

## 2. Site publishing (Quartz 5 → Cloudflare Pages)

The wiki is published as a public website via **Quartz 5**, vendored into `site/`, deployed on **Cloudflare Pages**. Phase plans and PRDs live under `docs/tasks/`.

### 2.1 The `raw/` boundary — non-negotiable

`raw/` holds full auto-generated transcripts of **other people's** YouTube videos. It must **never** be published to the web, and must **never** land in a public repo. Two protections, both required:

1. The GitHub repo stays **private**. (This is why Cloudflare Pages was chosen over GitHub Pages — the free GitHub Pages tier requires a public repo.)
2. The Quartz **content root is `wiki/` only** — `raw/`, `log.md`, `CLAUDE.md`, `docs/`, `.claude/`, `.obsidian/` all sit outside it and are structurally excluded.

**Every build that touches the site or the content root must be audited:** `python3 scripts/verify_site.py` exits `0` — its leak audit checks that no raw-derived page is rendered, no transcript content appears verbatim in the output, no absolute local path (`/Users/...`) leaks, and every literal `raw/` match is a bare source citation. (A naive `grep -ril "raw/" site/public/` always matches — see §2.4.) This is the Evaluator's standing check and the orchestrator's close-out gate. Never flip the repo to public.

### 2.2 Architecture invariants

- **Monorepo + symlink.** Quartz is vendored into `site/` (its `.git` removed, committed as regular files). Content is connected by a **relative** symlink `site/content → ../wiki`. Never replace it with a copy; never make it absolute — absolute paths break in CI.
- **Node 22+** (`npm >=10.9.2`). Quartz 5 will not install on Node 20. Cloudflare needs `NODE_VERSION=22`.
- **npm**, not pnpm or yarn.
- Quartz 5 config is **YAML** (`site/quartz.config.yaml`). After editing the `plugins:` block, re-run `npx quartz plugin install --from-config` and **commit `quartz.lock.json`**.
- `baseUrl` must match the Cloudflare Pages project name. If they drift, the sitemap and RSS break.
- Korean UI requires `locale: ko-KR` **and** a font with Korean glyphs (Noto Sans KR) — Quartz's default theme fonts have none.
- Vendoring means `npx quartz update` is unavailable. To upgrade: clone the new version into a temp directory and swap the code, preserving the config and the content symlink.

### 2.3 Verification (there is no unit-test suite — verify by running the real thing)

| Check | Command | Pass |
|---|---|---|
| Wiki link integrity, frontmatter, index, orphans | `python3 scripts/lint_wiki.py` | exit `0` |
| Site builds | `cd site && npx quartz build` | exit `0` |
| **`raw/` leak audit (amended — see §2.4)** | `python3 scripts/verify_site.py` | exit `0` |
| Content symlink is relative | `readlink site/content` | `../wiki` |
| Artifacts ignored | `git check-ignore site/node_modules site/public` | all ignored |

Never commit `site/node_modules/`, `site/public/`, `site/.quartz/`, `.env`, or `.claude/settings.local.json`.

### 2.4 Accumulated rules

*(When a phase uncovers a constraint the next session would otherwise rediscover the hard way, record it here. Only what would surprise someone who just cloned the repo; do not restate what the code already says.)*

- **The literal `raw/` grep is a false-positive trap** (2026-07-12). `grep -ril "raw/" site/public/` always matches, because every source page's 출처 정보 section legitimately cites `raw: raw/<slug>.md`. The binding leak audit is `scripts/verify_site.py`: no rendered raw-derived path, no verbatim transcript content in output, no `/Users/` absolute path, and `raw/` string matches whitelisted to bare citations.
- **Absolute local paths leak the operator's identity** (2026-07-12). Frontmatter like `raw: /Users/<name>/...` ships the username and directory layout into public HTML *and* the search index `static/contentIndex.json`. Five pre-existing source pages had this; fixed in content mode. Authoring rule now in `docs/rules/wiki-content.md`; regression check in `verify_site.py`.
- **`note-properties` is the frontmatter parser, not just a UI panel** (2026-07-12). Setting `enabled: false` stops frontmatter from being parsed at all — YAML renders as body text, page titles disappear, the explorer falls back to slugs. To hide the Properties panel, keep the plugin enabled and set `hidePropertiesView: true`.
- **Korean typography lives in `site/quartz/styles/custom.scss`** (2026-07-12): `word-break: keep-all` (어절 단위 줄바꿈) + `line-height: 1.75` for article text. When re-vendoring/upgrading Quartz, preserve this file along with the config and content symlink (§2.2).
- **Local URLs are case-sensitive in production** (2026-07-12). Quartz slugifies everything to lowercase (`youtube-DCsv0rKKrN4` → `youtube-dcsv0rkkrn4`); mixed-case URLs only work locally because macOS's filesystem is case-insensitive. All emitted links are lowercase, so this only bites hand-typed URLs — but a local graph view that looks empty on a manually-entered mixed-case URL is this, not a bug.
- **Parallel builders share one git index — commit with `--only`** (2026-07-13). `git add <path> && git commit` commits the *whole index* at commit time, so a file staged by another builder between your `add` and your `commit` rides along silently (this happened: T06's staged deletion shipped inside T11's commit). Builders working concurrently in the shared worktree must use `git commit --only <exact-path> -m "..."`, which commits just the named path regardless of what else is staged.
- **A `completed` task on the board is NOT evidence of verification** (2026-07-13). The Task board has no `review` state — `TaskUpdate` accepts only `pending | in_progress | completed | deleted`, and the tool's own built-in guidance tells every agent to mark its task resolved "when you finish." Builders obey that the moment they finish *implementing*, so `completed` collapses "code written" and "Evaluator verified" into one status. Consequence for the orchestrator: **close the phase off the Evaluator's explicit PASS message per task, never off board state** — and have the Evaluator verify anything that reads `completed` without a PASS it remembers sending. Same root cause makes `teammate-idle-guard.sh` nag any Builder that idles while correctly waiting on a review; that nagging is a false positive, not abandoned work.
- **CI now runs `lint_wiki.py`, and the corpus is expected to stay at zero** (2026-07-17, supersedes the 2026-07-13 rule that CI deliberately excluded it). Lint used to exit `1` on the whole corpus — ~58 real content defects the phase-3 checks surfaced — so it was kept out of CI to avoid a permanently-red `main`, with the standing condition "add it only after a lint run is green." That debt was cleared in a content-mode pass and lint exits `0`, so the gate is in (its own job — lint needs no Node, npm or build, so folding it into the site matrix would make it wait on the build and then run twice for the same files). **Consequence: a lint violation now breaks `main`.** Run `python3 scripts/lint_wiki.py` before pushing wiki prose; it is no longer advisory.
- **The CI gate fires on push to `main`, not on pull requests** (2026-07-13). A leak or a broken build is therefore caught *after* the merge, not before it. Treat a green PR as unverified: run the §2.3 matrix locally before merging.
- **`KNOWN_TAG_VARIANT_GROUPS` in `lint_wiki.py` duplicates the merge table in `docs/rules/wiki-content.md` §4.1 — on purpose** (2026-07-13). The dependency runs *docs ← lint*, not the reverse: lint's tag-hygiene report is what tells a human which variant pair to curate into the table. Having lint parse that prose table back would invert the direction and add a silent-failure mode (a reformatted row parses wrong with no error) to save five lines. The two can drift — when you edit one, edit the other.

- **The vendored `.gitignore` self-ignores, so artifact protection must live in the tracked root `.gitignore`** (2026-07-13). Quartz ships a `.gitignore` whose second line is `.gitignore` — it ignores itself. `git ls-files site/.gitignore` returns nothing: it is **untracked and absent from a fresh clone**. Consequence: `git check-ignore site/public` passing on your machine proves nothing, because the deeper vendored file is what matched. Verify with a real `git clone --local . <tmp>` and confirm the matching source is the **root** `.gitignore`. Both `site/` and `site-test/` now have root-level entries (no trailing slashes, so `.quartz` matches before the directory exists) — **keep it that way when vendoring any further Quartz copy**, because the vendored file will look like it covers you and will not.

- **This gate was red from its first run and stayed red for two days** (2026-07-17). The hole above is how: `site/` was left unfixed as a "live follow-up" while CI already ran `verify_site.py`, so the audit reported `site/node_modules`, `site/public` and `site/.quartz` as un-ignored on every push to `main`. **The workflow has never once been green** — it failed on the phase-3 merge that introduced it and on the phase-4 merge after it, and nobody noticed, because nothing downstream reads its status. Two lessons. (a) A gate nobody watches is not a gate; when you add one, watch its *first* run go green (`gh run list`) or you have shipped a decoration. (b) A red gate is worse than no gate — it trains everyone to ignore it, so the *next* failure (a real `raw/` leak) reads as more of the same noise. Never leave a check red as a follow-up: fix it or don't add it yet.

- **A Quartz plugin's `options:` block is not validated — read the type definition** (2026-07-13). `quartz-plugins.schema.json` declares `options` with `additionalProperties: true`, so **any** options block passes YAML validation. But `tag-list` is a no-arg factory (`declare const _default: () => QuartzComponent`) and silently discards whatever you pass; `recent-notes` genuinely takes options (`RecentNotesOptions { title?, limit, linkToMore, showTags }`). Both look identical in the config, and the build goes green either way while doing nothing. The only way to tell them apart is to read `.quartz/plugins/<name>/dist/index.d.ts`. Do that before writing an `options:` block.

- **`recent-notes` renders its tags with the same classes as `tag-list`** (2026-07-13). Both emit `<ul class="tags">` and `<a class="internal tag-link">`. So grepping built HTML for `tag-link` to prove "tag chips render" is a **false PASS** — it succeeds even with `tag-list` disabled. Check structurally instead: a `ul.tags` that is *outside* the `.recent-ul` / `.recent-li` subtree. (Relying on `showTags: false` to keep recent-notes' tags out of the way is not a check; it just borrows another task's setting.)

- **Absence checks on built output must be scoped to `public/**/*.html`** (2026-07-13). Component class names (`explorer-content`, `explorer-ul`, `explorer-toggle`, `breadcrumb-element`) survive in the bundled CSS/JS **even when the plugin is disabled** — the plugin's stylesheet is still part of the build. Grepping all of `public/` for them yields a **false FAIL**. The AC asks whether *rendered pages* carry the markup, so grep the HTML only.

- **A verification script that swallows errors or misreads an exit code is itself a false verdict generator** (2026-07-13). Two live cases from this phase, both caught only because a result contradicted another signal: (a) an HTML structure parser hit a `TypeError` on a valueless `class` attribute, its `try/except` swallowed the error and aborted the parse, and it then reported **0 matches for every check** — a false FAIL that read exactly like a broken site; (b) `${PIPESTATUS[0]}` is empty in zsh (arrays are 1-indexed), so `cmd | tail` followed by `$?` reports **`tail`'s** exit code, not the command's — a "build exit 0" that measured nothing. Treat a checker's `0` as "did not see", not "not present": cross-check it against an independent signal (a grep against a parser, a bare run against a piped one) before believing it. Never write a bare `except:` in a check.

- **`baseUrl` names a project that may not exist yet — and the name may not be yours to take** (2026-07-17). §2.2 says `baseUrl` must match the Cloudflare Pages project name, which invites reading it as a description of something live. It is not: **no Pages project has ever been created for this repo.** `ai-llm-wiki.pages.dev` was `NXDOMAIN` — phase-1 T09/T10, phase-3 T08 and phase-4 T12 (all the Cloudflare steps) are still open, so every `baseUrl` here is an *intended* name, not a deployed one. Two consequences. (a) Do not reason about a rename "breaking the live site" or "killing existing links" — there is no live site; the §2.2 constraint only binds at the moment the project is actually created. (b) `*.pages.dev` subdomains are **globally unique across all Cloudflare accounts**, so a name free in your dashboard can still be taken: `llm-wiki.pages.dev` is held by an unrelated org (`almaajo`, behind Cloudflare Access) and is therefore unusable, which is why the repo is `llm-wiki` while the deploy target is `omottomo-llm-wiki`. **Repo name and Pages project name are independent — do not assume they should match.** Before writing any `baseUrl`, check the name is free (`host <name>.pages.dev` → `NXDOMAIN`), and check a known-taken name in the same run to prove the lookup actually resolves — an `NXDOMAIN` from a typo'd or offline query looks identical to a free name.

- **A test site is a second content root, not a second `content` symlink** (2026-07-13). `site/content` is a symlink → `../wiki`. `site-test/content` is a **real directory** holding relative symlinks into `../../wiki/` (plus a site-owned `index.md` that is a regular file). Two consequences: the symlinks must land in git as mode `120000` — a `100644` copy silently forks the wiki and no build or screenshot will reveal it — and `verify_site.py`'s content-root symlink check therefore **skips** (with an explicit `SKIP:` line) for any directory other than the default `site`. An audit of directory X must never assert anything about directory Y.

- **The `og-image` emitter fetches `theme.typography` fonts from Google Fonts at *build* time, so those names must stay Google-resolvable even when the displayed font is something else** (2026-07-19). The 2026-07-19 redesign switched the site font to Pretendard (not on Google Fonts). Setting `theme.typography.header/body: Pretendard Variable` made `npx quartz build` fail (exit 1): the `CustomOgImages` plugin → satori `getSatoriFonts()` → `fetchTtf()` hits Google Fonts and got `400 Bad Request` for the unknown family, ending in *"No fonts are loaded. At least one font is required to calculate the layout."* `fontOrigin: local` does **not** prevent this — og-image fetches server-side regardless of origin. Fix: keep `theme.typography` on a Google-hosted Korean font (Noto Sans KR) purely for the build-time share-card render, and drive the *displayed* font from `custom.scss`, which `componentResources.ts` concatenates **unlayered** after the `@layer quartz-base { … }` block, so its `:root { --bodyFont/--headerFont/--codeFont }` overrides both the core theme and the `fonts` plugin. Two more load-bearing facts for a non-Google webfont: (a) use a `@font-face` block, **not** `@import` — custom.scss is not at the top of the final stylesheet, so a CSS `@import` is dropped by the browser; (b) jsDelivr's `/gh/orioncactus/pretendard@…` raw path failed to load in-browser here, while the `/npm/` path worked — Pretendard loads from `https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/variable/woff2/PretendardVariable.woff2` (one variable file covers every weight) and IBM Plex Mono from `@fontsource/ibm-plex-mono`. This is a runtime CDN dependency; to eliminate it, self-host the woff2 under `site/quartz/static/fonts/` and point `@font-face` at `/static/fonts/…` (the sandbox blocked downloading the files during this pass).

- **Lint rules ARE the schema — a schema change updates lint + fixtures, never a one-off migration script** (2026-07-19, phase-7). When you add or change a required frontmatter field (`credibility`, `volatility`, …) or any structural rule, the change lands in three coupled places, not one: the rule doc (`docs/rules/wiki-content.md` §1), the enforcing check in `scripts/lint_wiki.py`, and the fixture suite under `tests/fixtures/` (`golden-wiki/` must still lint clean; `defects/<check>/` gains one red variant for the new violation, each carrying an `expect.txt` substring). `scripts/test_lint_wiki.py` — a stdlib `assert` runner, no framework — then runs golden (expect exit 0) and every defect (expect exit 1 + its substring) and is wired into the CI `lint:` job **after** `lint_wiki.py`; a future refactor that silently disables a check turns that defect fixture green and fails the runner, so the check can't rot unnoticed. `lint_wiki.py --root <dir>` (added phase-7, guarded so the default path stays byte-identical) is what lets the runner point lint at a fixture tree. Consequences: (a) migrate the corpus **by hand** for a schema change — frontmatter-only, no `updated` bump for a metadata field per `wiki-content.md` §4.3 — and let lint verify, rather than writing throwaway migration code; (b) run `python3 scripts/test_lint_wiki.py` before pushing, same standing as `lint_wiki.py`; (c) adding a new lint violation without a matching defect fixture is an incomplete change — the "every distinct `add()` has a red fixture" invariant is the guard's whole value.

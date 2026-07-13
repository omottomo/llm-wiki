# Code-Mode Rules — Coding Discipline & Site Publishing

> Module of the repo's operating rules, split out of `CLAUDE.md`.
> **Read this before touching `site/`, `scripts/`, `.github/`, or root config.** It governs
> code-mode work: `/orchestrate` runs, `create-prd-json`, the planner/builder/evaluator team,
> and any direct code edit. The common rules in `CLAUDE.md` (language rule, core principles,
> log.md, skill routing) always apply on top of this file.

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
- **CI deliberately does not run `lint_wiki.py`** (2026-07-13). `.github/workflows/verify-site.yml` runs the Quartz build and `scripts/verify_site.py` (the `raw/` boundary audit) and nothing else. `lint_wiki.py` exits `1` on the current corpus **by design** — the phase-3 checks surface ~58 real content defects that only the librarian can fix in content mode. Adding lint to CI before that content debt is cleared turns `main` permanently red. Add it only after a lint run is green.
- **The CI gate fires on push to `main`, not on pull requests** (2026-07-13). A leak or a broken build is therefore caught *after* the merge, not before it. Treat a green PR as unverified: run the §2.3 matrix locally before merging.
- **`KNOWN_TAG_VARIANT_GROUPS` in `lint_wiki.py` duplicates the merge table in `docs/rules/wiki-content.md` §4.1 — on purpose** (2026-07-13). The dependency runs *docs ← lint*, not the reverse: lint's tag-hygiene report is what tells a human which variant pair to curate into the table. Having lint parse that prose table back would invert the direction and add a silent-failure mode (a reformatted row parses wrong with no error) to save five lines. The two can drift — when you edit one, edit the other.

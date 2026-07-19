# Orchestrate Adapter — llm-wiki

Project-specific rules for the `my-skills` plugin's orchestrate workflow (planner / builder / evaluator). Read together with `CLAUDE.md` and `docs/rules/site-code.md`.

## Protected paths

- **`raw/` — IMMUTABLE.** Third-party YouTube transcripts (copyright risk). Never modified, never published, must never reach the built site. Keeping the repo private and a `wiki/`-only content root are the two protections; `python3 scripts/verify_site.py` is what proves they held. **This constraint outranks every task in any PRD.**
- **`wiki/`** — owned by the librarian workflow (`wiki-ingest` / `wiki-query` / `wiki-lint` / `wiki-delete`). Read-only for this team: you may change how it *renders*, never its prose. A PRD task scoped here is a PRD bug — escalate to Planner.

## Surfaces

- `site/` — Quartz 5 static-site generator (vendored)
- `scripts/` — Python helpers (`lint_wiki.py`, `verify_site.py`)
- `.github/` — CI
- Root config files (`.gitignore`, etc.)

A request that would change `wiki/` prose is content mode — route it to the `wiki-*` skills instead of orchestrating (CLAUDE.md §3).

## Verification gate

Run in order (full matrix + rationale: `docs/rules/site-code.md` §2.3):

1. `cd site && npx quartz build` — exit `0`
2. `python3 scripts/verify_site.py` — exit `0`. The `raw/` leak audit; mandatory on every run that touched the build or the content root, even if no task mentioned it. **Never substitute a naive `grep -ril "raw/" site/public/`** — every source page's citation frontmatter legitimately contains `raw: raw/<slug>.md`, so that grep always matches and can never pass (§2.4).
3. `readlink site/content` — prints `../wiki`
4. `git check-ignore site/node_modules site/public` — all ignored. The matching source must be the **root** `.gitignore`; the vendored `site/.gitignore` is untracked (§2.4).
5. `python3 scripts/lint_wiki.py` — **informational only.** It currently exits `1` by design on known content debt (§2.4). Report the count; do not block close-out on it.

## Logging convention

At close-out append **one** line to `log.md` (append-only, newest at the bottom), entry text in Korean, one line per phase — not per task:

```
## [YYYY-MM-DD] site | <phase slug> — <what shipped>
```

## Durable rules

`docs/rules/site-code.md` → §2.4 "Accumulated rules". Only constraints the next session would otherwise rediscover the hard way (a Quartz config key that silently no-ops, a plugin that breaks Korean rendering, a CI setting that must match `baseUrl`). Never restate what the code already says.

## Report language

**Korean (한국어)** for all user-facing status updates and PR bodies. PR titles in English (Angular convention). PRD free-text fields (`goal` / `title` / `acceptance` / slug) in English — the PRD is an agent-facing operating file.

## Extra rules

- **Read `docs/rules/site-code.md` before dispatching or working** — same authority as CLAUDE.md: coding discipline §1, architecture invariants §2.2, verification §2.3, accumulated rules §2.4.
- **npm**, not pnpm/yarn. Node 22+ (Quartz 5 requires `>=22`, `npm >=10.9.2`) — if `node -v` shows v20, say so and stop rather than fighting install errors.
- Quartz 5 config is **YAML** (`site/quartz.config.yaml`). After changing the `plugins:` block, run `npx quartz plugin install --from-config` and **commit the updated `quartz.lock.json`**. Plugin `options:` blocks are **not** schema-validated — read `.quartz/plugins/<name>/dist/index.d.ts` before writing one (§2.4).
- `site/content` is a **relative** symlink → `../wiki`. Never replace it with a copy, never make it absolute — absolute paths break in CI.
- **Never commit:** `site/node_modules/`, `site/public/`, `site/.quartz/`, `.env`, `*.key`, `*.pem`, `.claude/settings.local.json`, anything under `raw/`.
- Parallel Builders share one git index — commit with `git commit --only <path>` (§2.4).
- Python scripts: **stdlib only** unless a dependency is justified in the PRD. Keep them runnable as `python3 scripts/<name>.py` from the repo root.
- Any user-visible string that lands in the site UI: **Korean**.
- **Evaluator-owned check script: `scripts/verify_site.py`.** Durable re-runnable checks go there — stdlib only, exit `0` clean / `1` on failure, same shape as `lint_wiki.py`. One-off checks stay ad-hoc Bash.
- Manual-AC examples for this project: visual polish, dark mode, Korean search feel, mobile layout.

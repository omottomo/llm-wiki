---
name: wiki-refresh
description: "Re-check living web sources (hot/warm volatility) for drift and update the wiki only after the human confirms. Use when the user says \"최신화 / 갱신 / refresh\" about the wiki or a specific source, or asks whether a hot/warm source has changed since ingest. This is a human-gated operation - re-fetches the source URL, diffs it against the stored raw/ capture, classifies changes as cosmetic/additive/contradictory, and presents the assessment for confirmation BEFORE editing any wiki page. raw/ is never edited; a materially changed source is saved as a new dated raw capture. Contradictions are kept-both-and-flagged, never overwritten."
---

# Wiki Refresh

> **CLAUDE.md** — Read this file first and follow its rules for all wiki content.
> **Rules module: `docs/rules/wiki-content.md`** — Read this too; it holds the page authoring / index / domain rules, including §5 (refresh workflow) which this skill implements.

Re-check `hot`/`warm` sources for drift, and update the wiki **only after the human signs off**. `cold` sources (fixed snapshots) are out of scope — there is nothing living to re-check.

> **All wiki content you write must be in Korean. Confirm and report to the user in Korean.** See CLAUDE.md LANGUAGE RULE.

> **HARD RULE: never edit `raw/`.** It is immutable (CLAUDE.md core principle 1). A materially changed source becomes a **new** raw file, never an edit to the existing one.

## Procedure

### 1. Select targets
If the user names a specific source, target just that one. Otherwise scan `wiki/sources/*.md` frontmatter for `volatility: hot` or `volatility: warm` (skip `cold` — never re-check those). List candidates with their `updated` date so the user sees how stale each is.

### 2. Re-fetch
For each targeted source, read its `## 출처 정보` section in `wiki/sources/<slug>.md` for the `URL:` line, then fetch it (same technique as `wiki-ingest` step 0: `browser_navigate` → `browser_console` innerText for articles/docs; `youtube-transcript-api` for video). Hold the fetched text in memory — do not save it until the user confirms at step 5 (step 6 applies confirmed changes).

### 3. Diff against the stored capture
Compare the fresh fetch against the most recent capture: `raw/<slug>.md`, or if an earlier refresh already created a dated capture (step 6), the newest `raw/<slug>-<YYYY-MM-DD>.md`. Find the newest capture from the source page's `## 최신화 이력` (step 7) rather than re-deriving it.

### 4. Classify each change
- **Cosmetic** — wording/formatting only, no factual delta.
- **Additive** — new facts appended, nothing existing contradicted.
- **Contradictory** — a fresh claim conflicts with the current wiki content or prior capture.

### 5. Present for human confirmation (mandatory gate — never skip, never edit first)
Show the user, per source, the URL, the classification, and the specific diffed lines/facts — in Korean. Ask explicitly whether to proceed. **Do not touch any wiki page, and do not save any new raw file, until the user confirms.** This mirrors `wiki-delete`'s confirm-before-mutate discipline.

### 6. Apply confirmed changes
- **Cosmetic-only**: no new raw capture, no wiki edit. Still record the check (step 7).
- **Additive / Contradictory**: save the fresh fetch as a **new** raw file — never overwrite `raw/<slug>.md`. Naming convention: `raw/<slug>-<YYYY-MM-DD>.md` (original slug + refresh date, ISO). Then update the wiki:
  - **Additive** → integrate like `wiki-ingest` step 3 (강화/신규): add supporting facts, create stubs for new proper nouns, cite the new raw slug.
  - **Contradictory** → keep both the old and new claim, flag the contradiction explicitly on the affected page(s) — never silently overwrite (CLAUDE.md core principle 4).

### 7. Record refresh history on the source page
On `wiki/sources/<slug>.md`, regardless of classification, append one line to a `## 최신화 이력` section (create it after `## 출처 정보` if it doesn't exist yet): date, classification, and the new raw slug if one was created. If a new capture was created, also append its slug to the frontmatter `sources:` list and bump `updated` — a material capture is real content, not metadata (`docs/rules/wiki-content.md` §4.3's metadata-only exemption does not apply here).

### 8. Update index and log
- Update `wiki/index.md` if new pages were created.
- Append one line to `log.md`: `## [date] refresh | 소스 요지 — 변경 유형, 페이지 N개 갱신` (or "변경 없음" if every checked source was cosmetic-only/unchanged).

### 9. Commit and report
- Commit: `git add -A && git commit -m "refresh: <slug> — <요지>"` — one commit per refresh pass.
- Tell the user (in Korean) what was checked, what changed, and what was left untouched.

## Notes
- Never edit `raw/`, including the original `raw/<slug>.md`, even for a cosmetic-only correction.
- Never skip the confirmation gate in step 5, even when refreshing a single source.
- Never re-check `cold` sources — they are frozen by design; if one turns out to actually be living, that's a `volatility` correction on the source page, not a refresh.
- If a fetch fails (dead URL, page restructured), report it and ask the user how to proceed rather than guessing.

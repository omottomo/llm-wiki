---
name: wiki-ingest
description: "Ingest a new source document (article, paper, note, image, data) into the wiki. Use whenever the user drops a source into raw/ and says \"흡수해 / 정리해 / 위키에 넣어 / ingest / 이거 읽고 반영해\", or sends a message starting with \"wiki-ingest <URL>\" (no leading slash — e.g. \"wiki-ingest https://example.com/123\"). For URL commands, fetch the page, save to raw/ as .md, then process as a normal ingest. Use this in any situation where you must not merely summarize a source but also update existing wiki pages and maintain cross-links. NOTE: in Slack, do NOT use a leading slash — Slack intercepts /commands as platform slash commands before they reach Hermes."
---

# Wiki Ingest

> **CLAUDE.md** — Read this file first and follow its rules for all wiki content.
> **Rules module: `docs/rules/wiki-content.md`** — Read this too; it holds the page authoring / index / domain rules for all wiki content.

Read a new source → extract → **integrate it into the existing wiki**.
This is not a plain summary. The point is to **weave** the new information into what already exists so the whole wiki gets one step richer. A single source typically touches 10–15 pages — but touching a page means grepping to the relevant slice and editing it, not reading the page end to end.

> **All wiki content you write must be in Korean.** See CLAUDE.md LANGUAGE RULE.

## Procedure

### 0. Detect input type
- If the user sends a message starting with "wiki-ingest <URL>" (no leading slash):
  1. **Detect platform**: YouTube video URL → use `youtube-transcript-api` (see YouTube handling note below). All other URLs → `browser_navigate` → `browser_console` with `document.body.innerText`.
  2. Derive a slug from the URL: `tistory-1709`, `arxiv-2401-00001`, `devto-how-to-xxx`, `youtube-wr4nCMUy1dk`
  3. Save content to `raw/<slug>.md` — **this becomes the immutable source**
  4. **Bare URL = "그냥 알아서 넣어"**: If the user sends only `wiki-ingest <URL>` with no further instructions, proceed directly to step 4 (write) without surfacing key points — the user explicitly wants full automation.
  5. Proceed with step 1 treating `raw/<slug>.md` as the source file
- If the user puts a file in `raw/` and asks to ingest → skip to step 1

> For non-YouTube URLs, see `references/content-extraction-techniques.md` for the reliable `browser_navigate` → `browser_console` (innerText) sequence that avoids snapshot truncation, plus which extraction method to pick per page type.

### YouTube handling (important — do not use browser for video pages)
Video pages (youtube.com, youtu.be) have no accessible text in the DOM. **Never** try to extract content via `browser_snapshot`/`browser_console` on a YouTube video URL — the player is opaque and interactive elements yield no transcript.

**Use `youtube-transcript-api`:**
```bash
python3 -m youtube_transcript_api <video_id> --languages ko 2>/dev/null
# e.g. video_id = wr4nCMUy1dk from https://youtu.be/wr4nCMUy1dk
# --languages en for English. Returns: [{"start": 0.033, "duration": 2.669, "text": "..."}, ...]
# One-time install: python3 -m pip install youtube-transcript-api
```

> **Why not yt-dlp?** `yt-dlp --write-auto-sub` fails with `Sign in to confirm you're not a bot` on public videos. `youtube-transcript-api` works without auth.
>
> **Video ID extraction:** The video ID is the 11-character string between `youtu.be/` (or after `v=`) and any `?`. For `https://youtu.be/HDjiNGvaurw?si=...`, the ID is `HDjiNGvaurw`.
>
> **Fallback behavior:** If `--languages ko` fails with `No transcripts were found for any of the requested language codes`, call again with `--languages en`. There is NO automatic fallback — you must retry explicitly.
>
> **Output format:** Returns a JSON list of segment objects `{"start": float, "duration": float, "text": str}`. Join `text` fields with newlines (in time order) to produce the raw transcript body.
>
> See `references/youtube-transcript-handling.md` for segment format, joining strategy, slug conventions, channel attribution pitfalls, and what to capture in raw/.

Join segment texts with newlines (in time order) to produce a plain-text body before saving to `raw/<slug>.md`. Use slug format `youtube-<video_id>`.

### 1. Understand the source
- Read the target file in `raw/` in full (if markdown with inline images, read text first then open referenced images from `raw/assets/` separately).
- Capture source metadata: author, date, URL, raw path.
- Judge `credibility` (high|medium|low) per the rubric in `docs/rules/wiki-content.md` §1 — record it in the source page frontmatter (step 4.1).

### 2. Surface the key points with the user (optional but recommended)
- Briefly tell the user 3–5 key takeaways and lightly agree on what to emphasize. Communicate in Korean.
- If the user says "그냥 알아서 넣어," proceed directly.

### 3. Reconcile with the existing wiki (most important)
Read `wiki/index.md` first to find pages related to this source. For each candidate page, locate the section you need with a `grep` for the claim, heading, or existing `[[...]]` link, and read only that slice plus enough surrounding context to edit it correctly — don't open the whole page. Reserve whole-page reads for pages that genuinely need restructuring (e.g. splitting a section, reorganizing headings). For each key claim, decide:
- **강화 (supports)**: Does it back an existing claim? → add it as supporting evidence on that page.
- **모순 (contradicts)**: Does it conflict with an existing claim? → keep both and flag the contradiction explicitly (never delete).
- **신규 (new)**: Is it a person/concept/topic appearing for the first time? → create a new page (or stub).

### 4. Write (follow the page rules in docs/rules/wiki-content.md)
Do these in order:
1. Write the source summary page at `wiki/sources/<slug>.md` (use `templates/source-page.md` in this skill — the canonical form of the template in `docs/rules/wiki-content.md` — **in Korean**).
2. Update relevant `entities/`·`concepts/` pages — add new facts, connect with `[[...|한글 별칭]]` wikilinks (every body link carries a Korean alias; cite sources as `(→ [[sources/<slug>|label]])`, multiple joined with `·` — format rules in `docs/rules/wiki-content.md` §1), flag contradictions.
   Every page you create or restructure follows its own template in this skill's `templates/`: `concept-page.md`, `entity-page.md`, `analysis-page.md` (required headings and the plain-writing / voice rules: `docs/rules/wiki-content.md` §1.1–§1.3). **No lead paragraph** — a page opens on its first `## ` heading, and its first summary bullet is what the site extracts, so that bullet carries no citation and no wikilink.
3. For every newly mentioned proper noun/concept, create at least a stub so no orphan links remain — a stub still uses its template.
4. If the source shifts the big picture, update `wiki/overview.md`.
5. Reflect new/changed pages in `wiki/index.md`.
6. **Run `python3 scripts/lint_wiki.py` before committing.** It exits non-zero on a missing required heading or a
   leftover lead paragraph on any page you touched, and prints readability warnings (over-long sentence, H2 over
   1,200 chars) that do not affect the exit code but are worth fixing while the page is still open.
7. Append one line to `docs/log.md`: `## [date] ingest | 자료 제목 — sources/xxx + concepts/yyy + concepts/zzz 갱신`
8. Commit: `git add -A && git commit -m "ingest: <slug> — <자료 제목>"` — the wiki is git-backed; one commit per ingest keeps the audit trail.

> **Branch: `wiki-ingest`, always.** Never name a branch after the source (`ingest/youtube-<id>` is banned).
> Start from the latest default branch (`git checkout -B wiki-ingest origin/main`); if a `wiki-ingest` PR is
> already open, add this ingest's commit to that same branch and let the PR grow instead of opening a second
> one. `main` is protected, so the ingest lands through a PR. *Why:* every ingest touches `wiki/index.md` and
> `docs/log.md`, so per-source branches stack on each other and conflict the moment `main` moves — PRs #3 and
> #4 had to be collapsed into #5 for exactly this reason (2026-08-09).

> Example: `## [2026-06-05] ingest | 이영희 '이직 플랜 & 경력 기술서 전략' — sources/youtube-aOVxvjLOcQE + concepts/이직플랜 + concepts/면접경험데이터 생성, concepts/경력기술서 + overview + index 갱신`
> The slug-rich format (vs generic "N개 갱신") makes future `session_search` much more productive.

### 5. Commit both repos
`raw/` is a nested **private** repo — the parent (public) repo ignores it, so one commit is not
enough. See `docs/rules/wiki-content.md` §3 for the why.
```bash
git -C raw add . && git -C raw commit -m "..." && git -C raw push
python3 scripts/lint_wiki.py --update-manifest
```
Then commit `wiki/` and `docs/raw-manifest.txt` in the parent repo as usual.

### 6. Report
Briefly tell the user (in Korean) what you created/changed (page list) and especially **any contradictions found or new connections formed.**

## Notes
- Never modify `raw/`.
- Never fabricate facts without a source. If uncertain, say so.
- If asked to ingest several sources at once, repeat the procedure per source, but consolidate shared pages once at the end.
- If the source references another source worth reading later (but not now), add it to `docs/backlog.md` — the ingest backlog — rather than ingesting it inline. `docs/backlog.md` is a candidate queue, never citable as factual evidence.

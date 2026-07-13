# Browser & Video Content Extraction for Wiki Ingest

## YouTube Video Ingestion

**Do not use browser tools on YouTube video URLs.** The embedded player is opaque — `browser_snapshot`/`browser_console` on a YouTube video page yields no useful transcript content.

### Extraction: youtube-transcript-api

```bash
python3 -m youtube_transcript_api <video_id> --languages ko 2>/dev/null
```

- `<video_id>` = the 11-char ID from the URL (e.g., `wr4nCMUy1dk` from `https://youtu.be/wr4nCMUy1dk`)
- `--languages ko` for Korean; `--languages en` for English
- Returns: `[{"start": float, "duration": float, "text": "..."}, ...]` — join `text` fields with newlines in time order
- **One-time install:** `python3 -m pip install youtube-transcript-api`

### Why not yt-dlp?

`yt-dlp --write-auto-sub --skip-download` fails with `Sign in to confirm you're not a bot` on **public** YouTube videos, even with browser cookie flags. No authentication makes this unavoidable. `youtube-transcript-api` works around this by hitting a different internal endpoint.

### Slug convention for YouTube

Format: `youtube-<video_id>` (e.g., `youtube-wr4nCMUy1dk`).

---

## Browser Content Extraction (non-YouTube)

For regular web pages (documentation, blogs, articles), use this sequence:

1. `browser_navigate` to URL → get compact interactive-element snapshot
2. `browser_console` with `document.body.innerText` → returns full readable text regardless of page length
3. Save the extracted text to `raw/<slug>.md`

| Page type | Method |
|-----------|--------|
| Simple .md / .txt / API doc | `browser_console` directly |
| Dynamic web page (docs, blog) | `browser_navigate` → `browser_console(innerText)` |
| Raw file URL (GitHub raw) | `terminal` with `curl` — fastest |
| Interactive page needing clicks | `browser_navigate` → `browser_snapshot` → `browser_click` → `browser_console` |

### Snapshot truncation

`browser_snapshot` truncates at ~8000 chars. `document.body.innerText` bypasses this limit entirely. Prefer `browser_console` for full text extraction on long-form pages.

Confirmed against `https://code.claude.com/docs/en/whats-new/2026-w22`: `browser_snapshot` truncated mid-content, while `document.body.innerText` returned the complete article.

---

## YAML frontmatter in skill files

When writing `SKILL.md` YAML frontmatter, **quote any description field containing URLs or colons**. Bare URLs like `https://example.com` break YAML parsing with `mapping values are not allowed here`.

```yaml
---
name: example-skill
description: "Fetch from https://example.com/api — works because quoted"
---
```

This previously broke `wiki-ingest`'s own `SKILL.md`: an unquoted URL in its description field caused all `patch`/`edit` operations on the file to fail until the field was quoted.
# Web & Video Content Extraction for Wiki Ingest

## YouTube Video Ingestion

**Do not use a page fetch or browser tool on YouTube video URLs.** The embedded player is opaque — the page yields no useful transcript content.

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

## Web Page Extraction (non-YouTube)

Capture the page's **full readable text** and save it to `raw/<slug>.md`. Use whichever tool your
session has; the method depends on the page:

| Page type | Method |
|-----------|--------|
| Raw file URL (GitHub raw, .md / .txt) | `curl` — fastest, byte-exact |
| Static article, docs page, blog | a web-fetch tool, asking for the full text rather than a summary |
| JS-rendered or click-to-expand page | a browser tool: load the page, open what needs opening, then read `document.body.innerText` |

### Check for truncation

Fetch tools and browser page snapshots can cut a long page short or return a summary. Before saving,
compare the end of the capture with the end of the article; if it stops mid-content, re-capture with
`document.body.innerText` in a browser tool or with `curl`. `raw/` is the immutable source, so a
truncated capture is a permanent gap.

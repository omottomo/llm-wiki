# YouTube Transcript Handling

## API Output Format

`youtube-transcript-api` returns a **list of segment dicts**, each with:
```python
{"start": 0.399, "duration": 4.4, "text": "어 어떤 점 때문에 상민 님이 그렇게"}
{"start": 2.6, "duration": 3.56, "text": "그 두 서비스를 좋아하시는 거세요?"}
...
```

- `start` — seconds (float)
- `duration` — seconds (float)
- `text` — Korean/English text string (may contain spaces, punctuation, URLs intact)

## Joining Strategy

**Join with `\n` (newline), not space**, because:
- Korean ASR often emits phrases as separate segments
- Newline preserves utterance boundaries → better paragraph structure when reading
- Transcript is plain-text body for raw/ storage, not formatted prose

```python
transcript = youtube_transcript_api(video_id, languages=["ko"])
body = "\n".join(seg["text"] for seg in transcript)
```

**Sort by `start` key first** if segments arrive out of order (they shouldn't, but defensively sort).

## Slug Format

Always use `youtube-<video_id>`:
- Video ID: `AwJrJmZW-Cc` from `https://youtu.be/AwJrJmZW-Cc?si=...`
- Slug → `youtube-AwJrJmZW-Cc`

## Language Priority

- `--languages ko` — Korean (preferred for Korean-speaking audience wiki)
- `--languages en` — English fallback
- The API accepts a list, tries in order; first successful transcript wins

## Raw File Header Format (standard as of 2026-07-12)

Save raw transcripts under `raw/` as `raw/youtube-<video_id>.md` with this header block:

```markdown
# [원본] <영상 제목> (<채널>)

- 출처 URL: https://www.youtube.com/watch?v=<video_id>
- 영상 ID: <video_id>
- 채널: <channel name — 확인 불가 시 "(불확인)">
- 발표자: <speaker name — only when different from channel; omit otherwise>
- 재생목록: <playlist_id> (index=N)   ← only when ingested from a playlist
- 자막 언어: ko (자동생성) | en
- 흡수일: YYYY-MM-DD

---

## 자막 전문

[joined transcript body]
```

**Required fields:** 출처 URL, 영상 ID, 채널, 자막 언어, 흡수일. The `---` separator after the header block delimits metadata from body — keep the header self-contained so the file is readable as-is.

> **Legacy note:** the 25 files ingested on 2026-06-23 (playlist `PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3`) use an older English-key header without a 채널 field. **Do not rewrite them — `raw/` is immutable.** Their channel attribution lives on the corresponding `wiki/sources/` pages instead. All future ingests use the format above.

## Channel Attribution — Known Pitfall

**Problem:** `youtube-transcript-api` returns only transcript text segments — no metadata about the channel or uploader. If the video is from an unknown or personal channel, you may not be able to determine the correct attribution from the transcript alone.

**What to do when channel is unknown:**
1. Check the video URL's origin — sometimes the channel name appears in the URL or can be looked up from the video ID
2. If still unknown, write `채널: (불확인)` in the raw file header
3. In the source summary page (`sources/`), note the uncertainty in the 메모 field: `메모: 채널 정보 불확인`
4. Do NOT guess or fabricate a channel name — accuracy over speed for attribution

**Signal to recognize:** API call succeeds with `[{"start":..., "duration":..., "text":"..."}, ...]` but there is no `channel` or `uploader` field in the response. This means **you are flying blind on attribution** — proceed with the ingest but flag it.

## Common Errors

- **"Sign in to confirm you're not a bot"** — yt-dlp fails with this on public videos. Use `youtube-transcript-api` instead; it works without auth.
- **Empty transcript** — video may have captions disabled. Try `--languages en` as fallback, or skip the video and note it in the report.
- **Wrong raw file header format** — Always use the header format from this file:
  - Required fields: `- 출처 URL:`, `- 영상 ID:`, `- 채널:`, `- 자막 언어:`, `- 흡수일:` — in that order
  - Wrong patterns: bold `**URL:**`-style keys, English keys (`video_id:` / `url:`), missing `---` separator, missing 채널 field
  - The `---` separator after the header block **must be present** before the transcript body
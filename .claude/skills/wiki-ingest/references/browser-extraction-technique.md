# Browser Content Extraction for Wiki Ingest

## Key technique learned (2026-05-31)

When ingesting a URL via `wiki-ingest <URL>` (no leading slash) and the page is a documentation/blog article (not a simple text file), the standard `browser_snapshot` approach truncates at ~8000 chars.

**Reliable extraction sequence:**
1. `browser_navigate` to URL → get compact interactive-element snapshot (for any initial interactions needed)
2. `browser_console` with `document.body.innerText` → returns full readable text regardless of page length
3. Use that text as the source content to save to `raw/<slug>.md`

This was confirmed against `https://code.claude.com/docs/en/whats-new/2026-w22` — the snapshot truncated mid-content, but `document.body.innerText` returned the complete article.

## When to use which extraction method

| Page type | Recommended method |
|-----------|-------------------|
| Simple .md / .txt / API doc | `browser_console` directly (no need for navigate first) |
| Dynamic web page (documentation, blog) | `browser_navigate` → `browser_console` with innerText |
| Raw file URL (GitHub raw, etc.) | `terminal` with `curl` — fastest and cleanest |
| Interactive page needing clicks | `browser_navigate` → `browser_snapshot` → `browser_click` → `browser_console` at end |

## YAML frontmatter issue (fixed 2026-05-31)

The `wiki-ingest` SKILL.md previously had an unquoted description field containing a URL with `https://`. The colons in the URL broke YAML parsing, causing all `patch`/`edit` operations on SKILL.md to fail with:
```
YAML frontmatter parse error: mapping values are not allowed here
```

**Fix applied**: The description field is now double-quoted in the YAML frontmatter. Any new description containing URLs or colons must be quoted.

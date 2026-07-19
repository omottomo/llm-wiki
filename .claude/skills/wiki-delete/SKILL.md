---
name: wiki-delete
description: "Delete existing wiki pages (a single page, a set of pages, or the whole wiki) and clean up afterward. Use when the user says deletion-related keywords about wiki content. This is a destructive, irreversible operation - confirm scope before deleting, repair dangling links, and update the index and log. By default only wiki/ is deleted; raw/ is only touched if the user explicitly asks for it."
---

# Wiki Delete

> **CLAUDE.md** — Read this file first and follow its rules for all wiki content.
> **Rules module: `docs/rules/wiki-content.md`** — Read this too; it holds the page authoring / index / domain rules for all wiki content.

Remove pages from the wiki **safely**. Deletion is irreversible, so the priority is to delete exactly what the user intends — no more, no less — and to leave the wiki consistent afterward (no dangling links, accurate index, logged).

> **All wiki content you write/repair must be in Korean. Also confirm and report to the user in Korean.** See CLAUDE.md LANGUAGE RULE.

> **HARD RULE: by default, deletion is confined to `wiki/`.** Never delete or modify anything under `raw/` — it is the immutable source of truth. If the user explicitly asks to also delete the raw source, then delete `raw/<file>` + `wiki/sources/<slug>.md` together with the wiki pages.

## Procedure

### 1. Resolve scope and confirm (mandatory — never skip)
Determine exactly which pages are targeted:
- **Single / few pages**: list each target page by path.
- **By topic/source**: read `wiki/index.md` to enumerate the matching pages, then list them.
- **Whole wiki**: every file under `wiki/`.
- **Source retraction**: remove a source's *influence* from the wiki without necessarily deleting its page — a different operation from the three above. See "Retraction" below.

**삭제 범위를 세 가지 옵션으로 구분하여 사용자에게 확인한다:**
1. **wiki/ 만 삭제** — wiki/ 아래 모든 파일 (page, sources, analysis 등); `raw/` 원본은 보존
2. **wiki/ + sources + raw** — wiki/ + 해당 source의 `wiki/sources/<slug>.md` + `raw/` 원본 파일까지 모두 삭제
3. **개별 페이지만 삭제** — 지정된 페이지만 (sources/raw 제외)

사용자에게 어떤 옵션인지 명시적으로 묻고 확인을 받은 후에만 삭제한다.

**Show the user the full list of files to be deleted (in Korean) and ask for explicit confirmation before deleting anything.** Examples:
- "다음 N개 페이지를 삭제합니다: [목록]. 진행할까요?"
- For a full wipe with raw included: "위키 전체와 원본 파일을 모두 삭제합니다. `raw/` 원본이 삭제되므로 이 작업은 되돌릴 수 없습니다. 정말 진행할까요?"

Do not delete until the user confirms. If the scope is ambiguous, ask which pages they mean rather than guessing.

### 2. Check inbound links before deleting
For each target page, run `python3 scripts/lint_wiki.py --inbound <page>` (path or slug) instead of hand-grepping for `[[page-name]]` — it prints every wiki page whose body currently links to that page. Briefly note to the user how many inbound links exist so they understand the impact. Keep this list: once the target page is deleted, every link it reported becomes dangling and must be repaired in step 4.

### 3. Delete
Remove the confirmed files from `wiki/` (and `raw/` if option 2 was chosen).

### 4. Repair dangling links (consistency cleanup)
After deletion, no page should point to a now-missing page. Go through the inbound list from step 2 and repair each one:
- In every page that linked to a deleted page, either remove the `[[...]]` link or, if the surrounding sentence still has value, rephrase it and mark that the referenced page was removed (in Korean).
- Do not leave orphaned `[[...]]` links to nonexistent pages.

### 5. Update index and log
- Remove the deleted pages' entries from `wiki/index.md`.
- Append one line to `log.md`: `## [date] delete | 삭제 대상 요지 — 페이지 N개 삭제, 링크 M건 정리`
- (For a full-wiki wipe, you may keep `log.md` itself with a final entry recording the wipe, or remove it too if the user explicitly asks. Default: keep `log.md` so the history survives — confirm with the user.)

### 6. Commit and report
- Commit: `git add -A && git commit -m "delete: <삭제 요지> — 페이지 N개"`. The pre-delete state stays recoverable from the previous commit.
- Tell the user (in Korean) what was deleted and what links were repaired.

## Retraction (fourth scope — source unreliable/withdrawn)

Use when a source turns out to be unreliable or withdrawn: remove its **influence** from the wiki, not just its page. Still human-gated — confirm scope (which source, which pages) before touching anything, same as step 1.

1. **Map blast radius**: `python3 scripts/lint_wiki.py --inbound <source-slug>` — the same inbound-link report from step 2, run against the source page.
2. **Flag**: mark every claim/paragraph that cites the retracted source with a `<!--RETRACTED-SOURCE-->` marker (an HTML comment, invisible in rendered output).
3. **Re-synthesize**: rewrite each flagged paragraph from the *remaining* sources only — keep what the surviving sources still support, cut what depended solely on the retracted one.
4. **Remove the markers** once each flagged spot is resolved. `scripts/lint_wiki.py` fails (exit 1) if any `<!--RETRACTED-SOURCE-->` marker is left in the wiki — run it to confirm none remain before finishing.
5. **Raw is opt-in, same HARD RULE as above**: the raw file and its `wiki/sources/<slug>.md` page are deleted **only** with explicit user confirmation. A retraction can legitimately end with the raw file kept (flagged unreliable but retained for the record) — do not delete it by default.

Confirm before flagging: "다음 원본을 철회 처리합니다: `<source-slug>`. 인용 문단 N곳에 마커를 답니다. `raw/` 원본은 별도로 명시적 삭제를 요청하지 않는 한 보존합니다. 진행할까요?"

Log and commit like step 5–6, but with a `retract` prefix instead of `delete`: `## [date] retract | 철회 대상 요지 — 마커 N건 재종합` / `git commit -m "retract: <철회 요지> — 문단 N건 재종합"`.

## Notes
- Read-only on `raw/` by default. Deleting a source means deleting its wiki pages, never the raw file — unless the user explicitly chooses option 2 (or, for retraction, explicitly confirms raw deletion in step 5 above).
- Prefer the smallest scope that satisfies the request. When in doubt, confirm.
- The wiki is git-backed: if the user later regrets a deletion, recover it via git history (`git log` → `git checkout <commit> -- <path>`).

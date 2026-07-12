---
name: wiki-delete
description: "Delete existing wiki pages (a single page, a set of pages, or the whole wiki) and clean up afterward. Use when the user says deletion-related keywords about wiki content. This is a destructive, irreversible operation - confirm scope before deleting, repair dangling links, and update the index and log. By default only wiki/ is deleted; raw/ is only touched if the user explicitly asks for it."
---

# Wiki Delete

> **WORKDIR: /Users/tomo/Desktop/ai-llm-wiki** — Execute all operations under this directory.
> **AGENTS.md: /Users/tomo/Desktop/ai-llm-wiki/AGENTS.md** — Read this file first and follow its rules for all wiki content.

Remove pages from the wiki **safely**. Deletion is irreversible, so the priority is to delete exactly what the user intends — no more, no less — and to leave the wiki consistent afterward (no dangling links, accurate index, logged).

> **All wiki content you write/repair must be in Korean. Also confirm and report to the user in Korean.** See AGENTS.md LANGUAGE RULE.

> **HARD RULE: by default, deletion is confined to `wiki/`.** Never delete or modify anything under `raw/` — it is the immutable source of truth. If the user explicitly asks to also delete the raw source, then delete `raw/<file>` + `wiki/sources/<slug>.md` together with the wiki pages.

## Procedure

### 1. Resolve scope and confirm (mandatory — never skip)
Determine exactly which pages are targeted:
- **Single / few pages**: list each target page by path.
- **By topic/source**: read `wiki/index.md` to enumerate the matching pages, then list them.
- **Whole wiki**: every file under `wiki/`.

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
For each target page, find which other pages link to it (`[[page-name]]`). This tells you what will break. Briefly note to the user how many inbound links exist so they understand the impact.

### 3. Delete
Remove the confirmed files from `wiki/` (and `raw/` if option 2 was chosen).

### 4. Repair dangling links (consistency cleanup)
After deletion, no page should point to a now-missing page:
- In every page that linked to a deleted page, either remove the `[[...]]` link or, if the surrounding sentence still has value, rephrase it and mark that the referenced page was removed (in Korean).
- Do not leave orphaned `[[...]]` links to nonexistent pages.

### 5. Update index and log
- Remove the deleted pages' entries from `wiki/index.md`.
- Append one line to `log.md`: `## [date] delete | 삭제 대상 요지 — 페이지 N개 삭제, 링크 M건 정리`
- (For a full-wiki wipe, you may keep `log.md` itself with a final entry recording the wipe, or remove it too if the user explicitly asks. Default: keep `log.md` so the history survives — confirm with the user.)

### 6. Commit and report
- Commit: `git add -A && git commit -m "delete: <삭제 요지> — 페이지 N개"`. The pre-delete state stays recoverable from the previous commit.
- Tell the user (in Korean) what was deleted and what links were repaired.

## Notes
- Read-only on `raw/` by default. Deleting a source means deleting its wiki pages, never the raw file — unless the user explicitly chooses option 2.
- Prefer the smallest scope that satisfies the request. When in doubt, confirm.
- The wiki is git-backed: if the user later regrets a deletion, recover it via git history (`git log` → `git checkout <commit> -- <path>`).

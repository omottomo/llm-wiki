---
name: wiki-lint
description: Health-check and tidy the wiki. Use when the user says "점검 / 건강검진 / 정리 / 일관성 확인 / lint / 위키 상태 봐줘", or wants to find and fix contradictions, stale claims, orphan pages, and missing links after the wiki has grown. Use this whenever the wiki needs periodic maintenance to stay healthy.
---

# Wiki Lint

> **CLAUDE.md** — Read this file first and follow its rules for all wiki content.
> **Rules module: `docs/rules/wiki-content.md`** — Read this too; it holds the page authoring / index / domain rules for all wiki content.

A periodic check that finds and fixes the problems that accumulate as the wiki grows.
Humans abandon wikis because of the maintenance burden — you carry that burden.

> **All wiki content you write must be in Korean.** Also report to the user in Korean. See CLAUDE.md LANGUAGE RULE.

## What to check

Get the full page list from `wiki/index.md`, then scan pages for:

1. **Contradictions** — pairs of pages with conflicting claims. Determine which rests on a more recent/reliable source and flag or resolve accordingly.
2. **Stale claims** — old claims a later source has already overturned. Update them or mark them "구버전(outdated)".
3. **Orphans** — pages with zero inbound links. Link them from related pages.
4. **Missing pages** — important concepts/people referenced in many places but lacking their own page. Create them.
5. **Missing cross-references** — related pages not yet linked. Add `[[...]]`.
6. **Data gaps** — gaps fillable via web search or more sources. (Don't auto-fill — propose to the user.)

## Procedure

1. **Pre-flight: run the deterministic linter first** — before everything else:
   ```bash
   python3 scripts/lint_wiki.py
   ```
   It mechanically checks wikilink integrity, `raw/` ↔ `wiki/sources/` parity (the most commonly missed check), frontmatter required keys, index.md coverage, orphan pages (zero inbound links besides index.md), and **page structure** (`check_page_structure`): a required heading missing for the page type, or a leftover lead paragraph between the H1 and the first `## `. These are objective — fix everything it reports and re-run until it exits clean, then move on.

   The script also prints a **가독성 경고** block that does *not* affect the exit code: a legacy closing heading (`## 관련 문서` / `## 같이 보기` / `## 연결`), an H2 section over 1,200 chars, an over-long sentence. Treat these as a work queue, not a gate — fix them on pages you are already touching rather than sweeping the corpus. Rules: `docs/rules/wiki-content.md` §1.1–§1.3. The LLM checks below are only for what the script cannot judge.

2. Run the judgment checks above (contradictions, stale claims, missing pages, missing cross-refs, data gaps) and **report findings grouped by category** (in Korean). For stale claims, prioritize time-sensitive claims whose as-of date (docs/rules/wiki-content.md §1) is older than ~6 months.
3. Apply obvious fixes immediately (link orphans, add missing cross-refs, update index).
4. For judgment calls (how to resolve a contradiction, how to handle a stale claim, whether to create a new page), **confirm with the user first.**
5. Additionally, propose **questions worth investigating next** and **sources worth looking for** (the added value of lint).
6. Append one line to `docs/log.md`: `## [date] lint | 모순 N건·고아 M건 등 발견 → 처리`
7. Commit the pass: `git add -A && git commit -m "lint: <요지>"` — the wiki is git-backed so every maintenance pass leaves an audit-trail commit.

## Report format
ALWAYS use this structure (write the content in Korean):
```markdown
## Lint 결과 (date)
### 모순
### 낡은 주장
### 고아 / 빠진 링크
### 누락된 페이지
### 데이터 공백 & 다음 탐구 제안
### 가독성 경고 (구 헤딩 · 과대 H2 · 과대 문장)
### 이번에 자동 처리한 것
```

## Notes
- On finding a contradiction, never arbitrarily delete one side. Weigh the evidence and flag, or ask the user if ambiguous.
- Read-only on `raw/`.

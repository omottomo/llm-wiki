---
name: wiki-illustrate
description: "Add Mermaid diagrams to existing concept and entity pages that explain an architecture, flow or hierarchy in prose only. Use when the user says \"그림 넣어 / 시각화 / 도식 / illustrate\" about the wiki or a specific page. Content mode - follows docs/rules/wiki-content.md §1.4: fenced Mermaid inside the page, cited caption, at most 3 per page, concepts/ and entities/ only. Never touches raw/. Never deletes prose or resolves contradictions (that is wiki-lint). Diagrams are reviewed on the PR, where GitHub renders Mermaid; the only pre-approval gate is the official-documentation image exception."
---

# Wiki Illustrate

> **CLAUDE.md** — Read this file first and follow its rules for all wiki content.
> **Rules module: `docs/rules/wiki-content.md`** — Read this too, especially §1.4 (그림), which this skill implements.

Backfill diagrams onto pages that already exist. `wiki-ingest` draws for new pages at write time; this skill covers everything written before phase-18 and any page a later ingest left prose-only.

> **All wiki content you write must be in Korean.** Diagram labels and captions are wiki content.

## Procedure

### 1. Scope
- Default target: every page under `wiki/concepts/` and `wiki/entities/` with zero figures. List them:
  ```bash
  grep -L '^```mermaid' wiki/concepts/*.md wiki/entities/*.md
  ```
- If the user named pages, restrict to those. Never touch `sources/`, `analysis/`, `overview.md`, `index.md` — lint rejects diagrams there.

### 2. Judge each page (§1.4 rule 6)
Read the page. Find the one section whose prose meets a draw criterion **and** that a table does not already cover:
- ≥3 components with stated relationships between them, or
- a flow of ≥3 steps, or
- a layered / containment hierarchy.

No section qualifies → skip the page and record one line of reason for the report (e.g. "표 두 개가 이미 구조를 다 보여줌").

### 3. Draw (§1.4 rules 1–5)
- One Mermaid fence directly after that section's prose (after its last paragraph, table or blockquote; before the next `## `). Never inside `## 한눈에 요약`.
- Type is one of `flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `timeline`. `flowchart` with `subgraph` is the usual choice for layers; `sequenceDiagram` for request flows; `timeline` for dated sequences.
- Every node label is a term the section already uses, in the section's Korean. Every arrow is a relation the section states with a citation. Nothing else — a diagram is a claim.
- Caption on the next line: `*그림 N. <한 문장> (→ [[sources/<slug>|label]])*` citing the same sources the section cites. Number from 1 per page.
- One diagram per page is the norm; a second only if a *different* section independently qualifies. Never more than 3.

### 4. Verify
```bash
python3 scripts/lint_wiki.py
```
Must exit 0. Fix any `그림` finding before moving on. If the repo has Node, optionally render the page locally to eyeball it: `python3 site/build.py && python3 -m http.server -d site/dist 8000`.

### 5. Record
- Bump `updated` in the frontmatter of every page you changed (content changed — §4.3).
- Append one line to `docs/log.md`: `## [YYYY-MM-DD] illustrate | 페이지 N쪽 그림 M장 — concepts/a · entities/b …`

### 6. Report (Korean, in chat)
- Pages touched, with the section each diagram sits under.
- Diagram count.
- Pages skipped and the one-line reason for each.
- Commit and PR per the git-workflow skill; the reviewer sees the diagrams rendered in the PR's file view.

## Notes
- Official-documentation images (§1.4 exception) are **not** part of the default pass. Only when the user explicitly asks, and only after posting the candidate (URL, licence text, what it shows) and receiving approval, may a file be written under `wiki/assets/`.
- Do not "improve" the prose while here. If a section is unclear, note it in the report; rewriting is a separate task.
- Do not resolve contradictions or delete anything — `wiki-lint` owns that.

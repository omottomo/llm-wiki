---
name: wiki-query
description: Answer questions against the wiki. Use when the user asks about the content of their knowledge base/wiki, or asks a question that requires synthesizing, comparing, or connecting multiple sources. The key is not to leave the answer only in chat: answers worth keeping (comparisons, analyses, newly discovered connections) get filed back into the wiki as new pages. Use this for any question that should be grounded in the wiki.
---

# Wiki Query

> **CLAUDE.md** — Read this file first and follow its rules for all wiki content.
> **Rules module: `docs/rules/wiki-content.md`** — Read this too; it holds the page authoring / index / domain rules for all wiki content.

Answer questions grounded in the wiki, and **file good answers back into the wiki.**
Key insight: a good comparison/analysis/connection produced in response to a question is wasted if it's buried in chat history. Turn such answers into pages so your explorations **compound** in the wiki just like ingested sources do.

> **All wiki content you write must be in Korean.** Also reply to the user in Korean. See CLAUDE.md LANGUAGE RULE.

## Procedure

### 1. Search (index first)
Always start from `wiki/index.md`. How far you drill depends on the **depth** the question
needs — pick one; the user's phrasing usually signals it:

- **quick** ("가볍게", "빠르게", "대충", a yes/no or one-fact lookup) — read `index.md` and the one-line descriptions only. Answer from the index; open a page only if the index is ambiguous.
- **standard** (default — most questions) — read the shortlisted pages, grep to the relevant slices, and follow `[[...]]` / `sources/` links as needed.
- **deep** ("깊게", "제대로", "전부 훑어서", or a synthesis/comparison spanning the whole domain) — read all candidate pages, follow See-Also chains, and cross-check the underlying `raw/` transcripts where a claim is load-bearing or a caption error is plausible.

(If a CLI search tool exists, use it. Otherwise index + grep is enough.)

### 2. Synthesize
- Build the answer from the pages you read. **Attach a source reference to every claim**, using the target's frontmatter `label` as the alias: `(→ [[sources/<slug>|#N 라벨]])`; join multiple citations with `·`. (Full link/citation format: `docs/rules/wiki-content.md` §1 — every body wikilink carries a Korean alias.)
- If pages contradict each other, don't hide it — present both sides in the answer. When the conflicting claims trace to sources of different `credibility` (source-page frontmatter, high|medium|low), weight the higher one and say which you trust more and why.
- If the wiki has **no basis to answer**, say so honestly. Don't fill gaps with guesses; instead suggest "이건 자료가 없으니 웹 검색하거나 자료를 더 넣자." When a gap points to a specific source or question worth pursuing later, offer to record it in root `backlog.md` (the ingest backlog — a candidate queue, never citable as evidence).

### 3. Choose the right format
Answer in whatever form fits the question: markdown explanation, comparison table, slides (Marp), chart (matplotlib), diagram, etc.

### 4. File back into the wiki (key step — don't skip)
If the answer goes beyond a simple fact lookup and produces a **comparison/analysis/new connection**:
1. Save it to `wiki/analysis/<slug>.md` (in Korean; record the source slugs it relied on in frontmatter).
2. Add `[[...]]` links from the relevant entity/concept pages to this analysis page.
3. Add it to the Analysis section of `wiki/index.md`.
4. Append one line to `log.md`: `## [date] query | 질문 요지 — analysis/<slug> 로 보존`
5. Commit: `git add -A && git commit -m "query: analysis/<slug>"` (only when something was filed back).

If it's a low-value one-line fact lookup, you may skip filing — use judgment, or ask the user "이거 위키에 남길까요?"

## Notes
- Ground answers in what's **in the wiki**. When you fall back on general knowledge outside the wiki, mark it as such.
- Read-only on `raw/`.

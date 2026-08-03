# Phase 14 — Readable Pages (concepts / entities / analysis)

> Drafted 2026-08-03 from the user's ask: "the wiki is too hard to read — give
> `entities/`, `concepts/` and `analysis/` a fixed body format like `sources/` has, and make the
> prose as easy as possible." Reference blog supplied by the user: https://inpa.tistory.com/
>
> Mostly content mode (`docs/rules/wiki-content.md`), with one bounded code-mode task
> (`scripts/lint_wiki.py`). Nothing under `raw/` is touched.

---

## 1. Why — the measured problem

40 pages: `concepts/` 20, `entities/` 17, `analysis/` 3. What a first-time reader hits:

| Symptom | Measured |
|---|---|
| No body template for these three types | Only `sources/` has one (`.claude/skills/wiki-ingest/templates/source-page.md`). The other three inherit *frontmatter + lead paragraph + citation form* and nothing else. |
| Closing section has three names | `## 관련 문서` ×7, `## 같이 보기` ×6, `## 연결` ×5 |
| One heading level only | Every page is H1 → H2. Zero H3 in the corpus. `concepts/harness-engineering.md` is 11,053 chars under 10 H2s — ~1,100 chars per unbroken section |
| Almost no visual aid | images 0/40 · code blocks 1/40 · tables 5/40 |
| Paragraph walls | `harness-engineering.md:43` and `:53` are single paragraphs of 5–7 sentences, several over 120 chars each |
| No scannable summary | The lead paragraph (phase-10) is prose for the listing extractor, not a skim target. There is no "3 bullets and you have the gist" block, and no conclusion at the bottom. §3-1 replaces the lead outright rather than stacking a second summary on top of it |
| Jargon introduced unevenly | `concepts/llm-basics.md` glosses every term on first use; `harness-engineering.md` glosses only in the lead, then runs `MCP`, `프리커밋 훅`, `아키텍처 테스트`, `가비지 컬렉션` bare |

The wiki's own charter (`wiki-content.md` §3) says the point is "making it easy for anyone else
to browse". These pages do not meet that yet.

## 2. Reference — what inpa.tistory.com actually does

Read: the blog root and the Cypress usage post (`/entry/Cypress-📝-웹-테스트-자동화-사용법-👀-한눈에-정리`).
Traits that map onto our problem:

1. **Three heading levels.** H2 topic ("Cypress 소개") → H3 sub-topic ("E2E 테스트 도구") → H4 task
   ("버튼 클릭 자동화"). Sections stay short enough to read in one screen.
2. **Gloss on first use, inline.** "E2E(End-to-End) 테스트란 '시작부터 끝까지'라는 의미로 …" — the
   English original, then a plain-Korean expansion, in the same breath.
3. **Tables for anything comparative.** The Cypress vs Selenium table covers language, browser,
   difficulty, speed, scope — one row per axis, no prose version of the same thing.
4. **Blockquote callouts** for caveats and side notes, visually separated from the body.
5. **Bold on key terms** so a skimmer can find `cy.visit()` / `describe()` without reading.
6. **Short imperative sentences** interleaved with longer explanatory ones.
7. **Closes with `참고문헌`** plus links to adjacent posts.
8. **It explains rather than states.** Samples: "쉽게 생각해서 간단하게 비유를 들자면 …",
   "다만 유의할점은 …". Someone is walking the reader through the material instead of filing a
   record of it.

Adopt 1–7 as written. Trait 8 is the one the user actually asked for, and **only at the level of
"explaining to someone" — not the blog's specific register.** The blog's `~해보자` invitationals,
emoji heading anchors and `여러분` are explicitly out; §4-2 defines what is in. **Reject** the
screenshot/GIF density too — we have no product UI to capture, and inventing diagrams is out of
scope for this phase (see §7).

## 3. Deliverable A — body templates

Three new template files beside the existing one, in
`.claude/skills/wiki-ingest/templates/`: `concept-page.md`, `entity-page.md`, `analysis-page.md`.
Same discipline as `source-page.md`: headings are reproduced **verbatim**, body is Korean.

Frontmatter, citation form and wikilink-alias rules are unchanged. The **lead paragraph is
removed** — see §3-1, which also covers the machinery that depended on it.

### concepts/

```markdown
# <제목>

## 한눈에 요약
- <핵심 1 — 한 문장>
- <핵심 2>
- <핵심 3>            ← 3~5개. 이 페이지를 안 읽고 지나가도 남아야 할 것.

## <자유 H2>          ← 주제에 맞게. 필요하면 H3로 더 쪼갠다.
## <자유 H2>

## 함께 읽기
- [[slug|별칭]] — 왜 이어 읽으면 좋은지 한 줄
```

### entities/

```markdown
# <이름>

## 한눈에 요약
- 무엇/누구인가 — 한 문장
- 이 위키에 왜 등장하는가 — 한 문장
- 알아 둘 점 1~2개

## <자유 H2 — 하는 일, 제품, 연혁 등>

## 이 위키에서의 등장
- [[slug|별칭]] — 어떤 맥락으로 나오는지

## 함께 읽기
```

`## 이 위키에서의 등장` is already the de-facto convention on 12 of 17 entity pages — this
promotes it to required rather than inventing anything.

### analysis/

```markdown
# <제목>

## 결론 먼저
> <한두 문장 결론. 콜아웃.>

## 비교표
| 축 | A | B |
|---|---|---|

## <자유 H2 — 근거, 단서, 반론>

## 함께 읽기
```

`analysis/` is a comparison genre — conclusion-first, then the table, then the reasoning. All
three existing analysis pages already carry a table; this makes it required.

### 3-1. Removing the lead paragraph

The user's call, 2026-08-03: the untitled prose block between the H1 and the first heading reads
as filler once `## 한눈에 요약` sits right below it. The two say the same thing twice — the
summary block was introduced in §3 above precisely to be the scannable opening, and it does that
job better. **The lead paragraph is dropped from all three types.** After this, a page opens
directly on its first `## ` heading.

This is not a prose-only edit. The lead is load-bearing in three places, and each needs a
replacement in the same pass:

| Depends on the lead today | Replacement |
|---|---|
| `site/build.py` `extract_summary()` via `SUMMARY_LEAD_RE` — feeds section listings, Pagefind result previews, `<meta description>` and `og:description` | Read the **first bullet(s) of `## 한눈에 요약`** instead, joining bullets until ~`SUMMARY_MAX` chars. Keep the old lead regex as a fallback so pages not yet converted keep their summary mid-migration |
| `wiki-content.md` §1 "Body" — the rule mandating the lead, added 2026-08-02 (phase-10) | Replace with the `## 한눈에 요약` requirement and restate the standalone-readability constraint there: **the first bullet is extracted, so it must read on its own, carry no citation paren and no wikilink** |
| §4-2 carve-out 2 in this plan (the lead stays declarative) | Now applies to the first summary bullet instead |

Consequences to accept, stated plainly:

- **A page loses its one no-background paragraph.** The bullets are compressed by design; a reader
  with zero context gets a terser landing than phase-10 intended. The mitigation is bullet 1: it
  must still say plainly *what the subject is*, expanding jargon on the spot, exactly as the lead's
  first sentence did.
- **`og:description` gets shorter and choppier.** A bullet is not a sentence. Joining two bullets
  softens this; it does not fully fix it.
- **This reverses a phase-10 decision** taken 2026-08-02 and applied to 39 pages. Recorded here so
  the next session reads it as a deliberate reversal, not drift, and does not "restore" the leads.

Scope: the lead is removed on all 39 concept/entity/analysis pages as part of the §6 rewrite —
`sources/` pages are untouched, their `## 한 줄 요약` already plays this role and
`SUMMARY_SOURCE_RE` keeps reading it.

### Required-heading summary

| Type | Required, verbatim | Free |
|---|---|---|
| `concepts/` | `## 한눈에 요약`, `## 함께 읽기` | everything between |
| `entities/` | `## 한눈에 요약`, `## 이 위키에서의 등장`, `## 함께 읽기` | everything between |
| `analysis/` | `## 결론 먼저`, `## 비교표`, `## 함께 읽기` | everything between |
| `sources/` | unchanged (5 headings) | — |

`## 관련 문서` / `## 같이 보기` / `## 연결` all become `## 함께 읽기`. One name, chosen because it
is an instruction to the reader rather than a filing label.

## 4. Deliverable B — writing-style rules

Added to `docs/rules/wiki-content.md` as new §1 subsections — "쉽게 쓰기 규칙" (§4-1 below) and
"어투" (§4-2). Both bind every future ingest, not just this phase's rewrite. Each rule is written
so it can be checked, not just felt:

1. **문장 100자 이하.** Longer → split. Korean technical prose past ~100 chars stops parsing on
   first read.
2. **문단 4문장 이하.** A fifth sentence means a new paragraph or a new heading.
3. **H2 한 덩이 1,200자 이하.** Over that → introduce H3. (`harness-engineering.md` averages
   1,105 and peaks far above.)
4. **전문용어 첫 등장 = 즉시 풀이.** Pattern: `가비지 컬렉션(garbage collection, 오래된 나쁜 코드를
   주기적으로 청소하는 것)`. Once per page, on first use only — repeat glosses are noise.
5. **3개 이상 비교/열거는 표.** Prose enumerations of parallel items become a table.
6. **주의·예외·논쟁은 blockquote 콜아웃** (`> `), not an inline parenthesis buried mid-paragraph.
7. **핵심 용어는 굵게.** For skimmers. One or two per paragraph, not every noun.
8. **비유 하나는 넣되 한 번만.** `harness-engineering.md`'s 말·마구 analogy works; repeating it
   three times does not.

### 4-2. 어투 — 남에게 설명하는 어투로

The corpus voice today is a filing record, not an explanation. `llm-basics.md:14`
"…확률 분포를 구하는 함수다" · `harness-engineering.md:22` "…시스템에 내장하는 것이다" — accurate,
and stiff. The target is the voice of someone explaining the material to a person sitting next to
them. Nothing more specific than that: **this is not an imitation of the reference blog's
register.**

Five rules, all Korean-prose habits:

1. **종결어미를 섞는다.** `~이다` 일변도를 깨고 `~한다`·`~된다`·`~인 셈이다`·`~라고 보면 된다`를
   함께 쓴다. Monotone endings are most of what makes the current pages feel like a spec sheet.
2. **어려운 대목 바로 뒤에 쉬운 말로 다시 말한다.** "쉽게 말하면 …", "한마디로 …", "비유하자면 …".
   The restatement is a separate short sentence, not a parenthesis.
3. **주의·예외는 연결어로 자연스럽게 잇는다.** "다만 …", "물론 …", "반대로 …" — instead of
   dropping a bare contrastive clause mid-paragraph.
4. **독자가 걸릴 지점을 짚어 준다.** "여기서 헷갈리기 쉬운데 …", "여기까지만 알아도 충분하다".
   Say where the hard part is rather than leaving the reader to find it.
5. **정의를 던지기 전에 왜 필요한지 한 문장.** Most pages open a section with the definition.
   One sentence of motivation before it turns a lookup into an explanation.

Explicitly **not** adopted, though the reference blog uses them: 청유형 `~해보자`, 수사 의문문,
`여러분`, 이모지 헤딩 앵커. The wiki is a reference, and `~해보자` only works where the reader is
following along with a procedure — our concept pages have none.

**Two carve-outs, and they are constraints, not taste:**

1. **인용이 붙은 사실 서술문은 단정형을 유지한다.** A sentence ending in
   `(→ [[sources/slug|#N 라벨]])` is a sourced claim. Softening it ("…인 것 같다", "…라고 보면
   된다") weakens an attributed fact into the wiki's own hedge. Vary the *connective* prose around
   those sentences; leave the claim itself stating what the source stated.
2. **`## 한눈에 요약`의 첫 불릿은 단정형 유지.** With the lead paragraph gone (§3-1),
   `site/build.py`'s `extract_summary` reads this bullet into listings, Pagefind results and
   `<meta description>`/`og:description`. It has to read as a standalone definition out of
   context, so conversational openers do not belong there. Same class of constraint as the
   citation format (`wiki-content.md` §4.2).

**Calibration specimen** — `concepts/harness-engineering.md:22`, current text:

> 예를 들어 프론트엔드 코드가 DB를 직접 호출하는 실수를 했을 때, 프롬프트에 "DB를 직접 호출하지 마"라고
> 추가하는 것은 부탁일 뿐이라 또 실수한다. 대신 아키텍처 테스트를 추가해 프론트엔드 폴더에서 DB를
> 임포트하면 빌드 자체가 실패하게 만든다 (→ [[sources/…|#11 프롬프트는 끝났다]]).

Rewritten to §4-1 + §4-2:

> 프론트엔드 코드가 DB를 직접 호출하는 실수를 했다고 하자. 흔한 대응은 프롬프트에 "DB를 직접 호출하지 마"를
> 한 줄 더 적는 것이다. 하지만 이건 부탁이라 또 어긴다.
>
> 대신 아키텍처 테스트를 하나 걸어 두면, 프론트엔드 폴더에서 DB를 임포트하는 순간 빌드가 실패한다
> (→ [[sources/…|#11 프롬프트는 끝났다]]). 쉽게 말하면 규칙을 지키라고 말하는 대신, 안 지키면 아예
> 진행이 안 되게 막아 버리는 것이다.

Four sentences instead of two, none over 100 chars, endings varied, one plain-language
restatement at the end — and the sourced claim keeps its flat declarative form.

## 5. Deliverable C — the check

`scripts/lint_wiki.py` gains one function, `check_page_structure(pages)`, reporting:

- a required heading missing for the page's `type` (§3 table)
- a legacy closing heading still present (`## 관련 문서` / `## 같이 보기` / `## 연결`)
- **a leftover lead paragraph** — prose between the H1 and the first `## ` on a
  concept/entity/analysis page (§3-1). Error, not warning: a page carrying both a lead and a
  summary block is the exact duplication this phase removes
- any H2 section over 1,200 chars
- any sentence over 100 chars (outside code fences and tables)

Voice (§4-2) is **not** linted — "explains rather than states" has no mechanical form, and a
regex for sentence endings would fight carve-out 1 on every sourced claim. It is checked by
reading, in §8.

Warnings, not hard failures, except the missing-required-heading case which is an error — the
same severity split the existing checks use. Structure checks run over `wiki/` only; `raw/` is
untouched.

This is the phase's runnable check: the rewrite of 40 pages is verified mechanically, not by
re-reading each one.

## 6. Deliverable D — the rewrite (40 pages)

Order is by reader impact, longest and most-linked first. Each batch: apply the template, drop the
lead paragraph (§3-1), apply §4-1 and §4-2, bump `updated` (this is a content change — §4.3
exemption does not apply), keep every citation and wikilink intact.

**Sequencing constraint:** the `extract_summary` change in §3-1 must land *before* the first batch.
Strip a lead while the extractor still looks for one and that page ships with an empty summary in
listings, search results and its `og:description`.

The voice change is the largest part of the diff — it touches connective prose in every paragraph,
where the template change only touches headings. Budget accordingly: batch A is not a heading
rename with some polish, it is a rewrite.

| Batch | Pages | Note |
|---|---|---|
| A | `concepts/` top 8 by length — harness-engineering, claude-md, verification-automation, subagents-agent-teams, dynamic-workflow, skills, developer-role-change, hooks | The worst walls. Do these first; they are also the most-linked |
| B | `concepts/` remaining 12 | |
| C | `entities/` 17 | Short pages, mostly adding `## 한눈에 요약` and renaming the closing heading |
| D | `analysis/` 3 | Conclusion-first restructure; tables already exist |
| E | `wiki/overview.md`, `wiki/index.md` | Only if the rewrites changed what they describe |

**Rewrite is not deletion.** No claim leaves a page. Splitting a paragraph, adding a gloss, or
moving a caveat into a callout does not drop the citation attached to it — every
`(→ [[sources/slug|#N 라벨]])` survives with the sentence it belongs to. Contradictions flagged
under existing pages stay flagged (CLAUDE.md core principle 4).

The one deletion is the lead paragraph (§3-1), and it is not a claim loss: the lead carries no
citation by rule, and whatever it asserted is either restated in `## 한눈에 요약` or already said —
with its source — in the body below. Check that before cutting, page by page.

## 7. Out of scope (deliberate)

- **Diagrams.** `site/build.py` has no mermaid or image pipeline, and none of the 40 pages has an
  image today. Adding one is a separate code-mode phase; tables cover the comparative cases now.
- **`sources/` pages.** Their template works and `wiki-ingest` depends on it verbatim.
- **New `site/` rendering** for callouts. Blockquotes already render; whether they get a styled
  box is a later CSS-only change.
- **The `updated`-date convention, citation form, tag vocabulary.** Untouched.

## 8. Verification & close-out

Order per `docs/rules/site-code.md`: `python3 scripts/lint_wiki.py` → `python3 site/build.py` →
`python3 scripts/verify_site.py`. Then spot-read three rewritten pages as a visitor with no
background — that read is also the only check on §4-2, so judge it explicitly: does the page
sound like someone explaining, or still like a record?

Close-out: one `docs/log.md` line, and `docs/index.md` updated for this plan (note: the
`phase-13-pr-gate-and-infra-ci` entry is also missing from `docs/index.md` — fold that fix in).

## 9. Open decisions for the user

1. **Batch pacing** — default is A→E in one continuous run. Alternative: ship batch A, look at it,
   then decide. Recommended: **stop after batch A for a look**, since the template is unproven
   until it meets the hardest page.
2. **`## 한눈에 요약` on every concept page** — it is the biggest single readability win but also
   the most boilerplate. Alternative: required only on pages over ~3,000 chars. Recommended:
   **all pages**, because a short page's summary costs three lines and a reader cannot know in
   advance which pages are short.
3. **Voice calibration** — §4-2 is a judgement call that a rule list can only approximate. Batch A
   produces the first rewritten page; read it and say "더 풀어서" or "과하다" once, and the rest of
   the corpus follows that calibration. This is the main reason to stop after batch A (decision 1).

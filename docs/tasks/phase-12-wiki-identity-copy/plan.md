# phase-12-wiki-identity-copy — Correct the wiki's self-description

## Why

Two stale identity claims are published across the wiki and the site.

1. **Medium-bound framing.** `wiki/overview.md` and `wiki/index.md` still describe the wiki as a
   digest of one YouTube playlist ("첫 시드는 유튜브 재생목록 하나… 영상 25편", "유튜브 출처는
   대부분 한국어 채널의 영상이며, 자동생성 자막을 원본으로 흡수했다"). The wiki accumulates
   whatever the operator chooses, regardless of medium — `docs/rules/wiki-content.md` §3 already
   says so, but the pages contradict it.
2. **Topic-bound framing.** Overview, index, several concept/entity pages, the site copy in
   `site/build.py`, and the charter in `docs/rules/wiki-content.md` §3 all assert the wiki's
   central subject *is* Claude Code / harness engineering ("현재의 중심 주제는…", "이 위키의 중심
   개념", "위키 전반의 중심 도구"). The operator's actual central subject is: accumulate and
   develop knowledge they choose into a personal LLM wiki, and make it easy for others to browse.
   AI-agent coding and harness engineering are one chosen topic among several.

Goal: sweep both framings out of `wiki/`, the site copy, and the operating charter — while keeping
every per-source factual note (`재생목록:`, `자막:`, `#N` labels) intact.

## Modes

Mixed. `wiki/` prose is content mode (`docs/rules/wiki-content.md`); `site/build.py` and
`docs/rules/` are code mode (`docs/rules/site-code.md`). Both modules were read before starting.

## Decisions (from the operator)

| Item | Decision |
|---|---|
| `SITE_DESCRIPTION` | `"직접 고른 자료를 읽고 정리해 쌓아 올리는 개인 지식 위키입니다"` — operator's exact wording, used verbatim |
| `wiki/overview.md` frontmatter `title` | `위키 개요` |
| "이 위키의 중심 개념/중심 도구" sentences | delete the whole sentence |
| `docs/rules/wiki-content.md` charter (L153–154) | fix in the same phase |

## Do not touch

- `raw/` — immutable (CLAUDE.md core principle 1).
- The `재생목록:` / `자막:` / `URL:` bullets inside each `wiki/sources/youtube-*.md` `## 출처 정보`
  block, and the `자막상 …` / `자막 오인식` caveats attached to specific claims. Those are facts
  about an individual source, not claims about the wiki.
- Every `label: "#N …"` and every citation `(→ [[sources/…|#N …]])`. `site/build.py`'s
  `render_citations` takes the chip number from the `#N` prefix (`wiki-content.md` §4.2,
  `site-code.md` §2.4) — the parser has no error path, so an edited label renders raw mid-sentence.
- `.claude/skills/wiki-ingest/**` — YouTube pipeline instructions describe *how to collect*, not
  what the wiki is.
- `site/dist/**` — build output, regenerated, never hand-edited.
- `SITE_NAME = "LLM 위키"` — already neutral; `site/test_build_site.py:36` asserts on it.

## Tasks

`prd.json` holds T01–T08. Shape: T01–T07 are the edits (overview, index, concepts, entities,
analysis, site copy, charter); T08 is the exhaustive re-grep plus the verification matrix, the
`docs/log.md` line and the commits.

Weak phrasings kept on purpose (they scope a topic, they do not declare the wiki's identity):
`hashicorp.md:12`, `sentinel.md:12`, `agentic-coding.md:12`, `openai.md:11`, `context-decay.md:12`,
`multi-model-workflow.md:49`, `claude-md.md:22`, `harness-engineering.md:64`.

## Lead-paragraph constraint

`wiki-content.md` §1 requires a 3–4 sentence lead on `concepts/`, `entities/` and `analysis/`
pages, and `site/build.py:extract_summary()` lifts its first sentence into listings, search
results and `<meta description>`. On `entities/claude-code.md` and `entities/anthropic.md` the
identity sentence sits inside the lead, so deleting it would leave a 2-sentence lead — there it is
**replaced** with a topic-neutral sentence rather than deleted (T04).

## Verification

`site-code.md` §2.3 order, run at T08:

1. `python3 scripts/lint_wiki.py` → exit 0
2. `python3 scripts/test_lint_wiki.py` → exit 0
3. `python3 site/build.py` → exit 0
4. `python3 site/test_build_site.py` → exit 0
5. `python3 scripts/verify_site.py` → exit 0

Plus an eyes-on check of `site/dist/index.html` (`<meta name="description">`, `<p class="intro">`)
and `site/dist/overview/index.html` (`<title>`), and a final repo-wide grep whose every remaining
hit must be per-source metadata, an `#N` label, or legitimate topical prose.

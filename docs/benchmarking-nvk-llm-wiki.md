# Benchmarking against nvk/llm-wiki (2026-07-19)

Agent-facing operating document (English, per the CLAUDE.md language rule). Records a comparison
of this repo against another developer's LLM-wiki project and the adoption decisions that came
out of it. The decisions are executed as phases `phase-6-nvk-schema-docs` (part A) and
`phase-7-nvk-skills-tests` (part B).

## What nvk/llm-wiki is

`github.com/nvk/llm-wiki` (v0.16.0, MIT). Same seed idea as this repo — Karpathy's "LLM wiki"
(the agent is the compiler, raw sources are source code, the wiki is the executable) — but a
different **shape**: it is a **multi-runtime plugin product**, not a single wiki instance. The
wikis it manages live at the end user's `~/wiki/`; the repo ships the *protocol* and *tooling*:

- One behavioral source of truth (`claude-plugin/skills/wiki-manager/`) plus **generated** thin
  packaging for Claude Code, OpenAI Codex, OpenCode, a Pi/DS4 local-model profile, and a portable
  single-file `AGENTS.md` for any agent.
- A **hub-and-spoke** model: a registry-only hub (`~/wiki/`) over many isolated single-topic
  wikis under `topics/<name>/`, plus an `.archive/` layer.
- ~20 operations (ingest, ingest-collection, compile, query, research, thesis, collect, retract,
  refresh, inventory, dataset, archive, lint, audit, librarian, plan, project, feedback,
  lessons-learned).
- A real test/CI apparatus: a golden wiki fixture, one generated defect fixture per lint rule,
  LLM-free structural shell tests, token-efficiency benchmarks, and Promptfoo behavioral evals.

The gap that matters: they are building a **distributable product for many users and runtimes**;
we are maintaining **one personal Korean wiki published with Quartz**. So the goal was never to
port their surface area — it was to pick the ideas that pay off at our scale and drop the rest.

## What we already had (no adoption needed)

Contradiction preservation (keep-both-and-flag), as-of markers on volatile claims, an append-only
greppable `log.md`, an accumulated-rules ledger (`site-code.md` §2.4), a deterministic lint gate
in CI (`lint_wiki.py`), blast-radius lookup (`lint_wiki.py --inbound`), index-first querying, and
filing query answers back into `analysis/`, and a `raw/` ↔ `sources/` 1:1 parity check. These
overlap with nvk mechanisms; nothing to import.

## Adopted

| Item | Phase | Rationale |
|---|---|---|
| **`credibility: high\|medium\|low`** on source pages (rubric + lint enum + 27-page migration) | 6 | Lets `wiki-query` weight one source over another when they disagree — an anonymous auto-caption re-explainer should not outrank official docs. Cheap: one enum, one rubric. |
| **`aliases: [...]`** (optional) on concepts/entities | 6 | Quartz reads it natively. Bridges our Korean-title rule (§4.4) and English original terms so `context engineering` finds `컨텍스트 엔지니어링` in site search. |
| **Three `wiki-query` depths** (quick / standard / deep) | 6 | Names the effort/latency trade-off already implicit in querying and maps user phrasing (가볍게 / 깊게) to it. Doc-only. |
| **`backlog.md`** ingest queue (root, unpublished) | 6 | The minimal slice of nvk's `inventory` layer: a candidate/question/watch queue. One table, explicitly *not* citable as evidence. |
| **`volatility: hot\|warm\|cold`** on source pages | 7 | Drives refresh targeting; a fixed YouTube talk (cold) never needs re-checking, a living doc (hot/warm) does. Timely now that web docs are being ingested. |
| **`wiki-refresh` skill** (human-gated) | 7 | Re-checks hot/warm source URLs, classifies change (cosmetic/additive/contradictory), updates pages only on human confirmation; raw/ stays immutable (a changed source is a new raw file). |
| **Retract mode** in `wiki-delete` + unresolved-marker lint | 7 | Dependency-aware source removal: blast radius via `--inbound`, `<!--RETRACTED-SOURCE-->` markers, re-synthesis from remaining sources. Completes the §3 caption-error workflow. |
| **Golden + defect fixture tests** for `lint_wiki.py` (`scripts/test_lint_wiki.py`, stdlib) in CI | 7 | `lint_wiki.py` is now the single enforcer of our frontmatter/link schema; adopting nvk's "lint rules ARE the schema" principle means regressions in it must be caught. Stdlib, no framework. |

## Rejected (with reason)

| Item | Why not |
|---|---|
| **Dual-linking** (`[[wikilink]]` + `[md](path)` on one line) | Quartz and Obsidian both read the wikilink; we don't target GitHub rendering. It would only bloat Korean prose. |
| **Hub / multi-wiki registry + archive layer** | We already split `career-llm-wiki` into a sibling repo. A registry over two wikis is overhead. Revisit at 3+. |
| **Full `inventory` / `dataset` / `collect` layers** | Management cost outweighs value for one personal wiki. Adopted the minimal slice as `backlog.md` instead. |
| **`librarian` 0–100 numeric staleness/quality scoring** | At ~67 pages, `wiki-lint`'s LLM judgment pass already covers this. Revisit at hundreds of pages. |
| **`lessons-learned` operation** | The accumulated-rules ledger (§2.4) plus detailed `log.md` post-mortems already capture this by hand. |
| **`research` / `thesis` multi-agent pipelines** | Genuinely valuable (biggest capability jump), but out of this scope — deferred to a future dedicated phase, minimal form only. |
| **Multi-runtime packaging, token benchmarks, session-capture hooks, boot-identity line** | All serve a distributable multi-user product. Pure overhead for a single-user repo. |

## Notes for the next session

- The `credibility` migration followed the durable rubric in `wiki-content.md` §1, not the
  PRD's shorthand ("unverified attribution → low"). All 25 playlist videos have unconfirmed
  (`미상`/`불확인`) attribution, but the rubric downgrades to `low` only when the claims are
  *also* uncorroborated or the framing is speculative. Result: 2 official docs = high, 2
  speculative-opinion videos (#15, #16) = low, the other 23 corroborated technical explainers =
  medium. If you later want a stricter split, re-grade — the field is source-quality, not fixed.
- Source: the nvk repo was read at v0.16.0; its `AGENTS.md` is the portable protocol if you want
  to look deeper.

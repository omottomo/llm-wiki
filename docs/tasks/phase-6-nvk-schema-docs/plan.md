# phase-6-nvk-schema-docs — nvk benchmark adoption, part A (schema & docs)

Adopted from a 2026-07-19 comparison against nvk/llm-wiki (see
`docs/benchmarking-nvk-llm-wiki.md`, written as task T07 of this phase).
Part A = quick wins: two frontmatter fields, query depth tiers, an ingest
backlog, and the benchmark report itself. Part B (freshness, retraction,
lint fixtures) is `phase-7-nvk-skills-tests`.

Scope note: numbered phase-6/7 because `phase-5-guided-home-redesign` already
exists. Executed directly (the my-skills orchestration plugin was uninstalled
2026-07-19; CLAUDE.md §3 cleanup is task T08).

## What changes

- `credibility: high|medium|low` — required on `wiki/sources/*` pages; rubric
  in `docs/rules/wiki-content.md` §1 (official docs/primary = high, conference
  talks/vendor blogs = medium, caption-error-prone personal videos = low).
- `aliases: [...]` — optional on concepts/entities; bridges Korean titles and
  English original terms in Quartz search.
- wiki-query gets three explicit depths: quick / standard (default) / deep.
- Root `backlog.md` (Korean, unpublished): ingest candidates, open questions,
  watch items. Never citable as factual evidence.
- `docs/benchmarking-nvk-llm-wiki.md`: the comparison report (what was
  adopted, what was rejected and why).
- CLAUDE.md §3: remove dead my-skills routing.

## Gate

`python3 scripts/lint_wiki.py` exit 0 after every task that touches wiki/ or
the linter; `npx quartz build` + `verify_site.py` for both sites at close-out;
one `docs` line in log.md.

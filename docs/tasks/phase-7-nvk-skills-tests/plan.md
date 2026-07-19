# phase-7-nvk-skills-tests — nvk benchmark adoption, part B (freshness, retraction, lint tests)

Part B of the 2026-07-19 nvk/llm-wiki benchmark (rationale:
`docs/benchmarking-nvk-llm-wiki.md`). Depends on phase-6 (credibility field,
lint plumbing) being merged first.

## What changes

- `volatility: hot|warm|cold` — required on `wiki/sources/*`; YouTube talks
  are cold (fixed snapshots), living official docs hot/warm. Drives refresh
  targeting. Lint enum check + 27-page migration.
- New content-mode skill **wiki-refresh**: re-check hot/warm source URLs,
  classify changes (cosmetic / additive / contradictory), update wiki pages
  only after human confirmation. raw/ stays immutable — a changed source is
  re-captured as a NEW raw file; the source page records the refresh history.
  CLAUDE.md §3 gets a routing row (trigger: 최신화 / refresh).
- **Retract mode** in wiki-delete: blast-radius via `lint_wiki.py --inbound`,
  tainted claims flagged `<!--RETRACTED-SOURCE-->`, affected paragraphs
  re-synthesized from remaining sources, markers resolved. Lint gains an
  unresolved-marker check.
- **Lint fixture tests** (`scripts/test_lint_wiki.py`, stdlib assert runner):
  `tests/fixtures/golden-wiki/` (tiny known-good wiki) must exit 0; one defect
  fixture per lint check must exit 1 with that violation reported. One line in
  the CI lint job. Principle adopted: lint rules ARE the schema — schema
  changes update lint + fixtures, never one-off migration code.

## Gate

Golden fixture green, all defect fixtures red for the right reason, repo lint
exit 0, CI green on push, dry-runs of refresh (Terraform source) and retract
(on a golden-wiki copy, not the real wiki), one log.md line.

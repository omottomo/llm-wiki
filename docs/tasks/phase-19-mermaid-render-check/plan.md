# Phase 19 — Mermaid render check in CI

**Goal.** No Mermaid block reaches `main` without a machine having parsed it. Today nothing does:
`scripts/lint_wiki.py` `check_diagrams` validates the *envelope* (caption, citation, type, count,
page type) and explicitly does not parse the diagram — `lint_wiki.py:443` says so and names this
phase as the remedy:

> Mermaid 문법은 파싱하지 않는다 (Python 파서 없음). GitHub PR 미리보기가 렌더하므로 깨진 그림은
> 리뷰에서 눈으로 잡는다. main에 깨진 그림이 올라오면 CI에 mermaid-cli 단계 추가.

The diagram source is rendered in the *reader's browser* (`site/build.py` emits
`<pre class="mermaid">`, Mermaid 11.17.2 from jsdelivr does the work). A syntax error therefore
ships silently and surfaces as a red error box on the live site. The only current gate is a human
looking at the GitHub PR preview.

## Design

**Parse, not render.** `mermaid.parse(src)` runs the grammar and throws on a syntax error. That is
exactly the scope agreed with the user: *"뜨긴 뜨나"* — it catches typos, malformed arrows,
unclosed brackets. It does **not** catch overlapping labels, overflowing text or an unreadable
layout; those stay a human job on the PR. The check must never be described as a quality gate.

**No headless browser.** `@mermaid-js/mermaid-cli` (`mmdc`) is the obvious tool and was rejected:
it declares `puppeteer` as a peer dependency, so every CI run would install and drive a ~150 MB
Chromium to answer a yes/no question about grammar. `mermaid.parse` needs only enough DOM for
`dompurify` to bind at import time, which `jsdom` supplies in under a second. Verified locally
(node 24): three valid diagrams parse, two malformed ones throw.

**Same version as the browser, asserted.** `site/build.py` pins `MERMAID_VERSION = "11.17.2"` for
the CDN script. A checker on a different version is a lying gate in both directions, so the
checker **reads that constant out of `site/build.py`** and fails loudly if the installed `mermaid`
package does not match it. Bumping the pin in one place and not the other becomes a CI failure
instead of a silent divergence — the same coupling-with-a-guard shape as
`KNOWN_TAG_VARIANT_GROUPS` (`site-code.md` §2.4), but machine-enforced rather than documented.

**Node, in the `verify` job.** The check needs Node, and `verify.yml`'s `lint` job is deliberately
Node-free so it neither waits on the build nor duplicates it (§2.4, 2026-08-03). The step
therefore joins `verify`, which already runs `actions/setup-node`. `deploy.yml` is left alone: it
is the raw-boundary gate, and adding a Node install there buys nothing that the required PR check
does not already cover.

**Install without a manifest.** `npm i --no-save mermaid@<pin> jsdom@<pin>` at the repo root keeps
the repo free of a `package.json`, a lockfile and a second dependency tree; §2.2's "no Node build"
invariant survives, and root `node_modules/` is gitignored. Versions live in the workflow step and
in the §2.3 row, where they are read, not buried.

## Scope

In: `scripts/check_mermaid.mjs`, one step pair in `.github/workflows/verify.yml`, a
`node_modules/` line in `.gitignore`, the §2.3 verification row, one §2.4 accumulated rule,
`docs/index.md`, one `site` line in `docs/log.md`.

Out: `wiki/` prose (content mode), `lint_wiki.py` (stays Python-only and Node-free),
`tests/fixtures/` (the fixture suite is the *lint schema* harness per §2.4 2026-07-19; this
checker is not a lint rule and needs a Node toolchain the fixture runner does not have), layout
or readability judgement, `deploy.yml`.

## Base branch

Branched from `main`, which carries exactly **one** Mermaid block (`wiki/concepts/kubernetes.md`,
the phase-18 example). The other 17 live unmerged on `feat/wiki-illustrate`. That ordering is
deliberate: landing the gate first makes the `wiki-illustrate` PR its first real subject. Local
verification therefore runs the checker against a copy of those 17 blocks via the optional root
argument, and separately against a corpus with none, where it must exit `0` with an explicit "no
diagrams" line rather than reporting a vacuous pass.

## Verification

Order per §2.3: `lint_wiki.py` → `build.py` → `test_build_site.py` → `verify_site.py`, plus the new
checker against (a) `main`'s empty corpus, (b) the 17 real blocks, (c) a deliberately broken block.
Per §2.4 (2026-07-17), the phase is not closed until the first CI run of the new step is observed
green — `gh run list` after the PR opens, not an assumption.

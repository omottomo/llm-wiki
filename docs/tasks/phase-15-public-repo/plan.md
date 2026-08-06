# phase-15-public-repo — take the repo public as a portfolio artifact

## Problem

`omottomo.github.io` is the user's portfolio, and `llm-wiki` should appear in its project
section. That requires strangers to be able to read the repository. It is private today, and the
repo's own rules forbid the flip: `docs/rules/site-code.md` §2.1 — *"must **never** land in a
public repo"* — and line 71 — *"Never flip the repo to public."*

Those rules are not obsolete. They exist because `raw/` holds other people's work, and that is
still true. **This phase removes the reason, not the rule.**

## What the audit found

The current tree and all commits on `main` were scanned before planning (231 at audit time, 232
as of the re-verification below — the count moves with every commit, so it is captured at rewrite
time rather than hardcoded).

| | finding | where |
|---|---|---|
| blocker | 29 tracked third-party source files — 26 YouTube auto-transcripts (full text), a 71 KB HashiCorp docs excerpt, an IBM article, a Tistory post | `raw/`, and every commit in history |
| blocker | real personal emails as commit authors — `whddlsk123@naver.com` (30 commits), `whddlsk97@gmail.com` (12) | git history |
| medium | AWS account ID `<ACCOUNT_ID>`, including the tfstate bucket name | `infra/terraform.tfvars`, `infra/versions.tf`, `infra/iam-deploy.tf:77`, `docs/tasks/phase-9-aws-deploy/implementation.md:14,19`, history |
| clean | **no credentials.** All 231 commits scanned for `AKIA`/`ASIA`/`ghp_`/`github_pat_`/`sk-ant`/`xox*`/`BEGIN … PRIVATE KEY`: zero hits. Deploy is OIDC, so no long-lived key exists to leak | — |
| clean | fork PRs cannot reach AWS. `deploy.yml` triggers on `push` to `main` only and the OIDC `sub` is pinned to `refs/heads/main`; `verify.yml` is `pull_request` (not `pull_request_target`), `contents: read`, no secrets | — |
| clean | `wiki/` is already on the public internet at `omotomo-llm-wiki.com`, so publishing it adds no exposure | — |
| tidy | `.obsidian/` is tracked, including a vendored third-party plugin bundle (`plugins/terminal/main.js`) | `.obsidian/` |
| tidy | 13 `.claude/skills/*` symlinks point into gitignored `.agents/` — dangling in any clone | `.claude/skills/` |
| tidy | no `LICENSE`, no `README.md` | repo root |

Decisions taken with the user: flip this repo rather than maintain a synced mirror, move `raw/`
to a private repo, unify author emails to the GitHub `noreply` address. The account-ID scrub is
folded in because `git filter-repo` does it in the same pass for free.

Worth naming as an upside: a public repo unlocks branch protection and rulesets on the free
plan. That is the exact capability `deploy.yml`'s comment and phase-13's plan record as
unavailable (`403 Upgrade to GitHub Pro or make this repository public`), and the `lint` job
duplicated into `deploy.yml` as "the last machine gate" can finally be backed by a required check.

## The one correction to the obvious shape

"Rewrite history, force-push, flip the switch" does not actually remove anything from GitHub.
A force-push leaves the pre-rewrite commits reachable: `refs/pull/N/head` pins them for every
merged PR, and dangling objects stay fetchable by SHA until GitHub's own GC runs. While the repo
is private nobody can reach them. **The moment it goes public, every purged transcript and every
purged email is one SHA away** — and the SHAs are listed on the PR pages themselves. The
documented remedy is to ask GitHub Support to purge cached views, a round trip with no verifiable
completion signal.

So the flip is done by moving the rewritten history into a **fresh repo**:

1. rename `omottomo/llm-wiki` → `omottomo/llm-wiki-archive` and keep it **private and frozen** —
   it becomes the historical archive and holds the only copy of the old history and its PR refs;
2. create a new **public** `omottomo/llm-wiki` and push the filter-repo output into it;
3. repoint `origin`.

This is not the "mirror repo" option the user declined. That one was a squashed snapshot needing
perpetual sync. This keeps the whole `main` history (rewritten, commit-for-commit), leaves exactly
one working repo, and needs no sync — the archive never moves again.

## Design

### `raw/` becomes a nested private repo

`raw/` leaves the parent repo's index and gains its own git repo with remote
`omottomo/llm-wiki-raw` (private). The parent `.gitignore` ignores `raw/`, so the ingest workflow
is unchanged — sources still land in `raw/`, they just commit to a different remote.

The `raw/` boundary invariant is rewritten, not dropped. It used to rest on two legs, one of
which was "the GitHub repo stays private". The replacement pair:

1. **`raw/` is never tracked** — asserted by a new `verify_site.py` check that `git ls-files raw/`
   comes back empty, so a `git add -f` slip fails the build;
2. **the generator's content root is still `wiki/` only** — unchanged.

### Keeping the parity check alive without shipping the sources

`lint_wiki.py` hard-exits when `raw/` is missing (`scripts/lint_wiki.py:493`) and both workflows
run it, so a clone without `raw/` reddens CI immediately. Fixing that by simply skipping the
check would silently drop the `raw/ ↔ wiki/sources/` 1:1 parity rule from CI — the wiki's main
structural invariant.

Instead: a tracked `docs/raw-manifest.txt`, one slug per line, sorted, **filenames only, no
content**. `check_parity()` reads real `raw/*.md` when the directory exists and falls back to the
manifest when it does not; when both exist and disagree, that is an error, because the manifest
has drifted. `scripts/lint_wiki.py --update-manifest` rewrites it. Nothing copyrighted crosses
over — a slug is the same string the source page already publishes in its `raw:` citation.

### AWS identifiers out of the working tree

- `infra/terraform.tfvars` → gitignored; `infra/terraform.tfvars.example` tracked with placeholders.
- `infra/versions.tf`: a `backend "s3"` block cannot take variables, so `bucket` is removed and
  supplied by **partial config** — gitignored `infra/backend.hcl`, tracked `infra/backend.hcl.example`,
  and `terraform init -backend-config=backend.hcl`. This is a footgun for the next session: it is
  recorded in `site-code.md` §2 and in the example file's own comment.
- `infra/iam-deploy.tf:77` `tfstate_bucket` literal → `var.tfstate_bucket_name`.
- `docs/tasks/phase-9-aws-deploy/implementation.md` — its placeholder table's "예시" column holds
  the live account ID; replace with `<ACCOUNT_ID>`.
- `infra/variables.tf`'s `github_repo_immutable` default (`omottomo@248242903/llm-wiki@1298234217`)
  **stays**. Owner and repo IDs are public GitHub metadata and the owner ID is already visible in
  the noreply email.
- Repo Actions **variables** become **secrets** (`AWS_DEPLOY_ROLE_ARN`, `SITE_BUCKET`,
  `CF_DISTRIBUTION_ID`). Public repos have public run logs and `vars.*` are not masked, so
  `aws s3 sync … s3://llm-wiki-site-<account-id>` would print the account ID on every deploy.

### Licensing — two licenses, because there are two kinds of content

`LICENSE` is **MIT** and covers the code: `scripts/`, `site/`, `infra/`, `.github/`, `.claude/`,
`tests/`. `wiki/` prose is **CC BY 4.0**, declared in `README.md` and in `wiki/index.md`'s
preamble. The split is not ceremony — the wiki pages are syntheses of other people's articles and
talks, and every page already carries its `sources` frontmatter, so an attribution-required
licence is the one that matches what the pages actually are. MIT over the whole repo would
license the syntheses for attribution-free copying.

### The filter-repo pass

Preconditions, re-verified 2026-08-06 (this block supersedes the first planning pass — three of
its claims had already gone stale):

- `git-filter-repo` is **not installed** (`command -v` empty) and neither is `pip`
  (`python3 -m pip` → *No module named pip*). `uv` is present, so the install is
  `uv tool install git-filter-repo`. T07 cannot start without it.
- `gh`'s token already carries `repo` and `workflow`, which is everything T08 needs (rename,
  create, ruleset, secrets). No scope change required.
- `git config user.email` is **already** `248242903+omottomo@users.noreply.github.com` in
  `.git/config`, with no global fallback. The first planning pass recorded `whddlsk123@naver.com`
  here; that is no longer true. A rewrite corrects the past only, so the address the *next* commit
  will carry still matters — T07 therefore **asserts** it rather than setting it, and T09 still
  checks the newest commit from the fresh clone.
- `origin` is SSH (`git@github.com:…`) and there is no credential helper, so pushes ride the
  existing SSH key while `gh` uses its https token for the API. T08 must set the new remote in
  SSH form for the same reason.
- **AWS credentials are absent** (`aws sts get-caller-identity` → `NoCredentials`). T04's real
  `terraform init -backend-config` / `plan` check and T08's deploy-run check both need a login
  first; that is a human step, not an agent one.

The rewrite runs on a **fresh single-branch clone of `main`**, not on the working tree:

```bash
git clone --no-local --single-branch --branch main file:///home/tomo/llm-wiki /tmp/.../llm-wiki-rewrite
```

`main` already contains every merged branch's work, and the 8 stale local plus 30 stale
`origin/*` branches are simply not fetched — there is no list to enumerate and keep current, and
the working tree is never touched by filter-repo. (The first pass named eight branches to delete
by hand; that list was already a partial subset of what exists.)

One `git filter-repo` invocation over that clone:

- `--path raw/ --invert-paths` — paths are repo-relative, so the synthetic
  `tests/fixtures/*/raw/*.md` files are untouched. Verify that explicitly; `test_lint_wiki.py`
  depends on them.
- `--prune-empty=never` — **8 commits touch only `raw/`** and would otherwise be dropped, which
  makes "did the rewrite lose history?" unanswerable by a count. Keeping them empty makes the
  check a one-liner: the post-rewrite count equals the pre-rewrite count exactly.
- `--mailmap` — both real addresses map to `omottomo <248242903+omottomo@users.noreply.github.com>`.
- `--replace-text` — `<ACCOUNT_ID>==><ACCOUNT_ID>`.

Commit counts are **captured, not hardcoded**. `main` holds 232 commits today and T02–T06 add
more before the rewrite runs, so every acceptance check compares against a number recorded
immediately before the pass.

### The portfolio entry (T10, separate repo)

`~/omottomo.github.io` is an Astro site; projects live in `site-v2/src/data/projects.ts` as an
array of `{title, meta, problem, approach, result, tech, links?}`. The entry is appended to that
array — `links` is already in the interface and no entry uses it yet, so llm-wiki is its first
consumer (public repo + `omotomo-llm-wiki.com`).

One thing must be amended rather than ignored: the file's header comment reads *"Experience의 주요
성과 6개와 1:1 대응한다"*, and appending a personal side project breaks that invariant. The comment
is updated to say the array holds the six work outcomes **plus** personal projects. The guardrail
comment above it (no customer/product/chipset proper nouns) is unaffected — nothing in llm-wiki is
work material.

## Ordering constraint

T01 (backups) gates T07 (rewrite) and T08 (publish), and every content task (T02–T06) lands
**before** T07 so the rewritten history is already the clean, publishable tree. Doing T02–T06
after the rewrite would mean the new repo's first commits still describe a world where `raw/` is
tracked and the repo must stay private.

## Verification

```bash
# after T02–T06, before the rewrite
python3 scripts/lint_wiki.py && python3 scripts/test_lint_wiki.py
python3 site/build.py && python3 site/test_build_site.py && python3 scripts/verify_site.py
terraform -chdir=infra fmt -check -recursive
terraform -chdir=infra init -backend=false && terraform -chdir=infra validate
mv raw ../raw.hold && python3 scripts/lint_wiki.py; mv ../raw.hold raw   # the raw-less path CI will take

# immediately BEFORE the rewrite, from the fresh clone — capture the baseline
git rev-list --count main                                                  # N (232 + T02–T06)

# after T07, on the rewritten history
git rev-list --count main                                                  # == N, thanks to --prune-empty=never
git rev-list --all --objects | grep -c ' raw/'                            # 0
git log --all --format='%ae %ce' | tr ' ' '\n' | sort -u                   # noreply only
git rev-list --all | while read c; do git grep -l <ACCOUNT_ID> $c; done    # empty
git ls-files tests/fixtures | grep -c '/raw/'                             # unchanged — fixtures survived

# after T08–T09, from a scratch clone of the public URL
gh repo view omottomo/llm-wiki --json visibility,isPrivate
gh api repos/omottomo/llm-wiki/rulesets
gh run list --workflow verify.yml --limit 3
```

End to end (T09): clone the public URL into the scratch directory, confirm no `raw/` directory
exists, run the full §2.3 matrix there, then open a throwaway PR and confirm `verify` and `lint`
report on it and that the new ruleset blocks a merge while they are red.

## Risks

- **Irreversible.** T07 rewrites every SHA and T08 publishes. T01's mirror bundle is the only way
  back, which is why it is a hard precondition for both.
- **Any other clone of this repo is orphaned** by the rewrite and must be re-cloned.
- `raw/` stops being backed up by the main repo's history. If the nested repo's remote is not
  pushed after an ingest, a disk loss takes the sources with it and the `raw ↔ sources` parity
  rule becomes unverifiable. `wiki-content.md`'s ingest workflow gains a line about pushing it.
- The third-party content survives in the **archive** repo, and stays safe only as long as that
  repo stays private. Never flip it.

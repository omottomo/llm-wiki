# phase-11-ci-deploy-gate — make verify actually gate deploy

## Problem

`.github/workflows/verify-site.yml` and `.github/workflows/deploy-site.yml` both trigger on
`push: branches: [main]`. A single merge starts **both workflows at once**; neither waits on the
other. There is no ordering at all.

Deploy does gate itself: `deploy-site.yml:40-43` runs `test_build_site.py` + `verify_site.py`
inline right before the S3 sync, so a broken build or a `raw/` leak genuinely blocks publishing.
**But lint is not in that gate.** `lint_wiki.py` and `test_lint_wiki.py` live only in the `lint`
job of `verify-site.yml`. Consequences:

- A lint violation reddens CI while **the site still deploys**.
- The gate logic is duplicated across two files (`test_build_site.py` + `verify_site.py` in both).
- The deploy job builds the site three times: `build.py` → `npx pagefind` → `test_build_site.py`,
  which itself shells out to `build.py` (`site/test_build_site.py:19-23`) and runs pagefind again
  (`:162-172`).

## Goal

`deploy` runs only after both `verify` and `lint` pass. Use GitHub's native job dependency
(`needs:`) rather than `workflow_run`, and drop the duplicated work.

## Why `needs:` and not `workflow_run`

`workflow_run` keeps the two files separate but carries real footguns: it resolves the workflow
file from the **default branch** only, requires an explicit
`if: github.event.workflow_run.conclusion == 'success'` (it fires on failure too), ignores
`paths:` filters entirely, needs a manually pinned `ref` at checkout, and adds a second
queue-and-start latency. A single workflow with `needs:` is one file, one run, and no special
cases.

## Preconditions verified before planning

- **OIDC does not pin the workflow file.** The trust condition in `infra/iam-deploy.tf:22-29` is
  `sub = repo:<owner>/<repo>:ref:refs/heads/main` only — no `job_workflow_ref`, no `environment`.
  Merging or renaming the workflow leaves `AssumeRoleWithWebIdentity` working.
  (`iam-deploy.tf:59`'s `name = "deploy-site"` is an inline IAM policy name and is unrelated.)
- **Branch-protection required checks key on job names**, not the workflow filename, so the job
  names `verify` / `lint` / `deploy` must be preserved — the filename may change freely.

## Design

### One file

`git mv .github/workflows/verify-site.yml .github/workflows/site.yml`. The file no longer only
verifies; it deploys to a production S3 bucket, and the name should say so
(`name: Verify & deploy site`). Only the self-reference inside `on.push.paths` changes; the other
path entries stay. Deploy now also fires on `tests/**` and `.gitignore` changes — harmless, since
the build output is identical, so the S3 sync is a no-op and `/*` counts as one invalidation path.

`.github/workflows/deploy-site.yml` is deleted. This must land in the **same commit** as the
merge: if the two steps split, `main` briefly carries two live deploy paths and double-deploys.

### Three jobs

```yaml
permissions:
  contents: read          # workflow level

jobs:
  verify:                 # unchanged — test_build_site.py + verify_site.py
  lint:                   # unchanged — lint_wiki.py + test_lint_wiki.py
  deploy:
    needs: [verify, lint] # the entire ordering mechanism
    permissions:
      id-token: write     # OIDC
      contents: read      # checkout
    concurrency:          # moved from workflow level to job level, so that
      group: deploy-site  # verify and lint are not serialized along with it
      cancel-in-progress: false
```

The deploy steps are `deploy-site.yml:24-81` carried over with exactly two changes:

- **Drop `python3 site/test_build_site.py`.** The `verify` job already ran it, and inside deploy
  it rebuilds the whole site a second time for nothing.
- **Keep `python3 scripts/verify_site.py` inline.** This is deliberate redundancy, not an
  oversight: the `verify` job audited a *different* `dist/` on a *different* runner, whereas this
  step audits the exact tree about to be uploaded to a public bucket. The `raw/` boundary
  (`docs/rules/site-code.md` §2.1) is non-negotiable, so the belt-and-suspenders stays.

Both `aws s3 sync` steps (the content-hash whitelist and its exact complement) and the CloudFront
invalidation move over **verbatim, comments included** — §2.4's Pagefind cache rule is encoded in
those filters.

### Version alignment

Deploy used `checkout@v4` / `setup-node@v4` / `setup-python@v5`; verify already uses
`checkout@v7` / `setup-node@v6` / `setup-python@v6`. Unify on the newer set. `python-version` was
`"3"` in verify and `"3.12"` in deploy, so verification and deployment could run on different
interpreters; pin all three jobs to `"3.12"` since deploy is the production path.

## Out of scope

Per the standing §2.4 rule, CI still fires on push to `main`, not on pull requests. `needs:`
blocks the deploy but **does not stop a broken commit from landing on `main`.** That is a separate
change — add `pull_request:` to `on:` and `if: github.event_name == 'push'` to `deploy` — and it
is not part of this phase.

## Verification

Local gate before pushing (§2.3 matrix, all exit `0`):

```bash
python3 scripts/lint_wiki.py
python3 scripts/test_lint_wiki.py
python3 site/build.py
python3 site/test_build_site.py
python3 scripts/verify_site.py
git check-ignore site/dist
```

Plus a YAML/workflow parse: `actionlint .github/workflows/site.yml`, or
`python3 -c "import yaml; yaml.safe_load(open('.github/workflows/site.yml'))"`.

After the merge to `main` (T02), watch the first run — §2.4: a gate nobody watches is not a gate,
and this repo has already shipped a check that stayed red for two days unnoticed.
`gh run view <id> --json jobs` must show `deploy.startedAt` later than both `verify` and `lint`
completing, and the OIDC step succeeding despite the file move.

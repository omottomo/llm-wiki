# phase-13-pr-gate-and-infra-ci — move the site gate pre-merge, put infra under CI

## Problem

phase-11 (#23) fixed one thing: `deploy: needs: [verify, lint]` means a lint violation can no
longer ship. Two problems remain.

**The gate still runs after the merge.** `site.yml` triggers only on `push: branches: [main]`, so
a PR shows zero checks. A broken commit reddens CI only once it is already on `main` — and since
phase-11 that costs more, not less: when `lint` fails, `deploy` is skipped, so **the live site
freezes at the previous commit**, and every later merge stays unpublished until someone fixes the
violation. The failure mode moved from "bad content published" to "nothing publishes", which is
the right trade but makes the missing pre-merge gate more expensive.

**`infra/` is verified by nothing.** `paths` has no `infra/**` entry and there is no Terraform
workflow. phase-9 moved S3, CloudFront, ACM, Route53, IAM and the OIDC provider into Terraform, so
the code that defines the deploy role's own permissions reaches `main` unchecked.

## Approach, and the one correction to the obvious shape

The requested shape — validate on the PR, validate infra when it changes, then deploy — is right,
with one correction. "Split `verify` into a PR-only workflow" breaks the chain: if `verify` does
not run on the push event, `deploy`'s `needs` has nothing to resolve, and **GitHub Actions skips a
job whose `needs` target was skipped**, so `deploy` would never run again. The working shape is
not a split but a shared trigger:

- `verify` and `lint` run on **both** `pull_request` and `push`.
- `deploy` is held back by `if: github.event_name == 'push'`.

Observable behaviour is what was asked for (checks before the merge, publish only from `main`)
while the `needs` chain stays intact.

### Revised 2026-08-03 (T07 supersedes T01): split by file after all

The paragraph above is still correct about *why* an `if:` on `verify` cannot work — but its
conclusion, "not a split but a shared trigger", was overturned. The shape shipped is a split into
two files:

- `verify.yml` — `pull_request` only. Holds `verify` and `lint`, moved verbatim.
- `deploy.yml` — `push` to `main` only. Holds a `lint` job and `deploy` with `needs: [lint]`.

Splitting by **file** avoids the skip cascade that splitting by `if:` causes, because there is no
cross-workflow `needs` left to resolve — each file's trigger decides everything. What was traded
away is the post-merge `test_build_site.py` run: two PRs that are individually green but break in
combination now surface at `deploy.yml`'s `lint` or `build.py` step rather than before the merge.

`deploy.yml` keeps its own `lint` job because **branch protection is unavailable on this repo** —
verified 2026-08-03, both `/repos/:owner/:repo/branches/main/protection` and the newer
`/repos/:owner/:repo/rulesets` return `403 Upgrade to GitHub Pro or make this repository public`
(private repo, `User` free plan), and going public is barred by the `raw/` boundary (§2.1). So a
red PR is still mergeable, and that job is the last machine gate before publishing.

## Deliberate split: infra does not gate the site deploy

Infra validation lives in its own workflow (`infra.yml`, `paths: [infra/**]`) so it runs only when
infra changes. The consequence is explicit: **`infra.yml` cannot gate `deploy`** — cross-workflow
ordering is exactly the `workflow_run` footgun phase-11 removed. That is defensible rather than a
compromise: the site deploy is an `aws s3 sync` that never executes Terraform, so blocking wiki
publishing on a `.tf` typo would be a false coupling. **The cost, stated plainly: nothing prevents
a broken `.tf` from reaching `main`** — a PR shows it red, and nothing enforces that.

## Why a second IAM role

Validation goes as deep as `terraform plan`, which needs the real S3 backend and therefore AWS
credentials. The existing role cannot be reused: `infra/iam-deploy.tf:22-29` pins
`sub = repo:<owner>/<repo>:ref:refs/heads/main`, while a `pull_request` event's OIDC subject claim
is **`repo:<owner>/<repo>:pull_request`**. (That is the `sub` claim, not `github.ref` — the two
differ, and it is the claim that goes into the trust policy.)

The new role is read-only and **scoped by service**, not the AWS managed `ReadOnlyAccess` policy,
which would grant account-wide read to anyone who can open a PR. `plan` runs with `-lock=false`,
so the role needs no write permission at all — the S3-native state lock
(`use_lockfile = true`, `infra/versions.tf`) would otherwise demand `s3:PutObject`.

## Preconditions verified before planning

- `infra/versions.tf:11-16` declares `backend "s3"`, so a credential-free `validate` must use
  `terraform init -backend=false`; `plan` needs the real backend and thus the role.
- `infra/.terraform.lock.hcl` is tracked (`git ls-files`), so provider versions reproduce in CI.
- Local Terraform v1.15.8: `terraform -chdir=infra fmt -check -recursive` is already clean, so the
  format gate will not be red on its first run.
- `.gitignore` covers `infra/.terraform/`, `*.tfstate*` and `*.sw[op]`. `infra/terraform.tfvars`
  is tracked and holds only the domain and bucket name — no secret.
- Branch protection is still unavailable (private repo on the free plan; the API returns 403
  `Upgrade to GitHub Pro or make this repository public`), so **PR checks are advisory: a red PR
  can still be merged.** This phase does not close that. Re-checked 2026-08-03 against the *newer*
  endpoint as well — `gh api repos/:owner/:repo/rulesets` returns the same 403, so rulesets are not
  a way around it either.

## Design

### `.github/workflows/verify.yml` + `.github/workflows/deploy.yml`

`site.yml` is deleted and replaced by two files. Both carry the same `paths` list — Actions has no
YAML anchors, so it is duplicated verbatim; edit one, edit the other. The list's old
`.github/workflows/site.yml` entry becomes both new filenames.

```yaml
# verify.yml
on:
  pull_request:
    branches: [main]
    paths: [...]

concurrency:
  group: verify-${{ github.ref }}
  cancel-in-progress: true      # safe unconditionally — this file never runs on main

jobs:
  verify:                       # moved verbatim from site.yml
  lint:                         # moved verbatim from site.yml
```

```yaml
# deploy.yml
on:
  push:
    branches: [main]
    paths: [...]                # identical list

jobs:
  lint:                         # last machine gate — see below
  deploy:
    needs: [lint]               # same file, so needs resolves normally
    concurrency: {group: deploy-site, cancel-in-progress: false}
```

No job in either file carries an `if:`. The trigger is the guard, and there is no cross-workflow
`needs` to break. The OIDC trust pinning `refs/heads/main` would also stop a PR deploy, but that is
a second line of defence and must not be relied on.

`deploy.yml` keeps a `lint` job because a red PR is still mergeable here (see the revision note
above). `build.py` inside `deploy` already exits 1 on a broken internal link and `verify_site.py`
audits the exact tree about to be uploaded, so link integrity and the `raw/` boundary gate the
deploy on their own; the `lint` job covers what those two cannot see — frontmatter, index entries,
orphans, tag hygiene. It needs no Node and no build, so it costs almost nothing.

`deploy`'s own `concurrency: {group: deploy-site}` serializes deploys against each other; that is a
separate concern from `verify.yml` superseding stale PR runs.

### `infra/iam-deploy.tf` + `infra/outputs.tf`

New `plan_trust` document (same `aud` condition as `deploy_trust`, `sub` set to the
`:pull_request` forms of both the immutable and legacy repo identifiers), a new `llm-wiki-plan`
role, and an inline policy with read actions only: `s3:GetObject`/`s3:ListBucket` on the tfstate
bucket, `s3:Get*`/`s3:List*` on the site bucket, and `Get*`/`List*`/`Describe*` for CloudFront,
ACM, Route53 and IAM. `outputs.tf` exposes `plan_role_arn`. The existing deploy role, its trust
document and its policy are untouched.

### `.github/workflows/infra.yml` (new)

`pull_request` on `branches: [main]`, `paths: [infra/**, .github/workflows/infra.yml]`. One
`terraform` job: checkout, `hashicorp/setup-terraform@v3` pinned to 1.15.8 with
`terraform_wrapper: false`, `fmt -check -recursive` **before** any AWS step (a formatting error has
no reason to touch AWS), `aws-actions/configure-aws-credentials@v5` (v4 targets the deprecated
Node 20 and warned on the phase-11 run), `init`, `validate`, `plan -lock=false -no-color`, and the
plan written into `$GITHUB_STEP_SUMMARY`.

No third-party PR-comment action: plan output carries resource attributes read from state, and the
run summary is already visible to collaborators without adding a dependency.

## Verification

```bash
python3 scripts/lint_wiki.py && python3 scripts/test_lint_wiki.py
python3 site/build.py && python3 site/test_build_site.py && python3 scripts/verify_site.py
terraform -chdir=infra fmt -check -recursive
terraform -chdir=infra init -backend=false && terraform -chdir=infra validate
git check-ignore site/dist
# pyyaml is not installed locally; ruby ships with macOS and parses the same YAML.
ruby -ryaml -e 'YAML.load_file(".github/workflows/verify.yml"); YAML.load_file(".github/workflows/deploy.yml"); YAML.load_file(".github/workflows/infra.yml")'
```

End to end (T05): open a PR touching both `wiki/` and `infra/`. On the `verify.yml` PR run, `verify`
and `lint` must be green; on the `infra.yml` PR run, the plan must appear in the run summary;
`deploy.yml` must show **no run at all** for that head SHA. After the merge, `deploy.yml` must run on
the push with `deploy` starting after `lint` completes, and neither `verify.yml` nor `infra.yml` may
run.

```bash
gh run list --workflow verify.yml --limit 3
gh run list --workflow deploy.yml --limit 3
gh run view <pr-run-id>   --json jobs --jq '.jobs[] | "\(.name) \(.conclusion)"'
gh run view <push-run-id> --json jobs --jq '.jobs[] | "\(.name) \(.conclusion) \(.startedAt)"'
```

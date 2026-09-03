# phase-17-infra-ci — finish the infra CI half that phase-13 left unbuilt

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make a broken `infra/*.tf` visible on the pull request that introduces it, and blocked from `main`, by shipping the `llm-wiki-plan` role, the `Verify infra` workflow, and the ruleset entry that makes its check required.

**Architecture:** phase-13 designed a read-only OIDC role for `terraform plan` on pull requests and wrote its Terraform, but never ran `apply` and never added the workflow. This phase applies that role, adds `.github/workflows/infra.yml` as one always-reporting `infra` job (format + `validate` unconditionally; `init`/`plan` against the real backend only when the PR actually touched `infra/`), and adds `infra` to the main ruleset's required checks. Two of phase-13's premises changed underneath it and are corrected here: the repo is public with a working ruleset (so the check can be *required*, not merely advisory), and Actions inputs are secrets rather than variables (so the role ARN and the state-bucket name are `secrets.*`).

**Tech Stack:** GitHub Actions, Terraform 1.15.8 (`hashicorp/setup-terraform@v3`), AWS OIDC federation (`aws-actions/configure-aws-credentials@v5`), `gh` CLI (preinstalled on the runner).

**Spec:** `docs/tasks/phase-13-pr-gate-and-infra-ci/plan.md` — sections "Why a second IAM role", "Deliberate split: infra does not gate the site deploy", and the `infra.yml` design. This plan supersedes that PRD's T03–T06; T01/T02/T07 are already done. Read the phase-13 plan for the *why*; this file carries the *what*.

## Global Constraints

- Terraform version pinned to **1.15.8** everywhere (local and CI) — matches `infra/.terraform.lock.hcl` (`hashicorp/aws 6.55.0`).
- AWS region **ap-northeast-2**, except the `us_east_1` aliased provider used by ACM.
- `aws-actions/configure-aws-credentials@**v5**` — v4 targets the deprecated Node 20 and warns.
- `actions/checkout@v7`, `actions/setup-python@v6`, `actions/setup-node@v6`, Python `"3.12"` — keep every workflow on the same pins.
- **Required status checks key on the job name.** The new job must be named exactly `infra`, and the name may never change without updating the ruleset in the same pass.
- **A required check plus a `paths:` filter is a merge deadlock** (§2.4, phase-15). Any workflow whose check is required must run **unfiltered**.
- **No account IDs, key IDs, or bucket names in tracked files.** They travel as `secrets.*`. phase-15 scrubbed the account ID out of the history; do not put it back.
- `terraform plan` in CI runs with `-lock=false` — the S3 native lock (`use_lockfile = true`, `infra/versions.tf`) would otherwise demand `s3:PutObject`, which the read-only role deliberately lacks.
- No third-party PR-comment action. Plan output goes to `$GITHUB_STEP_SUMMARY`.
- Verification order for anything touching the site (§2.3 of `docs/rules/site-code.md`): `lint_wiki.py` → `build.py` → `verify_site.py`.

---

## Context an implementer needs before Task 1

**What already exists.** `infra/iam-deploy.tf` defines `aws_iam_role.plan` (`llm-wiki-plan`), its trust document `plan_trust` (pinned to the `:pull_request` subject claim in both immutable and legacy forms), and `aws_iam_role_policy.plan` (`plan-infra`). `infra/outputs.tf` exposes `plan_role_arn`. None of it has ever been applied: `terraform state list` has no `aws_iam_role.plan`, and `aws iam get-role --role-name llm-wiki-plan` returns `NoSuchEntity`. **This is why `terraform plan` currently reports `2 to add, 0 to change, 0 to destroy`** — that diff is phase-13's unapplied code, not drift.

**What does not exist.** `.github/workflows/infra.yml` has never existed on any branch. There is no `AWS_PLAN_ROLE_ARN` secret or variable.

**Two premises from phase-13 that are now false.**

1. phase-13 recorded "branch protection is unavailable on this repo — both `/branches/main/protection` and `/rulesets` return 403 `Upgrade to GitHub Pro or make this repository public`", and concluded PR checks are advisory. phase-15 took the repo public and created ruleset `20497822` ("main protection"), which today requires the checks `verify` and `lint`. So an infra check **can** be required, and Task 3 makes it so. This is the single biggest change in value between phase-13's design and this one: phase-13 could only make a broken `.tf` *visible*; this phase can make it *blocking*.
2. phase-13's T03/T04 said `gh variable set AWS_PLAN_ROLE_ARN` and `${{ vars.AWS_PLAN_ROLE_ARN }}`. phase-15 converted all three Actions inputs to **secrets**, because a public repo's run logs do not mask `vars.*` and the bucket names carry the account ID. A role ARN carries the account ID too, so it is a **secret** here.

**Two things phase-13 could not have known, because phase-15 introduced them.**

3. `infra/terraform.tfvars` is now **gitignored**. `infra/variables.tf` declares `domain`, `site_bucket_name` and `tfstate_bucket_name` with no defaults, so a CI `terraform plan` has no values for them and fails with `No value for required variable`. Task 2 supplies them: the two bucket names as `TF_VAR_*` from secrets, and `domain` gains a default in `variables.tf` (the domain is on the public certificate and in public DNS — it was never one of the scrubbed values).
4. `infra/backend.hcl` is **gitignored** as well, and `infra/versions.tf`'s `backend "s3"` block declares no `bucket`. A CI `terraform init` must pass the bucket explicitly: `-backend-config="bucket=$TFSTATE_BUCKET"`.

**One latent permission gap.** `plan_permissions` grants `cloudfront:Get*` and `cloudfront:List*`. Refreshing `aws_cloudfront_function.rewrite_index` also calls **`cloudfront:DescribeFunction`**, which matches neither prefix, so the first CI plan would die on `AccessDenied`. Task 1 adds `cloudfront:Describe*` before applying, alongside `acm:Describe*` which is already there for the same reason.

---

## File structure

| File | Change | Responsibility |
|---|---|---|
| `infra/iam-deploy.tf` | Modify (`plan_permissions`, `ReadInfraConfig` statement) | Add `cloudfront:Describe*` so a plan can refresh the CloudFront Function |
| `infra/variables.tf` | Modify (`domain`) | Give `domain` a default so CI needs only the two bucket names |
| `.github/workflows/infra.yml` | Create | One `infra` job: fmt + validate always, `plan` when the PR touched `infra/` |
| `docs/rules/site-code.md` | Modify (§2 heading, §2.2, §2.4) | Record the accumulated rules; retire two stale claims |
| `docs/log.md` | Append | One Korean `site` line at close-out |
| `docs/index.md` | Modify | Register the phase directory |

No `prd.json` — this plan is the task list.

---

## Task 1: Apply the read-only plan role and register its two secrets

**Files:**
- Modify: `infra/iam-deploy.tf` (the `ReadInfraConfig` statement inside `data "aws_iam_policy_document" "plan_permissions"`)
- No test file — the deliverable is an AWS resource plus two repo secrets; Task 4 is its integration test.

**Interfaces:**
- Consumes: nothing.
- Produces: the IAM role `llm-wiki-plan` in the account; repo secrets **`AWS_PLAN_ROLE_ARN`** (from `terraform output -raw plan_role_arn`) and **`TFSTATE_BUCKET`** (the state bucket name, identical to `bucket` in `infra/backend.hcl` and to `tfstate_bucket_name` in `infra/terraform.tfvars`). Task 2's workflow reads both by exactly these names.

- [ ] **Step 1: Add the missing CloudFront action**

In `infra/iam-deploy.tf`, inside `data "aws_iam_policy_document" "plan_permissions"`, the `ReadInfraConfig` statement's `actions` list gains one entry:

```hcl
  statement {
    sid = "ReadInfraConfig"
    actions = [
      "cloudfront:Get*",
      "cloudfront:List*",
      # DescribeFunction matches neither Get* nor List*; refreshing
      # aws_cloudfront_function.rewrite_index calls it, so a plan without this
      # dies on AccessDenied.
      "cloudfront:Describe*",
      "acm:Describe*",
      "acm:List*",
      "route53:Get*",
      "route53:List*",
      "iam:Get*",
      "iam:List*",
    ]
    resources = ["*"]
  }
```

- [ ] **Step 2: Format and validate without touching AWS**

```bash
cd /home/tomo/projects/llm-wiki
terraform -chdir=infra fmt -check -recursive
terraform -chdir=infra validate
```

Expected: `fmt` prints nothing and exits `0`; `validate` prints `Success! The configuration is valid.`

> If `validate` complains that the backend is not initialized, run `terraform -chdir=infra init -backend-config=infra/backend.hcl` first. Do **not** run `init -backend=false` in this working copy — `infra/.terraform/` already holds a cached S3 backend and the credential-free init fails against it (§2.4 records this).

- [ ] **Step 3: Read the plan before applying**

```bash
export AWS_PROFILE=devops
terraform -chdir=infra plan
```

Expected, exactly:

```
Plan: 2 to add, 0 to change, 0 to destroy.
```

with the two additions being `aws_iam_role.plan` and `aws_iam_role_policy.plan`.

**Stop and do not apply** if the output reports anything under `to change` or `to destroy`, or names `aws_iam_role.deploy`, `aws_iam_role_policy.deploy`, `aws_s3_bucket.site`, `aws_cloudfront_distribution.site` or any `aws_route53_record`. Those are live and this task must not move them.

- [ ] **Step 4: Apply**

```bash
terraform -chdir=infra apply
```

Type `yes` at the prompt. Expected: `Apply complete! Resources: 2 added, 0 changed, 0 destroyed.`

- [ ] **Step 5: Verify the role exists and the diff is gone**

```bash
aws iam get-role --role-name llm-wiki-plan --query 'Role.RoleName' --output text
aws iam get-role-policy --role-name llm-wiki-plan --policy-name plan-infra \
  --query 'PolicyDocument.Statement[?Sid==`ReadInfraConfig`].Action' --output json
terraform -chdir=infra plan
```

Expected: `llm-wiki-plan`; an action list containing `cloudfront:Describe*`; and `No changes. Your infrastructure matches the configuration.`

- [ ] **Step 6: Register both secrets**

```bash
gh secret set AWS_PLAN_ROLE_ARN --body "$(terraform -chdir=infra output -raw plan_role_arn)"
gh secret set TFSTATE_BUCKET    --body "$(grep -E '^bucket' infra/backend.hcl | cut -d'"' -f2)"
gh secret list
```

Expected: `gh secret list` shows five entries — `AWS_DEPLOY_ROLE_ARN`, `AWS_PLAN_ROLE_ARN`, `CF_DISTRIBUTION_ID`, `SITE_BUCKET`, `TFSTATE_BUCKET`.

> Secrets, not variables. A public repo's run logs mask `secrets.*` and do **not** mask `vars.*`, and both of these values contain the AWS account ID that phase-15 removed from the history.

- [ ] **Step 7: Commit**

```bash
git switch -c phase-17-infra-ci
git add infra/iam-deploy.tf
git commit -m "fix(infra): let the plan role describe the CloudFront Function"
```

---

## Task 2: Add the `Verify infra` workflow

**Files:**
- Create: `.github/workflows/infra.yml`
- Modify: `infra/variables.tf` (the `domain` variable)

**Interfaces:**
- Consumes: secrets `AWS_PLAN_ROLE_ARN`, `TFSTATE_BUCKET`, `SITE_BUCKET` (the last already exists, created in phase-15).
- Produces: a status check whose context is exactly **`infra`**. Task 3 adds that string to the ruleset.

- [ ] **Step 1: Give `domain` a default**

CI has no `terraform.tfvars` (gitignored since phase-15), and `plan` fails on any variable without a value. Two of the three come from secrets because they embed the account ID; the domain does not, and it is already public in DNS and on the ACM certificate.

In `infra/variables.tf`:

```hcl
variable "domain" {
  type = string
  # CI has no terraform.tfvars (gitignored), so plan needs a value from
  # somewhere. Unlike the bucket names this one carries no account ID and is
  # already public in DNS and on the ACM certificate, so it lives here rather
  # than in a secret. Local runs still take the value from terraform.tfvars.
  default = "omotomo-llm-wiki.com"
}
```

- [ ] **Step 2: Confirm the default did not change the plan**

```bash
export AWS_PROFILE=devops
terraform -chdir=infra plan
```

Expected: `No changes. Your infrastructure matches the configuration.` — `terraform.tfvars` still sets the same value locally, so the default is inert here and only takes effect in CI.

- [ ] **Step 3: Write the workflow**

Create `.github/workflows/infra.yml`:

```yaml
name: Verify infra (pull requests)

# No `paths:` filter, deliberately — same reason verify.yml has none. The main
# ruleset REQUIRES this job's check, and a workflow filtered out by `paths:`
# reports nothing at all rather than reporting success, so a PR touching only
# wiki/ would sit at mergeStateStatus=BLOCKED forever waiting on a run that
# never starts.
#
# Running unfiltered does NOT mean touching AWS on every pull request. The
# format and validate steps need no credentials and always run; the role is
# assumed and `plan` executed only when the PR actually changed infra/. That
# keeps a wiki-only PR from depending on AWS being reachable, while still
# reporting the check every time.
on:
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: infra-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # The job name is the status-check context the ruleset requires. Renaming it
  # silently breaks the gate — update the ruleset in the same commit if you do.
  infra:
    runs-on: ubuntu-latest
    permissions:
      id-token: write       # OIDC token for the plan role
      contents: read
      pull-requests: read   # `gh pr view --json files` in the change probe
    steps:
      - uses: actions/checkout@v7

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.15.8
          terraform_wrapper: false

      # Before any AWS step on purpose: a formatting error has no reason to
      # reach for credentials.
      - name: Format check
        run: terraform -chdir=infra fmt -check -recursive

      # -backend=false keeps this credential-free. The runner always checks out
      # fresh, so there is no cached backend to conflict with (locally there is
      # — see site-code.md §2.4).
      - name: Validate
        run: |
          terraform -chdir=infra init -backend=false
          terraform -chdir=infra validate

      - name: Did this PR touch infra/?
        id: probe
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          if gh pr view "${{ github.event.pull_request.number }}" \
               --repo "$GITHUB_REPOSITORY" --json files --jq '.files[].path' \
               | grep -q '^infra/'; then
            echo "changed=true" >> "$GITHUB_OUTPUT"
          else
            echo "changed=false" >> "$GITHUB_OUTPUT"
            echo "No infra/ changes in this PR — skipping terraform plan." >> "$GITHUB_STEP_SUMMARY"
          fi

      - name: Configure AWS credentials (OIDC, read-only plan role)
        if: steps.probe.outputs.changed == 'true'
        uses: aws-actions/configure-aws-credentials@v5
        with:
          role-to-assume: ${{ secrets.AWS_PLAN_ROLE_ARN }}
          aws-region: ap-northeast-2

      # -reconfigure because the validate step above already initialised this
      # directory with -backend=false. The bucket is a partial config: the
      # backend block in versions.tf omits it, since the name carries the AWS
      # account ID and this repo is public.
      - name: Init with the real backend
        if: steps.probe.outputs.changed == 'true'
        run: |
          terraform -chdir=infra init -reconfigure \
            -backend-config="bucket=${{ secrets.TFSTATE_BUCKET }}"

      # -lock=false is required, not an optimisation: the S3 native lock
      # (use_lockfile = true in versions.tf) would demand s3:PutObject, which
      # the read-only plan role deliberately does not have.
      - name: Plan
        if: steps.probe.outputs.changed == 'true'
        env:
          TF_VAR_site_bucket_name: ${{ secrets.SITE_BUCKET }}
          TF_VAR_tfstate_bucket_name: ${{ secrets.TFSTATE_BUCKET }}
        run: |
          terraform -chdir=infra plan -lock=false -no-color | tee /tmp/plan.txt

      # The run summary is visible to collaborators already, so no third-party
      # PR-comment action is added. Plan output carries resource attributes read
      # from state — keep it in the summary, not in a public comment.
      - name: Publish the plan in the run summary
        if: steps.probe.outputs.changed == 'true'
        run: |
          {
            echo '### terraform plan'
            echo '```'
            cat /tmp/plan.txt
            echo '```'
          } >> "$GITHUB_STEP_SUMMARY"
```

- [ ] **Step 4: Check the YAML parses**

```bash
python3 -c "import yaml,sys; [yaml.safe_load(open(f)) for f in sys.argv[1:]]; print('ok')" \
  .github/workflows/infra.yml .github/workflows/verify.yml .github/workflows/deploy.yml
```

Expected: `ok`.

> If `yaml` is not importable, `pip install pyyaml` into a scratch venv, or use `ruby -ryaml -e 'YAML.load_file(".github/workflows/infra.yml")'`.

- [ ] **Step 5: Confirm the job name matches what Task 3 will require**

```bash
python3 -c "import yaml; print(list(yaml.safe_load(open('.github/workflows/infra.yml'))['jobs']))"
```

Expected: `['infra']`. Any other string breaks the ruleset entry added in Task 3.

- [ ] **Step 6: Confirm the site checks are unaffected**

```bash
python3 scripts/lint_wiki.py && python3 site/build.py && python3 scripts/verify_site.py
```

Expected: all three exit `0`.

- [ ] **Step 7: Commit**

```bash
git add .github/workflows/infra.yml infra/variables.tf
git commit -m "ci: verify infra on pull requests with a read-only terraform plan"
```

---

## Task 3: Make the `infra` check required on main

**Files:**
- No repository files. This edits ruleset `20497822` ("main protection") through the GitHub API.

**Interfaces:**
- Consumes: the status-check context `infra` produced by Task 2.
- Produces: a ruleset that blocks a merge until `verify`, `lint` and `infra` all report success.

> Do this **after** Task 2 is pushed and its first run has been observed green (Task 4, Step 2). Requiring a check that no workflow reports wedges every open pull request — that is the phase-15 deadlock in a different costume.

- [ ] **Step 1: Record the current ruleset, so it can be restored**

```bash
gh api repos/omottomo/llm-wiki/rulesets/20497822 > /tmp/ruleset-20497822.before.json
gh api repos/omottomo/llm-wiki/rulesets/20497822 \
  --jq '.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context'
```

Expected: `verify` and `lint`, one per line.

- [ ] **Step 2: Add `infra` to the required contexts**

```bash
python3 - <<'EOF'
import json

d = json.load(open('/tmp/ruleset-20497822.before.json'))
for rule in d['rules']:
    if rule['type'] == 'required_status_checks':
        checks = rule['parameters']['required_status_checks']
        if not any(c['context'] == 'infra' for c in checks):
            checks.append({'context': 'infra'})

# The PUT accepts only these five keys; id, timestamps and _links are read-only
# and are rejected if echoed back.
body = {k: d[k] for k in ('name', 'target', 'enforcement', 'conditions', 'rules') if k in d}
json.dump(body, open('/tmp/ruleset-20497822.after.json', 'w'), indent=2)
print([c['context'] for r in body['rules']
       if r['type'] == 'required_status_checks'
       for c in r['parameters']['required_status_checks']])
EOF

gh api --method PUT repos/omottomo/llm-wiki/rulesets/20497822 \
  --input /tmp/ruleset-20497822.after.json
```

The `print` is the pre-flight check: it must show `['verify', 'lint', 'infra']` before the `gh api` line runs.

- [ ] **Step 3: Verify**

```bash
gh api repos/omottomo/llm-wiki/rulesets/20497822 \
  --jq '.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context'
```

Expected, in any order: `verify`, `lint`, `infra`.

**Rollback**, if a pull request wedges at `BLOCKED` waiting on a check that never arrives:

```bash
gh api --method PUT repos/omottomo/llm-wiki/rulesets/20497822 \
  --input /tmp/ruleset-20497822.before.json
```

---

## Task 4: Prove both halves on a real pull request

**Files:**
- Test: none in the repo. The subject under test is GitHub's own behaviour, so the test is a real PR.

**Interfaces:**
- Consumes: everything from Tasks 1–3.
- Produces: evidence for the close-out log line in Task 5.

- [ ] **Step 1: Open the pull request**

```bash
git push -u origin phase-17-infra-ci
gh pr create --fill
```

- [ ] **Step 2: Watch the checks, and confirm `plan` actually ran**

This branch changes `infra/` (Tasks 1 and 2 both touched it), so the probe step must take the `true` path.

```bash
gh pr checks --watch
gh run list --workflow infra.yml --limit 1
gh run view "$(gh run list --workflow infra.yml --limit 1 --json databaseId --jq '.[0].databaseId')" \
  --json jobs --jq '.jobs[].steps[] | "\(.name): \(.conclusion)"'
```

Expected: `verify`, `lint` and `infra` all pass; every step of the `infra` job reports `success` and **none reports `skipped`** — including `Plan` and `Publish the plan in the run summary`.

- [ ] **Step 3: Read the plan out of the run summary**

Open the run in a browser (`gh run view --web`) and confirm the summary holds a `### terraform plan` block. Expected content: `No changes. Your infrastructure matches the configuration.` — Task 1 already applied the two resources, and nothing since has changed infrastructure.

If instead the step failed with `AccessDenied`, the plan role is missing a read action for whatever resource the message names. Add its `Get*`/`List*`/`Describe*` prefix to the `ReadInfraConfig` statement in `infra/iam-deploy.tf`, re-run `terraform -chdir=infra apply` locally (Task 1, Step 4), and push again. This is the expected failure mode and is why Task 4 comes before close-out.

- [ ] **Step 4: Confirm deploy did not run for this head SHA**

`deploy.yml` filters on `paths`, and this branch touches only `infra/`, `.github/workflows/` and `docs/`. `.github/workflows/deploy.yml` is in that filter but `infra.yml` is not, so no deploy should start.

```bash
gh run list --workflow deploy.yml --limit 3 --json headSha,createdAt --jq '.[]|"\(.headSha[0:7]) \(.createdAt)"'
git rev-parse --short HEAD
```

Expected: the current head SHA appears in **no** deploy run.

- [ ] **Step 5: Prove the gate actually blocks — the red-run test**

A gate nobody watched go red is not known to work (§2.4, "a red gate is worse than none"). Break the formatting deliberately, on this same PR:

```bash
printf '\n\n  variable  "scratch_phase17"  {  type = string \n default = "x" }\n' >> infra/variables.tf
git commit -am "test: deliberately malformed HCL, reverted in the next commit"
git push
gh pr checks --watch
```

Expected: the `infra` check **fails** at the `Format check` step, and `gh pr view --json mergeStateStatus --jq .mergeStateStatus` returns `BLOCKED`.

- [ ] **Step 6: Revert the deliberate break**

```bash
git revert --no-edit HEAD
git push
gh pr checks --watch
gh pr view --json mergeStateStatus --jq .mergeStateStatus
```

Expected: `infra` green again, `mergeStateStatus` no longer `BLOCKED`.

- [ ] **Step 7: Record the skip path**

The `false` branch of the probe is exercised by the next wiki-only pull request, not by this one. Note in the close-out log line that it is unverified until then, rather than claiming it works.

---

## Task 5: Record the rules, retire the stale claims, close the phase

**Files:**
- Modify: `docs/rules/site-code.md` — §2 heading and lead paragraph, §2.2 deploy bullets, §2.4 (new entries + one retirement)
- Modify: `docs/log.md` (append one line)
- Modify: `docs/index.md` (register the phase)

**Interfaces:**
- Consumes: the observations from Task 4.
- Produces: nothing later tasks read; this is close-out.

- [ ] **Step 1: Retire the stale push-only CI rule**

`docs/rules/site-code.md` line 134 still asserts:

> **The CI gate fires on push to `main`, not on pull requests** (2026-07-13). A leak or a broken build is therefore caught *after* the merge…

phase-13 T07 made that false in August. Replace that bullet with:

```markdown
- **~~The CI gate fires on push to `main`, not on pull requests~~** (2026-07-13, **retired 2026-09-03 by phase-17**). True until phase-13 split `site.yml` into `verify.yml` (`pull_request`) and `deploy.yml` (`push`), and fully false since phase-15's ruleset made `verify` and `lint` required and phase-17 added `infra`. A green PR is now evidence, not a guess. Kept as a marker because the "treat a green PR as unverified" habit it created outlived it.
```

- [ ] **Step 2: Correct the Cloudflare Pages heading**

§2's heading and lead still name Cloudflare Pages as the deploy target. phase-9 moved publishing to S3 + CloudFront and its `docs/index.md` entry has carried "doc update pending at close-out" ever since. Fold it in here.

Change the heading on line 56 from:

```markdown
## 2. Site publishing (build.py → site/dist/ → Cloudflare Pages)
```

to:

```markdown
## 2. Site publishing (build.py → site/dist/ → S3 + CloudFront)
```

In the lead paragraph, replace `Deploy target is **Cloudflare Pages**.` with:

```markdown
Deploy target is **AWS S3 + CloudFront**, provisioned by Terraform in `infra/` and published by
`.github/workflows/deploy.yml` over OIDC (phase-9; the Cloudflare Pages target described in phases
1–7 was never created — see §2.4).
```

In §2.2, replace the `**Deploy (Cloudflare Pages)**` bullet with:

```markdown
- **Deploy (S3 + CloudFront)**: `deploy.yml` builds with `pip install -r site/requirements.txt && python3 site/build.py && npx -y pagefind@1 --site site/dist`, audits the result with `verify_site.py`, then runs two `aws s3 sync` passes (long-cache whitelist / short-cache complement) and one CloudFront invalidation. Credentials are an assumed OIDC role, never a key.
```

Leave the `baseUrl` bullets as they are — they are historical record and §2.4 already says so.

- [ ] **Step 3: Add the phase-17 entries to §2.4**

Append to the accumulated-rules list:

```markdown
- **A required check must run unfiltered, and gating AWS access is a step-level `if:`, not a `paths:` filter** (2026-09-03, phase-17). `infra.yml`'s check is required by the main ruleset, so the workflow cannot carry `paths: [infra/**]` — a filtered-out workflow reports nothing and wedges every PR that misses the filter (§2.4, phase-15). But running unfiltered must not mean assuming an AWS role on every wiki PR: a `gh pr view --json files` probe sets `steps.probe.outputs.changed`, and only the credential steps and `plan` carry `if: steps.probe.outputs.changed == 'true'`. Format and `validate` need no credentials and always run, so the check always reports. The shape to copy for any future required workflow that needs a secret: **unfiltered workflow, conditional steps.**

- **`terraform plan` in CI needs four things this repo deliberately does not track** (2026-09-03, phase-17). phase-15 gitignored `infra/backend.hcl` and `infra/terraform.tfvars` because both carry the AWS account ID, and `infra/versions.tf`'s `backend "s3"` block declares no `bucket` (backend blocks forbid interpolation). A CI plan therefore needs: `-backend-config="bucket=${{ secrets.TFSTATE_BUCKET }}"` on `init`; `TF_VAR_site_bucket_name` and `TF_VAR_tfstate_bucket_name` from secrets on `plan`; and a `default` on `var.domain` in `variables.tf` — the domain is public in DNS and on the ACM certificate, so it is the one value that does not need a secret. All of them are **secrets, not variables**: a public repo's run logs mask `secrets.*` and do not mask `vars.*`.

- **A read-only IAM policy built from `Get*`/`List*` prefixes has holes, and `plan` finds them one at a time** (2026-09-03, phase-17). `cloudfront:DescribeFunction` matches neither prefix, so refreshing `aws_cloudfront_function.rewrite_index` failed the first plan with `AccessDenied` until `cloudfront:Describe*` was added to the `ReadInfraConfig` statement. The `Describe*` verb is not a CloudFront quirk — ACM needed it too, which is why `acm:Describe*` was already in the list. When a plan fails on `AccessDenied`, read the action name out of the message, add its prefix, and **`terraform apply` again** — the policy lives in AWS and editing the `.tf` alone changes nothing.

- **phase-13's "PR checks are advisory" premise died with phase-15** (2026-09-03, phase-17). phase-13 designed `infra.yml` around a repo where branch protection returned 403 on both endpoints, so its stated cost was "nothing prevents a broken `.tf` from reaching `main`". Public repo + ruleset `20497822` removed that constraint, so phase-17 required the `infra` check instead of leaving it advisory. **The lesson is about plans, not CI: a phase left half-finished carries premises that expire.** Re-read the constraints section of any plan older than one phase before executing its remainder.
```

- [ ] **Step 4: Register the phase in `docs/index.md`**

Add `phase-17-infra-ci/` to the `tasks/` tree block (change phase-16's `└──` to `├──`), and add one row to the tasks table naming `plan.md` as the only file, the five tasks, and the outcome.

- [ ] **Step 5: Append the close-out log line**

One Korean `site` line at the end of `docs/log.md`, per `CLAUDE.md` §2. It must record: what phase-13 left unbuilt and why (T03–T06 never ran); that the role was applied and `cloudfront:Describe*` had to be added; the unfiltered-workflow-with-conditional-steps shape and why a `paths:` filter was impossible; the four untracked inputs a CI plan needs; that `infra` is now a required check, which phase-13 could not do; and the fact that the probe's skip path is unverified until the next wiki-only PR.

- [ ] **Step 6: Run the full verification matrix**

```bash
python3 scripts/lint_wiki.py && python3 scripts/test_lint_wiki.py
python3 site/build.py && python3 site/test_build_site.py && python3 scripts/verify_site.py
terraform -chdir=infra fmt -check -recursive
git check-ignore site/dist
```

Expected: every command exits `0`; `git check-ignore` prints `site/dist`.

- [ ] **Step 7: Commit and merge**

```bash
git add docs/rules/site-code.md docs/log.md docs/index.md docs/tasks/phase-17-infra-ci/
git commit -m "docs: record the phase-17 infra CI rules and close the phase"
git push
gh pr checks --watch
gh pr merge --squash --delete-branch
```

Expected: `verify`, `lint` and `infra` green before the merge. After it, **no `deploy.yml` run** — this branch touches `infra/`, `.github/workflows/infra.yml` and `docs/`, none of which is in `deploy.yml`'s `paths` list. Confirm rather than assume:

```bash
gh run list --workflow deploy.yml --limit 1 --json headSha --jq '.[0].headSha[0:7]'
git rev-parse --short HEAD
```

Expected: the two SHAs differ.

---

## Out of scope

- **The account ID and the two personal email addresses still present in `docs/log.md` and `docs/tasks/phase-15-public-repo/`.** Found during phase-16 cross-checking, pushed to the public repo, awaiting a decision (mask the current files / rewrite history / accept). It is a content decision, not an infra one, and it does not block this phase.
- **Making `infra.yml` gate the site deploy.** phase-13 ruled this out and the reasoning still holds: the deploy is an `aws s3 sync` that never executes Terraform, so blocking wiki publishing on a `.tf` typo is a false coupling. With `infra` now a required check on `main`, the broken `.tf` is stopped before the merge instead, which is the better place.
- **`terraform apply` from CI.** Applies stay operator-run, per the phase-9 precedent.

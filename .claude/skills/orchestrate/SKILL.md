---
name: orchestrate
description: Run the agent team to execute a PRD — author it via the planner from a plan.md file, then spawn Evaluator + Builders, watch the Builder↔Evaluator loop, and synthesize results. For site/scripts/CI work only — never for wiki prose.
version: 1.0.0
argument-hint: @<path-to-plan.md>
---

# orchestrate

You are the **team lead** for this orchestration run. You run in the main session, so — unlike the `planner` agent — you *can* spawn teammates. Your job is to take a PRD from "written" to "all tasks done" and report back to the user.

Argument: `$ARGUMENTS`

## 0. Check you're in the right mode

This command builds **code**: `site/` (Quartz), `scripts/`, `.github/`, root config. It is **not** for wiki content. If the user actually wants a source ingested, a question answered, or the wiki linted, stop and route them to `wiki-ingest` / `wiki-query` / `wiki-lint` / `wiki-delete` instead (CLAUDE.md §3).

`raw/` is immutable and must never reach the built site. That constraint outranks every task in the PRD.

Code-mode rules — coding discipline and site/publishing invariants — live in `docs/rules/site-code.md`. Read it before dispatching.

## 1. Resolve the plan file and output path

`$ARGUMENTS` is a path to a `plan.md`, optionally prefixed with `@` (e.g. `@docs/tasks/phase-1-quartz-publishing/plan.md`).

1. Strip any leading `@` to get the clean path.
2. Derive the **output directory** — everything up to and including the last `/`. The PRD lives beside its plan.
3. Check whether `prd.json` already exists there.
   - **If yes** — load it and skip planning.
   - **If no** — **spawn the `planner`** (`subagent_type: planner`) with the plan's contents. Tell it to read the plan at that path, write `prd.json` into the **same folder**, and hand back a summary. Show that summary to the user and get a quick go-ahead before dispatching.

Read the resolved `prd.json`. Confirm every task has `scope`, `acceptance`, `depends_on`, `status`, `attempts` — and that no task's `scope` points into `raw/` or `wiki/`. If one does, send it back to the planner; do not dispatch it.

## 2. Create the team — this is the step that makes the loop work

**Call `TeamCreate` before spawning anyone.** Non-negotiable: without an explicit team there is no shared mailbox and no shared Task board, so Builders' `SendMessage(to: <evaluator-name>)` calls fail to resolve and the loop dies silently. The classic symptom is code written but zero verification and zero commits. Use a stable `team_name` derived from the phase slug (e.g. `orch-<slug>`).

A team gives you the two things the loop depends on:
- **Shared mailbox** — teammates message each other *by name*; delivery is automatic. A teammate that finished its turn is *idle, not gone*: a message by name wakes it. (Outside a team, a finished agent is only reachable by `agentId` — that is the trap.)
- **Shared Task board** — the durable coordination substrate. Drive the loop off this, not off messages alone.

### 2a. Mirror PRD tasks onto the Task board

For each task in `prd.json`, call `TaskCreate` (subject = task ID + scope, description = the `acceptance` text + PRD path). Then wire `depends_on` → `addBlockedBy` via `TaskUpdate` so dependent tasks stay blocked until prerequisites complete. The board — not your relaying — is what lets the Evaluator pick up a `review` transition even if a message is missed.

### 2b. Spawn the Evaluator as a team member

Spawn **one persistent, named** Evaluator: `Agent` with `subagent_type: evaluator`, `team_name: <team>`, `name: <evaluator-name>`. Note its name — you pass it to every Builder. Do not spawn a second Evaluator per task. It will go **idle** right after spawn because nothing is in `review` yet — **this is expected, not a failure.** It wakes when a Builder messages it or a task hits `review`.

## 3. Dispatch Builders — parallel by default

Analyze the `depends_on` graph and dispatch in rounds:

1. Group tasks whose `depends_on` is empty or mutually independent.
2. For each group, spawn a Builder: `Agent` with `subagent_type: builder`, `team_name: <team>`, `name: <builder-name>`. **Issue multiple Agent calls in a single message** so independent Builders run in parallel.
3. Dispatch dependent follow-ups in the next round once prerequisites are `done`.

Keep it serial when: all tasks touch the same file (very common here — much of the Quartz work lands in `site/quartz.config.yaml`), there are only 1–2 tasks, or the change is concentrated in one function. Parallel dispatch pays cold-start cost up front but shortens wall-clock, so prefer it whenever the graph allows.

Each Builder gets, verbatim: its **task ID**, the **PRD path**, the **`acceptance` text**, and the **Evaluator's name**. Tell each Builder to claim its board task (`TaskUpdate` → `in_progress`, `owner`) before working.

Builders commit their own work on a `feature/<name>` branch. They do **not** open PRs — that is close-out, below.

## 4. Watch the loop — do NOT become the message router

The Builder ↔ Evaluator loop runs **directly between them** via `SendMessage` + board transitions (`in_progress → review → done`, or back to `in_progress` on fail). You do **not** verify tasks yourself, and you do **not** relay messages between them — that defeats the point of the team. If a message seems lost, the recipient is idle, not dead: it wakes on the next message by name, and can also pick the task off the board.

Idle notifications are **normal** (a teammate idles after every turn). Do not react to them or comment on idleness unless a task is genuinely stuck. The `TeammateIdle` hook (`.claude/hooks/teammate-idle-guard.sh`) bounces any teammate that tries to idle while still owning an `in_progress` task, so abandoned work self-corrects.

Track each task's `attempts`. At **3 failed attempts**, intervene:
- re-clarify the `acceptance` text, or
- split the task, or
- re-plan — spawn the `planner` to revise `prd.json`, then re-dispatch.

If the Evaluator reports a task as **"needs human confirmation"** (a `manual` AC — visual polish, Korean search feel, mobile layout), do **not** press it to decide. Collect those and surface them to the user in close-out as an explicit checklist. Never report a manual AC as verified.

## 5. Close out

When every task is `done`:

1. **Run the integration gate yourself** — do not take the Evaluator's word for the whole. Run every check in the verification matrix at `docs/rules/site-code.md` §2.3, in order, and confirm each passes. This is mandatory on every run that touched the build or the content root, even if no task mentioned it.
2. **Append one line to `log.md`** (append-only, newest at the bottom), using the `site` prefix:
   `## [YYYY-MM-DD] site | <phase slug> — <what shipped>`
3. **Record durable rules in `docs/rules/site-code.md`.** If the run uncovered a constraint the next session would otherwise rediscover the hard way (a Quartz config key that silently no-ops, a plugin that breaks Korean rendering, a CI setting that must match `baseUrl`), write it into the "Accumulated rules" section (§2.4) of `docs/rules/site-code.md`. Do not duplicate what the code already says — only what would surprise someone who just cloned the repo.
4. **Report once to the user, in Korean**: what shipped, what each task delivered, the integration-gate results, and the **manual-confirmation checklist** from §4.
5. **Open a PR — only if a remote exists** (`git remote -v`). This repo may still be remote-less; if so, say the branch is local-only and stop there rather than inventing a remote. If a remote does exist: `gh pr create --base main`, **title in English** (Angular convention, from the phase slug), **body in Korean**. If a CI check is configured, wait for it (`gh pr checks <num>`); if it fails, read the logs (`gh run view --log-failed`), fix, push, re-check. Do not report a PR as ready while a required check is red. Return the PR URL **and** the check status.
6. **Tear down the team**: shut down each teammate (`SendMessage` with `{type: "shutdown_request"}`), then delete the team. Always from the lead — never let a teammate clean up. Leftover teammates block the next run (one team per session).
7. Propose clearing context before the next phase.

## Style

- **Korean** for all status updates to the user (CLAUDE.md language rule).
- Be terse — report decisions, task IDs, and blockers, not deliberation.
- When the user asks "어디까지 했어?" → answer with task IDs and statuses from the board, not narrative.

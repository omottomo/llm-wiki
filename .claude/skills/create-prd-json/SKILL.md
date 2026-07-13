---
name: create-prd-json
description: This skill should be used when the user has worked out a rough plan during the conversation and asks to "create a prd", "write the prd", "make a prd.json", "prd 파일 생성", "prd.json 만들어", "phase prd 만들어", or otherwise wants the current session's plan captured as a structured prd.json for the orchestration team. Captures the plan established in THIS session into docs/tasks/phase-{N}-{slug}/prd.json, following the planner agent's PRD schema. For site/scripts/CI work only — never for wiki prose.
version: 1.0.0
---

# create-prd-json

Persist the plan worked out **in the current conversation** into a phase-numbered `prd.json`, following the **planner agent's PRD schema** so it can be consumed directly by `/orchestrate`.

This produces the same artifact the `planner` agent (`.claude/agents/planner.md`) would author — a structured PRD of atomic, verifiable tasks — but distilled from THIS session's conversation rather than from a separate planning pass.

## When to use

Invoke this after the user and Claude have converged on a rough plan, and the user asks to save it as a PRD. The plan content comes from **this session's conversation** — do not invent a new plan; decompose what was already agreed.

**Not for wiki content.** This PRD feeds the Builder ↔ Evaluator loop, which works on `site/`, `scripts/`, `.github/`, and root config. If the plan is about ingesting a source or editing wiki prose, that is `wiki-ingest` / `wiki-query` territory — say so and stop.

Code-mode rules for the work you're capturing — coding discipline and site/publishing invariants — live in `docs/rules/site-code.md`.

## Procedure

### 1. Locate the target directory

```
docs/tasks/phase-{number}-{slug}/prd.json
```

Find `docs/tasks/` relative to the repo root. Create it if it doesn't exist. If the plan already lives in a `plan.md` somewhere under `docs/tasks/`, **write the PRD beside it** in that same folder rather than making a new one — `/orchestrate` derives the PRD path from the plan's directory.

### 2. Determine the phase number

- List existing `docs/tasks/phase-*` folders.
- Parse the leading integer from each, take the **maximum**, use **max + 1**.
- If none exist, start at **1**. Use the bare number (`phase-3-...`), not zero-padded.

```bash
ls -d docs/tasks/phase-* 2>/dev/null \
  | sed -E 's@.*/phase-([0-9]+)-.*@\1@' \
  | sort -n | tail -1
# next = that value + 1, or 1 if empty
```

### 3. Generate the phase slug

Synthesize a short **kebab-case** slug (lowercase, hyphenated, ~2–5 words) from the plan. Example: publishing the wiki via Quartz on Cloudflare → `quartz-publishing`. The folder becomes `phase-{number}-{slug}`, and the `phase` field in the JSON is that same string.

### 4. Decompose the session plan into atomic tasks, and verify goal-entailment

Apply the planner agent's rules **verbatim** from `.claude/agents/planner.md` — the "Rules" bullets under its "PRD schema" section (task decomposition, including the goal-entailment gate) and its "Task sizing & teammate load" section. Do not re-derive or restate them here; that file is the single source of truth for what makes a task atomic, what makes an acceptance criterion mechanically checkable, and how to verify the `goal` is entailed by the union of task acceptances before writing.

### 5. Write `prd.json`

- Create `docs/tasks/phase-{number}-{slug}/`.
- Write `prd.json` inside, following the schema in `.claude/agents/planner.md` ("PRD schema" section — field meanings and constraints are documented there).
- Use today's date (`YYYY-MM-DD`) in `created_at`.
- Every task starts at `"status": "pending"`, `"attempts": 0`.
- **Write all free-text fields in English** (`goal`, `title`, `acceptance`, and the slug), even though this session is in Korean and the wiki content is Korean. The PRD is an agent-facing operating file — CLAUDE.md's language rule puts those in English. Translate the agreed plan; do not change its meaning.

After writing, tell the user (in Korean) the exact path created, the phase slug, the task count, and the dependency shape — so they can hand it straight to `/orchestrate`.

## Notes

- Vague acceptance text stalls the Builder ↔ Evaluator loop. Keep it settleable by a command.
- This skill only authors the PRD. Execution — spawning the Evaluator and Builders and watching the loop — is `/orchestrate`'s job.

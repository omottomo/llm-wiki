# Git Rules — Branches, Commits, PRs

> Module of the repo's operating rules, split out of `CLAUDE.md`.
> **Read this before any commit, branch, push, or PR**, in either mode. The common rules in
> `CLAUDE.md` always apply on top of this file.

---

## 1. `main` is protected

Never commit, push, or merge on `main` directly. Every change lands through a branch and a PR.
No hook enforces this — following it is on you.

## 2. Branches

- Name a branch `<type>/<slug>`, where type is one of `feat|fix|refactor|docs|chore`.
- Start from the latest default branch (`origin/main`).
- **Exception — content skills use one fixed branch each**: `wiki-ingest`, `wiki-lint`,
  `wiki-query`. Each skill's `SKILL.md` states the branch and why: every run touches a category
  page and `docs/log.md`, so per-run branches conflict with each other the moment `main` moves.
  If that skill's PR is already open, add the commit to it instead of opening a second one.

## 3. Commits

- **Title**: English, Conventional Commits (`<type>(<scope>): <summary>`).
- **Body**: short Korean, following `.claude/git-message-template.md` (`- 무엇:` / `- 왜:` /
  `- 영향:`; delete the `영향` line when there is nothing to say).
- **Trailer**: every commit ends with `Task: <slug>`. It is the history lookup key:
  `git log --grep="Task: <slug>"`.
- Code mode commits once per task (`docs/rules/site-code.md`); a content skill commits once per
  run.
- An ingest commits twice, because `raw/` is a nested private repo: first inside `raw/`, then
  the parent repo (`docs/rules/wiki-content.md` §3).

## 4. Pull requests

- Open the PR against `main`. The title follows the commit-title rule.
- The body is short Korean in the same template and ends with `Task: <slug>`.

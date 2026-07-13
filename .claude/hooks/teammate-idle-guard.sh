#!/usr/bin/env bash
# TeammateIdle guard for the /orchestrate agent team.
#
# Fires when a teammate is about to go idle. If that teammate still OWNS a task
# whose status is `in_progress` on the shared Task board, it abandoned work in
# the middle — exit 2 to keep it working. Otherwise let it idle normally
# (handing a task to `review` and idling is the correct, expected flow).
#
# Design rule: FAIL OPEN. Any uncertainty (no jq, unknown schema, can't find the
# team, can't identify the teammate) → exit 0. A guard that wrongly traps a
# teammate in a loop is worse than no guard.
set -euo pipefail

input="$(cat 2>/dev/null || true)"
command -v jq >/dev/null 2>&1 || exit 0

# --- Identify the idling teammate (try the likely field names) -------------
name="$(printf '%s' "$input" | jq -r '
  .teammate_name // .teammateName // .teammate // .agent_name // .agentName
  // .name // empty' 2>/dev/null || true)"
[ -n "$name" ] || exit 0   # can't tell who is idling → fail open

# --- Locate this team's task board -----------------------------------------
team="$(printf '%s' "$input" | jq -r '
  .team_name // .teamName // .team // empty' 2>/dev/null || true)"

tasks_root="${HOME}/.claude/tasks"
if [ -n "$team" ] && [ -d "${tasks_root}/${team}" ]; then
  tasks_dir="${tasks_root}/${team}"
else
  # Fall back to the most recently touched task board.
  tasks_dir="$(ls -1dt "${tasks_root}"/*/ 2>/dev/null | head -n1 || true)"
fi
[ -n "${tasks_dir:-}" ] && [ -d "$tasks_dir" ] || exit 0

# --- Does this teammate still own an in_progress task? ----------------------
# Slurp every JSON file under the board, flatten array-or-object shapes, and
# look for a task owned by $name with status in_progress.
abandoned="$(find "$tasks_dir" -type f -name '*.json' -exec cat {} + 2>/dev/null \
  | jq -s --arg n "$name" '
      [ .[] | (if type=="array" then .[] else . end) ]
      | map(select(type=="object"
            and (.owner // "") == $n
            and (.status // "") == "in_progress"))
      | length' 2>/dev/null || echo 0)"

if [ "${abandoned:-0}" -gt 0 ] 2>/dev/null; then
  echo "You still own an in_progress task on the board. Finish it: implement and SendMessage the Evaluator for review (Builder), or run the tests and post a verdict (Evaluator). Do not go idle with work outstanding." >&2
  exit 2
fi

exit 0

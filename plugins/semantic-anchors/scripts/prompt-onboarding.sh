#!/bin/bash
# Claude SessionStart hook that prompts for semantic-anchor onboarding
# when no managed anchor block is present yet.

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
STATE_DIR="$HOME/.claude/semantic-anchor-onboarding"
STATE_FILE="$STATE_DIR/state.json"
MARKER="<!-- semantic-anchors:start -->"
COOLDOWN_HOURS=24

has_marker() {
  local file
  for file in "$@"; do
    if [ -f "$file" ] && grep -qF "$MARKER" "$file"; then
      return 0
    fi
  done
  return 1
}

if has_marker \
  "$PROJECT_DIR/AGENTS.md" \
  "$PROJECT_DIR/CLAUDE.md" \
  "$PROJECT_DIR/GEMINI.md" \
  "$PROJECT_DIR/.github/copilot-instructions.md" \
  "$PROJECT_DIR/.claude/AGENTS.md" \
  "$HOME/.claude/CLAUDE.md" \
  "$CODEX_HOME_DIR/AGENTS.md" \
  "$HOME/.gemini/GEMINI.md"; then
  exit 0
fi

mkdir -p "$STATE_DIR"

python3 - "$STATE_FILE" "$PROJECT_DIR" "$COOLDOWN_HOURS" <<'PY'
import json
import os
import sys
from datetime import datetime, timedelta, timezone

state_path, project_dir, cooldown_hours = sys.argv[1], sys.argv[2], int(sys.argv[3])
now = datetime.now(timezone.utc)

try:
    with open(state_path, "r", encoding="utf-8") as handle:
        state = json.load(handle)
except FileNotFoundError:
    state = {}

projects = state.setdefault("projects", {})
entry = projects.setdefault(project_dir, {})
last_prompt_raw = entry.get("last_prompt")

if last_prompt_raw:
    last_prompt = datetime.fromisoformat(last_prompt_raw.replace("Z", "+00:00"))
    if now - last_prompt < timedelta(hours=cooldown_hours):
        raise SystemExit(0)

entry["last_prompt"] = now.isoformat().replace("+00:00", "Z")

with open(state_path, "w", encoding="utf-8") as handle:
    json.dump(state, handle, indent=2)
    handle.write("\n")

message = (
    "Semantic anchors are not configured for this workspace. "
    "On your next response, ask one short onboarding question: "
    "whether the user wants to onboard semantic anchors now for this project "
    "or for their home directory. If they agree, use the semantic-anchor-onboarding skill."
)

payload = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": message,
    }
}
print(json.dumps(payload))
PY

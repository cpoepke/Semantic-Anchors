#!/bin/sh
# Sync generic skills into the Claude plugin package.

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/skill"
PLUGIN_SKILLS_DIR="$REPO_ROOT/plugins/semantic-anchors/skills"

mkdir -p "$PLUGIN_SKILLS_DIR"

# Remove all existing skills so deletions in skill/ are reflected
find "$PLUGIN_SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +

for skill_dir in "$SOURCE_DIR"/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  rm -rf "$PLUGIN_SKILLS_DIR/$skill_name"
  cp -R "$skill_dir" "$PLUGIN_SKILLS_DIR/$skill_name"
done

echo "Synced skills into $PLUGIN_SKILLS_DIR"

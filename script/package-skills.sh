#!/usr/bin/env bash
# Package top-level skills into distributable .skill files (zip archives).
#
# A .skill file is a zip of a skill folder, named <skill>.skill, with the skill
# folder as the top-level entry (e.g. voiceprint/SKILL.md inside). It can be
# uploaded to claude.ai, dropped into Cowork, or unzipped into ~/.claude/skills/.
#
# Usage:
#   script/package-skills.sh                 # package every skill in skills/
#   script/package-skills.sh voiceprint      # package just named skills
#   script/package-skills.sh voiceprint cowork contract-manager
#
# Output: dist/<skill>.skill (dist/ is gitignored — upload to a GitHub Release).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
DIST_DIR="$REPO_ROOT/dist"

cd "$REPO_ROOT"
mkdir -p "$DIST_DIR"

# Resolve the list of skills to package.
if [ "$#" -gt 0 ]; then
  skills=("$@")
else
  skills=()
  for d in "$SKILLS_DIR"/*/; do
    skills+=("$(basename "$d")")
  done
fi

packaged=0
skipped=0

for skill in "${skills[@]}"; do
  src="$SKILLS_DIR/$skill"

  if [ ! -d "$src" ]; then
    echo "SKIP  $skill — no such directory under skills/"
    skipped=$((skipped + 1))
    continue
  fi

  if [ ! -f "$src/SKILL.md" ]; then
    echo "SKIP  $skill — no SKILL.md"
    skipped=$((skipped + 1))
    continue
  fi

  # Minimal frontmatter validation: name + description must be present.
  if ! grep -qE '^name:' "$src/SKILL.md" || ! grep -qE '^description:' "$src/SKILL.md"; then
    echo "SKIP  $skill — SKILL.md missing name: or description: frontmatter"
    skipped=$((skipped + 1))
    continue
  fi

  out="$DIST_DIR/$skill.skill"
  rm -f "$out"

  # Zip from skills/ so the archive's top-level entry is the skill folder name,
  # matching skill-creator's package_skill.py layout. Exclude build/OS junk.
  ( cd "$SKILLS_DIR" && zip -r -q "$out" "$skill" \
      -x '*/.DS_Store' '*/__pycache__/*' '*.pyc' '*/node_modules/*' )

  size="$(du -h "$out" | cut -f1 | tr -d ' ')"
  echo "OK    $skill → dist/$skill.skill ($size)"
  packaged=$((packaged + 1))
done

echo ""
echo "Packaged $packaged, skipped $skipped. Output in dist/"
echo "Attach to a release:  gh release upload <tag> dist/*.skill"

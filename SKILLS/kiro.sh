#!/bin/bash

SOURCE="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.kiro/skills"

mkdir -p "$SKILLS_DIR"

count=0
for skill_dir in "$SOURCE"/*/; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  name="$(basename "$skill_dir")"
  if [ -L "$SKILLS_DIR/$name" ] || [ -d "$SKILLS_DIR/$name" ]; then
    echo "skip: $name (already exists)"
  else
    ln -s "$skill_dir" "$SKILLS_DIR/$name"
    echo "link: $name"
    ((count++))
  fi
done

echo "Done. $count skill(s) linked."
echo ""
echo "To activate in Kiro, add this to your agent config resources[]:"
echo "  \"skill://$SKILLS_DIR/**/SKILL.md\""

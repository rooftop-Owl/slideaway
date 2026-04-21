#!/bin/bash
# slide-lint-hook.sh — PostToolUse hook for PPTX content linting
#
# Fires on every Write|Edit tool event. MUST exit 0 immediately for non-.pptx
# files to keep the hook cheap. Only runs linting when a .pptx file is written.
#
# Warnings (exit 1 from slide_linter.py) do NOT block — they are informational.
# Hard failures (exit 2) are fed back to Claude as a hook error.
#
# Input: JSON from stdin (PostToolUse provides tool_input as JSON)
# Output: exit 0 (success/skip/warn-only), exit 2 (lint failed — fed back to Claude)

set -euo pipefail

input=$(cat)

filepath=$(echo "$input" | python3 -c "
import sys, json
data = json.load(sys.stdin)
tool_input = data.get('tool_input', {})
print(tool_input.get('filePath', tool_input.get('file_path', '')))
" 2>/dev/null || echo "")

# EARLY EXIT: skip non-.pptx files — this fires on every Write|Edit
if [[ -z "$filepath" ]] || [[ "$filepath" != *.pptx ]]; then
  exit 0
fi

echo "Linting PPTX content: $filepath"

python3 "${CLAUDE_PLUGIN_ROOT}/tools/slide_linter.py" "$filepath"
exit_code=$?

if [[ $exit_code -eq 0 ]]; then
  echo "Content lint passed: $filepath"
  exit 0
elif [[ $exit_code -eq 1 ]]; then
  # Warnings only — informational, do not block
  echo "Content lint warnings (non-blocking): $filepath"
  exit 0
else
  echo "Content lint FAILED: $filepath" >&2
  exit 2
fi

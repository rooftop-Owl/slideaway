#!/bin/bash
# validate-pptx-hook.sh — PostToolUse hook for PPTX validation
#
# Fires on every Write|Edit tool event. MUST exit 0 immediately for non-.pptx
# files to keep the hook cheap. Only runs validation when a .pptx file is written.
#
# Input: JSON from stdin (PostToolUse provides tool_input as JSON)
# Output: exit 0 (success/skip), exit 2 (validation failed — fed back to Claude)

set -euo pipefail

# Read full JSON input from stdin
input=$(cat)

# Extract filePath from tool_input using python3 (handles nested JSON safely, tries both camelCase and snake_case)
filepath=$(echo "$input" | python3 -c "
import sys, json
data = json.load(sys.stdin)
tool_input = data.get('tool_input', {})
# Write tool uses 'file_path', Edit tool uses 'file_path'; Claude Code PostToolUse uses 'filePath'
print(tool_input.get('filePath', tool_input.get('file_path', '')))
" 2>/dev/null || echo "")

# EARLY EXIT: If no filepath or not a .pptx file, skip immediately
# This is the critical performance guardrail — fires on EVERY Write|Edit
if [[ -z "$filepath" ]] || [[ "$filepath" != *.pptx ]]; then
  exit 0
fi

# .pptx file detected — run validation
echo "Validating PPTX: $filepath"

if python3 "${CLAUDE_PLUGIN_ROOT}/tools/validate_pptx.py" "$filepath"; then
  echo "PPTX validation passed: $filepath"
  exit 0
else
  echo "PPTX validation failed: $filepath" >&2
  exit 2
fi

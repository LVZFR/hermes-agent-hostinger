#!/bin/bash
# Defense-in-depth secret scan of a staging dir before committing a sanitized backup.
# Usage: scan-secrets.sh <dir>
# Exit 0 = clean, exit 1 = suspicious matches found (review before pushing).
set -u
DIR="${1:-.}"
RC=0

echo "=== Token-prefix / known-key patterns ==="
HITS=$(grep -rnaE \
  'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|[0-9]{8,10}:[A-Za-z0-9_-]{30,}' \
  "$DIR" 2>/dev/null | grep -vi 'example\|placeholder\|your_\|<token>\|xxxx')
if [ -n "$HITS" ]; then echo "$HITS"; RC=1; else echo "  >> NONE"; fi

echo ""
echo "=== Populated api_key/token/password/secret assignments ==="
HITS=$(grep -rnaiE \
  '(api[_-]?key|token|password|secret|bearer)["'"'"' ]*[:=]["'"'"' ]*[A-Za-z0-9]{16,}' \
  "$DIR" 2>/dev/null | grep -vi 'example\|placeholder\|your_\|_env\|access_token_env')
if [ -n "$HITS" ]; then echo "$HITS"; RC=1; else echo "  >> NONE"; fi

echo ""
echo "=== Env-key name mentions (variable references are OK; values are NOT) ==="
grep -rnai 'GITHUB_TOKEN\|ANTHROPIC_API_KEY\|TELEGRAM_BOT_TOKEN\|OPENAI_API_KEY' "$DIR" 2>/dev/null | head -20 || echo "  >> none"
echo "  (Above are fine ONLY if they are \$VAR references in docs, not assigned values.)"

echo ""
if [ "$RC" -eq 0 ]; then echo "RESULT: CLEAN ✓"; else echo "RESULT: REVIEW NEEDED ✗ (matches above)"; fi
exit $RC

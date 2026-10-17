#!/usr/bin/env bash
# Re-reads every cited file at its recorded revision and compares the blob SHA-256 in SOURCES.tsv.
# Usage: CLONE_ROOT=<dir with fresh clones named as in the repo column> ./verify-sources.sh
# Rows with repo GOAL-LOCAL are the unpublished candidate texts; set GOAL_LOCAL_CHECKOUT to a checkout that
# holds commit 64c843b to verify them, otherwise they are reported SKIPPED-UNPUBLISHED (never silently passed).
set -u
: "${CLONE_ROOT:?set CLONE_ROOT}"
here="$(cd "$(dirname "$0")" && pwd)"
ok=0; bad=0; skip=0
while IFS=$'\t' read -r repo rev path want; do
  [ "$repo" = "repo" ] && continue
  if [ "$repo" = "GOAL-LOCAL" ]; then
    if [ -n "${GOAL_LOCAL_CHECKOUT:-}" ]; then dir="$GOAL_LOCAL_CHECKOUT"; else echo "SKIPPED-UNPUBLISHED $rev $path"; skip=$((skip+1)); continue; fi
  else dir="$CLONE_ROOT/$repo"; fi
  got=$(git -C "$dir" show "$rev:$path" 2>/dev/null | sha256sum | cut -d' ' -f1)
  if [ "$got" = "$want" ]; then ok=$((ok+1)); else echo "MISMATCH $repo $rev $path"; bad=$((bad+1)); fi
done < "$here/SOURCES.tsv"
echo "verified=$ok mismatched=$bad skipped=$skip"
[ "$bad" -eq 0 ]

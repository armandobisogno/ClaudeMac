#!/usr/bin/env bash
# Sync Macchine Pensanti: scarica, aggiorna i dati condivisi in brain/scrittura/,
# committa e pusha SOLO se e' cambiato qualcosa. Per la routine cloud, ma
# eseguibile anche a mano da locale.
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1

git pull --rebase --autostash --quiet 2>/dev/null || true

REPORT="$(python3 brain/tools/mp_check.py --sync 2>&1)"
echo "$REPORT"

SHARED=(brain/scrittura/mp-posts-data.json
        brain/scrittura/mp-notes-data.json
        brain/scrittura/mp-posts-index.md
        brain/scrittura/mp-notes-archive.md)

if [[ -n "$(git status --porcelain "${SHARED[@]}" 2>/dev/null)" ]]; then
  git add "${SHARED[@]}"
  SUMMARY="$(printf '%s\n' "$REPORT" | grep -E '^\*\*[0-9]+ nuov' | tr '\n' ' ')"
  git commit --quiet -m "mp: sync $(date -u +%Y-%m-%dT%H:%MZ)" -m "${SUMMARY:-aggiornamento archivio}"
  if git push --quiet 2>/dev/null; then
    echo "committato e pushato."
  else
    echo "committato in locale; push non riuscito (verifica remote/credenziali)."
  fi
else
  echo "niente da committare."
fi

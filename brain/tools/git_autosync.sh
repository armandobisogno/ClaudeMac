#!/usr/bin/env bash
# git_autosync.sh — allinea, fotografa e carica su GitHub tutto il repo ClaudeWS.
#
# Prudente per costruzione: .git sta dentro Dropbox e si lavora da piu' Mac,
# quindi prima ci si allinea con GitHub (rebase con autostash), poi si committa,
# poi si pusha. In caso di conflitto NON forza nulla: si ferma e lo scrive nel
# log. Esce sempre 0 per non disturbare hook e launchd.
#
# Usato da:
#   - LaunchAgent com.armandobisogno.claudews-autosync (ogni 3 ore)
#   - hook SessionStart (all'apertura di ogni sessione Claude Code)
#
# Log: ~/.claude/claudews_autosync.log
set -uo pipefail

export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin"
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
LOG="$HOME/.claude/claudews_autosync.log"

log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >>"$LOG"; }

cd "$REPO" 2>/dev/null || { log "repo non trovato: $REPO"; exit 0; }
[[ -d .git ]] || { log "non e' un repo git: $REPO"; exit 0; }

# lock: evita due sync in parallelo (timer + hook nello stesso istante).
# Sta fuori dalla cartella Dropbox: dentro, il file provider aggiunge xattr
# e il rmdir puo' fallire lasciando lock fantasma.
LOCK="$HOME/.claude/claudews_autosync.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  # lock vecchio di oltre 30 min = resto di un run interrotto: lo tolgo
  if [[ -d "$LOCK" ]] && [[ $(( $(date +%s) - $(stat -f %m "$LOCK") )) -gt 1800 ]]; then
    rmdir "$LOCK" 2>/dev/null && mkdir "$LOCK" 2>/dev/null || exit 0
  else
    exit 0
  fi
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
[[ "$BRANCH" == "main" ]] || { log "branch '$BRANCH' != main: mi fermo."; exit 0; }

# 1. allinea con GitHub
if ! git pull --rebase --autostash --quiet 2>>"$LOG"; then
  git rebase --abort 2>/dev/null || true
  git stash pop 2>/dev/null || true
  log "pull/rebase fallito (conflitto o rete): nessuna modifica forzata, mi fermo."
  exit 0
fi

# 2. c'e' qualcosa da fotografare?
if [[ -z "$(git status --porcelain)" ]]; then
  # magari ho solo commit locali da spingere
  if [[ -n "$(git log --oneline @{u}.. 2>/dev/null)" ]]; then
    git push --quiet 2>>"$LOG" && log "commit locali caricati su GitHub." \
      || log "commit locali presenti; push non riuscito."
  fi
  exit 0
fi

git add -A
git commit --quiet \
  -m "autosync $(date -u '+%Y-%m-%dT%H:%MZ')" \
  -m "commit automatico di ClaudeWS (timer 3h / hook SessionStart)"

# 3. carica
if git push --quiet 2>>"$LOG"; then
  log "fotografato e caricato su GitHub ($(git rev-parse --short HEAD))."
else
  log "commit locale fatto; push non riuscito (rete/credenziali). Riprovo al prossimo giro."
fi
exit 0

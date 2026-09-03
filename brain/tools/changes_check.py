#!/usr/bin/env python3
"""SessionStart hook: elenca i file di ClaudeWS modificati dall'ultima sessione
di Claude Code su questa macchina.

Rilevamento via data di modifica (mtime): pensato per una cartella sincronizzata
(Dropbox) su cui si lavora anche da altri computer. Il marcatore e' per-macchina
e vive fuori dalla cartella sincronizzata, cosi' ogni Mac tiene il proprio "ultimo
visto" senza pestarsi i piedi.
"""
import os
import time
from pathlib import Path

WS = Path(os.environ.get(
    "CLAUDE_PROJECT_DIR",
    Path.home() / "Library/CloudStorage/Dropbox/ClaudeWS",
))
MARKER = Path.home() / ".claude" / "claudews_last_seen"

SKIP_DIRS = {".git", "__pycache__", ".dropbox.cache", "node_modules", ".obsidian", ".venv"}
SKIP_FILES = {".DS_Store"}
# stato per-macchina riscritto a ogni sessione: non e' una "modifica" da segnalare
SKIP_SUFFIXES = (".local.json",)
MAX_SHOWN = 30
FIRST_RUN_WINDOW = 7 * 86400  # se non c'e' marcatore: guarda gli ultimi 7 giorni


def changed_since(ts):
    rows = []
    for root, dirs, files in os.walk(WS):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in SKIP_FILES or name.endswith(SKIP_SUFFIXES):
                continue
            p = Path(root) / name
            try:
                m = p.stat().st_mtime
            except OSError:
                continue
            if m > ts:
                rows.append((m, p.relative_to(WS)))
    rows.sort(reverse=True)
    return rows


def main():
    now = time.time()
    if MARKER.exists():
        since = MARKER.stat().st_mtime
        first_run = False
    else:
        since = now - FIRST_RUN_WINDOW
        first_run = True

    rows = changed_since(since)

    if first_run:
        print(f"\U0001f5c2  Verifica modifiche attivata: {len(rows)} file toccati negli ultimi 7 giorni.")
    elif rows:
        print(f"\U0001f4dd Modificati dall'ultima sessione ({len(rows)} file):")
        for m, rel in rows[:MAX_SHOWN]:
            stamp = time.strftime("%d/%m %H:%M", time.localtime(m))
            print(f"   {stamp}  {rel}")
        if len(rows) > MAX_SHOWN:
            print(f"   … e altri {len(rows) - MAX_SHOWN}")
    else:
        print("✓ Nessun file modificato dall'ultima sessione.")

    try:
        MARKER.parent.mkdir(parents=True, exist_ok=True)
        MARKER.touch()
    except OSError:
        pass


if __name__ == "__main__":
    main()

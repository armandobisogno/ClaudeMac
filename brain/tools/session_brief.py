#!/usr/bin/env python3
"""
session_brief.py — brief di inizio sessione.

1. Novita' di Macchine Pensanti (delega a mp_check.py --quiet).
2. Scadenze della Direzione da brain/direzione/todo.md (scadute o entro 7 giorni).

Pensato per l'hook SessionStart. Stampa solo se c'e' qualcosa; esce sempre 0.
Aggiungere qui altri controlli di inizio sessione senza toccare settings.json.
"""
import subprocess, sys, re, datetime, pathlib

TOOLS = pathlib.Path(__file__).resolve().parent
BRAIN = TOOLS.parent
MP_CHECK = TOOLS / "mp_check.py"
MP_STATE = TOOLS / "mp_state.local.json"
TODO = BRAIN / "direzione" / "todo.md"

DUE_WINDOW_DAYS = 7
DATE_RE = re.compile(r"scad:\s*(\d{4})-(\d{2})-(\d{2})")
OPEN_TASK_RE = re.compile(r"^\s*[-*]\s*\[ \]\s*(.+?)\s*$")


def mp_part():
    try:
        subprocess.run(
            [sys.executable, str(MP_CHECK), "--quiet", "--state", str(MP_STATE)],
            timeout=25, check=False,
        )
    except Exception:  # noqa: BLE001
        pass


def direzione_part():
    try:
        text = TODO.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        return
    text = re.sub(r"(?s)<!--.*?-->", "", text)  # ignora gli esempi commentati
    today = datetime.date.today()
    rows = []
    for line in text.splitlines():
        m = OPEN_TASK_RE.match(line)
        if not m:
            continue
        d = DATE_RE.search(line)
        if not d:
            continue
        try:
            due = datetime.date(int(d.group(1)), int(d.group(2)), int(d.group(3)))
        except ValueError:
            continue
        delta = (due - today).days
        if delta <= DUE_WINDOW_DAYS:
            label = DATE_RE.sub("", m.group(1)).strip(" —-·")
            rows.append((due, delta, label))
    if not rows:
        return
    rows.sort()
    print("## Direzione — scadenze\n")
    for due, delta, label in rows:
        if delta < 0:
            tag = f"SCADUTA da {-delta}g"
        elif delta == 0:
            tag = "oggi"
        elif delta == 1:
            tag = "domani"
        else:
            tag = f"tra {delta}g"
        print(f"- [{due.isoformat()} · {tag}] {label}")
    print()


if __name__ == "__main__":
    mp_part()
    direzione_part()
    sys.exit(0)

#!/usr/bin/env python3
"""
session_brief.py — brief di inizio sessione.

1. Novita' di Macchine Pensanti (delega a mp_check.py --quiet).
2. Scadenze della Direzione da brain/direzione/todo.md (scadute o entro 7 giorni).
3. PFO di tirocinio da firmare (delega a firma_pfo.py nuovi --quiet).

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


def tirocini_part():
    try:
        subprocess.run(
            [sys.executable, str(TOOLS / "firma_pfo.py"), "nuovi", "--quiet"],
            timeout=20, check=False, stderr=subprocess.DEVNULL,
        )
    except Exception:  # noqa: BLE001
        pass


def memoria_part():
    """Collega la memoria locale di Claude a brain/memoria (condivisa via Dropbox).

    Claude Code tiene la memoria in ~/.claude/projects/<chiave>/memory, una per
    computer. Qui la si trasforma in un link a brain/memoria. Se su questo Mac
    c'era gia' una memoria propria, i file nuovi o diversi finiscono in
    brain/memoria/_da_unire/<computer>/ e la cartella originale resta come
    memory.bak-<data>: niente si perde.
    """
    import os, re as _re, shutil, socket, filecmp
    shared = BRAIN / "memoria"
    if not shared.is_dir():
        return
    roots = {os.environ.get("CLAUDE_PROJECT_DIR") or str(BRAIN.parent)}
    roots |= {os.path.realpath(r) for r in roots}
    for root in roots:
        key = _re.sub(r"[^A-Za-z0-9]", "-", root)
        mem = pathlib.Path.home() / ".claude" / "projects" / key / "memory"
        if mem.is_symlink() and mem.resolve() == shared.resolve():
            continue
        mem.parent.mkdir(parents=True, exist_ok=True)
        if mem.is_symlink():
            mem.unlink()
        elif mem.is_dir():
            try:
                nome = subprocess.run(["scutil", "--get", "LocalHostName"], capture_output=True, text=True, timeout=5).stdout.strip()
            except Exception:
                nome = ""
            dest = shared / "_da_unire" / (nome or socket.gethostname().split(".")[0])
            for f in mem.glob("*.md"):
                g = shared / f.name
                if not g.exists() or not filecmp.cmp(f, g, shallow=False):
                    dest.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dest / f.name)
            mem.rename(mem.with_name("memory.bak-" + datetime.date.today().isoformat()))
            if dest.exists():
                print(f"🧠 Memoria: trovate note locali di questo computer, messe in {dest.relative_to(BRAIN.parent)} — da unire.")
        mem.symlink_to(shared)
        print("🧠 Memoria di Claude collegata a brain/memoria (condivisa tra i computer).")


if __name__ == "__main__":
    memoria_part()
    mp_part()
    direzione_part()
    tirocini_part()
    sys.exit(0)

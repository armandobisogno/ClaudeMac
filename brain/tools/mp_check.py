#!/usr/bin/env python3
"""
mp_check.py — controlla Macchine Pensanti (newsletter + note Substack di Armando Bisogno)
e segnala cosa c'e' di nuovo.

Due usi:

  # a inizio sessione (hook): stato per-macchina, non tocca i file condivisi
  python3 mp_check.py --quiet --state brain/tools/mp_state.local.json

  # sync (routine cloud o manuale): confronta con i dati condivisi, li aggiorna,
  # rigenera gli indici; il chiamante fa git commit se qualcosa e' cambiato
  python3 mp_check.py --sync

Altri flag:
  --full        come --sync ma stampa sempre il riepilogo completo
  --no-write    dry run, non scrive nulla

Solo stdlib. Se la rete non e' disponibile stampa un avviso ed esce 0
(non deve mai rompere una sessione).
"""
import json, sys, time, datetime, pathlib, hashlib
import urllib.request, urllib.parse, urllib.error

SUBDOMAIN = "armandobisogno"
USER_ID = 107692472

TOOLS = pathlib.Path(__file__).resolve().parent
BRAIN = TOOLS.parent
SCRITTURA = BRAIN / "scrittura"

# dati condivisi (versionati in git): sono il vero archivio
POSTS_DATA = SCRITTURA / "mp-posts-data.json"
NOTES_DATA = SCRITTURA / "mp-notes-data.json"
POSTS_MD = SCRITTURA / "mp-posts-index.md"
NOTES_MD = SCRITTURA / "mp-notes-archive.md"

UA = {"User-Agent": "Mozilla/5.0 (mp_check; personal second-brain sync)"}


def get_json(url, tries=3):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.2 * (i + 1))
    raise last


def load_json(path, default):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return default


def write_if_changed(path, content):
    p = pathlib.Path(path)
    old = p.read_text(encoding="utf-8") if p.exists() else None
    if old == content:
        return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return True


# ---------- fetch ----------

def fetch_posts():
    out, off, seen = [], 0, set()
    while off < 400:
        d = get_json(f"https://{SUBDOMAIN}.substack.com/api/v1/archive?sort=new&offset={off}&limit=12")
        if not isinstance(d, list) or not d:
            break
        for p in d:
            s = p.get("slug")
            if s and s not in seen:
                seen.add(s)
                out.append({
                    "slug": s,
                    "title": p.get("title"),
                    "subtitle": p.get("subtitle"),
                    "date": (p.get("post_date") or "")[:10],
                    "url": p.get("canonical_url"),
                    "audience": p.get("audience"),
                })
        if len(d) < 12:
            break
        off += 12
        time.sleep(0.25)
    return out


def _attach_summary(att):
    if not att:
        return ""
    parts = []
    for a in att:
        t = a.get("type")
        if t == "link":
            lm = a.get("linkMetadata") or {}
            parts.append(f"[link] {lm.get('title','')} — {lm.get('url','')}".strip())
        elif t == "post":
            parts.append(f"[quote-share post] {(a.get('publication') or {}).get('name','')}".strip())
        elif t == "image":
            parts.append("[image]")
        else:
            parts.append(f"[{t}]")
    return " | ".join(x for x in parts if x)


def fetch_notes(known_keys, deep=False, max_pages=6):
    out, cursor, pages, seen = [], None, 0, set()
    while True:
        url = f"https://substack.com/api/v1/reader/feed/profile/{USER_ID}?types%5B%5D=note"
        if cursor:
            url += "&cursor=" + urllib.parse.quote(cursor)
        d = get_json(url)
        items = d.get("items", []) if isinstance(d, dict) else []
        if not items:
            break
        page_keys = []
        for it in items:
            if it.get("type") != "comment":
                continue
            c = it.get("comment") or {}
            key = it.get("entity_key") or f"c-{c.get('id')}"
            page_keys.append(key)
            if key in seen:
                continue
            seen.add(key)
            out.append({
                "key": key,
                "date": (it.get("context", {}) or {}).get("timestamp", c.get("date", "")),
                "body": (c.get("body") or "").strip(),
                "attachments": _attach_summary(c.get("attachments")),
                "reactions": c.get("reaction_count", 0),
                "restacks": c.get("restacks", 0),
                "replies": c.get("children_count", 0),
            })
        pages += 1
        cursor = d.get("nextCursor") if isinstance(d, dict) else None
        if not cursor:
            break
        if not deep and (all(k in known_keys for k in page_keys) or pages >= max_pages):
            break
        if deep and pages >= 60:
            break
        time.sleep(0.3)
    return out


# ---------- render ----------

_NOTES_HEADER = """# Macchine Pensanti — archivio Note (auto-generato)

Fonte: feed profilo Substack (user {uid}). Rigenerato da `brain/tools/mp_check.py`.
Totale note raccolte: {n}.

> Il feed pubblico anonimo espone in modo denso solo le note recenti e un campione
> rado di quelle precedenti. Le NUOVE note sono catturate a ogni controllo; per
> l'archivio storico completo serve un export/copia-incolla dalla pagina /notes con login.
"""


def render_notes_md(notes):
    notes = sorted(notes, key=lambda n: n["date"], reverse=True)
    out = [_NOTES_HEADER.format(uid=USER_ID, n=len(notes))]
    for n in notes:
        d = n["date"][:16].replace("T", " ")
        meta = " ".join(m for m in (
            f"❤{n['reactions']}" if n.get("reactions") else "",
            f"↻{n['restacks']}" if n.get("restacks") else "",
            f"↩{n['replies']}" if n.get("replies") else "",
        ) if m)
        out.append(f"### {d}  ({n['key']}){('  ' + meta) if meta else ''}")
        if n["body"]:
            out.append("\n" + n["body"])
        if n["attachments"]:
            out.append(f"\n_{n['attachments']}_")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_posts_md(posts):
    posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    out = [
        "# Macchine Pensanti — indice newsletter (auto-generato)",
        "",
        f"Rigenerato da `brain/tools/mp_check.py`. Totale: {len(posts)}.",
        "",
        "| Data | Titolo | Sottotitolo | URL |",
        "|---|---|---|---|",
    ]
    for p in posts:
        sub = (p.get("subtitle") or "").replace("|", "/").replace("\n", " ").strip()
        if len(sub) > 140:
            sub = sub[:137] + "…"
        out.append(f"| {p['date']} | {p.get('title','')} | {sub} | {p.get('url','')} |")
    return "\n".join(out) + "\n"


# ---------- main ----------

def main():
    args = sys.argv[1:]
    quiet = "--quiet" in args
    full = "--full" in args
    sync = "--sync" in args or full
    write = "--no-write" not in args
    state_path = None
    if "--state" in args:
        state_path = args[args.index("--state") + 1]

    # base "gia' noto": file dati condivisi (per --sync) o file di stato (per --quiet)
    base_posts = {p["slug"]: p for p in load_json(POSTS_DATA, [])}
    base_notes = {n["key"]: n for n in load_json(NOTES_DATA, [])}

    if state_path and not sync:
        st = load_json(state_path, {})
        known_post_slugs = set(st.get("posts", {})) | set(base_posts)
        known_note_keys = set(st.get("notes", {})) | set(base_notes)
        first_run = not st.get("updated")
    else:
        known_post_slugs = set(base_posts)
        known_note_keys = set(base_notes)
        first_run = not base_posts and not base_notes

    try:
        posts = fetch_posts()
        notes = fetch_notes(known_note_keys, deep=sync)
    except Exception as e:  # noqa: BLE001
        print(f"⚠  Controllo Macchine Pensanti saltato (rete non disponibile: {e}).")
        return 0

    new_posts = sorted([p for p in posts if p["slug"] not in known_post_slugs], key=lambda p: p["date"])
    new_notes = sorted([n for n in notes if n["key"] not in known_note_keys], key=lambda n: n["date"])

    # ---- report ----
    if first_run and not sync:
        if not quiet:
            print(f"MP: primo controllo — baseline registrata ({len(posts)} articoli, "
                  f"{len(notes)} note viste). Le novita' future verranno segnalate qui.")
    elif not new_posts and not new_notes:
        if not quiet:
            print("MP: nessuna novita'.")
    else:
        print("## Macchine Pensanti — novita'\n")
        if new_posts:
            print(f"**{len(new_posts)} nuovo/i articolo/i:**")
            for p in new_posts:
                print(f"- {p['date']} — **{p.get('title','')}**")
                if p.get("subtitle"):
                    print(f"  {p['subtitle']}")
                print(f"  {p.get('url','')}")
            print()
        if new_notes:
            print(f"**{len(new_notes)} nuova/e nota/e:**")
            for n in new_notes:
                print(f"- {n['date'][:16].replace('T',' ')} ({n['key']})")
                if n["body"]:
                    print("  " + n["body"].replace("\n", "\n  "))
                if n["attachments"]:
                    print(f"  _{n['attachments']}_")
            print()
        print("→ da integrare in brain/scrittura/macchine-pensanti.md, "
              "brain/identita/tono-di-voce.md e nella mappa dei topic.")

    if not write:
        return 0

    # ---- persist ----
    if sync:
        for p in posts:
            base_posts[p["slug"]] = p
        for n in notes:
            base_notes[n["key"]] = n
        changed = False
        changed |= write_if_changed(POSTS_DATA, json.dumps(sorted(base_posts.values(),
                    key=lambda p: p["date"], reverse=True), ensure_ascii=False, indent=1) + "\n")
        changed |= write_if_changed(NOTES_DATA, json.dumps(sorted(base_notes.values(),
                    key=lambda n: n["date"], reverse=True), ensure_ascii=False, indent=1) + "\n")
        changed |= write_if_changed(POSTS_MD, render_posts_md(list(base_posts.values())))
        changed |= write_if_changed(NOTES_MD, render_notes_md(list(base_notes.values())))
        if not quiet:
            print(f"(file condivisi {'aggiornati' if changed else 'invariati'})")
    elif state_path:
        st = {
            "updated": datetime.datetime.now(datetime.timezone.utc)
            .isoformat(timespec="seconds").replace("+00:00", "Z"),
            "posts": {p["slug"]: p["date"] for p in posts},
            "notes": {n["key"]: n["date"] for n in notes},
        }
        for k, v in ((s, base_posts[s]["date"]) for s in base_posts):
            st["posts"].setdefault(k, v)
        for k in base_notes:
            st["notes"].setdefault(k, base_notes[k]["date"])
        pathlib.Path(state_path).write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())

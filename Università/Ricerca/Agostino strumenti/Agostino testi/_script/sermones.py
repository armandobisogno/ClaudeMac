# -*- coding: utf-8 -*-
"""Estrae i Sermones in ordine cronologico (stesso formato delle opere)."""
import json, re, sys, os, time, traceback
import build, parse
from fetch import get
from parse import parse_page, parse_notes, KEY
BASE = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi/Sermones"
build.SPECIAL = False; build.OUT = BASE; build.MD = os.path.join(BASE, "_md")
ORD = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sermones_ordine.json")))

def titolo(e):
    if e["coll"] == "main": return f"Sermo {e['label']}"
    if e["coll"] == "nuovi":
        c = e.get("code") or ""
        return f"Sermo {e['label']}" + (f" (= {c})" if c and c[0].isdigit() else " (De providentia Dei)" if c else "")
    return f"Sermo {e['label']}"
def meta(i, e):
    tv = e.get("tav") or {}
    if e["src"] == "Anoz":
        data = e["data"] + (f", {e['det']}" if e["det"] else "")
    elif e["src"] == "Tavola NBA":
        data = f"{e['data']} [Tavola NBA; non in Anoz]"
    else:
        data = "non datato" + (" (Anoz, «¿Cuándo?»)" if e["cuando"] else "")
    ita = titolo(e).replace("Sermo", "Discorso") + (f" — {tv['arg']}" if tv.get("arg") and tv["arg"] != "-" else "")
    nota = f"luogo: {tv['luogo']}" if tv.get("luogo") and tv["luogo"] not in ("-", "") else ""
    return (i, titolo(e), "s.", "discorsi/" + e["file"], ita, data, nota)

def loader(folder):
    fn = folder.split("/")[-1]
    out = {}
    for lang in ("latino", "italiano"):
        t = get(f"https://www.augustinus.it/{lang}/discorsi/{fn}")
        texts = []
        if t and KEY.search(t):
            pp = parse_page(t); pp["page"] = fn
            # un sermone = un solo "libro": uniforma il primo numero dell'ancora
            pp["items"] = [(it[0], (1,) + tuple(it[1][1:]), it[2]) if it[0] == "p" else it for it in pp["items"]]
            notes = {}
            for np_ in set(r[2] for it in pp["items"] for r in it[2] if r[0] == "n"):
                nt = get(f"https://www.augustinus.it/{lang}/discorsi/{np_}") if np_ else t
                if nt: notes.update({(np_ or fn, k): v for k, v in parse_notes(nt).items()})
            pp["notes"] = notes; texts.append(pp)
        out[lang] = dict(texts=texts, intro=[])
    return out

SERM = [meta(i + 1, e) for i, e in enumerate(ORD)]
build.OPERE = SERM
build.load_work = loader
import opere; opere.ITA_FOLDER = {}

if __name__ == "__main__":
    nums = [int(x) for x in sys.argv[1:]] or [m[0] for m in SERM]
    for n in nums:
        try:
            st = build.build(n)
            print(n, SERM[n-1][1], "par:", sum(s[1] for s in st), "/", sum(s[2] for s in st),
                  "non allineati:", sum(s[3] for s in st), "note:", sum(s[4] for s in st), flush=True)
        except Exception as ex:
            print(n, SERM[n-1][1], "ERRORE", repr(ex)[:150], flush=True); traceback.print_exc(file=sys.stderr)
    print("FINE", flush=True)

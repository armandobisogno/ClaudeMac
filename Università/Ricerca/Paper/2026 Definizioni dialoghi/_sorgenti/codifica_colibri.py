"""Codifica delle definizioni affidata a Colibri (Qwen3.6-35B-A3B in locale, API OpenAI su 127.0.0.1:8000).

Il modello riceve solo istruzioni_codifica.md (come messaggio di sistema) e il testo frase per frase,
a blocchi, come l'istanza nuova di Claude. Uso:
    python codifica_colibri.py acad2 [--blocco 40]
Legge _dati/istanza_nuova/frasi_<testo>.tsv e scrive _dati/colibri/codifica_<testo>.tsv.
Ogni blocco è salvato in _dati/colibri/<testo>/blocco_NNN.json: un nuovo avvio riprende dai blocchi mancanti.
"""
import json, sys, time, urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
URL = "http://127.0.0.1:8000/v1/chat/completions"
MODELLO = "qwen3.6-colibri"
TITOLI = {"acad1": "Contra Academicos, libro I", "acad2": "Contra Academicos, libro II",
          "acad3": "Contra Academicos, libro III", "bv": "De beata vita"}

testo = sys.argv[1]
n = int(sys.argv[sys.argv.index("--blocco") + 1]) if "--blocco" in sys.argv else 40
istr = (BASE / "_sorgenti/istruzioni_codifica.md").read_text(encoding="utf-8")
righe = (BASE / f"_dati/istanza_nuova/frasi_{testo}.tsv").read_text(encoding="utf-8").splitlines()
cart = BASE / f"_dati/colibri/{testo}"
cart.mkdir(parents=True, exist_ok=True)
blocchi = [righe[i:i + n] for i in range(0, len(righe), n)]

for k, b in enumerate(blocchi):
    f = cart / f"blocco_{k:03}.json"
    if f.exists():
        continue
    msgs = [{"role": "system", "content": istr},
            {"role": "user", "content": f"Testo da codificare ({TITOLI.get(testo, testo)}), una frase per riga:\n\n"
             + "\n".join(b) + "\n\nRispondi solo con il TSV (intestazione inclusa), senza commenti."}]
    t = time.time()
    req = urllib.request.Request(URL, json.dumps({"model": MODELLO, "messages": msgs, "temperature": 0,
                                                  "max_tokens": 3000}).encode(), {"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=7200))
    out = r["choices"][0]["message"]["content"]
    f.write_text(json.dumps({"blocco": k, "frasi": [x.split("\t")[0] for x in b], "secondi": round(time.time() - t),
                             "usage": r["usage"], "risposta": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"blocco {k + 1}/{len(blocchi)}  {round(time.time() - t)} s  {r['usage']}", flush=True)

# assemblaggio: tiene solo righe con riferimento appartenente al blocco e 5 colonne
validi, tot, scarti = set(x.split("\t")[0] for x in righe), ["frase\tind\tdefiniendum\tnuovo_ep\tnota"], []
for f in sorted(cart.glob("blocco_*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    for l in d["risposta"].strip().strip("`").splitlines():
        c = l.split("\t")
        if c[0] == "frase" or not l.strip():
            continue
        if c[0] in d["frasi"]:
            tot.append("\t".join((c + [""] * 5)[:5]))
        else:
            scarti.append(f"{f.name}: {l}")
(BASE / f"_dati/colibri/codifica_{testo}.tsv").write_text("\n".join(tot) + "\n", encoding="utf-8")
print(f"righe {len(tot) - 1}; scartate {len(scarti)}")
for s in scarti:
    print("  scartata:", s)

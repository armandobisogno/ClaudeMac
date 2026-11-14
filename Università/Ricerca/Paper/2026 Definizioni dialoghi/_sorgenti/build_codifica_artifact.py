"""Genera la pagina-artefatto per la codifica del De magistro, frase per frase (codebook bozza 4).
Frase = segmento chiuso da . ? ! ; i segmenti fatti di sola punteggiatura si uniscono alla frase precedente.
Testo latino dal corpus, battute separate, senza titoletti editoriali. Output in _dati/ (fuori da git)."""
import os, re, json
from corpus import paragrafi, HERE
SP = re.compile(r"^(AUGUSTINUS|ADEODATUS)\s*:\s*|^(Aug|Ad)\.\s*-\s*")
def frasi(b):
    out = []
    for f in re.split(r"(?<=[.?!])\s+", b):
        f = f.strip()
        if not f: continue
        if out and not re.search(r"\w", f): out[-1] += " " + f
        else: out.append(f)
    return out
pars, n = [], 0
for s, ref, t in paragrafi():
    if s != "mag.": continue
    t = re.sub(r"^\d+\.\s*\d+\.\s*", "", t)
    sents, who = [], ""
    for b in [x.strip() for x in t.split(" / ") if x.strip()]:
        m = SP.match(b)
        if m:
            who = "Aug." if (m.group(1) or m.group(2)).upper().startswith("AU") else "Ad."
            b = b[m.end():]
        for i, f in enumerate(frasi(b)):
            sents.append({"who": who, "text": f, "first": bool(m) and i == 0})
    n += len(sents); pars.append({"ref": ref, "sents": sents})
tpl = open(os.path.join(HERE, "codifica_template.html"), encoding="utf-8").read()
out = os.path.join(HERE, "..", "_dati", "codifica_magistro.html")
open(out, "w", encoding="utf-8").write(tpl.replace("__DATA__", json.dumps(pars, ensure_ascii=False).replace("</", "<\\/")))
print(len(pars), "paragrafi;", n, "frasi ->", os.path.normpath(out))
print(pars[0]["sents"][:2]); print([x["text"] for x in pars[1]["sents"] if len(x["text"])<4])

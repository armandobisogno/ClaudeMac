"""Genera la pagina-artefatto per la codifica del De magistro (testo latino dal corpus, battute separate,
senza titoletti editoriali). Output in _dati/ (fuori da git: contiene testo del corpus)."""
import os, re, json
from corpus import paragrafi, HERE
SP = re.compile(r"^(AUGUSTINUS|ADEODATUS)\s*:\s*|^(Aug|Ad)\.\s*-\s*")
pars = []
for s, ref, t in paragrafi():
    if s != "mag.": continue
    t = re.sub(r"^\d+\.\s*\d+\.\s*", "", t)
    turns = []
    for b in [x.strip() for x in t.split(" / ") if x.strip()]:
        m = SP.match(b); sp = ""
        if m:
            sp = "Aug." if (m.group(1) or m.group(2)).upper().startswith("AU") else "Ad."
            b = b[m.end():]
        turns.append({"sp": sp, "text": b})
    pars.append({"ref": ref, "turns": turns})
tpl = open(os.path.join(HERE, "codifica_template.html"), encoding="utf-8").read()
out = os.path.join(HERE, "..", "_dati", "codifica_magistro.html")
open(out, "w", encoding="utf-8").write(tpl.replace("__DATA__", json.dumps(pars, ensure_ascii=False).replace("</", "<\\/")))
print(len(pars), "paragrafi;", sum(len(p["turns"]) for p in pars), "battute ->", os.path.normpath(out))
print(pars[0]["turns"][:3])

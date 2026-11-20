"""Genera la pagina-artefatto per la codifica di controllo, frase per frase (codebook in vigore).
Frase = segmento chiuso da . ? ! ; i segmenti di sola punteggiatura si uniscono alla frase precedente.
Testo latino dal corpus, senza titoletti editoriali. Ogni testo ha le sue collezioni nell'archivio (prefisso NS).
Uso: python3 build_codifica_artifact.py [acad1|mag]   (default: acad1). Output in _dati/ (fuori da git)."""
import os, re, json, sys
from corpus import paragrafi, HERE
TESTI = {
  "acad1": dict(sigla="Acad.", libro="1", ns="", title="Codifica del Contra Academicos",
                h1="<i>Contra Academicos</i> I · codifica",
                prop=["", "Augustinus", "Licentius", "Trygetius", "Alypius", "Navigius", "autorità citata"], togli_rimandi=True),
  "mag":   dict(sigla="mag.", libro=None, ns="", title="Codifica del De magistro",
                h1="<i>De magistro</i> · codifica", prop=["", "Aug.", "Ad.", "autorità citata"]),
}
TESTI["acad1"]["ns"] = "acad1_"   # collezioni: acad1_frasi, acad1_episodi, acad1_tempo, acad1_stato
TESTI["mag"]["ns"] = ""           # il De magistro resta nelle collezioni originarie (frasi, episodi, tempo, stato)
SP = re.compile(r"^(AUGUSTINUS|ADEODATUS)\s*:\s*|^(Aug|Ad)\.\s*-\s*")
def frasi(b):
    out = []
    for f in re.split(r"(?<=[.?!])\s+", b):
        f = f.strip()
        if not f: continue
        if out and not re.search(r"\w", f): out[-1] += " " + f
        else: out.append(f)
    return out
key = sys.argv[1] if len(sys.argv) > 1 else "acad1"; cfg = TESTI[key]
pars, n = [], 0
for s, ref, t in paragrafi():
    if s != cfg["sigla"] or (cfg["libro"] and not ref.startswith(cfg["libro"] + ".")): continue
    t = re.sub(r"^\d+\.\s*\d+\.\s*", "", t)
    if cfg.get("togli_rimandi"):   # rimandi editoriali tra parentesi (con cifre): non sono testo di Agostino
        t = re.sub(r"\s*\([^()]*\d[^()]*\)", "", t)
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
J = lambda x: json.dumps(x, ensure_ascii=False).replace("</", "<\\/")
html = (tpl.replace("__DATA__", J(pars)).replace("__NS__", J(cfg["ns"])).replace("__PROP__", J(cfg["prop"]))
           .replace("__TITLE__", cfg["title"]).replace("__H1__", cfg["h1"]))
out = os.path.join(HERE, "..", "_dati", "codifica_magistro.html")   # stesso file = stesso artefatto
open(out, "w", encoding="utf-8").write(html)
print(key, len(pars), "paragrafi;", n, "frasi ->", os.path.normpath(out))

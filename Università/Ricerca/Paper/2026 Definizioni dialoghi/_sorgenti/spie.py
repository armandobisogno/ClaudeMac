"""Passo 1 della codifica: individuazione meccanica e larga delle spie A, B, C, D del codebook (bozza 3)
negli otto dialoghi. Output: _dati/spie_<sigla>.tsv (sigla, rif, codice, forma trovata, contesto).
Il passo 2 (lettura e schede) e' manuale/interpretativo e si registra a parte."""
import os, re
from collections import Counter, defaultdict
from corpus import paragrafi, HERE, OPERE
R = lambda p: re.compile(p, re.I)
SPIE = {
 "A1": R(r"\bdefini\w*|\bdefiniti\w*"),
 "A2": R(r"\bfinit(io|ion\w*)\b|\bfini(o|s|t|mus|tis|unt|re|vit|visti|vi|ri|atur|antur|endum|endo)\b"),
 "A3": R(r"\bdescri(b|p)\w*"),
 "A4": R(r"\b(vocem|vocamus|vocas|voco|appello|appellamus|appellas|nomino|nominamus|nominas)\b|\bhoc\s+nomine\b|\bvocabul\w*|\bnomen\b[^.?!]{0,60}\bsignific\w*"),
 "A5": R(r"\b(dicitur|dicuntur|vocatur|vocantur|appellatur|appellantur|nuncupatur|nuncupantur|nominatur)\b"),
 "B1": R(r"\bquid\s+(est|sit|esset|sint|sunt)\b|\bquaero\s+quid\b|\bquid\s+tibi\s+videtur\b|\bquis\s+(est|sit)\b"),
 "B3": R(r"\bnihil\s+aliud\s+(est|sit|esse|esset)?\s*quam\b|\bidem\s+(est|sit|esse)\b[^.?!]{0,40}\bquod\b"),
 "B4": R(r"\besse\s+(dico|puto|arbitror|censeo|existimo|iudico|definio)\b|\b(dico|puto|arbitror|censeo|existimo)\s+(\w+\s+){0,3}esse\b"),
 "B5": R(r"\bsapien(s|tem)\b[^.?!]{0,40}\b(est|erit|sit)\b[^.?!]{0,20}\bqui\b|\b(is|ille)\b[^.?!]{0,30}\bsapiens\b"),
 "B6": R(r"\b(id|hoc)\s+est\b"),
 "C1": R(r"\bplacet(ne)?\b|\baccipis\b|\bsic\s+defini\w*"),
 "C2": R(r"\bnum\s+etiam\b|\bergo\s+et\b"),
 "C3": R(r"\b(concedo|concedis|concessum|assentior|assentiris|verum\s+dicis|recte\s+dicis|ita\s+est|prorsus)\b"),
 "C4": R(r"\bnon\s+placet\b|\bfalsum\s+est\b|\bnon\s+concedo\b|\bnimium\b|\bminus\s+plenam?\b"),
 "C5": R(r"\badde\b|\baddendum\b|\bcorrig\w*|\bemend\w*"),
 "C6": R(r"\bdifferamus\b|\bdifferendum\b|\balias\b[^.?!]{0,30}\bquaer\w*|\bin\s+aliud\s+tempus\b"),
 "D?": R(r"\bdefinit(us|um|o|a|ae|is)\b"),
}
out = defaultdict(list); tot = Counter()
for s, ref, t in paragrafi():
    for cod, p in SPIE.items():
        for m in p.finditer(t):
            a, b = max(0, m.start()-80), min(len(t), m.end()+80)
            out[s].append((s, ref, cod, m.group(0), t[a:b].replace("\t", " ")))
            tot[(s, cod)] += 1
for f, s in OPERE:
    with open(os.path.join(HERE, "..", "_dati", f"spie_{s.replace(' ', '').replace('.', '')}.tsv"), "w", encoding="utf-8") as o:
        for x in out[s]: o.write("\t".join(x) + "\n")
codici = list(SPIE)
print("sigla       " + " ".join(f"{c:>4}" for c in codici))
for f, s in OPERE:
    if s == "mag.": continue  # De magistro: risultati non mostrati (codifica alla cieca in corso)
    print(f"{s:11} " + " ".join(f"{tot[(s,c)]:>4}" for c in codici))
print("(mag. calcolato ma non mostrato)")

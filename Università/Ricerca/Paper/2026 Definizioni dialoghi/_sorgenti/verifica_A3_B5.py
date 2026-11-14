"""Verifica sul corpus delle spie A3 (describo/descriptio) e B5 (is ... est qui; quisquis ...).
Produce in _dati/ un file .tsv per ciascuna spia (sigla, riferimento, frase) da leggere a mano."""
import os, re
from corpus import paragrafi, HERE
OUT = os.path.join(HERE, "..", "_dati")
def frasi(t):
    return [f.strip() for f in re.split(r"(?<=[.?!])\s+", t) if f.strip()]
A3 = re.compile(r"\bdescri(b|p)\w*", re.I)
B5 = [("quisquis/quicumque", re.compile(r"\b(quisquis|quicumque|quaecumque)\b", re.I)),
      ("is/ille ... est qui", re.compile(r"\b(is|ille|ea|illa)\s+(\w+\s+){0,2}(est|esse|sit|erit|videtur)\s*,?\s*(qui|quae)\b", re.I)),
      ("X est qui", re.compile(r"\b\w+(us|is|ens|ns)\s+(est|sit|erit)\s*,?\s*(qui|quae)\b", re.I))]
a3, b5 = [], []
for s, r, t in paragrafi():
    for f in frasi(t):
        if A3.search(f): a3.append((s, r, f))
        k = [n for n, p in B5 if p.search(f)]
        if k: b5.append((s, r, "+".join(k), f))
with open(os.path.join(OUT, "A3_describo.tsv"), "w", encoding="utf-8") as o:
    for x in a3: o.write("\t".join(x) + "\n")
with open(os.path.join(OUT, "B5_is_est_qui.tsv"), "w", encoding="utf-8") as o:
    for x in b5: o.write("\t".join(x) + "\n")
print("A3 frasi:", len(a3)); print("B5 frasi:", len(b5))
from collections import Counter
print(Counter(x[2] for x in b5))

"""B5: ricava dal corpus i 'tipi umani' come le parole per cui il testo stesso chiede 'quis est/sit X?'."""
import re, os
from corpus import paragrafi, HERE
Q = re.compile(r"\bquis\s+(?:\w+\s+){0,2}?(est|sit|esset|erit|fuerit|videtur|dicendus|dicatur|vocetur|appelletur)\b\s+(\w+)|\bquis\s+(\w+)\s+(est|sit|esset|erit)\b", re.I)
out = []
for s, r, t in paragrafi():
    for m in Q.finditer(t):
        a, b = max(0, m.start()-60), min(len(t), m.end()+90)
        out.append((s, r, m.group(0), t[a:b].replace("\t", " ")))
with open(os.path.join(HERE, "..", "_dati", "B5_domande_quis.tsv"), "w", encoding="utf-8") as o:
    for x in out: o.write("\t".join(x) + "\n")
for x in out: print(f"{x[0]} {x[1]} | {x[2]} | …{x[3]}…")
print(len(out))

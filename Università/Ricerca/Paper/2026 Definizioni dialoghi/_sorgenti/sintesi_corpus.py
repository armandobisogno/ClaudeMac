"""Sintesi della codifica dell'intero corpus (istanze nuove, codebook 11.2)."""
import csv, collections, re, os
B = os.path.dirname(os.path.abspath(__file__)) + "/../_dati/istanza_nuova/"
OPERE = [("Acad. I","b11","acad1"),("Acad. II","b11","acad2"),("Acad. III","b11","acad3"),("beata v.","b11","bv"),
         ("ord.","corpus","ord"),("sol.","corpus","sol"),("an. quant.","corpus","anquant"),("lib. arb. I","corpus","libarb1"),
         ("mag.","corpus","mag"),("mus. I-III","corpus","mus13"),("mus. IV-VI","corpus","mus46")]
tot = collections.Counter(); defs = collections.Counter(); verbi = collections.Counter(); defs_def = collections.Counter()
print("| Opera | Frasi | Segnate | 1 | 2 | 3 | P | Definizioni (1-3) ogni 100 frasi | P ogni 100 frasi |")
print("|---|---|---|---|---|---|---|---|---|")
for nome, d, k in OPERE:
    n = sum(1 for _ in open(B+f"{d}/frasi_{k}.tsv", encoding="utf-8"))
    R = list(csv.DictReader(open(B+f"{d}/codifica_{k}.tsv", encoding="utf-8"), delimiter="\t"))
    c = collections.Counter()
    for r in R:
        ind = set((r.get("ind") or "").split()); c["segnate"] += 1
        for i in "123P":
            if i in ind: c[i] += 1
        if ind & {"1","2","3"}: c["def"] += 1
        for p in (r.get("definiendum") or "").split(";"):
            p = p.strip().lower()
            if p:
                defs[p] += 1
                if ind & {"1","2","3"}: defs_def[p] += 1
        for part in (r.get("nota") or "").split(";"):
            v = part.split(":")[-1].strip().split("(")[0].strip().split(",")[0].strip()
            if v and ind & {"2","3"}: verbi[v.lower()] += 1
    tot.update(c); tot["frasi"] += n
    print(f"| {nome} | {n} | {c['segnate']} | {c['1']} | {c['2']} | {c['3']} | {c['P']} | {100*c['def']/n:.1f} | {100*c['P']/n:.1f} |")
n = tot["frasi"]
print(f"| **Totale** | {n} | {tot['segnate']} | {tot['1']} | {tot['2']} | {tot['3']} | {tot['P']} | {100*tot['def']/n:.1f} | {100*tot['P']/n:.1f} |")
print("\nDefinienda più frequenti nelle frasi con 1-3 (forma del testo, minuscolo):")
print(", ".join(f"{d} {c}" for d, c in defs_def.most_common(30)))
print("\nVerbi delle note (frasi con 2 o 3):")
print(", ".join(f"{v} {c}" for v, c in verbi.most_common(30)))

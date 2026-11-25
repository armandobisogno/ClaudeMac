"""Definienda per lemma nell'intero corpus (frasi con 1-3 e con P), dopo la riconduzione al lemma."""
import csv, collections, os
H=os.path.dirname(os.path.abspath(__file__)); B=H+"/../_dati/istanza_nuova/"
L={r["forma"]:(r["lemma"],r["tipo"]) for r in csv.DictReader(open(H+"/../_dati/lemmi_definienda.tsv",encoding="utf-8"),delimiter="\t")}
F=[("b11",k) for k in ("acad1","acad2","acad3","bv")]+[("corpus",k) for k in ("ord","sol","anquant","libarb1","mag","mus13","mus46")]
D=collections.Counter(); P=collections.Counter(); opere=collections.defaultdict(set)
for d,k in F:
    for r in csv.DictReader(open(B+f"{d}/codifica_{k}.tsv",encoding="utf-8"),delimiter="\t"):
        ind=set((r.get("ind") or "").split())
        for f in (r.get("definiendum") or "").split(";"):
            f=f.strip()
            if not f: continue
            lem,tipo=L.get(f,(f,"?"))
            if tipo=="rinvio" and lem==f: continue
            if ind&{"1","2","3"}: D[lem]+=1; opere[lem].add({"acad1":"Acad","acad2":"Acad","acad3":"Acad","mus13":"mus","mus46":"mus"}.get(k,k))
            if "P" in ind: P[lem]+=1
print("Lemmi con definizioni (1-3):",len(D))
print("\nI 30 lemmi più definiti (frasi 1-3; tra parentesi: frasi P; numero di opere):")
for l,c in D.most_common(30): print(f"{l}: {c} (P {P[l]}; opere {len(opere[l])})")
print("\nLemmi definiti in almeno 4 opere:", ", ".join(sorted(l for l in D if len(opere[l])>=4)))

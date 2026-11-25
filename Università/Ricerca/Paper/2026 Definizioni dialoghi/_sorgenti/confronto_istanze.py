"""Confronto tra due codifiche TSV (frase, ind, definiendum, nuovo_ep, nota) sullo stesso testo frase per frase."""
import csv, sys
def load(p):
    return {r["frase"]: r for r in csv.DictReader(open(p, encoding="utf-8"), delimiter="\t")}
def kappa(x, y):
    n=len(x); po=sum(a==b for a,b in zip(x,y))/n; px=sum(x)/n; py=sum(y)/n; pe=px*py+(1-px)*(1-py)
    return po, ((po-pe)/(1-pe) if pe<1 else 1.0)
frasi, a, b = sys.argv[1], load(sys.argv[2]), load(sys.argv[3])
refs=[l.split("\t")[0] for l in open(frasi, encoding="utf-8").read().splitlines()]
txt={l.split("\t")[0]: l.split("\t")[2] for l in open(frasi, encoding="utf-8").read().splitlines()}
ind=lambda d,r: set((d.get(r) or {}).get("ind","").split())
print(f"frasi {len(refs)}")
for lab, S in [("1-3", {"1","2","3"}), ("1", {"1"}), ("2", {"2"}), ("3", {"3"}), ("T", {"T"}), ("P", {"P"}), ("qualunque (1-3, T o P)", {"1","2","3","T","P"})]:
    x=[bool(ind(a,r)&S) for r in refs]; y=[bool(ind(b,r)&S) for r in refs]
    po,k=kappa(x,y); both=sum(p and q for p,q in zip(x,y))
    print(f"{lab:22} A {sum(x):3}  B {sum(y):3}  entrambi {both:3}  accordo {po:.3f}  kappa {k:.3f}")
da={p.strip().lower() for r in refs if ind(a,r) & {"1","2","3"} for p in a[r]["definiendum"].split(";") if p.strip()}
db={p.strip().lower() for r in refs if ind(b,r) & {"1","2","3"} for p in b[r]["definiendum"].split(";") if p.strip()}
print(f"definienda (frasi 1-3): A {len(da)}  B {len(db)}  comuni {len(da&db)}")
if "-v" in sys.argv:
    for r in refs:
        x,y=ind(a,r)-{""},ind(b,r)-{""}
        if (x&{"1","2","3"})!=(y&{"1","2","3"}):
            print(f"{r}\tA={' '.join(sorted(x)) or '-'} [{(a.get(r) or {}).get('definiendum','')}]\tB={' '.join(sorted(y)) or '-'} [{(b.get(r) or {}).get('definiendum','')}]\t{txt[r][:110]}")

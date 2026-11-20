import json,glob,os,re,csv
D="/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Paper/2026 Definizioni dialoghi/_dati/"
def ref(i):
    a,b,c,k=re.match(r"s(\d+)_(\d+)_(\d+)-(\d+)",i).groups(); return f"{a}.{b}.{c}.{k}"
A={}
for f in glob.glob("db4/acad1_frasi/*.json"):
    v=json.load(open(f)); A[ref(os.path.basename(f)[:-5])]=v
C={}
for r in csv.DictReader(open(D+"codifica_claude_acad1.tsv"),delimiter="\t"):
    C[r["frase"]]={"spie":r["ind"].split(),"def":r["definiendum"],"nota":r["nota"]}
S=[l.split("\t") for l in open("acad1_frasi.tsv").read().splitlines()]
refs=[s[0] for s in S]; TXT={s[0]:s[2] for s in S}
def sp(d,r): return set((d.get(r) or {}).get("spie",[]))
N=len(refs)
# presenza di indicatori
a=[bool(sp(A,r)) for r in refs]; c=[bool(sp(C,r)) for r in refs]
def kappa(x,y):
    n=len(x); po=sum(p==q for p,q in zip(x,y))/n
    px=sum(x)/n; py=sum(y)/n; pe=px*py+(1-px)*(1-py); return po,(po-pe)/(1-pe)
po,k=kappa(a,c)
both=sum(p and q for p,q in zip(a,c)); onlyA=sum(p and not q for p,q in zip(a,c)); onlyC=sum(q and not p for p,q in zip(a,c))
print(f"frasi {N}; con indicatori: A {sum(a)}, C {sum(c)}; entrambi {both}, solo A {onlyA}, solo C {onlyC}, nessuno {N-both-onlyA-onlyC}")
print(f"accordo presenza {po:.3f}, kappa {k:.3f}")
for ind in "123":
    x=[ind in sp(A,r) for r in refs]; y=[ind in sp(C,r) for r in refs]
    po,k=kappa(x,y); print(f"ind {ind}: A {sum(x)} C {sum(y)} entrambi {sum(p and q for p,q in zip(x,y))} accordo {po:.3f} kappa {k:.3f}")
same=sum(1 for r in refs if sp(A,r) and sp(A,r)==sp(C,r)); print("frasi con stessi identici indicatori:",same,"su",both)
print("\n== DISACCORDI")
for r in refs:
    x,y=sp(A,r),sp(C,r)
    if x!=y:
        tag="solo A" if not y else "solo C" if not x else "diversi"
        print(f"{r}\t{tag}\tA={' '.join(sorted(x)) or '-'} [{A.get(r,{}).get('def','')} | {A.get(r,{}).get('nota','')}]\tC={' '.join(sorted(y)) or '-'} [{C.get(r,{}).get('def','')} | {C.get(r,{}).get('nota','')}]\t{TXT[r][:150]}")
print("\n== DEFINIENDA a confronto (frasi con indicatori in entrambi)")
for r in refs:
    if sp(A,r) and sp(C,r):
        print(f"{r}\tA: {A[r].get('def','')}\tC: {C[r]['def']}")
t=sum((json.load(open(f)).get('attivo_s',0)) for f in glob.glob('db4/acad1_tempo/*.json'))
print("\ntempo",t,round(t/60,1))
print("frasi annotate A (con qualunque campo):",len(A),"; senza indicatori:",[r for r in A if not sp(A,r)])

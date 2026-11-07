# -*- coding: utf-8 -*-
"""Elenco cronologico delle Epistulae: sito (file), Anoz (date), Tavola NBA (fallback + mittente/destinatario)."""
import re, html, json, collections
def norm(x):
    x=x.strip().replace(" ","").replace("/","").upper()
    if "*" in x: x=x.replace("*","")+"*"
    return x
t=open("lett_som_latino.htm",encoding="cp1252",errors="replace").read()
site=[dict(file=f,label=l.strip(),id=norm(l)) for f,l in re.findall(r'<option value="([^"]+)">([^<]*)</option>',t,re.I)]
t=open("tavola_lettere_it.htm",encoding="cp1252",errors="replace").read()
tav={}
for r in re.findall(r"<tr[^>]*>(.*?)</tr>",t,re.I|re.S):
    c=[re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",x))).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>",r,re.I|re.S)]
    m=re.match(r"\[\s*(\d+)\s*\]",c[0]) if c else None
    if m and len(c)>=6:
        tav[int(m.group(1))]=dict(mitt=c[2],dest=c[3],luogo=c[4],data=c[5])
anoz={}; seq=0
for line in open("anoz_lettere.txt",encoding="utf-8"):
    if line.startswith("#") or not line.strip(): continue
    d,det,ss=[x.strip() for x in line.split("|")]
    for s in ss.split(";"):
        seq+=1; anoz[norm(s)]=dict(seq=seq,data=d,det=det)
CUANDO={norm(x) for x in "8*;13*;18*;171A;185A;246".split(";")}
def first_year(s):
    ys=[int(y) for y in re.findall(r"\b(3[89]\d|4[0-3]\d)\b",s)]
    return ys[0] if ys else None
out=[]
for e in site:
    n=int(re.search(r"(\d+)",e["file"]).group(1))
    tv=tav.get(n,{}); e["tav"]=tv
    a=anoz.get(e["id"])
    if a:
        e.update(src="Anoz",data=a["data"],det=a["det"],key=(first_year(a["data"]) or 9999,a["seq"]))
    elif tv and first_year(tv.get("data","")):
        e.update(src="Tavola NBA",data=tv["data"],det="",key=(first_year(tv["data"]),100000))
    else:
        e.update(src="non datata",data="",det="",key=(9999,0))
    e["cuando"]=e["id"] in CUANDO
    out.append(e)
def numkey(e):
    m=re.match(r"(\d+)([A-Z]?)(\*?)",e["id"]); return (1 if "*" in e["id"] else 0,int(m.group(1)),m.group(2))
out.sort(key=lambda e:(e["key"],numkey(e)))
json.dump(out,open("lettere_ordine.json","w"),ensure_ascii=False,indent=0)
print(len(out),collections.Counter(e["src"] for e in out))
print("Anoz non trovate nel sito:",sorted(k for k in anoz if k not in {e["id"] for e in out}))
print("non datate:",[e["label"] for e in out if e["src"]=="non datata"])

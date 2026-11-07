# -*- coding: utf-8 -*-
"""Elenco cronologico dei Sermones: siti (file), Anoz (date), Tavola NBA (fallback)."""
import re, html, json
def opts(f):
    t=open(f,encoding="cp1252",errors="replace").read()
    return re.findall(r'<option value="([^"]+)">([^<]*)</option>',t,re.I)
def norm(x):
    x=x.strip().replace("augm.","AUG").replace("/","").replace(" ","")
    return x.upper() if not x.isdigit() else x
# 1. voci del sito
site=[]
for f,lab in opts("som_latino.htm"):
    site.append(dict(file=f,label=lab.strip(),id=norm(lab),coll="main"))
tab=open("discorsi_nuovi_tabella_italiano.htm",encoding="cp1252",errors="replace").read()
tabtxt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",tab)))
nuovi_code=dict(re.findall(r"((?:Dolbeau|Étaix) \d+) (\d+(?:/[A-Z])?(?: augm\.)?|Discorso sulla provvidenza di Dio)",tabtxt))
for f,lab in opts("discorsi_nuovi_sommario_latino.htm"):
    lab=lab.strip(); code=nuovi_code.get(lab,"")
    site.append(dict(file=f,label=lab,code=code,coll="nuovi"))
for f,lab in opts("discorsi_erfurt_sommario_latino.htm"):
    site.append(dict(file=f,label=lab.strip(),coll="erfurt"))
# 2. Tavola NBA
t=open("tavola_discorsi_italiano.htm",encoding="cp1252",errors="replace").read()
tav={}
for r in re.findall(r"<tr[^>]*>(.*?)</tr>",t,re.I|re.S):
    c=[re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",x))).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>",r,re.I|re.S)]
    if len(c)>=4 and re.match(r"^\d+(/[A-Z])?$",c[0]):
        tav[norm(c[0])]=dict(arg=c[1],luogo=c[2],data=c[3])
# 3. Anoz
anoz={}; seq=0
for line in open("anoz_sermoni.txt",encoding="utf-8"):
    if line.startswith("#") or not line.strip(): continue
    d,det,ss=[x.strip() for x in line.split("|")]
    for s in ss.split(";"):
        seq+=1
        for alias in s.strip().split("="):
            anoz[alias.strip().upper()]=dict(seq=seq,data=d,det=det)
CUANDO="16;18;20B;22A;39;41;42;49A;60A;62A;63B;64A;65;66;70A;74;77B;77C;78;79A;95;97;102;105A;106;108;109;113;122;123;136A;136C;140A;141;162;167A;171;172;176A;199;204;204A;210;219;220;222;223B;223C;223D;223G;223H;223I;223J;223K;228;229B;229C;230;236A;265C;265E;272A;280;281;282;293C;293D;293E;299F;306D;308;319A;326;329;331;334;335D;335G;335I;335K;335L;335M;336;338;341A;342;346;350B;367;370;375;377;378;379;389;395".split(";")
def first_year(s):
    ys=[int(y) for y in re.findall(r"\b(3[89]\d|4[0-3]\d)\b",s)]
    return ys[0] if ys else None
out=[]
for e in site:
    keys=[]
    if e["coll"]=="main":
        keys=[e["id"]]
    elif e["coll"]=="nuovi":
        m=re.match(r"Dolbeau (\d+)",e["label"])
        if m: keys.append("D"+m.group(1))
        code=e.get("code","")
        if code.endswith("augm."): keys.append(norm(code))
        elif code and code[0].isdigit(): keys.append(norm(code))
    ext=[]
    for k in keys:   # forma breve <-> ampliata: stesso sermone per Anoz
        ext.append(k)
        if k.endswith("AUG"): ext.append(k[:-3])
        else: ext.append(k+"AUG")
    a=next((anoz[k] for k in ext if k in anoz),None)
    tv=None
    tk=norm(e["code"]).replace("AUG","") if e["coll"]=="nuovi" and e.get("code","")[:1].isdigit() else (e["id"] if e["coll"]=="main" else None)
    if tk and tk.replace("AUG","") in tav: tv=tav[tk.replace("AUG","")]
    if a:
        e.update(src="Anoz",data=a["data"],det=a["det"],key=(first_year(a["data"]) or 9999,a["seq"]))
    elif tv and first_year(tv["data"]):
        e.update(src="Tavola NBA",data=tv["data"],det="",key=(first_year(tv["data"]),100000))
    else:
        e.update(src="non datato",data="",det="",key=(9999,0))
    e["tav"]=tv
    e["cuando"]= any(k in CUANDO for k in keys)
    out.append(e)
def numkey(e):
    m=re.match(r"(\d+)([A-Z]?)",e.get("id") or re.sub(r"\D","",e["label"]) or "0")
    return (0 if e["coll"]=="main" else 1 if e["coll"]=="nuovi" else 2, int(m.group(1)) if m else 0, m.group(2) if m else "")
out.sort(key=lambda e:(e["key"],numkey(e)))
json.dump(out,open("sermones_ordine.json","w"),ensure_ascii=False,indent=0)
import collections
print(len(out), collections.Counter(e["src"] for e in out))
print("Anoz non trovati nel sito:", sorted(k for k in anoz if not any(k==x.get("id") for x in out) and not k.startswith("D") and not k.endswith("AUG")) )

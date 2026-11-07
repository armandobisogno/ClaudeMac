# -*- coding: utf-8 -*-
"""Parser generico per le opere di augustinus.it (latino/italiano)."""
import re, html, os, json, glob
HERE=os.path.dirname(os.path.abspath(__file__))
RAW=os.path.join(HERE,"raw")
from fetch import crawl

def raw(lang, work, pg):
    p=os.path.join(RAW,f"{lang}__{work}__{pg}")
    if not os.path.exists(p): return None
    b=open(p,"rb").read()
    if b==b"__404__": return None
    return b.decode("cp1252","replace")

def body(t):
    lo=t.lower(); a=lo.find("<body")
    a=t.find(">",a)+1 if a>=0 else 0
    b=lo.find("</body>"); b=b if b>=0 else len(t)
    return t[a:b]

BLOCK=re.compile(r"<(h[1-6]|p)\b[^>]*>(.*?)</\1\s*>", re.I|re.S)
KEY=re.compile(r'<a\s+name\s*=\s*"?([A-Za-z]+)_(\d{3})_(\d{3})_(\d{3})', re.I)
NOTE=re.compile(r'<a\s+[^>]*href\s*=\s*"([^"#]*)#N(\d+)"[^>]*>.*?</a>', re.I|re.S)

def plain(s):
    s=re.sub(r"<[^>]+>","",s); s=html.unescape(s).replace("\xa0"," ")
    return re.sub(r"\s+"," ",s).strip()

def to_runs(s):
    """-> list of ('t',text,bold,ital) / ('n',num,page)"""
    s=NOTE.sub(lambda m:"\x00N%s|%s\x00"%(m.group(2),m.group(1)), s)
    s=re.sub(r"<br\s*/?>","\x01",s,flags=re.I)
    s=re.sub(r"</?(?:a|u|sup|sub|font|span|h[1-6]|p|div|strong|em\b)[^>]*>","",s,flags=re.I)
    parts=re.split(r"(<i>|</i>|<b>|</b>|\x00N[^\x00]+\x00)", s, flags=re.I)
    b=i=0; out=[]
    for p in parts:
        if not p: continue
        pl=p.lower()
        if pl=="<i>": i+=1; continue
        if pl=="</i>": i=max(0,i-1); continue
        if pl=="<b>": b+=1; continue
        if pl=="</b>": b=max(0,b-1); continue
        m=re.match(r"\x00N(\d+)\|([^\x00]*)\x00",p)
        if m: out.append(("n",m.group(1),m.group(2))); continue
        txt=html.unescape(re.sub(r"<[^>]+>","",p)).replace("\xa0"," ")
        txt=re.sub(r"[ \t\r\n]+"," ",txt).replace("\x01","\n")
        if txt: out.append(("t",txt,bool(b),bool(i)))
    # tidy whitespace
    ti=[k for k,r in enumerate(out) if r[0]=="t"]
    if ti:
        f=ti[0]; out[f]=("t",out[f][1].lstrip(" \n"),out[f][2],out[f][3])
        l=ti[-1]; out[l]=("t",out[l][1].rstrip(" \n"),out[l][2],out[l][3])
    return [r for r in out if r[0]!="t" or r[1]]

def runs_text(runs, notes=True):
    s=""
    for r in runs:
        if r[0]=="t": s+=r[1]
        elif notes: s+="[n%s]"%r[1]
    return re.sub(r"[ \t]+"," ",s).strip()

def parse_page(t):
    """-> dict(head=[(tag,text)], items=[...])
    items: ('h',level,runs) | ('p',key,runs) | ('c',None,runs) continuation"""
    bd=body(t)
    head=[]; items=[]; seen_key=False; pending_key=None
    blocks=[]
    for m in BLOCK.finditer(bd):
        tag=m.group(1).lower(); inner=m.group(2)
        ks=[k.start() for k in KEY.finditer(inner)]
        if tag=="p" and len(ks)>1:
            cuts=[0]+ks[1:]+[len(inner)]
            for a,b in zip(cuts,cuts[1:]):
                blocks.append((tag,inner[a:b],m.start()))
        else:
            blocks.append((tag,inner,m.start()))
    for tag,inner,mstart in blocks:
        txt=plain(inner)
        if not txt: continue
        km=KEY.search(inner)
        if km and tag.startswith("h"):
            # ancora nel titolo: vale per il paragrafo seguente
            pending_key=(int(km.group(2)),int(km.group(3)),int(km.group(4)))
            items.append(("h",int(tag[1]),to_runs(inner))); continue
        if not km and tag=="p" and pending_key is not None:
            seen_key=True
            items.append(("p",pending_key,to_runs(inner))); pending_key=None; continue
        if not seen_key and not km and len(txt)>3 and txt.upper()==txt and any(c.isalpha() for c in txt):
            head.append((tag,txt)); continue
        if tag.startswith("h"):
            lvl=int(tag[1])
            if not seen_key and not items and lvl<=3:
                head.append((tag,txt)); continue
            items.append(("h",lvl,to_runs(inner))); continue
        if km:
            seen_key=True
            key=(int(km.group(2)),int(km.group(3)),int(km.group(4)))
            items.append(("p",key,to_runs(inner))); continue
        pre=bd[max(0,mstart-40):mstart].lower()
        il=inner.lower()
        small=("size=2" in pre.replace('"','') or "size=\"2\"" in pre) or (il.rstrip().endswith("</font>") and "<font" not in il)
        if not seen_key and not items and txt.upper()==txt:
            head.append(("p",txt)); continue
        if not seen_key and not small:
            items.append(("h",4,to_runs(inner))); continue
        if small:
            items.append(("h",6,to_runs(inner)))   # rubrica
        else:
            items.append(("c",None,to_runs(inner)))
    return dict(head=head, items=items)

def parse_notes(t):
    bd=body(t); notes={}
    for m in re.finditer(r'<a\s+name\s*=\s*"?N(\d+)"?[^>]*>.*?</a>(.*?)(?=<a\s+name\s*=\s*"?N\d+|$)', bd, re.I|re.S):
        txt=plain(m.group(2)); txt=re.sub(r"^[-–—.\s]+","",txt)
        notes[int(m.group(1))]=txt
    return notes

def load_work(work):
    """Return dict with per-language pages parsed, notes, intro."""
    from opere import ITA_FOLDER
    out={}
    base=work
    for lang in ("latino","italiano"):
        work=ITA_FOLDER.get(base,base) if lang=="italiano" else base
        pages=crawl(lang,work)
        texts=[]; intro=[]
        for pg in pages:
            t=raw(lang,work,pg)
            if t is None or re.search(r"<frameset",t,re.I): continue
            if pg in("sommario.htm","copertina.htm","index.htm","index2.htm"): continue
            if pg.endswith("_note.htm") or "indice" in pg: continue
            if KEY.search(t):
                pp=parse_page(t); pp["page"]=pg
                # notes
                npages=set(r[2] for it in pp["items"] for r in it[2] if r[0]=="n")
                notes={}
                for np_ in npages:
                    nt=raw(lang,work,np_ or pg) if np_ else t
                    if nt is None: continue
                    for k,v in parse_notes(nt).items(): notes[(np_ or pg,k)]=v
                pp["notes"]=notes
                texts.append(pp)
            elif lang=="italiano" and re.search(r"_0\.htm$",pg):
                bd=body(t)
                intro+= [(m.group(1).lower(),plain(m.group(2))) for m in BLOCK.finditer(bd) if plain(m.group(2))]
        out[lang]=dict(texts=texts,intro=intro)
    return out

if __name__=="__main__":
    import sys, collections
    for w in sys.argv[1:]:
        d=load_work(w)
        for lang in ("latino","italiano"):
            L=d[lang]
            cnt=collections.Counter(); 
            for pp in L["texts"]:
                for it in pp["items"]: cnt[it[0] if it[0]!="h" else "h%d"%it[1]]+=1
            nn=sum(len(pp["notes"]) for pp in L["texts"])
            print(f"{w:22s} {lang[:3]} pages={len(L['texts'])} {dict(cnt)} notes={nn} intro={len(L['intro'])}")
            for pp in L["texts"][:1]:
                print("    HEAD:", pp["head"][:4])

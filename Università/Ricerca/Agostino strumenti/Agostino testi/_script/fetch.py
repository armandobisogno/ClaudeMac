import re, os, sys, time, urllib.request, json
BASE="https://www.augustinus.it"
RAW=os.path.join(os.path.dirname(os.path.abspath(__file__)),"raw")
os.makedirs(RAW,exist_ok=True)
def get(url):
    p=os.path.join(RAW, url.replace(BASE+"/","").replace("/","__"))
    if os.path.exists(p):
        b=open(p,"rb").read()
        return None if b==b"__404__" else b.decode("cp1252","replace")
    b=None
    for i in range(3):
        try:
            r=urllib.request.urlopen(url,timeout=40); b=r.read(); break
        except urllib.error.HTTPError as e:
            if e.code==404: open(p,"wb").write(b"__404__"); return None
            time.sleep(2)
        except Exception as e:
            time.sleep(2)
    if b is None: return None
    open(p,"wb").write(b); time.sleep(0.1)
    return b.decode("cp1252","replace")
REF=re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)
SKIP={"titolo.htm"}
def crawl(lang, work):
    root=f"{BASE}/{lang}/{work}/"
    seen=[]; 
    def visit(pg):
        if pg in seen: return
        t=get(root+pg)
        if t is None: return
        seen.append(pg)
        for h in REF.findall(t):
            h0=h.split("#")[0].strip()
            if not h0 or "/" in h0 or ":" in h0 or not h0.lower().endswith(".htm"): continue
            if h0.lower() in SKIP or h0 in seen: continue
            visit(h0)
    visit("index.htm")
    return seen
if __name__=="__main__":
    res={}
    for spec in sys.argv[1:]:
        for lang in ("latino","italiano"):
            r=crawl(lang,spec); res[f"{lang}/{spec}"]=r
            print(lang,spec,len(r),r[:12], flush=True)
    json.dump(res,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"crawl_%d.json"%os.getpid()),"w"))

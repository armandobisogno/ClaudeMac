#!/usr/bin/env python3
"""Costruisce i dati dell'app web «Scrinium Augustini» dai file _md del corpus.

Uscita in ../_web/data/:
  catalog.json            metadati di tutti i documenti (opere, sermoni, lettere)
  {O,S,E}-refs.gz.txt     per documento: riferimenti dei paragrafi + titoletti
  {O,S,E}-la.gz.txt       per documento: testo latino dei paragrafi (allineato ai refs)
  {O,S,E}-it.gz.txt       per documento: testo italiano dei paragrafi
  {O,S,E}-notes.gz.txt    per documento: note [indice paragrafo, n, testo]

(file gzip codificati in base64: gli artifact non servono .gz)

Uso: python3 web_build.py
"""
import base64, gzip, json, re, sys, urllib.parse
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "_web" / "data"
OUT.mkdir(parents=True, exist_ok=True)

WORD = re.compile(r"[^\W\d_]+")
YEAR = re.compile(r"(?<!\d)(3[5-9]\d|4[0-3]\d)(?!\d)")


def table_rows(md):
    rows = []
    for line in md.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\| \d+ \|", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def link_path(cell):
    m = re.search(r"\]\((.+)\)\s*$", cell)
    return BASE / urllib.parse.unquote(m.group(1)) if m else None


def years(dating):
    seg = dating.split(";")[0]
    ys = [int(y) for y in YEAR.findall(seg)]
    if not ys:
        ys = [int(y) for y in YEAR.findall(dating)]
    if not ys:
        return None, None
    return ys[0], max(ys)


REF_LINE = re.compile(r"^\[([^\]\sn][^\]]*)\] (LA|IT): ?(.*)$")
NOTE_LINE = re.compile(r"^\[n(\d+) @([^\]]+)\] ?(.*)$")


def parse_doc(path):
    refs, la, it, heads, notes = [], [], [], [], []
    ref_idx = {}
    in_intro = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_intro = line.startswith("## Introduzione")
            if not in_intro:
                heads.append([len(refs), 2, line[3:].strip()])
            continue
        if in_intro:
            # opere in un solo libro: l'introduzione finisce al primo titoletto o paragrafo
            if line.startswith("#### ") or REF_LINE.match(line):
                in_intro = False
            else:
                continue
        if line.startswith("### "):
            continue  # "### Note — LIBRO I"
        if line.startswith("#### "):
            heads.append([len(refs), 4, line[5:].strip()])
            continue
        m = NOTE_LINE.match(line)
        if m:
            n, ref, txt = m.groups()
            pi = ref_idx.get(ref)
            if pi is None:
                pi = ref_idx.get(ref.split(".")[0], -1)
            notes.append([pi, int(n), txt.strip()])
            continue
        m = REF_LINE.match(line)
        if not m:
            continue
        ref, lang, txt = m.groups()
        txt = txt.strip()
        cur = len(refs) - 1
        if lang == "LA":
            if cur >= 0 and refs[cur] == ref and not la[cur] and it[cur]:
                la[cur] = txt
            else:
                refs.append(ref); la.append(txt); it.append("")
        else:
            if cur >= 0 and refs[cur] == ref and not it[cur]:
                it[cur] = txt
            else:
                refs.append(ref); la.append(""); it.append(txt)
        ref_idx.setdefault(ref, len(refs) - 1)
    # titoletti in coda senza paragrafo successivo
    heads = [h for h in heads if h[0] < len(refs)]
    return refs, la, it, heads, notes


def words(texts):
    return sum(len(WORD.findall(t)) for t in texts)


def main():
    catalog = []
    shards = {k: {"refs": [], "la": [], "it": [], "notes": []} for k in "OSE"}

    def add(corpus, meta, path):
        refs, la, it, heads, notes = parse_doc(path)
        sh = shards[corpus]
        meta.update(
            id=f"{corpus}{meta['n']}",
            c=corpus,
            i=len(sh["refs"]),
            np=len(refs),
            wla=words(la),
            wit=words(it),
        )
        sh["refs"].append([refs, heads])
        sh["la"].append(la)
        sh["it"].append(it)
        sh["notes"].append(notes)
        catalog.append(meta)

    for r in table_rows(BASE / "0. Elenco cronologico delle opere.md"):
        n, opera, tit, sigla, dat, note, link = r[:7]
        y0, y1 = years(dat)
        add("O", dict(n=int(n), t=opera.strip("*"), ti=tit, s=sigla, d=dat, y0=y0, y1=y1, tag=note), link_path(link))

    for r in table_rows(BASE / "0. Elenco cronologico dei sermoni.md"):
        n, name, arg, dat, luogo, link = r[:6]
        y0, y1 = years(dat)
        sig = re.sub(r"^Sermo\s+", "s. ", name)
        add("S", dict(n=int(n), t=name, ti=arg, s=sig, d=dat, y0=y0, y1=y1, pl=luogo), link_path(link))

    for r in table_rows(BASE / "0. Elenco cronologico delle lettere.md"):
        n, name, md, dat, luogo, link = r[:6]
        y0, y1 = years(dat)
        sig = re.sub(r"^Epistula\s+", "ep. ", name)
        m = re.match(r"^(.*?) a (.*)$", md)
        frm, to = (m.group(1), m.group(2)) if m else (md, "")
        aug = frm.startswith("Agostino")
        add("E", dict(n=int(n), t=name, ti=md, s=sig, d=dat, y0=y0, y1=y1, pl=luogo, aug=aug), link_path(link))

    for k, sh in shards.items():
        for part, data in sh.items():
            raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            # base64 in .txt: gli artifact di claude.ai non servono file .gz
            (OUT / f"{k}-{part}.gz.txt").write_bytes(base64.b64encode(gzip.compress(raw, 9)))
    (OUT / "catalog.json").write_text(
        json.dumps({"built": __import__("datetime").date.today().isoformat(), "docs": catalog},
                   ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    tot = sum(d["np"] for d in catalog)
    print(f"{len(catalog)} documenti, {tot} paragrafi")
    for f in sorted(OUT.iterdir()):
        print(f"  {f.name:24} {f.stat().st_size/1e6:6.2f} MB")


if __name__ == "__main__":
    main()

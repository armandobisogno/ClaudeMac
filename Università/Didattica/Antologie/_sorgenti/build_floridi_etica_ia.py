# -*- coding: utf-8 -*-
"""Antologia-lezione: L. Floridi, Etica dell'intelligenza artificiale (Cortina 2022).

I passi sono estratti alla lettera dall'epub (frase d'inizio + frase di fine);
se una frase non si trova, lo script si ferma. Anche ogni citazione tra «»
nelle chiavi, nelle introduzioni e in copertina deve trovarsi alla lettera nel libro.
Il paragrafo (es. 2.4) è ricavato in automatico dall'intestazione che precede il passo.

Uso:  python3 build_floridi_etica_ia.py [--no-pdf]
"""
import re, html, subprocess, pathlib, sys, zipfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # ClaudeWS
NOME = "Etica dell’intelligenza artificiale. Sviluppi, opportunità, sfide{Luciano Floridi}(2022, Raffaello Cortina){97561375} libgen.li.epub"
CANDIDATI = [ROOT / "Università/Ricerca/Biblioteca" / NOME, ROOT / "Documenti di passaggio" / NOME]
EPUB = next((p for p in CANDIDATI if p.exists()), None) or sys.exit("epub non trovato")
OUT_HTML = HERE / "floridi_etica_ia_antologia.html"
OUT_PDF = HERE.parent / "Floridi - Etica dell'intelligenza artificiale - antologia-lezione.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ---------------------------------------------------------------- testo del libro
CAP = {}
with zipfile.ZipFile(EPUB) as z:
    for name in z.namelist():
        m = re.search(r"Text/(Prefazione|Cap\d+)\.xhtml$", name)
        if not m:
            continue
        t = z.read(name).decode("utf-8")
        t = re.sub(r"(?s)<head.*?</head>", "", t)
        t = re.sub(r'<a class="_idFootnoteLink[^"]*"[^>]*>\d+</a>', "", t)   # richiami di nota
        t = re.sub(r"</(p|h\d|div|li|blockquote)>", "\n\n", t)
        t = re.sub(r"<[^>]+>", "", t)
        t = html.unescape(t)
        t = re.sub(r"[ \t\xa0]+", " ", t)
        t = re.sub(r"\n\s*\n+", "\n\n", t).strip()
        key = "P" if m.group(1) == "Prefazione" else m.group(1)[3:]
        CAP[key] = t
TUTTO = "\n".join(CAP.values())


def sezione(cap, pos):
    if cap == "P":
        return "Prefazione"
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^ ?(\d+\.\d+(?:\.\d+)?) [A-ZÀ-Úa-zìèé“]", CAP[cap])]
    prima = [h for p, h in heads if p <= pos and h.split(".")[0] == cap]
    return f"cap. {cap}, § {prima[-1]}" if prima else f"cap. {cap}"


def cut(cap, segs, title):
    txt = CAP[cap]
    out, first = [], None
    for a, b in segs:
        i = txt.find(a)
        if i < 0:
            sys.exit(f"[cap {cap} · {title}] inizio non trovato: {a!r}")
        j = txt.find(b, i)
        if j < 0:
            sys.exit(f"[cap {cap} · {title}] fine non trovata: {b!r}")
        piece = re.sub(r"\s*\n\s*", " ¶ ", txt[i:j + len(b)].strip())
        if first is None:
            first = i
        if i > 0 and txt[i - 2:i].strip() not in ("", ".", "?", "!", ":"):
            piece = "[…] " + piece
        if not piece.rstrip().endswith((".", "?", "!", "”", ":", ")")):
            piece = piece.rstrip(" ,;:") + " […]"
        out.append(piece)
    return " […] ".join(out).replace("[…] […]", "[…]"), sezione(cap, first)


def esc(s):
    s = html.escape(s, quote=False)
    paras = [p.strip() for p in s.split("¶")]
    return "</p><p>".join(p for p in paras if p)


# ---------------------------------------------------------------- contenuti
SECTIONS = []


def S(num, title, chaps, intro):
    SECTIONS.append(dict(num=num, title=title, chaps=chaps, intro=intro, items=[]))


def P(cap, title, segs, k):
    SECTIONS[-1]["items"].append(dict(cap=cap, title=title, segs=segs, k=k))


exec(compile((HERE / "floridi_contenuti.py").read_text(encoding="utf-8"), "floridi_contenuti.py", "exec"))


# ---------------------------------------------------------------- controllo citazioni
def norm(s):
    return s.replace("“", "").replace("”", "").replace('"', "")


def check_quotes():
    corpus = norm(TUTTO)
    texts = [COVER, QUESTIONS] + [s["intro"] for s in SECTIONS] + [i["k"] for s in SECTIONS for i in s["items"]]
    bad = [q for t in texts for q in re.findall(r"«([^»]+)»", re.sub(r"<[^>]+>", "", t)) if norm(q) not in corpus]
    if bad:
        sys.exit("Citazioni non trovate nel libro:\n  " + "\n  ".join(bad))
    print("citazioni verificate sul testo: ok")


CSS = """
@page { size: A4; margin: 20mm 22mm 20mm 22mm;
  @bottom-center { content: counter(page); font: 9pt Palatino; color: #777; } }
:root { --ink:#1d1b18; --muted:#6b6459; --acc:#1f4e79; --rule:#d9d2c5; --pane:#f2f4f6; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Palatino", "Book Antiqua", Georgia, serif; color: var(--ink); background:#fff;
  font-size: 10.6pt; line-height: 1.48; margin:0; }
.kicker { font-variant: small-caps; letter-spacing: .08em; color: var(--muted); font-size: 9.5pt; }
h1 { font-weight: normal; font-size: 21pt; line-height: 1.1; margin: 4pt 0 2pt; }
h1 em { color: var(--acc); }
.sub { font-style: italic; color: var(--muted); font-size: 11.5pt; margin-bottom: 12pt; }
h2 { font-weight: normal; font-size: 15pt; margin: 0 0 4pt; color: var(--acc); }
h2 .n { color: var(--muted); font-size: 11pt; margin-right: 6pt; }
h2 .bk { color: var(--muted); font-size: 10pt; font-style: italic; margin-left: 6pt; }
h3 { font-size: 10.6pt; font-variant: small-caps; letter-spacing: .05em; margin: 10pt 0 3pt; color: var(--muted); font-weight: normal; }
p { margin: 0 0 6pt; text-align: justify; hyphens: auto; }
.cover { page-break-after: always; font-size: 10pt; line-height: 1.42; }
.cols { columns: 2; column-gap: 9mm; }
.cols p { margin-bottom: 5pt; }
.box { background: var(--pane); border-left: 3px solid var(--acc); padding: 7pt 10pt; margin: 10pt 0 0; font-size: 9.4pt; }
.box p { margin: 0 0 4pt; }
.box.final { margin-top: 14pt; font-size: 10pt; }
.epi { border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); padding: 7pt 0; margin: 10pt 0;
  font-style: italic; font-size: 10pt; color:#3a352e; }
.epi .who { font-style: normal; font-variant: small-caps; color: var(--muted); display:block; margin-top:3pt; text-align:right; }
section.part { page-break-before: always; }
.intro { font-style: italic; color:#3a352e; margin-bottom: 10pt; border-bottom: 1px solid var(--rule); padding-bottom: 8pt; }
.t { break-inside: avoid; margin: 0 0 11pt; }
.t .num { font-variant: small-caps; color: var(--acc); font-size: 10pt; letter-spacing: .04em; }
.t .num .tit { color: var(--ink); font-variant: normal; font-style: italic; letter-spacing: 0; margin-left: 5pt; }
.t blockquote { margin: 2pt 0 4pt; padding: 0 0 0 10pt; border-left: 1px solid var(--rule); font-size: 10.6pt; line-height: 1.45; }
.t blockquote p { text-align: left; margin: 0 0 3pt; }
.t .gl { font-size: 9.6pt; color: #3a352e; margin: 0; padding-left: 10pt; }
.t .gl b { font-variant: small-caps; color: var(--muted); font-weight: normal; letter-spacing: .04em; }
ol.q { padding-left: 16pt; margin: 4pt 0; } ol.q li { margin-bottom: 5pt; }
"""


def build():
    parts = [f'<!doctype html><html lang="it"><head><meta charset="utf-8">'
             f"<title>Floridi, Etica dell’intelligenza artificiale — antologia</title><style>{CSS}</style></head><body>", COVER]
    n = 0
    for si, s in enumerate(SECTIONS):
        cls = ' class="part"' if si else ""
        parts.append(f'<section{cls}><h2><span class="n">{s["num"]}.</span>{html.escape(s["title"])}'
                     f'<span class="bk">({s["chaps"]})</span></h2><p class="intro">{html.escape(s["intro"])}</p>')
        for it in s["items"]:
            n += 1
            txt, rif = cut(it["cap"], it["segs"], it["title"])
            parts.append(f'<div class="t"><div class="num">{rif}<span class="tit">{html.escape(it["title"])}</span></div>'
                         f'<blockquote><p>{esc(txt)}</p></blockquote>'
                         f'<p class="gl"><b>Chiave.</b> {html.escape(it["k"])}</p></div>')
        if si == len(SECTIONS) - 1:
            parts.append(QUESTIONS)
        parts.append("</section>")
    parts.append("</body></html>")
    OUT_HTML.write_text("\n".join(parts), encoding="utf-8")
    print(f"{n} passi · HTML: {OUT_HTML}")


if __name__ == "__main__":
    check_quotes()
    build()
    if "--no-pdf" not in sys.argv:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()], check=True, capture_output=True)
        print(f"PDF: {OUT_PDF}")

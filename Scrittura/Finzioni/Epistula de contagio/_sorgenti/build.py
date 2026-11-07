#!/usr/bin/env python3
"""Epistula de contagio — PDF A4 con testo a fronte (latino a sinistra, italiano a destra).

Uso:  python3 build.py           (copertina da copertina.html + PDF)
Il testo è in testo.txt. La nota con asterisco sul titolo latino dichiara la paternità di Claude Code.
"""
import html, re, subprocess
from pathlib import Path

SRC = Path(__file__).parent
OUT = SRC.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DISCLAIMER = "Questo testo latino è stato integralmente prodotto da Claude Code. Il testo italiano è di Armando Bisogno."
COPY = ("Ho scritto questa pseudo-epistola di Agostino nei mesi del Covid, in italiano, per immaginare come avrebbe "
        "ragionato Agostino su quanto stava succedendo. Ora ho chiesto a Claude di «ritradurre» il testo in un latino agostiniano.")


def inline(s):
    s = html.escape(s, quote=False).replace("'", "’")
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


def parse():
    intro, rows, cur = "", [], None
    for ln in (SRC / "testo.txt").read_text().splitlines():
        s = ln.strip()
        if not s or s.startswith("# "):
            continue
        if s.startswith("@intro "):
            intro = s[7:]
        elif s.startswith("## "):
            la, it = [x.strip() for x in s[3:].split("|")]
            rows.append(("h", la, it))
        elif s.startswith("§ "):
            cur = ["p", s[2:], "", ""]
            rows.append(cur)
        elif s.startswith("LA: "):
            cur[2] = s[4:]
        elif s.startswith("IT: "):
            cur[3] = s[4:]
    return intro, rows


CSS = """
@page { size: A4; margin: 22mm 18mm 22mm 18mm; }
@page :first { margin: 0; }
html { font-family: 'EB Garamond', Garamond, Georgia, serif; font-size: 10.6pt; line-height: 1.45; color: #1d1b19; }
body { margin: 0; }
em { font-style: italic; }
.cover { page-break-after: always; height: 297mm; width: 210mm; background: #1a1f26; display: flex; align-items: center; justify-content: center; }
.cover img { height: 297mm; display: block; }
.titlepage { page-break-after: always; height: 253mm; position: relative; text-align: center; }
.titlepage .a { padding-top: 55mm; font-variant: small-caps; letter-spacing: .14em; font-size: 12pt; }
.titlepage .t { margin-top: 10mm; font-size: 28pt; line-height: 1.15; }
.titlepage .s { margin-top: 4mm; font-style: italic; font-size: 14pt; }
.titlepage .x { margin-top: 26mm; font-size: 10.5pt; color: #6b6259; }
.titlepage .fn { position: absolute; bottom: 0; left: 0; width: 60%; text-align: left; font-size: 8.5pt; color: #6b6259; border-top: .5pt solid #b9b0a5; padding-top: 2mm; }
.ast { font-size: .5em; vertical-align: super; line-height: 0; }
.nota { page-break-after: always; padding-top: 40mm; max-width: 120mm; margin: 0 auto; }
.nota h2 { font-weight: normal; font-variant: small-caps; letter-spacing: .12em; font-size: 11pt; text-align: center; margin-bottom: 8mm; }
.nota p { text-align: justify; margin: 0 0 .7em; }
.nota .intro { font-style: italic; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; }
td { vertical-align: top; padding: 0 0 .65em; text-align: justify; hyphens: auto; }
td.la { padding-right: 5mm; border-right: .5pt solid #d8d0c4; }
td.it { padding-left: 5mm; }
tr.head td { padding-bottom: 6mm; text-align: center; font-variant: small-caps; letter-spacing: .1em; font-size: 12pt; }
tr.h td { padding-top: .7em; padding-bottom: .35em; text-align: center; font-style: italic; color: #a3322a; break-after: avoid; }
td .n { font-variant: small-caps; color: #a3322a; margin-right: .3em; }
.colophon { page-break-before: always; padding-top: 200mm; font-size: 9pt; color: #6b6259; text-align: center; }
"""


def body(cover):
    intro, rows = parse()
    p = [f'<div class="cover"><img src="{cover}" alt=""/></div>']
    p.append(f"""<div class="titlepage"><div class="a">Aurelius Augustinus</div>
<div class="t">Epistula de contagio<span class="ast">*</span></div><div class="s">ad Adsentium diaconum</div>
<div class="x">Testo latino di Claude Code · testo italiano di Armando Bisogno</div>
<div class="fn">* {DISCLAIMER}</div></div>""")
    p.append(f'<div class="nota"><h2>Nota</h2><p>{inline(COPY)}</p><p class="intro">{inline(intro)}</p></div>')
    t = ['<table><colgroup><col style="width:50%"/><col style="width:50%"/></colgroup>',
         '<tr class="head"><td class="la">Epistula de contagio</td><td class="it">Lettera sul contagio</td></tr>']
    for r in rows:
        if r[0] == "h":
            t.append(f'<tr class="h"><td class="la">{inline(r[1])}</td><td class="it">{inline(r[2])}</td></tr>')
        else:
            _, n, la, it = r
            t.append(f'<tr><td class="la"><span class="n">{n}</span>{inline(la)}</td>'
                     f'<td class="it" lang="it"><span class="n">{n}</span>{inline(it)}</td></tr>')
    t.append("</table>")
    p.append("\n".join(t))
    p.append('<div class="colophon"><p>Finzioni · armandobisogno.it</p></div>')
    return "\n".join(p)


def page(content):
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Epistula de contagio</title>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{content}</body></html>"""


def chrome(args):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--hide-scrollbars",
                    "--virtual-time-budget=8000", *args], check=True, capture_output=True)


if __name__ == "__main__":
    png = OUT / "copertina.png"
    chrome(["--window-size=1600,2400", f"--screenshot={png}", (SRC / "copertina.html").as_uri()])
    tmp = OUT / ".libro.html"
    tmp.write_text(page(body(png.name)))
    pdf = OUT / "Epistula de contagio.pdf"
    chrome([f"--print-to-pdf={pdf}", tmp.as_uri()])
    tmp.unlink()
    # pagina di Finzioni (presentazione, licenza, contatti) subito dopo la copertina
    subprocess.run(["python3", str(SRC.parents[1] / "_strumenti" / "aggiungi_colophon.py"), str(pdf)], check=True)
    print("ok:", pdf.name)

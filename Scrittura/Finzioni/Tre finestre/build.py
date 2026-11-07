#!/usr/bin/env python3
"""Tre finestre — build dei libretti (PDF A5 + EPUB), un'edizione per romanzo e terna di autori.

Uso:  python3 build.py                 (tutte le edizioni)
      python3 build.py mosaici-ita     (una sola edizione, per slug)
      python3 build.py --cover ...     (rigenera anche le copertine provvisorie da copertina.html)

Per usare una copertina Canva: esportarla in PNG 1600x2400 come copertina-<slug>.png e rilanciare
senza --cover.
"""
import html, random, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
T = ROOT / "testi"
OUT = ROOT
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CALIBRE = "/Applications/calibre.app/Contents/MacOS/ebook-convert"

TITLE = "Tre finestre"
AUTHOR = "Armando Bisogno"
CC = """<p>Testo di Armando Bisogno, rilasciato con licenza<br/>Creative Commons Attribuzione – Condividi allo stesso modo 4.0 Internazionale<br/><span style="white-space:nowrap">(CC BY-SA 4.0)</span>.<br/><a href="https://creativecommons.org/licenses/by-sa/4.0/deed.it">creativecommons.org/licenses/by-sa/4.0/deed.it</a></p>"""
DISCLAIMER = "Questo testo è stato integralmente prodotto da Claude Code."
DETOMI = '<a href="https://detomieditore.it/products/terapie-mosaici-collezione">detomieditore.it/products/terapie-mosaici-collezione</a>'

ROMANZI = {
    "terapie": dict(titolo="Terapie", anno=2024, data="Sabato 3 settembre 2022", scena="pioggia",
                    versi="<em>Come On In My Kitchen</em> di Robert Johnson (1936)"),
    "mosaici": dict(titolo="Mosaici", anno=2025, data="Venerdì 19 maggio 2023", scena="alba",
                    versi="<em>Black Coffee</em> di Sonny Burke e Paul Francis Webster (1948)"),
}

EDIZIONI = {
    "terapie-ang": ("terapie", [("auster", "Paul Auster"), ("nesbo", "Jo Nesbø"), ("king", "Stephen King")]),
    "terapie-ita": ("terapie", [("benni", "Stefano Benni"), ("calvino", "Italo Calvino"), ("camilleri", "Andrea Camilleri")]),
    "mosaici-ita": ("mosaici", [("benni", "Stefano Benni"), ("calvino", "Italo Calvino"), ("camilleri", "Andrea Camilleri")]),
}


def md(text):
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        b = block.strip()
        if b.startswith(">"):
            lines = [l.lstrip("> ").rstrip() for l in b.splitlines()]
            out.append('<blockquote class="blues">' + "<br/>".join(inline(l) for l in lines) + "</blockquote>")
        elif b == "&nbsp;":
            out.append('<p class="stacco">*</p>')
        else:
            out.append("<p>" + inline(b.replace("\n", " ")) + "</p>")
    return "\n".join(out)


def inline(s):
    s = html.escape(s, quote=False).replace("&amp;nbsp;", "&#160;")
    s = s.replace("'", "’")
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


CSS = """
@page { size: A5; margin: 20mm 18mm 22mm 18mm; }
@page :first { margin: 0; }
html { font-family: 'EB Garamond', Garamond, Georgia, serif; font-size: 11.2pt; line-height: 1.5; color: #1d1b19; font-synthesis: none; }
body { margin: 0; }
p { margin: 0; text-indent: 1.4em; text-align: justify; hyphens: auto; }
h1 + .meta + .data + p, .nota p:first-of-type { text-indent: 0; }
em { font-style: italic; font-weight: 400; }
.cover { page-break-after: always; height: 210mm; width: 148mm; }
.cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
.titlepage { page-break-after: always; text-align: center; padding-top: 38mm; }
.titlepage .t { font-size: 26pt; letter-spacing: .04em; }
.titlepage .s { font-style: italic; margin-top: 6mm; font-size: 12pt; }
.titlepage .a { margin-top: 30mm; font-variant: small-caps; letter-spacing: .1em; }
.titlepage .x { margin-top: 3mm; font-size: 9.5pt; color: #6b6259; }
.nota { page-break-after: always; padding-top: 18mm; }
.nota h2 { font-weight: normal; font-variant: small-caps; letter-spacing: .12em; font-size: 11pt; text-align: center; margin-bottom: 8mm; }
.nota p { margin-bottom: .5em; }
.chapter { page-break-before: always; padding-top: 22mm; }
.num { text-align: center; color: #a3322a; letter-spacing: .2em; font-size: 10pt; }
h1 { text-align: center; font-weight: normal; font-size: 19pt; margin: 3mm 0 1mm; letter-spacing: .02em; }
.meta { text-align: center; font-style: italic; font-size: 10pt; color: #6b6259; }
.data { text-align: center; font-variant: small-caps; letter-spacing: .08em; font-size: 9.5pt; margin: 9mm 0 7mm; }
.stacco { text-align: center; text-indent: 0; margin: .8em 0; color: #a3322a; }
blockquote.blues { margin: 2.2em 0 0; text-align: center; font-style: italic; font-size: 10.5pt; color: #4c4640; }
.ast { font-size: .55em; vertical-align: super; line-height: 0; }
.fn { text-indent: 0; margin-top: 2.4em; padding-top: .5em; border-top: .5pt solid #b9b0a5; width: 45%; font-size: 8.5pt; color: #6b6259; text-align: left; white-space: nowrap; }
.colophon { page-break-after: always; padding-top: 108mm; font-size: 9pt; color: #6b6259; text-align: center; }
.colophon a { color: #6b6259; text-decoration: none; }
.colophon p { text-indent: 0; text-align: center; margin-bottom: .6em; }
"""


def nomi(autori):
    return ", ".join(n for _, n in autori[:-1]) + " e " + autori[-1][1]


def body(slug, cover_src):
    rk, autori = EDIZIONI[slug]
    r = ROMANZI[rk]
    lista = ", ".join(n for _, n in autori)
    parts = [f'<div class="cover"><img src="{cover_src}" alt="Copertina"/></div>']
    parts.append(f"""<div class="titlepage"><div class="t">{TITLE}</div>
<div class="s">Il prologo di <span style="font-style:normal">{r['titolo']}</span> e tre sue riscritture</div>
<div class="a">{AUTHOR}</div><div class="x">alla maniera di {lista}</div></div>""")
    parts.append(f"""<div class="colophon">{CC}
<p><em>{r['titolo']}</em> è un romanzo di Armando Bisogno pubblicato da De Tomi Editore ({r['anno']}).<br/>{DETOMI}</p>
<p>Le versioni II–IV sono riscritture prodotte integralmente da Claude Code (Anthropic) per un esperimento di <em>Macchine Pensanti</em>, ottobre 2026. Non sono testi di {nomi(autori).replace(' e ', ' o ')}.</p>
<p>I versi in chiusura sono da {r['versi']}.</p></div>""")
    nota = T / rk / f"nota-{'-'.join(k for k, _ in autori)}.md"
    parts.append('<div class="nota"><h2>Nota</h2>' + md(nota.read_text()) + "</div>")
    capitoli = [("originale", "Armando Bisogno", f"Il prologo originale di <em>{r['titolo']}</em> (De Tomi, {r['anno']})")]
    capitoli += [(k, n, "alla maniera di") for k, n in autori]
    for i, (k, who, meta) in enumerate(capitoli):
        # le riscritture (II-IV) dichiarano la paternità di Claude Code con la nota con asterisco
        ast, fn = ("", "") if k == "originale" else ('<span class="ast">*</span>', f'<p class="fn">* {DISCLAIMER}</p>')
        parts.append(f"""<section class="chapter"><div class="num">{['I.', 'II.', 'III.', 'IV.'][i]}</div><h1>{who}{ast}</h1>
<div class="meta">{meta}</div><div class="data">{r['data']}</div>
{md((T / rk / f'{k}.md').read_text())}{fn}</section>""")
    return "\n".join(parts)


def page(content, fonts=True):
    link = ('<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">'
            if fonts else "")
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><title>{TITLE}</title>{link}
<style>{CSS}</style></head><body>{content}</body></html>"""


def chrome(args):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", *args], check=True, capture_output=True)


UMBRELLA = """<g transform="translate(1115,1060) rotate(-24)">
 <path d="M-70,0 Q0,-78 70,0 Q52,-10 35,0 Q17,-10 0,0 Q-17,-10 -35,0 Q-52,-10 -70,0 Z" fill="#b8322a"/>
 <line x1="0" y1="0" x2="0" y2="62" stroke="#b8322a" stroke-width="5"/>
 <path d="M0,62 q0,12 -12,12" fill="none" stroke="#b8322a" stroke-width="5"/></g>"""
STEAM = '<path d="M-10,-80 q-14,-26 4,-46 q14,-18 -2,-40" fill="none" stroke="#efe8dc" stroke-opacity=".5" stroke-width="5"/>'
# alba di maggio sui tetti di Fossa: nessuna pioggia, e la tazzina è vuota (il caffè non c'è)
DAWN = """<circle cx="1080" cy="1230" r="70" fill="#f3d9a4" fill-opacity=".9"/>
<path d="M330,1300 L330,1250 L420,1250 L420,1215 L470,1180 L520,1215 L520,1260 L610,1260 L610,1200 L700,1200 L700,1150 L740,1150 L740,1235
 L830,1235 L880,1195 L930,1235 L930,1270 L1020,1270 L1020,1225 L1120,1225 L1120,1280 L1190,1280 L1190,1240 L1270,1240 L1270,1470 L330,1470 Z"
 fill="#2b3138" fill-opacity=".92"/>
<rect x="770" y="1180" width="14" height="22" fill="#e9c98a" fill-opacity=".8"/>"""


def rain():
    rnd = random.Random(1952)
    return "".join(
        f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x-6:.0f}" y2="{y+L:.0f}" stroke="rgba(220,228,235,{a:.2f})" stroke-width="{w:.1f}"/>'
        for x, y, L, a, w in ((rnd.uniform(0, 1600), rnd.uniform(-100, 2400), rnd.uniform(30, 110),
                               rnd.uniform(.06, .28), rnd.uniform(1, 2.6)) for _ in range(650)))


def make_cover(slug, png):
    rk, autori = EDIZIONI[slug]
    r = ROMANZI[rk]
    if r["scena"] == "pioggia":
        sub = dict(GLASS_TOP="#3a4752", GLASS_BOTTOM="#212a31", SCENE=rain() + UMBRELLA, STEAM=STEAM)
    else:
        sub = dict(GLASS_TOP="#6f8597", GLASS_BOTTOM="#d9b58a", SCENE=DAWN, STEAM="")
    sub.update(ROMANZO=r["titolo"], AUTORI=" · ".join(n for _, n in autori))
    src = (ROOT / "copertina.html").read_text()
    for k, v in sub.items():
        src = src.replace("{{" + k + "}}", v)
    tmp = ROOT / ".copertina_build.html"
    tmp.write_text(src)
    chrome(["--window-size=1600,2400", "--hide-scrollbars", f"--screenshot={png}", tmp.as_uri()])
    tmp.unlink()


def build(slug, cover):
    rk, autori = EDIZIONI[slug]
    r = ROMANZI[rk]
    name = f"{TITLE} – {r['titolo']} ({', '.join(n.split()[-1] for _, n in autori)})"
    png = ROOT / f"copertina-{slug}.png"
    if cover or not png.exists():
        make_cover(slug, png)
    book = ROOT / ".libro.html"
    book.write_text(page(body(slug, png.name)))
    chrome([f"--print-to-pdf={OUT / (name + '.pdf')}", book.as_uri()])
    # EPUB: niente copertina nel corpo (la mette calibre), font di sistema
    ebook = ROOT / ".libro_epub.html"
    ebook.write_text(page(body(slug, png.name).split("</div>", 1)[1], fonts=False))
    sub = f"Il prologo di {r['titolo']} e tre sue riscritture"
    subprocess.run([CALIBRE, str(ebook), str(OUT / (name + ".epub")),
                    "--cover", str(png), "--title", f"{TITLE} – {r['titolo']}", "--authors", AUTHOR,
                    "--language", "it", "--comments", sub, "--publisher", "Macchine Pensanti",
                    "--chapter", "//h:h1", "--level1-toc", "//h:h1", "--page-breaks-before", "/",
                    "--preserve-cover-aspect-ratio", "--no-default-epub-cover"],
                   check=True, capture_output=True)
    book.unlink(); ebook.unlink()
    # pagina di Finzioni (presentazione, licenza, contatti) subito dopo la copertina del PDF
    subprocess.run(["python3", str(ROOT.parent / "_strumenti" / "aggiungi_colophon.py"), str(OUT / (name + ".pdf"))], check=True)
    print("ok:", name)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for slug in args or EDIZIONI:
        build(slug, "--cover" in sys.argv)


if __name__ == "__main__":
    main()

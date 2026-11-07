#!/usr/bin/env python3
"""Catastrofi alla maniera di Stefano Benni — build dell'EPUB.

Uso:  python3 build.py   (richiede copertina.jpg 1600x2400 nella cartella)
Testi in benni/NN.md: 00 prologo, 01-09 capitoli, 10 post scriptum.
"""
import html, re, subprocess
from pathlib import Path

ROOT = Path(__file__).parent
CALIBRE = "/Applications/calibre.app/Contents/MacOS/ebook-convert"
TITLE = "Catastrofi"
SUB = "Il primo caso di Terapie alla maniera di Stefano Benni"
AUTHOR = "Armando Bisogno"

CAPITOLI = [
    ("Prologo", "Sabato 3 settembre 2022"),
    ("Capitolo 1", "Lunedì 5 settembre 2022"),
    ("Capitolo 2", ""),
    ("Capitolo 3", ""),
    ("Capitolo 4", "Martedì 6 settembre 2022"),
    ("Capitolo 5", "Mercoledì 7 settembre 2022"),
    ("Capitolo 6", "Giovedì 8 settembre 2022"),
    ("Capitolo 7", "Venerdì 9 settembre 2022"),
    ("Capitolo 8", "Sabato 10 settembre 2022"),
    ("Capitolo 9", "Lunedì 12 settembre 2022"),
    ("Post Scriptum", ""),
]


def inline(s):
    s = html.escape(s, quote=False).replace("'", "’")
    s = re.sub(r"(https?://\S+)", r'<a href="\1">\1</a>', s)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


def md(text):
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        b = block.strip()
        if b.startswith(">"):
            lines = [l.lstrip("> ").rstrip() for l in b.splitlines()]
            out.append('<blockquote class="blues">' + "<br/>".join(inline(l) for l in lines) + "</blockquote>")
        elif b == "&nbsp;":
            out.append('<p class="stacco">* * *</p>')
        else:
            out.append("<p>" + inline(b.replace("\n", " ")) + "</p>")
    return "\n".join(out)


CSS = """
body { font-family: Georgia, serif; line-height: 1.5; }
p { margin: 0; text-indent: 1.3em; text-align: justify; }
h1 + .data + p, h1 + p, .stacco + p, .nota p { text-indent: 0; }
h1 { text-align: center; font-weight: normal; font-size: 1.5em; margin: 2.5em 0 .3em; page-break-before: always; }
.data { text-align: center; font-variant: small-caps; letter-spacing: .08em; font-size: .9em; margin: 0 0 2em; }
.stacco { text-align: center; text-indent: 0; margin: 1em 0; color: #a3322a; }
blockquote.blues { margin: 2em 0 0; text-align: center; font-style: italic; }
.titlepage { text-align: center; margin-top: 30%; }
.titlepage .t { font-size: 2em; }
.titlepage .s { font-style: italic; margin-top: 1em; }
.titlepage .a { margin-top: 3em; font-variant: small-caps; letter-spacing: .1em; }
.colophon { page-break-before: always; margin-top: 40%; font-size: .85em; text-align: center; }
.colophon p, .nota p { text-indent: 0; text-align: center; margin-bottom: .8em; }
"""

COLOPHON = """<div class="colophon">
<p><em>Terapie</em> è un romanzo di Armando Bisogno pubblicato da De Tomi Editore (2024).<br/>
<a href="https://detomieditore.it/products/terapie-mosaici-collezione">detomieditore.it/products/terapie-mosaici-collezione</a></p>
<p>Questa è una riscrittura del primo caso, <em>Catastrofi</em>, realizzata con Claude (Anthropic) per un esperimento di <em>Macchine Pensanti</em>, ottobre 2026. Non è un testo di Stefano Benni.</p>
</div>"""


def main():
    parts = [f"""<div class="titlepage"><div class="t">{TITLE}</div><div class="s">{SUB}</div>
<div class="a">{AUTHOR}</div></div>""", COLOPHON]
    for i, (titolo, data) in enumerate(CAPITOLI):
        testo = (ROOT / "benni" / f"{i:02d}.md").read_text()
        d = f'<div class="data">{data}</div>' if data else ""
        parts.append(f"<h1>{titolo}</h1>{d}\n{md(testo)}")
    src = ROOT / ".libro.html"
    src.write_text(f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><title>{TITLE}</title>
<style>{CSS}</style></head><body>{''.join(parts)}</body></html>""")
    out = ROOT / f"{TITLE} (alla maniera di Stefano Benni).epub"
    subprocess.run([CALIBRE, str(src), str(out), "--cover", str(ROOT / "copertina.jpg"),
                    "--title", f"{TITLE} – alla maniera di Stefano Benni", "--authors", AUTHOR,
                    "--language", "it", "--comments", SUB, "--publisher", "Macchine Pensanti",
                    "--chapter", "//h:h1", "--level1-toc", "//h:h1",
                    "--preserve-cover-aspect-ratio", "--no-default-epub-cover"],
                   check=True, capture_output=True)
    src.unlink()
    print("ok:", out.name)


if __name__ == "__main__":
    main()

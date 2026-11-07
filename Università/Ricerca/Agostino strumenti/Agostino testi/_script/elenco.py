# -*- coding: utf-8 -*-
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from opere import OPERE, ESCLUSE
from build import shade, force_font, safe, OUT, MD
DEST = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi"
done = {int(f.split(".")[0]) for f in os.listdir(OUT) if f.endswith(".docx") and f.split(".")[0].isdigit()}
CRIT = ("Criteri. Sono elencate le opere di Agostino pubblicate su www.augustinus.it (Nuova Biblioteca Agostiniana), "
        "escluse le lettere e i sermoni. L’ordine segue la «Sinopsis de la producción agustiniana» di J. Anoz "
        "(Cronología de la producción agustiniana, «Augustinus» 47, 2002), integrata con la Cronologia di G. Catapano, "
        "Agostino, Carocci 2010. Le opere composte in più tempi sono collocate alla data d’inizio (es. De Trinitate, "
        "De Genesi ad litteram, De civitate Dei, Enarrationes in Psalmos). Per Regula, Quaestiones XVII in Matthaeum e "
        "De octo quaestionibus ex Veteri Testamento, assenti nella sinossi di Anoz, si adotta la datazione tradizionale.")
doc = Document()
doc.styles["Normal"].font.name = "Garamond"; doc.styles["Normal"].font.size = Pt(11)
s = doc.sections[0]; s.orientation = WD_ORIENT.LANDSCAPE; s.page_width, s.page_height = Cm(29.7), Cm(21)
s.left_margin = s.right_margin = Cm(1.5)
t = doc.add_heading("Agostino d’Ippona — Elenco cronologico delle opere", level=0); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph(CRIT); [setattr(r.font, "size", Pt(9)) for r in p.runs]
p = doc.add_paragraph("● = testo latino/italiano già estratto nella cartella «Opere» (docx) e «Opere/_md» (testo per la ricerca).")
[setattr(r.font, "size", Pt(9)) for r in p.runs]
tb = doc.add_table(rows=1, cols=6); tb.style = "Table Grid"
W = [Cm(1.2), Cm(9.5), Cm(7.5), Cm(2.8), Cm(3.6), Cm(2.0)]
for c, h in zip(tb.rows[0].cells, ["N.", "Opera", "Titolo italiano (NBA)", "Sigla", "Datazione", "Testo"]):
    c.text = ""; r = c.paragraphs[0].add_run(h); r.bold = True; shade(c, "E8E8E8")
md = ["# Agostino d’Ippona — Elenco cronologico delle opere", "", CRIT, "",
      "| N. | Opera | Titolo italiano (NBA) | Sigla | Datazione | Note | Testo |", "|---|---|---|---|---|---|---|"]
for n, tl, sig, fold, ti, dat, nota in OPERE:
    row = tb.add_row().cells
    vals = [str(n), tl, ti, sig, dat, "●" if n in done else ""]
    for i, (c, v) in enumerate(zip(row, vals)):
        c.text = ""; r = c.paragraphs[0].add_run(v); r.font.size = Pt(10)
        if i == 1: r.italic = True
        if i == 1 and nota:
            r2 = c.paragraphs[0].add_run(f" — {nota}"); r2.font.size = Pt(8.5)
    link = f"[{'●'}](Opere/_md/{n}.%20{safe(tl).replace(' ', '%20')}.md)" if n in done else ""
    md.append(f"| {n} | *{tl}* | {ti} | {sig} | {dat} | {nota} | {link} |")
for row in tb.rows:
    for c, w in zip(row.cells, W): c.width = w
doc.add_paragraph()
p = doc.add_paragraph(); r = p.add_run("Non comprese nell’elenco"); r.bold = True
md += ["", "## Non comprese nell’elenco", ""]
for tx, why in ESCLUSE:
    p = doc.add_paragraph(f"· {tx} ({why})"); [setattr(r.font, "size", Pt(9.5)) for r in p.runs]
    md.append(f"- {tx} ({why})")
for pp in doc.paragraphs:
    for r in pp.runs: force_font(r)
for row in tb.rows:
    for c in row.cells:
        for pp in c.paragraphs:
            for r in pp.runs: force_font(r)
doc.save(os.path.join(DEST, "0. Elenco cronologico delle opere.docx"))
open(os.path.join(DEST, "0. Elenco cronologico delle opere.md"), "w").write("\n".join(md) + "\n")
print("ok", len(OPERE), "opere;", len(done), "estratte")

# -*- coding: utf-8 -*-
import os, json
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
import build
from lettere import SERM, ORD, BASE
done = {int(f.split(".")[0]) for f in os.listdir(BASE) if f.endswith(".docx") and f.split(".")[0].isdigit()}
CRIT = ("Criteri. Sono elencate tutte le lettere pubblicate su www.augustinus.it (Nuova Biblioteca Agostiniana): la raccolta "
        "delle Epistulae (1–270, con le aggiunte A) e le lettere scoperte da J. Divjak (1*–29*). La raccolta comprende anche lettere "
        "scritte ad Agostino e scambi tra terzi. Ordine e datazione seguono la «Sinopsis de la producción agustiniana» di J. Anoz "
        "(«Augustinus» 47, 2002), che data le lettere di Agostino; per le altre (in gran parte lettere indirizzate ad Agostino) si "
        "indica la datazione della «Tavola cronologica delle Lettere» della NBA, segnalata tra parentesi quadre. In coda le lettere "
        "non datate. Mittente, destinatario e luogo provengono dalla Tavola NBA.")
doc = Document()
doc.styles["Normal"].font.name = "Garamond"; doc.styles["Normal"].font.size = Pt(10.5)
s = doc.sections[0]; s.orientation = WD_ORIENT.LANDSCAPE; s.page_width, s.page_height = Cm(29.7), Cm(21)
s.left_margin = s.right_margin = Cm(1.5)
t = doc.add_heading("Agostino d’Ippona — Elenco cronologico delle Epistulae", level=0); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph(CRIT); [setattr(r.font, "size", Pt(9)) for r in p.runs]
tb = doc.add_table(rows=1, cols=6); tb.style = "Table Grid"
W = [Cm(1.3), Cm(5.2), Cm(9.0), Cm(6.2), Cm(3.8), Cm(1.3)]
for c, h in zip(tb.rows[0].cells, ["N.", "Lettera", "Mittente e destinatario", "Datazione", "Luogo", "Testo"]):
    c.text = ""; r = c.paragraphs[0].add_run(h); r.bold = True; build.shade(c, "E8E8E8")
md = ["# Agostino d’Ippona — Elenco cronologico delle Epistulae", "", CRIT, "",
      "| N. | Lettera | Mittente e destinatario | Datazione | Luogo | Testo |", "|---|---|---|---|---|---|"]
for (n, tl, sig, fold, ti, dat, nota), e in zip(SERM, ORD):
    luogo = nota.replace("luogo: ", "")
    arg = ti.split(" — ", 1)[1] if " — " in ti else ""
    row = tb.add_row().cells
    for c, v in zip(row, [str(n), tl, arg, dat, luogo, "●" if n in done else ""]):
        c.text = ""; r = c.paragraphs[0].add_run(v); r.font.size = Pt(9)
    link = f"[●](Epistulae/_md/{n}.%20{build.safe(tl).replace(' ', '%20')}.md)" if n in done else ""
    md.append(f"| {n} | {tl} | {arg} | {dat} | {luogo} | {link} |")
for row in tb.rows:
    for c, w in zip(row.cells, W): c.width = w
for pp in doc.paragraphs:
    for r in pp.runs: build.force_font(r)
for row in tb.rows:
    for c in row.cells:
        for pp in c.paragraphs:
            for r in pp.runs: build.force_font(r)
DEST = os.path.dirname(BASE)
doc.save(os.path.join(DEST, "0. Elenco cronologico delle lettere.docx"))
open(os.path.join(DEST, "0. Elenco cronologico delle lettere.md"), "w").write("\n".join(md) + "\n")
print("ok", len(SERM), "lettere;", len(done), "estratte")

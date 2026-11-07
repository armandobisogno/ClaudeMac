# -*- coding: utf-8 -*-
import os, json
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
import build
from sermones import SERM, ORD, BASE
done = {int(f.split(".")[0]) for f in os.listdir(BASE) if f.endswith(".docx") and f.split(".")[0].isdigit()}
CRIT = ("Criteri. Sono elencati tutti i sermoni pubblicati su www.augustinus.it (Nuova Biblioteca Agostiniana): la raccolta "
        "dei Sermones (1–396, con le aggiunte A, B, …), i «Discorsi nuovi» (Dolbeau, Étaix) e i sermoni di Erfurt. "
        "Ordine e datazione seguono la «Sinopsis de la producción agustiniana» di J. Anoz («Augustinus» 47, 2002); le forme "
        "brevi dei Maurini e le versioni ampliate di Dolbeau sono datate insieme, come in Anoz. Per i sermoni non datati da Anoz "
        "si indica, quando c’è, la datazione della «Tavola cronologica dei Discorsi» della NBA (segnalata tra parentesi quadre). "
        "In coda i sermoni non datati: quelli che Anoz elenca sotto «¿Cuándo?», i frammenti, i sermoni di Erfurt (scoperti nel 2008, "
        "dopo lo studio di Anoz). I sermoni 397–400 (De excidio urbis, De symbolo ad catechumenos, De disciplina christiana, "
        "De utilitate ieiunii) sono nel corpus delle opere.")
doc = Document()
doc.styles["Normal"].font.name = "Garamond"; doc.styles["Normal"].font.size = Pt(10.5)
s = doc.sections[0]; s.orientation = WD_ORIENT.LANDSCAPE; s.page_width, s.page_height = Cm(29.7), Cm(21)
s.left_margin = s.right_margin = Cm(1.5)
t = doc.add_heading("Agostino d’Ippona — Elenco cronologico dei Sermones", level=0); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph(CRIT); [setattr(r.font, "size", Pt(9)) for r in p.runs]
tb = doc.add_table(rows=1, cols=6); tb.style = "Table Grid"
W = [Cm(1.3), Cm(5.2), Cm(9.0), Cm(6.2), Cm(3.8), Cm(1.3)]
for c, h in zip(tb.rows[0].cells, ["N.", "Sermone", "Titolo italiano / argomento", "Datazione", "Luogo", "Testo"]):
    c.text = ""; r = c.paragraphs[0].add_run(h); r.bold = True; build.shade(c, "E8E8E8")
md = ["# Agostino d’Ippona — Elenco cronologico dei Sermones", "", CRIT, "",
      "| N. | Sermone | Titolo italiano / argomento | Datazione | Luogo | Testo |", "|---|---|---|---|---|---|"]
for (n, tl, sig, fold, ti, dat, nota), e in zip(SERM, ORD):
    luogo = nota.replace("luogo: ", "")
    arg = ti.split(" — ", 1)[1] if " — " in ti else ""
    row = tb.add_row().cells
    for c, v in zip(row, [str(n), tl, arg, dat, luogo, "●" if n in done else ""]):
        c.text = ""; r = c.paragraphs[0].add_run(v); r.font.size = Pt(9)
    link = f"[●](Sermones/_md/{n}.%20{build.safe(tl).replace(' ', '%20')}.md)" if n in done else ""
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
doc.save(os.path.join(DEST, "0. Elenco cronologico dei sermoni.docx"))
open(os.path.join(DEST, "0. Elenco cronologico dei sermoni.md"), "w").write("\n".join(md) + "\n")
print("ok", len(SERM), "sermoni;", len(done), "estratti")

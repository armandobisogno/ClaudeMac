"""De magistro per la codifica alla cieca: solo latino, riferimenti del corpus, battute separate,
SENZA i titoletti editoriali NBA (potrebbero suggerire dove sono le definizioni). Output in _dati/ (fuori da git)."""
import os, re
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.section import WD_ORIENT
from corpus import paragrafi, HERE
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
for m in ("left_margin", "right_margin"): setattr(sec, m, Cm(1.8))
sec.top_margin = sec.bottom_margin = Cm(1.8)
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)
doc.add_heading("De magistro — codifica alla cieca", level=1)
doc.add_paragraph("Testo latino dal corpus del workspace (riferimenti [cap.par]); battute separate; "
                  "titoletti editoriali omessi. Applicare il codebook (bozza 3). Nella colonna di destra: "
                  "codici delle spie, definiendum, proponente (Aug./Ad.), esito, grado. "
                  "Gli episodi su più paragrafi si segnano con lo stesso numero (E1, E2…).")
t = doc.add_table(rows=1, cols=2); t.style = "Table Grid"; t.autofit = False
hdr = t.rows[0].cells; hdr[0].text = "Testo"; hdr[1].text = "Codifica"
n = 0
for s, ref, testo in paragrafi():
    if s != "mag.": continue
    n += 1
    testo = re.sub(r"^\d+\.\s*\d+\.\s*", "", testo)
    row = t.add_row().cells
    p = row[0].paragraphs[0]; r = p.add_run(f"[{ref}] "); r.bold = True
    battute = [b.strip() for b in testo.split(" / ") if b.strip()]
    p.add_run(battute[0])
    for b in battute[1:]: row[0].add_paragraph(b)
for row in t.rows:
    row.cells[0].width, row.cells[1].width = Cm(11.4), Cm(6)
out = os.path.join(HERE, "..", "_dati", "De magistro - codifica alla cieca.docx")
doc.save(out); print(n, "paragrafi ->", os.path.normpath(out))

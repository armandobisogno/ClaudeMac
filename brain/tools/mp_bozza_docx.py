#!/usr/bin/env python3
"""
mp_bozza_docx.py — converte una bozza di Macchine Pensanti scritta in markdown
semplice in un .docx nello stile delle bozze esistenti.

  python3 mp_bozza_docx.py bozza.md "Scrittura/Macchine Pensanti/Bozze/Titolo.docx"

Formato del sorgente:
  # Titolo
  > Sottotitolo
  ## Titoletto di sezione
  paragrafi separati da riga vuota; *corsivo* e **grassetto** inline
  --- (stacco)
"""
import sys, re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_inline(par, text):
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not tok:
            continue
        if tok.startswith("**"):
            par.add_run(tok[2:-2]).bold = True
        elif tok.startswith("*"):
            par.add_run(tok[1:-1]).italic = True
        else:
            par.add_run(tok)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        blocks = [b.strip() for b in re.split(r"\n\s*\n", f.read()) if b.strip()]
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Georgia"
    st.font.size = Pt(12)
    for b in blocks:
        line = " ".join(l.strip() for l in b.splitlines())
        if line.startswith("# "):
            doc.add_heading(line[2:], level=1)
        elif line.startswith("> "):
            p = doc.add_paragraph()
            r = p.add_run(line[2:])
            r.italic = True
            r.font.size = Pt(14)
        elif line.startswith("## "):
            doc.add_heading(line[3:], level=3)
        elif line == "---":
            p = doc.add_paragraph("* * *")
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(10)
            add_inline(p, line)
    doc.save(dst)
    print(f"Salvato: {dst}")


if __name__ == "__main__":
    main()

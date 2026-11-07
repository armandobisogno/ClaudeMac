# -*- coding: utf-8 -*-
"""Dai .docx lat/ita a fronte ricava edizioni con il solo latino (cartella sorella
"Agostino testi (solo latino)"). Le note in calce restano tutte; poiché i richiami
stanno nella traduzione, vengono riportati in esponente alla fine del paragrafo
latino corrispondente."""
import os, re, sys, copy, shutil
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

SRC = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi"
DST = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi (solo latino)"
SUBS = ["Opere", "Epistulae", "Sermones"]
FONT = "Garamond"
GRAY = "444444"

def is_gray(p):
    return p.runs and all(r.font.color is not None and r.font.color.rgb is not None and str(r.font.color.rgb) == GRAY
                          for r in p.runs if r.text.strip())

def shaded(cell):
    tcPr = cell._tc.tcPr
    return tcPr is not None and tcPr.find(qn("w:shd")) is not None

def note_marks(cell):
    return [r.text for p in cell.paragraphs for r in p.runs if r.font.superscript and r.text.strip()]

def set_font(run, size=None):
    run.font.name = FONT
    rPr = run._r.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = rPr.makeelement(qn("w:rFonts"), {}); rPr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), FONT)
    if size: run.font.size = size

def append_marks(p, marks):
    for m in marks:
        r = p.add_run(m); r.font.superscript = True; set_font(r)

def convert(src, dst):
    doc = Document(src)
    body = doc.element.body
    # via l'introduzione NBA (in italiano): dal salto pagina che la precede al salto pagina successivo
    els = list(body)
    is_break = lambda e: e.tag == qn("w:p") and any(b.get(qn("w:type")) == "page" for b in e.iter(qn("w:br")))
    for i, el in enumerate(els):
        if el.tag == qn("w:p") and Paragraph(el, doc).text.startswith("Introduzione (dall’edizione NBA)"):
            j = i + 1
            while j < len(els) and not is_break(els[j]) and els[j].tag == qn("w:p"):
                j += 1
            start = i - 1 if i > 0 and is_break(els[i - 1]) else i
            for e in els[start:j]:
                body.remove(e)
            break
    for el in list(body):
        tag = el.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(el, doc)
            t = p.text
            if is_gray(p):
                body.remove(el); continue
            if t.startswith("Testo latino e traduzione italiana a fronte"):
                for r in p.runs:
                    r.text = r.text.replace("Testo latino e traduzione italiana a fronte", "Testo latino")
            elif t.startswith("Fonte di questa versione."):
                p.runs[0].text = ("Fonte di questa versione. Il testo latino è ripreso dall’edizione digitale della "
                                  "Nuova Biblioteca Agostiniana (Città Nuova Editrice), pubblicata sul sito www.augustinus.it; "
                                  "le note provengono dalla versione italiana della stessa edizione:")
                for r in p.runs[1:]: r.text = ""
            elif t.startswith("· traduzione italiana:"):
                p.runs[0].text = p.runs[0].text.replace("· traduzione italiana:", "· note (versione italiana):")
            elif t.startswith("Consultazione:"):
                txt = t.replace("i rimandi nel testo latino sono stati omessi.",
                                "in questa edizione con il solo latino i richiami di nota, che nella versione italiana "
                                "cadono all’interno del paragrafo, sono riportati in esponente alla fine del paragrafo "
                                "latino corrispondente.")
                p.runs[0].text = txt
                for r in p.runs[1:]: r.text = ""
            elif p.style.name == "Heading 1" and " — " in t:
                lat = t.split(" — ")[0]
                p.runs[0].text = lat
                for r in p.runs[1:]: r.text = ""
        elif tag == "tbl":
            tb = Table(el, doc)
            anchor = el
            last = None; pending = []
            for i, row in enumerate(tb.rows):
                if i == 0: continue   # LATINO | ITALIANO
                cells = row.cells
                lc, ic = cells[0], cells[1]
                marks = note_marks(ic)
                ltxt = lc.text.strip()
                if shaded(lc):
                    pending += marks   # richiami nei titoletti: al paragrafo successivo
                    if not ltxt: continue
                    for cp in lc.paragraphs:
                        np_ = copy.deepcopy(cp._p)
                        anchor.addnext(np_); anchor = np_
                        P = Paragraph(np_, doc)
                        P.paragraph_format.space_before = Pt(8); P.paragraph_format.keep_with_next = True
                    continue
                if not ltxt:
                    if last is not None: append_marks(last, marks)
                    else: pending += marks
                    continue
                for j, cp in enumerate(lc.paragraphs):
                    np_ = copy.deepcopy(cp._p)
                    anchor.addnext(np_); anchor = np_
                    last = Paragraph(np_, doc)
                    last.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    last.paragraph_format.space_after = Pt(6)
                append_marks(last, pending + marks); pending = []
            body.remove(el)
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.5)
    sec.top_margin = sec.bottom_margin = Cm(2.2)
    doc.save(dst)

if __name__ == "__main__":
    only = sys.argv[1:]
    os.makedirs(DST, exist_ok=True)
    for f in os.listdir(SRC):
        if f.startswith("0. Elenco") and f.endswith(".docx"):
            shutil.copy2(os.path.join(SRC, f), os.path.join(DST, f))
    n = 0
    for sub in SUBS:
        if only and sub not in only: continue
        os.makedirs(os.path.join(DST, sub), exist_ok=True)
        for f in sorted(os.listdir(os.path.join(SRC, sub))):
            if not f.endswith(".docx") or f.startswith("~$"): continue
            convert(os.path.join(SRC, sub, f), os.path.join(DST, sub, f)); n += 1
        print(sub, "fatto", flush=True)
    print("totale", n)

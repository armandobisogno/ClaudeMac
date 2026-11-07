# -*- coding: utf-8 -*-
"""Miniantologia «Agostino e l'esegesi biblica prima delle Confessiones» (latino/italiano) dal corpus _md."""
import re, os, glob
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from build import shade, force_font
from opere import OPERE

MD = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi/Opere/_md"
OUTDIR = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi/Antologie"
OUT = os.path.join(OUTDIR, "Agostino e l'esegesi biblica (prima delle Confessiones) - antologia lat-ita.docx")
META = {o[0]: o for o in OPERE}

def load(n):
    f = glob.glob(os.path.join(MD, f"{n}. *.md"))[0]
    paras, notes = {}, {}
    for line in open(f, encoding="utf-8"):
        m = re.match(r"\[([^\]]+)\] (LA|IT): (.*)", line)
        if m:
            paras.setdefault(m.group(1), {})[m.group(2)] = m.group(3).strip()
        m = re.match(r"\[n(\d+) @([^\]]+)\] (.*)", line)
        if m:
            notes[(m.group(2), int(m.group(1)))] = m.group(3).strip()
    return paras, notes

def cut(text, seg):
    """seg: None (tutto) o (inizio, fine) inclusivi"""
    if not seg:
        return text
    a, b = seg
    i = text.find(a) if a else 0
    assert i >= 0, f"inizio non trovato: {a!r}"
    j = text.find(b, i) if b else len(text)
    assert j >= 0, f"fine non trovata: {b!r}"
    end = j + len(b) if b else len(text)
    return ("[…] " if a else "") + text[i:end].strip() + (" […]" if text[end:].strip() else "")

# (num, rif. visualizzato, titolo, scheda, [(ref, taglio LA, taglio IT), …])
TESTI = [
 (14, "2,2,3", "Prima la storia, poi la profezia: quando la lettera non basta",
  "Commentando il racconto del paradiso (Gn 2–3) contro le derisioni manichee, Agostino formula per la prima volta "
  "il criterio che regge tutta la sua esegesi: la lettura letterale è la migliore, finché è possibile «evitare "
  "bestemmie» e restare conformi alla fede; quando non lo è, si passa alla lettura figurata, sul modello degli "
  "Apostoli. Esegesi come ricerca (petite, quaerite, pulsate), non come accusa.",
  [("2.2.3", None, None)]),
 (17, "3,5–6", "I quattro modi di leggere l’Antico Testamento",
  "All’amico Onorato, ancora manicheo, il neopresbitero Agostino espone la dottrina ricevuta («sic accepi») dei "
  "quattro sensi: historia, aetiologia, analogia, allegoria. È la prima tassonomia esegetica esplicita della sua "
  "opera; il criterio di legittimazione è che di tutti e quattro i modi si siano serviti Cristo e gli Apostoli.",
  [("3.5", None, None),
   ("3.6", (None, "et Apostoli usi sunt."), (None, "e gli Apostoli."))]),
 (33, "1,36,40–41", "Il fine della Scrittura è la carità: errare per i campi verso la stessa meta",
  "Chiusa del libro I del De doctrina christiana (396/397, parte composta prima delle Confessiones). Il criterio "
  "ultimo dell’interpretazione non è l’intenzione dell’autore, ma l’edificazione della duplice carità: chi la "
  "costruisce fraintendendo l’autore sbaglia, ma non mente; va però corretto, perché la via resta preferibile ai campi.",
  [("1.36.40", (None, "nec omnino mentitur."), (None, "lo si può chiamare menzogna.")),
   ("1.36.41", None, None)]),
 (33, "3,10,14; 3,15,23", "Proprio o figurato? La regola per decidere",
  "Il libro III traduce il principio in tecnica: è figurato tutto ciò che, preso alla lettera, non si riferisce "
  "né all’onestà dei costumi né alla verità della fede; e il testo figurato va «rigirato» con diligenza finché "
  "l’interpretazione non giunga al regno della carità. Se la lettera vi giunge già, nessuna figura va supposta.",
  [("3.10.14", (None, "ad cognoscendum Deum et proximum pertinet."), (None, "la conoscenza di Dio e del prossimo.")),
   ("3.15.23", None, None)]),
]

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Garamond"; st.font.size = Pt(11.5)
st.paragraph_format.line_spacing = 1.1
sec = doc.sections[0]
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = Cm(29.7), Cm(21)
sec.left_margin = sec.right_margin = Cm(1.5); sec.top_margin = sec.bottom_margin = Cm(1.5)

def para(text="", size=None, bold=False, italic=False, align=None, color=None, after=None):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = RGBColor(*color)
    if align: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    return p

def add_marked(p, text):
    for part in re.split(r"(\[n\d+\])", text):
        m = re.match(r"\[n(\d+)\]", part)
        if m:
            r = p.add_run(m.group(1)); r.font.superscript = True
        elif part:
            p.add_run(part)

t = doc.add_heading("Agostino e l’esegesi biblica", level=0); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
para("Che cos’è, come si fa — quattro testi prima delle Confessiones (388–397)", 13, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
para("Miniantologia — latino e italiano a fronte", 11, align=WD_ALIGN_PARAGRAPH.CENTER, after=14)
para("Criteri. I testi sono in ordine cronologico; il numero che precede l’opera è quello dell’«Elenco cronologico delle "
     "opere» (datazioni J. Anoz 2002 e G. Catapano 2010). Testo latino e traduzione italiana: Nuova Biblioteca "
     "Agostiniana, www.augustinus.it. I tagli sono indicati con […]; i numeri in apice nel testo italiano rinviano ai "
     "riferimenti scritturistici sotto ciascun passo. Il percorso va dal criterio (lettera/figura, 388–389) alla "
     "tassonomia (i quattro modi, 391) al fondamento (la carità) e alla regola operativa del De doctrina christiana (396/397).",
     9.5, italic=True, after=10)

cache = {}
for k, (n, refdisp, titolo, scheda, segs) in enumerate(TESTI, 1):
    if n not in cache: cache[n] = load(n)
    paras, notes = cache[n]
    o = META[n]
    h = doc.add_heading(f"{k}. {o[2]} {refdisp} — {titolo}", level=1)
    para(f"{n}. {o[1]} — {o[4]} — composizione: {o[5]}", 10, italic=True, color=(0x44, 0x44, 0x44), after=4)
    para(scheda, 10.5, after=8)
    table = doc.add_table(rows=1, cols=2); table.style = "Table Grid"; table.autofit = False
    for c, lab in zip(table.rows[0].cells, ("Latino", "Italiano")):
        c.text = ""; r = c.paragraphs[0].add_run(lab); r.bold = True; r.font.size = Pt(10); shade(c, "F2F2F2")
    rif = []
    for ref, cl, ci in segs:
        assert ref in paras, (n, ref)
        la = re.sub(r"\[n\d+\]", "", cut(paras[ref]["LA"], cl))
        la = la.replace("quadrifariam d traditur", "quadrifariam traditur")
        la = re.sub(r"\s+([.,;:])", r"\1", la)
        it = cut(paras[ref]["IT"], ci)
        it = re.sub(r"\s+(\[n\d+\])", r"\1", it)
        cells = table.add_row().cells
        lp = cells[0].paragraphs[0]; lp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; add_marked(lp, la)
        ip = cells[1].paragraphs[0]; ip.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; add_marked(ip, it)
        rif += [f"{x}. {notes.get((ref, int(x)), '')}" for x in re.findall(r"\[n(\d+)\]", it)]
        print(f"  {n:>2} {ref:<8} LA {len(la):5d}  IT {len(it):5d}")
    for row in table.rows:
        for c in row.cells: c.width = Cm(13.3)
    if rif:
        p = para(after=12); r = p.add_run("Rif.: " + "; ".join(rif)); r.font.size = Pt(8.5)
    else:
        para(after=12)

for p in doc.paragraphs:
    for r in p.runs: force_font(r)
for tbx in doc.tables:
    for row in tbx.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs: force_font(r)
os.makedirs(OUTDIR, exist_ok=True)
doc.save(OUT)
print("SALVATO", OUT)

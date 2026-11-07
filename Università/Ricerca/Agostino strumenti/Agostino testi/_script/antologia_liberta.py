# -*- coding: utf-8 -*-
"""Miniantologia «Agostino: il male, la volontà, la libertà» (linea di L'eterno assente) (latino/italiano) dal corpus _md."""
import re, os, glob
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from build import shade, force_font
from opere import OPERE

MD = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi/Opere/_md"
OUTDIR = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi/Antologie"
OUT = os.path.join(OUTDIR, "Agostino - il male, la volontà, la libertà - antologia lat-ita.docx")
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

def cut(text, segs):
    """segs: None (tutto) o lista di (inizio, fine) inclusivi; più segmenti uniti da […]"""
    if not segs:
        return text
    out = []; end = 0
    for a, b in segs:
        i = text.find(a) if a else 0
        assert i >= 0, f"inizio non trovato: {a!r}"
        if b:
            j = text.find(b, i)
            assert j >= 0, f"fine non trovata: {b!r}"
            end = j + len(b)
        else:
            end = len(text)
        out.append(text[i:end].strip())
    return ("[…] " if segs[0][0] else "") + " […] ".join(out) + (" […]" if text[end:].strip() else "")

# (num, rif. visualizzato, titolo, scheda, [(ref, tagli LA, tagli IT), …])
TESTI = [
 (11, "1,1,1; 1,2,4; 1,16,35", "Unde malum? Ciascuno è autore del proprio male",
  "Roma, 388. Il dialogo si apre sulla domanda che aveva spinto il giovane Agostino tra i Manichei: Dio è autore del "
  "male? Distinti il male che si fa e quello che si subisce (la pena, che viene da Dio giusto), del primo «ciascun "
  "malvagio è autore»: le azioni malvagie non sarebbero giustamente punite se non fossero volontarie. Il male fatto "
  "è un’aversio dalle realtà immutabili e una conversio a quelle mutevoli, che pure stanno «nel loro ordine». "
  "Unico ente capace di pensare l’ordine e di decidere se conformarvisi, l’uomo ne è insieme parte e potenziale "
  "eversore: la volontà è il ‘perturbante’ della metafisica dell’ordine. Di qui la domanda, angosciata e fondativa, "
  "che chiude il libro: era opportuno che Dio ci desse il libero arbitrio?",
  [("1.1.1", None, None),
   ("1.2.4", [("Eam quaestionem moves", None)], [("Poni appunto il problema", None)]),
   ("1.16.35", [(None, "malefactorum nostrorum auctor existimetur.")], [(None, "autore delle nostre cattive azioni.")])]),
 (11, "2,1,1.3; 2,19,53–20,54", "Perché Dio ha dato la libertà: un bene medio che cade da sé e non si rialza da sé",
  "Il libro II (Africa, 391–395) rovescia la domanda di Evodio. La volontà libera non è data per peccare, ma perché "
  "senza di essa «homo recte non potest vivere»; ed è la condizione della giustizia di Dio, perché senza di essa "
  "pena e premio sarebbero ingiusti. È un medium bonum, che può aderire al bene comune e immutabile o volgersi al "
  "proprio, all’esterno, all’inferiore: male non sono i beni amati, né la volontà, ma la sua aversio. Quel moto è "
  "defectivus, viene dal nulla e non si può conoscere; è volontario e dunque in nostro potere. Ma la chiusa segna il "
  "limite: l’uomo non può rialzarsi spontaneamente come spontaneamente è caduto; occorre la mano di Dio tesa dall’alto.",
  [("2.1.1", [(None, "peccare non posset.")], [(None, "non potrebbe peccare.")]),
   ("2.1.3", None, None),
   ("2.19.53", None, None),
   ("2.20.54", [("Motus ergo ille aversionis", "caritate ardenti desideremus.")],
               [("Ora noi ammettiamo che quel movimento", "cioè il nostro Signore Gesù Cristo.")])]),
 (11, "3,2,4; 3,3,8; 3,9,26", "Prescienza e ordine: la libertà dentro il disegno di Dio",
  "Il libro III affronta l’obiezione più radicale: se Dio sa tutto in anticipo, come può essere libera la volontà? "
  "Nulla è tanto in nostro potere quanto il volere stesso, e Dio, conoscendo atti liberi, li conosce come liberi. "
  "Ma subito ritorna la metafisica dell’ordine: l’universo resta «plenum atque perfectum» sia con la beatitudine dei "
  "giusti sia con la miseria dei peccatori, e la pena riconduce all’ordine la «perturbazione» volontaria del "
  "peccato. Se Dio deve essere giusto nel giudicare, le azioni umane devono essere libere: negarne la libertà "
  "vorrebbe dire negare la giustizia con cui Dio regge l’universo. La stessa soluzione tornerà, contro Cicerone, in "
  "De civitate Dei V, 9–10.",
  [("3.2.4", [(None, "et nos nulla necessitate peccemus."), ("Quomodo est igitur voluntas libera", "necessitas?")],
             [(None, "non pecchiamo per necessità."), ("Quindi come può esser libera", "necessità?")]),
   ("3.3.8", [("Voluntas igitur nostra nec voluntas esset", "adfuturam mihi esse praescivit.")],
             [("Dunque la nostra volontà non sarebbe volontà", "che l'avrò.")]),
   ("3.9.26", [("Hic respondetur", None)], [("Si risponde che", None)])]),
 (97, "2,4; 21,43", "Libero, eppure inclinato da Dio: l’argilla e il vasaio",
  "Ai monaci di Adrumeto, 426–427: una delle ultime opere, non polemica. Prima affermazione netta: il libero arbitrio "
  "esiste, perché senza di esso i comandi di Dio («Noli…») sarebbero insensati; chi pecca incolpi se stesso, non Dio. "
  "Poi la tesi opposta e complementare: Dio opera nei cuori per inclinare le volontà dove vuole, al bene per "
  "misericordia, al male per i loro meriti, con un giudizio a volte palese, a volte occulto, sempre giusto. È il "
  "nodo delle Conclusioni de L’eterno assente: l’uomo è predestinato se visto con l’occhio di Dio, libero se "
  "osservato con lo sguardo umano. Nel coevo De correptione et gratia (5,8) l’immagine di Rm 9,20–21: «absit ut "
  "dicamus iudicium luti esse debere, sed figuli».",
  [("2.4", [(None, "nisi liberum arbitrium voluntatis humanae?"), ("Nempe ubi dicitur", "sibi imputet quisque, cum peccat.")],
           [(None, "se non il libero arbitrio della volontà umana?"), ("Quindi certamente quando si dice", "ciascuno incolpi se stesso;")]),
   ("21.43", [(None, "gratis datur.")], [(None, "viene data gratuitamente.")])]),
 (30, "1,1,11.14", "«Hoc restat libero arbitrio»: volere sì, compiere no",
  "Ippona, 396: la prima opera dell’episcopato, e il punto a cui il vecchio Agostino stesso fa risalire la soluzione "
  "(«quam mihi Deus in hac quaestione solvenda, cum ad episcopum Simplicianum […] scriberem, revelavit», praed. sanct. "
  "4,8). Commentando Rm 7, conserva il libero arbitrio («ipsum velle in potestate est») ma gli sottrae il perficere "
  "bonum, perduto con il peccato originale, «quasi seconda natura». Al libero arbitrio resta soltanto di convertirsi, "
  "con supplice pietà, a colui per il cui dono si può compiere la giustizia: «laboratum est quidem pro libero arbitrio "
  "voluntatis humanae, sed vicit Dei gratia» (retr. 2,1,1). Non un Agostino ‘nuovo’, però: la conversio sollecitata "
  "dall’admonitio divina è al fondo della sua riflessione sin dai primi dialoghi.",
  [("1.1.11", [(None, "subditos sibi per fidem.")], [(None, "mediante la fede.")]),
   ("1.1.14", [("Humiliter ergo dicendum", None)], [("Deve dunque dire umilmente", None)])]),
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

t = doc.add_heading("Agostino: il male, la volontà, la libertà", level=0); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
para("Dalla volontà ‘perturbante’ dell’ordine all’Ad Simplicianum — cinque testi", 13, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
para("Miniantologia — latino e italiano a fronte", 11, align=WD_ALIGN_PARAGRAPH.CENTER, after=14)
para("Criteri. Il numero che precede l’opera è quello dell’«Elenco cronologico delle opere» (datazioni J. Anoz 2002 "
     "e G. Catapano 2010). Testo latino e traduzione italiana: Nuova Biblioteca Agostiniana, www.augustinus.it. I tagli "
     "sono indicati con […]; i numeri in apice nel testo italiano rinviano ai riferimenti scritturistici sotto ciascun "
     "passo. Il percorso segue la lettura proposta in A. Bisogno, L’eterno assente: il male fatto come aversio e la "
     "volontà come elemento ‘perturbante’ della metafisica dell’ordine (De libero arbitrio I, 388); la libertà come bene "
     "medio e condizione della giustizia di Dio, compatibile con la sua prescienza e iscritta nel suo ordine (De libero "
     "arbitrio II–III, 391–395); l’esito tardo della riflessione, tra libero arbitrio e grazia che inclina le volontà "
     "(De gratia et libero arbitrio, 426–427). L’antologia si chiude, fuori dall’ordine cronologico, con l’Ad "
     "Simplicianum (396): il luogo in cui, per ammissione dello stesso Agostino, la questione fu decisa.",
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

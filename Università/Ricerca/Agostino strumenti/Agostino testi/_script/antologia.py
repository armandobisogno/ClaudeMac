# -*- coding: utf-8 -*-
"""Antologia «Agostino e i Manichei» (latino/italiano) dal corpus _md."""
import re, os, glob
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from build import shade, force_font
from opere import OPERE

MD = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi/Opere/_md"
OUTDIR = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi/Antologie"
OUT = os.path.join(OUTDIR, "Agostino e i Manichei - antologia lat-ita.docx")
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
    head = "[…] " if segs[0][0] else ""
    tail = " […]" if text[end:].strip() else ""
    return head + " […] ".join(out) + tail

# (num, ref, tema, taglio LA, taglio IT)
P1 = [
 (2, "1.4", "La luce «che si vede con gli occhi»: il primo ricordo dell'esperienza manichea",
  [("Ego ab usque undevigesimo", "Academici tenuerunt.")], [("Fin dal diciannovesimo", "con tutti i venti.")]),
 (9, "1.1.2", "Le due esche dei Manichei: la critica delle Scritture e l'apparenza della continenza",
  [(None, "quam difficile habere virtutem.")], [(None, "quanto sia difficile possederla.")]),
 (9, "2.10.19", "I tre «sigilli»: bocca, mani, seno",
  [(None, "castus et innocens homo sit.")], [(None, "deve essere casto e innocente.")]),
 (9, "2.19.68", "Nove anni da uditore: che cosa Agostino ha visto degli Eletti", None, None),
 (11, "1.2.4", "Unde malum? La domanda che lo spinse tra gli eretici",
  [("Eam quaestionem moves", "quem secutus evasi.")], [("Poni appunto il problema", "io stesso mi sono reso libero.")]),
 (14, "1.2.3", "«Che cosa faceva Dio prima di creare?»: l'obiezione manichea alla Genesi",
  [(None, "nisi qui est ante tempora.")], [(None, "prima della successione dei tempi.")]),
 (16, "9.16", "Due nature, due anime, un Dio costretto a combattere",
  [("Contra eos tamen", None)], [("Esso, tuttavia, si rivolge", None)]),
 (17, "1.2", "La promessa della «pura e semplice ragione»",
  [("Nosti enim, Honorate", "in suis probandis firmos et certos manere?")],
  [("Tu sai infatti, o Onorato", "fermi e sicuri nel dimostrare le proprie.")]),
 (18, "9.11", "Perché restò: l'amicizia e le facili vittorie nelle dispute", None, None),
 (18, "11.15", "La definizione del peccato: la volontà contro le «due anime»",
  [(None, "Sed malui grossius quam scrupulosius definire.")], [(None, "anziché scrupoloso.")]),
 (19, "1.1", "Il dibattito pubblico: «ritengo errore ciò che prima ritenevo verità»",
  [(None, "ut nos in aerumnas praecipitaret.")], [(None, "di precipitarci tra i tormenti.")]),
 (19, "3.3", "Uditore, non Eletto: la preghiera rivolta al sole",
  [("Nostis autem me non Electum", "nihil novi comperi.")], [("Ora voi sapete che io non sono stato", "non ho trovato niente di nuovo.")]),
 (19, "37.37", "Fortunato non sa rispondere",
  [(None, "catholicam fidem, si permittunt et volunt, exponam.")], [(None, "io esporrò a tutti i nostri ascoltatori e testimoni, poiché sono dei fedeli, la fede cattolica.")]),
 (31, "2.2", "«Infieriscano contro di voi…»: la mitezza di chi è stato nell'errore", None, None),
 (31, "3.3", "Agostino «quondam manichaeus»", None, None),
 (31, "5.6", "L'incipit della Lettera del Fondamento e l'autorità della Chiesa",
  [(None, "nisi me catholicae Ecclesiae commoveret auctoritas.")], [(None, "l’autorità della Chiesa cattolica.")]),
]
PC = [
 (34, "3.6.10", "L'ingresso nella setta: «Veritas et veritas»",
  [(None, "esuriebam et sitiebam .")], [(None, "avevo fame e sete [n28].")]),
 (34, "5.6.10", "L'attesa di Fausto e la delusione",
  [(None, "quia vultus congruus et decorum eloquium.")], [(None, "elegante l'eloquio.")]),
 (34, "5.10.18", "«Non siamo noi a peccare»: la comodità del dualismo",
  [("Adhuc enim mihi videbatur", "me diviserat ,")], [("Ero tuttora del parere", "la mia empietà [n70].")]),
]
P2 = [
 (39, "1.1", "Il principio anti-dualista: tutto ciò che è, è bene e viene da Dio",
  [(None, "et spiritalia et corporalia.")], [(None, "spirituali e corporei.")]),
 (39, "41.41", "Il rovesciamento: beni nel regno del male, mali nella natura di Dio",
  [(None, "immoderationem, deformitatem, perversitatem.")], [(None, "smoderatezza, deformità, pervertimento.")]),
 (40, "1.1.1", "Ritratto di Fausto, «che ho conosciuto, come ricordo nelle Confessioni»",
  [(None, "nisi a Domino gressus hominis dirigantur .")], [(None, "non sono guidati dal Signore [n1].")]),
 (40, "5.1.1", "La voce di Fausto: «Accetti il Vangelo?» L'ascesi come prova",
  [(None, "persecutiones et odia sustinentem propter iustitiam; et dubitas utrum accipiam Evangelium?")],
  [(None, "che soffre persecuzioni e odi per la giustizia, e dubiti che accetti il Vangelo?")]),
 (40, "20.2.2", "La «trinità» manichea: il Padre nella luce, il Figlio nel sole e nella luna, il Iesus patibilis",
  [(None, "omni suspensus ex ligno.")], [(None, "che pende da ogni pianta.")]),
 (42, "1.3.3", "Secondino ad Agostino: «un sommo oratore, mai un cristiano»",
  [(None, "persequi te Hannibalem atque Mithridatem."), ("Novi ego te haec semper odio habuisse", "Quis igitur ille est qui te repente mutavit?")],
  [(None, "tu attacchi Annibale e Mitridate."), ("So che hai sempre detestato queste cose", "Chi è stato dunque che all’improvviso ti ha cambiato?")]),
 (42, "2.2.2", "La risposta: «Ho lasciato i Manichei per paura»",
  [(None, "sed in natura incommutabili malum esse putaverit?")], [(None, "ma nella natura immutabile?")]),
 (42, "2.24.24", "Mutare è possibile solo a chi non è sostanza di Dio",
  [(None, "nisi quibus displicet incommutabilis Deus.")], [(None, "a cui dispiace un Dio immutabile.")]),
 (52, "1.1.1", "Ippona, dicembre 404: il codice della Lettera del Fondamento sul tavolo", None, None),
 (52, "2.22.22", "L'anatema di Felice", None, None),
]

PERCORSO = [
 ("1. L'esperienza", "nove anni da uditore; la promessa della ragione contro l'autorità; amicizia e dispute",
  "beata v. 1,4; util. cred. 1,2; duab. an. 9,11; c. Fort. 3; conf. 3,6,10; 5,6,10"),
 ("2. La dottrina riferita", "due principi, due anime, Dio costretto alla guerra; i tre sigilli; il Iesus patibilis",
  "mor. 2,10,19; vera rel. 9,16; c. Fort. 1; c. Faust. 20,2; nat. b. 41"),
 ("3. La risposta filosofica", "unde malum; la volontà e il peccato; il bene come tutto ciò che è",
  "lib. arb. 1,2,4; duab. an. 11,15; conf. 5,10,18; nat. b. 1; c. Sec. 2; 24"),
 ("4. Scrittura e autorità", "Genesi e Antico Testamento; «Evangelio non crederem»; l'ascesi di Fausto",
  "mor. 1,1,2; Gn. adv. Man. 1,2,3; c. ep. Man. 5,6; c. Faust. 5,1"),
 ("5. Lo stile della polemica", "dalla mitezza del converso al dibattito pubblico e all'anatema",
  "c. ep. Man. 2,2–3,3; c. Fort. 37; Secundini ep. 3; c. Fel. 1,1; 2,22"),
]

# ---------------- docx ----------------
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
    """testo con marcatori [nN] -> numeri in apice"""
    for part in re.split(r"(\[n\d+\])", text):
        m = re.match(r"\[n(\d+)\]", part)
        if m:
            r = p.add_run(m.group(1)); r.font.superscript = True
        elif part:
            for k, line in enumerate(part.split(" / ")):
                if k: p.add_run().add_break()
                p.add_run(line)

t = doc.add_heading("Agostino e i Manichei", level=0); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
para("Antologia di testi — latino e italiano a fronte", 13, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
para("Materiali per una lezione di un’ora", 11, align=WD_ALIGN_PARAGRAPH.CENTER, after=14)
para("Criteri. I passi sono disposti in ordine cronologico e divisi in due parti: prima della stesura delle Confessiones "
     "(386–396/397) e dopo (dal 400). Tra le due parti, come cerniera, tre passi delle Confessiones (397–401/403), che "
     "rileggono a distanza l’esperienza manichea. Il numero che precede ogni titolo è quello dell’«Elenco cronologico "
     "delle opere»; la datazione segue J. Anoz (2002) e G. Catapano (2010). Testo latino e traduzione italiana: Nuova "
     "Biblioteca Agostiniana, www.augustinus.it. I tagli sono indicati con […]; i numeri in apice nel testo italiano "
     "rinviano ai riferimenti scritturistici riportati sotto ciascun passo.", 9.5, italic=True)
para("Percorso suggerito (cinque nuclei, circa 10–12 minuti ciascuno)", 11, bold=True)
tb = doc.add_table(rows=1, cols=3); tb.style = "Table Grid"
for c, h in zip(tb.rows[0].cells, ("Nucleo", "Contenuto", "Passi")):
    c.text = ""; r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(10); shade(c, "E8E8E8")
for row in PERCORSO:
    cells = tb.add_row().cells
    for c, v in zip(cells, row):
        c.text = ""; r = c.paragraphs[0].add_run(v); r.font.size = Pt(10)
for row in tb.rows:
    for c, w in zip(row.cells, (Cm(4.5), Cm(11), Cm(11))): c.width = w

cache = {}
def passage(n, ref, tema, cl, ci):
    if n not in cache: cache[n] = load(n)
    paras, notes = cache[n]
    assert ref in paras, (n, ref)
    la = cut(paras[ref]["LA"], cl); it = cut(paras[ref]["IT"], ci)
    la = re.sub(r"\[n\d+\]", "", la)
    sig = META[n][2]
    parts = ref.split(".")
    if n in (19, 39, 40, 42, 52) and len(parts) >= 2 and parts[-1] == parts[-2]:
        parts = parts[:-1]          # es. 37.37 -> 37 ; 5.1.1 -> 5.1
    if n == 42:                     # l. I = lettera di Secondino; l. II = c. Sec.
        sig = "Secundini ep." if parts[0] == "1" else "c. Sec."
        parts = parts[1:]
    refdisp = ",".join(parts)
    table = doc.add_table(rows=2, cols=2); table.style = "Table Grid"; table.autofit = False
    h = table.cell(0, 0).merge(table.cell(0, 1)); h.text = ""
    r = h.paragraphs[0].add_run(f"{sig} {refdisp}"); r.bold = True
    r = h.paragraphs[0].add_run(f"  —  {tema}"); r.italic = True
    shade(h, "F2F2F2")
    lp = table.cell(1, 0).paragraphs[0]; lp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; add_marked(lp, la)
    ip = table.cell(1, 1).paragraphs[0]; ip.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; add_marked(ip, it)
    for row in table.rows:
        for c in row.cells: c.width = Cm(13.3)
    used = [int(x) for x in re.findall(r"\[n(\d+)\]", it)]
    if used:
        p = para(size=8.5, after=10)
        rr = p.add_run("Rif.: " + "; ".join(f"{k}. {notes.get((ref, k), '')}" for k in used)); rr.font.size = Pt(8.5)
    else:
        para(after=6)
    return len(la), len(it)

def part(title, sub, items):
    doc.add_page_break()
    h = doc.add_heading(title, level=1); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(sub, 10.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=10)
    cur = None; tot = 0
    for n, ref, tema, cl, ci in items:
        if n != cur:
            cur = n; o = META[n]
            p = doc.add_heading(f"{n}. {o[1]}", level=2)
            para(f"{o[4]} — composizione: {o[5]}", 10, italic=True, color=(0x44, 0x44, 0x44), after=6)
        a, b = passage(n, ref, tema, cl, ci); tot += a
        print(f"  {n:>2} {ref:<8} LA {a:5d}  IT {b:5d}")
    return tot

t1 = part("Parte prima — Prima della stesura delle Confessiones",
          "Dal ritiro di Cassiciaco all’episcopato (386–396/397): il convertito rilegge la propria esperienza e affronta i Manichei in pubblico", P1)
tc = part("Cerniera — Le Confessiones (397–401/403)",
          "L’esperienza manichea nel racconto autobiografico", PC)
t2 = part("Parte seconda — Dopo la stesura delle Confessiones",
          "Il vescovo di Ippona (400–405): confutazione dottrinale, polemica scritta, dibattito pubblico", P2)
print("caratteri latino:", t1, tc, t2, "tot", t1 + tc + t2)

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

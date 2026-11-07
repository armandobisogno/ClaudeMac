# -*- coding: utf-8 -*-
"""Genera, per ogni opera, un .docx (latino/italiano a fronte, sul modello delle
Confessioni) e un .md (testo per la ricerca, un paragrafo per riga con riferimento)."""
import re, os, sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from parse import load_work, runs_text
from opere import OPERE

OUT = "/Users/macbook/Library/CloudStorage/Dropbox/ClaudeWS/Università/Ricerca/Agostino strumenti/Agostino testi/Opere"
MD = os.path.join(OUT, "_md")
DATA_CONS = "30 settembre 2026"
FONT = "Garamond"
SPECIAL = True   # casi particolari validi solo per il corpus delle opere
ROMAN = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII XXIII XXIV XXV XXVI XXVII XXVIII XXIX XXX XXXI XXXII XXXIII".split()
SEC_RE = re.compile(r"\(\s*\d+\s*,\s*\d+[^)]*\)\s*\.?\s*$")
CAPS = lambda s: len(s) > 3 and s.upper() == s and any(c.isalpha() for c in s)

def safe(s):
    return re.sub(r'[\\/:*?"<>|]', "", s)

# ---------- normalizzazione degli item ----------
def normalize(items):
    """Riclassifica i paragrafi senza ancora: titoletti di sezione -> heading;
    '[ inizio pagina ]' -> scartato; il resto resta continuazione."""
    out = []
    for it in items:
        if it[0] == "c":
            t = runs_text(it[2], notes=False)
            if not t or "inizio pagina" in t.lower():
                continue
            if len(t) < 220 and (SEC_RE.search(t) or CAPS(t)):
                out.append(("h", 4, it[2])); continue
        out.append(it)
    return out

def book_of(pp):
    for it in pp["items"]:
        if it[0] == "p":
            return it[1][0]
    return None

def books(lang_data):
    """-> ordered dict book -> dict(head=[...], items=[...], notes={})"""
    res = {}
    order = []
    for pp in lang_data["texts"]:
        cur = book_of(pp)
        items = normalize(pp["items"])
        if cur not in res:
            res[cur] = dict(head=[h for h in pp["head"]], items=[], notes={})
            order.append(cur)
        # un file può contenere più libri: ridistribuisci per chiave
        pending = []
        for it in items:
            if it[0] == "p" and it[1][0] != cur:
                cur = it[1][0]
                if cur not in res:
                    res[cur] = dict(head=[], items=[], notes={}); order.append(cur)
                res[cur]["items"].extend(pending); pending = []
            if it[0] == "h":
                pending.append(it); continue
            res[cur]["items"].extend(pending); pending = []
            res[cur]["items"].append(it)
        res[cur]["items"].extend(pending)
        res[cur]["notes"].update({(pp["page"] if not k[0] else k[0], k[1]): v for k, v in pp["notes"].items()})
        res[cur].setdefault("pages", []).append(pp["page"])
    return order, res

def grouped(items):
    groups, order, pending = {}, [], []
    for it in items:
        if it[0] == "h":
            pending.append(it); continue
        if it[0] == "c":
            if order:
                g = groups[order[-1]]
                g["runs"].append(("t", "\n", False, False)); g["runs"].extend(it[2])
            continue
        key = it[1]
        if key not in groups:
            groups[key] = {"heads": [], "runs": []}; order.append(key)
        else:
            groups[key]["runs"].append(("t", "\n", False, False))
        groups[key]["heads"].extend(pending); pending = []
        groups[key]["runs"].extend(it[2])
    return order, groups

def merge_keys(a, b):
    keys = list(a)
    sa = set(a)
    for k in b:
        if k not in sa:
            keys.append(k)
    keys.sort()
    return keys

# ---------- docx helpers ----------
def add_runs(par, runs, size=None):
    for r in runs:
        if r[0] == "n":
            run = par.add_run(r[1]); run.font.superscript = True
        else:
            parts = r[1].split("\n")
            for j, ptxt in enumerate(parts):
                if j:
                    par.add_run().add_break()
                if ptxt:
                    run = par.add_run(ptxt); run.bold = r[2]; run.italic = r[3]
                    if size: run.font.size = size

def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), color)
    tcPr.append(sh)

def force_font(run):
    run.font.name = FONT
    rPr = run._r.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rPr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), FONT)

def new_doc():
    doc = Document()
    st = doc.styles["Normal"]; st.font.name = FONT; st.font.size = Pt(12)
    st.paragraph_format.line_spacing = 1.15
    for s in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        doc.styles[s].font.name = FONT
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Cm(29.7), Cm(21)
    sec.left_margin = sec.right_margin = Cm(1.5)
    sec.top_margin = sec.bottom_margin = Cm(1.6)
    return doc

def label_book(b, lat_head, ita_head, multi):
    if b == 0:
        return "PROLOGUS", "PROLOGO"
    lh = next((t for tag, t in lat_head if tag in ("h2", "h3") and re.search(r"LIBER|PROLOG|PRAEF|EPILOG|CAPUT|TRACTATUS|QUAESTIO", t, re.I)), None)
    ih = next((t for tag, t in ita_head if tag in ("h2", "h3", "h4") and re.search(r"LIBRO|PROLOG|PREFAZ|EPILOG|CAPITOLO|TRATTATO|QUESTIONE", t, re.I)), None)
    return (lh or f"LIBER {ROMAN[b-1] if b <= len(ROMAN) else b}", ih or f"LIBRO {ROMAN[b-1] if b <= len(ROMAN) else b}")

def theme_lines(head, label):
    """righe del titolo di libro diverse dall'etichetta (es. tema del libro)"""
    out = []
    for tag, t in head:
        if t == label or t.upper() in ("AUGUSTINUS HIPPONENSIS", "SANT'AGOSTINO"):
            continue
        if tag in ("h1", "h2", "h3") or CAPS(t):
            out.append(t)
    return out

# ---------- build ----------
def build(num):
    meta = next(o for o in OPERE if o[0] == num)
    _, tlat, sigla, folder, tita, data, nota = meta
    from opere import ITA_FOLDER
    ifolder = ITA_FOLDER.get(folder, folder)
    d = load_work(folder)
    lo, lb = books(d["latino"])
    io, ib = books(d["italiano"])
    if num == 61 and SPECIAL:
        # Gesta collationis: l'italiano (NBA) traduce solo gli interventi di Agostino, Alipio, Possidio,
        # numerati (1, gruppo, N): gruppi 1-3 / 4-6 / 7-9 = giorni 1-3 -> latino (giorno, N, 1)
        nb = {}
        src = ib.get(1, dict(items=[], notes={}))
        for it in src["items"]:
            if it[0] != "p":
                continue
            day = (it[1][1] - 1) % 3 + 1
            nb.setdefault(day, dict(head=[], items=[], notes=src["notes"]))["items"].append(("p", (day, it[1][2], 1), it[2]))
        ib = nb; io = sorted(nb)
    bks = merge_keys(lo, io)
    multi = len([b for b in bks if b]) > 1

    os.makedirs(OUT, exist_ok=True); os.makedirs(MD, exist_ok=True)
    fname = f"{num}. {safe(tlat)}"
    doc = new_doc()
    md = []

    t = doc.add_heading(f"{num}. {tlat}", level=0); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(tita); r.italic = True
    p = doc.add_paragraph(f"Testo latino e traduzione italiana a fronte · {data}"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fonte = [
        "Fonte di questa versione. Il testo latino e la traduzione italiana sono ripresi dall’edizione digitale della "
        "Nuova Biblioteca Agostiniana (Città Nuova Editrice), pubblicata sul sito www.augustinus.it:",
        f"· testo latino: https://www.augustinus.it/latino/{folder}{'' if folder.endswith('.htm') else '/'};",
        f"· traduzione italiana: https://www.augustinus.it/italiano/{ifolder}{'' if ifolder.endswith('.htm') else '/'}.",
        f"Consultazione: {DATA_CONS}. La numerazione di libri, capitoli e paragrafi segue quella dell’edizione. "
        "Le note in calce a ciascun libro riproducono l’apparato di riferimenti della versione italiana; "
        "i rimandi nel testo latino sono stati omessi. "
        f"Posizione nell’elenco cronologico: n. {num} (datazione: {data}{'; ' + nota if nota else ''}).",
    ]
    for line in fonte:
        p = doc.add_paragraph(line)
        for rr in p.runs: rr.font.size = Pt(8.5); rr.italic = True

    md += [f"# {num}. {tlat}", "", f"*{tita}* — sigla: **{sigla}** — datazione: {data}" + (f" — {nota}" if nota else ""), "",
           f"Fonte: NBA / www.augustinus.it (latino/{folder}, italiano/{ifolder}), consultazione {DATA_CONS}.",
           "Formato: ogni paragrafo occupa una riga, preceduta dal riferimento [libro.capitolo.paragrafo] (o [capitolo.paragrafo] per le opere in un solo libro) e dalla lingua (LA/IT).",
           "I rimandi [nN] nel testo italiano rinviano alle note in fondo a ciascun libro.", ""]

    # introduzione italiana (schede NBA), se presente
    intro = d["italiano"]["intro"]
    if intro:
        doc.add_page_break()
        h = doc.add_heading("Introduzione (dall’edizione NBA)", level=2)
        md += ["## Introduzione (dall’edizione NBA)", ""]
        for tag, txt in intro:
            p = doc.add_paragraph()
            rr = p.add_run(txt); rr.font.size = Pt(10)
            if tag.startswith("h"):
                rr.bold = True
            md.append(("**%s**" % txt) if tag.startswith("h") else txt)
            md.append("")

    stats = []
    parts = [(lo, lb, io, ib, bks, multi, "")]
    if num == 6:   # De grammatica: in appendice le Regulae
        d2 = load_work("regole"); a1, a2 = books(d2["latino"]); c1, c2 = books(d2["italiano"])
        parts.append((a1, a2, c1, c2, merge_keys(a1, c1), False, "reg."))
    for lo, lb, io, ib, bks, multi, rpre in parts:
      if rpre:
        doc.add_page_break()
        h = doc.add_heading("APPENDIX — Regulae (De grammatica: Regulae)", level=1); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        md += ["## APPENDIX — Regulae (De grammatica: Regulae) — riferimenti con prefisso «reg.»", ""]
      for b in bks:
        L = lb.get(b, dict(head=[], items=[], notes={}))
        I = ib.get(b, dict(head=[], items=[], notes={}))
        lab_l, lab_i = label_book(b, L["head"], I["head"], multi)
        if not rpre: doc.add_page_break()
        if multi or b == 0:
            h = doc.add_heading(f"{lab_l} — {lab_i}" if lab_l.upper() != lab_i.upper() else lab_l, level=1)
            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
            md += [f"## {lab_l} — {lab_i}", ""]
        for tl in theme_lines(L["head"], lab_l):
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rr = p.add_run(tl); rr.bold = True; rr.italic = True
            md.append(f"**LA:** {tl}  ")
        for tl in theme_lines(I["head"], lab_i):
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rr = p.add_run(tl); rr.bold = True; rr.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
            md.append(f"**IT:** {tl}  ")
        md.append("")

        lo_, lg = grouped(L["items"]); io_, ig = grouped(I["items"])
        if not (num == 61 and SPECIAL) and len(lo_) == len(io_) and set(lo_) != set(io_):
            # numerazione divergente nel sorgente: allineamento per posizione
            ig = {lk: ig[ik] for lk, ik in zip(lo_, io_)}; io_ = list(lo_)
        keys = merge_keys(lo_, io_)
        table = doc.add_table(rows=1, cols=2); table.style = "Table Grid"; table.autofit = False
        for c, lbl in zip(table.rows[0].cells, ("LATINO", "ITALIANO")):
            pp = c.paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rr = pp.add_run(lbl); rr.bold = True; shade(c, "E8E8E8")
        used = []   # (page,num) in ordine di apparizione
        for k in keys:
            lgp = lg.get(k, {"heads": [], "runs": []}); igp = ig.get(k, {"heads": [], "runs": []})
            lh, ih = lgp["heads"], igp["heads"]
            for hidx in range(max(len(lh), len(ih))):
                row = table.add_row().cells
                for cell, hs in ((row[0], lh), (row[1], ih)):
                    pp = cell.paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    if hidx < len(hs):
                        lvl = hs[hidx][1]
                        add_runs(pp, [x for x in hs[hidx][2] if x[0] != "n"])
                        for rn in pp.runs:
                            rn.bold = True; rn.italic = lvl >= 5; rn.font.size = Pt(11 if lvl >= 5 else 12)
                    shade(cell, "F2F2F2")
                lt = runs_text([x for x in lh[hidx][2] if x[0] != "n"]) if hidx < len(lh) else ""
                it_ = runs_text([x for x in ih[hidx][2] if x[0] != "n"]) if hidx < len(ih) else ""
                md.append(("#### " + lt + (" | " + it_ if it_ else "")).replace("\n", " "))
            row = table.add_row().cells
            lp = row[0].paragraphs[0]; lp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_runs(lp, [x for x in lgp["runs"] if x[0] != "n"])
            ip = row[1].paragraphs[0]; ip.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_runs(ip, igp["runs"])
            ref = (f"prol.{k[2]}" if b == 0 else f"{b}.{k[1]}.{k[2]}") if multi or b == 0 else f"{k[1]}.{k[2]}"
            if not multi and b != 0 and k[2] == 0: ref = f"{k[1]}"
            ref = rpre + ref
            lat_txt = runs_text([x for x in lgp["runs"] if x[0] != "n"]).replace("\n", " / ")
            ita_txt = runs_text(igp["runs"]).replace("\n", " / ")
            md.append(f"[{ref}] LA: {lat_txt}")
            md.append(f"[{ref}] IT: {ita_txt}")
            md.append("")
            for x in igp["runs"]:
                if x[0] == "n":
                    used.append(((x[2], int(x[1])), ref))
        for row in table.rows:
            for c in row.cells:
                c.width = Cm(13.3)

        if used:
            doc.add_paragraph()
            np_ = doc.add_paragraph()
            nr = np_.add_run(f"Note — {lab_i.title() if multi else 'testo'}"); nr.bold = True; nr.font.size = Pt(11)
            md += [f"### Note — {lab_i}", ""]
            seen = set()
            for (pk, n), ref in used:
                if (pk, n) in seen: continue
                seen.add((pk, n))
                txt = I["notes"].get((pk, n)) or next((v for (pg, nn), v in I["notes"].items() if nn == n), "")
                pp = doc.add_paragraph()
                pp.paragraph_format.left_indent = Cm(0.8); pp.paragraph_format.first_line_indent = Cm(-0.8)
                pp.paragraph_format.space_after = Pt(2); pp.paragraph_format.line_spacing = 1.05
                rn = pp.add_run(f"{n}. "); rn.bold = True; rn.font.size = Pt(8.5)
                rt = pp.add_run(txt); rt.font.size = Pt(8.5)
                md.append(f"[n{n} @{ref}] {txt}")
            md.append("")
        stats.append((b, len(lo_), len(io_), len(set(lo_) ^ set(io_)), len(used)))

    for p in doc.paragraphs:
        for rr in p.runs: force_font(rr)
    for tb in doc.tables:
        for row in tb.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    for rr in p.runs: force_font(rr)
    doc.save(os.path.join(OUT, fname + ".docx"))
    with open(os.path.join(MD, fname + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    return stats

if __name__ == "__main__":
    for a in sys.argv[1:]:
        st = build(int(a))
        mism = sum(s[3] for s in st)
        print(a, "libri:", len(st), "par lat/ita:", sum(s[1] for s in st), "/", sum(s[2] for s in st),
              "non allineati:", mism, "note:", sum(s[4] for s in st), flush=True)

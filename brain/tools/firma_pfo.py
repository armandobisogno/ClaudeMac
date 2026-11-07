#!/usr/bin/env python3
"""
firma_pfo.py — firma dei PFO (progetti formativi di tirocinio) con la firma di Armando.

La firma (Università/Direzione/Firma.png) va SEMPRE sul rigo
«Firma e timbro del soggetto promotore ………… in data ……»: centrata sulla linea
punteggiata che segue la dicitura, appoggiata sulla linea. Una sola firma per PFO.

Sottocomandi:
  nuovi [--quiet]              PFO in Tirocini/ non ancora presenti in Tirocini/Firmati/
                               (estrae prima gli zip non ancora estratti)
  trova FILE --out DIR         cerca la dicitura nello strato di testo (OCR spesso sporco
                               o assente: serve solo a suggerire la pagina) e crea in DIR
                               il foglio-provini di tutte le pagine
  griglia FILE PAG [--zona Y0 Y1] --out DIR
                               rende la pagina PAG con griglia in punti PDF; con --zona
                               solo la fascia Y0–Y1, ingrandita e con griglia più fitta
  firma FILE PAG X Y [--larghezza 110] --out DIR
                               X = centro della linea punteggiata, Y = quota della linea
                               (coordinate VISIBILI, lette sulla griglia).
                               Salva Tirocini/Firmati/<nome>.pdf e un'anteprima in DIR.

PAG parte da 1. Le coordinate sono sempre quelle della pagina come la si vede
(rotazione già applicata): lo script converte da sé per le pagine ruotate.
Non si usano le coordinate dell'OCR per piazzare la firma: si leggono sulla griglia.
"""
import argparse, pathlib, re, sys, unicodedata, zipfile

import fitz  # PyMuPDF

ROOT = pathlib.Path(__file__).resolve().parents[2]
TIROCINI = ROOT / "Documenti di passaggio" / "Tirocini"
FIRMATI = TIROCINI / "Firmati"
FIRMA_PNG = ROOT / "Università" / "Direzione" / "Firma.png"

LARGHEZZA = 110      # punti PDF (~3,9 cm)
ALZO = 0.85          # quota dell'altezza della firma che sta sopra la linea

# «Firma e timbro del soggetto promotore», tollerante agli errori OCR (Fitma, timbr0…)
DICITURA = re.compile(r"f\w{2,4}a\W+e\W+timbr\w*\W+del\W+sogg\w*\W+promot\w*", re.I)


def norm(s):
    return unicodedata.normalize("NFC", s)


def estrai_zip():
    for z in TIROCINI.rglob("*.zip"):
        if FIRMATI in z.parents:
            continue
        dest = z.with_suffix("")
        if dest.exists():
            continue
        with zipfile.ZipFile(z) as zf:
            for m in zf.infolist():
                if m.filename.lower().endswith(".pdf") and ".." not in m.filename:
                    zf.extract(m, dest)


def da_firmare():
    firmati = {norm(p.name).lower() for p in FIRMATI.glob("*.pdf")}
    out = []
    for p in sorted(TIROCINI.rglob("*.pdf")):
        if FIRMATI in p.parents or "__MACOSX" in p.parts:
            continue
        if norm(p.name).lower() not in firmati:
            out.append(p)
    return out


def cmd_nuovi(a):
    try:
        estrai_zip()
        files = da_firmare()
    except Exception:  # noqa: BLE001
        return
    if not files:
        if not a.quiet:
            print("Nessun PFO da firmare.")
        return
    print(f"## Tirocini — {len(files)} PFO da firmare (usa /tirocini)\n")
    for p in files:
        print(f"- {p.relative_to(TIROCINI)}")
    print()


def cmd_trova(a):
    doc = fitz.open(a.file)
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    print(f"{pathlib.Path(a.file).name}: {doc.page_count} pagine")
    for page in doc:
        words = page.get_text("words")
        testo, pos = "", []
        for w in words:
            pos.append(len(testo)); testo += w[4] + " "
        for m in DICITURA.finditer(testo):
            w = words[max(i for i, s in enumerate(pos) if s < m.end())]
            print(f"  TESTO pag {page.number + 1}: «{m.group(0)}» (rigo a y≈{w[3]:.0f}, da verificare sulla griglia)")
    print(f"  provini → {provini(doc, out / 'provini.png')}")


def provini(doc, dest, dpi=42, col=5):
    """Tutte le pagine in un solo foglio, numerate: per individuare a colpo d'occhio la pagina."""
    from PIL import Image, ImageDraw
    ims = []
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    cw, ch = max(i.width for i in ims), max(i.height for i in ims)
    rows = (len(ims) + col - 1) // col
    sheet = Image.new("RGB", (cw * min(col, len(ims)), ch * rows), "white")
    d = ImageDraw.Draw(sheet)
    for n, im in enumerate(ims):
        x, y = (n % col) * cw, (n // col) * ch
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 26, y + 16], fill="red")
        d.text((x + 5, y + 3), str(n + 1), fill="white")
    sheet.save(dest)
    return dest


def cmd_griglia(a):
    doc = fitz.open(a.file)
    page = doc[a.pag - 1]
    W, H = page.rect.width, page.rect.height
    if a.zona:
        y0, y1 = a.zona
        passo, etich, dpi, clip = 10, 50, 160, fitz.Rect(0, y0, W, y1)
    else:
        y0, y1 = 0, H
        passo, etich, dpi, clip = 50, 100, 110, None
    sh = page.new_shape()
    for x in range(0, int(W) + 1, passo):
        sh.draw_line(fitz.Point(x, y0) * page.derotation_matrix, fitz.Point(x, y1) * page.derotation_matrix)
    for y in range(int(y0) // passo * passo, int(y1) + 1, passo):
        sh.draw_line(fitz.Point(0, y) * page.derotation_matrix, fitz.Point(W, y) * page.derotation_matrix)
    sh.finish(color=(1, 0, 0), width=0.3 if a.zona else 0.4)
    sh.commit()
    # etichette in coordinate non ruotate, testo ruotato come la pagina
    for x in range(0, int(W) + 1, etich):
        for y in range(int(y0) // passo * passo, int(y1) + 1, etich if not a.zona else passo * 2):
            p = fitz.Point(x + 1, y + 6) * page.derotation_matrix
            page.insert_text(p, f"{x},{y}", fontsize=4 if a.zona else 5, color=(1, 0, 0), rotate=page.rotation)
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    f = out / f"griglia_p{a.pag:02d}{'_zona' if a.zona else ''}.png"
    page.get_pixmap(dpi=dpi, clip=clip).save(f)
    print(f)


def firma_trasparente():
    """Firma.png ha il fondo bianco opaco: lo rende trasparente, così su scansioni e foto
    a fondo colorato non resta il riquadro bianco. L'inchiostro diventa nero pieno."""
    import io
    from PIL import Image
    im = Image.open(FIRMA_PNG).convert("L")
    alpha = im.point(lambda v: 0 if v > 225 else min(255, (225 - v) * 3))
    out = Image.new("RGBA", im.size, (20, 20, 20, 0))
    out.putalpha(alpha)
    buf = io.BytesIO(); out.save(buf, "PNG")
    return buf.getvalue(), im.size


def cmd_firma(a):
    src = pathlib.Path(a.file)
    doc = fitz.open(src)
    page = doc[a.pag - 1]
    w = a.larghezza
    png, (pw, ph) = firma_trasparente()
    h = w * ph / pw
    vis = fitz.Rect(a.x - w / 2, a.y - h * ALZO, a.x + w / 2, a.y + h * (1 - ALZO))
    rect = vis * page.derotation_matrix
    page.insert_image(rect, stream=png, rotate=page.rotation, keep_proportion=True)
    FIRMATI.mkdir(exist_ok=True)
    dest = FIRMATI / src.name
    doc.save(dest, garbage=3, deflate=True)
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    clip = fitz.Rect(vis.x0 - 220, vis.y0 - 50, vis.x1 + 140, vis.y1 + 50) & page.rect
    prev = out / f"anteprima_{src.stem}.png"
    fitz.open(dest)[a.pag - 1].get_pixmap(dpi=110, clip=clip).save(prev)
    print(f"firmato → {dest}\nanteprima → {prev}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("nuovi"); s.add_argument("--quiet", action="store_true"); s.set_defaults(f=cmd_nuovi)
    s = sub.add_parser("trova"); s.add_argument("file"); s.add_argument("--out", required=True); s.set_defaults(f=cmd_trova)
    s = sub.add_parser("griglia"); s.add_argument("file"); s.add_argument("pag", type=int)
    s.add_argument("--zona", type=float, nargs=2, metavar=("Y0", "Y1"))
    s.add_argument("--out", required=True); s.set_defaults(f=cmd_griglia)
    s = sub.add_parser("firma"); s.add_argument("file"); s.add_argument("pag", type=int)
    s.add_argument("x", type=float); s.add_argument("y", type=float)
    s.add_argument("--larghezza", type=float, default=LARGHEZZA)
    s.add_argument("--out", required=True); s.set_defaults(f=cmd_firma)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
    sys.exit(0)

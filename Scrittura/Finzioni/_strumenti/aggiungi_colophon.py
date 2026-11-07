#!/usr/bin/env python3
"""Mette la pagina di Finzioni (testo di presentazione, licenza CC BY-SA 4.0, nome e mail) subito dopo la copertina di un PDF.

Uso: python3 Finzioni/_strumenti/aggiungi_colophon.py file1.pdf [file2.pdf ...]
Se la pagina c'è già, viene sostituita (si può rilanciare dopo ogni build). Formato A4, A5 o libro 16×24 secondo il PDF.
"""
import subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FORMATI = {"A4": ("A4", "297mm", "34mm 30mm 30mm", "11.5pt"), "A5": ("A5", "210mm", "22mm 18mm 20mm", "9pt"),
           "L16": ("160mm 240mm", "240mm", "26mm 21mm 24mm", "9.5pt")}  # L16 = libro 16×24 cm
SWIFT = r'''
import PDFKit
let a = CommandLine.arguments            // target, colophonA4, colophonA5, colophonL16
let d = PDFDocument(url: URL(fileURLWithPath: a[1]))!
var i = 0
func isColophon(_ t: String) -> Bool {   // dopo un salvataggio PDFKit il testo della pagina può ridursi a una parola
  return t.contains("non-casa editrice") || t.contains("armandobisogno.it/finzioni") || (t.count < 200 && t.contains("divertissement"))
}
while i < d.pageCount { if isColophon(d.page(at: i)?.string ?? "") { d.removePage(at: i) } else { i += 1 } }
let ref = d.page(at: min(2, d.pageCount - 1))!.bounds(for: .mediaBox).width
let k = ref < 435 ? 3 : (ref < 520 ? 4 : 2)   // A5 = 420 pt, 16×24 = 454 pt, A4 = 595 pt
let c = PDFDocument(url: URL(fileURLWithPath: a[k]))!
d.insert(c.page(at: 0)!, at: 1)
d.write(to: URL(fileURLWithPath: a[1]))
print(["", "", "A4", "A5", "16×24"][k], d.pageCount, "pagine")
'''


def main(files):
    tmp = Path(tempfile.mkdtemp())
    src = (HERE / "colophon.html").read_text()
    pdfs = {}
    for k, (size, h, pad, fs) in FORMATI.items():
        html = tmp / f"colophon-{k}.html"
        html.write_text(src.replace("{{SIZE}}", size).replace("{{H}}", h).replace("{{PAD}}", pad).replace("{{FS}}", fs))
        pdfs[k] = tmp / f"colophon-{k}.pdf"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=6000",
                        f"--print-to-pdf={pdfs[k]}", html.as_uri()], check=True, capture_output=True)
    sw = tmp / "ins.swift"
    sw.write_text(SWIFT)
    for f in files:
        r = subprocess.run(["swift", str(sw), f, str(pdfs["A4"]), str(pdfs["A5"]), str(pdfs["L16"])], capture_output=True, text=True)
        print(Path(f).name, "→", r.stdout.strip() or r.stderr.strip()[-300:])


if __name__ == "__main__":
    main(sys.argv[1:] or sys.exit(__doc__))

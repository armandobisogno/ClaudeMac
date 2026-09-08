#!/usr/bin/env python3
"""
odg_extract.py — estrae lo scheletro di un dossier Consiglio/Giunta del DiSPaC.

Uso:
    python3 brain/tools/odg_extract.py [PDF]

Se PDF non e' indicato, prende il .pdf piu' recente in
"Direzione/Consigli e Giunte/" (esclusi i file *-sintesi-giunta.*).

Non interpreta nulla: estrae il testo pagina per pagina e segnala i marcatori
utili (Oggetto:, decreti d'urgenza da portare a ratifica, verbi deliberativi).
L'interpretazione (tipologia, importanza, sintesi) la fa il comando /giunta.

Produce due file affiancati (default in scratchpad):
  - odg_<stem>.json  — scheletro leggero: marcatori, elenco "Oggetto:",
                        decreti a ratifica, verbi deliberativi. Piccolo, si
                        legge tutto d'un fiato.
  - odg_<stem>.txt   — testo integrale del PDF, una pagina per blocco,
                        delimitata da "===== PAGINA n / N =====".

Struttura del JSON:
    {
      "source": "<path assoluto del PDF>",
      "stem": "090926",
      "n_pages": 92,
      "text_file": "<path del .txt>",
      "oggetti":   [{"page": 1, "text": "Comunicazioni del Direttore"}, ...],
      "ratifiche": [{"page": 3, "snippet": "..."}, ...],
      "delibere":  [{"page": 40, "snippet": "Delibera / Approva / Prende atto"}]
    }
"""
import sys, os, json, re, glob, argparse

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ODG_DIR = os.path.join(REPO, "Direzione", "Consigli e Giunte")

RE_OGGETTO = re.compile(r"^\s*Oggetto\s*:\s*(.+)$", re.I | re.M)
RE_RATIFICA = re.compile(r"portare a ratifica il presente provvedimento", re.I)
RE_DELIBERA = re.compile(
    r"^\s*(Delibera|Il Consiglio (?:di Dipartimento )?(?:approva|delibera)|"
    r"Approva all[’']unanimit[aà]|PRENDE ATTO|Il Consiglio approva)\b",
    re.I | re.M,
)


def pick_pdf(arg):
    if arg:
        p = os.path.abspath(arg)
        if not os.path.isfile(p):
            sys.exit(f"File non trovato: {p}")
        return p
    cand = [
        f for f in glob.glob(os.path.join(ODG_DIR, "*.pdf"))
        if "-sintesi-giunta" not in os.path.basename(f)
    ]
    if not cand:
        sys.exit(f"Nessun PDF in {ODG_DIR}")
    return max(cand, key=os.path.getmtime)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", nargs="?", help="percorso del PDF (default: piu' recente)")
    ap.add_argument("--out", help="percorso del JSON di output")
    args = ap.parse_args()

    try:
        import pypdf
    except ImportError:
        sys.exit("Manca pypdf: python3 -m pip install pypdf")

    src = pick_pdf(args.pdf)
    stem = os.path.splitext(os.path.basename(src))[0]
    reader = pypdf.PdfReader(src)

    n_pages = len(reader.pages)
    page_texts, oggetti, ratifiche, delibere = [], [], [], []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        page_texts.append(text)
        for m in RE_OGGETTO.finditer(text):
            oggetti.append({"page": i, "text": re.sub(r"\s+", " ", m.group(1)).strip()})
        if RE_RATIFICA.search(text):
            j = RE_RATIFICA.search(text).start()
            ratifiche.append({"page": i, "snippet": re.sub(r"\s+", " ", text[max(0, j - 240):j + 60]).strip()})
        m = RE_DELIBERA.search(text)
        if m:
            delibere.append({"page": i, "snippet": re.sub(r"\s+", " ", m.group(0)).strip()})

    out = args.out or os.path.join(
        os.environ.get("TMPDIR", "/tmp"), f"odg_{stem}.json"
    )
    txt_path = os.path.splitext(out)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as fh:
        for i, t in enumerate(page_texts, start=1):
            fh.write(f"\n===== PAGINA {i} / {n_pages} =====\n{t}\n")

    data = {
        "source": src, "stem": stem, "n_pages": n_pages,
        "text_file": txt_path, "oggetti": oggetti,
        "ratifiche": ratifiche, "delibere": delibere,
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)

    print(f"PDF:        {src}")
    print(f"Pagine:     {n_pages}")
    print(f"JSON:       {out}")
    print(f"Testo:      {txt_path}")
    print(f"\nOggetti all'OdG ({len(oggetti)}):")
    for o in oggetti:
        print(f"  p{o['page']:>3}  {o['text'][:150]}")
    print(f"\nDecreti d'urgenza da portare a ratifica: {len(ratifiche)} "
          f"(pagine: {', '.join(str(r['page']) for r in ratifiche) or '-'})")
    print(f"Blocchi con verbo deliberativo: {len(delibere)} "
          f"(pagine: {', '.join(str(d['page']) for d in delibere) or '-'})")


if __name__ == "__main__":
    main()

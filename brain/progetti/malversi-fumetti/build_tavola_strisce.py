#!/usr/bin/env python3
"""Monta una tavola verticale a strisce (stile Bonelli) da uno spec JSON.

uso: build_tavola_strisce.py catastrofi/ep00/tavola1.json  ->  tavola1.html + tavola1.png

Spec:
{
  "serie": "MALVERSI", "titolo": "Catastrofi", "episodio": "Il caffè puzza", "pagina": 1,
  "strisce": [
    [ {"img": "vignette/1-1.png", "w": 1,          # w = peso della larghezza nella striscia
       "pos": "50% 50%",                           # facoltativo: punto di ritaglio dell'immagine
       "testi": [ {"tipo": "didascalia"|"blues"|"balloon"|"sussurro", "testo": "...",
                   "x": 3, "y": 4, "w": 40,        # percentuali della vignetta
                   "coda": "bl"|"br"|"bc"|"tc"|"l"|"r"|null} ] } ]
  ]
}
"""
import html, json, os, subprocess, sys

CHROMES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

W, PAD, GAP = 1600, 44, 20
HEAD, SH, FOOT = 104, 610, 56          # testata, altezza striscia, piede
H = HEAD + 3 * SH + 2 * GAP + FOOT

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,700;1,700&family=Special+Elite&family=Oswald:wght@600&display=swap');
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: {W}px; height: {H}px; background: #fff; font-family: 'Comic Neue', sans-serif; }}
.head {{ height: {HEAD}px; padding: 26px {PAD}px 0; display: flex; align-items: baseline; gap: 20px; }}
.head .serie {{ font-family: 'Oswald', sans-serif; font-size: 50px; letter-spacing: 3px; }}
.head .tit {{ font-family: 'Special Elite', serif; font-size: 27px; }}
.head .num {{ margin-left: auto; font-family: 'Oswald', sans-serif; font-size: 24px; }}
.pag {{ padding: 0 {PAD}px; display: flex; flex-direction: column; gap: {GAP}px; }}
.s {{ display: flex; gap: {GAP}px; height: {SH}px; }}
.v {{ position: relative; height: 100%; border: 4px solid #000; overflow: hidden; min-width: 0; background: #fff; }}
.v img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.t {{ position: absolute; font-size: 23px; line-height: 1.16; color: #000; }}
.didascalia, .blues {{ background: #fff; border: 3px solid #000; padding: 9px 13px 7px; font-size: 21px;
    line-height: 1.22; font-family: 'Special Elite', serif; }}
.blues {{ background: #000; color: #fff; border-color: #000; font-style: italic; }}
.balloon, .sussurro {{ background: #fff; border: 3px solid #000; border-radius: 50% / 46%; padding: 24px 30px;
    text-align: center; text-transform: uppercase; }}
.sussurro {{ border-style: dashed; font-size: 20px; }}
.t::after, .t::before {{ content: ''; position: absolute; border-style: solid; display: none; }}
[class*="coda-"]::after, [class*="coda-"]::before {{ display: block; }}
.coda-bl::before {{ left: 24%; bottom: -42px; border-width: 42px 28px 0 0; border-color: #000 transparent transparent; }}
.coda-bl::after  {{ left: calc(24% + 3px); bottom: -34px; border-width: 38px 22px 0 0; border-color: #fff transparent transparent; }}
.coda-br::before {{ right: 24%; bottom: -42px; border-width: 42px 0 0 28px; border-color: #000 transparent transparent; }}
.coda-br::after  {{ right: calc(24% + 3px); bottom: -34px; border-width: 38px 0 0 22px; border-color: #fff transparent transparent; }}
.coda-bc::before {{ left: calc(50% - 14px); bottom: -42px; border-width: 42px 14px 0; border-color: #000 transparent transparent; }}
.coda-bc::after  {{ left: calc(50% - 10px); bottom: -34px; border-width: 38px 10px 0; border-color: #fff transparent transparent; }}
.coda-tc::before {{ left: calc(50% - 14px); top: -42px; border-width: 0 14px 42px; border-color: transparent transparent #000; }}
.coda-tc::after  {{ left: calc(50% - 10px); top: -34px; border-width: 0 10px 38px; border-color: transparent transparent #fff; }}
.coda-r::before {{ right: -44px; top: calc(50% - 13px); border-width: 13px 0 13px 44px; border-color: transparent transparent transparent #000; }}
.coda-r::after  {{ right: -36px; top: calc(50% - 9px); border-width: 9px 0 9px 39px; border-color: transparent transparent transparent #fff; }}
.coda-l::before {{ left: -44px; top: calc(50% - 13px); border-width: 13px 44px 13px 0; border-color: transparent #000 transparent transparent; }}
.coda-l::after  {{ left: -36px; top: calc(50% - 9px); border-width: 9px 39px 9px 0; border-color: transparent #fff transparent transparent; }}
.foot {{ height: {FOOT}px; padding: 16px {PAD}px 0; font-family: 'Special Elite', serif; font-size: 17px;
    display: flex; justify-content: space-between; }}
"""


def build(spec_path):
    spec_path = os.path.abspath(spec_path)
    base = os.path.dirname(spec_path)
    stem = os.path.splitext(os.path.basename(spec_path))[0]
    s = json.load(open(spec_path, encoding="utf-8"))
    rows = []
    for striscia in s["strisce"]:
        cells = []
        for v in striscia:
            pos = f' style="object-position:{v["pos"]}"' if v.get("pos") else ""
            parts = [f'<img src="{html.escape(v["img"])}"{pos}>']
            for t in v.get("testi", []):
                cls = f't {t["tipo"]}' + (f' coda-{t["coda"]}' if t.get("coda") else "")
                parts.append(
                    f'<div class="{cls}" style="left:{t["x"]}%;top:{t["y"]}%;width:{t["w"]}%">'
                    f'{html.escape(t["testo"]).replace(chr(10), "<br>")}</div>')
            cells.append(f'<div class="v" style="flex:{v.get("w", 1)} 1 0">' + "".join(parts) + "</div>")
        rows.append('<div class="s">' + "".join(cells) + "</div>")
    page = f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>{html.escape(s['serie'])} · {html.escape(s['titolo'])} · {s['pagina']}</title><style>{CSS}</style></head><body>
<div class="head"><span class="serie">{html.escape(s['serie'])}</span>
<span class="tit">{html.escape(s['titolo'])} · {html.escape(s['episodio'])}</span>
<span class="num">{s['pagina']}</span></div>
<div class="pag">{''.join(rows)}</div>
<div class="foot"><span>dal romanzo Terapie di Armando Bisogno (De Tomi Editore)</span>
<span>adattamento e disegni realizzati con Claude</span></div>
</body></html>"""
    out_html = os.path.join(base, stem + ".html")
    open(out_html, "w", encoding="utf-8").write(page)
    chrome = next((c for c in CHROMES if os.path.exists(c)), None)
    if not chrome:
        print("Nessun browser trovato: apri", out_html); return
    out_png = os.path.join(base, stem + ".png")
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={W},{H}", "--virtual-time-budget=5000",
                    f"--screenshot={out_png}", "file://" + out_html],
                   check=True, capture_output=True)
    print(out_png)


if __name__ == "__main__":
    build(sys.argv[1])

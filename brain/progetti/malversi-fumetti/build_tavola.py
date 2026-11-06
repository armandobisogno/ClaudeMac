#!/usr/bin/env python3
"""Monta una tavola di Malversi a fumetti (griglia 2x3) da uno spec JSON.

uso: build_tavola.py storie/001/tavola.json   ->  storie/001/tavola.html + tavola.png

Spec:
{
  "numero": "001", "titolo": "Il verbale intelligente",
  "vignette": [
    {"img": "vignette/v1.jpg",
     "testi": [
        {"tipo": "didascalia"|"balloon"|"schermo", "testo": "...",
         "x": 3, "y": 3, "w": 40,          # percentuali della vignetta
         "coda": "bl"|"br"|"bc"|"tc"|"l"|"r"|null}   # posizione della coda del balloon
     ]}
  ]
}
"""
import html, json, os, subprocess, sys

CHROMES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]

W, PAD, GAP = 1600, 40, 22            # larghezza pagina, margine, spazio tra vignette
PW = (W - 2 * PAD - GAP) // 2         # larghezza vignetta
PH = round(PW * 1088 / 1456)          # vignette 4:3 (1456x1088 da Canva)
HEAD = 120                            # testata
H = HEAD + 3 * PH + 2 * GAP + PAD + 50

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Special+Elite&family=Oswald:wght@600&display=swap');
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: {W}px; height: {H}px; background: #fff; font-family: 'Comic Neue', sans-serif; }}
.head {{ height: {HEAD}px; padding: 28px {PAD}px 0; display: flex; align-items: baseline; gap: 22px;
        border-bottom: 0; }}
.head .serie {{ font-family: 'Oswald', sans-serif; font-size: 58px; letter-spacing: 3px; }}
.head .tit {{ font-family: 'Special Elite', serif; font-size: 30px; }}
.head .num {{ margin-left: auto; font-family: 'Oswald', sans-serif; font-size: 26px; }}
.grid {{ padding: 0 {PAD}px; display: grid; grid-template-columns: {PW}px {PW}px; gap: {GAP}px; }}
.v {{ position: relative; width: {PW}px; height: {PH}px; border: 4px solid #000; overflow: hidden; }}
.v img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.t {{ position: absolute; font-size: 23px; line-height: 1.15; color: #000; text-transform: uppercase; }}
.balloon {{ background: #fff; border: 3px solid #000; border-radius: 50% / 45%; padding: 26px 34px;
            text-align: center; }}
.didascalia {{ background: #fdf6d8; border: 3px solid #000; padding: 8px 12px; font-size: 22px;
               text-transform: none; font-family: 'Special Elite', serif; }}
.schermo {{ background: #000; color: #fff; border: 2px solid #fff; padding: 10px 14px; font-size: 21px;
            text-transform: none; font-family: 'Special Elite', monospace; }}
.balloon::after, .balloon::before {{ content: ''; position: absolute; border-style: solid; }}
.coda-bl::before {{ left: 24%; bottom: -42px; border-width: 42px 28px 0 0; border-color: #000 transparent transparent; }}
.coda-bl::after  {{ left: calc(24% + 3px); bottom: -35px; border-width: 38px 22px 0 0; border-color: #fff transparent transparent; }}
.coda-br::before {{ right: 24%; bottom: -42px; border-width: 42px 0 0 28px; border-color: #000 transparent transparent; }}
.coda-br::after  {{ right: calc(24% + 3px); bottom: -35px; border-width: 38px 0 0 22px; border-color: #fff transparent transparent; }}
.coda-bc::before {{ left: calc(50% - 14px); bottom: -42px; border-width: 42px 14px 0; border-color: #000 transparent transparent; }}
.coda-bc::after  {{ left: calc(50% - 10px); bottom: -35px; border-width: 38px 10px 0; border-color: #fff transparent transparent; }}
.coda-tc::before {{ left: calc(50% - 14px); top: -42px; border-width: 0 14px 42px; border-color: transparent transparent #000; }}
.coda-tc::after  {{ left: calc(50% - 10px); top: -35px; border-width: 0 10px 38px; border-color: transparent transparent #fff; }}
.coda-r::before {{ right: -44px; top: calc(50% - 13px); border-width: 13px 0 13px 44px; border-color: transparent transparent transparent #000; }}
.coda-r::after  {{ right: -36px; top: calc(50% - 9px); border-width: 9px 0 9px 39px; border-color: transparent transparent transparent #fff; }}
.coda-l::before {{ left: -44px; top: calc(50% - 13px); border-width: 13px 44px 13px 0; border-color: transparent #000 transparent transparent; }}
.coda-l::after  {{ left: -36px; top: calc(50% - 9px); border-width: 9px 39px 9px 0; border-color: transparent #fff transparent transparent; }}
.foot {{ padding: 14px {PAD}px; font-family: 'Special Elite', serif; font-size: 18px; text-align: right; }}
"""


def build(spec_path):
    base = os.path.dirname(os.path.abspath(spec_path))
    s = json.load(open(spec_path, encoding="utf-8"))
    cells = []
    for v in s["vignette"]:
        parts = [f'<img src="{html.escape(v["img"])}">']
        for t in v.get("testi", []):
            cls = f't {t["tipo"]}' + (f' coda-{t["coda"]}' if t.get("coda") else "")
            parts.append(
                f'<div class="{cls}" style="left:{t["x"]}%;top:{t["y"]}%;width:{t["w"]}%">'
                f'{html.escape(t["testo"]).replace(chr(10), "<br>")}</div>')
        cells.append('<div class="v">' + "".join(parts) + "</div>")
    page = f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>Malversi {s['numero']}</title><style>{CSS}</style></head><body>
<div class="head"><span class="serie">MALVERSI</span><span class="tit">{html.escape(s['titolo'])}</span>
<span class="num">N. {s['numero']}</span></div>
<div class="grid">{''.join(cells)}</div>
<div class="foot">testi di Armando Bisogno · dai romanzi Terapie e Mosaici (De Tomi)</div>
</body></html>"""
    out_html = os.path.join(base, "tavola.html")
    open(out_html, "w", encoding="utf-8").write(page)
    chrome = next((c for c in CHROMES if os.path.exists(c)), None)
    if not chrome:
        print("Nessun Chrome: apri", out_html); return
    out_png = os.path.join(base, "tavola.png")
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={W},{H}", "--virtual-time-budget=4000",
                    f"--screenshot={out_png}", "file://" + out_html],
                   check=True, capture_output=True)
    print(out_png)


if __name__ == "__main__":
    build(sys.argv[1])

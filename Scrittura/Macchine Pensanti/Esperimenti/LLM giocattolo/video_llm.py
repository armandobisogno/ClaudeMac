#!/usr/bin/env python3
"""video_llm.py — video (1920x1080, ~70 s, muto) della simulazione «Un LLM giocattolo».

Stesso modello dell'artifact llm-giocattolo.html (stesso generatore casuale, seme 11):
le fasi 4-6 sono calcolate davvero; attenzione e dadi usano i numeri illustrativi dell'app.
Uso:  python3 video_llm.py   →  llm-giocattolo.mp4 nella stessa cartella
Dipendenze: Pillow, numpy (non serve), imageio-ffmpeg (o ffmpeg di sistema).
"""
import math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).with_name("llm-giocattolo.mp4")
W, H, K, FPS = 1920, 1080, 2, 30

# ---------------------------------------------------------------- colori e font
BG = (243, 245, 249); SURF = (255, 255, 255); INK = (21, 32, 58); MUTED = (90, 100, 121)
LINE = (216, 222, 232); SOFT = (233, 237, 244); OTHER = (142, 152, 172)
COL = {"gatto": (217, 72, 15), "cane": (11, 122, 117), "macchina": (95, 61, 196)}
AV = "/System/Library/Fonts/Avenir Next.ttc"; ME = "/System/Library/Fonts/Menlo.ttc"
_fc = {}
def F(kind, size):
    key = (kind, size)
    if key not in _fc:
        path, idx = {"bold": (AV, 0), "demi": (AV, 2), "med": (AV, 5), "reg": (AV, 7),
                     "mono": (ME, 0), "monob": (ME, 1)}[kind]
        _fc[key] = ImageFont.truetype(path, int(size * K), index=idx)
    return _fc[key]

def mix(c, a, base=BG):
    a = max(0.0, min(1.0, a))
    return tuple(int(base[i] + (c[i] - base[i]) * a) for i in range(3))

def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)
def seg(t, a, b): return max(0.0, min(1.0, (t - a) / (b - a)))

# ---------------------------------------------------------------- modello (identico all'app)
V = ["il", "gatto", "cane", "dorme", "sul", "divano", "tappeto", "mangia", "la", "pappa",
     "macchina", "corre", "sulla", "strada", "[fine]"]
IX = {w: i for i, w in enumerate(V)}
S = ["il gatto dorme sul divano", "il cane dorme sul tappeto", "il gatto mangia la pappa",
     "il cane mangia la pappa", "la macchina corre sulla strada"]
PAIRS, FOLLOW = [], [set() for _ in V]
for s in S:
    t = s.split() + ["[fine]"]
    for a, b in zip(t, t[1:]):
        PAIRS.append((IX[a], IX[b])); FOLLOW[IX[a]].add(IX[b])

def mulberry32(seed):
    st = [seed & 0xFFFFFFFF]
    M = 0xFFFFFFFF
    def imul(x, y): return (x * y) & M
    def r():
        st[0] = (st[0] + 0x6D2B79F5) & M
        a = st[0]
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & M) ^ t
        return ((t ^ (t >> 14)) & M) / 4294967296
    return r

def new_model(seed=11):
    r = mulberry32(seed)
    def gauss():
        u = 0
        while not u: u = r()
        v = r()
        return math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)
    E = [[r() * 2 - 1, r() * 2 - 1] for _ in V]
    E[IX["gatto"]] = [0.8, -0.3]; E[IX["cane"]] = [-0.6, 0.9]; E[IX["macchina"]] = [0.7, -0.2]
    Wm = [[gauss() * 0.5 for _ in V], [gauss() * 0.5 for _ in V]]
    return {"E": E, "W": Wm, "b": [0.0] * len(V)}

def probs(m, i):
    e = m["E"][i]
    z = [e[0] * m["W"][0][k] + e[1] * m["W"][1][k] + m["b"][k] for k in range(len(V))]
    mx = max(z); ex = [math.exp(v - mx) for v in z]; s = sum(ex)
    return [v / s for v in ex]

def epoch(m):
    n = len(V); gE = [[0, 0] for _ in V]; gW = [[0] * n, [0] * n]; gb = [0] * n; L = 0
    for a, t in PAIRS:
        p = probs(m, a); L -= math.log(p[t]); d = p[:]; d[t] -= 1; e = m["E"][a]
        for k in range(n):
            gW[0][k] += e[0] * d[k]; gW[1][k] += e[1] * d[k]; gb[k] += d[k]
            gE[a][0] += m["W"][0][k] * d[k]; gE[a][1] += m["W"][1][k] * d[k]
    N = len(PAIRS)
    for i in range(n):
        m["E"][i][0] -= 0.75 * gE[i][0] / N; m["E"][i][1] -= 0.75 * gE[i][1] / N
    for k in range(n):
        m["W"][0][k] -= 0.15 * gW[0][k] / N; m["W"][1][k] -= 0.15 * gW[1][k] / N; m["b"][k] -= 0.15 * gb[k] / N
    return L / N

def loss(m): return sum(-math.log(probs(m, a)[t]) for a, t in PAIRS) / len(PAIRS)

# istantanee di tutti i 600 giri
model = new_model(); SNAP = [([p[:] for p in model["E"]], loss(model), probs(model, IX["gatto"]))]
for _ in range(600):
    epoch(model)
    SNAP.append(([p[:] for p in model["E"]], loss(model), probs(model, IX["gatto"])))
TRAINED = model
P_SUL = probs(TRAINED, IX["sul"])

# ---------------------------------------------------------------- disegno
class Canvas:
    def __init__(self):
        self.im = Image.new("RGB", (W * K, H * K), BG); self.d = ImageDraw.Draw(self.im)
    def text(self, x, y, s, font, fill, anchor="la"):
        self.d.text((x * K, y * K), s, font=font, fill=fill, anchor=anchor)
    def tlen(self, s, font): return self.d.textlength(s, font=font) / K
    def line(self, pts, fill, w=2):
        self.d.line([(x * K, y * K) for x, y in pts], fill=fill, width=int(w * K), joint="curve")
    def dashed(self, a, b, fill, w=2, dash=10):
        L = math.hypot(b[0] - a[0], b[1] - a[1]);
        if L < 1: return
        n = int(L / dash)
        for i in range(0, n, 2):
            t0, t1 = i / n, min(1, (i + 1) / n)
            self.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                       (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill, w)
    def circle(self, x, y, r, fill):
        self.d.ellipse([(x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K], fill=fill)
    def rect(self, x0, y0, x1, y1, fill=None, outline=None, r=10, w=2):
        self.d.rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=r * K, fill=fill,
                                 outline=outline, width=int(w * K))
    def frame(self): return self.im.reduce(K)

def header(c, n, title, a=1):
    c.text(80, 64, f"PASSO {n}", F("demi", 22), mix(MUTED, a))
    c.text(80, 96, title, F("bold", 52), mix(INK, a))

def caption(c, main, sub=None, a=1):
    c.text(80, 950, main, F("demi", 38), mix(INK, a))
    if sub: c.text(80, 1002, sub, F("reg", 30), mix(MUTED, a))

def colored_sentence(c, x, y, s, font, a=1):
    for i, w in enumerate(s.split()):
        c.text(x, y, w, font, mix(COL.get(w, INK), a)); x += c.tlen(w + " ", font)

# ---- grafico dello spazio
class Plot:
    def __init__(self, box): self.box = box; self.view = None
    def draw(self, c, E, trails=None, smooth=False, a=1):
        x0b, y0b, x1b, y1b = self.box; w, h = x1b - x0b, y1b - y0b
        c.rect(x0b, y0b, x1b, y1b, fill=SURF, outline=LINE, r=16)
        pts = [E[i] for i in range(14)]
        xs = [p[0] for p in pts] + [0]; ys = [p[1] for p in pts] + [0]
        if trails:
            for tr in trails.values():
                xs += [p[0] for p in tr]; ys += [p[1] for p in tr]
        mnx, mxx, mny, mxy = min(xs), max(xs), min(ys), max(ys)
        px, py = (mxx - mnx) * .12 + .3, (mxy - mny) * .12 + .3
        mnx -= px; mxx += px + .5; mny -= py; mxy += py
        tgt = [(mnx + mxx) / 2, (mny + mxy) / 2, min(w / (mxx - mnx), h / (mxy - mny))]
        if self.view is None or not smooth: self.view = tgt
        else: self.view = [v + (t - v) * .08 for v, t in zip(self.view, tgt)]
        cx, cy, s = self.view
        X = lambda x: x0b + w / 2 + (x - cx) * s
        Y = lambda y: y0b + h / 2 - (y - cy) * s
        clip = lambda v, lo, hi: max(lo, min(hi, v))
        step = 1
        while step * s < 60: step *= 2
        gx = math.floor((cx - w / 2 / s) / step) * step
        while gx <= cx + w / 2 / s:
            X0 = X(gx)
            if x0b + 4 < X0 < x1b - 4: c.line([(X0, y0b + 2), (X0, y1b - 2)], mix(LINE, a), 1)
            gx += step
        gy = math.floor((cy - h / 2 / s) / step) * step
        while gy <= cy + h / 2 / s:
            Y0 = Y(gy)
            if y0b + 4 < Y0 < y1b - 4: c.line([(x0b + 2, Y0), (x1b - 2, Y0)], mix(LINE, a), 1)
            gy += step
        if x0b < X(0) < x1b: c.line([(X(0), y0b + 2), (X(0), y1b - 2)], mix(OTHER, a), 1.5)
        if y0b < Y(0) < y1b: c.line([(x0b + 2, Y(0)), (x1b - 2, Y(0))], mix(OTHER, a), 1.5)
        if trails:
            for k, tr in trails.items():
                if len(tr) > 1: c.line([(X(p[0]), Y(p[1])) for p in tr], mix(COL[k], .35 * a, SURF), 3)
        P = lambda k: (X(E[IX[k]][0]), Y(E[IX[k]][1]))
        for a_, b_ in (("gatto", "cane"), ("gatto", "macchina")):
            c.dashed(P(a_), P(b_), mix(MUTED, .7 * a, SURF), 2)
        items = [{"w": V[i], "x": X(E[i][0]), "y": Y(E[i][1]), "hl": V[i] in COL} for i in range(14)]
        for it in items:
            c.circle(it["x"], it["y"], 10 if it["hl"] else 6, mix(COL[it["w"]] if it["hl"] else OTHER, a, SURF))
        groups = []
        for it in sorted(items, key=lambda q: not q["hl"]):
            g = next((G for G in groups if math.hypot(G["x"] - it["x"], G["y"] - it["y"]) < 22), None)
            if g: g["l"].append(it)
            else: groups.append({"x": it["x"], "y": it["y"], "l": [it]})
        placed = [(it["x"] - 9, it["y"] - 9, it["x"] + 9, it["y"] + 9) for it in items]
        for G in groups:
            parts = []
            for j, it in enumerate(G["l"]):
                if j: parts.append((" · ", F("med", 22), MUTED))
                parts.append((it["w"], F("demi", 30) if it["hl"] else F("med", 22), COL[it["w"]] if it["hl"] else MUTED))
            tw = sum(c.tlen(p[0], p[1]) for p in parts); th = 30
            cands = [(G["x"] + 16, G["y"] - 18), (G["x"] + 16, G["y"] + 20), (G["x"] - 16 - tw, G["y"] - 18),
                     (G["x"] - 16 - tw, G["y"] + 20)]
            ok = lambda x, y: (x > x0b + 6 and x + tw < x1b - 6 and y > y0b + 18 and y < y1b - 18 and
                               all(x + tw < r[0] or x > r[2] or y + th / 2 < r[1] or y - th / 2 > r[3] for r in placed))
            x, y = next(((cx_, cy_) for cx_, cy_ in cands if ok(cx_, cy_)), cands[0])
            placed.append((x - 4, y - th / 2, x + tw + 4, y + th / 2))
            for s_, f, col in parts:
                c.text(x, y, s_, f, mix(col, a, SURF), "lm"); x += c.tlen(s_, f)
        return X, Y

def bars(c, x, y, rows, ok=(), a=1, wbar=360, rowh=52):
    for i, (w, p) in enumerate(rows):
        yy = y + i * rowh
        c.text(x + 150, yy + 14, w, F("mono", 26), mix(INK, a, SURF), "rm")
        c.rect(x + 170, yy, x + 170 + wbar, yy + 28, fill=mix(SOFT, a, SURF), r=5)
        if p > 0.004:
            c.rect(x + 170, yy, x + 170 + max(10, wbar * p), yy + 28, fill=mix(INK if w in ok else OTHER, a, SURF), r=5)
        c.text(x + 190 + wbar, yy + 14, f"{round(p * 100)}%", F("monob", 24), mix(INK, a, SURF), "lm")

def top(p, n): return sorted(zip(V, p), key=lambda q: -q[1])[:n]
def fmt(x, d=2): return f"{x:.{d}f}".replace(".", ",").replace("-", "−")
def dist(E, a, b): return math.hypot(E[IX[a]][0] - E[IX[b]][0], E[IX[a]][1] - E[IX[b]][1])

# ---------------------------------------------------------------- scene
T = [("titolo", 4), ("testi", 6), ("numeri", 5), ("posizioni", 6), ("addestra", 17), ("risultato", 5),
     ("attenzione", 8), ("dadi", 13), ("fine", 9)]
START = {}; acc = 0
for n, d in T: START[n] = acc; acc += d
TOTAL = acc
PLOT_A = Plot((80, 190, 1180, 900)); PLOT_B = Plot((80, 190, 1180, 900)); PLOT_C = Plot((80, 190, 1180, 900))
FADE = 0.5

def scene_alpha(t, d): return ease(seg(t, 0, FADE)) * (1 - ease(seg(t, d - FADE, d)))

def draw_titolo(c, t, d):
    a = scene_alpha(t, d)
    c.text(960, 430, "Un LLM giocattolo", F("bold", 110), mix(INK, a), "mm")
    c.text(960, 540, "come una macchina impara a prevedere le parole", F("reg", 40), mix(MUTED, a), "mm")
    c.text(960, 640, "gatto", F("monob", 44), mix(COL["gatto"], a), "mm")

def draw_testi(c, t, d):
    a = scene_alpha(t, d); header(c, 0, "I testi", a)
    for i, s in enumerate(S):
        ai = a * ease(seg(t, .3 + i * .5, .8 + i * .5))
        c.text(120, 250 + i * 110, str(i + 1), F("mono", 28), mix(MUTED, ai))
        colored_sentence(c, 180, 236 + i * 110, s, F("demi", 58), ai)
    caption(c, "Il modello legge soltanto queste cinque frasi.",
            "Gatto e cane non compaiono mai nella stessa frase.", a * ease(seg(t, 2.8, 3.4)))

def draw_numeri(c, t, d):
    a = scene_alpha(t, d); header(c, 1, "Il catalogo", a)
    for i, s in enumerate(S):
        k = ease(seg(t, 1 + i * .3, 1.6 + i * .3))
        y = 236 + i * 110
        c.text(120, y + 14, str(i + 1), F("mono", 28), mix(MUTED, a))
        if k < 1: colored_sentence(c, 180, y, s, F("demi", 58), a * (1 - k))
        if k > 0: c.text(180, y + 6, "  ·  ".join(str(IX[w] + 1) for w in s.split()), F("monob", 52), mix(INK, a * k))
    caption(c, "Ogni parola riceve un numero d'inventario.",
            "È una segnatura di biblioteca: non dice nulla del significato.", a * ease(seg(t, 2.6, 3.2)))

def side_panel(c, title, a):
    c.rect(1240, 190, 1840, 900, fill=mix(SURF, a), outline=mix(LINE, a), r=16)
    c.text(1280, 230, title, F("demi", 30), mix(INK, a, SURF))

def draw_posizioni(c, t, d):
    a = scene_alpha(t, d); header(c, 2, "Posizioni a caso", a)
    E0 = SNAP[0][0]; PLOT_A.draw(c, E0, a=a)
    side_panel(c, "Coordinate iniziali", a)
    for i, w in enumerate(("gatto", "cane", "macchina")):
        y = 300 + i * 70
        c.text(1280, y, w, F("demi", 34), mix(COL[w], a, SURF))
        c.text(1480, y + 4, f"({fmt(E0[IX[w]][0], 1)} ; {fmt(E0[IX[w]][1], 1)})", F("mono", 28), mix(INK, a, SURF))
    c.text(1280, 560, "distanza gatto–macchina", F("reg", 26), mix(MUTED, a, SURF))
    c.text(1280, 596, fmt(dist(E0, "gatto", "macchina")), F("monob", 44), mix(INK, a, SURF))
    c.text(1280, 680, "distanza gatto–cane", F("reg", 26), mix(MUTED, a, SURF))
    c.text(1280, 716, fmt(dist(E0, "gatto", "cane")), F("monob", 44), mix(INK, a, SURF))
    caption(c, "Ogni parola diventa un punto. All'inizio, a caso.",
            "Per puro caso gatto è vicino a macchina e lontano da cane.", a * ease(seg(t, 1, 1.6)))

def ep_at(t, d):
    u = seg(t, 1.0, d - 1.5)
    return int(round(600 * (u ** 1.6)))

def trails_upto(ep):
    tr = {k: [SNAP[e][0][IX[k]] for e in range(0, ep + 1, 3)] + [SNAP[ep][0][IX[k]]] for k in COL}
    return tr

def draw_addestra(c, t, d):
    a = scene_alpha(t, d); header(c, 3, "Addestramento", a)
    ep = ep_at(t, d); E, L, pg = SNAP[ep]
    PLOT_B.draw(c, E, trails=trails_upto(ep), smooth=True, a=a)
    side_panel(c, "Dopo «gatto» il modello prevede", a)
    bars(c, 1260, 290, top(pg, 5), ok=("dorme", "mangia"), a=a, wbar=300)
    c.text(1280, 590, "in scuro: le parole che seguono davvero", F("reg", 22), mix(MUTED, a, SURF))
    c.text(1280, 650, "giri", F("reg", 26), mix(MUTED, a, SURF))
    c.text(1280, 684, f"{ep} / 600", F("monob", 44), mix(INK, a, SURF))
    c.text(1560, 650, "errore medio", F("reg", 26), mix(MUTED, a, SURF))
    c.text(1560, 684, fmt(L), F("monob", 44), mix(INK, a, SURF))
    c.text(1280, 770, "gatto–cane", F("reg", 26), mix(MUTED, a, SURF))
    c.text(1280, 804, fmt(dist(E, "gatto", "cane")), F("monob", 40), mix(COL["cane"], a, SURF))
    c.text(1560, 770, "gatto–macchina", F("reg", 26), mix(MUTED, a, SURF))
    c.text(1560, 804, fmt(dist(E, "gatto", "macchina")), F("monob", 40), mix(COL["macchina"], a, SURF))
    caption(c, "Prevedere la parola dopo, sbagliare, correggere.",
            "A ogni errore la backpropagation sposta un poco le parole e i pesi.", a)

def draw_risultato(c, t, d):
    a = scene_alpha(t, d); header(c, 3, "Addestramento completato", a)
    E = SNAP[600][0]; PLOT_C.draw(c, E, trails=trails_upto(600), a=a)
    side_panel(c, "Dopo «gatto» il modello prevede", a)
    bars(c, 1260, 290, top(SNAP[600][2], 3), ok=("dorme", "mangia"), a=a, wbar=300)
    c.text(1280, 520, "Nel modello restano", F("demi", 30), mix(INK, a, SURF))
    c.text(1280, 566, "28 posizioni + 45 pesi = 73 numeri", F("mono", 24), mix(INK, a, SURF))
    c.text(1280, 610, "Frasi conservate: 0", F("monob", 30), mix(COL["gatto"], a, SURF))
    caption(c, "Gatto e cane finiscono nello stesso punto.",
            "Non stanno mai insieme: sono seguiti dalle stesse parole.", a)

def draw_attenzione(c, t, d):
    a = scene_alpha(t, d); header(c, 4, "Attenzione", a)
    words = ["il", "gatto", "dorme", "sul", "___"]; xs = [260, 520, 780, 1040, 1300]; y = 600
    wts = [0.05, 0.70, 0.20]
    g = ease(seg(t, 1.6, 3.4))
    for i in range(3):
        if g <= 0: break
        x0, x1 = xs[3], xs[i]; hgt = 90 + (3 - i) * 70
        pts = []
        for k in range(41):
            u = k / 40 * g
            bx = (1 - u) ** 3 * x0 + 3 * (1 - u) ** 2 * u * x0 + 3 * (1 - u) * u * u * x1 + u ** 3 * x1
            by = (1 - u) ** 3 * (y - 40) + 3 * (1 - u) ** 2 * u * (y - 40 - hgt) + 3 * (1 - u) * u * u * (y - 40 - hgt) + u ** 3 * (y - 40)
            pts.append((bx, by))
        col = COL["gatto"] if i == 1 else OTHER
        c.line(pts, mix(col, a), 2 + wts[i] * 26)
        if g > .95:
            c.text(x1 + 26, y - 82, f"{round(wts[i] * 100)}%", F("monob", 30), mix(col, a), "lm")
    for i, w in enumerate(words):
        fill = INK if i == 3 else None
        c.rect(xs[i] - 110, y - 40, xs[i] + 110, y + 40, fill=mix(fill, a) if fill else None,
               outline=mix(MUTED if i == 4 else INK, a), r=12, w=3)
        col = SURF if i == 3 else (COL["gatto"] if w == "gatto" else INK)
        c.text(xs[i], y, w, F("monob", 40), mix(col, a) if i != 3 else col, "mm")
    if t < 1.6:
        c.text(1500, 560, "solo «sul»:", F("reg", 28), mix(MUTED, a))
        c.text(1500, 600, f"divano {round(P_SUL[IX['divano']] * 100)}%  ·  tappeto {round(P_SUL[IX['tappeto']] * 100)}%", F("mono", 26), mix(INK, a))
    b = ease(seg(t, 3.8, 4.6))
    if b > 0:
        c.text(260, 720, "con l'attenzione (numeri illustrativi)", F("reg", 26), mix(MUTED, a * b))
        bars(c, 110, 770, [("divano", .85 * b), ("tappeto", .10 * b)], ok=("divano",), a=a * b, wbar=600)
    caption(c, "Il contesto: «sul» guarda indietro e trova il gatto.",
            "Nessuno ha scritto la regola: anche l'attenzione si regola sbagliando.", a)

# dadi: frase scritta con estrazioni fissate (stesse distribuzioni dell'app, temperatura 1)
GEN = [({"il": .8, "la": .2}, .30, "il"),
       ({"gatto": .45, "cane": .45, "macchina": .06, "divano": .02, "pappa": .02}, .62, "cane"),
       ({"dorme": .48, "mangia": .47, "corre": .05}, .21, "dorme"),
       ({"sul": .95, "sulla": .05}, .50, "sul"),
       ({"tappeto": .85, "divano": .10, "pappa": .03, "strada": .02}, .91, "divano"),
       ({"[fine]": .96, "il": .02, "la": .02}, .40, "[fine]")]
STACK_COLS = [INK, COL["cane"], COL["macchina"], COL["gatto"], MUTED]

def draw_dadi(c, t, d):
    a = scene_alpha(t, d); header(c, 5, "Scrittura", a)
    per = 1.7; i = min(len(GEN) - 1, int(max(0, t - .5) / per)); u = (max(0, t - .5) - i * per) / per
    if t - .5 > len(GEN) * per: i, u = len(GEN), 0
    written = [g[2] for g in GEN[:i]] + ([GEN[i][2]] if i < len(GEN) and u > .75 else [])
    x = 110
    for k, w in enumerate(written):
        col = COL["gatto"] if k == len(written) - 1 else INK
        c.text(x, 250, w, F("demi", 76), mix(col, a)); x += c.tlen(w + " ", F("demi", 76))
    if i < len(GEN):
        c.text(x, 250, "___", F("demi", 76), mix(MUTED, a))
        dist_, r, pick = GEN[i]
        rows = sorted(dist_.items(), key=lambda q: -q[1])
        x0, x1, yb = 110, 1810, 460
        c.text(x0, yb - 54, "probabilità della parola successiva", F("reg", 28), mix(MUTED, a))
        xx = x0; small = []
        for j, (w, p) in enumerate(rows):
            ww = (x1 - x0) * p; lab = f"{w} {round(p * 100)}%"
            c.rect(xx, yb, xx + ww, yb + 90, fill=mix(STACK_COLS[j % 5], a), r=4 if ww > 10 else 0)
            if c.tlen(lab, F("monob", 30)) < ww - 24:
                c.text(xx + ww / 2, yb + 45, lab, F("monob", 30), mix(SURF, a, STACK_COLS[j % 5]), "mm")
            else: small.append((w, p))
            xx += ww
        m = ease(seg(u, .1, .65)) * r
        mx = x0 + (x1 - x0) * m
        c.rect(mx - 3, yb - 18, mx + 3, yb + 108, fill=mix(INK, a), r=2)
        c.text(mx, yb + 150, f"dado: {round(m * 100)}", F("monob", 32), mix(INK, a), "mm")
        if small:
            c.text(x0, 680, "nei segmenti stretti: " +" · ".join(f"{w} {round(p * 100)}%" for w, p in small), F("mono", 26), mix(MUTED, a))
    else:
        c.text(110, 420, "Il dado è caduto sul 10% di «divano».", F("demi", 44), mix(INK, a))
        c.text(110, 490, "«il cane dorme sul divano» non compare nei testi: è una frase nuova.", F("reg", 36), mix(MUTED, a))
    caption(c, "Per scrivere, il modello tira i dadi: una parola alla volta.",
            "Se la frase nuova è plausibile la chiamiamo generalizzazione; se è falsa, allucinazione.", a)

def draw_fine(c, t, d):
    a = scene_alpha(t, d)
    a1 = a * ease(seg(t, .2, .8)); a2 = a * ease(seg(t, 2.2, 2.8)); a3 = a * ease(seg(t, 5, 5.6))
    c.text(960, 250, "Dentro il modello: pesi, non frasi.", F("bold", 68), mix(INK, a1), "mm")
    c.text(960, 340, "Il nostro giocattolo: 73 numeri. GPT-3: 175 miliardi.", F("reg", 40), mix(MUTED, a1), "mm")
    q1 = "«Sapere che “Burundi” è la parola probabile dopo"
    q2 = "“il paese a sud del Ruanda è” non equivale a sapere"
    q3 = "che il Burundi è a sud del Ruanda.»"
    for k, q in enumerate((q1, q2, q3)):
        c.text(960, 500 + k * 64, q, F("med", 44), mix(INK, a2), "mm")
    c.text(960, 720, "M. Shanahan, Talking About Large Language Models", F("reg", 30), mix(COL["gatto"], a2), "mm")
    c.text(960, 900, "Simulazione da T.B. Lee – S. Trott (2023) e M. Shanahan (2023)", F("reg", 28), mix(MUTED, a3), "mm")

DRAW = {"titolo": draw_titolo, "testi": draw_testi, "numeri": draw_numeri, "posizioni": draw_posizioni,
        "addestra": draw_addestra, "risultato": draw_risultato, "attenzione": draw_attenzione,
        "dadi": draw_dadi, "fine": draw_fine}

def ffmpeg_bin():
    exe = shutil.which("ffmpeg")
    if exe: return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def main(preview=None):
    if preview is not None:
        for name, sec in preview:
            c = Canvas(); DRAW[name](c, sec, dict(T)[name]); c.frame().save(OUT.with_name(f"_anteprima_{name}.png"))
        return
    cmd = [ffmpeg_bin(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
           "-preset", "medium", "-movflags", "+faststart", str(OUT)]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for f in range(n):
        t = f / FPS
        name = next(nm for nm, d in reversed(T) if t >= START[nm])
        c = Canvas(); DRAW[name](c, t - START[name], dict(T)[name])
        pr.stdin.write(c.frame().tobytes())
    pr.stdin.close(); pr.wait()
    print("scritto", OUT, f"({TOTAL} s)")

if __name__ == "__main__":
    import sys
    if "--anteprima" in sys.argv:
        main([("testi", 4), ("posizioni", 3), ("addestra", 12), ("risultato", 2.5), ("attenzione", 6), ("dadi", 8.2), ("fine", 6)])
    else:
        main()

"""Personaggi stilizzati nello stile del logo di Macchine Parlanti.
Si disegna a 4x (K) e si riduce, per avere linee morbide.
Ogni personaggio: testa tonda grande, corpo a bastoncino, pochi tratti distintivi."""
from PIL import Image, ImageDraw, ImageFont
import math

INK = (19, 38, 44); TEAL = (0, 151, 178); WARM = (242, 179, 94); PAPER = (251, 250, 247); TINT = (225, 242, 245)
K = 4
LW = 6

def _p(v): return v * K

class Pen:
    def __init__(self, img):
        self.d = ImageDraw.Draw(img)
    def line(self, pts, w=LW, fill=INK):
        self.d.line([(_p(x), _p(y)) for x, y in pts], fill=fill, width=int(_p(w)), joint='curve')
        for x, y in (pts[0], pts[-1]):  # estremi arrotondati
            r = w / 2
            self.d.ellipse((_p(x - r), _p(y - r), _p(x + r), _p(y + r)), fill=fill)
    def circle(self, cx, cy, r, w=LW, fill=None, outline=INK):
        self.d.ellipse((_p(cx - r), _p(cy - r), _p(cx + r), _p(cy + r)), outline=outline, width=int(_p(w)) if outline else 0, fill=fill)
    def dot(self, x, y, r=2.4, fill=INK):
        self.d.ellipse((_p(x - r), _p(y - r), _p(x + r), _p(y + r)), fill=fill)
    def arc(self, cx, cy, r, a0, a1, w=LW, fill=INK):
        self.d.arc((_p(cx - r), _p(cy - r), _p(cx + r), _p(cy + r)), a0, a1, fill=fill, width=int(_p(w)))
    def rrect(self, box, r, w=LW, fill=None, outline=INK):
        x0, y0, x1, y1 = box
        self.d.rounded_rectangle((_p(x0), _p(y0), _p(x1), _p(y1)), radius=_p(r), fill=fill, outline=outline, width=int(_p(w)) if outline else 0)
    def poly(self, pts, fill=INK):
        self.d.polygon([(_p(x), _p(y)) for x, y in pts], fill=fill)
    def text(self, xy, s, font, fill=INK, anchor='la'):
        self.d.text((_p(xy[0]), _p(xy[1])), s, font=font, fill=fill, anchor=anchor)

R = 42  # raggio della testa

# Tipi: armando, giulia (coda), marco (capelli a spazzola), sara (caschetto + occhiali tondi), paolo (calvo + baffi), elena (capelli lunghi), socrate
def head(p, x, y, kind, mouth='smile', look=0, blink=False):
    r = R
    if kind == 'elena':  # capelli lunghi dietro
        p.rrect((x - r - 8, y - 10, x + r + 8, y + r + 26), 18, fill=INK, outline=None)
    p.circle(x, y, r, fill=PAPER)
    ex = look * 5
    if kind == 'armando':
        for a in range(196, 345, 21):  # riccioli
            ax = x + math.cos(math.radians(a)) * (r + 2); ay = y + math.sin(math.radians(a)) * (r + 2)
            p.circle(ax, ay, 9, w=5, fill=PAPER)
        for a in range(35, 150, 16):   # barba a puntini sul mento
            p.dot(x + math.cos(math.radians(a)) * (r - 8), y + math.sin(math.radians(a)) * (r - 8), 2)
    elif kind == 'giulia':
        p.arc(x, y, r + 1, 185, 355, w=13); p.circle(x + r + 10, y - 18, 11, fill=INK, outline=None)
    elif kind == 'marco':
        for i in range(-3, 4): p.line([(x + i * 10, y - r + 3), (x + i * 10 + 4, y - r - 11)], w=5)
    elif kind == 'sara':
        p.d.chord((_p(x - r - 5), _p(y - r - 5), _p(x + r + 5), _p(y + r - 8)), 180, 360, fill=INK)
        p.line([(x - r - 2, y - 10), (x - r - 2, y + 14)], w=11); p.line([(x + r + 2, y - 10), (x + r + 2, y + 14)], w=11)
    elif kind == 'paolo':
        p.arc(x - r + 5, y - 2, 11, 100, 260, w=5); p.arc(x + r - 5, y - 2, 11, -80, 80, w=5)
    elif kind == 'elena':
        p.arc(x, y, r + 1, 190, 350, w=14)
    elif kind == 'socrate':
        p.arc(x - r + 6, y - 6, 12, 110, 250, w=5); p.arc(x + r - 6, y - 6, 12, -70, 70, w=5)
        p.d.pieslice((_p(x - r + 2), _p(y - 4), _p(x + r - 2), _p(y + r + 30)), 0, 180, fill=PAPER, outline=INK, width=_p(5))  # barba
        for i in range(-2, 3): p.line([(x + i * 9, y + 22), (x + i * 9, y + 46)], w=3)
    # occhi / occhiali
    if kind == 'armando':
        p.rrect((x - 30 + ex, y - 12, x - 6 + ex, y + 5), 3, w=5)
        p.rrect((x + 6 + ex, y - 12, x + 30 + ex, y + 5), 3, w=5)
        p.line([(x - 6 + ex, y - 5), (x + 6 + ex, y - 5)], w=4)
        if not blink: p.dot(x - 17 + ex, y - 3, 3.2); p.dot(x + 18 + ex, y - 3, 3.2)
    elif kind == 'sara':
        p.circle(x - 14 + ex, y - 2, 10, w=4); p.circle(x + 14 + ex, y - 2, 10, w=4)
        if not blink: p.dot(x - 14 + ex, y - 2, 2.8); p.dot(x + 14 + ex, y - 2, 2.8)
    else:
        if blink: p.line([(x - 18 + ex, y - 3), (x - 8 + ex, y - 3)], w=4); p.line([(x + 8 + ex, y - 3), (x + 18 + ex, y - 3)], w=4)
        else: p.dot(x - 13 + ex, y - 3, 4); p.dot(x + 13 + ex, y - 3, 4)
    if kind == 'paolo':
        p.arc(x, y + 22, 13, 205, 335, w=6)
    # bocca
    my = y + 18
    if kind == 'socrate': my = y + 12
    if mouth == 'smile': p.arc(x, my - 8, 13, 30, 150, w=4.5)
    elif mouth == 'open': p.circle(x, my + 2, 6, w=4, fill=INK)
    elif mouth == 'line': p.line([(x - 8, my + 1), (x + 8, my + 1)], w=4.5)
    elif mouth == 'o': p.circle(x, my + 2, 5, w=4)

def body_seated(p, x, y, arm='giu', arm2='giu', chair=True, skirt=False):
    """y = centro della testa. Figura seduta di tre quarti, rivolta a destra."""
    if chair:
        p.line([(x - 40, y + 140), (x + 46, y + 140)], w=5)
        p.line([(x - 36, y + 140), (x - 40, y + 220)], w=5); p.line([(x + 42, y + 140), (x + 46, y + 220)], w=5)
        p.line([(x - 40, y + 140), (x - 44, y + 60)], w=5)
    p.line([(x, y + R), (x, y + 132)])
    if skirt: p.poly([(x - 14, y + 108), (x + 14, y + 108), (x + 40, y + 150), (x - 4, y + 150)], fill=INK)
    p.line([(x, y + 132), (x + 50, y + 136), (x + 52, y + 208)]); p.line([(x + 52, y + 208), (x + 68, y + 208)])
    p.line([(x, y + 132), (x + 40, y + 142), (x + 42, y + 210)]); p.line([(x + 42, y + 210), (x + 58, y + 210)])
    arms = {'giu': [(x, y + 72), (x + 26, y + 108), (x + 48, y + 116)],
            'alzato': [(x, y + 72), (x + 30, y + 36), (x + 34, y - 4)],
            'scrive': [(x, y + 72), (x + 30, y + 100), (x + 58, y + 106)],
            'libro': [(x, y + 72), (x + 28, y + 96), (x + 50, y + 84)],
            'parla': [(x, y + 72), (x + 34, y + 80), (x + 60, y + 58)]}
    p.line(arms[arm]); p.line([(x, y + 72), (x - 20, y + 110), (x + 10, y + 120)] if arm2 == 'giu' else arms[arm2])

def body_standing(p, x, y, arm='indica', step=0):
    p.line([(x, y + R), (x, y + 170)])
    p.line([(x, y + 170), (x - 28 + step, y + 280)]); p.line([(x, y + 170), (x + 28 - step, y + 280)])
    p.line([(x - 28 + step, y + 280), (x - 46 + step, y + 280)]); p.line([(x + 28 - step, y + 280), (x + 46 - step, y + 280)])
    if arm == 'indica': p.line([(x, y + 76), (x + 50, y + 80), (x + 92, y + 48)]); p.line([(x, y + 76), (x - 34, y + 120), (x - 40, y + 148)])
    elif arm == 'aperte': p.line([(x, y + 76), (x + 44, y + 108), (x + 74, y + 92)]); p.line([(x, y + 76), (x - 44, y + 108), (x - 74, y + 92)])
    elif arm == 'saluta': p.line([(x, y + 76), (x + 40, y + 50), (x + 52, y + 6)]); p.line([(x, y + 76), (x - 34, y + 120), (x - 40, y + 148)])
    else: p.line([(x, y + 76), (x + 34, y + 120), (x + 40, y + 148)]); p.line([(x, y + 76), (x - 34, y + 120), (x - 40, y + 148)])

def phi(p, cx, cy, s=1.0):
    """Segno Φ di Phitness."""
    p.circle(cx, cy, 34 * s, w=10 * s, outline=TEAL)
    p.line([(cx, cy - 56 * s), (cx, cy + 56 * s)], w=9 * s)
    p.circle(cx, cy - 58 * s, 7 * s, fill=WARM, outline=None)

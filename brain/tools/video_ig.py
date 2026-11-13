#!/usr/bin/env python3
"""video_ig.py — dal video lungo di Armando, clip verticali per Instagram (Reel).

Fasi (le guida la skill /video-ig):

  1. trascrivi  VIDEO --out DIR
        audio → faster-whisper (italiano, timestamp per parola)
        → DIR/trascrizione.json, DIR/trascrizione.txt, DIR/info.json
  2. anteprima  VIDEO --t SEC [--x 0.5] [--zoom 1.0] --out FILE.jpg
        fotogramma col ritaglio 9:16 disegnato sopra, per controllare l'inquadratura
  3. sottotitoli PIANO.json
        per ogni clip: estremi agganciati ai confini di parola + bozza NN_slug.srt
        (con le correzioni globali del piano); i .srt vanno RILETTI e corretti a mano
  3b. correggi PIANO.json
        applica le correzioni «correzioni_srt» del piano ai .srt (parola per parola,
        anche a cavallo di due blocchi); per ritocchi puntuali si può editare il .srt
  4. render     PIANO.json [--solo N]
        ritaglio 9:16 1080x1920, sottotitoli incisi (titolo e firma in alto solo con "intestazione": true), audio a -14 LUFS
        → DIR/NN_slug.mp4

Dipendenze: ffmpeg (di sistema oppure `pip3 install --user imageio-ffmpeg`),
faster-whisper (`pip3 install --user faster-whisper`).
I percorsi relativi del piano si risolvono rispetto alla radice del repo.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
W, H = 1080, 1920


# ---------------------------------------------------------------- utilità
def ffmpeg_bin():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg non trovato: pip3 install --user imageio-ffmpeg")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg ha fallito:\n" + r.stderr[-3000:])
    return r


def percorso(p):
    p = Path(p).expanduser()
    return p if p.is_absolute() else REPO / p


def info_video(video):
    r = subprocess.run([ffmpeg_bin(), "-hide_banner", "-i", str(video)],
                       capture_output=True, text=True)
    m = re.search(r"Video: .*?(\d{3,5})x(\d{3,5})", r.stderr)
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    w, h = int(m.group(1)), int(m.group(2))
    rot = re.search(r"rotation of (-?[\d.]+)", r.stderr)
    if rot and abs(float(rot.group(1))) in (90, 270):
        w, h = h, w
    durata = int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3))
    return {"larghezza": w, "altezza": h, "durata": durata}


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


def ts_srt(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def ts_ass(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


def leggi_srt(path):
    blocchi = []
    for b in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()):
        righe = b.strip().splitlines()
        if len(righe) < 3:
            continue
        a, z = [x.strip() for x in righe[1].split("-->")]
        sec = lambda s: (lambda h, m, r: int(h) * 3600 + int(m) * 60 + float(r.replace(",", ".")))(*s.split(":"))
        blocchi.append((sec(a), sec(z), " ".join(righe[2:])))
    return blocchi


def ritaglio(src_w, src_h, x_centro, zoom):
    """Rettangolo 9:16 dentro il fotogramma sorgente: (w, h, x, y)."""
    ch = src_h / zoom
    cw = ch * 9 / 16
    if cw > src_w:
        cw, ch = src_w, src_w * 16 / 9
    cw, ch = int(cw) // 2 * 2, int(ch) // 2 * 2
    x = min(max(x_centro * src_w - cw / 2, 0), src_w - cw)
    y = (src_h - ch) / 2
    return cw, ch, int(x) // 2 * 2, int(y) // 2 * 2


def carica_piano(path):
    piano = json.loads(Path(path).read_text(encoding="utf-8"))
    piano["_video"] = percorso(piano["video"])
    piano["_out"] = percorso(piano["out"])
    piano["_out"].mkdir(parents=True, exist_ok=True)
    piano["_lav"] = percorso(piano.get("lavoro", piano["out"]))  # piano, trascrizione, .srt
    piano["_lav"].mkdir(parents=True, exist_ok=True)
    for i, c in enumerate(piano["clip"], 1):
        c["_nome"] = f"{i:02}_{slug(c['titolo'])}"
    return piano


# ---------------------------------------------------------------- 1. trascrivi
def cmd_trascrivi(a):
    video, out = percorso(a.video), percorso(a.out)
    out.mkdir(parents=True, exist_ok=True)
    info = info_video(video)
    (out / "info.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    wav = out / "_audio.wav"
    run([ffmpeg_bin(), "-y", "-loglevel", "error", "-i", str(video),
         "-vn", "-ac", "1", "-ar", "16000", str(wav)])
    from faster_whisper import WhisperModel
    m = WhisperModel(a.modello, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(str(wav), language="it", word_timestamps=True, vad_filter=True)
    dati, righe = [], []
    for s in segs:
        dati.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
                     "words": [[round(w.start, 2), round(w.end, 2), w.word] for w in s.words]})
        righe.append(f"[{s.start:6.1f}-{s.end:6.1f}] {s.text.strip()}")
        print(righe[-1], flush=True)
    (out / "trascrizione.json").write_text(json.dumps(dati, ensure_ascii=False), encoding="utf-8")
    (out / "trascrizione.txt").write_text("\n".join(righe) + "\n", encoding="utf-8")
    wav.unlink()
    print(f"\n{info}\n→ {out}/trascrizione.txt")


# ---------------------------------------------------------------- 2. anteprima
def cmd_anteprima(a):
    video = percorso(a.video)
    info = info_video(video)
    cw, ch, x, y = ritaglio(info["larghezza"], info["altezza"], a.x, a.zoom)
    vf = (f"drawbox=x={x}:y={y}:w={cw}:h={ch}:color=red@0.9:t=12,"
          f"scale=1280:-2")
    run([ffmpeg_bin(), "-y", "-loglevel", "error", "-ss", str(a.t), "-i", str(video),
         "-frames:v", "1", "-vf", vf, str(percorso(a.out))])
    print(f"ritaglio {cw}x{ch} a x={x}, y={y} → {a.out}")


# ---------------------------------------------------------------- 3. sottotitoli
def aggancia(trascr, c):
    """Estremi della clip sui confini di parola, con un piccolo respiro che non
    sconfina nella parola precedente o successiva. Restituisce (t0, t1, parole)."""
    ws = [w for s in trascr for w in s["words"]]
    idx = [i for i, w in enumerate(ws)
           if w[0] >= c["inizio"] - 0.3 and w[0] < c["fine"] - 0.2]
    i0, i1 = idx[0], idx[-1]
    t0 = ws[i0][0] - 0.25
    if i0 > 0:
        t0 = max(t0, ws[i0 - 1][1] + 0.05)
    t1 = ws[i1][1] + 0.6
    if i1 + 1 < len(ws):
        t1 = min(t1, ws[i1 + 1][0] - 0.05)
    unite = []  # «nell» + «'uso» → «nell'uso», così non finiscono in blocchi diversi
    for w in ws[i0:i1 + 1]:
        if unite and w[2].startswith("'"):
            unite[-1] = [unite[-1][0], w[1], unite[-1][2] + w[2]]
        else:
            unite.append(list(w))
    return max(t0, 0), t1, unite


def cmd_sottotitoli(a):
    piano = carica_piano(a.piano)
    tj = piano["_lav"] / "trascrizione.json"
    if not tj.exists():  # p. es. sottocartella «brevi/» accanto alla trascrizione
        tj = piano["_lav"].parent / "trascrizione.json"
    trascr = json.loads(tj.read_text(encoding="utf-8"))
    corr = piano.get("correzioni", {})
    maxc = piano.get("caratteri_per_blocco", 22)
    for c in piano["clip"]:
        t0, t1, ws = aggancia(trascr, c)
        c["taglio"] = [round(t0, 2), round(t1, 2)]
        blocchi, cur = [], []
        for w in ws:
            testo = "".join(x[2] for x in cur + [w]).strip()
            if cur and (len(testo) > maxc or w[0] - cur[-1][1] > 0.7):
                blocchi.append(cur)
                cur = []
            cur.append(w)
            if re.search(r"[.?!]$", w[2].strip()) and len(cur) > 2:
                blocchi.append(cur)
                cur = []
        if cur:
            blocchi.append(cur)
        out, tempi = [], []
        for i, b in enumerate(blocchi, 1):
            tempi.append([[round(x[0] - t0, 2), round(x[1] - t0, 2)] for x in b])
            testo = "".join(x[2] for x in b).strip()
            testo = re.sub(r"(\w) '(\w)", r"\1'\2", testo)  # «nell 'uso» → «nell'uso»
            for k, v in corr.items():  # chiavi = espressioni regolari
                testo = re.sub(k, v, testo)
            fine = b[-1][1] if i == len(blocchi) else min(blocchi[i][0][0], b[-1][1] + 0.4)
            out.append(f"{i}\n{ts_srt(max(b[0][0] - t0, 0))} --> {ts_srt(fine - t0)}\n{testo}\n")
        srt = piano["_lav"] / f"{c['_nome']}.srt"
        if srt.exists() and not a.sovrascrivi:
            print(f"  {srt.name} esiste già (corretto a mano?): non lo tocco. Usa --sovrascrivi.")
        else:
            srt.write_text("\n".join(out), encoding="utf-8")
            srt.with_suffix(".parole.json").write_text(json.dumps(tempi), encoding="utf-8")
        print(f"{c['_nome']}: {t0:.2f}–{t1:.2f} ({t1 - t0:.0f} s) → {srt.name}")
    piano_pulito = {k: v for k, v in piano.items() if not k.startswith("_")}
    for c in piano_pulito["clip"]:
        c.pop("_nome", None)
    Path(a.piano).write_text(json.dumps(piano_pulito, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Estremi agganciati (campo «taglio» del piano). Ora rileggi e correggi i .srt.")


# ---------------------------------------------------------------- 3b. correggi
def cmd_correggi(a):
    """Applica «correzioni_srt» del piano: {"01": [["da", "a"], ...], ...}.
    Le sostituzioni lavorano parola per parola, anche a cavallo di due blocchi,
    e lasciano intatti i tempi."""
    piano = carica_piano(a.piano)
    for i, c in enumerate(piano["clip"], 1):
        reps = piano.get("correzioni_srt", {}).get(f"{i:02}", [])
        srt = piano["_lav"] / f"{c['_nome']}.srt"
        if not reps or not srt.exists():
            continue
        blocchi = [b.splitlines() for b in re.split(r"\n\s*\n", srt.read_text(encoding="utf-8").strip())]
        toks = [(k, w) for k, b in enumerate(blocchi) for w in " ".join(b[2:]).split()]
        for da, a_ in reps:
            A, B = da.split(), a_.split()
            j, trovato = 0, False
            while j <= len(toks) - len(A):
                if [w for _, w in toks[j:j + len(A)]] == A:
                    idx = [k for k, _ in toks[j:j + len(A)]]
                    toks[j:j + len(A)] = [(idx[min(n, len(idx) - 1)], w) for n, w in enumerate(B)]
                    j += len(B)
                    trovato = True
                else:
                    j += 1
            if not trovato:
                print(f"  {c['_nome']}: «{da}» non trovato")
        out = [f"{b[0]}\n{b[1]}\n" + " ".join(w for k, w in toks if k == n) + "\n"
               for n, b in enumerate(blocchi)]
        srt.write_text("\n".join(out), encoding="utf-8")
        print(f"{srt.name}: {len(reps)} correzioni")


# ---------------------------------------------------------------- 4. render
STILE = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{font},{fs_sub},&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,1,0,0,0,100,100,1,0,1,6,2,2,70,70,{mv_sub},1
Style: Hook,{font},{fs_hook},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,1,0,1,7,3,8,70,70,{mv_hook},1
Style: Titolo,{font},66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H8C000000,1,0,0,0,100,100,0,0,3,22,0,8,90,90,240,1
Style: Firma,{font},38,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,2,1,8,90,90,128,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def colore_ass(hexrgb):
    """«#FF8A00» → «&H00008AFF&» (ASS vuole BGR)."""
    h = hexrgb.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}&".upper()


def eventi_karaoke(srt, maiuscolo, evidenzia):
    """Un evento per parola: tutto il blocco in bianco, la parola detta in colore.
    I tempi per parola vengono da .parole.json; se le correzioni hanno cambiato il
    numero di parole di un blocco, i tempi si ridistribuiscono in proporzione."""
    blocchi = leggi_srt(srt)
    pj = srt.with_suffix(".parole.json")
    tempi = json.loads(pj.read_text(encoding="utf-8")) if pj.exists() else []
    ev = []
    for n, (s0, s1, testo) in enumerate(blocchi):
        parole = testo.upper().split() if maiuscolo else testo.split()
        t = tempi[n] if n < len(tempi) and len(tempi[n]) == len(parole) else None
        if t is None:  # proporzionale alla lunghezza delle parole
            tot = sum(len(p) + 1 for p in parole)
            acc, t = s0, []
            for p in parole:
                d = (s1 - s0) * (len(p) + 1) / tot
                t.append([acc, acc + d])
                acc += d
        for k in range(len(parole)):
            a = max(t[k][0], s0) if k else s0
            z = t[k + 1][0] if k + 1 < len(parole) else s1
            if z <= a:
                continue
            riga = " ".join(
                (f"{{\\c{evidenzia}}}{p}{{\\c&H00FFFFFF&}}" if j == k else p)
                for j, p in enumerate(parole))
            ev.append(f"Dialogue: 1,{ts_ass(a)},{ts_ass(z)},Sub,,0,0,0,,{riga}")
    return ev


def cmd_render(a):
    piano = carica_piano(a.piano)
    video = piano["_video"]
    info = info_video(video)
    cw, ch, x, y = ritaglio(info["larghezza"], info["altezza"],
                            piano.get("x_centro", 0.5), piano.get("zoom", 1.0))
    font = piano.get("font", "Avenir Next Heavy")
    evid = colore_ass(piano.get("evidenzia", "#FF8A00"))
    maiusc = piano.get("maiuscolo", True)
    firma = piano.get("firma", "Armando Bisogno · Macchine Pensanti")
    for i, c in enumerate(piano["clip"], 1):
        if a.solo and i != a.solo:
            continue
        if "taglio" not in c:
            sys.exit("Manca il campo «taglio»: lancia prima la fase sottotitoli.")
        t0, t1 = c["taglio"]
        durata = t1 - t0
        if a.prova:
            durata = min(durata, a.prova)
        ass = piano["_lav"] / f"_{c['_nome']}.ass"
        ev = [STILE.format(font=font, fs_sub=piano.get("corpo_sottotitoli", 80), mv_sub=520,
                           fs_hook=piano.get("corpo_hook", 92), mv_hook=330)]
        fine = ts_ass(durata)
        if piano.get("intestazione", False):  # titolo + firma in alto: di norma no
            ev.append(f"Dialogue: 0,0:00:00.00,{fine},Titolo,,0,0,0,,{c['titolo']}")
            if firma:
                ev.append(f"Dialogue: 0,0:00:00.00,{fine},Firma,,0,0,0,,{firma}")
        srt = piano["_lav"] / f"{c['_nome']}.srt"
        if piano.get("sottotitoli", True) and srt.exists():
            ev += eventi_karaoke(srt, maiusc, evid)
        if c.get("hook"):  # domanda grande in alto nei primi secondi, poi svanisce
            h = c["hook"].upper() if maiusc else c["hook"]
            ev.append(f"Dialogue: 2,0:00:00.00,{ts_ass(c.get('durata_hook', 3.0))},Hook,,0,0,0,,"
                      f"{{\\fad(0,350)}}{h}")
        ass.write_text("\n".join(ev) + "\n", encoding="utf-8")
        ass_esc = str(ass).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
        vf = (f"crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos,setsar=1,"
              f"fade=t=in:st=0:d=0.3,fade=t=out:st={durata - 0.4:.2f}:d=0.4,"
              f"subtitles=filename='{ass_esc}':fontsdir=/System/Library/Fonts")
        af = (f"loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.2,"
              f"afade=t=out:st={durata - 0.4:.2f}:d=0.4")
        mp4 = piano["_out"] / f"{c['_nome']}{'_prova' if a.prova else ''}.mp4"
        print(f"render {mp4.name} ({durata:.0f} s)…", flush=True)
        run([ffmpeg_bin(), "-y", "-loglevel", "error", "-ss", f"{t0:.3f}", "-i", str(video),
             "-t", f"{durata:.3f}", "-vf", vf, "-af", af, "-r", "30",
             "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-profile:v", "high",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
             "-movflags", "+faststart", str(mp4)])
        ass.unlink()
        print(f"  → {mp4}")


# ---------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    t = sp.add_parser("trascrivi"); t.add_argument("video"); t.add_argument("--out", required=True)
    t.add_argument("--modello", default="small")
    t.set_defaults(f=cmd_trascrivi)
    v = sp.add_parser("anteprima"); v.add_argument("video"); v.add_argument("--t", type=float, default=60)
    v.add_argument("--x", type=float, default=0.5); v.add_argument("--zoom", type=float, default=1.0)
    v.add_argument("--out", required=True); v.set_defaults(f=cmd_anteprima)
    s = sp.add_parser("sottotitoli"); s.add_argument("piano")
    s.add_argument("--sovrascrivi", action="store_true"); s.set_defaults(f=cmd_sottotitoli)
    k = sp.add_parser("correggi"); k.add_argument("piano"); k.set_defaults(f=cmd_correggi)
    r = sp.add_parser("render"); r.add_argument("piano"); r.add_argument("--solo", type=int)
    r.add_argument("--prova", type=float, help="rende solo i primi N secondi (file _prova.mp4)")
    r.set_defaults(f=cmd_render)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

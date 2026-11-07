#!/usr/bin/env python3
"""Aggiornamenti di armandobisogno.it tramite il plugin «Armando Deploy».

Uso:
    python3 Web/Sito/deploy.py stato               # versione di WP/PHP, tema attivo, plugin
    python3 Web/Sito/deploy.py tema                # impacchetta Web/Sito/tema/armando-bisogno e lo carica (non lo attiva)
    python3 Web/Sito/deploy.py anteprima           # crea il link di anteprima privata del tema (3 giorni)
    python3 Web/Sito/deploy.py attiva              # attiva il tema armando-bisogno
    python3 Web/Sito/deploy.py plugin FILE.zip     # installa/aggiorna un plugin da zip
    python3 Web/Sito/deploy.py svuota              # svuota la cache di Aruba

Credenziali (password applicazione di un utente amministratore), da variabili d'ambiente:
    AB_WP_USER / AB_WP_APP_PASSWORD, AB_WP_URL (predefinito https://www.armandobisogno.it)
"""
import base64, json, os, sys, urllib.error, urllib.request, uuid, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = os.environ.get("AB_WP_URL", "https://www.armandobisogno.it").rstrip("/") + "/wp-json/ab-deploy/v1"


def auth():
    u, p = os.environ.get("AB_WP_USER"), os.environ.get("AB_WP_APP_PASSWORD")
    if not (u and p):
        sys.exit("Mancano AB_WP_USER / AB_WP_APP_PASSWORD")
    return "Basic " + base64.b64encode(f"{u}:{p}".encode()).decode()


def call(path, data=None, ctype=None, method=None):
    req = urllib.request.Request(BASE + path, data=data, method=method or ("POST" if data else "GET"))
    req.add_header("Authorization", auth())
    req.add_header("User-Agent", "ab-deploy/1.0")
    if ctype:
        req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:1500]}")


def upload(zip_path, kind):
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\n{kind}\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"package\"; filename=\"{zip_path.name}\"\r\n"
            f"Content-Type: application/zip\r\n\r\n").encode() + zip_path.read_bytes() + f"\r\n--{b}--\r\n".encode()
    return call("/package", body, f"multipart/form-data; boundary={b}")


def zip_theme():
    src = HERE / "tema" / "armando-bisogno"
    out = HERE / "tema" / "armando-bisogno.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            if f.is_file() and f.name not in (".DS_Store", "PRODUCT.md", "DESIGN.md", "DESIGN.json") and ".impeccable" not in f.relative_to(src).parts:
                z.write(f, Path("armando-bisogno") / f.relative_to(src))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stato"
    if cmd == "stato":
        print(json.dumps(call("/status"), indent=2, ensure_ascii=False))
    elif cmd == "tema":
        print(json.dumps(upload(zip_theme(), "theme"), indent=2, ensure_ascii=False))
        try:
            print("cache:", call("/purge", b"{}", "application/json"))
        except SystemExit as e:
            print("cache non svuotata:", e)
    elif cmd == "anteprima":
        print(call("/preview", json.dumps({"stylesheet": "armando-bisogno"}).encode(), "application/json"))
    elif cmd == "svuota":
        print(call("/purge", b"{}", "application/json"))
    elif cmd == "attiva":
        print(call("/activate-theme", json.dumps({"stylesheet": "armando-bisogno"}).encode(), "application/json"))
    elif cmd == "plugin" and len(sys.argv) > 2:
        print(json.dumps(upload(Path(sys.argv[2]), "plugin"), indent=2, ensure_ascii=False))
    else:
        sys.exit(__doc__)

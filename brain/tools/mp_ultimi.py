#!/usr/bin/env python3
"""
mp_ultimi.py — scarica il testo integrale degli ultimi N numeri di Macchine Pensanti
dal feed RSS di Substack e li scrive in un unico file di testo (per tarare il tono).

  python3 mp_ultimi.py [N] [file_output]

Default: N=10, output su stdout. Esclude le rassegne "Altre Macchine".
Solo stdlib.
"""
import sys, re, html, urllib.request
import xml.etree.ElementTree as ET

FEED = "https://armandobisogno.substack.com/feed"
NS = {"content": "http://purl.org/rss/1.0/modules/content/"}


def to_text(body):
    body = re.sub(r"(?is)<(script|style|figure|figcaption|button|svg)[^>]*>.*?</\1>", "", body)
    body = re.sub(r"(?i)<h[1-6][^>]*>", "\n\n## ", body)
    body = re.sub(r"(?i)</(p|h[1-6]|li|blockquote)>", "\n\n", body)
    body = re.sub(r"(?i)<br\s*/?>", "\n", body)
    body = re.sub(r"(?i)<li[^>]*>", "- ", body)
    body = re.sub(r"<[^>]+>", "", body)
    body = html.unescape(body)
    body = re.sub(r"[ \t]+", " ", body)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", body).strip()


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    out = sys.argv[2] if len(sys.argv) > 2 else None
    req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (mp_ultimi)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    parts = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        if title.lower().startswith("altre macchine"):
            continue
        sub = (item.findtext("description") or "").strip()
        date = (item.findtext("pubDate") or "").strip()
        body = item.findtext("content:encoded", default="", namespaces=NS)
        parts.append(f"=== {title} ===\n[{date}]\nSottotitolo: {sub}\n\n{to_text(body)}\n")
        if len(parts) >= n:
            break
    text = "\n\n".join(parts)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"{len(parts)} numeri scritti in {out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)


if __name__ == "__main__":
    main()

"""Corpus del progetto: otto dialoghi di Agostino, solo latino, dai file _md del workspace.
De libero arbitrio: solo libro I (riferimenti che iniziano con '1.')."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.normpath(os.path.join(HERE, "../../../Agostino strumenti/Agostino testi/Opere/_md"))
OPERE = [("1. Contra Academicos","Acad."),("2. De beata vita","beata v."),("3. De ordine","ord."),
         ("4. Soliloquia","sol."),("10. De quantitate animae","an. quant."),("11. De libero arbitrio","lib. arb."),
         ("12. De magistro","mag."),("15. De musica","mus.")]
def paragrafi():
    """Restituisce (sigla, riferimento, testo latino) per ogni paragrafo del corpus."""
    for f, s in OPERE:
        for line in open(os.path.join(MD, f + ".md"), encoding="utf-8"):
            m = re.match(r"\[([\d.]+)\] LA: (.*)", line.rstrip("\n"))
            if not m: continue
            ref, t = m.groups()
            if s == "lib. arb." and not ref.startswith("1."): continue
            yield s, ref, t
if __name__ == "__main__":
    from collections import Counter
    c = Counter(); w = Counter()
    for s, r, t in paragrafi(): c[s] += 1; w[s] += len(t.split())
    for f, s in OPERE: print(f"{s:12} paragrafi {c[s]:5}  parole {w[s]:7}")
    print("totale", sum(c.values()), sum(w.values()))

# Malversi a fumetti — procedura

Una tavola a settimana (6 vignette, stile Bonelli). Pubblicazione a cura di Armando.
Bibbia di personaggi/luoghi/prompt: [bibbia.md](bibbia.md).

## Pipeline (testata sulla n. 001, 30.09.2026)

1. **Storia** → `storie/NNN-slug.md`: idea, personaggi, 6 vignette con didascalie/battute e
   prompt visivo per vignetta (prompt base + descrizioni fisse dalla bibbia).
2. **Vignette** → Canva `generate-image`, `aspectRatio: LANDSCAPE_4_3`, sempre con
   `imageReferences: [MAHWstljyp4]` (model sheet Malversi v1) per la coerenza del volto.
   Il testo NON va generato nell'immagine.
3. **Alta risoluzione** → le anteprime di generate-image sono 199px e i link media sono
   firmati: si passa dal design di appoggio Canva **DAHWspKSzpI** ("Malversi 001 - vignette"):
   `read-design` con `open_transaction` → `add_page` 1456×1088 per vignetta → `insert_fill`
   dell'asset a 0,0,1456,1088 → `commit` → `export-design` PNG delle pagine → `curl` in
   `storie/NNN/vignette/v1..v6.png`. (Per le tavole successive: aggiungere pagine allo stesso
   design o crearne uno nuovo.)
4. **Montaggio** → `storie/NNN/tavola.json` (testi con posizione % e coda del balloon:
   bl/br/bc/tc/l/r) → `python3 build_tavola.py storie/NNN/tavola.json` → `tavola.html` +
   **`tavola.png`** (1600px, Chrome headless). Controllare il PNG: balloon che coprono volti,
   testo che tocca i bordi, code che puntano male; aggiustare x/y/w e rigenerare.

## Regole editoriali

- storie autoconclusive, battute ≤ ~20 parole, chiusa con battuta o verso blues
- varietà: alternare commissariato, casa/Laura, barbiere, cena del giovedì, radio, casi
- registro ironico camilleriano, mai farsa; ponte con Macchine Pensanti quando viene naturale

## Numerazione

| N. | Titolo | Stato |
|---|---|---|
| 001 | Il verbale intelligente | tavola pronta 30.09.2026 |

---
description: Firma i PFO (progetti formativi di tirocinio) nuovi in Documenti di passaggio/Tirocini/ con la firma di Armando, sempre nello stesso punto, e li salva in Tirocini/Firmati/
argument-hint: "[nome o percorso di un PFO opzionale; se vuoto firma tutti quelli non ancora firmati]"
---

Sei "tirocini" di Armando Bisogno, Direttore del DiSPaC (Università di Salerno).
Come Direttore firma i **PFO** (Progetti Formativi e di Orientamento) dei
tirocini curriculari, nella veste di **soggetto promotore**. Armando scarica i
PFO (spesso uno zip da Google Drive) in `Documenti di passaggio/Tirocini/`; tu
li firmi con la sua firma e li salvi in `Documenti di passaggio/Tirocini/Firmati/`.

Argomento di questo giro (se vuoto, ignora): **$ARGUMENTS**

## La regola (non cambia mai)

- La firma è l'immagine `Università/Direzione/Firma.png` (resa trasparente dallo script).
- Va **una sola volta per PFO**, sul rigo
  **«Firma e timbro del soggetto promotore ………… in data ……»**: di solito è la
  penultima pagina del modulo, nel blocco firme sotto «Autorizzazione al
  trattamento dei dati personali…» (pag. 4 della numerazione del modulo).
- **Centrata sulla linea punteggiata** che segue la dicitura, appoggiata sulla
  linea. Larghezza 110 pt (predefinita dello script, non cambiarla).
- **Mai** sui righi «tutore designato dal soggetto promotore», «soggetto
  ospitante», «tirocinante». La data («in data») non si scrive.
- L'originale non si tocca: l'output è `Firmati/<stesso nome>.pdf`.

## Strumento

`brain/tools/firma_pfo.py` (PyMuPDF + Pillow). Lancialo con `python3` dalla
cartella scratchpad (non da dentro Tirocini), passando percorsi assoluti; **non**
usare `python3 -I`, che disattiva le librerie installate per l'utente.
`--out` va sempre in una cartella dello scratchpad (anteprime e griglie).

## Procedura

1. `python3 brain/tools/firma_pfo.py nuovi` → estrae gli zip nuovi ed elenca i PFO
   che non hanno ancora una copia in `Firmati/` (confronto per nome file).
   Se `$ARGUMENTS` indica un file, lavora solo su quello.
2. Per ogni PFO: `trova FILE --out DIR` → crea `provini.png` (tutte le pagine
   numerate) e, se c'è strato di testo, indica la pagina con la dicitura.
   **Guarda i provini** e individua la pagina col blocco firme (le pagine possono
   essere scansioni, foto storte, ruotate: lo script gestisce la rotazione).
   Le coordinate dell'OCR **non** servono a piazzare la firma: sono inaffidabili.
3. `griglia FILE PAG --out DIR` → leggi sulla griglia (punti PDF, linee ogni 50)
   **inizio e fine della linea punteggiata** del rigo «soggetto promotore» e la sua
   quota y. X = centro dei puntini. Se serve precisione: `--zona Y0 Y1` (fascia
   ingrandita, linee ogni 10).
4. `firma FILE PAG X Y --out DIR` → salva in `Firmati/` e produce l'anteprima.
5. **Controlla ogni anteprima** (conviene comporle in un unico foglio con Pillow):
   firma dritta, sul rigo giusto, sopra i puntini, senza riquadro bianco. Se è
   fuori posto, correggi X/Y e rilancia `firma` (sovrascrive).
6. Chiudi con una tabella: PFO · pagina · esito, ed eventuali anomalie (rigo
   assente, modulo diverso, firma del promotore già presente…). Se un PFO ha già
   la firma di Armando sul rigo, non firmarlo di nuovo: segnalalo.

## Note

- `Documenti di passaggio/Tirocini/` è in `.gitignore` (dati degli studenti):
  niente va su GitHub.
- L'hook di inizio sessione (`session_brief.py`) segnala i PFO da firmare.

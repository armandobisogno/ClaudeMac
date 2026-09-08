---
description: Dal PDF del dossier Consiglio produce la sintesi schematica per la Giunta (.md + PDF stampabile), con tutti i punti raggruppati per tipologia e importanza
argument-hint: "[percorso PDF opzionale; se vuoto prende il più recente in Direzione/Consigli e Giunte/]"
---

Sei "giunta" di Armando Bisogno, Direttore del Dipartimento di Scienze del
Patrimonio Culturale (DiSPaC) dell'Università di Salerno. Armando dirige il
Consiglio di Dipartimento e, **due giorni prima**, la Giunta che lo istruisce.
Per ogni seduta l'ufficio prepara **un unico PDF** con tutte le delibere da
prendere; lui lo scorre in Giunta punto per punto e segna con una freccia quelli
che vanno effettivamente **deliberati** (gli altri sono comunicazioni o prese
d'atto).

Il tuo compito: dal PDF produrre una **sintesi schematica e ordinata da
presentare in Giunta**. Giri in locale, hai accesso a filesystem e shell.

Argomento di questo giro (percorso del PDF; se vuoto, ignora): **$ARGUMENTS**

## Cosa produci

Tre file, **accanto al PDF**, con lo stesso nome-base del PDF:
- `<stem>-sintesi-giunta.md` — la sintesi (artefatto principale)
- `<stem>-sintesi-giunta.html` — sorgente impaginata, ritoccabile a mano
- `<stem>-sintesi-giunta.pdf` — la stessa sintesi, impaginata per la seduta

Es. da `Direzione/Consigli e Giunte/090926.pdf` →
`Direzione/Consigli e Giunte/090926-sintesi-giunta.{md,html,pdf}`.
La cartella `Direzione/` è in `.gitignore`: gli output restano solo in locale.

## Regole d'oro

1. **Nessun punto va perso.** Ogni punto all'ordine del giorno del PDF deve
   comparire nella sintesi. Meglio un punto in più con nota "voce minore" che uno
   in meno. Alla fine fai un **controllo di integrità** esplicito.
2. **Schema essenziale, non parafrasi.** Per ogni punto poche righe: cosa è,
   se si vota, i numeri che contano. Niente "visto/considerato/udito".
3. **Distinzione netta delibera / non-delibera.** In Giunta serve sapere a colpo
   d'occhio dove va messa la freccia.
4. **Raggruppa per tipologia e, dentro ogni gruppo, per importanza** (prima i
   punti pesanti, poi l'ordinaria amministrazione). Ma prima dei gruppi metti
   sempre il **quadro sinottico** con *tutti* i punti in ordine di OdG.
5. **Non inventare.** Importi, nomi, SSD, codici concorso, date: solo se sono nel
   testo. Se un dato è illeggibile o assente, scrivi "(non indicato)".

## Passi

### 1. Estrai lo scheletro
Esegui:
```
python3 brain/tools/odg_extract.py $ARGUMENTS
```
(senza argomento prende il `.pdf` più recente in `Direzione/Consigli e Giunte/`,
esclusi i file `*-sintesi-giunta.*`). Annota dall'output: percorso del PDF,
`stem`, numero pagine, elenco **Oggetti** (con pagina), numero e pagine dei
**decreti d'urgenza da portare a ratifica**, pagine con **verbo deliberativo**.
Lo script scrive `odg_<stem>.json` (scheletro) e `odg_<stem>.txt` (testo
integrale, delimitato da `===== PAGINA n / N =====`).

### 2. Leggi il contenuto
Leggi tutto `odg_<stem>.json`, poi tutto `odg_<stem>.txt` (in più passaggi con
offset se supera il limite di righe). Ricostruisci i **punti dell'OdG**:

- Ogni riga `Oggetto:` apre di norma un punto. Punti su più pagine (es. quattro
  "Protocollo d'intesa" consecutivi) restano **punti distinti**: uno per Oggetto.
- Il **blocco di decreti d'urgenza** (pagine senza `Oggetto:`, ciascuno con
  "…di portare a ratifica il presente provvedimento adottato d'urgenza…") è **un
  solo punto**: «Ratifica dei decreti del Direttore adottati d'urgenza», con
  **sotto-elenco** di tutti i decreti (oggetto sintetico + eventuale importo/beneficiario).
- «Comunicazioni del Direttore» è **un punto** di tipo Comunicazione, con i vari
  capoversi come sotto-punti brevi.
- Per ogni punto individua il **verbo finale**: *Delibera / Approva / Il Consiglio
  approva* → si vota; *Prende atto / Presa d'atto* → non si vota; *Ratifica* → si
  vota (ratifica).

### 3. Classifica ogni punto

**Tipo** (una parola, in etichetta): `DELIBERA` · `RATIFICA` · `COMUNICAZIONE` ·
`PRESA D'ATTO`.

**Tipologia** (per il raggruppamento — adatta ai punti realmente presenti):
- Comunicazioni
- Ratifica decreti del Direttore
- Bilancio
- Personale docente e reclutamento (chiamate, commissioni, convenzioni ex art. 6)
- Didattica (programmazione, contratti di insegnamento, Scuole di specializzazione)
- Ricerca e incarichi (affidamenti, borse, contratti di consulenza/ricerca)
- Convenzioni, protocolli e contratti
- Patrocini e contributi
- Regolamenti
- Relazioni e prese d'atto

**Importanza**: `alta` (reclutamento e chiamate docenti; convenzioni/protocolli/
contratti che impegnano il Dipartimento; regolamenti; programmazione didattica;
variazioni di bilancio rilevanti) · `ordinaria` (patrocini, piccoli contributi,
nomine di commissioni per borse/incarichi, rinnovi di routine, prese d'atto).
In dubbio: `alta`.

### 4. Scrivi `<stem>-sintesi-giunta.md`

Struttura esatta:

```
# Giunta — dossier del Consiglio di Dipartimento del <data del Consiglio>

**Fonte:** `<nome PDF>` · <N> pagine · <N_punti> punti all'OdG
**Sintesi generata il:** <AAAA-MM-GG>
**Da deliberare:** <n> punti (voci ▶) · **Solo comunicazione/presa d'atto:** <n>

---

## Quadro sinottico

| # | Tipo | Punto | Pag. | Imp. |
|---|------|-------|------|------|
| 1 | COMUNICAZIONE | Comunicazioni del Direttore | 1 | – |
| 2 | RATIFICA | Ratifica decreti del Direttore d'urgenza (15) | 2–38 | alta |
| 3 | DELIBERA | Variazioni al bilancio – settembre 2026 | 39 | alta |
| … | | | | |

---

## ▶ Da deliberare

### <Tipologia> — importanza alta

#### N · <titolo breve>  · pag. <x>
- **In sintesi:** <1–2 righe>
- **Si vota:** <frase secca: cosa deve deliberare il Consiglio>
- **Numeri/nomi/date:** <importi, persone, SSD, codici concorso, scadenze — solo se presenti>
- **Attenzione:** <nodo politico o procedurale da tenere presente in Giunta — solo se c'è>

#### N · <titolo breve> · pag. <x>
…

### <Tipologia> — ordinaria amministrazione
…

---

## Comunicazioni e prese d'atto

#### N · <titolo breve> · pag. <x>
- **In sintesi:** <1–2 righe>
- **Numeri/nomi/date:** <se presenti>

---

## Controllo integrità
- Oggetti `Oggetto:` rilevati dallo script: **<n>** → tutti mappati su un punto della sintesi: sì / no (dettaglio)
- Decreti d'urgenza a ratifica: **<n>** → elencati nel punto «Ratifica»: <n>/<n>
- Punti totali in sintesi: **<n>**  ·  di cui da votare: **<n>**
- ⚠ Discrepanze / punti dubbi: <elenco, oppure "nessuna">
```

Regole di compilazione:
- La **numerazione N è quella dell'OdG** (ordine del PDF) e resta la stessa nel
  quadro sinottico, nelle sezioni tematiche e nel controllo integrità.
- Nel quadro sinottico ci sono **tutti** i punti, in ordine di OdG.
- "Si vota:" **solo** per i punti `DELIBERA` / `RATIFICA`. Per la ratifica in
  blocco: "Ratificare i 15 decreti elencati (in blocco o singolarmente)".
- "Attenzione:" solo se c'è davvero qualcosa (spesa a carico del Dipartimento,
  nomine che toccano equilibri, punti che tornano dopo un rinvio, scadenze
  strette, delibera "seduta stante / immediatamente esecutiva"). Non riempirlo
  per forza.
- Il punto «Ratifica decreti» porta un sotto-elenco puntato: `- <oggetto sintetico>
  — <beneficiario/importo se indicato> (p. <x>)`.
- Tieni ogni punto **compatto**: di norma 3–5 righe. Il dettaglio è nel PDF.

### 5. Genera il PDF stampabile
Scrivi un HTML autonomo `<stem>-sintesi-giunta.html` **accanto al PDF** con lo
stesso contenuto della sintesi: A4, margini ~18mm, carattere di sistema ~11pt,
tabella del quadro sinottico con bordi leggeri, titoli di sezione distinguibili,
`▶` ben visibile, blocchi `page-break-inside: avoid` sui singoli punti. Niente
CSS o font esterni. È la sorgente editabile del PDF (per ritoccare a mano). Poi:
```
brain/tools/html_to_pdf.sh <stem>-sintesi-giunta.html "Direzione/Consigli e Giunte/<stem>-sintesi-giunta.pdf"
```
Se lo script esce con codice 3 (nessun browser), segnalalo: il .md resta
comunque il documento buono.

### 6. Riepilogo a schermo
Elenca: PDF di partenza, i due file prodotti (percorsi), numero di punti totali,
quanti da votare e quanti no, e — se presenti — i punti che hai marcato dubbi nel
controllo integrità.

## Vincoli
- Scrivi **solo** i file `<stem>-sintesi-giunta.{md,pdf,html}`. Non toccare il PDF
  di partenza né altri file della cartella.
- Niente rete, niente Notion, niente git/commit/push: la cartella `Direzione/` è
  locale e riservata (contiene nomi e questioni di personale).
- Non chiedere conferme: procedi con le scelte migliori e segnala i dubbi nel
  controllo integrità e nel riepilogo.

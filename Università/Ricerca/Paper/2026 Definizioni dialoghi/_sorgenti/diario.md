# Diario di metodo — Le definizioni nei dialoghi di Agostino

Registro cronologico delle scelte e dei risultati, base per il paper illustrativo finale.
Vincolo di sessione (14.11.2026): l'analisi usa solo i testi di Agostino presenti nel workspace; niente memoria esterna del modello né letteratura secondaria.

## 14.11.2026 — Percorso delle scelte

1. Punto di partenza: Schwitzgebel, Schwitzgebel, Strasser, «Creating a large language model of a philosopher», *Mind & Language* 39 (2024), 237-259 (PDF in `Università/Ricerca/AI Augustinus/`). Logica: modello addestrato su un autore + test di discriminazione con esperti.
2. Primo spostamento: la condizione dello storico della filosofia è diversa (autore morto, interesse per l'autore e non per la macchina). Domanda: in che cosa un LLM aiuta lo studio di Agostino? Scelta: solo la ricerca per concetto, non la simulazione.
3. Secondo spostamento: la domanda teorica. La ricerca, garantito il lato documentale, scopre o produce i significati? Obiezione di Armando: anche la scelta delle parole latine «pertinenti» (voluntas sì, domus no) è già una precomprensione. Il circolo non si elimina; si riduce e si dichiara.
4. Terzo spostamento (proposta di Armando): corpus = soli dialoghi; presupposto: l'*intentio auctoris* in purezza non è coglibile, si lavora sull'*intentio operis*. Passo 1a: dove l'opera fornisce definizioni esplicite, e di che cosa.
5. Criterio: non si applica ai testi la teoria agostiniana della definizione (averla formulata non implica usarla). Si costruisce un codebook di elementi-spia, nostro e dichiarato. Codebook: Claude Doc https://claude.ai/artifact/DyonmrY9zKyJySW7g4V8V1 (bozza 2).
6. Decisioni sui punti aperti: A3 e B5 restano ma si verificano sul corpus; tipi su due livelli (nominale/reale, poi il modo); soglia B1 + B2/B3/B4 = grado 2; campione per la codifica alla cieca = *De magistro*.

## Corpus (script `corpus.py`)

Otto dialoghi, solo latino, *De libero arbitrio* solo libro I: 659 paragrafi, 150.182 parole.

| Sigla | Paragrafi | Parole |
|---|---|---|
| Acad. | 100 | 21.013 |
| beata v. | 36 | 7.219 |
| ord. | 89 | 17.586 |
| sol. | 66 | 16.314 |
| an. quant. | 85 | 19.650 |
| lib. arb. I | 36 | 8.101 |
| mag. | 47 | 12.090 |
| mus. | 200 | 48.209 |

Nota: la ricognizione esplorativa su *defin-* (152 occorrenze) era stata fatta prima della restrizione al libro I del *De libero arbitrio*; non è un risultato, va rifatta con il codebook approvato.

## 14.11.2026 — Verifica di A3 (*describo*, *descriptio*) — script `verifica_A3_B5.py`

16 frasi. Tre usi distinti:
- **valore definitorio** (8): Acad. 1.4.12, 1.5.14, 1.8.23; an. quant. 8.13, 12.21, 16.27; lib. arb. 1.13.27; mus. 1.3.4. In Acad. 1.4.12 il testo stesso affianca *mea descriptio* a *tua definitio* e *ego definivi*; in an. quant. 12.21 *nomen descriptionemque*; in mus. 1.3.4 *scientia describatur* riferito alla definizione della musica.
- **ritratto di un tipo umano** (5): Acad. 2.5.12, 2.7.19, 2.8.20, 3.4.10, 3.7.16. Solo 3.7.16 è unito a una domanda B1 (*quis sit sapiens*).
- **tracciare, scrivere** (3): sol. 1.1.3 (*lex … describitur*), sol. 2.20.35 (*circulum … describimus*), an. quant. 11.17 (figura; ambiguo tra tracciare e definire).

Esito: A3 è una spia legittima, ma solo nel senso definitorio; gli altri usi vanno tra i falsi positivi (D).

## 14.11.2026 — Verifica di B5 (*is / quisquis … est qui*)

88 frasi candidate, ottenute con tre schemi (quisquis/quicumque: 73; «X est qui»: 11; «is/ille … est qui»: 4).
- Gli schemi «X est qui» e «is/ille … est qui» catturano quasi solo domande retoriche (*quis tam … est qui…?*) e relative descrittive: nessuna definizione.
- *Quisquis/quicumque* è per lo più un indefinito generico («chiunque», «qualunque»), anche in contesti tecnici (*De musica*).
- Circa 10 frasi hanno valore definitorio di un tipo umano: Acad. 1.3.9, 1.4.10, 1.5.14 (*sapiens igitur erit ille, qui perfecte quaesierit veritatem*); beata v. 3.19, 3.21, 3.22, 4.33 (*Habet ergo modum suum, id est sapientiam, quisquis beatus est*), 4.34 (due); mag. 13.41.
- Emerso per caso un caso di B3: beata v. 4.29 (*nihil aliud miseriam quam egestatem esse conficimus*).

Esito: B5 come formulato è troppo largo (circa 1 su 9). Funziona solo quando il predicato è un tipo umano (*beatus*, *sapiens*, *miser*…) dentro un episodio definitorio.

## 14.11.2026 — Decisioni dopo la verifica (codebook bozza 3)

- **A3**: Armando sceglie di tenerla nel senso di *definire* e di *ritrarre un tipo umano* (8 + 5 frasi); *tracciare/scrivere* → falsi positivi (D).
- **B5**: criterio scelto da Armando = i tipi umani si ricavano dal testo, cioè dalle domande *quis est / quis sit X?* (script `tipi_B5.py`, 8 occorrenze in tutto). Risultato: un solo tipo, *sapiens* (Acad. 3.7.16); le altre 7 sono domande retoriche (*quis est qui…?*), *Dei Filius* (beata v. 4.34) o non pertinenti.
- Verifica di controllo (non adottata): i tipi delle frasi B5 compaiono in frasi interrogative di qualunque forma (beatus 26, sapiens 35, miser 12, stultus 9), ma «comparire in una domanda» non equivale a «essere definito».
- Decisione: **criterio rigoroso + dubbi**. B5 vale solo per *sapiens*; le altre ~9 frasi di tipo entrano con altre spie o vanno nell'elenco dei dubbi.
- **Dato per il paper**: nei dialoghi il testo quasi non pone la domanda «chi è X?» per un tipo umano; le definizioni di tipo compaiono in altre forme (da descrivere dopo la codifica, senza anticipare interpretazioni).
- Nota di metodo: la verifica di controllo è partita da una lista di tipi già nota (beatus, miser…), quindi da una nostra precomprensione; per questo non è stata adottata.

## 14.11.2026 — Campione per la codifica alla cieca

- `build_magistro_cieco.py` → `_dati/De magistro - codifica alla cieca.docx`: 47 paragrafi, solo latino, riferimenti [cap.par], battute separate, colonna per la codifica.
- Omessi i titoletti editoriali NBA (es. *Verba signa sunt…*): suggerirebbero dove si trovano le definizioni.
- `_dati/` è esclusa da git (regola aggiunta a `.gitignore`): contiene testo del corpus.

## 14.11.2026 — Prima codifica di Claude e strumento di codifica per Armando

- `spie.py`: individuazione meccanica e larga delle spie negli otto dialoghi (`_dati/spie_*.tsv`). Conteggi del De magistro calcolati ma non mostrati (codifica alla cieca in corso).
- **De beata vita** codificato per intero da Claude (`_dati/schede_beata_vita.md`): 11 episodi sopra soglia, 7 dubbi, note per una revisione del codebook. Le note NON vengono comunicate ad Armando prima che abbia finito il De magistro, per non influenzarne la codifica.
- Su proposta di Armando, lo strumento di codifica è diventato un artefatto: https://claude.ai/artifact/FFNvwdREpWLrgjnxWMhBcG (privato). Testo latino a sinistra (battute separate, senza titoletti NBA), a destra episodi con spie scelte da menù (ogni spia con il suo significato), definiendum, proponente, esito, tipo/modo, segni (*, ?, NBA), nota; il grado si calcola dalle spie secondo la soglia. Le annotazioni stanno nell'archivio dell'artefatto (collezione `codifica`, un documento per paragrafo; scrive solo il proprietario, gli altri vedono in sola lettura): Claude le legge per il confronto. Generato da `build_codifica_artifact.py` + `codifica_template.html`.
- L'artefatto è pensato anche per mostrare il metodo in una presentazione.

# ClaudeWS — workspace di Armando Bisogno

Professore di Storia della filosofia medievale e Direttore del DiSPaC (Università di Salerno). Studia Agostino e il tardo-antico, si occupa di Digital Humanities e IA. Scrive la newsletter *Macchine Pensanti* e i gialli del commissario Malversi. Questo workspace è insieme spazio di lavoro e *second brain*.

**Rispondi sempre in italiano**, anche nelle risposte tecniche.

Questo file è condiviso tra i vari Mac, perché la cartella sta su Dropbox. Lo stesso vale per la **memoria di Claude**, che sta in `brain/memoria/`: la cartella locale `~/.claude/projects/<chiave>/memory` è solo un link lì. Il link lo crea da solo `session_brief.py` a ogni inizio sessione, su qualunque Mac. Se su un computer trova note proprie, le mette in `brain/memoria/_da_unire/<computer>/`: in quel caso vanno unite alle schede esistenti e poi la cartella va cancellata. `brain/memoria/` è fuori da GitHub (note di direzione e salute): la sincronizza Dropbox, che ne conserva anche le versioni.

## Mappa

| Cartella | Contenuto | Git |
|---|---|---|
| `brain/` | second brain: identità e ToV (`identita/`), scrittura MP, ricerca, progetti, strumenti (`tools/`), memoria di Claude (`memoria/`) | sì (tranne `direzione/` e `memoria/`) |
| `Direzione/` | Consigli e Giunte, Programmazione, Deleghe, Eventi e saluti, Personale, SMA 2026, Mappa Dispac | **no** |
| `Documenti di passaggio/` («DdP») | vaschetta d'ingresso: i file arrivano qui e vanno **smistati** nelle cartelle giuste; resta fissa solo `Tirocini/` | **no** |
| `Ricerca/` | corpus Agostino, Paper, Relazioni, Lavori in corso (*Il racconto fragile*, *L'illusione necessaria*, EUG, Forme), Biblioteca, Monografie | **no** (diritti editoriali) |
| `Didattica/` | anno accademico, lezioni, tesi | sì, tesi escluse |
| `Macchine Pensanti/` | `Bozze/` (.docx dei post), `Esperimenti/` | sì |
| `Macchine Parlanti/` | micropodcast: scalette, template, puntate | sì, audio esclusi |
| `Finzioni/` | testi integralmente prodotti da Claude (Redeo ad me, Ermete Metello, Tre finestre, Epistula de contagio) | sì |
| `Sito/` | tema WP su misura di armandobisogno.it, plugin `ab-deploy`, `deploy.py`, Rassegna | sì |
| `Phitness/` | plugin WordPress Phitness Core (`src/`, ultime zip; vecchie in `_archivio zip/`) e testi degli incontri | no |
| `Ermenetica/`, `Romanzi/`, `UIF/`, `Ermengol/`, `Inglese/` | libro-manifesto DH, epub dei romanzi (solo locale), materiali UIF, maestro di scacchi, varie | vari |
| `Documenti personali e ufficiali/` | CV, documenti, registri; `Salute/` | `Salute/` **mai** su git |

## Come si lavora

- **Testi da leggere, modificare e commentare** (post MP, relazioni, note): come **Claude Doc**, poi copia .docx in `Macchine Pensanti/Bozze/` per i post MP.
- **Paper scientifici**: .docx locale in `Ricerca/Paper/`. Si parte da un sorgente in `_sorgenti/` e si costruisce con `build_paper.py`, con le norme di `Ricerca/Norme editoriali.doc`, salvo norme proprie della rivista. Ogni dato bibliografico va verificato.
- **Agostino**: citare sempre dal corpus in `Ricerca/Agostino testi/` (grep sui `_md`), in latino e nella traduzione NBA, con riferimento e datazione.
- **Relazioni orali**: di norma poche frasi di appunti per passaggio, più la bibliografia. Niente testo da leggere, salvo richiesta esplicita.
- **Macchine Pensanti**: seguire `brain/identita/tono-di-voce.md`. Registro elegante, mai ammiccante. Per ogni uscita anche il post social gemello (IG/FB/LinkedIn).
- **Smistare la DdP**: proporre la destinazione di ogni file prima di spostarlo. Non cancellare mai senza conferma.

## Comandi e strumenti

- `/giunta`: dal PDF del dossier del Consiglio, sintesi schematica per la Giunta.
- `/rassegna`: edizione della rassegna stampa su armandobisogno.it/rassegna.
- `/tirocini`: firma i PFO in `Documenti di passaggio/Tirocini/`.
- `/MacchinePensanti-spunti`, `/substack-5articoli`: spunti e letture nei DB Notion.
- Hook di inizio sessione (`.claude/settings.json`): `session_brief.py` (novità MP, scadenze, PFO), `changes_check.py`, `git_autosync.sh`.

## Più computer: cosa sapere

- **Git**: il repo è `github.com/armandobisogno/ClaudeMac` (privato). `git_autosync.sh` fa pull, commit e push a ogni sessione. La cartella `.git` sta dentro Dropbox: evitare di lavorare su due Mac **nello stesso momento**.
- **Mai su git** file sopra i 95 MB, audio e video, dati sanitari, dati di studenti, verbali riservati. Lo script scarta da solo i file troppo grandi; il resto lo regola `.gitignore`.
- **Dipende dalla singola macchina** (va configurato su ognuna): token GitHub nel portachiavi, variabili d'ambiente (`PH_WP_*` per Phitness, `AB_WP_APP_PASSWORD` per il sito), timer launchd, file `brain/tools/*.local.json`.
- Il percorso di Dropbox può cambiare da Mac a Mac (`~/Library/CloudStorage/Dropbox/` oppure `~/Dropbox/`). Negli script usare percorsi relativi al repo, mai assoluti.
- Le Note vocali → Diario e le routine MP girano **in cloud** (claude.ai/code/routines), non su questo Mac.
- Su questo Mac mancano node e LibreOffice. I .docx si generano con script Python che scrivono direttamente il formato Word (vedi `build_paper.py`); per contare le pagine si usa Word tramite osascript.

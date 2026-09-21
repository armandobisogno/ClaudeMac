# Phitness — laboratorio filosofico di allenamento cognitivo

Progetto pubblico ideato e condotto da Armando Bisogno. «Un *fitness filosofico*».
- Sito live: **phitness.it** (WordPress + plugin custom **Phitness Core**, GPL).
- Pagina di presentazione: **armandobisogno.it/phitnesslab**.
- Codice del plugin in `Phitness/` (non versionato nel repo).

## L'idea

**La "cognitive crisis":** decenni di studi mostrano un declino delle capacità
cognitive; abituati a vedere/produrre contenuti veloci e senza attenzione analitica,
abbiamo innescato una «crisi cognitiva». L'IA la amplifica (sintetizza e produce
testi al posto nostro). **Cal Newport** (NYT): serve un «fitness cognitivo», un
allenamento per (re)imparare a concentrarsi, leggere testi lunghi, scrivere in modo
meditato. Da qui Phitness.

## Il formato — una sessione in tre momenti

1. **Esercizio filosofico** — un problema di storia della filosofia analizzato in un
   video (~20'), per allenare la focalizzazione del pensiero.
2. **Esercizio di lettura** — uno o più testi, ~10' in silenzio; concentrazione sulle
   parole «per pe(n)sare il loro significato».
3. **Esercizio di scrittura** — produrre un testo su un topic fornito al momento.

**«Zero performance, solo esercizio»:** non è una gara; niente domande, niente
interrogazioni, niente confronto; si rispettano i propri ritmi. È pensato anche per
**aziende e comunità**.

## Il plugin (Phitness Core)

WordPress, nessun LMS, nessun ACF, codice di proprietà del committente. CPT
«Allenamenti» compilabile da un'unica schermata; frontend dedicato (dashboard,
«stanza», **Quaderno** personale privato) che non passa dal tema; **timer calcolato
sul server** (resiste al refresh); autosalvataggio della scrittura; analytics
aggregate per il docente (mai i contenuti privati); modalità «open» senza account
(il **report** finale si scarica e resta solo sul dispositivo dell'utente); blocco di
`/wp-admin/` per gli utenti standard. Guida amministratore inclusa.

## Posto nella mappa dell'identità

È la **messa in pratica** di due filoni:
- l'attenzione / lettura / scrittura di [[reference-macchine-pensanti]] («chi scrive
  senza pensare», l'IA che «fa tutto al posto nostro»);
- l'**ermenetica della comunicazione** e le **Public Humanities** di
  [[reference-ermenetica]]: portare fuori le competenze, la *di-vulgazione*, il
  «niente metriche» (= «zero performance»), «Phitness in azienda o con la tua
  comunità».

## Interventi

- **2026-08-31:** allineato il testo della landing del plugin alla versione pubblica
  di armandobisogno.it/phitnesslab. Fasi rinominate «Analisi/Lettura/Scrittura» →
  «Esercizio filosofico / Esercizio di lettura / Esercizio di scrittura»; rimossi i
  badge di durata (30/10/20 minuti) e la nota «I minuti indicati sono un'indicazione»
  **dalla home** (resta nella «stanza»). File toccati:
  `includes/class-phitness-frontend.php` (`render_landing()`), `phitness-core.php`
  (Version 1.2.0 → **1.3.0**), `readme.txt` (Stable tag + changelog). Pacchetto:
  `Phitness/phitness-core-1.3.0.zip` (da ricaricare su WordPress).
- **2026-09-21:** ritocchi al testo della landing (`render_landing()`): a capo dopo
  «...esercizio di scrittura.» prima di «Per riprendere il tempo del pensiero.»;
  la nota «Niente account, niente password...» ora in un riquadro più grande e
  visibile (nuova classe CSS `.phit-lp-privacy`, non più `.phit-microcopy`) e
  integrata con «Oppure invii il tuo testo per una revisione, in forma completamente
  anonima.»; *device*, *topic*, *fitness* in corsivo nel testo; video dell'esercizio
  filosofico descritto come «non più di venti minuti»; «Armando Bisogno» linkato a
  armandobisogno.it; claim finale «Un'ora per te. Si comincia quando vuoi.» →
  «Prenditi un momento per pensare.». File toccati: `includes/class-phitness-frontend.php`,
  `assets/css/phitness.css`, `phitness-core.php` (Version 1.3.0 → **1.4.0**),
  `readme.txt` (Stable tag + changelog). Pacchetto: `Phitness/phitness-core-1.4.0.zip`
  (da ricaricare su WordPress).
- **2026-09-21:** rivisti i testi #2 (`Sapere`, Apologia di Socrate) e #3
  (`Pensare Dio`, argomento ontologico di Anselmo): tolto l'header
  "PHITNESS/#N" e il titolo maiuscolo isolato (il testo #1 "Verità" non li usa
  più), portati a prosa continua senza sottotitoli/elenchi puntati (testo #2
  aveva 4 sottotitoli in grassetto + un elenco puntato), corretti refusi e
  frasi incomplete nel #2 (l'accusa a Socrate, l'oracolo di Cherofonte),
  aggiunta una chiusura riflessiva che riprende il tema iniziale in entrambi
  (come fa il #1 con "che cos'è la verità?"), e nel #3 il registro "voi"
  diretto→teatrale è stato riportato al "noi" inclusivo del #1 (es. "Notiamo"
  non "Notate", "Immaginiamo" non "Immaginate"), comprimendo i due paragrafi
  finali di istruzioni d'esercizio in un'unica chiusura aperta. File:
  `Phitness/2. Sapere_Socrate.docx`, `Phitness/3. Pensare Dio.docx`.
  Create anche le slide Canva corrispondenti clonando lo stile del mazzo
  "Verità" (banda turchese, logo PHITNESS bicolore, frecce e X rossa per lo
  schema "candidati eliminati"): **ESERCIZIO #2 - Sapere**
  (politico/poeta/artigiano → chi è davvero sapiente, con politico scartato e
  Socrate come risposta finale) e **ESERCIZIO #3 - Pensare Dio** (i cinque
  passi di Anselmo compressi in tre tappe, poi la parodia di Gaunilone
  sull'isola perfetta scartata mentre triangolo/Dio reggono), 13 slide
  ciascuna. Nota: il mazzo Canva originale "Verità" e il file "1. Verità.docx"
  risultavano già in fase di revisione live durante questa sessione
  (probabilmente modifiche in corso di Armando in parallelo) — i nuovi mazzi
  e i due testi sono stati allineati alla versione più aggiornata trovata.
  Su richiesta, applicato lo stesso trattamento anche al **testo #4**
  (`Destino e libertà`, stoicismo/Crisippo/Epitteto): tolto l'header
  maiuscolo, registro "voi" (Immaginate, notate, badate, pensate) riportato a
  "noi"/impersonale in tutto il testo, e i due "movimenti" finali
  dell'esercizio (smascherare l'argomento pigro + le due colonne di Epitteto)
  compressi in un'unica chiusura riflessiva. File:
  `Phitness/4. Destino e libertà.docx`. Creato anche il mazzo
  **ESERCIZIO #4 - Destino e libertà** (13 slide, stesso stile clonato):
  fan-out su "l'argomento pigro / il cilindro / il cane e il carro", build per
  ciascuno dei tre, poi la chiusura "Siamo davvero liberi?" che le ripropone
  tutte e tre scartando (X rossa) l'argomento pigro mentre cilindro e cane
  restano validi.

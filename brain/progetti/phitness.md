# Phitness — laboratorio filosofico di allenamento cognitivo

Progetto pubblico ideato e condotto da Armando Bisogno. «Un *fitness filosofico*».
- Sito live: **phitness.it** (WordPress + plugin custom **Phitness Core**, GPL).
- Pagina di presentazione: **armandobisogno.it/phitness**.
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
  di armandobisogno.it/phitness. Fasi rinominate «Analisi/Lettura/Scrittura» →
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
- **2026-10-06 — versione 2.0.0** (online su phitness.it). Sorgente di lavoro in
  `Phitness/src/phitness-core/`, pacchetto `Phitness/phitness-core-2.0.0.zip`.
  - **Consegna anonima**: pagine `/consegna` e `/ritira`. Testo scritto/incollato,
    `.txt` letto nel browser (al server arriva solo il testo), foto del foglio
    ricodificata (via EXIF: posizione, telefono, ora; lato max 2400 px) in
    `uploads/phitness-consegne/` chiusa da `.htaccess`. Codice personale tipo
    `LUCE-VENTO-ARCO-4821` salvato solo come HMAC; niente IP/nome/email; si salva
    il giorno, non l'ora; limite 15 tentativi/ora per impronta IP giornaliera
    (transient); cancellazione automatica dopo 180 giorni (cron giornaliero);
    pagine escluse dalla cache. Classi: `class-phitness-consegne.php`,
    `trait-phitness-frontend-consegne.php`, `assets/js/phitness-consegna.js`.
  - **Bacheca**: Phitness → Consegne (lettura, restituzione «Salva e rendi
    visibile» / bozza, elimina; numero da restituire nel menu) e Phitness →
    Incontri (codici tipo `ACME-OTT26`, link `/consegna?incontro=…`). Mail di
    avviso all'admin senza contenuto. `class-phitness-admin-consegne.php`.
  - **Identità**: stile di armandobisogno.it (turchese #0097B2, zafferano,
    Libre Caslon + Hanken Grotesk ospitati nel plugin), nuovo marchio Φ
    (`assets/img/phitness-mark.svg`: anello turchese, asta scura, punto zafferano).
  - Landing riscritta (niente minutaggi; restituzione anonima; link a
    armandobisogno.it/phitness per le aziende); dashboard senza «N minuti»;
    a fine sessione box «Vuoi una restituzione?» → `/consegna?da=ID` che riprende
    il testo dal localStorage.
  - Testato su WordPress locale (SQLite) e con una consegna reale su phitness.it,
    poi cancellata.
  - Deploy: plugin «Armando Deploy» anche su phitness.it; credenziali
    `PH_WP_USER`/`PH_WP_APP_PASSWORD` in ~/.zshrc; comando:
    `AB_WP_URL=https://www.phitness.it AB_WP_USER=$PH_WP_USER AB_WP_APP_PASSWORD=$PH_WP_APP_PASSWORD python3 Sito/deploy.py plugin Phitness/phitness-core-X.zip`.
  - La vecchia copia del plugin (1.0.0) su armandobisogno.it è stata disattivata.
- **2026-10-06 — versione 2.1.0**: Fase 1 anche in **audio** (meta `_phit_audio` = allegato
  della Libreria media, oppure `_phit_audio_url` link diretto; `phit_audio_url()` in helpers;
  lettore «Ascolta la lezione» nella stanza; video e audio possono convivere). Metabox
  rinominata «Fase 1 — Lezione filosofica (video o audio)». Pacchetto
  `Phitness/phitness-core-2.1.0.zip`, online su phitness.it.
- **2026-10-06 — versione 2.2.0**: svolta di Armando: **niente allenamento da soli**, almeno per ora.
  phitness.it diventa la vetrina degli incontri per aziende e comunità, allineata ai testi di
  armandobisogno.it/phitness (che restano il riferimento). In primo piano «Organizza un incontro»
  (menu + apertura + sezione `#contatti` con modulo → `class-phitness-contatti.php`, mail a
  `phit_contatti_email`, predefinito arbisogno@unisa.it, via WP Mail SMTP). Area, stanze e quaderno
  rimandano alla home (riattivabili con l'opzione `phit_solo` = 1). Consegna e Ritira restano, «per chi
  ha partecipato a un incontro». Tolti da armandobisogno.it/phitness tutti i riferimenti all'allenarsi
  da soli (simulazioni online, «prova per conto tuo»).

## Svolta 2026-10-19 — Phitness come «passioni che non deleghiamo»

Nuova idea di Armando: davanti all'IA resteranno nostre le attività che non vogliamo
delegare perché ci piacciono. Phitness allena e coltiva tre passioni tutte umane —
**pensare, leggere, scrivere** — e prova a suscitarle in chi non le ha scoperte
(componente pedagogica; «proprio ora che c'è SUNO, organizzo corsi di chitarra»).
Non più servizio di consulenza / crisi cognitiva come motore.
- Nessuna condivisione finale (crea l'ansia del «devo dire qualcosa»); si partecipa
  solo nel momento filosofico iniziale. Niente confronto a voce dopo la lettura.
  Bocciato anche il Mentimeter anonimo (in 20 persone l'anonimato non regge).
- Pagina armandobisogno.it/phitness riscritta (tema 1.5.2), testi rivisti riga per
  riga da Armando: H1 «Cosa resterà? *Le nostre passioni.*»; «Perché proprio adesso?»
  (Cosa perderemo / Cosa resterà nostro / Il laboratorio); «Tre passioni, tre
  esercizi» (Pensare/Leggere/Scrivere); fascia «Zero performance, solo esercizio.»
  confermata; contatti «dove vivi, studi o lavori». Scheda home e meta aggiornate.
- **Grafica:** pagina con tavolozza propria come Finzioni (`body.phitness` in
  style.css). Verde provato e bocciato; ora **ambra-ocra #C47D10** (testo scuro
  sull'ocra, bruno #3A260F per le fasce profonde). Armando «ci pensa». Cerchio Φ
  ocra; puntino ancora zafferano (proposto bruno).
- **Da fare:** portare testi e colore su phitness.it (plugin) quando Armando conferma.
- **Grafica (stesso giorno, tema 1.6.0):** ocra bocciato («rende tutto banale»).
  Pagina ripensata ad hoc, **«Tre stanze»**, senza la foto di Armando: carta avorio
  + inchiostro; apertura con tre «porte» ad arco sui dipinti; tre stanze a tutto
  schermo, una per passione, col colore del dipinto: Pensare = Rembrandt, *Filosofo
  in meditazione* (bruno #16110A, PD, mostrato intero perché il file è piccolo);
  Leggere = Fragonard, *La lettrice* (lilla #DCD0DA, NGA CC0); Scrivere = Vermeer,
  *Donna che scrive una lettera* (blu #1C2846, NGA CC0). Immagini in
  `assets/img/phit-*.jpg`; CSS `.ph-*` in style.css. Cerchio Φ ora oro #B8862E.
- **2026-10-19, struttura finale** (tema 1.7.1 / plugin **2.6.0** su phitness.it):
  apertura solo testo («Nella stagione dell'IA quello che resta umano è ciò che
  facciamo per il piacere di farlo. / *Phitness* è proprio questo. / Un *fitness*
  filosofico…») → dittico «Cosa delegheremo all’IA?» (grigio pietra) / «Cosa resterà
  nostro?» (inchiostro, «nostro?» oro) → «*Phitness* nasce per allenare e coltivare tre
  di queste passioni…» + tre porte ad arco coi dipinti (nomi sotto, su mobile carosello
  orizzontale) → «Un tema. Tre passioni. Tre esercizi.» (3 righe solo su mobile) → tre
  stanze (su mobile quadri interi) → «Zero performance» con **ensō** oro → carosello,
  svolgimento, restituzione, formati, contatti. «Chi usa chi?» tolto. «a penna», non
  «a mano». Plugin: tavolozza carta/inchiostro per tutta la piattaforma (blocco CSS
  «v2.6» in coda a phitness.css), Φ con cerchio oro anche nel favicon.
  PHP per lint: binario statico in scratchpad (dl.static-php.dev, macos-aarch64).
- **2026-10-20** (tema 1.8.1 / plugin 2.7.1): tolte le tre porte; «*Phitness* nasce per
  allenare e coltivare queste passioni.» chiude la metà scura del dittico (filo oro);
  sotto, striscia (Lemonnier provato e TOLTO su richiesta; ora tre cerchi oro a pennello «ph-tre», stile ensō) (era: Lemonnier 1812,
  PD, Commons WGA12652, `phit-lemonnier.jpg`) + testo «laboratorio guidato, un momento
  che puoi organizzare per la tua comunità… un’ora, tre momenti» con le tre passioni in
  grassetto. Carta più scura, **pergamena** #ECE2CF (paper-2 #E2D5BD).
- **2026-10-20 — plugin 2.8.0 (online su phitness.it dal 20/10)**: avviato il «flusso di lavoro» degli
  incontri, con un documento per ogni fase, ognuno pensato come pagina di phitness.it. Primo: **/organizza**, «Organizzare un incontro»
  (scheda per chi invita: spazio, tecnica, tempi, chi partecipa, cosa porto io, da decidere
  insieme), stampabile in 2 pagine A4. File `includes/trait-phitness-frontend-organizza.php`
  (voci in `organizza_sezioni()`, filtro `phit_organizza_sezioni`), CSS blocco «v2.8».
  Collegata dai contatti («Prima di scrivermi…») e dal piè di pagina; ancora `#lezioni` sul
  carosello; permalink rigenerati automaticamente al cambio di versione (`phit_rules_version`).
  Stesso pacchetto: **Incontri** (decisione di Armando 20/10): tabella incontri estesa (titolo,
  luogo, workout_id, inizio, durata 75'; DB v5); bacheca crea/modifica con stato; pagine
  `/incontri` (codice) e `/incontri/CODICE` (`trait-phitness-frontend-incontri.php`): prima = solo
  data/ora/luogo, aperto = testi dell'allenamento + traccia + consegna, chiuso = solo ritiro;
  consegna aperta fino a **24 h dopo la fine** (`PHIT_CONSEGNA_ORE`, controllo anche lato server).
  **Si scrive fuori dal sito** (word processor) e si incolla — scelta di Armando per non rischiare
  testi persi; foto delle pagine con avviso «numera le pagine in alto a destra». Accesso solo col
  codice (niente elenco pubblico), testi visibili solo dall'inizio. Menu: Come funziona · Formati ·
  Incontri · [Organizza un incontro]; #contatti in due colonne (modulo | card «Che cosa serve» →
  /organizza). Prossimo: istruzioni per i partecipanti, foglio da sala con QR, checklist interna.
- **2026-10-20 — plugin 2.8.1–2.9.0 (online)**: 2.8.1 testo card contatti («Una breve guida per
  sapere cosa serve per fare *Phitness*!»); 2.8.2 /organizza più asciutta; 2.8.3 nuova og-image
  `og-phitness-2.jpg` (pergamena, «Cosa resterà? Le nostre passioni.») e «Come funziona» →
  `#come-funziona` (fascia laboratorio guidato). **2.9.0 = flusso di lavoro** (decisioni di
  Armando): restituzioni **entro 10 giorni**; iscrizioni dal referente per aziende/gruppi chiusi,
  **Eventbrite** (evento non pubblico, widget embedded checkout nella pagina dell'incontro fino
  all'inizio) per incontri aperti; checklist nella **scheda dell'incontro** in bacheca (8 tappe con
  scadenze da `inizio`, spunte via ajax `phit_incontro_check`, colonna `checklist` JSON, DB v6;
  campi `referente`, `eventbrite`); modelli da copiare: conferma, invito, restituzioni pronte,
  grazie (`modelli()` in admin-consegne). Slide da sala `/incontri/CODICE/?sala=1` con QR
  (`assets/js/qrcode.min.js`, MIT). Backoffice di Armando: phitness.it/wp-admin, utente «admin».
- **2026-10-21 — sul bianco** (tema 1.9.0 / plugin **2.9.1**; attenzione: un'altra sessione
  il 20.10 ha portato il plugin a 2.8.0–2.9.0 con incontri, /organizza, checklist: non
  sovrascrivere, partire sempre dal sorgente locale aggiornato). Pagine Phitness su fondo
  bianco (#FFFFFF, fasce #F5F4F1); caratteri come luisacarrada.it: **Prata** (titoli) +
  **DM Sans** (testo), corsivi dei titoli in **Playfair Display** italic (Prata non ha
  corsivo); woff2 ospitati in assets/fonts di tema e plugin. Prova grafica «sul bianco»
  (collage, schede a colori pieni arancio/fucsia/cobalto, disegni al tratto animati per
  Pensare/Leggere/Scrivere, ritratto a retino cobalto) nell'artifact privato
  https://claude.ai/artifact/M4H5DyWFWEsqbLRxbZUEpH — non ancora portata online.
- **2026-10-21, plugin 2.9.2:** phitness.it ha l'apertura della bozza nuova («Un’ora per
  pensare, leggere e scrivere *insieme.*» + testo + pulsanti «Organizza un incontro» /
  «Per saperne di più su di me» → armandobisogno.it), senza ritratto né riga dei fatti.
  **Prata per tutto il testo** (scelta di Armando, campione A), corsivi Playfair Display,
  niente grassetti. Bozza completa da zero (prima cosa succede, poi perché; per chi; FAQ)
  nell'artifact M4H5DyWFWEsqbLRxbZUEpH; campionario font GM4v4LNb3CBVxtXTuKi89i.
  armandobisogno.it/phitness: ancora Prata titoli + DM Sans testo e vecchia apertura.
- **2026-10-21, plugin 2.9.13 / tema 1.9.7:** apertura con foto originale e parole chiave in
  arancio (controcolore #E2520A); dittico «Cosa stiamo delegando all’IA?» (scuro) / «Cosa
  resterà sempre nostro?» (chiaro) con testi asciugati; via la fascia dei tre cerchi e la
  sezione Formati (anche dal menu); «Come si svolge un incontro…» con freccia disegnata
  verso la restituzione. Proposte A/B/C per ripensare il dittico: artifact LbAiybqcqfY7nySA5b7m9R
  (per ora lasciato com'è).

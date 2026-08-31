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

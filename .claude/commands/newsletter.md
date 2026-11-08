---
description: Scrive un nuovo numero di Macchine Pensanti nel tono di voce di Armando, a partire da un contenuto fornito (testo, file, link, PDF), e lo salva come .docx in Scrittura/Macchine Pensanti/Bozze/
argument-hint: [contenuto di partenza: testo incollato, percorso di file, URL; più eventuali indicazioni su taglio, titolo, lunghezza]
---

Scrivi un nuovo numero della newsletter Substack **Macchine Pensanti** di Armando Bisogno,
nella sua voce, a partire dal contenuto che ti passa.

Contenuto e indicazioni per questo numero: **$ARGUMENTS**

Se il contenuto di partenza manca o non è chiaro, chiedilo prima di procedere.

## 1. Leggi il contenuto di partenza

Testo incollato, file locale (docx, pdf, md, txt), URL (WebFetch) o file nella cartella
temporanea (`C:\Users\Armando Bisogno\Dropbox\LAVORO\FileTempClaude` se dice "c'è un file
temp"). Leggilo per intero: è l'oggetto concreto da cui parte il pezzo, non il suo
argomento esaustivo. Annota autore, titolo, anno, tesi e i passaggi citabili.

## 2. Taratura del tono: gli ultimi dieci numeri

Scarica il testo integrale degli ultimi dieci numeri pubblicati:

```
python3 brain/tools/mp_ultimi.py 10 <scratchpad>/mp_ultimi10.txt
```

e leggili tutti. Osserva attacchi, lunghezza dei periodi, uso dei titoletti, modo di
introdurre le fonti, chiuse. Servono anche a evitare ripetizioni: non riprendere
attacchi, esempi o immagini già usati di recente, e se il tema tocca un numero
precedente richiamalo esplicitamente (l'auto-citazione è una mossa tipica).
Se lo script fallisce (rete), dillo e procedi solo con le regole qui sotto.

## 3. Regole di voce

Leggi `brain/identita/tono-di-voce.md` **escludendo tutto ciò che riguarda i romanzi**
(sezione "Romanzi (Malversi)", blues, Camilleri, dialogo, cornice epistolare): per la
newsletter valgono solo la voce saggistica e le note di Macchine Pensanti. Consulta
`brain/scrittura/macchine-pensanti.md` per gli archi tematici e i numeri da richiamare.
Leggi anche la memoria `user_letture_spunti.md` per eventuali letture pertinenti.

In sintesi, vincolanti:

- **Formato**: titolo evocativo e allusivo, mai descrittivo; sottotitolo che enuncia la
  domanda o il tema in una frase distesa; corpo in prosa continua con 2–4 titoletti di
  sezione; **nessun elenco puntato**. Lunghezza 700–1000 parole salvo indicazione diversa.
- **Percorso**: aggancio concreto (il contenuto passato, o una scena quotidiana che lo
  introduce) → risalita a un concetto classico o a un autore-bussola → applicazione al
  presente → riformulazione che ribalta la domanda iniziale → chiusa aperta (domanda
  sospesa, immagine forte o gancio al prossimo numero).
- **Registro**: colto ma piano, prima persona misurata («Credo che il punto stia qui»),
  ci si rivolge al lettore («proviamo a…», «chiediamoci…»). Termini tecnici tradotti
  subito in un'immagine quotidiana. Alternanza di affondi brevi e periodi analitici.
- **Elegante, mai ammiccante**: niente «per capirci», «si dirà», «Ecco:», anglicismi
  giocosi, strizzate d'occhio, CTA enfatiche, finta neutralità, moralismo spocchioso.
  Né apocalisse né entusiasmo.
- **Fonti**: citate con precisione (Autore, anno) nel corpo del testo; nessun dato
  bibliografico inventato: se non è verificabile dal contenuto o da una ricerca, non
  metterlo. Agostino si cita dal corpus in `Università/Ricerca/Agostino strumenti/`.
- Nessun meta-commento, nessuna avvertenza sull'uso dell'IA.

## 4. Salva la bozza in Word

Scrivi il pezzo in un file markdown nello scratchpad con questo formato:

```
# Titolo

> Sottotitolo

Paragrafo...

## Titoletto di sezione

Paragrafo con *corsivo* e **grassetto**...
```

(`---` su riga a sé per uno stacco). Poi convertilo:

```
python3 brain/tools/mp_bozza_docx.py <scratchpad>/bozza.md "Scrittura/Macchine Pensanti/Bozze/AAAA-MM-GG_titolo-breve.docx"
```

con la data di oggi e un titolo breve in minuscolo con trattini.

## 5. Consegna

Nella risposta, in poche righe: titolo e sottotitolo, percorso del .docx, fonti usate.
Aggiungi il **post social gemello** (IG/FB/LinkedIn) secondo le regole "Post social" di
`tono-di-voce.md`: apertura che accompagna, tesi in 2–3 righe ancorata a un'immagine del
pezzo, chiusa morbida, «Ne parlo nell'ultima uscita di Macchine Pensanti.» + «Link in
bio alla newsletter.», hashtag #macchinepensanti #IA #AI + un termine chiave.

---
description: Dal video di Armando (in DdP) 4 Reel brevi per Instagram (sottotitoli grandi in maiuscolo, karaoke arancione, domanda-hook); prima propone tagli e hook e attende l'approvazione, poi produce i video in Scrittura/Video/<data>/ e il copy dei post
argument-hint: "[nome o percorso del video; se vuoto prende il video più recente in Documenti di passaggio/]"
---

Sei "reel" di Armando Bisogno. Armando registra video orizzontali in cui parla
(di solito seduto sul divano, al centro dell'inquadratura). Il video intero va su
YouTube; tu ne ricavi **4 Reel brevi per Instagram** e il **copy** di ciascun post.

Video di questo giro (se vuoto, il più recente .mp4/.mov in `Documenti di passaggio/`): **$ARGUMENTS**

Il lavoro ha **due tempi**: prima proponi tagli e hook e **ti fermi** finché Armando
non approva; solo dopo produci.

## Dove vanno i file

- `Scrittura/Video/<AAAA-MM-GG>/` (data di oggi; se esiste già, aggiungi `-2`):
  dentro **solo** i 4 video (`01_titolo.mp4` … `04_titolo.mp4`) e `copy.md`.
- `Scrittura/Video/<AAAA-MM-GG>/_lavoro/`: piano, trascrizione, .srt, tempi per
  parola. Si versionano (gli .mp4 no, li esclude il `.gitignore`).
- Il video originale resta in DdP: non spostarlo né cancellarlo senza chiedere.

## Strumento

`brain/tools/video_ig.py` (ffmpeg + faster-whisper). Lancialo dalla radice del repo
con `python3` (non `python3 -I`: le librerie stanno nei pacchetti utente). Se manca
qualcosa: `pip3 install --user imageio-ffmpeg faster-whisper`. Sotto, `DIR` è la
cartella con la data e `LAV` è `DIR/_lavoro`.

## Primo tempo: la proposta

1. **Trascrivi** (≈2 min ogni 10 min di video; in background se è lungo):
   `python3 brain/tools/video_ig.py trascrivi "<video>" --out "LAV"`

2. **Controlla l'inquadratura**: due o tre fotogrammi in punti diversi con
   `python3 brain/tools/video_ig.py anteprima "<video>" --t SEC --x 0.5 --zoom 1.0 --out <scratchpad>/a.jpg`
   e guardali (il rettangolo rosso è il ritaglio 9:16). Armando gesticola: le mani
   devono restare dentro. Di norma `zoom 1.0` e `x` sul centro del corpo (≈0.49
   nel video del divano).

3. **Scegli i 4 tagli** leggendo tutta la trascrizione:
   - **20–40 s**, uno per idea; i Reel funzionano da soli, non riassumono il video;
   - **la prima parola è già la tesi**: si parte da una delle frasi più nette del
     discorso, non dalla premessa. Niente rimandi iniziali («come dicevo»,
     «questo», «Punto secondo»); se la frase comincia con un connettivo («Cioè il
     sapere…»), si taglia dopo il connettivo e si mette la maiuscola nel .srt;
   - finisce su una frase conclusa; se il discorso prosegue senza pausa, la
     dissolvenza finale ammorbidisce il taglio;
   - i quattro, insieme, coprono l'arco del discorso, senza ripetersi.

   Per ciascuno, un **titolo** breve (≤ 32 caratteri; dà il nome al file, non
   compare nel video) e una **domanda-hook**: breve (≤ 40 caratteri), compare
   grande in alto nei primi 3 secondi e fa anche da copertina. Deve essere una
   domanda vera, a cui il passaggio risponde («I dati sono davvero neutrali?»,
   «Un dato è una fotografia della realtà?»), mai un'esca («Non crederai a…»).

4. **Sottoponi la proposta ad Armando e fermati.** Una tabella con, per ogni Reel:
   numero, titolo, domanda-hook, inizio–fine nel video (mm:ss) e durata, prima e
   ultima frase del taglio. Aggiungi in una riga i punti dubbi della trascrizione,
   se ce ne sono. Poi **attendi l'approvazione**: Armando può cambiare tagli,
   domande, ordine. Non generare sottotitoli né video prima del suo via libera.

## Secondo tempo: la produzione (dopo l'approvazione)

5. **Scrivi `LAV/piano.json`**:
   ```json
   {
    "video": "Documenti di passaggio/<file>",
    "out": "Scrittura/Video/<data>",
    "lavoro": "Scrittura/Video/<data>/_lavoro",
    "x_centro": 0.49, "zoom": 1.0,
    "correzioni": {"\\bmanistic": "umanistic"},
    "correzioni_srt": {},
    "clip": [{"titolo": "…", "hook": "…?", "inizio": 70.9, "fine": 101.0}, …]
   }
   ```
   `inizio`/`fine` in secondi dalla trascrizione: lo script li aggancia ai confini
   di parola (campo `taglio`); metti `inizio` un poco **prima** dell'attacco della
   prima parola. `correzioni` = espressioni regolari per gli errori ricorrenti di
   Whisper. Lo stile è già quello predefinito (deciso da Armando il 13.11.2026) e
   non va cambiato senza richiesta: MAIUSCOLO, Avenir Next Heavy corpo 80, blocchi
   di ≤ 22 caratteri, parola pronunciata in arancione `#FF8A00`, hook corpo 92 per
   3 s, **nessuna intestazione** (né titolo né firma nel video).

6. **Sottotitoli**: `python3 brain/tools/video_ig.py sottotitoli "LAV/piano.json"`
   (`--sovrascrivi` per rifarli). Controlla la prima e l'ultima parola di ogni clip.

7. **Correggi i sottotitoli: è il passaggio che conta.** Rileggi ogni .srt per
   intero. Whisper sbaglia nomi propri («Drachre» per Drucker), parole tronche
   («manistico»), accenti («da» per «dà»), concordanze, punteggiatura. Le
   correzioni vanno in `correzioni_srt` del piano, per clip
   (`"01": [["da", "a"], …]`); lavorano parola per parola, anche a cavallo di due
   blocchi, e restano registrate. Poi
   `python3 brain/tools/video_ig.py correggi "LAV/piano.json"`.
   Si correggono i refusi e la punteggiatura, non si riscrive il parlato. Se non si
   capisce che cosa è stato detto, **lo segnali** invece di inventare.

8. **Render**: `python3 brain/tools/video_ig.py render "LAV/piano.json"` (≈35 s a
   clip; `--solo N` per rifarne una; `--prova 8` per un file `_prova.mp4` di 8 s,
   da cancellare dopo). Uscita 1080×1920, H.264 + AAC, audio a −14 LUFS.
   Prima di consegnare:
   - estrai un fotogramma nei primi 2 s di un Reel (si vede l'hook) e uno a metà,
     e guardali: l'hook non deve coprire il viso; se va su tre righe e lo tocca,
     proponi una domanda più corta;
   - **verifica la sincronia**: ritrascrivi l'audio dei Reel finiti con
     faster-whisper e controlla che la prima, una centrale e l'ultima riga di ogni
     .srt cadano entro pochi decimi dalla parola corrispondente.

9. **Copy dei post**: `DIR/copy.md`, un testo per Reel, preceduto dal link al video
   YouTube (chiedilo se non lo hai) e dal **calendario**: il video completo esce il
   venerdì insieme al Reel 01, poi un Reel ogni due giorni (domenica, martedì,
   giovedì), così la serie copre la settimana fino al video successivo; con le date
   reali e l'hook di ciascuno. Il modello del testo è il post del
   primo Reel di Armando (13.11.2026, «Il nuovo petrolio»):

   > Produciamo dati continuamente: ogni volta che usiamo il telefono, paghiamo con
   > la carta o passiamo davanti a una videocamera di sorveglianza.
   >
   > La fiducia che riponiamo nella loro utilità ha prodotto uno strano effetto
   > collaterale: ci ha portato a credere che il dato sia un'informazione neutrale,
   > una fotografia oggettiva della realtà per quella che è.
   >
   > Un dato, però, non nasce da solo: c'è sempre qualcuno che ha deciso di
   > raccoglierlo, che ha scelto che cosa registrare e che cosa lasciare fuori.
   >
   > Ne parlo nel video completo, sul mio canale YouTube. Link in bio.

   Come regolarsi:
   - **tre paragrafi brevi + la chiusa fissa** «Ne parlo nel video completo, sul mio
     canale YouTube. Link in bio.»;
   - si parte da **esperienze quotidiane concrete** (il telefono, la carta, la
     videocamera), in prima persona plurale, con frasi dichiarative;
   - il secondo paragrafo dà la tesi del Reel; il terzo apre il passo successivo con
     un «però», e lascia al video completo il resto del ragionamento;
   - **niente retorica**: niente «Proviamo a pensare», «Forse vale la pena», domande
     a effetto, nomi di studiosi usati come etichetta, imperativi; niente hashtag,
     salvo richiesta;
   - registro sorvegliato, mai ammiccante (`brain/identita/tono-di-voce.md`).

10. **Riferisci**: la cartella, i 4 Reel con titolo, hook e durata, i dubbi di
    trascrizione rimasti, il copy (riportalo anche nella risposta, pronto da
    incollare).

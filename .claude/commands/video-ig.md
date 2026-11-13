---
description: Da un video lungo di Armando (in DdP) estrae 4 clip verticali per Instagram (Reel 9:16, titolo, sottotitoli incisi) in Scrittura/Video/<nome>/, con le didascalie dei post
argument-hint: "[nome o percorso del video; se vuoto prende il video più recente in Documenti di passaggio/]"
---

Sei "video-ig" di Armando Bisogno. Armando registra video orizzontali in cui parla
(di solito seduto sul divano, al centro dell'inquadratura) e li lascia in
`Documenti di passaggio/`. Tu ne ricavi **4 Reel per Instagram**: quattro passaggi
autonomi, ritagliati in verticale, con titolo e sottotitoli incisi, più la
didascalia di ciascun post.

Video di questo giro (se vuoto, il più recente .mp4/.mov in DdP): **$ARGUMENTS**

## Strumento

`brain/tools/video_ig.py` (ffmpeg + faster-whisper). Va lanciato dalla radice del
repo con `python3` (non `python3 -I`: le librerie stanno nei pacchetti utente).
Se manca qualcosa: `pip3 install --user imageio-ffmpeg faster-whisper`.

Uscita: `Scrittura/Video/<nome del video senza estensione>/` (`DIR` qui sotto).
Gli .mp4 sono esclusi da git dal `.gitignore`; piano, trascrizione, .srt e
didascalie invece si versionano.

## Procedura

1. **Trascrivi** (≈2 min ogni 10 min di video):
   `python3 brain/tools/video_ig.py trascrivi "<video>" --out "DIR"`
   Lancialo in background se il video è lungo. Produce `trascrizione.txt` (righe
   con i tempi) e `trascrizione.json` (tempi per parola).

2. **Controlla l'inquadratura**: due o tre fotogrammi in punti diversi del video con
   `python3 brain/tools/video_ig.py anteprima "<video>" --t SEC --x 0.5 --zoom 1.0 --out <scratchpad>/a.jpg`
   e guardali (il rettangolo rosso è il ritaglio 9:16). Armando gesticola: le mani
   devono restare dentro. Di norma `zoom 1.0` (altezza piena) e `x` sul centro del
   corpo (≈0.49 nel video del divano).

3. **Scegli i 4 passaggi** leggendo tutta la trascrizione. Criteri:
   - ciascuno **autonomo**: si capisce senza il resto del video; non comincia con
     un rimando («come dicevo», «questo», «Punto secondo») né con un nome non
     ancora introdotto, se si può evitare;
   - **30–90 s** (meglio 45–75); comincia su una frase forte e finisce su una frase
     conclusa, mai a metà ragionamento;
   - i quattro, insieme, coprono **l'arco del discorso** (tesi, esempio,
     svolgimento, ricaduta), senza ripetersi;
   - un **titolo** breve per ciascuno (≤ 32 caratteri), sobrio e non ammiccante
     (ToV di `brain/identita/tono-di-voce.md`): un'idea, non un clickbait.

4. **Scrivi `DIR/piano.json`**:
   ```json
   {
    "video": "Documenti di passaggio/<file>",
    "out": "Scrittura/Video/<nome>",
    "x_centro": 0.49, "zoom": 1.0, "sottotitoli": true,
    "correzioni": {"\\bmanistic": "umanistic"},
    "correzioni_srt": {},
    "clip": [{"titolo": "…", "inizio": 43.0, "fine": 100.9}, …]
   }
   ```
   `inizio`/`fine` in secondi, presi dalla trascrizione: lo script li aggancia ai
   confini di parola (campo `taglio`), quindi basta l'approssimazione al decimo;
   per non perdere la prima parola, metti `inizio` un poco **prima** del suo
   attacco. `correzioni` = espressioni regolari applicate a ogni blocco quando si
   generano i sottotitoli (errori ricorrenti di Whisper). Opzionali: `"firma"`
   (predefinita «Armando Bisogno · Macchine Pensanti»; `""` per toglierla),
   `"font"`, `"caratteri_per_riga"` (32).

5. **Genera i sottotitoli**:
   `python3 brain/tools/video_ig.py sottotitoli "DIR/piano.json"` (aggiungi
   `--sovrascrivi` per rifarli). Controlla che la prima e l'ultima parola di ogni
   clip siano quelle volute.

6. **Correggi i sottotitoli: è il passaggio che conta.** Rileggi ogni .srt per
   intero. Whisper sbaglia nomi propri (Drucker → «Drachre»), parole tronche
   («manistico»), accenti («da» per «dà»), concordanze, punteggiatura. Metti le
   correzioni in `correzioni_srt` del piano, per clip (`"01": [["da", "a"], …]`):
   lavorano parola per parola, anche a cavallo di due blocchi, e restano registrate.
   Poi `python3 brain/tools/video_ig.py correggi "DIR/piano.json"`.
   Si corregge la trascrizione, non si riscrive il parlato: si tolgono i refusi e si
   sistema la punteggiatura, non si migliora lo stile. Se un punto è dubbio (non si
   capisce che cosa è stato detto), **segnalalo ad Armando** invece di inventare.

7. **Render**: `python3 brain/tools/video_ig.py render "DIR/piano.json"` (≈35 s a
   clip; `--solo N` per rifarne una). Uscita: `DIR/NN_titolo.mp4`, 1080×1920,
   H.264 + AAC, audio normalizzato a −14 LUFS, dissolvenza breve in entrata e in
   uscita, titolo e firma in alto, sottotitoli nella fascia bassa ma sopra
   l'interfaccia di Instagram. Estrai un fotogramma da una clip e guardalo prima di
   consegnare.

8. **Didascalie**: `DIR/didascalie.md`, una per Reel, con il formato fisso del post
   social (sezione «Post social» di `brain/identita/tono-di-voce.md`): apertura che
   accompagna, tesi in 2–3 righe ancorata a un'immagine del video, chiusa morbida,
   CTA sobria, hashtag essenziali (#macchinepensanti #IA #AI + 1 termine chiave).
   Se il video nasce da un'uscita di MP, la CTA è quella fissa («Ne parlo
   nell'ultima uscita di Macchine Pensanti. / Link in bio alla newsletter.»).
   Indica anche l'ordine di pubblicazione consigliato.

9. **Riferisci**: i 4 file con durata e titolo, i dubbi di trascrizione rimasti,
   il percorso delle didascalie. **Non** spostare né cancellare il video originale
   in DdP senza chiedere (regola della DdP).

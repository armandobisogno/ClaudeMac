# Finzioni

Prodotti pseudo-medievistici e letterari scritti per intero da Claude Code.

- `Redeo ad me/`: saggio su Agostino e la scrittura autobiografica (prima in `Ricerca/Paper/`)
- `Ermete Metello/`: monografia su un monaco-filosofo cavense inesistente (in corso)
- `Tre finestre/`: il prologo di *Terapie* (e di *Mosaici*) riscritto alla maniera di tre autori; libretti PDF+EPUB con `build.py` proprio (prima in `Macchine Pensanti/Esperimenti/`); sul sito solo le due *Terapie*. Il prologo originale è di Armando, quindi la nota con l'asterisco va solo sulle riscritture (II–IV), in fondo a ciascuna

- `Epistula de contagio/`: pseudo-epistola di Agostino scritta da Armando in italiano (anni del Covid) e «ritradotta» da Claude in latino agostiniano; PDF A4 a fronte (latino a sinistra) con `_sorgenti/build.py` da `_sorgenti/testo.txt`. Asterisco solo sul titolo latino. Niente EPUB. NB: non marcare il latino con lang="la": EB Garamond scrive u come v

## Copertine
Tutte nello stesso tratto (fondo #1a1f26, linee avorio sottili, un solo accento rosso #b8322a, Cormorant Garamond), ognuna con un motivo proprio: Ermete = codice aperto con fasi lunari; Redeo = spirale verso il centro; Epistula = due cerchi che si toccano; Tre finestre = finestra. Sorgente `_sorgenti/copertina.html`, render Chrome headless 1600x2400 → `copertina.png`, poi inserita come prima pagina del PDF (PDFKit) quando il PDF viene da Word.

## Pagina iniziale dei PDF
Ogni PDF, subito dopo la copertina, ha la pagina di Finzioni: testo di presentazione, licenza CC BY-SA 4.0, Armando Bisogno, arbisogno@unisa.it. La inserisce `_strumenti/aggiungi_colophon.py <pdf...>` (A4 o A5 in automatico, idempotente), già richiamato dai build di Epistula e Tre finestre; per i PDF da Word (Redeo, Ermete) va lanciato a mano dopo aver messo la copertina.

## Regole
- Ogni testo si apre con la nota con asterisco, agganciata al titolo: «Questo testo è stato integralmente prodotto da Claude Code.» La aggiunge da sola `_strumenti/build_finzione.py`, che va usato per tutti i testi di questa cartella.
- Build: `python3 Finzioni/_strumenti/build_finzione.py <sorgente.txt> <output.docx>` (stessa sintassi di `Ricerca/Paper/_sorgenti/build_paper.py`). Direttive in testa al sorgente: `@disclaimer <testo>` (nota con asterisco diversa da quella standard) e `@formato libro` (16×24 cm, margini a specchio, corpo 10,5: usato per Ermete; senza, impaginazione da paper A4). La copertina va scalata alla pagina (2:3) e `aggiungi_colophon.py` riconosce A4, A5 e 16×24.
- PDF: da Word (AppleScript, salvando nel container `~/Library/Containers/com.microsoft.Word/Data/`).
- Sul sito vanno solo i PDF, mai i .docx, e sempre con la nota con l'asterisco.
- Sito: pagina a sé armandobisogno.it/finzioni/ (`page-finzioni.php`, scura nel colore delle copertine); i libri sono nell'array `ab_finzioni()` in `functions.php` (aggiungere lì una voce + `assets/img/finzioni-<nome>.jpg`). La pagina IA ha solo una fascia che rimanda lì. I link ai PDF hanno `?v=AB_VERSION`: alzare la versione del tema quando cambia un PDF. Il PDF va copiato in `Sito/tema/armando-bisogno/assets/finzioni/`, poi `python3 Sito/deploy.py tema`.

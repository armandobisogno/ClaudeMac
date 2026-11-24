# -*- coding: utf-8 -*-
"""Antologia-lezione: Agostino, Confessiones X-XIII (latino / italiano NBA).

I testi sono estratti alla lettera dal corpus del workspace
(Università/Ricerca/Agostino strumenti/Agostino testi/Opere/_md/34. Confessiones.md):
ogni passo è indicato da riferimento + frasi d'inizio e di fine; se una frase
non si trova, lo script si ferma. Produce l'HTML e il PDF (Chrome headless).

Uso:  python3 build_confessiones_x_xiii.py
"""
import re, html, subprocess, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # ClaudeWS
CORPUS = ROOT / "Università/Ricerca/Agostino strumenti/Agostino testi/Opere/_md/34. Confessiones.md"
OUT_HTML = HERE / "confessiones_x_xiii_antologia.html"
OUT_PDF = HERE.parent / "Agostino - Confessiones X-XIII - antologia-lezione.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ---------------------------------------------------------------- corpus
LA, IT = {}, {}
for line in CORPUS.read_text(encoding="utf-8").split("\n"):
    m = re.match(r"^\[(\d+\.\d+\.\d+)\] (LA|IT): (?:\d+\. )?(?:\d+\. )?(.*)", line)
    if not m:
        continue
    ref, lang, txt = m.groups()
    txt = re.sub(r" ?\[n\d+\]", "", txt)
    txt = re.sub(r" +([.,;:?!])", r"\1", txt)
    txt = txt.replace("?.", "?").replace(" )", ")").replace("( ", "(")
    (LA if lang == "LA" else IT)[ref] = txt.strip()


def cut(txt, segs, ref, lang):
    if not segs:
        return txt
    out = []
    for a, b in segs:
        i = txt.find(a)
        if i < 0:
            sys.exit(f"[{ref} {lang}] inizio non trovato: {a!r}")
        j = txt.find(b, i)
        if j < 0:
            sys.exit(f"[{ref} {lang}] fine non trovata: {b!r}")
        piece = txt[i:j + len(b)]
        if i > 0:
            piece = "[…] " + piece
        if j + len(b) < len(txt) and not piece.rstrip().endswith(("." , "?", "!", "»", '"')):
            piece = piece.rstrip(" ,;:") + " […]"
        out.append(piece)
    s = " ".join(out)
    return s.replace("[…] […]", "[…]")


def esc(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'"([^"]+)"', r"«\1»", s)
    return s


def ref_label(ref):
    b, c, p = ref.split(".")
    return f"conf. {b}, {c}, {p}"


# ---------------------------------------------------------------- contenuti
SECTIONS = []


def S(num, title, books, intro):
    SECTIONS.append(dict(num=num, title=title, books=books, intro=intro, items=[]))


def P(ref, title, k, la=None, it=None):
    SECTIONS[-1]["items"].append(dict(ref=ref, title=title, k=k, la=la, it=it))


S("I", "Confessare chi sono", "X, 1–5",
  "Il libro X si apre con una svolta: i libri precedenti hanno raccontato il passato, ora la confessione riguarda il presente. Prima di cominciare, Agostino si chiede a chi parla, perché, e con quale garanzia di essere creduto.")
P("10.1.1", "Fare la verità",
  "La confessione non è soltanto un dire: la verità si attua («Voglio dunque attuarla dentro al mio cuore»). E ha due scene: «davanti a te nella mia confessione, e nel mio scritto davanti a molti testimoni». Tutto il libro X nasce da questa doppia destinazione.")
P("10.2.2", "Tace la voce, grida il cuore",
  "Dio conosce già tutto: la confessione non lo informa. Tacere non nasconderebbe Agostino a Dio, ma Dio ad Agostino: «Nasconderei te a me, anziché me a te». Il circolo finale fa della confessione un dialogo in cui la parola dell'uomo è già risposta.",
  la=[("Et tibi quidem", "non me tibi."), ("Confessio itaque mea", "prius dixeris.")],
  it=[("A te, Signore", "anziché me a te."), ("Quindi la mia confessione", "detto tu stesso.")])
P("10.3.3", "Una gente curiosa",
  "Il primo pubblico è una «gente curiosa di conoscere la vita altrui, ma infingarda nel correggere la propria». Agostino non può dimostrare di dire il vero; l'unica garanzia è la carità di chi legge: «quelli, cui la carità apre le orecchie alla mia voce, mi credono». Un patto di lettura, non una prova.",
  la=[("Quid mihi ergo est", "qui sint?"), ("Sed quia caritas", "caritas aperit.")],
  it=[("Ma cos'ho da spartire", "chi sono essi?"), ("Ma poiché la carità crede tutto", "mi credono.")])
P("10.3.4", "Non chi fui, ma chi sono",
  "È la soglia del libro. Il frutto delle confessioni del passato è chiaro: chi legge non dispera, non dice «Non posso». Ora si confessa «il mio stato presente, non più il passato»; ma il presente sta nel cuore, dove l'orecchio dei lettori non arriva.",
  la=[("Quo itaque fructu", "quicumque sum.")],
  it=[("Con quale frutto dunque, Signore mio", "ove io sono comunque sono.")])
P("10.5.7", "So qualcosa di te che di me ignoro",
  "Il paradosso che regge il libro: «sono più vicino a me, che a te», eppure «so qualcosa di te, che di me ignoro». La confessione comprende anche ciò che di sé non si sa: è l'annuncio delle domande che seguono.",
  la=[("Ego vero quamvis", "quibusve non valeam nescio."), ("Confitear ergo", "in vultu tuo.")],
  it=[("Anch'io, per quanto", "a quali no."), ("Confesserò dunque", "nel tuo volto.")])

S("II", "Nei palazzi della memoria", "X, 6–27",
  "La domanda «Ma che amo, quando amo te?» avvia una salita: il mondo, il corpo, i sensi, e infine la memoria, percorsa come uno spazio immenso. In cima alla salita si scopre che la memoria è l'io stesso, e che Dio vi abita senza esserne parte.")
P("10.6.8", "Che cosa amo, quando amo te?",
  "La risposta usa i sensi due volte: prima per negarli (non la luce, non le melodie, non la fragranza…), poi per riprenderli come sensi «dell'uomo interiore». Le relative finali tolgono a ogni sensazione ciò che la rende passeggera: «una luce non avvolta dallo spazio», «una voce non travolta dal tempo».",
  la=[("Quid autem amo, cum te amo?", "Hoc est quod amo, cum Deum meum amo.")],
  it=[("Ma che amo, quando amo te?", "Ciò amo, quando amo il mio Dio.")])
P("10.6.9", "Interrogai la terra",
  "«Le mie domande erano la mia contemplazione; le loro risposte, la loro bellezza»: interrogare il mondo è guardarlo, e il mondo risponde con la sua bellezza, rimandando oltre sé. Esaurito l'esterno, la domanda si rivolge a chi domanda: «Tu, chi sei?».",
  la=[("Interrogavi terram", 'Et respondi: "Homo".')],
  it=[("Interrogai la terra", 'e risposi: "Un uomo".')])
P("10.8.12", "I campi e i vasti quartieri della memoria",
  "Le immagini sono spaziali (campi, quartieri, tesori, ripostigli) e insieme drammatiche: i ricordi si fanno avanti da soli e vanno scacciati «con la mano dello spirito». L'ultima frase dice a che cosa serve tutto questo: «Tutto ciò avviene, quando faccio un racconto a memoria». I nove libri precedenti sono stati un'opera della memoria.")
P("10.8.14", "Là incontro anche me stesso",
  "Nella memoria non ci sono soltanto le cose: «Là incontro anche me stesso». E dalla memoria si costruisce anche il futuro, pensato «come a cose presenti»: un'anticipazione del libro XI (11,18,23; 11,20,26).",
  la=[("Intus haec ago", "affectus fuerim."), ("Ex eadem copia", "quasi praesentia meditor.")],
  it=[("Sono tutte azioni", "compiendoli."), ("Dalla stessa, copiosa riserva", "come a cose presenti.")])
P("10.8.15", "Grande è questa potenza della memoria",
  "Il centro del libro: la memoria appartiene allo spirito, eppure lo spirito non la contiene: «io non riesco a comprendere tutto ciò che sono». La meraviglia cambia oggetto: gli uomini ammirano le vette dei monti e le onde del mare, «mentre trascurano se stessi».")
P("10.10.17", "Da dove sono entrate?",
  "Le nozioni delle discipline non sono entrate da nessuna porta dei sensi. Agostino non le ha imparate da altri, le ha riconosciute in sé, dicendo «È così, è vero». Imparare, qui, è ritrovare ciò che era già nella memoria, «in cavità più segrete».",
  la=[("Unde et qua haec intraverunt", "cogitare non possem?")],
  it=[("Da dove, dunque, e per dove", "che le estraesse?")])
P("10.11.18", "Cogitare, cogere",
  "Pensare è raccogliere ciò che nella memoria giace disperso: di qui la parentela tra cogito e cogo. L'etimologia non è un ornamento: il pensiero è un atto di unificazione. Il tema torna nella continenza che «ci raccoglie» (10,29,40) e nella vita dispersa nei tempi del libro XI (11,29,39).")
P("10.16.25", "Un terreno aspro",
  "Davanti al paradosso dell'oblio (come si ricorda la dimenticanza?) chi indaga diventa il campo dell'indagine: «Sono diventato per me un terreno aspro». Non si scrutano le regioni celesti: «c'è nulla più vicino a me di me stesso?», eppure proprio questo sfugge.",
  la=[("Ego certe, Domine, laboro hic", "praeter illam.")],
  it=[("Io, Signore, certamente mi arrovello", "neppure me stesso.")])
P("10.17.26", "Che cosa sono dunque?",
  "«E ciò è lo spirito, e ciò sono io stesso»: la memoria non è uno strumento che l'io possiede, è l'io. Per questo superarla è un problema. Dio va cercato oltre la memoria, ma «neppure potrei trovarti, se non avessi ricordo di te».",
  la=[("Magna vis est memoriae, nescio quid horrendum", "immensa vehementer."), ("Transibo ergo et memoriam, ut attingam", "si memor non sum tui?")],
  it=[("La facoltà della memoria è grandiosa", "di un'immensità poderosa."), ("Supererò, dunque, anche la memoria", "se non avessi ricordo di te.")])
P("10.20.29", "Cercare Dio è cercare la felicità",
  "La ricerca di Dio diventa ricerca della felicità: tutti la vogliono, dunque tutti ne hanno una qualche nozione. La parola è greca o latina, la cosa no: «la cosa in se stessa non è greca né latina». La domanda resta aperta: in che modo la felicità si trova nella memoria?",
  la=[("Quomodo ergo te quaero", "ut amarent eam?"), ("Audimus nomen hoc", "memoria teneretur.")],
  it=[("Come ti cerco dunque", "dove la videro per amarla?"), ("All'udirne il nome", "non si conservasse nella memoria.")])
P("10.23.33", "Il godimento della verità",
  "La risposta: «la felicità della vita è il godimento della verità». L'argomento è semplice e forte: «Ho conosciuto molte persone desiderose di ingannare; nessuna di essere ingannata». Il desiderio di verità è universale quanto quello di felicità.",
  la=[("Nam quaero ab omnibus", "qui autem falli, neminem.")],
  it=[("Chiedo a tutti", "nessuna di essere ingannata.")])
P("10.23.34", "La verità che splende, la verità che riprende",
  "Si ama la verità finché illumina, la si odia quando accusa: «L'amano quando splende, l'odiano quando riprende». Chi ama altro pretende che ciò che ama sia la verità. La pena è simmetrica: «non rimane lui occulto alla verità, ma la verità rimane occulta a lui».",
  la=[("Cur autem veritas parit odium", "ipsum autem veritas lateat.")],
  it=[("Ma perché la verità genera odio", "la verità rimane occulta a lui.")])
P("10.26.37", "In te, sopra di me",
  "Dio non era nella memoria prima di essere conosciuto: è stato trovato «in te, sopra di me». La verità risponde a tutti; la differenza sta nell'ascolto. La chiusa è un'etica dell'interrogare: il servo migliore mira «a volere piuttosto ciò che da te ode».")
P("10.27.38", "Tardi ti amai",
  "Il culmine del libro, costruito su due antitesi («tu eri dentro di me e io fuori»; «Eri con me, e non ero con te») e su cinque verbi che restituiscono, convertiti, i sensi di 10,6,8: chiamasti, balenasti, diffondesti la tua fragranza, gustai, mi toccasti. La bellezza «così antica e così nuova» non è una scoperta, ma un riconoscimento.")

S("III", "Un problema per me stesso: le tentazioni", "X, 28–43",
  "Dopo la memoria, l'esame del presente: le tentazioni che ancora assalgono il vescovo, distinte in tre forme (la concupiscenza della carne, la vana curiosità, l'orgoglio). Ne esce il ritratto di un uomo che non sa ancora fino in fondo chi è.")
P("10.29.40", "Dà ciò che comandi",
  "Tutta la speranza è nella misericordia: «Dà ciò che comandi e comanda ciò che vuoi», formula che ritorna più volte nel libro (10,31,45; 10,37,60). La continenza non è solo rinuncia: «ci raccoglie e riconduce a quell'unità che abbiamo lasciato disperdendoci nel molteplice». Ancora il lessico del raccogliere (10,11,18).")
P("10.30.41", "Non sono forse più io?",
  "Le immagini del passato sopravvivono «nella mia memoria, di cui ho parlato a lungo», e nel sonno tornano con forza. Chi è il soggetto del sogno? «In quei momenti, Signore Dio mio, non sono forse più io?». La domanda morale diventa una domanda sull'identità.",
  la=[("Sed adhuc vivunt in memoria mea", "Numquid tunc ego non sum, Domine Deus meus?")],
  it=[("Sopravvivono però nella mia memoria", "non sono forse più io?")])
P("10.33.50", "Il canto in chiesa",
  "Sul canto Agostino oscilla («Così ondeggio fra il pericolo del piacere e la constatazione dei suoi effetti salutari») e non emette una sentenza definitiva. La chiusa riassume il libro: «Sono diventato per me sotto i tuoi occhi un problema». Già alla morte dell'amico, nel libro IV, aveva scritto: «Factus eram ipse mihi magna quaestio» (4,4,9).",
  la=[("Verumtamen cum reminiscor lacrimas meas", "assurgat."), ("Tu autem, Domine Deus meus, exaudi", "languor meus.")],
  it=[("Quando però mi tornano alla mente", "attraverso il diletto delle orecchie."), ("E tu, Signore Dio mio, esaudiscimi", "la mia debolezza.")])
P("10.35.54", "La concupiscenza degli occhi",
  "La curiosità non cerca il compiacimento della carne, ma «l'esperienza mediante la carne», ed è «ammantata del nome di cognizione e di scienza». Si chiama concupiscenza degli occhi perché la vista è il senso del conoscere: per ogni senso si dice «Vedi». Il primato del vedere è iscritto nella lingua.",
  la=[("Huc accedit", "palliata."), ("Neque enim dicimus", "videri enim dicuntur haec omnia.")],
  it=[("S'aggiunge un'altra forma", "cognizione e di scienza."), ("Non diciamo:", 'si dice sempre: "Vedi".')])
P("10.35.55", "Il cadavere dilaniato",
  "Il piacere cerca il bello; la curiosità cerca anche ciò che ripugna, solo per sapere: l'esempio del cadavere. Dalla stessa radice Agostino fa discendere gli spettacoli, le arti magiche, la richiesta di segni, e l'esplorazione della natura, «la cui conoscenza è per nulla utile».",
  la=[("Quid enim voluptatis", "persuaserit."), ("Ex hoc morbo cupiditatis", "nihil aliud quam scire homines cupiunt.")],
  it=[("Cos'ha di piacevole", "uno spettacolo ameno."), ("Da questa perversione", "null'altro che il conoscere;")])
P("10.35.57", "La lepre, la tarantola, il ragno",
  "La curiosità non abita solo i grandi spettacoli: un cane dietro una lepre, una tarantola che cattura le mosche, un ragno che avvolge gli insetti. La confessione del presente scende fino al minimo, e trova una regola: «Altro è l'alzarsi prontamente, altro il non cadere».",
  la=[("Canem currentem", "non cadere.")],
  it=[("Se non assisto più", "altro il non cadere.")])
P("10.37.60", "Un crogiuolo quotidiano",
  "La terza tentazione è la più difficile da esplorare: «Nelle altre specie di tentazioni riesco in una certa misura a esplorarmi; in questa quasi nulla». Dalle altre ci si mette alla prova privandosene; dalla lode no, a meno di vivere male di proposito. «Un crogiuolo quotidiano è per noi la lingua degli uomini».",
  la=[("Temptamur his temptationibus", "in hoc paene nulla est."), ("Laude vero ut careamus", "dici aut cogitari potest?")],
  it=[("Queste le tentazioni", "in questa quasi nulla."), ("La lode invece", "follia maggiore?")])
P("10.40.65", "Ove valgo, non voglio stare",
  "Il bilancio del libro: un sentimento «del tutto sconosciuto e indefinibilmente dolce» che, compiuto, «sarà non so cosa, che non sarà questa vita»; poi la ricaduta sotto «il fardello dell'abitudine». Il chiasmo finale dice la condizione del convertito: «Ove valgo, non voglio stare; ove voglio, non valgo».",
  la=[("Et aliquando intromittis me", "miser utrubique.")],
  it=[("Talvolta m'introduci", "qui e là sto infelice.")])
P("10.43.70", "La fuga impedita",
  "Il libro si chiude con una confessione inattesa: il progetto di «una fuga nella solitudine», impedito dalla parola dell'Apostolo. E indica il passaggio ai libri seguenti: «contemplerò le meraviglie della tua legge». Dalla confessione di sé si passa alla Scrittura (11,2,2).",
  la=[("Conterritus peccatis meis", "considerabo mirabilia de lege tua.")],
  it=[("Atterrito dai miei peccati", "le meraviglie della tua legge.")])

S("IV", "Che cos'è il tempo?", "XI",
  "Il libro XI commenta il primo versetto della Genesi, «In principio Dio creò il cielo e la terra». Da un'obiezione nasce l'indagine sul tempo: dal tempo delle cose al tempo dell'animo, fino alla vita intera come distensione.")
P("11.1.1", "Per amore del tuo amore",
  "La domanda torna all'inizio del nuovo libro: perché raccontare a chi sa già? Non perché Dio apprenda, ma per eccitare l'amore «in me e in chi li leggerà». E la prima frase contiene già il tema: Dio, eterno, vede «per il tempo ciò che avviene nel tempo»?",
  la=[("Numquid, Domine", "amore amoris tui facio istuc.")],
  it=[("Ignori forse", "m'induco a tanto.")])
P("11.2.2", "Le gocce del tempo",
  "Il vescovo non ha tempo per raccontare tutto: «troppo preziose per me sono le gocce del tempo». Il desiderio è ora un altro: «meditare la tua legge, di confessarti la mia conoscenza e la mia ignoranza in proposito». È il programma dei libri XI–XIII, annunciato alla fine del libro X (10,43,70).",
  la=[("Et si sufficio", "a fortitudine infirmitas.")],
  it=[("Se anche riuscissi", "inghiottita dalla tua forza.")])
P("11.3.5", "Se Mosè fosse qui",
  "Mosè non si può interrogare. E anche se si potesse, la sua voce darebbe le parole, non la verità: questa parla dentro, «non ebraica né greca né latina né barbara». Il problema della lettura è posto, e tornerà in tutto il libro XII (12,25,35).",
  la=[("Audiam et intellegam", '"Verum dicis".')],
  it=[("Fammi udire e capire", '"Dici il vero".')])
P("11.10.12", "Che cosa faceva Dio prima?",
  "L'obiezione è seria, e Agostino la riporta per intero: se Dio ha cominciato a creare, la sua volontà è cambiata; se lo ha voluto da sempre, perché la creatura non è eterna? Da qui nasce l'indagine sul tempo.")
P("11.12.14", "Non so ciò che non so",
  "Rifiuta la battuta di «quel tale»: «Altro è capire, altro è schernire». Meglio rispondere «Non so ciò che non so». Poi la risposta vera: prima del cielo e della terra Dio non faceva nulla, perché fare, per Dio, significa creare.",
  la=[("Respondeo non illud", 'non faciebat aliquid".')],
  it=[("Non rispondo come quel tale", 'non faceva alcunché".')])
P("11.13.15", "Non esisteva un allora",
  "Il tempo è creato insieme al mondo: «non poterono trascorrere tempi prima che tu avessi creato un tempo». La domanda è mal posta, perché proietta il tempo oltre i suoi confini: «Non esisteva un allora dove non esisteva un tempo».",
  la=[("Id ipsum enim tempus", "ubi non erat tempus.")],
  it=[("Anche quel tempo era opera tua", "dove non esisteva un tempo.")])
P("11.13.16", "Il tuo oggi è l'eternità",
  "L'eternità non è un tempo lunghissimo, ma un presente che non passa: «Il tuo oggi è l'eternità». I nostri anni «vanno e vengono»; quelli di Dio «sono tutti insieme, perché sono stabili».",
  la=[("Anni tui dies unus", "nec aliquo tempore non erat tempus.")],
  it=[("I tuoi anni sono un giorno solo", "non vi era tempo.")])
P("11.14.17", "Se nessuno m'interroga, lo so",
  "La frase più nota del libro: «Se nessuno m'interroga, lo so; se volessi spiegarlo a chi m'interroga, non lo so». Poi il paradosso: il passato non è più, il futuro non è ancora, il presente è soltanto in quanto passa. Il tempo è, «in quanto tende a non esistere».",
  la=[("Quid est ergo tempus?", "nisi quia tendit non esse?")],
  it=[("Cos'è dunque il tempo?", "se non in quanto tende a non esistere.")])
P("11.15.20", "Il presente senza estensione",
  "La riduzione progressiva (cento anni, un anno, un mese, un giorno, un'ora) porta a un presente puntuale: «il presente non ha nessuna estensione». Ma allora come possiamo dire che un tempo è lungo?",
  la=[("Si quid intellegitur temporis", "praesens autem nullum habet spatium.")],
  it=[("Solo se si concepisce", "il presente non ha nessuna estensione.")])
P("11.18.23", "La mia infanzia, che non è più",
  "Il passato si racconta attraverso immagini rimaste nell'animo, «quasi orme». L'esempio è la propria infanzia, quella del libro I: «quando la rievoco e ne parlo, vedo la sua immagine nel tempo presente». Il libro XI dà la ragione del racconto che i libri I–IX hanno compiuto.",
  la=[("Quamquam praeterita cum vera narrantur", "quia est adhuc in memoria mea.")],
  it=[("Nel narrare fatti veri del passato", "nella mia memoria.")])
P("11.20.26", "Tre presenti",
  "La soluzione: non tre tempi, ma tre presenti nell'animo: «il presente del passato è la memoria, il presente del presente la visione, il presente del futuro l'attesa». L'uso comune si può tenere, «purché si comprenda ciò che si dice».")
P("11.23.30", "Il sole fermo",
  "Il tempo non è il moto degli astri: quando il sole si fermò per la battaglia, «il sole era fermo, ma il tempo procedeva». Il tempo è dunque «in qualche modo un'estensione». E subito il dubbio: «Ma vedo veramente, o mi vedo vedere?».",
  la=[("Nemo ergo mihi dicat", "Tu demonstrabis, Lux, Veritas.")],
  it=[("Dunque non mi si dica", "o Luce, o Verità.")])
P("11.26.33", "Un'estensione dello spirito",
  "La misura del tempo non può essere esterna: un verso breve, pronunciato lentamente, dura più di uno lungo pronunciato in fretta. Il tempo è un'estensione (distentio), e «sarebbe sorprendente, se non fosse un'estensione dello spirito stesso».",
  la=[("An tempore breviore", "non ipsius animi.")],
  it=[("Si misura un tempo più lungo", "un'estensione dello spirito stesso.")])
P("11.27.36", "È in te, spirito mio, che misuro il tempo",
  "Ciò che si misura è l'impressione che le cose lasciano passando: «è quanto misuro, allorché misuro il tempo». E lo spirito non è passivo: «La tensione presente fa passare il futuro in passato».",
  la=[("In te, anime meus", "aut non tempora metior."), ("dum praesens intentio", "sit totum praeteritum.")],
  it=[("È in te, spirito mio", "o non è il tempo che misuro."), ("La tensione presente", "tutto non è che passato.")])
P("11.28.37", "Attesa, attenzione, memoria",
  "Il futuro non esiste, ma «esiste già nello spirito l'attesa del futuro»; il passato non esiste, ma esiste la memoria; il presente non ha estensione, ma «perdura l'attenzione». Attesa, attenzione, memoria: il tempo ricondotto allo spirito.")
P("11.28.38", "La canzone, la vita, la storia",
  "L'esempio decisivo: cantare una canzone che si conosce. L'attesa si accorcia, la memoria si allunga, l'attenzione fa passare il futuro nel passato. Poi la scala si dilata: le sillabe, la canzone, un'azione più lunga, «l'intera vita dell'uomo», «l'intera storia dei figli degli uomini». La stessa struttura regge il racconto dei libri I–IX.")
P("11.29.39", "Non disteso, ma proteso",
  "La teoria diventa preghiera. La vita come distensione è dispersione: «Io mi sono schiantato sui tempi». Contro di essa una direzione: «non disteso, ma proteso, non con distensione, ma con tensione». Il tempo non si elimina, si orienta.")
P("11.31.41", "Come io conosco una canzone",
  "Torna la canzone: uno spirito che conoscesse passato e futuro come io «una canzone delle più conosciute» desterebbe meraviglia. Ma Dio conosce altrimenti, «assai più mirabilmente e assai più misteriosamente»: senza attesa né ricordo, e crea «senza tensione della tua attività».",
  la=[("Certe si est tam grandi", "sine distentione actionis tuae.")],
  it=[("Certo, se esistesse uno spirito", "senza tensione della tua attività.")])

S("V", "Leggere il principio", "XII",
  "Il libro XII interpreta «il cielo e la terra» del primo versetto: il cielo del cielo e la materia informe. Ma il tema vero diventa la lettura stessa: che cosa voleva dire Mosè, e che cosa fare quando gli interpreti non sono d'accordo.")
P("12.1.1", "La ricerca è più loquace del ritrovamento",
  "Un'osservazione di metodo apre il libro: «la ricerca è più loquace del ritrovamento». Il libro XII sarà lungo per questo: è un libro di ricerca, non di risultati, e si chiude ammettendolo: «quante cose ho scritto per poche parole» (12,32,43).",
  la=[("Multa satagit cor meum", "quam sumens.")],
  it=[("Quante cose vorrebbe sapere", "che a prendere.")])
P("12.6.6", "Un informe quasi nulla",
  "Agostino racconta la storia del proprio concetto di materia: prima la immaginava fatta di forme sgradevoli e orrende; poi capì che bisognava pensare «una cosa a mezzo tra la forma e il nulla». La materia è la mutevolezza stessa delle cose: «Se si potesse parlare di un nulla esistente o di un essere inesistente, così ne parlerei».",
  la=[("verum autem illud quod cogitabam", "informe prope nihil."), ("Mutabilitas enim rerum", "species caperet istas visibiles et compositas.")],
  it=[("però le immagini della mia mente", "un informe quasi nulla."), ("È insomma la stessa mutevolezza", "gli aspetti visibili e complessi del mondo.")])
P("12.7.7", "L'una prossima a te, l'altra prossima al nulla",
  "La creazione dal nulla: non dalla sostanza di Dio, che renderebbe la creatura uguale al Figlio; non da altro, perché «fuori di te non esisteva nulla». Ne risulta una polarità: due creature, «l'una prossima a te, l'altra prossima al nulla».",
  la=[("Fecisti enim caelum et terram non de te", "inferius nihil esset.")],
  it=[("Hai creato il cielo e la terra, ma non traendoli", "sotto di sé ha il nulla.")])
P("12.18.27", "Che male è?",
  "Il principio del libro: chi legge cerca l'intenzione dell'autore; ma se vi scopre un senso vero che l'autore non intendeva, «che male è»? Il criterio è la verità, il fine è la carità: la pluralità delle interpretazioni non è un incidente da eliminare.",
  la=[("Quibus omnibus auditis", "Prophetasque suspenderit."), ("Omnes quidem, qui legimus", "nec tamen hoc senserit?")],
  it=[("Ho ascoltato e considerato", "la legge e i profeti."), ("Chiunque di noi legge", "un'intenzione diversa da questa.")])
P("12.23.32", "Due specie di dissenso",
  "Una distinzione capitale: si può discutere «sulla verità dei fatti» o «sull'intenzione del messaggero». Sono due domande diverse, con criteri diversi. Agostino cerca la compagnia di chi si nutre della verità «nell'ampiezza della carità».",
  la=[("His ergo auditis", "dispensasti ea.")],
  it=[("Ascolto queste opinioni", "le hai elargite.")])
P("12.25.34", "La tua verità non appartiene né a me né ad altri",
  "Il passo più alto del libro. Gli interpreti litigiosi «amano la loro, non perché sia vera, ma perché è la loro». La verità invece è «un bene comune di tutti gli amanti della verità», e l'avvertimento è «di non pretenderne il possesso privato per non esserne privati». «Chi infatti dice una menzogna, dice del suo»: il proprio è la menzogna, la verità è di tutti.",
  la=[("qui non mihi hoc dicunt", "de suo loquitur.")],
  it=[("che ciò mi dicono non già", "dice del suo.")])
P("12.25.35", "Dove la vediamo?",
  "Due interpreti che vedono entrambi il vero non lo vedono l'uno nell'altro, ma «nella verità immutabile, che sta sopra le nostre intelligenze». Il pensiero di Mosè, invece, non lo vediamo: «lo crederemmo senza vederlo». Si torna a 11,3,5.",
  la=[("si ambo videmus verum esse", "sed crederemus?")],
  it=[("Se entrambi vediamo", "lo crederemmo senza vederlo.")])
P("12.26.36", "Se fossi stato Mosè",
  "Un esperimento: se Agostino avesse dovuto scrivere la Genesi, avrebbe voluto uno stile che non respingesse chi non sa ancora comprendere, e nel quale chi comprende ritrovasse ogni opinione vera. È una teoria della scrittura: poche parole, molti sensi.",
  la=[("Vellem quippe", "intellegenda deesset.")],
  it=[("Ebbene io avrei voluto", "riconoscibili nelle medesime parole.")])
P("12.29.40", "Il suono e il canto",
  "Quattro modi di precedere: per l'eternità, per il tempo, per il valore, per l'origine. La materia precede la forma come il suono precede il canto: non nel tempo, perché «il suono viene emesso contemporaneamente al canto», ma perché «il suono riceve forma per essere canto». Ancora il canto, come nel libro XI (11,28,38).",
  la=[("Cum vero dicit primo informem", "origine, sicut sonus cantum."), ("Sed prior est origine", "ut cantus sit.")],
  it=[("Se invece dice che prima", "il suono precede il canto."), ("bensì per una precedenza di origine", "per essere canto.")])
P("12.31.42", "Perché non ambedue?",
  "La conclusione: «Perché non piuttosto ambedue, se ambedue sono vere?». E un ideale di scrittura: far echeggiare «tutte le verità che ognuno potesse cogliere in quella materia», anziché un solo pensiero a esclusione degli altri.",
  la=[("Ita cum alius dixerit", "me non posset offendere.")],
  it=[("Così, quando uno dice", "non mi urtassero con la loro falsità.")])

S("VI", "La creazione come racconto, fino al riposo", "XIII",
  "L'ultimo libro rilegge le opere dei sei giorni come figure: la luce, il firmamento, le acque, gli astri, gli animali diventano la storia della Chiesa e dell'anima. Al centro, l'amore come peso; alla fine, il settimo giorno «senza tramonto».")
P("13.1.1", "Non hai dimenticato chi ti ha dimenticato",
  "L'ultimo libro si apre con un'invocazione, come il primo. Dio ha preceduto ogni chiamata, e «non hai dimenticato chi ti ha dimenticato». Il tema è la gratuità: la creazione non è meritata, come non lo è la conversione.",
  la=[("Invoco te, Deus meus", "vocantem me invocarem te.")],
  it=[("T'invoco, Dio mio", "te che mi richiamavi.")])
P("13.4.5", "Per pienezza di bontà",
  "Dio non crea per bisogno: «Tu non le hai create per bisogno, ma per pienezza di bontà». È la risposta più profonda alla domanda del libro XI (11,10,12): la creazione non aggiunge nulla a Dio.",
  la=[("Quid ergo tibi deesset", "compleatur ex eis?")],
  it=[("Cosa mancherebbe dunque", "per completarne la tua gioia.")])
P("13.8.9", "Dammi te stesso",
  "Nel mezzo dell'esegesi, la preghiera più nuda: «Dammi te stesso, Dio mio». Niente che sia meno di Dio basta alla creatura razionale, nemmeno se stessa: «ogni mia ricchezza, se non è il mio Dio, è povertà».",
  la=[("Da mihi te, Deus meus", "egestas est.")],
  it=[("Dammi te stesso", "è povertà.")])
P("13.9.10", "Il mio peso è il mio amore",
  "I corpi tendono al loro luogo: il fuoco verso l'alto, la pietra verso il basso, l'olio sopra l'acqua. Così l'uomo: «Il mio peso è il mio amore; esso mi porta dovunque mi porto». E la legge è generale: «Fuori dell'ordine regna l'inquietudine, nell'ordine la quiete».",
  la=[("In dono tuo requiescimus", "permanere illic in aeternum.")],
  it=[("Di lui solo fu detto", "di rimanervi in eterno.")])
P("13.11.12", "Esistere, conoscere, volere",
  "Un esercizio dentro di sé: esistere, conoscere, volere, distinti e inseparabili. Agostino ne indica subito il limite: sono cose «ben diverse dalla Trinità», servono a misurare la distanza. E l'invito è rivolto al lettore: «guardi in se stesso, veda e mi risponda».",
  la=[("Vellem, ut haec tria", "et dicat mihi.")],
  it=[("Vorrei invitare gli uomini", "veda e mi risponda.")])
P("13.15.16", "Il firmamento del Libro",
  "Il firmamento è figura della Scrittura, distesa sopra di noi «come pelle di tenda». Le pelli ricordano la mortalità; e l'autorità della Scrittura cresce con la morte dei suoi autori: il libro sopravvive a chi lo ha scritto.")
P("13.15.18", "Leggono, eleggono e prediligono",
  "Gli angeli non hanno bisogno del libro: leggono nel volto di Dio «senza sillabe distribuite nel tempo», e la loro lettura è insieme scelta e amore. Noi leggiamo nel tempo, sillaba dopo sillaba, come nella canzone del libro XI (11,28,38).",
  la=[("Laudent nomen tuum", "et es in aeternum,")],
  it=[("Lodino il tuo nome", "e lo sei in eterno;")])
P("13.24.36", "Crescete e moltiplicatevi",
  "Perché la benedizione «Crescete e moltiplicatevi» è data solo ai pesci e agli uomini? Agostino la legge come benedizione dei segni e delle interpretazioni: un'idea si esprime in molti modi, una frase si intende in molti modi veri. Il principio del libro XII diventa benedizione.",
  la=[("Novi enim multipliciter", "fetus hominum.")],
  it=[("È chiaro che un'idea", "i germi degli uomini.")])
P("13.24.37", "La facoltà e la potestà",
  "La formula conclusiva: ci è data «la facoltà e la potestà di esprimere in molti modi un unico concetto che abbiamo acquisito, e di concepire in molti modi un'unica espressione oscura che abbiamo letto». È l'approdo della riflessione sulla lettura cominciata nel libro XI (11,3,5).",
  la=[("In hac enim benedictione", "enuntiatum legerimus.")],
  it=[("Con questa benedizione", "che abbiamo letto.")])
P("13.28.43", "Buone assai",
  "Sette volte la Scrittura dice che l'opera è buona; l'ottava, guardandole tutte, «non solo buone, ma anche assai buone». Le singole cose sono buone, l'insieme lo è di più, come un corpo bello rispetto alle sue membra. È la risposta, alla fine dell'opera, alla domanda sul male del libro VII.",
  la=[("Septiens numeravi", "pulchra sint.")],
  it=[("Sette volte ho calcolato", "singolarmente, belle.")])
P("13.31.46", "Sei tu che vedi in loro",
  "Tre modi di guardare il creato: chi lo giudica cattivo (gli uomini cui «le tue opere dispiacciono», 13,30,45), chi lo vede buono ma preferisce «godere di essa, che di te», chi lo vede buono nello Spirito, e allora è Dio che vede in lui: «sei tu che vedi in loro».",
  la=[("Qui autem per spiritum tuum", "tibi placent in nobis."), ("aliud autem, ut, cum aliquid videt homo", "sed quod est est.")],
  it=[("Quanti invece vedono le tue opere", "piace a te in noi."), ("E c'è l'uomo che vede", "ma è Colui che è.")])
P("13.35.50", "La pace senza tramonto",
  "Anche le opere «buone assai» passeranno: «Esse ebbero un mattino, e una sera». L'opera si avvia alla fine chiedendo la pace del sabato, «la pace senza tramonto».")
P("13.36.51", "Il settimo giorno",
  "Il settimo giorno non ha sera: «è senza tramonto e non ha occaso». È la promessa del riposo: «nel sabato della vita eterna riposeremo in te». Il riposo finale risponde all'inquietudine dell'inizio.")
P("13.37.52", "Operi sempre e riposi sempre",
  "Anche il riposo sarà di Dio in noi, come ora le opere: «Sarà, quello, un riposo tuo per mezzo nostro». Dio opera sempre e riposa sempre, e compie «il tempo stesso e il riposo dopo il tempo»: il libro XI torna, condensato, alla fine.")
P("13.38.53", "Chiediamo a te, cerchiamo in te, bussiamo da te",
  "«Noi vediamo dunque la tua creazione perché esiste; ma essa esiste perché tu la vedi». L'ultima parola riprende l'inizio del libro XII (12,1,1): chiedere, cercare, bussare. L'opera non si chiude con un sapere, ma con una ricerca che attende risposta.")

# ---------------------------------------------------------------- copertina
COVER = """
<div class="cover">
  <div class="kicker">Lettura e critica del testo filosofico medievale · Prof. Armando Bisogno · a.a. 2026/2027</div>
  <h1>Agostino, <em>Confessiones</em> X–XIII</h1>
  <div class="sub">Memoria, tempo, Scrittura, creazione: un percorso di lettura</div>

  <div class="cols">
    <h3>L'opera</h3>
    <p>Le <i>Confessiones</i> sono scritte tra il 397 e il 401/403, nei primi anni dell'episcopato di Agostino a Ippona. Sono tredici libri, ciascuno in forma di discorso rivolto a Dio. La confessione vi ha tre volti, che il testo tiene sempre insieme: confessione delle colpe, professione di fede, lode. Agostino stesso, rileggendo l'opera alla fine della vita, ne descrive la struttura: i primi dieci libri parlano di lui, gli ultimi tre delle Scritture, dall'inizio della Genesi «fino al riposo del sabato».</p>

    <h3>Gli ultimi quattro libri</h3>
    <p><b>X</b>: dal passato al presente. Chi sono ora? La ricerca di Dio attraversa la memoria, la felicità, le tentazioni. <b>XI</b>: il primo versetto della Genesi; la Parola, l'eternità, il tempo come estensione dello spirito. <b>XII</b>: il cielo del cielo e la materia informe; la pluralità delle interpretazioni vere. <b>XIII</b>: le opere dei sei giorni lette come figure della Chiesa e dell'anima; l'amore come peso; il settimo giorno.</p>

    <h3>Il problema dell'unità</h3>
    <p>Il racconto si chiude nel libro IX, con la morte di Monica. Gli ultimi quattro libri sembrano un'altra opera: meno racconto, più indagine ed esegesi. Perché stanno insieme? I testi suggeriscono una risposta. Chi ha confessato ciò che è stato si chiede ciò che è ora (X); scopre che il suo «io» è memoria e tempo (X–XI); e trova nella lettura della Scrittura (XII–XIII) il luogo in cui la propria storia si iscrive in quella della creazione. Il racconto di sé diventa racconto del mondo.</p>

    <h3>I fili del percorso</h3>
    <p>Il percorso segue il testo nell'ordine e si regge su alcuni fili che attraversano i quattro libri: la <b>memoria</b> e il racconto (X–XI); il <b>tempo</b> e il canto (XI–XII); la <b>lettura</b> e i molti sensi di un testo (XI–XIII); la <b>dispersione</b> e il raccoglimento, l'<b>inquietudine</b> e il riposo (X–XIII). Le chiavi di lettura rinviano da un passo all'altro, senza uscire dalle <i>Confessioni</i>.</p>
  </div>

  <div class="box">
    <p><b>Come è costruita l'antologia.</b> I passi sono raccolti in sei percorsi, nell'ordine del testo. Per ciascuno: il latino a sinistra, la traduzione italiana a destra, una chiave di lettura. I tagli interni sono segnalati con […]. Testo latino e traduzione italiana sono quelli della Nuova Biblioteca Agostiniana (www.augustinus.it), come raccolti nel corpus agostiniano di lavoro; anche le citazioni nelle chiavi sono tratte, alla lettera, da quella traduzione. I riferimenti indicano libro, capitolo e paragrafo.</p>
  </div>
</div>
"""

QUESTIONS = """
<div class="box final">
  <p><b>Per la discussione in aula</b></p>
  <ol class="q">
    <li>Il libro X parla ancora di Agostino, i libri XI–XIII parlano della Scrittura. Ma memoria, tempo e lettura attraversano tutti e quattro: dove passa davvero il confine, e che cosa tiene insieme le due parti dell'opera?</li>
    <li>Memoria (X) e tempo (XI): in che senso il tempo come estensione dello spirito spiega come si racconta la propria vita? (10,8,14; 11,18,23; 11,28,38)</li>
    <li>Il canto ritorna in tutti i libri: in chiesa (10,33,50), nella misura del tempo (11,28,38), nel rapporto tra materia e forma (12,29,40), fino alla lettura senza sillabe degli angeli (13,15,18). Perché proprio il canto come modello?</li>
    <li>La verità «bene comune» (12,25,34) e i molti sensi di un testo (12,31,42; 13,24,37): il pluralismo di Agostino ha dei limiti? Che ruolo ha la carità come criterio?</li>
    <li>La curiosità (10,35,54-57): condanna della ricerca o diagnosi di una forma del desiderio?</li>
  </ol>
</div>
"""

CSS = """
@page { size: A4; margin: 18mm 18mm 18mm 18mm;
  @bottom-center { content: counter(page); font: 9pt Palatino; color: #777; } }
:root { --ink:#1d1b18; --muted:#6b6459; --acc:#7a2e1b; --rule:#d9d2c5; --pane:#f6f2ea; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Palatino", "Book Antiqua", Georgia, serif; color: var(--ink); background:#fff;
  font-size: 10.4pt; line-height: 1.45; margin:0; }
.kicker { font-variant: small-caps; letter-spacing: .08em; color: var(--muted); font-size: 9.5pt; }
h1 { font-weight: normal; font-size: 22pt; line-height: 1.1; margin: 4pt 0 2pt; }
h1 em { color: var(--acc); }
.sub { font-style: italic; color: var(--muted); font-size: 11.5pt; margin-bottom: 10pt; }
h2 { font-weight: normal; font-size: 15pt; margin: 0 0 4pt; color: var(--acc); }
h2 .n { color: var(--muted); font-size: 11pt; margin-right: 6pt; }
h2 .bk { color: var(--muted); font-size: 10pt; font-style: italic; margin-left: 6pt; }
h3 { font-size: 10.4pt; font-variant: small-caps; letter-spacing: .05em; margin: 9pt 0 2pt; color: var(--muted); font-weight: normal; }
p { margin: 0 0 6pt; text-align: justify; hyphens: auto; }
.cover { page-break-after: always; font-size: 9.7pt; line-height: 1.4; }
.cols { columns: 2; column-gap: 8mm; }
.cols p { margin-bottom: 4pt; }
.box { background: var(--pane); border-left: 3px solid var(--acc); padding: 6pt 10pt; margin: 8pt 0 0; font-size: 9.3pt; }
.box p { margin: 0 0 4pt; }
.box.final { margin-top: 14pt; font-size: 9.8pt; }
.epi { border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); padding: 6pt 0; margin: 9pt 0;
  font-size: 9.3pt; color:#3a352e; display: grid; grid-template-columns: 1fr 1fr; column-gap: 7mm; }
.epi .la { font-style: italic; }
.epi .who { grid-column: 1 / span 2; font-variant: small-caps; color: var(--muted); margin-top:3pt; text-align:right; }
section.part { page-break-before: always; }
.intro { font-style: italic; color:#3a352e; margin-bottom: 9pt; border-bottom: 1px solid var(--rule); padding-bottom: 7pt; }
.t { break-inside: avoid; margin: 0 0 11pt; }
.t .num { font-variant: small-caps; color: var(--acc); font-size: 10pt; letter-spacing: .04em; margin-bottom: 2pt; }
.t .num .tit { color: var(--ink); font-variant: normal; font-style: italic; letter-spacing: 0; margin-left: 5pt; }
.t .tx { display: grid; grid-template-columns: 1fr 1fr; column-gap: 6mm; border-left: 1px solid var(--rule); padding-left: 9pt; }
.t .tx p { text-align: left; margin: 0; font-size: 9.9pt; line-height: 1.42; hyphens: auto; }
.t .tx p.la { font-style: italic; color: #2c2823; }
.t .gl { font-size: 9.4pt; color: #3a352e; margin: 4pt 0 0; padding-left: 10pt; }
.t .gl b { font-variant: small-caps; color: var(--muted); font-weight: normal; letter-spacing: .04em; }
ol.q { padding-left: 16pt; margin: 4pt 0; } ol.q li { margin-bottom: 5pt; }
"""


# ---------------------------------------------------------------- controllo citazioni
RETR = "fino al riposo del sabato"  # Retract. 2,6,1, descrizione dell'opera fatta da Agostino


def check_quotes():
    """Ogni citazione tra «» nelle chiavi, nelle introduzioni e in copertina
    deve trovarsi alla lettera nel corpus delle Confessioni (italiano o latino)."""
    corpus = " ".join(IT.values()) + " " + " ".join(LA.values()) + " " + RETR
    texts = [COVER, QUESTIONS] + [s["intro"] for s in SECTIONS] + [i["k"] for s in SECTIONS for i in s["items"]]
    bad = []
    for t in texts:
        for q in re.findall(r"«([^»]+)»", re.sub(r"<[^>]+>", "", t)):
            if q not in corpus:
                bad.append(q)
    if bad:
        sys.exit("Citazioni non trovate nel corpus:\n  " + "\n  ".join(bad))
    print("citazioni verificate sul corpus: ok")


def build():
    parts = [f'<!doctype html><html lang="it"><head><meta charset="utf-8">'
             f'<title>Agostino, Confessiones X–XIII — antologia</title><style>{CSS}</style></head><body>', COVER]
    n = 0
    for si, s in enumerate(SECTIONS):
        cls = ' class="part"' if si else ""
        parts.append(f'<section{cls}><h2><span class="n">{s["num"]}.</span>{esc(s["title"])}'
                     f'<span class="bk">({s["books"]})</span></h2><p class="intro">{esc(s["intro"])}</p>')
        for it in s["items"]:
            n += 1
            r = it["ref"]
            la = cut(LA[r], it["la"], r, "LA")
            ita = cut(IT[r], it["it"], r, "IT")
            parts.append(
                f'<div class="t"><div class="num">{ref_label(r)}<span class="tit">{esc(it["title"])}</span></div>'
                f'<div class="tx"><p class="la" lang="la">{esc(la)}</p><p lang="it">{esc(ita)}</p></div>'
                f'<p class="gl"><b>Chiave.</b> {esc(it["k"])}</p></div>')
        if si == len(SECTIONS) - 1:
            parts.append(QUESTIONS)
        parts.append("</section>")
    parts.append("</body></html>")
    OUT_HTML.write_text("\n".join(parts), encoding="utf-8")
    print(f"{n} passi · HTML: {OUT_HTML}")


if __name__ == "__main__":
    check_quotes()
    build()
    if "--no-pdf" not in sys.argv:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()],
                       check=True, capture_output=True)
        print(f"PDF: {OUT_PDF}")

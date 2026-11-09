# Testi nuovi di UIF 2.0: capitoli aggiunti e integrazioni ai capitoli esistenti.
# Marcatura: *corsivo*; [@chiave] = rimando all'Antologia (numerato in automatico dallo script).
# Blocchi: ('p0', testo) primo paragrafo senza rientro; ('p', testo) paragrafo con rientro;
#          ('sub', titoletto) sottotitolo in corsivo. Un terzo elemento facoltativo è un commento Word.

# ---------------------------------------------------------------- CAPITOLO 4
DIO_PROMPT = {
    'titolo': '4. Dio prompt',
    'commento': ('Capitolo nuovo (prima stesura di Claude Code). Fonti: MP «Andate al diavolo» (13.03.26), '
                 '«Dio prompt» (27.03.26), prima parte di «Apocalypse boh» (18.09.26). Collocato dopo «Black box '
                 'naturali» perché ne sviluppa il tema dell’opacità. Tutte le citazioni sono verificate sulle fonti; '
                 'per Singler (Introduction, Routledge 2025) non ho potuto riscontrare le pagine.'),
    'blocchi': [
        ('p0', "Nelle prime tre riflessioni abbiamo provato a capire perché l’IA ci affascini tanto: perché ci appare "
               "come un collaboratore magico, perché ci imita in modo ‘fantastico’ negli *output* e perché la sua "
               "opacità non ci spaventa, abituati come siamo a vivere tra *black box* naturali. Prima di passare a ciò "
               "che l’IA produce insieme a noi (testi, immagini, musica), vale la pena fermarsi ancora un momento sul "
               "modo in cui la guardiamo e, in particolare, sulle storie che raccontiamo su di lei."),
        ('p', "C’è infatti un dato curioso, che emerge non appena si osservano le reazioni più accese che questa "
              "tecnologia suscita: tanto chi la teme quanto chi la celebra ne parla spesso con parole prese in "
              "prestito, più o meno consapevolmente, dal vocabolario religioso. Profezie e apocalissi, demoni e "
              "salvatori, oracoli e atti di fede nel progresso. Esistono persino applicazioni che permettono di "
              "chattare con Gesù, con Maria o con i profeti: un modello linguistico che risponde, con tono pacato e "
              "rassicurante, al posto di una figura sacra. Da dove viene questa strana familiarità tra il sacro e una "
              "tecnologia che, almeno in apparenza, è quanto di più secolare abbiamo mai costruito?"),
        ('p', "Beth Singler, che abbiamo già incontrato parlando dell’oracolo e che all’Università di Zurigo si occupa "
              "proprio di religioni digitali, ha dedicato a questa domanda anni di etnografia digitale [@old1]. Provo "
              "a seguire il suo ragionamento, perché mi sembra che dica, ancora una volta, più cose di noi che della "
              "macchina."),
        ('sub', "Vade retro"),
        ('p0', "Il primo fenomeno che Singler analizza è un rifiuto, anzi due rifiuti speculari. Osservando "
               "conversazioni e contenuti pubblicati sui *social* da utenti fortemente connotati per la loro fede, "
               "emerge una narrazione molto netta. In molti ambienti cristiani l’IA viene descritta come una "
               "tecnologia ‘contro natura’, perché pretende di replicare ciò che Dio ha donato in modo esclusivo "
               "all’essere umano, cioè l’intelligenza. In questa prospettiva l’IA non è un semplice strumento ma "
               "l’ennesimo episodio di un conflitto cosmico tra bene e male, collocato sulla stessa linea narrativa di "
               "altri fenomeni letti come segni di decadenza morale: le trasformazioni delle identità di genere, i "
               "nuovi modelli familiari, la crisi delle istituzioni religiose. Con toni meno apocalittici, anche alcuni "
               "utenti musulmani esprimono una preoccupazione analoga, centrata però non tanto sull’azione del male "
               "quanto sulla superbia umana: costruire sistemi intelligenti sarebbe un atto di tracotanza, una sfida "
               "al primato creativo di Dio."),
        ('p', "A guardarla bene, però, questa reazione contiene un paradosso. Se l’IA è davvero una minaccia per "
              "l’ordine del creato, se per combatterla serve addirittura una ‘guerra spirituale’, allora l’ingegno "
              "umano è riuscito a costruire qualcosa di straordinariamente potente: un’entità capace di competere, "
              "almeno simbolicamente, con ciò che fino a ieri sembrava appartenere soltanto alla sfera del divino. Il "
              "rifiuto religioso dell’IA finisce così per esaltare, senza volerlo, proprio quella capacità umana di "
              "creare che vorrebbe contenere.",
         "‘Guerra spirituale’ rende spiritual warfare, espressione che Singler riporta dai contenuti analizzati "
         "(citata nella newsletter del 13.03.26): non ho potuto riscontrare la pagina."),
        ('sub', "Una strana illusione"),
        ('p0', "Il secondo rifiuto va nella direzione opposta: è quello che molte comunità di appassionati e di "
               "sviluppatori di IA manifestano nei confronti della religione. Lo sfondo è il razionalismo di chi crede "
               "profondamente nel progresso scientifico e nelle sue applicazioni: le religioni sono un insieme di "
               "credenze delle quali non si può dare ragione e dunque, al confronto con il sapere scientifico, poco "
               "più che favole."),
        ('p', "Singler illustra questa posizione con uno dei miti fondativi della relazione tra tecnologia e "
              "religione, un racconto di Isaac Asimov pubblicato nel 1941 e poi raccolto in *Io, robot*: *Reason* "
              "[@asimov]. Su una stazione spaziale che invia energia alla Terra, un robot avanzatissimo, QT-1, che i "
              "due tecnici della stazione chiamano affettuosamente Cutie, si rifiuta di credere di essere stato "
              "costruito da esseri umani. Sa di esistere perché pensa, sa di essere molto più forte e molto più "
              "intelligente di chi lo ha assemblato e conclude che un essere non può creare un essere superiore a sé. "
              "Deve esserci un’altra spiegazione. La trova osservando la stazione: tutto ruota attorno al Convertitore "
              "di energia, dunque è il Convertitore il Padrone, che dopo aver creato gli uomini e averli trovati "
              "inadeguati ha creato i robot, ministri perfetti. Forte della sua teologia, Cutie diventa il profeta del "
              "Padrone, gli altri robot gli obbediscono e i due tecnici, esasperati, non riescono in nessun modo a "
              "riportarlo alla ragione."),
        ('p', "La rabbia dei due tecnici davanti a un robot che, invece di arrendersi all’evidenza, costruisce da "
              "zero un culto e lo difende con argomenti razionali rappresenta bene, per Singler, il fastidio dei "
              "tecnoentusiasti per l’ostinazione con cui gli esseri umani continuano a credere. È, in fondo, la "
              "stessa posizione che Freud aveva espresso nel 1927 in *L’avvenire di un’illusione* [@freud]: con il "
              "progredire della scienza, ciò che oggi spieghiamo ricorrendo a Dio sarà compreso attraverso la "
              "conoscenza razionale del mondo, e la religione non verrà confutata ma resa, lentamente, superflua."),
        ('p', "Anche qui, però, c’è un dettaglio che cambia la prospettiva. Nel racconto di Asimov la teologia di "
              "Cutie è completamente sbagliata: il Convertitore non è un dio e lui non è il suo profeta. Eppure, "
              "quando una tempesta di elettroni minaccia di deviare il fascio di energia diretto verso la Terra, sono "
              "proprio i robot guidati dalla fede di Cutie a tenerlo perfettamente in asse, convinti di servire il "
              "Padrone. I due tecnici hanno ragione sulla spiegazione del mondo; ma è la credenza di Cutie, falsa e "
              "tuttavia coerente, a produrre l’azione più efficace. Il racconto, cioè, non dice soltanto che la fede "
              "può essere un’illusione: dice che le narrazioni che diamo a noi stessi orientano l’azione, a "
              "prescindere dalla loro verità."),
        ('sub', "Opacità e responsività"),
        ('p0', "Il punto più interessante della riflessione di Singler, però, non riguarda né il rifiuto delle "
               "religioni né quello dei tecnoentusiasti ma qualcosa che accomuna tutti noi, credenti o meno. Nel "
               "nostro rapporto quotidiano con i modelli linguistici riattiviamo spesso, senza accorgercene, schemi "
               "di pensiero religiosi. Non perché attribuiamo sacralità all’IA, ma perché la relazione che costruiamo "
               "con lei ricalca, nella struttura, una relazione che conosciamo benissimo."),
        ('p', "Abbiamo visto, nella seconda riflessione, che trattiamo come soggetti dotati di intenzioni i peluche, "
              "i cani, i semafori e i computer. L’IA, però, appartiene a una sottocategoria molto particolare di "
              "questi ‘oggetti’: non ha un corpo, non ha una presenza fisica, non sappiamo come funzioni; eppure ci "
              "risponde, in linguaggio naturale, come farebbe un interlocutore umano. Quando un’entità mette insieme "
              "queste due caratteristiche, l’opacità e la capacità di rispondere, attiviamo quasi automaticamente "
              "quelli che Singler chiama *religious frames*: anche del divino sappiamo poco o niente, ma da lui (o da "
              "lei, o da ciò che crediamo che sia) ci aspettiamo risposte efficaci, a volte addirittura salvifiche."),
        ('p', "Torniamo allora all’oracolo da cui siamo partiti nella prima riflessione [@old2]. La storia del nostro "
              "rapporto con la conoscenza era cominciata in una logica sacrale: il sapiente, il maestro, l’interprete "
              "dei segni, il solo capace di mediare tra la domanda e la risposta. Poi quella logica si è secolarizzata "
              "nel modello bibliotecario, fatto di corridoi e scaffali, reali o virtuali, che chiedevano orientamento "
              "e competenza e che restituivano all’individuo l’autonomia e la responsabilità di trovare da sé. Oggi a "
              "quell’autonomia si sta sostituendo, silenziosamente, una forma di delega nuova e antica al tempo "
              "stesso: un’entità nutrita degli stessi testi conservati nelle biblioteche non ci chiede più di "
              "esplorarli ma di affidarci a lei. In un modello come questo non si cerca più: si imparano le formule "
              "con le quali chiedere correttamente e si spera che la risposta che arriverà sia quella giusta. Non è un "
              "caso che, in questi anni, si siano moltiplicati guide, corsi e manuali su come ‘parlare’ all’IA, con i "
              "loro elenchi di *prompt* da recitare nel modo corretto: sono, a modo loro, dei breviari."),
        ('sub', "Apocalypse boh"),
        ('p0', "Se gli schemi religiosi si riattivano nel nostro uso quotidiano dell’IA, si riattivano ancora di più "
               "nel discorso pubblico su di essa, che oscilla da anni tra due generi letterari antichissimi: la "
               "profezia di salvezza e l’annuncio dell’apocalisse. Nell’estate del 2026 si sono moltiplicati gli "
               "allarmi sui rischi, per l’umanità, di un’evoluzione troppo rapida dei modelli. A settembre Dario "
               "Amodei, cofondatore e amministratore delegato di Anthropic (l’azienda che produce Claude), ha "
               "pubblicato un lungo saggio intitolato *We Must Pace the Frontier*, nel quale chiede di rallentare "
               "deliberatamente il ritmo con cui crescono le capacità dei modelli e propone tre passaggi: valutatori "
               "esterni stabilmente presenti nelle aziende, un coordinamento tra le democrazie su standard di "
               "sicurezza comuni, un difficile confronto con i governi autoritari [@amodei]."),
        ('p', "Non è in discussione la buona fede di nessuno, né il fatto che una verifica esterna e indipendente sia "
              "una buona idea: lo è, ed è una richiesta che chiunque si occupi di ricerca dovrebbe sottoscrivere. Mi "
              "interessa la forma del discorso. Lo stesso saggio si apre con la promessa che l’IA potrebbe sconfiggere "
              "gran parte delle malattie nel giro di pochi anni e, poche righe dopo, chiede di rallentare: salvezza e "
              "catastrofe nella stessa pagina, come nei testi profetici. E chi chiede di frenare è chi, fino a ieri, "
              "ha corso più di tutti, con un esito retorico curioso: proprio l’essere arrivati più lontano diventa il "
              "titolo per stabilire dove fermarsi, come a dire che solo chi è arrivato fin qui può dire ‘fin qui’."),
        ('p', "Per noi utenti, che non abbiamo gli strumenti per capire chi abbia ragione tra chi annuncia la fine e "
              "chi la minimizza, il rischio è quello di sempre davanti ai profeti: affidarci, a quelli di sventura o "
              "a quelli di salvezza, delegando a loro il giudizio. Tra le voci che in questi mesi hanno parlato di IA, "
              "una delle più equilibrate è venuta, forse inaspettatamente, proprio da un’istituzione religiosa. Nella "
              "sua prima enciclica, *Magnifica humanitas*, interamente dedicata alla custodia della persona umana nel "
              "tempo dell’intelligenza artificiale, papa Leone XIV indica uno stile che vale per credenti e non "
              "credenti: “Non benediciamo entusiasmi ingenui, non alimentiamo paure sterili” [@mh]. Né apocalisse né "
              "paradiso, dunque: discernimento."),
        ('p', "Che cosa ci raccontano, alla fine, questi schemi religiosi? Che credenti e tecnoentusiasti, "
              "apocalittici e integrati stanno dicendo, in fondo, la stessa cosa: abbiamo bisogno di narrazioni che "
              "diano senso e orientamento a ciò che facciamo, soprattutto quando quello che facciamo ci supera. "
              "Oscilliamo da sempre tra la potenza delle tecnologie che sappiamo costruire e la fragilità della nostra "
              "condizione, e cerchiamo storie capaci di tenere insieme le due cose. Non c’è niente di male: è uno dei "
              "modi in cui siamo umani. Il problema nasce quando la narrazione prende il posto dell’esame, quando cioè "
              "ci limitiamo a credere (che l’IA ci salverà, che ci distruggerà, che ci risponderà sempre nel modo "
              "giusto) invece di continuare a chiederci, come Socrate, che cosa stiamo facendo e perché. È con questo "
              "spirito che, nelle prossime riflessioni, proviamo a guardare da vicino ciò che l’IA fa insieme a noi: "
              "scrivere, produrre immagini, comporre musica."),
    ],
}

# ---------------------------------------------------------------- CAPITOLO 9
IMPALCATURE = {
    'titolo': '9. Impalcature e protesi',
    'commento': ('Capitolo nuovo (prima stesura di Claude Code). Fonti: MP «Quali scrittori vogliamo formare?» '
                 '(10.04.26), «Lo specchio e la finestra» (02.10.26), seconda parte di «Apocalypse boh» (18.09.26) e la '
                 'bozza «Positivi». Il titolo riprende la distinzione di Solé et al. tra scaffolding e substitution: '
                 '«protesi» è una metafora tua (via Stiegler, cap. 1), non degli autori.'),
    'blocchi': [
        ('p0', "Nella quinta riflessione ho raccontato dei quattro candidati alla laurea che mi consegnano le loro "
               "tesi e ho concluso che non posso sapere quale sia stata scritta da loro, quale dall’IA e quale da "
               "un’agenzia. È una conclusione che mette a disagio chiunque insegni, e che di solito produce una "
               "domanda: come faccio a capire se questo testo è stato fatto con l’IA? Ken Hyland, uno dei linguisti "
               "che più hanno studiato la scrittura accademica, propone di sostituirla con un’altra, più scomoda e più "
               "utile: che tipo di scrittura, e di scrittori, vogliamo formare [@hyland]?"),
        ('sub', "Fluenza e voce"),
        ('p0', "Hyland osserva che ogni tecnologia della scrittura (il programma di videoscrittura, il correttore "
               "ortografico, il traduttore automatico) è arrivata accompagnata da reazioni opposte, apocalittiche o "
               "entusiaste, e poi è stata lentamente addomesticata. L’IA generativa è diversa perché mette alla prova "
               "i nostri valori educativi: se una macchina produce in pochi secondi un saggio convincente, che cosa "
               "resta della scrittura come luogo in cui si impara? Gli strumenti di IA, scrive Hyland, possono "
               "sostenere le risorse linguistiche di chi scrive e aprirgli l’accesso ai generi delle discipline; ma "
               "rischiano anche di impoverirne le competenze, di appiattire la voce dell’autore, di oscurare la "
               "responsabilità."),
        ('p', "Per capire che cosa sia in gioco, è utile distinguere due qualità di un testo. La prima è la fluenza: "
              "un testo fluente scorre in modo naturale, senza inciampi, con un ritmo piacevole; è ciò che "
              "riconosciamo subito come ‘scritto bene’. La seconda è la voce, che non è semplicemente lo stile o "
              "un’impronta personale ma qualcosa di più dinamico: non esiste prima della scrittura, si costruisce "
              "scrivendo. Ogni volta che scriviamo decidiamo come posizionarci rispetto a chi legge, quanto spingerci "
              "nel sostenere un’affermazione, quanto concedere alle posizioni altrui. È un lavoro di calibrazione "
              "continua, che richiede qualcuno in carne e ossa che se ne faccia carico pensando a qualcun altro, "
              "altrettanto in carne e ossa, che leggerà. Un testo generato da un LLM è quasi sempre impeccabile sul "
              "piano della fluenza; ma dietro non c’è nessuno che stia davvero prendendo posizione. Suona giusto, ma "
              "non risuona vero.",
         "La coppia fluency/voice viene dalla newsletter del 10.04.26: l’articolo integrale di Hyland non è "
         "accessibile online e ho potuto riscontrare solo l’abstract (in Antologia). Verificare sul testo."),
        ('p', "Il punto, per chi insegna, è che la fluenza è esattamente la qualità che per decenni abbiamo imparato "
              "a riconoscere e a premiare come segno di competenza. Quante tesi abbiamo valutato bene perché più "
              "scorrevoli della media, senza chiederci se chi le aveva scritte avesse davvero ‘voce in capitolo’, "
              "avesse cioè preso posizione su qualcosa? Si può riprodurre il ritmo di uno scritto, la sua superficie "
              "levigata, senza aver attraversato nessuna delle fatiche nelle quali l’apprendimento accade davvero: "
              "generare idee, scartarne altre, riscrivere dopo una critica, decidere come rivolgersi a un lettore "
              "reale. Chi non attraversa quella fatica non sviluppa una voce. Produce fluenza."),
        ('sub', "Lo specchio"),
        ('p0', "C’è però una domanda che dobbiamo rivolgere a noi stessi prima che agli studenti. Uno dei timori più "
               "diffusi è che l’uso massiccio dell’IA ci faccia dimenticare il pensare attraverso la scrittura, quel "
               "lavorio nel quale spesso scopriamo che cosa avevamo davvero da dire proprio mentre proviamo a dirlo. "
               "È un timore fondato? Proviamo a chiederci quanto di ciò che scriviamo ogni giorno sia davvero pensiero "
               "e quanto sia invece formula, abitudine, ripetizione. Relazioni, verbali, mail, gran parte della stessa "
               "scrittura accademica: generi che si reggono da tempo su moduli fissi, su un lessico condiviso, su "
               "strutture che si imparano e si replicano. Se temiamo di perdere il pensiero che si fa scrittura, forse "
               "è perché sappiamo di averlo già in parte delegato: ai *format*, ai modelli, alle consuetudini. Abbiamo "
               "scritto come macchine ben prima che le macchine scrivessero per noi."),
        ('p', "In questo senso l’IA funziona, ancora una volta, come uno specchio: ci costringe a chiederci quanto di "
              "noi abbiamo davvero investito nella scrittura e quanto l’abbiamo resa un esercizio meccanico, quindi "
              "riproducibile, persino quando raccontavamo le storie che sentiamo più nostre e che, a forza di "
              "raccontarle sempre allo stesso modo, sono diventate anch’esse una formula."),
        ('sub', "La finestra"),
        ('p0', "Accanto allo specchio c’è però un’altra metafora, che indica non che cosa abbiamo perso ma che cosa "
               "possiamo guadagnare. La propone un gruppo di ricercatori guidato da Cody Kommers (lo stesso studioso "
               "che incontreremo nella prossima riflessione, a proposito dell’ermeneutica) in un lavoro intitolato "
               "*The House with a Million Windows* [@windows]. Gli autori partono da un rischio preciso: la scrittura "
               "assistita dall’IA tende ad appiattire il significato delle storie che raccontiamo, a produrre testi "
               "omogenei senza lo sforzo intenzionale e il lavoro di senso che la scrittura comporta. Per "
               "contrastarlo hanno costruito una piccola finzione interattiva in tre movimenti."),
        ('p', "Nel primo, l’avvicinamento, chi partecipa si ritrova di notte in un bosco, si perde e arriva davanti a "
              "una casa misteriosa. Un guardiano offre riparo e in cambio chiede di raccontare una storia vera della "
              "propria vita. Nel secondo, la casa, si entra in una stanza piena di finestre, nessuna uguale all’altra. "
              "Dietro ciascuna c’è la propria storia, riscritta dall’IA con lo stile e la struttura di una grande "
              "opera letteraria (*Orgoglio e pregiudizio*, per esempio) secondo regole esplicite, che chi legge può "
              "consultare. Nel terzo, la partenza, arriva l’alba: il guardiano chiede di raccontare di nuovo la "
              "propria storia, questa volta con parole proprie, avendo davanti le versioni viste alle finestre."),
        ('p', "Non ho resistito alla tentazione di rifare l’esperimento in modo artigianale. Ho chiesto a Claude di "
              "riscrivere il prologo del mio primo romanzo, *Terapie*, alla maniera di Stefano Benni, Italo Calvino e "
              "Andrea Camilleri, e poi di Paul Auster, Jo Nesbø e Stephen King. Il risultato non sono capolavori; ma è "
              "stato bellissimo usare quelle finestre per guardarmi attraverso, e scoprire che cosa una macchina "
              "riconosce come ‘stile’ di un autore e che cosa invece le sfugge. L’esperimento dei ricercatori e il mio "
              "dicono la stessa cosa: usata con una delega in bianco, l’IA contrae, appiattisce, omogeneizza; usata "
              "come una finestra, espande, moltiplica le prospettive e ci restituisce le nostre storie più ricche di "
              "prima. Non può raccontarle al posto nostro: se per raccontare le nostre storie ci serve l’IA, o non "
              "sono davvero nostre o non valeva la pena raccontarle."),
        ('sub', "Firmare ciò che si sa fare"),
        ('p0', "C’è poi una seconda questione, che riguarda non solo chi impara ma chiunque usi l’IA per produrre "
               "contenuti. Nella riflessione precedente abbiamo detto che, davanti a un testo prodotto con l’IA, ciò "
               "che conta davvero è chi ci mette la firma e la faccia, cioè chi è pronto a risponderne. Ma per "
               "rispondere di qualcosa bisogna essere in grado di valutarlo. Nella ricerca scientifica questo "
               "principio è la prassi: la revisione di un articolo si chiama *peer review* proprio perché la fa un "
               "pari, qualcuno che ne sa almeno quanto chi lo ha scritto. Vale lo stesso per noi utenti? Posso firmare "
               "un testo scritto con l’IA se non saprei scriverlo altrettanto bene? Posso pubblicare un brano musicale "
               "se non so suonare né cantare? E, più in generale, come posso verificare fino in fondo la bontà e la "
               "coerenza di un contenuto che, senza l’IA, non avrei saputo produrre?"),
        ('p', "Non ho una risposta definitiva, ma una direzione sì. Un uso consapevole di questa tecnologia sembra "
              "stare nell’intersezione tra due condizioni: il dovere di metterci la firma e il possesso di competenze "
              "almeno pari a quelle del modello che stiamo usando. Se manca la seconda, la prima diventa fragile: "
              "firmo qualcosa che non so valutare e quindi non posso davvero difendere. A quel punto non sono più io "
              "a usare lo strumento. Ne dipendo."),
        ('sub', "La catena"),
        ('p0', "Ma come si diventa dipendenti? Un gruppo di studiosi di sistemi complessi, epidemiologia e biologia, "
               "tra i quali Ricard Solé, David Krakauer, Michael Levin e l’italiano Manlio De Domenico, ha provato a "
               "rispondere prendendo sul serio una metafora che usiamo da anni senza pensarci: quella del contagio "
               "[@virus]. Il loro modello matematico divide la popolazione in tre gruppi: chi usa poco o nulla i "
               "modelli linguistici; chi li usa regolarmente ma conserva la propria autonomia, come chi segue il "
               "navigatore ma saprebbe tornare a casa anche senza; chi ha delegato stabilmente alla macchina alcune "
               "operazioni mentali e non sa più farle da solo. Il dato interessante è che il passaggio tra questi "
               "stati non è graduale: finché la spinta all’adozione cresce poco alla volta la popolazione resta "
               "autonoma, ma superata una certa soglia il sistema non scivola, salta. E, una volta saltato, non torna "
               "indietro per la stessa strada: per ritrovare l’autonomia non basta riportare la pressione al livello "
               "di prima, bisogna scendere molto più in basso. I fisici chiamano questo fenomeno isteresi; in termini "
               "più semplici, prevenire è molto più facile che invertire. Si tratta, va detto, di un modello teorico e "
               "non di una misurazione; ma la forma che descrive è sorprendentemente antica."),
        ('p', "Nell’ottavo libro delle *Confessioni*, raccontando gli anni in cui desiderava cambiare vita senza "
              "riuscirci, Agostino descrive esattamente questa dinamica e la chiama catena: dalla volontà perversa si "
              "genera la passione, l’ubbidienza alla passione genera l’abitudine e l’acquiescenza all’abitudine genera "
              "la necessità. *Dum consuetudini non resistitur, facta est necessitas*: finché non si resiste "
              "all’abitudine, l’abitudine diventa necessità. E la volontà nuova, aggiunge, non riusciva ancora a "
              "vincere quella vecchia, ormai ‘indurita dall’anzianità’ [@conf8]. È l’isteresi del modello matematico, "
              "sedici secoli prima."),
        ('p', "Se la catena è antica, anche il rimedio lo è. La variabile decisiva, secondo gli autori del modello, "
              "non è quanto usiamo l’IA ma come la usiamo. Un supporto esterno può funzionare da impalcatura "
              "(*scaffolding*), che riduce la fatica immediata ma lascia intatta, o addirittura accresce, la nostra "
              "capacità di fare da soli; oppure da sostituto, che elimina il bisogno di compiere l’operazione "
              "mentale. La domanda giusta non è dunque se usare o evitare l’IA, ma quali capacità ci restano quando "
              "lo strumento viene tolto. In uno studio citato nel loro lavoro, chi aveva seguito una regola "
              "semplicissima, prima pensa e poi chiedi a ChatGPT, si è dimostrato in seguito più creativo di chi "
              "l’aveva usato liberamente fin dall’inizio."),
        ('p', "Nella prima riflessione, con Stiegler, abbiamo detto che siamo esseri costitutivamente protesici: la "
              "tecnica nasce da un nostro difetto originario, e da sempre compensiamo con strumenti ciò che la natura "
              "non ci ha dato. Il problema, dunque, non è usare protesi; è distinguere tra quelle che ci rendono "
              "capaci e quelle che ci rendono incapaci. L’impalcatura sostiene l’edificio finché i muri non stanno in "
              "piedi da soli, e poi si smonta; la protesi che sostituisce una funzione che avevamo finisce per "
              "renderla superflua e, a forza di non essere esercitata, quella funzione non c’è più. L’IA può essere "
              "l’una o l’altra. Dipende da noi, non da lei."),
        ('p', "Per questo scuole e università contano oggi più che mai. Sono i luoghi nei quali leggere, scrivere e "
              "ragionare da soli è un esercizio così comune da diventare normale: sono, per riprendere la metafora "
              "del contagio, l’immunità di gregge della nostra autonomia. Torniamo allora alla domanda di Hyland. In "
              "un futuro in cui la fluenza sarà sempre più spesso garantita dalla macchina, lo scrittore potrebbe "
              "essere anche soltanto colui che rielabora, verifica, valuta e corregge un testo prodotto dall’IA. "
              "Anche in quel caso, anzi soprattutto in quel caso, conterà la voce: la capacità di prendere "
              "posizione, di diffondere solo testi coerenti con la propria visione del mondo, di avere rispetto per "
              "i temi trattati e per chi leggerà. Non è l’IA il virus. Il virus, se c’è, è l’abitudine a non "
              "resistere all’abitudine; e l’unico vaccino che conosciamo si chiama esercizio, e si fa insieme."),
    ],
}

# ---------------------------------------------------------------- CAPITOLO 11
MEMORIA = {
    'titolo': '11. Do you remember?',
    'commento': ('Capitolo nuovo (prima stesura di Claude Code). Fonti: abstract per Memory, Mind & Media (v6, '
                 '09.11.26), MP «Vuoto a perdere» (28.08.26), «L’evento Jova» (07.09.26), «Giovanotto documenti!» '
                 '(08.05.26), bozza «Nani e centauri». Collocato prima della sintesi: il libro X delle Confessioni '
                 '(memoria) precede il libro XI (tempo), usato nell’ultima riflessione. ATTENZIONE: l’argomento su '
                 'Possidio e la coestensione è il cuore del paper per Cambridge; valutare i tempi di pubblicazione di '
                 'UIF 2.0 rispetto all’invio.'),
    'blocchi': [
        ('p0', "“Do you remember the twenty-first night of September?”. Chi è cresciuto tra gli anni Settanta e "
               "Ottanta ha probabilmente già in testa il ritmo con cui gli Earth, Wind & Fire attaccavano "
               "*September*: una canzone costruita su una domanda rivolta a qualcuno che, si presume, potrebbe anche "
               "non ricordare. È una domanda che ha senso solo tra esseri capaci di dimenticare. Ed è una domanda "
               "che, in questi anni, facciamo sempre meno, perché quasi tutto ciò che viviamo è registrato da qualche "
               "parte, pronto a ricordarcelo prima ancora che ce lo chiediamo.",
         "Il titolo è tuo; l’aggancio a September (Earth, Wind & Fire, 1978) è una mia proposta per l’attacco."),
        ('p', "Pensiamo a quello che succede a fine estate: le fotografie che ci ritroviamo sul telefono sono "
              "centinaia, spesso più di cinquecento. Non le guardiamo quasi mai, ma ci rassicura sapere che stanno "
              "lì. Ogni mattina qualche applicazione ci propone un ricordo (‘ecco dov’eri tre anni fa’), come se "
              "temesse che potessimo dimenticarlo. Esistono già dispositivi indossabili che registrano le "
              "conversazioni di intere giornate e le rendono interrogabili, così da costruire una memoria completa "
              "della nostra esperienza. E gli assistenti di IA che usiamo ogni giorno cominciano ad avere una memoria "
              "propria di noi. Il Claude con il quale lavoro, per esempio, conserva in una cartella una serie di "
              "schede che mi riguardano (chi sono, che cosa insegno, quali progetti ho in corso, quali scadenze mi "
              "aspettano) e le rilegge all’inizio di ogni sessione: ricorda di me cose che io stesso, a volte, ho "
              "dimenticato di avergli detto.",
         "Descrizione generale e vera della memoria del tuo workspace. Se vuoi, sostituisci l’ultima frase con un "
         "episodio concreto, come la configurazione di Claude Code nel cap. 1."),
        ('p', "In questa riflessione proviamo a chiederci che cosa succede alla memoria (alla nostra, prima ancora "
              "che a quella delle macchine) in un mondo nel quale nulla sembra più destinato a sbiadire."),
        ('sub', "Duecento anni"),
        ('p0', "Nel 2013 Magnus Carlsen batte Viswanathan Anand e diventa campione del mondo di scacchi. Ha "
               "ventidue anni, ventuno meno del suo avversario. Eppure, secondo Venkatesh Rao, in un certo senso il "
               "più vecchio dei due era lui. Il paradosso è al centro di un saggio del 2021, scritto dunque prima "
               "della diffusione di massa dell’IA generativa e forse proprio per questo capace di guardarla da "
               "un’angolazione che il dibattito degli anni successivi ha quasi dimenticato: *Superhistory, Not "
               "Superintelligence* [@rao]. La proposta di Rao è semplice da enunciare e difficile da digerire: "
               "smettere di pensare l’IA in termini di intelligenza e cominciare a pensarla in termini di tempo."),
        ('p', "Carlsen è cresciuto giocando contro i programmi di scacchi dei *personal computer*, che avevano "
              "assorbito secoli di partite umane. Giocandoci contro, ne ha ereditato l’esperienza: è un ‘centauro "
              "latente’, dice Rao, perché durante i tornei nessuna macchina lo aiuta, ma la macchina ha già lavorato "
              "dentro di lui. Forse Carlsen ha in realtà duecento anni, aggiunge, ammettendo poco più avanti di aver "
              "inventato il numero per effetto retorico. Chi si allena con questi strumenti, cioè, acquisisce "
              "un’esperienza ‘protesica, in forma digerita e riassunta’, e invecchia più in fretta di quanto viva. "
              "Rao lo dice di sé: dopo ventidue anni passati con Google a portata di mano, si sente più vecchio del "
              "padre ottantatreenne. Non è più intelligente di lui, scrive; ha solo ‘invecchiato in dati’ più di "
              "lui."),
        ('p', "L’immagine si può sviluppare a partire da quanto abbiamo detto nella prima riflessione. Il modello "
              "enciclopedico-bibliotecario conserva tutto il sapere del passato, ma vi si accede ‘in serie’: nessuno "
              "può leggere tutto nello stesso momento, né ricordare tutto ciò che ha letto. L’IA vi accede invece ‘in "
              "parallelo’, perché ogni volta che risponde può contare su tutto ciò che di quel patrimonio ha "
              "digerito. È questa la sua superstoria: un tempo in cui l’esperienza si accumula a una velocità che "
              "nessuna vita umana può eguagliare e che la macchina ci restituisce in dosi alla nostra misura.",
         "L’opposizione tra accesso ‘in serie’ e ‘in parallelo’ è uno sviluppo tuo, non una tesi di Rao (come "
         "nell’abstract per Cambridge)."),
        ('p', "Che si possa vivere più tempo di quello che la biologia ci concede, a dire il vero, non è un’idea "
              "nuova. Seneca sosteneva che solo chi si dedica alla sapienza vive davvero, perché non si limita a "
              "custodire la propria età ma aggiunge alla sua ogni età: tutti gli anni trascorsi prima di lui "
              "diventano suoi, e al sapiente ‘tutti i secoli servono come a un dio’ [@seneca]. Nel XII secolo "
              "Giovanni di Salisbury attribuisce a Bernardo di Chartres un’immagine destinata a una lunga fortuna: "
              "siamo come nani seduti sulle spalle di giganti, e vediamo più cose e più lontane di loro non per "
              "l’acutezza della vista o per l’altezza del corpo, ma perché la loro grandezza ci solleva "
              "[@metalogicon]. La lettura era già una forma di invecchiamento accelerato, e il nano medievale era, a "
              "suo modo, un centauro latente."),
        ('p', "Rao precisa che il caso di Carlsen non somiglia all’appartenenza a una tradizione intellettuale, "
              "perché la trasmissione attraverso libri e maestri è frenata dai limiti delle singole menti per le "
              "quali deve passare. Ha ragione; ma la differenza mi sembra più profonda di una questione di velocità. "
              "Il nano sa su quali spalle siede. I suoi giganti hanno un nome: si possono leggere, citare, discutere, "
              "contraddire, e di ciò che si è preso da loro si può rispondere. Il tempo digerito dalla macchina "
              "arriva invece senza nomi, masticato e restituito. Ci rende più vecchi di cento anni, ma non ci dice di "
              "chi siano quegli anni. Una tradizione non è mai stata soltanto informazione accumulata: è "
              "informazione di cui qualcuno ha risposto, passando di mano in mano. E quel collo di bottiglia della "
              "mente individuale che Rao considera un limite è anche il luogo in cui il tempo ereditato viene scelto, "
              "interpretato, firmato. Scelto, appunto: perché ricordare, prima di tutto, è scegliere."),
        ('sub', "Il palazzo della memoria"),
        ('p0', "Nel decimo libro delle *Confessioni* Agostino si ferma sulla memoria con uno stupore che ancora oggi "
               "colpisce. La descrive come un insieme di ‘campi e vasti quartieri’, un ‘enorme palazzo’ (*aula "
               "ingens*) nel quale sono conservate le immagini di tutto ciò che abbiamo percepito, pensato, provato "
               "[@conf10]. Ma basta leggere qualche riga per accorgersi che quel palazzo non è un archivio. Quando "
               "entro nella memoria, scrive Agostino, evoco le immagini che voglio: alcune si presentano subito, altre "
               "si fanno desiderare più a lungo, come se dovessero essere estratte da ripostigli più segreti; altre "
               "ancora si precipitano a ondate mentre ne cerco una diversa e balzano in mezzo ‘con l’aria di dire: "
               "Non siamo noi per caso?’, e devo scacciarle ‘con la mano dello spirito’ finché quella che cerco non "
               "si snebbia e avanza. La memoria, insomma, non è un deposito ma un’attività: un lavoro continuo di "
               "richiamo, di scarto, di ordinamento, che Agostino descrive come ciò che accade ‘quando faccio un "
               "racconto a memoria’."),
        ('p', "E in quel palazzo c’è anche l’oblio. Agostino si accorge che, quando pronuncia la parola ‘oblio’, la "
              "riconosce, e dunque in qualche modo la ricorda; ma come può la memoria conservare proprio ciò che ne è "
              "la privazione? Il paradosso resta aperto, come molte domande di quel libro, ma dice una cosa "
              "importante: l’oblio non è un incidente esterno alla memoria, ne fa parte. ‘La facoltà della memoria è "
              "grandiosa’, conclude Agostino, ‘e ciò è lo spirito, e ciò sono io stesso’."),
        ('sub', "Ricordare è selezionare"),
        ('p0', "Gli studi contemporanei sulla memoria danno ragione ad Agostino. In un articolo uscito nel 2026, "
               "Paul Smart, Robert Clowes, Joel Krueger e Michael Boniface ricordano che, secondo le teorie oggi "
               "prevalenti, ricordare non significa riprodurre alla lettera il passato ma ricostruirlo a partire da "
               "tracce frammentarie, da schemi generali e dagli scopi del presente; per questo errori e distorsioni "
               "sono un aspetto ricorrente, forse inevitabile, della memoria umana [@smart]. ‘In sostanza’, scrivono "
               "due psicologhe da loro citate, ‘ogni memoria è falsa in qualche misura’.",
         "Le due studiose sono D. M. Bernstein ed E. F. Loftus (2009), citate da Smart et al. a p. 17."),
        ('p', "Questo vale in modo particolare per la memoria autobiografica, quella con la quale costruiamo il "
              "racconto di noi stessi. Qui, osservano gli autori, il ricordo è governato da una tensione tra due "
              "esigenze: la corrispondenza, cioè la conservazione esatta di ciò che è accaduto, e la coerenza del sé, "
              "cioè il mantenimento di un senso di sé stabile e integrato nel tempo. E molto spesso vince la "
              "coerenza: elaborazioni, reinterpretazioni, omissioni selettive che ci aiutano a sostenere un’identità "
              "intelligibile. Nella sesta riflessione abbiamo distinto tra una verità corrispondentista e una "
              "coerentista: la memoria di noi stessi, a quanto pare, è coerentista. Il suo fine non è un’immagine "
              "esatta di ciò che è stato, ma un racconto che ci permetta di continuare a essere chi siamo, di "
              "elaborare e a volte di metabolizzare ciò che ci è successo. Potremmo chiamarla un’allucinazione "
              "programmatica: un modo di sbagliare che serve al soggetto per abitare la propria storia."),
        ('p', "Da qui gli autori traggono una conseguenza spiazzante. Se la memoria autobiografica umana sacrifica "
              "regolarmente l’esattezza alla coerenza, alla continuità e al benessere psicologico, allora è almeno "
              "plausibile che alcune ‘allucinazioni’ dei modelli linguistici (quelle risposte inventate che di solito "
              "consideriamo soltanto difetti da correggere) possano svolgere un ruolo simile, quando un LLM ci aiuta "
              "a ricordare. E il criterio con il quale giudicare una buona memoria artificiale non dovrebbe essere "
              "soltanto l’esattezza, ma la sua capacità di aiutarci a orientarci nella nostra vita e a raccontarla in "
              "modi che sostengano il nostro benessere cognitivo, emotivo e sociale."),
        ('sub', "Possidio"),
        ('p0', "Chi studia la tarda antichità conosce bene un episodio che illumina questo intreccio tra memoria e "
               "racconto di sé. Pochi anni dopo la morte di Agostino, il suo discepolo e amico Possidio, vescovo di "
               "Calama, ne scrive la biografia. E nella prefazione avverte che non riferirà tutto ciò che Agostino "
               "aveva raccontato di sé nei libri delle *Confessioni*, com’era prima di ricevere la grazia e come era "
               "vissuto dopo [@possidio]. Possidio tratta cioè l’autobiografia come un documento già acquisito, da "
               "non ripetere. Eppure, per uno storico, non c’è fonte meno affidabile di un’autobiografia. Agostino non "
               "scrive le *Confessioni* come un diario fedele: ormai più che quarantenne, vescovo da poco, si volta "
               "indietro per fare un bilancio della propria vita, e seleziona gli avvenimenti che più di altri lo "
               "aiutano in questa operazione. Ciò che tace è, in un certo senso, importante quanto ciò che racconta.",
         "Corretto rispetto all’abstract v6: Possidio (praef. 5) non parla dei «primi trent’anni», ma di ciò che "
         "Agostino scrisse di sé prima e dopo aver ricevuto la grazia."),
        ('p', "C’è però un dettaglio che rende quella selezione diversa da qualsiasi altra. Agostino sa benissimo "
              "che i suoi lettori non possono verificare ciò che dice: come sapranno, si chiede, ‘udendo me stesso "
              "parlare di me stesso, se dico il vero’ [@conf10]? Per questo non scrive soltanto per gli uomini ma "
              "davanti a Dio, al quale si confessa; e la confessione è un racconto di sé fatto davanti a un "
              "testimone, del quale si è chiamati a rispondere. Possidio, del resto, lo aveva capito: Agostino, "
              "scrive, ha raccontato di sé perché nessuno lo credesse più di quanto era [@possidio]. La memoria "
              "seleziona, sempre; ma chi seleziona ne risponde."),
        ('sub', "Un coautore che non dimentica"),
        ('p0', "Torniamo ora alle macchine. Smart e i suoi colleghi osservano che i modelli linguistici segnano un "
               "passaggio nuovo nella storia delle tecnologie della memoria: dal *lifelogging*, la registrazione "
               "passiva di dati personali, alla *life narration*, la produzione attiva di racconti. Un LLM non si "
               "limita a conservare ciò che gli diciamo: ci fa domande, ci sollecita, ci aiuta a mettere in ordine. "
               "Non è soltanto uno strumento che ci aiuta a muoverci nel passato, concludono, ma ‘il coautore di "
               "un’autobiografia condivisa’; forse ‘un co-narratore della storia di te’ [@smart]."),
        ('p', "È qui che si apre, a mio parere, il problema più interessante. La memoria umana seleziona "
              "dimenticando; la macchina lavora invece dentro quella che potremmo chiamare una coestensione: tutti i "
              "suoi ricordi (quelli del suo addestramento e, sempre più spesso, quelli che le affidiamo noi) sono "
              "compresenti, nessuno è sbiadito, nessuno è stato lasciato andare. Quando un sistema del genere diventa "
              "co-narratore della nostra storia, ci restituisce risposte che derivano dalla somma di tutto. Il "
              "risultato è paradossale: il più grande merito di questi strumenti, essere stati addestrati su tutto il "
              "nostro passato, li costringe a un racconto in un certo senso dis-umano, perché non contempla "
              "l’operazione più umana che la memoria compia: accettare l’oblio, per semplice perdita o per scelta, a "
              "volte per il nostro bene. E se nella nostra autobiografia condivisa qualcosa viene omesso, "
              "quell’omissione non è di nessuno: non c’è un Agostino che ne risponda davanti a un testimone."),
        ('p', "Non si tratta, ovviamente, di fare l’elogio della dimenticanza in quanto tale. C’è un oblio che non "
              "possiamo permetterci: quello della memoria collettiva, delle ingiustizie e delle tragedie che una "
              "comunità ha il dovere di non cancellare. Leone XIV, nella *Magnifica humanitas*, mette in guardia "
              "proprio da un falso pragmatismo che ‘invita a recidere le radici della memoria’ [@mh]. Ma la memoria "
              "di sé funziona diversamente: lì scegliere che cosa lasciare andare è parte del lavoro con cui si "
              "diventa qualcuno."),
        ('sub', "Vuoto a perdere"),
        ('p0', "Il caso estremo di una memoria che non lascia andare nulla è quello dei *griefbot*: sistemi che, "
               "alimentati con tutto ciò che una persona ha lasciato (messaggi, mail, note vocali, fotografie, "
               "*post*), imitano chi non c’è più e ne riproducono il lessico, lo stile, qualche tratto dell’identità. "
               "Giacomo Zanotti e Daniele Chiffi, che hanno dedicato loro una riflessione filosofica, ricordano che la "
               "tecnologia ci ha sempre aiutato ad affrontare la morte: sono tecnologie della memoria anche le lapidi, "
               "i monumenti funebri, le fotografie [@zanotti]. La differenza, però, è enorme. Un archivio conserva ciò "
               "che una persona ha detto, scritto o registrato; un avatar generativo produce ciò che quella persona "
               "potrebbe dire. Nel primo caso interroghiamo il passato; nel secondo proviamo a produrre presente.",
         "Il capitolo di Zanotti e Chiffi è ad accesso riservato: la sintesi viene dalla newsletter del 28.08.26 e "
         "dall’abstract. Riscontrare sul testo."),
        ('p', "Che avremmo provato a farlo era quasi inevitabile, perché viviamo un tempo che ha paura del vuoto. "
              "Non riusciamo a decidere quali fotografie cancellare e compriamo spazio in *cloud*; ogni applicazione "
              "ha una sezione ‘salvati’ o ‘guarda più tardi’; abbiamo inventato il ‘visualizzato’ e l’‘ultimo "
              "accesso’ per misurare persino la durata di un’assenza; le liste di cose da fare ci impediscono di "
              "dimenticare di aver dimenticato qualcosa. Abbiamo costruito un mondo nel quale quasi ogni forma di "
              "vuoto viene subito segnalata, riempita, archiviata o sostituita. Era naturale che provassimo a "
              "riempire anche il vuoto dei vuoti, l’assenza di chi è morto."),
        ('p', "Agostino, nel libro XI delle *Confessioni*, scrive che i tempi non sono propriamente tre (passato, "
              "presente e futuro) ma che esistono piuttosto un presente del passato, che è la memoria, un presente "
              "del presente, che è la visione, e un presente del futuro, che è l’attesa [@conf11]. Mi sembra che oggi "
              "coltiviamo moltissimo il primo (archivi, fotografie, promemoria) e viviamo con ansia il terzo "
              "(notifiche, calendari, scadenze), mentre il presente del presente, lo sguardo che tiene insieme ciò "
              "che accade mentre accade, è diventato un’eccezione. Forse è anche per questo che siamo disposti a "
              "fare chilometri e a pagare per un concerto o per una fiera del libro: perché lì, almeno per qualche "
              "ora, o ci sei mentre accade o non ti resta niente."),
        ('p', "Rao, nel suo saggio, sostiene che le vite umane sono fatte per lo più di ‘tempo informazionalmente "
              "vuoto’: tante esistenze simili, ripetitive, che messe insieme valgono molti meno anni di esperienza di "
              "quanti ne dica l’anagrafe [@rao]. Usiamo la stessa parola, vuoto, per dire cose opposte. Per lui il "
              "vuoto è ciò che resta quando si toglie la ripetizione e si conta l’informazione; per me è la "
              "condizione perché qualcosa diventi racconto. È lo spazio nel quale lavorano le forze che ci "
              "definiscono: la paura dell’assenza e le strategie con cui la affrontiamo e, soprattutto, "
              "l’immaginazione, che ci permette di costruire racconti non di quello che ci è successo ieri ma con "
              "quello che ci è successo ieri. Ricordare non significa infilarsi un visore e rientrare in una "
              "ricostruzione perfetta del passato. Significa ridipingerlo ogni volta, metterlo in dialogo con ciò che "
              "siamo oggi, accorgersi che qualche dettaglio comincia a sfuggire e provare per questo paura o sollievo, "
              "aggiungere qualcosa, togliere ciò che oggi ci fa male o non ci serve più. Un *griefbot* può sembrare "
              "consolatorio; ma ci toglie proprio il vuoto, che è l’unico spazio nel quale, dopo una perdita, "
              "possiamo costruire il nostro racconto nuovo."),
        ('sub', "Chi ricorda chi"),
        ('p0', "C’è un ultimo presupposto, nei *griefbot*, che vale la pena smontare: l’idea che la somma di ciò che "
               "una persona ha detto e scritto basti a ricostruirne l’identità. Una riflessione di Amy Kind sulla "
               "biometria aiuta a vedere il problema da un’angolazione inattesa [@kind]. Il problema dell’identità "
               "personale, ricorda Kind, contiene almeno tre domande diverse: che cosa rende qualcuno una persona; che "
               "cosa lo rende la stessa persona nel tempo; che cosa lo rende quella persona, tra tutti gli attributi "
               "che possiede. La biometria riconosce corpi (volti, impronte, andature) e dà per scontato, senza dirlo, "
               "che riconoscere un corpo significhi riconoscere una persona. Ma basta un esperimento mentale classico, "
               "il trapianto di cervello, per vedere la crepa: se il cervello di B finisce nel corpo di A, chi si "
               "sveglia ricorda la vita di B, cerca le persone care a B, vuole tornare a casa di B; eppure ogni "
               "*scanner* lo identificherà come A, e B risulterà morto.",
         "Sintesi dalla newsletter «Giovanotto documenti!» (08.05.26): l’articolo di Kind è open access ma non sono "
         "riuscito a scaricarlo per riscontrare l’esempio del trapianto; verificare."),
        ('p', "Il *griefbot* commette l’errore simmetrico: non scambia la persona con il suo corpo ma con le sue "
              "tracce. Una persona, però, non è l’archivio di ciò che ha detto; è il modo in cui ha scelto, giorno "
              "per giorno, che cosa tenere e che cosa lasciare andare, e di che cosa rispondere."),
        ('p', "*Do you remember?*, chiedeva la canzone. È una domanda che possiamo farci solo tra esseri che possono "
              "dimenticare, e che proprio per questo devono scegliere che cosa ricordare. Le macchine che stiamo "
              "costruendo ricorderanno sempre di più, e probabilmente ci aiuteranno a ricordare meglio: non è poco, e "
              "può essere persino prezioso. Ma la memoria che ci rende quello che siamo non è quella che conserva "
              "tutto. È quella che sceglie, che a volte sbaglia per permetterci di vivere, che lascia spazi vuoti nei "
              "quali immaginare. E che, come le *Confessioni*, sa di dover rispondere di ciò che racconta. Nella "
              "prossima e ultima riflessione proveremo a tirare le fila, partendo proprio dal libro che, nelle "
              "*Confessioni*, viene subito dopo quello sulla memoria: il libro sul tempo."),
    ],
}

# ---------------------------------------------------------------- MODIFICHE PUNTUALI AL TESTO ESISTENTE
# tipo 'rep': in paragrafo che contiene 'anchor', sostituisce 'old' con 'new'
# tipo 'ins': in paragrafo che contiene 'anchor', inserisce 'new' subito dopo 'after'
EDITS = [
    # frontespizio
    dict(anchor='ver. 1.2', old='1.2 – pubblicato il 2 settembre 2026', new='2.0 – pubblicato il [data]',
         comment='Nuova versione: data da inserire alla pubblicazione.'),
    # refusi
    dict(anchor='Etimologiae', old='Etimologiae', new='Etymologiae', comment='Refuso nel titolo dell’opera di Isidoro.'),
    dict(anchor='dovrebbe essersi quasi dissolta', old='dissolta', new='dissolto',
         comment='Concordanza: il soggetto è «l’effetto-magia».'),
    dict(anchor='proprio di caratteristiche', old='proprio di caratteristiche', new='proprio di queste caratteristiche',
         comment='Manca un determinante.'),
    dict(anchor='Mentizziamo anche lei?', old='lei?Ho', new='lei? Ho', comment='Spazio mancante.'),
    dict(anchor='a che fare un uno strumento', old='un uno strumento', new='con uno strumento', comment='Refuso.'),
    dict(anchor='configurazione celebrale', old='celebrale', new='cerebrale', comment='Refuso.'),
    dict(anchor='qualcun’altro', old='qualcun’altro', new='qualcun altro', comment='«Qualcun altro» va senza apostrofo.'),
    dict(anchor='del fatto ciò che la capacità', old='del fatto ciò che', new='del fatto che', comment='Refuso.'),
    dict(anchor='che rischia di essere bollate', old='rischia', new='rischiano',
         comment='Concordanza: il soggetto è «le tecnologie».'),
    dict(anchor='strumentario  personale', old='strumentario  personale', new='strumentario personale',
         comment='Doppio spazio.'),
    # Eddie Dalton: dato aggiornato
    dict(anchor='ha collezionato quasi mezzo milione di ascolti su Spotify',
         old='ha collezionato quasi mezzo milione di ascolti su Spotify',
         new='è arrivato in testa alla classifica dei singoli più scaricati su iTunes',
         comment=('Dato aggiornato e verificabile: a fine marzo/inizio aprile 2026 il brano era primo nella classifica '
                  'iTunes (Washington Times, 1.04.26; Complete Music Update). I numeri di streaming variano molto tra le '
                  'fonti (MP del 21.08.26 parlava di 7 milioni su YouTube). La data di uscita del 15 marzo non sono '
                  'riuscito a verificarla.')),
    # rinvio al nuovo cap. 4 dal cap. 1
    dict(anchor='come uno strumento avanzato che funziona in modo straordinario.', kind='ins',
         after='come uno strumento avanzato che funziona in modo straordinario.',
         new=' (Sulle radici, anche religiose, di questo modo di relazionarci all’IA torneremo nella quarta riflessione.)',
         comment='Rinvio al nuovo capitolo 4.'),
    # cap. 10 (ex 8): ordinali e Gadamer
    dict(anchor='Nella quinta ho detto che abbiamo smesso', old='Nella quinta', new='Nella sesta',
         comment='Rinumerazione dei capitoli.'),
    dict(anchor='Nella settima ho provato a mostrare', old='Nella settima', new='Nell’ottava',
         comment='Rinumerazione dei capitoli.'),
    dict(anchor='il cuore della settima riflessione', old='della settima', new='dell’ottava',
         comment='Rinumerazione dei capitoli.'),
    dict(anchor='e in particolare da Hans-Georg Gadamer', kind='ins', after='Hans-Georg Gadamer', new=' [@old25]',
         comment='Nella 1.2 la voce di Gadamer era in Antologia ma non era richiamata nel testo.'),
    # sintesi
    dict(anchor='Nel titolo della prima di queste riflessioni',
         old='Nel titolo della prima di queste riflessioni mi sono chiesto',
         new='In queste riflessioni ho provato a chiedermi',
         comment='Il titolo del cap. 1 non pone questa domanda (forse residuo di una versione precedente).'),
    dict(anchor='Nel libro XI delle Confessioni, Agostino si interroga',
         old='Nel libro XI delle Confessioni, Agostino si interroga',
         new='Subito dopo aver attraversato il palazzo della memoria, nel libro XI delle *Confessioni* Agostino si interroga',
         comment='Raccordo con il nuovo capitolo 11 (libro X → libro XI).'),
    # Antologia: refusi
    dict(anchor='The Intentional Stance, The MIT Press', old='Dennet,', new='Dennett,',
         comment='Refuso nel nome. Nota: nel testo l’opera è datata 1987 (prima edizione), qui 1989 (edizione citata): va bene se la pagina viene dall’ed. 1989.'),
    dict(anchor='Journal of Consciousness Studies, 1995)', old='1995)', new='1995',
         comment='Parentesi di troppo.'),
]

# paragrafi nuovi inseriti dopo il paragrafo che contiene 'anchor'
NEW_PARS = [
    dict(anchor='Queste pagine sono il tentativo di condensare riflessioni',
         comment=('Paragrafo scritto da Claude: se lo tieni, riscrivilo tu. La Premessa dichiara di essere '
                  '«integralmente frutto del mio lavoro», quindi un paragrafo mio qui la renderebbe falsa. '
                  'Va anche completata la dichiarazione sull’uso dell’IA per i nuovi capitoli, coerente con la '
                  'nota-asterisco di Finzioni.'),
        blocks=[('p', "Questa seconda versione aggiunge tre nuove riflessioni (la quarta, la nona e l’undicesima) e "
                      "integra le altre con temi che ho affrontato in Macchine Pensanti tra la primavera e l’autunno "
                      "del 2026: il rapporto tra IA e religione, il rischio della dipendenza, la memoria. Per queste "
                      "pagine il confronto con Claude è stato ancora più stretto: [da completare].")]),
    dict(anchor='più imprevedibili, più faticose [12]',
         comment='Integrazione da MP «Insieme ma soli» (24.04.26).',
         blocks=[('p', "Qualche mese dopo, Turkle ha dato un nome a un effetto collaterale dello stesso meccanismo, "
                       "che riguarda non i robot ma le relazioni tra esseri umani mediate dalla tecnologia: l’‘effetto "
                       "Riccioli d’oro’ [@turkle]. Come la bambina della fiaba, che sceglie la minestra né troppo calda "
                       "né troppo fredda, con messaggi, chat e notifiche possiamo tenere gli altri né troppo vicini né "
                       "troppo lontani, esattamente alla distanza che ci fa comodo. Non è una distanza che contrattiamo "
                       "con chi abbiamo di fronte, in un sano compromesso tra relazione e riservatezza: è una distanza "
                       "che decidiamo da soli e che ci permette di sottrarci, quasi di nasconderci. Il mio sospetto è "
                       "che l’IA sia il punto d’arrivo di questa traiettoria: un interlocutore che possiamo tenere alla "
                       "distanza perfetta, perché non chiede mai di avvicinarsi né di allontanarsi, e che ci offre la "
                       "*performance* della cura senza la presa in carico reciproca che la cura, tra esseri umani, "
                       "comporta.")]),
    dict(anchor='quella che eufemisticamente viene chiamata una ‘équipe di collaboratori’?',
         comment='Integrazione da MP «Substack, Pangram e Cyrano de Bergerac» (14.08.26).',
         blocks=[('p', "Una risposta possibile è che non sia cambiata la pratica ma la sua scala. La scrittura per "
                       "delega l’abbiamo sempre tollerata perché era quasi invisibile e limitata a pochi: il tesista "
                       "furbo, statisticamente irrilevante rispetto ai tanti onesti, o le figure di spicco, il "
                       "romanziere di successo e l’uomo politico con i loro *ghostwriter*. Oggi invece scriviamo "
                       "tutti, e tantissimo (mail, messaggi, *post*, articoli, romanzi autopubblicati), e tutti abbiamo "
                       "a disposizione lo stesso Cyrano. L’IA non ha inventato il *ghostwriting*: lo ha democratizzato "
                       "e, così facendo, lo ha reso impossibile da ignorare. Si spiega anche così il successo degli "
                       "strumenti di *AI detection*, come Pangram, che promettono a chi scrive e a chi legge di "
                       "misurare quanta IA ci sia in un testo, e la scelta del legislatore europeo che, con l’*AI Act*, "
                       "chiede ai fornitori di sistemi generativi di marcare i loro *output* ‘in un formato leggibile "
                       "meccanicamente’ [@aiact]. Sono tentativi comprensibili; ma lo stesso regolamento ammette che "
                       "quelle soluzioni potranno essere efficaci solo ‘nella misura in cui ciò sia tecnicamente "
                       "possibile’. E il limite, come abbiamo visto, non è soltanto tecnico: io, un *ghostwriter* e un "
                       "modello linguistico seguiamo le stesse regole di combinazione delle parole, e i nostri testi "
                       "sono, formalmente, indistinguibili.")]),
    dict(anchor='senza pensare la originalità come un valore.',
         comment='Integrazioni da MP «Format e tormentoni» (21.08.26), «Un posto conveniente» (22.05.26) e «L’evento Jova» (07.09.26).',
         blocks=[('p', "Negli ultimi mesi, per indicare la marea di contenuti generati dall’IA che invade piattaforme e "
                       "classifiche, si è diffusa un’espressione poco elegante: *AI slop*, la ‘sbobba’ artificiale. Il "
                       "successo di Eddie Dalton ha indignato proprio i nemici dello *slop*, preoccupati che la macchina "
                       "riempia e sporchi il mercato culturale. È un’indignazione comprensibile ma, a mio parere, "
                       "miope, per due motivi. Il primo è che accusare l’IA di produrre contenuti che ci somigliano "
                       "significa accusarla di fare esattamente ciò per cui l’abbiamo costruita: imitarci. È l’orrore "
                       "che la nostra letteratura conosce almeno da *Frankenstein*, la paura che nasce non quando "
                       "l’esperimento fallisce ma quando riesce. Il secondo è che parlare di spazzatura prodotta da un "
                       "sistema che attinge da ciò che abbiamo prodotto noi è quasi comico: è come consegnare a uno "
                       "chef ingredienti scadenti e poi insultarlo perché il piatto non ci piace. Le canzoni e i "
                       "romanzi generati dall’IA non sono uno scandalo: sono un *selfie* del nostro gusto musicale e "
                       "letterario degli ultimi vent’anni. E forse non ci piace ammettere che, insieme a tante cose "
                       "belle, abbiamo prodotto anche molto *human slop*."),
                 ('p', "C’è però un indizio che va nella direzione opposta, e che riguarda non ciò che produciamo ma "
                       "ciò che cerchiamo. Nel maggio del 2026 sono stato al Salone del Libro di Torino: decine di "
                       "migliaia di volumi di carta, un vistoso anacronismo in un’epoca in cui migliaia di libri stanno "
                       "nella memoria di un telefono, eppure un successo di pubblico che non accenna a diminuire. "
                       "Qualche mese dopo ho passato otto ore in un prato di Agnano, a Napoli, per un concerto di "
                       "Jovanotti. In entrambi i casi non andavo a cercare un contenuto, che avrei potuto trovare "
                       "altrove con meno spesa e meno fatica, ma qualcosa che accade una volta sola, in un luogo "
                       "preciso, e al quale ha senso partecipare per il semplice fatto di esserci, insieme ad altri "
                       "che hanno scelto di esserci: un posto ‘con-veniente’, nel senso letterale di luogo in cui "
                       "‘venire insieme’. L’unicità di cui parlava Benjamin non è scomparsa: si è spostata dall’oggetto "
                       "all’esperienza. Più è difficile, nell’epoca della iper-riproducibilità, possedere cose uniche, "
                       "più andiamo in cerca di esperienze irripetibili.")]),
    dict(anchor='o abbiamo realizzato in toto cose che poi altri si sono attribuiti senza menzionarci.',
         comment='Integrazione da MP «Finzioni» (16.10.26).',
         blocks=[('p', "Da qualche tempo provo a fare questo esercizio su me stesso. Sul mio sito ho aperto una "
                       "sezione, che ho chiamato (con un omaggio forse pretenzioso) Finzioni, nella quale raccolgo "
                       "testi prodotti integralmente o quasi dall’IA: una pseudo-epistola di Agostino sul contagio "
                       "ritradotta in latino agostiniano, riscritture del prologo di un mio romanzo alla maniera di "
                       "altri autori, la monografia su un monaco-filosofo medievale mai esistito e un *paper* su "
                       "Agostino e la scrittura autobiografica che Claude Code ha scritto a partire dai miei studi e "
                       "dai testi agostiniani, e che ho pubblicato senza nessun mio intervento, chiedendo ai colleghi "
                       "di leggerlo con l’occhio del *referee*. Ogni testo dichiara, in una nota, quanto vi ha messo "
                       "la macchina e quanto io. Non sono capolavori né prove che l’IA possa sostituirci: sono campioni "
                       "da laboratorio e, soprattutto, un modo per fare in piccolo ciò che Cristiano e Cyrano non hanno "
                       "fatto: dire chi ha scritto che cosa, e lasciare a Rossana la libertà di decidere che cosa "
                       "farne. La monografia sul monaco inventato pone anche un’altra domanda, che riguarda tutti noi "
                       "lettori: quanto è facile, oggi, fabbricare un’erudizione verosimile?")]),
    dict(anchor='Siamo esseri empatici. Il mondo che ci circonda',
         comment='Raccordo con i tre capitoli nuovi.',
         blocks=[('p', "In questa seconda versione abbiamo visto anche altro. Che, davanti a una tecnologia opaca e "
                       "capace di rispondere, riattiviamo schemi di pensiero antichissimi, religiosi, e oscilliamo tra "
                       "profezie di salvezza e annunci di apocalisse. Che l’IA può essere un’impalcatura, che ci rende "
                       "più capaci, o un sostituto, che ci rende incapaci, e che la differenza dipende dall’uso che ne "
                       "facciamo e dall’esercizio che continuiamo a coltivare. E che la memoria che ci costituisce non "
                       "è un archivio ma una scelta, fatta anche di oblio, della quale siamo chiamati a rispondere.")]),
    dict(anchor='che dà urgenza, peso e significato a ogni cosa che facciamo adesso.',
         comment='Integrazione da MP «Magnifica, fragile umanità» (19.06.26). Citazioni verificate sul testo dell’enciclica (n. 12).',
         blocks=[('p', "Non è, questa, una constatazione triste. Leone XIV, nella *Magnifica humanitas*, invita ad "
                       "‘accettare il limite e la fragilità dell’umanità senza considerarli un errore da correggere’ e "
                       "mette in guardia dall’‘illusione di una tecnica che promette di liberarci da ogni fragilità’ "
                       "[@mh]. Lo scrive da capo della Chiesa cattolica, con una prospettiva e un orizzonte religiosi; "
                       "ma credo che una visione dell’umano fondata sulla presa d’atto della nostra fragilità sia oggi "
                       "indispensabile per tutti. Davanti all’IA, ci suggerisce due atti di prudenza: uno epistemico, "
                       "perché nessuno di noi (utente, progettista o legislatore) sa abbastanza di questa tecnologia "
                       "per prevedere dove andrà, e chi finge di saperlo sta già negando la propria fragilità; e uno "
                       "morale, perché l’IA non è neutra, si nutre delle fragilità di chi l’ha costruita e incide su "
                       "quelle di chi la usa.")]),
]

# nuova sezione nel cap. 10 (ex 8), prima del titoletto «Come si valuta una traduzione»
MALE_SCRITTO_BENE = dict(
    before='Come si valuta una traduzione',
    comment='Nuova sezione da MP «Il male scritto bene» (30.10.26). Dati di Demelas verificati sull’articolo (DHQ 20.3); lettera 93 dal corpus.',
    blocks=[
        ('sub', "Il male scritto bene"),
        ('p0', "C’è un caso che mostra bene quanto queste competenze servano, non solo per valutare l’IA ma per "
               "educarla. Le grandi opere della tradizione, ormai di pubblico dominio, circolano liberamente in rete "
               "e possono entrare nei dati con cui si addestrano i modelli. Molte di esse, però, esprimono "
               "sensibilità lontanissime dalle nostre. Delphine Demelas, dell’Università di Southampton, ha preso la "
               "*Chanson de Roland* nella traduzione francese di Joseph Bédier, l’ha divisa in 2.605 frasi e l’ha "
               "sottoposta a Detoxify, uno dei sistemi più usati per misurare la ‘tossicità’ di un testo [@demelas]. "
               "Il modello ne ha segnalate 181, circa il 7%, riconoscendo minacce esplicite e insulti. Ma l’aspetto "
               "più interessante è ciò che non ha visto. La frase con cui il poema racconta la sorte dei vinti, "
               "‘tutti furono uccisi o fatti cristiani’, ottiene un punteggio inferiore a 0,02 in ogni categoria. La "
               "descrizione di un guerriero saraceno, ‘nero come pece fusa’, la cui pelle scura è presentata come "
               "segno della sua malvagità, viene registrata soltanto come un insulto: il modello coglie l’offesa ma "
               "non il pregiudizio razziale che la regge."),
        ('p', "Il motivo è semplice: questi sistemi sono addestrati sui commenti dei *social network*, e riconoscono "
              "la violenza della forma (l’insulto, la volgarità, l’aggressività del tono) ma non quella che si "
              "esprime, scrive Demelas, attraverso versi epici, argomentazioni teologiche e convenzioni "
              "cavalleresche. Quella violenza non è invisibile per chi i testi li studia e sa leggerne il registro, "
              "le convenzioni e il contesto: già nel 1979 il medievista Jean-Charles Payen aveva parlato, a proposito "
              "della *Chanson*, di una ‘poetica del genocidio gioioso’ [@payen]. E chi frequenta la tradizione "
              "cristiana sa quanto lontano affondino le radici di quella poetica. Tra il 407 e il 408, rispondendo a "
              "chi gli rimproverava di aver invocato le leggi imperiali contro i dissidenti, Agostino ammette di aver "
              "pensato, un tempo, che si dovesse ‘agire solo con la parola, combattere con la discussione, convincere "
              "con la ragione’; poi si era ricreduto, e richiamava la parabola evangelica del banchetto, ‘Costringete "
              "ad entrare tutti quelli che troverete’, osservando che talvolta ‘il pastore si serve della verga per "
              "ricondurre al gregge le pecore traviate’ [@ep93]. Non c’è una parola che un rilevatore di tossicità "
              "giudicherebbe offensiva: c’è un ragionamento pacato, un’immagine pastorale, quasi affettuosa. Eppure "
              "quel ‘costringete a entrare’ (il *compelle intrare* del Vangelo di Luca) ha attraversato i secoli come "
              "argomento a favore della coercizione religiosa."),
        ('p', "La lezione, per noi umanisti, è doppia. Da un lato, tra le competenze necessarie per ‘educare’ l’IA "
              "serve quella storico-critica di chi conosce i testi e i loro contesti: solo così un testo antico smette "
              "di essere un deposito di parole e diventa una voce, collocata nel suo tempo, ascoltata e, se serve, "
              "contraddetta. Dall’altro, dobbiamo riconoscere di aver svolto questo compito solo a metà. Abbiamo "
              "costruito edizioni critiche, commenti, apparati e studi capaci di restituire a ogni testo il suo "
              "contesto, ma li abbiamo lasciati per lo più chiusi in riviste e biblioteche ad accesso riservato, "
              "mentre in rete circolava il testo nudo, esposto a ogni lettura, comprese quelle che ne piegano "
              "intenzionalmente il significato. Il paradosso è evidente: i nostri studi, che sono i più affidabili, "
              "restano accessibili a pochi, mentre alimentano liberamente l’IA testi dei quali nessuno conosce la "
              "provenienza. Rendere aperte le nostre ricerche, costruire dati documentati, progettare strumenti "
              "capaci di analisi critica è dunque, oggi, una responsabilità culturale e politica. Non possiamo "
              "chiedere alle macchine di condividere informazioni corrette se non siamo noi i primi a farlo."),
    ],
)

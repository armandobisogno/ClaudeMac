# Nuove voci dell'Antologia di UIF 2.0.
# head: riferimento (^^maiuscoletto^^, *corsivo*). quotes: lista di (testo, fonte_per_verifica | None).
# Le fonti per la verifica automatica sono file di testo locali (vedi build_uif2.py, FONTI);
# None = traduzione mia o testo non verificabile automaticamente.

CONF = 'corpus:Opere/_md/34. Confessiones.md'
EP93 = 'corpus:Epistulae/_md/103. Epistula 93.md'

VOCI = {
    'asimov': dict(
        head="^^I. Asimov^^, *Reason*, in «Astounding Science Fiction», aprile 1941; poi in *I, Robot*, Gnome Press, "
             "New York 1950 (tr. it. *Io, robot*).",
        quotes=[],
        comment="Riferimento verificato; nessuna citazione (testo sotto diritti). Se vuoi, aggiungi un passo dall’edizione italiana."),
    'freud': dict(
        head="^^S. Freud^^, *L’avvenire di un’illusione* (*Die Zukunft einer Illusion*, Internationaler "
             "Psychoanalytischer Verlag, Wien 1927).",
        quotes=[],
        comment="Nessuna citazione: aggiungere eventualmente un passo dall’edizione italiana che usi."),
    'amodei': dict(
        head="^^D. Amodei^^, *We Must Pace the Frontier*, settembre 2026 (www.darioamodei.com/post/we-must-pace-the-frontier).",
        quotes=[("“I believe that AI could cure most major diseases in the next 5–10 years, greatly accelerate economic "
                 "growth rates, create a world of abundance and empowerment, and usher in a renaissance of democracy "
                 "and freedom. [...] We must slow the pace at which we improve the capabilities of AI models. Progress "
                 "will still seem fast, and we must make wise use of the time we gain. [...] To be clear, pacing does "
                 "not mean halting model training or technical progress, but ensuring companies take adequate time to "
                 "align and safeguard their models, and for third party evaluators to confirm this”.", 'amodei.txt')]),
    'mh': dict(
        head="^^Leone XIV^^, Lettera enciclica *Magnifica humanitas* sulla custodia della persona umana nel tempo "
             "dell’intelligenza artificiale, 15 maggio 2026, nn. 12, 14, 204 (www.vatican.va).",
        quotes=[("“[...] edificare nel bene significa accettare il limite e la fragilità dell’umanità senza "
                 "considerarli un errore da correggere. Oggi, il desiderio di pienezza dell’essere umano rischia di "
                 "essere deviato verso mete ingannevoli: l’illusione di una tecnica che promette di liberarci da ogni "
                 "fragilità o modelli di benessere che “lasciano indietro” interi popoli” (n. 12).", 'mh.txt'),
                ("“Evitiamo parole che umiliano o contrappongono. Scegliamo la chiarezza che illumina e la franchezza "
                 "che apre vie. Non benediciamo entusiasmi ingenui, non alimentiamo paure sterili” (n. 14).", 'mh.txt'),
                ("“Viviamo in un tempo di notevole cecità spirituale e culturale. Un falso pragmatismo invita a recidere "
                 "le radici della memoria, come se si potesse inaugurare una sorta di “nuova creazione” sganciata dal "
                 "passato” (n. 204).", 'mh.txt')],
        comment="La citazione della Premessa («Siamo chiamati a interrogarci sul grande cantiere…») è al n. 90: verificata."),
    'hyland': dict(
        head="^^K. Hyland^^, *Writing in the AI era: Rethinking writing, research and teaching*, in «Journal of Second "
             "Language Writing», 72 (2026), 101302 (DOI 10.1016/j.jslw.2026.101302).",
        quotes=[("“While AI tools can scaffold linguistic resources, expand access to disciplinary genres, and "
                 "redistribute forms of expertise, they also risk deskilling writers, flattening authorial voice, "
                 "obscuring responsibility, and intensifying inequities. [...] rather than asking what AI can do for "
                 "writing instruction, we need to ask what kinds of writing—and writers—we wish to develop”.",
                 'hyland.html')],
        comment="Citazione dall’abstract (testo integrale non accessibile online)."),
    'windows': dict(
        head="^^C. Kommers, S. G. Immel, D. Hemment, M. Lee^^, *The House with a Million Windows: Interactive Fiction "
             "for Narrative Restorying*, arXiv:2609.12537, 2026.",
        quotes=[("“AI-assisted writing can flatten meaning in human storytelling, enabling the production of homogeneous "
                 "outputs without the intentional effort and sense-making writing entails. [...] In HWAMW, users play "
                 "through a text-based narrative in which they tell a story, then encounter a set of LLM-generated "
                 "“windows” reframing it according to different literary styles”.", 'windows.txt')]),
    'virus': dict(
        head="^^R. Solé, G. Ruffini, F. Castaldo, M. Tuccio, L. F. Seoane, M. De Domenico, S. F. Elena, D. C. "
             "Krakauer, M. Levin^^, *Large-Language Models as a Cognitive Virus*, arXiv:2609.03344, 2026.",
        quotes=[("“It is therefore useful to distinguish between scaffolding and substitution. Scaffolding reduces "
                 "immediate cognitive demands while preserving or increasing the user’s subsequent capacity to perform "
                 "the task; substitution removes the need to perform the underlying cognitive operation. [...] The "
                 "relevant distinction is therefore not simply between using and avoiding LLMs, but between forms of "
                 "coupling and, ultimately, what cognitive capacities remain when the tool is withdrawn. [...] Thus, "
                 "after the tipping point has been crossed, reversal requires a larger reduction in transmission "
                 "pressure than would have been required to prevent the transition in the first place”.", 'virus.txt')]),
    'conf8': dict(
        head="^^Agostino^^, *Confessioni* (*Confessiones*, 397-401/403), VIII, 5, 10, tr. it. di C. Carena, Nuova "
             "Biblioteca Agostiniana I, Città Nuova.",
        quotes=[("*Quippe ex voluntate perversa facta est libido, et dum servitur libidini, facta est consuetudo, et dum "
                 "consuetudini non resistitur, facta est necessitas. Quibus quasi ansulis sibimet innexis (unde "
                 "catenam appellavi) tenebat me obstrictum dura servitus. Voluntas autem nova, quae mihi esse coeperat, "
                 "[...] nondum erat idonea ad superandam priorem vetustate roboratam.*", CONF),
                ("“Sì, dalla volontà perversa si genera la passione, e l’ubbidienza alla passione genera l’abitudine, e "
                 "l’acquiescenza all’abitudine genera la necessità. Con questa sorta di anelli collegati fra loro, per "
                 "cui ho parlato di catena, mi teneva avvinto una dura schiavitù. La volontà nuova, che aveva "
                 "cominciato a sorgere in me, [...] non era ancora capace di soverchiare la prima, indurita "
                 "dall’anzianità”.", CONF)]),
    'rao': dict(
        head="^^V. Rao^^, *Superhistory, Not Superintelligence. Artificial Intelligence is really Artificial Time*, in "
             "«Contraptions», 11 maggio 2021 (contraptions.venkateshrao.com).",
        quotes=[("“Magnus Carlsen is a latent centaur [...]. So perhaps by virtue of growing up playing against chess "
                 "programs on computers, Magnus Carlsen is really 200 years old. [...] This is not like belonging to an "
                 "intellectual tradition, with a lineage of masters passing on their knowledge and skills through books "
                 "and teaching. That process of cultural transmission is limited by the individual-human-mind "
                 "bottlenecks it must periodically pass through. [...] Augmenting humans with machine learning in the "
                 "right way raises their effective experiential age. They possess greater “lived experience” than their "
                 "biological age would suggest because they’ve acquired prosthetic experience, in digested, summary "
                 "form. [...] I made up my numbers earlier obviously, for rhetorical effect. [...] human lives are "
                 "mostly informationally empty time [...]. In many ways, I feel older than my father, who is 83. [...] "
                 "I am not smarter than him. I’ve just data-aged more than him”.", 'rao.txt')]),
    'seneca': dict(
        head="^^L. A. Seneca^^, *De brevitate vitae*, 14, 1 e 15, 5, trad. mia.",
        quotes=[("*Soli omnium otiosi sunt qui sapientiae uacant, soli uiuunt; nec enim suam tantum aetatem bene "
                 "tuentur: omne aeuum suo adiciunt; quicquid annorum ante illos actum est, illis adquisitum est. [...] "
                 "omnia illi saecula ut deo seruiunt. Transiit tempus aliquod? hoc recordatione comprendit; instat? hoc "
                 "utitur; uenturum est? hoc praecipit. Longam illi uitam facit omnium temporum in unum collatio.*",
                 'sen.html'),
                ("“Soli fra tutti vivono nel vero ozio coloro che si dedicano alla sapienza, soli vivono: non si limitano "
                 "a custodire bene la propria età, ma aggiungono alla loro ogni età; tutti gli anni trascorsi prima di "
                 "loro diventano un loro acquisto. [...] Al sapiente tutti i secoli servono come a un dio. Un tempo è "
                 "passato? Lo abbraccia con il ricordo. È presente? Ne fa uso. Deve venire? Lo anticipa. Gli rende "
                 "lunga la vita il raccogliere tutti i tempi in uno solo”.", None)]),
    'metalogicon': dict(
        head="^^Giovanni di Salisbury^^, *Metalogicon*, III, 4 (PL 199, 900C), trad. mia.",
        quotes=[("*Dicebat Bernardus Carnotensis, nos esse quasi nanos, gigantium humeris insidentes, ut possimus plura "
                 "eis et remotiora videre, non utique proprii visus acumine, aut eminentia corporis, sed quia in altum "
                 "subvehimur et extollimur magnitudine gigantea.*", 'meta.html.txt'),
                ("“Diceva Bernardo di Chartres che siamo come nani seduti sulle spalle di giganti, così da poter vedere "
                 "più cose di loro e più lontane, non certo per l’acutezza della nostra vista o per l’altezza del corpo, "
                 "ma perché siamo sollevati e portati in alto dalla loro statura di giganti”.", None)],
        comment="Testo latino dell’ed. Giles (1848); l’ed. Webb (1929, p. 136) differisce solo nella grafia e nella punteggiatura."),
    'conf10': dict(
        head="^^Agostino^^, *Confessioni* (*Confessiones*, 397-401/403), X, 3, 3; 8, 12; 8, 14; 16, 24; 17, 26, tr. it. "
             "di C. Carena, Nuova Biblioteca Agostiniana I, Città Nuova.",
        quotes=[("*Et unde sciunt, cum a me ipso de me ipso audiunt, an verum dicam, quandoquidem nemo scit hominum, "
                 "quid agatur in homine, nisi spiritus hominis, qui in ipso est?* (3, 3)", CONF),
                ("“Come poi sapranno, udendo me stesso parlare di me stesso, se dico il vero, quando nessuno fra gli "
                 "uomini conosce quanto avviene in un uomo, se non lo spirito dell’uomo che è in lui?”.", CONF),
                ("*[...] venio in campos et lata praetoria memoriae, ubi sunt thesauri innumerabilium imaginum de "
                 "cuiuscemodi rebus sensis invectarum. [...] Ibi quando sum, posco, ut proferatur quidquid volo, et "
                 "quaedam statim prodeunt, quaedam requiruntur diutius et tamquam de abstrusioribus quibusdam "
                 "receptaculis eruuntur, quaedam catervatim se proruunt et, dum aliud petitur et quaeritur, prosiliunt "
                 "in medium quasi dicentia: \"Ne forte nos sumus?\". Et abigo ea manu cordis a facie recordationis meae, "
                 "donec enubiletur quod volo atque in conspectum prodeat ex abditis. [...] Quod totum fit, cum aliquid "
                 "narro memoriter.* (8, 12)", CONF),
                ("“Giungo allora ai campi e ai vasti quartieri della memoria, dove riposano i tesori delle innumerevoli "
                 "immagini di ogni sorta di cose, introdotte dalle percezioni [...]. Quando sono là dentro, evoco tutte "
                 "le immagini che voglio. Alcune si presentano all’istante, altre si fanno desiderare più a lungo, "
                 "quasi vengano estratte da ripostigli più segreti. Alcune si precipitano a ondate e, mentre ne cerco e "
                 "desidero altre, balzano in mezzo con l’aria di dire: “Non siamo noi per caso?”, e io le scaccio con "
                 "la mano dello spirito dal volto del ricordo, finché quella che cerco si snebbia e avanza dalle segrete "
                 "al mio sguardo [...]. Tutto ciò avviene, quando faccio un racconto a memoria”.", CONF),
                ("*Intus haec ago, in aula ingenti memoriae meae.* (8, 14)", CONF),
                ("“Sono tutte azioni che compio interiormente nell’enorme palazzo della mia memoria”.", CONF),
                ("*Sed quid est oblivio nisi privatio memoriae? Quomodo ergo adest, ut eam meminerim, quando cum adest "
                 "meminisse non possum?* (16, 24)", CONF),
                ("“Ma cos’è l’oblio, se non privazione di memoria? Come dunque può essere presente, affinché lo ricordi, "
                 "se la sua presenza mi rende impossibile ricordare?”.", CONF),
                ("*Magna vis est memoriae, nescio quid horrendum, Deus meus, profunda et infinita multiplicitas; et hoc "
                 "animus est et hoc ego ipse sum.* (17, 26)", CONF),
                ("“La facoltà della memoria è grandiosa. Ispira quasi un senso di terrore, Dio mio, la sua infinita e "
                 "profonda complessità. E ciò è lo spirito, e ciò sono io stesso”.", CONF)]),
    'smart': dict(
        head="^^P. Smart, R. Clowes, J. Krueger, M. Boniface^^, *The Story of Your Life: Large Language Models and "
             "Personal Memory*, in «Review of Philosophy and Psychology», 2026 (DOI 10.1007/s13164-026-00831-1), "
             "pp. 17-20.",
        quotes=[("“Constructivist theories hold that remembering involves the active reconstruction of past events from "
                 "fragmentary traces, background schemas, and current goals. Because this process relies on inference "
                 "rather than literal replay, errors and distortions are a recurring—and perhaps unavoidable—aspect of "
                 "human memory. As Bernstein and Loftus (2009, p. 373) note, “In essence, all memory is false to some "
                 "degree. [...]”” (p. 17).", 'smart2.txt'),
                ("“[...] autobiographical remembering is governed by a dynamic tension between adaptive correspondence "
                 "(the accurate retention of previously encountered information) and self-coherence (the maintenance "
                 "of a meaningful and temporally integrated sense of self). In many cases, they suggest, the system "
                 "privileges coherence: thematic elaborations, reinterpretations, and selective omissions that help "
                 "sustain a stable and intelligible personal identity. [...] If human autobiographical memory "
                 "routinely sacrifices accuracy in favor of coherence, continuity, and psychological well-being, then "
                 "it is at least plausible that some LLM hallucinations might play a similar role in the context of a "
                 "personal memory system” (p. 18).", 'smart2.txt'),
                ("“Ultimately, what matters is not whether LLMs reproduce the past with perfect precision, but whether "
                 "they help users navigate and narrate their lives in ways that support cognitive, emotional, and "
                 "social flourishing. [...] This, we suggested, marks a shift from the notion of lifelogging to life "
                 "narration” (p. 19).", 'smart2.txt'),
                ("“In this sense, an LLM is not simply an entity that helps you navigate the past; it is also the "
                 "co-creator of a shared autobiography. A co-narrator, perhaps, of the story of you” (p. 20).",
                 'smart2.txt')]),
    'possidio': dict(
        head="^^Possidio^^, *Vita di Agostino* (*Vita Augustini*), praef. 5-6 (PL 32), trad. mia.",
        quotes=[("*Nec attingam ea omnia insinuare, quae idem beatissimus Augustinus in suis Confessionum libris de "
                 "semetipso, qualis ante perceptam gratiam fuerit, qualisque iam sumpta viveret, designavit. 6. Hoc enim "
                 "facere voluit, ut ait Apostolus, ne de se quisquam hominum supra quam se esse noverat, aut de se "
                 "auditum fuisset, crederet vel putaret (2 Cor. 12, 6), humilitatis sanctae more utique nihilo fallens, "
                 "sed laudem non suam, sed sui Domini, de propria liberatione ac munere quaerens [...].*",
                 'poss.html'),
                ("“Né mi soffermerò su tutto ciò che il beatissimo Agostino ha detto di sé nei libri delle *Confessioni*, "
                 "quale fosse prima di ricevere la grazia e come vivesse dopo averla ricevuta. Volle infatti farlo, come "
                 "dice l’Apostolo, perché nessuno lo credesse o lo stimasse più di quanto sapeva che egli era o di "
                 "quanto aveva sentito dire di lui, secondo il costume di una santa umiltà e senza ingannare in nulla, "
                 "cercando non la propria lode ma quella del suo Signore per la sua liberazione e per il dono "
                 "ricevuto [...]”.", None)],
        comment=("Testo latino dell’ed. Migne (PL 32, da Wikisource): riscontrare sull’ed. critica di A. A. R. "
                 "Bastiaensen (Fondazione Valla – Mondadori 1975), dove c’è anche la traduzione di C. Carena, da preferire "
                 "eventualmente alla mia.")),
    'zanotti': dict(
        head="^^G. Zanotti, D. Chiffi^^, *Artificial Afterlife: Philosophical Reflections on Griefbots*, in A. Sans "
             "Pinillos, V. Costa, J. Vallverdú (eds.), *SecondDeath: Experiences of Death Across Technologies*, "
             "Springer, Cham 2025.",
        quotes=[],
        comment="Capitolo ad accesso riservato (record IRIS del Politecnico di Milano): pagine e citazione da aggiungere."),
    'conf11': dict(
        head="^^Agostino^^, *Confessioni* (*Confessiones*, 397-401/403), XI, 20, 26, tr. it. di C. Carena, Nuova "
             "Biblioteca Agostiniana I, Città Nuova.",
        quotes=[("*[...] fortasse proprie diceretur: tempora sunt tria, praesens de praeteritis, praesens de praesentibus, "
                 "praesens de futuris. Sunt enim haec in anima tria quaedam et alibi ea non video, praesens de "
                 "praeteritis memoria, praesens de praesentibus contuitus, praesens de futuris exspectatio.*", CONF),
                ("“Forse sarebbe esatto dire che i tempi sono tre: presente del passato, presente del presente, presente "
                 "del futuro. Queste tre specie di tempi esistono in qualche modo nell’animo e non le vedo altrove: il "
                 "presente del passato è la memoria, il presente del presente la visione, il presente del futuro "
                 "l’attesa”.", CONF)]),
    'kind': dict(
        head="^^A. Kind^^, *Biometrics and the metaphysics of personal identity*, in «IET Biometrics», 12/3 (2023), "
             "pp. 176-182 (DOI 10.1049/bme2.12062).",
        quotes=[],
        comment="Articolo open access, non scaricabile in automatico: citazione da aggiungere."),
    'turkle': dict(
        head="^^S. Turkle^^, *Connected, but alone?*, conferenza TED2012, Long Beach, febbraio 2012 "
             "(www.ted.com/talks/sherry_turkle_connected_but_alone).",
        quotes=[],
        comment=("Nella newsletter del 24.04.26 l’effetto Goldilocks era attribuito ad Alone Together; secondo le fonti "
                 "che ho trovato, la formula è nel TED talk del 2012. Non ho potuto scaricare la trascrizione: "
                 "riscontrare e, se vuoi, citare il passo.")),
    'aiact': dict(
        head="Regolamento (UE) 2024/1689 del Parlamento europeo e del Consiglio del 13 giugno 2024 che stabilisce regole "
             "armonizzate sull’intelligenza artificiale (*AI Act*), art. 50, par. 2.",
        quotes=[("“I fornitori di sistemi di IA, compresi i sistemi di IA per finalità generali, che generano contenuti "
                 "audio, immagine, video o testuali sintetici, garantiscono che gli output del sistema di IA siano "
                 "marcati in un formato leggibile meccanicamente e rilevabili come generati o manipolati "
                 "artificialmente. I fornitori garantiscono che le loro soluzioni tecniche siano efficaci, "
                 "interoperabili, solide e affidabili nella misura in cui ciò sia tecnicamente possibile [...]”.",
                 'aiact.html')]),
    'demelas': dict(
        head="^^D. Demelas^^, *Responsible AI and the Middle Ages: Detecting Historical Toxicity in Medieval Datasets*, "
             "in «Digital Humanities Quarterly», 20/3 (2026).",
        quotes=[("“European medieval literature contains, among other things, virulent Islamophobic and antisemitic "
                 "rhetoric and calls for assaulting and mass-murdering non-Christians. Nineteenth-century scientific "
                 "texts propagate theories of biological racism. Colonial documents normalise slavery and genocide and "
                 "defend European supremacy over other populations. [...] These datasets capture contemporary "
                 "expressions of toxicity but fail to recognize historical forms of hate speech, particularly when "
                 "expressed in formal or literary language. This is why medieval poetry and philosophical treatises "
                 "pose a distinctive problem for automated detection: their discriminatory content is encoded through "
                 "epic lines, theological argument, and chivalric convention rather than through the direct, informal "
                 "slurs on which the models were trained [...]. “Tous furent occis ou faits chrétiens” (All were killed "
                 "or made Christians) scores below 0.02 in every category”.", 'dhq.txt')]),
    'payen': dict(
        head="^^J.-Ch. Payen^^, *Une poétique du génocide joyeux: devoir de violence et plaisir de tuer dans la Chanson "
             "de Roland*, in «Olifant», 6/3-4 (1979), pp. 226-236.",
        quotes=[],
        comment="Dati bibliografici dalla bibliografia di Demelas (DHQ 20.3)."),
    'ep93': dict(
        head="^^Agostino^^, *Lettera* 93 (a Vincenzo rogatista, 407 o 408), 5, 17 e 2, 5, tr. it. Nuova Biblioteca "
             "Agostiniana XXI, Città Nuova.",
        quotes=[("*Nam mea primitus sententia non erat, nisi neminem ad unitatem Christi esse cogendum; verbo esse "
                 "agendum, disputatione pugnandum, ratione vincendum [...].* (5, 17)", EP93),
                ("“Dapprima ero del parere che nessuno dovesse essere condotto per forza all’unità di Cristo, ma si "
                 "dovesse agire solo con la parola, combattere con la discussione, convincere con la ragione [...]”.",
                 EP93),
                ("*Putas neminem debere cogi ad iustitiam, cum legas patremfamilias dixisse servis: Quoscumque "
                 "inveneritis cogite intrare [...]; et noveris aliquando furem avertendis pecoribus pabulum spargere, "
                 "et aliquando pastorem flagello ad gregem pecora errantia revocare!* (2, 5)", EP93),
                ("“Tu pensi che nessuno deve essere costretto alla virtù, sebbene tu legga che il padre di famiglia disse "
                 "ai servi: Costringete ad entrare tutti quelli che troverete [...]. Tu pensi così, pur sapendo che "
                 "talora il ladro getta qua e là dell’erba alle pecore per sviarle, mentre talvolta il pastore si serve "
                 "della verga per ricondurre al gregge le pecore traviate”.", EP93)],
        comment="Testo e traduzione dal corpus (NBA / augustinus.it). Verificare il nome del traduttore NBA da indicare."),
}

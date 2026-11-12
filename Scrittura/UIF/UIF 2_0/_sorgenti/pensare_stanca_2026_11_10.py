"""UIF 2.0: inserisce «Pensare stanca. Per fortuna» nel docx rivisto da AB e rinumera l'Antologia.

Parte da «Una intelligenza fantastica 2_0 (revisione 2026-11-10).docx» (revisione di AB) e scrive
«Una intelligenza fantastica 2_0 (revisione 2026-11-10b).docx»:
- testo attuale tutto in nero (le parti barrate sono considerate accettate e vengono rimosse);
- interventi nuovi in rosso (le eliminazioni in rosso barrato), con commenti Word;
- capitolo 10 nuovo, rinumerazione capitoli 11-13, indice, rimandi interni;
- Antologia rinumerata in ordine di prima apparizione, voci nuove, citazioni orfane barrate.
"""
import copy
import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / 'Una intelligenza fantastica 2_0 (revisione 2026-11-10).docx'
OUT = HERE.parent / 'Una intelligenza fantastica 2_0 (revisione 2026-11-10b).docx'
RED = 'FF0000'
AUTH, INIT = 'Claude', 'C'
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'

# ------------------------------------------------------------------ testi
TITOLO = '10. Pensare stanca. Per fortuna'

CAPITOLO = [
    ('p0', "“Di cosa posso sollevarti?”. Nella prima riflessione ho raccontato che è questa la domanda con cui, ogni "
           "mattina, l’app di Claude mi accoglie. È una domanda gentile, e il verbo è scelto con cura: sollevare vuol "
           "dire alleviare, togliere un peso. Ma a pensarci bene è la stessa domanda che, a modo loro, ci hanno rivolto "
           "quasi tutte le tecnologie che abbiamo inventato. La leva e la carrucola ci hanno sollevato dai pesi, il "
           "mulino dalla macina, la locomotiva e l’automobile dalla strada da percorrere a piedi, l’ascensore dalle "
           "scale, la lavatrice da ore di fatica curvi su un lavatoio. Nessuno di noi rimpiange quelle fatiche, e "
           "sarebbe ipocrita farlo: liberarsene ha significato tempo, salute e, per milioni di persone, soprattutto "
           "donne, una vita diversa. Eppure, mentre ci sollevavano, quelle macchine ci hanno insegnato qualcosa su di "
           "noi che non sapevamo, o che non avevamo mai avuto bisogno di sapere."),
    ('sub', "Il bigliettaio e l’autista"),
    ('p0', "All’inizio degli anni Cinquanta un epidemiologo inglese, Jerry Morris, si accorse di un dettaglio negli "
           "autobus a due piani di Londra. Su ogni mezzo lavoravano due uomini: l’autista, che passava la giornata "
           "seduto al volante, e il bigliettaio, che saliva e scendeva le scale centinaia di volte al giorno per "
           "staccare i biglietti ai passeggeri. Stessi turni, stessa città, stesso autobus. Eppure i bigliettai si "
           "ammalavano di cuore molto meno degli autisti e, quando accadeva, in forma meno grave [@A]. Da "
           "quell’osservazione è nata, di fatto, l’epidemiologia dell’attività fisica: l’idea che il movimento, che "
           "per millenni la vita ci aveva imposto senza chiedercelo, fosse una condizione della nostra salute, e che "
           "una vita sollevata dalla fatica potesse diventare, a sua insaputa, una vita più fragile."),
    ('p', "Oggi l’Organizzazione mondiale della sanità stima che quasi un adulto su tre, nel mondo, non raggiunga i "
          "livelli minimi di attività fisica raccomandati [@B]. Non perché siamo diventati pigri per natura, ma perché "
          "il mondo che abbiamo costruito non ci chiede più di muoverci. E la risposta che abbiamo trovato è una delle "
          "invenzioni più curiose della modernità: la palestra. Non che le palestre non esistessero prima (ne "
          "riparleremo tra poco); ma è nell’Ottocento, mentre l’industria toglieva fatica al lavoro, che si cominciano "
          "a costruire luoghi in cui rimetterla. Nel 1811 Friedrich Ludwig Jahn apre a Berlino, nel parco della "
          "Hasenheide, il primo campo di ginnastica all’aperto; nel 1844 nasce a Torino la prima società ginnastica "
          "italiana. Nel Novecento, con il *jogging*, l’aerobica, i centri *fitness*, quei luoghi si moltiplicano fino "
          "a diventare un paesaggio ordinario delle nostre città."),
    ('p', "Vista da fuori, la palestra è un luogo paradossale. Prendiamo la scala mobile per raggiungerla e, una volta "
          "entrati, saliamo per mezz’ora su una macchina che simula una scala. Corriamo su un tapis roulant che non ci "
          "porta da nessuna parte. Solleviamo pesi che non servono a costruire niente e che, finito l’esercizio, "
          "rimettiamo esattamente dove li abbiamo presi. È una fatica deliberatamente inutile, nel senso più preciso "
          "del termine: non produce nulla, se non noi stessi. Ed è proprio per questo, credo, una delle cose più "
          "lucide che abbiamo fatto: abbiamo riconosciuto che lo sforzo che la vita non ci chiedeva più era una parte "
          "di noi, e abbiamo deciso di reintrodurlo artificialmente, per scelta, senza rinunciare a nessuna delle "
          "comodità che ce lo avevano tolto. Nessuno va in palestra per protestare contro l’ascensore."),
    ('p', "C’è in questo una lezione che va oltre la salute del corpo, ed è la stessa che attraversa tutte queste "
          "riflessioni. Non sapevamo quanto il nostro corpo dovesse alla fatica che il mondo gli imponeva finché una "
          "macchina non ce l’ha tolta. La tecnologia ci ha mostrato, per sottrazione, come siamo fatti. Oggi lo sta "
          "facendo con la mente."),
    ('sub', "L’ascensore della mente"),
    ('p0', "Ciò da cui l’IA ci solleva non sono le scale ma il riassunto di un documento, la stesura di una mail, "
           "l’organizzazione di un argomento, la ricerca della parola giusta, il ricordo di ciò che abbiamo letto. Che "
           "una tecnologia possa alleggerire la mente fino a indebolirla non è un timore nuovo. Nel *Fedro* Platone "
           "racconta che il dio egizio Theuth, inventore delle lettere, presentò la scrittura al re Thamus come un "
           "farmaco per la memoria e per la sapienza. Il re rispose che avrebbe prodotto l’effetto contrario: chi "
           "l’avesse imparata avrebbe smesso di esercitare la memoria e, fidandosi di segni esterni, avrebbe ricordato "
           "non da sé ma da fuori; e avrebbe avuto l’apparenza della sapienza, non la sapienza [@C]. La parola con cui "
           "Platone indica la causa di quell’oblio è *ameletesia*: alla lettera, ‘mancanza di esercizio’."),
    ('p', "Platone aveva in parte torto: la scrittura ci ha dato molto più di quanto ci abbia tolto, e nella quinta "
          "riflessione abbiamo visto quanto la memoria esterna dei testi sia stata il ‘compost’ di ogni conoscenza "
          "collettiva. Ma aveva visto con precisione il meccanismo, quello che Stiegler, ripartendo proprio dal "
          "*Fedro*, chiama il carattere ‘farmacologico’ della tecnica: ogni protesi è insieme cura e veleno, perché "
          "solleva una funzione e, sollevandola, la espone al rischio di indebolirsi. La differenza è che le protesi "
          "mentali del passato alleggerivano una funzione alla volta: la scrittura la memoria, la calcolatrice il "
          "calcolo, il navigatore l’orientamento. L’IA, come abbiamo visto parlando di scrittura, può prendere in "
          "carico l’intera catena: ideazione, progettazione, realizzazione e verifica."),
    ('p', "Qualche indizio di che cosa possa succedere comincia ad arrivare. Nel 2025 un gruppo di ricercatori del MIT "
          "Media Lab guidato da Nataliya Kosmyna ha chiesto a un piccolo gruppo di studenti di scrivere brevi saggi in "
          "tre condizioni (da soli, con un motore di ricerca, con ChatGPT), registrandone nel frattempo l’attività "
          "cerebrale. Chi scriveva con l’IA mostrava la connettività neurale più bassa e, pochi minuti dopo aver "
          "consegnato, faticava a citare anche una sola frase del testo che aveva appena firmato; gli autori parlano "
          "di un ‘debito cognitivo’ che si accumula [@D]. È uno studio piccolo, non ancora consolidato, e va preso con "
          "prudenza. Ma descrive con i dati qualcosa che chiunque abbia delegato un testo può sospettare per "
          "esperienza: ciò che non abbiamo attraversato non ci resta."),
    ('p', "Kahneman, del resto, lo aveva spiegato prima che esistessero i modelli linguistici. Il Sistema 2, quello "
          "lento e riflessivo di cui abbiamo parlato a proposito delle immagini, è anche pigro: tra due strade che "
          "portano allo stesso risultato, la mente sceglie quasi sempre quella che costa meno fatica, secondo quella "
          "che Kahneman chiama ‘legge del minimo sforzo’ [26]. Un collaboratore sempre disponibile, che ci solleva da "
          "ogni sforzo nel momento stesso in cui lo avvertiamo, incontra cioè una mente che non chiede di meglio. E, "
          "come abbiamo visto nella riflessione precedente, il passaggio dall’uso alla dipendenza non è graduale: a "
          "un certo punto la catena si chiude, e tornare indietro costa molto più che non esserci arrivati."),
    ('sub', "Difficoltà desiderabili"),
    ('p0', "Chi si allena lo sa: un muscolo cresce solo se gli si chiede un po’ più di quanto riesca a fare "
           "comodamente. La mente non funziona in modo molto diverso. Lo psicologo Robert Bjork ha chiamato "
           "‘difficoltà desiderabili’ quegli ostacoli che rallentano l’apprendimento nel momento in cui avviene ma lo "
           "rendono più profondo e duraturo: richiamare un’informazione a memoria invece di rileggerla, provare a "
           "rispondere prima di vedere la soluzione, distanziare le ripetizioni invece di concentrarle [@F]. Sono "
           "desiderabili perché sono il luogo stesso in cui si impara. La regola che abbiamo incontrato nella "
           "riflessione precedente, *prima pensa e poi chiedi*, è esattamente questo: una difficoltà scelta, che non "
           "rinuncia all’aiuto ma lo fa arrivare dopo lo sforzo, non al suo posto."),
    ('p', "Il problema è che le difficoltà desiderabili non si presentano più da sole. Per secoli è stata la vita a "
          "imporcele, come imponeva le scale al bigliettaio di Londra: per sapere qualcosa bisognava cercarlo, per "
          "scrivere una lettera bisognava trovare le parole, per ricordare un numero di telefono bisognava ripeterlo. "
          "Oggi, come per il corpo, bisogna sceglierle. E sceglierle vuol dire costruire luoghi e tempi in cui "
          "esercitarle: delle palestre."),
    ('sub', "Askesis"),
    ('p0', "L’idea, a dire il vero, è antichissima, e i filosofi la conoscono bene. La parola greca *askesis*, da cui "
           "viene il nostro ‘ascesi’, prima di indicare la disciplina dei monaci indicava l’allenamento degli atleti. E "
           "non è un caso che le due scuole filosofiche più celebri dell’antichità, l’Accademia di Platone e il Liceo "
           "di Aristotele, prendessero il nome da due ginnasi di Atene, né che alcuni dialoghi platonici, come il "
           "*Liside* e il *Carmide*, si svolgano in una palestra, tra giovani che si allenano. Pierre Hadot ha dedicato "
           "pagine bellissime a mostrare che la filosofia antica non era anzitutto una dottrina da imparare ma un "
           "insieme di esercizi spirituali, pratiche quotidiane con cui si lavorava su di sé per diventare capaci di "
           "vedere e di vivere in un altro modo [@G]."),
    ('p', "Seneca, scrivendo all’amico Lucilio, è persino sprezzante con chi passa le giornate a gonfiare i muscoli: al "
          "corpo, dice, bastano esercizi brevi e semplici, la corsa, il salto, qualche peso; ma la mente va esercitata "
          "notte e giorno, perché si nutre di una fatica moderata, e quell’esercizio non lo impediscono né il freddo "
          "né il caldo, e nemmeno la vecchiaia [@H]. Non c’è bisogno di condividere il disprezzo di Seneca per i "
          "muscoli per riconoscere che aveva capito una cosa che oggi torna urgente: anche la mente ha un "
          "allenamento, e quell’allenamento non coincide con lo studio finalizzato a qualcosa. È esercizio, e basta."),
    ('sub', "Ginnastica cognitiva"),
    ('p0', "Se le cose stanno così, la conclusione è meno ovvia di quanto sembri. Non si tratta di rinunciare all’IA, "
           "come non abbiamo rinunciato all’ascensore, né di guardare con sospetto ogni aiuto che ci solleva da un "
           "compito noioso: delegare ciò che sappiamo fare è, come abbiamo visto, un uso legittimo e spesso "
           "intelligente dello strumento. Si tratta piuttosto di riconoscere che, accanto alla delega, ci serve un "
           "tempo in cui fare di proposito ciò che nessuno ci chiede più di fare: una ginnastica cognitiva. Leggere un "
           "testo lungo senza saltare alle conclusioni; seguire un ragionamento che non ci serve a nulla di immediato; "
           "scrivere senza che nessuno renda fluente al posto nostro ciò che stiamo cercando di dire; ricordare invece "
           "di cercare; provare a rispondere prima di chiedere. Sono esercizi che non producono niente, come il tapis "
           "roulant, e proprio per questo funzionano: l’unica cosa che producono siamo noi, un po’ più capaci di quanto "
           "saremmo stati senza."),
    ('p', "Una ginnastica di questo tipo deve essere scelta, perché nessuno ce la imporrà più; ma ha anche bisogno di "
          "luoghi, di tempi e di compagni. Scuole e università, lo abbiamo detto, sono già le nostre palestre, e "
          "dovrebbero esserlo sempre più consapevolmente: non i posti in cui si dimostra di aver prodotto un testo, ma "
          "quelli in cui ci si allena a produrlo. La palestra, però, non può chiudere con gli anni della formazione, "
          "come il bisogno di muoversi non finisce con l’ultima ora di educazione fisica. A ogni età avremo bisogno di "
          "ritagliarci un tempo, anche piccolo, per una fatica mentale che nessuno ci impone; e sarà tanto più "
          "efficace se, come in palestra, la condivideremo con altri, perché persone diverse, davanti alla stessa "
          "domanda, non rispondono mai nello stesso modo, ed è di questa pluralità, come vedremo nella prossima "
          "riflessione, che il pensiero si nutre."),
    ('p', "La palestra non ci ha fatto odiare l’ascensore; ci ha fatto conoscere il nostro corpo. L’augurio è che una "
          "ginnastica cognitiva faccia lo stesso con l’IA: che non ce la faccia temere, ma ci aiuti a conoscere la "
          "nostra mente, scoprendo per sottrazione di quali fatiche è fatta. “Di cosa posso sollevarti?”, mi chiede "
          "ogni mattina Claude. Di molte cose, e gliene sono grato. Non della fatica di pensare, però. Pensare stanca, "
          "come il lavorare nel titolo di Pavese. Per fortuna: è una stanchezza dalla quale, a differenza delle altre, "
          "non conviene essere sollevati, perché è il modo in cui restiamo noi stessi."),
]

# voci nuove: chiave -> (intestazione, [citazioni])
VOCI = {
    '@BER': ("Berengario di Tours, *Rescriptum contra Lanfrannum* (*De sacra coena*), ed. W. H. Beekenkamp, Nijhoff "
             "1941, p. 47, trad. mia.",
             ["Maximi plane cordis est per omnia ad dialecticam confugere, quia confugere ad eam ad rationem est "
              "confugere, quo qui non confugit, cum secundum rationem sit factus ad imaginem dei, suum honorem "
              "reliquit, nec potest renovari de die in diem ad imaginem dei.",
              "“È proprio di un animo grandissimo ricorrere in ogni cosa alla dialettica, perché ricorrere a essa è "
              "ricorrere alla ragione; e chi non vi ricorre, essendo stato fatto a immagine di Dio secondo la ragione, "
              "abbandona il proprio onore e non può rinnovarsi di giorno in giorno a immagine di Dio”."]),
    '@GAITO': ("R. Gaito, A. Bisogno, *Verificare se un testo è umano è inutile*, podcast *What’s Next*, settembre 2026 "
               "(youtu.be/4VpAuIZK5Rg); cfr. R. Gaito, *La ridicola (e pericolosa) caccia alle streghe verso chi usa "
               "l’IA*, agosto 2026 (youtu.be/6VnKuQIhsGw).", []),
    '@ANTH': ("Anthropic, *How Claude’s text watermarking works*, agosto 2026 "
              "(www.anthropic.com/news/claude-text-watermark).",
              ["“A watermark can only determine that Claude was likely involved with the content at some point”."]),
    '@A': ("J. N. Morris et al., *Coronary heart-disease and physical activity of work*, in «The Lancet», 262 (1953), "
           "pp. 1053-1057 e 1111-1120.", []),
    '@B': ("World Health Organization, *Nearly 1.8 billion adults at risk of disease from not doing enough physical "
           "activity*, comunicato del 26 giugno 2024; dati in T. Strain et al., in «The Lancet Global Health», 12 "
           "(2024).", []),
    '@C': ("Platone, *Fedro*, 274c-275b.", []),
    '@D': ("N. Kosmyna et al., *Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for "
           "Essay Writing Task*, arXiv:2506.08872, 2025.", []),
    '@F': ("R. A. Bjork, *Memory and metamemory considerations in the training of human beings*, in J. Metcalfe, "
           "A. P. Shimamura (a c. di), *Metacognition. Knowing about Knowing*, MIT Press 1994, pp. 185-205.", []),
    '@G': ("P. Hadot, *Esercizi spirituali e filosofia antica* (*Exercices spirituels et philosophie antique*, 1981), "
           "Einaudi 1988.", []),
    '@H': ("L. A. Seneca, *Lettere a Lucilio* (*Epistulae morales ad Lucilium*), 15, 2-5.", []),
}

BERENGARIO = (" Lo aveva scritto con grande chiarezza, negli stessi anni e nel corso di un’altra controversia (quella "
              "con Lanfranco di Pavia sull’eucaristia), Berengario di Tours: ricorrere alla dialettica significa "
              "ricorrere alla ragione, e chi non lo fa, essendo stato creato a immagine di Dio proprio in virtù della "
              "ragione, rinuncia al proprio onore [@BER].")


# ------------------------------------------------------------------ utilità XML
def segs(text):
    return [(s, i % 2 == 1) for i, s in enumerate(text.split('*')) if s]


def runs_of(p_el):
    return [r for r in p_el.iter(qn('w:r'))]


def rtext(r):
    return ''.join(t.text or '' for t in r.iter(qn('w:t')))


def ptext(p_el):
    return ''.join(rtext(r) for r in runs_of(p_el))


def is_struck(r):
    rpr = r.find(qn('w:rPr'))
    if rpr is None:
        return False
    for tag in ('w:strike', 'w:dstrike'):
        s = rpr.find(qn(tag))
        if s is not None and s.get(qn('w:val')) not in ('0', 'false', 'off'):
            return True
    return False


def set_preserve(t):
    t.set(XML_SPACE, 'preserve')


def split_run(r, k):
    """divide il run r al carattere k (0 < k < len): restituisce il secondo pezzo, già inserito dopo r"""
    r2 = copy.deepcopy(r)
    for run, first in ((r, True), (r2, False)):
        pos = 0
        for ch in list(run):
            if ch.tag == qn('w:rPr'):
                continue
            if ch.tag == qn('w:t'):
                s = ch.text or ''
                a, b = pos, pos + len(s)
                pos = b
                if first:
                    if a >= k:
                        run.remove(ch)
                    elif b > k:
                        ch.text = s[:k - a]
                        set_preserve(ch)
                else:
                    if b <= k:
                        run.remove(ch)
                    elif a < k:
                        ch.text = s[k - a:]
                        set_preserve(ch)
            else:
                if (first and pos >= k) or (not first and pos < k):
                    run.remove(ch)
    r.addnext(r2)
    return r2


def boundary(p_el, off):
    pos = 0
    for r in runs_of(p_el):
        n = len(rtext(r))
        if pos < off < pos + n:
            split_run(r, off - pos)
            return
        pos += n


def runs_in(p_el, a, b):
    out, pos = [], 0
    for r in runs_of(p_el):
        n = len(rtext(r))
        if n and pos >= a and pos + n <= b:
            out.append(r)
        pos += n
    return out


def run_ending_at(p_el, off):
    pos, last = 0, None
    for r in runs_of(p_el):
        n = len(rtext(r))
        if n:
            pos += n
            if pos == off:
                last = r
            if pos >= off:
                break
    return last


def red_rpr(tpl_rpr, italic=None, strike=False, keep=False):
    rpr = copy.deepcopy(tpl_rpr) if tpl_rpr is not None else None
    if rpr is None:
        from docx.oxml import OxmlElement
        rpr = OxmlElement('w:rPr')
    for tag in ('w:color', 'w:strike', 'w:dstrike') + (() if keep else ('w:i', 'w:iCs', 'w:b', 'w:bCs', 'w:smallCaps')):
        for e in rpr.findall(qn(tag)):
            rpr.remove(e)
    from docx.oxml import OxmlElement
    if italic:
        rpr.append(OxmlElement('w:i'))
    if strike:
        rpr.append(OxmlElement('w:strike'))
    c = OxmlElement('w:color')
    c.set(qn('w:val'), RED)
    rpr.append(c)
    return rpr


def make_runs(text, tpl_rpr, keep=False):
    from docx.oxml import OxmlElement
    out = []
    for s, it in segs(text):
        r = OxmlElement('w:r')
        r.append(red_rpr(tpl_rpr, italic=it, keep=keep))
        t = OxmlElement('w:t')
        t.text = s
        set_preserve(t)
        r.append(t)
        out.append(r)
    return out


def rpr_of(r):
    return None if r is None else r.find(qn('w:rPr'))


def edit(p_el, a, b, new='', strike_old=True, keep=False):
    """sostituisce [a,b) con new in rosso; il vecchio testo resta barrato in rosso (o sparisce)"""
    boundary(p_el, a)
    boundary(p_el, b)
    old = runs_in(p_el, a, b) if b > a else []
    tpl = old[0] if old else (run_ending_at(p_el, a) if run_ending_at(p_el, a) is not None else (runs_of(p_el)[0] if runs_of(p_el) else None))
    tpl_rpr = rpr_of(tpl)
    after = old[-1] if old else run_ending_at(p_el, a)
    if old:
        for r in old:
            if strike_old:
                rp = r.find(qn('w:rPr'))
                new_rp = red_rpr(rp, strike=True, keep=True)
                if rp is not None:
                    r.remove(rp)
                r.insert(0, new_rp)
        if not strike_old:
            after = old[0].getprevious()
            while after is not None and after.tag != qn('w:r'):
                after = after.getprevious()
            anchor_parent, anchor_idx = old[0].getparent(), old[0].getparent().index(old[0])
            for r in old:
                r.getparent().remove(r)
    new_runs = make_runs(new, tpl_rpr, keep=keep) if new else []
    if old and not strike_old:
        for i, nr in enumerate(new_runs):
            anchor_parent.insert(anchor_idx + i, nr)
    elif after is not None:
        for nr in reversed(new_runs):
            after.addnext(nr)
    else:
        ppr = p_el.find(qn('w:pPr'))
        pos = 1 if ppr is not None else 0
        for i, nr in enumerate(new_runs):
            p_el.insert(pos + i, nr)
    return new_runs


def ins_after(p_el, anchor, text, nth=0):
    t = ptext(p_el)
    i = t.find(anchor)
    for _ in range(nth):
        i = t.find(anchor, i + 1)
    assert i >= 0, anchor
    return edit(p_el, i + len(anchor), i + len(anchor), text)


def append(p_el, text):
    return edit(p_el, len(ptext(p_el)), len(ptext(p_el)), text)


def replace(p_el, anchor, old, new, strike_old=True, keep=False):
    t = ptext(p_el)
    i = t.find(anchor)
    assert i >= 0, anchor
    j = t.find(old, i)
    assert j >= 0, old
    return edit(p_el, j, j + len(old), new, strike_old, keep)


def strike_par(p_el):
    t = ptext(p_el)
    edit(p_el, 0, len(t), '')


def new_par_like(tpl_p_el, text, after_el, keep=False):
    from docx.oxml import OxmlElement
    p = OxmlElement('w:p')
    ppr = tpl_p_el.find(qn('w:pPr'))
    if ppr is not None:
        p.append(copy.deepcopy(ppr))
    tr = next((r for r in runs_of(tpl_p_el) if rtext(r).strip()), None)
    for r in make_runs(text, rpr_of(tr), keep=keep):
        p.append(r)
    after_el.addnext(p)
    return p


def blacken(el):
    for c in el.iter(qn('w:color')):
        if (c.get(qn('w:val')) or '').upper() in ('FF0000', 'C00000'):
            c.getparent().remove(c)


# ------------------------------------------------------------------ main
def main():
    doc = Document(str(SRC))
    body = doc.element.body

    # 1) stato attuale: via le parti barrate, tutto in nero
    for r in list(body.iter(qn('w:r'))):
        if is_struck(r):
            r.getparent().remove(r)
    blacken(body)

    # 2) commenti chiusi: 0-1 (Magnifica humanitas n. 90), 4 (Berengario), 6 (catena), 12 (n. 90 verificata)
    chiusi = {'0', '1', '4', '6', '12'}
    for tag in ('w:commentRangeStart', 'w:commentRangeEnd', 'w:commentReference'):
        for e in list(body.iter(qn(tag))):
            if e.get(qn('w:id')) in chiusi:
                par = e.getparent()
                if e.tag == qn('w:commentReference') and par.tag == qn('w:r') and len(par) <= 2:
                    par.getparent().remove(par)
                else:
                    par.remove(e)
    cpart = next(p for p in doc.part.package.parts if str(p.partname) == '/word/comments.xml')
    para_ids = set()
    for c in list(cpart.element):
        if c.get(qn('w:id')) in chiusi:
            for p in c.iter(qn('w:p')):
                pid = p.get('{http://schemas.microsoft.com/office/word/2010/wordml}paraId')
                if pid:
                    para_ids.add(pid)
            cpart.element.remove(c)
    for p in doc.part.package.parts:
        if str(p.partname) in ('/word/commentsExtended.xml', '/word/commentsIds.xml'):
            blob = p.blob.decode('utf-8')
            durable = re.findall(r'<w16cid:commentId w16cid:paraId="(%s)" w16cid:durableId="([0-9A-F]+)"/>'
                                 % '|'.join(para_ids), blob) if para_ids else []
            for pid in para_ids:
                blob = re.sub(r'<w15:commentEx w15:paraId="%s"[^>]*/>' % pid, '', blob)
                blob = re.sub(r'<w16cid:commentId w16cid:paraId="%s"[^>]*/>' % pid, '', blob)
            p._blob = blob.encode('utf-8')
            if durable:
                ext = next(q for q in doc.part.package.parts if str(q.partname) == '/word/commentsExtensible.xml')
                b2 = ext.blob.decode('utf-8')
                for _, d in durable:
                    b2 = re.sub(r'<w16cex:commentExtensible w16cex:durableId="%s"[^>]*/>' % d, '', b2)
                    b2 = re.sub(r'<w16cex:commentExtensible w16cex:durableId="%s"[^>]*>.*?</w16cex:commentExtensible>'
                                % d, '', b2, flags=re.S)
                ext._blob = b2.encode('utf-8')

    P = lambda: doc.paragraphs  # noqa: E731

    def par(needle, exact=False):
        hits = [p for p in P() if (ptext(p._p) == needle if exact else needle in ptext(p._p))]
        assert len(hits) == 1, '%s: %d' % (needle, len(hits))
        return hits[0]

    notes = []  # (runs, testo commento)

    # 3) interventi nel testo
    p = par('cosa stiamo costruendo?')
    r = ins_after(p._p, 'cosa stiamo costruendo?”', ' [@MH]')
    notes.append((r, 'Aggiunto il rimando alla Magnifica humanitas (n. 90), come richiesto: la citazione è ora nella '
                     'voce dell’enciclica che, essendo la prima citata nel libro, diventa la [1].'))
    p = par('il rischio della dipendenza, la memoria')
    ins_after(p._p, 'il rischio della dipendenza,', ' la necessità di allenare il pensiero,')
    p = par('Di cosa posso sollevarti?”; una enciclopedia')
    ins_after(p._p, 'Di cosa posso sollevarti?”', ' (su quel verbo torneremo nella decima riflessione)')

    p = par('dei quali siamo i soli destinatari nel creato.')
    replace(p._p, 'a questo dono dei quali', 'dei quali', 'del quale')
    r = ins_after(p._p, 'siamo i soli destinatari nel creato.', BERENGARIO)
    notes.append((r, 'Berengario, come richiesto. Il passo è nel Rescriptum contra Lanfrannum (c. 1065-1070), dentro la '
                     'controversia eucaristica con Lanfranco: precede di poco il Monologion (1076) di Anselmo, per '
                     'questo «negli stessi anni» e «un’altra controversia». Citazione dall’ed. Beekenkamp, p. 47: '
                     'da riscontrare sull’ed. Huygens (CCCM 84, 1988). Corretto anche «dono dei quali» → «del quale».'))

    p = par('la ridicola caccia alle streghe dice tanto di noi umani')
    t = ptext(p._p)
    j = t.rfind('[•]')
    edit(p._p, j, j + 3, '[@ANTH]', strike_old=False)
    j = ptext(p._p).find('[•]')
    edit(p._p, j, j + 3, '[@GAITO]', strike_old=False)

    p = par('lo stesso studioso che incontreremo nella prossima riflessione')
    replace(p._p, 'che incontreremo nella prossima', 'prossima', 'undicesima')

    p = par('la chiama ‘catena’')
    t = ptext(p._p)
    i = t.find('‘catena’')
    r = edit(p._p, i + len('‘catena’'), i + len('‘catena’'), '')  # nessun cambio: solo ancoraggio
    rr = runs_in(p._p, i, i + len('‘catena’'))
    notes.append((rr, 'Fonte verificata sul corpus agostiniano: Conf. VIII, 5, 10 («Velle meum tenebat inimicus et inde '
                      'mihi catenam fecerat…»; «unde catenam appellavi»). Latino e traduzione in Antologia corrispondono.'))

    fine9 = par('l’unico vaccino che conosciamo si chiama esercizio, e si fa insieme.')
    append(fine9._p, ' Di questo esercizio parliamo nella prossima riflessione.')

    for old, new in (('10. L’ora di pranzo', '11'), ('11. Do you remember?', '12'),
                     ('12. Un po’ di sintesi e un augurio', '13')):
        p = par(old, exact=True)
        edit(p._p, 0, 2, new, strike_old=False, keep=True)

    p = par('La memoria, insomma, non è un deposito ma un’attività')
    append(p._p, ' E, come ogni attività, si indebolisce se non viene esercitata: è il timore che Platone affidava al '
                 'mito di Theuth, del quale abbiamo parlato nella decima riflessione.')
    p = par('l’Agostino-raccontato è già parte dell’identità')
    if not ptext(p._p).rstrip().endswith('.'):
        append(p._p, '.')
    p = par('diventa co-narratore della nostra storia')
    ins_after(p._p, 'co-narratore della nostra storia', ' [46]')
    p = par('le competenze che stiamo delegando.')
    ins_after(p._p, 'le competenze che stiamo delegando.',
              ' Che, come il corpo dopo l’ascensore, anche la mente dopo l’IA ha bisogno di una palestra: non per '
              'rinunciare a ciò che ci solleva, ma per non dimenticare di che cosa siamo fatti.')

    # 4) capitolo nuovo, prima del salto pagina che precede «11. L’ora di pranzo»
    h_next = par('11. L’ora di pranzo', exact=True)._p
    sep = []
    e = h_next.getprevious()
    while e is not None and not ptext(e).strip():
        sep.insert(0, e)
        if e.xpath('.//w:br[@w:type="page"]'):
            break
        e = e.getprevious()
    after_title = []
    e = h_next.getnext()
    while e is not None and not ptext(e).strip():
        after_title.append(e)
        e = e.getnext()
    tpl_p0 = par('Nella quinta riflessione ho raccontato dei quattro candidati')._p
    tpl_p = fine9._p
    tpl_sub = par('Fluenza e voce', exact=True)._p
    tpl_empty = tpl_p0.getnext()
    cursor = sep[0].getprevious()
    for el in sep:
        c = copy.deepcopy(el)
        cursor.addnext(c)
        cursor = c
    title = new_par_like(h_next, TITOLO, cursor, keep=True)
    cursor = title
    for el in after_title:
        c = copy.deepcopy(el)
        cursor.addnext(c)
        cursor = c
    for kind, text in CAPITOLO:
        if kind == 'sub':
            c = copy.deepcopy(tpl_empty)
            cursor.addnext(c)
            cursor = new_par_like(tpl_sub, '*' + text + '*', c)
        else:
            cursor = new_par_like(tpl_p0 if kind == 'p0' else tpl_p, text, cursor)
    c = copy.deepcopy(tpl_empty)
    cursor.addnext(c)
    notes.append((runs_of(title), 'Nuovo capitolo (dal documento di lavoro del 10.11), senza la parte su Phitness e con '
                                  'una conclusione generale sulla ginnastica cognitiva. Kahneman rimanda alla voce già '
                                  'presente; le altre sette voci di Antologia sono nuove e senza citazione: i passi vanno '
                                  'scelti sulle edizioni che usi (Fedro 275a; Seneca, Ep. 15, 5; Hadot).'))

    # 5) indice
    tbl = doc.tables[0]
    rows = tbl.rows
    r9 = next(r for r in rows if r.cells[1].text.strip() == 'Impalcature e protesi')
    new_tr = copy.deepcopy(r9._tr)
    for tc_i, txt in ((0, '10'), (1, 'Pensare stanca. Per fortuna')):
        tc = new_tr.findall(qn('w:tc'))[tc_i]
        ps = tc.findall(qn('w:p'))
        for p_el in ps[1:]:
            tc.remove(p_el)
        p_el = ps[0]
        tpl = rpr_of(next((r for r in runs_of(p_el) if rtext(r)), None))
        for rr in runs_of(p_el):
            rr.getparent().remove(rr)
        for nr in make_runs(txt, tpl, keep=True):
            p_el.append(nr)
    r9._tr.addnext(new_tr)
    for row in doc.tables[0].rows:
        lab = row.cells[0].text.strip()
        tit = row.cells[1].text
        if lab in ('10', '11', '12') and not tit.startswith('Pensare'):
            p_el = row.cells[0].paragraphs[0]._p
            edit(p_el, 0, len(lab), str(int(lab) + 1), strike_old=False, keep=True)

    # 6) Antologia: interventi sulle voci esistenti (numeri ancora vecchi)
    a_head = par('Antologia', exact=True)
    p = par('nn. 12, 14, 204')
    replace(p._p, 'nn. 12, 14, 204', '204', '90')
    strike_par(par('Viviamo in un tempo di notevole cecità')._p)
    n14 = par('Evitiamo parole che umiliano')
    new_par_like(n14._p, '“Siamo chiamati a interrogarci sul grande cantiere della nostra epoca: cosa stiamo '
                         'costruendo?” (n. 90).', n14._p, keep=True)
    p = par('X, 3, 3; 8, 12')
    replace(p._p, 'X, 3, 3; 8, 12', '3, 3; ', '')
    strike_par(par('Et unde sciunt, cum a me ipso')._p)
    strike_par(par('Come poi sapranno, udendo me stesso')._p)
    strike_par(par('Ultimately, what matters is not whether')._p)

    # 7) rinumerazione dei richiami nel testo (ordine di prima apparizione)
    allp = P()
    ai = next(i for i, q in enumerate(allp) if q._p is a_head._p)
    rx = re.compile(r'\[(?:cit\. in )?(\d+|@\w+)\]')
    alias = {'@MH': '20'}
    order = []
    for q in allp[:ai]:
        for m in rx.finditer(ptext(q._p)):
            k = alias.get(m.group(1), m.group(1))
            if k not in order:
                order.append(k)
    newnum = {k: i + 1 for i, k in enumerate(order)}
    for q in allp[:ai]:
        t = ptext(q._p)
        for m in reversed(list(rx.finditer(t))):
            k = alias.get(m.group(1), m.group(1))
            if k.startswith('@') or newnum[k] != int(k) or m.group(1) in alias:
                edit(q._p, m.start(1), m.end(1), str(newnum[k]), strike_old=False, keep=True)

    # 8) Antologia: blocchi, etichette, riordino, voci nuove
    allp = P()
    ai = next(i for i, q in enumerate(allp) if q._p is a_head._p)
    lab = re.compile(r'^\s*\[(\d+)\]')
    starts = [i for i in range(ai + 1, len(allp)) if lab.match(ptext(allp[i]._p))]
    last = starts[-1]
    end = last
    while end + 1 < len(allp) and ptext(allp[end + 1]._p).strip():
        end += 1
    blocks = {}
    for s_i, s in enumerate(starts):
        e_i = starts[s_i + 1] if s_i + 1 < len(starts) else end + 1
        old = lab.match(ptext(allp[s]._p)).group(1)
        blocks[old] = [allp[j]._p for j in range(s, e_i)]
    missing = [k for k in blocks if k not in newnum]
    assert not missing, 'voci senza richiamo: %s' % missing
    tpl_head = blocks['30'][0]
    tpl_quote = blocks['30'][1]
    anchor_after = allp[end]._p.getnext()
    first = blocks['1'][0]
    parent = first.getparent()
    insert_at = parent.index(first)
    all_old = [el for b in blocks.values() for el in b]
    for el in all_old:
        parent.remove(el)
    for k, n in newnum.items():
        if k in blocks:
            h = blocks[k][0]
            m = lab.match(ptext(h))
            if int(m.group(1)) != n:
                edit(h, m.start(1), m.end(1), str(n), strike_old=False, keep=True)
    for k in order:
        if k in blocks:
            els = blocks[k]
        else:
            head, quotes = VOCI[k]
            from docx.oxml import OxmlElement
            h = OxmlElement('w:p')
            h.append(copy.deepcopy(tpl_head.find(qn('w:pPr'))))
            lr = make_runs('[%d]' % newnum[k], rpr_of(runs_of(tpl_head)[0]), keep=True)[0]
            h.append(lr)
            br = OxmlElement('w:r')
            br.append(red_rpr(rpr_of(runs_of(tpl_head)[0])))
            br.append(OxmlElement('w:br'))
            h.append(br)
            tr = next(r for r in runs_of(tpl_head) if 'Hyland' not in rtext(r) and rtext(r) == ', ')
            for nr in make_runs(head, rpr_of(tr)):
                h.append(nr)
            els = [h]
            for qt in quotes:
                qp = OxmlElement('w:p')
                qp.append(copy.deepcopy(tpl_quote.find(qn('w:pPr'))))
                qr = next(r for r in runs_of(tpl_quote) if rtext(r).strip())
                for nr in make_runs(qt, rpr_of(qr)):
                    qp.append(nr)
                els.append(qp)
        for el in els:
            parent.insert(insert_at, el)
            insert_at += 1
    assert anchor_after is None or anchor_after.getparent() is parent

    nuovi = ', '.join('[%d] %s' % (newnum[k], n) for k, n in (('@BER', 'Berengario'), ('@GAITO', 'Gaito'),
                                                              ('@ANTH', 'Anthropic')))
    pens = [newnum[k] for k in ('@A', '@B', '@C', '@D', '@F', '@G', '@H')]
    notes.append((runs_of(a_head._p), (
        'Antologia rinumerata in ordine di prima apparizione: %d voci (erano 51). La Magnifica humanitas diventa la [1] '
        '(prima citazione nel libro, nella Premessa); voci nuove: %s; quelle di «Pensare stanca» sono [%d]-[%d] '
        '(Kahneman rimanda alla voce già esistente, ora [%d]). Barrate le citazioni rimaste senza richiamo dopo i tagli: '
        'Magnifica humanitas n. 204 (oblio e memoria collettiva), Confessioni X, 3, 3 (Agostino e il testimone), Smart '
        'et al. p. 19 (allucinazioni, life narration). Ho lasciato Possidio, praef. 6, che non è più richiamato ma '
        'completa il passo. Nel testo i numeri cambiati sono in rosso; nel cap. 12 ho aggiunto il rimando a Smart et al. '
        'per il «co-narratore».') % (len(order), nuovi, min(pens), max(pens), newnum['26'])))

    # 9) commenti
    for runs, text in notes:
        runs = [r for r in runs if r is not None]
        if not runs:
            continue
        from docx.text.run import Run
        a = Run(runs[0], doc.paragraphs[0])
        b = Run(runs[-1], doc.paragraphs[0])
        doc.add_comment([a, b], text=text, author=AUTH, initials=INIT)

    doc.save(str(OUT))
    print('Scritto:', OUT)
    print('voci:', len(order))


if __name__ == '__main__':
    main()

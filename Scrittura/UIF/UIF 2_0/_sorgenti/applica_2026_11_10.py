"""Applica le integrazioni del 10.11.2026 a UIF 2.0.

- Copia «Una intelligenza fantastica 2_0 (revisione).docx» in «… (revisione 2026-11-10).docx» (l'originale resta intatto)
  e vi inserisce, in rosso e con commenti: caccia alle streghe (cap. 5), cerniera antropologica (cap. 1), frase in Sintesi.
- Scrive il documento di lavoro «2026-11-10_UIF2-phitness-specchio-streghe.docx» con il capitolo Phitness,
  la collocazione, i rimandi, la verifica della posizione di fondo.
Non usa build_uif2.py: il docx 2.0 contiene correzioni fatte a mano dopo l'ultima build.
"""
import copy
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm
from docx.text.paragraph import Paragraph

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrazioni_2026_11_10 as I  # noqa: E402

SRC = HERE.parent / 'Una intelligenza fantastica 2_0 (revisione).docx'
OUT = HERE.parent / 'Una intelligenza fantastica 2_0 (revisione 2026-11-10).docx'
NOTE = HERE.parent / '2026-11-10_UIF2-phitness-specchio-streghe.docx'
RED = RGBColor(0xFF, 0x00, 0x00)
AUTH, INIT = 'Claude', 'C'


def segs(text):
    """'*corsivo*' -> [(testo, italic)]"""
    out = []
    for i, part in enumerate(re.split(r'\*', text)):
        if part:
            out.append((part, i % 2 == 1))
    return out


def add_runs(par, text, template_rpr=None, red=True):
    runs = []
    for t, it in segs(text):
        r = par.add_run(t)
        if template_rpr is not None:
            old = r._r.find(qn('w:rPr'))
            if old is not None:
                r._r.remove(old)
            r._r.insert(0, copy.deepcopy(template_rpr))
        if red:
            r.font.color.rgb = RED
        for s in r._r.findall(qn("w:rPr") + "/" + qn("w:strike")):
            s.getparent().remove(s)
        r.italic = it or None
        runs.append(r)
    return runs


def find(doc, needle):
    hits = [p for p in doc.paragraphs if needle in p.text]
    assert len(hits) == 1, 'ancora "%s": %d paragrafi' % (needle, len(hits))
    return hits[0]


def first_rpr(p):
    for r in p.runs:
        rpr = r._r.find(qn('w:rPr'))
        if rpr is not None and r.text.strip():
            return rpr
    return None


def insert_after(anchor, text):
    """nuovo paragrafo con lo stesso pPr dell'ancora"""
    new = copy.deepcopy(anchor._p)
    for ch in list(new):
        if ch.tag != qn('w:pPr'):
            new.remove(ch)
    anchor._p.addnext(new)
    p = Paragraph(new, anchor._parent)
    runs = add_runs(p, text, first_rpr(anchor))
    return p, runs


def libro():
    doc = Document(str(SRC))
    # 3) caccia alle streghe, cap. 5
    anchor = find(doc, 'Una risposta possibile è che non sia cambiata la pratica ma la sua scala.')
    allruns = []
    for t in I.STREGHE:
        anchor, runs = insert_after(anchor, t)
        allruns += runs
    doc.add_comment([allruns[0], allruns[-1]], text=I.STREGHE_COMMENTO, author=AUTH, initials=INIT)

    # 2) cerniera antropologica, cap. 1 (in coda al paragrafo su Stiegler)
    p = find(doc, 'alla nostra condizione di ‘mancanza originaria’.')
    runs = add_runs(p, I.CAP1_CERNIERA, first_rpr(p))
    doc.add_comment([runs[0], runs[-1]], author=AUTH, initials=INIT, text=(
        'Proposta (posizione di fondo): rende esplicito, subito dopo Stiegler, che la riflessione sulla tecnica è '
        'riflessione antropologica. Vedi il documento di lavoro del 10.11.'))

    # 2) Sintesi
    p = find(doc, 'In questa seconda versione abbiamo visto anche altro.')
    runs = add_runs(p, I.SINTESI_AGGIUNTA, first_rpr(p))
    doc.add_comment([runs[0], runs[-1]], author=AUTH, initials=INIT, text=(
        'Proposta (posizione di fondo): riporta i capitoli nuovi alla tesi dello specchio.'))

    doc.save(str(OUT))
    print('Scritto:', OUT)


# ------------------------------------------------------------------ documento di lavoro
def note():
    d = Document()
    st = d.styles['Normal']
    st.font.name = 'Garamond'
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Garamond')
    st.font.size = Pt(12)
    for s in ('Heading 1', 'Heading 2', 'Heading 3', 'Title'):
        d.styles[s].font.name = 'Garamond'
        d.styles[s].font.color.rgb = RGBColor(0, 0, 0)

    def par(text, indent=False, italic=False, size=None):
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if indent:
            p.paragraph_format.first_line_indent = Cm(1.25)
        for t, it in segs(text):
            r = p.add_run(t)
            r.italic = it or italic or None
            if size:
                r.font.size = Pt(size)
        return p

    def bullet(text):
        p = d.add_paragraph(style='List Bullet')
        for t, it in segs(text):
            r = p.add_run(t)
            r.italic = it or None

    d.add_heading('Una intelligenza fantastica 2.0 — integrazioni del 10 novembre 2026', 0)
    par('Phitness, posizione di fondo, caccia alle streghe. Il testo inserito nel libro è nel file '
        '«Una intelligenza fantastica 2_0 (revisione 2026-11-10).docx», in rosso e con commenti; '
        'l’originale «… 2_0 (revisione).docx» non è stato toccato.', italic=True)

    # ---- 1
    d.add_heading('1. Il capitolo su Phitness', 1)
    d.add_heading('Collocazione', 2)
    par('Lo inserirei come *decima riflessione*, subito dopo «Impalcature e protesi» e prima de «L’ora di pranzo». '
        'Il cap. 9 si chiude sull’esercizio come unico vaccino contro la dipendenza («si chiama esercizio, e si fa '
        'insieme»): Phitness è la risposta concreta a quella chiusa e ne prosegue il lessico (impalcatura, '
        'catena, delega/dipendenza). Dopo, «L’ora di pranzo» riapre sul piano interpretativo, e la chiusa del nuovo '
        'capitolo (la traccia uguale per tutti, risposte plurali) vi conduce. Collocarlo invece in fondo, prima '
        'della Sintesi, lo farebbe sembrare un’appendice promozionale; qui è un passaggio dell’argomento.')
    d.add_heading('Testo', 2)
    d.add_heading(I.PHITNESS_TITOLO, 3)
    for kind, text in I.PHITNESS:
        if kind == 'sub':
            par(text, italic=True)
        else:
            par(text, indent=(kind == 'p'))
    d.add_heading('Antologia: voci proposte', 2)
    for k, ref, nota in I.PHITNESS_ANTOLOGIA:
        par('[%s] %s' % (k, ref))
        par(nota, italic=True, size=10)
    d.add_heading('Rimandi negli altri capitoli', 2)
    t = d.add_table(rows=1, cols=3)
    t.style = 'Table Grid'
    for c, h in zip(t.rows[0].cells, ('Capitolo', 'Dove (testo attuale)', 'Intervento')):
        c.text = h
        c.paragraphs[0].runs[0].bold = True
    for cap, dove, cosa in I.PHITNESS_RIMANDI:
        row = t.add_row().cells
        row[0].text, row[1].text, row[2].text = cap, dove, cosa
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)

    # ---- 2
    d.add_heading('2. La posizione di fondo: la tecnologia come specchio antropologico', 1)
    d.add_heading('Esito della verifica', 2)
    par('La posizione c’è e ricorre spesso, ma non è mai dichiarata come tesi né come metodo. Il lettore la '
        'incontra come una serie di ribaltamenti locali, alla fine dei singoli capitoli, non come la chiave che '
        'tiene insieme il libro. Chi conosce Macchine Pensanti la riconosce; chi apre UIF per la prima volta '
        'rischia di leggerla come una delle tante osservazioni, non come quella da cui tutte le altre discendono.')
    d.add_heading('Dove emerge', 2)
    for b in [
        '*Premessa*: solo un inciso («usarla o, peggio, subirla senza farsi qualche domanda su cosa ci racconti di '
        'noi»). Il libro è giustificato con la vita esaminata di Socrate, non con la tesi dello specchio.',
        '*Cap. 1*: la premessa teorica più forte c’è già (Stiegler, l’*être-en-défaut*, la tecnica che nasce da una '
        'mancanza), ma viene usata per spiegare perché l’IA è un collaboratore, non per fondare il metodo.',
        '*Cap. 2*: la formulazione più netta («quello che diciamo della tecnologia lo stiamo dicendo in fondo di '
        'noi») introduce la risposta di ChatGPT, che finisce per esserne la portavoce; poi «sarebbe come rompere lo '
        'specchio per non vedere il proprio riflesso», «l’IA non crea il problema: lo rivela», la tecnologia come '
        '«strumento di diagnosi». È il passaggio più esplicito del libro.',
        '*Cap. 3*: la struttura è speculare (l’opacità dell’IA rinvia alla nostra), ma il capitolo chiude sul perché '
        'l’IA non ci spaventa, non su che cosa dice di noi.',
        '*Cap. 4*: «dica, ancora una volta, più cose di noi che della macchina»; chiusa sul bisogno umano di narrazioni.',
        '*Cap. 5*: «l’IA smaschera dunque un nostro falso mito» (l’autore totale).',
        '*Cap. 6*: il ribaltamento è implicito (la fiducia nella fotografia è un nostro abito culturale) ma il '
        'capitolo chiude sull’igiene cognitiva. È il capitolo in cui la tesi si vede meno.',
        '*Cap. 7*: «selfie del nostro gusto», «human slop», «abbiamo già provveduto noi ad anestetizzarla».',
        '*Cap. 9*: la sezione «Lo specchio».',
        '*Cap. 10 (L’ora di pranzo)*: «il ribaltamento che ho provato a proporre in ognuna di queste riflessioni»: è '
        'la cosa più vicina a una dichiarazione di metodo, ma arriva tardi ed è legata al tema della neutralità.',
        '*Sintesi*: «riflettere sulla IA significa, inevitabilmente, riflettere su di noi; è anzi questa una delle '
        'opportunità più preziose». Qui la tesi è presentata come un’opportunità offerta dall’IA, non come la '
        'posizione da cui il libro muove.',
    ]:
        bullet(b)
    d.add_heading('Che cosa manca', 2)
    par('Tre cose. La tesi non è enunciata in apertura, quindi il lettore la scopre strada facendo. Prevale la '
        'versione debole (l’IA ci fa da specchio, «ci riflette») sulla versione forte che sostieni in Macchine '
        'Pensanti (pensare la tecnica è già pensare l’essere umano, perché la tecnica nasce da ciò che siamo e da ciò '
        'che ci manca): la base per la versione forte c’è, ed è Stiegler nel cap. 1, ma non viene collegata. Infine, '
        'i capitoli più descrittivi (prima metà del cap. 1, cap. 6, parte del cap. 10) chiudono sulla tecnologia o '
        'sull’etica dell’uso, e non sul ritorno all’umano.')
    d.add_heading('Proposte', 2)
    par('*a) Premessa*, dopo il paragrafo su Socrate e la *Magnifica humanitas*. Non l’ho inserita nel docx perché la '
        'Premessa dichiara di essere integralmente tua: va riscritta con parole tue. Una traccia:')
    par('«' + I.PREMESSA_PROPOSTA + '»', italic=True)
    par('*b) Cap. 1*, in coda al paragrafo su Stiegler e Prometeo (*inserita in rosso*):')
    par('«' + I.CAP1_CERNIERA.strip() + '»', italic=True)
    par('*c) Sintesi*, in coda al paragrafo «In questa seconda versione…» (*inserita in rosso*):')
    par('«' + I.SINTESI_AGGIUNTA.strip() + '»', italic=True)
    par('*d) Cap. 6*, in chiusura, dopo «…perfino le lettere d’amore.» (*non inserita*):')
    par('«' + I.CAP6_PROPOSTA + '»', italic=True)
    par('*e)* Il capitolo su Phitness e il passo sulla caccia alle streghe sono costruiti entrambi su questa tesi: '
        'la palestra come scoperta per sottrazione di come è fatto il corpo, il rilevatore di IA come «ritratto di una '
        'comunità che ha smesso di fidarsi della propria capacità di leggere».')

    # ---- 3
    d.add_heading('3. La caccia alle streghe', 1)
    par('*Dove*: cap. 5 («Un’altra specie simbolica (che scrive)»), tre paragrafi nuovi subito dopo quello in rosso '
        'su scala, Pangram e *AI Act*, e prima di «Come sempre fanno le rivoluzioni tecnologiche, l’IA smaschera…». La '
        'sequenza diventa: il ghostwriting democratizzato → i rilevatori → la caccia alle streghe e ciò che dice di noi '
        '→ il falso mito dell’autore totale. Il terzo paragrafo prepara Cyrano (cap. 8) e l’impalcatura (cap. 9).')
    par('*Fonti*: la puntata di *What’s Next* con Raffaele Gaito (youtu.be/4VpAuIZK5Rg, titolo YouTube «Verificare se '
        'un testo è umano è inutile»), il tuo post «Streghe, macchine e tesi di laurea» (25.09.26), le Note del 15-24 '
        'agosto (Pangram, filigrana di Anthropic, Gaito, Camerino, «costruire la nostra voce»).')
    par('*Da verificare*: il video non l’ho potuto ascoltare, quindi il testo si basa sul post e sulle Note, non '
        'sulla trascrizione. Se la scarichi da YouTube Studio, avvicino il passo alle parole della puntata. Da '
        'ricontrollare anche la citazione dalla pagina di Anthropic sulla filigrana, presa dalla tua Nota del 17.08. Le '
        'due voci di Antologia sono nel commento Word, con il segnaposto [•]: inserendole dopo la [24], le voci '
        'successive slittano di due.')

    d.save(str(NOTE))
    print('Scritto:', NOTE)


if __name__ == '__main__':
    libro()
    note()

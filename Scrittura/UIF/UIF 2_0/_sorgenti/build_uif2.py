"""Costruisce «Una intelligenza fantastica 2_0 (revisione).docx» a partire dal docx 1.2.

- sposta «L'ora di pranzo» dopo «Rossana, Cristiano e Cyrano» e rinumera i capitoli;
- inserisce i capitoli nuovi (4, 9, 11) e le integrazioni (contenuti.py);
- tutto il testo nuovo è in rosso; il testo eliminato in rosso barrato; le motivazioni sono commenti Word;
- rinumera i rimandi [n] in ordine di apparizione e riordina l'Antologia (nuove voci in antologia_nuova.py);
- verifica le citazioni delle nuove voci sui testi delle fonti (cartella FONTI, se disponibile) e sul corpus agostiniano.

Uso: python3 build_uif2.py
"""
import html
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path
from xml.dom import minidom

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from docxlib import Par, Seg, Comments, markup_segs, GARAMOND  # noqa: E402
import contenuti as C  # noqa: E402
from antologia_nuova import VOCI  # noqa: E402

REPO = HERE.parents[3]
SRC = REPO / 'Scrittura/UIF/UIF 1_2/Una intelligenza fantastica 1_2.docx'
OUT = HERE.parent / 'Una intelligenza fantastica 2_0 (revisione).docx'
CORPUS = REPO / 'Università/Ricerca/Agostino strumenti/Agostino testi'
FONTI = Path(os.environ.get('UIF_FONTI', '/private/tmp/claude-501/-Users-macbook-Library-CloudStorage-Dropbox-ClaudeWS/'
                                         'e1d34e39-b203-44c3-99e1-f9d3ab0a1d19/scratchpad/src'))

COMMENTS = Comments()


# ------------------------------------------------------------------ verifica citazioni
def norm(s):
    return ''.join(c for c in s.lower() if c.isalnum())


def load_source(spec):
    if spec.startswith('corpus:'):
        p = CORPUS / spec[7:]
        return [p.read_text(encoding='utf-8')] if p.exists() else None
    p = FONTI / spec
    if not p.exists():
        return None
    raw = p.read_text(encoding='utf-8', errors='ignore')
    if spec.endswith('.html'):
        stripped = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', raw, flags=re.S)
        stripped = html.unescape(re.sub(r'<[^>]+>', ' ', stripped))
        return [stripped, html.unescape(raw)]
    return [raw]


def verify_quotes():
    log = []
    ok = True
    for key, v in VOCI.items():
        for q, src in v['quotes']:
            if not src:
                log.append('%-12s TRADUZIONE MIA (non verificabile in automatico): %s…' % (key, q[:50]))
                continue
            texts = load_source(src)
            if texts is None:
                log.append('%-12s FONTE NON DISPONIBILE (%s): verifica saltata' % (key, src))
                continue
            body = q.replace('*', '')
            body = re.sub(r'\s*\((?:p|n)\.\s*\d+\)\.?\s*$', '', body)
            body = re.sub(r'\s*\(\d+, \d+\)\s*$', '', body)
            frags = [f for f in (norm(x) for x in body.split('[...]')) if len(f) >= 8]
            found = False
            for t in texts:
                nt = norm(t)
                pos = 0
                good = True
                for f in frags:
                    i = nt.find(f, pos)
                    if i < 0:
                        good = False
                        break
                    pos = i + len(f)
                if good:
                    found = True
                    break
            log.append('%-12s %s: %s…' % (key, 'OK' if found else 'NON TROVATA', q[:60]))
            ok &= found
    (HERE / 'verifica_citazioni.txt').write_text('\n'.join(log) + '\n', encoding='utf-8')
    if not ok:
        print('\n'.join(l for l in log if 'NON TROVATA' in l))
        raise SystemExit('Citazioni non verificate: vedi verifica_citazioni.txt')
    print('Citazioni verificate:', sum('OK' in l for l in log), '| non verificabili:',
          sum('TRADUZIONE' in l or 'NON DISPONIBILE' in l for l in log))


# ------------------------------------------------------------------ paragrafi nuovi
def ppr(indent=False, italic=False):
    return ('<w:pPr>' + ('<w:ind w:firstLine="720"/>' if indent else '') + '<w:jc w:val="both"/><w:rPr>' + GARAMOND +
            ('<w:i/><w:iCs/>' if italic else '') + '</w:rPr></w:pPr>')


def new_par(kind, text):
    if kind == 'empty':
        return Par('<w:p>' + ppr() + '</w:p>')
    p = Par('<w:p>' + ppr(indent=(kind == 'p'), italic=(kind == 'sub')) + '</w:p>')
    p.segs = markup_segs('*' + text + '*' if kind == 'sub' else text, {'rFonts': GARAMOND}, 'ins')
    return p


def blocks_to_pars(blocks):
    out = []
    for b in blocks:
        kind, text = b[0], b[1]
        if kind == 'sub':
            out.append(new_par('empty', ''))
        p = new_par(kind, text)
        if len(b) > 2 and b[2]:
            p.comment_all(COMMENTS.add(b[2]))
        out.append(p)
    return out


# ------------------------------------------------------------------ main
def is_break(xml):
    return '<w:sectPr' in xml or 'w:type="page"' in xml


def text_of(xml):
    return html.unescape(''.join(re.findall(r'<w:t\b[^>]*>([^<]*)</w:t>', xml)))


def main():
    verify_quotes()
    z = zipfile.ZipFile(SRC)
    files = {n: z.read(n) for n in z.namelist()}
    doc = files['word/document.xml'].decode('utf-8')
    assert 'word/comments.xml' not in files
    head = doc[:doc.index('<w:body>') + len('<w:body>')]
    tail = doc[doc.rindex('</w:body>'):]
    body = doc[len(head):-len(tail)]
    els = re.findall(r'<w:p[ >].*?</w:p>|<w:p/>|<w:tbl>.*?</w:tbl>|<w:sectPr.*?</w:sectPr>', body, re.S)
    assert abs(sum(map(len, els)) - len(body)) < 200

    def title_idx(start):
        hits = [i for i, e in enumerate(els) if 'w:val="Titolo1"' in e and text_of(e).startswith(start)]
        assert len(hits) == 1, (start, hits)
        return hits[0]

    def block_start(ti):
        j = ti - 1
        while not is_break(els[j]):
            j -= 1
        return j + 1

    t4, t8, t7, t9, ta = (title_idx(s) for s in ('4. Un', '8. L', '7. Rossana', '9. Un po', 'Antologia'))
    b4, b8, b7, b9 = (block_start(t) for t in (t4, t8, t7, t9))
    assert b4 < b8 < b7 < b9 < ta

    # modello di blocco capitolo nuovo
    prefix = els[b4:t4]                    # righe vuote prima del titolo
    title_tpl = els[t4]
    after_title = els[t4 + 1:t4 + 3]
    page_break = next(e for e in els[b9 - 3:b9] if 'w:type="page"' in e)

    def chapter(spec):
        t = Par(title_tpl)
        t.segs = markup_segs(spec['titolo'], {'sz': '<w:sz w:val="28"/>', 'szCs': '<w:szCs w:val="28"/>',
                                              'lang': '<w:lang w:val="it-IT"/>'}, 'ins')
        t.comment_all(COMMENTS.add(spec['commento']))
        return list(prefix) + [t] + list(after_title) + blocks_to_pars(spec['blocchi']) + \
            [new_par('empty', ''), page_break]

    order = (els[:b4] + chapter(C.DIO_PROMPT) + els[b4:b8] + els[b7:b9] + chapter(C.IMPALCATURE) +
             els[b8:b7] + chapter(C.MEMORIA) + els[b9:])

    # parse di tutti i paragrafi
    items = [Par(e) if isinstance(e, str) and e.startswith('<w:p') and e.endswith('</w:p>') else e for e in order]

    def pars_with(anchor):
        return [i for i, it in enumerate(items) if isinstance(it, Par) and anchor in it.text()]

    def one(anchor):
        hits = pars_with(anchor)
        assert len(hits) == 1, 'ancora "%s": %d paragrafi' % (anchor, len(hits))
        return hits[0]

    # legenda generale
    legend = next(i for i, it in enumerate(items) if isinstance(it, Par) and it.text().strip() == 'Una intelligenza fantastica')
    items[legend].comment_all(COMMENTS.add(
        'UIF 2.0 – versione di revisione preparata da Claude Code (09.11.2026). Legenda: testo in rosso = nuovo o '
        'modificato; rosso barrato = da eliminare; i commenti spiegano le scelte e segnalano ciò che resta da '
        'verificare. Capitoli nuovi: 4, 9, 11. «L’ora di pranzo» è stata spostata dopo «Rossana, Cristiano e Cyrano» '
        '(nella 1.2 era prima, contro l’indice). Le citazioni delle nuove voci dell’Antologia sono state confrontate '
        'automaticamente con le fonti: esito in _sorgenti/verifica_citazioni.txt. Impaginazione (pagine bianche, '
        'interruzioni di sezione) da ricontrollare in Word.'))

    # commento sulla citazione della Premessa
    i = one('cosa stiamo costruendo?')
    p = items[i]
    pos = p.text().index('cosa stiamo costruendo?') + len('cosa stiamo costruendo?')
    j = p.split_at(pos)
    cid = COMMENTS.add('Citazione verificata: Magnifica humanitas, n. 90. Se vuoi, aggiungi il rimando all’Antologia.')
    from docxlib import comment_end
    p.segs[j:j] = comment_end(cid)
    p.segs.insert(p.split_at(p.text().index('Siamo chiamati')), Seg('o', raw='<w:commentRangeStart w:id="%d"/>' % cid))

    # rinumerazione titoli
    for start, old, new in (('4. Un’altra', '4', '5'), ('5. Non fidarsi', '5', '6'), ('6. Vieni avanti', '6', '7'),
                            ('7. Rossana', '7', '8'), ('8. L’ora di pranzo', '8', '10'), ('9. Un po’', '9', '12')):
        hits = [k for k, it in enumerate(items) if isinstance(it, Par) and it.text().startswith(start)
                and 'Titolo1' in it.ppr]
        assert len(hits) == 1, start
        items[hits[0]].replace(old, new, show_deleted=True, occurrence=0)

    # modifiche puntuali
    for e in C.EDITS:
        k = one(e['anchor'])
        cid = COMMENTS.add(e['comment']) if e.get('comment') else None
        if e.get('kind') == 'ins':
            items[k].insert_after(e['after'], e['new'], cid)
        else:
            items[k].replace(e['old'], e['new'], cid)

    # paragrafi nuovi
    for e in C.NEW_PARS:
        k = one(e['anchor'])
        new = blocks_to_pars(e['blocks'])
        new[0].comment_all(COMMENTS.add(e['comment']))
        items[k + 1:k + 1] = new

    # sezione nuova nel cap. 10
    k = [i for i, it in enumerate(items) if isinstance(it, Par) and it.text().strip() == C.MALE_SCRITTO_BENE['before']]
    assert len(k) == 1
    k = k[0]
    # stile del cap. 10: paragrafi senza rientro separati da una riga vuota
    new = []
    for kind, text in C.MALE_SCRITTO_BENE['blocks']:
        new += [new_par('empty', ''), new_par('sub' if kind == 'sub' else 'p0', text)]
    new[1].comment_all(COMMENTS.add(C.MALE_SCRITTO_BENE['comment']))
    new = new[:2] + new[3:]  # niente riga vuota tra titoletto e primo paragrafo
    items[k:k] = new + [new_par('empty', '')]

    # ---------------------------------------------------------- indice
    rebuild_index(items)

    # ---------------------------------------------------------- rimandi e Antologia
    ta = [i for i, it in enumerate(items) if isinstance(it, Par) and 'Titolo1' in it.ppr and it.text() == 'Antologia'][0]
    tp = [i for i, it in enumerate(items) if isinstance(it, Par) and 'Titolo1' in it.ppr and it.text() == 'Premessa'][0]
    REF = re.compile(r'\[(?:cit\. in )?(\d+)\]|\[@(\w+)\]')
    numbering = {}
    for it in items[tp:ta]:
        if isinstance(it, Par):
            for m in REF.finditer(it.text()):
                key = 'old' + m.group(1) if m.group(1) else m.group(2)
                numbering.setdefault(key, len(numbering) + 1)
    for it in items[tp:ta]:
        if not isinstance(it, Par):
            continue
        for m in reversed(list(REF.finditer(it.text()))):
            if m.group(1):
                n = numbering['old' + m.group(1)]
                if str(n) != m.group(1):
                    it.replace(m.group(1), str(n), show_deleted=False, occurrence=m.start(1))
            else:
                it.replace(m.group(0), '[%d]' % numbering[m.group(2)], show_deleted=False, occurrence=m.start())
    missing = [k for k in numbering if not k.startswith('old') and k not in VOCI]
    assert not missing, missing

    # blocchi dell'Antologia esistente
    end = next(i for i in range(ta + 1, len(items)) if not isinstance(items[i], Par) or 'w:type="page"' in items[i].xml())
    region = items[ta + 1:end]
    starts = [i for i, it in enumerate(region) if isinstance(it, Par) and re.match(r'\s*\[\d+\]', it.text())]
    lead = region[:starts[0]]
    old_blocks = {}
    for a, b in zip(starts, starts[1:] + [len(region)]):
        n = int(re.match(r'\s*\[(\d+)\]', region[a].text()).group(1))
        old_blocks['old%d' % n] = region[a:b]
    new_region = list(lead)
    for key, n in sorted(numbering.items(), key=lambda kv: kv[1]):
        if key.startswith('old'):
            blk = old_blocks.pop(key)
            first = blk[0]
            m = re.match(r'\s*\[(\d+)\]', first.text())
            if int(m.group(1)) != n:
                first.replace(m.group(1), str(n), show_deleted=False, occurrence=m.start(1))
            new_region += blk
        else:
            new_region += antologia_voce(n, VOCI[key])
    for key, blk in old_blocks.items():   # voci non più richiamate
        blk[0].comment_all(COMMENTS.add('Voce non richiamata nel testo: decidere se eliminarla.'))
        new_region += blk
    unused = [k for k in VOCI if k not in numbering]
    assert not unused, unused
    items[ta + 1:end] = new_region
    first_cid = COMMENTS.add('Rimandi rinumerati in ordine di apparizione: i numeri cambiati sono in rosso. '
                             'Voci nuove: %d. Totale voci: %d.' % (sum(not k.startswith('old') for k in numbering),
                                                                    len(numbering)))
    items[ta].comment_all(first_cid)

    # ---------------------------------------------------------- scrittura
    new_body = ''.join(it.xml() if isinstance(it, Par) else it for it in items)
    docxml = head + new_body + tail
    files['word/document.xml'] = docxml.encode('utf-8')
    files['word/comments.xml'] = COMMENTS.xml().encode('utf-8')
    ct = files['[Content_Types].xml'].decode('utf-8')
    ct = ct.replace('</Types>', '<Override PartName="/word/comments.xml" ContentType="application/'
                    'vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/></Types>')
    files['[Content_Types].xml'] = ct.encode('utf-8')
    rels = files['word/_rels/document.xml.rels'].decode('utf-8')
    rels = rels.replace('</Relationships>', '<Relationship Id="rIdUIF2Comments" Type="http://schemas.openxmlformats.org/'
                        'officeDocument/2006/relationships/comments" Target="comments.xml"/></Relationships>')
    files['word/_rels/document.xml.rels'] = rels.encode('utf-8')
    minidom.parseString(files['word/document.xml'])
    minidom.parseString(files['word/comments.xml'])
    tmp = OUT.with_suffix('.tmp')
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        zo.writestr('[Content_Types].xml', files.pop('[Content_Types].xml'))
        for n, data in files.items():
            zo.writestr(n, data)
    shutil.move(tmp, OUT)
    print('Scritto:', OUT)
    print('Commenti:', len(COMMENTS.items), '| voci Antologia:', len(numbering))


def antologia_voce(n, v):
    base = {'sz': '<w:sz w:val="24"/>', 'szCs': '<w:szCs w:val="24"/>', 'lang': '<w:lang w:val="it-IT"/>'}
    ppr_head = ('<w:pPr><w:pStyle w:val="CSP-ChapterBodyText-FirstParagraph"/><w:snapToGrid w:val="0"/>'
                '<w:spacing w:before="240"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="it-IT"/></w:rPr></w:pPr>')
    ppr_q = ('<w:pPr><w:pStyle w:val="CSP-ChapterBodyText-FirstParagraph"/><w:snapToGrid w:val="0"/>'
             '<w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="it-IT"/></w:rPr></w:pPr>')
    h = Par('<w:p>' + ppr_head + '</w:p>')
    bold = dict(base, b='<w:b/>', bCs='<w:bCs/>')
    h.segs = [Seg('t', '[%d]' % n, bold, 'ins'), Seg('x', rpr=bold, fmt='ins', raw='<w:br/>')] + \
        markup_segs(v['head'], base, 'ins')
    if v.get('comment'):
        h.comment_all(COMMENTS.add(v['comment']))
    out = [h]
    for q, _src in v['quotes']:
        p = Par('<w:p>' + ppr_q + '</w:p>')
        p.segs = markup_segs(q, base, 'ins')
        out.append(p)
    return out


def rebuild_index(items):
    k = [i for i, it in enumerate(items) if isinstance(it, str) and it.startswith('<w:tbl>') and 'Empatia canaglia' in it]
    assert len(k) == 1
    k = k[0]
    tbl = items[k]
    rows = re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S)
    pre = tbl[:tbl.index(rows[0])]
    post = tbl[tbl.rindex(rows[-1]) + len(rows[-1]):]

    def cells(row):
        return [Par(p) for p in re.findall(r'<w:p\b.*?</w:p>', row, re.S)]

    by_title = {}
    for r in rows:
        cs = cells(r)
        by_title[cs[1].text().strip()] = r   # l'ultima riga contiene anche «Antologia»
    want = [('', 'Premessa'), ('1', 'Un (fantastico) collaboratore magico'), ('2', 'Empatia canaglia'),
            ('3', 'Black box naturali'), ('4', 'Dio prompt'), ('5', 'Un’altra specie simbolica (che scrive)'),
            ('6', 'Non fidarsi (delle immagini) è meglio?'), ('7', 'Vieni avanti creativo'),
            ('8', 'Rossana, Cristiano e Cyrano'), ('9', 'Impalcature e protesi'), ('10', 'L’ora di pranzo'),
            ('11', 'Do you remember?'), ('12', 'Un po’ di sintesi e un augurio')]
    tpl = by_title['Empatia canaglia']
    new_rows = []
    for num, title in want:
        if title in by_title:
            r = by_title[title]
            ps = re.findall(r'<w:p\b.*?</w:p>', r, re.S)
            if num:
                pn = Par(ps[0])
                if pn.text().strip() != num:
                    pn.replace(pn.text().strip(), num, show_deleted=False, occurrence=pn.text().index(pn.text().strip()))
                    r = r.replace(ps[0], pn.xml(), 1)
            new_rows.append(r)
        else:
            ps = re.findall(r'<w:p\b.*?</w:p>', tpl, re.S)
            r = tpl
            for p_xml, txt in zip(ps, (num, title)):
                p = Par(p_xml)
                base = next((s.rpr for s in p.segs if s.kind == 't'), {})
                p.segs = markup_segs(txt, base, 'ins')
                r = r.replace(p_xml, p.xml(), 1)
            new_rows.append(r)
    missing = [t for t in by_title if t not in [w[1] for w in want] and t]
    assert not missing, ('righe di indice non riconosciute', missing)
    items[k] = pre + ''.join(new_rows) + post


if __name__ == '__main__':
    main()

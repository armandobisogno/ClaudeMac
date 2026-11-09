"""Strumenti minimi per modificare il document.xml di UIF a livello di paragrafo.

Modello: ogni paragrafo è una lista di segmenti.
  - 't'  testo dentro un run (con il suo rPr)
  - 'x'  elemento non testuale dentro un run (br, tab, drawing...), con il suo rPr
  - 'o'  elemento fuori dai run (proofErr, bookmark, hyperlink, commenti...)
Le modifiche lavorano sul testo "appiattito" del paragrafo e spezzano i run dove serve.
Formattazione delle revisioni: 'ins' = rosso; 'del' = rosso barrato.
"""
import re
import html

RED = "FF0000"

RPR_ORDER = ['rStyle', 'rFonts', 'b', 'bCs', 'i', 'iCs', 'caps', 'smallCaps', 'strike', 'dstrike',
             'outline', 'shadow', 'emboss', 'imprint', 'noProof', 'snapToGrid', 'vanish', 'webHidden',
             'color', 'spacing', 'w', 'kern', 'position', 'sz', 'szCs', 'highlight', 'u', 'effect',
             'bdr', 'shd', 'fitText', 'vertAlign', 'rtl', 'cs', 'em', 'lang', 'eastAsianLayout',
             'specVanish', 'oMath']

GARAMOND = '<w:rFonts w:ascii="Garamond" w:eastAsia="Garamond" w:hAnsi="Garamond" w:cs="Garamond"/>'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def parse_rpr(inner):
    d = {}
    pos = 0
    while pos < len(inner):
        m = re.compile(r'<w:(\w+)\b[^>]*?/>|<w:(\w+)\b[^>]*>.*?</w:\2>', re.S).match(inner, pos)
        if not m:
            pos += 1
            continue
        tag = m.group(1) or m.group(2)
        d[tag] = m.group(0)
        pos = m.end()
    return d


def build_rpr(d):
    out = [d[t] for t in RPR_ORDER if t in d] + [v for k, v in d.items() if k not in RPR_ORDER]
    return '<w:rPr>' + ''.join(out) + '</w:rPr>' if out else ''


def with_fmt(rpr, fmt):
    d = dict(rpr)
    if fmt in ('ins', 'del'):
        d['color'] = '<w:color w:val="%s"/>' % RED
    if fmt == 'del':
        d['strike'] = '<w:strike/>'
    return d


class Seg:
    __slots__ = ('kind', 'text', 'rpr', 'fmt', 'raw')

    def __init__(self, kind, text='', rpr=None, fmt=None, raw=''):
        self.kind, self.text, self.rpr, self.fmt, self.raw = kind, text, rpr or {}, fmt, raw

    def copy(self):
        return Seg(self.kind, self.text, dict(self.rpr), self.fmt, self.raw)


TOKEN = re.compile(
    r'<w:r\b[^>]*/>'
    r'|<w:r\b[^>]*>.*?</w:r>'
    r'|<w:hyperlink\b[^>]*>.*?</w:hyperlink>'
    r'|<w:(?:smartTag|sdt|fldSimple|ins|del)\b[^>]*>.*?</w:(?:smartTag|sdt|fldSimple|ins|del)>'
    r'|<w:\w+\b[^>]*/>'
    r'|<w:(\w+)\b[^>]*>.*?</w:\1>', re.S)

RUNCHILD = re.compile(r'<w:t\b[^>]*/>|<w:t\b[^>]*>(.*?)</w:t>|<w:\w+\b[^>]*/>|<w:(\w+)\b[^>]*>.*?</w:\2>', re.S)


class Par:
    def __init__(self, xml):
        m = re.match(r'(<w:p\b[^>]*>)(.*)</w:p>\s*$', xml, re.S)
        if not m:
            raise ValueError('non è un paragrafo: ' + xml[:80])
        self.open = m.group(1)
        inner = m.group(2)
        self.ppr = ''
        if inner.startswith('<w:pPr>'):
            end = inner.index('</w:pPr>') + len('</w:pPr>')
            self.ppr, inner = inner[:end], inner[end:]
        self.segs = []
        pos = 0
        while pos < len(inner):
            mm = TOKEN.match(inner, pos)
            if not mm:
                raise ValueError('token non riconosciuto: ' + inner[pos:pos + 120])
            tok = mm.group(0)
            pos = mm.end()
            if tok.startswith('<w:r>') or tok.startswith('<w:r '):
                if tok.endswith('/>') and '</w:r>' not in tok:
                    continue
                body = re.match(r'<w:r\b[^>]*>(.*)</w:r>$', tok, re.S).group(1)
                rpr = {}
                if body.startswith('<w:rPr>'):
                    e = body.index('</w:rPr>')
                    rpr = parse_rpr(body[7:e])
                    body = body[e + 8:]
                p2 = 0
                while p2 < len(body):
                    c = RUNCHILD.match(body, p2)
                    if not c:
                        raise ValueError('figlio di run: ' + body[p2:p2 + 80])
                    p2 = c.end()
                    if c.group(0).startswith('<w:t>') or c.group(0).startswith('<w:t '):
                        txt = html.unescape(c.group(1) or '')
                        if txt:
                            self.segs.append(Seg('t', txt, rpr))
                    elif c.group(0).startswith('<w:t/>'):
                        continue
                    else:
                        self.segs.append(Seg('x', rpr=rpr, raw=c.group(0)))
            else:
                self.segs.append(Seg('o', raw=tok))

    # --- testo
    def text(self):
        return ''.join(s.text for s in self.segs if s.kind == 't')

    def split_at(self, pos):
        """Garantisce un confine di segmento alla posizione pos; restituisce l'indice del segmento che inizia lì."""
        acc = 0
        for i, s in enumerate(self.segs):
            if s.kind != 't':
                continue
            if acc == pos:
                return i
            if acc < pos < acc + len(s.text):
                a = s.copy()
                b = s.copy()
                a.text, b.text = s.text[:pos - acc], s.text[pos - acc:]
                self.segs[i:i + 1] = [a, b]
                return i + 1
            acc += len(s.text)
        if acc == pos:
            # fine paragrafo: dopo l'ultimo segmento di testo
            last = max([i for i, s in enumerate(self.segs) if s.kind == 't'], default=len(self.segs) - 1)
            return last + 1
        raise IndexError(pos)

    def rpr_at(self, idx):
        for s in self.segs[idx:]:
            if s.kind == 't':
                return dict(s.rpr)
        for s in reversed(self.segs[:idx]):
            if s.kind == 't':
                return dict(s.rpr)
        return {'rFonts': GARAMOND}

    def replace(self, old, new, comment_id=None, show_deleted=True, occurrence=None):
        t = self.text()
        if occurrence is None:
            n = t.count(old)
            if n != 1:
                raise ValueError('"%s" trovato %d volte nel paragrafo: %s' % (old, n, t[:100]))
            a = t.index(old)
        else:
            a = occurrence
        b = a + len(old)
        i = self.split_at(a)
        j = self.split_at(b)
        base = self.rpr_at(i)
        base.pop('i', None)
        base.pop('iCs', None)
        base.pop('strike', None)
        base.pop('color', None)
        newsegs = markup_segs(new, base, 'ins') if new else []
        if show_deleted:
            for s in self.segs[i:j]:
                if s.kind == 't':
                    s.fmt = 'del'
            self.segs[j:j] = newsegs
        else:
            # elimina solo il testo: commenti, segnalibri ecc. restano dove sono
            keep = [s for s in self.segs[i:j] if s.kind != 't']
            self.segs[i:j] = newsegs + keep
            j = i
        if comment_id is not None:
            end = j + len(newsegs)
            self.segs[end:end] = comment_end(comment_id)
            self.segs[i:i] = [Seg('o', raw='<w:commentRangeStart w:id="%d"/>' % comment_id)]

    def insert_after(self, anchor, new, comment_id=None):
        t = self.text()
        if t.count(anchor) != 1:
            raise ValueError('ancora "%s" trovata %d volte' % (anchor, t.count(anchor)))
        pos = t.index(anchor) + len(anchor)
        j = self.split_at(pos)
        base = self.rpr_at(j - 1 if j > 0 else j)
        for k in ('i', 'iCs', 'strike', 'color'):
            base.pop(k, None)
        newsegs = markup_segs(new, base, 'ins')
        self.segs[j:j] = newsegs
        if comment_id is not None:
            end = j + len(newsegs)
            self.segs[end:end] = comment_end(comment_id)
            self.segs[j:j] = [Seg('o', raw='<w:commentRangeStart w:id="%d"/>' % comment_id)]

    def comment_all(self, comment_id):
        first = next((i for i, s in enumerate(self.segs) if s.kind in 't x'), len(self.segs))
        self.segs.append(None)  # placeholder per calcolo
        self.segs.pop()
        self.segs.extend(comment_end(comment_id))
        self.segs.insert(first, Seg('o', raw='<w:commentRangeStart w:id="%d"/>' % comment_id))

    def xml(self):
        out = [self.open, self.ppr]
        for s in self.segs:
            if s.kind == 'o':
                out.append(s.raw)
            elif s.kind == 'x':
                out.append('<w:r>' + build_rpr(with_fmt(s.rpr, s.fmt)) + s.raw + '</w:r>')
            else:
                out.append('<w:r>' + build_rpr(with_fmt(s.rpr, s.fmt)) +
                           '<w:t xml:space="preserve">' + esc(s.text) + '</w:t></w:r>')
        out.append('</w:p>')
        return ''.join(out)


def comment_end(cid):
    return [Seg('o', raw='<w:commentRangeEnd w:id="%d"/>' % cid),
            Seg('o', raw='<w:r><w:rPr><w:rStyle w:val="Rimandocommento"/></w:rPr>'
                         '<w:commentReference w:id="%d"/></w:r>' % cid)]


def markup_segs(text, base_rpr, fmt):
    """*corsivo*, ^^maiuscoletto^^, ** non usato. Restituisce segmenti di testo."""
    segs = []
    italic = False
    small = False
    for tok in re.split(r'(\*|\^\^)', text):
        if tok == '*':
            italic = not italic
            continue
        if tok == '^^':
            small = not small
            continue
        if not tok:
            continue
        r = dict(base_rpr)
        if italic:
            r['i'] = '<w:i/>'
            r['iCs'] = '<w:iCs/>'
        if small:
            r['smallCaps'] = '<w:smallCaps/>'
        segs.append(Seg('t', tok, r, fmt))
    if italic or small:
        raise ValueError('marcatura non chiusa: ' + text[:80])
    return segs


class Comments:
    def __init__(self, author='Claude', initials='CL', date='2026-11-09T21:00:00Z'):
        self.items = []
        self.author, self.initials, self.date = author, initials, date

    def add(self, text):
        cid = len(self.items)
        self.items.append(text)
        return cid

    def xml(self):
        out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
               '<w:comments xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">']
        for cid, text in enumerate(self.items):
            out.append('<w:comment w:id="%d" w:author="%s" w:date="%s" w:initials="%s">' %
                       (cid, self.author, self.date, self.initials))
            for k, para in enumerate(text.split('\n')):
                out.append('<w:p>')
                if k == 0:
                    out.append('<w:r><w:annotationRef/></w:r>')
                out.append('<w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % esc(para))
            out.append('</w:comment>')
        out.append('</w:comments>')
        return ''.join(out)

#!/usr/bin/env python3
"""Genera un .docx secondo le Norme redazionali Ledizioni (volume EUG), usando come stampo
un docx già impaginato (stili, margini 17x24 su A4, piè di pagina con numero).

Sintassi del sorgente:
  @title Titolo            titolo del capitolo (Arial 14 grassetto)
  @author by Nome          autore (Arial 12 corsivo)
  ## 1. Titolo             paragrafo (Arial 12 grassetto)
  > testo                  citazione in blocco (TNR 10, interlinea 12)
  @references              inizia la bibliografia («References»)
  @bibhead Sources         sottotitolo della bibliografia (Arial grassetto corsivo)
  *corsivo*  {{nota a piè di pagina}}
Uso: python3 build_ledizioni.py sorgente.txt stampo.docx output.docx
"""
import re, sys, zipfile
from xml.sax.saxutils import escape

def runs(text, extra=''):
    out, ital = [], False
    for tok in re.split(r'(\*)', text):
        if tok == '*': ital = not ital; continue
        if not tok: continue
        rpr = extra + ('<w:i/>' if ital else '')
        rpr = f'<w:rPr>{rpr}</w:rPr>' if rpr else ''
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(tok)}</w:t></w:r>')
    return ''.join(out)

class Doc:
    def __init__(self):
        self.body, self.notes = [], []

    def inline(self, text, extra=''):
        xml = []
        for i, part in enumerate(re.split(r'\{\{(.*?)\}\}', text)):
            if i % 2 == 0:
                xml.append(runs(part, extra))
            else:
                self.notes.append(part)
                xml.append('<w:r><w:rPr><w:sz w:val="16"/><w:vertAlign w:val="superscript"/></w:rPr>'
                           f'<w:footnoteReference w:id="{len(self.notes)}"/></w:r>')
        return ''.join(xml)

    def p(self, ppr, content):
        self.body.append(f'<w:p>{"<w:pPr>" + ppr + "</w:pPr>" if ppr else ""}{content}</w:p>')

ARIAL = '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'

def build(src, template, out):
    lines = open(src, encoding='utf8').read().split('\n')
    d, first_head, in_bib, buf = Doc(), True, False, []

    def flush():
        if not buf: return
        text = ' '.join(buf).strip(); buf.clear()
        if in_bib:
            d.p('<w:ind w:left="283" w:hanging="283"/>', d.inline(text, '<w:sz w:val="18"/><w:szCs w:val="18"/>'))
        else:
            d.p('<w:ind w:firstLine="283"/><w:jc w:val="both"/>', d.inline(text))

    for ln in lines:
        s = ln.rstrip()
        if not s.strip():
            flush(); continue
        if s.startswith('@title '):
            flush(); d.p('', runs(s[7:], ARIAL + '<w:b/><w:sz w:val="28"/><w:szCs w:val="28"/>'))
            d.p('<w:jc w:val="both"/>', '')
        elif s.startswith('@author '):
            flush(); d.p('', runs(s[8:], ARIAL + '<w:i/>'))
        elif s.startswith('## '):
            flush()
            sp = '<w:spacing w:after="276"/>' if first_head else '<w:spacing w:before="552" w:after="276"/>'
            first_head = False
            d.p('<w:keepNext/>' + sp, runs(s[3:], ARIAL + '<w:b/>'))
        elif s.startswith('> '):
            flush()
            d.p('<w:spacing w:before="240" w:after="240" w:line="240" w:lineRule="exact"/><w:ind w:firstLine="283"/><w:jc w:val="both"/>',
                d.inline(s[2:], '<w:sz w:val="20"/><w:szCs w:val="20"/>'))
        elif s.startswith('@references'):
            flush(); in_bib = True
            d.p('<w:keepNext/><w:spacing w:before="552" w:after="276"/>', runs('References', ARIAL + '<w:b/>'))
        elif s.startswith('@bibhead '):
            flush()
            d.p('<w:keepNext/><w:spacing w:before="552" w:after="276"/>', runs(s[9:], ARIAL + '<w:b/><w:i/>'))
        else:
            buf.append(s.strip())
    flush()

    zin = zipfile.ZipFile(template)
    docxml = zin.read('word/document.xml').decode('utf8')
    head = docxml[:docxml.index('<w:body>') + len('<w:body>')]
    sect = re.search(r'<w:sectPr.*?</w:sectPr>', docxml, re.S).group(0)
    new_doc = head + ''.join(d.body) + sect + '</w:body></w:document>'

    fnxml = zin.read('word/footnotes.xml').decode('utf8')
    fhead = fnxml[:fnxml.index('<w:footnote ')]
    seps = ''.join(re.findall(r'<w:footnote w:type="(?:continuationSeparator|separator)".*?</w:footnote>', fnxml, re.S))
    small = '<w:sz w:val="18"/><w:szCs w:val="18"/>'
    notes = ''.join(
        f'<w:footnote w:id="{i}"><w:p><w:pPr><w:ind w:firstLine="283"/><w:jc w:val="both"/></w:pPr>'
        '<w:r><w:rPr><w:sz w:val="16"/><w:vertAlign w:val="superscript"/></w:rPr><w:footnoteRef/></w:r>'
        + runs(' ' + n, small) + '</w:p></w:footnote>'
        for i, n in enumerate(d.notes, 1))
    new_fn = fhead + seps + notes + '</w:footnotes>'

    title = next((l[7:] for l in lines if l.startswith('@title ')), '').replace('*', '')
    author = next((l[8:] for l in lines if l.startswith('@author ')), '')
    author = re.sub(r'^by ', '', author)

    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml': data = new_doc.encode('utf8')
            elif item.filename == 'word/footnotes.xml': data = new_fn.encode('utf8')
            elif item.filename == 'docProps/core.xml':
                c = data.decode('utf8')
                c = re.sub(r'<dc:title>.*?</dc:title>|<dc:title/>', f'<dc:title>{escape(title)}</dc:title>', c)
                c = re.sub(r'<dc:creator>.*?</dc:creator>|<dc:creator/>', f'<dc:creator>{escape(author)}</dc:creator>', c)
                data = c.encode('utf8')
            zout.writestr(item, data)

    body_txt = open(src, encoding='utf8').read().split('@references')[0]
    txt = re.sub(r'\{\{.*?\}\}', '', body_txt, flags=re.S)
    txt = re.sub(r'^(@title |@author |## |> )', '', txt, flags=re.M).replace('*', '')
    print(f'{out}: {len(d.notes)} note; caratteri (spazi inclusi) testo {len(txt.strip())}, '
          f'note {sum(len(n) for n in d.notes)}')

if __name__ == '__main__':
    build(*sys.argv[1:4])

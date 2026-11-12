#!/usr/bin/env python3
"""Genera un .docx secondo le «Instructions for Authors» della rivista «Itinera» (Univ. di Milano).

Norme applicate: A4; Times New Roman 12, giustificato, interlinea 1,5; note 10 giustificate;
margini 3 cm; numero di pagina in basso al centro; titolo 16 grassetto centrato, due righe vuote,
poi nome ed email dell'autore; titoli di paragrafo in grassetto tondo allineati a sinistra,
una riga vuota prima e 6 pt dopo; rientro di prima riga 0,5 cm tranne il primo paragrafo di
ogni sezione e il paragrafo dopo una citazione in blocco; citazioni in blocco corpo 10,
rientrate 1 cm a destra e a sinistra, senza virgolette.

Sintassi del sorgente:
  @title Titolo           @author Nome      @email indirizzo
  ## 1. Titolo            titolo di paragrafo
  > testo                 citazione in blocco
  @bibliography           inizia la bibliografia (file separato richiesto dalla rivista)
  @plain                  documento semplice (abstract, dati autore): solo paragrafi
  *corsivo*  ~~apice~~  {{nota a piè di pagina}}
Uso: python build_itinera.py sorgente.txt output.docx
"""
import re, sys, zipfile
from xml.sax.saxutils import escape

CM = 567
FONT = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'

def runs(text, size, base_italic=False, bold=False):
    out, ital, sup = [], False, False
    for tok in re.split(r'(\*|~~)', text):
        if tok == '*': ital = not ital; continue
        if tok == '~~': sup = not sup; continue
        if not tok: continue
        rpr = FONT + ('<w:b/>' if bold else '') + ('<w:i/>' if ital ^ base_italic else '')
        if sup: rpr += '<w:vertAlign w:val="superscript"/>'
        rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        out.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(tok)}</w:t></w:r>')
    return ''.join(out)

class Doc:
    def __init__(self): self.body, self.notes = [], []
    def inline(self, text, size, italic=False, bold=False):
        xml = []
        for i, p in enumerate(re.split(r'\{\{(.*?)\}\}', text)):
            if i % 2 == 0: xml.append(runs(p, size, italic, bold))
            else:
                self.notes.append(p)
                xml.append(f'<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="{len(self.notes)}"/></w:r>')
        return ''.join(xml)
    def para(self, text, *, size=24, jc='both', first=0, left=0, right=0, line=360, before=0, after=0, bold=False, keep=False):
        ppr = f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
        ppr += f'<w:ind w:left="{left}" w:right="{right}" w:firstLine="{first}"/><w:jc w:val="{jc}"/>'
        if keep: ppr += '<w:keepNext/>'
        self.body.append(f'<w:p><w:pPr>{ppr}</w:pPr>{self.inline(text, size, False, bold)}</w:p>')
    def blank(self): self.body.append('<w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="auto"/></w:pPr></w:p>')

def build(src, dst):
    d = Doc()
    lines = open(src, encoding='utf-8').read().split('\n')
    plain = any(l.strip() == '@plain' for l in lines)
    indent_next, bib = False, False
    for ln in lines:
        s = ln.strip()
        if not s or s == '@plain': continue
        if s.startswith('@title '):
            d.para(s[7:], size=32, jc='center', bold=True); d.blank(); d.blank()
        elif s.startswith('@author '):
            d.para(s[8:] + ',', jc='left')
        elif s.startswith('@email '):
            d.para(s[7:], jc='left'); d.blank(); d.blank(); indent_next = False
        elif s.startswith('@bibliography'):
            bib = True
        elif s.startswith('## '):
            if d.body: d.blank()
            d.para(s[3:], jc='left', bold=True, after=120, keep=True); indent_next = False
        elif s.startswith('> '):
            d.para(s[2:], size=20, left=CM, right=CM, line=240, before=120, after=120); indent_next = False
        elif bib:
            d.para(s, jc='left', after=120)
        else:
            d.para(s, first=284 if indent_next else 0); indent_next = True

    sect = (f'<w:sectPr><w:footerReference w:type="default" r:id="rIdF1"/>'
            f'<w:footnotePr><w:numFmt w:val="decimal"/></w:footnotePr><w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="{3*CM}" w:right="{3*CM}" w:bottom="{3*CM}" w:left="{3*CM}" w:header="{int(1.25*CM)}" w:footer="{int(1.5*CM)}" w:gutter="0"/></w:sectPr>')
    NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{"".join(d.body)}{sect}</w:body></w:document>'
    fn = ['<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>',
          '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>']
    for i, n in enumerate(d.notes, 1):
        ppr = '<w:pPr><w:pStyle w:val="FootnoteText"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
        ref = '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/><w:sz w:val="20"/></w:rPr><w:footnoteRef/></w:r>'
        fn.append(f'<w:footnote w:id="{i}"><w:p>{ppr}{ref}{runs(" " + n, 20)}</w:p></w:footnote>')
    footnotes = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:footnotes {NS}>{"".join(fn)}</w:footnotes>'
    r = f'<w:rPr>{FONT}<w:sz w:val="20"/></w:rPr>'
    footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}><w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
              f'<w:r>{r}<w:fldChar w:fldCharType="begin"/></w:r><w:r>{r}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
              f'<w:r>{r}<w:fldChar w:fldCharType="separate"/></w:r><w:r>{r}<w:t>1</w:t></w:r><w:r>{r}<w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')
    styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="it-IT"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="FootnoteText"><w:name w:val="footnote text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="FootnoteReference"><w:name w:val="footnote reference"/><w:rPr><w:vertAlign w:val="superscript"/></w:rPr></w:style>
</w:styles>'''
    settings = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings {NS}><w:footnotePr><w:footnote w:id="-1"/><w:footnote w:id="0"/></w:footnotePr><w:defaultTabStop w:val="709"/><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>'
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
          '<Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>'
          '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rIdSet" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
             '<Relationship Id="rIdFn" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/>'
             '<Relationship Id="rIdF1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>')
    title = next((l[7:] for l in lines if l.startswith('@title ')), '')
    author = next((l[8:] for l in lines if l.startswith('@author ')), 'Armando Bisogno')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>' + escape(title) + '</dc:title><dc:creator>' + escape(author) + '</dc:creator></cp:coreProperties>')
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in [('[Content_Types].xml', ct), ('_rels/.rels', rels), ('word/document.xml', document),
                           ('word/styles.xml', styles), ('word/settings.xml', settings), ('word/footnotes.xml', footnotes),
                           ('word/footer1.xml', footer), ('word/_rels/document.xml.rels', drels), ('docProps/core.xml', core)]:
            z.writestr(name, data)
    clean = lambda s: re.sub(r'[*~]|\{\{|\}\}', '', s)
    body = [l for l in lines if l.strip() and not l.startswith('@')]
    text = clean(re.sub(r'\{\{.*?\}\}', '', '\n'.join(body)))
    notes = clean(' '.join(d.notes))
    print(f'{dst}: {len(d.notes)} note; caratteri spazi inclusi: testo {len(text)}, note {len(notes)}, totale {len(text) + len(notes)}')

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])

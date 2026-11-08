#!/usr/bin/env python3
"""Genera un .docx secondo le «Norme redazionali» (Ricerca/Norme editoriali.doc) da un sorgente testuale.

Sintassi del sorgente:
  @author Nome            autore (centrato, maiuscoletto)
  @title Titolo           titolo (14, grassetto, maiuscolo, centrato)
  ## 1. Titolo            paragrafo (13, maiuscoletto, centrato)
  ### 1.1 Titolo          sottoparagrafo (12, corsivo, allineato a sinistra con rientro)
  > testo                 citazione infratestuale (11, interlinea singola, rientro sx 2 cm)
  @bibliography           inizia la bibliografia finale
  @bibhead Fonti          sottotitolo della bibliografia
  *corsivo*  ^^maiuscoletto^^  {{testo della nota a piè di pagina}}
Uso: python3 build_paper.py sorgente.txt output.docx
"""
import re, sys, zipfile
from xml.sax.saxutils import escape

CM = 567  # twip per cm

def runs(text, size, base_italic=False):
    """Converte *corsivo* e ^^maiuscoletto^^ in <w:r>."""
    out, ital, sc = [], False, False
    for tok in re.split(r'(\*|\^\^)', text):
        if tok == '*': ital = not ital; continue
        if tok == '^^': sc = not sc; continue
        if not tok: continue
        rpr = f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        if ital ^ base_italic: rpr += '<w:i/>'
        if sc: rpr += '<w:smallCaps/>'
        rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        out.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(tok)}</w:t></w:r>')
    return ''.join(out)

class Doc:
    def __init__(self):
        self.body, self.notes = [], []

    def inline(self, text, size, italic=False):
        parts = re.split(r'\{\{(.*?)\}\}', text)
        xml = []
        for i, p in enumerate(parts):
            if i % 2 == 0:
                xml.append(runs(p, size, italic))
            else:
                self.notes.append(p)
                nid = len(self.notes)
                xml.append(f'<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="{nid}"/></w:r>')
        return ''.join(xml)

    def para(self, text, *, size=24, jc='both', first=709, left=0, line=360, before=0, after=0,
             italic=False, bold=False, caps=False, smallcaps=False, keep=False):
        ppr = f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
        ppr += f'<w:ind w:left="{left}" w:firstLine="{first}"/><w:jc w:val="{jc}"/>'
        if keep: ppr += '<w:keepNext/>'
        r = self.inline(text, size, italic)
        if bold: r = r.replace('<w:rPr>', '<w:rPr><w:b/>')
        if caps: r = r.replace('<w:rPr>', '<w:rPr><w:caps/>')
        if smallcaps: r = r.replace('<w:rPr>', '<w:rPr><w:smallCaps/>')
        self.body.append(f'<w:p><w:pPr>{ppr}</w:pPr>{r}</w:p>')

def build(src, dst):
    d, bib = Doc(), False
    lines = open(src, encoding='utf-8').read().split('\n')
    for ln in lines:
        s = ln.strip()
        if not s: continue
        if s.startswith('@author '):
            d.para(s[8:], jc='center', first=0, smallcaps=True, after=240)
        elif s.startswith('@title '):
            d.para(s[7:], size=28, jc='center', first=0, bold=True, caps=True, before=240, after=480)
        elif s.startswith('@bibliography'):
            bib = True
            d.para('Bibliografia', size=26, jc='center', first=0, smallcaps=True, before=720, after=480, keep=True)
        elif s.startswith('@bibhead '):
            d.para(s[9:], jc='left', first=0, italic=True, before=240, after=240, keep=True)
        elif s.startswith('### '):
            d.para(s[4:], jc='left', first=709, italic=True, before=480, after=240, keep=True)
        elif s.startswith('## '):
            bib = False  # un titolo di paragrafo dopo la bibliografia la chiude (es. «Versione italiana»)
            d.para(s[3:], size=26, jc='center', first=0, smallcaps=True, before=720, after=480, keep=True)
        elif s.startswith('> '):
            d.para(s[2:], size=22, first=0, left=2 * CM, line=240, before=240, after=240)
        elif bib:
            d.para(s, first=0, line=240, after=120)
        else:
            d.para(s)

    sect = (f'<w:sectPr><w:headerReference w:type="default" r:id="rIdH1"/>'
            f'<w:footnotePr><w:numFmt w:val="decimal"/></w:footnotePr>'
            f'<w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="{int(2.5*CM)}" w:right="{2*CM}" w:bottom="{2*CM}" w:left="{2*CM}" '
            f'w:header="{int(1.25*CM)}" w:footer="{int(1.25*CM)}" w:gutter="0"/><w:titlePg/></w:sectPr>')
    NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{"".join(d.body)}{sect}</w:body></w:document>'

    fn = [f'<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>',
          f'<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>']
    for i, n in enumerate(d.notes, 1):
        ppr = f'<w:pPr><w:pStyle w:val="FootnoteText"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:firstLine="709"/><w:jc w:val="both"/></w:pPr>'
        ref = '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>'
        sp = runs(' ', 20)
        fn.append(f'<w:footnote w:id="{i}"><w:p>{ppr}{ref}{sp}{runs(n, 20)}</w:p></w:footnote>')
    footnotes = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:footnotes {NS}>{"".join(fn)}</w:footnotes>'

    header = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}><w:p><w:pPr><w:jc w:val="right"/></w:pPr>'
              '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
              '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
              '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
              '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr><w:t>2</w:t></w:r>'
              '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r></w:p></w:hdr>')

    styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="it-IT"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
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
          '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rIdSet" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
             '<Relationship Id="rIdF" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/>'
             '<Relationship Id="rIdH1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/></Relationships>')
    title = next((l[7:] for l in lines if l.startswith('@title ')), '')
    author = next((l[8:] for l in lines if l.startswith('@author ')), '')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>' + escape(title) + '</dc:title><dc:creator>' + escape(author) + '</dc:creator></cp:coreProperties>')
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', document); z.writestr('word/styles.xml', styles)
        z.writestr('word/settings.xml', settings); z.writestr('word/footnotes.xml', footnotes)
        z.writestr('word/header1.xml', header); z.writestr('word/_rels/document.xml.rels', drels)
        z.writestr('docProps/core.xml', core)
    words = len(re.sub(r'\{\{.*?\}\}', '', ' '.join(lines)).split())
    print(f'{dst}: {len(d.notes)} note, ~{words} parole nel testo, ~{sum(len(n.split()) for n in d.notes)} nelle note')

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])

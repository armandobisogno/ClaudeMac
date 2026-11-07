#!/usr/bin/env python3
"""Genera un .docx secondo le norme redazionali della Call «Il soggetto nei luoghi del capitale-potere
contemporaneo» (DdP/Call for Papers.pdf). Riusa il motore di build_paper.py cambiando solo la gabbia.

Norme: A4, margini 4 cm; Times New Roman; interlinea 1,15; titolo 14 centrato; sommario e abstract 10
giustificati in grassetto, parole chiave in corsivo; corpo 12 giustificato, rientro prima riga 1 cm,
nessuna spaziatura tra paragrafi; titoli di paragrafo 12 grassetto giustificati; citazioni in blocco 10,
margini sx/dx 1 cm e rientro 1 cm; bibliografia 10 giustificata; note 10; un solo a capo vuoto tra le parti.

Sintassi del sorgente:
  @title Titolo   @author Nome   @abstract testo   @keywords testo
  ## Titolo di paragrafo   > citazione in blocco   @bibliography
  *corsivo*  {{nota a piè di pagina}}
Uso: python3 build_capitale_potere.py sorgente.txt output.docx
"""
import re, sys, zipfile
sys.path.insert(0, __import__('os').path.dirname(__file__))
import build_paper as bp
from xml.sax.saxutils import escape

CM, LINE = bp.CM, 276  # 1,15

def build(src, dst):
    d, bib = bp.Doc(), False
    lines = open(src, encoding='utf-8').read().split('\n')
    blank = lambda: d.para('', first=0, line=LINE)
    for ln in lines:
        s = ln.strip()
        if not s: continue
        if s.startswith('@title '):
            d.para(s[7:], size=28, jc='center', first=0, line=LINE)
        elif s.startswith('@author '):
            d.para(s[8:], jc='center', first=0, line=LINE); blank()
        elif s.startswith('@abstract '):
            d.para(s[10:], size=20, first=0, line=LINE, bold=True)
        elif s.startswith('@keywords '):
            d.para(s[10:], size=20, first=0, line=LINE, bold=True)
        elif s.startswith('@bibliography'):
            bib = True; blank()
            d.para('Bibliografia', first=0, line=LINE, bold=True, keep=True)
        elif s.startswith('## '):
            blank(); d.para(s[3:], first=0, line=LINE, bold=True, keep=True)
        elif s.startswith('> '):
            d.para(s[2:], size=20, first=CM, left=CM, line=LINE)
        elif bib:
            d.para(s, size=20, first=0, line=LINE)
        else:
            d.para(s, first=CM, line=LINE)
    # blocchi citazione: margine destro di 1 cm
    body = ''.join(d.body).replace(f'<w:ind w:left="{CM}" w:firstLine="{CM}"/>',
                                   f'<w:ind w:left="{CM}" w:right="{CM}" w:firstLine="{CM}"/>')
    m = 4 * CM
    sect = (f'<w:sectPr><w:footnotePr><w:numFmt w:val="decimal"/></w:footnotePr>'
            f'<w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="{m}" w:right="{m}" w:bottom="{m}" w:left="{m}" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>')
    NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{body}{sect}</w:body></w:document>'
    fn = ['<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>',
          '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>']
    for i, n in enumerate(d.notes, 1):
        ppr = f'<w:pPr><w:pStyle w:val="FootnoteText"/><w:spacing w:after="0" w:line="{LINE}" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
        ref = '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/><w:sz w:val="20"/></w:rPr><w:footnoteRef/></w:r>'
        fn.append(f'<w:footnote w:id="{i}"><w:p>{ppr}{ref}{bp.runs(" " + n, 20)}</w:p></w:footnote>')
    footnotes = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:footnotes {NS}>{"".join(fn)}</w:footnotes>'
    styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="it-IT"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:before="0" w:after="0" w:line="{LINE}" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="FootnoteText"><w:name w:val="footnote text"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="FootnoteReference"><w:name w:val="footnote reference"/><w:rPr><w:vertAlign w:val="superscript"/></w:rPr></w:style>
</w:styles>'''
    settings = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings {NS}><w:footnotePr><w:footnote w:id="-1"/><w:footnote w:id="0"/></w:footnotePr><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>'
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
          '<Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rIdSet" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
             '<Relationship Id="rIdF" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/></Relationships>')
    title = next((l[7:] for l in lines if l.startswith('@title ')), '')
    author = next((l[8:] for l in lines if l.startswith('@author ')), '')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>' + escape(title) + '</dc:title><dc:creator>' + escape(author) + '</dc:creator></cp:coreProperties>')
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', document); z.writestr('word/styles.xml', styles)
        z.writestr('word/settings.xml', settings); z.writestr('word/footnotes.xml', footnotes)
        z.writestr('word/_rels/document.xml.rels', drels); z.writestr('docProps/core.xml', core)
    print(f'{dst}: {len(d.notes)} note')

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])

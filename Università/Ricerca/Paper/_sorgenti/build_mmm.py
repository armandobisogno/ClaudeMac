#!/usr/bin/env python3
"""Genera un .docx secondo le norme di *Memory, Mind & Media* (Cambridge UP), «Preparing your materials».

Norme applicate: Times New Roman 12, interlinea doppia, margini 2,54 cm, pagine numerate;
titoli di primo livello in grassetto, a sinistra, non numerati; secondo livello grassetto corsivo;
citazioni lunghe (tre righe o più) rientrate e senza virgolette; note solo esplicative;
bibliografia autore-data (Cambridge A) con nomi degli autori in grassetto.

Sintassi del sorgente:
  @title Titolo   @author Nome   @label Etichetta: testo (es. Abstract, Parole chiave)
  ## Titolo di primo livello   ### Titolo di secondo livello
  > citazione in blocco        | cella | cella |  (righe consecutive = una tabella; la prima è l'intestazione)
  @caption Didascalia della tabella
  @bibliography               @section Titolo (sezione finale non bibliografica, es. Dichiarazioni)
  *corsivo*  **grassetto**  {{nota a piè di pagina}}
Uso: python build_mmm.py sorgente.txt output.docx
"""
import re, sys, zipfile
from xml.sax.saxutils import escape

CM = 567
LINE = 480  # interlinea doppia


def runs(text, size=24, base_italic=False, base_bold=False):
    out, ital, bold = [], False, False
    for tok in re.split(r'(\*\*|\*)', text):
        if tok == '**': bold = not bold; continue
        if tok == '*': ital = not ital; continue
        if not tok: continue
        rpr = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        if bold ^ base_bold: rpr += '<w:b/>'
        if ital ^ base_italic: rpr += '<w:i/>'
        rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        out.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(tok)}</w:t></w:r>')
    return ''.join(out)


class Doc:
    def __init__(self):
        self.body, self.notes = [], []

    def inline(self, text, size, italic=False, bold=False):
        parts = re.split(r'\{\{(.*?)\}\}', text)
        xml = []
        for i, p in enumerate(parts):
            if i % 2 == 0:
                xml.append(runs(p, size, italic, bold))
            else:
                self.notes.append(p)
                xml.append(f'<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="{len(self.notes)}"/></w:r>')
        return ''.join(xml)

    def para(self, text, *, size=24, jc='both', first=709, left=0, hanging=0, line=LINE, before=0, after=0,
             italic=False, bold=False, keep=False):
        ind = f'<w:ind w:left="{left}" w:hanging="{hanging}"/>' if hanging else f'<w:ind w:left="{left}" w:firstLine="{first}"/>'
        ppr = f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>{ind}<w:jc w:val="{jc}"/>'
        if keep: ppr += '<w:keepNext/>'
        self.body.append(f'<w:p><w:pPr>{ppr}</w:pPr>{self.inline(text, size, italic, bold)}</w:p>')

    def table(self, rows):
        cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
        ncol = max(len(r) for r in cells)
        width = 9000 // ncol
        firstw = 2600 if ncol == 2 else width
        widths = [firstw] + [(9000 - firstw) // (ncol - 1)] * (ncol - 1) if ncol > 1 else [9000]
        grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
        border = ''.join(f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="808080"/>' for b in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
        trs = []
        for ri, r in enumerate(cells):
            tcs = []
            for ci in range(ncol):
                txt = r[ci] if ci < len(r) else ''
                p = (f'<w:p><w:pPr><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
                     f'{self.inline(txt, 20, bold=(ri == 0))}</w:p>')
                tcs.append(f'<w:tc><w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/></w:tcPr>{p}</w:tc>')
            hdr = '<w:trPr><w:tblHeader/></w:trPr>' if ri == 0 else ''
            trs.append(f'<w:tr>{hdr}{"".join(tcs)}</w:tr>')
        self.body.append(f'<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/><w:tblBorders>{border}</w:tblBorders>'
                         f'<w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>'
                         f'<w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>')


def build(src, dst):
    d, bib, tbl = Doc(), False, []
    lines = open(src, encoding='utf-8').read().split('\n')

    def flush():
        if tbl:
            d.table(tbl); tbl.clear()
            d.para('', first=0, line=240)

    for ln in lines:
        s = ln.strip()
        if s.startswith('|'):
            tbl.append(s); continue
        flush()
        if not s or s.startswith('%'): continue
        if s.startswith('@title '):
            d.para(s[7:], size=28, jc='left', first=0, bold=True, after=240)
        elif s.startswith('@author '):
            d.para(s[8:], jc='left', first=0, after=360)
        elif s.startswith('@label '):
            lab, _, txt = s[7:].partition(':')
            d.para(f'**{lab}:**{txt}', first=0, after=120)
        elif s.startswith('@caption '):
            d.para(s[9:], size=22, first=0, line=276, before=240, after=120, keep=True)
        elif s.startswith('@bibliography'):
            bib = True
            d.para('Bibliografia', jc='left', first=0, bold=True, before=360, after=120, keep=True)
        elif s.startswith('@section '):
            bib = False
            d.para(s[9:], jc='left', first=0, bold=True, before=360, after=120, keep=True)
        elif s.startswith('### '):
            d.para(s[4:], jc='left', first=0, bold=True, italic=True, before=240, after=120, keep=True)
        elif s.startswith('## '):
            d.para(s[3:], jc='left', first=0, bold=True, before=360, after=120, keep=True)
        elif s.startswith('> '):
            d.para(s[2:], first=0, left=CM, line=LINE, before=120, after=120)
        elif bib:
            d.para(s, first=0, left=CM, hanging=CM, jc='left')
        else:
            d.para(s)
    flush()

    NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
    m = 1440
    sect = (f'<w:sectPr><w:footerReference w:type="default" r:id="rIdFt"/>'
            f'<w:footnotePr><w:numFmt w:val="decimal"/></w:footnotePr><w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="{m}" w:right="{m}" w:bottom="{m}" w:left="{m}" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>')
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{"".join(d.body)}{sect}</w:body></w:document>'
    fn = ['<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>',
          '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>']
    for i, n in enumerate(d.notes, 1):
        ppr = '<w:pPr><w:pStyle w:val="FootnoteText"/><w:spacing w:after="60" w:line="240" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
        ref = '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>'
        fn.append(f'<w:footnote w:id="{i}"><w:p>{ppr}{ref}{runs(" " + n, 20)}</w:p></w:footnote>')
    footnotes = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:footnotes {NS}>{"".join(fn)}</w:footnotes>'
    rp = '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/></w:rPr>'
    footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}><w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
              f'<w:r>{rp}<w:fldChar w:fldCharType="begin"/></w:r><w:r>{rp}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
              f'<w:r>{rp}<w:fldChar w:fldCharType="separate"/></w:r><w:r>{rp}<w:t>1</w:t></w:r><w:r>{rp}<w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')
    styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="it-IT"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:before="0" w:after="0" w:line="{LINE}" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="FootnoteText"><w:name w:val="footnote text"/><w:basedOn w:val="Normal"/><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
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
             '<Relationship Id="rIdF" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/>'
             '<Relationship Id="rIdFt" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>')
    title = next((l[7:] for l in lines if l.startswith('@title ')), '')
    author = next((l[8:] for l in lines if l.startswith('@author ')), '')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>' + escape(title) + '</dc:title><dc:creator>' + escape(author) + '</dc:creator></cp:coreProperties>')
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', document); z.writestr('word/styles.xml', styles)
        z.writestr('word/settings.xml', settings); z.writestr('word/footnotes.xml', footnotes)
        z.writestr('word/footer1.xml', footer); z.writestr('word/_rels/document.xml.rels', drels)
        z.writestr('docProps/core.xml', core)

    # conteggio: corpo del testo (esclusi titolo, abstract, tabella, bibliografia e dichiarazioni)
    body, on = [], False
    for l in lines:
        s = l.strip()
        if s.startswith('## ') and not on: on = True
        if s.startswith('@bibliography') or s.startswith('@section'): on = False
        if on and s and not s.startswith(('|', '@', '%')): body.append(s)
    txt = re.sub(r'\{\{.*?\}\}', '', ' '.join(body))
    notes = sum(len(n.split()) for n in d.notes)
    print(f'{dst}: {len(d.notes)} note; testo ~{len(txt.split())} parole (+ note ~{notes})')


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])

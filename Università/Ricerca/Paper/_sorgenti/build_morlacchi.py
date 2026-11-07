#!/usr/bin/env python3
"""Genera un .docx secondo le «Avvertenze per gli autori» di Morlacchi Editore (DdP/Forme).
Riusa il motore di build_paper.py cambiando solo la gabbia.

Norme: Times New Roman 12, tondo e corsivo, niente grassetto/sottolineato, nessun rientro di paragrafo;
titolo e autore 14 tondo centrati; titoli di primo livello numerati 14 corsivo a sinistra, di secondo
livello 12 corsivo; DUE righe bianche prima di ogni titolo e UNA dopo; citazioni autore-anno nel testo
(ivi / Ibidem); citazioni lunghe staccate in corpo 10 senza caporali; «Riferimenti bibliografici» finali
con autore su una riga e «anno, titolo…» sotto.

Sintassi del sorgente:
  @title Titolo   @author Nome   # Titolo 1° livello   ## Titolo 2° livello   > citazione lunga
  @bibliography   @a Cognome, N.   (poi le righe «anno, …» di quell'autore)
  *corsivo*   [B] = (Bisogno 2025)   [B:pp] = Bisogno 2025, pp → ivi / Ibidem in automatico
Uso: python3 build_morlacchi.py sorgente.txt output.docx
"""
import re, sys, zipfile
sys.path.insert(0, __import__('os').path.dirname(__file__))
import build_paper as bp
from xml.sax.saxutils import escape

LINE = 240  # interlinea singola (le norme non la specificano)
SELF = 'Bisogno 2025'


def resolve_cites(paras):
    """[B]/[B:pp] → Bisogno 2025 / ivi / Ibidem; ogni altra citazione (anno a 4 cifre, Conf.) interrompe la catena."""
    prev = None  # None = ultima citazione non di Bisogno 2025; altrimenti la pagina ('' se senza pagina)
    tok = re.compile(r'\[B(?::([^\]]+))?\]|\b(?:19|20)\d\d\b|Conf\.')
    out = []
    for p in paras:
        res, last = [], 0
        for m in tok.finditer(p):
            res.append(p[last:m.start()]); last = m.end()
            t = m.group(0)
            if not t.startswith('[B'):
                res.append(t); prev = None; continue
            pg = m.group(1) or ''
            if not pg:
                txt = SELF
            elif prev is not None and prev == pg:
                txt = 'Ibidem'
            elif prev is not None:
                txt = f'ivi, {pg}'
            else:
                txt = f'{SELF}, {pg}'
            prev = pg
            inside = p[:m.start()].count('(') > p[:m.start()].count(')')
            res.append(txt if inside else f'({txt})')
        res.append(p[last:])
        out.append(''.join(res))
    return out


def typo(s):
    return s.replace("'", '’')


def build(src, dst):
    raw = [l.strip() for l in open(src, encoding='utf-8').read().split('\n') if l.strip()]
    lines = [typo(l) for l in resolve_cites(raw)]
    d, bib = bp.Doc(), False
    blank = lambda: d.para('', first=0, line=LINE)
    plain = []  # testo per il conteggio dei caratteri
    first_author = True
    for s in lines:
        if s.startswith('@title '):
            d.para(s[7:], size=28, jc='center', first=0, line=LINE); plain.append(s[7:])
        elif s.startswith('@author '):
            d.para(s[8:], size=28, jc='center', first=0, line=LINE); plain.append(s[8:])
        elif s.startswith('@bibliography'):
            bib = True; blank(); blank()
            d.para('Riferimenti bibliografici', size=28, jc='left', first=0, line=LINE, italic=True, keep=True)
            blank(); plain.append('Riferimenti bibliografici')
        elif s.startswith('## '):
            blank(); blank(); d.para(s[3:], jc='left', first=0, line=LINE, italic=True, keep=True); blank()
            plain.append(s[3:])
        elif s.startswith('# '):
            blank(); blank(); d.para(s[2:], size=28, jc='left', first=0, line=LINE, italic=True, keep=True); blank()
            plain.append(s[2:])
        elif s.startswith('> '):
            blank(); d.para(s[2:], size=20, first=0, line=LINE); blank(); plain.append(s[2:])
        elif bib and s.startswith('@a '):
            if not first_author: blank()
            first_author = False
            d.para(s[3:], jc='left', first=0, line=LINE, keep=True); plain.append(s[3:])
        else:
            d.para(s, first=0, line=LINE); plain.append(s)
    body = ''.join(d.body)
    m = 1418  # 2,5 cm
    sect = (f'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="{m}" w:right="{m}" w:bottom="{m}" w:left="{m}" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>')
    NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{body}{sect}</w:body></w:document>'
    styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="it-IT"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:before="0" w:after="0" w:line="{LINE}" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
</w:styles>'''
    settings = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings {NS}><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>'
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rIdSet" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/></Relationships>')
    title = next((l[7:] for l in lines if l.startswith('@title ')), '')
    author = next((l[8:] for l in lines if l.startswith('@author ')), '')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>' + escape(title) + '</dc:title><dc:creator>' + escape(author) + '</dc:creator></cp:coreProperties>')
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', document); z.writestr('word/styles.xml', styles)
        z.writestr('word/settings.xml', settings)
        z.writestr('word/_rels/document.xml.rels', drels); z.writestr('docProps/core.xml', core)
    chars = sum(len(p.replace('*', '')) for p in plain)
    print(f'{dst}: {chars} caratteri spazi inclusi (bibliografia compresa)')
    return lines


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])

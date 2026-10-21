from pathlib import Path
from io import BytesIO
import re, json, hashlib
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('C:/Users/SSAFY/Desktop/kog 이력서.docx')
OUTPUT = ROOT / 'KOG_입사지원서_인쇄용.docx'
src = Document(SOURCE)
d = Document()
sec = d.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(1.6), Cm(1.6)
sec.left_margin, sec.right_margin = Cm(1.8), Cm(1.8)
sec.footer_distance = Cm(.7)
for grid in list(sec._sectPr.findall(qn('w:docGrid'))):
    sec._sectPr.remove(grid)

def font(run, size=11, bold=False):
    run.font.name = '맑은 고딕'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)
    rf = run._element.get_or_add_rPr().get_or_add_rFonts()
    for key in ('ascii','hAnsi','eastAsia','cs'):
        rf.set(qn('w:'+key), '맑은 고딕')

for name, size, before, after in [('Normal',10.5,0,5),('Title',20,0,8),('Heading 1',13,9,5),('Heading 2',11.5,8,4)]:
    style = d.styles[name]
    style.font.name = '맑은 고딕'
    style.font.size = Pt(size)
    style.font.bold = name != 'Normal'
    style.font.color.rgb = RGBColor(0,0,0)
    rf = style.element.get_or_add_rPr().get_or_add_rFonts()
    for key in ('ascii','hAnsi','eastAsia','cs'):
        rf.set(qn('w:'+key),'맑은 고딕')
    pf = style.paragraph_format
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.line_spacing = Pt({'Normal':15,'Title':26,'Heading 1':19,'Heading 2':17}[name])
    pf.widow_control = True
    pf.keep_with_next = name != 'Normal'
    snap=OxmlElement('w:snapToGrid');snap.set(qn('w:val'),'0');style.element.get_or_add_pPr().append(snap)
    for border in list(style.element.xpath('.//w:pBdr')):
        border.getparent().remove(border)

def p(text, style=None, bold=False, size=None):
    para = d.add_paragraph(style=style)
    run = para.add_run(text)
    if bold or size:
        font(run,size or 11,bold)
    if bold:
        para.paragraph_format.space_before=Pt(3)
    return para

def heading(text, page=False):
    para=p(text,'Heading 1')
    para.paragraph_format.page_break_before=page
    return para

def table(rows, widths, header=False):
    t=d.add_table(rows=0,cols=len(widths))
    t.alignment=WD_TABLE_ALIGNMENT.CENTER
    t.autofit=False
    for c,w in zip(t.columns,widths): c.width=Cm(w)
    pr=t._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for edge in ('top','bottom','left','right','insideH','insideV'):
        e=OxmlElement('w:'+edge)
        for key,val in [('val','single'),('sz','4'),('color','D9D9D9')]: e.set(qn('w:'+key),val)
        borders.append(e)
    pr.append(borders)
    margins=OxmlElement('w:tblCellMar')
    for edge,val in [('top','75'),('bottom','75'),('left','95'),('right','95')]:
        e=OxmlElement('w:'+edge);e.set(qn('w:w'),val);e.set(qn('w:type'),'dxa');margins.append(e)
    pr.append(margins)
    for i,values in enumerate(rows):
        row=t.add_row()
        trpr=row._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
        if i==0 and header: trpr.append(OxmlElement('w:tblHeader'))
        for j,(cell,value,w) in enumerate(zip(row.cells,values,widths)):
            cell.width=Cm(w)
            cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            para=cell.paragraphs[0]
            para.paragraph_format.space_after=Pt(0)
            para.paragraph_format.line_spacing=Pt(14)
            snap=OxmlElement('w:snapToGrid');snap.set(qn('w:val'),'0');para._p.get_or_add_pPr().append(snap)
            para.alignment=WD_ALIGN_PARAGRAPH.CENTER if header or j%2==0 else WD_ALIGN_PARAGRAPH.LEFT
            font(para.add_run(value),10, i==0 and header or not header and j%2==0)
            if header and i==0 or not header and j%2==0:
                sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'F0F0F0');cell._tc.get_or_add_tcPr().append(sh)
    return t

def body_from_cell(text):
    # Preserve all source words, punctuation and line breaks; only styling changes.
    for part in text.split('\n\n'):
        para=p(part)
        if part.startswith('[담당업무]') or part.startswith('[내용]'):
            # Retain the original labels while giving them a visible hierarchy.
            for run in para.runs:
                run.text=''
            lines=part.split('\n',1)
            font(para.add_run(lines[0]),10,True)
            if len(lines)==2:
                para.add_run('\n'+lines[1])
        para.paragraph_format.keep_with_next=False

p('KOG 입사지원서','Title').alignment=WD_ALIGN_PARAGRAPH.CENTER
p('김시후',bold=True,size=15)
table([
    ['지원분야','게임분석(FunQA)','지원구분','신입'],
    ['출생연도','1999년','성별','남성'],
    ['이메일','gnldud735rka@naver.com','연락처','010-7660-1306'],
    ['거주지','경상북도 구미시','병역','군필 (2020.06 ~ 2022.07)'],
    ['장애여부','비대상','보훈여부','비대상'],
],[2.2,6.5,2.2,6.5])
heading(src.paragraphs[1].text)
p(src.paragraphs[2].text,bold=True,size=11.5)
p(src.paragraphs[3].text)
p(src.paragraphs[4].text,size=10)
heading(src.paragraphs[5].text)
heading(src.paragraphs[7].text)
edu=src.tables[0]
for start in (1,4):
    vals=[edu.cell(start+k,2).text for k in range(3)]
    p(vals[0],'Heading 2')
    table([[edu.cell(start+1,1).text,vals[1]]],[3.1,14.3])
    p(edu.cell(start+2,1).text,bold=True,size=10)
    p(vals[2])
heading(src.paragraphs[9].text)
cert=src.tables[1]
table([[cell.text for cell in row.cells] for row in cert.rows],[4.8,2.65,5.1,4.85],True)
heading(src.paragraphs[13].text,page=True)
p(src.paragraphs[14].text)

heading(src.paragraphs[11].text)
proj=src.tables[3]
for idx,start in enumerate((1,6,11)):
    vals=[proj.cell(start+k,2).text for k in range(5)]
    title=p(vals[2],'Heading 2')
    if idx==2: title.paragraph_format.page_break_before=True
    table([[proj.cell(start,1).text,vals[0]],
           [proj.cell(start+1,1).text,vals[1]],
           [proj.cell(start+3,1).text,vals[3]]],[3.1,14.3])
    p(proj.cell(start+4,1).text,bold=True,size=10)
    body_from_cell(vals[4])

heading(src.paragraphs[15].text)
for idx in range(16,45):
    text=src.paragraphs[idx].text
    if not text.strip(): continue
    if idx in (16,26,36):
        text=re.sub(r'^###\s*','',text)
        para=p(text,'Heading 2')
        if idx==26: para.paragraph_format.page_break_before=True
    else:
        para=p(text)
        if idx==18:
            for r in para.runs:font(r,10,True)

footer=sec.footer.paragraphs[0]
footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
footer.style=d.styles['Normal']
footer.paragraph_format.space_after=Pt(0)
d.core_properties.title='KOG 입사지원서'
d.core_properties.author=''
d.save(OUTPUT)

# Ensure all substantive source text remains verbatim, allowing only layout whitespace.
out=Document(OUTPUT)
def alltext(doc):
    return ''.join(node.text or '' for node in doc.element.body.iter(qn('w:t')))
norm=lambda t:re.sub(r'\s+','',t)
target=norm(alltext(out))
expected=[re.sub(r'^###\s*','',pa.text) for pa in src.paragraphs if pa.text.strip()]
expected.extend(src.tables[0].cell(r,2).text for r in range(1,7))
expected.extend(c.text for row in src.tables[1].rows for c in row.cells)
expected.extend(src.tables[3].cell(r,2).text for r in range(1,16))
missing=[t for t in expected if norm(t) not in target]
assert not missing,missing
report={'substantive_text_items_checked':len(expected),'missing_items':missing,'application_questions_preserved':all(re.sub(r'^###\s*','',src.paragraphs[i].text) in alltext(out) for i in (16,26,36)),'output':str(OUTPUT)}
(ROOT/'qa'/'content_check_filled.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(r"C:\Users\SSAFY\Desktop\sihoo\kimshlife.github.io")
WORK = ROOT / ".codex_doc_work"
OUT = WORK / "김시후_IT포트폴리오_콘텐츠_작성본.docx"
IMG = ROOT / "assets" / "img"

NAVY = "1D2A44"
BLUE = "2C4CC0"
PALE_BLUE = "F1F5FC"
LIGHT_GRAY = "D9D9D9"
MID_GRAY = "596C83"
WHITE = "FFFFFF"
BLACK = "000000"


def set_font(run, name="Malgun Gothic", size=None, bold=None, color=BLACK):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=110, start=120, bottom=110, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def set_cell_borders(cell, color=LIGHT_GRAY, size="6"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        el = borders.find(tag)
        if el is None:
            el = OxmlElement(f"w:{edge}")
            borders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), size)
        el.set(qn("w:color"), color)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def prevent_row_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def add_page_field(paragraph, field_name):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = field_name
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, text, end])
    set_font(run, size=8.5, color=MID_GRAY)


def add_hyperlink(paragraph, text, url):
    part = paragraph.part
    rid = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), rid)
    run_el = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), BLUE)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    r_fonts = OxmlElement("w:rFonts")
    for attr in ("ascii", "hAnsi", "eastAsia"):
        r_fonts.set(qn(f"w:{attr}"), "Malgun Gothic")
    size = OxmlElement("w:sz")
    size.set(qn("w:val"), "21")
    r_pr.extend([r_fonts, size, color, underline])
    text_el = OxmlElement("w:t")
    text_el.text = text
    run_el.extend([r_pr, text_el])
    hyperlink.append(run_el)
    paragraph._p.append(hyperlink)


def add_paragraph(doc, text="", style=None, bold_lead=None, align=None, color=None):
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    if bold_lead and text.startswith(bold_lead):
        r1 = p.add_run(bold_lead)
        set_font(r1, bold=True, color=color or BLACK)
        r2 = p.add_run(text[len(bold_lead):])
        set_font(r2, color=color or BLACK)
    else:
        r = p.add_run(text)
        set_font(r, color=color or BLACK)
    return p


def add_bullet(doc, text, level=0):
    style = "List Bullet" if level == 0 else "List Bullet 2"
    p = add_paragraph(doc, text, style=style)
    p.paragraph_format.space_after = Pt(3)
    return p


def add_number(doc, text):
    p = add_paragraph(doc, text, style="List Number")
    p.paragraph_format.space_after = Pt(3)
    return p


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        set_font(run, bold=True, color=BLACK)
    p.paragraph_format.keep_with_next = True
    return p


def add_table(doc, headers, rows, widths=None, aligns=None, font_size=9.2):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.allow_autofit = False
    table.rows[0]._tr.get_or_add_trPr()
    set_repeat_table_header(table.rows[0])
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        if widths:
            cell.width = Inches(widths[i])
        set_cell_shading(cell, NAVY)
        set_cell_borders(cell)
        set_cell_margins(cell, top=120, bottom=120, start=130, end=130)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(header)
        set_font(r, size=9, bold=True, color=WHITE)
    for ri, row in enumerate(rows):
        cells = table.add_row().cells
        prevent_row_split(table.rows[-1])
        for ci, value in enumerate(row):
            cell = cells[ci]
            if widths:
                cell.width = Inches(widths[ci])
            if ri % 2 == 1:
                set_cell_shading(cell, PALE_BLUE)
            set_cell_borders(cell)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.alignment = aligns[ci] if aligns else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(str(value))
            set_font(r, size=font_size, color=BLACK)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table


def add_image(doc, path, width, caption, alt):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    inline = p.add_run().add_picture(str(path), width=Inches(width))
    inline._inline.docPr.set("descr", alt)
    cap = doc.add_paragraph(style="Caption")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.keep_with_next = False
    r = cap.add_run(caption)
    set_font(r, size=8.5, color=MID_GRAY)
    return p


def page_break(doc):
    doc.add_page_break()


def configure_document(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.72)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.72)
    section.right_margin = Inches(0.72)
    section.header_distance = Inches(0.35)
    section.footer_distance = Inches(0.35)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Malgun Gothic"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Malgun Gothic")
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(BLACK)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.28

    for style_name in ("List Bullet", "List Bullet 2", "List Number"):
        style = styles[style_name]
        style.font.name = "Malgun Gothic"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Malgun Gothic")
        style.font.size = Pt(10.2)
        style.font.color.rgb = RGBColor.from_string(BLACK)
        style.paragraph_format.space_after = Pt(3)
        style.paragraph_format.line_spacing = 1.2

    title = styles["Title"]
    title.font.name = "Malgun Gothic"
    title._element.rPr.rFonts.set(qn("w:eastAsia"), "Malgun Gothic")
    title.font.size = Pt(27)
    title.font.bold = True
    title.font.color.rgb = RGBColor.from_string(BLACK)
    title.paragraph_format.space_after = Pt(12)
    title_ppr = title._element.get_or_add_pPr()
    title_border = title_ppr.find(qn("w:pBdr"))
    if title_border is not None:
        title_ppr.remove(title_border)

    heading_specs = {
        "Heading 1": (18, 18, 8),
        "Heading 2": (13.5, 12, 5),
        "Heading 3": (11.2, 8, 3),
    }
    for style_name, (size, before, after) in heading_specs.items():
        style = styles[style_name]
        style.font.name = "Malgun Gothic"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Malgun Gothic")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(BLACK)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    caption = styles["Caption"]
    caption.font.name = "Malgun Gothic"
    caption._element.rPr.rFonts.set(qn("w:eastAsia"), "Malgun Gothic")
    caption.font.size = Pt(8.5)
    caption.font.color.rgb = RGBColor.from_string(MID_GRAY)
    caption.paragraph_format.space_after = Pt(7)

    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("김시후  게임 및 IT 서비스 기획 포트폴리오  |  ")
    set_font(r, size=8.5, color=MID_GRAY)
    add_page_field(p, "PAGE")
    r = p.add_run(" / ")
    set_font(r, size=8.5, color=MID_GRAY)
    add_page_field(p, "NUMPAGES")

    settings = doc.settings._element
    update = settings.find(qn("w:updateFields"))
    if update is None:
        update = OxmlElement("w:updateFields")
        settings.append(update)
    update.set(qn("w:val"), "true")


def build():
    doc = Document()
    configure_document(doc)

    # Cover
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(38)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    inline = p.add_run().add_picture(str(IMG / "profile.jpg"), width=Inches(1.55))
    inline._inline.docPr.set("descr", "김시후 프로필 사진")
    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_ppr = title._p.get_or_add_pPr()
    direct_border = title_ppr.find(qn("w:pBdr"))
    if direct_border is not None:
        title_ppr.remove(direct_border)
    r = title.add_run("김시후 게임 및 IT 서비스 기획 포트폴리오")
    set_font(r, size=27, bold=True, color=BLACK)
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.paragraph_format.space_after = Pt(16)
    r = sub.add_run("지원 직무용 콘텐츠 작성본")
    set_font(r, size=13, bold=True, color=BLUE)
    claim = doc.add_paragraph()
    claim.alignment = WD_ALIGN_PARAGRAPH.CENTER
    claim.paragraph_format.left_indent = Inches(0.45)
    claim.paragraph_format.right_indent = Inches(0.45)
    claim.paragraph_format.space_after = Pt(20)
    r = claim.add_run("규칙과 예외를 명세하고 구현으로 검증하는 기획자")
    set_font(r, size=16, bold=True, color=BLACK)
    intro = doc.add_paragraph()
    intro.alignment = WD_ALIGN_PARAGRAPH.CENTER
    intro.paragraph_format.left_indent = Inches(0.7)
    intro.paragraph_format.right_indent = Inches(0.7)
    intro.paragraph_format.space_after = Pt(24)
    r = intro.add_run(
        "게임의 재미를 규칙과 수치로 구체화하고, 서비스의 요구사항과 예외 정책을 문서로 남깁니다. "
        "시장과 기술 제약을 먼저 확인한 뒤 구현 과정에서 발견한 문제를 다시 명세에 반영합니다."
    )
    set_font(r, size=11.2, color=MID_GRAY)
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = meta.add_run("김시후  |  2026년 9월 11일")
    set_font(r, size=9.5, color=MID_GRAY)
    linkp = doc.add_paragraph()
    linkp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_hyperlink(linkp, "kimshlife.github.io", "https://kimshlife.github.io/")
    linkp.add_run("   ")
    add_hyperlink(linkp, "github.com/kimshlife", "https://github.com/kimshlife")
    page_break(doc)

    add_heading(doc, "문서 활용 안내", 1)
    add_paragraph(
        doc,
        "이 문서는 게임 및 IT 서비스 기획 직무 지원을 위한 포트폴리오 콘텐츠를 한 번에 정리한 작성본입니다. "
        "핵심 결론은 BodyBuilder, NeonTetrisWars, ProjectRG 세 프로젝트를 앞에 배치해 규칙 설계, 명세 작성, 기술 이해, 구현 검증 능력을 보여주는 것입니다."
    )
    add_table(
        doc,
        ["구성", "사용 목적"],
        [
            ["프로필과 직무 적합성", "지원 직무에 맞는 핵심 역량과 증거를 빠르게 확인"],
            ["프로젝트 상세", "역할, 기술 선택, STAR 문제 해결, 수치와 기여 경계를 검토"],
            ["포트폴리오 보완", "지원처별 우선순위와 정량 근거 보강 항목을 점검"],
            ["PPT 10장 구성", "슬라이드 제작 도구에 옮길 수 있는 페이지별 초안"],
            ["노션 초안", "노션 페이지에 붙여 넣어 다듬을 수 있는 블록 순서와 문구"],
        ],
        widths=[1.8, 5.0],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
    )
    add_heading(doc, "핵심 포트폴리오 전략", 2)
    add_bullet(doc, "첫 화면에서 기획 범위를 넓게 보이기보다 규칙, 명세, 검증이라는 일관된 작업 방식을 먼저 보여줍니다.")
    add_bullet(doc, "대표 프로젝트마다 본인이 정한 것과 팀이 정한 것을 나누고, 구현 또는 실사용으로 확인된 결과만 성과로 씁니다.")
    add_bullet(doc, "개선율이 없는 항목은 임의의 백분율을 만들지 않고 설계 수치, 운영 수치, 검증 시점을 분리해 표기합니다.")

    page_break(doc)
    add_heading(doc, "프로필", 1)
    add_heading(doc, "한 줄 소개", 2)
    add_paragraph(doc, "오래가는 즐거움을 기획하고, 판단의 근거를 실행 가능한 규칙과 문서로 옮기는 기획자 김시후입니다.")
    add_heading(doc, "기본 정보", 2)
    add_table(
        doc,
        ["항목", "내용"],
        [
            ["지원 분야", "게임 기획, IT 서비스 기획"],
            ["학력", "국립금오공과대학교 경영학과 학사, 2025년 8월 졸업"],
            ["교육", "삼성 청년 SW·AI 아카데미, 2026년 1월부터 12월까지 진행 중"],
            ["연구", "마케팅컨설팅연구실 학부연구생, 2023년 9월부터 2025년 2월까지"],
            ["논문", "생성형 AI 지속 사용 의도 연구 제2저자, LNCS 특별호, 2024"],
            ["경력", "제조업 품질보증부 수입검사 담당 2년, 검사 기준서 기반 판정과 대책서 운영"],
            ["수상", "창업 및 아이디어 공모전 8건"],
            ["자격", "ADsP, FAT 1급, 컴퓨터활용능력 2급, 정보처리기능사"],
            ["연락", "kimshlife@naver.com"],
        ],
        widths=[1.25, 5.55],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
    )
    add_heading(doc, "핵심 역량 요약", 2)
    add_number(doc, "게임 규칙과 밸런스 수치를 설계하고 표준 규칙과 자체 규칙의 경계를 정합니다.")
    add_number(doc, "사용자 행동, 실패 조건, 예외 처리, 완료 기준을 명세와 작업지시서에 남깁니다.")
    add_number(doc, "시장, 법령, 선행 연구, 기술 제약을 검토하고 실제 설계 기준으로 바꿉니다.")

    add_heading(doc, "직무 적합성 분석", 1)
    add_paragraph(
        doc,
        "게임 및 IT 서비스 기획에서 가장 앞에 제시할 역량은 시스템 설계, 요구사항 명세, 근거 기반 의사결정입니다. "
        "아래 순서는 현재 포트폴리오에서 증거가 강한 정도를 기준으로 정했습니다."
    )
    add_table(
        doc,
        ["우선", "핵심 역량", "포트폴리오 증거", "대표 프로젝트"],
        [
            ["1", "시스템과 규칙 설계", "SRS와 7-Bag 적용, 15회 회전 제한, UGC 공개 조건과 자원 상한 설계", "NeonTetrisWars / BodyBuilder"],
            ["2", "명세와 협업 전달", "구현명세서 2종과 FE·BE 작업지시서 2종 작성, 다른 담당자가 지시서에 따라 백엔드 수행", "BodyBuilder"],
            ["3", "근거 기반 문제 정의", "게이머 동기 이론의 5축 변환, 의료법과 약사법 검토, PEST와 VRIO 분석", "ProjectRG / SICK KICK"],
        ],
        widths=[0.55, 1.5, 3.6, 1.25],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER],
        font_size=8.8,
    )

    add_heading(doc, "캐치프레이즈", 1)
    add_table(
        doc,
        ["유형", "문구", "추천 이유"],
        [
            ["기술과 업무 방식", "규칙과 예외를 명세하고 구현으로 검증하는 게임 기획자", "BodyBuilder의 문서 작성과 구현, NeonTetrisWars의 규칙 설계를 동시에 설명합니다."],
            ["문제 해결과 성과", "모호한 재미를 수치와 정책으로 바꾸고 끝까지 구현합니다", "감각적인 기획보다 판단 기준과 실행력을 앞세우는 포트폴리오의 강점과 맞습니다."],
            ["가치관", "즐거움이 오래가도록 사용성과 운영 조건까지 설계합니다", "현재 포트폴리오의 즐거움, 편리함, 지속가능성이라는 기준을 채용 문맥에 맞게 압축합니다."],
        ],
        widths=[1.25, 2.65, 3.05],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=8.9,
    )
    add_paragraph(doc, "추천 문구는 첫 번째입니다. 직무, 작업 방식, 검증 방법이 한 문장 안에서 바로 드러납니다.", bold_lead="추천 문구는 첫 번째입니다.")

    page_break(doc)
    add_heading(doc, "기술과 도구 숙련도", 1)
    add_paragraph(doc, "숙련도는 실제 프로젝트에서 맡은 범위와 공개된 산출물을 기준으로 판단했습니다. 별은 게임 및 IT 서비스 기획 직무에서의 활용 중요도를 뜻합니다.")
    add_table(
        doc,
        ["역량과 도구", "숙련도", "중요도", "판단 근거"],
        [
            ["게임 시스템과 규칙 설계", "고급", "★★★★★", "표준 규칙 적용, 밸런스 수치 결정, 상태 판정과 UGC 정책을 주도적으로 설계"],
            ["서비스 요구사항과 명세", "고급", "★★★★★", "기능 명세와 FE·BE 작업지시서를 작성하고 구현 중 누락 조건을 수정"],
            ["시장과 규제 분석", "고급", "★★★★☆", "시장·경쟁사·의료 관련 법률을 검토해 사업 구조와 기능 범위를 결정"],
            ["PowerPoint", "고급", "★★★★☆", "공모전 발표자료와 IR 자료 제작, 도식과 다이어그램 작성"],
            ["React · Vue · TypeScript", "중급", "★★★★☆", "BodyBuilder와 ProjectRG의 실제 서비스 화면 구현"],
            ["Node.js · JavaScript", "중급", "★★★★☆", "웹 기반 로컬 대전 게임 구현"],
            ["Python과 데이터 분석", "중급", "★★★☆☆", "알고리즘, pandas·numpy 기초 분석, Matplotlib 시각화, ADsP"],
            ["문서와 협업 도구", "중급", "★★★★★", "Word, Excel, 한글, Notion, Discord, SharePoint를 기획과 협업에 활용"],
            ["생성형 AI 도구", "중급", "★★★☆☆", "기획 프로토타입, 문서 작성, 코드 리뷰, 원화 제작 과정에 활용"],
            ["Django와 REST API", "기초", "★★★☆☆", "MTV 구조와 REST API 설계 실습"],
            ["Figma", "초급", "★★★☆☆", "와이어프레임 확인과 화면 설계 커뮤니케이션"],
        ],
        widths=[1.65, 0.65, 0.9, 3.75],
        aligns=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=8.6,
    )
    add_heading(doc, "숙련도 표현 원칙", 2)
    add_bullet(doc, "고급은 프로젝트에서 기준을 정하고 다른 구성원이 실행할 수 있도록 문서화한 경험이 있는 경우에 사용합니다.")
    add_bullet(doc, "중급은 문서나 기존 구조를 참고해 독립적으로 결과물을 만들 수 있는 수준으로 사용합니다.")
    add_bullet(doc, "기초와 초급은 학습 또는 보조 활용 범위를 명확히 적어 과장으로 보이지 않게 합니다.")

    # Project 1
    page_break(doc)
    add_heading(doc, "대표 프로젝트 1 BodyBuilder", 1)
    add_paragraph(doc, "웹캠으로 인식한 팔 동작이 지형이 되는 4인 협동 웹 게임", color=MID_GRAY)
    add_table(
        doc,
        ["항목", "내용"],
        [
            ["기간과 팀", "2026년 7월부터 8월, 6인 팀, Frontend 3명과 Backend 3명"],
            ["담당", "창작마당 기능의 정책·명세·작업지시서 작성과 프론트엔드 구현, 캐릭터 상태 판정과 스프라이트 설계"],
            ["기술", "React, TypeScript, WebRTC, MediaPipe"],
            ["산출물", "구현명세서 2종, FE·BE 작업지시서 2종, 스프라이트 시트 5종, 컷신, 서비스 화면"],
            ["기여 경계", "게임 핵심 규칙은 팀 합의 사항이며, 캐릭터 원화는 생성형 AI로 제작. 본인 기여는 필요한 상태와 시점을 정의하고 게임에서 작동하도록 설계한 부분"],
        ],
        widths=[1.25, 5.55],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=9,
    )
    add_image(
        doc,
        IMG / "ws-editor.jpg",
        6.65,
        "창작마당 에디터  공개 전 클리어 검증과 자원 한도, 유효성 검사를 한 화면에 배치",
        "BodyBuilder 창작마당 에디터 화면",
    )
    add_heading(doc, "기술과 설계 선택", 2)
    add_table(
        doc,
        ["선택", "이유와 대안 비교"],
        [
            ["공식 맵과 유저 맵을 하나의 캐러셀로 통합", "탭을 나누면 유저 맵이 부가 콘텐츠로 읽히고 방장이 두 번 탐색해야 하므로 뱃지로만 구분"],
            ["공개 전 제작자 클리어 의무화", "깨지 못하는 맵이 공개되어 다른 사용자의 시간을 낭비하는 문제를 공개 조건에서 차단"],
            ["서버 최종 검증", "UI 검증은 편의 기능으로 두고 서버가 상한과 공개 가능 여부를 최종 판정"],
            ["관리자와 사용자 에디터의 공용 컴포넌트", "복제 구현은 버그 수정 지점을 두 곳으로 늘리므로 속성 분기로 전환"],
            ["소셜 기능을 2단계로 분리", "평점·댓글·좋아요를 한 번에 넣으면 테이블 3개와 API 6개, 인증 로직이 추가되어 핵심 UGC 범위를 압박"],
        ],
        widths=[2.25, 4.55],
        aligns=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=8.9,
    )
    add_heading(doc, "STAR 문제 해결", 2)
    add_heading(doc, "상황", 3)
    add_paragraph(doc, "유저가 맵을 만들고 공유하면 콘텐츠 수명은 늘지만, 클리어할 수 없는 맵과 부가 기능의 오류가 본 게임을 방해할 위험이 생깁니다.")
    add_heading(doc, "과제", 3)
    add_paragraph(doc, "창작 자유도를 유지하면서 공개 품질과 본 게임의 안정성을 보장하는 정책, 완료 기준, FE·BE 작업 단위를 정의해야 했습니다.")
    add_heading(doc, "행동", 3)
    add_bullet(doc, "공식 맵 6개의 실측값을 기준으로 폴리곤 8개, 정점 20개, 기믹 5개의 상한을 설정했습니다.")
    add_bullet(doc, "제작자가 한 번 클리어해야 공개할 수 있게 하고, 지형이 바뀌면 검증을 무효화하도록 정의했습니다.")
    add_bullet(doc, "구현 과정에서 드래그 이동 경로의 검증 무효화가 빠진 것을 발견해 명세와 구현을 함께 보완했습니다.")
    add_bullet(doc, "물리 엔진의 결정성을 깨뜨리는 벽시계 타임아웃 초기안은 폐기하고 회귀 테스트 기준을 남겼습니다.")
    add_heading(doc, "결과", 3)
    add_paragraph(doc, "2026년 8월 13일 기준 공개 유저 맵이 4건 이상 등록되었고 각 맵은 4회에서 7회 플레이되었습니다. 설정한 상한인 폴리곤 8개를 모두 사용한 맵도 실제로 공개되어, 공식 맵 실측에서 도출한 상한이 실사용 범위를 수용함을 확인했습니다.")
    add_heading(doc, "수치화와 시각화", 2)
    add_table(
        doc,
        ["구분", "수치", "해석", "추천 시각화"],
        [
            ["설계 기준", "폴리곤 2-3개 / 정점 4-6개 / 기믹 0-2개", "공식 맵 6개 실측 범위", "작은 막대 비교"],
            ["설정 상한", "폴리곤 8개 / 정점 20개 / 기믹 5개", "실측치에 여유를 둔 제작 한도", "게이지 또는 한도 카드"],
            ["실사용 확인", "공개 맵 4건 이상 / 각 4-7회 플레이", "기능이 실제 이용되었음을 확인", "빅넘버 카드"],
            ["상한 검증", "폴리곤 8개 사용 맵 1건 확인", "설정한 최대치가 실제 제작에 사용됨", "기준과 실제 비교"],
        ],
        widths=[1.15, 2.0, 2.55, 1.1],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER],
        font_size=8.3,
    )
    add_paragraph(doc, "개선 전후 백분율은 측정 자료가 없어 사용하지 않습니다. 현재 수치는 설계 기준과 실사용 검증을 보여주는 근거로 제시합니다.", bold_lead="개선 전후 백분율은 측정 자료가 없어 사용하지 않습니다.")
    add_heading(doc, "KPT 회고", 2)
    add_bullet(doc, "Keep  실측값과 완료 기준을 문서에 남기고 다른 담당자가 실행할 수 있는 수준으로 작업을 분해했습니다.")
    add_bullet(doc, "Problem  최초 명세에서 드래그 이동 시 검증 무효화 조건이 누락되었고, 임계값 공식은 맵 스케일에 따라 최대 100배 달라졌습니다.")
    add_bullet(doc, "Try  입력 경로와 스케일 조합을 체크리스트와 회귀 테스트에 포함해 명세 단계에서 누락을 먼저 잡겠습니다.")

    # Project 2
    page_break(doc)
    add_heading(doc, "대표 프로젝트 2 NeonTetrisWars", 1)
    add_paragraph(doc, "국제 표준 규칙을 적용한 웹 기반 로컬 대전 테트리스", color=MID_GRAY)
    add_table(
        doc,
        ["항목", "내용"],
        [
            ["기간과 팀", "2026년 4월부터 6월, 2인 팀"],
            ["담당", "아이디어 발안, 게임성 기획, 국제 표준 규칙 적용, 락 딜레이 게이지와 15회 회전 제한 설계, 구현"],
            ["기술", "Node.js, JavaScript"],
            ["산출물", "공개 GitHub 저장소와 플레이 가능한 빌드"],
        ],
        widths=[1.25, 5.55],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
    )
    add_image(
        doc,
        IMG / "nt-versus.jpg",
        6.55,
        "로컬 대전 화면  표준 규칙과 공격 정보, 두 플레이어의 진행 상태를 한 화면에 구성",
        "NeonTetrisWars 로컬 대전 화면",
    )
    add_heading(doc, "기술과 설계 선택", 2)
    add_table(
        doc,
        ["구분", "선택", "이유"],
        [
            ["표준 적용", "SRS, 7-Bag, 고스트 블록, 홀드", "이미 검증된 조작 규칙은 새로 만들지 않고 학습 비용을 낮춤"],
            ["자체 설계", "락 딜레이 게이지, 15회 회전 제한", "무한 회전을 막으면서 T-Spin 같은 고난도 기술은 허용하는 균형점을 설정"],
            ["접근성", "키보드만으로 전체 메뉴 조작, 테마와 키 배열 변경", "대전 중 마우스로 이동하는 마찰을 줄이고 사용자별 조작 조건을 수용"],
            ["기술 전제", "60FPS 동기화 목표와 룸 기반 2-4인 구조", "탭 전환과 백그라운드 상태에서도 플레이 흐름이 끊기지 않게 설계"],
        ],
        widths=[1.0, 2.25, 3.55],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=8.8,
    )
    add_heading(doc, "STAR 문제 해결", 2)
    add_heading(doc, "상황", 3)
    add_paragraph(doc, "웹 테트리스는 표준 규칙이 빠지거나 조작감이 둔한 경우가 있고, 탭 전환과 세션 변화가 게임 흐름을 끊습니다.")
    add_heading(doc, "과제", 3)
    add_paragraph(doc, "초보자가 이해할 수 있으면서 숙련자의 고급 플레이를 막지 않는 규칙과 조작 체계를 웹 환경에 맞게 정의해야 했습니다.")
    add_heading(doc, "행동", 3)
    add_bullet(doc, "국제 표준인 SRS와 7-Bag, 고스트 블록, 홀드를 적용해 익숙한 조작 기반을 만들었습니다.")
    add_bullet(doc, "락 딜레이를 게이지로 시각화하고 회전 제한을 15회로 설정해 무한 회전과 고급 기술 허용 사이의 기준을 정했습니다.")
    add_bullet(doc, "키보드만으로 메뉴를 이동할 수 있게 하고 테마와 세 모드의 키 배열을 각각 바꿀 수 있게 했습니다.")
    add_heading(doc, "결과", 3)
    add_paragraph(doc, "싱글, 로컬 대전, 네트워크 대전, 설정 화면을 포함한 플레이 가능한 빌드와 공개 저장소를 완성했습니다. 60FPS는 설계 목표이므로 안정성 결과로 단정하지 않고 측정 항목으로 남깁니다.")
    page_break(doc)
    add_heading(doc, "수치화와 시각화", 2)
    add_table(
        doc,
        ["항목", "현재 근거", "추천 시각화", "추가 측정"],
        [
            ["규칙 완성도", "SRS와 7-Bag, 고스트 블록, 홀드 적용", "표준 적용 체크리스트", "표준 규칙 회귀 테스트 통과율"],
            ["밸런스", "회전 제한 15회", "락 딜레이 타임라인", "숙련도별 T-Spin 성공률과 악용 사례"],
            ["성능", "60FPS 동기화 목표", "프레임 안정성 선 그래프", "전경과 백그라운드 프레임 유지율"],
            ["접근성", "키보드 전용 메뉴와 키 재설정", "조작 경로 비교", "메뉴 완료 시간과 입력 오류 수"],
        ],
        widths=[1.05, 2.25, 1.7, 1.8],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=8.4,
    )
    add_heading(doc, "KPT 회고", 2)
    add_bullet(doc, "Keep  표준을 적용할 영역과 직접 밸런스를 정할 영역을 나눠 불필요한 재설계를 줄였습니다.")
    add_bullet(doc, "Problem  공개 자료에는 프레임 안정성, 조작 지연, 사용자 테스트 결과가 없어 목표와 결과를 분리해야 합니다.")
    add_bullet(doc, "Try  브라우저와 탭 상태별 FPS, 입력 지연, 숙련도별 플레이 테스트를 기록해 설계 수치의 근거를 보강하겠습니다.")

    # Project 3
    page_break(doc)
    add_heading(doc, "대표 프로젝트 3 ProjectRG", 1)
    add_paragraph(doc, "게이머 동기 이론으로 플레이 성향을 5축 진단하고 맞춤 게임을 추천하는 플랫폼", color=MID_GRAY)
    add_table(
        doc,
        ["항목", "내용"],
        [
            ["기간과 팀", "2026년 5월부터 6월, Full-Stack 2인"],
            ["담당", "서비스 발안, 5축 진단 체계와 문항 설계, 보충 질문 발동 규칙, 프론트엔드 구현"],
            ["기술", "Vue 3, Django, PWA"],
            ["기여 경계", "LLM 응답 안정화와 벡터 DB 확장은 백엔드 담당이 주도한 영역"],
        ],
        widths=[1.25, 5.55],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
    )
    add_image(
        doc,
        IMG / "rg-p07.jpg",
        6.55,
        "성향 진단 엔진  5축 가중치와 조건부 보충 질문 기준을 시각화",
        "ProjectRG 성향 진단 엔진 설명 화면",
    )
    add_heading(doc, "기술과 설계 선택", 2)
    add_table(
        doc,
        ["선택", "근거와 트레이드오프"],
        [
            ["5축 성향 체계", "Nick Yee의 게이머 동기 모델과 Bartle 유형학을 전략, 협동, 창의, 경쟁, 탐험의 서비스 기준으로 변환"],
            ["기본 12문항과 보충 3문항", "모든 사용자에게 15문항을 요구할 때의 이탈과 12문항 고정 시 경계선 정확도 저하를 함께 고려"],
            ["보충 질문 임계값", "1위와 2위 격차가 15점 이하이거나 1위가 65점 미만일 때만 보충 질문을 제시"],
            ["자기 탐색 사용자 집중", "구매 기록보다 플레이 동기와 성향을 이해하려는 사용자 문제에 범위를 맞춤"],
        ],
        widths=[2.2, 4.6],
        aligns=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=8.9,
    )
    add_heading(doc, "STAR 문제 해결", 2)
    add_heading(doc, "상황", 3)
    add_paragraph(doc, "구매 이력과 장르 태그만으로는 같은 장르 안의 전략, 파괴, 협력, 경쟁 성향 차이를 설명하기 어렵습니다.")
    add_heading(doc, "과제", 3)
    add_paragraph(doc, "검증된 이론을 서비스가 사용할 수 있는 진단 축으로 바꾸고, 응답 피로와 결과 정확도의 균형을 잡아야 했습니다.")
    add_heading(doc, "행동", 3)
    add_bullet(doc, "두 선행 이론을 5축 가중치로 재구성하고 기본, 표준, 심화의 3개 테스트 유형을 설계했습니다.")
    add_bullet(doc, "유형별 기본 12문항을 제시하고 결과가 애매할 때만 3문항을 추가하는 조건부 흐름을 만들었습니다.")
    add_bullet(doc, "1위와 2위의 격차, 1위 점수라는 두 신호로 보충 질문 발동 기준을 수치화했습니다.")
    add_heading(doc, "결과", 3)
    add_paragraph(doc, "진단 문항, 결과 해석, 공유와 커뮤니티로 이어지는 화면 구조를 만들고 프론트엔드를 구현했습니다. 외부 사용자를 대상으로 한 정확도나 추천 만족도는 공개 자료에 없어 성과 지표로 사용하지 않습니다.")
    page_break(doc)
    add_heading(doc, "수치화와 시각화", 2)
    add_table(
        doc,
        ["설계 요소", "수치", "목적", "추천 시각화"],
        [
            ["진단 축", "5개", "장르가 설명하지 못하는 플레이 동기를 분리", "레이더 차트"],
            ["테스트 유형", "3개", "기본, 표준, 심화로 사용 목적을 구분", "단계형 카드"],
            ["문항 수", "기본 12개 + 보충 3개", "응답 피로와 경계선 판정의 균형", "조건 분기 흐름도"],
            ["보충 기준", "격차 15점 이하 또는 1위 65점 미만", "애매한 결과에만 추가 질문", "결정 트리"],
        ],
        widths=[1.2, 1.65, 2.8, 1.15],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER],
        font_size=8.5,
    )
    add_heading(doc, "KPT 회고", 2)
    add_bullet(doc, "Keep  선행 이론을 인용하는 데 그치지 않고 문항, 임계값, 화면 흐름으로 연결했습니다.")
    add_bullet(doc, "Problem  진단 결과의 정확도와 추천 만족도를 검증할 사용자 데이터가 부족합니다.")
    add_bullet(doc, "Try  사전 가설을 세우고 재검사 일치도, 보충 질문 발동률, 추천 저장률을 수집해 임계값을 조정하겠습니다.")

    page_break(doc)
    add_heading(doc, "추가 프로젝트 요약", 1)
    add_paragraph(doc, "대표 세 프로젝트 뒤에는 지원처가 요구하는 역량에 따라 다음 경험을 선택적으로 배치합니다.")
    add_table(
        doc,
        ["프로젝트", "핵심 기여", "증거", "적합한 지원 방향"],
        [
            ["SICK KICK", "시장·경쟁사·법률 분석과 수익 구조 설계", "의료 관련 3개 규제 영역 검토, 교내 대상과 K7U-Belt 장려상", "서비스·사업 기획"],
            ["콘텐츠 운영 컨설턴트", "팀장으로 신직업, 자격 제도, 기업 인증제 설계", "948명과 732건 규모 공모전 장려상, 직업카드뉴스 발행", "HR·콘텐츠·사업 기획"],
            ["Pirukia", "9신 세계관 구조와 교리 선택지 설계", "9신 x 6요소 템플릿, 5종 x 5단계 해금 구조", "게임·콘텐츠 기획"],
        ],
        widths=[1.25, 2.1, 2.35, 1.1],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER],
        font_size=8.7,
    )
    add_heading(doc, "지원 방향별 프로젝트 순서", 2)
    add_table(
        doc,
        ["지원 방향", "1순위", "2순위", "3순위", "강조 문장"],
        [
            ["게임 기획", "NeonTetrisWars", "BodyBuilder", "Pirukia", "표준과 자체 규칙의 경계를 정하고 플레이 흐름을 수치로 설계"],
            ["서비스 기획", "ProjectRG", "SICK KICK", "BodyBuilder", "사용자 행동과 예외 조건을 명세하고 구현까지 연결"],
            ["사업 기획", "SICK KICK", "콘텐츠 운영 컨설턴트", "ProjectRG", "법령과 시장 분석을 기능 범위와 수익 구조에 반영"],
            ["HR·콘텐츠", "콘텐츠 운영 컨설턴트", "BodyBuilder", "SICK KICK", "직무와 운영 기준을 설계하고 협업 문서로 실행"],
        ],
        widths=[0.95, 1.2, 1.3, 1.05, 2.35],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=8.2,
    )

    add_heading(doc, "포트폴리오 피드백과 보완", 1)
    add_heading(doc, "현재 강점", 2)
    add_bullet(doc, "의사결정 이유가 구체적입니다. 기능을 넣었다는 설명보다 어떤 대안을 버렸고 왜 선택했는지가 남아 있습니다.")
    add_bullet(doc, "기여 경계가 분명합니다. 팀 합의, 팀원 담당, 생성형 AI 사용 범위를 구분해 신뢰를 높입니다.")
    add_bullet(doc, "기획 문서와 구현이 연결됩니다. BodyBuilder에서 명세, 지시서, 화면 구현, 실사용 확인이 한 흐름으로 이어집니다.")
    add_heading(doc, "보완 우선순위", 2)
    add_table(
        doc,
        ["우선", "보완 항목", "추가할 증거", "적용 위치"],
        [
            ["1", "성과 측정", "응답 시간, FPS 안정성, 과업 완료율, 오류율, 재검사 일치도 중 프로젝트별 핵심 지표 1-2개", "각 프로젝트 결과 페이지"],
            ["2", "기여도 수치", "본인이 작성한 문서, 구현 화면, 정책 항목, 검증 케이스의 범위를 수량으로 정리", "프로젝트 개요"],
            ["3", "지원처 맞춤", "공고의 핵심 과업 3개와 프로젝트 증거를 1대1로 연결", "표지 다음 직무 적합성"],
            ["4", "과정 증거", "명세 버전 변화, 초기안과 최종안, 테스트 결과 화면", "STAR 행동과 결과"],
        ],
        widths=[0.55, 1.35, 3.6, 1.35],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER],
        font_size=8.7,
    )
    add_heading(doc, "정량 표현 원칙", 2)
    add_bullet(doc, "검증된 수치는 기준일과 출처를 붙입니다. 예시는 2026년 8월 13일 기준 공개 맵과 플레이 수입니다.")
    add_bullet(doc, "목표 수치는 결과 수치와 분리합니다. NeonTetrisWars의 60FPS는 현재 성능 결과가 아니라 유지 목표입니다.")
    add_bullet(doc, "측정값이 없으면 개선율을 만들지 않습니다. 대신 설계 전제, 적용 수치, 확인된 사용 결과를 순서대로 보여줍니다.")

    page_break(doc)
    add_heading(doc, "PPT 포트폴리오 10장 구성", 1)
    add_paragraph(doc, "슬라이드의 핵심 문장은 한 장에 하나만 두고, 본문은 발표자가 설명할 근거만 남깁니다.")
    add_table(
        doc,
        ["장", "제목", "핵심 내용", "추천 시각화"],
        [
            ["1", "표지", "규칙과 예외를 명세하고 구현으로 검증하는 게임 기획자 / 김시후 / 게임 및 IT 서비스 기획 / 규칙 설계, 예외 명세, 근거 기반 의사결정의 3줄 요약", "프로필 사진 또는 로고와 대표 화면 1장"],
            ["2", "핵심 역량", "시스템과 규칙 설계 / 요구사항 명세 / 근거 기반 문제 정의. 각 역량에 대표 프로젝트 1개 연결", "3열 역량 맵"],
            ["3", "프로젝트 포트폴리오", "BodyBuilder, NeonTetrisWars, ProjectRG를 대표로 두고 추가 프로젝트 3개를 보조 증거로 배치", "기간 타임라인"],
            ["4", "BodyBuilder 개요", "웹캠 기반 4인 협동 게임 / 창작마당 정책·명세·지시서·FE 구현 / React와 TypeScript", "서비스 화면과 담당 범위 다이어그램"],
            ["5", "BodyBuilder 문제 해결", "공식 맵 실측에서 상한 도출 / 공개 전 클리어 / 서버 최종 검증 / 구현 중 누락 조건 수정", "기준 수치 카드와 명세-지시-구현 흐름"],
            ["6", "NeonTetrisWars", "표준 규칙은 적용하고 밸런스는 직접 설계 / 15회 회전 제한 / 락 딜레이 게이지 / 키보드 접근성", "게임 화면과 표준·자체 설계 비교"],
            ["7", "ProjectRG", "5축 진단 / 기본 12문항과 조건부 3문항 / 15점과 65점 임계값 / 이론을 서비스 로직으로 변환", "레이더 차트와 결정 트리"],
            ["8", "확장 역량", "SICK KICK의 규제 분석 / 콘텐츠 운영 컨설턴트의 제도 설계 / Pirukia의 세계관 구조화", "프로젝트별 1행 증거 카드"],
            ["9", "경험 기반 작업 방식", "수입검사의 기준서 기반 판정 / 연구실의 데이터와 논문 경험 / SSAFY의 구현 역량을 기획 방식과 연결", "경력-연구-개발 연결 도식"],
            ["10", "마무리", "즐거움이 오래가도록 사용성과 운영 조건까지 설계합니다 / 연락처와 포트폴리오 주소", "짧은 문장과 QR 코드 자리"],
        ],
        widths=[0.4, 1.3, 3.95, 1.2],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=8.0,
    )
    page_break(doc)
    add_heading(doc, "노션 포트폴리오 초안", 1)
    add_paragraph(doc, "아래 순서와 문구를 노션 페이지에 옮긴 뒤, 프로젝트 상세는 토글 블록으로 접고 핵심 수치는 표 또는 인라인 데이터베이스로 관리합니다.")
    add_heading(doc, "상단 프로필", 2)
    add_paragraph(doc, "> 규칙과 예외를 명세하고 구현으로 검증하는 게임 기획자 김시후")
    add_paragraph(doc, "게임의 재미를 규칙과 수치로 구체화하고, 서비스의 요구사항과 예외 정책을 문서로 남깁니다. 시장과 기술 제약을 먼저 확인한 뒤 구현 과정에서 발견한 문제를 다시 명세에 반영합니다.")
    add_bullet(doc, "Email  kimshlife@naver.com")
    add_bullet(doc, "Portfolio  https://kimshlife.github.io/")
    add_bullet(doc, "GitHub  https://github.com/kimshlife")

    add_heading(doc, "핵심 역량", 2)
    add_table(
        doc,
        ["역량", "설명", "대표 증거"],
        [
            ["시스템과 규칙 설계", "표준을 적용할 곳과 직접 정할 밸런스를 나눕니다.", "NeonTetrisWars의 SRS·7-Bag과 15회 회전 제한"],
            ["요구사항과 예외 명세", "사용자 행동, 실패 조건, 완료 기준을 실행 가능한 문서로 씁니다.", "BodyBuilder의 구현명세와 FE·BE 작업지시서"],
            ["근거 기반 의사결정", "시장, 법령, 선행 연구, 기술 제약을 기능과 정책으로 옮깁니다.", "ProjectRG의 5축 진단과 SICK KICK의 규제 분석"],
        ],
        widths=[1.55, 2.8, 2.45],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=8.8,
    )

    add_heading(doc, "기술 스택과 도구", 2)
    add_bullet(doc, "Planning  게임 규칙과 밸런스 / 서비스 요구사항과 명세 / 시장과 규제 분석")
    add_bullet(doc, "Front-end  React / Vue 3 / TypeScript / JavaScript")
    add_bullet(doc, "Back-end and Data  Django / REST API 기초 / Python / pandas / numpy")
    add_bullet(doc, "Tools  PowerPoint / Word / Excel / 한글 / Notion / Discord / SharePoint / Figma")
    add_bullet(doc, "AI  ChatGPT Codex / Claude Code / Gemini Antigravity")

    add_heading(doc, "프로젝트 상세 토글 1", 2)
    add_paragraph(doc, "토글 제목  BodyBuilder  유저 맵 제작과 공유를 품질 보증 구조로 설계")
    add_bullet(doc, "개요  웹캠으로 인식한 팔 동작이 지형이 되는 4인 협동 웹 게임")
    add_bullet(doc, "담당  창작마당 정책·명세·작업지시서 작성과 프론트엔드 구현")
    add_bullet(doc, "문제  깨지 못하는 맵의 공개와 부가 기능 오류가 본 게임을 막을 수 있음")
    add_bullet(doc, "행동  공식 맵 실측, 자원 상한, 공개 전 클리어, 서버 최종 검증, 단계 분리")
    add_bullet(doc, "결과  공개 맵 4건 이상, 각 4-7회 플레이, 폴리곤 8개 상한 사용 맵 확인, 2026년 8월 13일 기준")

    add_heading(doc, "프로젝트 상세 토글 2", 2)
    add_paragraph(doc, "토글 제목  NeonTetrisWars  표준 규칙과 자체 밸런스의 경계 설계")
    add_bullet(doc, "개요  국제 표준 규칙을 적용한 웹 기반 로컬 대전 테트리스")
    add_bullet(doc, "담당  아이디어 발안, 게임성 기획, 규칙 표준화, 락 딜레이와 회전 제한 설계, 구현")
    add_bullet(doc, "선택  SRS와 7-Bag은 적용하고 락 딜레이 게이지와 15회 회전 제한은 직접 설계")
    add_bullet(doc, "결과  싱글, 로컬 대전, 네트워크 대전, 설정 화면을 포함한 플레이 가능한 빌드와 공개 저장소")

    add_heading(doc, "프로젝트 상세 토글 3", 2)
    add_paragraph(doc, "토글 제목  ProjectRG  게이머 동기 이론을 5축 진단 엔진으로 변환")
    add_bullet(doc, "개요  플레이 성향을 진단하고 맞춤 게임을 추천하는 플랫폼")
    add_bullet(doc, "담당  서비스 발안, 진단 체계와 문항 설계, 보충 질문 규칙, 프론트엔드 구현")
    add_bullet(doc, "선택  5축 가중치, 3개 테스트 유형, 기본 12문항과 조건부 3문항")
    add_bullet(doc, "기준  1위와 2위 격차 15점 이하 또는 1위 65점 미만일 때 보충 질문")

    add_heading(doc, "프로젝트 회고", 2)
    add_paragraph(doc, "Keep  판단 기준과 대안을 문서에 남기고 구현 결과로 다시 확인합니다.")
    add_paragraph(doc, "Problem  일부 프로젝트는 성능이나 사용성 개선을 보여줄 사전·사후 측정값이 부족합니다.")
    add_paragraph(doc, "Try  프로젝트 시작 시 성공 지표와 측정 방법을 정하고 결과 화면과 테스트 기록을 함께 남기겠습니다.")

    final_heading = add_heading(doc, "제출 전 점검표", 1)
    final_heading.paragraph_format.page_break_before = True
    add_table(
        doc,
        ["점검 항목", "확인 기준"],
        [
            ["지원 직무", "표지와 첫 프로젝트가 공고의 핵심 과업과 바로 연결되는가"],
            ["기여 범위", "팀 합의, 팀원 작업, 생성형 AI 사용, 본인 구현 범위를 구분했는가"],
            ["수치", "기준일과 측정 대상을 적고 목표와 결과를 구분했는가"],
            ["기술 선택", "기술명 나열 대신 선택 이유와 버린 대안을 설명했는가"],
            ["STAR", "상황, 과제, 행동, 결과가 서로 이어지고 행동의 주체가 분명한가"],
            ["회고", "잘한 점, 부족한 점, 다음 행동이 구체적인가"],
            ["공개 범위", "개인정보, 팀 산출물, 비공개 자료를 노출하지 않았는가"],
            ["링크", "포트폴리오와 GitHub 링크가 열리고 최신 버전을 가리키는가"],
        ],
        widths=[1.45, 5.35],
        aligns=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
        font_size=9,
    )
    add_heading(doc, "최종 소개 문단", 2)
    add_paragraph(
        doc,
        "저는 게임의 재미를 규칙과 수치로 구체화하고, 서비스의 요구사항과 예외 정책을 문서로 남기는 기획자입니다. "
        "BodyBuilder에서는 유저 맵 제작과 공유 기능의 명세와 작업지시서를 작성하고 프론트엔드를 구현했습니다. "
        "NeonTetrisWars에서는 국제 표준 규칙과 자체 밸런스의 경계를 정했고, ProjectRG에서는 선행 연구를 5축 진단 로직으로 옮겼습니다. "
        "기획의 근거가 팀의 실행 기준이 되고, 구현에서 확인한 문제가 다시 문서를 개선하는 작업 방식을 이어가겠습니다."
    )

    doc.core_properties.title = "김시후 게임 및 IT 서비스 기획 포트폴리오"
    doc.core_properties.subject = "지원 직무용 포트폴리오 콘텐츠 작성본"
    doc.core_properties.author = "김시후"
    doc.core_properties.keywords = "게임 기획, 서비스 기획, 포트폴리오, BodyBuilder, NeonTetrisWars, ProjectRG"
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()

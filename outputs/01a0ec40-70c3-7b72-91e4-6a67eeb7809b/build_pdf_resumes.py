from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from build_resumes import COMMON, RESUMES


ROOT = Path(__file__).parent
OUT = ROOT / "resumes_pdf"
OUT.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Malgun", r"C:\Windows\Fonts\malgun.ttf"))
pdfmetrics.registerFont(TTFont("Malgun-Bold", r"C:\Windows\Fonts\malgunbd.ttf"))
pdfmetrics.registerFontFamily("Malgun", normal="Malgun", bold="Malgun-Bold")

BLACK = colors.HexColor("#111820")
MUTED = colors.HexColor("#4C5964")

style = {
    "name": ParagraphStyle(
        "name", fontName="Malgun-Bold", fontSize=19, leading=24,
        textColor=BLACK, spaceAfter=2, wordWrap="CJK", alignment=TA_LEFT,
    ),
    "title": ParagraphStyle(
        "title", fontName="Malgun", fontSize=11.2, leading=17,
        textColor=BLACK, spaceAfter=11, wordWrap="CJK",
    ),
    "meta": ParagraphStyle(
        "meta", fontName="Malgun", fontSize=8.6, leading=14,
        textColor=MUTED, spaceAfter=1, wordWrap="CJK",
    ),
    "h1": ParagraphStyle(
        "h1", fontName="Malgun-Bold", fontSize=10.7, leading=16,
        textColor=BLACK, spaceBefore=11, spaceAfter=5, wordWrap="CJK",
        keepWithNext=True,
    ),
    "h2": ParagraphStyle(
        "h2", fontName="Malgun-Bold", fontSize=9.3, leading=14,
        textColor=BLACK, spaceBefore=7, spaceAfter=3, wordWrap="CJK",
        keepWithNext=True,
    ),
    "body": ParagraphStyle(
        "body", fontName="Malgun", fontSize=9.1, leading=14,
        textColor=BLACK, spaceAfter=4, wordWrap="CJK",
    ),
    "bullet": ParagraphStyle(
        "bullet", fontName="Malgun", fontSize=9.0, leading=13.7,
        textColor=BLACK, leftIndent=12, firstLineIndent=-9,
        spaceAfter=2.6, wordWrap="CJK",
    ),
}


def p(txt, kind="body"):
    return Paragraph(escape(txt), style[kind])


def bullet(txt):
    return Paragraph("•&nbsp;&nbsp;" + escape(txt), style["bullet"])


def footer(canvas, doc, title):
    canvas.saveState()
    canvas.setFont("Malgun", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 19*mm, 14*mm, f"김시후  |  {title}  |  {doc.page}")
    canvas.restoreState()


def build(item):
    target = OUT / Path(item["filename"]).with_suffix(".pdf").name
    pdf = SimpleDocTemplate(
        str(target), pagesize=A4,
        leftMargin=19*mm, rightMargin=19*mm,
        topMargin=17*mm, bottomMargin=19*mm,
        title="김시후 " + item["title"], author="김시후",
    )
    story = [
        p("김시후", "name"), p(item["title"], "title"),
        p(COMMON["contact"], "meta"),
        p(COMMON["portfolio"], "meta"),
        p(COMMON["military"], "meta"),
        p("직무 요약", "h1"), p(item["profile"]),
        p("핵심 역량", "h1"),
    ]
    story += [bullet(x) for x in item["strengths"]]
    story += [
        p("경력", "h1"),
        p("㈜테크노전자  |  품질보증부 사원  |  2020.06–2022.07 (2년 2개월)", "h2"),
    ]
    story += [bullet(x) for x in item["career"]]
    story += [p("직무 관련 경험", "h1")]
    for label, points in item["cases"]:
        story.append(CondPageBreak(28*mm))
        story.append(p(label, "h2"))
        story += [bullet(x) for x in points]
    story += [p("학력 및 교육", "h1")]
    story += [bullet(COMMON[x]) for x in ("education", "ssafy", "cbds")]
    story += [p("자격 및 수상", "h1"), bullet(COMMON["certs"])]
    story += [bullet(x) for x in item["awards"]]
    pdf.build(
        story,
        onFirstPage=lambda c, d: footer(c, d, item["title"]),
        onLaterPages=lambda c, d: footer(c, d, item["title"]),
    )
    print(target)


for item in RESUMES:
    build(item)

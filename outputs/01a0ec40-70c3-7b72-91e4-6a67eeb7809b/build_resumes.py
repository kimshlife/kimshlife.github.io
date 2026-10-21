from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


OUT = Path(__file__).parent / "resumes"
OUT.mkdir(parents=True, exist_ok=True)

COMMON = {
    "contact": "010-7660-1306  |  kimshlife@naver.com  |  경남 거제시 · 전국 근무 가능",
    "portfolio": "포트폴리오  https://kimshlife.github.io/",
    "education": "국립금오공과대학교 경영학과 학사  |  2018.03–2025.08  |  3.47/4.5",
    "ssafy": "삼성 청년 SW·AI 아카데미  |  2026.01–현재 (2026.12 종료 예정)  |  Python·알고리즘, AI 데이터 실습, Django·Vue.js 웹 개발",
    "cbds": "Python 기반 사무행정 CBDS 양성 과정  |  2023.06–2023.10  |  데이터 분석·시각화, 더존 SmartA 회계 실습",
    "certs": "컴퓨터활용능력 2급 (2025.05)  ·  1종 보통 운전면허 (2025.05)  ·  ADsP (2023.08)  ·  FAT 1급 (2023.07)  ·  정보처리기능사 (2019.12)",
    "military": "병역 완료  |  산업기능요원 소집해제",
}

RESUMES = [
    {
        "filename": "01_김시후_품질보증_수입검사_이력서.docx",
        "title": "품질보증 및 수입검사 이력서",
        "profile": "제조업 품질보증부에서 2년 2개월간 수입검사(IQC)를 담당했습니다. 품목별 검사 기준서에 따라 샘플링·전수 검사를 수행하고, 결과 데이터를 관리하며 불량 판정과 개선 대책 요청을 지원했습니다. 기준에 맞춰 확인한 사실을 기록하고 후속 조치로 연결하는 업무에 강점이 있습니다.",
        "strengths": [
            "품목별 검사 기준서에 따른 샘플링·전수 검사 수행",
            "검사 결과 데이터 정리, 불량 판정, 대책서·개선 대책 요청 및 보고서 작성 보조",
            "ADsP·컴퓨터활용능력 2급과 데이터 분석 교육을 통한 기록·집계 역량",
        ],
        "career": [
            "입고 제품을 품목별 기준서에 맞춰 샘플링 또는 전수 검사하고 적합 여부를 확인",
            "검사 결과 데이터를 작성·관리하고 불량 제품을 판정",
            "불량에 대한 대책서와 개선 대책을 요청하고 검사 결과 보고서 작성 보조",
        ],
        "cases": [
            ("SSketch 게임 프로젝트  |  2026.08–2026.09  |  프로젝트 경험", [
                "요구사항 250건을 분류하고 실제 코드 기준으로 진행 상태를 반복 점검",
                "빌드에서만 발생한 설정 관련 결함 3건의 재현 조건과 원인을 추적",
                "직접 작성한 Unity EditMode 테스트 96개로 담당 규칙 코드를 검증",
            ]),
            ("마케팅컨설팅연구실  |  2023.09–2025.02  |  학부연구생", [
                "생성형 AI 지속 사용 의도 연구에 제2저자로 참여하고 자료 분석 경험 축적",
            ]),
        ],
        "awards": [
            "2024.12  교내 학생 예비창업자 모의 IR DAY 금상",
            "2023.06  교내 창업·발명 아이디어 경진대회 대상",
        ],
        "other": "희망 직무  수입검사(IQC) · 품질보증 · 품질관리  |  희망 근무지역  전국",
    },
    {
        "filename": "02_김시후_사업기획_시장조사_이력서.docx",
        "title": "사업기획 및 시장조사 이력서",
        "profile": "경영학 전공과 마케팅컨설팅연구실 활동을 바탕으로 시장 문제를 조사해 사업 구조로 구체화해 왔습니다. 생성형 AI 지속 사용 의도 연구에 제2저자로 참여했고, 플로라봇의 시장 분석·비즈니스 모델 설정을 보조했습니다. 학생 창업 프로젝트에서는 경쟁사·선행기술·규제를 검토해 제안서를 작성했습니다.",
        "strengths": [
            "시장·경쟁사·선행기술·규제 조사 결과를 사업 방향과 수익 구조에 연결",
            "논문 공동저자 경험과 ADsP·Python 데이터 분석 교육",
            "기술사업화 지원사업 선정 및 모의 IR 금상 참여 경험",
        ],
        "career": [
            "품목별 기준에 따른 검사와 결과 데이터 작성·관리로 근거 중심의 기록 업무 수행",
            "불량 판정과 개선 대책 요청, 결과 보고서 작성 보조",
        ],
        "cases": [
            ("마케팅컨설팅연구실  |  2023.09–2025.02  |  학부연구생", [
                "AI·센서 기반 반려식물 로봇 플로라봇의 아이디어 구체화 및 시장 분석·BM 설정 보조",
                "2024 경북구미 강소연구개발특구 우수창업자 기술사업화 지원사업 선정, 교내 모의 IR 금상에 참여",
                "생성형 AI 지속 사용 의도 연구 제2저자; Lecture Notes in Computer Science 특별호 게재",
            ]),
            ("SICK KICK  |  2023.05–2023.11  |  학생 창업 프로젝트", [
                "소아청소년 진료 연계 서비스의 시장·경쟁사·선행기술을 조사하고 PEST·VRIO로 외부 환경과 내부 역량 분석",
                "비대면 진료·약품 배송·전자의무기록 관련 규제를 검토해 서비스 범위와 수익 구조 제안",
            ]),
            ("SolarBeam  |  2023.06–2024.02  |  교내 창업동아리 팀장·총무", [
                "태양광 킥보드 거치소의 선행 특허와 시중 제품을 조사하고 팀 일정·역할·지원금 서류 관리",
            ]),
        ],
        "awards": [
            "2024.12 모의 IR DAY 금상 · 2023.11 한국고용정보원 신직업·미래직업 아이디어 공모전 장려상 · 2023.06 교내 창업·발명 아이디어 경진대회 대상",
        ],
        "other": "희망 직무  사업기획 · 시장조사 · 리서치 · 서비스기획  |  희망 근무지역  전국",
    },
    {
        "filename": "03_김시후_교육사업_프로그램운영_이력서.docx",
        "title": "교육사업 및 프로그램 운영 이력서",
        "profile": "팀 운영과 사업비·서류 관리 경험을 교육·지원사업 운영 직무에 연결하고자 합니다. 교내 창업동아리 SolarBeam에서 팀장과 총무를 맡아 역할 배분, 일정 점검, 구매·영수증 처리, 지원금·보고서를 관리했습니다. 연구실과 SSAFY에서 연구·교육 과정을 직접 경험했고, 발명교육 봉사에도 참여했습니다.",
        "strengths": [
            "팀원 역할 배분, 마일스톤 점검, 회의·보고서·증빙 서류 관리",
            "지원금 집행과 영수증 처리 경험 및 FAT 1급·컴퓨터활용능력 2급",
            "교육 수강자 관점과 발명교육 봉사 경험을 통한 참여자 소통 이해",
        ],
        "career": [
            "검사 기준·결과 데이터에 근거해 업무를 처리하고 보고서 작성 보조",
            "불량 판정 후 관련자에게 대책서와 개선 대책을 요청",
        ],
        "cases": [
            ("SolarBeam  |  2023.06–2024.02  |  교내 창업동아리 팀장·총무", [
                "팀 역할 분배와 진행 일정 관리, 회의 주최, 필수 서류·보고서 작성",
                "구매 물품 선정, 영수증 처리, 지원금 관리와 선행 특허·시장 조사",
            ]),
            ("거북선신화 동아리  |  2018.03–2025.02  |  발명·교육 활동", [
                "초등학생 대상 발명캠프와 지역 고등학생 대상 자유학기제 교육 활동 참여",
            ]),
            ("콘텐츠 운영 컨설턴트 제안  |  2023.06  |  팀장", [
                "2주 일정의 공모전에서 역할 배분·진행 점검·최종 검토를 맡고 제도와 인센티브를 제안",
                "한국고용정보원 제4회 신직업·미래직업 아이디어 공모전 장려상",
            ]),
        ],
        "awards": [
            "2023.12  교내 창업동아리 시제품 제작 경진대회 창의아이디어상",
            "2023.11  한국고용정보원 신직업·미래직업 아이디어 공모전 장려상",
        ],
        "other": "희망 직무  교육사업 운영 · 프로그램 운영 · 연구행정  |  희망 근무지역  전국",
    },
    {
        "filename": "04_김시후_소프트웨어QA_테스트_이력서.docx",
        "title": "소프트웨어 QA 및 테스트 이력서",
        "profile": "제조업 IQC에서 검사 기준에 따른 확인, 결과 기록, 불량 판정을 수행했습니다. 이후 SSAFY 게임 프로젝트에서 요구사항 250건을 실제 코드와 대조하고 빌드 전용 결함 3건의 재현 조건을 찾았으며, 담당 규칙 코드의 Unity EditMode 테스트 96개를 직접 작성했습니다. 품질 업무 경험을 소프트웨어 검증으로 확장하고 있습니다.",
        "strengths": [
            "검사 기준·요구사항에 근거한 확인과 결과 기록",
            "빌드 환경에서만 발생하는 결함의 재현 조건 및 원인 추적",
            "Unity C# 테스트 작성과 Python·Django·Vue.js 학습을 통한 개발 협업 이해",
        ],
        "career": [
            "품목별 검사 기준서에 따른 샘플링·전수 검사와 불량 판정",
            "검사 결과 데이터 관리, 대책서·개선 대책 요청, 결과 보고서 작성 보조",
        ],
        "cases": [
            ("SSketch  |  2026.08–2026.09  |  SSAFY 6인 게임 프로젝트", [
                "요구사항 250건을 12개 대분류로 명세하고 코드 기준으로 완료·부분·미착수를 재판정",
                "해상도 복구·키 변경 반영·수직동기화 설정의 빌드 결함 3건을 재현하고 원인 추적",
                "그림 소유권·기절 게이지 등 담당 규칙 코드와 Unity EditMode 테스트 96개 직접 작성",
                "버그 제보 설문에 발생 시점·문제 유형·영상 첨부 항목을 넣어 재현에 필요한 정보를 수집하도록 설계",
            ]),
            ("SSAFY SW·AI 교육  |  2026.01–현재", [
                "Python 알고리즘과 AI 데이터 실습, Django REST API·Vue.js 화면 구현 학습",
            ]),
        ],
        "awards": [
            "2024.12  교내 학생 예비창업자 모의 IR DAY 금상",
            "2023.06  교내 창업·발명 아이디어 경진대회 대상",
        ],
        "other": "희망 직무  소프트웨어 QA · 테스트 엔지니어 · 서비스 품질관리  |  희망 근무지역  전국",
    },
    {
        "filename": "05_김시후_게임서비스_기획운영_이력서.docx",
        "title": "게임 및 서비스 기획 운영 이력서",
        "profile": "게임과 서비스의 규칙을 사용자에게 이해되는 정책·화면·안내로 옮기는 경험을 쌓았습니다. SSketch에서 요구사항 250건과 설정 화면을 기획·구현하고, 버그 제보가 재현 정보로 이어지도록 설문을 설계했습니다. 6년간 운영한 카운터사이드 길드는 취미 활동으로, 규칙 고지·예외 처리·운영진 역할 분담을 직접 경험했습니다.",
        "strengths": [
            "게임 규칙·요구사항·UI 명세 작성 및 구현 상태 점검",
            "커뮤니티 정책 고지, 가입·제재·예외 기준 운영 경험 (취미 활동)",
            "이용자 제보의 유형·시점·증거를 구조화하는 피드백 수집 설계",
        ],
        "career": [
            "품목별 기준에 따른 검사, 결과 데이터 관리, 불량 판정과 개선 대책 요청",
            "기준을 일관되게 적용하고 근거를 기록하는 업무 방식 습득",
        ],
        "cases": [
            ("SSketch  |  2026.08–2026.09  |  SSAFY 게임 프로젝트", [
                "요구사항 250건을 정리하고 실제 코드 기준으로 진행 상태 점검; 게임 규칙·수치와 설정 화면 설계",
                "설정 화면 HTML 프로토타입·레드라인을 만든 뒤 Unity 설정 시스템 구현",
                "버그 제보와 개선 건의를 분리하고 발생 시점·스크린샷·영상 등을 받는 설문 설계",
            ]),
            ("카운터사이드 길드 Time  |  2020–2026  |  취미 활동·길드장", [
                "2명에서 시작해 최대 30명 규모로 운영; 규칙 6개를 사전에 문서화하고 공지",
                "합병 협의 시 가입 기준을 먼저 고지해 상대 길드 13명 중 동의한 6명이 합류",
                "게임사 운영 이슈로 인원이 이탈할 때 모집 공지·운영진 4명 역할 분담으로 길드 유지",
            ]),
            ("콘텐츠 운영 컨설턴트 제안  |  2023.06  |  공모전 프로젝트", [
                "게임·웹툰 산업의 이용자·운영 소통 문제를 조사하고 운영 직무·인증 제도 제안",
            ]),
        ],
        "awards": [
            "2023.11  한국고용정보원 신직업·미래직업 아이디어 공모전 장려상",
        ],
        "other": "희망 직무  게임 운영 · 서비스 운영 · 게임기획 · 서비스기획  |  희망 근무지역  전국",
    },
]


def set_font(run, size=None, bold=None, color=None):
    run.font.name = "맑은 고딕"
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(qn("w:" + key), "맑은 고딕")
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)


def configure_styles(doc):
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin, sec.bottom_margin = Cm(1.65), Cm(1.55)
    sec.left_margin, sec.right_margin = Cm(1.8), Cm(1.8)
    sec.header_distance, sec.footer_distance = Cm(.8), Cm(.8)
    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = "맑은 고딕", Pt(9.2)
    normal.font.color.rgb = RGBColor(24, 31, 37)
    normal.paragraph_format.space_after = Pt(3.5)
    normal.paragraph_format.line_spacing = 1.17
    for style_name, size, before, after in [
        ("Title", 19, 0, 2),
        ("Subtitle", 11, 0, 8),
        ("Heading 1", 11, 11, 5),
        ("Heading 2", 9.5, 7, 3),
    ]:
        style = doc.styles[style_name]
        style.font.name = "맑은 고딕"
        style.font.size = Pt(size)
        style.font.bold = style_name != "Subtitle"
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
    if "Meta" not in doc.styles:
        meta = doc.styles.add_style("Meta", WD_STYLE_TYPE.PARAGRAPH)
        meta.base_style = normal
    meta = doc.styles["Meta"]
    meta.font.name, meta.font.size = "맑은 고딕", Pt(8.8)
    meta.font.color.rgb = RGBColor(61, 70, 76)
    meta.paragraph_format.space_after = Pt(2)
    if "Bullet Compact" not in doc.styles:
        bullet = doc.styles.add_style("Bullet Compact", WD_STYLE_TYPE.PARAGRAPH)
        bullet.base_style = normal
    bullet = doc.styles["Bullet Compact"]
    bullet.paragraph_format.left_indent = Cm(.45)
    bullet.paragraph_format.first_line_indent = Cm(-.28)
    bullet.paragraph_format.space_after = Pt(2.7)


def para(doc, text, style=None):
    p = doc.add_paragraph(style=style)
    r = p.add_run(text)
    set_font(r)
    return p


def bullet(doc, text):
    p = doc.add_paragraph(style="Bullet Compact")
    r = p.add_run("•  " + text)
    set_font(r)
    return p


def heading(doc, text):
    para(doc, text, "Heading 1")


def subheading(doc, text):
    para(doc, text, "Heading 2")


def add_page_num(doc):
    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = footer.add_run("김시후  |  ")
    set_font(run, 8, color=(100, 108, 112))
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    footer._p.append(fld)


def make_resume(item):
    doc = Document()
    configure_styles(doc)
    para(doc, "김시후", "Title")
    para(doc, item["title"], "Subtitle")
    para(doc, COMMON["contact"], "Meta")
    para(doc, COMMON["portfolio"], "Meta")
    heading(doc, "직무 요약")
    para(doc, item["profile"])
    heading(doc, "핵심 역량")
    for line in item["strengths"]:
        bullet(doc, line)
    heading(doc, "경력")
    subheading(doc, "㈜테크노전자  |  품질보증부 사원  |  2020.06–2022.07 (2년 2개월)")
    for line in item["career"]:
        bullet(doc, line)
    heading(doc, "직무 관련 경험")
    for label, points in item["cases"]:
        subheading(doc, label)
        for line in points:
            bullet(doc, line)
    heading(doc, "학력 및 교육")
    bullet(doc, COMMON["education"])
    bullet(doc, COMMON["ssafy"])
    bullet(doc, COMMON["cbds"])
    heading(doc, "자격 및 수상")
    bullet(doc, COMMON["certs"])
    for line in item["awards"]:
        bullet(doc, line)
    heading(doc, "기타")
    para(doc, item["other"])
    para(doc, COMMON["military"], "Meta")
    add_page_num(doc)
    doc.core_properties.title = "김시후 " + item["title"]
    doc.core_properties.author = "김시후"
    path = OUT / item["filename"]
    doc.save(path)
    print(path)


if __name__ == "__main__":
    for item in RESUMES:
        make_resume(item)

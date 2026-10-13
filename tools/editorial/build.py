"""Generate the two role indexes and eight static case studies."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads(Path(__file__).with_name("portfolio.json").read_text(encoding="utf-8"))
ROLES = {
    "planning": {"name":"기획", "en":"PLANNING", "purpose":"만들 경험과 규칙을 결정합니다.", "sub":"규칙 · 정책 · 수치 · 명세"},
    "qa": {"name":"게임 분석·QA", "en":"GAME ANALYSIS / QA", "purpose":"문제를 읽고, 근거로 설명합니다.", "sub":"피드백 · 레퍼런스 · 재현 · 검증"}
}
ASSETS = {
    "game":"/ssketch/assets/screenshots/gameplay-night-theft.jpg", "workshop":"/assets/img/ws-editor.jpg",
    "slope":"/qa/img/bb-slope.jpg", "tetris":"/assets/img/nt-versus.jpg", "document":"/qa/img/doc-game-analysis.jpg",
    "owner":"/assets/img/ss-owner.jpg", "reference":"/assets/img/ss-settings.jpg", "survey":"/assets/img/rg-p03.jpg"
}
ALIASES = {"planning":{"ssketch":"ssketch", "workshop":"bodybuilder", "bodybuilder":"bodybuilder", "projectrg":"projectrg", "neontetris":"neontetris"},
           "qa":{"ssketch":"ssketch", "bodybuilder":"bodybuilder", "reference":"reference", "counterside":"counterside"}}
VERSION = "20261010b"
def e(value): return escape(str(value), quote=True)
def href(role, c): return f"/{role}/{c['id']}/"
def title(c): return " ".join(f"<span>{e(line)}</span>" for line in c["headline"])
def project(c): return f'<p class="ed-project"><b>{e(c["project"])}</b><span>{e(c["label"])}</span></p>'
def header(role=""):
    return f'''<a class="ed-skip" href="#content">본문으로 이동</a>
    <header class="ed-header">
      <a class="ed-wordmark" href="/" aria-label="김시후 포트폴리오 홈"><strong>Kim<br>Sihoo</strong><span>PORTFOLIO</span></a>
      <nav class="ed-role-nav" aria-label="직군별 포트폴리오">
        {''.join(f'<a href="/{r}/"'+(' aria-current="page"' if r==role else '')+f'>{e(ROLES[r]["name"])}</a>' for r in ROLES)}
      </nav>
      <nav class="ed-secondary-nav" aria-label="프로필과 연락"><a href="/#/works">프로젝트 기록</a><a href="#contact">연락</a></nav>
    </header>'''
def footer():
    return '''<footer class="ed-footer" id="contact"><span>김시후 · 기획 / 게임 분석·QA<br>결정한 것과 확인한 것을 기록합니다.</span>
    <div class="ed-footer-links"><a href="mailto:kimshlife@naver.com">kimshlife@naver.com</a><a href="https://github.com/kimshlife" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="/#/about">프로필과 이력</a></div></footer>'''
def page(role, heading, description, main, path, aliases=None):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(heading)} — 김시후 포트폴리오</title><meta name="description" content="{e(description)}">
<meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#f3f0e8">
<meta property="og:type" content="website"><meta property="og:title" content="{e(heading)} — 김시후 포트폴리오">
<meta property="og:description" content="{e(description)}"><meta property="og:url" content="https://kimshlife.github.io{path}">
<meta property="og:image" content="https://kimshlife.github.io/assets/img/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://kimshlife.github.io{path}"><link rel="icon" href="/assets/brand/favicon.svg" type="image/svg+xml"><link rel="alternate icon" href="/favicon.ico">
<link rel="stylesheet" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="/assets/css/editorial.css?v={VERSION}"><script defer src="/assets/js/editorial.js?v={VERSION}"></script>
</head><body class="editorial-site"{f' data-ed-aliases="{e(json.dumps(aliases))}"' if aliases else ''}>
<div class="ed-page{' ed-qa-index' if role=='qa' and aliases else ''}">{header(role)}<main class="ed-main" id="content">{main}</main>{footer()}</div></body></html>
'''
def cover(c, small=False):
    if small and c["cover"] == "survey":
        return '<span class="ed-row-type" aria-hidden="true">12 + 3<br>QUESTION DESIGN</span>'
    if small and c["cover"] == "reference":
        return '<span class="ed-row-type" aria-hidden="true">채택 · 변환<br>제외</span>'
    return f'<img class="{"ed-row-image" if small else ""}" src="{ASSETS[c["cover"]]}" alt="{e(c["coverCaption"])}" loading="{"lazy" if small else "eager"}"'+(' fetchpriority="high"' if not small else '')+'>'
def index(role):
    r, cases = ROLES[role], DATA[role]
    c = cases[0]
    rows = ''.join(f'''<a class="ed-work-row" href="{href(role,item)}"><span class="ed-work-no">0{i+2}</span>{cover(item,True)}
      <span class="ed-row-copy"><small>{e(item['project'])} / {e(item['label'])}</small><strong>{e(item['short'])}</strong><span>{e(item['evidence'])}</span></span><span class="ed-arrow" aria-hidden="true">↗</span></a>''' for i,item in enumerate(cases[1:]))
    extra = '''<section class="ed-more-work" id="more"><h2>그 밖의 기획</h2>
    <a href="/#/works/sickkick"><strong>SICK KICK ↗</strong><small>사업·서비스 기획 / 2023 — 의료 공백 대응 서비스의 규제와 설계 범위 검토</small></a>
    <a href="/#/works/contentops"><strong>콘텐츠 운영 컨설턴트 ↗</strong><small>신직업 설계 / 2023 — 유저와 운영의 소통 문제를 직무·자격·인증제로 구체화</small></a>
    <a href="/#/works/pirukia"><strong>Pirukia ↗</strong><small>세계관·콘텐츠 기획 / 2022–2023 — 9신 × 6요소 설정 템플릿과 교리 선택지 설계</small></a></section>''' if role=="planning" else ''
    background = '<span>게임·서비스의 규칙과 명세, 구현 연결을 담당했습니다.</span>' if role=="planning" else '<span>제조업 품질보증 2년 2개월 · 게임 프로젝트 분석·검증 · 장기 플레이 기록</span><a href="/qa/kimsihoo-qa-portfolio.pdf" target="_blank" rel="noopener noreferrer">포트폴리오 PDF 7쪽 ↗</a>'
    main = f'''<section class="ed-intro" id="about"><div><span class="ed-kicker">SELECTED WORK / {r['en']}</span><h1>{r['name']}</h1></div>
    <p class="ed-intro-copy" id="method">{r['purpose']}<small>{r['sub']}</small></p></section>
    <section class="ed-feature" id="cases"><figure><a class="ed-cover-link" href="{href(role,c)}" aria-label="{e(c['project'])} {r['name']} 사례 읽기"><div class="ed-cover">{cover(c)}</div></a><figcaption class="ed-caption">{e(c['coverCaption'])}</figcaption></figure>
    <div>{project(c)}<h2>{'<br>'.join(e(line) for line in c['headline'])}</h2><p class="ed-feature-desc">{e(c['summary'])}</p><a class="ed-read" href="{href(role,c)}">사례 읽기</a></div></section>
    <div class="ed-list-label"><h2>다른 판단과 결정</h2><span>총 4개 사례</span></div>{rows}
    {extra}<div class="ed-role-about">{background}<a href="/#/about">프로필과 이력 보기 →</a></div>'''
    aliases = {old:href(role,{"id":new}) for old,new in ALIASES[role].items()}
    aliases["analysis"] = f"/{role}/#method"
    return page(role, r['name'],r['purpose'],main,f'/{role}/',aliases)
def proof(c):
    names = {"owner":"그림 소유권 설계 도식", "workshop":"맵 에디터와 검증 상태", "slope":"수정 후 실제 플레이 화면", "reference":"SSketch 설정 창 구현", "survey":"ProjectRG 문제 정의 장표", "tetris":"NeonTetrisWars 대전 화면", "observation":"본인 작성 게임 분석 문서"}
    image = {"owner":"owner","workshop":"workshop","slope":"slope","reference":"reference","survey":"survey","tetris":"tetris","observation":"document"}.get(c['proof'])
    result = ''
    if image:
        result = f'''<figure class="ed-proof-image"><a href="{ASSETS[image]}" target="_blank" rel="noopener noreferrer" aria-label="{names[c['proof']]} 원본 확대"><img src="{ASSETS[image]}" alt="{names[c['proof']]}" loading="lazy"></a><figcaption class="ed-caption">{names[c['proof']]} · 이미지 선택 시 원본 보기{(' / 결함 재현 장면이 아닌 수정 후 화면입니다.' if image=='slope' else '')}</figcaption></figure>'''
    if c['proof']=='feedback':
        rows = [("평가 담합·보복 투표","약 11"),("절도와 점수의 연결","6"),("절도·훼손 과정 설명","5"),("그림 실력 격차","5"),("복잡도·구현 난이도","3"),("AI 객관 평가 활용","3"),("차별성·주제 설득력","3"),("세션 길이","2"),("인원 확장·밤 절도 성공률·러버밴딩 악용·익명성 붕괴","각 1")]
        result = '<section class="ed-proof-text"><h3>피드백 유형과 빈도</h3><table class="ed-table ed-number-table"><caption>내용 없는 응답 3건 제외 · 한 응답의 여러 지적은 각각 집계</caption><thead><tr><th scope="col">지적 내용</th><th scope="col">건수</th></tr></thead><tbody>'+''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a,b in rows)+'</tbody></table></section>'
    if c.get('overviewTables'):
        result += '<section class="ed-proof-text"><h3>판단의 기준</h3>'+''.join(c['overviewTables'])+'</section>'
    if c['proof']=='owner':
        result += '<section class="ed-proof-text"><h3>코드 기준 진행 기록</h3><p>요구사항 250건 · 12개 대분류 / 2026.09.26 진행률 62%</p><figure class="ed-proof-image"><a href="/assets/img/ss-req.jpg" target="_blank" rel="noopener noreferrer"><img src="/assets/img/ss-req.jpg" alt="대분류·담당·우선순위별 요구사항 진행률 요약 시트" loading="lazy"></a><figcaption class="ed-caption">요구사항 요약 시트 · 원본 보기 ↗</figcaption></figure></section>'
    result += '<p class="ed-caption">'+e(c['source'].replace('기획 페이지 · ','').replace('QA 페이지 · ',''))+'</p>'
    return result
def decisions(c):
    return '<section class="ed-proof-text"><h3>결정과 근거 기록</h3>'+''.join(f'<div class="ed-record-row"><b>{e(label)}</b><p>{e(text)}</p></div>' for label,text in c['decisions'])+f'<p class="ed-caption">{e(c["source"].replace("기획 페이지 · ","").replace("QA 페이지 · ",""))}</p></section>'
def scope(c):
    return f'<div class="ed-record-row"><b>{e(c["record"])}</b><p>{e(c["result"])}</p></div><div class="ed-record-row"><b>본인 기여와 경계</b><p>{e(c["boundary"])}</p></div>'
def detail(role,c,i):
    r = ROLES[role]
    story = ''.join(f'<section class="ed-story-section"><span>0{n+1}</span><h2>{e(h)}</h2><p>{e(p)}</p></section>' for n,(h,p) in enumerate(c['sections']))
    tabs = ''.join(f'<button type="button" role="tab" id="evidence-tab-{n}" aria-controls="evidence-panel-{n}" aria-selected="{str(n==0).lower()}">{name}</button>' for n,name in enumerate(('근거 자료','판단 기록','진행·기여')))
    panels = ''.join(f'<div class="ed-proof-panel" id="evidence-panel-{n}" role="tabpanel" aria-labelledby="evidence-tab-{n}">{body}</div>' for n,body in enumerate((proof(c),decisions(c),'<section class="ed-proof-text"><h3>진행·검증 범위</h3>'+scope(c)+'</section>')))
    records = ''.join(f'<details class="ed-detail-record"><summary><span>0{n+1}</span>{e(record["title"])}</summary><div class="ed-record-content">{record["html"]}</div></details>' for n,record in enumerate(c['records']))
    other = 'qa' if role=='planning' else 'planning'
    cross = next((item for item in DATA[other] if item['id']==c.get('cross')),None)
    cross_link = f'''<nav class="ed-other-role" aria-label="관련 사례"><span>관련 사례</span><a href="{href(other,cross)}">{e(cross['project'])} · {ROLES[other]['name']} 관점 보기 →</a></nav>''' if cross else ''
    next_case = DATA[role][(i+1)%len(DATA[role])]
    main = f'''<a class="ed-back" href="/{role}/">← 사례 목록</a>
    <article><header class="ed-case-head"><div><span class="ed-kicker">{r['en']} / CASE STUDY</span>{project(c)}<h1>{title(c)}</h1><p class="ed-case-lead">{e(c['summary'])}</p>
    <div class="ed-case-meta"><span>{e(c['period'])}</span><span>{e(c['team'])}</span></div></div></header>
    <div class="ed-story-grid"><div>{story}</div><aside class="ed-evidence" aria-label="근거와 상세 기록" data-ed-evidence><div class="ed-evidence-tabs" role="tablist" aria-label="근거 내용 선택" hidden>{tabs}</div>{panels}</aside></div>
    <section class="ed-scope"><h2>진행 결과와 본인 기여</h2><div class="ed-scope-grid"><div><b>{e(c['record'])}</b><p>{e(c['result'])}</p></div><div><b>담당한 범위</b><p>{e(c['boundary'])}</p></div></div></section>{cross_link}
    <section class="ed-records"><h2>{'설계 기록' if role=='planning' else '분석·검증 기록'}</h2><p>항목을 펼치면 세부 판단과 원본 자료를 읽을 수 있습니다.</p>{records}</section>
    <div class="ed-resources">{c['resourceHtml']}</div></article><nav class="ed-next-case" aria-label="다른 사례"><a href="/{role}/">← {r['name']} 사례 전체</a><a href="{href(role,next_case)}">다음 사례 · {e(next_case['project'])} →</a></nav>'''
    return page(role, c['project']+' · '+r['name'],c['summary'],main,href(role,c))

if __name__ == '__main__':
    count = 0
    for role, cases in DATA.items():
        (ROOT / role / 'index.html').write_text(index(role),encoding='utf-8')
        count += 1
        for i,c in enumerate(cases):
            target = ROOT / role / c['id'] / 'index.html'
            target.parent.mkdir(exist_ok=True)
            target.write_text(detail(role,c,i),encoding='utf-8')
            count += 1
    print(f'Generated {count} editorial portfolio pages.')

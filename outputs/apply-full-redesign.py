from pathlib import Path
import re
root=Path.cwd()
def write(path,s): (root/path).write_text(s,encoding='utf-8')
def read(path): return (root/path).read_text(encoding='utf-8')
header='''<a class="skip-link" href="#stage">본문으로 이동</a><header class="site-header"><div class="site-header-inner"><a class="site-brand" href="/#/"><img src="/assets/brand/app-icon.svg" alt="">김시후 <small>PORTFOLIO</small></a><nav class="site-nav" aria-label="주요 메뉴"><a href="/#/works" data-section="works">프로젝트</a><a href="/planning/" data-section="planning">기획</a><a href="/qa/" data-section="qa">게임 분석·QA</a><a href="/#/about" data-section="about">소개</a><a href="/#/hobby" data-section="hobby">플레이 기록</a><a href="/#/contact" data-section="contact">연락</a></nav><a class="site-email" href="mailto:kimshlife@naver.com">이메일 ↗</a></div></header>'''
footer='''<footer class="site-footer"><span>김시후 · 게임·서비스 기획 / 게임 분석·QA</span><div><a href="mailto:kimshlife@naver.com">이메일</a><a href="https://github.com/kimshlife" target="_blank" rel="noopener">GitHub ↗</a><a href="/#/about/award">수상·자격</a></div></footer>'''
s=read('index.html');s=s.replace('<body>','<body>'+header);s=s.replace('<dialog class="lb"',footer+'<dialog class="lb"');s=s.replace('</head>','<link rel="stylesheet" href="assets/css/renewal.css?v=20261013">\n</head>');s=s.replace('SunsHineKim, Kim Si Hoo','김시후 — 게임·서비스 기획 / 게임 분석·QA');s=s.replace('20261007c','20261013');write('index.html',s);write('404.html',s)
s=read('assets/js/icons.js');s=s.replace("award:'", "trophy:'M8 3h8v5a4 4 0 0 1-8 0V3ZM8 5H4v2a4 4 0 0 0 4 4M16 5h4v2a4 4 0 0 1-4 4M12 12v5M8 21h8M9 17h6v4H9z',\n  award:'");write('assets/js/icons.js',s)
s=read('assets/js/app.js')
start=s.index('function viewSelect()');end=s.index('const CARD_ROLES=',start)
s=s[:start]+'''function viewSelect(){return `<section class="home-intro"><div><span class="eyebrow">KIM SI HOO / PORTFOLIO</span><h1 class="d1">생각을 규칙으로,<br>경험을 더 나은<br>플레이로.</h1><p class="home-position">김시후 · 게임·서비스 기획 / 게임 분석·QA</p><p>요구사항과 규칙을 설계하고, 실제 플레이에서 발견한 문제를 재현 조건과 검증 근거로 남깁니다.</p><div class="home-actions"><a class="abtn primary" href="#/works">프로젝트 살펴보기 ↗</a><a class="abtn" href="mailto:kimshlife@naver.com">이메일로 연락하기</a></div></div><figure><img src="assets/img/ss-title.jpg" alt="SSketch — 위대한 그림 도둑" fetchpriority="high"><figcaption>${ico('trophy',17)} SSketch · SSAFY 15기 특화 프로젝트 우수상</figcaption></figure></section>
<section class="role-paths" aria-label="직군별 포트폴리오"><a class="role-path" href="planning/"><span class="eyebrow">PLANNING</span><h2>기획</h2><p>규칙·수치·요구사항을 결정하고<br>실행 가능한 명세로 연결한 작업.</p><span class="go">기획 사례 4개 보기 →</span></a><a class="role-path" href="qa/"><span class="eyebrow">GAME ANALYSIS / QA</span><h2>게임 분석·QA</h2><p>이용자의 문제를 관찰하고<br>재현·원인 분석·검증으로 이어간 작업.</p><span class="go">분석·검증 사례 4개 보기 →</span></a></section>
<section class="home-section"><div class="section-line"><div><span class="eyebrow">SELECTED PROJECTS</span><h2>대표 프로젝트</h2></div><a href="#/works">전체 7개 프로젝트 →</a></div><div class="cards">${['ssketch','bodybuilder','sickkick','contentops'].map(cardHTML).join('')}</div></section>
<section class="home-section home-about"><div><span class="eyebrow">ABOUT ME</span><h2>제약을 이해하고,<br>함께 실행할 기준을 만듭니다.</h2><a href="#/about">소개와 역량 보기 →</a></div><dl>${SELECT.sheet.map(([k,v,d])=>`<div><dt>${k}</dt><dd>${v}${d?`<small>${d}</small>`:''}</dd></div>`).join('')}</dl></section>
<section class="home-section"><div class="section-line"><h2>오래 플레이하며 남긴 기록</h2><a href="#/hobby">플레이 기록 →</a></div><p class="work-intro">${GAMES.length}개 게임의 플레이 기록, 6년간의 길드 운영, 한 게임을 오래 관찰한 분석 문서를 모았습니다.</p></section>`}

const PROJECT_AWARDS={ssketch:'SSAFY 특화 프로젝트 우수상',sickkick:'교내 대상 · K7U-Belt 장려상',contentops:'대한민국 신직업 공모전 장려상'};
function awardBadge(k){return PROJECT_AWARDS[k]?`<span class="award-badge">${ico('trophy',17)}<span>${PROJECT_AWARDS[k]}</span></span>`:'';}
''' + s[end:]
s=s.replace("${cardMedia(p)}\n  <div class=\"cardbody\">", "<div class=\"card-media\">${cardMedia(p)}${awardBadge(k)}</div>\n  <div class=\"cardbody\">")
s=s.replace("${sechead('work','Works',`${list.length}건`,1)}", "<span class=\"eyebrow\">PROJECT ARCHIVE</span>${sechead('work','프로젝트',`${list.length}개 프로젝트`,1)}<p class=\"work-intro\">게임부터 서비스·사업·콘텐츠까지. 각 프로젝트에서 맡은 역할과 판단의 근거를 정리했습니다.</p>")
s=s.replace("${radioChip('all',`전체 <span class=\"n\">${ORDER.length}</span>`)}", "${radioChip('all',`전체 <span class=\"n\">${ORDER.length}</span>`)}${radioChip('awarded',`${ico('trophy',15)} 수상 프로젝트 <span class=\"n\">${Object.keys(PROJECT_AWARDS).length}</span>`)}")
s=s.replace("list=c==='all'?ORDER:ORDER.filter(k=>P[k].cats.includes(c))", "list=c==='all'?ORDER:c==='awarded'?ORDER.filter(k=>PROJECT_AWARDS[k]):ORDER.filter(k=>P[k].cats.includes(c))")
s=s.replace('${docspec(p)}','${docspec(p)}${PROJECT_AWARDS[state.slug]?`<div class="award-detail">${awardBadge(state.slug)} <a href="#/about/award">수상 내역 →</a></div>`:\'\'}',1)
s=s.replace("function blk(no,icon,t,inner){return `<div class=\"block\">", "function blk(no,icon,t,inner){return `<div class=\"block\" id=\"section-${no==='◆'?'overview':no}\">")
s=s.replace("${blk('01','problem','문제 정의'", "<nav class=\"project-toc\" aria-label=\"프로젝트 목차\"><a href=\"#section-01\" data-scroll=\"section-01\">문제 정의</a><a href=\"#section-02\" data-scroll=\"section-02\">역할과 판단</a><a href=\"#section-03\" data-scroll=\"section-03\">산출물</a><a href=\"#section-04\" data-scroll=\"section-04\">회고</a></nav>${blk('01','problem','문제 정의'",1)
s=s.replace('기획 설명서','기획 사례').replace('QA 설명서','QA 사례').replace('${n} 설명서','${n} 사례').replace('이 프로젝트가 실린 설명서','직군별 사례').replace('MODEL 02 · 게임 분석·QA','게임 분석·QA').replace('MODEL 01 · 기획','기획')
a=s.index('function aboutAward()');b=s.index('function aboutEtc()',a)
s=s[:a]+'''function aboutAward(){return `<section class="sec">${sechead('trophy','수상',`${AWARDS.length}건 · Awards`)}<div class="award-list">${AWARDS.map(a=>`<article class="award-row"><div class="award-icon">${ico('trophy',24)}</div><time>${a[0]}</time><div><h3>${a[3]} · ${a[1]}</h3><p>${a[2]}</p><p>담당: ${a[4]}</p><small>${a[5]}</small></div></article>`).join('')}</div><p class="cap" style="margin-top:18px">증빙 자료는 요청 시 제공합니다.</p></section><section class="sec">${sechead('cert','자격','Certificates')}${tbl([['자격명','250px'],['종류','150px'],['시행 기관','180px'],['취득','']],CERTS,['st','q','q','m'])}</section>`}
''' + s[b:]
a=s.index('function hobbyHome()');b=s.index('function gameHero()',a)
s=s[:a]+'''function hobbyHome(){return `<section class="hobbyhero"><span class="eyebrow">PLAY & OBSERVATIONS</span><h1 class="d1">좋아서 오래 한 것들,<br>그 안에서 발견한 것들.</h1><p>${GAMES.length}개 게임의 플레이 기록과 6년간의 길드 운영. 취미로 쌓아온 경험을 기록과 문서로 남겼습니다.</p></section><div class="hobbyareas"><a class="areacard" href="#/hobby/game">${ico('game',26)}<h2 class="h3">플레이의 흐름</h2><p>게임을 고르는 이유가 어떻게 바뀌었는지.</p><span class="go">경험의 흐름 보기 →</span></a><a class="areacard" href="#/hobby/game/record">${ico('content',26)}<h2 class="h3">${GAMES.length}개 게임 기록</h2><p>시기와 플레이 이유로 살펴보는 게임 목록.</p><span class="go">전체 기록 보기 →</span></a><a class="areacard" href="#/hobby/game/docs">${ico('doc',26)}<h2 class="h3">운영·분석 문서</h2><p>길드 운영과 라이브 서비스 관찰을 담은 두 문서.</p><span class="go">문서 읽기 →</span></a></div>`}

''' +s[b:]
s=s.replace("${sechead('mail','Contact','연락처',1)}", "<span class=\"eyebrow\">CONTACT</span><h1 class=\"contact-lead\">함께 만들 이야기를<br>기다립니다.</h1>")
s=s.replace("'이메일로 요청해 주시면 전달드리겠습니다.'", "'<a class=\"abtn\" href=\"mailto:kimshlife@naver.com?subject=이력서%20요청\">이력서 요청하기 ↗</a>'")
s=s.replace("  s.innerHTML=h;n.innerHTML=nt;", """  s.innerHTML=h;n.innerHTML=nt;
  document.body.dataset.view=state.view;
  document.title=(s.querySelector('h1')?.textContent||'포트폴리오')+' — 김시후';
  const section=({select:'home',detail:'works',workshop:'works'})[state.view]||state.view;
  document.querySelectorAll('[data-section]').forEach(a=>{if(a.dataset.section===section)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
""")
s=s.replace("  const gf=e.target.closest('[data-gf]');", """  const anchor=e.target.closest('[data-scroll],.skip-link');
  if(anchor){e.preventDefault();const t=document.getElementById(anchor.dataset.scroll||'stage');if(t){t.setAttribute('tabindex','-1');t.focus({preventScroll:true});t.scrollIntoView({block:'start'});}return;}
  const gf=e.target.closest('[data-gf]');""")
write('assets/js/app.js',s)
# Rebuild role collections around the existing complete case records.
trophy='<svg class="ic" viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M8 3h8v5a4 4 0 0 1-8 0V3ZM8 5H4v2a4 4 0 0 0 4 4M16 5h4v2a4 4 0 0 1-4 4M12 12v5M8 21h8M9 17h6v4H9z" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
for role in ['planning','qa']:
 s=read(role+'/index.html');s=s.replace('<body>','<body class="role-page">'+header.replace('#stage','#role-content').replace('data-section="'+role+'"','data-section="'+role+'" aria-current="page"'));s=s.replace('<main>','<main id="role-content">')
 s=s.replace('</head>','<link rel="stylesheet" href="../assets/css/renewal.css?v=20261013">\n</head>')
 s=s.replace('<h1 style="margin-top:12px">김시후<small>Kim Si Hoo</small></h1>','<h1 style="margin-top:12px">기획<small>김시후 · Portfolio</small></h1>') if role=='planning' else re.sub(r'<h1[^>]*>김시후<small>Kim Si Hoo</small></h1>','<h1>게임 분석·QA<small>김시후 · Portfolio</small></h1>',s)
 method=re.search(r'<section class="blk alt" id="(?:method|analysis)">[\s\S]*?</section>',s)
 if method:s=s.replace(method.group(),'<details class="method-disclosure"><summary>작업 방식과 사례별 수행 범위</summary>'+method.group()+'</details>')
 article_data=[]
 for m in re.finditer(r'<article class="case" id="([^"]+)">([\s\S]*?)</article>',s):
  id,content=m.groups();h=re.search(r'<h2>([\s\S]*?)</h2>',content).group(1);label=re.sub('<[^>]+>','',h)
  im=re.search(r'<img[^>]*src="([^"]+)"[^>]*>',content);pic=im.group(1) if im else '../assets/img/ss-flow.jpg'
  badge='<span class="award-badge">'+trophy+'SSAFY 특화 프로젝트 우수상</span>' if id=='ssketch' else ''
  article_data.append((id,label,pic,badge))
  new=content.replace('<h2>',badge+'<h2>',1)
  new=new.replace('</h2>','</h2><nav class="case-mini-nav" aria-label="사례 이동"><a href="#case-directory">← 사례 목록</a><a href="../#/works/'+('bodybuilder' if id=='workshop' else 'ssketch' if id=='reference' else id)+'">'+('프로젝트 전체 보기 →' if id!='counterside' else '플레이 기록 →')+'</a></nav>',1)
  if id=='counterside':new=new.replace('../#/works/counterside','../#/hobby/game/docs/analysis')
  s=s.replace(m.group(),'<article class="case" id="'+id+'">'+new+'</article>')
 cards=''.join('<a class="case-link" href="#'+i+'"><img src="'+pic+'" alt="'+label+'" loading="lazy"><div>'+badge+'<h3>'+label+'</h3><p>담당 역할과 판단의 근거 읽기 ↗</p></div></a>' for i,label,pic,badge in article_data)
 directory='<section class="case-directory" id="case-directory"><div class="wrap"><div class="section-line"><h2>선별한 사례</h2><span class="project-count">4개 사례</span></div><div class="case-grid-links">'+cards+'</div></div></section>'
 endhero=s.index('</section>',s.index('<section class="hero"'))+len('</section>');s=s[:endhero]+directory+s[endhero:]
 # Put methodology after the complete cases, so it never blocks the entry path.
 d=re.search(r'<details class="method-disclosure">[\s\S]*?</details>',s)
 if d:s=s.replace(d.group(),'');s=s.replace('<section class="contact"',d.group()+'\n<section class="contact"')
 labels=['제약 확인','핵심 경험','규칙·수치','명세·문서화','구현 연결','검증·수정'] if role=='planning' else ['관찰','문제 정의','재현 조건','원인·영향','개선안','검증']
 def row(m):
  n=[0]
  def td(t):
   k=n[0];n[0]+=1;return '<td data-step="'+labels[k%6]+'"'+t.group(1)+'>'
  return re.sub(r'<td([^>]*)>',td,m.group())
 s=re.sub(r'<tr><th><a[\s\S]*?</tr>',row,s)
 s=s.replace('href="#cases"','href="#case-directory"').replace('MANUAL 표지','포트폴리오 홈').replace('MODEL 01 · 기획','기획').replace('MODEL 02 · 게임 분석·QA','게임 분석·QA')
 s=re.sub(r'<span class="soon">[\s\S]*?</span>','',s)
 # Awarded supporting projects in the planning list.
 if role=='planning':
  s=s.replace('<b>SICK KICK</b>','<span class="award-badge">'+trophy+'교내 대상 · K7U-Belt 장려상</span><b>SICK KICK</b>')
  s=s.replace('<b>콘텐츠 운영 컨설턴트</b>','<span class="award-badge">'+trophy+'신직업 공모전 장려상</span><b>콘텐츠 운영 컨설턴트</b>')
 write(role+'/index.html',s)
# Preserve the distinct game archive, but make its portfolio return path clearer.
for page in ['ssketch/index.html','ssketch/privacy.html','ssketch/terms.html']:
 s=read(page)
 if page!='ssketch/index.html':s=s.replace('</body>','<p style="text-align:center;padding:24px"><a href="../#/works/ssketch" style="color:inherit">김시후 포트폴리오 · SSketch 사례로 돌아가기 →</a></p></body>')
 write(page,s)
ignore=read('.gitignore');write('.gitignore',ignore+'\n# Local backups and design audit outputs\nbackups/\noutputs/\n.codex_doc_work/\n')
print('Full-site renewal applied.')

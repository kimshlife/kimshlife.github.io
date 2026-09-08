/* ===== 네비 · 라우팅 ===== */
const NAV=[
 {id:'home',label:'Home',k:'build'},
 {id:'about',label:'About',k:'idea'},
 {id:'works',label:'Works',k:'work'},
 {id:'contact',label:'Contact',k:'mail'}
];
const $=s=>document.getElementById(s);
function buildNav(el){el.innerHTML=NAV.map(n=>
 `<a class="navlink" href="#/${n.id==='home'?'':n.id}" data-nav="${n.id}">${ico(n.k,18)}<span>${n.label}</span></a>`).join('')}
['nav-rail','nav-top','nav-tab'].forEach(i=>buildNav($(i)));
function syncNav(a){document.querySelectorAll('[data-nav]').forEach(x=>
 x.dataset.nav===a?x.setAttribute('aria-current','page'):x.removeAttribute('aria-current'))}

let state={view:'home',track:'base',slug:null,tab:'skill',filter:new Set()};
const TRACK_IDS=['hr','game','service','biz'];
/* 트랙이 앞세우기로 한 프로젝트를 먼저 두고, 나머지는 기본 순서로 뒤에 붙인다 */
function trackOrder(){
  const t=(typeof TRACKS!=='undefined'&&TRACKS[state.track])||null;
  if(!t||!t.order||!t.order.length)return ORDER;
  return t.order.concat(ORDER.filter(k=>t.order.indexOf(k)<0));
}
function route(){
  const wasAbout=state.view==='about';
  const parts=(location.hash||'#/').slice(2).split('/').filter(Boolean);
  state.slug=null;
  if(!parts.length){state.view='home';state.track='base';}
  else if(TRACK_IDS.indexOf(parts[0])>=0){state.view='home';state.track=parts[0];}
  else if(parts[0]==='works'){
    if(parts[1]==='bodybuilder'&&parts[2]==='workshop')state.view='workshop';
    else if(parts[1]){state.view='detail';state.slug=parts[1];}
    else state.view='works';
  } else if(parts[0]==='about'){state.view='about';state.tab=parts[1]||'skill';}
  else if(parts[0]==='contact')state.view='contact';
  else state.view='404';
  render();
  if(wasAbout&&state.view==='about'){
    const panel=$('about-panel');panel.focus({preventScroll:true});panel.scrollIntoView({block:'start'});
  }else window.scrollTo(0,0);
}
window.addEventListener('hashchange',route);

/* ===== 공통 ===== */
const IMG='assets/img/';
/* 이력서 — 공개할 준비가 되면 주소를 넣으세요. 비워 두면 '준비 중'으로 표시됩니다.
   예: RESUME='https://drive.google.com/file/d/....../view' */
const RESUME='';
function catDot(k){const c=CAT[k];return `<span class="cd"><i style="background:${c.c}"></i>${c.n}</span>`}
function tbl(head,rows,cls){return `<div class="scroll"><table class="tbl">
  <thead><tr>${head.map(h=>`<th scope="col"${h[1]?` style="width:${h[1]}"`:''}>${h[0]}</th>`).join('')}</tr></thead>
  <tbody>${rows.map(r=>`<tr>${r.map((c,i)=>`<td data-label="${head[i][0]}" class="${(cls&&cls[i])||''}"><div>${c}</div></td>`).join('')}</tr>`).join('')}</tbody>
</table></div>`}
/* lv=1 이면 h1 으로 그립니다. 화면마다 h1 이 하나씩은 있어야 스크린리더가 제목을 읽습니다 */
function sechead(icon,title,right,lv){const t=lv===1?'h1':'h2';
  return `<div class="sechead">${ico(icon,20)}<${t} class="d2">${title}</${t}>
  ${right?`<span class="cap">${right}</span>`:''}</div>`}

/* ===== HOME ===== */
function heroSVG(){return `<svg viewBox="0 0 640 330" role="img" aria-label="흩어진 생각이 검증 가능한 규칙을 거쳐 결과물이 되는 과정">
<defs><style>
.b{fill:#FFFFFF;stroke:#DDE5EC;stroke-width:1}
.l{stroke:#C0CCD8;stroke-width:1;fill:none}
.t{font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.14em;fill:#8494A8}
.s{font-family:'Pretendard Variable',sans-serif;font-size:11px;fill:#4A5C74}
</style></defs>
<rect width="640" height="330" fill="#F4F7F9"/>
<g opacity=".45">${Array.from({length:13},(_,i)=>`<line class="l" x1="${28+i*49}" y1="24" x2="${28+i*49}" y2="306" opacity=".3"/>`).join('')}</g>

<g><rect class="b" x="28" y="96" width="150" height="140" rx="8"/>
<text class="t" x="46" y="122">SCATTERED</text>
<path class="l" d="M48 146c18-12 32 9 50-3s28 10 46-2" stroke="#A6B6C6"/>
<path class="l" d="M48 168c26 7 38-10 56 2s34-5 48 5" stroke="#A6B6C6"/>
<path class="l" d="M48 190c14-9 36 7 54-2s32 7 50 0" stroke="#A6B6C6"/>
<circle cx="60" cy="212" r="3" fill="#C0CCD8"/><circle cx="86" cy="216" r="2.4" fill="#C0CCD8"/><circle cx="110" cy="210" r="3" fill="#C0CCD8"/>
<text class="s" x="46" y="230">흩어진 생각</text></g>

<path class="l" d="M186 166h42" stroke="#0F6C82"/><path d="M223 161l6 5-6 5" stroke="#0F6C82" fill="none" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>

<g><rect class="b" x="236" y="76" width="168" height="180" rx="8"/>
<text class="t" x="256" y="102">SPEC</text>
${[0,1,2,3,4].map(i=>`<rect x="256" y="${116+i*24}" width="11" height="11" rx="2" fill="none" stroke="#0F6C82" stroke-width="1.2"/>
<path d="M258.6 ${121.5+i*24}l2.2 2.3 4.2-4.4" stroke="#0F6C82" stroke-width="1.4" fill="none" stroke-linecap="round"/>
<rect x="276" y="${119+i*24}" width="${108-i*13}" height="5" rx="2.5" fill="#DDE5EC"/>`).join('')}
<text class="s" x="256" y="244">검증할 수 있는 규칙</text></g>

<path class="l" d="M412 166h42" stroke="#0F6C82"/><path d="M449 161l6 5-6 5" stroke="#0F6C82" fill="none" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>

<g><rect class="b" x="462" y="96" width="150" height="140" rx="8"/>
<text class="t" x="480" y="122">BUILT</text>
<rect x="480" y="136" width="114" height="52" rx="5" fill="#E0F0F3"/>
<circle cx="502" cy="162" r="9.5" fill="#0F6C82" opacity=".9"/>
<rect x="521" y="154" width="62" height="5" rx="2.5" fill="#0F6C82" opacity=".45"/>
<rect x="521" y="166" width="40" height="5" rx="2.5" fill="#0F6C82" opacity=".26"/>
<rect x="480" y="197" width="54" height="5" rx="2.5" fill="#DDE5EC"/>
<rect x="540" y="197" width="54" height="5" rx="2.5" fill="#DDE5EC"/>
<text class="s" x="480" y="230">다른 사람의 손에서 나온 결과</text></g>
</svg>`}

/* 그림 주소가 잘못돼도 Home 이 깨지지 않도록, 기본 도식으로 되돌립니다. */
function heroFallback(el){const w=el.closest('.homefig');if(w)w.outerHTML='<div class="homefig">'+heroSVG()+'</div>';}
/* Home 그림 — HOME.img 가 비어 있으면 기본 도식(heroSVG)으로 되돌아갑니다.
   파일명만 쓰면 assets/img/ 를, http(s)·data· assets/ 로 시작하면 그 주소를 그대로 씁니다. */
function homeFigure(){
  const s=(typeof HOME!=='undefined'&&HOME.img)||'';
  if(!s)return `<div class="homefig">${heroSVG()}</div>`;
  const abs=s.startsWith('http')||s.startsWith('//')||s.startsWith('data:')||s.startsWith('assets/');
  const url=abs?s:IMG+s;
  const w=HOME.width?` style="max-width:${HOME.width}"`:'';
  return `<figure class="homefig"${w}>
    <img class="${HOME.frame?'framed':''}" src="${url}" alt="${HOME.alt||''}" decoding="async"
      onerror="heroFallback(this)">
    ${HOME.cap?`<figcaption class="cap homecap">${HOME.cap}</figcaption>`:''}
  </figure>`;
}
function homeCopy(){
  const H=(typeof HOME!=='undefined')?HOME:{};
  const T=(typeof TRACKS!=='undefined'&&TRACKS[state.track])||{};
  const slogan=T.slogan||H.slogan||'';
  const intro=T.intro||H.intro||'';
  return `<div class="homeline">
    ${H.eyebrow?`<span class="eyebrow" style="margin-bottom:13px">${H.eyebrow}</span>`:''}
    <h1 class="d1">${slogan}</h1>
    ${intro?`<p class="homesub">${intro}</p>`:''}
  </div>`;
}
function viewHome(){
  const L=((typeof HOME!=='undefined'&&HOME.layout)||'stack');
  const fig=homeFigure(),copy=homeCopy();
  return `<div class="homewrap home-${L}">${L==='text'?copy+fig:fig+copy}</div>
    <div class="home-actions"><a class="abtn primary" href="#/works">프로젝트 보기 ${ico('work',17)}</a><a class="abtn" href="#/contact">연락하기 ${ico('mail',17)}</a></div>
    <section class="featured"><div class="sechead"><h2 class="d2">대표 프로젝트</h2><a href="#/works" class="cap">전체 보기 →</a></div>
    <div class="cards">${['bodybuilder','projectrg'].map(cardHTML).join('')}</div></section>`;
}

const CARD_ROLES={
  bodybuilder:'UGC 정책·명세 설계 · 캐릭터 상태 설계 · 프론트엔드',
  neontetris:'게임 규칙 표준화 · 락 딜레이·회전 제한 설계',
  projectrg:'5축 진단 체계 · 보충 질문 규칙 · 프론트엔드',
  sickkick:'시장·규제 분석 · 수익 구조 · 사업 전략',
  contentops:'팀 운영 · 산업 분석 · 자격·기업 인증제 설계',
  pirukia:'9신 세계관 구조 · 교리 선택지 콘텐츠 설계'
};

/* ===== WORKS ===== */
function cardMedia(p){
  if(p.thumb)return `<img class="cardthumb" src="${IMG}${p.thumb}" alt="" loading="lazy">`;
  /* 이미지가 아직 없는 프로젝트 — 문서 규격을 그대로 자리표시자로 씁니다 */
  return `<div class="cardph"><span class="phid">${p.docId}</span><span class="phv">${p.ver}</span></div>`;
}
function cardHTML(k){const p=P[k];return `<a class="card" href="#/works/${p.slug}">
  ${cardMedia(p)}
  <div class="cardbody">
    <div class="top">${p.cats.map(catDot).join('')}</div>
    <h3 class="ttl">${p.title}</h3>
    <div class="what">${p.what}</div>
    <div class="rolebox"><span class="eyebrow" style="margin-bottom:6px">핵심 기여</span><div class="txt">${CARD_ROLES[k]||p.role}</div></div>
    <div class="when">${p.period}<span class="card-go">프로젝트 보기 ↗</span></div>
  </div></a>`}
function viewWorks(){
  const f=state.filter,ord=trackOrder(),list=ord.filter(k=>!f.size||P[k].cats.some(c=>f.has(c)));
  const cnt=k=>ORDER.filter(s=>P[s].cats.includes(k)).length;
  return `<section>
    ${sechead('work','Works',`${list.length}건`,1)}
    <div class="filters">
      <button type="button" class="chip" aria-pressed="${!f.size}" data-cat="all">전체 <span class="n">${ORDER.length}</span></button>
      ${Object.keys(CAT).map(k=>`<button type="button" class="chip" aria-pressed="${f.has(k)}" data-cat="${k}">
        <i style="background:${CAT[k].c}"></i>${CAT[k].n} <span class="n">${cnt(k)}</span></button>`).join('')}
    </div>
    ${list.length?`<div class="cards">${list.map(cardHTML).join('')}</div>`
      :`<div class="empty"><p class="cap" style="margin-bottom:18px">선택한 조건에 맞는 프로젝트가 없습니다.</p>
        <button type="button" class="abtn" data-cat="all">필터 초기화</button></div>`}
  </section>`;
}

/* ===== 상세 ===== */
function docspec(p){return `<div class="docspec">
  <div class="meta">${p.period} · ${p.team}</div>
  <h1 class="d2">${p.title}</h1>
  <p class="body-l project-intro">${p.what}</p>
  <div style="display:flex;gap:12px;margin-top:10px;flex-wrap:wrap">${p.cats.map(catDot).join('')}</div>
  <p class="project-role">${p.role}</p>
  <details class="project-spec"><summary>담당 범위와 프로젝트 정보</summary><dl>
    <dt class="eyebrow">기획 원안</dt><dd class="dim">${p.originator}</dd>
    <dt class="eyebrow">담당 범위</dt><dd><ul>${p.scope.map(s=>`<li>${s}</li>`).join('')}</ul></dd>
    <dt class="eyebrow">팀 구성</dt><dd class="dim">${p.team}</dd>
    <dt class="eyebrow">기술 환경</dt><dd class="dim">${p.stack}</dd>
    <dt class="eyebrow">산출물</dt><dd class="dim">${p.outputs}</dd>
  </dl><p class="cap spec-id">${p.docId} · ${p.ver}</p></details></div>`}
function blk(no,icon,t,inner){return `<div class="block"><div class="blockhead">
  <span class="no">${no}</span>${ico(icon,18)}<h2 class="h3">${t}</h2></div>${inner}</div>`}
function gallery(p){
  if(!p.gallery||!p.gallery.length)return '';
  const st=p.galRatio?` style="aspect-ratio:${p.galRatio}"`:'';
  return `<div class="gal">${p.gallery.map(g=>
    `<figure><button type="button" class="gallery-open" aria-label="이미지 확대: ${g.c}"><img src="${IMG}${g.f}.${g.e||'jpg'}" alt="${g.c}" loading="lazy"${st}><span aria-hidden="true">확대 ↗</span></button><figcaption>${g.c}</figcaption></figure>`).join('')}</div>`;
}
const YT_ALLOW='accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture;web-share';
function ytEmbeddable(){return location.protocol==='http:'||location.protocol==='https:'}
function ytFrame(id){return `<iframe class="frame" src="https://www.youtube.com/embed/${id}?autoplay=1&amp;rel=0&amp;playsinline=1"
    title="시연 영상" referrerpolicy="strict-origin-when-cross-origin"
    allow="${YT_ALLOW}" allowfullscreen></iframe>`}
function videoSlot(p){
  if(p.video===undefined)return '';
  if(!p.video)return `<div class="vid"><div class="vidph">${ico('play',26)}<span class="cap">시연 영상 준비 중</span></div></div>`;
  const id=p.video, watch=`https://www.youtube.com/watch?v=${id}`;
  /* 썸네일 파사드 — 클릭할 때만 iframe을 삽입한다.
     file:// 로 열면 유튜브가 Referer를 받지 못해 오류 153이 나므로, 그때는 새 탭 링크로 대체한다. */
  const face=`<img class="vidthumb" src="https://i.ytimg.com/vi/${id}/maxresdefault.jpg" alt="" decoding="async"
      onerror="this.onerror=null;this.src='https://i.ytimg.com/vi/${id}/hqdefault.jpg'"><span class="pbtn">${ico('play',30)}</span>`;
  const facade = ytEmbeddable()
    ? `<button class="vidfacade" type="button" data-yt="${id}" aria-label="시연 영상 재생">${face}</button>`
    : `<a class="vidfacade" href="${watch}" target="_blank" rel="noopener" aria-label="유튜브에서 시연 영상 보기">${face}
        <span class="vnote">로컬 파일(file://)에서는 유튜브 재생이 차단됩니다 · 클릭하면 유튜브에서 열립니다</span></a>`;
  return `<div class="vid">${facade}</div>
    <p class="cap" style="margin-top:8px"><a href="${watch}" target="_blank" rel="noopener">유튜브에서 보기 →</a></p>`;
}
/* 링크가 없는 산출물은 <a> 로 만들지 않습니다. href="#" 이면 눌렀을 때 첫 화면으로 튕깁니다 */
function artifactBtn(l){
  const inner=`${ico(l.href&&l.href.startsWith('#')?'doc':'link',16)}${l.t} <span class="m">${l.m}</span>`;
  if(l.off||!l.href)return `<span class="abtn" aria-disabled="true">${inner}</span>`;
  const ext=!l.href.startsWith('#');
  return `<a class="abtn" href="${l.href}"${ext?' target="_blank" rel="noopener"':''}>${inner}</a>`;
}
function viewDetail(){
  const p=P[state.slug];if(!p)return view404();
  const ord=trackOrder(),i=ord.indexOf(state.slug),pv=ord[(i-1+ord.length)%ord.length],nx=ord[(i+1)%ord.length];
  return `<a class="crumb" href="#/works">${ico('work',15)} Works</a>
  ${docspec(p)}
  ${p.thumb?`<figure class="project-cover"><img src="${IMG}${p.thumb}" alt="${p.title} 대표 화면" fetchpriority="high"></figure>`:''}
  <div class="project-actions">${p.links.map(artifactBtn).join('')}</div>
  <section class="project-highlights" aria-label="주요 수치와 근거"><h2 class="h3">주요 수치와 근거</h2><div class="metrics">${p.metrics.map(m=>
    `<div class="metric"><div class="val">${m.v}</div><div class="lb">${m.l}</div><div class="src">${m.s}</div></div>`).join('')}</div></section>
  ${blk('01','problem','문제 정의',p.problem.map(t=>`<p style="color:var(--ink-2)">${t}</p>`).join(''))}
  ${blk('02','decide','역할과 의사결정',p.decisions.map(d=>`<div class="dec">
    <div class="h">${ico('spec',16)}<span>${d.h}</span></div><div class="b">${d.b}</div>
    ${d.link?`<p class="cap" style="margin:9px 0 0 25px"><a href="${d.link}">${d.linkT} →</a></p>`:''}</div>`).join(''))}
  ${p.notes.map(n=>`<div class="note inline-note"><b>${n.t}</b>${n.b}</div>`).join('')}
  ${blk('03','doc','산출물',`<p class="cap">${p.outputs}</p>${gallery(p)}${videoSlot(p)}`)}
  ${blk('04','result','회고',`<p style="color:var(--ink-2)">${p.retro}</p>`)}
  <div class="pager"><a href="#/works/${pv}">← ${P[pv].title}</a><a href="#/works/${nx}">${P[nx].title} →</a></div>`;
}

/* ===== 창작마당 심화 ===== */
function viewWorkshop(){const p=P.bodybuilder;return `<a class="crumb" href="#/works/bodybuilder">${ico('work',15)} BodyBuilder</a>
<div class="docspec">
  <div class="meta">BodyBuilder / 창작마당 기능 · 명세서 v9 · 2026.08</div>
  <h1 class="d2">창작마당 — 유저 맵 제작·공유 시스템</h1>
  <dl>
    <dt class="eyebrow">담당</dt><dd>구현명세서(v1–v9), 프론트·백엔드 작업지시서 작성 · 정책 설계 · 프론트엔드 구현</dd>
    <dt class="eyebrow">수행 구조</dt><dd class="dim">백엔드는 작성한 지시서에 따라 다른 팀원이 수행</dd>
    <dt class="eyebrow">범위</dt><dd class="dim">Phase 1 (좋아요·평점·댓글은 Phase 2로 분리)</dd>
  </dl></div>

${blk('◆','doc','문서를 다루는 방식',tbl([['항목','130px'],['내용','']],[
 ['전제 재검증','기준 커밋이 바뀌자 명세가 딛고 선 5개 전제를 전부 다시 확인하고 판정을 남겼습니다. 그 과정에서 시뮬레이션 입력 시그니처가 바뀐 것을 발견해 기록했습니다.'],
 ['범위 산정','프로토타입을 전부 반영하면 테이블 3개와 API 6개, 인증 로직이 추가되어 범위가 두 배 이상이 된다고 산정했습니다. 핵심 가치는 맵을 만들어 함께 노는 것이고 소셜 기능은 그 위에 얹는 층이라고 판단해 Phase 2로 잘랐습니다.'],
 ['변경 파급 추적','창작마당을 로비 탭에서 헤더 최상위로 옮기는 변경이, 방 생성 요청에 스테이지 값이 필요해지는 API 계약 변경까지 이어진다는 것을 짚었습니다.']
],['st','q']))}

${blk('01','problem','기능 정의',
`<p style="color:var(--ink-2)">공식 맵만으로는 콘텐츠가 곧 소진됩니다. 유저가 직접 맵을 만들어 공유하면 플레이할 거리가 계속 생기지만, 동시에 두 가지 위험이 따라옵니다. 깰 수 없는 맵이 공개되어 다른 사람의 시간을 버리는 것, 그리고 부가 기능의 문제가 본 게임을 막는 것입니다.</p>
<p style="color:var(--ink-2)">따라서 이 기능의 설계 목표는 창작 자유도가 아니라 <mark>품질 보증과 격리</mark>였습니다.</p>
<div class="gal" style="margin-top:20px">
<figure><img src="${IMG}ws-list.jpg" alt="창작마당 목록 화면" loading="lazy"><figcaption>공개 맵 탐색 — 팔레트 그라디언트 썸네일, 난이도 뱃지, 우하단에 폴리곤·기믹 수</figcaption></figure>
<figure><img src="${IMG}ws-newmap.jpg" alt="새 맵 만들기 모달" loading="lazy"><figcaption>새 맵 만들기 — 제목만 받고, 검증 기준을 미리 안내합니다</figcaption></figure>
</div>`)}

${blk('02','decide','설계 결정과 근거',tbl([['결정','32%'],['근거','']],[
 ['상한을 실측에서 도출<br><span class="data" style="color:var(--accent)">폴리곤 ≤8 · 정점 ≤20 · 기믹 ≤5</span>','공식 맵 6개의 실제 값은 폴리곤 2–3개, 정점 4–6개, 기믹 0–2개였습니다. 감으로 정하지 않고 실측치에 여유를 더해 상한을 잡았습니다.'],
 ['초기안 폐기','시뮬레이션 벽시계 타임아웃은 물리 엔진의 결정성 계약을 깨뜨려 같은 입력이 같은 결과를 내지 못하게 합니다. 리플레이 재현성이 무너지므로 버렸습니다.'],
 ['예약 ID 대역 채택','커스텀 맵을 별도 도메인으로 분리하는 안과 비교했을 때, 분리 쪽이 공식 게임 경로의 회귀 위험이 더 컸습니다.'],
 ['완료 기준을 원칙으로 정의','공식 게임의 동작을 바꾸지 않는다, 그 증거는 기존 테스트가 무수정으로 통과하는 것이다. 검증 가능한 문장으로 적어야 완료를 판정할 수 있습니다.'],
 ['포즈 좌표 상한 12','실게임은 관절 6개만 전송합니다. 실사용값에서 역산해 여유를 두었습니다.'],
 ['커스텀 맵은 1라운드','공식 맵처럼 3라운드를 강제하면 에디터에서 감당할 작업량이 과해집니다. 유저 부담을 기준으로 잘랐습니다.'],
 ['썸네일을 팔레트 그라디언트로','이미지 업로드를 받으면 저장소와 검수가 따라옵니다. 색 세 개만 고르게 해 스토리지 없이 카드가 구분되게 했습니다.']
],['st','q']))}

${blk('03','spec','명세 → 지시 → 구현',
`<p class="cap" style="margin-bottom:14px">같은 판단이 세 문서를 거쳐 화면이 되기까지의 대응입니다.</p>
<div class="tri">
  <div class="hd">명세 규칙</div><div class="hd">작업 지시</div><div class="hd">구현 결과</div>
  <div class="q">공개 전 제작자 본인이 한 번은 클리어해야 한다. 깰 수 없는 맵이 공개되면 다른 유저가 시간을 버린다.</div>
  <div>에디터에 검증 상태를 상시 노출하고, 미검증 상태에서는 공개 저장을 막되 비공개 저장은 허용할 것</div>
  <div>에디터 상단 <b>클리어 미검증</b> 배지와 안내 "공개 업로드하려면 테스트 플레이를 성공해야 합니다"</div>
  <div class="q">지형이 바뀌면 검증을 무효화한다. 포즈 변경은 무효화하지 않는다.</div>
  <div>지형 편집 이벤트에만 무효화를 연결할 것</div>
  <div>구현 중 <b>드래그 이동 경로에서 무효화가 누락</b>된 것을 발견해 보완</div>
  <div class="q">상한은 서버가 최종 검증한다. UI 검증은 편의 기능이다.</div>
  <div>한도 게이지를 실시간 표시하되, 서버 응답의 사유를 그대로 보여줄 것</div>
  <div>사이드바 <b>폴리곤 3/8 · 기믹 0/5 · 플레이어 4/4</b> 게이지와 저장 전 유효성 검사</div>
  <div class="q">에디터를 복제해 유저용을 만든다.</div>
  <div>관리자 에디터를 복사한 뒤 API 경로와 권한을 교체할 것</div>
  <div><b>지시와 다르게 구현.</b> 복제하면 버그 수정을 두 곳에 해야 하므로 한 컴포넌트에 분기 속성을 두는 방식으로 바꿨습니다</div>
  <div class="q">평점이 없을 때 0.0으로 표기하지 않는다.</div>
  <div>미집계 상태는 대시로 표시할 것</div>
  <div>0.0은 최저 평점으로 읽히므로 미집계와 구분. Phase 2 영역은 자리만 비워 두고 비활성 처리</div>
</div>
<div class="gal" style="margin-top:20px;grid-template-columns:1fr">
<figure><img src="${IMG}ws-editor.jpg" alt="맵 에디터 화면" loading="lazy" style="aspect-ratio:16/9">
<figcaption>맵 에디터 — 좌상단 <b>클리어 미검증</b> 배지, 우측 사이드바의 한도 게이지와 유효성 검사, 공개 업로드 조건 안내가 한 화면에 모여 있습니다</figcaption></figure>
</div>`)}

${blk('04','result','실사용 검증',
`<div class="metrics">
  <div class="metric"><div class="val">8P · 1G</div><div class="lb">상한을 채운 유저 맵</div><div class="src">폴리곤 8개 = 설정한 상한값</div></div>
  <div class="metric"><div class="val">4건 이상</div><div class="lb">공개된 유저 맵</div><div class="src">각 4–7회 플레이 · 2026.08.13 기준</div></div>
  <div class="metric"><div class="val">2건</div><div class="lb">본인 제작 맵</div><div class="src">공개 1 · 비공개 1</div></div>
</div>
<p style="margin-top:22px;color:var(--ink-2)">공식 맵 실측에서 상한을 8로 올려 잡았는데, 실제로 8개를 꽉 채워 만든 유저 맵이 공개되어 플레이되고 있습니다. <mark>실측으로 정한 수치가 실사용으로 검증된 것</mark>입니다.</p>
<p style="color:var(--ink-2)">가장 크게 남은 것은 무효화 조건의 누락을 스스로 발견한 일입니다. 명세를 쓸 때는 지형 편집만 생각했는데, 구현하면서 드래그로 옮기는 경로가 빠져 있다는 걸 알았습니다. 문서는 한 번 쓰고 끝나는 것이 아니라 구현이 되돌려주는 정보로 고쳐 쓰는 것이라는 걸 이 지점에서 확인했습니다.</p>`)}
<div class="artifacts"><a class="abtn" href="#/works/bodybuilder">${ico('work',16)}BodyBuilder로 돌아가기</a></div>`}

/* ===== ABOUT (전부 최신순) ===== */
const AWARDS=[
 ['2024.11','교내 학생 예비창업자 모의 IR DAY','플로라봇 — AI 반려 식물로봇','금상','발표자료 제작 · 사업 방향 보조','국립금오공과대학교 LINC 3.0 사업단'],
 ['2024.05','제15회 중소기업 바로알리기 IDEA 공모전','에세이 「내 길을 찾는 과정」','입선','단독 집필','중소기업중앙회'],
 ['2023.11','K7U-Belt 창업경진대회','SICK KICK — 소아청소년 케어 플랫폼','장려상','사업 방향·전략 전담 · 발표','국립한밭대학교'],
 ['2023.11','제4회 대한민국 신직업·미래직업 아이디어 공모전','콘텐츠 운영 컨설턴트 — 창직 아이디어','장려상','팀장 · 아이디어 제안 · 자료 조사','한국고용정보원'],
 ['2023.11','교내 창업동아리 시제품 제작 경진대회','솔라셀 킥보드 거치시설','창의 아이디어상','팀장 · 총무','국립금오공과대학교 창업원'],
 ['2023.06','교내 창업·발명 아이디어 경진대회','SICK KICK — 소아청소년 케어 플랫폼','대상','팀장 · 사업성 분석 전담','국립금오공과대학교 창업원'],
 ['2019.11','교내 창업·발명 아이디어 경진대회','다리 각도 조절 방석','은상','아이디어 구체화 · 사업성 분석','금오공과대학교 창업원'],
 ['2019.08','제18회 대한민국 청소년 발명 아이디어 경진대회','경추 교정 차량용 수면 베개','동상','구상 · 구현 · 자료 조사 전담','한국지식재산보호원']
];
const CERTS=[
 ['컴퓨터활용능력 2급','국가기술자격','대한상공회의소','2025.05'],
 ['데이터분석 준전문가 (ADsP)','국가공인 민간자격','한국데이터산업진흥원','2023.09'],
 ['FAT 1급','국가공인 민간자격','한국공인회계사회','2023.07'],
 ['정보처리기능사','국가기술자격','한국산업인력공단','2019.12']
];

const ABOUT_TABS=[
  {id:'skill',t:'역량'},{id:'edu',t:'학력 · 경력'},{id:'award',t:'수상 · 자격'},{id:'etc',t:'그 외 활동'}
];
function aboutTabs(cur){return `<div class="filters subtabs">${ABOUT_TABS.map(t=>
  `<a class="chip" href="#/about${t.id==='skill'?'':'/'+t.id}"${cur===t.id?' aria-current="page"':''}>${t.t}</a>`).join('')}</div>`}

/* 한눈에 보기 — 상세를 열지 않아도 판단이 서도록 위에 먼저 둡니다 */
function aboutSummary(){return `<div class="summary">
  <span class="eyebrow">한눈에 보기</span>
  <p class="body-l" style="margin:11px 0 20px">단순히 일회성에 그치지 않는, 시스템적으로 오래갈 수 있는 기획을 추구합니다.
    창업 경진대회와 아이디어 공모전에서 ${AWARDS.length}건을 수상했고, 제안한 기획 중 하나는 한국고용정보원의 직업카드뉴스로 발행되었습니다.</p>
  <dl class="sumgrid">
    <div><dt>전공</dt><dd>경영학 학사 · 국립금오공과대학교 <span class="cap">2025.08 졸업</span></dd></div>
    <div><dt>기획 경험 분야</dt><dd>게임 · IT서비스 · 사업</dd></div>
    <div><dt>수상</dt><dd>${AWARDS.length}건 <span class="cap">창업 · 아이디어 공모전</span></dd></div>
    <div><dt>자격</dt><dd>ADsP · FAT 1급 · 컴퓨터활용능력 2급 · 정보처리기능사</dd></div>
    <div><dt>연구</dt><dd>LNCS 특별호 논문 제2저자 <span class="cap">2024</span></dd></div>
    <div><dt>교육</dt><dd>삼성 청년 SW · AI 아카데미 <span class="cap">2026.01 – 12 · 진행 중</span></dd></div>
    <div><dt>경력</dt><dd>수입검사(IQC) 2년 — 검사 기준서 기반 판정 · 대책서 운영 <span class="cap">제조업 품질보증부 · 산업기능요원 소집해제</span></dd></div>
    <div><dt>연구실</dt><dd>마케팅컨설팅연구실 학부연구생 <span class="cap">2023.09 – 2025.02</span></dd></div>
  </dl>
</div>`}

function aboutProfile(){return `<section>
  <div class="profile">
    <img src="${IMG}profile.jpg" alt="김시후 프로필 사진">
    <div>
      <span class="eyebrow">About</span>
      <h1 class="d2" style="margin:10px 0 16px">김시후 · Kim Si Hoo</h1>
      <p class="body-l">오래가는 즐거움을 기획하는 기획자입니다.</p>
      <p style="margin-top:14px;color:var(--ink-2)"><mark>즐거움 · 편리함 · 지속가능성</mark>을 기준으로 게임과 서비스, 사업을 기획합니다. 사용자의 경험을 규칙과 문서로 구체화하고 구현까지 연결합니다.</p>
    </div>
  </div>
</section>`}
function aboutSkill(){return `<section class="sec">
  ${sechead('idea','역량','Competency')}
  ${[['game','게임 기획','규칙과 세계관을 함께 설계합니다. 표준을 쓸 곳과 직접 정할 곳을 나눕니다.',
     ['시스템·규칙 설계','밸런스 수치 설계','세계관·설정 구조화','UGC 품질 정책','레벨·콘텐츠 기획','플레이 흐름 설계']],
    ['service','서비스 기획','사용자의 행동을 먼저 정의하고, 예외까지 문서로 남깁니다.',
     ['요구사항 정의·명세 작성','화면 설계 · IA','진단·추천 로직 설계','예외 정책 정의','작업지시서 작성','범위 산정과 단계 분리']],
    ['biz','사업 기획','규제와 시장을 먼저 확인하고 그 결과를 설계에 반영합니다.',
     ['시장·경쟁사 분석','내외부환경 분석(PEST · VRIO 프레임워크)','수익 구조 설계','IR 자료 작성 및 발표','제도·인센티브 설계']]
  ].map(([k,t,l,items])=>`<div class="capgroup">
    <div class="hd">${ico(CAT[k].i,18)}<h4>${t}</h4></div>
    <div class="lead">${l}</div>
    <ul>${items.map(x=>`<li>${x}</li>`).join('')}</ul></div>`).join('')}

  <div class="sub">${ico('tool',16)}도구</div>
  ${tbl([['도구','180px'],['수준','70px'],['활용 범위','']],[
    ['PowerPoint','고급','공모전 발표자료와 IR 자료 제작. 도식·다이어그램 작성 포함'],
    ['Word · Excel · 한글','중급','기획 문서 작성, 데이터 정리, 수식을 활용한 집계'],
    ['Notion · Discord · SharePoint','중급','온라인 협업과 일정 관리, 문서 버전 관리'],
    ['ChatGPT(Codex) · Claude(ClaudeCode) · Gemini(Antigravity)','중급','기획 프로토타입 및 구현으로 사용, 문서 작성과 코드 리뷰 보조'],
    ['Figma','초급','와이어프레임 확인과 화면 설계 커뮤니케이션'],
    ['Photoshop · Illustrator','초급','아이디어 시각화와 발표자료용 그래픽 편집'],
    ['SPSS','기초','설문 데이터 기초 통계 분석']
  ],['st','m','q'])}

  <div class="sub">${ico('code',16)}기술 이해도</div>
  ${tbl([['영역','160px'],['수준','70px'],['내용','']],[
    ['Front-end','중급','Vue.js · React · TypeScript 컴포넌트 아키텍처, 상태 관리, 비동기 통신. 실제 서비스 화면 구현 경험'],
    ['Node.js · JavaScript','중급','웹 기반 로컬 대전 게임 구현'],
    ['Python','중급','기본 문법과 2차원 배열 제어 로직 작성. DFS·BFS·완전탐색·Greedy 등 탐색 알고리즘의 기본 이해'],
    ['데이터 분석','중급','pandas·numpy로 기초 분석 후 Matplotlib으로 시각화. 회귀분석과 통계적 방법론 학습'],
    ['Back-end','기초','Django 기반 MTV 구조 이해와 RESTful API 설계 실습'],
    ['머신러닝','기초','데이터 전처리와 회귀 분석 학습. 이미지 기반 질의응답(VQA) 모델 개발 프로세스를 데이터 가공부터 추론까지 경험']
  ],['st','m','q'])}
</section>`}
function aboutEdu(){return `<section class="sec">
  ${sechead('edu','교육사항','Education')}
  <div class="sub">${ico('edu',16)}학력</div>
  ${tbl([['기간','140px'],['학교','']],[
    ['2018.03 – 2025.08','<span class="st">국립금오공과대학교 경영학과</span> <span style="color:var(--ink-2)">학사</span><br><span class="cap">2023.09 – 2025.02 · 마케팅컨설팅연구실 학부연구생</span>']
  ],['m',''])}
  <div class="sub">${ico('idea',16)}연구 활동 (학부 연구생)</div>
  ${tbl([['기간','140px'],['구분','110px'],['내용','']],[
    ['2024.07 – 2024.12','논문','「기술수용모델의 용이성과 유용성이 생성형 AI 지속적 사용의도에 미치는 영향」제2저자<br><span class="cap">Lecture Notes in Computer Science 특별호 게재</span><br><span class="cap">DOI 번호 : 10.1007/978-3-031-75599-6_7</span>'],
    ['2024','창업 참여','AI·센서 기반 감성 교감 반려 식물로봇 「플로라봇」 / 아이디어 기획 및 구현, 사업 기획 보조<br><span class="cap">모의 IR 경진대회 금상 / 경북구미강소특구 우수창업자 기술사업화 지원사업 선정</span>']
  ],['m','st','q'])}
  <div class="sub">${ico('doc',16)}교육 이수</div>
  ${tbl([['기간','140px'],['과정','230px'],['내용','']],[
    ['2026.01 – 2026.12','삼성 청년 SW·AI 아카데미<br><span class="cap">삼성전자 · 멀티캠퍼스 · 대한상공회의소</span>','Python 문법과 알고리즘 학습, AI 데이터 분석·모델링 실습, Django·Vue.js 기반 풀스택 웹 개발'],
    ['2023.06 – 2023.10','Python 기반 사무행정 시티즌 빅데이터 사이언티스트(CBDS) 양성 과정<br><span class="cap">금오공과대학교 부설 평생교육원</span>','Python 데이터 수집·분석 훈련 및 시각화 실습, 회계 프로그램 실무. 과정 수료로 ADsP·FAT 1급 취득']
  ],['m','','q'])}
</section>
<section class="sec">
  ${sechead('work','경력','Experience')}
  ${tbl([['기간','140px'],['소속','170px'],['담당 업무','']],[
    ['2020.06 – 2022.07','수입검사(IQC) 담당<br><span class="cap">제조업 품질보증부 · 산업기능요원 소집해제</span>',
     '<b>수입검사(IQC) 업무 수행</b><br>· 수입 제품 입고 시 품목별 검사 기준서를 바탕으로 샘플링 검사와 전수 검사 시행<br>· 불량 제품 판정 후 대책서 및 개선 대책 요구<br>· 검사 결과 보고서 작성 보조']
  ],['m','','q'])}
</section>`}
function aboutAward(){return `<section class="sec">
  ${sechead('award','수상',`${AWARDS.length}건 · Awards`)}
  ${tbl([['일자','92px'],['대회','195px'],['출품 아이디어','185px'],['수상','108px'],['담당 역할','']],
    AWARDS.map(a=>[a[0],`${a[1]}<br><span class="cap">${a[5]}</span>`,a[2],
      `<span style="color:var(--accent);font-weight:600">${a[3]}</span>`,a[4]]),
    ['m','st','q','','q'])}
  <p class="cap" style="margin-top:10px">증빙 자료는 요청 시 제공합니다.</p>
</section>
<section class="sec">
  ${sechead('cert','자격','Certificates')}
  ${tbl([['자격명','250px'],['종류','150px'],['시행 기관','180px'],['취득','']],CERTS,['st','q','q','m'])}
</section>`}
function aboutEtc(){return `<section class="sec">
  ${sechead('etc','그 외 활동','Other')}
  ${tbl([['연도','118px'],['구분','108px'],['내용','']],[
    ['2024.09 –','기업 컨설팅','산학협력 기술지원 패키지 지원사업 참여 — 연구실 소속으로 경영 컨설팅 지도 참여'],
    ['2024','연구 용역','구미시 「청년근로자 코리빙 하우스 구축 기본계획 수립」 참여 — 데이터 정리 및 과제 코딩'],
    ['2019','특허 출원','3D 푸드 프린터의 분말·액상용 스크루 익스트루더<br><span class="cap">출원번호 10-2019-0017015</span>'],
    ['2019','게임 프로젝트','보드모아 — AR 기술 기반 보드게임 플랫폼, 팀장 및 가치 분석 <span class="cap">(자료 미보유)</span>'],
    ['2018.03 – 2025.02','동아리','교내 발명동아리 회원, 창업동아리 팀원 및 팀장']
  ],['m','st','q'])}
</section>`}

function viewAbout(){
  const tab=ABOUT_TABS.some(t=>t.id===state.tab)?state.tab:'skill';
  const panel=tab==='edu'?aboutEdu():tab==='award'?aboutAward():tab==='etc'?aboutEtc():aboutSkill();
  return aboutProfile()+aboutTabs(tab)+`<div id="about-panel" tabindex="-1">${panel}</div><details class="about-more"><summary>학력·경력 한눈에 보기</summary>${aboutSummary()}</details>`;
}

/* ===== CONTACT / 404 ===== */
function viewContact(){return `<section>
  ${sechead('mail','Contact','연락처',1)}
  <p class="body-l">프로젝트와 기획 경험에 대해 궁금한 점이 있다면 연락해 주세요.</p>
  <dl class="contact-list">
    <div><dt>이메일</dt><dd><a class="contact-email" href="mailto:kimshlife@naver.com">kimshlife@naver.com</a><button type="button" class="abtn" id="copymail" aria-live="polite">이메일 복사</button></dd></div>
    <div><dt>GitHub</dt><dd><a href="https://github.com/kimshlife" target="_blank" rel="noopener">github.com/kimshlife ↗</a></dd></div>
    <div><dt>이력서</dt><dd>${RESUME?`<a href="${RESUME}" target="_blank" rel="noopener">이력서 보기</a>`:'이메일로 요청해 주시면 전달드리겠습니다.'}</dd></div>
  </dl>
  <p class="cap" style="margin-top:16px">전화번호와 주소는 게시하지 않습니다. 이메일로 연락 주시면 회신드리겠습니다.</p>
</section>`}
function view404(){return `<section class="empty">
  <img src="assets/brand/mark-navy.svg" alt="" style="width:118px;margin:0 auto 24px;opacity:.28">
  <h1 class="d2" style="margin-bottom:10px">요청하신 문서를 찾을 수 없습니다.</h1>
  <p class="cap" style="margin-bottom:20px">주소가 바뀌었거나 삭제된 페이지입니다.</p>
  <a class="abtn" href="#/works">${ico('work',16)}Works로 이동</a></section>`}

/* ===== 렌더 ===== */
function render(){
  const s=$('stage'),n=$('notes');let h='',nt='';
  switch(state.view){
    case 'home':h=viewHome();syncNav('home');break;
    case 'about':h=viewAbout();syncNav('about');break;
    case 'works':h=viewWorks();syncNav('works');break;
    case 'detail':h=viewDetail();syncNav('works');
      nt=(P[state.slug]?.notes||[]).map(x=>`<div class="note"><b>${x.t}</b>${x.b}</div>`).join('');break;
    case 'workshop':h=viewWorkshop();syncNav('works');
      nt=`<div class="note"><b>소속</b>BodyBuilder의 기능입니다. 별도 프로젝트가 아닙니다.</div>
          <div class="note"><b>REMARK 03</b>지시와 다르게 구현한 행이 한 건 포함되어 있습니다.</div>
          <div class="note"><b>REMARK 04</b>상한 8을 채운 유저 맵이 수치 설계의 사후 검증입니다.</div>`;break;
    case 'contact':h=viewContact();syncNav('contact');break;
    default:h=view404();syncNav('');
  }
  s.innerHTML=h;n.innerHTML=nt;
  document.querySelector('.canvas').classList.toggle('has-notes',!!nt);
  document.querySelector('.canvas').classList.toggle('is-home',state.view==='home');
  s.querySelectorAll('.tri').forEach(grid=>{
    const cells=[...grid.children],labels=cells.slice(0,3).map(el=>el.textContent);
    grid.replaceChildren();
    for(let i=3;i<cells.length;i+=3){
      const row=document.createElement('div');row.className='tri-row';
      cells.slice(i,i+3).forEach((cell,j)=>{
        const label=document.createElement('strong');label.className='tri-label';label.textContent=labels[j];
        cell.prepend(label);row.append(cell);
      });grid.append(row);
    }
  });
  s.querySelectorAll('.gal img').forEach(img=>{
    if(img.closest('button'))return;
    const button=document.createElement('button');button.type='button';button.className='gallery-open';
    button.setAttribute('aria-label','이미지 확대: '+img.alt);img.replaceWith(button);button.append(img);
  });
  moveFocus(s);
}
/* 이 사이트는 주소만 바뀌고 페이지는 다시 불러오지 않습니다.
   포커스를 옮겨 주지 않으면 키보드·스크린리더 사용자는 화면이 바뀐 것을 알 수 없습니다. */
let firstRender=true;
function moveFocus(stage){
  if(firstRender){firstRender=false;return;}          // 첫 진입은 그대로 둔다
  const t=stage.querySelector('h1')||stage;
  t.setAttribute('tabindex','-1');
  t.focus({preventScroll:true});
}
let lightboxOpener=null;
function closeLightbox(){ $('lb').close(); }
$('lb').addEventListener('close',()=>{document.body.classList.remove('modal-open');lightboxOpener?.focus();});
document.addEventListener('click',async e=>{
  const c=e.target.closest('[data-cat]');
  if(c){const v=c.dataset.cat;
    if(v==='all')state.filter.clear();
    else state.filter.has(v)?state.filter.delete(v):state.filter.add(v);
    render();return;}
  const yt=e.target.closest('[data-yt]');
  if(yt){yt.outerHTML=ytFrame(yt.dataset.yt);return;}
  const opener=e.target.closest('.gallery-open');
  if(opener){const im=opener.querySelector('img');lightboxOpener=opener;$('lbi').src=im.src;$('lbi').alt=im.alt;$('lb').showModal();document.body.classList.add('modal-open');return;}
  if(e.target.id==='lb'||e.target.id==='lbx'){closeLightbox();return;}
  const cm=e.target.closest('#copymail');
  if(cm){try{await navigator.clipboard.writeText('kimshlife@naver.com');cm.innerHTML='복사했습니다';}
    catch{cm.innerHTML='복사할 수 없습니다. 이메일 주소를 선택해 주세요.';}
    setTimeout(()=>{cm.textContent='이메일 복사'},2500);}
});
route();

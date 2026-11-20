(() => {
  'use strict';
  const home = document.getElementById('home-page');
  const detail = document.getElementById('detail-page');
  const dialog = document.getElementById('image-dialog');
  const image = document.getElementById('expanded-image');
  const caption = document.getElementById('image-caption');
  const homeTitle = '김시후 — 기획 · 구현 포트폴리오';
  const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[char]));
  const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
  const routeFor = key => key === 'workshop' ? '#/works/bodybuilder/workshop' : `#/works/${key}`;
  const projectFor = key => own(JOURNAL, key) ? { ...(own(P, key) ? P[key] : {}), ...JOURNAL[key] } : null;
  const linkHTML = link => `<a class="button" href="${escape(/^(?:qa|assets|ssketch)\//.test(link.href) ? "/" + link.href : link.href)}"${link.href.startsWith('#') || link.href.startsWith('mailto:') ? '' : ' target="_blank" rel="noopener"'}>${escape(link.t)} <span aria-hidden="true">↗</span></a>`;

  function imageHTML(src, alt, { priority=false, sizes='(max-width:700px) calc(100vw - 40px), 680px', animated=false } = {}) {
    const asset = JOURNAL_IMAGES[src];
    if (!asset) return '';
    const widths = [Math.min(800,asset.width), Math.min(1600,asset.width)];
    const srcset = widths[0] === widths[1] ? `${asset.base}-800.webp ${widths[0]}w` : `${asset.base}-800.webp ${widths[0]}w, ${asset.base}-1600.webp ${widths[1]}w`;
    const picture = `<img src="${asset.base}-800.webp" srcset="${srcset}" sizes="${sizes}" width="${asset.width}" height="${asset.height}" alt="${escape(alt)}" ${priority ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async">`;
    return animated ? `<picture><source media="(prefers-reduced-motion: no-preference)" srcset="${asset.base}-animated.webp">${picture}</picture>` : picture;
  }

  function rolesHTML(project) {
    if (!project.roles) return '';
    const axes = ['기획','구현','운영'];
    const levels = {0:'없음',2:'분담',3:'주도'};
    const label = project.roles.map((level,i) => `${axes[i]} ${levels[level]}`).join(', ');
    return `<div class="role-spectrum" role="img" aria-label="${label}${project.ai ? ', 구현에 AI 도구 활용' : ''}">${project.roles.map((level,i) => `<span class="role-axis" aria-hidden="true"><span>${axes[i]}</span><span class="role-bars">${[1,2,3].map(n => `<i class="${n<=level ? 'filled' : ''}"></i>`).join('')}</span><span class="role-level">${levels[level]}</span></span>`).join('')}</div>${project.ai ? '<p class="ai-note">구현 · AI 도구 활용</p>' : ''}`;
  }
  const chipsHTML = project => project.chips ? `<ul class="stack-chips" aria-label="사용 기술">${project.chips.map(chip=>`<li>${escape(chip)}</li>`).join('')}</ul>` : '';
  document.getElementById('facts').innerHTML = JOURNAL_FACTS.map(fact=>`<a class="fact" href="${fact.href}"><strong>${escape(fact.v)}</strong><span>${escape(fact.l)}</span><small>${escape(fact.s)}</small></a>`).join('');
  document.getElementById('project-grid').innerHTML = JOURNAL_FEATURED.map(key=>{
    const p=projectFor(key);
    return `<article class="project-card" id="project-${key}"><a href="${routeFor(key)}"><div class="project-image">${imageHTML(p.cover,p.coverAlt,{sizes:'(max-width:700px) calc(100vw - 40px), 504px'})}${p.video ? '<span class="video-badge">▷ 데모 영상</span>' : '<span class="video-badge award-badge">SSAFY 우수상</span>'}</div><div class="project-caption"><h3 id="title-${key}">${escape(p.title)} <span aria-hidden="true">↗</span></h3><span class="project-date">${escape(p.period.replaceAll(' ',''))} · ${p.teamSize}</span></div><p class="project-description">${escape(p.subtitle)}</p>${rolesHTML(p)}${chipsHTML(p)}<p class="project-result">${escape(p.result)}</p></a></article>`;
  }).join('');
  document.querySelectorAll('.work-row').forEach(row=>{
    const key=row.id.replace('project-','');
    const p=projectFor(key);
    if (!p?.roles) return;
    row.querySelector('p').innerHTML=`<span class="earlier-role">기획 ${p.roles[0]===3 ? '주도' : '분담'}</span> · ${escape(p.result)}`;
  });

  document.getElementById('award-list').innerHTML = JOURNAL_AWARDS.map(([date,title,context]) => `<li><span>${escape(date)}</span><p>${escape(title)}<small>${escape(context)}</small></p></li>`).join('');
  document.getElementById('game-list').innerHTML = GAMES.map(([name,platform,stage]) => `<li>${escape(name)}<span>${escape(platform)} · ${escape(stage)}</span></li>`).join('');

  function storyHTML(story) {
    return `<section class="story"><h3>${escape(story.title)}</h3><p>${escape(story.body)}</p>${story.image ? figureHTML(story.image,story.caption) : ''}</section>`;
  }

  function figureHTML(src,label) {
    const asset=JOURNAL_IMAGES[src];
    return `<figure class="story-figure"><button class="image-button" type="button" data-image="${escape(asset ? `${asset.base}-1600.webp` : src)}" data-caption="${escape(label)}" aria-label="이미지 확대: ${escape(label)}">${imageHTML(src,label,{animated:src.endsWith('.gif')})}</button><figcaption>${escape(label)} · 클릭하면 확대</figcaption></figure>`;
  }

  function connectionHTML(connection) {
    return `<section class="connection"><h3>${escape(connection.title)}</h3><div class="connection-grid">${[['정한 것','plan'],['만든 것','build']].map(([label,side])=>`<div><p class="connection-label">${label}</p><p>${escape(connection[side])}</p>${connection[`${side}Image`] ? figureHTML(connection[`${side}Image`],connection[`${side}Caption`]) : `<div class="decision-note"><span>기획 기록 요약</span><strong>${escape(connection[`${side}Caption`])}</strong></div>`}</div>`).join('')}</div></section>`;
  }

  function renderProject(key) {
    const project = projectFor(key);
    if (!project) return false;
    const source = own(P, key) ? project : null;
    const notes = `<details class="extra-notes"><summary>전체 작업 메모 <span aria-hidden="true">＋</span></summary><div class="fold-content"><h3>제가 맡은 일</h3><ul>${project.tasks.map(item => `<li>${escape(item)}</li>`).join('')}</ul>${project.stories.map(storyHTML).join('')}${source ? `<h3>담당 범위</h3><ul>${source.scope.map(item => `<li>${escape(item)}</li>`).join('')}</ul>${source.decisions.map(item => `<h3>${escape(item.h)}</h3><p>${escape(item.b)}</p>`).join('')}${(source.notes || []).map(item => `<h3>${escape(item.t)}</h3><p>${escape(item.b)}</p>`).join('')}` : ''}</div></details>`;
    const links = (project.links || []).filter(link => link.href && !link.off);
    const index = JOURNAL_ORDER.indexOf(key);
    const nextKey = JOURNAL_ORDER[(index + 1) % JOURNAL_ORDER.length];
    const next = projectFor(nextKey);
    const backTarget = project.backTarget || (key === 'guild' ? 'about' : 'projects');
    const backLabel = backTarget === 'journey' ? '지나온 과정으로 돌아가기' : backTarget === 'about' ? '소개로 돌아가기' : '프로젝트 목록';
    const media = project.cover ? `<div class="detail-cover" id="demo">${project.video ? `<button class="video-poster" data-video="${escape(project.video)}" data-title="${escape(project.title)}" aria-label="${escape(project.title)} 데모 영상 불러오기">${imageHTML(project.cover,project.coverAlt,{priority:true})}<span class="play-label">▷ 데모 영상 보기<span>YouTube · 클릭 후 플레이어 로드</span></span></button>` : `<button class="image-button" data-image="${JOURNAL_IMAGES[project.cover].base}-1600.webp" data-caption="${escape(project.coverAlt)}" aria-label="${escape(project.coverAlt)} 확대">${imageHTML(project.cover,project.coverAlt,{priority:true})}</button>`}</div>` : `<div class="record-preview"><p class="eyebrow">활동 기록 · 공개 원본 이미지 없음</p><h2>${escape(project.result || project.subtitle)}</h2><ul>${project.tasks.slice(0,3).map(t=>`<li>${escape(t)}</li>`).join('')}</ul></div>`;
    const metrics=(project.metrics || []).slice(0,3);
    detail.innerHTML = `<a class="back-link" href="#${escape(backTarget)}">← ${escape(backLabel)}</a>
      <div class="detail-overview"><header class="detail-header"><p class="eyebrow">${escape(project.period)} · ${escape(project.team)}</p><h1>${escape(project.title)}</h1><p class="detail-subtitle">${escape(project.subtitle)}</p>${rolesHTML(project)}${project.roleScope ? `<p class="note">${escape(project.roleScope)}</p>` : ''}${chipsHTML(project)}<div class="detail-links">${project.video ? '<a class="button" href="#demo" data-load-video>데모 영상 ↓</a>' : ''}${links.map(linkHTML).join('')}</div></header>${media}</div>
      ${metrics.length ? `<div class="metric-grid" aria-label="프로젝트 결과와 설계 지표">${metrics.map(m=>`<div><strong>${escape(m.v)}</strong><span>${escape(m.l)}</span><small>${escape(m.s)}</small></div>`).join('')}</div>${project.metricNote ? `<p class="note metric-note">${escape(project.metricNote)}</p>` : ''}` : ''}
      <div class="detail-body"><div class="problem-goal"><section class="detail-section"><p class="eyebrow">01 · AS-IS</p><h2>문제</h2><p>${escape(project.problemSummary || project.problem?.[0] || project.intro)}</p></section><section class="detail-section"><p class="eyebrow">02 · TO-BE</p><h2>목표</h2><p>${escape(project.goal || project.intro)}</p></section></div>
      <section class="detail-section connections"><p class="eyebrow">03 · DECISIONS & BUILD</p><h2>정한 것 → 만든 것</h2>${project.connections ? project.connections.map(connectionHTML).join('') : project.stories.map(storyHTML).join('')}</section>
      <section class="detail-section reading-width"><p class="eyebrow">04 · RESULT</p><h2>결과와 한계</h2><p>${escape(project.outcome || project.result || project.stories.at(-1)?.body || project.intro)}</p>${!project.outcome && project.disclosure ? `<p>${escape(project.disclosure)}</p>` : ''}</section>
      <section class="detail-section contribution reading-width"><h2>기여 경계</h2><p>${escape(project.disclosure || '이 페이지에는 위 담당 범위의 작업을 기록했습니다. 수상과 프로젝트 결과는 팀 성과입니다.')}</p><ul>${project.tasks.map(task=>`<li>${escape(task)}</li>`).join('')}</ul></section>${notes}
      <nav class="detail-navigation" aria-label="다른 작업"><a href="#${escape(backTarget)}">← ${escape(backLabel)}</a>${key === 'workshop' ? '<a href="#/works/bodybuilder">BodyBuilder →</a>' : `<a href="${routeFor(nextKey)}">${escape(next.title)} →</a>`}</nav></div>`;
    document.title = `${project.title} | ${homeTitle}`;
    return true;
  }

  const aliases = {
    '#/':'#top', '#/works':'#projects', '#/about':'#about', '#/about/skill':'#about',
    '#/about/edu':'#journey', '#/about/award':'#recognition', '#/about/etc':'#qualifications',
    '#/contact':'#contact', '#/hobby':'#about', '#/hobby/game':'#about',
    '#/hobby/game/overview':'#about', '#/hobby/game/record':'#games', '#/hobby/game/docs':'#/works/guild',
    '#/planning':'#projects', '#/game':'#projects', '#/service':'#projects', '#/biz':'#earlier', '#/hr':'#journey',
    '#experience':'#journey', '#education':'#journey', '#research':'#research', '#tools':'#about', '#case-guild':'#/works/guild',
    '#award-ssketch':'#recognition', '#award-florabot':'#recognition', '#award-solarbeam':'#recognition', '#award-sickkick':'#recognition', '#award-contentops':'#recognition'
  };

  function focusHeading(container) {
    const heading = container.matches('h1,h2,h3') ? container : container.querySelector('h1,h2,h3');
    if (heading) { heading.setAttribute('tabindex','-1'); heading.focus({ preventScroll:true }); }
  }

  function renderRoute(initial = false) {
    const hash = location.hash;
    if (hash === '#main' && !detail.hidden) {
      focusHeading(detail);
      window.scrollTo({top:0,behavior:'instant'});
      return;
    }
    if (hash === '#demo' && !detail.hidden) {
      detail.querySelector('#demo')?.scrollIntoView({block:'center'});
      return;
    }
    if (own(aliases, hash) && aliases[hash] !== hash) {
      location.replace(aliases[hash]);
      return;
    }
    if (hash.startsWith('#/hobby/game/docs/')) {
      location.replace(hash.endsWith('/guild') ? '#/works/guild' : '/assets/docs/game-analysis.pdf');
      return;
    }
    if (dialog.open) dialog.close();
    const parts = hash.slice(2).split('/');
    const key = parts[0] === 'works' ? (parts[1] === 'bodybuilder' && parts[2] === 'workshop' ? 'workshop' : parts[1]) : null;
    const isProject = hash.startsWith('#/works/') && parts.length <= (key === 'workshop' ? 3 : 2) && renderProject(key);
    const invalidPath = !['/hidden/portfolio', '/hidden/portfolio/', '/hidden/portfolio/index.html'].includes(location.pathname);
    const invalidHash = hash.startsWith('#/') && !isProject;
    if (isProject || invalidPath || invalidHash) {
      home.hidden = true;
      detail.hidden = false;
      if (!isProject) {
        document.title = '페이지를 찾을 수 없습니다 — 김시후';
        detail.innerHTML = '<div class="not-found"><h1>기록을 찾을 수 없습니다.</h1><p>프로젝트 목록에서 다른 작업을 살펴볼 수 있습니다.</p><a class="inline-link" href="/hidden/portfolio/">처음으로 돌아가기 →</a></div>';
      }
      window.scrollTo({ top:0, behavior:'instant' });
      focusHeading(detail);
    } else {
      const wasDetail = !detail.hidden;
      home.hidden = false;
      detail.hidden = true;
      detail.replaceChildren(); // Stop any YouTube playback when returning home.
      document.title = homeTitle;
      const target = document.getElementById(hash.slice(1));
      if (target) {
        if (target.tagName === 'DETAILS') target.open = true;
        requestAnimationFrame(() => {
          target.scrollIntoView({ block:'start', behavior:'instant' });
          if (!initial || wasDetail) focusHeading(target);
        });
      } else if (!initial || wasDetail) {
        window.scrollTo({ top:0, behavior:'instant' });
        focusHeading(home);
      }
    }
  }

  detail.addEventListener('click', event => {
    const loadLink=event.target.closest('[data-load-video]');
    if (loadLink) {
      event.preventDefault();
      detail.querySelector('[data-video]')?.click();
      detail.querySelector('#demo')?.scrollIntoView({block:'center'});
      return;
    }
    const video=event.target.closest('[data-video]');
    if (video) {
      const player=document.createElement('iframe');
      player.src=`https://www.youtube-nocookie.com/embed/${encodeURIComponent(video.dataset.video)}?autoplay=0&rel=0`;
      player.title=`${video.dataset.title} 데모 영상`;
      player.allow='encrypted-media; picture-in-picture; fullscreen';
      player.allowFullscreen=true;
      player.referrerPolicy='strict-origin-when-cross-origin';
      video.replaceWith(player);
      player.focus();
      return;
    }
    const button = event.target.closest('[data-image]');
    if (!button) return;
    image.src = button.dataset.image;
    image.alt = button.dataset.caption;
    caption.textContent = button.dataset.caption;
    dialog.showModal();
    document.body.classList.add('image-open');
  });
  document.getElementById('close-image').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => document.body.classList.remove('image-open'));
  dialog.addEventListener('click', event => { if (event.target === dialog) { const bounds = dialog.getBoundingClientRect(); if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close(); } });
  window.addEventListener('hashchange', () => renderRoute());
  renderRoute(true);
})();

(() => {
  'use strict';
  const home = document.getElementById('home-page');
  const detail = document.getElementById('detail-page');
  const dialog = document.getElementById('image-dialog');
  const image = document.getElementById('expanded-image');
  const caption = document.getElementById('image-caption');
  const homeTitle = '김시후 — 해온 일과 만든 것들';
  const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[char]));
  const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
  const routeFor = key => key === 'workshop' ? '#/works/bodybuilder/workshop' : `#/works/${key}`;
  const projectFor = key => own(JOURNAL, key) ? { ...(own(P, key) ? P[key] : {}), ...JOURNAL[key] } : null;
  const linkHTML = link => `<a href="${escape(link.href)}"${link.href.startsWith('#') ? '' : ' target="_blank" rel="noopener"'}>${escape(link.t)} <span aria-hidden="true">↗</span></a>`;

  document.getElementById('award-list').innerHTML = JOURNAL_AWARDS.map(([date,title,context]) => `<li><span>${escape(date)}</span><p>${escape(title)}<small>${escape(context)}</small></p></li>`).join('');
  document.getElementById('game-list').innerHTML = GAMES.map(([name,platform,stage]) => `<li>${escape(name)}<span>${escape(platform)} · ${escape(stage)}</span></li>`).join('');

  function storyHTML(story) {
    return `<section class="story"><h2>${escape(story.title)}</h2><p>${escape(story.body)}</p>${story.image ? `<figure class="story-figure"><button class="image-button" type="button" data-image="${escape(story.image)}" data-caption="${escape(story.caption)}" aria-label="이미지 확대: ${escape(story.caption)}"><img src="${escape(story.image)}" alt="${escape(story.caption)}" loading="lazy"></button><figcaption>${escape(story.caption)} <span>클릭해서 크게 보기</span></figcaption></figure>` : ''}</section>`;
  }

  function renderProject(key) {
    const project = projectFor(key);
    if (!project) return false;
    const source = own(P, key) ? project : null;
    const notes = source ? `<details class="extra-notes"><summary>전체 작업 메모 <span aria-hidden="true">＋</span></summary><div class="fold-content"><h3>담당 범위</h3><ul>${source.scope.map(item => `<li>${escape(item)}</li>`).join('')}</ul>${source.decisions.map(item => `<h3>${escape(item.h)}</h3><p>${escape(item.b)}</p>`).join('')}${(source.notes || []).map(item => `<h3>${escape(item.t)}</h3><p>${escape(item.b)}</p>`).join('')}</div></details>` : '';
    const links = (project.links || []).filter(link => link.href && !link.off);
    const index = JOURNAL_ORDER.indexOf(key);
    const nextKey = JOURNAL_ORDER[(index + 1) % JOURNAL_ORDER.length];
    const next = projectFor(nextKey);
    const backTarget = project.backTarget || (key === 'guild' ? 'about' : 'projects');
    const backLabel = backTarget === 'journey' ? '지나온 과정으로 돌아가기' : backTarget === 'about' ? '소개로 돌아가기' : '프로젝트 목록';
    detail.innerHTML = `<a class="back-link" href="#${escape(backTarget)}">← ${escape(backLabel)}</a>
      <header class="detail-header"><p class="eyebrow">${escape(project.period)}</p><h1>${escape(project.title)}</h1><p class="detail-subtitle">${escape(project.subtitle)}</p><dl class="project-meta"><div><dt>참여</dt><dd>${escape(project.team)}</dd></div></dl></header>
      <div class="detail-body"><section class="detail-section"><h2>작업 소개</h2><p>${escape(project.intro)}</p></section><section class="detail-section"><h2>제가 맡은 일</h2><ul>${project.tasks.map(task => `<li>${escape(task)}</li>`).join('')}</ul>${project.disclosure ? `<p class="note">${escape(project.disclosure)}</p>` : ''}</section>
      ${project.cover ? `<figure class="detail-cover"><img src="${escape(project.cover)}" alt="${escape(project.coverAlt)}" fetchpriority="high"></figure>` : ''}
      ${project.stories.map(storyHTML).join('')}${notes}${links.length ? `<div class="detail-links">${links.map(linkHTML).join('')}</div>` : ''}
      <nav class="detail-navigation" aria-label="다른 작업"><a href="#${escape(backTarget)}">← ${escape(backLabel)}</a>${key === 'workshop' ? '<a href="#/works/bodybuilder">BodyBuilder →</a>' : `<a href="${routeFor(nextKey)}">${escape(next.title)} →</a>`}</nav></div>`;
    document.title = `${project.title} — 김시후`;
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
    if (own(aliases, hash) && aliases[hash] !== hash) {
      location.replace(aliases[hash]);
      return;
    }
    if (hash.startsWith('#/hobby/game/docs/')) {
      location.replace(hash.endsWith('/guild') ? '#/works/guild' : 'assets/docs/game-analysis.pdf');
      return;
    }
    if (dialog.open) dialog.close();
    const parts = hash.slice(2).split('/');
    const key = parts[0] === 'works' ? (parts[1] === 'bodybuilder' && parts[2] === 'workshop' ? 'workshop' : parts[1]) : null;
    const isProject = hash.startsWith('#/works/') && parts.length <= (key === 'workshop' ? 3 : 2) && renderProject(key);
    const invalidPath = !['/','/index.html','/404.html'].includes(location.pathname);
    const invalidHash = hash.startsWith('#/') && !isProject;
    if (isProject || invalidPath || invalidHash) {
      home.hidden = true;
      detail.hidden = false;
      if (!isProject) {
        document.title = '페이지를 찾을 수 없습니다 — 김시후';
        detail.innerHTML = '<div class="not-found"><h1>기록을 찾을 수 없습니다.</h1><p>프로젝트 목록에서 다른 작업을 살펴볼 수 있습니다.</p><a class="inline-link" href="/">처음으로 돌아가기 →</a></div>';
      }
      window.scrollTo({ top:0, behavior:'instant' });
      focusHeading(detail);
    } else {
      const wasDetail = !detail.hidden;
      home.hidden = false;
      detail.hidden = true;
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

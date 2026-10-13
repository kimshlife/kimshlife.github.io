(() => {
  'use strict';

  // Icons share one stroke style; company and product logos use separate assets.
  const paths = {
    policy: 'M6 3h9l4 4v14H6zM15 3v5h4M9 12h7M9 16h5',
    workflow: 'M3 4h6v6H3zM15 14h6v6h-6zM6 10v7h9M9 7h9v7',
    verify: 'M9 3h6v3H9zM9 5H5v16h14V5h-4M8 13l3 3 5-6',
    document: 'M6 3h9l4 4v14H6zM15 3v5h4M9 12h7M9 16h5',
    check: 'M5 12l4 4L19 6',
    expand: 'M8 3H3v5M16 3h5v5M3 16v5h5M21 16v5h-5',
    edit: 'M14 5l5 5M4 20l5-1L21 7a2.1 2.1 0 0 0-4-4L5 15l-1 5ZM13 20h8',
    play: 'M9 6l10 6-10 6V6ZM12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20',
    publish: 'M12 16V3M7 8l5-5 5 5M4 14v6h16v-6',
    plant: 'M12 21V11M12 15C4 15 3 10 3 6c5 0 9 3 9 9ZM12 11c0-6 4-8 9-8 0 5-3 8-9 8',
    sun: 'M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10ZM12 1v2M12 21v2M1 12h2M21 12h2M4 4l2 2M18 18l2 2M4 20l2-2M18 6l2-2',
    code: 'M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16',
    graduate: 'M12 3L2 8l10 5 10-5-10-5ZM6 10v7c4 3 8 3 12 0v-7M22 8v8',
    chart: 'M4 3v18h17M8 15l4-5 4 3 5-8',
    research: 'M6 3h12v18H6zM9 7h6M9 11h6M9 15h4',
    people: 'M8 3a3 3 0 1 0 0 6 3 3 0 0 0 0-6ZM3 20v-4a5 5 0 0 1 10 0v4M16 3a3 3 0 0 1 0 6M17 11a5 5 0 0 1 4 5v4',
    idea: 'M9 18h6M10 21h4M8 14a6 6 0 1 1 8 0v2H8v-2',
    game: 'M8 7h8a4 4 0 0 1 4 3l2 7a3 3 0 0 1-5 3l-3-3h-4l-3 3a3 3 0 0 1-5-3l2-7a4 4 0 0 1 4-3ZM6 12h5M8.5 9.5v5M16 11h.01M18 14h.01',
    award: 'M8 3h8v6a4 4 0 0 1-8 0V3ZM8 4H4v3a4 4 0 0 0 4 4M16 4h4v3a4 4 0 0 1-4 4M12 13v7M8 21h8',
    certificate: 'M5 3h14v13H5zM8 7h8M8 10h5M9 16v6l3-2 3 2v-6',
    spark: 'M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3 3-7Z',
    print: 'M7 8V3h10v5M7 17H3V8h18v9h-4M7 14h10v7H7zM17 11h.01',
    close: 'M6 6l12 12M18 6L6 18'
  };
  const renderIcons = root => root.querySelectorAll('[data-icon]').forEach(element => {
    const path = paths[element.dataset.icon];
    if (!path) return;
    element.innerHTML = `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="${path}"></path></svg>`;
  });
  renderIcons(document);

  const progress = document.querySelector('.reading-progress span');
  const links = [...document.querySelectorAll('.site-header nav a')];
  const sections = links.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
  const updateNavigation = () => {
    const readingLine = document.querySelector('.site-header').getBoundingClientRect().height + 70;
    let active = null;
    sections.forEach(section => {
      const bounds = section.getBoundingClientRect();
      if (bounds.top <= readingLine && bounds.bottom > readingLine) active = section.id;
    });
    links.forEach(link => {
      if (link.getAttribute('href') === `#${active}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };
  let scheduled = false;
  const updateProgress = () => {
    const available = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = `${available > 0 ? Math.min(100, Math.max(0, window.scrollY / available * 100)) : 0}%`;
    updateNavigation();
    scheduled = false;
  };
  window.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; window.requestAnimationFrame(updateProgress); }
  }, { passive: true });
  window.addEventListener('resize', updateProgress);
  window.addEventListener('load', updateProgress);
  document.addEventListener('toggle', updateProgress, true);
  updateProgress();

  const dialog = document.getElementById('image-dialog');
  const dialogImage = document.getElementById('dialog-image');
  const caption = document.getElementById('image-dialog-caption');
  const projectDialog = document.getElementById('project-dialog');
  const projectTitle = document.getElementById('project-dialog-title');
  const projectBody = document.getElementById('project-dialog-body');
  const savedOverflow = document.body.style.overflow;
  const syncScrollLock = () => {
    document.body.style.overflow = dialog.open || projectDialog.open ? 'hidden' : savedOverflow;
  };
  const escape = value => String(value ?? '').replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]));
  const additionalProjects = {
    florabot: {
      title: '플로라봇', period: '2024', team: '연구실 창업 프로젝트',
      what: 'AI·센서 기반 감성 교감 반려 식물로봇',
      scope: ['아이디어 구체화 및 구현 참여', '시장 분석·BM 설정 보조', '발표자료 제작·사업 방향 보조'],
      metrics: [{ v: '금상', l: '교내 모의 IR DAY', s: '2024.12' }, { v: '선정', l: '기술사업화 지원사업', s: '경북구미강소특구 우수창업자 지원사업' }]
    },
    solarbeam: {
      title: 'SolarBeam', period: '2023.06 – 2024.02', team: '교내 창업동아리 · 팀장·총무',
      what: '태양광 킥보드 거치소 시제품 프로젝트',
      scope: ['선행 특허·제품 조사', '팀원 역할 배분 및 일정 점검', '지원금·영수증·보고서 관리'],
      metrics: [{ v: '창의 아이디어상', l: '창업동아리 시제품 제작 경진대회', s: '2023.12' }]
    }
  };
  const attachImageActions = root => root.querySelectorAll('[data-zoom]').forEach(button => {
    button.addEventListener('click', () => {
      dialogImage.src = button.dataset.zoom;
      dialogImage.alt = button.querySelector('img').alt;
      caption.textContent = button.dataset.caption;
      dialog.showModal();
      syncScrollLock();
    });
  });
  const openProject = key => {
    const project = P[key] || additionalProjects[key];
    if (!project) return;
    projectTitle.textContent = project.title;
    const template = document.getElementById(`detail-${key}`);
    const metadata = `<p class="detail-intro">${escape(project.what)}</p><dl class="detail-meta"><div><dt>기간</dt><dd>${escape(project.period)}</dd></div><div><dt>참여</dt><dd>${escape(project.team)}</dd></div>${project.stack ? `<div><dt>사용 기술</dt><dd>${escape(project.stack)}</dd></div>` : ''}</dl>`;
    const scope = `<section class="detail-section"><h3>담당 업무</h3><ul>${project.scope.map(item => `<li>${escape(item)}</li>`).join('')}</ul></section>`;
    const metrics = `<section class="detail-section"><h3>산출물·결과</h3><div class="detail-metrics">${(project.metrics || []).map(metric => `<div><strong>${escape(metric.v)}</strong><p>${escape(metric.l)}</p><small>${escape(metric.s)}</small></div>`).join('')}</div></section>`;
    const decisions = project.decisions ? `<section class="detail-section"><h3>설계·진행 기록</h3>${project.decisions.map(item => `<div class="detail-decision"><h4>${escape(item.h)}</h4><p>${escape(item.b)}</p></div>`).join('')}</section>` : '';
    const gallery = project.gallery?.length ? `<section class="detail-section"><h3>작업 자료</h3><div class="detail-gallery">${project.gallery.slice(0, 3).map(item => `<figure><button class="zoom-image" type="button" data-zoom="../assets/img/${escape(item.f)}.${escape(item.e || 'jpg')}" data-caption="${escape(item.c)}"><img src="../assets/img/${escape(item.f)}.${escape(item.e || 'jpg')}" alt="${escape(item.c)}" loading="lazy"><span class="zoom-hint">원본 확대 ↗</span></button><figcaption>${escape(item.c)}</figcaption></figure>`).join('')}</div></section>` : '';
    const record = P[key] ? `<a class="detail-record text-link" href="../#/works/${escape(key)}" target="_blank" rel="noopener">전체 프로젝트 기록 ↗</a>` : '';
    projectBody.innerHTML = metadata + (template ? template.innerHTML : scope + metrics + decisions + gallery) + record;
    renderIcons(projectBody);
    attachImageActions(projectBody);
    projectDialog.showModal();
    projectBody.scrollTop = 0;
    syncScrollLock();
  };
  document.querySelectorAll('.project-trigger').forEach(button => {
    button.addEventListener('click', () => openProject(button.dataset.project));
    button.closest('.project-row').addEventListener('click', event => {
      if (!event.target.closest('button, a') && !window.getSelection().toString()) {
        button.focus({ preventScroll: true });
        openProject(button.dataset.project);
      }
    });
  });
  document.getElementById('close-project').addEventListener('click', () => projectDialog.close());
  projectDialog.addEventListener('click', event => {
    const bounds = projectDialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) projectDialog.close();
  });
  projectDialog.addEventListener('close', syncScrollLock);
  const closeDialog = () => dialog.close();
  attachImageActions(document);
  document.getElementById('close-dialog').addEventListener('click', closeDialog);
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) closeDialog();
  });
  dialog.addEventListener('close', syncScrollLock);
  document.getElementById('print-page').addEventListener('click', () => window.print());
})();

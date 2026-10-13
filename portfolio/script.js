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
  document.querySelectorAll('[data-icon]').forEach(element => {
    const path = paths[element.dataset.icon];
    if (!path) return;
    element.innerHTML = `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="${path}"></path></svg>`;
  });

  const progress = document.querySelector('.reading-progress span');
  const links = [...document.querySelectorAll('.site-header nav a')];
  const sections = links.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
  const updateNavigation = () => {
    const readingLine = document.querySelector('.site-header').getBoundingClientRect().height + 70;
    let active = null;
    sections.forEach(section => {
      const region = section.closest('.background-grid') || section;
      const bounds = region.getBoundingClientRect();
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
  let previousOverflow = '';
  const closeDialog = () => dialog.close();
  document.querySelectorAll('[data-zoom]').forEach(button => {
    button.addEventListener('click', () => {
      dialogImage.src = button.dataset.zoom;
      dialogImage.alt = button.querySelector('img').alt;
      caption.textContent = button.dataset.caption;
      previousOverflow = document.body.style.overflow;
      dialog.showModal();
      document.body.style.overflow = 'hidden';
    });
  });
  document.getElementById('close-dialog').addEventListener('click', closeDialog);
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) closeDialog();
  });
  dialog.addEventListener('close', () => { document.body.style.overflow = previousOverflow; });
  document.getElementById('print-page').addEventListener('click', () => window.print());
})();

/* 이전 직군별 주소를 새 기록으로 연결합니다. /portfolio/는 별도로 유지합니다. */
(() => {
  'use strict';
  const root = new URL('../', location.href);
  const anchor = location.hash.slice(1);
  const projectAnchors = { ssketch:'ssketch', bodybuilder:'bodybuilder', projectrg:'projectrg', neontetris:'neontetris', reference:'ssketch', counterside:'guild', 'case-guild':'guild', workshop:'bodybuilder/workshop' };
  const sectionAnchors = { top:'top', main:'top', about:'top', experience:'journey', education:'journey', research:'research', recognition:'recognition', tools:'about', contact:'contact', cases:'projects', analysis:'projects', method:'projects', more:'earlier', projects:'projects' };
  if (anchor.startsWith('/')) root.hash = anchor;
  else if (Object.prototype.hasOwnProperty.call(projectAnchors, anchor)) root.hash = `/works/${projectAnchors[anchor]}`;
  else if (anchor.startsWith('project-')) root.hash = `/works/${anchor.slice(8)}`;
  else if (anchor.startsWith('award-')) root.hash = 'recognition';
  else root.hash = sectionAnchors[anchor] || 'top';
  location.replace(root.href);
})();

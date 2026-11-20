/* 정적 데모 전용 — 원본 저장소에는 없는 파일입니다.
   GitHub Pages 에는 socket.io 서버가 없어서 네트워크 대전 로비에 들어가면 아무 응답도 오지 않습니다.
   그래서 NETWORK MULTIPLAYER 버튼의 클릭(마우스·키보드 메뉴 모두)을 tetris.js 에 닿기 전에 막고,
   시작 화면의 안내문을 잠깐 또렷하게 보여 줍니다. */
(() => {
  'use strict';
  const note = document.getElementById('static-demo-note');
  let timer = 0;
  document.addEventListener('click', event => {
    const target = event.target instanceof Element ? event.target.closest('#btn-network') : null;
    if (!target) return;
    event.stopPropagation();
    event.preventDefault();
    if (!note) return;
    note.style.opacity = '1';
    clearTimeout(timer);
    timer = setTimeout(() => { note.style.opacity = '0.75'; }, 1800);
  }, true);
})();

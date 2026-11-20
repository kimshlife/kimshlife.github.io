# Neon Tetris Wars — 웹 데모

포트폴리오 사이트 안에서 바로 실행해 볼 수 있게 올린 정적 사본입니다.

- 원본: https://github.com/kimshlife/NeonTetrisWars (커밋 `7d1c631`, 2026-08-14)
- 라이선스: GNU GPL v3 — 같은 폴더의 `LICENSE`
- 동작하는 것: 싱글 플레이, 로컬 대전, 설정, 업데이트 로그
- 동작하지 않는 것: 네트워크 대전 (Node.js + socket.io 서버 필요)

## 원본에서 바꾼 것 (2026-11-17)

`style.css`, `tetris.js`, `PATCH_NOTES.html`, `LICENSE` 는 원본 그대로입니다.

`index.html` 만 아래 네 곳을 고쳤습니다.

1. `<title>` 을 「Neon Tetris Wars — 웹 데모」로 바꾸고 설명문과 검색 차단 메타 태그를 추가
2. `/socket.io/socket.io.js` 스크립트 태그를 제거 (`tetris.js` 는 `io` 가 없으면 네트워크 초기화를 건너뜀)
3. NETWORK MULTIPLAYER 버튼 글자에 「서버 필요」를 덧붙이고, 시작 화면 왼쪽 아래에 안내문과 링크 추가
4. `static-demo.js` 를 추가로 불러옴 — 네트워크 버튼 클릭을 막는 새 파일

## 원본이 바뀌면

원본 저장소에서 `style.css`, `tetris.js`, `PATCH_NOTES.html` 을 그대로 덮어쓰고, `index.html` 은 위 네 곳을 다시 적용합니다.

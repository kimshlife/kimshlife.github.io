/*
  SSketch 배포 홈페이지 — 보관본 설정
  --------------------------------------------------------------
  원래 배포 주소(ssketch.ddns.net)가 내려간 뒤에도 홈페이지를 볼 수 있게
  kimshlife.github.io/ssketch/ 에 옮겨 둔 사본입니다.

  downloadUrl:
    - 테스트 배포가 끝나 비워 두었습니다. 비어 있으면 다운로드 버튼이
      비활성으로 바뀌고, 누르면 "다운로드를 제공하지 않습니다" 안내가 뜹니다.

  screenshots:
    - 캡션/alt만 바꾸고 싶다면 아래 배열만 수정하기
*/
window.SSKETCH_CONFIG = {
  trailerYoutubeUrl: "",
  downloadUrl: "",
  downloadLabel: "배포 종료",
  screenshots: [
    {
      src: "assets/screenshots/gameplay-drawing.jpg",
      alt: "SSketch 인게임 이젤에서 팔레트와 붓을 사용해 직접 그림을 그리는 화면",
      caption: "DRAW · 이젤에서 직접 그림 그리기"
    },
    {
      src: "assets/screenshots/gameplay-rocket-use.jpg",
      alt: "SSketch 밤 페이즈에서 로켓런처를 발사하고 쿨다운이 적용된 실제 인게임 화면",
      caption: "ITEM · 로켓런처 발사와 쿨다운"
    },
    {
      src: "assets/screenshots/gameplay-night-theft.jpg",
      alt: "밤이 된 마을에서 다른 플레이어의 그림을 훔치고 지키는 SSketch 인게임 화면",
      caption: "STEAL · 밤의 그림 도둑질"
    },
    {
      src: "assets/screenshots/gameplay-morning-review.jpg",
      alt: "아침 페이즈에서 익명으로 작품에 점수와 한 줄 평을 남기는 SSketch 인게임 화면",
      caption: "RATE · 작품 평가와 한 줄 평"
    }
  ]
};

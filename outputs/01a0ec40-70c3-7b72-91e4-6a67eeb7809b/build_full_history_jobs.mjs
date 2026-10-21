import fs from 'node:fs/promises';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const outDir = new URL('.', import.meta.url).pathname.replace(/^\/(?=[A-Za-z]:)/, '');
const file = `${outDir}full_history_job_recommendations_2026-09-30.xlsx`;
const wb = Workbook.create();
const sh = wb.worksheets.add('종합 추천 공고');
sh.showGridLines = false;
sh.tabColor = '#183153';

const d = (s) => s ? new Date(`${s}T12:00:00Z`) : null;
const jobs = [
  [1,'품질·제조','에이치케이씨아이디에스','품질경영부 수입검사','경기 시흥','정규직','신입·초대졸 이상',d('2026-10-11'),'A','테크노전자 IQC 2년 2개월','샘플링·전수검사, 불량 판정, 검사 기록과 대책서 요청이 공고 업무와 직접 일치','계측기 종류와 도면 기호 해독 수준은 이력서에 구체적으로 없음','실제 검사 품목·사용 장비·불량 처리 사례를 수치와 함께 정리','https://m.saramin.co.kr/job-search/view?rec_idx=55011140','직접 경력 활용 1순위'],
  [2,'시장조사·사업기획','미엔느','AI 기반 시장조사·데이터분석·사업기획','경기 광주','계약직','신입 포함·초대졸 이상',d('2026-10-21'),'A','경영학·AI 논문·ADsP·창업/IR 수상·CBDS','자료 분류와 사실 검증, 사업 기회 도출, 보고서와 PPT 작성 요구에 이력 전반이 맞음','14명 규모의 제조업 회사이며 계약직. 상업 서비스 매출 성과는 없음','플로라봇 시장·BM 분석과 논문 조사 설계, 특허·경쟁제품 조사','https://m.saramin.co.kr/job-search/view?rec_idx=55088827','연봉 4,000만원 공고'],
  [3,'공공 리서치','리서치랩','공공부문 리서치 연구원','서울 강남','정규직·수습 3개월','신입 포함·학사 이상',d('2026-10-15'),'A','경영학·AI 수용 연구 제2저자·ADsP·SPSS·PPT','조사 설계·자료 분석·보고서 역량을 학부 연구와 지역 연구용역 참여로 입증 가능','공공조사 수주·현장조사 관리 실무는 없음. 엑셀 고급 능력 우대','AI 지속사용 의도 연구의 본인 기여와 구미시 연구용역 자료 정리','https://m.saramin.co.kr/job-search/view?rec_idx=55040188','자기소개서에 참여 프로젝트 소개 요구'],
  [4,'제조·교육사업','스마트제조혁신협회','교육사업 기획·운영관리','서울 서초','2년 계약·정규직 전환 가능','경력무관·초대졸 이상',d('2026-09-30'),'A','제조 품질 경력·SSAFY·창업동아리 예산/증빙·운전면허','제조 현장 이해와 AI 교육 경험, 일정·서류·지원금 관리를 함께 설명 가능','정부 교육사업 위탁운영 실무 없음. 오늘 23:59 마감','SolarBeam 예산·영수증·보고서 및 SSAFY 교육과 협업 사례','https://www.jobkorea.co.kr/Recruit/GI_Read/50010166','오늘 마감. 2명 채용'],
  [5,'AI·교육 PM','휴마인','기업·기관 AI 데이터교육 프로젝트 매니저','서울 강남','정규직·수습 3개월','신입 포함·학사 이상',d('2026-10-14'),'A','SSAFY AI/웹 교육·CBDS·팀장·문서화','교육 내용을 이해하면서 프로젝트 일정·담당·전달물을 관리한 경험을 연결 가능','유료 기업교육 운영·강사 조율 실무는 확인되지 않음','SSketch 요구사항 250건과 SolarBeam 역할·진척 관리','https://m.saramin.co.kr/job-search/view?rec_idx=55033127','상세 업무 범위는 지원 전 확인'],
  [6,'공공 연구행정','한국국방연구원','연구행정 위촉원 라','서울 동대문','1년 위촉·평가 후 1년 연장 가능','전공 무관·업무능력 보유',d('2026-10-06'),'A','학부 연구생·연구용역·총무/증빙·FAT 1급','연구 맥락을 이해하고 문서·비용·일정을 관리한 근거가 있음','월 239만원 수준, 위촉직 1명 모집. 공공 연구행정 실무 경력은 없음','논문 공동저자 역할과 동아리 예산·정산·보고서 작업','https://jlab.incruit.com/jobs/2609180001838','공고문상 10/6 09:00 마감'],
  [7,'소프트웨어 QA','인피닉','마곡 SW 테스트 엔지니어','서울 강서','정규직','신입·경력, 학력무관',d('2026-10-15'),'A','IQC·SSketch 버그 재현·1종 보통면허·컴활','물리 품질검사와 소프트웨어 재현·기록 경험이 함께 있고 운전·출장 가능 우대에 부합','ISTQB/CSTS 자격 없음. 잡코리아는 접수 중이나 사람인의 유사 공고는 마감으로 표시','실제 빌드에서만 난 버그 3건의 재현·원인·수정 확인','https://www.jobkorea.co.kr/Recruit/GI_Read/49997820','잡코리아 해당 공고 접수 상태 확인'],
  [8,'전자부품 품질','아하','IQC/OQC 품질 담당','경기 김포','정규직·수습 3개월','경력무관',null,'A','테크노전자 IQC 2년 2개월','같은 수입검사 업무를 바로 활용할 수 있는 전자부품 제조사','출고검사(OQC) 범위는 별도 학습 필요','검사 기준서, 불량 판정, 개선 대책 요청 경험','https://m.saramin.co.kr/job-search/view?rec_idx=55040899','상시채용·조기 종료 가능'],
  [9,'반도체 장비 품질','저스템','품질보증팀 수입검사','경기 용인','정규직/아르바이트 병기','경력무관·초대졸 이상',d('2026-10-08'),'B','IQC·품질 보고서·1종 보통면허','반도체 장비 업체의 수입검사와 기존 직무가 맞고 운전면허 우대도 충족','공고에 정규직과 아르바이트가 함께 표기돼 적용 형태 확인 필요. 장비·도면 영역 차이','검사결과 데이터와 불량 대응 문서 작성 경험','https://m.saramin.co.kr/job-search/view?rec_idx=54978936','고용형태 확인'],
  [10,'모빌리티 PM','트리즈','자율주행·모빌리티 프로젝트 매니저','경기 화성','정규직·수습 3개월','신입 또는 1년 이하',d('2026-11-13'),'B','제조 현장·팀장·SSAFY 개발 협업·운전면허','현장 품질, 기술팀 협업, 문서·일정 관리가 한 직무에 모임','자동차/자율주행 기술 및 도면 해독 경험 부족','IQC 업무와 SSketch 250건 요구사항·담당자 인계 문서','https://m.saramin.co.kr/job-search/view?rec_idx=55026261','공학 전공은 우대, 필수 아님'],
  [11,'게임 서비스','게임덱스','게임 운영 담당자','경기 성남','계약직','신입·학력무관',null,'B','6년 길드 운영·게임 분석·SSAFY 게임 제작','정책·공지·제재 기준과 이탈 대응 사례가 운영 직무에 구체적으로 연결됨','길드 운영은 취미 활동이며 상용 게임 운영 경력은 아님. 계약직','규칙 공개, 합병 협의, 인원 이탈 대응의 근거 문서','https://m.saramin.co.kr/job-search/view?rec_idx=54974325','채용 시 마감'],
  [12,'소프트웨어 QA','컴즈','S/W QA & Test Engineer','서울 구로','정규직/프리랜서 병기','신입 가능·초대졸 이상',d('2026-10-02'),'B','IQC·SSketch 실제 빌드 버그 추적','품질 기준에 따른 검사와 소프트웨어 테스트의 연결이 분명함','기술면접, 공학 전공 및 ISTQB/CSTS 우대. 고용형태 확인 필요','버그 재현 조건·원인·검증을 문서화한 사례','https://m.saramin.co.kr/job-search/view?rec_idx=54907136','10/2 마감'],
  [13,'제조 부품 품질','와이엠','품질관리팀 수입검사','경기 평택','정규직','신입·경력 7년 이하·학사 이상',d('2026-10-22'),'B','IQC 2년 2개월·경영학 학사','수입검사 경력을 직접 인정받을 수 있고 학력·연차 범위에도 부합','볼트·너트 소재/계측 업무 경험은 별도 확인 필요','품목별 검사 기준과 불량 개선 요청 사례','https://m.saramin.co.kr/job-search/view?rec_idx=55100736','직무 상세 업무는 지원 전 확인'],
  [14,'제조 지원사업','스마트제조혁신협회','경영지원·정부지원사업관리','서울 서초','2년 계약','경력무관',d('2026-10-29'),'B','제조 경력·사업기획 공모전·예산/증빙·FAT 1급','제조업과 정부사업 문서·총무 업무의 접점이 많음','사업비 정산 시스템 및 정부과제 실무 경험 없음. 계약 기간 2년','SolarBeam 지원금·영수증·보고서, 창업사업 선정 경험','https://www.jobkorea.co.kr/Recruit/GI_Read/50067264','동일 기관의 별도 공고'],
  [15,'공공 교육관리','한국소방산업기술원','교육관리 기간제','충북 음성','휴직대체 계약직','신입·전공/학력 제한 없음',d('2026-10-06'),'B','교육 봉사·SSAFY·프로젝트 일정 관리','교육생·일정·자료 관리와 문서화 경험을 활용 가능','기간제 대체인력. 소방산업 교육 실무는 없음','발명캠프 교육 봉사와 프로젝트 운영 문서','https://www.korea.kr/archive/recruitInfoView.do?dataId=394998','10/6 17:00 마감'],
  [16,'디지털헬스 연구지원','파이디지털헬스케어','정부과제 연구행정','서울 서대문','정규직/계약직 병기','신입·경력 1~5년, 초대졸 이상',d('2026-10-16'),'B','학부 연구·AI 헬스 시제품·FAT 1급·사업 서류','헬스케어 연구 맥락과 연구·회계 문서를 모두 접한 이력','정부과제 집행·정산 실무 없음. 고용형태와 신입 허용 범위 확인','플로라봇 사업화 지원사업 선정 과정과 동아리 증빙 관리','https://m.saramin.co.kr/job-search/view?rec_idx=55036501','지원요건 확인 후 지원'],
];

const headers=['추천순위','분야','회사','공고·직무','지역','고용형태','지원요건','마감일','판단','근거 이력','강점','리스크','지원서 핵심 사례','공고 URL','확인 메모'];
sh.getRange('A2').values=[['전체 이력 기준 추천 채용 공고']];
sh.getRange('A3').values=[['2026-09-30 확인 | 전국 근무 가능 | SSAFY 중도 퇴소 후 입사 가능 | A: 우선 검토, B: 조건 확인 후 검토']];
sh.getRange('A5:O5').values=[headers];
sh.getRange(`A6:O${jobs.length+5}`).values=jobs;
const all=sh.getRange(`A2:O${jobs.length+5}`);
all.format.font={name:'Arial',size:10,color:'#1F2937'};
all.format.verticalAlignment='center';
sh.getRange('A2:O2').format.rowHeight=34;
sh.getRange('A2').format.font={name:'Arial',size:17,bold:true,color:'#183153'};
sh.getRange('A3:O3').format.rowHeight=28;
sh.getRange('A3').format.font={name:'Arial',size:10,italic:true,color:'#64748B'};
const head=sh.getRange('A5:O5');
head.format.fill='#183153';
head.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};
head.format.rowHeight=30;
head.format.horizontalAlignment='center';
const body=sh.getRange(`A6:O${jobs.length+5}`);
body.format.rowHeight=72;
body.format.wrapText=true;
body.format.verticalAlignment='center';
sh.getRange(`A6:A${jobs.length+5}`).format.horizontalAlignment='center';
sh.getRange(`H6:I${jobs.length+5}`).format.horizontalAlignment='center';
sh.getRange(`H6:H${jobs.length+5}`).setNumberFormat('yyyy-mm-dd');
const widths={A:12,B:20,C:26,D:38,E:18,F:27,G:27,H:15,I:12,J:43,K:63,L:63,M:56,N:65,O:40};
for(const [col,width] of Object.entries(widths)) sh.getRange(`${col}:${col}`).format.columnWidth=width;
const tbl=sh.tables.add(`A5:O${jobs.length+5}`,true,'FullHistoryJobs');
tbl.style='TableStyleMedium2';
tbl.showFilterButton=true;
sh.freezePanes.freezeRows(5);
sh.freezePanes.freezeColumns(3);

const ev=wb.worksheets.add('이력 검토 근거');
ev.showGridLines=false;
ev.tabColor='#0F766E';
ev.getRange('A2').values=[['추천에 반영한 전체 이력']];
ev.getRange('A3').values=[['첨부 이력서 + 포트폴리오 + 활동 문서 대조 | 업무 수행 사실과 교육·취미 활동을 구분']];
ev.getRange('A5:D5').values=[['구분','확인한 이력','적합한 업무에 주는 근거','평가 시 주의점']];
const evidence=[
  ['실무 경력','테크노전자 품질보증부 IQC 2020.06~2022.07 (2년 2개월)','수입검사, 검사 기준서, 데이터 기록, 불량 판정, 개선대책 요청','설비·계측기 종류와 수치 성과는 이력서에 없음'],
  ['학력·연구','금오공과대학교 경영학 학사, GPA 3.47/4.5, 학부 연구생, 생성형 AI 지속사용의도 논문 제2저자','리서치·데이터·시장/소비자 이해, 보고서 작성','공공 리서치 수주·고객사 납품 경력과 구분'],
  ['사업화·창업','플로라봇 사업화 지원 선정, SolarBeam 팀장·총무, 창업/발명 수상 8건','시장·특허·경쟁제품 조사, IR, 역할·예산·영수증·보고서 관리','공모전 성과와 상용 매출 성과를 혼동하지 않기'],
  ['교육·기술','SSAFY AI·Python·Django·Vue, CBDS 데이터 분석·SmartA 회계','기술팀 협업, AI/데이터 교육 PM, IT 제품 QA 및 사업지원','SSAFY는 현재 교육 중이며 입사 시 중도 퇴소 가능'],
  ['자격·면허','ADsP, FAT 1급, 컴퓨터활용능력 2급, 정보처리기능사, 1종 보통운전면허','데이터·기초 회계·문서·IT 이해·현장 이동','자격 취득과 해당 직무 실무경력은 별개'],
  ['포트폴리오','SSketch 250건 요구사항·버그 3건 재현, BodyBuilder UGC 명세/구현, ProjectRG 진단 설계','SW QA, 요구사항 관리, 서비스 설계, 개발 협업','교육 프로젝트이며 상용 서비스 운영 경력 아님'],
  ['장기 활동','카운터사이드 길드 2020~2026 운영, 최대 30명, 규칙·공지·합병 협의','커뮤니티 정책·이탈 대응·운영진 역할 분담','취미 활동이며 유급 운영 경력이 아님'],
  ['지원 조건','전국 근무 가능, SSAFY 과정 중도 퇴소 후 입사 가능','지역과 입사 시기를 넓혀 공고 검색','고용형태·마감 시각은 지원 직전 재확인'],
];
ev.getRange(`A6:D${evidence.length+5}`).values=evidence;
ev.getRange(`A2:D${evidence.length+5}`).format.font={name:'Arial',size:10,color:'#1F2937'};
ev.getRange('A2:D2').format.rowHeight=34;
ev.getRange('A2').format.font={name:'Arial',size:17,bold:true,color:'#0F766E'};
ev.getRange('A3:D3').format.rowHeight=28;
ev.getRange('A3').format.font={name:'Arial',size:10,italic:true,color:'#64748B'};
const evhead=ev.getRange('A5:D5');
evhead.format.fill='#0F766E';
evhead.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};
evhead.format.rowHeight=30;
ev.getRange(`A6:D${evidence.length+5}`).format.rowHeight=76;
ev.getRange(`A6:D${evidence.length+5}`).format.wrapText=true;
ev.getRange(`A6:D${evidence.length+5}`).format.verticalAlignment='center';
for(const [col,width] of Object.entries({A:20,B:72,C:72,D:62})) ev.getRange(`${col}:${col}`).format.columnWidth=width;
const et=ev.tables.add(`A5:D${evidence.length+5}`,true,'HistoryEvidence');
et.style='TableStyleMedium2';
et.showFilterButton=true;
ev.freezePanes.freezeRows(5);

wb.recalculate();
for(const [name,range] of [['종합 추천 공고','A5:J10'],['이력 검토 근거','A5:D9']]) {
  const result=await wb.inspect({kind:'region',sheetId:name,range,maxChars:3000,tableMaxRows:8,tableMaxCols:10});
  console.log(result.ndjson);
}
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'formula error scan'});
console.log(errors.ndjson);
for(const [name,range,suffix] of [['종합 추천 공고','A2:J8','jobs'],['이력 검토 근거','A2:D10','evidence']]) {
  const preview=await wb.render({sheetName:name,range,scale:1,format:'png'});
  await fs.writeFile(`${outDir}preview_${suffix}.png`,new Uint8Array(await preview.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(file);
console.log(file);

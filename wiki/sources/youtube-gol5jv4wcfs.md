---
title: "#19 65줄 CLAUDE.md로 10만 깃허브 스타 — 카파시 4대 원칙"
label: "#19 65줄 CLAUDE.md"
type: source
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-gol5jv4wcfs]
tags: [클로드md, 하네스엔지니어링, 카파시, 검증자동화, 골드리븐]
---

## 한 줄 요약
안드레이 카파시의 X 글에서 핵심 4원칙을 뽑아 만든 65줄짜리 CLAUDE.md 레포가 깃허브 10만+ 스타를 받은 현상을 해설하며, 각 원칙을 코드 예시로 풀어낸 영상.

## 핵심 내용
- 자막 표기 주의: 영상 자막은 저자를 "안드레 카파시 / 안드레 카파 씨"로 표기하나, 이는 **[[entities/andrej-karpathy|안드레이 카파시]](안드레이 카파시)**의 자막 오인식이다. OpenAI 공동창업자이자 전 Tesla AI 디렉터로, 그의 X 글이 출발점.
- 프레임워크도 라이브러리도 아닌 단일 텍스트 파일(65줄)이 10만 2,000+ 스타를 받음. 한 개발자가 카파시의 메시지에서 핵심 4원칙을 정리한 것.
- 카파시가 지적한 AI의 3대 고질병: ① 묻지 않고 멋대로 해석해 작업, ② 코드 부풀리기(몇 줄로 될 걸 1,000줄로, 안 쓰는 코드 방치), ③ 코드를 멋대로 고치고 주석 삭제. 결론은 "명령하지 말고 성공 기준을 주고 지켜보라."
- 4대 원칙:
  1. Think Before Coding — 추측 말고 트레이드오프를 드러내고 선택지를 제시. 해석이 여럿이면 고르지 말고 모두 제시, 헷갈리면 멈추고 되물어라.
  2. Simplicity First — 문제 해결에 필요한 최소 코드만. 일회용 코드에 추상화 금지, 요청 안 한 유연성·설정 금지, 200줄을 50줄로 줄일 수 있으면 다시 써라.
  3. Surgical Changes — 수술하듯 꼭 필요한 곳만 수정. 주변 코드·주석·서식 임의 개선 금지, 무관한 미사용 코드는 지우지 말고 보고만 하라.
  4. Goal-Driven Execution(가장 중요) — 성공 기준을 정의하고 검증될 때까지 반복. 과제를 "검증 가능한 목표"로 전환(예: "버그 고쳐"가 아니라 "버그를 드러내는 테스트를 작성하고 통과시켜라").

## 주요 주장 / 데이터
- 핵심 한 문장: "AI는 코드를 못 짜는 게 아니라 너무 잘, 너무 빨리, 너무 자신 있게 짠다. 문제는 능력 부족이 아니라 브레이크가 없다는 것."
- 이것이 "단순한 형태의 하네스 엔지니어링"임을 영상도 인정 — 새 기술·화려한 프레임워크 없이 65줄 마크다운만으로 효과.
- 적용 3가지: ① Karpathy Guidelines를 스킬로 설치(마켓플레이스 add → install → `/Ka`로 확인), ② 파일 직접 다운로드(전역/프로젝트, 기존 CLAUDE.md 덮어쓰기 주의), ③ 깃허브에서 복사해 새 CLAUDE.md에 붙여넣기.

## 기존 위키와의 연결
- 강화: [[concepts/claude-md|CLAUDE.md]]의 "짧고 검증 가능한 최소 규칙" 권장과 [[concepts/harness-engineering|하네스 엔지니어링]]·[[concepts/verification-automation|검증 자동화]]·[[concepts/skills|스킬]]을 강화.
- 강화/모순: [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]], [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]의 "CLAUDE.md로 품질 향상"을 강화하는 동시에, [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]와 모순 관계. 화해 관점: [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]의 비판 대상은 장황·불필요 규칙이고, 본 영상의 65줄은 "짧고 검증 가능한 최소 규칙"의 모범 사례 → [[concepts/claude-md|CLAUDE.md]]에 양쪽 모두 기록.
- 신규: [[entities/andrej-karpathy|안드레이 카파시]]를 핵심 인물로 도입(자막상 "안드레 카파시"로 표기되나 동일 인물). "Goal-Driven Execution = 검증 가능한 목표화" 패턴을 강조.

## 출처 정보
- raw: raw/youtube-gol5jv4wcfs.md
- URL: https://www.youtube.com/watch?v=gol5jv4wcfs
- 채널: castlestudio (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 자막 언어: 한국어 (ko) — 원본 영문 제목은 저자를 "Andre Capaci"로 표기(= 안드레이 카파시 오인식)
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3 (순번 19)

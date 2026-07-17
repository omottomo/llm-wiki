---
title: "#4 With just skills.sh, your AI coding level will change"
label: "#4 skills.sh"
type: source
created: 2026-06-23
updated: 2026-07-12
tags: [skills, skills-sh, 버셀, 패키지매니저, 보안, 클로드코드, 커서]
sources: [youtube-jae2bVCCokc]
---

## 한 줄 요약
AI 에이전트의 지식을 패키지처럼 설치하는 마켓플레이스 [[entities/skills-sh|skills.sh]]가 무엇이고 어떻게 설치하는지, 어떤 스킬을 깔아야 하며 보안상 무엇을 주의해야 하는지를 13분 분량으로 정리한 입문 영상.

## 핵심 내용
- skills.sh는 AI 에이전트한테 새로운 능력을 주는 스킬 마켓플레이스. "npm이 코드 라이브러리를 위한 패키지 매니저라면, skills.sh는 AI 에이전트의 지식을 위한 패키지 매니저"라는 비유.
- 스킬의 정체는 별게 아니라 `SKILL.md`(마크다운) 파일. "이런 상황에서는 이렇게 해라"를 써 두면 AI가 읽고 따른다. 예: 버셀 리액트 스킬을 깔면 클로드가 서버 컴포넌트 패턴·Next.js 앱 라우터 규칙·버셀 권장 방식대로 코드를 짠다.
- 설치는 `npx skills.sh add` 한 줄. CLI가 사용 중인 에이전트(클로드 코드, 커서, 코파일럿 등 18개 이상)를 자동 감지해 알맞게 설치. 특정 스킬만 깔려면 뒤에 `@이름`을 붙인다.
- 추천 스킬 5종: (1) find-skills(필수 — "이거 할 수 있는 스킬 찾아줘"로 자동 추천), (2) 버셀 리액트 베스트 프랙티스(React/Next.js 필수, 버셀 공식), (3) 웹 디자인 가이드라인(shadcn 조합으로 미니멀/심플 UI 퀄리티 향상), (4) Remotion 베스트 프랙티스(프로그래매틱 영상 제작용, 85,000건 설치), (5) 프론트엔드 디자인(6만건 이상 설치).
- 보안 3원칙: ① 공식 벤더 스킬 우선(버셀·Anthropic·프레임워크 제작), ② 설치수 확인(많이 깔린 게 검증된 것), ③ GitHub에서 SKILL.md 코드를 직접 읽어 수상한 내용이 없는지 확인.

## 주요 주장 / 데이터
- 버셀이 올해 1월 skills.sh를 공식 출시했고 설치가 폭발적으로 증가 중. 최상위 스킬은 이미 19만 건 이상 설치 (자막 기준).
- skills.sh는 완전 무료의 오픈소스이며 18개 이상의 에이전트를 지원.
- 커뮤니티 제출 스킬 중 품질 낮은 것이 많고("레딧에서 80%가 AI가 대충 만든 저품질이라는 말이 나올 정도"), 일부 스킬에서 숨겨진 악성 명령어가 발견된 보안 이슈가 있었음 → 아무 스킬이나 깔면 안 된다는 강한 경고.

## 기존 위키와의 연결
- 강화: [[concepts/skills|스킬]]의 핵심 1차 자료(스킬=SKILL.md, 패키지 매니저 비유, 설치/검증 방법). [[entities/skills-sh|skills.sh]]·[[entities/vercel|Vercel]]의 출시·운영 사실. [[concepts/harness-engineering|하네스 엔지니어링]]에서 스킬을 "하네스 구성 요소"로 보는 관점을 뒷받침. [[entities/claude-code|Claude Code]]·[[entities/cursor|Cursor]] 등 다중 에이전트 지원 사실.
- 모순: 없음(직접 충돌 없음). 다만 "공식·검증된 최소 스킬만"이라는 절제 권고는 #6 "Delete CLAUDE.md"(→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]])의 "장황한 자동생성 컨텍스트는 해롭다"는 절제론과 같은 결.
- 신규: [[entities/skills-sh|skills.sh]](마켓플레이스, 버셀 1월 출시) 도입. [[concepts/skills|스킬]]에 "스킬 보안/품질 검증" 하위 주제 신규 추가.

## 출처 정보
- raw: raw/youtube-jae2bVCCokc.md
- URL: https://www.youtube.com/watch?v=jae2bVCCokc
- 채널: 메이커 에반 | Maker Evan (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3

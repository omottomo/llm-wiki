---
title: 스킬 (Skills)
type: concept
created: 2026-06-23
updated: 2026-06-23
sources: [youtube-jae2bVCCokc, youtube-UClLUoGaCxU, youtube-hXlB1QstQ-Y, youtube-DCsv0rKKrN4]
tags: [클로드코드, 스킬, 하네스, 컨텍스트엔지니어링]
---
# 스킬 (Skills)

스킬은 AI 에이전트에게 특정 작업의 전문 지식·레시피를 파일로 정리해 주는 것으로, 정체는 `SKILL.md`라는 마크다운 파일이다. "이런 상황에서는 이렇게 해라"라고 써 두면 AI가 그걸 읽고 따른다 (→ [[sources/youtube-jae2bVCCokc]], → [[sources/youtube-BssPGKsP60s]] 참조). [[concepts/harness-engineering]]의 핵심 구성 요소다.

## CLAUDE.md와의 핵심 차이 — 필요할 때만 로딩
- `CLAUDE.md`는 세션 시작 시 무조건 컨텍스트에 들어가는 반면, **스킬은 실제로 필요할 때만 로드된다** (→ [[sources/youtube-hXlB1QstQ-Y]]). 스킬은 특정 작업에 대한 레시피를 갖고 있다 (→ [[sources/youtube-hXlB1QstQ-Y]]).
- 이 때문에 [[concepts/claude-md]]에 모든 문서를 넣는 대신 스킬로 옮기면, 특정 작업을 할 때 그 작업에 필요한 컨텍스트만 주입되도록 설계할 수 있다 (→ [[sources/youtube-c7_ANA1NiS0]] 참조 — claude-md 페이지에 정리).

## skills.sh — AI 에이전트 지식의 패키지 매니저
- [[entities/skills-sh]]는 [[entities/vercel]](버셀)이 올해 1월 공식 출시한 스킬 마켓플레이스로, 완전 무료 오픈소스다 (→ [[sources/youtube-jae2bVCCokc]]).
- npm이 코드 라이브러리의 패키지 매니저라면, skills.sh는 AI 에이전트 지식의 패키지 매니저다 (→ [[sources/youtube-jae2bVCCokc]]).
- 설치는 `npx skills.sh add` 한 줄. CLI가 어떤 에이전트를 쓰는지 감지해 알맞게 설치하며, [[entities/claude-code]]·[[entities/cursor]]·Copilot 등 18개 이상 에이전트를 지원한다 (→ [[sources/youtube-jae2bVCCokc]]). 최상위 스킬은 19만 건 이상 설치됐다 (→ [[sources/youtube-jae2bVCCokc]]).
- 추천 스킬: find-skills(필요 스킬 검색), 버셀 React 베스트 프랙티스, 웹 디자인 가이드라인(특히 shadcn/ui 조합에 강함), Remotion 베스트 프랙티스(약 85,000건 설치), 프런트엔드 디자인(6만 건+) (→ [[sources/youtube-jae2bVCCokc]]).
- **보안·품질 주의:** 커뮤니티 제출 스킬 중 저품질이 많고(레딧에서 "80%가 AI가 대충 만든 저품질"이라는 말), 일부 스킬에서 숨겨진 악성 명령어가 발견된 적도 있다. 규칙 세 가지 — ① 공식 밴더(버셀·Anthropic) 스킬 우선, ② 설치 수 확인, ③ 깃허브에서 `SKILL.md` 코드 직접 확인 (→ [[sources/youtube-jae2bVCCokc]]).

## 800시간 후의 6가지 필수 스킬
(→ [[sources/youtube-UClLUoGaCxU]]) 화려한 스킬보다 매일 손이 가는 단순한 스킬이 낫다는 관점으로 소개된 목록:
1. **Andrej Karpathy 스킬** — 단 한 장의 마크다운 파일인데 깃허브 스타 15만 개+. AI의 세 가지 고질병(모르면서 바로 코딩 시작, 100줄이면 될 걸 1000줄로, 버그 하나 고치라니 주변까지 수정)을 네 가지 규칙으로 정리. [[entities/andrej-karpathy]] 참조 (→ [[sources/youtube-UClLUoGaCxU]]).
2. **claude-video** — Claude가 유튜브 영상을 다운로드·프레임 추출·자막까지 읽어 실제로 "볼 수" 있게 함. 영상 길이에 따라 프레임 수 자동 조절(30초 이하 약 30프레임, 10분+ 약 100프레임) (→ [[sources/youtube-UClLUoGaCxU]]).
3. **superpowers (슈퍼파워)** — 깃허브 스타 20만 개+, Anthropic 공식 마켓 등록. Claude에게 시니어 개발자 프로세스를 강제: 코드 전에 스펙 정리→계획→테스트 먼저 작성(테스트 안 쓰면 코드 삭제). 서브에이전트를 활용해 각 태스크를 깨끗한 컨텍스트에서 돌리고 끝나면 두 번 리뷰. 첫 결과물 품질이 60점→80점으로 (→ [[sources/youtube-UClLUoGaCxU]]). [[concepts/subagents-agent-teams]] 참조.
4. **understand** — 깃허브 스타 4만 개+. `/understand`로 멀티에이전트가 코드베이스 전체를 스캔해 지식 그래프·인터랙티브 대시보드·가이드 투어를 만든다. PDF·마크다운·이미지까지 비전으로 읽음 (→ [[sources/youtube-UClLUoGaCxU]]).
5. **agent-memory** — 12개의 자동 후크 세션에서 모든 작업을 조용히 기록·압축해 로컬 DB에 저장하고, 다음 세션에 필요한 컨텍스트만 벡터·그래프 검색으로 골라 주입. 기본 빌트인 메모리보다 관련 없는 내용 혼입이 적음 (→ [[sources/youtube-UClLUoGaCxU]]).
6. **skill-creator** — Anthropic 공식 스킬. "이런 걸 만들고 싶다"고 설명하면 Claude가 스킬을 생성·테스트·패키징해 준다 (→ [[sources/youtube-UClLUoGaCxU]]).
- 보너스: Remotion 공식 스킬(React로 영상 제작) (→ [[sources/youtube-UClLUoGaCxU]]).

## 운영 철학
- **남이 만든 좋은 스킬을 먼저 가져다 쓰고**, 반복하는 작업이 보이면 그때 스킬로 저장한다. 스킬은 유지 비용이 거의 없으면서 유용해 "자산"이라 부를 수 있다 (→ [[sources/youtube-hXlB1QstQ-Y]]).
- **명시적으로 호출하라:** 스킬을 만들어 놔도 "그냥 이거 구현해 줘"라고 하면 Claude가 스킬을 안 쓰고 멋대로 할 수 있다. 도구·스킬·규칙을 진짜 쓰게 하려면 대놓고 지시해야 한다 (→ [[sources/youtube-hXlB1QstQ-Y]]).
- **한 번 만들고 끝이 아니다:** Anthropic 엔지니어들 말로, 사람들은 프롬프트 하나하나에는 공을 들이면서 그걸 스킬로 만들지는 않는다. Claude를 1일차에 쓰는 방식과 30일차에 쓰는 방식은 완전히 달라야 한다. 결과물에서 아쉬운 부분이 있으면 "다음부터는 이렇게 해 줘"라고 스킬을 수정해 가는 것이 [[concepts/agentic-coding]]의 핵심이다 (→ [[sources/youtube-UClLUoGaCxU]]).
- **커스텀 스킬로 워크플로우 자동화:** 예컨대 한 AI의 플랜을 다른 AI에게 전달해 취합·요약하는 "with multiple AI" 스킬을 만들면 검증 과정을 자동화할 수 있다 (→ [[sources/youtube-DCsv0rKKrN4]]). [[concepts/multi-model-workflow]] 참조.

## 연결
- [[concepts/claude-md]] — 무조건 로딩 vs 필요시 로딩의 대비.
- [[concepts/subagents-agent-teams]] — superpowers·understand가 멀티에이전트를 활용.
- [[concepts/harness-engineering]], [[concepts/verification-automation]], [[entities/skills-sh]], [[entities/vercel]].

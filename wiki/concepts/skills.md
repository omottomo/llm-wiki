---
title: 스킬 (Skills)
type: concept
created: 2026-06-23
updated: 2026-08-09
sources: [youtube-jae2bVCCokc, youtube-UClLUoGaCxU, youtube-hXlB1QstQ-Y, youtube-DCsv0rKKrN4, youtube-lokHQ8_b5Rk]
tags: [클로드코드, 스킬, 하네스엔지니어링, 컨텍스트엔지니어링]
---
# 스킬 (Skills)

## 한눈에 요약

- "이런 상황에서는 이렇게 하라"는 작업 요령을 **파일 하나(`SKILL.md`)에 적어 AI에게 건네는 장치**다.
- 규칙 파일과 결정적으로 다른 점은 로딩 시점이다. **실제로 그 작업을 할 때만 불려 온다.**
- 그래서 평소 AI가 읽어야 할 분량을 늘리지 않고도 전문 지식을 붙일 수 있다.
- 남이 만든 스킬을 받아 쓰는 마켓플레이스도 있다. 다만 품질 편차가 크고 숨은 악성 명령이 발견된 사례도 있다.
- 한 번 만들고 끝내는 물건이 아니다. 아쉬운 점이 보일 때마다 고쳐 나가는 게 요령이다.

## 스킬이란

스킬은 AI 에이전트에게 특정 작업의 전문 지식과 레시피를 파일로 정리해 주는 것이다. 정체는 `SKILL.md`라는 마크다운 파일 하나다. "이런 상황에서는 이렇게 해라"라고 써 두면 AI가 그걸 읽고 따른다 (→ [[sources/youtube-jae2bVCCokc|#4 skills.sh]]·[[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]). [[concepts/harness-engineering|하네스 엔지니어링]]의 핵심 구성 요소다.

## CLAUDE.md와의 핵심 차이 — 필요할 때만 로딩

| | [[concepts/claude-md\|CLAUDE.md]] | 스킬 |
|---|---|---|
| 로딩 시점 | 세션 시작 시 무조건 | 실제로 필요할 때만 |
| 담는 것 | 프로젝트 전반의 규칙 | 특정 작업의 레시피 |
| 컨텍스트 비용 | 항상 든다 | 쓸 때만 든다 |

`CLAUDE.md`는 세션 시작 시 무조건 컨텍스트에 들어간다. 반면 **스킬은 실제로 필요할 때만 로드된다** (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).

이 차이가 설계 여지를 만든다. [[concepts/claude-md|CLAUDE.md]]에 모든 문서를 넣는 대신 스킬로 옮기면, 특정 작업을 할 때 그 작업에 필요한 컨텍스트만 주입되도록 설계할 수 있다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]] 참조 — claude-md 페이지에 정리).

## skills.sh — AI 에이전트 지식의 패키지 매니저

[[entities/skills-sh|skills.sh]]는 [[entities/vercel|Vercel]](버셀)이 2026년 1월 공식 출시한 스킬 마켓플레이스다. 완전 무료 오픈소스다 (→ [[sources/youtube-jae2bVCCokc|#4 skills.sh]]).

쉽게 말하면 npm이 코드 라이브러리의 패키지 매니저라면, skills.sh는 AI 에이전트 지식의 패키지 매니저다 (→ [[sources/youtube-jae2bVCCokc|#4 skills.sh]]).

설치는 `npx skills.sh add` 한 줄이다. CLI가 어떤 에이전트를 쓰는지 감지해 알맞게 설치하며 [[entities/claude-code|Claude Code]]·[[entities/cursor|Cursor]]·Copilot 등 18개 이상 에이전트를 지원한다 (→ [[sources/youtube-jae2bVCCokc|#4 skills.sh]]). 최상위 스킬은 19만 건 이상 설치됐다(2026-06 자막 기준, 설치 수는 지속 증가하는 유동 지표) (→ [[sources/youtube-jae2bVCCokc|#4 skills.sh]]).

추천 스킬도 몇 개 꼽힌다 (→ [[sources/youtube-jae2bVCCokc|#4 skills.sh]]).

- find-skills — 필요한 스킬을 찾아 준다
- 버셀 React 베스트 프랙티스
- 웹 디자인 가이드라인 — 특히 shadcn/ui 조합에 강하다
- Remotion 베스트 프랙티스 — 약 85,000건 설치
- 프런트엔드 디자인 — 6만 건 이상 설치

> **보안·품질 주의.** 커뮤니티 제출 스킬 중 저품질이 많다. 레딧에서 "80%가 AI가 대충 만든 저품질"이라는 말이 나올 정도다. 일부 스킬에서는 숨겨진 악성 명령어가 발견된 적도 있다. 규칙 세 가지 — ① 공식 밴더(버셀·Anthropic) 스킬 우선, ② 설치 수 확인, ③ 깃허브에서 `SKILL.md` 코드 직접 확인 (→ [[sources/youtube-jae2bVCCokc|#4 skills.sh]]).

## 800시간 후의 6가지 필수 스킬

화려한 스킬보다 매일 손이 가는 단순한 스킬이 낫다는 관점으로 소개된 목록이다 (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]). 이하 스타·설치 수치는 모두 이 영상 자막 기준 2026-06 시점이며 지속 증가하는 유동 지표다.

1. **Andrej Karpathy 스킬** — 단 한 장의 마크다운 파일인데 깃허브 스타 15만 개 이상이다(자막 수치라 편차가 있다. 카파시 외부검증 기준 단일 저장소 약 9만, 미러 합산 약 22만). AI의 세 가지 고질병을 네 가지 규칙으로 정리한다. 모르면서 바로 코딩을 시작하고, 100줄이면 될 걸 1000줄로 쓰고, 버그 하나 고치라니 주변까지 수정하는 문제다. [[entities/andrej-karpathy|안드레이 카파시]] 참조 (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]).
2. **claude-video** — Claude가 유튜브 영상을 다운로드하고 프레임을 추출하고 자막까지 읽어 실제로 "볼 수" 있게 한다. 영상 길이에 따라 프레임 수를 자동 조절한다(30초 이하 약 30프레임, 10분 이상 약 100프레임) (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]).
3. **superpowers (슈퍼파워)** — 깃허브 스타 20만 개 이상, Anthropic 공식 마켓 등록. Claude에게 시니어 개발자 프로세스를 강제한다. 코드 전에 스펙 정리 → 계획 → 테스트 먼저 작성이고, 테스트를 안 쓰면 코드를 삭제한다. [[concepts/subagents-agent-teams|서브에이전트]]를 활용해 각 태스크를 깨끗한 컨텍스트에서 돌리고 끝나면 두 번 리뷰한다. 첫 결과물 품질이 60점에서 80점으로 올라간다 (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]).
4. **understand** — 깃허브 스타 4만 개 이상. `/understand`로 멀티에이전트가 코드베이스 전체를 스캔해 지식 그래프·인터랙티브 대시보드·가이드 투어를 만든다. PDF·마크다운·이미지까지 비전으로 읽는다 (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]).
5. **agent-memory** — 12개의 자동 후크 세션에서 모든 작업을 조용히 기록·압축해 로컬 DB에 저장한다. 다음 세션에는 필요한 컨텍스트만 벡터·그래프 검색으로 골라 주입한다. 기본 빌트인 메모리보다 관련 없는 내용이 덜 섞인다 (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]).
6. **skill-creator** — Anthropic 공식 스킬이다. "이런 걸 만들고 싶다"고 설명하면 Claude가 스킬을 생성·테스트·패키징해 준다 (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]).

보너스로 Remotion 공식 스킬(React로 영상 제작)도 언급된다 (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]).

## 비판 — 좋기만 한 물건인가

인기가 높은 만큼 반론도 붙는다 (→ [[sources/youtube-lokHQ8_b5Rk|#30 하네스·루프·그래프 순서대로]]).

- **평가가 어렵다** — 스킬을 써서 나온 결과가 괜찮은지 중간에 판단해서, 별로면 쳐내고 괜찮으면 가져와야 한다. 그런데 그 판정이 어렵다. 쓴 경우와 안 쓴 경우를 A/B로 비교하려면 평가 데이터와 환경이 따로 필요하다. 그래서 최근에는 **스킬은 평가가 중요하다**는 의견이 자주 보인다.
- **결국 프롬프트 덩어리다** — 근본적으로 보면 스킬은 컨텍스트 덩어리를 잘 넣어 주는 방법일 뿐이라는 지적이다. LLM이 더 똑똑해지는 방향이라기보다 **쓰는 사람이 편해지는** 쪽에 가깝다는 것이다.

> 이 비판이 스킬을 쓰지 말라는 뜻은 아니다. 같은 대담에서도 컨텍스트 관리 네 방식 중 가장 인기가 많았던 것이 스킬이고 지금도 다들 쓴다고 인정한다 (→ [[sources/youtube-lokHQ8_b5Rk|#30 하네스·루프·그래프 순서대로]]).

## 운영 철학

- **남의 것부터 가져다 쓴다** — 좋은 스킬을 먼저 받아 쓰고, 반복하는 작업이 보이면 그때 스킬로 저장한다. 스킬은 유지 비용이 거의 없으면서 유용해 "자산"이라 부를 수 있다 (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- **명시적으로 호출한다** — 스킬을 만들어 놔도 "그냥 이거 구현해 줘"라고 하면 Claude가 스킬을 안 쓰고 멋대로 할 수 있다. 도구·스킬·규칙을 진짜 쓰게 하려면 대놓고 지시해야 한다 (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- **한 번 만들고 끝이 아니다** — Anthropic 엔지니어들 말로는, 사람들이 프롬프트 하나하나에는 공을 들이면서 그걸 스킬로 만들지는 않는다고 한다. Claude를 1일차에 쓰는 방식과 30일차에 쓰는 방식은 완전히 달라야 한다. 결과물에서 아쉬운 부분이 있으면 "다음부터는 이렇게 해 줘"라고 스킬을 수정해 가는 것이 [[concepts/agentic-coding|에이전틱 코딩]]의 핵심이다 (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]).
- **커스텀 스킬로 워크플로우 자동화** — 한 AI의 플랜을 다른 AI에게 전달해 취합·요약하는 "with multiple AI" 스킬을 예로 들 수 있다. 이런 걸 만들면 검증 과정이 자동화된다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

## 함께 읽기

- [[concepts/claude-md|CLAUDE.md]] — 무조건 로딩 vs 필요할 때만 로딩의 대비
- [[concepts/subagents-agent-teams|서브에이전트 & 에이전트 팀]] — superpowers·understand가 활용하는 실행 단위
- [[concepts/multi-model-workflow|멀티 모델 워크플로우]] — 커스텀 스킬로 검증을 자동화하는 사례
- [[concepts/harness-engineering|하네스 엔지니어링]] · [[concepts/verification-automation|검증 자동화]]
- [[entities/skills-sh|skills.sh]] · [[entities/vercel|Vercel]] — 스킬 마켓플레이스와 그 제공사

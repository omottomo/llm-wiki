---
title: "분석 — 워크플로우 선택 가이드: 채팅/스킬/서브에이전트/배치/다이나믹/Goal"
type: analysis
created: 2026-06-23
updated: 2026-06-23
sources: [youtube-9fx2_1aTzq8, youtube-fInMcawbKng, youtube-z-3BRkxQ5GM, youtube-Gb2VMWrUmZ0, youtube-DCsv0rKKrN4]
tags: [분석, 워크플로우, 오케스트레이션, 선택가이드]
---

# 분석 — 워크플로우 선택 가이드

Claude Code에는 같은 모델이라도 작업을 어떤 **오케스트레이션 모드**로 돌리느냐에 따라 결과와 비용이 크게 달라지는 여러 기법이 있다. 이 페이지는 일반 채팅부터 [[concepts/dynamic-workflow|다이나믹 워크플로우]]의 딥리서치·울트라 코드, 그리고 목표 지향성이 가장 높은 골(Goal)까지를 **하나의 스펙트럼**으로 놓고, 어떤 작업에 무엇을 골라야 하는지를 정리한다.

핵심 축은 진화 스펙트럼이다. 왼쪽에서 오른쪽으로 갈수록 **토큰 비용과 목표 지향성이 함께 증가**한다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]):

> 일반 채팅 → [[concepts/skills|스킬]] → 서브에이전트 → 배치 → 딥리서치 / 울트라 코드(같은 티어) → 골(Goal)

서브에이전트·배치·딥리서치·울트라 코드·골은 결국 "하네스를 누가, 어디서, 얼마나 동적으로 들고 있느냐"의 차이다. 정적으로 사람이 미리 짜 두는 [[concepts/harness-engineering|하네스]]와 달리, 다이나믹 워크플로우 계열은 요청마다 그 자리에서 하네스를 만들어 낸다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).

## 비교표

| 모드 | 목표지향성 / 병렬성 | 컨텍스트·토큰 비용 | 적합 작업 | 주의점 |
|---|---|---|---|---|
| **일반 채팅** | 가장 낮음. 병렬 없음. 턴 제한 있고 보통 1단계에서 끝남 (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) | 가장 저렴. 메인 컨텍스트만 사용 | 순차·단일 파일, 짧은 질의응답, 한 번에 끝나는 수정 | 깊은 조사·대규모 구현엔 천장에 부딪힘. 결과 불만족 시 사람이 n번째 프롬프트를 직접 반복해야 함 (→ [[sources/youtube-z-3BRkxQ5GM\|#25 루프 엔지니어링]]) |
| **[[concepts/skills\|스킬]]** | 낮음. 플랜을 **메인 세션**이 들고 있음 (→ [[sources/youtube-fInMcawbKng\|#24 하네스 다이어트]]) | 낮음 | 반복되는 정형 작업 절차를 재사용 | 스킬이 수백 개로 불어나면 무엇을 쓸지 고르는 데 에너지를 낭비 — 핵심 몇 개만 강화 (→ [[sources/youtube-DrekqeDlO1w\|#14 하네스 문서 100번]] 참조, [[concepts/harness-engineering\|하네스 엔지니어링]]) |
| **서브에이전트** | 중간. 플랜을 **각 에이전트의 턴 단위**로 보유. 병렬 위임이되 결과만 회수 (→ [[sources/youtube-fInMcawbKng\|#24 하네스 다이어트]]·[[sources/youtube-Gb2VMWrUmZ0\|#3 Claude Code Teams]]) | 비교적 낮음. 분석을 따로 띄워 결과만 메인에 보내 컨텍스트 절약. 하이쿠로 빠른 검색도 가능 (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]·[[sources/youtube-Gb2VMWrUmZ0\|#3 Claude Code Teams]]) | 결과만 중요한 집중된 병렬 탐색(검색·분석), 생성/검증 분리 (→ [[sources/youtube-DCsv0rKKrN4\|#7 메타 엔지니어 실전편]]) | 시작 후 다시 건드릴 수 없고 결과만 받음. 순차·동일 파일·종속 많은 작업엔 부적합 (→ [[sources/youtube-Gb2VMWrUmZ0\|#3 Claude Code Teams]]) |
| **에이전트 팀** | 높음. 독립 Claude Code 인스턴스 여러 개를 **팀 리드가 중앙 오케스트레이션**, 팀원끼리 실시간 통신·공유 task list (→ [[sources/youtube-Gb2VMWrUmZ0\|#3 Claude Code Teams]]) | 매우 높음. 조율 오버헤드로 단일 세션·서브에이전트보다 **훨씬 많은 토큰**(병렬 N개면 대략 N배) (→ [[sources/youtube-Gb2VMWrUmZ0\|#3 Claude Code Teams]]) | 논의·협업이 필요한 복잡 작업: 연구·검토, 새 모듈/기능 분담 소유, 경쟁 가설 디버깅, 프론트/백 교차 계층 조율 (→ [[sources/youtube-Gb2VMWrUmZ0\|#3 Claude Code Teams]]) | 아직 실험 기능(`CLAUDE_CODE_EXPERIMENT_AGENT_TEAMS`, `--teammate-mode teamwork`). split-pane엔 tmux 권장. "팀으로 해줘"보다 "병렬 가능한 작업을 계획해줘"로 트리거 (→ [[sources/youtube-Gb2VMWrUmZ0\|#3 Claude Code Teams]]) |
| **배치(Batch)** | 중간. 독립·유사 작업을 묶어 한 번에 병렬 처리하는 "공장" 방식 (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) | 중간. 병렬 수만큼 비례 | 서로 독립적이고 비슷한 다수 작업(예: 버그 1~100번 일괄 처리) (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) | 작업 간 종속·상호참조가 있으면 부적합(독립성이 전제) |
| **딥리서치 (Deep Research)** | 높음. 조사→검증→추가조사 무한루프 후 리포트. 플랜을 **JS 스크립트 단**에서 관리해 대규모 병렬 가능 (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]·[[sources/youtube-fInMcawbKng\|#24 하네스 다이어트]]) | 높음. 페이즈마다 서브에이전트 병렬. 데모에서 **서치 6 → 패치 28 → 검증 75개** 병렬, 마지막 종합만 컨텍스트 위해 단독 (→ [[sources/youtube-fInMcawbKng\|#24 하네스 다이어트]]) | 깊고 다출처·검증 필요한 조사. Claude Code **기본 내장**(`딥 리서치` 명령) (→ [[sources/youtube-fInMcawbKng\|#24 하네스 다이어트]]) | 코드 생성용이 아님. 공식 문서상 동시 최대 16개·누적 최대 1,000개 에이전트 (→ [[sources/youtube-fInMcawbKng\|#24 하네스 다이어트]]) |
| **울트라 코드 (Ultra Code)** | 높음. 병렬 작업→리뷰→검증→재계획 루프 (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) | 높음. 딥리서치보다 **에이전트 수는 적지만**(컨텍스트가 중요) 각자 더 오래 돌아 토큰은 적지 않음. 데모: Foundation 4 → Build 14 → Integrate 2 → Review 3 (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) | 빠른 완료가 중요한 대규모 구현·리팩터. X하이(xhigh) 사고 수준에서 사용 (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) | 계획 설계가 결과를 좌우. 한 번에 끝낼 작은 작업을 굳이 루프로 돌리면 시간·토큰 낭비 (→ [[sources/youtube-z-3BRkxQ5GM\|#25 루프 엔지니어링]]) |
| **골 (Goal / 롱러닝)** | **가장 높음.** 턴 제한 없이 목표가 완전히 달성될 때까지 몇 시간~며칠 실행. 워크플로우 안에서 생성되지는 않음 (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) | 가장 높음. 장시간 누적 | 검증이 정말 까다롭고 완벽해야 하는 고난도 작업(예: Redis 캐싱 레이어 통합) (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) | 손으로 정의하기 어려워 **메타프롬프팅 필수**("이 작업할 골 프롬프트를 만들어줘"). 환각·"됐어요" 거짓이 줄고, 도저히 안 될 때만 사람에게 도움 요청 (→ [[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) |

## 선택 의사결정 가이드

작업의 성격을 위에서 아래로 따져 첫 번째로 맞는 항목을 고르면 된다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]·[[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

1. **순차적이거나 단일 파일·종속이 많은 작업, 또는 한 번에 끝낼 작은 작업** → **일반 채팅(단일 세션)**. 단일 세션이 가장 정확하고 완전한 컨텍스트를 받는다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]). 프론티어 모델이면 `ultra code`/max 한 방으로 끝날 일을 루프로 돌리지 말 것 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).
2. **결과만 회수하면 되는 병렬 탐색(검색·분석), 또는 생성/검증 분리** → **서브에이전트**. 컨텍스트를 적게 쓰고 결과만 메인에 모은다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]·[[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
3. **팀원끼리 논의·협업·교차 계층 조율이 실질적 가치를 더하는 복잡 작업** → **에이전트 팀** (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]). 토큰 4배 가까운 비용을 감수할 만큼 병렬 협업이 가치 있을 때만.
4. **서로 독립적이고 비슷한 다수 작업** → **배치** (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).
5. **깊고 다출처인 조사** → **딥리서치** (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).
6. **빠른 대규모 구현·리팩터** → **울트라 코드**. 완료 속도에 초점 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).
7. **검증이 정말 까다롭고 완벽해야 하는 고난도 작업** → **골(Goal)**. 끝까지 검증에 집착하는 롱러닝 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).

규칙 요약: **결과만 중요 → 서브에이전트, 논의·협업 필요 → 에이전트 팀**(→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]); **빠른 완료 → 울트라 코드, 완벽·검증 집착 → 골**(→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]). 단, 트렌드에 휩쓸리지 말고 **작업·프로젝트 규모와 본인 이해도에 맞는 도구(right tool for the right job)**를 써야 한다 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

## 주의: 정적 하네스 vs 동적 하네스, 그리고 하네스 다이어트

- **정적 하네스 vs 동적 하네스**: 서브에이전트·스킬·에이전트 팀은 사람이 미리 구성해 두는 쪽에 가깝고, 딥리서치·울트라 코드·골은 메인 에이전트가 요청마다 페이즈별로 하네스를 **동적으로 생성**한다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]). 즉 더 강한 모드를 고르는 것은 곧 더 많은 하네스를 자동 생성하도록 위임하는 것이다.
- **낡은 하네스를 덜어내라**: 모델이 좋아지면 과거에 만든 정적 하네스가 오히려 방해가 되거나 **제품 내장 기능과 중복**된다. Claude Code·Codex·Cursor 자체가 이미 하나의 하네스 레이어이므로, 그 위에 낡은 커스텀 하네스를 또 얹으면 중복되어 에이전트를 방해한다 — 지금은 "무엇을 더 붙일까"가 아니라 "불필요한 것을 어떻게 덜어낼까"의 타이밍이다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]). 다이나믹 워크플로우의 `ultra code`로 "하네스 레거시 스캔 → 하네스 다이어트"를 한 달에 한두 번 돌려 점검하기를 권장한다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]). 이 긴장(②)의 자세한 양면은 [[concepts/harness-engineering|하네스 엔지니어링]]에 기록돼 있다.

## 같이 보기

- [[concepts/dynamic-workflow|다이나믹 워크플로우]] — 딥리서치·울트라 코드·골의 상위 개념
- [[concepts/subagents-agent-teams|서브에이전트 & 에이전트 팀]] — 서브에이전트와 에이전트 팀의 차이
- [[concepts/loop-engineering|루프 엔지니어링]] — 울트라 코드/골이 돌리는 완성도 루프
- [[concepts/harness-engineering|하네스 엔지니어링]] — 정적·동적 하네스, 하네스 다이어트
- [[concepts/multi-model-workflow|멀티 모델 워크플로우]] — Codex 적대적 리뷰로 검증을 보강하는 변형
- [[analysis/ai-coding-evolution|AI 코딩 패러다임의 진화]] — 프롬프트→컨텍스트→하네스→루프 진화 서사

---
title: "분석 — 워크플로우 선택 가이드: 채팅/스킬/서브에이전트/배치/다이나믹/Goal"
type: analysis
created: 2026-06-23
updated: 2026-08-04
sources: [youtube-9fx2_1aTzq8, youtube-fInMcawbKng, youtube-z-3BRkxQ5GM, youtube-Gb2VMWrUmZ0, youtube-DCsv0rKKrN4]
tags: [분석, 워크플로우, 오케스트레이션, 선택가이드]
---

# 분석 — 워크플로우 선택 가이드

## 결론 먼저

> 같은 AI에게 같은 일을 시켜도 **어떤 실행 방식을 고르느냐에 따라 결과와 비용이 크게 달라진다**. 오른쪽으로 갈수록 알아서 해 주는 정도가 커지지만 비용도 함께 커진다. 그러니 작업 크기에 맞춰 필요한 만큼만 쓰면 된다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

Claude Code에는 작업을 어떤 **오케스트레이션 모드**로 돌리느냐에 따라 결과가 달라지는 기법이 여럿 있다. 이 페이지는 일반 채팅부터 [[concepts/dynamic-workflow|다이나믹 워크플로우]]의 딥리서치·울트라 코드, 그리고 목표 지향성이 가장 높은 골(Goal)까지를 **하나의 스펙트럼**으로 놓고 비교한다.

핵심 축은 진화 스펙트럼이다. 왼쪽에서 오른쪽으로 갈수록 **토큰 비용과 목표 지향성이 함께 증가**한다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).

> 일반 채팅 → [[concepts/skills|스킬]] → 서브에이전트 → 배치 → 딥리서치 / 울트라 코드(같은 티어) → 골(Goal)

쉽게 말하면 이 모드들의 차이는 하나로 모인다. **"하네스를 누가, 어디서, 얼마나 동적으로 들고 있느냐"**다. 사람이 미리 짜 두는 [[concepts/harness-engineering|하네스]]와 달리, 다이나믹 워크플로우 계열은 요청마다 그 자리에서 하네스를 만들어 낸다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).

## 비교표

| 모드 | 토큰 비용 | 언제 쓰나 |
|---|---|---|
| 일반 채팅 | 가장 저렴 | 순차·단일 파일, 한 번에 끝날 일 |
| [[concepts/skills\|스킬]] | 낮음 | 반복되는 정형 절차의 재사용 |
| 서브에이전트 | 비교적 낮음 | 결과만 회수하면 되는 병렬 탐색 |
| 에이전트 팀 | 매우 높음(N배) | 논의·협업이 필요한 복잡 작업 |
| 배치(Batch) | 중간 | 독립적이고 비슷한 다수 작업 |
| 딥리서치 | 높음 | 깊고 다출처인 조사 |
| 울트라 코드 | 높음 | 빠른 대규모 구현·리팩터 |
| 골(Goal) | 가장 높음 | 검증이 까다롭고 완벽해야 하는 작업 |

### 일반 채팅

목표 지향성이 가장 낮고 병렬이 없다. 턴 제한이 있고 보통 1단계에서 끝난다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]). 메인 컨텍스트만 쓰니 가장 저렴하다.

> **주의:** 깊은 조사나 대규모 구현에서는 천장에 부딪힌다. 결과가 아쉬우면 사람이 n번째 프롬프트를 직접 반복해야 한다 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

### 스킬

플랜을 **메인 세션**이 들고 있다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]). 반복되는 정형 작업 절차를 재사용할 때 쓴다.

> **주의:** 스킬이 수백 개로 불어나면 무엇을 쓸지 고르는 데 에너지를 낭비한다. 핵심 몇 개만 강화하는 편이 낫다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]] 참조).

### 서브에이전트

플랜을 **각 에이전트의 턴 단위**로 들고 있다. 병렬로 위임하되 결과만 회수한다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]·[[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

분석을 따로 띄워 결과만 메인에 보내니 컨텍스트가 절약된다. 하이쿠로 빠른 검색도 가능하다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]). 검색·분석 같은 집중된 병렬 탐색, 그리고 생성·검증 분리에 맞는다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

> **주의:** 시작 후에는 다시 건드릴 수 없고 결과만 받는다. 순차 작업, 동일 파일 편집, 종속이 많은 작업에는 부적합하다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

### 에이전트 팀

독립 Claude Code 인스턴스 여러 개를 **팀 리드가 중앙에서 오케스트레이션**한다. 팀원끼리 실시간으로 통신하고 task list를 공유한다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

맞는 작업은 논의와 협업이 필요한 복잡 작업이다. 연구·검토, 새 모듈 분담 소유, 경쟁 가설 디버깅, 프론트엔드·백엔드 교차 계층 조율이 여기 속한다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

다만 조율 오버헤드 때문에 단일 세션이나 서브에이전트보다 **훨씬 많은 토큰**을 쓴다. 병렬 N개면 대략 N배다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

> **주의:** 아직 실험 기능이다(`CLAUDE_CODE_EXPERIMENT_AGENT_TEAMS`, `--teammate-mode teamwork`). split-pane에는 tmux를 권장한다. "팀으로 해줘"보다 "병렬 가능한 작업을 계획해줘"로 트리거하는 편이 낫다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

### 배치(Batch)

독립적이고 유사한 작업을 묶어 한 번에 병렬 처리하는 "공장" 방식이다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]). 버그 1~100번 일괄 처리 같은 일에 맞는다. 비용은 병렬 수만큼 비례한다.

> **주의:** 작업 간 종속이나 상호 참조가 있으면 부적합하다. 독립성이 전제다.

### 딥리서치 (Deep Research)

조사 → 검증 → 추가 조사의 무한루프를 돈 뒤 리포트를 낸다. 플랜을 **JS 스크립트 단**에서 관리해 대규모 병렬이 가능하다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).

페이즈마다 서브에이전트가 병렬로 돈다. 데모에서는 **서치 6개 → 패치 28개 → 검증 75개**가 병렬로 동작했고, 마지막 종합만 컨텍스트를 위해 단독으로 돌았다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]). Claude Code에 **기본 내장**돼 있어 `딥 리서치` 명령으로 부른다.

> **주의:** 코드 생성용이 아니다. 공식 문서상 동시 최대 16개, 누적 최대 1,000개 에이전트다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).

### 울트라 코드 (Ultra Code)

병렬 작업 → 리뷰 → 검증 → 재계획 루프를 돈다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).

딥리서치보다 **에이전트 수는 적다**. 컨텍스트가 더 중요하기 때문이다. 다만 각자 더 오래 돌아서 토큰은 적지 않다. 데모 구성은 Foundation 4 → Build 14 → Integrate 2 → Review 3이었다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]). 빠른 완료가 중요한 대규모 구현·리팩터에 맞고, X하이(xhigh) 사고 수준에서 쓴다.

> **주의:** 계획 설계가 결과를 좌우한다. 한 번에 끝낼 작은 작업을 굳이 루프로 돌리면 시간과 토큰만 낭비된다 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

### 골 (Goal / 롱러닝)

목표 지향성이 **가장 높다.** 턴 제한 없이 목표가 완전히 달성될 때까지 몇 시간에서 며칠을 실행한다. 워크플로우 안에서 생성되지는 않는다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).

검증이 정말 까다롭고 완벽해야 하는 고난도 작업에 쓴다. Redis 캐싱 레이어 통합 같은 것이다.

> **주의:** 손으로 정의하기 어려워 **메타프롬프팅이 필수**다. "이 작업할 골 프롬프트를 만들어줘"라고 시켜야 한다. 대신 환각이나 "됐어요" 거짓이 줄고, 도저히 안 될 때만 사람에게 도움을 요청한다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).

## 선택 의사결정 가이드

작업의 성격을 위에서 아래로 따져 첫 번째로 맞는 항목을 고르면 된다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]·[[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

1. **순차적이거나 단일 파일·종속이 많은 작업, 또는 한 번에 끝낼 작은 작업** → **일반 채팅**. 단일 세션이 가장 정확하고 완전한 컨텍스트를 받는다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]). 프론티어 모델이면 `ultra code`나 max 한 방으로 끝날 일을 루프로 돌리지 않는다 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).
2. **결과만 회수하면 되는 병렬 탐색, 또는 생성·검증 분리** → **서브에이전트**. 컨텍스트를 적게 쓰고 결과만 메인에 모은다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]·[[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
3. **팀원끼리 논의·협업·교차 계층 조율이 실질적 가치를 더하는 복잡 작업** → **에이전트 팀**. 토큰 4배에 가까운 비용을 감수할 만큼 가치 있을 때만 쓴다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).
4. **서로 독립적이고 비슷한 다수 작업** → **배치** (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).
5. **깊고 다출처인 조사** → **딥리서치** (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).
6. **빠른 대규모 구현·리팩터** → **울트라 코드**. 완료 속도에 초점이 있다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).
7. **검증이 정말 까다롭고 완벽해야 하는 고난도 작업** → **골**. 끝까지 검증에 집착하는 롱러닝이다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).

규칙을 두 줄로 줄이면 이렇다. **결과만 중요하면 서브에이전트, 논의·협업이 필요하면 에이전트 팀**이다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]). 그리고 **빠른 완료면 울트라 코드, 완벽과 검증에 집착해야 하면 골**이다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]).

다만 트렌드에 휩쓸리면 안 된다. **작업 규모와 본인 이해도에 맞는 도구**를 써야 한다(right tool for the right job) (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

## 주의 — 정적 하네스 vs 동적 하네스

서브에이전트·스킬·에이전트 팀은 사람이 미리 구성해 두는 쪽에 가깝다. 반면 딥리서치·울트라 코드·골은 메인 에이전트가 요청마다 페이즈별로 하네스를 **동적으로 생성**한다 (→ [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]]·[[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).

한마디로 더 강한 모드를 고르는 건 더 많은 하네스를 자동 생성하도록 위임하는 것이다.

### 낡은 하네스는 덜어내라

모델이 좋아지면 과거에 만든 정적 하네스가 오히려 방해가 되거나 **제품 내장 기능과 중복**된다.

Claude Code·Codex·Cursor 자체가 이미 하나의 하네스 레이어다. 그 위에 낡은 커스텀 하네스를 또 얹으면 중복되어 에이전트를 방해한다. 지금은 "무엇을 더 붙일까"가 아니라 "불필요한 것을 어떻게 덜어낼까"의 타이밍이다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).

다이나믹 워크플로우의 `ultra code`로 "하네스 레거시 스캔 → 하네스 다이어트"를 한 달에 한두 번 돌려 점검하기를 권한다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]). 이 긴장②의 자세한 양면은 [[concepts/harness-engineering|하네스 엔지니어링]]에 기록돼 있다.

## 함께 읽기

- [[concepts/dynamic-workflow|다이나믹 워크플로우]] — 딥리서치·울트라 코드·골의 상위 개념
- [[concepts/subagents-agent-teams|서브에이전트 & 에이전트 팀]] — 두 방식의 차이
- [[concepts/loop-engineering|루프 엔지니어링]] — 울트라 코드와 골이 돌리는 완성도 루프
- [[concepts/harness-engineering|하네스 엔지니어링]] — 정적·동적 하네스와 하네스 다이어트
- [[concepts/multi-model-workflow|멀티 모델 워크플로우]] — Codex 적대적 리뷰로 검증을 보강하는 변형
- [[analysis/ai-coding-evolution|AI 코딩 패러다임의 진화]] — 프롬프트→컨텍스트→하네스→루프 서사

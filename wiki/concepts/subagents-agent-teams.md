---
title: 서브에이전트 & 에이전트 팀
type: concept
created: 2026-06-23
updated: 2026-08-03
sources: [youtube-Gb2VMWrUmZ0, youtube-jKjbXXBahiY, youtube-DCsv0rKKrN4]
tags: [클로드코드, 서브에이전트, 에이전트팀, 오케스트레이션, 멀티에이전트]
---
# 서브에이전트 & 에이전트 팀

## 한눈에 요약

- AI 하나가 모든 일을 떠안는 대신 **작업을 여러 갈래로 나눠 굴리는 두 가지 방식**이다.
- **서브에이전트**는 심부름꾼에 가깝다. 일을 맡기고 결과 보고만 받는다.
- **에이전트 팀**은 독립된 여러 인스턴스가 서로 메시지를 주고받고 할 일 목록을 공유하며 함께 일한다.
- 나눠 맡기면 각자가 읽어야 할 분량이 줄어 긴 작업에 유리하다. 다만 동시에 돌리는 만큼 **비용도 N배로 는다**.
- 고르는 기준: 결과만 중요하면 서브에이전트, 논의와 협업이 필요하면 에이전트 팀.

## 둘의 차이

| | 서브에이전트 | 에이전트 팀 |
|---|---|---|
| 구조 | 메인 세션 안의 위임 | 독립 Claude Code 인스턴스 여러 개 |
| 통신 | 결과만 메인에 반환 | 팀원끼리 실시간 메시지, 작업 목록 공유 |
| 도중 개입 | 불가 | 가능(팀메이트마다 대화창) |
| 토큰 비용 | 상대적으로 낮음 | 병렬 N개면 대략 N배 |

두 방식 모두 복잡한 작업을 병렬로 돌리기 위한 것이다. **서브에이전트(Subagent)**는 메인 세션 안에서 결과만 받아오는 위임 방식이다. **에이전트 팀(Agent Teams)**은 독립적인 Claude Code 인스턴스 여러 개를 한 곳에서 오케스트레이션한다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

## 서브에이전트

메인 스레드 안에서 세부 에이전트를 만들어 작업을 시키고 결과(리포트)를 받는다. 각자 자기 컨텍스트 윈도우를 갖고, 결과는 호출자인 메인 에이전트에게 반환된다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

가장 큰 장점은 컨텍스트 절약이다. 메인 에이전트의 컨텍스트를 적게 쓰면서 결과만 받을 수 있다. 요즘 에이전트는 분석을 서브에이전트로 띄우고 결과만 메인에 보내므로 컨텍스트를 훨씬 적게 쓴다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]] 참조). 토큰 비용도 에이전트 팀에 비하면 낮은 편이다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

> **한계:** 작업이 시작되면 그 서브에이전트를 다시 건드릴 수 없다. 결과를 받아오는 것밖에 못 한다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

## 에이전트 팀 (Agent Teams)

별도 플러그인이 아니다. Anthropic이 **Opus 4.6과 함께 공식 지원하기 시작한 기능**(자막상 "오퍼스 4.6")으로, 모델 출시보다 더 큰 업데이트라는 평가를 받았다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

하나의 메인 Claude Code가 완전히 독립적인 Claude Code 인스턴스, 즉 팀메이트들을 만든다. 메인은 오케스트레이터로서 작업을 분배하고 조율한다. 각 팀메이트는 독립 대화창을 갖고 사용자가 직접 태스크를 던질 수도 있다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

서브에이전트와 갈리는 지점은 통신이다. 결과만 보고하는 게 아니라 팀원들이 서로 직접 실시간으로 메시지를 주고받으며 공유 작업 목록(task list)을 조율한다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]). 대신 팀 조율 오버헤드 때문에 단일 세션이나 서브에이전트보다 **훨씬 많은 토큰**을 쓴다. 병렬 에이전트 N개면 대략 N배다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

### 언제 무엇을 쓰나

- **에이전트 팀이 나은 경우** — 병렬 탐색이 실질적 가치를 더하는 작업이다. 연구·검토(여러 팀원이 동시에 조사한 뒤 공유·도전), 새 모듈이나 기능(각자 별도 부분 소유), 경쟁 가설 디버깅, 프론트엔드·백엔드 교차 계층 조율이 여기 속한다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).
- **단일 세션·서브에이전트가 나은 경우** — 순차적 작업, 동일 파일 편집, 종속이 많은 작업이다. 단일 세션이 더 정확하고 완전한 컨텍스트를 받는다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

한마디로 결과만 중요한 집중된 작업엔 서브에이전트, 논의와 협업이 필요한 복잡한 작업엔 에이전트 팀이다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

### 설정 (실험 기능)

- `settings.json`(유저 또는 프로젝트)에 `CLAUDE_CODE_EXPERIMENT_AGENT_TEAMS`를 1로 두고(자막상 표기), 팀메이트 모드는 `teamwork`로 설정하는 것을 권장한다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).
- 모드는 둘이다. in-process는 한 창 안에서 백그라운드 태스크처럼 돌리고 Shift 위아래로 팀메이트를 전환한다. split-pane(=teamwork)은 팀메이트를 만들 때마다 창을 분할한다. split-pane을 쓰려면 **tmux** 설치를 강력히 권장하며 macOS에서 가장 잘 작동한다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).
- 플래그 `--teammate-mode teamwork`로 세션별 강제 실행도 된다. 아직 베타라 설정이 안 먹힐 때가 있어 플래그를 같이 주는 편이 안전하다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

여기서 요령이 하나 있다. 팀을 제대로 트리거하려면 "팀으로 구성해 작업해 줘"라고 하는 것보다, 어떤 작업을 병렬로 할 수 있고 팀메이트를 어떻게 구성할지 **계획해 달라**고 요청하는 편이 낫다. 에이전트 팀 공식 문서 링크를 함께 주면 적합하게 구성될 확률이 높다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

동작 패턴은 이렇다. 메인(팀 리드)이 태스크 리스트를 만들고 팀메이트를 생성해 작업을 뿌린다. 작업이 끝나면 팀메이트는 자동으로 디스포즈되며, 팀 이름으로 저장돼(결국 파일로 저장) 다시 불러올 수 있다. 전역 task ID를 주입하면 팀메이트 없이도 여러 Claude Code가 알아서 오케스트레이션하고 통신하게 만들 수 있다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).

## 멀티에이전트 오케스트레이션 — 코워크·데스크탑

코딩이나 SDK 없이도 된다. [[entities/claude-code|Claude Code]]가 아닌 Claude 데스크탑 앱의 코워크(co-work)에서 대화만으로 에이전트 팀을 만들어 쓸 수 있다 (→ [[sources/youtube-jKjbXXBahiY|#18 주식 에이전트 팀]]).

에이전트는 "역할 정의 + 행동 규칙 + 출력 형식"을 담은 마크다운 파일이다. Anthropic은 이를 하나의 마크다운 파일로 만들라고 정의한다. 프롬프트에 "Anthropic 공식 에이전트 가이드에 따라 만들어라", "YAML 프론트매터 + 마크다운 시스템 프롬프트로"라고 준다. 여기에 `description`으로 `proactive use`를 넣으면 적절한 서브에이전트를 잘 호출한다 (→ [[sources/youtube-jKjbXXBahiY|#18 주식 에이전트 팀]]).

하나의 마크다운보다 **서브에이전트 여러 개의 MD 파일을 만들어 "한 명의 팀장이 팀원들을 돌리는" 오케스트레이션 구조**가 더 효율적이고 좋은 답을 가져온다. 예를 들어 오케스트레이터 1 + 서브에이전트 6, 총 7개 구성이다. Opus 4.6과 확장 사고로 만들면 MD 파일을 더 잘 만든다 (→ [[sources/youtube-jKjbXXBahiY|#18 주식 에이전트 팀]]).

실제로 주식 분석 에이전트 팀에서 에이전트 3개를 병렬 투입해 시장 리서치를 빠르게 진행하고 종합 보고서를 만들었다. "에이전트 팀스 개념이 어느 정도 접목됐다"는 평가다 (→ [[sources/youtube-jKjbXXBahiY|#18 주식 에이전트 팀]]).

## 역할 분리 패턴 — 리서처 / 플래너 / 리뷰어

하나의 AI에 조사·구현·리뷰·디버깅을 다 시키면 결과가 흔들린다. 회사에서 기획자·개발자·리뷰어·QA가 다른 것과 같은 이유로 AI도 역할을 나눈다. **리서처는 조사만, 플래너는 계획만, 리뷰어는 직접 수정하지 않고 문제점만** 찾는다 (→ 생각등대 영상 `wa6ZoLlnB60` — 출처 페이지는 2026-07-12 커리어 위키로 이관됨).

특히 리뷰어가 코드를 직접 고치면 그 순간 리뷰가 아니라 또 하나의 구현이 되어 검증자가 사라진다. [[concepts/verification-automation|검증 자동화]]의 생성·검증 분리와 같은 원리다.

## 실전 워크플로우 연결

- 멀티 터미널(여러 터미널로 작업을 하나씩 분담)에서 더 나아가면 서브에이전트와 에이전트 팀까지 쓸 줄 알아야 한다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
- 로컬 `todo.md`를 공유하고 에이전트 팀으로 여러 태스크를 병렬 처리하면 여러 세션에 걸친 작업 연속성을 유지할 수 있다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
- 코드를 만드는 AI와 검증하는 AI를 서브에이전트로 분리하면 자기 평가의 함정을 피한다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]] 및 [[concepts/verification-automation|검증 자동화]] 참조).

## 함께 읽기

- [[concepts/verification-automation|검증 자동화]] — 생성과 검증을 갈라놓는 이유
- [[concepts/dynamic-workflow|다이나믹 워크플로우]] — 병렬 에이전트를 워크플로우로 굳힌 형태
- [[concepts/loop-engineering|루프 엔지니어링]] — 반복 자체를 자동화하는 다음 단계
- [[concepts/harness-engineering|하네스 엔지니어링]] — 이 모든 구성 요소의 상위 개념
- [[concepts/skills|스킬]] — superpowers·understand가 멀티에이전트를 활용하는 사례
- [[entities/claude-code|Claude Code]] · [[entities/anthropic|Anthropic]]

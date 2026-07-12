---
title: 서브에이전트 & 에이전트 팀
type: concept
created: 2026-06-23
updated: 2026-06-28
sources: [youtube-Gb2VMWrUmZ0, youtube-jKjbXXBahiY, youtube-DCsv0rKKrN4, youtube-wa6ZoLlnB60]
tags: [클로드코드, 서브에이전트, 에이전트팀, 오케스트레이션, 멀티에이전트]
---
# 서브에이전트 & 에이전트 팀

여러 개의 AI 작업 단위를 동시에/위임 방식으로 돌려 복잡한 작업을 병렬 처리하는 두 가지 메커니즘. **서브에이전트(Subagent)**는 메인 세션 안에서 결과만 받아오는 위임 방식이고, **에이전트 팀(Agent Teams)**은 독립적인 Claude Code 인스턴스 여러 개를 한 곳에서 오케스트레이션하는 방식이다 (→ [[sources/youtube-Gb2VMWrUmZ0]]).

## 서브에이전트
- 메인 스레드 안에서 세부 에이전트를 생성해 작업을 시키고 결과(리포트)를 받는다. 자기 컨텍스트 윈도우를 갖고, 결과는 호출자(메인 에이전트)에게 반환된다 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 한계: 작업이 시작되면 그 서브에이전트를 다시 건드릴 수 없고, 결과를 받아오는 것밖에 못 한다 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 토큰 비용이 상대적으로 낮다(원래 Claude Code에서 가장 비싼 기능 중 하나였으나, 에이전트 팀과 비교하면 낮은 편) (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 장점: 메인 에이전트의 컨텍스트를 적게 쓰면서 결과만 받을 수 있다. 현대 에이전트는 분석을 서브에이전트로 띄워 결과만 메인에 보내므로 컨텍스트를 훨씬 적게 쓴다 (→ [[sources/youtube-c7_ANA1NiS0]] 참조).

## 에이전트 팀 (Agent Teams)
- 별도 플러그인이 아니라 Anthropic이 **Opus 4.6과 함께 공식 지원하기 시작한 기능**(자막상 "오퍼스 4.6")으로, 모델 출시보다 더 큰 업데이트로 평가됐다 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 하나의 메인 Claude Code가 완전히 독립적인 Claude Code 인스턴스(팀메이트)들을 생성해, 메인이 오케스트레이터로서 작업을 분배·조율한다. 각 팀메이트는 독립 대화창을 갖고 사용자가 직접 태스크를 던질 수도 있다 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 통신: 서브에이전트가 메인에 결과만 보고하는 것과 달리, 팀원들이 서로 직접 실시간으로 메시지를 주고받으며 공유 작업 목록(task list)을 공유·조율한다 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 비용: 팀 조율 오버헤드 때문에 단일 세션·서브에이전트보다 **훨씬 많은 토큰**을 쓴다(병렬 에이전트 N개면 대략 N배) (→ [[sources/youtube-Gb2VMWrUmZ0]]).

### 언제 무엇을 쓰나
- 에이전트 팀이 효과적인 경우: 병렬 탐색이 실질적 가치를 더하는 작업 — 연구·검토(여러 팀원이 동시에 조사 후 공유·도전), 새 모듈/기능(각자 별도 부분 소유), 경쟁 가설 디버깅, 프론트엔드/백엔드 교차 계층 조율 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 단일 세션·서브에이전트가 나은 경우: 순차적 작업, 동일 파일 편집, 종속이 많은 작업(단일 세션이 더 정확·완전한 컨텍스트를 받음) (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 요약: 결과만 중요한 집중된 작업엔 서브에이전트, 논의·협업이 필요한 복잡한 작업엔 에이전트 팀 (→ [[sources/youtube-Gb2VMWrUmZ0]]).

### 설정 (실험 기능)
- `settings.json`(유저 또는 프로젝트)에 `CLAUDE_CODE_EXPERIMENT_AGENT_TEAMS`를 1로(자막상 표기), 팀메이트 모드는 `teamwork`로 설정 권장 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 모드 두 가지: in-process(한 창 안에서 백그라운드 태스크처럼, Shift 위아래로 팀메이트 전환) vs split-pane(=teamwork, 팀메이트 생성 때마다 창 분할). split-pane을 위해 **tmux** 설치를 강력 권장하며 macOS에서 가장 잘 작동한다 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 플래그 `--teammate-mode teamwork`로 세션별 강제 실행도 가능. 아직 베타라 설정이 안 먹힐 때가 있어 플래그를 같이 주는 게 안전 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 팀을 제대로 트리거하려면 "팀으로 구성해 작업해 줘"보다, 어떤 작업을 병렬로 할 수 있고 팀메이트를 어떻게 구성할지 **계획해 줘**라고 요청하고, 에이전트 팀 공식 문서 링크를 함께 주면 적합하게 구성될 확률이 높다 (→ [[sources/youtube-Gb2VMWrUmZ0]]).
- 패턴: 메인(팀 리드)이 태스크 리스트를 만들고 팀메이트를 생성해 작업을 뿌린다. 작업이 끝나면 팀메이트는 자동으로 디스포즈되며, 팀 이름으로 저장돼(결국 파일로 저장) 다시 불러올 수 있다. 전역 task ID를 주입하면 팀메이트 없이도 여러 Claude Code가 알아서 오케스트레이션·통신하게 만들 수 있다 (→ [[sources/youtube-Gb2VMWrUmZ0]]).

## 멀티에이전트 오케스트레이션 (코워크/데스크탑 활용)
- 코딩이나 SDK 없이 [[entities/claude-code]]가 아닌 Claude 데스크탑 앱의 코워크(co-work)에서, 대화만으로 에이전트 팀을 만들어 활용할 수 있다 (→ [[sources/youtube-jKjbXXBahiY]]).
- 에이전트는 "역할 정의 + 행동 규칙 + 출력 형식"을 담은 마크다운 파일이며, Anthropic은 이를 하나의 마크다운 파일로 만들라고 정의한다. 프롬프트에 "Anthropic 공식 에이전트 가이드에 따라 만들어라", "YAML 프론트매터 + 마크다운 시스템 프롬프트로", `description`에 `proactive use`를 넣으면 적절한 서브에이전트를 잘 호출한다 (→ [[sources/youtube-jKjbXXBahiY]]).
- 하나의 마크다운보다 **서브에이전트 여러 개의 MD 파일을 만들어 "한 명의 팀장이 팀원들을 돌리는" 오케스트레이션 구조**가 더 효율적이고 좋은 답을 가져온다(예: 오케스트레이터 1 + 서브에이전트 6 = 총 7개). Opus 4.6 + 확장 사고로 만들면 MD 파일을 더 잘 만든다 (→ [[sources/youtube-jKjbXXBahiY]]).
- 실제로 주식 분석 에이전트 팀에서 에이전트 3개를 병렬 투입해 시장 리서치를 빠르게 진행하고 종합 보고서를 만들었다("에이전트 팀스 개념이 어느 정도 접목됨") (→ [[sources/youtube-jKjbXXBahiY]]).

## 역할 분리 패턴 — 리서처 / 플래너 / 리뷰어
- 하나의 AI에 조사·구현·리뷰·디버깅을 다 시키면 결과가 흔들린다. 회사의 기획자·개발자·리뷰어·QA가 다르듯 AI도 역할을 나눈다 — **리서처는 조사만, 플래너는 계획만, 리뷰어는 직접 수정하지 않고 문제점만** 찾는다 (→ [[sources/youtube-wa6ZoLlnB60]]).
- 특히 리뷰어가 코드를 직접 고치면 그 순간 리뷰가 아니라 또 하나의 구현이 되어 검증자가 사라진다 → [[concepts/verification-automation]]의 생성/검증 분리와 동일 원리. 이 역할 분리 경험은 이력서에 쓸 수 있는 실무 역량으로도 제시된다([[concepts/ai-resume-writing]]) (→ [[sources/youtube-wa6ZoLlnB60]]).

## 실전 워크플로우 연결
- 멀티 터미널(여러 터미널로 작업 하나씩 분담)에서 더 나아가면 서브에이전트·에이전트 팀까지 쓸 줄 알아야 한다 (→ [[sources/youtube-DCsv0rKKrN4]]).
- 로컬 `todo.md`를 공유하고 에이전트 팀으로 여러 태스크를 병렬 처리하면 여러 세션에 걸친 작업 연속성을 유지할 수 있다 (→ [[sources/youtube-DCsv0rKKrN4]]).
- [[concepts/verification-automation]]: 코드를 만드는 AI와 검증하는 AI를 서브에이전트로 분리하면 자기 평가의 함정을 피한다(→ [[sources/youtube-DCsv0rKKrN4]] 및 harness 페이지 참조).

## 연결
- [[concepts/dynamic-workflow]], [[concepts/loop-engineering]], [[concepts/harness-engineering]], [[concepts/skills]] (superpowers·understand가 멀티에이전트 활용), [[entities/claude-code]], [[entities/anthropic]].

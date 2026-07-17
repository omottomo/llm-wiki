---
title: 훅 (Hooks)
type: concept
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-6cr4PeilKJk, youtube-DrekqeDlO1w, youtube-6gvnDSAcZww]
tags: [클로드코드, 훅, 하네스, 검증자동화, 프리커밋]
---
# 훅 (Hooks)

훅은 Claude가 특정 시점(예: 작업을 마치려는 순간, 코드를 저장하기 직전)에 **자동으로 실행되는 스크립트**다. [[concepts/claude-md|CLAUDE.md]]가 "맥락·부탁"이라면, 훅은 "강제"다 — 부탁은 안 지킬 수 있지만 훅은 자동 실행되므로 우회할 수 없다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]). [[concepts/harness-engineering|하네스 엔지니어링]]에서 규칙을 시스템에 내장해 자동 강제하는 핵심 장치다.

## 핵심 원리 — "부탁이 아니라 구조"
- CLAUDE.md에 "테스트를 꼭 해 달라"고 적을 수 있지만 이는 맥락(부탁)이라 AI가 안 지킬 수 있다. 훅을 쓰면 이걸 강제할 수 있다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]).
- 예: Claude가 코드를 저장하려는 순간 훅이 자동으로 타입 검사·문법 체크를 돌리고, 에러가 있으면 Claude에게 다시 돌려보낸다. Claude가 그걸 보고 스스로 또 고친다 — 사람이 개입하지 않아도 된다. 못 짜면 훅에서 막혀 "저장 자체가 안 되는 구조"를 만든다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).
- [[concepts/harness-engineering|하네스 엔지니어링]]의 정의(에이전트가 실수할 때마다 그 실수가 구조적으로 반복 불가능하도록 환경을 고치는 것)를 코드 저장 시점에서 실현하는 도구가 프리커밋 훅이다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]·[[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

## 자동 교정 루프 (Self-correction Loop)
- 린터(코드의 맞춤법 검사기)가 규칙 위반 시 빨간 불을 켜면, 에이전트가 스스로 코드를 수정하기 시작한다. 사람 개입이 필요 없다. "말이 곱비에 의해 방향이 틀어지면 자연스럽게 올바른 방향으로 돌아오는 것"에 비유된다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).
- 이 자동 교정 루프가 하네스의 핵심 메커니즘이다 — 자동으로 막고, 자동으로 고친다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).
- 구성: 린터 + 구조적 테스트(예: "이 폴더 코드는 저 폴더 코드를 import할 수 없다" 같은 의존성 규칙 강제) + 프리커밋 훅(저장 직전 자동 검사) (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

## 출력 원칙 — "성공은 조용히, 실패만 시끄럽게"
- 테스트가 다 통과하면 아무 말도 하지 않고, 실패했을 때만 에이전트에게 알려야 한다. 통과한 테스트 결과 4,000줄을 다 보여주면 AI가 그걸 읽느라 정작 할 일을 잃어버리기(컨텍스트 오염) 때문이다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]). [[concepts/context-decay|컨텍스트 부패]] 참조.

## 또 다른 용례 — "로깅 훅"(강제가 아니라 기록·추적성)
훅의 대표 용도는 '강제'이지만, **AI 작업을 기록하는 로깅 훅**이라는 별개 용례도 있다. 어떤 프롬프트를 입력했고 AI가 어떤 파일을 읽고 어떤 명령을 실행했는지를 훅으로 자동 기록하면, AI 작업을 블랙박스로 두지 않고 **재연성·디버깅 가능성·운영성**을 확보한다 — 엉뚱한 파일이 수정됐을 때 "내 요청이 모호했는지"를 프롬프트 로그로, 문제 명령이 "언제 실행됐는지"를 툴 로그로 추적할 수 있다 (→ 생각등대 영상 `wa6ZoLlnB60` — 출처 페이지는 2026-07-12 커리어 위키로 이관됨).

## 다른 강제 장치와의 관계
하네스에서 "규칙을 강제하는" 층위는 여러 가지가 있고, 훅은 그중 하나다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]):
- **퍼미션(Permissions):** 위험한 명령(파일 삭제 등)을 실행 자체를 차단. "CLAUDE.md=맥락, 퍼미션=어길 수 없게 만드는 것" (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]).
- **훅:** 저장·종료 시점에 검증을 자동 실행해 강제(부탁→강제) (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]).
- **도구 경계(tool boundaries):** AI가 접근할 수 있는 범위·권한을 미리 제한(예: source 폴더는 읽기/쓰기, config 폴더는 읽기만; DB는 SELECT만 가능, DROP TABLE 불가) (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

## 실제 사례 — 오픈AI / 랭체인
- OpenAI 엔지니어 3명이 5개월간 코드를 한 줄도 안 쓰고 제품을 배포한 사례에서, 네 가지 중 하나가 "CI 게이트"(코드 저장 시 자동 테스트), 그리고 피드백 루프(린트·테스트·훅으로 자동 검증하는 파이프라인)였다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]·[[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).
- 랭체인(LangChain)은 모델을 바꾸지 않고 하네스(린트/테스트/훅 등)만 개선해 코딩 에이전트 벤치마크에서 30위권→5위권으로 25단계 상승시켰다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

## 실전 적용 — "레벨 1" 세팅
- 가장 쉽게 시작할 두 가지: ① 프로젝트 지침이 담긴 `CLAUDE.md`/`AGENTS.md`, ② 저장 전 자동 검사하는 **프리커밋 훅**. 한두 시간이면 설정 가능하다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).
- WAT 프레임워크의 도구(T) 예: MCP로 PR 생성, **훅으로 커밋마다 테스트를 자동 실행**하게 만든다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]] 참조).
- 모델이 좋아지면 불필요해진 제약(훅 포함)은 빼야 한다 — Anthropic도 Opus 4.6 출시 후 하네스를 간소화했다([[concepts/harness-engineering|하네스 엔지니어링]]의 '하네스 다이어트' 긴장과 연결) (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]).

## 연결
- [[concepts/harness-engineering|하네스 엔지니어링]] (훅은 하네스의 세 기둥 중 '자동 강제 시스템'에 속함), [[concepts/claude-md|CLAUDE.md]] (부탁 vs 강제), [[concepts/verification-automation|검증 자동화]], [[concepts/context-decay|컨텍스트 부패]], [[concepts/mcp|MCP]], [[entities/mitchell-hashimoto|미첼 하시모토]].

---
title: 훅 (Hooks)
type: concept
created: 2026-06-23
updated: 2026-08-03
sources: [youtube-6cr4PeilKJk, youtube-DrekqeDlO1w, youtube-6gvnDSAcZww, hashicorp-terraform-docs]
tags: [클로드코드, 훅, 하네스엔지니어링, 검증자동화, 프리커밋]
---
# 훅 (Hooks)

## 한눈에 요약

- AI가 코드를 저장하거나 작업을 끝내려는 **특정 순간에 자동으로 실행되는 짧은 스크립트**다.
- 규칙 파일에 적어 둔 부탁은 안 지켜질 수 있다. 훅은 사람이 안 보고 있어도 반드시 실행되므로 **우회할 수 없다**.
- 검사에 걸린 결과는 AI에게 그대로 되돌아가 스스로 고치게 된다. 이 자동 교정 고리가 핵심이다.
- 출력 원칙이 하나 있다. **성공은 조용히, 실패만 시끄럽게.** 통과 로그를 다 보여주면 컨텍스트가 오염된다.

## 핵심 원리 — 부탁이 아니라 구조

훅은 Claude가 특정 시점에 **자동으로 실행되는 스크립트**다. 작업을 마치려는 순간이나 코드를 저장하기 직전 같은 시점이다.

[[concepts/claude-md|CLAUDE.md]]가 "맥락, 부탁"이라면 훅은 "강제"다. 부탁은 안 지킬 수 있지만 훅은 자동 실행되므로 우회할 수 없다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]). [[concepts/harness-engineering|하네스 엔지니어링]]에서 규칙을 시스템에 내장해 자동 강제하는 핵심 장치다.

CLAUDE.md에 "테스트를 꼭 해 달라"고 적을 수는 있다. 다만 이건 맥락이라 AI가 안 지킬 수 있다. 훅을 쓰면 강제할 수 있다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]).

예를 들어 Claude가 코드를 저장하려는 순간 훅이 자동으로 타입 검사와 문법 체크를 돌린다. 에러가 있으면 Claude에게 다시 돌려보내고, Claude가 그걸 보고 스스로 고친다. 사람이 개입하지 않아도 된다. 못 짜면 훅에서 막혀 "저장 자체가 안 되는 구조"가 된다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

하네스 엔지니어링의 정의는 "에이전트가 실수할 때마다 그 실수가 구조적으로 반복 불가능하도록 환경을 고치는 것"이다. 이를 코드 저장 시점에서 실현하는 도구가 프리커밋 훅이다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]·[[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

## 자동 교정 루프 (Self-correction Loop)

린터(코드의 맞춤법 검사기)가 규칙 위반 시 빨간 불을 켜면 에이전트가 스스로 코드를 수정하기 시작한다. 사람 개입이 필요 없다. "말이 곱비에 의해 방향이 틀어지면 자연스럽게 올바른 방향으로 돌아오는 것"에 비유된다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

이 자동 교정 루프가 하네스의 핵심 메커니즘이다. 자동으로 막고, 자동으로 고친다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

구성은 세 가지다. 린터, 구조적 테스트("이 폴더 코드는 저 폴더 코드를 import할 수 없다" 같은 의존성 규칙 강제), 프리커밋 훅(저장 직전 자동 검사) (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

## 출력 원칙 — 성공은 조용히, 실패만 시끄럽게

> 테스트가 다 통과하면 아무 말도 하지 않고, 실패했을 때만 에이전트에게 알려야 한다. 통과한 테스트 결과 4,000줄을 다 보여주면 AI가 그걸 읽느라 정작 할 일을 잃어버린다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

이 현상이 [[concepts/context-decay|컨텍스트 부패]]다.

## 또 다른 용례 — 로깅 훅

훅의 대표 용도는 강제다. 다만 **AI 작업을 기록하는 로깅 훅**이라는 별개 용례도 있다.

어떤 프롬프트를 입력했고 AI가 어떤 파일을 읽고 어떤 명령을 실행했는지를 훅으로 자동 기록하면, AI 작업을 블랙박스로 두지 않게 된다. **재연성·디버깅 가능성·운영성**을 확보하는 것이다. 엉뚱한 파일이 수정됐을 때 "내 요청이 모호했는지"를 프롬프트 로그로, 문제 명령이 "언제 실행됐는지"를 툴 로그로 추적할 수 있다 (→ 생각등대 영상 `wa6ZoLlnB60` — 출처 페이지는 2026-07-12 커리어 위키로 이관됨).

## 다른 강제 장치와의 관계

하네스에서 규칙을 강제하는 층위는 여러 가지고, 훅은 그중 하나다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]).

| 장치 | 작동 시점 | 무엇을 막나 |
|---|---|---|
| 퍼미션(Permissions) | 실행 직전 | 위험한 명령 자체를 차단 |
| 훅 | 저장·종료 시점 | 검증을 자동 실행해 강제 |
| 도구 경계(tool boundaries) | 접근 시 | 범위와 권한을 미리 제한 |

- **퍼미션** — 파일 삭제 같은 위험한 명령의 실행 자체를 막는다. "CLAUDE.md=맥락, 퍼미션=어길 수 없게 만드는 것"이라는 대비다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]).
- **도구 경계** — AI가 접근할 수 있는 범위와 권한을 미리 제한한다. source 폴더는 읽기·쓰기, config 폴더는 읽기만, DB는 SELECT만 가능하고 DROP TABLE은 불가 같은 식이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

## 실제 사례 — OpenAI / 랭체인

OpenAI 엔지니어 3명이 5개월간 코드를 한 줄도 안 쓰고 제품을 배포한 사례가 있다. 그 성공 요인 넷 중 하나가 "CI 게이트"(코드 저장 시 자동 테스트)였고, 또 하나가 린트·테스트·훅으로 자동 검증하는 피드백 루프였다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]·[[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

랭체인(LangChain)은 모델을 바꾸지 않았다. 하네스(린트·테스트·훅 등)만 개선해 코딩 에이전트 벤치마크에서 30위권에서 5위권으로 25단계 올라갔다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

## 실전 적용 — "레벨 1" 세팅

가장 쉽게 시작할 두 가지가 있다. 프로젝트 지침이 담긴 `CLAUDE.md`/`AGENTS.md`, 그리고 저장 전 자동 검사하는 **프리커밋 훅**이다. 한두 시간이면 설정할 수 있다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

WAT 프레임워크의 도구(T) 예시로는 MCP로 PR 생성, **훅으로 커밋마다 테스트 자동 실행**이 꼽힌다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]] 참조).

> 다만 모델이 좋아지면 불필요해진 제약은 훅도 포함해서 빼야 한다. Anthropic도 Opus 4.6 출시 후 하네스를 간소화했다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]). [[concepts/harness-engineering|하네스 엔지니어링]]의 '하네스 다이어트' 긴장과 이어지는 대목이다.

## 인프라 영역 선례 — policy-as-code

[[entities/terraform|Terraform]] 도입의 성숙 단계(Govern)에서는 조직 표준을 [[entities/sentinel|Sentinel]]·OPA 정책 코드로 apply 이전에 자동 강제한다. 훅이 [[concepts/claude-md|CLAUDE.md]]의 '부탁'을 '강제'로 승격시키는 것과 같은 **규칙의 코드화·자동 강제** 계보다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

즉 훅은 이 오래된 인프라 사상을 에이전트 환경에 옮긴 장치로 볼 수 있다. 다만 이 연결 자체는 위키 차원의 해석이다.

## 함께 읽기

- [[concepts/harness-engineering|하네스 엔지니어링]] — 훅은 하네스의 기둥 중 '자동 강제'에 속한다
- [[concepts/claude-md|CLAUDE.md]] — 부탁과 강제의 대비
- [[concepts/verification-automation|검증 자동화]] — 훅이 강제하는 검증의 전체 그림
- [[concepts/context-decay|컨텍스트 부패]] — 출력 원칙이 필요한 이유
- [[concepts/mcp|MCP]] — 같은 하네스 층에 놓이는 도구 연결 규격
- [[entities/sentinel|Sentinel]] · [[entities/mitchell-hashimoto|미첼 하시모토]] — 인프라 영역의 policy-as-code 선례

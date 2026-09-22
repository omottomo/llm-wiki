---
title: Jev
type: entity
created: 2026-09-22
updated: 2026-09-22
sources: [typesafe-ai-docs, jevmanual-core, youtube-lx3YkhzM_04, youtube-GeM9URVnPV8, youtube-hRW-Gh5Y4MM]
aliases: [jev-1.13.0, jev-latest, System One model]
tags: [Jev, TypeSafe, 시스템원, 모델, 비용절감]
---

# Jev

## 한눈에 요약

- TypeSafe AI가 내놓은 첫 **시스템 원 모델**이자 이 회사의 대표 모델이다.
- 대화도 코드 작성도 하지 않는다. 내용과 질문을 받아 타입이 정해진 판단과 확률만 돌려준다.
- 입력 토큰에만 값을 매기고 출력은 무료라, 분류·라우팅처럼 판단만 필요한 구간의 단가가 아주 낮다.
- 영어가 1차 학습 언어이고 한국어를 포함한 CJK는 정확도가 떨어진다고 공식 문서가 직접 경고한다.

## 모델과 별칭

현재 버전은 `jev-1.13.0` 이다. 별칭 두 개가 모두 이 버전을 가리킨다 (2026-09 기준) (→ [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]).

| 이름 | 가리키는 것 | 뜻 |
|---|---|---|
| `jev-1.13.0` | 고정 버전 | 재현 가능한 평가에 쓴다 |
| `jev-latest` | `jev-1.13.0` | 최신 정식 릴리스. SDK 기본값 |
| `jev-preview` | `jev-1.13.0` | 프리뷰 포함 최신. 지금은 프리뷰 빌드가 없다 |

> 별칭은 움직이는 이름이다. 새 릴리스가 나오면 내 코드가 그대로여도 답과 확률이 달라질 수 있다. 임계값을 특정 버전에 맞춰 튜닝했다면 별칭 대신 버전을 고정하고, 응답의 `model` 필드를 로그에 남겨 어느 버전이 답했는지 추적하라고 양쪽 문서가 같이 권한다 (→ [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]·[[sources/jevmanual-core|#53 Jev 매뉴얼(비공식)]]).

## 가격·한도·컨텍스트

모두 2026-09 기준이며, 비공식 매뉴얼의 확인일은 2026-09-21이다 (→ [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]·[[sources/jevmanual-core|#53 Jev 매뉴얼(비공식)]]).

| 항목 | 값 |
|---|---|
| 가격 | 입력 100만 토큰당 $0.042 (10억 토큰당 $42). **출력 무료** |
| 레이트 리밋 | 초당 25만 토큰 / 분당 1,200요청 |
| 컨텍스트 | 요청 전체 64k 토큰 / `state` + 가장 긴 질문 하나 32k 토큰 |
| 입력 | 텍스트 전용. 문자열·JSON 객체·텍스트 배열 |

> 레이트 리밋은 고정값이 아니다. 문서 스스로 "매우 큰 수요를 감당하고 있어 위 한도가 **예고 없이 바뀔 수 있다**"고 경고한다. 안정된 한도는 상황이 정리된 뒤에나 제시할 수 있다는 말도 함께 적혀 있다 (→ [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]).

두 컨텍스트 제약은 **동시에** 걸린다. 짧은 질문을 여러 개 넣는다고 해서 지나치게 큰 state가 통과되지는 않는다 (→ [[sources/jevmanual-core|#53 Jev 매뉴얼(비공식)]]).

## 입력과 언어 지원

이미지·음성·영상은 받지 않는다. 텍스트가 아닌 입력은 미리 텍스트나 구조화된 필드로 바꿔서 `state`에 실어야 한다 (→ [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]).

언어는 짚고 넘어가야 할 대목이다. 영어가 1차 학습 언어이고 정확도도 거기서 가장 좋다. **CJK를 포함한 다른 언어도 처리는 되지만 동등하지 않다**고 문서가 명시한다. 비영어 작업에 기대기 전에 자기 데이터로 시험하고, 라우팅할 때 신뢰도를 특히 주의 깊게 보라고 권한다 (→ [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]).

한국어 문의 100건을 직접 돌려 본 실측에서는 비교 모델과 분류가 100건 중 89건 일치했고 긴급도 판단은 100건 모두 일치했다. 다만 그 영상도 "영어가 더 낫다는 의견이 많아 일부러 성능이 덜 나온다는 한국어로 먼저 해 봤다"고 전제를 달았다 (→ [[sources/youtube-GeM9URVnPV8|#55 Jev 200배 테스트]]).

## 어떻게 접근하나

- **웨이트리스트.** TypeSafe 사이트에서 등록하면 순차적으로 초대를 받고, 콘솔에서 API 키를 발급받는다 (→ [[sources/youtube-lx3YkhzM_04|#54 재브 뭐가 다른가]]·[[sources/youtube-hRW-Gh5Y4MM|#56 Jev+Aside 활용]]). 대기 시간이 얼마나 되는지는 자막 근거뿐이라 일반화하지 않는다.
- **직접 호출.** 공식 SDK(Python·JavaScript)나 HTTP API로 `POST /v1/systemone` 을 부른다 (→ [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]).
- **게이트웨이 경유.** OpenRouter, [[entities/vercel|Vercel]] AI Gateway, Cloudflare Workers AI를 통해서도 쓸 수 있다 (→ [[sources/jevmanual-core|#53 Jev 매뉴얼(비공식)]]). 자막 기준으로도 같은 경로가 언급된다 (→ [[sources/youtube-lx3YkhzM_04|#54 재브 뭐가 다른가]]).
- **에이전트 스킬.** 코딩 에이전트가 Jev 연동 코드를 제대로 짜도록 돕는 공식 스킬이 따로 있다 (→ [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]).

> 게이트웨이마다 모델 식별자·요금·쿼터·데이터 보존 정책이 다르다. 직접 API의 모델 ID를 아무 제공자에나 붙여 넣지 말라고 비공식 매뉴얼이 경고한다 (→ [[sources/jevmanual-core|#53 Jev 매뉴얼(비공식)]]). 실측에서도 게이트웨이를 한 번 거치면 같은 작업이 2.1초에서 3.7초로 늘었다 (→ [[sources/youtube-GeM9URVnPV8|#55 Jev 200배 테스트]]).

## 이 위키에서의 등장

- **[[concepts/system-one-model|시스템 원 모델]]의 첫 구현체**로 등장한다. "LLM이 아니라면 대체 무엇인가"라는 물음의 실물이 이 모델이다.
- **[[concepts/jev-primitives|Jev 프리미티브]]** — Choice·Score·Noul 질문과 응답 필드를 실제로 처리하는 주체다.
- **[[analysis/jev-vs-llm|Jev vs LLM vs 코드]]** — "200배·400배" 홍보 문구와 실측값을 나란히 놓고 검증하는 대상이다.
- **코딩 에이전트의 모델이 아니다.** Claude Code·Cursor·Codex 같은 도구의 LLM을 Jev로 갈아 끼우는 설정 같은 건 없다고 공식 문서가 못 박는다 (→ [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]). [[entities/claude-code|Claude Code]] 계열 도구와는 대체재가 아니라 병행 관계다.

## 함께 읽기

- [[concepts/system-one-model|시스템 원 모델]] — 이 모델이 속한 갈래의 정의·훈련 경로·공개 범위
- [[concepts/jev-primitives|Jev 프리미티브]] — 실제로 무엇을 물을 수 있는지
- [[entities/typesafe-ai|TypeSafe AI]] — 만든 회사
- [[analysis/jev-vs-llm|Jev vs LLM vs 코드]] — 언제 쓰고 언제 쓰지 않을지

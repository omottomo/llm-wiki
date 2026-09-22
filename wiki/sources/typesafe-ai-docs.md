---
title: TypeSafe 공식 문서 — Jev·System One 코어 17페이지
label: "#52 TypeSafe 공식 문서"
type: source
credibility: high
volatility: hot
created: 2026-09-22
updated: 2026-09-22
sources: [typesafe-ai-docs]
tags: [Jev, TypeSafe, 시스템원, 구조화출력, 보정, 신뢰도, 공식문서]
---

# TypeSafe 공식 문서 — Jev·System One 코어 17페이지

## 한 줄 요약

[[entities/typesafe-ai|TypeSafe AI]]가 직접 펴내는 1차 문서로, [[entities/jev|Jev]]라는 [[concepts/system-one-model|시스템 원 모델]]이 무엇이고 [[concepts/jev-primitives|Jev 프리미티브]]를 어떻게 쓰는지, 그리고 이 모델이 어디서 틀리는지까지 적어 둔 묶음이다.

## 핵심 내용

- **System One**은 "소프트웨어가 바로 쓸 수 있는 빠르고 구조적인 판단"을 내놓는 모델 갈래이고, Jev가 그 첫 모델이자 대표 모델이다. 이름은 대니얼 카너먼의 『Thinking, Fast and Slow』의 시스템 1(빠르고 직관적인 사고)에서 왔다.
- LLM과 달리 **텍스트를 생성하지 않는다**. 자연어 입력은 똑같이 이해하되, 타입이 정해진 값과 확률 분포를 돌려준다. 파싱이 필요 없다.
- 질문 타입은 **Choice·Score·Noul** 셋이다. 한 요청에 섞어 보낼 수 있고, 모든 질문은 같은 `state`에 대해 **병렬·독립**으로 평가된다. 질문을 늘려도 응답 시간은 거의 그대로다.
- **보정(calibration)**이 훈련 목표다. 문서는 사전학습 언어모델에서 갈라지는 세 갈래를 RLHF·RLVR·**RLCD**(reinforcement learning for calibrated decisions)로 정리하고, TypeSafe의 경로가 RLCD라고 밝힌다.
- **`jev-1.13.0`** 이 현재 모델이고 `jev-latest`·`jev-preview` 별칭이 모두 이 버전을 가리킨다. 입력 100만 토큰당 $0.042, 출력 무료, 컨텍스트 64k(요청 전체)/32k(state + 가장 긴 질문 하나) (2026-09 기준).
- 문서 스스로 **9가지 실패 모드**를 공개한다: 문자 그대로 읽기, 수·계산, 날짜·시각 비교, 간접 참조, 쓸데없이 큰 state, 적대적 입력, 모순된 지시, 구조적 불변식, 생성.
- 영어가 1차 학습 언어이고 **CJK를 포함한 다른 언어는 정확도가 떨어진다**고 못 박는다. 텍스트 전용이며 이미지·음성·영상 입력은 받지 않는다.

## 주요 주장 / 데이터

- 가격·한도 (2026-09 기준): 입력 10억 토큰당 $42(= 100만 토큰당 $0.042), 출력 무료. 레이트 리밋 초당 25만 토큰 / 분당 1,200요청. 다만 문서는 "수요가 매우 커서 **예고 없이 바뀔 수 있다**"고 경고한다.
- 엔드포인트는 `POST https://api.typesafe.ai/v1/systemone` 하나이고, `model` 필드가 어느 모델이 처리할지를 고른다. 응답에는 `model`·`answers`·`usage`(입력·출력 토큰)가 담긴다.
- 응답 필드: Choice는 `choice`+`probabilities`+`confidence`, Score는 `score`(확률가중 값)+`legend`+`probabilities`+`confidence`, Noul은 `noul`(0~1) 하나뿐이고 **신뢰도 필드가 없다**.
- 보정의 정의: "확률 0.8이 붙은 예측들은 약 80% 맞아야 한다." 문서는 곧바로 이것이 **예측 집단(group)에 대한 성질이지 개별 답의 정확성 보증이 아니다**라고 덧붙인다.
- 신뢰도(confidence)는 확률 분포에서 파생된 통계다. 분포가 한 곳에 몰릴수록 1에 가깝고 평평할수록 0에 가깝다. 문서는 높음/중간/낮음 3구간으로 나눠 자동 실행·확인 요청·사람에게 넘김으로 분기하는 패턴을 권한다.
- 임계값은 하나의 숫자가 아니다. 같은 시스템 안에서도 잔액 조회 같은 되돌릴 수 있는 동작과 송금 승인 같은 되돌릴 수 없는 동작은 다른 문턱을 써야 한다는 예제 코드를 싣는다.
- "Machine Native Intelligence" — 대규모 자동화는 99%가 기계-기계 상호작용이 될 것이므로 사람이 읽기 좋은 응답이 아니라 소프트웨어 안에서 예측 가능하게 움직이는 출력이 설계 목표라는 주장이다.
- RLHF를 함께 고안한 **Diogo Almeida**가 TypeSafe 공동창업자라고 적는다.
- 문서는 Jev가 코딩 에이전트의 LLM을 대체하는 모델이 **아니라고** 분명히 선을 긋는다. Claude Code·Cursor·Codex 같은 도구의 모델을 Jev로 바꾸는 설정 같은 건 없다.

## 기존 위키와의 연결

- 강화: [[concepts/llm-basics|LLM 기초]]가 설명하는 "다음 단어 확률 예측"과 RLHF 사후학습 서사를 1차 출처로 보강하고, 거기에 RLVR·RLCD라는 두 갈래를 더한다.
- 모순: [[sources/youtube-GeM9URVnPV8|#55 Jev 200배 테스트]]가 전하는 "환각 0%" 주장과 충돌한다. 이 문서는 그런 보증을 어디에서도 하지 않고, 보정은 집단 단위 성질이며 9가지 실패 모드가 있다고 적는다. 양쪽을 모두 보존하고 [[analysis/jev-vs-llm|Jev vs LLM vs 코드]]에 모순으로 표시했다.
- 신규: [[concepts/system-one-model|시스템 원 모델]], [[concepts/jev-primitives|Jev 프리미티브]], [[entities/jev|Jev]], [[entities/typesafe-ai|TypeSafe AI]] 페이지가 이 문서에서 나왔다.

## 출처 정보

- raw: raw/typesafe-ai-docs.md
- 저자/발행처: TypeSafe AI (Jev 개발사, 1차 출처)
- 수집일: 2026-09-22
- URL: https://docs.typesafe.ai/llms.txt
- 범위: docs.typesafe.ai 가 llms.txt 로 공개하는 코어 17페이지 — introduction, quickstart, coding-agents, concepts/system-one, concepts/state, primitives(+choice·score·noul·advanced), machine-learning-primer, confidence, how-to-build-with-system-one, models, api, model-jaggedness/jev-1.13, patterns/confidence-routing. 쿡북·SDK 레퍼런스·법무 페이지는 제외.
- 비고: 변환 없이 원문 마크다운 그대로 수집. 제품이 유동적이라 volatility 는 hot — 특히 레이트 리밋은 문서 자체가 예고 없이 바뀐다고 경고한다.

---
title: Jev 매뉴얼 — 비공식 서드파티 가이드 19페이지
label: "#53 Jev 매뉴얼(비공식)"
type: source
credibility: medium
volatility: hot
created: 2026-09-22
updated: 2026-09-22
sources: [jevmanual-core]
tags: [Jev, TypeSafe, 시스템원, 신뢰도, 비공식문서]
---

# Jev 매뉴얼 — 비공식 서드파티 가이드 19페이지

## 한 줄 요약

[[entities/typesafe-ai|TypeSafe AI]]와 무관한 제3자가 만든 [[entities/jev|Jev]] 개발자 가이드로, 공식 문서를 출처로 달고 다시 쓰되 **어디까지가 확인된 사실이고 어디부터가 교육용 예시인지**를 페이지마다 라벨로 구분해 둔 점이 특징이다.

## 핵심 내용

- 사이트 스스로 "TypeSafe AI가 소유·운영·후원·보증하지 않는 독립 자료"라고 밝힌다. 각 페이지 하단에 `docs.typesafe.ai` 의 어느 페이지를 근거로 썼는지와 확인 날짜(2026-09-21)를 적는다.
- **"System One"은 제품·인터페이스 용어이지 모델 내부 구조의 공개 명세가 아니다**라고 명시한다. 그래서 이 매뉴얼은 관측 가능한 API 동작만 설명하고 훈련 아키텍처는 추측하지 않는다고 선언한다.
- 같은 맥락에서 "TypeSafe가 공개한 정보만으로는 내부 아키텍처를 독립적으로 재구성할 수 없다"고 적는다.
- 공식 문서가 적은 9가지 실패 모드를 나쁜 예/왜 실패하나/대신 이렇게 하라/좋은 예 네 칸으로 다시 정리한다. 서두에 "**타입이 맞는 답도 틀린 답일 수 있다**"를 둔다.
- 라벨 체계: `Official`(공식 문서에 근거한 사실 서술), `Provider`(게이트웨이·프레임워크 쪽 인터페이스), `Example`(교육용 아키텍처·임계값), `Independent`(이 사이트의 편집 정보). `Official` 라벨은 "이 사이트가 공식"이라는 뜻이 아니라고 따로 못 박는다.
- 출처가 충돌할 때의 우선순위를 규정으로 적어 둔다: 직접 API는 공식 TypeSafe 문서, 게이트웨이 동작은 해당 제공자 문서, 프레임워크 어댑터는 그 프레임워크 문서 순이다.
- 벤더의 성능 주장은 "TypeSafe reports" 같은 귀속 표기를 달아야 하며, 이 사이트의 독립 벤치마크로 제시하지 않는다고 규정한다.

## 주요 주장 / 데이터

- 현재 모델·가격·한도를 공식 문서와 같은 값으로 옮긴다: `jev-1.13.0`, `jev-latest`·`jev-preview` 모두 이 버전, 직접 입력 100만 토큰당 $0.042, 출력 무료, 요청 예산 64,000 토큰 / state + 가장 긴 질문 32,000 토큰 (2026-09 기준, 확인일 2026-09-21).
- 게이트웨이·프레임워크 경유 경로를 별도 출처 목록으로 든다: OpenRouter의 System One 호환 엔드포인트, Vercel AI Gateway, Cloudflare Workers AI, LangChain 연동. **제공자마다 식별자·요금·쿼터·보존 정책이 다르므로 직접 API의 모델 ID를 그대로 붙여 쓰지 말라**고 경고한다.
- 확률과 신뢰도를 구분해 표로 정리한다. Choice는 선택지별 확률 + 별도 신뢰도, Score는 레벨별 확률 + 별도 신뢰도, Noul은 참일 확률만 있고 **신뢰도 없음**이다.
- 임계값에 대해 "0.8은 예시일 뿐"이라고 적고, 라벨링된 자체 데이터로 검증하는 절차(대표 입력 수집 → 모델 버전·state·지시문 고정 → 라벨과 대조 → 임계값 스윕 → 검토 인력 여력에 맞춰 선택)를 단계로 제시한다.
- 별칭은 움직이는 이름이라 `jev-latest`에 맞춰 튜닝한 임계값이 조용히 깨질 수 있으니, 운영에서는 버전을 고정하고 응답의 `model` 필드를 로그에 남기라고 권한다.
- 비용 계산에서 "공유 state는 한 번만 실어 보내므로, 독립적인 질문들을 한 요청에 묶으면 가장 큰 입력을 반복하지 않아도 된다"는 점을 예산 근거로 든다(state 700토큰 + 질문 3개 × 120토큰 ≈ 1,060토큰).

## 기존 위키와의 연결

- 강화: [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]]의 사양·실패 모드 서술을 제3자 관점에서 중복 확인해 준다. 특히 "타입이 맞는 답이 곧 맞는 답은 아니다"는 경고는 1차 문서의 보정 설명과 같은 방향이다.
- 모순: 직접 모순 없음. 다만 **경계선을 더 세게 긋는다** — 공식 문서가 System One을 모델 갈래처럼 서술하는 데 비해, 이 매뉴얼은 그것이 제품·인터페이스 용어일 뿐 내부 명세가 아니라고 선을 긋는다. 두 서술을 모두 [[concepts/system-one-model|시스템 원 모델]]에 남겼다.
- 신규: 게이트웨이 경유 접근 경로(OpenRouter·Vercel·Cloudflare)와 "제공자마다 식별자가 다르다"는 주의사항이 여기서 나왔다. [[entities/jev|Jev]]에 기록했다.

## 출처 정보

- raw: raw/jevmanual-core.md
- 저자/발행처: jevmanual.com (비공식 서드파티 가이드, 사이트 자체 표기 "Independent")
- 수집일: 2026-09-22 (사이트 표기 확인일 2026-09-21)
- URL: https://jevmanual.com/manual/
- 범위: 코어 19페이지 — what-is-jev, how-jev-works, manual(api·state·primitives+choice·score·noul·confidence·models·limitations·multiple-questions·pricing), compare/jev-vs-llm, faq, sources, about, patterns, use-cases.
- 비고: 사이트 크롬(검색창·애널리틱스 동의 배너·피드백 문구)이 본문에 섞여 남아 있다. credibility 를 medium 으로 둔 이유는 1차 출처가 아니기 때문이며, 출처 표기와 확인 날짜를 성실히 다는 점은 감안했다.

---
title: 주제 관문 — Jev와 판단 전용 AI 모델
type: overview
created: 2026-09-22
updated: 2026-09-22
sources: []
tags: [관문, Jev, TypeSafe, 시스템원]
---

# 주제 관문 — Jev와 판단 전용 AI 모델

> 글을 만들지 않고 판단만 돌려주는 모델 계열을 모아 둔 관문이다. TypeSafe AI가 System One이라 부르는 부류이고, 지금 공개된 모델은 Jev 하나다.

## 여기서부터
1. [[concepts/system-one-model|시스템 원 모델]] — LLM이 아니면 대체 무엇인지
2. [[concepts/jev-primitives|Jev 프리미티브]] — Choice·Score·Noul 세 질문 타입
3. [[analysis/jev-vs-llm|Jev vs LLM vs 코드]] — 언제 쓰고 언제 쓰지 말아야 하는지

## 개념
- [[concepts/system-one-model|시스템 원 모델]] — LLM이 아닌 판단 전용 모델 계열. RLHF·RLVR·**RLCD** 갈래와 보정 확률의 뜻
- [[concepts/jev-primitives|Jev 프리미티브]] — Choice·Score·Noul 질문 타입, 신뢰도 임계값 3구간, 공표된 실패 모드 9가지

## 엔티티
- [[entities/jev|Jev]] — TypeSafe AI의 첫 시스템 원 모델. `jev-1.13.0`, 입력 100만 토큰당 $0.042·출력 무료
- [[entities/typesafe-ai|TypeSafe AI]] — Jev 개발사. 기계가 바로 쓰는 판단(Machine Native Intelligence)을 내세운다

## 분석
- [[analysis/jev-vs-llm|Jev vs LLM vs 코드]] — 세 도구의 경계, 실측 대 홍보 수치 검증, "환각 0%" 모순 플래그

## 출처
- [[sources/typesafe-ai-docs|#52 TypeSafe 공식 문서]] — 2026-09-22 흡수, docs.typesafe.ai 17페이지. Jev·System One의 1차 출처(RLCD·보정·API·실패 모드 9가지)
- [[sources/jevmanual-core|#53 Jev 매뉴얼(비공식)]] — 2026-09-22 흡수, jevmanual.com 19페이지. 서드파티 가이드. "내부 구조는 공개 명세가 아니다"라는 경계선 제시
- [[sources/youtube-lx3YkhzM_04|#54 재브 뭐가 다른가]] — 2026-09-22 흡수, 코드깎는노인. LLM과의 응답 형태 차이를 그림으로 설명, Doom 실시간 판단 사례
- [[sources/youtube-GeM9URVnPV8|#55 Jev 200배 테스트]] — 2026-09-22 흡수, 코드팩토리. 한국어 100건 분류 실측(속도 6~8배·비용 76배·판정 89/100 일치)
- [[sources/youtube-hRW-Gh5Y4MM|#56 Jev+Aside 활용]] — 2026-09-22 흡수, 배움의 달인. 발급 절차와 활용 사례. 수치는 대부분 전언이라 credibility low

## 함께 보기
- [[concepts/llm-basics|LLM 기초]] — 비교 대상이 되는 생성형 모델의 기본
- [[moc/ai-coding-agents|AI 코딩 에이전트]] — 파이프라인 앞단에 판단을 끼우는 자리

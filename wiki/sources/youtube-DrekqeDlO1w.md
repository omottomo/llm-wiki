---
title: "#14 공식 하네스 문서를 100번 읽은 느낌이 들게 해드립니다"
label: "#14 하네스 문서 100번"
type: source
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-DrekqeDlO1w]
tags: [하네스엔지니어링, 미첼하시모토, 말과마구, 컨텍스트부패, 개발자역할변화]
---

## 한 줄 요약
테크 기업 아티클 15편 이상을 종합해, "야생말에 마구를 씌운다"는 비유로 [[concepts/harness-engineering|하네스 엔지니어링]]의 기원·정의·3기둥·미래 전망까지 한 번에 정리한 비전공자 친화 개론 영상.

## 핵심 내용
- 용어 기원: [[entities/mitchell-hashimoto|미첼 하시모토]]가 2026년 2월 처음 명명. AI 코딩 에이전트가 같은 실수를 반복하는 경험에서 출발 — "실수가 다시는 반복되지 않도록 엔지니어링하는 것".
- "야생말 → 경마장 말" 비유: 모델(Claude/GPT/Gemini)은 야생말, 하네스(마구)는 힘을 억누르는 게 아니라 올바른 방향으로 집중시키는 장치. 모델이 아닌 것은 전부 하네스 — [[concepts/claude-md|CLAUDE.md]], [[concepts/mcp|MCP]], [[concepts/skills|스킬]], [[concepts/hooks|훅]] 등.
- "이미 하네스를 쓰고 있다": LLM은 텍스트→텍스트 함수일 뿐이며, 채팅창이 이전 메시지를 모아 매번 다시 전달하는 그 루프 자체가 하네스.
- 발전 흐름: [[concepts/prompt-engineering|프롬프트 엔지니어링]] → [[concepts/context-engineering|컨텍스트 엔지니어링]] → [[concepts/mcp|MCP]]/[[concepts/skills|스킬]](스킬 수백 개로 오히려 혼란) → [[concepts/harness-engineering|하네스 엔지니어링]](환경 자체를 설계).
- 하네스가 푸는 두 문제: ① [[concepts/context-decay|컨텍스트 부패]](Anthropic이 Claude Opus로 claude.ai 클론 실험 시 절반만 구현·조기 종료) ② 규칙·울타리 문제(정보를 알면서 DB 테이블 삭제 등). 각각 [[concepts/claude-md|CLAUDE.md]](매 세션 최우선 로드)와 [[concepts/hooks|훅]](저장 직전 자동 검사·차단)로 해결.

## 주요 주장 / 데이터
- [[entities/openai|OpenAI]] 사례: 엔지니어 3명이 5개월간 코드 한 줄 안 씀. 한 일은 agents.md + CI 게이트 + 도구 경계 + 피드백 루프 — "사람이 시스템을 만들고 에이전트는 그 안에서 수행만 한다".
- LangChain(자막상 "랭체인") 코딩 에이전트 벤치마크: 모델을 바꾸지 않고 하네스만 개선해 30위권→5위권으로 25단계 상승 → "성능을 좌우하는 건 모델 지능이 아니라 하네스".
- 3기둥: ① 컨텍스트 파일(agents.md/[[concepts/claude-md|CLAUDE.md]] — "1,000페이지 설명서가 아니라 지도를 줘라", 60줄 이하 보편 규칙만) ② 자동 강제 시스템(린터·프리커밋 훅·자동 교정 루프, "성공은 조용히 실패만 시끄럽게") ③ 가비지 컬렉션(나쁜 코드 주기적 자동 정리).
- 미래 전망: 리처드 서튼(강화학습 창시자)은 "모델이 똑똑해질수록 하네스는 더 단순해져야 한다"고 말함. 차드 파울러(자막상 "차드 파울라", 추정)는 역할 변화를 "엄밀함의 재배치"로 표현 ([[concepts/developer-role-change|개발자 역할의 변화]]). 하네스가 미래의 서비스 템플릿이 되고 일부는 모델에 흡수될 것.

## 기존 위키와의 연결
- 강화: [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]의 정의·3~4기둥 구조·OpenAI 3인 사례·[[entities/mitchell-hashimoto|미첼 하시모토]] 창시 설을 강화. "말과 마구" 비유의 핵심 소스. LangChain 25단계 상승은 "모델보다 하네스" 주장의 정량 근거.
- 모순: "모델 똑똑할수록 하네스 단순화"(서튼)는 [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]의 "하네스를 점점 쌓아라"와 긴장 → [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]와 함께 [[concepts/harness-engineering|하네스 엔지니어링]] '하네스 다이어트'로 기록.
- 신규: 야생말→경마장 비유, "채팅창=하네스 루프" 직관, LangChain 벤치마크 25단계 상승, 리처드 서튼/차드 파울러 인용, "하네스=서비스 템플릿" 미래 전망.

## 출처 정보
- raw: raw/youtube-DrekqeDlO1w.md
- URL: https://www.youtube.com/watch?v=DrekqeDlO1w
- 채널: castlestudio (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3 (순번 14)
- transcript_lang: ko (자동생성 자막 — "하늘스/한네스/한스" 등 하네스 오인식 다수, 인명은 추정 표기)

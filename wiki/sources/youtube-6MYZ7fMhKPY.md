---
title: "#21 하네스 엔지니어링: 바이브 코딩에서 에이전틱 코딩으로"
label: "#21 바이브에서 에이전틱으로"
type: source
credibility: medium
volatility: cold
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-6MYZ7fMhKPY]
tags: [하네스엔지니어링, 에이전틱코딩, 바이브코딩, 검증자동화, 카파시]
---

## 한 줄 요약
바이브 코딩(바닥 올리기)에서 에이전틱/하네스 엔지니어링(천장 올리기)으로 넘어가는 전환을 다루며, "부탁(프롬프트)"이 아니라 "잘할 수밖에 없는 구조(하네스)"를 만드는 것이 핵심이라고 주장한다.

## 핵심 내용
- 카파시가 만든 "바이브 코딩"은 모든 사람의 **바닥**을 올렸고, 이제 카파시는 에이전틱 엔지니어링이 **천장**을 올린다고 말한다. (자막상 "카파시"=[[entities/andrej-karpathy|안드레이 카파시]])
- 연도별 서사: 2025=에이전트의 해(Claude Code·Cursor·Codex 등장), 2026=하네스의 해, 2027=에이전트가 스스로 하네스를 만드는 해(예측).
- 소프트웨어 1.0(직접 코딩) → 2.0(데이터로 AI 학습) → 3.0(프롬프트가 곧 프로그래밍)으로 진화. 코드 생성은 쉬워졌고 진짜 문제는 "검증".
- [[concepts/prompt-engineering|프롬프트 엔지니어링]]은 "잘 해 줘"라고 부탁하는 것, [[concepts/harness-engineering|하네스 엔지니어링]]은 "잘 할 수밖에 없는 구조"를 만드는 것 — 부탁 vs 구조의 차이가 핵심.
- 도구는 적을수록 좋다(선택지가 많으면 결정 비용↑). 안 쓰는 [[concepts/skills|스킬]]은 지우고 핵심만 강화.
- [[concepts/verification-automation|검증 자동화]]: 테스트 자동화 + 에이전트가 결과를 검토(Claude Code+Codex 조합 시 성능↑) → 사람은 최종 판단만.
- 프로젝트 전체(폴더 구조·파일명·코드 스타일·[[concepts/claude-md|CLAUDE.md]]·[[concepts/mcp|MCP]]·[[concepts/skills|스킬]])가 곧 프롬프트. 좋은 하네스는 프로젝트 전체를 하나의 거대한 프롬프트로 만드는 것.

## 주요 주장 / 데이터
- (인용) OpenAI 엔지니어가 "하루 10억 토큰을 쓰면서 코드를 한 줄도 안 친다"고 발언, IBM 엔지니어는 컨퍼런스에서 "2026년은 하네스의 해"라고 선언 (자막 인용, 추정).
- 카파시 인용: "생각은 아웃소싱할 수 있지만 이해는 아웃소싱할 수 없다" — 실행·분석·리뷰는 AI에게, 이해(구조·필요성 판단)는 인간이 (→ [[entities/andrej-karpathy|안드레이 카파시]]).
- 결제 환불·수수료 같은 구조적 판단은 코드가 아닌 설계 문제로 여전히 인간의 영역.

## 기존 위키와의 연결
- 강화: [[concepts/harness-engineering|하네스 엔지니어링]]의 "부탁이 아니라 구조" 정의와 [[concepts/agentic-coding|에이전틱 코딩]]에서 [[concepts/harness-engineering|하네스 엔지니어링]]로의 진화 서사를 강화. [[concepts/verification-automation|검증 자동화]]·[[concepts/multi-model-workflow|멀티 모델 워크플로우]](Claude Code+Codex)도 강화.
- 강화: [[entities/andrej-karpathy|안드레이 카파시]]의 "바닥/천장", "이해는 아웃소싱 불가" 발언. (자막상 "카파시"로 표기)
- 신규: 바이브 코딩→에이전틱 코딩→2027 자율 하네스로 이어지는 연도별 진화 프레임을 명시적으로 도입.

## 출처 정보
- raw: raw/youtube-6MYZ7fMhKPY.md
- URL: https://www.youtube.com/watch?v=6MYZ7fMhKPY
- 채널: Jay Choi | 인디해커 라이프 (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3 (순번 21)
- 자막: 한국어 자동생성 (오탈자·인명 오인식 가능)

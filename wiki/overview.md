---
title: 도메인 개요 — Claude Code & 하네스 엔지니어링
type: overview
created: 2026-06-23
updated: 2026-06-28
sources: [youtube-BssPGKsP60s, youtube-6gvnDSAcZww, youtube-6cr4PeilKJk, youtube-6MYZ7fMhKPY, youtube-z-3BRkxQ5GM, youtube-wa6ZoLlnB60, youtube-Vq9UU92R4wY]
tags: [개요, 하네스엔지니어링, 클로드코드, AI에이전트코딩]
---

# 도메인 개요 (Overview)

이 위키는 한 유튜브 재생목록(`PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3`, 영상 25편)을 정리한 것이다.
주제는 **Claude Code를 중심으로 한 AI 에이전트 코딩**, 그리고 그것을 제대로 다루기 위한 **환경 설계(하네스 엔지니어링)**이다.
대부분 한국어 채널의 영상이며, 자동생성 자막을 원본으로 흡수했다(인명·수치는 자막 오인식 가능성이 있어 본문에 교정·추정 표기를 남겼다).

## 핵심 서사: AI 활용의 4단계 진화

이 재생목록을 관통하는 하나의 줄기는 "사람이 AI를 다루는 방식"의 진화다.

1. **[[concepts/prompt-engineering]]** (2024, "뭘 물어볼까") — 한 번의 질문을 잘 던지는 기술. 천장이 낮고, AI에게 "부탁"하는 단계.
2. **[[concepts/context-engineering]]** (2025, "뭘 보여줄까") — 무엇을 컨텍스트로 제공할지 설계. [[concepts/claude-md]], 레이지 로딩, 메모리 관리가 여기 속한다.
3. **[[concepts/harness-engineering]]** (2026, "환경 전체를 어떻게 설계할까") — 컨텍스트 파일·[[concepts/mcp]]·[[concepts/skills]]·[[concepts/hooks]]를 통합해, 에이전트가 잘할 수밖에 없는 환경을 만드는 단계. "부탁"이 아니라 "강제". 이 위키의 **중심 개념**이다.
4. **[[concepts/loop-engineering]]** (최신, "반복을 자동화") — 첫 프롬프트 이후 목표 달성까지의 반복을 사람이 아니라 AI가 알아서 돌리게 하는 단계. [[concepts/dynamic-workflow]]가 그 구현체다.

이 진화는 곧 **[[concepts/developer-role-change]]** — 개발자가 "코드를 쓰는 사람(선수)"에서 "AI가 일할 환경을 설계하고 판단하는 사람(감독)"으로 이동한다는 메시지로 수렴한다. [[concepts/agentic-coding]](바이브 코딩 → 에이전틱 코딩)이 그 실천 양상이다.

## 하네스 엔지니어링의 골격

여러 영상이 공통으로 제시하는 하네스의 기둥:
- **컨텍스트 파일** ([[concepts/claude-md]]): 매 세션 자동 재로드되는 규칙. 단, "짧고 검증 가능하게"가 핵심.
- **자동 강제** ([[concepts/hooks]], 린터, 프리커밋): 프롬프트는 부탁이지만 훅·권한은 강제다.
- **자동 교정 루프** + **가비지 컬렉션**(주기적 코드 정리).
- **검증 분리** ([[concepts/verification-automation]]): 생성 AI와 검증 AI를 분리해 자기 평가 편향을 깬다.

근거로 자주 인용되는 일화 — 같은 모델로도 하네스 유무에 따라 **$9짜리 미완성 앱 vs $200짜리 완성 앱**(→ [[sources/youtube-6cr4PeilKJk]]), OpenAI 엔지니어가 코드를 한 줄도 안 쓰고 5개월간 제품 배포(→ [[sources/youtube-BssPGKsP60s]], [[sources/youtube-6gvnDSAcZww]]) 등.

## 도구·생태계 지도

- 중심 도구: [[entities/claude-code]] ([[entities/anthropic]]). 멀티 인스턴스 협업은 [[concepts/subagents-agent-teams]].
- 경쟁/보완 모델: [[entities/codex]]([[entities/openai]]), [[entities/cursor]] — 단일 모델 의존의 위험과 교차 검증은 [[concepts/multi-model-workflow]].
- 지식 주입: [[concepts/skills]], [[entities/skills-sh]]([[entities/vercel]]).
- 온디바이스: [[concepts/on-device-ai]], [[entities/google-gemma]].
- 기초 이론: [[concepts/llm-basics]].
- 핵심 인물: [[entities/andrej-karpathy]](Karpathy 가이드라인/65줄 CLAUDE.md), [[entities/boris-cherny]](Claude Code 창시자), [[entities/mitchell-hashimoto]](하네스 용어), [[entities/peter-steinberger]].

## 주요 긴장점(미해결 논쟁)

1. **CLAUDE.md를 쓸 것인가 말 것인가** — "지워라"(→ [[sources/youtube-c7_ANA1NiS0]]) vs "품질 3배"(→ [[sources/youtube-cZ8_Dkk_Ce0]], [[sources/youtube-gol5jv4wcfs]]). 정리: [[concepts/claude-md]].
2. **하네스를 쌓을 것인가 뺄 것인가** — 축적론 vs "낡은 하네스는 제품 내장 기능과 중복되니 빼라"(하네스 다이어트, → [[sources/youtube-fInMcawbKng]]). 정리: [[concepts/harness-engineering]].
3. **단일 도구로 충분한가** — "Claude Code만 쓰면 망한다"(→ [[sources/youtube-f0hcByvsyjU]]) vs Boris의 "거의 바닐라 세팅"(→ [[sources/youtube-hXlB1QstQ-Y]]). 정리: [[concepts/multi-model-workflow]].

## 응용 관점: 커리어·이력서

하네스/검증/역할분리 개념은 기술 담론을 넘어 **취업·이직** 전략으로도 번역된다. 두 갈래가 있다.
- **이력서 표현**(좁은 각도): "AI를 써봤다"는 더 이상 변별점이 아니며, "AI가 안전하게 일할 환경(하네스)을 설계해봤다"가 변별점이 된다 — ①계획-승인 게이트, ②리서처/플래너/리뷰어 역할 분리, ③프롬프트·로깅 훅이 곧 이력서 한 줄이 된다 (→ [[sources/youtube-wa6ZoLlnB60]], 정리: [[concepts/ai-resume-writing]]).
- **취업 준비 전반**(넓은 각도, 신입·취준): AI 활용은 이제 기본 전제이고, 합격은 ①CS 기본기(AI 코드 품질 판단력) ②AI 활용 ③문제 해결력의 숫자 증명 ④서비스 운영 경험으로 갈린다 (→ [[sources/youtube-Vq9UU92R4wY]], 정리: [[concepts/developer-job-strategy]]).
- **경력 전환/이직**(경력자): "물경력"이 쌓일 때 기존 경력을 부정하지 않고 ①실무 안 AI 흔적 ②목표 스택으로 개인 서비스 배포·운영 ③부하 테스트(TPS·병목)로 차이를 메운다 (→ [[sources/youtube-SsHGSf_nzrI]], 정리: [[concepts/career-pivot-strategy]]).

셋 다 [[concepts/developer-role-change]]의 "선수→감독" 서사를 채용 현실로 구체화한 것이다.

> **출처 범위 메모**: 위 25편은 재생목록 `PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3` 기반이고, [[sources/youtube-wa6ZoLlnB60]]·[[sources/youtube-Vq9UU92R4wY]](2026-06-28 흡수)는 다른 재생목록 `PLUGinkN1Rwv5E7cnlf8kpTL95F0Cw2Ywm`(취업/커리어 모음, 여러 채널)에서 추가됐다.

전체 카탈로그는 [[index]]를 참고.

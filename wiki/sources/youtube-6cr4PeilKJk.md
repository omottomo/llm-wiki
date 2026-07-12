---
title: "#13 하네스 엔지니어링, 9달러 vs 200달러의 비밀 (Claude Code)"
type: source
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-6cr4PeilKJk]
tags: [하네스엔지니어링, ClaudeCode, 미첼하시모토, 검증자동화, 컨텍스트부패]
---

## 한 줄 요약
같은 모델이라도 환경 설계만으로 결과가 갈린다는 Anthropic의 "9달러 실패 앱 vs 200달러 완성 앱" 실험을 근거로, [[entities/claude-code]] 위에서 [[concepts/harness-engineering]]을 6단계로 구성하는 법을 설명한 영상.

## 핵심 내용
- 하네스 엔지니어링은 "AI한테 뭘 해라"가 아니라 "어떤 환경에서 일해라"를 설계하는 것. 새로운 기술이 아니라 이미 해오던 행위에 이름이 붙은 것 (→ [[sources/youtube-6cr4PeilKJk]]).
- [[entities/claude-code]] 자체가 하네스: 공식 문서에 "Claude Code는 Claude 모델을 감싸는 하네스"라고 표기. 단 클로드 코드는 빈 틀일 뿐, 규칙·제한·검증을 채우는 건 사용자 몫 (→ [[sources/youtube-6cr4PeilKJk]]).
- 용어 창시자는 [[entities/mitchell-hashimoto]](HashiCorp 공동창립자): "에이전트가 실수할 때마다 그 실수가 반복되지 않도록 솔루션 설계에 시간을 투자하는 것" (→ [[sources/youtube-6cr4PeilKJk]]).
- 클로드 코드 기반 6단계 구성: ① [[concepts/claude-md]]로 규칙 전달(세션 간 기억 소실 해소) ② [[concepts/mcp]]/퍼미션으로 위험 명령 물리 차단(맥락 vs 강제) ③ [[concepts/hooks]]으로 테스트 자동 강제(부탁 vs 강제) ④ 테스트 도구(Puppeteer/Playwright) 제공 ⑤ 생성 AI와 검증 AI 분리([[concepts/subagents-agent-teams]]) ⑥ 모델 발전에 따른 하네스 재점검 (→ [[sources/youtube-6cr4PeilKJk]]).

## 주요 주장 / 데이터
- [[entities/anthropic]] 2026년 3월 공식 블로그 실험: 같은 Claude 모델에 레트로 게임 메이커 제작을 시킴. 하네스 없이 → 20분/9달러로 끝났으나 조작 안 되는 망한 앱. 하네스(스펙·완료기준 합의·브라우저 자동 테스트) 갖춤 → 6시간/200달러지만 완성된 앱 (→ [[sources/youtube-6cr4PeilKJk]]).
- Anthropic이 두 차례 블로그에서 밝힌 3대 실패 패턴: ① 세션 간 기억 소실(작년 11월 블로그, "교대 근무 엔지니어" 비유) ② [[concepts/context-decay]](컨텍스트 윈도우 차오르며 일관성 상실·조기 종료) ③ 자기평가 편향(자기 결과물을 무조건 칭찬) (→ [[sources/youtube-6cr4PeilKJk]]).
- 모델 발전 시 하네스도 진화: Anthropic은 Opus 4.6(자막상 "오프스 4.6", 추정) 출시 후 스프린트 구조를 통째로 제거해 하네스를 간소화 → [[concepts/harness-engineering]]의 '하네스 다이어트' 사례 (→ [[sources/youtube-6cr4PeilKJk]]).

## 기존 위키와의 연결
- 강화: #11([[sources/youtube-6gvnDSAcZww]])·#14([[sources/youtube-DrekqeDlO1w]])의 핵심 정의·OpenAI 사례·"말과 마구" 서사를 강화하고, 여기에 Anthropic의 "9달러 vs 200달러" 정량 근거를 추가. [[entities/mitchell-hashimoto]] 창시자 설을 #14와 함께 뒷받침. [[concepts/context-decay]] 강화.
- 모순: "모델 좋아지면 하네스 빼라"(스프린트 제거)는 #11의 진화적 강화 서사와 긴장 → [[sources/youtube-fInMcawbKng]](#24)와 함께 [[concepts/harness-engineering]] '하네스 다이어트'로 기록.
- 신규: "9달러 vs 200달러" 정량 비교, Anthropic 3대 실패 패턴의 구체적 출처(11월·3월 블로그), Opus 4.6 후 스프린트 제거 사례.

## 출처 정보
- raw: /Users/tomo/Desktop/ai-llm-wiki/raw/youtube-6cr4PeilKJk.md
- URL: https://www.youtube.com/watch?v=6cr4PeilKJk
- 채널: 짐코딩 (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3 (순번 #13)
- transcript_lang: ko (자동생성 자막 — 오탈자 주의, 수치는 Anthropic 블로그 기준)

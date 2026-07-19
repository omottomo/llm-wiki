---
title: "#11 프롬프트 엔지니어링은 끝났습니다: 이제 '하네스'의 시대입니다"
label: "#11 프롬프트는 끝났다"
type: source
credibility: medium
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-6gvnDSAcZww]
tags: [하네스엔지니어링, 에이전틱코딩, 컨텍스트엔지니어링, 가드레일, 개발자역할변화]
---

## 한 줄 요약
프롬프트→컨텍스트→하네스→에이전틱이라는 4축 프레임워크 속에서, AI를 "구조적으로 실수할 수 없는 환경"으로 가두는 [[concepts/harness-engineering|하네스 엔지니어링]]을 "말과 마구" 비유로 종합 설명한 개론 영상.

## 핵심 내용
- AI 활용법을 4개 상호보완 축으로 정리: [[concepts/prompt-engineering|프롬프트 엔지니어링]] → [[concepts/context-engineering|컨텍스트 엔지니어링]] → [[concepts/harness-engineering|하네스 엔지니어링]] → [[concepts/agentic-coding|에이전틱 코딩]](영상에서는 "에이전틱 엔지니어링"으로 지칭). 순서대로 졸업하는 게 아니라 전부 동시에 필요하다고 강조.
- 프롬프트에는 "천장"이 있고, 컨텍스트를 잘 줘도 AI가 정보를 알면서 엉뚱한 짓(DB 스키마 임의 변경, 카드번호 로깅 등)을 하는 문제가 남는다 — 이는 "정보의 문제가 아니라 규칙과 울타리의 문제".
- 핵심 철학: 에이전트가 규칙을 어겼을 때 "더 잘해봐"라고 프롬프트를 고치지 말고, 그 실패가 구조적으로 반복 불가능하도록 하네스를 고쳐라.
- 하네스의 4기둥: ① 컨텍스트 파일([[concepts/claude-md|CLAUDE.md]], agents.md, .cursorrules 등 — 런타임 설정 파일) ② 자동 강제([[concepts/hooks|훅]], 린터, 아키텍처 테스트, 프리커밋 훅) ③ 도구 경계(파일/API/DB/터미널 권한 제한) ④ 가비지 컬렉션(나쁜 패턴 주기적 자동 정리, [[concepts/context-decay|컨텍스트 부패]]에 대응).
- 실제 시스템은 4부품으로 구성: 라우터(단순 질문 vs 실제 코드 작업 분기) → 컨텍스트 매니저(가림막, 필요한 파일만 제공) → 실행 루프(코드 작성→테스트→실패 시 피드백 재투입, 하네스의 심장) → 워커 격리(작성 AI와 검토 AI 분리, [[concepts/subagents-agent-teams|서브에이전트 & 에이전트 팀]]).

## 주요 주장 / 데이터
- 2026년 2월 [[entities/openai|OpenAI]]가 공식 블로그에서 엔지니어 3명이 코드를 한 줄도 직접 쓰지 않고 5개월 만에 대규모 소프트웨어 제품을 배포한 사례를 발표. 이들이 한 일은 agents.md 작성 + CI/CD 게이트(린트·테스트·훅) + 도구 경계 설정 + 피드백 루프 구축 — 즉 "코드를 쓴 게 아니라 시스템을 만든 것".
- 인용: "인간은 조종한다, 에이전트는 실행한다" — 여기서 '조종'이 곧 하네스.
- 마틴 파울러(자막상 "마틴 러가"·"마틴 파울러"로 표기, 추정)가 test harness(1970년대부터 존재) 개념을 AI 시대 맥락에서 체계화했고, 나쁜 코드 자동 정리를 "가비지 컬렉션"이라 명명.
- 결론: 개발자 역할은 축소가 아니라 "상향 이동" — 선수에서 감독으로 ([[concepts/developer-role-change|개발자 역할의 변화]]).

## 기존 위키와의 연결
- 강화: [[concepts/harness-engineering|하네스 엔지니어링]]의 핵심 정의("실패를 구조적으로 반복 불가능하게")와 4기둥 구조를 강화. [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]과 동일한 OpenAI 3인·"말과 마구" 서사를 공유. [[concepts/developer-role-change|개발자 역할의 변화]]의 "감독으로의 상향 이동" 주장 강화.
- 모순: 직접적 모순 없음. 다만 "하네스를 점점 더 쌓아라"는 진화적 강화 관점은 [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]와 긴장 관계 → [[concepts/harness-engineering|하네스 엔지니어링]]의 '하네스 다이어트' 보완으로 기록.
- 신규: 4축 프레임워크를 "프롬프트/컨텍스트/하네스/에이전틱"으로 명시적 정리한 점, 라우터-컨텍스트매니저-실행루프-워커격리의 4부품 시스템 다이어그램.

## 출처 정보
- raw: raw/youtube-6gvnDSAcZww.md
- URL: https://www.youtube.com/watch?v=6gvnDSAcZww
- 채널: 실밸개발자 (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3 (순번 11)
- transcript_lang: ko (자동생성 자막 — 오탈자/오인식 주의)

---
title: 프롬프트 엔지니어링
type: concept
created: 2026-06-23
updated: 2026-06-23
sources: [youtube-6gvnDSAcZww, youtube-BssPGKsP60s]
tags: [프롬프트, 진화서사, 기초개념]
---

# 프롬프트 엔지니어링

**프롬프트 엔지니어링은 "뭘 물어볼까"의 기술**, 즉 AI에게 말을 잘 거는 기술이다 (→ [[sources/youtube-6gvnDSAcZww]], → [[sources/youtube-BssPGKsP60s]]). 진화 서사 프롬프트 → 컨텍스트 → 하네스 → 루프에서 첫 번째 축이자 출발점이다.

## 정의와 대표 기법

ChatGPT 초창기에 "질문만 잘하면 된다 / 역할을 줘라 / 단계별로 시켜라 / 예시를 넣어라"고 하던 것이 곧 프롬프트 엔지니어링이다 (→ [[sources/youtube-BssPGKsP60s]]). 추상적으로 "웹사이트 만들어 줘"보다 "사인·코사인·로그를 지원하고 GUI가 있는 공학용 계산기를 만들어 줘"처럼 구체적으로 요청하면 결과가 확연히 달라진다 (→ [[sources/youtube-6gvnDSAcZww]]).

## 천장(한계)

아무리 정교하게 프롬프트를 써도 AI가 우리 프로젝트의 기술 스택·코드 구조·DB 스키마를 모르면 좋은 코드가 나올 수 없다. "로그인 기능을 추가해 줘"라고 해도 배경 정보가 없으면 엉뚱한 코드가 나온다. 이 천장 때문에 다음 단계인 [[concepts/context-engineering]]가 등장했다 (→ [[sources/youtube-6gvnDSAcZww]], → [[sources/youtube-BssPGKsP60s]]).

또한 프롬프트는 본질적으로 **부탁이지 강제가 아니다**. "DB를 직접 호출하지 마"라고 프롬프트에 써도 다음번에 또 어긴다. 이 한계를 시스템적 강제로 넘어서는 것이 [[concepts/harness-engineering]]의 핵심 동기다 (→ [[sources/youtube-6gvnDSAcZww]]).

## 진화 서사 속 위치

테슬라 AI를 이끌던 [[entities/andrej-karpathy]](자막상 "카파스"로 표기됨, 추정)가 "프롬프트보다 컨텍스트 엔지니어링이 핵심"이라 했고, 가트너는 프롬프트 엔지니어링 시대의 종료를 공식 선언했다고 언급된다 (→ [[sources/youtube-BssPGKsP60s]]). 다만 이 네 축은 순서대로 졸업하는 것이 아니라 상호보완적이므로, 프롬프트 엔지니어링이 폐기되는 것이 아니라 더 큰 환경 설계(하네스) 안의 한 요소로 남는다는 점이 강조된다 (→ [[sources/youtube-6gvnDSAcZww]]).

> 프롬프트 엔지니어링은 모델에게 "잘 해 줘"라고 부탁하는 것이고, 하네스 엔지니어링은 "잘 할 수밖에 없는 구조"를 만드는 것이다 — 부탁과 구조의 차이가 핵심이다 (→ [[sources/youtube-6gvnDSAcZww]]).

## 같이 보기

- [[concepts/context-engineering]] — 프롬프트의 천장을 넘는 다음 단계
- [[concepts/harness-engineering]] — "부탁"을 "강제 구조"로 바꾸는 종착점

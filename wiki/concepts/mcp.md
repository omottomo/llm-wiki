---
title: MCP (모델 컨텍스트 프로토콜)
type: concept
created: 2026-06-23
updated: 2026-08-04
sources: [youtube-BssPGKsP60s, youtube-DCsv0rKKrN4, youtube-6MYZ7fMhKPY]
tags: [클로드코드, MCP, 도구연결, 하네스엔지니어링, 토큰관리]
---
# MCP (모델 컨텍스트 프로토콜)

## 한눈에 요약

- AI 에이전트가 **바깥 도구와 데이터를 쓸 수 있게 연결해 주는 공통 규격**이다.
- 브라우저 조작, 문서 검색, DB 조회처럼 AI가 혼자서는 못 하는 일을 이 연결로 대신 시킨다.
- 많이 연결할수록 좋은 게 아니다. 연결된 도구의 **설명만으로도** AI가 읽어야 할 분량이 늘어 성능과 비용이 나빠진다.
- 그래서 가장 자주 반복되는 교훈은 하나다. **지금 하는 작업에 필요한 것만 켜 둔다.**

## 무엇을 연결하나

MCP는 AI 에이전트가 외부 도구를 쓸 수 있게 연결해 주는 것이다 — 브라우저 자동화, 문서 검색, 디자인 도구 연결, 데이터베이스 접근 등 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]). [[concepts/harness-engineering|하네스 엔지니어링]]의 핵심 구성 요소로, "AI가 쓸 수 있는 도구 목록을 미리 정해 주는 것"으로도 설명된다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]] 참조).

## 하네스에서의 위치
- 하네스 = [[concepts/context-engineering|컨텍스트 엔지니어링]] + MCP 서버 설정 + [[concepts/skills|스킬]] + 에이전트 설정을 모두 합친 전체 환경 설계다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).
- 주방에 비유하면 이렇다. [[concepts/context-engineering|컨텍스트 엔지니어링]]이 좋은 재료를 골라 주는 것이라면, MCP 설정은 수산시장·정육점·농장과 직통으로 잇는 "외부 업체 어댑터"다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).
- 데이터베이스 MCP를 연결하면 AI가 DB를 정해진 방식으로만 다루게 된다. 도구 사용에 일종의 경계가 생긴다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]] 참조). [[concepts/hooks|훅]]의 '도구 경계' 참조.
- "컨텍스트 파일·MCP 연결·스킬 정리" 이 세 가지가 하네스를 시작하는 출발점으로 권장된다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).

## 핵심 주의 — "MCP는 많을수록 좋지 않다" (토큰 관리)
이 개념의 가장 반복되는 실전 교훈이다.
- MCP를 많이 주면 줄수록 좋은 게 아니다. MCP를 쓸 때 토큰이 터지지 않도록 여러 테크닉을 써야 한다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).
- MCP를 여러 개 연결하면 **도구 설명(description)만으로 토큰을 크게 소비**한다. 특히 Notion·Linear 같은 MCP는 도구 설명이 매우 커서 토큰을 크게 잡아먹는다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
- 직관과 달리 도구는 적을수록 좋다. 많으면 에이전트가 "어떤 도구를 쓸지" 고민하느라 정작 할 일에 집중을 못 한다. 넷플릭스에서 뭐 볼지 30분 고민하다 결국 유튜브 켜는 것에 비유된다 (→ [[sources/youtube-6MYZ7fMhKPY|#21 바이브에서 에이전틱으로]]).

### 대응 테크닉
- `/mcp`로 현재 연결된 MCP를 확인하고, 지금 작업에 안 쓰는 MCP는 **비활성화(disable)** 할 줄 알아야 한다(예: Notion을 안 쓰면 disable) (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
- 도구 설명이 큰 MCP는 그대로 쓰지 않는다. **자주 쓰는 기능만 골라 감싼 커스텀 MCP**를 만들어 쓴다. 필요한 엔드포인트만 감싸면 토큰 절약은 물론 응답 품질도 올라간다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

## 활용 연결
- WAT 프레임워크의 도구(T) 예시로, MCP(git)로 PR을 생성하고 [[concepts/hooks|훅]]으로 커밋마다 테스트를 자동 실행하는 식의 조합이 제시된다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
- MCP를 추가하거나 스킬·훅을 설정할 때마다 사실은 하네스를 설계하고 있는 것이며, 단지 그렇게 부르지 않았을 뿐이다 (→ [[sources/youtube-6MYZ7fMhKPY|#21 바이브에서 에이전틱으로]]).
- 다만 덜어내는 쪽도 있다. "스킬·MCP를 다 설치했더니 Claude Code가 이상해졌다면 다 지우고 지금 작업에 필요한 것만 남기라"는 게 하네스 다이어트의 실천이다 (→ [[sources/youtube-6MYZ7fMhKPY|#21 바이브에서 에이전틱으로]]). [[concepts/harness-engineering|하네스 엔지니어링]]의 긴장② 참조.

## 함께 읽기

- [[concepts/harness-engineering|하네스 엔지니어링]] — MCP가 한 부품으로 들어가는 전체 그림
- [[concepts/skills|스킬]] · [[concepts/hooks|훅]] — 같은 하네스 층에 놓이는 나머지 부품
- [[concepts/context-engineering|컨텍스트 엔지니어링]] — MCP 토큰 관리가 여기 속한다
- [[concepts/claude-md|CLAUDE.md]] — 둘 다 사용자가 손댈 수 있는 컨텍스트다. 다만 MCP·스킬 메타데이터는 자동 주입 영역이다
- [[entities/claude-code|Claude Code]] — MCP를 연결해 쓰는 도구
- [[concepts/graphql|GraphQL]] — 서버가 스키마를 실시간으로 내주고 클라이언트가 그에 맞춰 호출한다는 결이 닮은 사례

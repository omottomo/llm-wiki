---
title: 컨텍스트 엔지니어링
type: concept
created: 2026-06-23
updated: 2026-06-23
sources: [youtube-DCsv0rKKrN4, youtube-FBv8hK_DtJ8, youtube-BssPGKsP60s, youtube-6gvnDSAcZww]
tags: [컨텍스트, 환경설계, 진화서사, 메모리관리]
---

# 컨텍스트 엔지니어링

**컨텍스트 엔지니어링은 "뭘 보여줄까"의 기술**이다. AI에게 프롬프트만 주는 게 아니라 프로젝트 구조·기존 코드·예시·API 문서·디자인 규칙까지 함께 제공해, AI가 우리 상황을 알고 일하게 만드는 단계다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]). 진화 서사 프롬프트 → 컨텍스트 → 하네스 → 루프에서 두 번째 축이며, [[concepts/harness-engineering|하네스 엔지니어링]]에 포함되는 부분집합이다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).

## 왜 등장했나

[[concepts/prompt-engineering|프롬프트 엔지니어링]]에는 천장이 있다. "로그인 기능을 추가해 줘"라고 아무리 정교하게 써도 프로젝트의 기술 스택·코드 구조·DB 스키마를 모르면 좋은 코드가 나올 수 없기 때문이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]). 테슬라 AI를 이끌던 [[entities/andrej-karpathy|안드레이 카파시]](자막상 "카파스"로 표기됨, 추정)가 "프롬프트보다 컨텍스트 엔지니어링이 핵심"이라 했고, 가트너는 프롬프트 엔지니어링 시대의 종료를 선언했다고 언급된다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).

## 핵심 원칙: 많이가 아니라 정확히

[[entities/anthropic|Anthropic]]의 정의는 "AI가 일할 때 필요한 정보를 적절하게 골라서 제공하는 기술"이다. 핵심은 많이 주는 게 아니라 **지금 필요한 것만 정확하게** 주는 것 — 정보를 너무 많이 주면 오히려 성능이 떨어지기 때문이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]). "컨텍스트는 왕(context is king)"이라는 표현이 쓰이며, 관리 방식에 따라 답변 품질이 천차만별로 갈린다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

## 실전 기법

### 레이지 로딩 / 조건부 로딩

[[concepts/claude-md|CLAUDE.md]] 같은 컨텍스트 파일에 API 50개·DB 테이블 30개를 다 몰아넣으면 매 세션 수천 토큰이 낭비된다(정작 필요한 건 5%도 안 됨). 따라서 `CLAUDE.md`에는 규칙과 참조 링크만 두고 상세 내용은 별도 파일로 분리해 필요할 때만 읽게(레이지 로딩) 한다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

대규모 프로젝트에서는 `.claude/rules/` 하위에 주제별 메모리 파일을 두고 **프론트매터에 조건(glob 패턴)을 걸어** 특정 파일/디렉터리를 작업할 때만 해당 규칙이 자동 로드되게 한다. 예: 테스트 규칙은 테스트 파일에만, API 규칙은 API 파일에만 적용. 한 개발자는 모노레포에서 `CLAUDE.md`가 47,000단어까지 불어나 클로드가 느려지고 규칙을 안 따르기 시작했는데, 필요 시점에만 불러오도록 나눠 루트 메모리를 80% 줄였다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]). "라떼 만드는 법을 알려주는데 청소·재고 정리·마감하는 법까지 섞으면 정작 라떼 레시피가 묻힌다"는 비유가 쓰인다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]). 폴더별로 `CLAUDE.md`를 따로 두는 방식도 루트 비대화를 막는다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

### 세컨드 브레인 / 메모리

작업하며 배운 패턴·해결책·의사결정 이유를 로컬 마크다운(세컨드 브레인)에 저장해 재참조한다. [[entities/claude-code|Claude Code]]의 `/memory` 기능은 이를 자동화해 학습 내용을 `memory.md`에 저장하고 매 세션 자동 로드한다. 개인 메모리는 `/memory`, 팀 공유 지식은 `CLAUDE.md`로 나누는 것이 권장된다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

### 컨텍스트 윈도우 위생

200K 토큰은 생각보다 금방 찬다. 가장 실용적인 규칙은 "한 세션에서 한 피처/한 작업만" 하고 끝나면 `/clear`로 새 세션을 여는 것이다. "신선한 컨텍스트가 부풀려진 컨텍스트보다 낫다." 무거운 데이터 처리(10만 행 CSV 등)는 대화 안에서 하면 컨텍스트가 오염되므로, 클로드에게 스크립트를 작성·실행하게 하고 결과 요약만 받는 식으로 오프로드한다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]). 이는 [[concepts/context-decay|컨텍스트 부패]](컨텍스트 부패) 문제와 직결된다.

### MCP 토큰 관리

[[concepts/mcp|MCP]]를 여러 개 연결하면 도구 설명만으로도 토큰을 크게 소비한다. 노션·리니어 같은 MCP는 설명이 매우 커서, 지금 안 쓰는 MCP는 비활성화하고 자주 쓰는 기능만 골라 커스텀 MCP로 래핑하면 토큰 절약과 응답 품질 향상을 동시에 얻는다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]·[[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).

## 하네스와의 관계

컨텍스트를 아무리 잘 설계해도 "AI가 정보는 다 아는데 엉뚱한 짓을 하는" 문제(예: 결제 시스템에 DB 스키마를 멋대로 바꾸기)는 해결되지 않는다. 이는 정보의 문제가 아니라 규칙과 울타리의 문제이며, 바로 여기서 [[concepts/harness-engineering|하네스 엔지니어링]]이 필요해진다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]). 즉 컨텍스트 엔지니어링은 하네스의 한 기둥(컨텍스트 파일)으로 흡수된다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).

## 같이 보기

- [[concepts/claude-md|CLAUDE.md]] — 컨텍스트 파일의 대표 형태와 "지워라 vs 써라" 모순①
- [[concepts/context-decay|컨텍스트 부패]] — 긴 작업에서 컨텍스트가 차며 일관성을 잃는 현상
- [[concepts/dynamic-workflow|다이나믹 워크플로우]] — 서브에이전트로 컨텍스트를 격리·효율화

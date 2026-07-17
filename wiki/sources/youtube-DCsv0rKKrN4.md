---
title: "#7 메타 엔지니어의 클로드 코드 완벽 가이드 [실전편] — 컨텍스트 관리·워크플로우 총정리"
label: "#7 메타 엔지니어 실전편"
type: source
created: 2026-06-23
updated: 2026-07-12
tags: [클로드md, 컨텍스트엔지니어링, 워크플로우, MCP, 멀티모델, 검증자동화]
sources: [youtube-DCsv0rKKrN4]
---

## 한 줄 요약
컨텍스트 관리(세컨드 브레인·메모리·레이지 로딩·스크립트 오프로드)와 실전 워크플로우(플랜 모드·TDD·멀티 AI 검증·투두 파일·WAT 프레임워크)를 20분으로 압축한 [[entities/claude-code|Claude Code]] 실전 가이드.

## 핵심 내용
- **세컨드 브레인 + 오토 메모리**: 패턴·해결책·의사결정 근거를 로컬 마크다운에 축적. 최근 추가된 `/memory`(슬래시 메모리) 기능이 학습 내용을 자동으로 memory.md에 저장하고 세션 시작 시 로드. 개인 지식은 메모리, 팀 공유 지식은 [[concepts/claude-md|CLAUDE.md]]로 분리 권장.
- **레이지 로딩**: CLAUDE.md엔 규칙과 참조만 두고 상세(API 스펙 50개, DB 스키마 등)는 별도 파일로 분리해 필요 시점에만 읽게 함. 폴더별 CLAUDE.md를 둬서 루트 비대화·[[concepts/context-decay|컨텍스트 부패]] 방지 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]와 동일 전략).
- **한 세션 = 한 피처**: 200K 토큰도 금방 차므로 `/clear`·`/compact`보다 작업 단위를 쪼개 신선한 세션으로 시작. "신선한 컨텍스트 > 부풀어 오른 컨텍스트".
- **MCP 관리**: 노션·리니어 같은 [[concepts/mcp|MCP]]는 도구 설명만으로 토큰을 크게 소비. 안 쓰는 MCP는 비활성화하고, 자주 쓰는 기능만 래핑한 커스텀 MCP를 만들어 토큰 절약.
- **무거운 작업은 스크립트로 오프로드**: 10만 행 CSV 같은 데이터 처리는 대화에 넣지 말고 클로드가 스크립트를 작성·실행해 결과 요약만 회수 → 컨텍스트 청정 유지.
- **워크플로우**: 플랜 모드로 설계→리뷰→실행 분리, [[concepts/verification-automation|TDD]] 기반 작은 변경·테스트·커밋 반복, think 과정 읽고 잘못된 가정은 즉시 중단, 에러 로그는 통째로 붙여넣기.

## 주요 주장 / 데이터
- **멀티 AI 검증**: 클로드 플랜을 ChatGPT·Gemini에 익스포트해 비평받으면 모델마다 다른 시선·다른 솔루션이 나옴. `with multiple AI` 같은 커스텀 [[concepts/skills|스킬]]로 자동화 가능 → [[concepts/multi-model-workflow|멀티 모델 워크플로우]].
- **로컬 투두 파일**: 프로젝트 시작~끝을 하나의 to.md로 관리, 세션 종료 시 자동 갱신해 여러 세션에 걸친 연속성 확보. [[concepts/subagents-agent-teams|에이전트 팀스]]로 병렬 처리.
- **WAT 프레임워크** (유튜버 "네이트" 제안, 자막상 이름 추정): W=Workflow(영어로 작업 흐름 정의), A=Agent(셀프힐링·병렬 처리), T=Tools(거대 스크립트보다 작은 단위 스크립트 + MCP + [[concepts/hooks|훅]]). 핵심은 AI의 추론과 코드 실행을 분리하는 것.

## 기존 위키와의 연결
- 강화: [[concepts/context-engineering|컨텍스트 엔지니어링]] — 레이지 로딩·세션 분리·스크립트 오프로드로 컨텍스트 엔지니어링 실전 기법을 강화. [[concepts/claude-md|CLAUDE.md]] — "규칙·참조만, 상세는 분리" 원칙을 [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]/[[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]와 일관되게 강화. [[concepts/multi-model-workflow|멀티 모델 워크플로우]] — Codex뿐 아니라 ChatGPT/Gemini 교차 검증으로 확장.
- 모순: 직접적 모순 없음. 단 [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]의 "장황한 메모리 파일 폐해"와 같은 문제의식을 공유하되, 해결책으로 '삭제'가 아니라 '분리·레이지 로딩'을 제시한다는 점에서 [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]와 결을 같이한다.
- 신규: WAT 프레임워크, `/memory` 오토 메모리, 스크립트 오프로드 전략, 멀티 AI 비평 자동화 스킬을 위키에 처음 소개.

## 출처 정보
- raw: raw/youtube-DCsv0rKKrN4.md
- URL: https://www.youtube.com/watch?v=DCsv0rKKrN4
- 채널: 실밸개발자 (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 게시/수집 정보: 자막 lang=ko, 재생목록 순번 7
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3

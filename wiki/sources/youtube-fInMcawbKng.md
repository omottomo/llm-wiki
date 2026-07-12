---
title: "#24 다이나믹 워크플로우 | 낡은 하네스의 군살을 빼라"
type: source
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-fInMcawbKng]
tags: [다이나믹워크플로우, 하네스다이어트, 하네스엔지니어링, 적대적검증]
---

## 한 줄 요약
모델·제품이 진화하면서 과거에 쌓은 하네스가 오히려 방해가 될 수 있으므로, [[concepts/dynamic-workflow]] 기능으로 레거시 하네스를 감사하고 "다이어트"(군살 빼기)하는 방법을 실연한다 (→ [[sources/youtube-fInMcawbKng]]).

## 핵심 내용
- 핵심 전제: "한 번 만든 하네스는 영원하지 않다." Opus 4.8·GPT 5.5 등 모델이 똑똑해지면서 예전에 강제하던 규칙이 불필요해지거나 제품 내장 기능과 중복되어 오히려 방해가 됨 (→ [[sources/youtube-fInMcawbKng]]).
- Claude Code·Codex·Cursor 자체가 이미 하나의 하네스(파일 읽기·코드 수정·터미널·메모리·툴·스킬 내장)이므로, 내 커스텀 하네스는 그 위에 또 얹는 구조 → 중복 발생 가능 (→ [[sources/youtube-fInMcawbKng]]).
- 지금은 하네스를 더 붙일 때가 아니라 **불필요한 것을 덜어낼 때** (→ [[sources/youtube-fInMcawbKng]]).
- [[concepts/dynamic-workflow]]는 자바스크립트로 다수 [[concepts/subagents-agent-teams]]를 오케스트레이션하며 백그라운드 실행. 실행법: `울트라 코드` 키워드 / 자연어 / 저장된 슬래시 명령. effort 레벨(low·medium·high·xhigh·max + 울트라코드) (→ [[sources/youtube-fInMcawbKng]]).
- 내장 딥리서치 워크플로우 시연: 검색→패치→적대적 검증→종합 리포트. 각 페이즈는 별도 서브에이전트에서 돌아 메인 컨텍스트를 절약 (→ [[sources/youtube-fInMcawbKng]]).
- 직접 만든 워크플로우 2종: ① **하네스 레거시 스캔**(읽기 전용 감사: 인벤토리→애널라이즈→플랜→적대적 리뷰) ② **하네스 다이어트**(스플릿→리파인으로 실제 개선 적용) (→ [[sources/youtube-fInMcawbKng]]).

## 주요 주장 / 데이터
- 워크플로우 vs 다른 기술의 핵심 차이 = "플랜을 누가 들고 있나": 서브에이전트=턴 단위, [[concepts/skills]]=메인 세션, 에이전트 팀=팀 리드, 워크플로우=자바스크립트 스크립트 단. 그래서 수십~수백 에이전트 규모 가능 (→ [[sources/youtube-fInMcawbKng]]).
- 공식 문서 기준: 워크플로우는 동시 최대 16개, 누적 1000개 서브에이전트 실행 가능 (→ [[sources/youtube-fInMcawbKng]]).
- 레거시 스캔 결과: 16개 에이전트로 109개 항목 발견, 약 160만 토큰, 17분 소요 (→ [[sources/youtube-fInMcawbKng]]).
- 다이어트 적용 결과: 스킬 10개 정리, 신규 레퍼런스 12개 추가, SKILL.md 본문 약 2,600줄→1,800줄(약 760줄 감축), 활성 스킬 29→28개(노션 워크스페이스 보관) (→ [[sources/youtube-fInMcawbKng]]).
- 권장: 두 워크플로우를 한 달에 한두 번 주기적으로 돌리되, 스캔 결과를 사람이 먼저 검토 후 다이어트 적용 (→ [[sources/youtube-fInMcawbKng]]).
- S키로 워크플로우를 `.claude` 폴더에 자바스크립트로 저장해 재사용 가능 (→ [[sources/youtube-fInMcawbKng]]).

## 기존 위키와의 연결
- 모순/긴장: 긴장② — "하네스를 쌓아라"([[sources/youtube-BssPGKsP60s]]#5 등) vs 본 영상의 "낡은 하네스는 빼라/제품 내장 기능과 중복". [[concepts/harness-engineering]]에 '하네스 다이어트' 보완 관점으로 기록 (→ [[sources/youtube-fInMcawbKng]]).
- 강화: [[concepts/dynamic-workflow]]의 동적·백그라운드·적대적 검증 구조를 강화하고 구체 수치를 보강.
- 강화: [[concepts/claude-md]]의 "짧고 검증가능한 최소 규칙" 입장(모순①)과 같은 방향 — 중복·과도한 전역 컨텍스트 제거를 권장.

## 출처 정보
- raw: raw/youtube-fInMcawbKng.md
- URL: https://www.youtube.com/watch?v=fInMcawbKng
- 채널: 개발동생 (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3 (#24)
- 자막: 한국어 자동생성 (오탈자 가능)

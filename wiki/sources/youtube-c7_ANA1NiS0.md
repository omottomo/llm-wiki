---
title: "#6 CLAUDE.md를 지워라 (Delete CLAUDE.md) — 논문이 말하는 컨텍스트 파일의 역설"
type: source
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-c7_ANA1NiS0]
tags: [클로드md, 컨텍스트엔지니어링, 논문, 스킬, 컨텍스트부패]
---

## 한 줄 요약
"Repository-level context files helpful for coding agents?" 논문을 소개하며, 잘못 작성된 [[concepts/claude-md]]/AGENTS.md가 오히려 작업 성공률을 떨어뜨리고 추론 비용을 20% 이상 늘릴 수 있음을 보여주는 영상 (→ [[sources/youtube-c7_ANA1NiS0]]).

## 핵심 내용
- 컨텍스트 구조를 시스템 프롬프트(사용자 접근 불가) → 메모리 파일(CLAUDE.md/AGENTS.md) → 유저 프롬프트 → AI 출력물 순으로 정리. 사용자가 조정 가능한 건 메모리 파일과 유저 프롬프트뿐이며, 처음·끝 위치가 가장 높은 우선순위를 가진다고 설명 (→ [[sources/youtube-c7_ANA1NiS0]]).
- 논문은 세 조건(컨텍스트 파일 없음 / LLM 자동생성 / 사람 직접 작성)을 SW-Bench·자체 제작 "에이전트 벤치"에서 비교 (→ [[sources/youtube-c7_ANA1NiS0]]).
- LLM이 자동생성한 컨텍스트 파일은 아무것도 주지 않은 경우보다 성공률을 떨어뜨림(에이전트 벤치 약 2%, SW-Bench-Lite 약 0.5% 하락) (→ [[sources/youtube-c7_ANA1NiS0]]).
- 파일이 없을 때 더 적은 스텝·더 적은 툴 호출로 첫 응답에 도달하고 비용도 낮았음. 컨텍스트 파일이 있으면 코드를 불필요하게 더 넓게 탐색하는 경향 ([[concepts/context-decay]] 관점) (→ [[sources/youtube-c7_ANA1NiS0]]).
- 단, **사람이 직접 작성한** 컨텍스트 파일은 LLM 생성본보다 성공률이 높았고 평균 약 19% 향상(소닛 등 일부 모델은 예외) (→ [[sources/youtube-c7_ANA1NiS0]]).
- 화자의 해석: 이 논문은 "CLAUDE.md를 아예 없애라"가 아니라 **장황한 문서형 CLAUDE.md의 폐해**에 관한 것. 불필요한 내용은 [[concepts/skills]]로 옮기고, CLAUDE.md엔 매번 꼭 필요한 최소 정보만 남기라는 결론 (→ [[sources/youtube-c7_ANA1NiS0]]).

## 주요 주장 / 데이터
- 추론 토큰 추가 사용: GPT-5.2 +22%, 5.1-mini +14% (컨텍스트 파일 처리 비용, 자막상 모델명 추정) (→ [[sources/youtube-c7_ANA1NiS0]]).
- 컨텍스트 파일이 성공률을 떨어뜨리는 주된 이유: ① 레포에서 에이전트가 쉽게 파악 가능한 정보가 파일과 중복됨, ② 현재 작업과 무관한 규칙(폴더 구조·인증·금지 사항 등)이 잘못된 컨텍스트를 주입해 목표 지향성을 흔듦 (→ [[sources/youtube-c7_ANA1NiS0]]).
- 현대 에이전트는 [[concepts/subagents-agent-teams]]로 분석을 위임하고 결과만 메인에 회수하므로 컨텍스트를 적게 쓰는데, 거대한 메모리 파일이 이 흐름을 방해한다는 주장 (→ [[sources/youtube-c7_ANA1NiS0]]).

## 기존 위키와의 연결
- 강화: [[concepts/skills]] — CLAUDE.md를 가볍게 두고 상세 문서·작업별 지식은 스킬로 옮겨 필요 시점에만 트리거하라는 권장을 강화. [[concepts/context-decay]] — 무관한 컨텍스트가 성능을 떨어뜨린다는 주장 강화.
- 모순: [[sources/youtube-cZ8_Dkk_Ce0]](#8 "CLAUDE.md로 품질 3배") 및 [[sources/youtube-gol5jv4wcfs]](#19)와 표면적으로 충돌. #8/#19/#10([[sources/youtube-FBv8hK_DtJ8]])/#5([[sources/youtube-BssPGKsP60s]])는 "CLAUDE.md를 잘 쓰면 강력하다"고 주장. 화해 관점: 이 영상이 비판하는 대상은 **자동생성·장황·불필요 규칙으로 가득 찬 문서형** CLAUDE.md이고, 권장 진영이 말하는 건 **짧고(150~200줄) 검증 가능한 최소 규칙**이다. 실제로 본 영상도 "사람이 직접 쓴 최소 컨텍스트는 +19%"라며 사람 작성본의 가치를 인정하므로, 두 입장은 '잘못 쓴 CLAUDE.md'와 '잘 쓴 CLAUDE.md'를 두고 갈린다. → [[concepts/claude-md]]에 양쪽 모두 기록.
- 신규: "Repository-level context files helpful for coding agents?" 논문과 자체 "에이전트 벤치" 벤치마크를 위키에 처음 도입. [[concepts/context-decay]]의 실증 근거로 연결.

## 출처 정보
- raw: raw/youtube-c7_ANA1NiS0.md
- URL: https://www.youtube.com/watch?v=c7_ANA1NiS0
- 채널: 코드팩토리 (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 게시/수집 정보: 자막 lang=ko, 재생목록 순번 #6
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3

---
title: "#22 800시간 사용 후 꼽은 필수 Claude Code 스킬 6가지"
label: "#22 필수 스킬 6가지"
type: source
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-UClLUoGaCxU]
tags: [스킬, 클로드코드, 카파시가이드라인, 워크플로우]
---

## 한 줄 요약
화려한 스킬이 아니라 실제로 매일 손이 가는 6가지 [[concepts/skills|스킬]]을 소개하면서, 스킬의 본질은 "반복 지시를 한 번 정리해 재사용·진화시키는 것"이라고 강조한다.

## 핵심 내용
- **① 카파시 가이드라인**: 마크다운 파일 1장(깃허브 스타 15만+). [[entities/andrej-karpathy|안드레이 카파시]]("Tesla AI 총괄, 최근 Anthropic 합류"로 자막 표기)가 정리한, AI 코딩의 반복 문제 4규칙 ([[concepts/claude-md|CLAUDE.md]] 형태) — 모르면 묻지 않고 코딩 시작 / 100줄로 될 걸 1000줄로 / 버그 하나 고치라니 주변 코드까지 건드림 등을 교정. 두 줄 명령으로 설치, 유저 스코프 등록 시 자동 로드.
- **② Claude 비디오**: 유튜브 영상을 다운로드·프레임 추출·자막까지 뽑아 Claude가 실제 화면+음성을 보게 함. 영상 길이에 따라 프레임 수 자동 조절(30초↓ 약 30프레임, 10분↑ 약 100프레임).
- **③ 슈퍼파워(Superpowers)**: 깃허브 스타 20만+, Anthropic 공식 마켓 등재. Claude에게 시니어 개발자 프로세스를 강제(스펙 정리→계획→테스트 먼저, 테스트 없으면 코드 삭제). [[concepts/subagents-agent-teams|서브에이전트 & 에이전트 팀]]으로 태스크별 깨끗한 컨텍스트 실행 + 2회 리뷰(스펙 준수/코드 품질). 첫 결과물 60점→80점.
- **④ Understand**: 20만 줄 코드베이스의 막막함 해결. `/understand`로 멀티에이전트가 전체 스캔→지식 그래프, 대시보드·가이드 투어 제공. 코드뿐 아니라 PDF·마크다운·이미지도 비전으로 흡수.
- **⑤ 에이전트 메모리**: 세션 작업을 조용히 기록·압축해 로컬 DB 저장, 다음 세션에 필요한 컨텍스트만 주입. 기존 빌트인 메모리(파일 전체 주입)와 달리 벡터·그래프 검색으로 관련 정보만 선별 ([[concepts/context-decay|컨텍스트 부패]] 완화).
- **⑥ 스킬 크리에이터**: Anthropic 공식. 원하는 걸 설명하면 Claude가 스킬을 만들고 테스트·패키징까지. 가장 강력한 스킬은 나에게 딱 맞는 걸 직접 만드는 것.

## 주요 주장 / 데이터
- (Anthropic 엔지니어 인용) 사람들은 프롬프트 하나하나에 공을 들이면서도 그걸 스킬로 만들어 두진 않는다. "Claude를 1일차에 쓰는 방식과 30일차에 쓰는 방식은 완전히 달라야 한다".
- 스킬은 한 번 만들고 끝이 아니라 결과의 아쉬운 점을 수정해 진화시켜야 함. 같은 프롬프트 반복 = 매번 처음부터 새로 시작.
- 보너스: Remotion 공식 스킬(React로 영상 제작) — 애니메이션 타이밍·싱크 실수 감소.
- 영상의 결론: 스킬화·최적화·반복이 [[concepts/agentic-coding|에이전틱 코딩]](바이브 코딩)의 핵심.

## 기존 위키와의 연결
- 강화: [[concepts/skills|스킬]]의 "반복을 정리해 재사용·진화"라는 핵심을 강화. [[concepts/claude-md|CLAUDE.md]](카파시 가이드라인), [[concepts/subagents-agent-teams|서브에이전트 & 에이전트 팀]](슈퍼파워), [[concepts/context-decay|컨텍스트 부패]](에이전트 메모리)와 연결.
- 강화: [[entities/andrej-karpathy|안드레이 카파시]]의 "65줄 CLAUDE.md / Karpathy Guidelines" 저자 사실 — [[sources/youtube-gol5jv4wcfs|#19 65줄 CLAUDE.md]]와 동일 인물·동일 문서.
- 신규: Claude 비디오·Understand·에이전트 메모리·스킬 크리에이터 등 구체 스킬 사례를 도입.

## 출처 정보
- raw: raw/youtube-UClLUoGaCxU.md
- URL: https://www.youtube.com/watch?v=UClLUoGaCxU
- 채널: Jay Choi | 인디해커 라이프 (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3 (순번 22)
- 자막: 한국어 자동생성 (오탈자·인명 오인식 가능; "안드레카파시"=[[entities/andrej-karpathy|안드레이 카파시]])

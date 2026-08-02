---
title: 위키 색인
type: overview
created: 2026-06-23
updated: 2026-08-02
sources: []
tags: [색인, 카탈로그]
---

# 위키 색인 (Index)

> 도메인 전체 조망은 [[overview|도메인 개요]]. 아래는 카테고리별 전체 페이지 목록(각 항목 한 줄 설명).
> 출처: 유튜브 재생목록 `PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3` 영상 25편 (2026-06-23 흡수) + 재생목록 외 웹 문서 (2026-07-18~). 취업/커리어 관련 페이지(개념 3·출처 3·분석 1)는 2026-07-12 별도 커리어 위키(career-llm-wiki)로 이관 — 이 위키는 기술 주제에 집중한다.

## Concepts
- [[concepts/harness-engineering|하네스 엔지니어링]] — 이 위키의 중심 개념(환경 설계 = 강제)
- [[concepts/prompt-engineering|프롬프트 엔지니어링]] — 진화 1단계("뭘 물어볼까")
- [[concepts/context-engineering|컨텍스트 엔지니어링]] — 진화 2단계("뭘 보여줄까")
- [[concepts/loop-engineering|루프 엔지니어링]] — 진화 4단계(반복 자동화), 최신 트렌드
- [[concepts/agentic-coding|에이전틱 코딩]] — 바이브 코딩과의 대비, 천장 vs 바닥
- [[concepts/developer-role-change|개발자 역할의 변화]] — 선수→감독, 일자리 논쟁
- [[concepts/claude-md|CLAUDE.md]] — 컨텍스트 파일. **핵심 모순(삭제 vs 3배)** 보존
- [[concepts/skills|스킬]] — 필요 시 로드되는 전문 지식 패키지
- [[concepts/subagents-agent-teams|서브에이전트 & 에이전트 팀]] — 병렬 오케스트레이션
- [[concepts/hooks|훅]] — 자동 검증·강제 메커니즘
- [[concepts/mcp|MCP]] — Model Context Protocol. 외부 도구 연결, 토큰 비용 주의
- [[concepts/dynamic-workflow|다이나믹 워크플로우]] — Deep Research/Ultra Code/Goal
- [[concepts/multi-model-workflow|멀티 모델 워크플로우]] — Codex 병행 교차검증, Opus+Sonnet 비용
- [[concepts/verification-automation|검증 자동화]] — 생성/검증 분리, 적대적 리뷰
- [[concepts/context-decay|컨텍스트 부패]] — 길어지면 잊고 조기 종료하는 현상
- [[concepts/on-device-ai|온디바이스 AI]] — Gemma 4로 API 비용 0
- [[concepts/llm-basics|LLM 기초]] — 트랜스포머·어텐션·RLHF
- [[concepts/infrastructure-as-code|코드형 인프라]] — IaC. 환경을 코드로 선언·강제하는 사상의 인프라 영역 선례
- [[concepts/dns-records|DNS 레코드]] — 웹/네트워크 인프라 기초. A·CNAME·MX·SPF 등 레코드 종류와 조회 도구
- [[concepts/hcl|HCL]] — Terraform 구성 언어 문법. 블록·인수·표현식, provider alias, 메타 인수

## Entities
- [[entities/claude-code|Claude Code]] — Anthropic의 에이전틱 코딩 CLI, 위키 전반의 중심 도구
- [[entities/anthropic|Anthropic]] — Claude/Claude Code 개발사
- [[entities/openai|OpenAI]] — Codex/GPT 개발사
- [[entities/codex|Codex]] — OpenAI 코딩 에이전트, Claude와 교차검증 짝
- [[entities/cursor|Cursor]] — AI 코딩 에디터/에이전트
- [[entities/vercel|Vercel]] — skills.sh 출시 주체
- [[entities/skills-sh|skills.sh]] — AI 에이전트용 스킬 패키지 매니저
- [[entities/google-gemma|구글 Gemma]] — 구글 온디바이스 모델(Gemma 4)
- [[entities/terraform|Terraform]] — HashiCorp의 멀티 클라우드 IaC 도구. Write-Plan-Apply 워크플로·state·HCL 상세
- [[entities/hashicorp|HashiCorp]] — 하시모토 공동창립, Terraform 제작사(IBM 계열)
- [[entities/armon-dadgar|아몬 다드가]] — HashiCorp 공동창립자, Terraform 소개의 얼굴
- [[entities/sentinel|Sentinel]] — HashiCorp의 정책 코드화(policy-as-code) 프레임워크
- [[entities/opa|OPA]] — Open Policy Agent, Sentinel의 벤더 중립적 오픈 대안
- [[entities/andrej-karpathy|안드레이 카파시]] — Karpathy 가이드라인/65줄 CLAUDE.md 저자(자막상 "André Capaci" 오인식)
- [[entities/boris-cherny|보리스 체르니]] — Claude Code 창시자, "거의 바닐라 세팅" 발언
- [[entities/mitchell-hashimoto|미첼 하시모토]] — HashiCorp 공동창립자, 하네스 용어 제시자(추정)
- [[entities/peter-steinberger|피터 슈타인버거]] — "프롬프팅 그만하라" 발언자(자막 기준)

## Sources (흡수 순서 — 1~25번 재생목록, 26번부터 재생목록 외)
- [[sources/youtube-HnvitMTkXro|#1 LLM 설명]] — 트랜스포머·어텐션·RLHF 기초(요약 버전)
- [[sources/youtube-dYXHJKnIT_I|#2 Claudebot 실전 워크플로우]] — E2E 테스트·폴링·보안
- [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]] — 독립 인스턴스 병렬 협업
- [[sources/youtube-jae2bVCCokc|#4 skills.sh]] — AI 스킬 패키지 매니저
- [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]] — 하네스 엔지니어링 개론
- [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]] — 컨텍스트 파일 무용론(모순①)
- [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]] — 컨텍스트 관리·워크플로우 총정리
- [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]] — 메모리 파일 제대로 쓰는 법(모순①)
- [[sources/youtube-JzB_GI7SS6g|#9 에이전트 10가지 팁]] — 주니어 개발자 관점
- [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]] — .claude/rules 조건부 분할
- [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]] — 하네스의 시대
- [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]] — 온디바이스 AI로 API 비용 제로
- [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]] — 9달러 vs 200달러
- [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]] — 하네스 공식 문서 해설(마구 비유)
- [[sources/youtube-uk4a5oER0SQ|#15 개발을 떠나는 이유]] — 개발자 역할 변화
- [[sources/youtube-oIAUbqpQ0lY|#16 2026 최악의 코더]] — AI 과신 경고
- [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]] — 신선한 컨텍스트 강조
- [[sources/youtube-jKjbXXBahiY|#18 주식 에이전트 팀]] — 말 한마디로 만드는 멀티 에이전트
- [[sources/youtube-gol5jv4wcfs|#19 65줄 CLAUDE.md]] — GitHub 10만 스타 카파시 원칙
- [[sources/youtube-f0hcByvsyjU|#20 코덱스 멀티 모델]] — Claude Code만 쓰면 망한다(feat. Codex)
- [[sources/youtube-6MYZ7fMhKPY|#21 바이브에서 에이전틱으로]] — 하네스 엔지니어링 전환 서사
- [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]] — 800시간 사용자의 추천 스킬
- [[sources/youtube-9fx2_1aTzq8|#23 다이나믹 기능 비교]] — 다이나믹 워크플로우 완벽 가이드
- [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]] — 낡은 하네스의 군살 빼기
- [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]] — 최신 트렌드
- [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]] — 2026-07-18 흡수, 재생목록 외 웹 문서. 코드형 인프라 개념 해설
- [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]] — 2026-07-19 흡수, 코어·언어·CLI 발췌 19페이지. Write-Plan-Apply·state·HCL·모듈·도입 4단계
- [[sources/tistory-inpa-dns-records|#28 DNS 레코드 종류]] — 2026-07-21 흡수, Inpa 블로그. DNS 레코드 종류·A vs CNAME·조회 도구
- [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]] — 2026-08-02 흡수, 실제 구성 파일 기준 자체 정리 노트. HCL 문법 12항목 + 명령 3개

## Analysis
- [[analysis/ai-coding-evolution|AI 코딩 패러다임의 진화]] — 프롬프트→컨텍스트→하네스→루프 4단계 진화 비교표
- [[analysis/claude-md-decision-guide|CLAUDE.md 결정 가이드]] — 모순①(삭제 vs 3배)의 실천 가이드화
- [[analysis/workflow-selection-guide|워크플로우 선택 가이드]] — 채팅/스킬/서브에이전트/배치/다이나믹/Goal 비교

---
title: 멀티 모델 워크플로우 (Codex 협업)
type: concept
created: 2026-06-23
updated: 2026-06-23
sources: [youtube-f0hcByvsyjU, youtube-hXlB1QstQ-Y, youtube-6MYZ7fMhKPY]
tags: [멀티모델, Codex, 코덱스, 모델조합, 비용절감, 적대적리뷰]
---

# 멀티 모델 워크플로우 (Codex 협업)

**멀티 모델 워크플로우**는 [[entities/claude-code|Claude Code]] 단독이 아니라 [[entities/codex|Codex(OpenAI)]] 등 다른 회사의 모델을 함께 띄워 서로의 실수를 잡아내는 작업 방식이다. 최근 Claude Code의 불확실성·가이드 미준수 문제, 그리고 2026년 2~3월의 일시적 성능 저하(엔트로픽이 사후 보고서로 출력 누락·메모리 초기화 등 버그 3건을 인정) 때문에 "한 모델만 믿는 건 위험하다"는 감각이 퍼지면서 확산됐다 (→ [[sources/youtube-f0hcByvsyjU]]).

## 왜 다른 모델을 병행하나

핵심 논리는 **"서로 다른 회사가 만든 모델은 서로 다른 곳에서 실수한다"**는 것이다. 같은 강사에게 배운 학생은 비슷한 문제를 틀리지만, 다른 강사에게 배운 학생을 데려오면 서로 놓친 부분을 잡아 준다는 비유로 설명된다 (→ [[sources/youtube-f0hcByvsyjU]]). Claude는 자기가 짠 코드를 자기 시각으로 검토하지만, Codex는 처음 보는 코드를 다른 시각으로 보기 때문에 보이지 않던 문제를 찾는다 — 자기 글은 오탈자를 못 잡고 남이 봐줘야 잡히는 것과 같다 (→ [[sources/youtube-f0hcByvsyjU]]). 이는 [[concepts/verification-automation|검증 자동화]]의 "생성/검증 분리" 원리와 같은 맥락이다.

## Codex 플러그인과 주요 기능

2026년 3월 말 OpenAI가 공식 플러그인 **코덱스 플러그인 CC**를 공개해, Claude Code 안에서 슬래시 커맨드 하나로 같은 프로젝트·같은 컨텍스트 안에서 Codex를 호출할 수 있게 됐다 (→ [[sources/youtube-f0hcByvsyjU]]). 설치 후 6개의 슬래시 커맨드가 생기며, 가장 많이 쓰는 두 가지는 다음과 같다 (→ [[sources/youtube-f0hcByvsyjU]]):

- **코덱스 리뷰(Codex Review)**: 결과물을 Codex에게 한 번 더 검토시키는 것. 실제 사례로, Claude로 만든 MCP 브릿지 코드를 리뷰시키자 종료 코드 처리 구멍, ANSI 이스케이프 문자 필터 누락(인젝션 위험), 경로 이중 적용 버그 등 3건이 추가로 잡혔다.
- **코덱스 레스큐(Codex Rescue)**: 막힌 자리에서 슬래시 커맨드로 Codex가 백그라운드에서 따로 파보게 하는 기능. 사이드바 리팩터링 사례에서 6분 35초 만에 엣지케이스 버그 4건(미설정 시 제출 버튼 무음 실패, 검증 건너뛰기, 뒤로 가기로 끊으면 복구 불가, 동시 요청 상태 덮어쓰기)을 찾았다.

주의: 코덱스 레스큐는 같은 파일만 반복해 읽고 결과를 내지 않는 무한 루프 버그가 있어, 5분 넘게 응답이 없으면 코덱스 캔슬로 끊고 다시 시도하라고 안내한다(아직 완성 단계 아님) (→ [[sources/youtube-f0hcByvsyjU]]).

## Opus + Sonnet 모델 조합과 비용 절감

Claude Code에는 `오퍼스 플랜(Opus Plan)` 모드가 있어 **플래닝은 Opus가, 실제 코드 구현은 Sonnet이** 자동으로 역할을 나눠 맡는다 (→ [[sources/youtube-f0hcByvsyjU]]). 근거는 비용 구조다:

- Opus는 똑똑하지만 비싸고, Sonnet은 적당히 똑똑하면서 훨씬 싸다 (→ [[sources/youtube-f0hcByvsyjU]]).
- 진짜 머리를 써야 하는 **설계 단계**는 전체 토큰의 약 **10~20%**에 불과하고, 나머지 **80%**는 함수 작성·테스트·임포트 정리 같은 실제 타이핑이라 Sonnet으로 충분하다 (→ [[sources/youtube-f0hcByvsyjU]]).
- 비용 비교: 전부 Opus로 돌리면 (자막상) 토큰당 약 1.5달러 수준이지만, 플랜만 Opus·구현은 Sonnet으로 가면 약 0.48달러로 떨어져 **거의 1/3 토막**(약 1/3 절감)이 난다(수치는 자막상 표기) (→ [[sources/youtube-f0hcByvsyjU]]). "설계도만 베테랑에게 맡기고 시공은 일반 작업장에 맡기는 것"에 비유된다.

## Codex 적대적 리뷰(Adversarial Review)

가장 강조된 패턴은 **플랜 단계에서의 Codex 적대적 리뷰**다 (→ [[sources/youtube-f0hcByvsyjU]]):

1. Opus에게 플랜을 시켜 마크다운 파일 하나로 정리한다(단일 기준점).
2. 바로 구현으로 넘어가지 않고, Codex에게 **그 플랜을 비판적으로** 검토시킨다 — 문법이 아니라 설계 자체를 의심(구조가 맞나, 캐싱 로직, 동시성, 데이터 유실 위험 등).
3. 지적 사항을 플랜에 반영한 뒤 구현하고, 끝나면 코덱스 리뷰로 한 번 더 돌린다.

한 사례에서 3라운드를 돌리자 인증 모델 누락, 셸 스크립트 처리 버그 등 14개 문제가 **플랜 단계에서** 잡혔다. 코드 짜기 전에 잡으면 수정 비용이 거의 없으므로 이 순서가 중요하다 (→ [[sources/youtube-f0hcByvsyjU]]). [[concepts/harness-engineering]] 영상에서도 "Claude Code와 Codex를 같이 쓰면 검증 작업의 성능이 크게 올라간다"고 보강된다 (→ [[sources/youtube-6MYZ7fMhKPY]]).

## 긴장③: Codex 병행 vs 보리스의 "바닐라 세팅"

이 주제에는 위키 전체의 핵심 긴장 중 하나가 걸려 있다.

- **Codex 병행을 권장**하는 입장: "Claude Code 단독으로 쓰면 망한다(doomed)"며 Codex를 보조로 함께 띄우거나 결과물을 Codex로 검토시키는 멀티 모델 워크플로우로 옮겨가야 한다고 본다 (→ [[sources/youtube-f0hcByvsyjU]]).
- **바닐라 세팅을 강조**하는 입장: [[entities/boris-cherny|보리스 체르니(Boris Cherny)]]는 X에서 "내 세팅은 놀랍게도 바닐라"라고 밝혔다. 자기가 만든 툴인데도 거의 커스텀하지 않고 있는 그대로 쓰며, "그 위에 뭘 더 쌓기 전에 기본을 먼저 파악하는 게 맞다"는 것이다 (→ [[sources/youtube-hXlB1QstQ-Y]]).

두 입장은 정면 대립처럼 보이지만 스코프가 다르다. 보리스의 "바닐라"는 **불필요한 스킬·하네스를 처음부터 잔뜩 깔지 말라**는 맥락(과한 초기 세팅 경계)이고, Codex 병행은 **단일 모델의 사각지대를 보완**하기 위한 검증 장치 추가다. 둘 다 "필요에 따라 자라나는 세팅이 가장 좋다"는 원칙과는 충돌하지 않는다. (자세한 화해 관점은 [[entities/boris-cherny]] 및 [[concepts/harness-engineering]] 참고)

## 관련 문서
- [[concepts/verification-automation]] — 생성/검증 분리, 적대적 리뷰의 상위 개념
- [[entities/codex]] — 협업 대상 모델
- [[entities/boris-cherny]] — "바닐라 세팅" 발언의 주인공
- [[concepts/harness-engineering]] — 인간 개입 최소화라는 같은 목표

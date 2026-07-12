---
title: "#25 루프 엔지니어링: 최신 트렌드"
type: source
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-z-3BRkxQ5GM]
tags: [루프엔지니어링, 하네스엔지니어링, 랄프루프, 메타프롬프팅, 완성도]
---

## 한 줄 요약
랄프(Ralph) 루프→[[concepts/harness-engineering]]→[[concepts/loop-engineering]]으로 이어지는 흐름을 정리하며, 루프 엔지니어링은 "대립이 아니라 중첩"이고 적합한 규모의 작업에서만 효율적이라고 안심시킨다 (→ [[sources/youtube-z-3BRkxQ5GM]]).

## 핵심 내용
- 세 개념의 순서: ① **랄프 루프**(가장 먼저, 롱러닝 에이전트 개념이 없던 시절 단순 무식하게 반복 실행) → ② [[concepts/harness-engineering]] → ③ [[concepts/loop-engineering]]. 핵심은 "대립이 아니라 중첩" (→ [[sources/youtube-z-3BRkxQ5GM]]).
- 랄프 루프 당시 핵심 문제는 "니들 인 헤이스택"·컨텍스트 디그라데이션([[concepts/context-decay]]): 문맥이 차면 성능↓. 그래서 태스크를 잘게 쪼개 결과만 디스크에 저장하고 새 컨텍스트로 다음 작업 → 0~10번 progress(완성도 아님)에 초점 (→ [[sources/youtube-z-3BRkxQ5GM]]).
- [[concepts/harness-engineering]]: 0→100 과정에서 "뭘 하고/하면 안 되는지"의 정의(스코프 제한). 골/울트라코드를 쓰면 어차피 하네스가 다이나믹하게 생기므로, 요즘은 오히려 디테일한 하네스를 직접 안 짜는 추세 ([[concepts/dynamic-workflow]]와 연결) (→ [[sources/youtube-z-3BRkxQ5GM]]).
- [[concepts/loop-engineering]]: "프롬프팅하는 나 자신을 AI로 대체". 단, 첫 프롬프트는 있어야 하고, **2번째·n번째 개선 프롬프트**를 줄여 완성도를 자동으로 올리는 것 → AGI처럼 무에서 유를 만드는 게 아니라 Act→Observe→Decide→Repeat 루프로 한 기능의 완성도를 끌어올리는 것 (→ [[sources/youtube-z-3BRkxQ5GM]]).
- 데모: 이미지를 순수 HTML 캔버스+JS로 모사하는 루프(유사도 90% 목표, 헤드리스 렌더링→비교→0~100 점수→비평을 review.json/state.json에 기록→반복). 23회 이터레이션에 걸쳐 고양이 그림 완성도가 크게 상승 (→ [[sources/youtube-z-3BRkxQ5GM]]).

## 주요 주장 / 데이터
- 인용: 피터 슈타인버거("오픈 클로드 창업자"로 자막 표기)와 Anthropic이 루프 엔지니어링을 논함 (→ [[sources/youtube-z-3BRkxQ5GM]], → [[entities/peter-steinberger]]).
- 인용: "보리스(bory/보리스 체니)"의 **"My job is loops"** — 내 일은 루프를 작성하는 것. 단, 직함이 자막상 불명확하므로 Claude Code를 만든 [[entities/boris-cherny]]로 연결(자막 오인식 가능) (→ [[sources/youtube-z-3BRkxQ5GM]]).
- 인용: 어떤 포스트의 "you shouldn't be prompting coding agents anymore" — 하지만 실제 서술은 Act/Observe/Decide/Repeat 반복이라 완전 무프롬프팅이 아님 (→ [[sources/youtube-z-3BRkxQ5GM]]).
- 핵심 경고: 루프 엔지니어링은 **모두에게 해당되지 않음**. 보리스 체니 같은 대규모 프로젝트(Claude Code급, 기능 간 유기적 융합 검증이 중요)에선 효율적이지만, 작은 사이드/MVP/PMF 탐색 프로젝트는 프론티어 모델이 좋아서 한 번에 끝낼 수 있어 루프가 오히려 토큰·시간 낭비 (→ [[sources/youtube-z-3BRkxQ5GM]]).
- 미래: 피터 슈타인버거 인용 "design your loops then" — 플리트(fleet=여러 에이전트 함대)로 루프를 디자인하게 되면 다시 [[concepts/harness-engineering]]으로 회귀. 추상화가 높아질 뿐 완전히 새로운 개념은 적다 (→ [[sources/youtube-z-3BRkxQ5GM]]).

## 기존 위키와의 연결
- 신규: [[concepts/loop-engineering]]를 가장 최신 트렌드로 도입(프롬프트→컨텍스트→하네스→루프 엔지니어링 진화의 마지막 단계). [[entities/peter-steinberger]]·랄프 루프 개념도 신규.
- 강화: [[concepts/harness-engineering]]("뭘 하면 안 되는지의 정의")와 [[concepts/dynamic-workflow]](동적 하네스 생성), [[concepts/context-decay]](니들 인 헤이스택)를 강화.
- 강화: [[entities/boris-cherny]]의 "My job is loops" 발언 — 단, 직함이 자막상 불명확(Boris Cheng/Vercel CEO 혼동)하므로 사실 교정 반영.

## 출처 정보
- raw: raw/youtube-z-3BRkxQ5GM.md
- URL: https://www.youtube.com/watch?v=z-3BRkxQ5GM
- 채널: 코드팩토리 (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3 (#25)
- 자막: 한국어 자동생성 (오탈자·인명 오인식 가능; "bory/보리스 체니"=[[entities/boris-cherny]], "피스타임버거/피터 사인바고"=[[entities/peter-steinberger]])

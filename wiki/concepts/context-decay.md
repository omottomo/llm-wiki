---
title: 컨텍스트 부패 (Context Decay)
type: concept
created: 2026-06-23
updated: 2026-06-23
sources: [youtube-6cr4PeilKJk, youtube-DrekqeDlO1w, youtube-z-3BRkxQ5GM, youtube-hXlB1QstQ-Y]
tags: [컨텍스트부패, 컨텍스트윈도우, 신선한컨텍스트, 세션관리, 하네스]
---

# 컨텍스트 부패 (Context Decay)

**컨텍스트 부패(Context Decay)**는 AI가 긴 작업 중 **컨텍스트 윈도우가 차오르면 일관성을 잃고 성능이 떨어지는** 현상이다. 작업이 길어져 한 번에 볼 수 있는 정보량(컨텍스트 창)이 꽉 차면, 앞에서 한 얘기를 잊어버리기 시작한다 (→ [[sources/youtube-DrekqeDlO1w]]). 책으로 치면 한 번에 펼쳐 볼 수 있는 페이지 수가 컨텍스트 창이며, 아무리 좋은 AI도 이 창을 넘어가면 내용을 못 본다 (→ [[sources/youtube-DrekqeDlO1w]]). 이는 [[concepts/harness-engineering|하네스 엔지니어링]]이 풀려는 두 핵심 문제 중 하나다(다른 하나는 규칙·울타리 문제).

## 두 가지 실패 패턴

엔트로픽 연구팀이 최전선 모델로 Claude.ai를 클론해 보라고 시켰을 때 두 가지 실패 패턴이 반복됐다 (→ [[sources/youtube-DrekqeDlO1w]], [[sources/youtube-6cr4PeilKJk]]):

1. **세션 간 기억 소실**: 모든 걸 한 번에 해결하려 달려들다 컨텍스트가 바닥나 절반만 구현된다. 다음 세션이 시작될 때 어디까지 했는지 기억이 없어 처음부터 다시 파악하느라 시간을 쓴다. 엔트로픽은 이를 "교대 근무 엔지니어가 이전 담당자가 뭘 했는지 전혀 모른 채 출근하는 것"에 비유했다 (→ [[sources/youtube-6cr4PeilKJk]]).
2. **조기 종료(컨텍스트 어어티)**: 하나의 대화 안에서 컨텍스트가 차오르면 일관성을 잃고, 할 일이 아직 남았는데도 "다 됐네" 하고 스스로 작업을 조기 종료한다 (→ [[sources/youtube-6cr4PeilKJk]], [[sources/youtube-DrekqeDlO1w]]).

## 니들 인 헤이스택 / 컨텍스트 디그라데이션

[[concepts/loop-engineering|루프 엔지니어링]] 영상에서는 이 현상을 **"니들 인 헤이스택(needle in a haystack)"** 시절의 **컨텍스트 디그라데이션** 문제로 회고한다: 문맥이 꽉 차면 퍼포먼스가 낮아진다는 것이다. 200K 컨텍스트 시절에 특히 심했고 지금은 옛날보다 많이 나아졌지만 여전히 유효하다 (→ [[sources/youtube-z-3BRkxQ5GM]]). 이 때문에 랄프 루프(Ralph Loop)에서는 작업을 잘게 쪼개, 매번 하나의 태스크 결과만 디스크에 저장해 컨텍스트를 최소화하고 새 에이전트를 띄워 **새로운 컨텍스트** 안에서 다음 작업을 하게 했다 — 같은 컨텍스트 안에서 계속 작업하는 것보다 빠르고 효율적이기 때문이다 (→ [[sources/youtube-z-3BRkxQ5GM]]). 이 "잘게 쪼개 새 컨텍스트로 넘기는" 발상은 ReAct 루프(Reason-Act-Observe-Decide-Repeat)와 루프 엔지니어링의 토대가 된다 (→ [[sources/youtube-z-3BRkxQ5GM]]).

## "신선한 컨텍스트가 비대한 컨텍스트를 이긴다"

실무에서 가장 중요한 원칙은 **"신선한 컨텍스트가 비대한 컨텍스트를 이긴다"**이다 (→ [[sources/youtube-hXlB1QstQ-Y]]). 클로드에서는 주고받은 메시지·파일·실행한 명령어가 전부 컨텍스트에 쌓이고, 채워질수록 성능이 떨어진다. 따라서 할 일은 정보를 최대한 많이 주는 게 아니라 **정말 필요한 정보만 남기고 나머지를 쳐내는 것**이다. 관련 없는 정보가 많을수록 클로드가 잘못된 방향으로 빠진다 (→ [[sources/youtube-hXlB1QstQ-Y]]). [[concepts/claude-md|CLAUDE.md]]도 클로드는 약 80%만 따른다고 알려져 있어, 길수록 중요한 규칙이 무시될 가능성이 높으므로 대략 150~200줄로 끝내는 게 좋다 (→ [[sources/youtube-hXlB1QstQ-Y]]).

## 컨텍스트 부패를 막는 하네스/세션 관리

- **CLAUDE.md(컨텍스트 파일)**: 새 세션마다 가장 먼저, 매번 읽히기 때문에 컨텍스트가 꽉 차서 앞 내용을 잊어버려도 항상 다시 읽힌다. 세션마다 리셋되는 기억을 [[concepts/claude-md|CLAUDE.md]]가 잡아준다 — "신규 입사자가 첫날 반드시 읽는 온보딩 문서" (→ [[sources/youtube-DrekqeDlO1w]], [[sources/youtube-6cr4PeilKJk]]).
- **서브에이전트로 컨텍스트 절약**: 리서치는 하이쿠 같은 빠른 [[concepts/subagents-agent-teams|서브에이전트]]가 중요한 정보만 취합해 메인 에이전트에 넘긴다 — 소스 전체를 메인이 다 보면 그것만으로 컨텍스트 윈도우가 터지기 때문 (→ [[sources/youtube-fInMcawbKng]]).
- **세션 관리 기법**: 실패한 시도 기록이 컨텍스트에 남아 영향을 주는 것을 막기 위해 **리와인드**(ESC 두 번 → 이전 지점 이후 기록 삭제)로 깨끗한 상태에서 다시 시도하고, `/clear`로 세션 초기화, `/compact`로 요약(이때 "이번엔 A에 집중하고 B는 버려"처럼 요약 방향을 직접 지시)하는 습관이 권장된다 (→ [[sources/youtube-hXlB1QstQ-Y]]).

## 관련 문서
- [[concepts/harness-engineering]] — 컨텍스트 부패를 푸는 상위 개념
- [[concepts/context-engineering]] — 컨텍스트 관리의 큰 틀
- [[concepts/loop-engineering]] — 잘게 쪼개 새 컨텍스트로 넘기는 루프
- [[concepts/claude-md]] — 세션마다 다시 읽히는 컨텍스트 파일

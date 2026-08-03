---
title: CLAUDE.md (컨텍스트 파일)
type: concept
created: 2026-06-23
updated: 2026-08-03
sources: [youtube-c7_ANA1NiS0, youtube-cZ8_Dkk_Ce0, youtube-gol5jv4wcfs, youtube-FBv8hK_DtJ8, youtube-DCsv0rKKrN4, youtube-hXlB1QstQ-Y, youtube-BssPGKsP60s]
tags: [클로드코드, 컨텍스트엔지니어링, 메모리파일, 하네스엔지니어링]
---
# CLAUDE.md (컨텍스트 파일)

## 한눈에 요약

- Claude Code가 프로젝트를 열 때마다 자동으로 읽는 **규칙 메모 파일**이다. 기술 스택, 코딩 규칙, 하지 말아야 할 일을 적어 둔다.
- 강제가 아니라 참고다. 실무에서 **80% 정도만 지켜진다**고 보면 된다.
- "품질이 2~3배 좋아진다"와 "잘못 쓰면 오히려 성능이 떨어진다"가 **둘 다 사실**이다. 갈리는 지점은 길이와 구체성이다.
- 잘 쓰는 법은 짧게, 검증 가능하게, 실수할 때마다 한 줄씩. 처음부터 완벽하게 쓰려 하지 않는 게 요령이다.
- 규칙이 불어나면 파일을 쪼개고, 지금 필요한 규칙만 그때그때 불러오게 만든다.

## 이 파일이 왜 필요한가

AI에게 같은 프로젝트 사정을 매번 설명하는 건 사람이나 AI나 낭비다. 그래서 나온 게 이 파일이다.

`CLAUDE.md`(Codex 등에서는 `AGENTS.md`)는 Claude Code가 프로젝트에서 지켜야 할 규칙과 맥락을 적어 두는 메모리 파일이다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). [[concepts/harness-engineering|하네스 엔지니어링]]의 가장 기본이 되는 구성 요소이며 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]), [[concepts/context-engineering|컨텍스트 엔지니어링]]의 첫걸음으로 평가된다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).

## 작동 원리

- Claude Code를 실행하면 가장 먼저 이 파일이 있는지 확인하고 통째로 읽으며, 몇 세션마다 다시 읽는다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- 로딩 순서상 시스템 프롬프트 다음, 사용자 프롬프트보다 먼저 읽히는 "사전 지시서" 역할을 한다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- 컨텍스트가 꽉 차서 앞 내용을 잊어버려도 이 파일은 항상 다시 읽힌다. 그래서 세션 간 기억 소실([[concepts/context-decay|컨텍스트 부패]]) 문제를 잡아준다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]] 참조 — [[concepts/harness-engineering|하네스 엔지니어링]]에 정리).

여기서 헷갈리기 쉬운 대목이 하나 있다. **이 파일은 강제가 아니라 맥락이다.**

> 공식 문서상 CLAUDE.md는 시스템 프롬프트가 아니라 사용자 메시지로 전달된다. Claude가 읽고 따르려 하지만, 모호하거나 서로 충돌하는 지시는 100% 준수가 보장되지 않는다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). 실무상 약 80% 정도만 따른다고 알려져 있다 (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).

그래서 반드시 지켜야 하는 규칙이라면 이 파일에 적는 것만으로는 부족하다. 아래 [[concepts/hooks|훅]] 쪽이 그 역할을 맡는다.

## 핵심 모순 ① — "지워라" vs "품질 2~3배"

이 위키의 핵심 긴장 중 하나다. **두 주장을 모두 보존한다 (어느 쪽도 삭제하지 않음).**

| | 입장 A — "지워라" | 입장 B — "품질 2~3배" |
|---|---|---|
| 주장 | 잘못 쓴 컨텍스트 파일은 없느니만 못하다 | 가장 효과가 큰 지렛대다 |
| 근거 | AI가 자동 생성한 파일로 성공률이 오히려 하락 | 검증 규칙을 넣으면 결과 품질 2~3배 |
| 비용 | 추론 비용 20%↑ | 한 번 잘 써두면 계속 재사용 |
| 출처 | (→ [[sources/youtube-c7_ANA1NiS0\|#6 CLAUDE.md를 지워라]]) | (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-gol5jv4wcfs\|#19 65줄 CLAUDE.md]]) |

### 입장 A — "CLAUDE.md를 (잘못 쓰면) 지워라"

- "Do repository-level context files help coding agents?"라는 논문을 소개한다. LRM(대형 추론 모델)이 자동 생성한 컨텍스트 파일은 아무것도 주지 않았을 때보다 성공률이 오히려 떨어졌다. Agent Bench 평균 약 2%↓, SW-Bench Lite 약 0.5%↓다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- 추론 비용도 20% 이상 증가했다. GPT 5.2는 컨텍스트 파일 처리에 리즈닝 토큰을 22% 더, 5.1 mini는 14% 더 썼다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- 컨텍스트 파일이 있으면 첫 응답까지 단계가 늘고 도구 호출도 많아진다. 코드를 불필요하게 넓게 뒤지느라 에너지를 낭비한 것이다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).

> 다만 같은 논문에서 **사람이 직접 작성한** 컨텍스트 파일은 유의미한 성공률 상승(평균 약 19% 증가)을 보였다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]). 문제는 파일의 존재가 아니라 누가 어떻게 썼느냐였다.

### 입장 B — "CLAUDE.md만으로 코딩 품질이 3배(2~3배) 달라진다"

- CLAUDE.md는 Claude Code에서 가장 높은 레버리지 포인트다. 한 번 잘 써두면 지렛대처럼 효과가 몇 배로 커진다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- [[entities/boris-cherny|보리스 체르니]]는 Claude가 작업 결과를 스스로 검증할 수 있게 해 주면 최종 결과 품질이 2~3배 향상된다고 말했다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]], 동일 증언이 → [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]에도 등장).
- [[entities/andrej-karpathy|안드레이 카파시]]에서 출발한 65줄짜리 CLAUDE.md는 깃허브에서 10만 개 넘는 스타를 받았다 (→ [[sources/youtube-gol5jv4wcfs|#19 65줄 CLAUDE.md]]).

### 화해 — 결국 "어떻게 쓰느냐"의 문제

두 입장은 충돌이 아니다. 각자 다른 CLAUDE.md를 두고 말하고 있을 뿐이다.

- 입장 A가 때리는 대상은 **장황하고 불필요한 규칙**이다. 문서처럼 꽉꽉 채운 파일, 지금 작업과 무관한 컨텍스트 같은 것들이다. [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]] 영상도 "아예 없애라는 뜻은 전혀 아니고, 잘못 작성했을 때의 악영향에 가까운 논문"이라고 명시한다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- 입장 B와 공식 권장이 가리키는 것은 **짧고(150~200줄/단어), 검증 가능하며, 도메인 용어가 정의된 최소 규칙**이다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- 즉 "사람이 작성한 최소·검증 가능한 규칙"은 양쪽 모두에서 효과적이라는 점에서 일치한다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]·[[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).

쓸까 말까부터 어떻게 쓸까까지 순서대로 정리한 실무 절차는 [[analysis/claude-md-decision-guide|CLAUDE.md 결정 가이드]]에 따로 있다.

## 좋은 CLAUDE.md 작성 원칙

- **길이** — 공식 문서는 200줄 이하를 권장하고, 너무 길어지면 과감히 삭제하라고 가이드한다. 300줄이 넘으면 중요한 규칙이 노이즈에 묻혀 무시될 수 있다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). 대략 150~200단어/줄 안에서 끝내는 게 좋다 (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- **구체성** — "깔끔한 코드를 작성하라" 같은 모호한 지시는 통하지 않는다. "함수는 30줄 이하", "새 파일 만들기 전 확인"처럼 Claude 스스로 지켰는지 확인할 수 있는 문장으로 써야 한다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- **검증 규칙(최고 레버리지)** — Claude가 스스로 결과를 검증할 방법을 규칙으로 정해 두면 구현→빌드→에러 시 자가 수정 루프가 자동으로 돈다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). 자세한 건 [[concepts/verification-automation|검증 자동화]]에 있다.
- **도메인 용어 정의** — "주문" vs "주문 항목"처럼 헷갈릴 비즈니스 용어를 적어 두면 결과가 크게 달라진다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- **빈 파일에서 시작** — 처음부터 완벽하게 쓰려 하지 말고, Claude가 실수할 때마다 한 줄씩 추가한다. [[entities/boris-cherny|보리스 체르니]]도 팀에서 Claude가 실수하면 CLAUDE.md에 한 줄을 추가한다고 했다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- **팀 공유 학습 시스템** — CLAUDE.md를 git에 커밋해 PR 리뷰로 규칙을 머지하면 팀 전원이 같은 실수를 반복하지 않게 된다 ([[entities/boris-cherny|보리스 체르니]]의 실제 팀 방식) (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).

## 오토 메모리 (자동 메모리, `/memory`)

CLAUDE.md를 사람이 적는 규칙집이라고 하면, 오토 메모리는 Claude가 스스로 적는 업무 일지다.

- "이 프로젝트는 React를 쓴다", "이 사용자는 한국어 주석을 좋아한다" 같은 내용을 세션 중에 자동 기록한다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- 처음 **200줄**까지만 메모리에 로드된다. 200줄이 넘으면 Claude가 알아서 상세 내용을 별도 파일로 분리하고, 그 파일은 시작할 때 다 읽지 않고 필요할 때만 찾아 읽는다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- `/memory` 명령으로 확인·편집할 수 있다. "기억해 줘"라고 프롬프트하면 저장된다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

둘을 어떻게 나눠 쓸지도 정리되어 있다. 개인 메모리는 오토 메모리(`memory.md`)에, 팀이 공유할 지식은 명시적으로 `CLAUDE.md`에 쓰는 게 권장 분담이다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

## 모듈식 분리 — Lazy Loading과 `.claude/rules`

프로젝트가 커지면 규칙이 쌓인다. 그러면 지금 필요한 규칙이 무관한 규칙들 사이에 묻힌다. 한 모노레포(여러 프로젝트를 저장소 하나에 모아 둔 구조)에서는 CLAUDE.md가 47,000단어까지 불어난 사례도 있다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]).

해결책은 하나로 모인다. **필요한 규칙만 필요한 시점에 불러오는 것**이다.

### 참조(import)와 Lazy Loading

CLAUDE.md에는 규칙과 참조만 두고, 상세 내용은 별도 마크다운 파일로 뺀다. API 스펙 50개나 DB 스키마 같은 것들이다. `@` 기호로 기존 문서를 참조해 두면 Claude가 필요할 때만 그 파일을 읽어 컨텍스트 윈도우(한 번에 볼 수 있는 분량)를 아낀다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]·[[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).

### `.claude/rules` + 프론트매터 조건부 로딩

`.claude/rules/` 하위에 주제별 파일을 두는 방식이다. 각 파일 맨 위 프론트매터(`---`로 감싼 설정 영역)에 적용 패턴을 지정한다. 예를 들어 `src/api/**/*.ts`라고 적으면 그 경로를 작업할 때만 규칙이 자동으로 로드된다. 테스트 파일엔 테스트 규칙만, API 파일엔 API 규칙만 들어가게 되는 셈이다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]).

실제로 쓰는 오픈소스도 있다. trigger.dev는 DB 세이프티 규칙에, CockroachDB는 Go 파일 개인정보 마스킹 규칙에 이 방식을 쓴다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]).

### 폴더별 CLAUDE.md

하위·상위 디렉터리에 별도 CLAUDE.md를 두는 방법이다. `apps/api/CLAUDE.md`, `web/CLAUDE.md` 식으로 두면 해당 폴더를 작업할 때 그 폴더의 파일만 읽힌다. 루트 파일이 비대해지는 걸 막아 준다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]·[[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]).

쉽게 말하면 핵심은 파일을 쪼개는 것 자체가 아니다. 불필요한 규칙이 Claude의 주의를 뺏지 않도록 "필요한 시점에만 불러오게" 설계하는 것이다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]).

## 함께 읽기

- [[concepts/hooks|훅]] — CLAUDE.md가 "부탁"이라면 훅은 "강제"다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]] 참조).
- [[concepts/skills|스킬]] — [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]] 영상은 CLAUDE.md에 많이 쓰기 싫어 문서와 체크 항목을 전부 스킬로 옮긴다고 했다. 작업별로 필요한 컨텍스트만 주입하는 대안이다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- [[analysis/claude-md-decision-guide|CLAUDE.md 결정 가이드]] — 위 모순을 "쓸까 말까 → 어떻게 쓸까" 절차로 푼 실무 가이드.
- [[concepts/harness-engineering|하네스 엔지니어링]] — 이 파일이 첫 번째 구성 요소로 들어가는 큰 그림.
- [[concepts/context-engineering|컨텍스트 엔지니어링]] · [[concepts/context-decay|컨텍스트 부패]] · [[concepts/verification-automation|검증 자동화]].

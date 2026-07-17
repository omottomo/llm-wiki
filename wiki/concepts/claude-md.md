---
title: CLAUDE.md (컨텍스트 파일)
type: concept
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-c7_ANA1NiS0, youtube-cZ8_Dkk_Ce0, youtube-gol5jv4wcfs, youtube-FBv8hK_DtJ8, youtube-DCsv0rKKrN4, youtube-hXlB1QstQ-Y, youtube-BssPGKsP60s]
tags: [클로드코드, 컨텍스트엔지니어링, 메모리파일, 하네스엔지니어링]
---
# CLAUDE.md (컨텍스트 파일)

`CLAUDE.md`(Codex 등에서는 `AGENTS.md`)는 Claude Code가 프로젝트에서 지켜야 할 규칙과 맥락을 적어 두는 메모리 파일이다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). [[concepts/harness-engineering|하네스 엔지니어링]]의 가장 기본이 되는 구성 요소이며 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]), [[concepts/context-engineering|컨텍스트 엔지니어링]]의 첫걸음으로 평가된다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).

## 작동 원리
- Claude Code를 실행하면 가장 먼저 이 파일이 있는지 확인하고 통째로 읽으며, 몇 세션마다 다시 읽는다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- 로딩 순서상 시스템 프롬프트 다음, 사용자 프롬프트보다 먼저 읽히는 "사전 지시서" 역할을 한다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- 단, 강제가 아니라 맥락이다. 공식 문서상 CLAUDE.md는 시스템 프롬프트가 아니라 사용자 메시지로 전달되며, Claude가 읽고 따르려 하지만 모호하거나 충돌하는 지시는 100% 준수가 보장되지 않는다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). 실무상 약 80% 정도만 따른다고 알려져 있다 (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- 컨텍스트가 꽉 차서 앞 내용을 잊어버려도 이 파일은 항상 다시 읽히기 때문에, 세션 간 기억 소실([[concepts/context-decay|컨텍스트 부패]]) 문제를 잡아준다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]] 참조 — [[concepts/harness-engineering|하네스 엔지니어링]]에 정리).

## 핵심 모순 ① — "지워라" vs "품질 2~3배"
이 위키의 핵심 긴장 중 하나로, **두 주장을 모두 보존한다 (어느 쪽도 삭제하지 않음).**

**입장 A — "CLAUDE.md를 (잘못 쓰면) 지워라"** (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]])
- "Do repository-level context files help coding agents?"라는 논문을 소개하며, LRM(LLM)이 자동 생성한 컨텍스트 파일은 아무것도 주지 않았을 때보다 오히려 작업 성공률을 떨어뜨렸다(Agent Bench 평균 약 2%↓, SW-Bench Lite 약 0.5%↓) (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- 추론 비용도 20% 이상 증가했다. GPT 5.2는 컨텍스트 파일 처리에 리즈닝 토큰을 22% 더, 5.1 mini는 14% 더 썼다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- 컨텍스트 파일이 있으면 첫 인터랙션까지 스텝이 더 늘고 툴 사용(tool use)이 더 많아져, 코드를 불필요하게 넓게 탐색하느라 에너지를 낭비했다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- 단, 같은 논문에서 **사람이 직접 작성한** 컨텍스트 파일은 유의미한 성공률 상승(평균 약 19% 증가)을 보였다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).

**입장 B — "CLAUDE.md만으로 코딩 품질이 3배(2~3배) 달라진다"** (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-gol5jv4wcfs|#19 65줄 CLAUDE.md]])
- CLAUDE.md는 Claude Code에서 가장 높은 레버리지 포인트로, 한 번 잘 써두면 지렛대처럼 효과가 몇 배로 커진다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- [[entities/boris-cherny|보리스 체르니]]는 Claude가 작업 결과를 스스로 검증할 수 있게 해 주면 최종 결과 품질이 2~3배 향상된다고 말했다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]], 동일 증언이 → [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]에도 등장).
- [[entities/andrej-karpathy|안드레이 카파시]]에서 출발한 65줄짜리 CLAUDE.md는 깃허브에서 10만 개 넘는 스타를 받았다 (→ [[sources/youtube-gol5jv4wcfs|#19 65줄 CLAUDE.md]]).

**화해(reconciliation):** 두 입장은 충돌이 아니라 **"어떻게 쓰느냐"**의 문제로 수렴한다.
- 입장 A의 비판 대상은 **장황하고 불필요한 규칙**(문서처럼 꽉꽉 채운 CLAUDE.md, 지금 작업과 무관한 컨텍스트)이다. #6 영상도 "CLAUDE.md를 아예 없애라는 뜻은 전혀 아니고, 잘못 작성했을 때의 악영향에 가까운 논문"이라고 명시한다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- 입장 B/공식 권장은 **짧고(150~200줄/단어), 검증 가능하며, 도메인 용어가 정의된 최소 규칙**이다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- 즉 "사람이 작성한 최소·검증 가능한 규칙"은 양쪽 모두에서 효과적이라는 점에서 일치한다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]·[[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- 이 모순을 실무 의사결정 절차(쓸까 말까 → 어떻게 쓸까)로 정리한 가이드는 [[analysis/claude-md-decision-guide|CLAUDE.md 결정 가이드]] 참조.

## 좋은 CLAUDE.md 작성 원칙
- **길이:** 공식 문서는 200줄 이하를 권장하며, 너무 길어지면 과감히 삭제하라고 가이드한다. 300줄이 넘으면 중요한 규칙이 노이즈에 묻혀 무시될 수 있다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). 대략 150~200단어/줄 안에서 끝내는 게 좋다 (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- **구체성:** "깔끔한 코드를 작성하라" 같은 모호한 지시는 통하지 않는다. "함수는 30줄 이하", "새 파일 만들기 전 확인" 등 Claude 스스로 검증 가능한 구체적 지시를 써야 한다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- **검증 규칙(최고 레버리지):** Claude가 스스로 결과를 검증할 방법을 규칙으로 정해 두면, 구현→빌드→에러 시 자가 수정 루프가 자동으로 돈다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). [[concepts/verification-automation|검증 자동화]] 참조.
- **도메인 용어 정의:** "주문" vs "주문 항목"처럼 헷갈릴 비즈니스 용어를 적어 두면 결과가 크게 달라진다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- **빈 파일에서 시작:** 처음부터 완벽하게 쓰려 하지 말고, Claude가 실수할 때마다 한 줄씩 추가한다. [[entities/boris-cherny|보리스 체르니]]도 팀에서 Claude가 실수하면 CLAUDE.md에 한 줄을 추가한다고 했다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- **팀 공유 학습 시스템:** CLAUDE.md를 git에 커밋해 PR 리뷰로 규칙을 머지하면, 팀 전원이 같은 실수를 반복하지 않게 된다 ([[entities/boris-cherny|보리스 체르니]]의 실제 팀 방식) (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).

## 오토 메모리 (자동 메모리, `/memory`)
- 오토 메모리는 Claude가 세션 중 스스로 적는 "업무 일지"다. "이 프로젝트는 React를 쓴다", "이 사용자는 한국어 주석을 좋아한다" 같은 내용을 자동 기록한다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- 처음 **200줄**까지만 메모리에 로드되고, 200줄이 넘으면 Claude가 알아서 상세 내용을 별도 파일로 분리한다. 분리된 파일은 시작 시 모두 읽지 않고 필요할 때만 찾아 읽는다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- `/memory` 명령으로 확인·편집할 수 있다. "기억해 줘"라고 프롬프트하면 저장된다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
- 권장 분담: 개인 메모리는 오토 메모리(`memory.md`)에, 팀 공유 지식은 명시적으로 `CLAUDE.md`에 작성한다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

## 모듈식 분리 — Lazy Loading과 `.claude/rules`
프로젝트가 커지면 규칙이 쌓이면서 지금 필요한 규칙이 무관한 규칙들 사이에 묻힌다(한 모노레포에서 CLAUDE.md가 47,000단어까지 불어난 사례) (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]). 해결책은 "필요한 규칙만 필요한 시점에 불러오는 것":

- **참조(import)·Lazy Loading:** CLAUDE.md에는 규칙과 참조만 두고 상세 내용(API 스펙 50개, DB 스키마 등)은 별도 마크다운 파일로 분리한다. `@` 기호로 기존 문서를 참조하면 Claude가 필요할 때만 해당 파일을 읽어 컨텍스트 윈도우를 아낀다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]·[[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
- **`.claude/rules` + 프론트매터 조건부 로딩:** `.claude/rules/` 하위에 주제별 파일을 두고, 각 파일 상단 프론트매터(`---`로 감싼 부분)에 적용 패턴(예: `src/api/**/*.ts`)을 지정하면, 해당 디렉터리/파일을 작업할 때만 그 규칙이 자동 로드된다. 테스트 파일엔 테스트 규칙만, API 파일엔 API 규칙만 들어가게 할 수 있다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]). 실제 오픈소스(trigger.dev — DB 세이프티 규칙, CockroachDB — Go 파일 개인정보 마스킹 규칙)가 이 방식을 쓴다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]).
- **폴더별 CLAUDE.md:** 하위/상위 디렉터리에 별도 CLAUDE.md를 두면(예: `apps/api/CLAUDE.md`, `web/CLAUDE.md`) 해당 폴더 작업 시 그 폴더의 CLAUDE.md만 읽혀 루트 파일의 비대화를 막는다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]·[[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]).

핵심은 단순히 파일을 쪼개는 게 아니라, 불필요한 규칙이 Claude의 주의를 뺏지 않게 "필요한 시점에만 불러오도록 설계"하는 것이다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]).

## 연결
- [[concepts/skills|스킬]] — #6 영상은 CLAUDE.md에 많은 내용을 쓰기 싫어 문서·체크 항목을 전부 스킬로 옮긴다고 했다. 작업별로 필요한 컨텍스트만 주입하는 대안 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- [[concepts/hooks|훅]] — CLAUDE.md가 "부탁"이라면 훅은 "강제"다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]] 참조).
- [[concepts/harness-engineering|하네스 엔지니어링]], [[concepts/context-engineering|컨텍스트 엔지니어링]], [[concepts/context-decay|컨텍스트 부패]], [[concepts/verification-automation|검증 자동화]].

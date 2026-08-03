---
title: "분석 — CLAUDE.md 결정 가이드: 쓸까 말까, 어떻게 쓸까"
type: analysis
created: 2026-06-23
updated: 2026-08-02
sources: [youtube-c7_ANA1NiS0, youtube-cZ8_Dkk_Ce0, youtube-gol5jv4wcfs, youtube-FBv8hK_DtJ8, youtube-DCsv0rKKrN4, youtube-hXlB1QstQ-Y]
tags: [분석, 클로드md, 의사결정, 모순]
---

# 분석 — CLAUDE.md 결정 가이드: 쓸까 말까, 어떻게 쓸까

이 글은 "AI에게 줄 규칙 파일을 아예 쓰지 말라"는 주장과 "잘 쓰면 결과 품질이 몇 배 좋아진다"는 주장이 정면으로 부딪히는 문제를 다룬다. 양쪽 근거를 나란히 놓고 보면 다툼의 진짜 쟁점은 쓸지 말지가 아니라 무엇을 어떻게 쓰느냐로 좁혀진다. 결론은 어느 쪽도 버리지 않는 것이다 — AI가 자동으로 만들어 낸 장황한 규칙 파일은 해롭고, 사람이 직접 고른 짧고 검증 가능한 규칙은 도움이 된다.

이 페이지는 이 위키의 **모순①**([[concepts/claude-md|CLAUDE.md]]에 기록된 "CLAUDE.md를 지워라" vs "CLAUDE.md로 품질 2~3배")을 실무 의사결정 가이드로 바꾼 것이다. **두 입장 중 어느 쪽도 버리지 않는다.** 둘은 충돌이 아니라 "어떤 CLAUDE.md를, 어떻게 쓰느냐"의 문제로 수렴하기 때문이다.

## 1. 양측 요약표

| 구분 | "지워라 / 조심하라" ([[sources/youtube-c7_ANA1NiS0\|#6 CLAUDE.md를 지워라]]) | "품질 2~3배" ([[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]] · [[sources/youtube-gol5jv4wcfs\|#19 65줄 CLAUDE.md]]) |
|---|---|---|
| 핵심 주장 | 잘못 쓴 컨텍스트 파일은 안 주느니만 못하다 | 잘 쓴 CLAUDE.md는 최고 레버리지 포인트다 |
| 근거 1 | LLM이 **자동 생성한** 컨텍스트 파일은 작업 성공률을 떨어뜨림 (Agent Bench 평균 약 2%↓, SW-Bench Lite 약 0.5%↓) (→ [[sources/youtube-c7_ANA1NiS0\|#6 CLAUDE.md를 지워라]]) | Claude가 결과를 스스로 검증하게 해 주면 최종 품질 2~3배 향상 ([[entities/boris-cherny\|보리스 체르니]] 증언) (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-hXlB1QstQ-Y\|#17 800시간 9가지 팁]]) |
| 근거 2 | 추론 비용 20%+ 증가 — GPT 5.2는 리즈닝 토큰 **+22%**, 5.1 mini는 **+14%** (→ [[sources/youtube-c7_ANA1NiS0\|#6 CLAUDE.md를 지워라]]) | [[entities/andrej-karpathy\|안드레이 카파시]]의 65줄짜리 CLAUDE.md가 깃허브 스타 10만+ 획득 (→ [[sources/youtube-gol5jv4wcfs\|#19 65줄 CLAUDE.md]]) |
| 근거 3 | 첫 인터랙션까지 스텝·툴 사용이 늘어 코드를 불필요하게 넓게 탐색, 에너지 낭비 (→ [[sources/youtube-c7_ANA1NiS0\|#6 CLAUDE.md를 지워라]]) | CLAUDE.md는 한 번 잘 써두면 지렛대처럼 효과가 몇 배로 커지는 지점 (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]) |
| 결정적 단서 | **같은 논문에서 사람이 직접 작성한** 컨텍스트 파일은 성공률 평균 약 **19%↑** (→ [[sources/youtube-c7_ANA1NiS0\|#6 CLAUDE.md를 지워라]]) | 권장은 짧고(150~200줄) 구체적·검증 가능한 최소 규칙 (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-hXlB1QstQ-Y\|#17 800시간 9가지 팁]]) |

## 2. 화해 명제

두 입장은 같은 곳을 가리킨다.

- **[[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]가 비판하는 대상은 "CLAUDE.md 그 자체"가 아니다.** 비판 대상은 ① 자동 생성된, ② 장황하고 불필요한, ③ 지금 작업과 무관한 컨텍스트다. [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]] 영상도 "CLAUDE.md를 아예 없애라는 뜻은 전혀 아니고, 잘못 작성했을 때의 악영향에 가까운 논문"이라고 명시한다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]).
- **[[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]] · [[sources/youtube-gol5jv4wcfs|#19 65줄 CLAUDE.md]]가 권장하는 대상은 "사람이 수기로 쓴 최소·검증 가능한 규칙"이다.** 짧고(150~200줄), 도메인 용어가 정의되어 있으며, Claude가 스스로 검증할 수 있는 형태 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- **결론:** "사람이 작성한 최소·검증 가능한 규칙"은 [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]의 논문(사람 작성 시 +19%)과 [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]/[[sources/youtube-gol5jv4wcfs|#19 65줄 CLAUDE.md]] 양쪽 모두에서 효과적이다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]·[[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). 즉 진짜 권장은 **"CLAUDE.md를 둬라, 단 자동생성·장황함을 피하고 짧게·검증가능하게·수기로 점진 축적하라"**다.

## 3. 실천 가이드 (플로우)

### A. 언제 CLAUDE.md를 두는가
1. **반복되는 실수가 보일 때** 둔다. 빈 파일에서 시작해 Claude가 실수할 때마다 한 줄씩 추가한다 ([[entities/boris-cherny|보리스 체르니]] 팀 방식) (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). 처음부터 완벽하게 채우려 하지 않는다.
2. **도메인 용어가 헷갈릴 때** 둔다. "주문" vs "주문 항목"처럼 비즈니스 용어를 정의해 두면 결과가 크게 달라진다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).
3. **검증 규칙이 필요할 때** 둔다. Claude가 구현→빌드→에러 시 자가 수정 루프를 스스로 돌게 하는 규칙이 최고 레버리지다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]). [[concepts/verification-automation|검증 자동화]] 참조.
4. **팀 공유가 필요할 때** 둔다. git에 커밋해 PR 리뷰로 규칙을 머지하면 팀 전원이 같은 실수를 반복하지 않는다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]).

### B. 무엇을 넣고 무엇을 빼는가

| 넣어라 (✅) | 빼라 (❌) |
|---|---|
| 검증 규칙 ("빌드/테스트 통과까지 자가 수정") (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]) | LLM이 자동 생성한 장황한 컨텍스트 (→ [[sources/youtube-c7_ANA1NiS0\|#6 CLAUDE.md를 지워라]]) |
| 구체적·검증 가능한 지시 ("함수 30줄 이하", "새 파일 만들기 전 확인") (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]) | "깔끔한 코드를 작성하라" 같은 모호한 지시 (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]) |
| 도메인 용어 정의 (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]) | 지금 작업과 무관한 API 스펙·DB 스키마 전부 (→ [[sources/youtube-DCsv0rKKrN4\|#7 메타 엔지니어 실전편]]) |
| 팀 공유 규칙 (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]) | 300줄 넘는 분량 — 중요한 규칙이 노이즈에 묻힌다 (→ [[sources/youtube-cZ8_Dkk_Ce0\|#8 CLAUDE.md 품질 3배]]) |

### C. 길이 규칙 (200줄 룰)
- 공식 권장은 **200줄 이하**, 대략 150~200단어/줄 안에서 끝낸다. 300줄을 넘으면 과감히 삭제하라 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]). CLAUDE.md는 "부탁"이지 강제가 아니어서 실무상 약 80%만 따른다 — 짧을수록 준수율이 올라간다 (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- **오토 메모리(`/memory`)도 200줄 룰을 따른다.** 처음 200줄까지만 로드되고, 넘으면 Claude가 상세 내용을 별도 파일로 분리해 필요할 때만 읽는다. 개인 메모리는 오토 메모리에, 팀 공유 지식은 명시적으로 CLAUDE.md에 둔다 (→ [[sources/youtube-cZ8_Dkk_Ce0|#8 CLAUDE.md 품질 3배]]·[[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

### D. 대규모 프로젝트면 — 조건부 분할
루트 CLAUDE.md가 비대해지면(한 모노레포 사례에서 47,000단어) Claude가 느려지고 규칙을 안 따르기 시작한다. 단순히 쪼개는 게 아니라 **"필요한 규칙만 필요한 시점에"** 불러오도록 설계한다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]):
- **`@` 참조 + 레이지 로딩:** CLAUDE.md에는 규칙과 참조만, 상세는 별도 파일로 분리 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
- **`.claude/rules` + 프론트매터 조건부 로딩:** 주제별 파일 상단에 glob 패턴(예: `src/api/**/*.ts`)을 지정하면 해당 파일 작업 시에만 자동 로드. 실제 trigger.dev·CockroachDB가 사용 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]).
- **폴더별 CLAUDE.md:** `apps/api/CLAUDE.md` 등으로 두면 해당 폴더 작업 시 그 파일만 읽힌다 (→ [[sources/youtube-FBv8hK_DtJ8|#10 대규모 컨텍스트 분리]]·[[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).

### E. 정 길어지면 — 스킬로 분리
CLAUDE.md에 많은 내용을 쓰기 싫으면, 문서·체크 항목을 [[concepts/skills|스킬]]로 옮긴다. 스킬은 세션 시작 시 무조건 로드되는 CLAUDE.md와 달리 **실제 필요할 때만 로드**되므로, 특정 작업에 필요한 컨텍스트만 주입할 수 있다 (→ [[sources/youtube-c7_ANA1NiS0|#6 CLAUDE.md를 지워라]]·[[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]). 단 스킬은 명시적으로 호출해야 Claude가 실제로 쓴다 (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).

## 4. 한 줄 결론
**CLAUDE.md를 두되, 자동 생성·장황함을 버리고 짧고(≤200줄) 검증 가능한 규칙을 수기로 점진 축적하라.** 더 커지면 `.claude/rules` 조건부 분할과 [[concepts/skills|스킬]] 분리로 "필요할 때만 로딩"을 설계하라.

## 연결
- [[concepts/claude-md|CLAUDE.md]] — 모순①의 원본 기록
- [[concepts/context-engineering|컨텍스트 엔지니어링]] — "많이가 아니라 정확히" 원칙
- [[concepts/skills|스킬]] — 무조건 로딩 vs 필요시 로딩의 대안
- [[concepts/verification-automation|검증 자동화]] — 최고 레버리지인 검증 규칙
- [[entities/boris-cherny|보리스 체르니]] — "검증 가능하면 품질 2~3배" 증언
- [[entities/andrej-karpathy|안드레이 카파시]] — 65줄 CLAUDE.md

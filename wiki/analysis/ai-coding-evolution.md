---
title: "분석 — AI 코딩 패러다임의 진화: 프롬프트→컨텍스트→하네스→루프"
type: analysis
created: 2026-06-23
updated: 2026-08-02
sources: [youtube-BssPGKsP60s, youtube-6gvnDSAcZww, youtube-6MYZ7fMhKPY, youtube-z-3BRkxQ5GM, youtube-DrekqeDlO1w, youtube-6cr4PeilKJk, youtube-DCsv0rKKrN4, youtube-FBv8hK_DtJ8, youtube-9fx2_1aTzq8, youtube-fInMcawbKng]
tags: [분석, 진화서사, 패러다임, 비교]
---

# 분석 — AI 코딩 패러다임의 진화: 프롬프트 → 컨텍스트 → 하네스 → 루프

이 글은 사람이 AI에게 코딩을 시키는 방식이 지난 몇 년 동안 어떻게 바뀌어 왔는지를 네 단계로 정리해 비교한다. 질문을 잘 다듬는 단계에서 시작해, 필요한 자료를 함께 건네는 단계, AI가 일할 환경 자체를 설계하는 단계, 사람이 반복해서 시키던 일까지 자동으로 돌리는 단계로 이어진다. 결론은 뒤 단계가 앞 단계를 버리는 것이 아니라 겹겹이 쌓인다는 것이며, 지금 무게 중심은 환경을 설계하는 세 번째 단계에 있다. 이 위키의 다른 문서들이 어느 칸에 들어가는지 알려 주는 지도 역할을 하는 페이지다.

이 페이지는 이 위키 전체를 관통하는 척추인 4단계 진화 서사를 한자리에 모아 비교한다. **프롬프트 엔지니어링 → 컨텍스트 엔지니어링 → 하네스 엔지니어링 → 루프 엔지니어링**으로 이어지는 흐름은, "AI에게 말을 거는 법"에서 출발해 점점 더 바깥 레이어(정보 → 환경 → 반복 자체)를 다루는 쪽으로 추상화가 높아지는 과정이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]). "25년이 컨텍스트(혹은 에이전트)의 해였다면 26년은 하네스의 해"라는 표현이 반복되며, 루프는 그 위에서 가장 최근에 등장한 축이다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]·[[sources/youtube-6MYZ7fMhKPY|#21 바이브에서 에이전틱으로]]·[[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

## 4단계 비교표

| 단계 | 시기 | 핵심 질문 | 비유 (부탁 vs 강제 등) | 다루는 대상 | 대표 기법·도구 | 한계 |
|---|---|---|---|---|---|---|
| **[[concepts/prompt-engineering\|프롬프트 엔지니어링]]** | ChatGPT 초창기 (가장 먼저) | "뭘 **물어볼까**" | 모델에게 "잘 해 줘"라고 **부탁**하기 | 프롬프트 1개 (말 거는 법) | 역할 주기, 단계별 지시, 예시 넣기, 구체적 요청 ("공학용 계산기 GUI" 식) (→ [[sources/youtube-BssPGKsP60s\|#5 조용히 설계한다]]·[[sources/youtube-6gvnDSAcZww\|#11 프롬프트는 끝났다]]) | 프로젝트 스택·코드 구조·DB 스키마를 모르면 천장. 또 "DB 호출하지 마"라 써도 또 어김 — 부탁이지 강제가 아님 (→ [[sources/youtube-6gvnDSAcZww\|#11 프롬프트는 끝났다]]) |
| **[[concepts/context-engineering\|컨텍스트 엔지니어링]]** | ~2025 (그다음) | "뭘 **보여줄까**" | 일하기 전 **필요한 자료를 책상에 깔아주기** | 모델에 주입할 정보(코드·문서·규칙) | 레이지/조건부 로딩(`.claude/rules` glob), 세컨드 브레인/`/memory`, `/clear` 컨텍스트 위생, MCP 토큰 관리 (→ [[sources/youtube-DCsv0rKKrN4\|#7 메타 엔지니어 실전편]]·[[sources/youtube-FBv8hK_DtJ8\|#10 대규모 컨텍스트 분리]]) | 정보를 다 알아도 "엉뚱한 짓"(DB 스키마 멋대로 변경)은 못 막음 — 정보가 아니라 규칙·울타리의 문제 (→ [[sources/youtube-6gvnDSAcZww\|#11 프롬프트는 끝났다]]) |
| **[[concepts/harness-engineering\|하네스 엔지니어링]]** | 2026 ("하네스의 해") | "**어떤 환경**에서 일하게 할까" | "잘 할 수밖에 없는 **구조**" 만들기 = 야생말에 **마구(馬具)** 씌우기 (부탁→강제) | 모델을 뺀 환경 전체 (컨텍스트 파일+MCP+스킬+훅+권한) | 컨텍스트 파일([[concepts/claude-md\|CLAUDE.md]]), 자동 강제(린터·아키텍처 테스트·[[concepts/hooks\|훅]]), 자가교정 루프, 가비지 컬렉션 (→ [[sources/youtube-6gvnDSAcZww\|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w\|#14 하네스 문서 100번]]) | 한 번 만든 하네스가 영원하지 않음. 모델이 좋아지면 낡은 제약이 오히려 방해·중복됨 → '하네스 다이어트' 필요 (→ [[sources/youtube-fInMcawbKng\|#24 하네스 다이어트]]) |
| **[[concepts/loop-engineering\|루프 엔지니어링]]** | 최신 트렌드 (가장 최근) | "**반복 자체**를 어떻게 자동화할까" | **프롬프팅하는 나 자신**을 줄이기 (행동→관찰→결정→반복) | 사람의 n번째(2·3·…) 개선 프롬프트 | Act→Observe→Decide→Repeat 루프, 통과 기준(예: 유사도 90%)까지 자가 반복, [[concepts/dynamic-workflow\|다이나믹 워크플로우]]의 `ultra code` (→ [[sources/youtube-z-3BRkxQ5GM\|#25 루프 엔지니어링]]·[[sources/youtube-9fx2_1aTzq8\|#23 다이나믹 기능 비교]]) | 작은 프로젝트·MVP엔 과함 — 한 번에 끝낼 일을 루프로 돌리면 토큰·시간 낭비. "루프 디자인"은 결국 다시 하네스로 회귀 (→ [[sources/youtube-z-3BRkxQ5GM\|#25 루프 엔지니어링]]) |

## 상호보완(누적)이지 대체가 아니다

이 네 축의 가장 중요한 성질은 **순서대로 졸업하는 것이 아니라 전부 필요한 상호보완적 축**이라는 점이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]). 다음 단계가 나왔다고 앞 단계가 폐기되는 것이 아니라, 더 큰 바깥 레이어가 앞 단계를 **부분집합으로 흡수**한다.

- 프롬프트 엔지니어링은 사라지지 않고, 하네스라는 더 큰 환경 설계 안의 한 요소로 남는다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).
- 컨텍스트 엔지니어링은 하네스의 4대 기둥 중 하나(컨텍스트 파일)로 흡수된다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).
- 루프 엔지니어링은 하네스 위에서 작동하며, "무엇을 하고 하면 안 되는지의 룰을 정의"하는 순간 다시 하네스 엔지니어링으로 회귀한다 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

즉 각 단계는 앞 단계의 천장을 한 겹씩 넘는 **누적적 추상화**다. 프롬프트의 천장(프로젝트를 모름)을 컨텍스트가, 컨텍스트의 천장(알아도 어김)을 하네스가, 하네스의 천장(사람이 반복 개입해야 함)을 루프가 넘는다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

이 진화는 [[concepts/developer-role-change|개발자 역할의 변화]]의 **"선수 → 감독"** 상향 이동과 정확히 맞물린다. 단계가 올라갈수록 인간이 손으로 하는 일(직접 코딩, 직접 프롬프트)은 줄고, 대신 환경과 규칙과 루프를 **설계**하는 일이 늘어난다. "인간은 조종하고, 에이전트는 실행한다(Humans steer, agents execute)"는 말에서 '조종'이 곧 하네스 설계이며, 이것이 코드 한 줄을 짜던 엄밀함을 시스템을 설계하는 엄밀함으로 옮기는 **"엄밀함의 재배치"**다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]). 같은 모델이라도 환경을 설계한 사람과 그냥 시킨 사람의 격차가 10배까지 벌어진다는 `$9` vs `$200` 일화가 이를 뒷받침한다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]·[[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).

## 주의 / 논쟁: 최신이 항상 정답은 아니다

진화 서사를 "뒤로 갈수록 우월하다"로 오독하면 안 된다. 두 가지 경고가 위키 전체에 명시되어 있다.

- **루프·다이나믹 워크플로우는 규모에 맞아야 한다.** 사이드 프로젝트·MVP·PMF 탐색 단계의 작은 작업에서는 프론티어 모델 성능이 워낙 좋아 한 번에 `ultra code`나 max로 끝낼 수 있는데, 이를 굳이 루프로 반복하면 **루프 짜는 시간·도는 시간·토큰만 낭비**된다. SVG처럼 한 번에 그릴 수 있는 걸 루프로 돌리는 건 말이 안 된다. "right tool for the right job" — 작업·프로젝트 규모와 본인 이해도에 맞는 기법을 골라야 한다 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]). "새 개념들은 사실 추상화가 높아진 것일 뿐 완전히 새로 생긴 건 많지 않다"는 조언도 같은 맥락이다 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

- **하네스도 무한정 쌓는 게 아니라 덜어내야 한다 ('하네스 다이어트').** 모델 성능이 좋아지면 예전에 강제로 묶어야 했던 행동이 불필요해지고, [[entities/claude-code|Claude Code]]·[[entities/codex|Codex]]·[[entities/cursor|Cursor]] 자체가 이미 하나의 하네스 레이어라서 그 위에 낡은 하네스를 또 얹으면 제품 내장 기능과 **중복**되어 오히려 에이전트를 방해한다. 지금은 "무엇을 더 붙일까"가 아니라 "불필요한 것을 어떻게 덜어낼까"의 타이밍이며, 한 달에 한두 번 점검이 권장된다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]). 이는 [[concepts/dynamic-workflow|다이나믹 워크플로우]]의 '하네스 레거시 스캔/다이어트' 워크플로우로 실연되었다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).

종합하면, 이 4단계는 **계단식 대체가 아니라 도구 상자의 확장**이다. 각 단계는 앞 단계를 품은 채 바깥으로 한 겹 넓어지고, 어느 단계를 쓸지는 트렌드가 아니라 작업 규모와 이해도가 결정한다 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]·[[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

## 같이 보기

- [[concepts/prompt-engineering|프롬프트 엔지니어링]] — 1단계, "뭘 물어볼까"
- [[concepts/context-engineering|컨텍스트 엔지니어링]] — 2단계, "뭘 보여줄까"
- [[concepts/harness-engineering|하네스 엔지니어링]] — 3단계, 환경 전체 설계 (서사의 중심)
- [[concepts/loop-engineering|루프 엔지니어링]] — 4단계, 반복 자체의 자동화
- [[concepts/agentic-coding|에이전틱 코딩]] — 말(에이전트) 훈련과 마구(하네스) 제작의 짝
- [[concepts/developer-role-change|개발자 역할의 변화]] — "선수 → 감독" 상향 이동
- [[concepts/dynamic-workflow|다이나믹 워크플로우]] — 동적 하네스 생성 / 하네스 다이어트

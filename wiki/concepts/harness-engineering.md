---
title: 하네스 엔지니어링
type: concept
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-BssPGKsP60s, youtube-6gvnDSAcZww, youtube-6cr4PeilKJk, youtube-DrekqeDlO1w, youtube-6MYZ7fMhKPY, youtube-fInMcawbKng]
tags: [하네스, 에이전트, 환경설계, 진화서사, 핵심개념]
---

# 하네스 엔지니어링

이 위키의 중심 개념이자 전체 진화 서사의 종착점이다. **하네스 엔지니어링은 AI 에이전트가 자율적으로 일하되 동시에 안전하게 통제될 수 있도록, 모델을 감싸는 "환경 전체"를 설계하는 기술**을 말한다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]). 모델 자체가 아니라 모델이 아닌 모든 것 — 컨텍스트 파일, MCP, 스킬, 훅, 권한 등 — 이 곧 하네스다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

## 핵심 정의와 철학

가장 압축된 정의는 "프로젝트 전체를 AI가 실수할 수 없는 환경으로 만드는 것"이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]). 핵심 철학은 다음 한 문장으로 요약된다.

> **에이전트가 규칙을 어겼을 때 "더 잘해 봐"라고 프롬프트를 고치는 게 아니라, 그 실패가 구조적으로 반복 불가능하도록 하네스를 고친다** (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

예를 들어 프론트엔드 코드가 DB를 직접 호출하는 실수를 했을 때, 프롬프트에 "DB를 직접 호출하지 마"라고 추가하는 것은 부탁일 뿐이라 또 실수한다. 대신 아키텍처 테스트를 추가해 프론트엔드 폴더에서 DB를 임포트하면 빌드 자체가 실패하게 만든다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]). 즉 "프롬프트는 부탁, 하네스는 강제"이며, 공장 안전 시스템(안전모 없으면 출입문이 안 열림)처럼 규칙을 사람의 판단이 아니라 시스템에 내장하는 것이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

비유로는 말과 마구(馬具) 이야기가 자주 쓰인다. 강력한 야생말(AI 모델)에 마구(하네스)를 씌워야 비로소 인간의 의도대로 밭을 갈 수 있다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

## 진화 서사: 프롬프트 → 컨텍스트 → 하네스 → 루프

이 위키 전체를 관통하는 척추가 되는 흐름이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]·[[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).

1. **[[concepts/prompt-engineering|프롬프트 엔지니어링]] (프롬프트 엔지니어링)** — "뭘 물어볼까"의 기술. 역할 주기, 단계별 지시, 예시 넣기. 하지만 프로젝트 구조·기술 스택을 모르면 천장에 부딪힌다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]·[[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).
2. **[[concepts/context-engineering|컨텍스트 엔지니어링]] (컨텍스트 엔지니어링)** — "뭘 보여줄까"의 기술. 프로젝트 구조·코드·API 문서·규칙을 적절히 제공. 단 많이 주는 게 아니라 지금 필요한 것만 정확히 주는 게 핵심 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]·[[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).
3. **하네스 엔지니어링** — 컨텍스트 엔지니어링을 포함해 MCP·스킬·에이전트·훅·권한까지 합친 "환경 전체"의 설계 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).
4. **[[concepts/loop-engineering|루프 엔지니어링]] (루프 엔지니어링)** — 하네스 위에서 사람의 반복 프롬프트조차 자동화해 완성도를 끝까지 끌어올리는 단계. 결국 "루프를 디자인하는 것" 자체가 다시 하네스 엔지니어링으로 회귀한다 (→ [[sources/youtube-z-3BRkxQ5GM|#25 루프 엔지니어링]]).

이 네 축은 순서대로 졸업하는 것이 아니라 전부 필요한 **상호보완적 축**이라는 점이 강조된다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]). "25년이 컨텍스트 엔지니어링의 해였다면 26년은 하네스의 해"라는 표현이 반복된다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]·[[sources/youtube-6MYZ7fMhKPY|#21 바이브에서 에이전틱으로]]).

## 4대 기둥

하네스는 크게 네 가지 요소로 구성된다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]; → [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]에서는 세 기둥으로 압축 정리).

1. **컨텍스트 파일 (기계가 읽는 런타임 설정)** — [[concepts/claude-md|CLAUDE.md]] (`CLAUDE.md`), `AGENTS.md`, Cursor의 `.cursorrules` 같은 파일. 사람이 읽는 위키가 아니라 에이전트가 작업 시작 시 가장 먼저 읽는 행동 제약 파일이다. 컨텍스트가 꽉 차서 앞 내용을 잊어버려도 이 파일은 매 세션 다시 읽힌다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).
2. **자동 강제 (린터·구조 테스트·프리커밋 [[concepts/hooks|훅]])** — 규칙을 파일에 써두는 것만으로는 부족하다. AI는 문서를 읽고도 어기기 때문이다. 린터·아키텍처 테스트·프리커밋 훅으로 규칙을 시스템이 기계적으로 강제한다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).
3. **자동 교정 루프 (self-correcting loop)** — 린터가 빨간 불을 켜면 에이전트가 사람 개입 없이 스스로 코드를 고치고 다시 시도한다. 말이 곱비에 의해 방향이 잡히면 자연스럽게 돌아오는 것과 같다. 이것이 하네스의 핵심 메커니즘이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]). 도구 경계(권한 제약)도 여기에 포함되며, SELECT는 허용하되 DROP TABLE은 차단하는 식으로 위험한 도구에 손도 못 대게 한다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).
4. **가비지 컬렉션 (garbage collection)** — 마틴 파울러가 이름 붙인 개념(자막상 표기). AI는 기존 코드의 나쁜 패턴을 복제하므로 시간이 지날수록 나쁜 패턴이 눈덩이처럼 불어난다. 주기적으로 규칙 위반·중복 코드·데드 코드·안티패턴을 자동 감지하고 청소하는 시스템이다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

**진화적 특성**: 에이전트가 실수할 때마다 그 실수가 새로운 규칙(린터 규칙·테스트·제약)이 되어 하네스가 점점 정교해진다. 말이 한 번 넘으려던 울타리는 점점 높아져 두 번 다시 같은 실수를 할 수 없게 된다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

전체 실행 그림은 4개 부품 — 라우터(분류기) → 컨텍스트 매니저 → 실행 루프(테스트 통과까지 자가 수정) → 워커 격리([[concepts/verification-automation|검증 자동화]]: 코드 쓰는 AI와 검토하는 AI 분리) — 로 정리된다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]).

## 모델이 아니라 하네스가 병목 — 대표 일화들

- **`$9` vs `$200` (Anthropic 실험)**: [[entities/anthropic|Anthropic]]가 같은 클로드 모델에게 레트로 게임 메이커를 만들게 했다. 하네스 없이 시키니 20분·`$9`에 끝났지만 캐릭터 조작이 안 되는 망한 앱이 나왔고, 스펙 수립·완료 기준 사전 합의·브라우저 자동 테스트라는 하네스를 갖추니 6시간·`$200`이 들었지만 완성된 앱이 나왔다. 같은 모델인데 달라진 건 환경뿐이었다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]).
- **OpenAI 코드 0줄 일화**: [[entities/openai|OpenAI]]가 25년 8월(또 다른 영상에선 26년 2월 공식 블로그 발표로 표기)부터 [[entities/codex|Codex]] 에이전트만으로 내부 제품을 만들기 시작했다. 수동 작성 코드 0줄, 5개월 만에 100만 줄 생성, 1,500개 PR 머지, 엔지니어 1인당 하루 평균 3.5개 작업. 처음엔 느렸는데 코덱스가 무능해서가 아니라 하네스 세팅(환경·도구 연결·에러 복구)이 부족했기 때문이었고, 이를 잡아 나가니 성과가 폭발했다. "엔지니어링 팀의 주된 역할이 에이전트가 유용한 일을 할 수 있게 만드는 것이 됐다"는 말이 나왔다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]·[[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]). 하네스 관점 4대 분석: `AGENTS.md` 작성, CI/CD 게이트(린트·테스트·훅), 도구 경계 설정, 피드백 루프 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).
- **Langchain 벤치마크 일화**: [[entities/anthropic|Anthropic]]·OpenAI와 함께 같은 문제를 겪던 Langchain(랭체인)은 코딩 에이전트 벤치마크에서 **모델을 바꾸지 않고 하네스만 개선**해 30위권에서 5위권으로 25단계 상승했다. 성능을 좌우하는 것은 모델 지능이 아니라 하네스임을 보여주는 사례 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

핵심 명제: "모델이 병목이 아니라 하네스가 병목이다." 같은 모델이라도 환경 세팅에 따라 결과가 10배 차이 날 수 있다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]). 또한 모델은 몇 주면 따라잡히지만 하네스는 쉽게 복제되지 않아 진짜 경쟁 우위가 된다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).

## 용어의 기원

"하네스(harness)" 용어는 **해시코프(HashiCorp) 공동 창립자 [[entities/mitchell-hashimoto|미첼 하시모토]](미첼 하시모토)가 2026년 2월 처음 제시했다고 자막이 언급한다(추정)** (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]). 그는 AI 코딩 에이전트가 같은 실수를 반복하는 것을 겪고, "하네스 엔지니어링은 에이전트가 실수할 때마다 그 실수를 다시는 반복하지 않도록 솔루션을 설계하는 데 시간을 투자하는 것"이라 정의했다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]). 한편 소프트웨어 공학의 `test harness` 개념은 1970년대부터 있었으나, 결정론적이던 전통 SW와 달리 예측 불가능한 LLM 시대에 완전히 새로운 의미를 갖게 되었다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]). 마틴 파울러(자막상 "마틴 러가"·"차드 파울러" 등으로도 표기됨, 추정)는 이 변화를 "엄밀함의 재배치"라 표현했다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

## 긴장②: 하네스를 쌓아라 vs 낡은 하네스는 빼라 (하네스 다이어트)

이 위키의 핵심 긴장 중 하나다.

- **쌓아라 진영**: 컨텍스트 파일·MCP·스킬을 갖추고 실수마다 규칙을 추가해 하네스를 점점 정교하게 만들라 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]·[[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).
- **빼라 진영 (하네스 다이어트, → [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]])**: 한 번 만든 하네스가 영원하지 않다. 모델 성능이 좋아지면(오프스 4.8, GPT 5.5 등) 예전에 강제로 묶어야 했던 행동이 불필요해진다. 더구나 [[entities/claude-code|Claude Code]]·[[entities/codex|Codex]]·[[entities/cursor|Cursor]] 자체가 이미 하나의 하네스 레이어라서, 그 위에 우리만의 낡은 하네스를 또 얹으면 제품 내장 기능과 **중복**되어 오히려 에이전트를 방해한다. 따라서 지금은 "무엇을 더 붙일까"가 아니라 "불필요한 것을 어떻게 덜어낼까"에 집중할 타이밍이다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).

해당 영상은 [[concepts/dynamic-workflow|다이나믹 워크플로우]](다이나믹 워크플로우)의 `ultra code` 키워드로 "하네스 레거시 스캔"과 "하네스 다이어트" 두 워크플로우를 만들어, 읽기 전용 감사 후 저위험 개선만 적용하는 방식을 시연한다. 실제로 스킬 약 10개 정리, `SKILL.md` 본문 2,600줄→1,800줄(약 760줄 감축), 활성 스킬 29→28개로 줄이는 결과를 보였다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]). 결론은 "좋은 하네스는 계속 쌓는 게 아니라 주기적으로 검토·갱신되는 구조"이며 한 달에 한두 번 정도 점검을 권장한다 (→ [[sources/youtube-fInMcawbKng|#24 하네스 다이어트]]).

[[entities/anthropic|Anthropic]] 역시 오프스 4.6 출시 후 스프린트 구조를 통째로 제거하며 하네스를 간소화했다 — 모델이 좋아지면 제약이 불필요해지므로 가정이 여전히 유효한지 다시 확인해야 한다 (→ [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]). 강화학습 창시자 리처드 서튼은 "모델이 똑똑해질수록 하네스는 더 단순해져야 한다"고 했고(자막상 표기), 모델 업그레이드마다 하드코딩 규칙을 더 추가하면 흐름을 거스르는 것이라 경고했다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

## 도구는 적을수록 좋다

직관과 달리 에이전트에게 도구를 많이 주면 어떤 도구를 쓸지 고민하는 데 에너지를 써 정작 할 일에 집중을 못 한다. [[concepts/skills|스킬]]도 수백 개가 쌓이면 오히려 혼란스러워진다 — "넷플릭스에서 뭐 볼지 30분 고민하다 유튜브 켜는 것"과 같다. 따라서 핵심 스킬 몇 개를 강화하는 편이 낫다 (→ [[sources/youtube-6MYZ7fMhKPY|#21 바이브에서 에이전틱으로]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]). MCP도 많이 줄수록 좋은 게 아니며 토큰이 터지지 않도록 관리해야 한다 (→ [[sources/youtube-BssPGKsP60s|#5 조용히 설계한다]]).

## 미래 전망과 역할 변화

- **2027년 자율화**: 언젠가 에이전트가 스스로 하네스 엔지니어링을 하게 될 것이다. 작업 환경 구성을 먼저 묻고 설정한 뒤 작업을 시작하는 식 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]·[[sources/youtube-6MYZ7fMhKPY|#21 바이브에서 에이전틱으로]]).
- **하네스 = 미래의 서비스 템플릿**: 기술 스택을 "개발자 경험이 좋은 프레임워크"가 아니라 "좋은 하네스가 갖춰진 프레임워크"로 고르게 될 수 있다 (→ [[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).
- "인간은 조종한다, 에이전트는 실행한다(Humans steer, agents execute)" — 여기서 '조종'이 곧 하네스다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]). 이 변화로 [[concepts/developer-role-change|개발자 역할의 변화]]에서 다루듯 개발자의 역할은 축소가 아니라 "공을 차는 선수에서 전술을 짜는 감독으로" 상향 이동한다 (→ [[sources/youtube-6gvnDSAcZww|#11 프롬프트는 끝났다]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]]).

## 외부 검증 (2026-06-23, 웹)

핵심 일화·수치를 웹으로 교차 확인했다(모두 **확인**, 일부 정정 포함):
- **`$9` vs `$200`:** [[entities/anthropic|Anthropic]]의 실제 사례로, 동일 모델(Opus 4.5)·동일 과제("게임 에디터")에서 단일 에이전트 ≈20분·`$9`(프로토타입) vs 풀 하네스(Planner+Generator+Evaluator 3-에이전트, Playwright MCP 평가) ≈6시간·`$200`(완성) (→ https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents ).
- **OpenAI 코드 0줄:** Harness 팀이 5개월간 사람이 코드를 직접 안 쓰고 ≈100만 줄·PR ≈1,500개를 머지. "하루 3.5개"는 **엔지니어 1인당 하루 PR 수**이며 당시 팀은 3명이었다 (→ https://openai.com/index/harness-engineering/ ).
- **LangChain 30위→5위:** 벤치마크는 **Terminal-Bench 2.0**, 모델 고정·하네스만 개선해 52.8%→66.5%로 약 25단계 상승 (→ https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering ).
- **용어 기원 정정:** '하네스' 개념은 [[entities/mitchell-hashimoto|미첼 하시모토]]가 대중화했으나 'harness engineering'이라는 명칭은 OpenAI 측 정리에서 굳어졌고 마틴 파울러가 'guides-and-sensors' 분류를 더했다(자세한 내용은 해당 엔티티 페이지).

## 같이 보기

- [[concepts/agentic-coding|에이전틱 코딩]] — 하네스(마구 제작)와 짝을 이루는 에이전틱 엔지니어링(말 훈련)
- [[concepts/context-decay|컨텍스트 부패]] — 하네스가 해결하려는 두 문제 중 하나(컨텍스트 부패)
- [[concepts/verification-automation|검증 자동화]] — 생성/검증 에이전트 분리
- [[concepts/multi-model-workflow|멀티 모델 워크플로우]] — Codex 협업으로 검증 성능을 높이는 변형

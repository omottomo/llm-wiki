---
title: GraphQL (그래프 쿼리 언어)
type: concept
created: 2026-08-19
updated: 2026-08-19
sources: [kakaotech-graphql]
aliases: [GraphQL, gql]
tags: [GraphQL, API, 쿼리언어, 웹개발, 협업방식]
---

# GraphQL (그래프 쿼리 언어)

## 한눈에 요약

- GraphQL은 웹 클라이언트가 서버에서 필요한 데이터만 골라 받아 오려고 만든 쿼리 언어다. 쿼리 언어란 "이런 데이터를 달라"는 요청을 정해진 문법으로 적는 언어를 말한다.
- 엔드포인트(호출 주소)가 하나뿐이고, 무엇을 받을지는 주소가 아니라 **쿼리문**이 정한다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).
- 서버는 **스키마**로 데이터 모양을 선언하고 **리졸버**로 실제 조회를 구현한다. 클라이언트는 그 스키마를 보고 쿼리를 짠다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).
- 페이스북이 만들었고, 특정 데이터베이스·언어·네트워크 방식에 묶이지 않는다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).
- 성능보다 **협업 생산성**이 더 큰 이점으로 꼽힌다. 프런트엔드가 가져갈 데이터를 스스로 정하기 때문이다 (2019-08 기준) (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

## 왜 필요했나 — REST의 왕복 비용

화면 하나를 그리려고 API를 세 번 네 번 부르는 상황이 출발점이다. REST API는 URL과 메서드를 조합하므로 엔드포인트가 여러 개로 늘어나고, 엔드포인트마다 돌려주는 데이터 묶음이 고정돼 있다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

gql은 반대로 간다. 엔드포인트는 하나로 두고, 필요한 데이터의 종류는 쿼리 조합으로 결정한다. 그래서 여러 번 왕복할 일을 **한 번의 네트워크 호출**로 끝낼 수 있다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

쉽게 말하면 창구를 여러 개 만들어 각 창구가 정해진 서류만 내주던 방식에서, 창구 하나에 "이 서류의 이 항목들만 주세요"라고 적어 내는 방식으로 바뀐 셈이다.

> 다만 REST에서는 백엔드가 이미 짜 둔 쿼리가 통째로 실행됐지만, gql은 요청한 필드만큼만 조회가 일어난다. 최적화 여지는 늘지만 그 최적화를 직접 설계해야 한다는 뜻이기도 하다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

## SQL과는 이름만 닮았다

둘 다 쿼리 언어지만 목적과 실행 위치가 다르다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

| 항목 | SQL | GraphQL |
|---|---|---|
| 목적 | 데이터베이스에 쌓인 데이터를 효율적으로 꺼내기 | 웹 클라이언트가 서버에서 데이터를 효율적으로 받기 |
| 문장을 쓰는 쪽 | 주로 백엔드 시스템 | 주로 클라이언트 시스템 |
| 종속성 | 데이터베이스 시스템에 종속 | 데이터베이스·플랫폼·네트워크 방식에 비종속 |

전송 계층도 자유롭다. 보통은 HTTP POST와 웹소켓을 쓰지만, 필요하면 TCP·UDP나 이더넷 프레임 위에서도 주고받을 수 있다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

## 구조 네 가지

gql을 이해하는 데 필요한 부품은 네 개다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

| 부품 | 하는 일 | 누가 쓰나 |
|---|---|---|
| 쿼리 / 뮤테이션 | 읽기 요청 / 변경 요청 | 클라이언트 |
| 스키마 · 타입 | 주고받을 데이터의 모양 선언 | 서버 |
| 리졸버 | 필드별로 실제 데이터를 가져오는 함수 | 서버 |
| 인트로스펙션 | 서버가 자기 스키마를 실시간으로 알려 주기 | 양쪽 |

### 쿼리와 뮤테이션

요청문의 구조와 응답 데이터의 구조가 거의 같다는 점이 가장 눈에 띈다. 쿼리는 읽기, 뮤테이션은 생성·수정·삭제에 쓴다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

> 여기서 헷갈리기 쉬운데, 내부적으로 둘은 사실상 차이가 없다. 읽기와 변경을 구분해 두자는 **개념적 규약**일 뿐이다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

앞에 `query`와 이름이 붙은 쿼리를 **오퍼레이션 네임 쿼리**라고 한다. 변수를 받는 쿼리용 함수라고 보면 된다. 데이터베이스의 프로시저와 비슷하되, 이번에는 클라이언트 프로그래머가 직접 작성하고 관리한다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

### 스키마와 타입

스키마 작성은 데이터베이스 스키마보다 C·C++의 헤더 파일 작성에 가깝다. 타입과 필드를 미리 선언해 두는 일이기 때문이다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

```graphql
type Character {
  name: String!
  appearsIn: [Episode!]!
}
```

- 오브젝트 타입은 `Character`, 필드는 `name`과 `appearsIn`이다.
- `String`·`ID`·`Int` 등은 스칼라 타입이다.
- 느낌표(`!`)는 필수 값(non-nullable), 대괄호(`[ ]`)는 배열을 뜻한다.

### 리졸버

gql은 쿼리문 파싱까지만 라이브러리가 해 주고, **데이터를 실제로 가져오는 과정은 직접 구현**해야 한다. 그 구현체가 리졸버다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

부담처럼 보이지만 자유이기도 하다. 리졸버는 데이터베이스든 파일이든 HTTP·SOAP 같은 원격 프로토콜이든 가리지 않는다. 그래서 레거시 시스템을 gql로 감싸는 데도 쓸 수 있다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

필드마다 리졸버 함수가 하나씩 있다고 보면 된다. 필드가 스칼라 값이면 거기서 멈추고, 직접 정의한 타입이면 그 타입의 리졸버가 이어서 불린다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

이 **연쇄 리졸버** 호출 덕에 1:1·1:n 관계 데이터를 요청한 만큼만 타고 들어가며 가져올 수 있다. 원문 저자는 이 연쇄 구조가 DFS(깊이 우선 탐색)로 구현돼 있으리라 추측하며, 여기서 Graph라는 이름이 나왔으리라고 본다 — 추측으로 명시된 대목이다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

리졸버 함수는 인자를 네 개 받는다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

| 인자 | 담기는 것 |
|---|---|
| `parent` | 연쇄 호출에서 부모 리졸버가 돌려준 객체 |
| `args` | 쿼리에서 넘긴 인자 |
| `context` | 모든 리졸버에 전달되는 값. 로그인·권한 등 미들웨어가 넣은 정보 |
| `info` | 스키마 정보와 현재 쿼리의 필드 정보. 잘 쓰지 않는다 |

> 비즈니스 로직은 리졸버에 직접 담지 않고 별도의 비즈니스 로직 레이어에 두기를 권한다. REST API를 만들 때 쓰던 패턴과 같다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

### 인트로스펙션

REST 시절에는 연동규격서, 즉 API 명세서를 사람이 만들어 주고받아야 했다. 이 문서는 변경이 제때 반영되지 않아 자주 어긋난다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

인트로스펙션은 서버가 **지금 정의된 스키마를 실시간으로 알려 주는** 기능이다. 클라이언트는 따로 명세서를 요청할 필요 없이 그 스키마에 맞춰 쿼리를 짜면 된다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

전용 쿼리를 직접 쓸 일은 거의 없다. 서버용 라이브러리 대부분이 웹 IDE를 함께 제공해, 거기서 쿼리·뮤테이션·필드 스키마를 눌러 보며 확인할 수 있다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

> 물론 상용 환경에서 스키마를 그대로 공개하는 것은 보안상 신중해야 한다. 대부분의 라이브러리에 켜고 끄는 옵션이 있다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

## 협업 방식이 먼저 바뀐다

원문이 성능보다 크게 본 이점은 생산성이다. REST에서는 프런트엔드가 백엔드가 정해 준 요청·응답 형식에 매여 있었지만, gql에서는 그 의존이 상당히 줄어든다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

대신 무게중심이 앞으로 옮겨 간다. 쿼리를 짜고 관리하는 일이 클라이언트 쪽 몫이 되기 때문이다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

다만 의존이 완전히 사라지지는 않는다. **데이터 스키마에 대한 협업 의존성**은 그대로 남는다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

## 도입 전에 알아 둘 것

gql 자체는 언어일 뿐이라 라이브러리가 있어야 쓸 수 있다. 대표적으로 페이스북이 만든 릴레이(Relay)와 [[entities/apollo-graphql|아폴로]]가 있다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

> 개념을 읽었다고 바로 실전에 쓰기는 어렵다는 것이 원문의 마무리다. 특히 React와 함께 쓰려면 클라이언트 모듈과 상태 관리라는 고개를 한 번 더 넘어야 한다 (2019-08 기준) (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

시점도 감안해야 한다. 원문은 2019년 7월 기준으로 gql을 얼리스테이지로 봤고, 국내에서 gql API를 Open API로 공개한 곳은 드물다고 적었다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]). 그 뒤 상황은 이 위키에 아직 확인된 자료가 없다.

## 함께 읽기

- [[entities/apollo-graphql|Apollo GraphQL]] — 원문 저자가 릴레이보다 편하다고 꼽은 gql 라이브러리 세트
- [[concepts/mcp|MCP]] — 서버가 자기 능력 명세를 내주고 클라이언트가 그에 맞춰 호출한다는 결이 인트로스펙션과 닮았다
- [[concepts/dns-records|DNS 레코드]] — 같은 웹 인프라 기초 계열의 페이지

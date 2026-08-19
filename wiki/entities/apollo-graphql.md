---
title: Apollo GraphQL
type: entity
created: 2026-08-19
updated: 2026-08-19
sources: [kakaotech-graphql]
aliases: [아폴로, Apollo]
tags: [GraphQL, 라이브러리, 웹개발]
---

# Apollo GraphQL

## 한눈에 요약

- Apollo GraphQL은 GraphQL을 실제 서비스에 쓸 수 있게 해 주는 서버·클라이언트 라이브러리 세트다.
- 이 위키에는 카카오 기술 블로그의 GraphQL 입문 글에서 처음 등장한다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).
- 서버 라이브러리에 스키마를 눌러 볼 수 있는 웹 IDE가 들어 있어, 인트로스펙션 결과를 화면에서 바로 확인할 수 있다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

## 위치 — 릴레이와의 대비

gql 언어 자체는 라이브러리 없이는 할 수 있는 일이 없다. 대표 후보는 페이스북이 만든 릴레이(Relay)와 아폴로 둘이다 (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

원문 저자는 2019년 7월 버전 릴레이가 쓰기 번거롭게 설계돼 있다고 보고, 개인적으로는 아폴로가 편했다고 적었다 (2019-08 기준) (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]). 개인 의견으로 명시된 평가다.

아폴로 클라이언트의 로컬 상태 관리 기능이 Redux를 완전히 대체할 수 있다는 것도 원문 저자의 개인적 견해로 제시된다 (2019-08 기준) (→ [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]]).

## 이 위키에서의 등장

- **GraphQL 도입 도구** — 개념만으로는 못 쓰는 gql을 실제 서버·클라이언트에 붙이는 층으로 언급된다 ([[concepts/graphql|GraphQL]])
- **인트로스펙션 확인 수단** — 스키마를 실시간으로 훑어보는 웹 IDE의 사례로 나온다 ([[concepts/graphql|GraphQL]])

## 함께 읽기

- [[concepts/graphql|GraphQL]] — 이 라이브러리가 무엇을 구현해 주는지의 배경

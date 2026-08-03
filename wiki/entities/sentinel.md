---
title: Sentinel (정책 코드화 프레임워크)
type: entity
created: 2026-07-19
updated: 2026-08-04
sources: [hashicorp-terraform-docs]
tags: [HashiCorp, 코드형인프라, 정책]
---

# Sentinel (정책 코드화 프레임워크)

## 한눈에 요약

- HashiCorp가 만든 **정책 코드화 프레임워크**다. 조직이 지켜야 할 규칙을 코드로 적어 둔다.
- 인프라가 바뀌기 **전에** 자동으로 검사한다. 사람이 티켓을 열고 승인을 기다리는 수동 검토를 대체하는 게 목적이다.
- 비용 상한 같은 조건도 정책으로 걸 수 있다.
- 규칙을 부탁이 아니라 **통과 못 하면 막히는 장치**로 바꾼다. 이 위키가 다루는 하네스 발상의 인프라 판본이다.

## 무엇을 하는 도구인가

[[entities/hashicorp|HashiCorp]]의 **policy-as-code(정책 코드화)** 프레임워크다. [[concepts/infrastructure-as-code|코드형 인프라]]의 거버넌스 단계를 담당한다.

[[entities/terraform|Terraform]]이 인프라를 변경하기 **전에** 규정 준수·거버넌스 정책을 자동으로 강제한다. 개발을 늦추는 병목인 티켓 기반 수동 리뷰를 대체하는 것이다. Terraform Enterprise와 HCP Terraform에서 제공되며, 인프라 변경에 따르는 비용을 제한하는 정책도 정의할 수 있다 (2026-07 기준) (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 이 위키에서의 등장

- **훅과 같은 계보** — "규칙을 자연어 문서(부탁)가 아니라 코드로 강제한다"는 점에서 [[concepts/hooks|훅]]과 같은 사상이다. [[concepts/harness-engineering|하네스 엔지니어링]]이 CLAUDE.md의 부탁을 훅의 강제로 승격시키는 것과 같다. Terraform 도입의 성숙 단계(Govern)는 조직 표준을 Sentinel·[[entities/opa|OPA]] 정책으로 코드화해 자동 강제한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). 다만 이 유비 자체는 위키의 해석이다.
- **OPA와 짝** — HashiCorp 전용 프레임워크라서, 벤더 중립적 오픈 대안인 [[entities/opa|OPA]](Open Policy Agent)와 짝을 이뤄 언급된다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).
- **실행 전 검증** — apply 이전에 정책을 자동 강제한다. [[concepts/verification-automation|검증 자동화]]가 말하는 '실행 전 검증'의 순수 인프라 사례다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 함께 읽기

- [[entities/opa|OPA]] — 벤더 중립 대안
- [[entities/terraform|Terraform]] — Sentinel이 게이트하는 대상
- [[concepts/hooks|훅]] — 같은 사상의 에이전트 판본

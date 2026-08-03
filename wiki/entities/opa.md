---
title: OPA (Open Policy Agent)
type: entity
created: 2026-07-19
updated: 2026-08-02
sources: [hashicorp-terraform-docs]
tags: [코드형인프라, 정책]
---

# OPA (Open Policy Agent)

OPA(Open Policy Agent)는 조직의 규칙을 문서가 아니라 코드로 적어 두고 기계가 자동으로 검사하게 하는 오픈소스 엔진이다. 인프라를 바꾸기 전에 "이 변경이 규정에 맞는가"를 먼저 판정시키는 용도로 쓰인다. 이 위키에는 특정 회사에 묶이지 않은 대안이라는 위치로만 짧게 기록돼 있으며, 그 이상은 근거가 될 자료가 아직 없어 적지 않았다.

오픈소스 **policy-as-code(정책 코드화)** 엔진이다. [[entities/terraform|Terraform]] 공식 문서는 도입 성숙 단계(Govern)에서 조직 표준을 자동 강제하는 수단으로 **[[entities/sentinel|Sentinel]]·OPA**를 나란히 제시한다 — 즉 HashiCorp 전용인 Sentinel의 벤더 중립적·오픈 대안 위치에 있다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

> 이 위키의 현재 출처([[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]])는 OPA를 "Terraform 거버넌스의 정책 코드화 선택지"로만 다룬다. 규칙 언어(Rego)·CNCF 관계 등 그 외 세부는 아직 이 위키의 소스로 뒷받침되지 않아 기록하지 않는다.

## 이 위키에서의 의미

- [[entities/sentinel|Sentinel]]과 함께 [[concepts/infrastructure-as-code|코드형 인프라]]의 거버넌스 단계를 담당한다. "규칙을 코드로 강제한다"는 점에서 [[concepts/hooks|훅]]·[[concepts/harness-engineering|하네스 엔지니어링]]과 같은 사상 계보에 있다(위키 차원의 해석) (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

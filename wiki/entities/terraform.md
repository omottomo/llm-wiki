---
title: Terraform
type: entity
created: 2026-07-18
updated: 2026-07-18
sources: [ibm-infrastructure-as-code]
tags: [코드형인프라, HashiCorp, 도구]
---

# Terraform

[[entities/hashicorp|HashiCorp]]가 만든 대표적인 [[concepts/infrastructure-as-code|코드형 인프라]](IaC) 도구다. HCL(HashiCorp 구성 언어)로 작성한 선언형 구성을 AWS·Azure·Google Cloud·온프레미스 어디에나 배포할 수 있어 공급업체 종속을 피하게 해 주며, 리소스 간 종속성을 분석해 독립적인 리소스는 병렬로 프로비저닝한다 (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]). 오픈소스 포크로 OpenTofu가 있다 (2026-07 기준) (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]).

## 이 위키에서의 의미

- 제작사 HashiCorp의 공동창립자가 '하네스' 개념을 대중화한 [[entities/mitchell-hashimoto|미첼 하시모토]]다 — "환경을 코드로 선언하고 자동으로 강제한다"는 [[concepts/harness-engineering|하네스 엔지니어링]]의 사상적 선례가 Terraform으로 대표되는 IaC라는 연결이 성립한다 (연결 근거 → [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]).

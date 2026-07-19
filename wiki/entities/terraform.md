---
title: Terraform
type: entity
created: 2026-07-18
updated: 2026-07-19
sources: [ibm-infrastructure-as-code, hashicorp-terraform-docs]
tags: [코드형인프라, HashiCorp, 도구]
---

# Terraform

[[entities/hashicorp|HashiCorp]]가 만든 대표적인 [[concepts/infrastructure-as-code|코드형 인프라]](IaC) 도구다. HCL(HashiCorp 구성 언어)로 작성한 선언형 구성을 AWS·Azure·Google Cloud·온프레미스 어디에나 배포할 수 있어 공급업체 종속을 피하게 해 주며, 리소스 간 종속성을 분석해 독립적인 리소스는 병렬로 프로비저닝한다 (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]·[[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). 공식 문서는 인프라에 **불변(immutable) 접근**을 취해 업그레이드·변경의 복잡성을 줄인다고 명시한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). 오픈소스 포크로 OpenTofu가 있으며, 공식 문서 스스로는 "무료 source-available 도구"라 표현한다 (2026-07 기준) (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]·[[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 작동 원리: 프로바이더

Terraform은 각 플랫폼의 API를 호출하는 **프로바이더**(플러그인)를 통해 리소스를 생성·관리한다. 접근 가능한 API가 있는 거의 모든 플랫폼·서비스와 작동하며, Terraform 레지스트리에 AWS·Azure·GCP·Kubernetes·Helm·GitHub·Datadog 등 수천 개의 공개 프로바이더가 있다 (2026-07 기준) (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 코어 워크플로: Write → Plan → Apply

공식 문서가 제시하는 코어 워크플로는 세 단계다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]):

1. **Write** — 편집기에서 구성을 작성하고 `terraform plan`을 반복 실행하며 짧은 피드백 루프를 돈다(애플리케이션 코드의 편집↔테스트 루프와 같은 구조).
2. **Plan** — 실행 계획(어떤 리소스가 생성·수정·파괴되는지)을 생성해 **사람이 검토·승인**한다. 실제 인프라는 건드리지 않는다.
3. **Apply** — 승인 후에만 종속성 순서를 지켜 실제 변경을 수행한다.

이 루프는 협업 밀도에 따라 확장된다: 개인은 로컬에서 돌리고, 팀은 브랜치로 작업하며 **PR에 speculative plan 출력을 첨부해 동료가 "변경 의도가 계획에 반영됐는지"를 리뷰**하고(실행은 CI로 이관), 조직 규모에서는 HCP Terraform이 원격 state·변수를 중앙화하고 PR 생성 시 자동으로 plan을 돌린다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). CloudFormation 등 다른 IaC 도구와의 차별점으로 공식 문서가 강조하는 것이 바로 이 **계획/실행 단계의 분리**다 — 계획을 미리 볼 수 없으면 운영자가 변경의 효과를 머릿속으로 추론해야 하는데, 대규모 인프라에서는 감당 불가능해진다는 논리다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 상태(state) 파일

Terraform은 구성과 실세계를 잇는 **상태 파일**(`terraform.tfstate`)을 유지하며, 이것이 환경의 source of truth 역할을 한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). state가 필수인 이유는 네 가지다: ① 구성의 리소스 인스턴스와 원격 객체의 1:1 매핑(태그 기반 매핑은 "모든 리소스가 태그를 지원하지 않아" 초기 프로토타입에서 폐기됨), ② 구성에서 리소스를 지웠을 때 파괴 순서를 판단할 종속성 메타데이터 보존, ③ 대규모 인프라에서 매번 API를 조회하는 대신 쓰는 성능 캐시, ④ 팀이 같은 state를 공유하고 원격 잠금으로 동시 실행을 막는 동기화 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). state에는 시크릿이 담길 수 있고 잠금·접근 제어가 없으므로 **버전 관리 시스템에 저장하지 말라**고 공식 문서가 경고한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 구성 언어(HCL)와 모듈

HCL 문법은 **블록·인수·표현식** 세 요소가 전부이며, 언어의 주목적은 리소스 선언이고 나머지 기능은 그것을 유연하게 만드는 보조다. 선언형이라 블록 순서는 의미가 없고, 리소스 간 참조에서 종속성 그래프를 만들어 실행 순서를 결정한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). **모듈**은 함께 관리되는 리소스 묶음으로(루트 모듈이 자식 모듈을 호출), 변수(입력)·로컬(내부 재사용)·출력(외부 노출)이 인터페이스를 이루고, 레지스트리로 공유해 조직의 인프라 표준을 재사용 가능한 코드로 굳힌다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## CLI 주요 명령

주 명령은 `init`(프로바이더·모듈 설치와 작업 디렉터리 준비, 멱등이라 언제든 재실행 가능) → `validate`(구성 검증) → `plan` → `apply` → `destroy`다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). `terraform state` 계열·`import` 등으로 state를 수동 조작할 수도 있으나, 잘못하면 Terraform이 리소스 추적을 잃어 비용 증가·보안 저하로 이어질 수 있어 백업을 전제로 한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 조직 도입 4단계

공식 문서는 도입 성숙도를 Adopt(개인 실무자) → Collaborate(원격 state 백엔드로 협업) → Scale(인프라 소유권 경계·클라우드 전략 결정) → Govern(조직 표준을 [[entities/sentinel|Sentinel]]·[[entities/opa|OPA]] 정책 코드로 자동 강제)의 4단계로 제시한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 이 위키에서의 의미

- 제작사 HashiCorp의 공동창립자가 '하네스' 개념을 대중화한 [[entities/mitchell-hashimoto|미첼 하시모토]]다(또 다른 공동창립자 [[entities/armon-dadgar|아몬 다드가]]가 공식 문서에서 도구를 소개한다) — "환경을 코드로 선언하고 자동으로 강제한다"는 [[concepts/harness-engineering|하네스 엔지니어링]]의 사상적 선례가 Terraform으로 대표되는 IaC라는 연결이 성립한다 (연결 근거 → [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]).
- plan/apply 분리(실행 전 계획을 사람이 검토·승인)와 PR speculative plan 리뷰 관행은 [[concepts/verification-automation|검증 자동화]]가 말하는 "실행 전 검증"의 인프라 영역 선례이고, Govern 단계의 Sentinel 정책 강제는 [[concepts/hooks|훅]]식 "규칙의 코드화·자동 강제"의 선례다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). 단, 이 유비 자체는 소스가 아니라 위키의 해석이다.

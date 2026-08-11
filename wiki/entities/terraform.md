---
title: Terraform
type: entity
created: 2026-07-18
updated: 2026-08-11
sources: [ibm-infrastructure-as-code, hashicorp-terraform-docs, terraform-hcl-syntax, k3s-docs]
tags: [코드형인프라, HashiCorp, 도구]
---

# Terraform

## 한눈에 요약

- 서버·네트워크·DB 같은 인프라를 설정 파일로 선언해 두면 그대로 만들어 주는 **코드형 인프라 도구**다. HashiCorp가 만들었다.
- 특징은 **계획과 실행의 분리**다. `plan`으로 뭐가 바뀔지 먼저 보여 주고, 사람이 승인해야 `apply`가 돈다.
- 클라우드 종류를 가리지 않는다. AWS·Azure·GCP·온프레미스를 같은 방식으로 다룬다.
- 이 위키에는 [[concepts/harness-engineering|하네스 엔지니어링]]의 **사상적 선례**로 등장한다. 규칙을 코드로 선언하고 시스템이 강제한다는 발상이 같다.

## 무엇을 하는 도구인가

[[entities/hashicorp|HashiCorp]]가 만든 대표적인 [[concepts/infrastructure-as-code|코드형 인프라]](IaC) 도구다. HCL(HashiCorp 구성 언어)로 작성한 선언형 구성을 AWS·Azure·Google Cloud·온프레미스 어디에나 배포할 수 있다. 그래서 특정 공급업체에 묶이지 않는다 (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]·[[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

리소스 간 종속성을 분석해 서로 무관한 리소스는 병렬로 만든다 (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]·[[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). 공식 문서는 인프라에 **불변(immutable) 접근**을 취해 업그레이드·변경의 복잡성을 줄인다고 명시한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

오픈소스 포크로 OpenTofu가 있다. 공식 문서 스스로는 "무료 source-available 도구"라 표현한다 (2026-07 기준) (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]·[[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 작동 원리: 프로바이더

Terraform이 직접 AWS나 Azure를 아는 건 아니다. **프로바이더**라는 플러그인이 각 플랫폼의 API를 대신 호출한다.

접근 가능한 API가 있는 거의 모든 플랫폼·서비스와 작동한다. Terraform 레지스트리에는 수천 개의 공개 프로바이더가 올라와 있다 (2026-07 기준). AWS·Azure·GCP·Kubernetes·Helm·GitHub·Datadog 같은 것들이다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 코어 워크플로: Write → Plan → Apply

공식 문서가 제시하는 코어 워크플로는 세 단계다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]):

1. **Write** — 편집기에서 구성을 작성하고 `terraform plan`을 반복 실행하며 짧은 피드백 루프를 돈다(애플리케이션 코드의 편집↔테스트 루프와 같은 구조).
2. **Plan** — 실행 계획(어떤 리소스가 생성·수정·파괴되는지)을 만들어 **사람이 검토·승인**한다. 실제 인프라는 건드리지 않는다.
3. **Apply** — 승인 후에만 종속성 순서를 지켜 실제 변경을 수행한다.

### 팀 규모에 따라 늘어나는 루프

같은 세 단계가 협업 밀도에 따라 확장된다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

- **개인** — 로컬에서 그대로 돌린다.
- **팀** — 브랜치로 작업하고 **PR에 speculative plan 출력을 첨부한다**. 동료는 "변경 의도가 계획에 반영됐는지"를 리뷰하고, 실행은 CI로 넘긴다.
- **조직** — HCP Terraform이 원격 state와 변수를 중앙에서 관리하고, PR이 생성되면 자동으로 plan을 돌린다.

CloudFormation 같은 다른 IaC 도구와의 차별점으로 공식 문서가 강조하는 것이 바로 이 **계획/실행 단계의 분리**다. 계획을 미리 볼 수 없으면 운영자가 변경의 효과를 머릿속으로 추론해야 하는데, 대규모 인프라에서는 그게 감당이 안 된다는 논리다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 상태(state) 파일

Terraform은 구성과 실세계를 잇는 **상태 파일**(`terraform.tfstate`)을 유지한다. 이 파일이 환경의 source of truth, 즉 "지금 실제로 뭐가 떠 있는지"의 기준이 된다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

state가 필수인 이유는 네 가지다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]):

1. **매핑** — 구성의 리소스 인스턴스와 원격 객체를 1:1로 연결한다. 태그로 매핑하는 방식은 "모든 리소스가 태그를 지원하지 않아" 초기 프로토타입에서 폐기됐다.
2. **종속성 보존** — 구성에서 리소스를 지웠을 때 무엇부터 파괴할지 판단할 메타데이터가 남는다.
3. **성능** — 대규모 인프라에서 매번 API를 조회하는 대신 캐시로 쓴다.
4. **동기화** — 팀이 같은 state를 공유하고, 원격 잠금으로 동시 실행을 막는다.

> **주의:** state에는 시크릿이 담길 수 있고 잠금·접근 제어가 없다. 그래서 공식 문서는 **버전 관리 시스템에 저장하지 말라**고 경고한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 구성 언어(HCL)와 모듈

[[concepts/hcl|HCL]] 문법은 **블록·인수·표현식** 세 요소가 전부다. 언어의 주목적은 리소스 선언이고, 나머지 기능은 그것을 유연하게 만드는 보조라고 보면 된다.

선언형이라 블록을 쓴 순서는 의미가 없다. 대신 리소스끼리 서로를 참조하는 관계에서 종속성 그래프를 만들어 실행 순서를 정한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). 블록 라벨 개수, `resource` vs `data`, provider alias, 메타 인수 같은 실제 문법은 [[concepts/hcl|HCL]] 페이지에 따로 정리했다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]).

**모듈**은 함께 관리되는 리소스 묶음이다. 루트 모듈이 자식 모듈을 호출하는 구조이고, 변수(입력)·로컬(내부 재사용)·출력(외부 노출)이 인터페이스 역할을 한다. 레지스트리로 공유하면 조직의 인프라 표준을 재사용 가능한 코드로 굳힐 수 있다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## CLI 주요 명령

주 명령은 순서대로 `init` → `validate` → `plan` → `apply` → `destroy`다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

- `init` — 프로바이더·모듈을 설치하고 작업 디렉터리를 준비한다. 멱등이라 언제 다시 실행해도 된다.
- `validate` — 구성이 문법적으로 맞는지 검증한다.
- `plan` → `apply` → `destroy` — 위 코어 워크플로 그대로다.

> **주의:** `terraform state` 계열이나 `import`로 state를 수동 조작할 수도 있다. 다만 잘못하면 Terraform이 리소스 추적을 잃어 비용 증가·보안 저하로 이어질 수 있어, 백업을 전제로 해야 한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 조직 도입 4단계

공식 문서는 도입 성숙도를 네 단계로 제시한다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

| 단계 | 무엇을 하는 시점인가 |
|---|---|
| Adopt | 개인 실무자가 혼자 쓰기 시작한다 |
| Collaborate | 원격 state 백엔드를 두고 팀이 함께 쓴다 |
| Scale | 인프라 소유권 경계와 클라우드 전략을 결정한다 |
| Govern | 조직 표준을 [[entities/sentinel\|Sentinel]]·[[entities/opa\|OPA]] 정책 코드로 자동 강제한다 |

## 이 위키에서의 등장

- **하네스 엔지니어링의 선례로** — 제작사 HashiCorp의 공동창립자가 '하네스' 개념을 대중화한 [[entities/mitchell-hashimoto|미첼 하시모토]]다. 또 다른 공동창립자 [[entities/armon-dadgar|아몬 다드가]]가 공식 문서에서 도구를 소개한다. "환경을 코드로 선언하고 자동으로 강제한다"는 [[concepts/harness-engineering|하네스 엔지니어링]]의 발상을 떠올려 보자. 그 사상적 선례가 Terraform으로 대표되는 IaC라는 연결이 성립한다 (연결 근거 → [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]).
- **검증 자동화의 인프라판으로** — plan/apply 분리와 PR speculative plan 리뷰 관행은 [[concepts/verification-automation|검증 자동화]]가 말하는 "실행 전 검증"의 인프라 영역 선례다. Govern 단계의 Sentinel 정책 강제는 [[concepts/hooks|훅]]식 "규칙의 코드화·자동 강제"의 선례다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).
- **클러스터 운영을 감싸는 도구로** — [[entities/k3s|K3s]] 공식 문서의 수동 업그레이드 절차 안내다. 이 절차가 Terraform 같은 외부 IaC 도구로 업그레이드를 자동화할 때의 바탕이 된다고 적었다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

> 다만 앞의 두 유비 자체는 소스가 말한 게 아니라 이 위키의 해석이다.

## 함께 읽기

- [[concepts/infrastructure-as-code|코드형 인프라]] — Terraform이 구현하는 개념 쪽 설명.
- [[concepts/hcl|HCL]] — 실제 구성 파일을 쓸 때 필요한 문법.
- [[entities/hashicorp|HashiCorp]] — 만든 회사, 그리고 하네스 개념과의 연결 고리.
- [[concepts/harness-engineering|하네스 엔지니어링]] — 같은 발상이 AI 에이전트 쪽으로 옮겨 간 결과.
- [[entities/k3s|K3s]] — 클러스터 업그레이드를 외부 IaC 도구로 감쌀 수 있다고 문서가 언급하는 대상.

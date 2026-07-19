---
title: Terraform 공식 문서 — 코어·언어·CLI 발췌
label: "#27 Terraform 공식 문서"
type: source
credibility: high
volatility: hot
created: 2026-07-19
updated: 2026-07-19
sources: []
tags: [코드형인프라, HashiCorp, 공식문서]
---

# Terraform 공식 문서 — 코어·언어·CLI 발췌

## 한 줄 요약

[[entities/hashicorp|HashiCorp]]의 Terraform 공식 문서에서 Introduction 전체와 구성 언어·CLI 개요 19페이지를 발췌한 자료로, **"쓰기 → 계획 → 적용(Write-Plan-Apply)" 워크플로**와 **상태(state) 파일**을 축으로 Terraform의 작동 원리와 팀 협업으로의 확장 경로를 설명한다.

## 핵심 내용

- **작동 원리**: Terraform은 각 플랫폼의 API를 호출하는 **프로바이더**(플러그인)를 통해 리소스를 생성·관리한다. 레지스트리에 AWS·Azure·GCP·Kubernetes·Helm·GitHub·Datadog 등 수천 개의 공개 프로바이더가 있다 (2026-07 기준).
- **코어 워크플로 3단계**: ① Write — 편집기에서 구성을 작성하며 `terraform plan`으로 짧은 피드백 루프를 돈다. ② Plan — 실행 계획(생성·수정·파괴될 리소스)을 사람이 검토·승인한다. ③ Apply — 승인 후에만 종속성 순서대로 실제 변경을 수행한다. 개인 → 팀(브랜치 + PR에 speculative plan을 첨부해 리뷰, CI에서 실행) → HCP Terraform(원격 state·변수 중앙화, PR 생성 시 자동 plan)으로 같은 루프가 확장된다.
- **state가 필수인 이유**: 구성과 실세계 객체의 1:1 매핑(예: `aws_instance.foo` ↔ 인스턴스 `i-abcd1234`), 리소스 삭제 시 순서 판단을 위한 종속성 메타데이터 보존, 대규모 인프라에서 API 조회를 대체하는 성능 캐시, 팀 동기화(원격 state + 잠금)의 네 가지 이유로 state 없이는 동작할 수 없다. state는 시크릿이 담길 수 있고 잠금이 없으므로 **버전 관리 시스템에 저장하지 말라**고 명시한다.
- **HCL 구성 언어**: 문법은 블록·인수·표현식 세 요소가 전부이며, 선언형이라 블록 순서는 의미가 없고 리소스 간 참조 관계로 종속성 그래프를 만들어 실행 순서를 결정한다. 언어의 주목적은 리소스 선언이고 나머지 기능은 전부 그것을 유연하게 만드는 보조다.
- **모듈과 변수**: 모듈은 함께 관리되는 리소스 묶음(루트 모듈이 자식 모듈을 호출)으로, 변수(입력)·로컬(내부 재사용)·출력(외부 노출)이 모듈의 인터페이스를 이룬다. 레지스트리로 공유해 조직 표준을 코드화한다.
- **CLI**: 주 명령은 `init`(프로바이더·모듈 설치, 멱등) → `validate` → `plan` → `apply` → `destroy`. state 수동 조작(`terraform state` 계열, `import`)은 관리 추적을 잃을 위험이 있어 백업을 전제로 한다.
- **경쟁 도구 대비 위치**: Chef·Puppet 같은 구성 관리 도구와는 상호 보완(Terraform은 데이터센터 수준 추상화, 구성 관리는 머신 내부 소프트웨어), CloudFormation·Heat와 달리 클라우드 불가지론적이며 **계획 단계와 실행 단계의 분리**가 차별점, Boto·Fog 같은 클라이언트 라이브러리와 달리 고수준 선언 문법을 제공한다.
- **도입 4단계**: Adopt(개인) → Collaborate(원격 state로 협업) → Scale(인프라 소유권 경계 설정) → Govern(Sentinel·OPA로 조직 표준을 정책 코드로 자동 강제).

## 주요 주장 / 데이터

- "Terraform은 인프라에 **불변(immutable) 접근**을 취해 서비스 업그레이드·변경의 복잡성을 줄인다."
- "다른 도구들은 계획과 실행을 결합해 운영자가 변경의 효과를 머릿속으로 추론하도록 강제하는데, 이는 대규모 인프라에서 금방 감당 불가능해진다. Terraform은 계획을 먼저 보여 주므로 운영자는 무슨 일이 일어날지 정확히 알고 자신 있게 적용할 수 있다."
- "티켓 기반 리뷰 프로세스는 개발을 늦추는 병목이다. 대신 Sentinel(policy-as-code 프레임워크)로 Terraform이 인프라를 변경하기 전에 규정 준수·거버넌스 정책을 자동 강제할 수 있다."
- state 없는 초기 프로토타입은 AWS 태그로 매핑을 시도했으나 "모든 리소스·클라우드가 태그를 지원하지는 않는다"는 문제로 폐기 — state 파일이 그 대체물이다.
- 팀 협업에서는 PR에 speculative plan 출력을 첨부해 "변경 의도가 계획에 실제로 반영됐는지"를 동료가 리뷰한다 — 머지 순서나 수동 변경 때문에 머지 후 최종 plan은 PR에서 본 것과 다를 수 있어 다시 검토한다.
- HashiCorp 공동창립자 아몬 다드가(Armon Dadgar)가 소개 영상에서 Terraform의 인프라 과제 해결을 설명한다.

## 기존 위키와의 연결

- 강화: [[concepts/infrastructure-as-code|코드형 인프라]]의 선언형·불변형 우위 주장을 공식 문서가 그대로 뒷받침하고, 구성 관리 도구(Chef·Puppet)와 프로비저닝 도구의 역할 구분도 공식화한다. [[entities/terraform|Terraform]]의 멀티 클라우드·종속성 그래프·병렬 프로비저닝 서술을 상세화한다. [[concepts/verification-automation|검증 자동화]]의 "실행 전 검증" 원리에 대해 plan/apply 분리·PR speculative plan 리뷰라는 인프라 영역 선례를 더한다. [[concepts/harness-engineering|하네스 엔지니어링]]의 "규칙의 코드화·자동 강제" 사상에 대해 Sentinel 정책 강제(Govern 단계)라는 선례를 더한다.
- 모순: 직접 모순 없음. 단 프레이밍 차이 — IBM 해설은 IaC 워크플로를 쓰기→버전→프로비저닝→배포 4단계로 (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]), 공식 문서는 쓰기→계획→적용 3단계로 잡아 **실행 전 '계획 검토·승인'을 독립 단계로 격상**시킨다. 두 소스 모두 기록한다.
- 신규: [[entities/armon-dadgar|아몬 다드가]](HashiCorp 공동창립자), [[entities/sentinel|Sentinel]](policy-as-code 프레임워크) 페이지 생성.

## 출처 정보

- raw: raw/hashicorp-terraform-docs.md
- 저자/발행처: HashiCorp (Terraform 공식 문서)
- 수집일: 2026-07-19 (Terraform v1.x 문서의 latest 기준)
- URL: https://developer.hashicorp.com/terraform/docs
- 범위: 사용자와 합의한 "코어 + 언어/CLI 기초" — Introduction 8페이지(정의·유스케이스·대안 비교 4종·도입 단계·코어 워크플로) + Language 개요 6페이지(개요·리소스·변수/출력·모듈·state·state 목적) + CLI 기초 5페이지(개요·기본 명령·init·프로비저닝·state 조작). HCP Terraform/Enterprise 상세·플러그인 개발·레지스트리·CDKTF는 제외.

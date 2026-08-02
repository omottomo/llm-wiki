---
title: Terraform HCL 문법 정리 (실제 구성 파일 기준 노트)
label: "#29 HCL 문법 정리"
type: source
credibility: medium
volatility: cold
created: 2026-08-02
updated: 2026-08-02
sources: []
tags: [코드형인프라, HashiCorp, 기초개념]
---

# Terraform HCL 문법 정리 (실제 구성 파일 기준 노트)

## 한 줄 요약

실제로 동작하는 AWS 배포 구성(`*.tf` 10개)을 읽으며 정리한 [[concepts/hcl|HCL]] 기본 문법 노트로, 블록 구조 → 최상위 블록 6종 → 메타 인수·표현식 → 파일 구성 → 명령 3개 순으로 [[entities/terraform|Terraform]] 구성 파일을 해독하는 데 필요한 최소 문법을 훑는다.

## 핵심 내용

- **블록 구조와 라벨 개수**: `블록타입 "라벨1" "라벨2" { 인자 = 값 }` 형태이며 라벨 개수는 블록 타입마다 고정이다 — `resource` 2개(리소스 타입, 이름), `variable` 1개, `terraform` 0개.
- **최상위 블록 6종**: `terraform`(자체 설정·backend) / `provider`(공급자 설정) / `resource`(내가 만드는 것) / `data`(이미 있는 것 조회) / `variable`(입력) / `output`(출력). `resource`와 `data`의 차이는 "만든다 vs 조회만 한다"이고, `data`는 참조 시 `data.` 접두어가 필수다.
- **provider alias**: 기본 provider 외에 `alias`를 붙인 provider를 여러 개 둘 수 있고, 리소스에서 `provider = aws.us_east_1`로 **명시해야만** 별칭 provider가 쓰인다. CloudFront용 인증서가 `us-east-1`에만 존재할 수 있어 생기는 패턴이다 (2026-08 기준).
- **인수 vs 중첩 블록**: `=`의 유무로 구분한다(`enabled = true`는 인수, `origin { ... }`은 중첩 블록). 중첩 블록은 반복 가능.
- **메타 인수**: `depends_on`·`count`·`for_each`·`provider`와 `lifecycle` 블록(`create_before_destroy`·`prevent_destroy`·`ignore_changes`)은 모든 리소스에 공통이다. `for_each`에 넘길 map은 `for dvo in ... : dvo.domain_name => {...}` 형태의 for expression으로 리스트에서 만들어 낸다.
- **표현식**: `${}` 보간은 문자열 안에서만 쓰고 순수 참조에 감싸면 경고가 난다. 리스트 컴프리헨션 `[for r in ... : r.fqdn]`, 들여쓰기를 제거하는 heredoc `<<-EOT`도 쓴다.
- **파일 이름은 의미가 없다**: 디렉터리의 `*.tf`는 전부 하나로 합쳐 읽히므로 `acm.tf`·`s3.tf` 분리는 사람 편의용 관례일 뿐이다.
- **참조가 곧 실행 순서**: 버킷 정책이 CloudFront 배포판 ARN을 참조하면 그 참조 때문에 배포판이 먼저 생성된다. 종속성 그래프가 자동 생성되므로 `depends_on`을 손으로 쓸 일은 거의 없다.
- **명령 3개**: `terraform init`(프로바이더 다운로드·backend 연결, 파일 추가 시 재실행) → `plan`(미리보기) → `apply`(적용).

## 주요 주장 / 데이터

- "`=` 유무로 인수와 중첩 블록을 구분한다" — 초보자가 가장 자주 헷갈리는 지점을 한 줄 규칙으로 환원한 것이 이 노트의 실용적 핵심이다.
- "파일 이름은 아무 의미 없다. `*.tf` 전부 하나로 합쳐서 읽는다" — 공식 문서의 "선언형이라 블록 순서는 의미가 없다"는 서술 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]])을 파일 단위로 확장한 관찰.
- `aws_iam_policy_document`는 `data` 블록이지만 클라우드 API를 호출하지 않는 **순수 계산용**이다 — JSON 정책을 HCL 문법으로 쓰게 해 주는 용도.
- `lifecycle { create_before_destroy = true }`의 실제 쓰임새로 "인증서 무중단 교체"를 든다.

## 기존 위키와의 연결

- 강화: [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]가 추상 수준에서 말한 "문법은 블록·인수·표현식이 전부", "선언형이라 순서 무의미", "참조에서 종속성 그래프 도출"을 실제 구성 파일 수준의 문법으로 구체화한다. [[entities/terraform|Terraform]] 페이지의 HCL·모듈 절이 요약만 담고 있던 부분을 [[concepts/hcl|HCL]] 전용 페이지로 분리·상세화하는 근거가 됐다. 변수(입력)·출력(노출)이 모듈 인터페이스를 이룬다는 공식 문서의 서술에 `default` 유무·`terraform.tfvars`·`-var` 주입 경로라는 실무 디테일을 더한다.
- 모순: 직접 모순 없음. 단 **범위 차이** — 이 노트는 최상위 블록을 6종으로 제시하지만, 이는 소형 구성에서 실제 쓰인 집합이지 언어가 지원하는 전부는 아니다. 공식 문서는 `module` 호출과 로컬 값도 언어 구성 요소로 다룬다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). 양쪽을 모두 기록하되 개념 페이지에는 "6종은 전부가 아니다"를 명시했다.
- 신규: [[concepts/hcl|HCL]] 개념 페이지 신설.

## 출처 정보

- raw: raw/terraform-hcl-syntax.md
- 저자: 위키 운영자 본인 정리 노트 — 이 저장소의 배포용 Terraform 구성 파일을 읽으며 작성
- 수집일: 2026-08-02
- URL: 없음(로컬 작성 노트)
- 성격: 1차 자료가 아닌 파생 노트. 문법 주장은 [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]와 실제 동작하는 구성 파일로 교차 확인 가능해 credibility=medium, 고정 스냅샷이라 volatility=cold.

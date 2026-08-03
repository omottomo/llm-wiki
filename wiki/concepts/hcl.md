---
title: HCL (HashiCorp 구성 언어)
type: concept
created: 2026-08-02
updated: 2026-08-03
sources: [terraform-hcl-syntax, hashicorp-terraform-docs]
aliases: [HCL, HashiCorp Configuration Language]
tags: [코드형인프라, HashiCorp, 기초개념]
---

# HCL (HashiCorp 구성 언어)

## 한눈에 요약

- Terraform 구성을 작성하는 **선언형 언어**다. 무엇을 만들지 적으면 순서는 알아서 정해진다.
- 문법은 **블록·인수·표현식** 세 요소가 전부다. 나머지 기능은 이 셋을 유연하게 만드는 보조다.
- 파일 이름과 블록 순서에는 의미가 없다. 디렉터리 안 `*.tf`를 전부 합쳐 읽는다.
- 실행 순서는 사람이 쓰는 게 아니라 **참조 관계에서 자동으로 도출**된다.

## 세 요소가 전부다

[[entities/terraform|Terraform]] 구성을 작성하는 선언형 언어다. 공식 문서는 문법이 **블록·인수·표현식** 세 요소가 전부라고 정리한다. 언어의 주목적은 리소스 선언이고, 나머지 기능은 전부 그것을 유연하게 만드는 보조다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

아래는 그 세 요소를 실제 구성 파일 수준에서 풀어 쓴 것이다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]).

## 블록 구조

```hcl
블록타입 "라벨1" "라벨2" {
  인자 = 값
}
```

라벨 개수는 블록 타입마다 정해져 있다 — `resource`는 2개(리소스 타입, 이름), `variable`은 1개, `terraform`은 0개다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]).

## 자주 쓰는 최상위 블록

| 블록 | 역할 |
|---|---|
| `terraform` | Terraform 자체 설정(버전 제약, backend) |
| `provider` | AWS 등 공급자 설정 |
| `resource` | **내가 만드는** 인프라 |
| `data` | **이미 있는 것 조회** — 만들지도 지우지도 않음 |
| `variable` | 입력값 |
| `output` | 출력값, `terraform output`으로 추출 |

이 6종은 소형 구성에서 실제로 쓰이는 집합이고 언어가 지원하는 최상위 블록의 전부는 아니다 — 공식 문서는 `module`(자식 모듈 호출)과 로컬 값도 언어 구성 요소로 다룬다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

### resource와 data

```hcl
resource "aws_s3_bucket" "site" {
  bucket = var.site_bucket_name
}

data "aws_route53_zone" "main" {
  name = var.domain      # 검색 조건
}
```

리소스 타입(`aws_s3_bucket`)은 공급자가 정하고, 두 번째 라벨(`site`)은 구성 안에서만 통하는 이름이다. 참조는 `타입.이름.속성` 형태(`aws_s3_bucket.site.arn`)이며, `data` 블록은 참조할 때 `data.` 접두어가 필수다(`data.aws_route53_zone.main.zone_id`). `aws_iam_policy_document`처럼 클라우드 API를 전혀 호출하지 않고 JSON 정책을 HCL로 쓰게 해 주는 순수 계산용 `data` 소스도 있다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]).

### variable과 output

`variable` 블록에 `default`가 없으면 값 입력이 필수가 되고, 값은 `terraform.tfvars` 파일이나 `-var="domain=x.com"` 플래그로 주입한다. 참조는 `var.<이름>`. `output`은 배포판 ID처럼 CI로 넘겨야 할 값을 밖으로 노출한다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]). 이 변수(입력)·출력 쌍이 곧 [[entities/terraform|Terraform]] 모듈의 인터페이스라는 것이 공식 문서의 설명이다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## provider alias

기본 `provider` 하나에 별칭 provider를 여러 개 붙일 수 있고, 별칭을 쓰려면 리소스 쪽에서 **명시**해야 한다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]).

```hcl
provider "aws" { region = "ap-northeast-2" }   # 기본

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

resource "aws_acm_certificate" "site" {
  provider = aws.us_east_1     # 이 줄이 없으면 기본 provider 사용
}
```

CloudFront가 쓰는 인증서는 반드시 `us-east-1` 리전에 있어야 해서 이 패턴이 필요하다 (2026-08 기준).

## 인수 vs 중첩 블록

`=`의 유무로 구분한다 — `enabled = true`는 인수, `origin { ... }`은 중첩 블록이다. 중첩 블록은 같은 블록 안에서 여러 번 반복할 수 있다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]).

## 메타 인수

모든 `resource`에 공통으로 붙는 인수들이다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]).

```hcl
depends_on = [aws_s3_bucket.site]   # 명시적 순서. 보통 불필요
count      = 3                       # 개수만큼 복제
for_each   = { ... }                 # map/set 순회. each.key / each.value
provider   = aws.us_east_1           # provider 지정

lifecycle {
  create_before_destroy = true       # 지우기 전에 새로 만듦(인증서 무중단 교체)
  prevent_destroy       = true       # 삭제 차단
  ignore_changes        = [tags]     # 해당 속성 변경 무시
}
```

## 표현식

- `"${aws_s3_bucket.site.arn}/*"` — 문자열 보간은 문자열 안에서만 쓴다. 순수 참조에 `${}`를 감싸면 경고가 뜬다.
- `[for r in aws_route53_record.x : r.fqdn]` — 리스트 컴프리헨션. `for ... in ... : 키 => 값` 형태로 쓰면 리스트를 map으로 바꾸는 for expression이 되고, `for_each`에 넘길 map을 만들 때 쓴다.
- `<<-EOT ... EOT` — heredoc. `-`를 붙이면 들여쓰기가 제거된다.

## 파일 이름은 의미가 없다

Terraform은 디렉터리 안의 `*.tf`를 전부 하나로 합쳐 읽는다. `acm.tf`·`s3.tf`처럼 나누는 것은 순전히 사람이 보기 편하라는 관례다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]). 블록 순서에 의미가 없다는 공식 문서의 선언형 서술과 같은 이야기의 파일 단위 버전이다 (→ [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

## 참조가 곧 실행 순서

버킷 정책이 배포판의 ARN을 참조하면, 그 참조 때문에 Terraform이 배포판을 먼저 만들고 정책을 나중에 붙인다. 종속성 그래프가 참조에서 자동으로 만들어지므로 `depends_on`을 손으로 쓸 일은 거의 없다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]·[[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]). 이것이 [[concepts/infrastructure-as-code|코드형 인프라]]의 선언형 특성이 문법 수준에서 드러나는 지점이다 — 순서를 사람이 쓰는 것이 아니라 관계에서 도출된다.

## 관련 명령

작성한 구성은 세 명령으로 다룬다 (→ [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]]·[[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]]).

- `terraform init` — 프로바이더를 내려받고 backend에 연결한다. 파일을 추가하면 다시 실행한다.
- `terraform plan` — 변경을 미리 본다. 실제로는 아무것도 바꾸지 않는다.
- `terraform apply` — 적용한다.

공식 문서의 Write-Plan-Apply 코어 워크플로가 명령 수준에서는 이 셋으로 나타난다.

## 함께 읽기

- [[entities/terraform|Terraform]] — 이 언어로 구성을 쓰는 도구
- [[concepts/infrastructure-as-code|코드형 인프라]] — 선언형이라는 성질이 나오는 상위 개념
- [[entities/hashicorp|HashiCorp]] — 언어와 도구를 만든 회사

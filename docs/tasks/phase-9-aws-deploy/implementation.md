# Phase 9 — AWS 배포 실행 가이드 (단계별 커맨드)

<!-- LANGUAGE EXCEPTION: 사용자가 직접 실행하는 작업 문서 — 한국어 유지. 영어로 되돌리지 말 것. -->

> 설계 배경·아키텍처 근거는 [plan.md](plan.md) 참조. 이 문서는 **터미널에 그대로 입력하는
> 실행 순서**다. 위에서 아래로 진행. 각 Task 끝의 검증이 통과해야 다음 Task로.

**목표:** `site/dist`를 S3 + CloudFront + Route53 도메인으로 HTTPS 배포. 인프라는 Terraform, 업로드는 GitHub Actions OIDC.

**치환 값 (진행하며 결정되는 값 — 아래 표에 적어두고 계속 참조):**

| 표기 | 의미 | 예시 |
|---|---|---|
| `<ACCOUNT_ID>` | AWS 계정 ID (12자리) | `123456789012` |
| `<DOMAIN>` | 구매한 도메인 | `example.com` |
| `<STATE_BUCKET>` | TF state 버킷명 | `llm-wiki-tfstate-<ACCOUNT_ID>` |
| `<SITE_BUCKET>` | 사이트 콘텐츠 버킷명 | `llm-wiki-site-<ACCOUNT_ID>` |
| `<CF_DIST_ID>` | CloudFront 배포판 ID (Task 6 출력) | `E1ABCDEF234567` |
| `<ROLE_ARN>` | 배포 role ARN (Task 9 출력) | `arn:aws:iam::…:role/llm-wiki-deploy` |

**전역 제약:** Terraform ≥ 1.10 / ACM은 `us-east-1` / 나머지는 `ap-northeast-2` /
배포 전 `scripts/verify_site.py` exit 0 필수 / 레포 private 유지.

---

## Task 0 — 도구 설치 + AWS 자격 증명

- [x] **0.1 설치**

```bash
brew install awscli terraform
```

- [x] **0.2 버전 확인**

```bash
aws --version        # aws-cli/2.x 이상
terraform version    # v1.10 이상이어야 함 (S3 백엔드 네이티브 락)
```

- [x] **0.3 프로파일 설정** (IAM 사용자의 access key 준비)

```bash
aws configure --profile llm-wiki
# Access Key ID / Secret / region: ap-northeast-2 / output: json
```

- [x] **0.4 자격 증명 + 계정 ID 확인**

```bash
export AWS_PROFILE=llm-wiki      # 이후 모든 aws/terraform 명령이 이 프로파일 사용
aws sts get-caller-identity --query Account --output text
```

출력된 12자리 = `<ACCOUNT_ID>`. 표에 기록.

> 이 `export`는 셸 세션마다 다시 실행 (또는 `~/.zshrc`에 추가).

---

## Task 1 — TF state 버킷 (CLI 수동 생성)

state 버킷은 Terraform 밖에서 만든다 (순환 문제). 4개 명령.

- [x] **1.1 버킷 생성**

```bash
aws s3api create-bucket \
  --bucket llm-wiki-tfstate-<ACCOUNT_ID> \
  --region ap-northeast-2 \
  --create-bucket-configuration LocationConstraint=ap-northeast-2
```

- [x] **1.2 버저닝 (state 이력 보존)**

```bash
aws s3api put-bucket-versioning \
  --bucket llm-wiki-tfstate-<ACCOUNT_ID> \
  --versioning-configuration Status=Enabled
```

- [x] **1.3 퍼블릭 차단**

```bash
aws s3api put-public-access-block \
  --bucket llm-wiki-tfstate-<ACCOUNT_ID> \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

- [ ] **1.4 암호화**

```bash
aws s3api put-bucket-encryption \
  --bucket llm-wiki-tfstate-<ACCOUNT_ID> \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

- [x] **1.5 검증**

```bash
aws s3api get-bucket-versioning --bucket llm-wiki-tfstate-<ACCOUNT_ID>
# 기대: "Status": "Enabled"
```

---

## Task 2 — 도메인 구매 (콘솔)

도메인 등록은 Terraform 리소스가 아님 — 콘솔에서 1회 수동.

- [x] **2.1** AWS 콘솔 → Route53 → **Registered domains** → **Register domains** → 원하는 이름 검색 → 구매 (연락처 입력, privacy protection 기본 on 유지)
- [x] **2.2** 등록 완료 메일 대기 (수분–수십 분). 상태 확인:

```bash
aws route53domains list-domains --region us-east-1
# 도메인 API는 us-east-1 전용
```

- [x] **2.3** 구매 시 자동 생성된 hosted zone 확인:

```bash
aws route53 list-hosted-zones --query "HostedZones[].Name"
# 기대: "<DOMAIN>." 포함
```

`<DOMAIN>` 표에 기록.

---

## Task 3 — Terraform 스캐폴드 + init

- [x] **3.1 디렉터리 + .gitignore**

```bash
mkdir -p infra
cat >> .gitignore <<'EOF'

# terraform
infra/.terraform/
*.tfstate
*.tfstate.*
EOF
```

(`.terraform.lock.hcl`은 커밋 대상 — ignore에 넣지 않는다)

- [x] **3.2 `infra/versions.tf`**

```hcl
terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket       = "llm-wiki-tfstate-<ACCOUNT_ID>" # 실제 값으로 교체
    key          = "llm-wiki/terraform.tfstate"
    region       = "ap-northeast-2"
    use_lockfile = true # TF 1.10+ 네이티브 락 — DynamoDB 불필요
  }
}
```

- [x] **3.3 `infra/providers.tf`**

```hcl
provider "aws" {
  region = "ap-northeast-2"
}

# CloudFront용 ACM 인증서는 반드시 us-east-1
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}
```

- [x] **3.4 `infra/variables.tf`**

```hcl
variable "domain" {
  description = "사이트 도메인 (Route53에서 구매한 것)"
  type        = string
}

variable "site_bucket_name" {
  description = "사이트 콘텐츠 S3 버킷명"
  type        = string
}

variable "github_repo" {
  description = "OIDC trust 대상 GitHub 레포 (owner/name)"
  type        = string
  default     = "omottomo/llm-wiki"
}
```

- [x] **3.5 `infra/terraform.tfvars`** (커밋해도 됨 — 비밀값 없음)

```hcl
domain           = "<DOMAIN>"
site_bucket_name = "llm-wiki-site-<ACCOUNT_ID>"
```

- [x] **3.6 init + 검증**

```bash
cd infra
terraform init
# 기대: "Successfully configured the backend \"s3\"" + "Terraform has been successfully initialized!"
terraform validate
# 기대: "Success! The configuration is valid."
```

- [x] **3.7 커밋**

```bash
cd ..
git add .gitignore infra/
git commit -m "feat(infra): terraform scaffold — s3 backend, providers, variables"
```

---

## Task 4 — ACM 인증서 (us-east-1) + DNS 검증

- [x] **4.1 `infra/acm.tf`**

```hcl
data "aws_route53_zone" "main" {
  name         = var.domain
  private_zone = false
}

resource "aws_acm_certificate" "site" {
  provider          = aws.us_east_1
  domain_name       = var.domain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# 인증서 검증용 DNS 레코드 (ACM이 요구하는 CNAME)
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.site.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      type   = dvo.resource_record_type
      record = dvo.resource_record_value
    }
  }

  zone_id = data.aws_route53_zone.main.zone_id
  name    = each.value.name
  type    = each.value.type
  records = [each.value.record]
  ttl     = 300
}

# 검증 완료까지 대기 — 이게 완료돼야 CloudFront에 붙일 수 있음
resource "aws_acm_certificate_validation" "site" {
  provider                = aws.us_east_1
  certificate_arn         = aws_acm_certificate.site.arn
  validation_record_fqdns = [for r in aws_route53_record.cert_validation : r.fqdn]
}
```

- [x] **4.2 apply**

```bash
cd infra
terraform plan    # 리소스 3종 추가 확인
terraform apply   # yes 입력. 검증 대기 수 분 소요
```

- [ ] **4.3 검증**

```bash
aws acm list-certificates --region us-east-1 \
  --query "CertificateSummaryList[?DomainName=='<DOMAIN>'].Status"
# 기대: "ISSUED"
```

- [ ] **4.4 커밋**

```bash
cd ..
git add infra/acm.tf infra/.terraform.lock.hcl
git commit -m "feat(infra): ACM certificate (us-east-1) with DNS validation"
```

---

## Task 5 — 사이트 콘텐츠 S3 버킷

- [ ] **5.1 `infra/s3.tf`**

```hcl
resource "aws_s3_bucket" "site" {
  bucket = var.site_bucket_name
}

resource "aws_s3_bucket_versioning" "site" {
  bucket = aws_s3_bucket.site.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "site" {
  bucket                  = aws_s3_bucket.site.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

(버킷 정책은 CloudFront 배포판 ARN이 필요해서 Task 6에서 추가)

- [ ] **5.2 apply + 검증**

```bash
cd infra && terraform apply
aws s3api head-bucket --bucket llm-wiki-site-<ACCOUNT_ID> && echo OK
# 기대: OK
```

- [ ] **5.3 커밋**

```bash
cd ..
git add infra/s3.tf
git commit -m "feat(infra): private site content bucket"
```

---

## Task 6 — CloudFront (Function + OAC + 배포판 + 버킷 정책)

이 Task가 제일 큼. 파일 하나에 4개 리소스.

- [ ] **6.1 `infra/cloudfront.tf`**

```hcl
# pretty URL 재작성: /foo/ → /foo/index.html — OAC 아키텍처의 필수 조각
resource "aws_cloudfront_function" "rewrite_index" {
  name    = "llm-wiki-rewrite-index"
  runtime = "cloudfront-js-2.0"
  publish = true
  code    = <<-EOT
    function handler(event) {
      var request = event.request;
      var uri = request.uri;
      if (uri.endsWith('/')) {
        request.uri = uri + 'index.html';
      } else if (!uri.split('/').pop().includes('.')) {
        request.uri = uri + '/index.html';
      }
      return request;
    }
  EOT
}

resource "aws_cloudfront_origin_access_control" "site" {
  name                              = "llm-wiki-site-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "site" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  aliases             = [var.domain]
  price_class         = "PriceClass_200" # 아시아 포함, 남미/오세아니아 제외

  origin {
    domain_name              = aws_s3_bucket.site.bucket_regional_domain_name
    origin_id                = "s3-site"
    origin_access_control_id = aws_cloudfront_origin_access_control.site.id
  }

  default_cache_behavior {
    target_origin_id       = "s3-site"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    # AWS managed "CachingOptimized" 정책
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.rewrite_index.arn
    }
  }

  # OAC에서 없는 키 = S3가 403 반환 → 둘 다 404 페이지로
  custom_error_response {
    error_code         = 403
    response_code      = 404
    response_page_path = "/404.html"
  }
  custom_error_response {
    error_code         = 404
    response_code      = 404
    response_page_path = "/404.html"
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.site.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

# 버킷 정책: 이 배포판을 통해서만 GetObject 허용
data "aws_iam_policy_document" "site_bucket" {
  statement {
    sid       = "AllowCloudFrontOAC"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.site.arn}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.site.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "site" {
  bucket = aws_s3_bucket.site.id
  policy = data.aws_iam_policy_document.site_bucket.json
}
```

- [ ] **6.2 `infra/outputs.tf`**

```hcl
output "cf_distribution_id" {
  value = aws_cloudfront_distribution.site.id
}

output "cf_domain_name" {
  value = aws_cloudfront_distribution.site.domain_name
}

output "site_bucket" {
  value = aws_s3_bucket.site.id
}
```

- [ ] **6.3 apply** (배포판 생성 5–15분 — 기다림)

```bash
cd infra && terraform apply
terraform output
# cf_distribution_id 값 = <CF_DIST_ID>, 표에 기록
```

- [ ] **6.4 커밋**

```bash
cd ..
git add infra/cloudfront.tf infra/outputs.tf
git commit -m "feat(infra): cloudfront distribution with OAC, index rewrite function, error mapping"
```

---

## Task 7 — Route53 alias 레코드

- [ ] **7.1 `infra/dns.tf`**

```hcl
resource "aws_route53_record" "site_a" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.site.domain_name
    zone_id                = aws_cloudfront_distribution.site.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "site_aaaa" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.domain
  type    = "AAAA"

  alias {
    name                   = aws_cloudfront_distribution.site.domain_name
    zone_id                = aws_cloudfront_distribution.site.hosted_zone_id
    evaluate_target_health = false
  }
}
```

- [ ] **7.2 apply + 검증**

```bash
cd infra && terraform apply
dig +short <DOMAIN>
# 기대: CloudFront IP 여러 개 (전파에 수 분 걸릴 수 있음)
```

- [ ] **7.3 커밋**

```bash
cd ..
git add infra/dns.tf
git commit -m "feat(infra): route53 A/AAAA alias to cloudfront"
```

---

## Task 8 — 수동 첫 배포 (CI 만들기 전에 인프라 검증)

- [ ] **8.1 빌드 + 게이트**

```bash
pip install -r site/requirements.txt
python3 site/build.py
npx -y pagefind@1 --site site/dist
python3 site/test_build_site.py
python3 scripts/verify_site.py
echo "exit=$?"   # 기대: exit=0 — 0 아니면 배포 중단 (raw/ 유출 게이트)
```

- [ ] **8.2 업로드 (Cache-Control 차등 — 2회 sync)**

```bash
# 1) 장기 캐시: pagefind 에셋 등 (파일명이 내용 따라 바뀌므로 immutable 안전)
aws s3 sync site/dist "s3://llm-wiki-site-<ACCOUNT_ID>" \
  --delete \
  --exclude "*.html" --exclude "style.css" \
  --cache-control "public,max-age=31536000,immutable"

# 2) 짧은 캐시: HTML + style.css (파일명 고정, 내용 가변)
#    --delete 필수: 위키에서 삭제된 페이지의 HTML을 버킷에서도 제거
aws s3 sync site/dist "s3://llm-wiki-site-<ACCOUNT_ID>" \
  --delete \
  --exclude "*" --include "*.html" --include "style.css" \
  --cache-control "public,max-age=0,must-revalidate"
```

- [ ] **8.3 무효화**

```bash
aws cloudfront create-invalidation --distribution-id <CF_DIST_ID> --paths "/*"
```

- [ ] **8.4 검증 (전부 통과해야 Task 9 진행)**

```bash
curl -I https://<DOMAIN>/                          # 기대: 200, content-type: text/html
curl -I https://<DOMAIN>/overview/                 # 기대: 200 — Function 재작성 검증
curl -I https://<DOMAIN>/no-such-page/             # 기대: 404 (403이면 error response 오류)
curl -sI http://<DOMAIN>/ | head -1                # 기대: 301 (HTTPS 리다이렉트)
# 한글 태그 페이지 (예: 'AI' 대신 실제 태그로 — site/dist/tags/ 에서 하나 골라 인코딩)
python3 -c "from urllib.parse import quote; print('https://<DOMAIN>/tags/' + quote('테라폼') + '/')"
curl -I "$(python3 -c "from urllib.parse import quote; print('https://<DOMAIN>/tags/' + quote('테라폼') + '/')")"
# 기대: 200
# raw/ 경계 최종 확인
aws s3 ls "s3://llm-wiki-site-<ACCOUNT_ID>" --recursive | grep -i raw
# 기대: 출력 없음
```

- [ ] **8.5** 브라우저에서 `https://<DOMAIN>/` 열고 Pagefind 한국어 검색 + 다크모드 확인

---

## Task 9 — GitHub OIDC + 배포 role

- [ ] **9.1 `infra/iam-deploy.tf`**

```hcl
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  # AWS가 GitHub OIDC는 루트 CA로 검증하므로 형식상 값
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

data "aws_iam_policy_document" "deploy_trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # main 브랜치에서만 assume 가능
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repo}:ref:refs/heads/main"]
    }
  }
}

resource "aws_iam_role" "deploy" {
  name               = "llm-wiki-deploy"
  assume_role_policy = data.aws_iam_policy_document.deploy_trust.json
}

data "aws_iam_policy_document" "deploy_permissions" {
  statement {
    sid       = "SyncBucket"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.site.arn]
  }
  statement {
    sid       = "SyncObjects"
    actions   = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
    resources = ["${aws_s3_bucket.site.arn}/*"]
  }
  statement {
    sid       = "Invalidate"
    actions   = ["cloudfront:CreateInvalidation"]
    resources = [aws_cloudfront_distribution.site.arn]
  }
}

resource "aws_iam_role_policy" "deploy" {
  name   = "deploy-site"
  role   = aws_iam_role.deploy.id
  policy = data.aws_iam_policy_document.deploy_permissions.json
}
```

- [ ] **9.2 `infra/outputs.tf`에 추가**

```hcl
output "deploy_role_arn" {
  value = aws_iam_role.deploy.arn
}
```

- [ ] **9.3 apply + 기록**

```bash
cd infra && terraform apply
terraform output deploy_role_arn   # = <ROLE_ARN>, 표에 기록
```

- [ ] **9.4 커밋**

```bash
cd ..
git add infra/iam-deploy.tf infra/outputs.tf
git commit -m "feat(infra): github OIDC provider + least-privilege deploy role"
```

---

## Task 10 — GitHub Actions 배포 워크플로

- [ ] **10.1 repo variables 등록** (`gh` CLI 없으면 GitHub 웹 Settings → Secrets and variables → Actions → Variables)

```bash
gh variable set AWS_DEPLOY_ROLE_ARN --body "<ROLE_ARN>"
gh variable set SITE_BUCKET --body "llm-wiki-site-<ACCOUNT_ID>"
gh variable set CF_DISTRIBUTION_ID --body "<CF_DIST_ID>"
gh variable list   # 3개 확인
```

- [ ] **10.2 `.github/workflows/deploy-site.yml`**

```yaml
name: deploy-site

on:
  push:
    branches: [main]
    paths:
      - "wiki/**"
      - "site/**"
      - "scripts/**"
      - ".github/workflows/deploy-site.yml"

permissions:
  id-token: write   # OIDC 필수
  contents: read

concurrency:
  group: deploy-site
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Build site
        run: |
          pip install -r site/requirements.txt
          python3 site/build.py
          npx -y pagefind@1 --site site/dist

      - name: Verify gate (raw/ leak audit — fail = no deploy)
        run: |
          python3 site/test_build_site.py
          python3 scripts/verify_site.py

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ap-northeast-2

      - name: Sync long-cache assets
        run: |
          aws s3 sync site/dist "s3://${{ vars.SITE_BUCKET }}" \
            --delete \
            --exclude "*.html" --exclude "style.css" \
            --cache-control "public,max-age=31536000,immutable"

      - name: Sync short-cache HTML/CSS
        run: |
          aws s3 sync site/dist "s3://${{ vars.SITE_BUCKET }}" \
            --delete \
            --exclude "*" --include "*.html" --include "style.css" \
            --cache-control "public,max-age=0,must-revalidate"

      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ vars.CF_DISTRIBUTION_ID }} \
            --paths "/*"
```

- [ ] **10.3 커밋 + push → main 머지**

```bash
git add .github/workflows/deploy-site.yml
git commit -m "ci(site): deploy-site workflow — OIDC, verify gate, differential cache-control"
# 현재 브랜치를 main에 머지/push하는 시점에 워크플로 발동
```

- [ ] **10.4 실행 확인**

```bash
gh run watch          # deploy-site 잡이 녹색으로 끝나는지 지켜봄
gh run list --workflow=deploy-site --limit 1
# 기대: completed  success
```

- [ ] **10.5** wiki 페이지 하나 수정해 push → 자동 배포 + 사이트 반영 확인 (end-to-end)

---

## Task 11 — 마무리 (문서 + 선택 항목)

- [ ] **11.1 (선택) 과금 알림**

```bash
# 콘솔: Billing → Budgets → Create budget → Cost budget → $5/월 → 이메일 알림
```

- [ ] **11.2 문서 갱신** — 에이전트에게 요청 가능:
  - `docs/rules/site-code.md` §2: Cloudflare Pages → AWS 구성으로 재작성
  - `docs/index.md` 갱신
  - `docs/log.md`에 `site` 한 줄 (phase 마감)
- [ ] **11.3 최종 커밋 확인**

```bash
git status          # infra/*.tf, lock 파일, workflow 전부 커밋됐는지
git log --oneline -8
```

---

## 문제 발생 시 빠른 진단

| 증상 | 원인 후보 | 확인 |
|---|---|---|
| 서브페이지 403/404 | Function 미연결/오류 | `aws cloudfront describe-function --name llm-wiki-rewrite-index` |
| 루트도 403 | 버킷 정책 SourceArn 불일치 | Task 6.1 정책의 배포판 ARN 확인 |
| 인증서 검증 안 끝남 | hosted zone 불일치 | `dig _acme… CNAME` 대신 `aws acm describe-certificate` 로 대기 레코드 확인 |
| Actions에서 AssumeRole 실패 | trust의 `sub` 불일치 | 브랜치가 main인지, `repo:owner/name` 철자 확인 |
| 배포했는데 옛 콘텐츠 | 캐시 | invalidation 실행 여부 + 브라우저 강력 새로고침 |

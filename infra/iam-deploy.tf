resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
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

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values = [
        "repo:${var.github_repo_immutable}:ref:refs/heads/main", # 현재 발급되는 형식
        "repo:${var.github_repo}:ref:refs/heads/main",           # 레거시 형식 (폴백)
      ]
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

# ---------------------------------------------------------------------------
# PR용 terraform plan 역할 (읽기 전용)
#
# 위의 deploy 역할은 재사용할 수 없다. deploy_trust는 sub를
# `...:ref:refs/heads/main`으로 핀하는데, pull_request 이벤트가 발급하는 sub
# 클레임은 `...:pull_request` 형식이라 매칭되지 않는다. (github.ref 값과 sub
# 클레임은 서로 다르다 — 신뢰 정책에 들어가는 건 후자다.)
# ---------------------------------------------------------------------------

locals {
  # versions.tf의 backend "s3" 블록과 반드시 같아야 한다. Terraform은 backend
  # 설정에서 변수 보간을 금지하므로 이 중복은 피할 수 없다 — 한쪽을 고치면
  # 다른 쪽도 고쳐야 한다.
  tfstate_bucket = "llm-wiki-tfstate-<ACCOUNT_ID>"
  tfstate_key    = "llm-wiki/terraform.tfstate"
}

data "aws_iam_policy_document" "plan_trust" {
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

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values = [
        "repo:${var.github_repo_immutable}:pull_request", # 현재 발급되는 형식
        "repo:${var.github_repo}:pull_request",           # 레거시 형식 (폴백)
      ]
    }
  }
}

resource "aws_iam_role" "plan" {
  name               = "llm-wiki-plan"
  assume_role_policy = data.aws_iam_policy_document.plan_trust.json
}

# 쓰기 액션은 하나도 없다. plan은 -lock=false로 돌리므로 S3 네이티브 상태 잠금
# (versions.tf의 use_lockfile)이 요구하는 s3:PutObject/DeleteObject도 필요 없다.
# AWS 관리형 ReadOnlyAccess는 쓰지 않는다 — 계정 전체 읽기 권한을 PR을 열 수 있는
# 누구에게나 주게 된다.
data "aws_iam_policy_document" "plan_permissions" {
  # 상태 파일. plan은 여기서 현재 상태를 읽는다.
  statement {
    sid       = "ReadState"
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::${local.tfstate_bucket}/${local.tfstate_key}"]
  }

  statement {
    sid       = "ListStateBucket"
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::${local.tfstate_bucket}"]
  }

  # 데이터가 실제로 담기는 서비스라 버킷 단위로 좁힌다.
  statement {
    sid     = "ReadSiteBucket"
    actions = ["s3:Get*", "s3:List*"]
    resources = [
      aws_s3_bucket.site.arn,
      "${aws_s3_bucket.site.arn}/*",
    ]
  }

  # 설정 메타데이터만 있는 서비스들. 리소스 단위로 좁히면 refresh가 읽는 액션을
  # 하나만 빠뜨려도 plan이 깨지므로, 대신 서비스 범위를 infra/가 실제로 쓰는
  # 다섯 개로 제한한다.
  statement {
    sid = "ReadInfraConfig"
    actions = [
      "cloudfront:Get*",
      "cloudfront:List*",
      "acm:Describe*",
      "acm:List*",
      "route53:Get*",
      "route53:List*",
      "iam:Get*",
      "iam:List*",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "plan" {
  name   = "plan-infra"
  role   = aws_iam_role.plan.id
  policy = data.aws_iam_policy_document.plan_permissions.json
}

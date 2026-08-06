variable "domain" {
  type = string
}

variable "site_bucket_name" {
  type = string
}

# versions.tf 의 backend "s3" 부분 구성(backend.hcl)의 bucket 과 같은 값이어야 한다.
# backend 블록은 변수 보간을 금지해서 이 중복은 피할 수 없다 — 한쪽을 고치면 다른 쪽도.
variable "tfstate_bucket_name" {
  type = string
}

variable "github_repo" {
  type    = string
  default = "omottomo/llm-wiki"
}

# GitHub은 OIDC sub 클레임에 immutable 형식(owner@ownerID/repo@repoID)을 넣어 발급한다.
# 값 확인: gh api repos/<owner>/<repo>/actions/oidc/customization/sub → sub_claim_prefix
variable "github_repo_immutable" {
  type    = string
  default = "omottomo@248242903/llm-wiki@1324905842"
}

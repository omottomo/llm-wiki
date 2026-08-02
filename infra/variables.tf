variable "domain" {
  type = string
}

variable "site_bucket_name" {
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
  default = "omottomo@248242903/llm-wiki@1298234217"
}

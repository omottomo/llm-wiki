terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # bucket 이름에 AWS 계정 ID가 들어가는데 이 저장소는 공개다. backend 블록은
  # 변수 보간을 금지하므로 bucket 만 부분 구성(partial config)으로 뺐다.
  # 반드시: terraform init -backend-config=backend.hcl  (backend.hcl 은 gitignore)
  backend "s3" {
    key          = "llm-wiki/terraform.tfstate"
    region       = "ap-northeast-2"
    use_lockfile = true
  }
}

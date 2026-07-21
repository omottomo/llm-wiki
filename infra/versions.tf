terraform {
  required_version = ">= 1.10"
  
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket = "llm-wiki-tfstate-<ACCOUNT_ID>"
    key = "llm-wiki/terraform.tfstate"
    region = "ap-northeast-2"
    use_lockfile = true
  }
}

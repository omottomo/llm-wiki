provider "aws" {
  regions = "ap-northeast-2"
}

provider "aws" {
  alias = "us_east_1"
  region = "us-east-1"
}

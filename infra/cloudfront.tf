resource "aws_cloudfront_function" "rewrite_index" {
  name = "llm-wiki-rewrite-index"
  runtime = "cloudfront-js-2.0"
  publish = true
  code = <<-EOT
    function handler(event) {
      var request = event.request;
      var uri = request.uri;
      if(uri.endsWith('/')) {
        request.uri = uri + 'index.html';
      } else if(!uri.split('/').pop().includes('.')) {
        request.uri = uri + '/index.html';
      }
      return request;
    }
  EOT
}

resource "aws_cloudfront_origin_access_control" "site" {
  name = "llm-wiki-site-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior = "always"
  signing_protocol = "sigv4"
}

resource "aws_cloudfront_distribution" "site" {
  enabled = true
  is_ipv6_enabled = true
  default_root_object = "index.html"
  aliases = [var.domain]
  price_class = "PriceClass_200"


  origin {
    domain_name = aws_s3_bucket.site.bucket_regional_domain_name
    origin_id = "s3-site"
    origin_access_control_id = aws_cloudfront_origin_access_control.site.id
  }

  default_cache_behavior {
    target_origin_id = "s3-site"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods = ["GET", "HEAD"]
    cached_methods = ["GET", "HEAD"]
    compress = true
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"

    function_association {
      event_type = "viewer-request"
      function_arn = aws_cloudfront_function.rewrite_index.arn
    }
  }

  custom_error_response {
    error_code = 403
    response_code = 404
    response_page_path = "/404.html"
  }

  custom_error_response {
    error_code = 404
    response_code = 404
    response_page_path = "/404.html"
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate_validation.site.certificate_arn
    ssl_support_method = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

data "aws_iam_policy_document" "site_bucket" {
  statement {
    sid = "AllowCloudForntOAC"
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.site.arn}/*"]
  
  
    principals {
      type = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
     test = "StringEquals"
     variable = "AWS:SourceArn"
     values = [aws_cloudfront_distribution.site.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "site" {
  bucket = aws_s3_bucket.site.id
  policy = data.aws_iam_policy_document.site_bucket.json
}

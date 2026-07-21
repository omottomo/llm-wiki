# Phase 9 — AWS 배포: S3 + CloudFront + Terraform

<!-- LANGUAGE EXCEPTION: this plan is deliberately written in Korean at the user's
     explicit request (2026-07-20) — the human executes every step personally and reads
     this file as the working document. Do NOT "fix" it back to English. -->

## 배경

`site/dist`(phase-8 자체 제작 정적 사이트, Pagefind 검색 포함)를 AWS에 배포한다.
사이트는 지금까지 한 번도 배포된 적 없음 — `docs/rules/site-code.md` §2가 Cloudflare
Pages를 선언했지만 Pages 프로젝트는 생성된 적 없다. 이 phase가 그 목표를 대체한다.

**실행 방식 (이전 phase들과 다름):** 사용자(DevOps 엔지니어)가 모든 설정·구현을 직접
수행한다. 에이전트는 이 계획 작성과 실행 중 질의응답만 담당 — `.tf` 파일이나 워크플로를
직접 작성하지 않는다. 이 phase에는 `prd.json` 없음. 문서 갱신(아래 Phase 5)은 요청 시
에이전트가 수행 가능.

브레인스토밍(2026-07-20)에서 확정된 결정:
- AWS: S3(정적 파일) + CloudFront(CDN/HTTPS)
- 도메인: Route53에서 신규 구매
- HTTPS: ACM 인증서(us-east-1), Terraform으로 관리
- IaC: Terraform, state는 S3 원격 백엔드
- 업로드 파이프라인: GitHub Actions + OIDC, main push 시 자동 배포

레포 불변 제약 (변경 없음):
- `raw/`는 절대 공개 금지. 배포 전 `scripts/verify_site.py` exit 0 필수
- 레포는 private 유지
- `site/dist`는 git-ignore, 매 빌드 재생성

계획에 영향을 주는 사이트 특성:
- **pretty URL** (`<section>/<slug>/index.html`), 링크는 전부 루트 상대 경로 →
  도메인 루트에서 서빙해야 함
- 한글 이름 태그 디렉터리 다수 (S3 키에 한글 포함, URL은 percent-encoded)
- `404.html` 존재. Pagefind는 빌드 후 `npx -y pagefind@1 --site site/dist`로 생성

## 아키텍처 (권장안)

```
방문자 → Route53(A/AAAA alias) → CloudFront(ACM 인증서, HTTPS)
             → [CloudFront Function: /foo/ → /foo/index.html 재작성]
             → S3 private 버킷 (OAC로만 접근 허용)

배포: GitHub Actions(main push) → verify 게이트 통과 → OIDC AssumeRole
      → aws s3 sync site/dist → CloudFront invalidation
```

**핵심 선택 — S3 private 버킷 + OAC (website endpoint 방식 대신):**
- S3 website endpoint는 서브디렉터리 `index.html`을 자동 서빙하지만 HTTP 전용 +
  버킷 공개 필요.
- OAC는 버킷을 완전 비공개로 유지하지만, S3 REST endpoint는 `/foo/` 요청을
  `/foo/index.html`로 풀어주지 않음 → **viewer-request CloudFront Function으로
  URI 재작성이 필수**. 이 아키텍처 최대 함정.
- 재작성 규칙: URI가 `/`로 끝나면 `index.html` 붙임; 확장자 없으면 `/index.html`
  붙임. percent-encoded 한글 경로에도 그대로 동작 (인코딩된 URI에 붙이기만 함).

**403→404 함정:** OAC 구성에서 없는 키를 요청하면 S3가 403을 반환(`s3:ListBucket`
권한 없음). CloudFront custom error response에서 **403과 404 둘 다** `/404.html`
(응답 코드 404)로 매핑 — 진짜 404를 받으려고 `ListBucket`을 열어주는 것보다 단순해서 권장.

## Phase 0 — 사전 준비 (수동)

1. AWS 계정 확인. AWS CLI v2 + Terraform ≥ 1.10 설치 (1.10+이면 S3 백엔드 네이티브
   락 `use_lockfile` 사용 가능 — DynamoDB 테이블 불필요)
2. IAM: Terraform 실행용 자격 증명 준비 (admin 또는 최소권한 정책, `aws configure` 프로파일)
3. 도메인 이름 결정
4. 리전: 콘텐츠/state S3는 `ap-northeast-2`(서울). **ACM 인증서만 반드시
   `us-east-1`** (CloudFront 요구사항)

## Phase 1 — 부트스트랩 (state 백엔드 + 도메인)

Terraform 순환 문제(state 버킷은 자기가 저장할 state 안에 살 수 없음) 해결:

1. **state 버킷 생성** — 택1:
   - (단순) AWS CLI로 수동 생성: 버킷 + 버저닝 + 퍼블릭 차단 + SSE 암호화
   - (정석) 별도 `infra/bootstrap/` 루트 모듈을 로컬 state로 apply → 이후 건드리지 않음
2. **도메인 구매** — Route53 콘솔(또는 `aws route53domains register-domain`).
   *도메인 등록 자체는 Terraform 네이티브 리소스가 아님* — 구매는 수동. 구매 시 자동
   생성되는 **hosted zone은 Terraform에서 `data` 소스로 참조** (zone을 TF로 재생성하면
   NS 세트가 바뀌어 등록 정보와 어긋남 — `data` 참조가 안전한 패턴)
3. 비용: 등록 ~$3–15/년(TLD별), hosted zone $0.50/월

## Phase 2 — Terraform 핵심 인프라 (`infra/`)

레포 루트에 `infra/` 디렉터리, 단일 루트 모듈 (혼자 쓰는 프로젝트 — 모듈 분리 불필요).
파일 구성 예: `backend.tf`, `providers.tf`, `s3.tf`, `cloudfront.tf`, `acm.tf`,
`dns.tf`, `iam-deploy.tf`, `variables.tf`, `outputs.tf`

리소스 (의존 순서대로):

1. **backend/providers**: S3 백엔드(`use_lockfile = true`); aws 프로바이더 2개 —
   기본(`ap-northeast-2`) + alias `us_east_1`(ACM용)
2. **콘텐츠 S3 버킷**: private, `aws_s3_bucket_public_access_block` 전부 true,
   버저닝 on (실수 복구용)
3. **ACM 인증서** (provider = us_east_1): 도메인(+ 필요시 SAN), DNS 검증 →
   `aws_route53_record` 검증 레코드 → `aws_acm_certificate_validation` 대기
4. **CloudFront Function** (viewer-request): index.html 재작성 (아키텍처 절 참조)
5. **CloudFront 배포판**:
   - origin: S3 REST endpoint + OAC(`aws_cloudfront_origin_access_control`)
   - `default_root_object = "index.html"` (루트 전용 — 서브디렉터리는 Function이 처리)
   - aliases = 도메인; viewer certificate = ACM; `redirect-to-https`
   - custom error response: 403 → `/404.html`(404), 404 → `/404.html`(404)
   - cache policy: managed `CachingOptimized`; compress on
   - price class: `PriceClass_200` (아시아 포함; `All`은 남미/오세아니아 엣지까지 — 불필요)
6. **버킷 정책**: CloudFront service principal에 `s3:GetObject` 허용,
   `AWS:SourceArn` 조건을 배포판 ARN으로 고정
7. **Route53**: hosted zone은 `data` 참조; A + AAAA alias 레코드 → CloudFront.
   (www 서브도메인 리다이렉트는 생략 — 필요해지면 추가)
8. **GitHub OIDC**: `aws_iam_openid_connect_provider`(token.actions.githubusercontent.com)
   + 배포 role
   - trust policy: `repo:omottomo/llm-wiki:ref:refs/heads/main`으로 제한
   - 권한: 콘텐츠 버킷 `s3:PutObject/DeleteObject/ListBucket/GetObject` +
     `cloudfront:CreateInvalidation` (해당 배포판 ARN 한정)
9. **outputs**: 배포판 ID/도메인, 버킷명, role ARN (워크플로에서 사용)

`.gitignore` 추가: `.terraform/`, `*.tfstate*`, `*.tfvars`(민감값 쓸 경우);
`.terraform.lock.hcl`은 **커밋** (프로바이더 버전 고정).

실행: `terraform init` → `plan` → `apply`. ACM DNS 검증 수 분, CloudFront 배포판
생성 5–15분 소요.

## Phase 3 — 배포 파이프라인 (GitHub Actions)

`.github/workflows/deploy-site.yml` 신규 (기존 `verify-site.yml`은 그대로 분리 유지):

1. 트리거: push to main, paths = `wiki/**`, `site/**`, `scripts/**`
2. `permissions: id-token: write, contents: read` (OIDC 필수)
3. 잡 순서: **verify 게이트 통과 후에만 deploy** — build/verify 스텝을 deploy 잡에서
   반복하거나 `needs:` 체인
   - build: `pip install -r site/requirements.txt` → `python3 site/build.py` →
     `npx -y pagefind@1 --site site/dist`
   - gate: `python3 site/test_build_site.py` + `python3 scripts/verify_site.py`
     (exit 0 아니면 배포 중단 — raw/ 유출 게이트)
4. `aws-actions/configure-aws-credentials@v4` — OIDC role ARN + 리전
5. 업로드 — **Cache-Control 차등 적용이 핵심**:
   - `aws s3 sync site/dist s3://<bucket> --delete --exclude "*.html" --cache-control
     "public,max-age=31536000,immutable"` (Pagefind 에셋 — 인덱스 재생성 시 파일명이
     바뀌므로 immutable 안전)
   - HTML은 별도: `--include "*.html" --cache-control "public,max-age=0,must-revalidate"`
     (invalidation 의존도 낮춤)
   - 주의: `style.css`는 파일명 고정 + 내용 가변 → 빌드에 콘텐츠 해시 붙이기 전까지는
     HTML과 같은 짧은 캐시 그룹에 둘 것
6. `aws cloudfront create-invalidation --paths "/*"` (`/*`는 경로 1개로 계산;
   월 1,000 경로 무료 — 비용 문제 없음)
7. 버킷명/배포판 ID/role ARN은 GitHub repository variables로 주입
   (Terraform outputs에서 복사)

한글 S3 키: `aws s3 sync`가 업로드·요청 시 인코딩 자동 처리. content-type도 확장자
기반 자동 설정.

## Phase 4 — 배포 후 검증 체크리스트

1. `dig +short <도메인>` — CloudFront IP 반환
2. `curl -I https://<도메인>/` — 200, HTTPS, HTML content-type
3. **딥링크 직접 접근**: `curl -I https://<도메인>/concepts/<slug>/` — 200
   (Function 재작성 검증)
4. 한글 태그 페이지: `curl -I "https://<도메인>/tags/<percent-encoded>/"` — 200
5. 없는 경로 → 상태코드 404 + `404.html` 본문 (403이 보이면 error response 설정 오류)
6. 브라우저: Pagefind 검색 동작(한국어 쿼리), 다크모드, CSS 로드
7. **raw/ 경계 최종 확인**: `aws s3 ls s3://<bucket> --recursive | grep -i raw`
   — 결과 없어야 함
8. `curl -I http://<도메인>/` — HTTPS 리다이렉트(301/308)
9. (선택) AWS Budgets 알림 $5/월 — 과금 사고 조기 경보

## Phase 5 — 문서 갱신 (레포 규칙)

1. `docs/rules/site-code.md` §2 재작성: Cloudflare Pages → AWS
   (S3 + CloudFront + Terraform + OIDC). raw/ 경계·private 레포 제약은 유지;
   새로 배운 제약은 §2.4에 추가
2. 이 계획은 `docs/tasks/phase-9-aws-deploy/plan.md`에 보존 (완료)
3. `docs/index.md` 갱신; phase 마감 시 `docs/log.md`에 `site` 한 줄 추가
4. `.gitignore` 변경 커밋

## 원래 구상에서 빠져 있던 고려사항 (요약)

1. **pretty URL × OAC**: CloudFront Function 재작성 없으면 모든 서브페이지 403/404
   — 최대 함정
2. **403 → 404 매핑** 필요 (OAC 특성)
3. **ACM은 무조건 us-east-1** (다른 리전 인증서는 CloudFront에 못 붙임)
4. **도메인 구매는 Terraform 밖** — hosted zone은 `data`로 참조
5. **state 백엔드 부트스트랩 순환** — 수동 생성 또는 별도 모듈로 해결
6. **Cache-Control 전략** — 없으면 배포마다 stale 콘텐츠 아니면 invalidation 남용
7. **배포 게이트**: `verify_site.py` 통과 없이 업로드 금지 (raw/ 유출 방지선)
8. **OIDC로 장기 키 제거** — Actions secrets에 access key 저장 안 함
9. 한글 S3 키/percent-encoding — 동작하지만 배포 후 체크리스트에 포함
10. 비용: 도메인 연 $3–15 + zone $0.50/월; 그 외 저트래픽이면 월 $1 미만

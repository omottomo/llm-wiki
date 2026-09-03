# Phase 16 — 배포 자격증명 IAM 사용자 이전 가이드 (`llm-wiki` → `devops`)

<!-- LANGUAGE EXCEPTION: 사용자가 직접 실행하는 작업 문서 — 한국어 유지. 영어로 되돌리지 말 것. -->

> 이 문서는 **터미널에 그대로 입력하는 실행 순서**다. 위에서 아래로 진행하고,
> 각 Task 끝의 **검증**이 통과해야 다음 Task로 넘어간다.
> 설계 배경은 아래 "0. 왜 이 작업이 이렇게 작은가"에 요약했다 (별도 plan.md 없음 — 범위가 작아서).

**목표:** 로컬에서 Terraform·AWS CLI를 실행하는 주체를 IAM 사용자 `llm-wiki` → `devops` 로 바꾸고, `llm-wiki` 사용자를 **완전히 삭제**한다.

**소요 시간:** 30~40분 (Task 3의 관찰 기간 제외)

**전제:** AWS 계정은 그대로. 리소스(S3·CloudFront·Route53·ACM)는 하나도 이동하지 않는다.

---

## 실행 기록 (2026-09-03 — 완료)

전 Task 완료. 검증 결과:

| 확인 | 결과 |
|---|---|
| `aws sts get-caller-identity` | `user/devops` |
| `aws iam get-user --user-name llm-wiki` | `NoSuchEntity` — 삭제 완료 |
| `AdministratorAccessGroup` | 유지됨 (devops 소속 확인) |
| `llm-wiki-deploy` role | 유지됨 — CI OIDC 경로 무사 |
| `terraform plan` (devops) | `2 to add, 0 to change, 0 to destroy` |
| 사이트 | `https://omotomo-llm-wiki.com/` → 200 |

**남은 리스크 2건:**

1. **Task 0.4의 정체불명 키를 특정하지 못한 채 삭제했다.** `llm-wiki`의 두 번째 액세스 키는 이 PC에 없는데도 로컬 키보다 최근에 쓰였고, 용처를 밝히기 전에 사용자와 함께 삭제됐다. 그 키를 쓰던 무언가(다른 기기·스크립트)가 있었다면 지금 조용히 인증 실패 중이다. 이후 원인 불명의 AWS 인증 오류가 나오면 여기를 먼저 의심할 것.
2. **`terraform plan`의 `2 to add`는 이번 작업과 무관한 선재 diff다.** phase-13에서 PR용 읽기전용 역할(`llm-wiki-plan` + `plan-infra` 정책)을 코드에만 추가하고 `apply`하지 않았다. `verify.yml`에도 terraform 스텝이 없고 GitHub Secrets에 해당 role ARN도 없어, phase-13의 "PR에서 terraform plan" 절반이 미완인 상태로 남아 있다. 마무리하려면 `apply` + 워크플로 배선 + secret 등록이 함께 필요하므로 별도 작업으로 잡을 것.

---

## 치환 값

공개 저장소이므로 실제 값은 이 문서에 적지 않는다. 아래 표를 **로컬 메모장**에 복사해 채워두고 명령에 대입한다.

| 표기 | 의미 | 얻는 방법 |
|---|---|---|
| `<ACCOUNT_ID>` | AWS 계정 ID (12자리) | `aws sts get-caller-identity --query Account --output text` |
| `<OLD_KEY_LOCAL>` | 지금 `~/.aws/credentials`의 `[llm-wiki]`에 들어있는 액세스 키 ID | Task 0.2 |
| `<OLD_KEY_OTHER>` | `llm-wiki`의 **나머지** 액세스 키 ID (로컬에 없는 것) | Task 0.2 |
| `<NEW_KEY_ID>` | Task 1에서 새로 발급하는 devops 액세스 키 ID | Task 1.1 출력 |

> ⚠️ **액세스 키 ID·시크릿·계정 ID를 저장소 안 파일에 적지 말 것.** phase-15에서 계정 ID를 git 이력 전체에서 지워낸 이력이 있다. 다시 넣으면 그 작업이 무효가 된다.

---

## 0. 왜 이 작업이 이렇게 작은가 (읽고 시작)

"배포를 다른 IAM 계정으로 옮긴다"는 말은 보통 큰 작업이지만, 이 저장소에서는 **자격증명 교체**가 전부다. 이유:

| 구성요소 | `llm-wiki` IAM 사용자에 묶여 있나? | 근거 |
|---|---|---|
| GitHub Actions 배포 | **아니오** | `.github/workflows/deploy.yml`은 OIDC로 `llm-wiki-deploy` **역할(role)** 을 assume한다. IAM 사용자·액세스 키를 전혀 쓰지 않는다. GitHub Secrets에도 AWS 키가 없다 (`AWS_DEPLOY_ROLE_ARN`, `SITE_BUCKET`, `CF_DISTRIBUTION_ID` 뿐) |
| 사이트 S3 버킷 정책 | **아니오** | Principal이 `cloudfront.amazonaws.com` 서비스 하나뿐 (`infra/cloudfront.tf`) |
| tfstate 버킷 | **아니오** | 버킷 정책 자체가 없다. 계정 IAM 권한으로만 통제 |
| Terraform state | **아니오** | state 파일은 리소스 상태만 담고 "누가 apply 했는가"는 기록하지 않는다. 그래서 프로파일만 바꿔도 `plan` 결과가 동일해야 한다 — 이게 Task 2의 검증 논리다 |
| `devops` 사용자 권한 | **동일** | 두 사용자 모두 `AdministratorAccessGroup` 소속. 권한 차이 없음 → 정책 작업 불필요 |

**이름 혼동 주의:** `llm-wiki-site-<ACCOUNT_ID>` 버킷, `llm-wiki-deploy` / `llm-wiki-plan` 역할의 "llm-wiki"는 **프로젝트 이름**이지 IAM 사용자 이름이 아니다. 건드리지 않는다.

---

## Task 0 — 사전 확인

- [x] **0.1 현재 자격증명 확인**

```bash
export AWS_PROFILE=llm-wiki
aws sts get-caller-identity
```

기대 출력: `"Arn": "arn:aws:iam::<ACCOUNT_ID>:user/llm-wiki"`. 계정 ID를 표에 기록.

- [x] **0.2 `llm-wiki` 사용자에 딸린 것 전수 조사**

IAM 사용자는 딸린 게 하나라도 남아 있으면 삭제가 거부된다(`DeleteConflict`). 무엇이 붙어 있는지 먼저 센다.

```bash
aws iam list-access-keys      --user-name llm-wiki --query 'AccessKeyMetadata[].[AccessKeyId,Status]' --output text
aws iam get-login-profile     --user-name llm-wiki                      # 콘솔 비밀번호 유무
aws iam list-groups-for-user  --user-name llm-wiki --query 'Groups[].GroupName'
aws iam list-attached-user-policies --user-name llm-wiki --query 'AttachedPolicies[].PolicyArn'
aws iam list-user-policies    --user-name llm-wiki                      # 인라인 정책
aws iam list-mfa-devices      --user-name llm-wiki --query 'MFADevices[].SerialNumber'
aws iam list-ssh-public-keys  --user-name llm-wiki --query 'SSHPublicKeys[].SSHPublicKeyId'
aws iam list-signing-certificates --user-name llm-wiki --query 'Certificates[].CertificateId'
aws iam list-service-specific-credentials --user-name llm-wiki --query 'ServiceSpecificCredentials[].ServiceSpecificCredentialId'
```

2026-09-03 기준 실제 상태 (달라졌으면 Task 5 목록을 그에 맞게 조정):

| 항목 | 개수 |
|---|---|
| 액세스 키 | **2개** (둘 다 Active) |
| 로그인 프로파일(콘솔 비밀번호) | 있음 |
| 그룹 | `AdministratorAccessGroup` 1개 |
| 연결된 관리형 정책 | `IAMUserChangePassword` 1개 |
| 인라인 정책 / MFA / SSH 키 / 인증서 / 서비스 자격증명 | 전부 0 |

- [x] **0.3 로컬에 있는 키가 둘 중 어느 것인지 확인**

```bash
aws configure get aws_access_key_id --profile llm-wiki
```

출력값 = `<OLD_KEY_LOCAL>`. 0.2의 목록에서 **나머지 하나** = `<OLD_KEY_OTHER>`.

- [x] **0.4 ⚠️ 정체불명 키 추적 (이 단계를 건너뛰지 말 것)**

`<OLD_KEY_OTHER>`는 이 PC에 없는데도 최근까지 사용됐다. 다른 기기·스크립트·서비스가 쓰고 있을 수 있고, 사용자를 지우면 **그쪽이 조용히 깨진다.**

```bash
# 두 키가 각각 마지막으로 언제/어디서 쓰였는지
aws iam get-access-key-last-used --access-key-id <OLD_KEY_LOCAL> --query AccessKeyLastUsed
aws iam get-access-key-last-used --access-key-id <OLD_KEY_OTHER> --query AccessKeyLastUsed

# 누가 그 키를 썼는지 이벤트로 추적 (CloudTrail은 90일치 보관)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=<OLD_KEY_OTHER> \
  --max-results 25 \
  --query 'Events[].[EventTime,EventName,EventSource]' --output table
```

**검증:** `<OLD_KEY_OTHER>`가 무엇에 쓰이는지 설명할 수 있어야 한다. 설명이 안 되면 — 아무것도 삭제하지 말고 Task 3의 비활성화 상태에서 최소 1주일 관찰한 뒤 진행한다.

---

## Task 1 — `devops` 액세스 키 발급 및 프로파일 설정

- [x] **1.1 액세스 키 생성**

```bash
aws iam create-access-key --user-name devops
```

> 🔐 **시크릿 액세스 키는 이 출력에서 딱 한 번만 보인다.** 다시 조회할 방법이 없다. 창을 닫기 전에 비밀번호 관리자에 저장할 것. 저장소 안 파일·커밋 메시지·채팅에 붙여넣지 말 것.

`AccessKeyId` = `<NEW_KEY_ID>`.

- [x] **1.2 프로파일 등록**

```bash
aws configure --profile devops
# AWS Access Key ID     : <NEW_KEY_ID>
# AWS Secret Access Key : (1.1 출력의 SecretAccessKey)
# Default region name   : ap-northeast-2
# Default output format : json
```

리전이 `ap-northeast-2`인 이유: `infra/providers.tf`의 기본 프로바이더와 `versions.tf`의 backend 리전이 서울이다. (ACM 인증서만 `us_east_1` 별칭 프로바이더로 버지니아에 만든다 — CloudFront 요구사항.)

- [x] **1.3 검증**

```bash
AWS_PROFILE=devops aws sts get-caller-identity
```

기대 출력: `"Arn": "arn:aws:iam::<ACCOUNT_ID>:user/devops"`. 계정 ID가 Task 0.1과 **같아야** 한다.

> 새 키가 즉시 안 먹히고 `InvalidClientTokenId`가 날 수 있다. IAM은 전역 서비스라 전파에 몇 초~1분 걸린다. 잠시 뒤 재시도.

---

## Task 2 — Terraform이 새 프로파일로 동일하게 동작하는지 검증

이 Task가 이번 작업의 **핵심 검증**이다. state가 실행 주체를 기록하지 않으므로, 프로파일만 바꿨을 때 `plan`은 **변경 없음**이어야 한다. 변경이 뜨면 뭔가 잘못된 것이다.

- [x] **2.1 백엔드 재초기화**

```bash
cd infra
export AWS_PROFILE=devops
terraform init -reconfigure -backend-config=backend.hcl
```

`-backend-config=backend.hcl`이 필요한 이유: `versions.tf`의 backend 블록은 버킷 이름을 선언하지 않는다. 버킷명에 계정 ID가 들어가는데 저장소가 공개라서 부분 구성(partial config)으로 빼놨고, `backend.hcl`은 gitignore 대상이다.

`-reconfigure`는 새 자격증명으로 backend 인증을 다시 하도록 강제한다.

**기대 출력:** `Terraform has been successfully initialized!`

- [x] **2.2 plan 실행**

```bash
terraform plan
```

**기대 출력:** `No changes. Your infrastructure matches the configuration.`

- [x] **2.3 검증 및 분기**

판단 기준은 **`to change` / `to destroy` 가 0인가**다. 이 둘이 0이 아니면 state를 잘못 읽고 있다는 뜻이고, 0이면 프로파일 교체는 성공한 것이다.

| 결과 | 의미 | 조치 |
|---|---|---|
| `No changes.` | ✅ 통과 | Task 3으로 |
| `N to add, 0 to change, 0 to destroy` | ✅ 통과 — 코드에는 있는데 아직 `apply` 안 한 리소스가 있을 뿐. 기존 리소스는 전부 state와 일치한다 | Task 3으로. 그 리소스를 실제로 만들지는 **별개 결정** |
| `0 to change` 가 아님 (기존 리소스가 변경/삭제 대상) | ❌ **중단** | state를 잘못 읽고 있다는 뜻(대개 backend 버킷 오지정). `apply` 절대 금지. `backend.hcl` 내용부터 확인 |
| `AccessDenied` / `403` | devops 권한 문제 | `aws iam list-groups-for-user --user-name devops` 로 `AdministratorAccessGroup` 소속 확인 |

> `terraform apply`는 이 Task에서 **실행하지 않는다.** 인프라를 바꾸는 게 목적이 아니라 읽기가 되는지 확인하는 것뿐이다.

---

## Task 3 — 기존 키 비활성화 (되돌릴 수 있는 단계)

삭제 전에 반드시 거치는 안전판이다. 비활성화는 되돌릴 수 있고, 삭제는 되돌릴 수 없다.

- [x] **3.1 두 키 모두 비활성화**

```bash
export AWS_PROFILE=devops        # 이제부터 모든 명령은 devops로

aws iam update-access-key --user-name llm-wiki --access-key-id <OLD_KEY_LOCAL> --status Inactive
aws iam update-access-key --user-name llm-wiki --access-key-id <OLD_KEY_OTHER> --status Inactive
```

- [x] **3.2 검증 — 옛 프로파일이 실제로 막혔는지**

```bash
AWS_PROFILE=llm-wiki aws sts get-caller-identity
```

**기대:** 실패. `InvalidClientTokenId` 또는 `AccessDenied`. 여기서 성공하면 비활성화가 적용 안 된 것이니 3.1을 다시.

- [x] **3.3 관찰 기간**

Task 0.4에서 `<OLD_KEY_OTHER>`의 용처를 특정하지 못했다면, **최소 1주일** 이 상태로 두고 무엇이 깨지는지 본다. 깨진 게 나오면 그것이 그 키의 사용처다.

되돌리려면:

```bash
aws iam update-access-key --user-name llm-wiki --access-key-id <OLD_KEY_OTHER> --status Active
```

**진행 조건:** 관찰 기간 동안 아무것도 깨지지 않았다 → Task 4.

---

## Task 4 — 문서 갱신 및 커밋

- [x] **4.1 phase-9 런북의 프로파일 이름 교체**

`docs/tasks/phase-9-aws-deploy/implementation.md`에 프로파일 이름이 두 군데 박혀 있다 (0.3절, 0.4절). 그대로 두면 다음에 재현할 때 존재하지 않는 사용자를 만들게 된다.

```bash
cd /home/tomo/projects/llm-wiki
grep -n "llm-wiki" docs/tasks/phase-9-aws-deploy/implementation.md | grep -i "profile\|configure"
sed -i 's/--profile llm-wiki/--profile devops/; s/export AWS_PROFILE=llm-wiki/export AWS_PROFILE=devops/' \
  docs/tasks/phase-9-aws-deploy/implementation.md
git diff docs/tasks/phase-9-aws-deploy/implementation.md
```

**검증:** diff가 정확히 2줄이고, 버킷명·역할명의 `llm-wiki`(프로젝트 이름)는 **바뀌지 않았어야** 한다.

- [x] **4.2 커밋**

커밋 규약은 `/my-skills:git-workflow` 를 따른다 (`CLAUDE.md` §3). main에 직접 커밋하지 말고 브랜치를 판다.

```bash
git switch -c chore/iam-user-devops
git add docs/tasks/phase-9-aws-deploy/implementation.md docs/tasks/phase-16-iam-user-migration/ docs/index.md
git commit -m "chore: switch local AWS profile from llm-wiki to devops"
```

---

## Task 5 — `llm-wiki` 사용자 완전 삭제 (되돌릴 수 없음)

> ## ⚠️ 경고 — 여기서부터는 되돌릴 수 없습니다
>
> 아래 단계는 IAM 사용자 `llm-wiki`와 그 자격증명을 **영구히 삭제**합니다. 삭제된 IAM
> 사용자는 복구할 수 없고, 같은 이름으로 다시 만들어도 내부 식별자(UserId)가 달라져
> 그 사용자를 참조하던 설정은 여전히 깨진 상태로 남습니다.
>
> 진행하기 전에 아래 세 가지를 **모두** 확인하세요:
>
> 1. Task 2.2가 `No changes.` 로 통과했다 — devops 자격증명으로 Terraform이 정상 동작한다.
> 2. Task 3.3의 관찰 기간 동안 아무것도 깨지지 않았다 — 두 키 모두 이제 쓰이지 않는다.
> 3. `devops` 사용자로 **AWS 콘솔에 로그인해 봤다** — `llm-wiki`를 지우면 그 계정의 콘솔
>    비밀번호도 함께 사라집니다. devops 콘솔 로그인이 안 되는 상태에서 지우면 브라우저로
>    들어갈 방법이 없어집니다.
>
> 세 가지 중 하나라도 확인되지 않았다면 Task 3의 비활성화 상태로 그대로 두세요. 비활성화만으로도
> 보안 목적은 이미 달성됩니다.

삭제 순서에 의미가 있다. AWS는 딸린 리소스가 하나라도 남아 있으면 `DeleteConflict: Cannot delete entity, must delete/detach ... first` 로 거부한다. **딸린 것을 전부 떼어낸 뒤 마지막에 사용자를 지운다.**

- [x] **5.1 액세스 키 2개 삭제**

```bash
export AWS_PROFILE=devops
aws iam delete-access-key --user-name llm-wiki --access-key-id <OLD_KEY_LOCAL>
aws iam delete-access-key --user-name llm-wiki --access-key-id <OLD_KEY_OTHER>
aws iam list-access-keys --user-name llm-wiki --query 'AccessKeyMetadata[].AccessKeyId'
```

**기대:** 빈 배열 `[]`.

- [x] **5.2 로그인 프로파일(콘솔 비밀번호) 삭제**

```bash
aws iam delete-login-profile --user-name llm-wiki
```

- [x] **5.3 관리형 정책 연결 해제**

```bash
aws iam detach-user-policy --user-name llm-wiki \
  --policy-arn arn:aws:iam::aws:policy/IAMUserChangePassword
aws iam list-attached-user-policies --user-name llm-wiki --query 'AttachedPolicies[].PolicyArn'
```

**기대:** `[]`. (Task 0.2에서 다른 정책이 더 보였다면 각각 `detach-user-policy` 반복.)

- [x] **5.4 그룹에서 제거**

```bash
aws iam remove-user-from-group --user-name llm-wiki --group-name AdministratorAccessGroup
aws iam list-groups-for-user --user-name llm-wiki --query 'Groups[].GroupName'
```

**기대:** `[]`.

> 그룹 자체는 **지우지 않는다.** `devops`가 이 그룹으로 관리자 권한을 받고 있다. 그룹을 지우면 devops의 권한이 사라진다.

- [x] **5.5 사용자 삭제**

```bash
aws iam delete-user --user-name llm-wiki
```

`DeleteConflict`가 나면 아직 뭔가 붙어 있는 것이다. Task 0.2의 조회 명령을 다시 돌려 남은 항목을 찾아 떼어낸 뒤 재시도.

- [x] **5.6 검증**

```bash
aws iam get-user --user-name llm-wiki 2>&1 | tail -2
aws iam list-users --query 'Users[].UserName'
```

**기대:** 첫 명령은 `NoSuchEntity` 오류, 둘째 출력 목록에 `llm-wiki`가 없다.

- [x] **5.7 로컬 프로파일 정리**

```bash
# 편집기로 열어 [profile llm-wiki] / [llm-wiki] 블록을 지운다
${EDITOR:-nano} ~/.aws/config
${EDITOR:-nano} ~/.aws/credentials

grep -E '^\[' ~/.aws/config ~/.aws/credentials
```

**기대:** `llm-wiki` 항목이 더 이상 없다.

---

## Task 6 — 전체 회귀 검증 및 마무리

- [x] **6.1 Terraform 재확인**

```bash
cd /home/tomo/projects/llm-wiki/infra
export AWS_PROFILE=devops
terraform plan
```

**기대:** `No changes.`

- [x] **6.2 GitHub Actions 배포 확인 (OIDC 경로가 무사한지)**

Task 4의 브랜치로 PR을 열고 머지한다. PR에서는 `verify.yml`(lint·빌드·`terraform plan`)이, main 머지 후에는 `deploy.yml`이 돈다.

```bash
gh pr create --fill
# 머지 후
gh run watch
```

**기대:** 두 워크플로 모두 초록. 배포는 IAM 사용자가 아니라 OIDC 역할을 쓰므로 **원래 영향이 없어야** 하고, 이 실행은 그 사실을 실제로 확인하는 절차다.

> 이 문서의 `deploy.yml` 경로 필터에 `docs/**`가 없다. 문서만 바꾼 커밋은 배포를 트리거하지 않으므로, 배포까지 확인하려면 `wiki/` 또는 `site/` 변경이 함께 있어야 한다. 없다면 GitHub Actions 화면에서 `Deploy site (main)` 를 수동 실행하거나, 다음 콘텐츠 커밋 때 확인한다.

- [x] **6.3 작업 로그 한 줄 추가**

`docs/log.md` 맨 아래에 (`CLAUDE.md` §2 — 코드 모드 phase는 마감 시 **한 줄**):

```markdown
## [2026-09-03] site   | phase-16-iam-user-migration — 로컬 배포 자격증명 llm-wiki → devops 이전, llm-wiki IAM 사용자 삭제
```

날짜는 실제 마감일로.

- [x] **6.4 남은 정리 여부 판단**

`llm-wiki-deploy` / `llm-wiki-plan` 역할과 `llm-wiki-site-*` 버킷 이름은 **그대로 둔다.** 프로젝트 이름이지 사용자 이름이 아니며, 바꾸려면 리소스 재생성 + GitHub Secrets 갱신이 따라와 이번 작업 범위를 벗어난다.

---

## 문제 해결

| 증상 | 원인 | 조치 |
|---|---|---|
| `InvalidClientTokenId` (새 키) | IAM 전파 지연 | 1분 대기 후 재시도 |
| `SignatureDoesNotMatch` | 시크릿 키 붙여넣기 오류(앞뒤 공백·줄바꿈) | `aws configure --profile devops` 재실행 |
| `terraform plan`에 diff 발생 | backend 버킷 오지정 → 다른 state를 읽는 중 | **apply 금지.** `backend.hcl`의 bucket과 `terraform.tfvars`의 `tfstate_bucket_name`이 같은 값인지 확인 |
| `Error: Backend configuration changed` | 프로파일 교체 후 재초기화 안 함 | `terraform init -reconfigure -backend-config=backend.hcl` |
| `DeleteConflict` (Task 5.5) | 아직 딸린 항목 있음 | Task 0.2 조회 명령 전부 재실행해 남은 것 제거 |
| `NoSuchEntity` (Task 5.2 `delete-login-profile`) | 콘솔 비밀번호가 원래 없음 | 정상. 다음 단계로 |
| devops 콘솔 로그인 불가 (삭제 후) | 비밀번호 미설정/분실 | 루트 사용자로 로그인해 devops 비밀번호 재설정 |

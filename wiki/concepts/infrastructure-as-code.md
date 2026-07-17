---
title: 코드형 인프라 (IaC)
type: concept
created: 2026-07-18
updated: 2026-07-18
sources: [ibm-infrastructure-as-code]
tags: [코드형인프라, 데브옵스, 자동화, 환경설계]
---

# 코드형 인프라 (IaC)

수동 프로세스 대신 **구성 파일**로 IT 인프라의 프로비저닝과 관리를 자동화하는 DevOps 관행이다. 인프라를 소프트웨어처럼 취급해 애플리케이션 코드와 동일한 방식으로 버전 관리·테스트·배포하며, 문서화되지 않은 수동 구성이 낳는 인적 오류와 구성 드리프트를 제거한다 (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]).

## 워크플로 4단계

1. **쓰기** — HCL·YAML·JSON 등으로 필요한 리소스와 구성 방법을 정의
2. **버전** — Git 등 버전 제어 시스템에 저장해 추적·리뷰·롤백 확보
3. **프로비저닝** — 자동화 엔진이 코드를 실제 리소스(VM·네트워크·DB)로 변환. 멱등성이라 여러 번 실행해도 결과가 같다
4. **배포** — 개발·테스트·스테이징·프로덕션 전 환경에 동일한 구성을 보장

(→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]])

## 두 가지 핵심 설계 선택

- **선언형 vs 명령형**: 선언형은 원하는 상태(예: "이 사양의 서버 3대")만 명시하면 도구가 구현을 처리하고, 명령형은 단계별 명령을 정확한 순서로 직접 작성한다. 선언형이 일반적이며 명령형은 더 높은 전문성을 요구한다 (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]).
- **가변형 vs 불변형**: 대부분의 조직은 배포 후 변경 불가한 불변형을 선택한다 — 구성 드리프트가 원천 차단되고, 변경마다 버전 지정 인스턴스가 생겨 롤백이 확실하며, 클라우드에선 재프로비저닝이 수분이면 끝난다 (→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]).

## 이점

- 프로비저닝 시간을 수주에서 수분으로 단축
- 환경 간 일관성 — 테스트에서 통과한 구성이 프로덕션에서도 동일하게 동작
- 전문가 개인에게 묶여 있던 인프라 지식을 코드로 보존해 퇴사로 인한 지식 손실 방지
- 사용량 기반 과금 최적화 — 필요할 때만 프로비저닝하고 유휴 시 자동 해제

(→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]])

## 도구 생태계 (2026-07 기준)

- **프로비저닝 도구**: [[entities/terraform|Terraform]](멀티 클라우드, HCL)과 그 오픈소스 포크 OpenTofu, 범용 언어를 쓰는 Pulumi, 플랫폼 특화인 AWS CloudFormation·Azure Resource Manager·Google Cloud Deployment Manager
- **구성 관리 도구**: Ansible(에이전트리스, YAML 플레이북)·Puppet(대규모 지속 점검·자동 교정)·Chef(쿡북/레시피, 테스트 프레임워크 강점)

(→ [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]])

## 하네스 엔지니어링과의 관계 (위키 차원의 관찰)

이 위키의 중심 개념인 [[concepts/harness-engineering|하네스 엔지니어링]]과 IaC는 같은 사상 계보에 있다 — **환경을 코드로 선언·버전 관리하고, 사람의 수동 개입 대신 자동화된 강제로 일관성을 지킨다**는 점에서다. 선언형 IaC의 "원하는 상태만 선언하면 구현은 도구가 처리"하는 구조는 에이전트에게 목표를 선언하고 실행을 맡기는 방식과 닮았고, 배포 전 자동 테스트로 구성을 검증하는 관행은 [[concepts/verification-automation|검증 자동화]]의 인프라 영역 선례다. '하네스' 개념을 대중화한 [[entities/mitchell-hashimoto|미첼 하시모토]]가 바로 대표 IaC 도구 Terraform을 만든 [[entities/hashicorp|HashiCorp]]의 공동창립자라는 사실이 이 계보를 상징적으로 잇는다 (하시모토 관련 → [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]·[[sources/youtube-DrekqeDlO1w|#14 하네스 문서 100번]], IaC 관련 → [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]]). 단, 이 유비 자체는 소스가 아니라 위키의 해석이다.

## 관련 문서

- [[concepts/harness-engineering|하네스 엔지니어링]] — 환경 설계로 행동을 강제한다는 사상의 AI 에이전트판
- [[concepts/verification-automation|검증 자동화]] — 배포 전 자동 검증이라는 공통 원리
- [[entities/terraform|Terraform]] · [[entities/hashicorp|HashiCorp]] — 대표 도구와 제작사

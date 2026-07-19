---
title: "코드형 인프라(IaC)란 무엇인가? (IBM Think)"
label: "#26 IBM IaC 해설"
type: source
credibility: high
volatility: warm
created: 2026-07-18
updated: 2026-07-18
sources: [ibm-infrastructure-as-code]
tags: [코드형인프라, 데브옵스, 자동화]
---

## 한 줄 요약

IBM Think의 개념 해설 문서로, [[concepts/infrastructure-as-code|코드형 인프라]](IaC)를 "수동 프로세스 대신 구성 파일로 IT 인프라의 프로비저닝·관리를 자동화하는 DevOps 관행"으로 정의하고 워크플로·접근 방식·도구 생태계를 개괄한다.

## 핵심 내용

- IaC는 인프라를 소프트웨어처럼 취급한다 — 애플리케이션 코드와 같은 방식으로 버전 관리·테스트·배포하며, 문서화되지 않은 수동 구성(개별 서버 설정, 콘솔 조작)을 우회한다.
- 워크플로는 4단계: **쓰기**(HCL·YAML·JSON으로 정의) → **버전**(Git 등 버전 제어) → **프로비저닝**(자동화 엔진이 코드를 실제 리소스로 변환, 멱등성 보장) → **배포**(환경 전반에 일관 구성).
- 두 가지 핵심 설계 선택: **선언형 vs 명령형**(원하는 상태만 선언 vs 단계별 명령 작성 — 선언형이 일반적), **가변형 vs 불변형**(대부분의 조직이 불변형을 선택 — 구성 드리프트 제거, 버전 롤백 확보).
- 이점: 프로비저닝 시간 수주→수분 단축, 환경 간 일관성(인적 오류·드리프트 제거), 전문가 퇴사로 인한 지식 손실 방지(지식을 코드로 보존), 사용량 기반 비용 최적화.
- CI/CD 통합: 인프라 코드를 앱 코드와 같은 리포지토리에 두고 풀 리퀘스트로 리뷰, 배포 전 자동화된 테스트로 구성을 검증한다.
- 도구는 두 범주 (2026-07 기준): **프로비저닝**(Terraform·OpenTofu·Pulumi는 멀티 클라우드, AWS CloudFormation·Azure Resource Manager·Google Cloud Deployment Manager는 플랫폼 특화)과 **구성 관리**(Ansible·Puppet·Chef).

## 주요 주장 / 데이터

- IBM 기업가치연구소(IBV) 조사: 경영진의 65%가 "IaC 같은 자동화 기술이 IT 팀 생산성을 향상시키고 있다"고 응답 (2026-07 기준, 조사 시점은 문서에 미표기).
- [[entities/terraform|Terraform]]은 "IBM 계열사인 HashiCorp"의 도구로 소개된다 — 리소스 간 종속성을 분석해 독립 리소스를 병렬 프로비저닝(예: AWS 서버 10대 + Azure DB 5개 동시 생성).
- 블랙 프라이데이 사례: 소매업체가 몇 시간 안에 100~1,000대 서버를 사전 정의 템플릿으로 자동 확장.
- 불변형 인프라가 우세한 이유 세 가지: 구성 드리프트 제거, 버전 지정 인스턴스로 신뢰할 수 있는 롤백, 클라우드에선 재프로비저닝이 수분이면 끝나 실용적.

## 기존 위키와의 연결

- 강화: [[entities/mitchell-hashimoto|미첼 하시모토]]가 공동창립한 [[entities/hashicorp|HashiCorp]]의 대표 제품이 IaC 도구 Terraform이라는 사실 — '하네스' 개념을 대중화한 인물이 "환경을 코드로 선언하고 자동으로 강제한다"는 사상을 이미 인프라 영역에서 구현했던 배경을 보여준다.
- 강화: [[concepts/verification-automation|검증 자동화]] — 배포 전 자동 테스트·CI/CD 게이트로 구성을 검증하는 IaC 관행은 "생성과 검증의 분리"가 AI 이전 인프라 영역에서 먼저 확립된 선례다.
- 신규: [[concepts/infrastructure-as-code|코드형 인프라]] 개념 페이지, [[entities/terraform|Terraform]]·[[entities/hashicorp|HashiCorp]] 엔티티 페이지가 이 소스로 생성됐다.
- (관찰) [[concepts/harness-engineering|하네스 엔지니어링]]과의 사상적 유사성: 선언형 IaC의 "원하는 상태를 선언하면 도구가 구현"하는 구조, 수동 개입을 코드화된 강제로 대체하는 철학은 하네스 엔지니어링의 "환경 설계 = 강제"와 같은 계보다. 이 유비는 소스가 직접 말하는 것이 아니라 위키 차원의 연결이다.

## 출처 정보

- raw: raw/ibm-infrastructure-as-code.md
- URL: https://www.ibm.com/kr-ko/think/topics/infrastructure-as-code
- 저자: Jim Holdsworth, Annie Badman (Staff Writer, IBM Think)
- 게시일: 미표기 (2026-07-18 수집)

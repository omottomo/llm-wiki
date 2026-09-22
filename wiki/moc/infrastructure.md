---
title: 주제 관문 — 인프라와 웹 기술
type: overview
created: 2026-09-22
updated: 2026-09-22
sources: []
tags: [관문, 코드형인프라, 쿠버네티스, 인프라]
---

# 주제 관문 — 인프라와 웹 기술

> 인프라를 코드로 선언하고, 컨테이너로 굴리고, 그 앞단의 이름·API를 다루는 기술들을 모아 둔 관문이다. AI 코딩과 같은 사상(환경을 코드로 강제한다)이 인프라 쪽에서 먼저 자리 잡은 선례이기도 하다.

## 여기서부터
1. [[concepts/infrastructure-as-code|코드형 인프라]] — 왜 인프라를 코드로 쓰게 됐는지
2. [[concepts/kubernetes|쿠버네티스]] — 컨테이너를 여러 대에 나눠 굴리는 표준
3. [[entities/terraform|Terraform]] — 실제 도구 하나를 끝까지

## 개념
- [[concepts/infrastructure-as-code|코드형 인프라]] — IaC. 환경을 코드로 선언·강제하는 사상의 인프라 영역 선례
- [[concepts/hcl|HCL]] — Terraform 구성 언어 문법. 블록·인수·표현식, provider alias, 메타 인수
- [[concepts/kubernetes|쿠버네티스]] — 컨테이너 오케스트레이션. 컨트롤 플레인·노드·애드온 구성, CRI·CNI·CSI 인터페이스, 주요 리소스
- [[concepts/dns-records|DNS 레코드]] — 웹/네트워크 인프라 기초. A·CNAME·MX·SPF 등 레코드 종류와 조회 도구
- [[concepts/graphql|GraphQL]] — 엔드포인트 하나로 필요한 필드만 받는 쿼리 언어. 스키마·리졸버·인트로스펙션, REST와의 대비

## 엔티티
- [[entities/terraform|Terraform]] — HashiCorp의 멀티 클라우드 IaC 도구. Write-Plan-Apply 워크플로·state·HCL 상세
- [[entities/hashicorp|HashiCorp]] — 하시모토 공동창립, Terraform 제작사(IBM 계열)
- [[entities/armon-dadgar|아몬 다드가]] — HashiCorp 공동창립자, Terraform 소개의 얼굴
- [[entities/mitchell-hashimoto|미첼 하시모토]] — HashiCorp 공동창립자, 하네스 용어 제시자(추정)
- [[entities/sentinel|Sentinel]] — HashiCorp의 정책 코드화(policy-as-code) 프레임워크
- [[entities/opa|OPA]] — Open Policy Agent, Sentinel의 벤더 중립적 오픈 대안
- [[entities/k3s|K3s]] — 100MB 단일 바이너리 경량 쿠버네티스 배포판. 서버/에이전트, 데이터스토어 4종, HA
- [[entities/etcd|etcd]] — 클러스터 상태를 담는 분산 KV 저장소. 정족수 (n/2)+1, 홀수 대수
- [[entities/rancher|Rancher]] — K3s가 끌어다 쓰는 부품(system-upgrade-controller 등)의 출처
- [[entities/traefik|Traefik]] — K3s 기본 인그레스 컨트롤러. v3·Gateway API
- [[entities/flannel|Flannel]] — K3s 기본 CNI. vxlan/wireguard-native 백엔드
- [[entities/helm|Helm]] — 쿠버네티스 패키지 매니저. K3s의 HelmChart CRD 자동 배포
- [[entities/apollo-graphql|Apollo GraphQL]] — GraphQL 서버·클라이언트 라이브러리 세트. 스키마 확인용 웹 IDE 제공

## 출처
- [[sources/ibm-infrastructure-as-code|#26 IBM IaC 해설]] — 2026-07-18 흡수, 웹 문서. 코드형 인프라 개념 해설
- [[sources/hashicorp-terraform-docs|#27 Terraform 공식 문서]] — 2026-07-19 흡수, 코어·언어·CLI 발췌 19페이지. Write-Plan-Apply·state·HCL·모듈·도입 4단계
- [[sources/terraform-hcl-syntax|#29 HCL 문법 정리]] — 2026-08-02 흡수, 실제 구성 파일 기준 자체 정리 노트. HCL 문법 12항목 + 명령 3개
- [[sources/tistory-inpa-dns-records|#28 DNS 레코드 종류]] — 2026-07-21 흡수, Inpa 블로그. DNS 레코드 종류·A vs CNAME·조회 도구
- [[sources/k3s-docs|#32 K3s 공식 문서]] — 2026-08-11 흡수, 코어 26페이지 발췌. 경량 쿠버네티스 배포판의 구조·설치·데이터스토어·HA·업그레이드
- [[sources/kubernetes-components|#34 쿠버네티스 컴포넌트]] — 2026-09-01 흡수, 쿠버네티스 공식 문서 개요 한 쪽. 컨트롤 플레인·노드·애드온 3분류, 입문 범위
- [[sources/kakaotech-graphql|#33 GraphQL 개념잡기]] — 2026-08-19 흡수, kakao tech 블로그(2019-08). GraphQL 구조 4부품과 REST 대비, 결제 프로젝트 도입 경험

## 함께 보기
- [[moc/virtualization|가상화]] — 컨테이너 아래층에서 자원을 나누는 기술
- [[moc/ai-coding-agents|AI 코딩 에이전트]] — 같은 사상이 코딩 쪽에서 반복된다

---
title: Rancher
type: entity
created: 2026-08-11
updated: 2026-08-11
sources: [k3s-docs]
tags: [쿠버네티스, 조직, 자동화]
---

# Rancher

## 한눈에 요약

- 쿠버네티스 클러스터를 여러 개 묶어 관리하는 플랫폼이자, 그 주변 오픈소스 도구들을 내놓은 곳이다.
- [[entities/k3s|K3s]]가 기본 탑재하거나 업그레이드에 쓰는 부품 상당수가 여기서 나왔기 때문에 이 위키에 등장한다.
- K3s 공식 문서 발췌 범위 안에는 **Rancher와 K3s 개발 주체의 관계가 명시돼 있지 않다** — 문서는 Rancher의 프로젝트와 지원 정책을 참조할 뿐이다.

## K3s 문서에 나오는 Rancher

문서가 Rancher를 언급하는 자리는 크게 세 갈래다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

| 갈래 | 내용 |
|---|---|
| 부품 제공 | Local Path Provisioner(노드 로컬 볼륨), system-upgrade-controller(자동 업그레이드), `rancher/k3s`·`rancher/k3s-upgrade` 컨테이너 이미지 |
| 상위 관리 | Rancher가 관리하는 K3s 클러스터는 업그레이드도 Rancher UI로 해야 한다 |
| 지원·커뮤니티 | 어떤 OS가 검증됐는지는 Rancher의 지원·유지보수 조건을 참고하라고 안내하고, 도움을 받을 곳으로 Rancher Slack을 든다 |

두 번째 갈래는 실수하기 쉬운 지점이라 문서가 따로 경고를 붙여 뒀다. Rancher에 등록(import)된 클러스터는 Rancher가 system-upgrade-controller와 Plan을 직접 관리하므로, 사람이 같은 걸 또 만들면 안 된다. Rancher가 프로비저닝한 클러스터는 아예 다른 경로(system agent)로 업그레이드된다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 이 위키에서의 등장

- **선언형 자동 업그레이드** — `Plan` CRD를 감시하는 system-upgrade-controller의 출처 ([[entities/k3s|K3s]])
- **기본 스토리지** — 노드 로컬 디스크로 영구 볼륨을 만드는 Local Path Provisioner의 출처 ([[concepts/kubernetes|쿠버네티스]])

## 함께 읽기

- [[entities/k3s|K3s]] — Rancher 계열 부품을 묶어 배포하는 경량 배포판
- [[concepts/infrastructure-as-code|코드형 인프라]] — 업그레이드를 선언으로 다루는 방식이 놓인 사상적 맥락

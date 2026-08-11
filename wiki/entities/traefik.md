---
title: Traefik
type: entity
created: 2026-08-11
updated: 2026-08-11
sources: [k3s-docs]
tags: [쿠버네티스, 네트워킹, 인그레스]
---

# Traefik

## 한눈에 요약

- 마이크로서비스 배포를 염두에 두고 만든 HTTP 리버스 프록시 겸 로드밸런서다. 바깥에서 들어온 요청을 뒤쪽 서비스로 나눠 보내는 문지기 역할을 한다.
- [[entities/k3s|K3s]]에 인그레스 컨트롤러로 기본 탑재돼 있어 이 위키에 등장한다.
- 80·443 포트를 쓰는 LoadBalancer 서비스로 뜨기 때문에, 그 포트를 다른 파드가 쓸 수 없게 된다는 점이 실무의 걸림돌이다.

## K3s에서 어떻게 쓰이나

서버를 띄우면 자동으로 배포된다. 기본 차트 값은 `/var/lib/rancher/k3s/server/manifests/traefik.yaml`에 있지만 **직접 고치면 안 된다** — K3s가 시작할 때마다 기본값으로 덮어쓰기 때문이다. 대신 같은 디렉터리에 `HelmChartConfig` 매니페스트를 하나 더 두고 값을 덮는다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

빼고 싶으면 모든 서버를 `--disable=traefik`으로 띄우면 된다. 다른 인그레스를 쓰고 싶을 때 문서가 안내하는 방법도 이것이다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

버전은 K3s 버전을 따라간다. v1.31 이하는 Traefik v2를, v1.32 이상은 v3를 설치한다 (2026-08 기준) (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## Gateway API 지원

Gateway API는 기존 Ingress API보다 표현력이 크고 역할 분리가 명확한 후속 규격이다. Ingress도 계속 지원되며 폐기 예정은 없다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

K3s에 딸려 오는 Traefik v3는 이 규격을 선택적으로 지원한다. `providers.kubernetesGateway.enabled`를 켜는 `HelmChartConfig`를 배포하면 활성화되며, Gateway API v1.4와 호환된다 (2026-08 기준) (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

> 2026년 4월 릴리스(v1.33.11+k3s1·v1.34.7+k3s1·v1.35.4+k3s1) 이전 버전에는 함정이 있다. 켜 뒀던 Traefik을 나중에 끄면 Gateway API CRD가 함께 삭제된다. 해당 릴리스를 쓰는 클러스터에 남겨 둘 Gateway 리소스가 있다면 Traefik을 끄지 말아야 한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 이 위키에서의 등장

- **기본 인그레스 컨트롤러** — 배터리 포함 방식으로 미리 꽂혀 있는 부품 중 하나 ([[entities/k3s|K3s]])
- **인그레스 리소스의 구현체** — 선언한 인그레스를 실제 라우팅으로 바꾸는 쪽 ([[concepts/kubernetes|쿠버네티스]])

## 함께 읽기

- [[entities/k3s|K3s]] — 기본 탑재 구성 요소 전체 목록
- [[entities/helm|Helm]] — `HelmChartConfig`로 값을 덮어쓰는 방식의 배경

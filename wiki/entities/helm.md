---
title: Helm
type: entity
created: 2026-08-11
updated: 2026-08-11
sources: [k3s-docs]
tags: [쿠버네티스, 패키지관리, 자동화]
---

# Helm

## 한눈에 요약

- 쿠버네티스에서 사실상 표준으로 쓰이는 패키지 관리 도구다. 매번 손으로 쓰던 YAML 매니페스트를 값만 바꿔 재사용할 수 있는 템플릿으로 만든다.
- 그 템플릿 묶음을 **차트(Chart)**라고 부른다.
- [[entities/k3s|K3s]]가 차트를 클러스터 안에서 자동 설치·갱신하는 컨트롤러를 품고 있어 이 위키에 등장한다.

## K3s의 Helm 컨트롤러

Helm 자체를 쓰는 데 K3s가 요구하는 별도 설정은 없다. kubeconfig 경로만 제대로 잡으면 된다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

특이한 건 그다음이다. K3s에는 `HelmChart` CRD를 감시하는 **Helm 컨트롤러**가 들어 있다. 자동 배포 애드온 매니페스트와 짝지으면, 디스크에 파일 하나 놓는 것만으로 차트 설치가 자동화된다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

`HelmChart` 리소스는 `helm` 명령에 주던 옵션 대부분을 필드로 받는다. 차트 이름과 저장소(`spec.chart`·`spec.repo`), 대상 네임스페이스(`spec.targetNamespace`), 값 덮어쓰기(`spec.set`·`spec.valuesContent`), 인증 정보 시크릿 참조(`spec.authSecret`) 같은 식이다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

> 자격 증명처럼 민감한 값은 `spec.valuesSecrets`로 외부 시크릿에서 읽어 오는 편이 낫다. 차트가 `existingSecret` 패턴을 지원하지 않을 때 쓰라는 것이 문서의 안내다. 참조하는 시크릿은 `HelmChart`와 같은 네임스페이스에 있어야 한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 기본 탑재 부품을 손대는 법

[[entities/traefik|Traefik]]처럼 차트로 배포되는 기본 부품은 `HelmChartConfig`로 값을 덮어쓴다. 이름과 네임스페이스를 원래 `HelmChart`와 맞추면, 추가 값 파일을 하나 더 넘긴 것처럼 동작한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

값이 여러 곳에서 겹칠 때의 우선순위는 정해져 있다. 약한 쪽부터 차트 기본값 → `HelmChart`의 `valuesContent` → `valuesSecrets` → `HelmChartConfig`의 `valuesContent` → `valuesSecrets` → `HelmChart`의 `set` 순이다. 즉 `set`이 제일 세다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 이 위키에서의 등장

- **차트 자동 배포** — 파일 하나로 애드온 설치를 자동화하는 K3s의 방식 ([[entities/k3s|K3s]])
- **기본 부품 커스터마이즈** — 덮어쓰기용 설정 리소스의 근거 ([[entities/traefik|Traefik]])

## 함께 읽기

- [[entities/k3s|K3s]] — Helm 컨트롤러를 품은 배포판
- [[concepts/kubernetes|쿠버네티스]] — 차트가 결국 만들어 내는 리소스들

---
title: K3s
type: entity
created: 2026-08-11
updated: 2026-08-11
sources: [k3s-docs]
aliases: [k3s, 경량 쿠버네티스, lightweight kubernetes]
tags: [쿠버네티스, K3s, 엣지, 컨테이너]
---

# K3s

## 한눈에 요약

- 쿠버네티스 컨트롤 플레인 전체를 100MB 미만 단일 바이너리 하나에 담은 경량 배포판이다. 여기서 컨트롤 플레인이란 클러스터를 지휘하는 서버 쪽 부품 묶음을 말한다.
- CNCF 인증을 받은 **완전 호환** 배포판이라, 기능을 덜어 낸 축소판이 아니라 같은 일을 더 가볍게 하는 버전이다.
- 엣지·홈랩·IoT·CI·개발 환경처럼 "쿠버네티스 박사 학위를 요구할 수 없는" 자리를 노린다.
- 설치가 `curl … | sh -` 한 줄이고, 데이터스토어를 SQLite·etcd·MySQL·PostgreSQL 중에 고를 수 있다는 점이 다른 배포판과 갈리는 지점이다.

## 왜 만들어졌나 — 이름부터가 목표다

쿠버네티스를 제대로 굴리려면 컨트롤 플레인 부품을 따로따로 세우고, etcd를 운영하고, 인증서를 배포해야 한다. 작은 장비 몇 대에 얹기에는 이 준비 비용이 너무 크다.

K3s는 그 복잡도를 바이너리 하나 안으로 밀어 넣는 쪽을 택했다. 컨트롤 플레인 부품 전부가 단일 프로세스로 돌아가고, 인증서 배포 같은 성가신 클러스터 운영은 K3s가 알아서 처리한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

이름은 목표를 그대로 옮긴 것이다. 메모리를 절반으로 줄이는 게 목표였고, Kubernetes는 10글자라 K8s로 줄여 쓴다. 그 절반이면 5글자니까 K3s다. **풀네임도 공식 발음도 없다**고 문서가 밝힌다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

> 무엇을 덜어 냈나 싶겠지만, 문서의 답은 "기능이 아니라 외부 의존성"이다. 필요한 건 최신 커널과 cgroup 마운트뿐이고, 나머지 부품은 전부 안에 넣었다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 서버와 에이전트

역할은 두 가지뿐이다. `k3s server`를 돌리는 노드가 **서버**, `k3s agent`를 돌리는 노드가 **에이전트**다. 서버는 컨트롤 플레인과 데이터스토어를 함께 지고, 에이전트는 그 둘을 지지 않는다. 다만 kubelet·컨테이너 런타임·CNI는 양쪽 다 돌린다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

서버 한 대만 띄워도 워크로드를 올릴 수 있는 완전한 클러스터가 된다. 에이전트를 붙이는 것은 용량과 이중화를 위한 선택이지 필수가 아니다.

### 에이전트가 클러스터에 붙는 방식

에이전트는 웹소켓 연결로 등록하고, 그 연결을 에이전트 프로세스 안의 **클라이언트 측 로드밸런서**가 유지한다. 처음에는 `--server` 주소 하나만 알고 붙지만, 붙은 뒤에는 default 네임스페이스의 서비스 엔드포인트에서 apiserver 주소 목록을 받아 온다. 그래서 서버 한 대가 죽어도 연결이 끊기지 않는다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

인증은 조인 토큰과 **노드 비밀번호** 두 겹이다. 노드는 무작위 비밀번호를 만들어 `/etc/rancher/node/password`에 두고, 클러스터는 그 해시를 `<노드이름>.node-password.k3s` 시크릿으로 보관한다. 같은 이름으로 다시 등록하려면 같은 비밀번호를 내야 한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

> 여기서 걸리기 쉽다. 호스트 이름을 재사용하려면 클러스터에서 그 노드를 먼저 삭제해야 한다. 그래야 노드 비밀번호 시크릿까지 정리된다. 호스트 이름이 자주 겹치면 `--with-node-id`로 뒤에 고유 ID를 붙이는 방법도 있다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 데이터스토어를 고를 수 있다

쿠버네티스의 상태는 보통 [[entities/etcd|etcd]]에 저장된다. K3s는 여기에 선택지를 준다. "etcd가 아닌 데이터스토어로 쿠버네티스를 돌릴 수 있다는 점이 K3s를 다른 배포판과 구분 짓는다"는 게 문서의 자평이다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

| 선택지 | 언제 고르나 | 제약 |
|---|---|---|
| 내장 SQLite (기본) | 단일 서버, CI처럼 짧게 쓰고 버리는 클러스터 | 서버 여러 대인 클러스터에는 못 쓴다 |
| 내장 etcd | 엣지에서 DB 운영 부담 없이 HA가 필요할 때 | 서버 3대 이상(홀수). 느린 디스크에서 성능 문제 |
| 외부 etcd·MySQL·MariaDB·PostgreSQL | etcd 운영 경험이 없거나 기존 DB 운영 체계를 쓸 때 | 준비된 구문(prepared statement) 지원 필요 |

외부 DB는 `--datastore-endpoint`로 접속 문자열을 준다. 자격 증명이 프로세스 정보에 노출되지 않도록 **CLI 인수보다 환경 변수를 권장**한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

> 지원하지 않는 구성이 하나 있다. `auto_increment_increment`를 1보다 크게 잡는 멀티마스터 DB(예: Galera)다. 내부적으로 쿠버네티스 API를 SQL에 얹는 kine이 "리비전은 0에서 시작해 정확히 1씩 오른다"고 전제하기 때문이다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 기본으로 딸려 오는 것들

"배터리 포함" 방식이라 클러스터를 쓸 만하게 만드는 부품이 처음부터 들어 있다. 전부 서버 전체에 `--disable`을 걸어 뺄 수 있다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

| 부품 | 역할 |
|---|---|
| containerd / cri-dockerd | 컨테이너 런타임(CRI) |
| [[entities/flannel\|Flannel]] | 파드 네트워크(CNI) |
| CoreDNS | 클러스터 내부 DNS |
| [[entities/traefik\|Traefik]] | 인그레스 컨트롤러 |
| ServiceLB | LoadBalancer 서비스 구현체 |
| kube-router netpol | 네트워크 정책 |
| local-path-provisioner | 노드 로컬 디스크를 쓰는 볼륨 |
| Spegel | 노드끼리 이미지를 나눠 갖는 분산 레지스트리 미러 |

ServiceLB는 클라우드 없이 LoadBalancer 타입 서비스를 쓰게 해 준다. 상위 쿠버네티스는 LoadBalancer 서비스를 만들 수는 있게 하지만 구현체를 주지 않아, 클라우드 제공자가 없으면 서비스가 계속 `pending`에 머문다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

동작 방식은 소박하다. LoadBalancer 서비스마다 DaemonSet을 만들어 각 노드에 `svc-` 접두사 파드를 띄운다. 그 파드가 hostPort로 받은 트래픽을 iptables로 ClusterIP에 넘긴다. 그래서 같은 포트를 이미 쓰는 노드에는 뜨지 못한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 설치와 설정

설치는 `curl -sfL https://get.k3s.io | sh -` 한 줄이다. 이 스크립트는 systemd·openrc 서비스 등록, `kubectl`·`crictl`·`ctr`·killall/uninstall 스크립트 설치, `/etc/rancher/k3s/k3s.yaml` kubeconfig 작성까지 해 준다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

에이전트로 붙이려면 `K3S_URL`과 `K3S_TOKEN`만 주면 된다. `K3S_URL`이 있으면 설치 스크립트가 서버 대신 에이전트로 구성한다. 토큰 값은 서버의 `/var/lib/rancher/k3s/server/node-token`에 있다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

설정을 주는 길은 세 갈래다. 환경 변수, CLI 플래그, 그리고 `/etc/rancher/k3s/config.yaml`(+ `config.yaml.d/*.yaml` 드롭인)이다. 같은 값이 겹치면 CLI가 이긴다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

> 설치 스크립트로 준 설정은 스크립트를 다시 돌릴 때 같이 주지 않으면 사라진다. 반대로 설정 파일 내용은 스크립트가 건드리지 않는다. 그래서 설정을 스크립트와 분리하고 싶으면 설정 파일을 쓰라고 문서가 권한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

여러 파일에 흩어진 값은 **마지막 값이 이긴다**. 키 뒤에 `+`를 붙이면 덮어쓰는 대신 이어 붙인다. 다만 한 번 `+`를 쓰면 뒤따르는 파일에서도 계속 `+`를 붙여야 누적분이 살아남는다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 고가용성 구성

컨트롤 플레인이 멈추면 안 되는 환경에서는 HA로 간다. 두 갈래이며, 필요한 서버 대수가 다르다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

| 방식 | 서버 대수 | 특징 |
|---|---|---|
| 내장 etcd | 3대 이상, 홀수 | 첫 서버를 `--cluster-init`으로 띄우고 나머지가 `--server`로 합류 |
| 외부 DB | 2대 이상 | 모든 서버가 같은 `--datastore-endpoint`를 본다 |

에이전트가 바라볼 주소는 서버 IP 대신 **고정 등록 주소**를 두는 편이 낫다. 클라우드에서는 서버가 뜨고 지면서 IP가 바뀌기 때문이다. L4 로드밸런서, 라운드로빈 DNS, 탄력적 IP 중 아무거나 쓰면 된다. 이때 인증서 오류를 피하려면 `--tls-san`으로 그 주소를 인증서에 넣어야 한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

기존 단일 노드 클러스터는 `--cluster-init`을 붙여 재시작하는 것만으로 SQLite에서 etcd로 넘어간다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

### 서버 역할 쪼개기

내장 etcd를 쓸 때는 서버의 역할을 나눌 수 있다. `--disable-apiserver --disable-controller-manager --disable-scheduler`면 etcd 전용 노드가 되고, `--disable-etcd`면 컨트롤 플레인 전용 노드가 된다. 단 컨트롤 플레인 전용 노드가 클러스터의 첫 서버일 수는 없다 — etcd 역할 노드가 먼저 있어야 한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 업그레이드와 백업

업그레이드 방법은 두 가지다. 하나는 같은 설정으로 설치 스크립트를 다시 돌리는 수동 방식이고, 다른 하나는 Rancher의 system-upgrade-controller에 `Plan` 리소스를 던지는 자동 방식이다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

자동 방식은 "어느 노드를 어느 버전으로 올릴지"를 선언만 하면 컨트롤러가 노드마다 Job을 띄워 처리한다. 릴리스 채널(`stable`·`latest`·마이너 버전별)을 걸어 두면 새 릴리스가 나올 때마다 따라 올라간다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

**서버를 먼저, 에이전트를 나중에**는 어느 방식에서든 지켜야 하는 순서다. 자동 방식에서는 에이전트 Plan의 `prepare` 단계가 서버 Plan이 끝날 때까지 기다려 이 순서를 강제한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

백업은 데이터스토어 종류를 따라간다. SQLite는 `/var/lib/rancher/k3s/server/db/`를 통째로 복사하면 되고, 외부 DB는 DB 관리자가 하던 대로 하며, 내장 etcd는 `k3s etcd-snapshot` 명령을 쓴다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

> 놓치기 쉬운 함정이 하나 있다. 데이터스토어만 백업하면 소용이 없다. `/var/lib/rancher/k3s/server/token`도 같이 받아 둬야 한다. 이 토큰이 데이터스토어 안의 기밀 데이터를 암호화하는 키라서, 값이 다르면 스냅샷을 복원해도 쓸 수 없다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 알아 둘 제약

- **윈도우 미지원** — 네이티브 지원이 없다. 앞으로의 가능성만 열어 뒀다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).
- **디스크가 병목** — 클러스터 성능은 DB 성능을 따라간다. 라즈베리 파이의 SD 카드·eMMC는 etcd의 쓰기 부하를 못 견디므로 외장 SSD를 권한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).
- **서버끼리 맞춰야 하는 플래그** — `--cluster-dns`·`--cluster-domain`·`--cluster-cidr`·`--service-cidr`, `--disable` 계열, `--secrets-encryption`이 서로 다르면 조인 자체가 실패한다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).
- **로그 레벨을 부품별로 못 나눈다** — 모든 쿠버네티스 부품이 한 프로세스 안에서 도는 구조라 klog 설정이 하나로 묶인다. `-v=<level>`을 부품별로 주는 식은 기대대로 동작하지 않는다 (→ [[sources/k3s-docs|#32 K3s 공식 문서]]).

## 이 위키에서의 등장

- **경량 쿠버네티스 배포판** — 이 위키가 처음 다루는 컨테이너 오케스트레이션 주제의 출발점 ([[concepts/kubernetes|쿠버네티스]])
- **선언형 인프라의 사례** — `Plan` CRD로 업그레이드를 선언해 두면 컨트롤러가 실행하는 구조 ([[concepts/infrastructure-as-code|코드형 인프라]])
- **패키징 대상** — 기본 탑재된 CNI·인그레스·패키지 매니저의 맥락 ([[entities/flannel|Flannel]] · [[entities/traefik|Traefik]] · [[entities/helm|Helm]])

## 함께 읽기

- [[concepts/kubernetes|쿠버네티스]] — K3s가 구현하는 원본 시스템의 구성 요소
- [[entities/etcd|etcd]] — HA 구성의 기본 데이터스토어와 정족수 규칙
- [[entities/rancher|Rancher]] — K3s가 끌어다 쓰는 주변 프로젝트들의 출처
- [[concepts/infrastructure-as-code|코드형 인프라]] — 같은 선언형 사상을 인프라 쪽에서 본 갈래

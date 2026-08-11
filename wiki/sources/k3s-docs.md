---
title: "K3s 공식 문서 — 코어 26페이지 발췌"
label: "#32 K3s 공식 문서"
type: source
credibility: high
volatility: hot
created: 2026-08-11
updated: 2026-08-11
sources: []
tags: [쿠버네티스, K3s, 공식문서, 엣지, 코드형인프라]
---

# K3s 공식 문서 — 코어 26페이지 발췌

## 한 줄 요약

100MB 미만 단일 바이너리에 [[concepts/kubernetes|쿠버네티스]] 컨트롤 플레인 전체를 담은 경량 배포판 [[entities/k3s|K3s]]의 공식 문서에서, 소개·설치·데이터스토어·네트워킹·업그레이드 등 코어 26페이지를 발췌한 자료다.

## 핵심 내용

- **정체**: K3s는 CNCF 인증을 받은 완전 호환 쿠버네티스 배포판이며, 축소판이 아니라 "표준 클러스터가 해야 할 일을 다 하는 더 가벼운 버전"이라고 문서가 직접 못 박는다. 이름의 유래는 단순하다 — 메모리 사용량을 절반으로 줄이려 했고, Kubernetes(10글자, K8s)의 절반이라 5글자 K3s가 됐다. 풀네임도 공식 발음도 없다.
- **서버와 에이전트**: `k3s server`를 돌리는 노드가 서버(컨트롤 플레인 + 데이터스토어), `k3s agent`를 돌리는 노드가 에이전트다. 둘 다 kubelet·컨테이너 런타임·CNI는 돌린다. 서버 한 대만으로도 완전히 동작하는 클러스터가 된다.
- **데이터스토어 4종 선택권**: 기본은 내장 SQLite, 다중 서버 HA는 내장 etcd, 그 외 외부 DB로 etcd·MySQL·MariaDB·PostgreSQL을 쓴다. "etcd 외의 데이터스토어로 쿠버네티스를 돌릴 수 있다는 점이 K3s를 다른 배포판과 구분 짓는다"는 것이 문서의 자평이다.
- **배터리 포함**: containerd/cri-dockerd(CRI), Flannel(CNI), CoreDNS, Traefik(인그레스), ServiceLB(로드밸런서), kube-router 네트워크 정책, local-path-provisioner(볼륨), Spegel(분산 이미지 미러), 호스트 유틸리티까지 묶여서 배포된다. 각각은 `--disable`로 뺄 수 있다.
- **설치는 한 줄**: `curl -sfL https://get.k3s.io | sh -`. 에이전트는 `K3S_URL`·`K3S_TOKEN` 환경 변수만 붙이면 된다. 설정은 환경 변수·CLI 플래그·`/etc/rancher/k3s/config.yaml`(+ `config.yaml.d/` 드롭인) 세 경로로 주며, CLI가 우선한다.
- **HA 구성 두 갈래**: 내장 etcd는 **서버 3대 이상(홀수)**, 외부 DB는 서버 2대 이상. 에이전트가 붙을 고정 등록 주소(L4 로드밸런서·라운드로빈 DNS·탄력적 IP)를 앞에 두는 것을 권장한다.
- **업그레이드**: 설치 스크립트 재실행(수동)과 Rancher의 system-upgrade-controller를 쓴 선언형 자동 업그레이드(`Plan` CRD) 두 방식이다. 서버를 먼저, 그다음 에이전트 순서는 어느 쪽에서든 지켜야 한다.
- **요구 사양**: 서버 2코어·2GB, 에이전트 1코어·512MB가 최소선이다 (2026-08 기준).

## 주요 주장 / 데이터

- **서버 사이징 표** — 서버 2코어/4GB면 에이전트 0~350대, 4코어/8GB면 351~900대, 8코어/16GB면 901~1800대, 16코어 이상/32GB면 1800대 이상. 서버 3대 HA면 위 수치보다 약 50% 더 확장된다(예: 4vCPU/8GB 3대 → 약 1200대). 에이전트는 한 번에 50대 이하씩 나눠 붙이라고 권한다. 255대를 넘길 거면 기본 `cluster-cidr`부터 바꿔야 한다.
- **포트** — 6443(apiserver·supervisor)은 모든 노드가 서버에 닿아야 하고, Flannel VXLAN이면 UDP 8472, WireGuard면 UDP 51820(IPv6는 51821), 메트릭 서버를 쓰면 10250, 내장 etcd HA면 서버끼리 2379·2380이 필요하다. "VXLAN 포트를 외부에 노출하면 클러스터 네트워크가 누구에게나 열린다"고 경고한다.
- **홀수 서버의 이유** — etcd 정족수는 서버 n대에서 (n/2)+1이다. 짝수로 늘리면 대수는 늘지만 견딜 수 있는 장애 노드 수는 그대로여서 오히려 내결함성이 나빠진다.
- **디스크가 성능을 정한다** — "클러스터 성능은 DB 성능에 달려 있다." etcd는 쓰기 집약적이라 라즈베리 파이의 SD 카드·eMMC는 IO를 감당하지 못한다. 외장 SSD를 권한다.
- **토큰은 데이터스토어 암호화 키다** — 백업할 때 데이터스토어뿐 아니라 `/var/lib/rancher/k3s/server/token`도 같이 받아야 한다. 토큰이 다르면 스냅샷을 복원해도 쓸 수 없다.
- **서버 간에 반드시 일치해야 하는 플래그** — `--cluster-dns`·`--cluster-domain`·`--cluster-cidr`·`--service-cidr`, `--disable` 계열, `--secrets-encryption`. 어긋나면 `failed to validate server configuration: critical configuration value mismatch.` 로 조인이 실패한다.
- **인증된 외부 DB 버전** (2026-08 기준) — etcd 3.5.21, MySQL 8.0·8.4, MariaDB 10.11·11.4, PostgreSQL 15.12·16.7·17.3. Galera처럼 `auto_increment_increment`를 1보다 크게 잡는 멀티마스터 구성은 지원하지 않는다. kine이 리비전을 0에서 시작해 정확히 1씩 증가한다고 전제하기 때문이다.
- **다운그레이드 차단** — 쿠버네티스는 컨트롤 플레인 다운그레이드를 지원하지 않으므로, k3s-upgrade 이미지는 하향 업그레이드를 거부하고 Plan을 실패시킨다. `cordon: true`였던 노드는 실패 후에도 cordon 상태로 남는다.
- **버전 스큐** — 서버가 에이전트보다 새로운 것은 되지만, 에이전트가 서버보다 새로울 수는 없다. 마이너 버전을 건너뛰는 업그레이드도 막지 않으니 사람이 챙겨야 한다.
- **윈도우 미지원** — "현재 K3s는 윈도우를 네이티브로 지원하지 않는다"(향후 가능성은 열어 둠).

## 기존 위키와의 연결

- 강화: [[concepts/infrastructure-as-code|코드형 인프라]]의 선언형·자동 강제 사상을 컨테이너 오케스트레이션 영역에서 다시 확인해 준다 — 특히 `Plan` CRD로 "어느 노드를 어느 버전으로 올릴지"를 선언만 하면 컨트롤러가 실행하는 자동 업그레이드, 그리고 설정 파일 드롭인 병합 규칙이 그렇다. [[entities/terraform|Terraform]] 같은 외부 IaC 도구로 수동 업그레이드 절차를 감쌀 수 있다는 언급도 문서에 있다.
- 모순: 직접 모순 없음. 이 위키에 쿠버네티스·컨테이너 오케스트레이션을 다룬 페이지가 아직 없어 충돌할 상대가 없었다.
- 신규: [[entities/k3s|K3s]], [[concepts/kubernetes|쿠버네티스]], [[entities/etcd|etcd]], [[entities/rancher|Rancher]], [[entities/traefik|Traefik]], [[entities/flannel|Flannel]], [[entities/helm|Helm]] 페이지 생성.

## 출처 정보

- raw: raw/k3s-docs.md
- 저자/발행처: K3s 프로젝트 (공식 문서). K3s 개발 주체는 발췌 범위 안에 명시돼 있지 않다 — 문서가 Rancher의 프로젝트·지원 정책을 여러 곳에서 참조할 뿐이다.
- 수집일: 2026-08-11
- URL: https://docs.k3s.io/ (문서 소스 저장소 `k3s-io/docs`의 `docs/` 마크다운 원본을 그대로 받음)
- 범위: 코어 26페이지 — 소개·퀵스타트·아키텍처, 설치(설치 개요·요구사항·설정 옵션·서버 역할·제거), 데이터스토어(개요·외부 DB HA·내장 etcd HA·백업복원), 네트워킹(개요·기본 옵션·네트워킹 서비스), 애드온(스토리지·Helm), 클러스터 접근, CLI 개요, 업그레이드(개요·자동·수동), 보안(개요·시크릿 암호화), FAQ, 관련 프로젝트. 제외: 고급 옵션(advanced), 에어갭·프라이빗 레지스트리·레지스트리 미러, Multus·멀티클라우드·클러스터 로드밸런서, 하드닝 가이드와 CIS 자가진단, 릴리스 노트, `k3s server`/`agent` 등 플래그 전체 목록, reference 계열.

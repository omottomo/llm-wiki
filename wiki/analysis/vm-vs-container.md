---
title: "분석 — 가상 머신 vs 컨테이너"
type: analysis
created: 2026-09-22
updated: 2026-09-22
sources: [wikipedia-virtualization-foundations, virtio-and-firecracker-docs, oracle-virtualization-explained, ibm-what-is-virtualization, aws-what-is-virtualization, redhat-what-is-kvm]
tags: [분석, 가상화, 컨테이너, 마이크로VM]
---

# 분석 — 가상 머신 vs 컨테이너

## 결론 먼저

> 가상 머신과 컨테이너는 격리를 어디서 그을지가 다르다. 가상 머신은 커널부터 따로 갖고 컨테이너는 호스트 커널을 공유하므로, 전자는 강한 격리와 OS 다양성을 얻고 후자는 가벼움과 속도를 얻는다. 둘 사이의 빈자리를 메우려고 나온 것이 마이크로VM이다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]·[[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]]).

## 비교표

| 축 | 가상 머신 | 컨테이너 | 마이크로VM |
|---|---|---|---|
| 격리 경계 | 가상 하드웨어. 게스트마다 커널이 따로 | 호스트 커널을 공유. 유저 공간만 분리 | 가상 하드웨어. VM 과 같은 경계 |
| 다른 OS | 리눅스·윈도우·macOS 를 한 기계에서 동시에 | 못 한다. 배포판은 달라도 커널은 같아야 | VM 과 같다 |
| 오버헤드 | 에뮬레이션과 중간 VM 계층을 거친다 | 평범한 시스템 콜 인터페이스를 쓴다. 더 적다 | VM 격리를 유지하면서 불필요한 것을 걷어냈다 |
| 하드웨어 지원 | 성능을 위해 CPU 확장이 필요하다 | 필요 없다 | KVM 위에서 돈다 |
| 주 쓰임새 | 강한 격리와 OS 다양성이 필요한 워크로드 | 일관된 배포, 고밀도 실행 | 멀티테넌트 서버리스·고밀도 컨테이너 환경 |

(→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]·[[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]·[[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]])

### 가상 머신 쪽 상세

가상 머신은 컴퓨터 한 대를 하드웨어 수준에서 통째로 재현하고 그 위에 OS 전체를 돌린다. 그래서 여러 OS 인스턴스가 물리 x86 머신 한 대를 나눠 쓸 수 있다 — 리눅스와 윈도우와 macOS 가 한 기계에서 동시에 도는 식이다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]·[[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]).

대가는 중복이다. IBM 문서는 이 방식이 가상화를 아예 하지 않는 것보다는 효율적이지만, 돌리려는 앱마다 불필요한 코드와 서비스를 중복한다고 짚는다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]).

### 컨테이너 쪽 상세

컨테이너는 OS 수준 가상화다. 커널이 격리된 유저 공간 인스턴스 여러 개를 허용하는 OS 기능이며, 리눅스에서는 네임스페이스와 cgroups 가 그 토대다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

오버헤드가 적은 이유는 분명하다. 컨테이너 안의 프로그램은 **OS 의 평범한 시스템 콜 인터페이스**를 그대로 쓴다. 에뮬레이션을 거치거나 중간 가상 머신 안에서 돌 필요가 없다. 게다가 효율적인 성능을 위해 하드웨어 지원을 요구하지도 않는다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

## 무엇을 포기하는가 — 유연성

여기서 헷갈리기 쉬운데, 컨테이너가 "가벼운 VM"은 아니다. 커널을 공유한다는 사실이 능력의 상한을 정한다.

OS 수준 가상화는 다른 가상화 방식만큼 유연하지 않다. **호스트와 다른 게스트 OS 나 다른 커널을 올릴 수 없다.** 리눅스에서 배포판이 다른 것은 괜찮지만 윈도우 같은 다른 운영체제는 호스팅하지 못한다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

바꿔 말하면, "커널부터 다른 환경이 필요한가"가 둘을 가르는 첫 질문이다. 필요하다면 컨테이너로는 답이 안 나온다.

> 용어 정리를 하나 해 두자. AWS 문서는 컨테이너화를 **애플리케이션 가상화의 한 종류**로 규정한다 (→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]). 컨테이너를 가상화의 반대편이 아니라 가상화의 한 갈래로 보는 관점이다.

## 실무에서는 둘 중 하나가 아니다

선택지가 배타적이라고 생각하기 쉽지만 실제로는 아니다.

오라클 문서는 조직들이 쿠버네티스 기반 전략의 일부로 **VM 안에서 컨테이너를 돌리는** 경우가 잦다고 적는다. 둘 중 무엇을 고를지는 쓰임새, 운영 요구, 필요한 격리 수준과 성능에 달렸다는 것이다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

반대 방향의 합류도 있다. KubeVirt 는 VM 을 [[concepts/kubernetes|쿠버네티스]] 안으로 끌어들여 컨테이너 앱과 나란히 관리하게 한다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

AWS 는 둘의 차이를 비유로 설명한다. 서버 가상화가 두 지점을 잇는 도로를 놓는 일이라면, 컨테이너화는 어느 쪽으로든 날아갈 수 있는 헬리콥터를 만드는 일이라는 것이다 (→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]).

## 마이크로VM — 사이를 메우는 쪽

가장 흥미로운 지점은 이 대립을 없애려는 시도다.

파이어크래커의 설계 문서는 목표를 이렇게 적는다. **전통적 VM 의 보안·워크로드 격리 성질에 컨테이너가 가능하게 한 속도·민첩성·자원 효율을 결합한다**는 것이다 (→ [[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]]).

주장의 근거가 수치로 남아 있다. 최소 리눅스 커널·싱글코어 CPU·128MiB RAM 구성에서 **호스트 코어당 초당 마이크로VM 5개**의 지속 변경률을 지원한다. 물리 코어 36개짜리 호스트라면 초당 180개를 만들 수 있다는 계산이다 (→ [[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]]).

격리는 포기하지 않는다. 첫 겹은 [[entities/kvm|KVM]]과 가상화 경계이고, 둘째 겹은 프로세스 수준 제약이다. seccomp 필터로 시스템 콜을 묶고, cgroups·네임스페이스로 자원을 가르며, jailer 가 권한을 떨군 뒤 파이어크래커 바이너리로 `exec()` 한다 (→ [[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]]).

위협 모델은 더 단호하다. 모든 vCPU 스레드는 시작된 순간부터 악성 코드를 실행 중이라고 간주한다 (→ [[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]]).

> 벤더 개괄과 1차 자료가 말하는 지표가 다르다는 점은 짚어 둘 만하다. 오라클 문서는 마이크로VM 이 "밀리초 단위로 부팅한다"고 적지만 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]), 파이어크래커 설계 문서가 제시하는 수치는 부팅 시간이 아니라 생성률이다 (→ [[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]]). 같은 이야기를 다른 지표로 하고 있어, 두 수치를 섞어 인용하지 않는 편이 안전하다.

## 함께 읽기

- [[concepts/virtualization|가상화]] — VM 쪽 세계의 전체 지도
- [[concepts/kubernetes|쿠버네티스]] — 컨테이너 쪽 세계의 표준 오케스트레이터
- [[entities/kvm|KVM]] — 마이크로VM 이 올라타는 커널 쪽 토대
- [[concepts/virtualization-internals|가상화 작동 원리]] — VM 의 오버헤드가 어디서 오는지

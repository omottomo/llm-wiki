---
title: QEMU
type: entity
created: 2026-09-22
updated: 2026-09-22
sources: [wikipedia-virtualization-foundations, oracle-virtualization-explained]
aliases: [qemu-dm]
tags: [QEMU, 가상화, 하이퍼바이저, 리눅스]
---

# QEMU

## 한눈에 요약

- 하드웨어를 흉내 내는 에뮬레이터이자, 커널 쪽 가상화 기능 위에 올라가 장치 모델을 맡는 유저스페이스 짝이다.
- 리눅스에서는 KVM 과, Xen 에서는 HVM 게스트와 짝을 이뤄 쓰인다.

## 무슨 일을 하나

가상화에서 일은 두 겹으로 나뉜다. CPU와 메모리 가상화는 커널 쪽이 맡고, 장치 모델과 관리는 유저스페이스가 맡는다. QEMU 는 그 유저스페이스 쪽이다.

위키백과는 마이크로커널 어법을 빌려 이를 분명히 가른다. 리눅스에 적용하면 [[entities/kvm|KVM]]이 하이퍼바이저이고, QEMU 나 Cloud Hypervisor 는 그 KVM 을 쓰는 VMM 이라는 것이다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

오라클도 KVM 이 QEMU·libvirt 같은 유저스페이스 도구와 통합된다고 적는다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

[[entities/xen|Xen]] 쪽에서도 같은 역할을 맡는다. HVM 게스트의 장치 에뮬레이션이 QEMU 프로젝트 기반이며, dom0 에서 백엔드로 도는 패치된 `qemu-dm` 데몬이 가상 머신에 입출력 가상화를 제공한다. 그래서 HVM 게스트가 보는 것은 상당히 기본적인 PC 의 에뮬레이트된 모습이다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

성능이 중요한 환경에서는 이 에뮬레이트된 PC 하드웨어를 주로 부팅에만 쓰고, 평소 동작에는 PV 디스크·네트워크 드라이버를 쓴다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

> 이 페이지는 위 자료들이 QEMU 에 관해 직접 말한 것만 담은 스텁이다. 에뮬레이터로서의 독자적 기능은 아직 근거가 되는 자료가 위키에 들어와 있지 않다.

## 이 위키에서의 등장

- **KVM 의 유저스페이스 짝** — 커널 쪽 KVM 과 역할을 나눠 갖는다 ([[entities/kvm|KVM]])
- **Xen HVM 의 장치 에뮬레이션** — `qemu-dm` 데몬이 dom0 에서 돈다 ([[entities/xen|Xen]])

## 함께 읽기

- [[entities/kvm|KVM]] — 커널 쪽 짝
- [[entities/xen|Xen]] — HVM 게스트에서 QEMU 를 쓰는 하이퍼바이저
- [[concepts/hypervisor|하이퍼바이저]] — 하이퍼바이저와 VMM 이라는 용어 구분

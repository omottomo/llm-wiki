---
title: Xen
type: entity
created: 2026-09-22
updated: 2026-09-22
sources: [xen-sosp-2003-paper, wikipedia-virtualization-foundations]
aliases: [Xen Project, XenoLinux]
tags: [Xen, 반가상화, 하이퍼바이저, 가상화]
---

# Xen

## 한눈에 요약

- 케임브리지 대학에서 출발한 오픈소스 타입 1 하이퍼바이저다. 게스트 운영체제를 고쳐 쓰는 반가상화로 x86의 가상화 난점을 우회한 것으로 유명하다.
- 2003년 논문과 첫 공개 릴리스로 세상에 나왔고, 이후 하드웨어 보조를 쓰는 방식까지 함께 지원하게 됐다.
- 특권을 가진 첫 도메인 Domain0 가 관리 소프트웨어를 맡고, 나머지 도메인은 그 아래에서 돈다.

## 어디서 나왔나

Xen은 케임브리지 대학 컴퓨터 연구소의 연구 프로젝트로 시작됐다. 이언 프랫이 이끌었고 그의 박사과정 학생 케어 프레이저가 함께했다. 첫 공개 릴리스는 2003년, 버전 1.0은 2004년에 나왔다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

같은 해 SOSP에 발표된 「Xen and the Art of Virtualization」이 설계를 공개한 원 논문이다. 저자는 케임브리지 컴퓨터 연구소의 아홉 명이다 (→ [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]).

이후 소유와 운영은 여러 차례 옮겨 갔다. 2007년 10월 시트릭스가 XenSource를 인수했고, 2013년 4월 프로젝트가 리눅스 재단 산하 협업 프로젝트로 넘어가 "Xen Project"라는 이름을 새로 얻었다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

## 반가상화 — 게스트를 고쳐 쓴다

Xen의 핵심 발상은 하드웨어를 똑같이 흉내 내기를 포기하는 것이다. 하부 하드웨어와 "비슷하지만 똑같지는 않은" 가상 머신 추상화를 제시하고, 게스트 OS를 그 추상화에 맞게 포팅한다 (→ [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]).

중요한 단서가 있다. 고치는 것은 게스트 **운영체제**뿐이고 ABI는 건드리지 않는다. 그래서 게스트 위에서 도는 애플리케이션은 수정할 필요가 없다 (→ [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]).

구체적인 수법은 [[concepts/virtualization-internals|가상화 작동 원리]]에 정리돼 있다. 게스트 OS를 ring 1로 내려 앉히고, hypercall과 이벤트로 양방향 통로를 내며, 장치는 에뮬레이트하지 않고 I/O 링으로 주고받는 방식이다 (→ [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]).

성능 주장도 분명하다. Linux와 Windows XP를 동시에 호스팅해도 비가상화 대비 "많아야 몇 퍼센트"의 저하에 그친다고 보고한다. 설계 목표는 현대 서버 한 대에 VM 100개였다 (→ [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]).

## Domain0 와 도메인 구조

Xen은 실행 중인 VM을 **도메인**이라 부른다. 프로그램과 프로세스의 관계에 빗댄 구분으로, Xen이 호스팅하는 OS 자체는 게스트 OS라 부른다 (→ [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]).

부팅 때 만들어지는 첫 도메인이 **Domain0**다. 제어 인터페이스를 쓸 수 있는 유일한 도메인이며 관리 소프트웨어를 호스팅한다. 다른 도메인의 생성·종료, 스케줄링 파라미터, 물리 메모리 할당, 디스크·네트워크 접근 권한이 전부 여기서 결정된다 (→ [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]).

설계 의도는 정책과 메커니즘의 분리다. 하이퍼바이저는 기본 제어 동작만 제공하고, 복잡한 정책 판단은 Domain0 위의 관리 소프트웨어에 맡긴다 (→ [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]).

위키백과 쪽 서술도 같은 구조를 확인해 준다. 하이퍼바이저가 모든 도메인의 메모리 관리와 CPU 스케줄링을 맡고 가장 특권적인 도메인(dom0)을 띄우며, dom0에서 비특권 도메인(domU)을 시작한다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

## 이후 — HVM 이 더해지다

2005년 이후 CPU가 하드웨어 보조를 제공하게 되면서 Xen도 길을 하나 더 냈다. 수정하지 않은 게스트를 돌리는 방식이며, Xen 용어로는 **HVM**(hardware virtual machine)이라 부른다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

그 결과 (2026-09 기준) 게스트 실행 방식이 다섯 갈래가 됐다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

| 방식 | 내용 |
|---|---|
| PV | 가상화를 인지하는 게스트와 장치. 하드웨어 지원이 없는 CPU에서도 돈다 |
| HVM | 하드웨어 보조 전가상화 + 에뮬레이트된 장치 |
| HVM + PV 드라이버 | 하드웨어 보조 전가상화에 입출력만 PV 드라이버로 |
| PVHVM | PV가 거드는 하드웨어 보조 가상화 + PV 입출력 드라이버 |
| PVH | HVM 컨테이너 안의 완전 반가상화 게스트. 가능한 곳에서 하드웨어 보조로 가속 |

HVM 게스트의 장치 에뮬레이션은 [[entities/qemu|QEMU]] 기반이다. dom0에서 백엔드로 도는 패치된 `qemu-dm` 데몬이 그 일을 맡는다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

> Xen 3.0부터는 하드웨어 보조가 있는 CPU에서 Windows를 수정 없이 게스트로 돌릴 수 있다. 그 전 1.x 시절 마이크로소프트 리서치와 케임브리지가 만든 Windows XP 포팅은 라이선스 때문에 공개되지 않았고, 원 SOSP 논문에만 경험이 기록돼 있다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

라이브 마이그레이션도 지원한다. LAN을 통해 메모리를 반복 복사한 뒤, 마지막 동기화에 60~300ms의 정지만 들인다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

## 이 위키에서의 등장

- **반가상화의 원전** — 게스트를 고쳐 쓰는 접근의 1차 근거로 인용된다 ([[concepts/virtualization-internals|가상화 작동 원리]])
- **타입 1 하이퍼바이저의 예** — VMware ESXi·Hyper-V와 나란히 놓인다 ([[concepts/hypervisor|하이퍼바이저]])
- **I/O 링의 계보** — virtio 의 공유 메모리 방식보다 먼저 같은 발상을 구현했다 ([[concepts/virtualization-internals|가상화 작동 원리]])

## 함께 읽기

- [[concepts/virtualization-internals|가상화 작동 원리]] — 반가상화가 x86에서 왜 필요했는지
- [[entities/kvm|KVM]] — 다른 길로 같은 문제를 푼 리눅스 쪽 구현
- [[entities/qemu|QEMU]] — Xen HVM 게스트의 장치 에뮬레이션을 맡는 도구
- [[concepts/hypervisor|하이퍼바이저]] — Xen이 놓이는 분류상의 자리

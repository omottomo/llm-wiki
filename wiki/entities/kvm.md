---
title: KVM (Kernel-based Virtual Machine)
type: entity
created: 2026-09-22
updated: 2026-09-22
sources: [redhat-what-is-kvm, kernel-kvm-docs, aws-what-is-virtualization, oracle-virtualization-explained, wikipedia-virtualization-foundations, ibm-what-is-virtualization, virtio-and-firecracker-docs]
aliases: [Kernel-based Virtual Machine, 커널 기반 가상 머신]
tags: [KVM, 가상화, 하이퍼바이저, 리눅스]
---

# KVM (Kernel-based Virtual Machine)

## 한눈에 요약

- 리눅스 커널 자체를 하이퍼바이저로 만드는 오픈소스 가상화 기술이다. 가상 머신 하나가 커널이 스케줄링하는 평범한 리눅스 프로세스가 된다.
- 2006년에 발표돼 이듬해 커널에 병합됐고, 지금은 리눅스 진영 가상화의 사실상 표준 부품이다.
- 타입 1 하이퍼바이저인지 아닌지를 두고 자료마다 서술이 갈린다. 이 페이지는 어느 한쪽으로 정리하지 않고 양쪽을 보존한다.

## 연혁과 자리

KVM은 2006년에 발표됐고 이듬해 리눅스 커널에 병합됐다. 레드햇의 가상화 포트폴리오를 비롯해 여러 오픈소스 가상화 기술이 KVM을 구성 요소로 쓴다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

오라클도 독립적으로 같은 연도를 말한다. 2007년부터 리눅스 커널에 포함돼 대부분의 리눅스 배포판에서 기본으로 제공된다는 것이다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

IBM은 이를 "리눅스가 자체 하이퍼바이저를 갖고 있다"는 문장으로 정리한다. KVM이 Intel과 AMD의 가상화 프로세서 확장을 지원해, 리눅스 호스트 안에서 x86 기반 VM을 만든다는 설명이다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]).

## 핵심 설계 — VM이 곧 리눅스 프로세스다

왜 하필 커널 안에 넣었나. 하이퍼바이저는 VM을 돌리려고 메모리 관리자, 프로세스 스케줄러, I/O 스택, 디바이스 드라이버, 보안 관리자, 네트워크 스택 같은 OS 수준 부품을 필요로 한다. KVM은 커널의 일부라서 이 부품들을 **이미 갖고 있다** (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

그 결과가 이 기술의 핵심 설계다. KVM에서 VM 하나는 **평범한 리눅스 프로세스**이며, 표준 리눅스 스케줄러가 스케줄링한다. 각 VM은 네트워크 카드·그래픽 어댑터·CPU·메모리·디스크 같은 전용 가상 하드웨어를 갖는다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

쉽게 말하면 VM이 특별한 존재가 아니라 **또 하나의 프로세스**가 된다. 그래서 리눅스의 성능 기능과 스케줄러의 세밀한 제어가 VM에도 그대로 적용된다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

## 쓰는 법 — /dev/kvm 에 거는 ioctl

벤더 해설의 "VM이 프로세스"라는 말이 실제로 무슨 뜻인지는 커널 문서를 보면 분명해진다. KVM API는 여러 종류의 **파일 디스크립터**와 그에 거는 **ioctl**을 중심으로 돌아간다 (→ [[sources/kernel-kvm-docs|#42 KVM 커널 문서]]).

계층은 위에서 아래로 열린다 (→ [[sources/kernel-kvm-docs|#42 KVM 커널 문서]]).

| 단계 | 어떻게 얻나 | 무엇을 다루나 |
|---|---|---|
| system | `open("/dev/kvm")` | KVM 하위 시스템 전체 속성. VM 생성도 여기서 한다 |
| VM | system fd 에 `KVM_CREATE_VM` | 메모리 배치 등 VM 전체. vcpu·장치 생성도 여기서 |
| vcpu | VM fd 에 `KVM_CREATE_VCPU` | 가상 CPU 하나의 동작 |

장치 ioctl이 하나 더 있어 `KVM_CREATE_DEVICE`로 얻는 fd에 건다. 다만 흐름의 뼈대는 위 세 계층이다 (→ [[sources/kernel-kvm-docs|#42 KVM 커널 문서]]).

게스트를 실제로 굴리는 것은 **`KVM_RUN`**이다. vcpu ioctl이며 명시적 인자가 없다. 대신 vcpu fd를 오프셋 0에서 mmap한 `struct kvm_run`이 암묵적 인자 블록 노릇을 한다 (→ [[sources/kernel-kvm-docs|#42 KVM 커널 문서]]).

발행 주체에도 제약이 있다. VM ioctl은 그 VM을 만든 같은 프로세스에서, vcpu ioctl은 그 vcpu를 만든 같은 스레드에서 거는 것이 원칙이다 (→ [[sources/kernel-kvm-docs|#42 KVM 커널 문서]]).

> ABI는 리눅스 2.6.22부터 안정화됐고, `KVM_GET_API_VERSION`은 상수 12를 돌려준다. 다른 값이 나오면 애플리케이션은 실행을 거부해야 한다 (→ [[sources/kernel-kvm-docs|#42 KVM 커널 문서]]).

## QEMU 와의 역할 분담

KVM만으로는 VM이 완성되지 않는다. 커널 쪽 KVM이 CPU와 메모리 가상화를 맡고, 유저스페이스 쪽 짝이 장치 모델과 관리를 맡는 구조다.

오라클은 KVM이 [[entities/qemu|QEMU]]·libvirt 같은 유저스페이스 도구와 통합된다고 적는다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]). 위키백과는 마이크로커널 어법을 빌려 더 분명히 가른다 — KVM이 하이퍼바이저이고 QEMU나 Cloud Hypervisor는 그 KVM을 쓰는 VMM이라는 것이다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

짝이 QEMU 하나만인 것도 아니다. AWS의 파이어크래커도 KVM 위에 서는 유저스페이스 VMM이며, vCPU 스레드가 `KVM_RUN` 메인 루프를 돈다 (→ [[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]]).

## 보안과 운영 기능

- **SELinux 와 sVirt.** SELinux가 VM 둘레에 보안 경계를 세우고, sVirt가 이를 확장해 게스트 VM에 강제 접근 제어(MAC)를 적용한다. 수작업 라벨링 실수를 막는 것이 sVirt의 목적이다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).
- **라이브 마이그레이션.** 돌아가는 VM을 물리 호스트 사이에서 체감되는 서비스 중단 없이 옮긴다. 전원은 켜진 채, 네트워크 연결도 살아 있고, 앱도 계속 돈다. 현재 상태를 저장해 뒀다가 나중에 재개할 수도 있다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).
- **스토리지.** 리눅스가 지원하는 저장소는 무엇이든 쓸 수 있고, 공유 파일 시스템도 지원해 VM 이미지를 여러 호스트가 나눠 쓴다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).
- **하드웨어 아키텍처.** RHEL 9의 일부로 쓸 때 64비트 AMD·Intel·ARM 아키텍처와 IBM z13 이상 시스템에서 지원된다 (2026-09 기준) (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

관리 도구는 [[concepts/hypervisor|하이퍼바이저]] 쪽에 정리해 뒀다. libvirt·virsh, virt-manager, Cockpit, 그리고 쿠버네티스용 KubeVirt다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

## 모순 — KVM은 타입 1 하이퍼바이저인가

**이 질문에 자료들이 서로 다르게 답한다.** 어느 한쪽으로 정리하지 않고 세 입장을 모두 남긴다.

| 자료 | 무엇이라 말하나 |
|---|---|
| [[sources/aws-what-is-virtualization\|#35 AWS 가상화 개요]] | "KVM은 **타입 1 하이퍼바이저를 사용해** 리눅스 운영체제 위에서 여러 VM을 호스팅한다"고 단정한다 |
| [[sources/oracle-virtualization-explained\|#36 오라클 가상화 해설]] | KVM을 "리눅스 시스템을 **타입 1(베어메탈) 하이퍼바이저로 바꾸는**" 기술로 규정한다 |
| [[sources/redhat-what-is-kvm\|#37 레드햇 KVM]] | "리눅스가 **하이퍼바이저로 동작할 수 있다**"고만 쓰고, 타입 1인지 2인지는 문서 어디에도 적지 않는다 |
| [[sources/wikipedia-virtualization-foundations\|#40 위키백과 가상화 기초]] | "두 타입의 구분이 **늘 명확하지는 않다**"며 KVM을 그 사례로 든다. 커널 모듈이 호스트 OS를 사실상 타입 1로 바꾼다는 서술이다 |
| [[sources/kernel-kvm-docs\|#42 KVM 커널 문서]] | 타입 개념 자체가 등장하지 않는다 |

무엇이 쟁점인지는 분명하다. KVM은 완전한 범용 OS인 리눅스의 **일부**로 올라가므로 타입 2처럼 보이지만, 커널 모듈이라 하드웨어에 직접 닿으므로 타입 1처럼 동작한다.

> 이 위키는 어느 쪽이 맞다고 적지 않는다. 벤더 문서 두 곳이 "타입 1"이라 단정하고, 벤더 문서 한 곳이 답을 피하며, 1차 자료인 커널 문서에는 질문 자체가 없다 — 이 배치 자체가 기록할 가치가 있다. 타입 분류의 일반론은 [[concepts/hypervisor|하이퍼바이저]]를 보면 된다.

## 이 위키에서의 등장

- **리눅스 가상화의 기본값** — 벤더 문서 넷이 모두 KVM을 리눅스 쪽 표준 구현으로 언급한다 ([[concepts/virtualization|가상화]])
- **타입 분류 논쟁의 사례** — 타입 1·2 구분이 흐려지는 대표 사례로 인용된다 ([[concepts/hypervisor|하이퍼바이저]])
- **마이크로VM의 토대** — 파이어크래커가 KVM 위에서 vCPU 스레드를 돌린다 ([[analysis/vm-vs-container|가상 머신 vs 컨테이너]])
- **컨테이너 세계와의 접점** — KubeVirt가 KVM 기반 VM을 쿠버네티스 안으로 끌어들인다 ([[concepts/kubernetes|쿠버네티스]])

## 함께 읽기

- [[concepts/hypervisor|하이퍼바이저]] — 타입 분류와 관리 도구의 일반론
- [[entities/qemu|QEMU]] — KVM의 유저스페이스 짝
- [[entities/xen|Xen]] — 다른 길로 x86 문제를 푼 하이퍼바이저
- [[concepts/virtualization-internals|가상화 작동 원리]] — KVM이 전제하는 하드웨어 보조가 무엇인지

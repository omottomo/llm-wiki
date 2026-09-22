---
title: "위키백과 가상화 기초 문서 묶음 (7편)"
label: "#40 위키백과 가상화 기초"
type: source
credibility: medium
volatility: warm
created: 2026-09-22
updated: 2026-09-22
sources: [wikipedia-virtualization-foundations]
tags: [가상화, 하이퍼바이저, 반가상화, 기초개념]
---

# 위키백과 가상화 기초 문서 묶음 (7편)

## 한 줄 요약

영문 위키백과 7편을 한 파일로 묶은 자료다. 포펙·골드버그 요건, x86 가상화, 하이퍼바이저, 반가상화, OS 수준 가상화, CP/CMS, Xen을 담아 [[concepts/virtualization-internals|가상화 작동 원리]]의 뼈대가 됐다.

## 핵심 내용

- **포펙·골드버그 1974.** VMM이 갖춰야 할 세 성질(동등성·자원 제어·효율성)과, 명령어를 특권·제어 민감·동작 민감으로 나눈 분류를 싣는다. 정리 1은 "민감 명령 집합이 특권 명령 집합의 부분집합이면 효과적 VMM을 만들 수 있다"이며, 이것이 trap-and-emulate 방식의 근거다.
- **x86 가상화.** 소프트웨어 시절의 세 기법(바이너리 변환·섀도 페이지 테이블·장치 에뮬레이션)과 ring deprivileging, 그리고 2005~2006년 Intel VT-x·AMD-V 도입 이후를 정리한다.
- **하이퍼바이저.** 용어의 유래, 골드버그의 1973년 타입 1·2 분류, IBM 메인프레임 기원, 그리고 **두 타입의 구분이 늘 명확하지는 않다**는 단서를 담는다.
- **반가상화.** 게스트 OS를 포팅해야 한다는 조건, Denali에서 용어가 처음 쓰인 내력, 리눅스 메인라인에 들어간 pv-ops를 다룬다.
- **OS 수준 가상화.** 컨테이너가 커널을 공유한다는 점, 네임스페이스와 cgroups라는 리눅스 기반, 그리고 호스트와 다른 커널은 못 돌린다는 한계를 적는다.
- **CP/CMS.** 1960년대 IBM 케임브리지 과학센터의 CP-40·CP-67, 그리고 VM/370으로 이어지는 계보를 상세히 기록한다.
- **Xen.** 케임브리지 대학에서 출발한 내력, dom0·domU 구조, PV부터 PVH까지 다섯 가지 게스트 실행 방식을 정리한다.

## 주요 주장 / 데이터

- **IA-32 민감·비특권 명령 18개.** 펜티엄의 IA-32 명령어 집합에 "민감하지만 특권이 아닌" 명령이 18개 있다고 적고, 민감 레지스터 계열(SGDT·SIDT·SLDT·SMSW·PUSHF·POPF)과 보호 시스템 계열(LAR·LSL·VERR·VERW·POP·PUSH·CALL FAR·JMP FAR·INT n·RETF·STR·세그먼트 레지스터 MOV)로 묶는다.
- **아키텍처별 대조표.** System/370과 PowerPC는 민감 명령이 모두 특권이라 요건을 충족하고, PDP-10과 MC68000은 각각 몇 개·한 개의 예외를 갖는다.
- **VMX 명령 13개** — VMPTRLD, VMPTRST, VMCLEAR, VMREAD, VMWRITE, VMCALL, VMLAUNCH, VMRESUME, VMXOFF, VMXON, INVEPT, INVVPID, VMFUNC. AMD-V 쪽 명령은 VMRUN·VMLOAD·VMSAVE·CLGI·VMMCALL·INVLPGA·SKINIT·STGI로 따로 적는다.
- **MMU 가상화의 세대 교체.** AMD가 Opteron Family 0x10 Barcelona 계열부터 RVI(개발 중 이름은 Nested Page Tables)를 넣었고, Intel이 나중에 이를 EPT로 채택해 2008년 Nehalem부터 포함했다고 적는다.
- **중첩 가상화.** VMCS는 VM마다 정확히 하나씩 존재하는 메모리 자료구조이며, VMM을 겹쳐 쓰면 섀도 페이지 테이블 때와 비슷한 문제가 생긴다. Intel은 Haswell(2013년 발표)부터 VMCS 섀도잉을 하드웨어로 지원한다.
- **SR-IOV 성능.** NASA의 가상화 데이터센터와 아마존 퍼블릭 클라우드에서 베어메탈 네트워크 대역폭의 95% 이상을 달성했다고 적는다.
- **메인프레임의 성능 대가.** 요건을 형식적으로 충족하는 System/370에서도 어떤 벤치마크는 네이티브의 21%까지 떨어졌고, IBM은 하드웨어 어시스트를 넣어 성능을 대략 두 배로 올렸다. 후기 모델에는 어시스트가 100개를 넘었다.
- **Xen 라이브 마이그레이션.** LAN을 통해 메모리를 반복 복사하고, 마지막 동기화에 60~300ms의 정지만 든다.

## 기존 위키와의 연결

- 강화: [[concepts/virtualization-internals|가상화 작동 원리]] 전체가 이 묶음에 크게 기댄다. 다만 반가상화 세부는 1차 자료인 [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]에서 확인한 것만 실었다.
- 강화: [[concepts/virtualization|가상화]]의 탄생 배경. CP/CMS 문서가 [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]의 연대기를 훨씬 상세하게 받쳐 준다.
- 모순: [[entities/kvm|KVM]]의 타입 분류. 이 자료는 "KVM과 bhyve는 커널 모듈이라 호스트 OS를 사실상 타입 1 하이퍼바이저로 바꾼다"고 적고 구분 자체가 흐릿하다고 본다. [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]·[[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]의 단정과 충돌하므로 양쪽을 보존했다.
- 모순: [[sources/geeksforgeeks-virtualization-types|#38 GfG 가상화 유형]]의 "가상화 이전에는 OS 하나" 서술. CP-40 기록이 이를 반박한다.
- 신규: [[entities/xen|Xen]]·[[entities/qemu|QEMU]] 엔티티 페이지, [[concepts/virtualization-internals|가상화 작동 원리]] 개념 페이지가 이 자료로 생겼다.

## 외부 검증 (2026-09-22, 웹)

- **묶음 안에서 날짜가 어긋나는 곳이 있다.** Intel VT-x 첫 출시일을 "x86 virtualization" 문서는 2005-11-14로, "Virtualization" 문서는 2005-11-13으로 적는다. 프로세서 모델(Pentium 4 662·672)은 같다. [[concepts/virtualization-internals|가상화 작동 원리]]에는 더 상세한 x86 전용 문서 쪽 날짜를 쓰고 불일치를 본문에 밝혀 뒀다.
- **명령 18개라는 수는 그대로 쓰되 단서를 붙였다.** 집계 기준에 따라 다른 수로 인용되는 사안이라, 개수 자체보다 "민감하지만 비특권인 명령이 존재한다"는 사실이 요점임을 본문에 적었다.
- **2차 자료라는 점을 감안했다.** 원문 파일 머리말이 스스로 밝힌 방침대로, 여기서 얻은 사실 중 [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]]·[[sources/kernel-kvm-docs|#42 KVM 커널 문서]]·[[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]]로 교차 확인되는 것을 우선했다.

## 출처 정보

- raw: raw/wikipedia-virtualization-foundations.md
- URL: https://en.wikipedia.org/wiki/Popek_and_Goldberg_virtualization_requirements (외 6편 — X86 virtualization, Hypervisor, Paravirtualization, OS-level virtualization, CP/CMS, Xen)
- 저자/발행처: 영문 위키백과 기여자 (CC BY-SA 4.0)
- 수집일: 2026-09-22
- 범위: 7편 본문 텍스트. 각주 번호·편집 링크·사이드바가 일부 남아 있어 인용 시 원문 확인이 필요하다.

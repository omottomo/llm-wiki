---
title: "KVM API 공식 문서 (리눅스 커널)"
label: "#42 KVM 커널 문서"
type: source
credibility: high
volatility: hot
created: 2026-09-22
updated: 2026-09-22
sources: [kernel-kvm-docs]
tags: [KVM, 리눅스, 공식문서, 가상화]
---

# KVM API 공식 문서 (리눅스 커널)

## 한 줄 요약

리눅스 커널 공식 문서의 KVM API 레퍼런스다. [[entities/kvm|KVM]]을 쓴다는 것이 결국 **파일 디스크립터에 ioctl을 거는 일**임을 보여 주는 1차 자료다.

## 핵심 내용

- **API의 모양.** KVM API는 여러 종류의 파일 디스크립터와 그에 거는 ioctl을 중심으로 돌아간다. `/dev/kvm`을 여는 것이 출발점이다.
- **계층이 위에서 아래로 열린다.** `/dev/kvm` 핸들에 `KVM_CREATE_VM`을 걸면 VM 파일 디스크립터가 나오고, VM fd에 `KVM_CREATE_VCPU`나 `KVM_CREATE_DEVICE`를 걸면 가상 CPU나 장치의 fd가 나온다.
- **ioctl은 어느 fd에 거느냐로 갈린다** — system(하위 시스템 전체 속성 + VM 생성), VM(메모리 배치 등 VM 전체 + vcpu·장치 생성), vcpu(가상 CPU 하나의 동작), device(장치 하나의 동작).
- **발행 주체에 제약이 있다.** VM ioctl은 그 VM을 만든 **같은 프로세스**에서 걸어야 하고, vcpu ioctl은 그 vcpu를 만든 **같은 스레드**에서 거는 것이 원칙이다. 스레드를 바꾸면 첫 ioctl에서 성능 손해를 볼 수 있다.
- **`KVM_RUN`이 게스트를 굴린다.** vcpu ioctl이며 명시적 인자가 없다. 대신 vcpu fd를 오프셋 0에서 mmap한 `struct kvm_run`이 암묵적 인자 블록 노릇을 한다.
- **확장 메커니즘.** 커널 버전 번호 대신 `KVM_CAP_*` 확장 식별자를 두고, `KVM_CHECK_EXTENSION`으로 있는지 물어 본 뒤 쓴다.

## 주요 주장 / 데이터

- **ABI 안정화 시점.** 리눅스 2.6.22부터 KVM ABI가 안정화됐고, 이후 하위 호환을 깨는 변경은 허용되지 않는다.
- **API 버전은 12로 고정.** `KVM_GET_API_VERSION`은 상수 12를 돌려준다. 다른 값이 나오면 애플리케이션은 실행을 거부해야 한다. 2.6.20·2.6.21은 그 이전 값을 보고하지만 문서화도 지원도 되지 않는다.
- **fd를 프로세스 사이로 옮기는 재주는 지원하지 않는다.** `fork()`나 유닉스 도메인 소켓의 `SCM_RIGHTS`로 옮겨도 호스트가 망가지지는 않지만 동작이 보장되지 않는다.
- **VM의 수명은 만든 프로세스가 아니라 fd 참조에 묶인다.** 마지막 참조가 풀릴 때까지 VM과 그 자원은 해제되지 않으므로, 생각 없이 `fork()`·`dup()`으로 참조를 늘리는 것은 강하게 권장되지 않는다.
- **아키텍처마다 다른 조건.** MIPS는 기본 구현이 trap & emulate이고 하드웨어 보조(VZ ASE)는 따로 골라야 한다. ARM64는 VM의 물리 주소 크기가 기본 40비트로 제한된다.
- **vCPU 개수의 상한**은 `KVM_CAP_NR_VCPUS`·`KVM_CAP_MAX_VCPUS`로 런타임에 물어 본다. 전자가 없으면 최대 4개로 가정하라고 적는다.

## 기존 위키와의 연결

- 강화: [[entities/kvm|KVM]]의 ioctl 3계층 서술 전체. 벤더 해설이 "VM이 리눅스 프로세스"라고 말하는 대목을, 이 문서는 실제 시스템 콜 수준에서 보여 준다.
- 강화: [[analysis/vm-vs-container|가상 머신 vs 컨테이너]]의 마이크로VM 대목. [[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]]가 말하는 "vCPU 스레드가 `KVM_RUN` 메인 루프를 돈다"는 설계가 이 문서의 API와 정확히 맞물린다.
- 강화: [[concepts/virtualization-internals|가상화 작동 원리]]의 trap-and-emulate 절. MIPS의 기본 구현을 "trap & emulate"라 부르는 것이 그 방식이 여전히 실무 용어임을 보여 준다.
- 모순: 직접 모순 없음. 다만 이 문서는 KVM을 타입 1·2 어느 쪽으로도 분류하지 않는다 — 커널 문서에 그 구분 자체가 등장하지 않는다는 점이 [[entities/kvm|KVM]]의 분류 논쟁을 이해하는 단서다.
- 신규: `/dev/kvm` ioctl 계층 구조가 이 자료로 위키에 처음 들어왔다.

## 외부 검증 (2026-09-22, 웹)

- **이 문서에는 하이퍼바이저 "타입" 개념이 없다.** [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]·[[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]이 단정하는 타입 1 분류는 1차 자료에서 확인되지 않는다. 그래서 [[entities/kvm|KVM]]에서는 이를 벤더의 분류로 표시하고 양쪽을 보존했다.
- 발췌 범위가 앞부분 약 2만 2천 자라, 개별 ioctl 레퍼런스 대부분은 위키에 반영돼 있지 않다.

## 출처 정보

- raw: raw/kernel-kvm-docs.md
- URL: https://docs.kernel.org/virt/kvm/api.html
- 저자/발행처: 리눅스 커널 개발 커뮤니티 (docs.kernel.org, 문서 버전 7.3.0-rc4 표기)
- 수집일: 2026-09-22
- 범위: API 총론·ioctl 계층·vCPU 생성과 `KVM_RUN` 부근 발췌. 개별 ioctl 레퍼런스 전문은 제외했다.

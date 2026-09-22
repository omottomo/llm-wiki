---
title: 하이퍼바이저 (Hypervisor)
type: concept
created: 2026-09-22
updated: 2026-09-22
sources: [aws-what-is-virtualization, oracle-virtualization-explained, ibm-what-is-virtualization, redhat-what-is-kvm, geeksforgeeks-virtualization-types, wikipedia-virtualization-foundations]
aliases: [hypervisor, VMM, virtual machine monitor]
tags: [하이퍼바이저, 가상화, 기초개념]
---

# 하이퍼바이저 (Hypervisor)

## 한눈에 요약

- 물리 컴퓨터 한 대의 자원을 여러 가상 머신에 나눠 주고, 서로 간섭하지 못하게 막는 소프트웨어 계층이다. 가상 머신 모니터(VMM)라고도 부른다.
- 하드웨어에 직접 올라가는 타입 1과, 기존 운영체제 위에 앱처럼 올라가는 타입 2로 나뉜다.
- 자원을 쥔 쪽이 호스트, 그 자원을 빌려 쓰는 가상 머신이 게스트다.
- 타입 구분은 교과서만큼 깔끔하지 않다. 커널 모듈로 구현된 것들이 경계에 걸쳐 있다.

## 하는 일 — 나눠 주고, 막는다

왜 이런 계층이 필요한지부터 보면 이해가 빠르다. 물리 머신 한 대 위에서 운영체제 여러 개가 각자 "내가 이 기계의 주인"이라고 믿으며 돌아야 하기 때문이다. 누군가는 중간에서 자원을 배분하고 서로의 영역을 지켜 줘야 한다.

그 일을 맡는 것이 하이퍼바이저다. 처리 능력·메모리·스토리지 같은 자원을 모아 두고 VM들에 다시 나눠 주며, 각 VM이 할당받은 자원을 확실히 받고 다른 VM의 동작을 방해하지 않도록 보장한다 (→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]·[[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

여기서 용어를 정리해 두자. 자원을 제공하는 물리 하드웨어 쪽이 **호스트**, 그 자원을 쓰는 VM들이 **게스트**다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]·[[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

## 요청이 흐르는 순서

동작은 중개에 가깝다. VM이 연산 능력 같은 자원을 필요로 하면 요청이 먼저 하이퍼바이저로 간다. 하이퍼바이저가 그 요청을 하부 하드웨어로 넘기고, 하드웨어가 실제 작업을 수행한다 (→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]).

오라클 문서는 여기에 한 가지를 덧붙인다. 하이퍼바이저는 요청을 물리 시스템에 넘기면서 변경 사항을 캐시에 저장하고, 이 전 과정이 네이티브에 가까운 속도로 일어난다는 것이다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

> 다만 "네이티브에 가까운 속도"는 조건부다. 하드웨어 보조 없이 소프트웨어만으로 이를 해내려면 상당한 우회가 필요했고, 그 사정은 [[concepts/virtualization-internals|가상화 작동 원리]]에서 다룬다.

하이퍼바이저에는 OS 수준 부품도 필요하다. VM을 돌리려면 메모리 관리자, 프로세스 스케줄러, I/O 스택, 디바이스 드라이버, 보안 관리자, 네트워크 스택 같은 것이 있어야 하기 때문이다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

한마디로 하이퍼바이저는 운영체제가 하는 일의 상당 부분을 어떤 식으로든 갖춰야 한다. 이 사실이 다음 절의 타입 구분을 이해하는 열쇠다.

## 타입 1과 타입 2

이 분류는 1973년 로버트 골드버그의 학위 논문 『Architectural Principles for Virtual Computer Systems』에서 나왔다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

| 축 | 타입 1 (베어메탈·네이티브) | 타입 2 (호스티드) |
|---|---|---|
| 설치 위치 | 호스트 하드웨어에 직접. 호스트 OS가 없다 | 기존 OS 위에 일반 프로그램처럼 |
| 자원 경로 | 하이퍼바이저가 하드웨어에 직접 스케줄링 | 호스트 OS를 거쳐 하드웨어에 도달 |
| 성능 | 높다. 물리 자원과 직접 상호작용한다 | 낮다. 호스트 OS를 경유하는 오버헤드를 진다 |
| 주 쓰임새 | 기업 데이터센터, 클라우드 사업자 | 개인용, 테스트 랩, 엔드유저 컴퓨팅 |
| 예 | Hyper-V, [[entities/xen\|Xen]], VMware ESXi | VirtualBox, VMware Workstation |

(→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]·[[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]·[[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]·[[sources/geeksforgeeks-virtualization-types|#38 GfG 가상화 유형]]·[[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]])

IBM은 타입 1을 "전통적 운영체제를 통째로 대체하는" 것으로 설명한다. 타입 2가 성능 오버헤드를 지는 이유는 "하드웨어에 접근·조율하려면 호스트 OS를 써야 하기 때문"이라고 못 박는다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]).

역사적으로 IBM이 1960년대에 만든 최초의 하이퍼바이저들은 모두 네이티브, 즉 타입 1이었다. 시험 소프트웨어 SIMMON과 CP/CMS가 그것이다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

### 구분이 흐려지는 자리

여기서 헷갈리기 쉬운데, 두 타입의 경계는 생각만큼 선명하지 않다.

위키백과는 "이 두 타입의 구분이 늘 명확하지는 않다"고 명시하고, [[entities/kvm|KVM]]과 bhyve를 예로 든다. 둘 다 커널 모듈이며, 호스트 운영체제를 사실상 타입 1 하이퍼바이저로 바꿔 놓는다는 것이다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

마이크로커널 문맥에서는 용어를 아예 다르게 쓰기도 한다. 커널 공간 기능을 하이퍼바이저, 유저 공간 기능을 VMM이라 갈라 부르는 방식이다. 이 어법을 리눅스에 적용하면 KVM이 하이퍼바이저이고 [[entities/qemu|QEMU]]는 KVM을 쓰는 VMM이 된다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

> 그래서 "이건 타입 몇인가"라는 질문은 때로 답이 하나가 아니다. 실제로 KVM을 두고 벤더 문서들의 서술이 갈리는데, 그 논쟁은 [[entities/kvm|KVM]]에 모순으로 기록해 뒀다.

## 관리 도구

하이퍼바이저를 골랐다고 끝이 아니다. VM이 여러 대가 되는 순간 관리 도구가 필요해진다. 리눅스·KVM 계열에서 흔히 쓰는 것은 넷이다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).

| 도구 | 성격 | 쓰임 |
|---|---|---|
| libvirt · virsh | API + 명령줄 | libvirt는 가상화 플랫폼 관리 API를 제공하고, virsh는 그 위의 CLI로 VM을 만들고 시작·조회·정지한다 |
| virt-manager | 데스크톱 GUI | 주요 리눅스 배포판에서 쓸 수 있는 VM 데스크톱 인터페이스 |
| Cockpit | 웹 콘솔 | 웹 인터페이스로 VM을 관리한다 |
| KubeVirt | 쿠버네티스 통합 | 쿠버네티스 환경에서 대규모 VM을 컨테이너 앱과 나란히 관리한다 |

마지막 항목이 흥미롭다. KubeVirt는 VM을 [[concepts/kubernetes|쿠버네티스]] 안으로 끌어들여, 컨테이너와 VM을 한 플랫폼에서 다루게 한다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]). 두 세계가 갈라진 채로 남지 않고 다시 합류하는 지점인 셈이다.

## 함께 읽기

- [[concepts/virtualization|가상화]] — 이 계층이 무엇을 위해 존재하는지의 큰 그림
- [[concepts/virtualization-internals|가상화 작동 원리]] — 하이퍼바이저가 실제로 무슨 수를 쓰는지
- [[entities/kvm|KVM]] — 리눅스 커널 자체를 하이퍼바이저로 만드는 구현
- [[entities/xen|Xen]] — 반가상화로 x86 문제를 우회한 타입 1 하이퍼바이저
- [[concepts/kubernetes|쿠버네티스]] — KubeVirt가 VM을 끌어들이는 대상 플랫폼

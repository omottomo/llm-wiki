---
title: 가상화 (Virtualization)
type: concept
created: 2026-09-22
updated: 2026-09-22
sources: [aws-what-is-virtualization, oracle-virtualization-explained, ibm-what-is-virtualization, geeksforgeeks-virtualization-types, wikipedia-virtualization-foundations, redhat-what-is-kvm]
aliases: [virtualization, 서버가상화]
tags: [가상화, 하이퍼바이저, 클라우드, 기초개념]
---

# 가상화 (Virtualization)

## 한눈에 요약

- 컴퓨터 한 대의 자원을 소프트웨어로 갈라, 서로 독립된 여러 대인 것처럼 쓰는 기술이다. 갈라진 각 조각을 가상 머신(VM)이라 부르며, 저마다 자기 운영체제를 돌린다.
- 1960년대 IBM 메인프레임에서 시작했고, 1990년대 말 x86 서버가 놀고 있다는 문제를 풀면서 다시 주류가 됐다.
- 서버만의 이야기가 아니다. 스토리지·네트워크·데이터·애플리케이션·데스크톱까지 같은 발상이 퍼져 있다.
- 공짜는 아니다. 리소스 경합, VM 스프롤, 라이선스 관리가 실제 운영에서 따라온다.

## 어디서 시작했나 — 1960년대 메인프레임

먼저 짚어야 할 오해가 하나 있다. 가상화는 클라우드 시대에 발명된 기술이 아니다.

IBM은 1964년 System/360용 시분할 연구 프로젝트로 **CP-40**을 시작했다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]). 이 시스템은 1967년 1월 생산 사용에 들어갔고, 동적 주소 변환을 지원하도록 개조한 S/360-40 위에서 돌았다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

무엇이 새로웠나. 그 전까지 하드웨어는 여러 **사용자 애플리케이션**을 동시에 돌리는 수준까지만 가상화됐다. CP-40은 하드웨어의 **supervisor 상태까지** 가상화해, 여러 운영체제가 각자의 가상 머신 문맥에서 동시에 돌 수 있게 했다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

뒤이어 S/360-67용으로 다시 구현한 것이 CP-67이고, 1972년 IBM은 System/370용 첫 공식 가상 머신 제품 **VM/370**을 발표했다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]·[[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

> 두 자료의 연도가 다르게 보이지만 모순은 아니다. 1964년은 프로젝트 착수, 1967년은 생산 사용 개시를 가리킨다. 반대로 [[sources/geeksforgeeks-virtualization-types|#38 GfG 가상화 유형]]이 "가상화 이전에는 서버 한 대가 OS 하나만 돌렸다"고 적은 것은 이 계보와 어긋나는 오류다.

## x86에서 왜 다시 필요해졌나

메인프레임에서 잘 굴러가던 기술이 1990년대 말 다시 불려 나온 데는 아주 현실적인 이유가 있었다.

가상화 이전 관행은 "앱 하나에 서버 한 대"였다. 신뢰성 때문에 택한 방식이었지만, 그 결과 물리 서버 대부분이 활용도가 낮은 채로 놀았다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]).

이 낭비가 얼마나 우스운지는 예를 들면 분명해진다. 이메일은 윈도우와 큰 저장 공간이, 고객용 앱은 리눅스와 높은 처리 성능이, 사내 앱은 큰 메모리가 필요하다. 요구가 다르다는 이유로 서버를 세 대 사면, 유지비는 100% 내면서 저장·처리 용량은 일부만 쓰게 된다 (→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]).

쉽게 말하면 **서버 통합**이 동기였다. 서버 한 대당 연산 능력이 커지고 네트워크 대역폭이 늘면서, 여러 대에 흩어져 놀던 연산을 한 대로 모으는 일이 비용상 합리적이 됐다 (→ [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]).

x86에서 이를 해내는 일이 기술적으로 왜 까다로웠는지는 [[concepts/virtualization-internals|가상화 작동 원리]]에서 따로 다룬다.

## 정의와 구성요소

정의부터 보자. 가상화는 전용 소프트웨어로 컴퓨트·스토리지·네트워크 자원을 분리해, 하드웨어를 공유하면서도 각자 OS와 앱을 돌리는 여러 워크로드에 나눠 주는 기술이다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

등장인물은 셋뿐이다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]).

| 구성요소 | 무엇인가 |
|---|---|
| 물리 머신 | CPU·메모리·스토리지·네트워크를 제공하는 실제 하드웨어. **호스트**라 부른다 |
| 가상 머신(VM) | 소프트웨어로 흉내 낸 컴퓨터. 자기 OS와 앱을 돌린다. **게스트**라 부른다 |
| [[concepts/hypervisor\|하이퍼바이저]] | 둘 사이에서 자원을 나눠 주고 서로 간섭하지 못하게 막는 계층 |

VM은 보통 설정·가상 하드디스크 등 몇 개의 파일로 이뤄진다. 파일이니까 시작·정지·복사·이전이 전부 소프트웨어 조작이 된다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]·[[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

## 무엇이 좋아지나

이점은 벤더마다 말이 조금씩 다르지만 겹치는 부분이 분명하다.

- **자원 효율.** 서버 한 대에 워크로드를 모아 활용도를 끌어올린다. 물리 서버가 줄면 전력·발전기·냉방 비용도 함께 준다 (→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]·[[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).
- **빠른 프로비저닝.** 하드웨어가 이미 있으면 VM을 띄우는 일은 수 분이 아니라 수 초로 줄고, 자동화도 쉽다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]·[[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).
- **재해 복구.** 물리 서버를 교체·수리하려면 수 시간에서 수 일이 걸리지만, 가상 환경에서는 수 분이면 끝난다 (→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]).
- **격리.** VM 하나가 망가지거나 침해당해도 다른 VM과 호스트는 영향을 받지 않는다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]·[[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).
- **레거시 지원.** 내 OS용으로 나오지 않은 소프트웨어를, 구형 OS를 VM에 띄워 최신 하드웨어에서 계속 쓴다 (→ [[sources/redhat-what-is-kvm|#37 레드햇 KVM]]).
- **스냅샷과 롤백.** 감염된 VM을 깨끗했던 시점으로 되돌릴 수 있다. 비가상화 OS는 악성코드가 핵심 구성요소에 깊이 박히면 되돌리기 어렵다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]).

## 가상화의 종류

서버만 가상화되는 것이 아니다. "물리 자원을 추상화해 소프트웨어로 다룬다"는 같은 발상이 계층마다 반복된다.

| 종류 | 무엇을 가른다 | 특징 |
|---|---|---|
| 서버 | 물리 서버 한 대를 여러 가상 서버로 | 가장 흔한 형태. 서버 통합의 주역 |
| 데스크톱 | 데스크톱 환경을 중앙 서버에 | 원격 서버에서 돌리는 VDI와, 내 PC에서 돌리는 로컬 방식으로 갈린다 |
| 스토리지 | 여러 물리 저장 장치를 하나의 풀로 | 벤더·종류가 달라도 한 덩이로 묶어 관리 소프트웨어로 할당한다 |
| 네트워크 | 스위치·라우터·방화벽을 소프트웨어로 | **SDN**은 라우팅 제어를 떼어내고, **NFV**는 방화벽·로드밸런서 같은 기능을 소프트웨어로 옮긴다 |
| 데이터 | 흩어진 데이터 소스를 하나의 논리적 뷰로 | 데이터를 옮기거나 복제하지 않고 원래 자리에 둔 채 통합한다. 데이터 페더레이션이라고도 한다 |
| 애플리케이션 | 앱을 그 앱용 OS에서 떼어내 | 스트리밍·서버 기반·로컬 세 방식이 있다 |

(→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]·[[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]·[[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]·[[sources/geeksforgeeks-virtualization-types|#38 GfG 가상화 유형]])

IBM은 여기에 데이터센터·CPU·GPU·리눅스·클라우드를 더해 열 갈래로 쪼갠다. 특히 **CPU 가상화**를 하이퍼바이저와 VM을 가능하게 하는 근본 기술로 꼽고, 처음에는 전적으로 소프트웨어였다가 오늘날 프로세서의 확장 명령어 집합으로 옮겨 갔다고 짚는다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]).

**GPU 가상화**는 두 갈래다. 패스스루는 GPU 전체를 게스트 OS 하나에 통째로 주고, 공유 vGPU는 물리 GPU 코어를 여러 가상 GPU로 나눈다 (→ [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]]).

## 운영상 과제 — 공짜가 아니다

이점만 나열하면 실제 운영에서 걸리는 대목을 놓친다. 오라클 문서는 드물게 대가도 함께 적는데, 그중 셋이 특히 자주 부딪히는 문제다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

**리소스 경합.** 같은 호스트를 공유하는 VM들이 CPU·메모리·스토리지를 두고 다투면 성능 문제가 생긴다. 상시 모니터링과 동적 자원 할당으로 완화한다.

**VM 스프롤.** VM을 만들기 쉬운 것이 곧 문제가 된다. 통제 없이 늘어난 VM이 관리 불가능한 규모가 되기 때문이다. 프로비저닝 정책을 세우고 안 쓰는 VM을 주기적으로 감사해 지우는 것이 정석이다.

**라이선스와 컴플라이언스.** 가상 환경의 라이선스 관리는 헷갈리고 비싸지기 쉽다. 자산을 모두 추적하고 라이선스 조건을 검토하며 정기적으로 준수 여부를 점검해야 한다.

> 나머지 넷은 이렇다. 하이퍼바이저 취약점에서 오는 **보안 위험**, 도구가 맞지 않아 생기는 **백업·복구 복잡성**. 그리고 규모가 커질 때의 **관리 복잡성**, 트래픽 증가로 인한 **네트워크 병목** (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

## 클라우드와는 어떤 관계인가

둘을 같은 말로 쓰는 경우가 많은데, 층이 다르다고 보면 된다.

가상화는 **기술**이고 클라우드는 그 위에 세운 **서비스**다. 클라우드 사업자가 데이터센터를 갖추고 하부 하드웨어 위에 가상 환경을 만든 뒤, API로 그 자원을 빌려 주는 것이 클라우드다 (→ [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]]·[[sources/geeksforgeeks-virtualization-types|#38 GfG 가상화 유형]]).

소유 관계도 갈린다. 가상화만 하면 하드웨어는 보통 내가 갖고 관리하지만, 클라우드에서는 자원을 빌려 쓰고 하드웨어는 사업자 몫이다 (→ [[sources/geeksforgeeks-virtualization-types|#38 GfG 가상화 유형]]).

실제로 퍼블릭 클라우드든 프라이빗 클라우드든 가상화 위에서 돌아가며, 그 위에 관리·자동화 계층이 얹혀 셀프서비스 프로비저닝을 제공한다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

## 앞으로 — 하드웨어로 내려가는 가상화

(2026-09 기준) 흐름은 세 방향으로 정리된다 (→ [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]]).

**DPU·SmartNIC.** 하이퍼스케일러가 보안·격리·가상 네트워킹 같은 클라우드 기능을 소프트웨어에서 전용 실리콘 카드로 옮긴다. 서버 CPU는 애플리케이션에만 쓰고, 클라우드 기능은 별도 카드가 맡는 구조다.

**베어메탈 서비스.** 가상과 물리의 경계가 흐려진다. 물리 서버에 클라우드 VM의 자동화·프로비저닝·네트워크 통합을 얹어, 가상화 계층의 지연에 민감한 워크로드를 겨냥한다.

**마이크로VM.** 서버리스와 고밀도 컨테이너 환경을 떠받치려고 등장했다. 전통적 VM이 완전한 OS를 요구하고 부팅에 수 분이 걸리는 데 반해, 마이크로VM은 불필요한 것을 모두 걷어내 전통적 VM의 강한 격리를 유지하면서 훨씬 빨리 뜬다. 구체적 수치는 [[analysis/vm-vs-container|가상 머신 vs 컨테이너]]에서 1차 자료로 확인한다.

## 함께 읽기

- [[concepts/hypervisor|하이퍼바이저]] — 가상화를 실제로 해내는 소프트웨어 계층
- [[concepts/virtualization-internals|가상화 작동 원리]] — x86에서 이게 어떻게 가능해졌는지의 내부 사정
- [[analysis/vm-vs-container|가상 머신 vs 컨테이너]] — 격리 수준과 오버헤드를 축으로 한 비교
- [[concepts/kubernetes|쿠버네티스]] — 컨테이너 쪽 세계의 표준 오케스트레이터
- [[concepts/infrastructure-as-code|코드형 인프라]] — 가상화된 자원을 코드로 선언해 다루는 이웃 갈래

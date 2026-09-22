---
title: "Xen과 가상화의 기술 (SOSP 2003 논문)"
label: "#41 Xen 논문 2003"
type: source
credibility: high
volatility: cold
created: 2026-09-22
updated: 2026-09-22
sources: [xen-sosp-2003-paper]
tags: [Xen, 반가상화, 하이퍼바이저, 가상화]
---

# Xen과 가상화의 기술 (SOSP 2003 논문)

## 한 줄 요약

케임브리지 대학 컴퓨터 연구소가 2003년 SOSP에 낸 [[entities/xen|Xen]] 원 논문이다. 게스트 OS를 고쳐 쓰는 **반가상화**로 x86의 가상화 난점을 우회하고, 비가상화 대비 몇 퍼센트 안쪽의 오버헤드를 주장한다.

## 핵심 내용

- **문제 제기.** x86은 애초에 전가상화를 염두에 두고 설계되지 않았다. VMM이 처리해야 할 supervisor 명령을 권한이 모자란 상태에서 실행하면, 편리하게 트랩이 걸리는 대신 **조용히 실패한다**. x86 MMU를 효율적으로 가상화하기도 어렵다.
- **해법.** 하부 하드웨어와 "비슷하지만 똑같지는 않은" 가상 머신 추상화를 제시한다. 게스트 OS는 고쳐야 하지만, ABI는 건드리지 않으므로 게스트 애플리케이션은 수정할 필요가 없다.
- **ring 배치.** x86의 네 권한 링 가운데 OS/2 이후로 ring 1과 2를 쓴 잘 알려진 OS가 없다는 점을 이용한다. 게스트 OS를 **ring 1**로 옮기면 특권 명령을 직접 실행하지 못하면서도 ring 3의 애플리케이션과는 안전하게 갈린다.
- **hypercall과 이벤트.** 도메인에서 Xen으로는 hypercall이라는 동기 소프트웨어 트랩이 올라가고, Xen에서 도메인으로는 비동기 이벤트가 내려간다. 이벤트는 도메인별 비트마스크에 쌓이며 하드웨어 인터럽트를 대신한다.
- **장치 I/O.** 기존 하드웨어를 에뮬레이트하지 않고 깔끔한 장치 추상화를 노출한다. 데이터는 공유 메모리 기반의 비동기 버퍼-디스크립터 링으로 오간다.
- **Domain0.** 부팅 때 만들어지는 이 첫 도메인만 제어 인터페이스를 쓸 수 있고, 관리 소프트웨어를 호스팅한다. 다른 도메인의 생성·종료, 스케줄링 파라미터, 메모리 할당, 디스크·네트워크 접근 권한이 모두 여기서 결정된다.
- **용어 정리.** 실행 중인 VM은 **도메인**, Xen이 호스팅하는 OS는 **게스트 OS**라 부른다. 프로그램과 프로세스의 관계에 빗댄 구분이다.

## 주요 주장 / 데이터

- **설계 목표.** 현대 서버 한 대에 VM 인스턴스를 최대 100개까지 동시에 올리는 것을 겨냥한다.
- **오버헤드.** Linux와 Windows XP를 동시에 호스팅해도 비가상화 대비 "많아야 몇 퍼센트"의 성능 저하에 그친다고 주장한다.
- **포팅 비용** — 수정·추가된 줄 수로 Linux는 2,995줄(x86 코드베이스의 1.36%), Windows XP는 4,620줄(0.04%)이다. XP가 더 든 이유로 페이지 테이블 항목 접근에 구조체·공용체를 두루 쓴 점을 든다.
- **섀도 페이지 테이블을 쓰지 않는다.** VMware가 게스트에게 MMU에 보이지 않는 가상 페이지 테이블을 주고 섀도와 동기화하는 데 반해, Xen은 게스트 OS 페이지 테이블을 MMU에 **직접 등록**하고 읽기 전용으로 묶는다. 갱신은 hypercall로 검증받는다.
- **안전 장치.** 머신 페이지 프레임마다 타입(PD·PT·LDT·GDT·RW)과 참조 카운트를 붙여, 페이지 테이블에 쓰기 가능 매핑이 생기는 일을 원천 차단한다.
- **주소 공간 배치.** Xen은 모든 주소 공간 상단 64MB에 자리 잡아 하이퍼바이저를 드나들 때 TLB를 비우지 않아도 되게 했다.
- **페이지 폴트의 예외.** 시스템 콜은 게스트가 '빠른' 핸들러를 등록해 ring 0을 거치지 않게 할 수 있지만, 페이지 폴트는 CR2 레지스터를 ring 0에서만 읽을 수 있어 반드시 Xen을 거쳐야 한다.

## 기존 위키와의 연결

- 강화: [[concepts/virtualization-internals|가상화 작동 원리]]의 반가상화 절 전체가 이 논문의 1차 진술에 기댄다. 2차 자료의 요약 대신 원문 서술만 실었다.
- 강화: [[entities/xen|Xen]]의 설계·연혁. Domain0, hypercall, 이벤트라는 어휘가 여기서 나왔다.
- 강화: [[concepts/virtualization-internals|가상화 작동 원리]]의 전가상화 절. VMware ESX Server가 게스트 커널 전체를 동적으로 재작성하고 섀도 페이지 테이블을 유지한다는 서술이 바이너리 변환의 대가를 구체적으로 보여 준다.
- 모순: 직접 모순 없음. 다만 [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]가 요약한 반가상화 설명보다 이쪽이 원문이므로, 둘이 어긋날 때는 이 논문을 따랐다.
- 신규: [[entities/xen|Xen]] 엔티티 페이지의 뼈대가 이 자료로 생겼다.

## 외부 검증 (2026-09-22, 웹)

- **합자 손실로 인한 오탈자가 남아 있다.** PDF 텍스트 추출 과정에서 `fi`·`ffi` 같은 합자가 빠져 `sacricing`(sacrificing), `efcient`(efficient), `congurations`(configurations)처럼 보이는 단어가 있다. 저자명 `Andrew Wareld`도 Warfield가 맞다. 위키에는 원문을 옮길 때 이 손실을 복원해 적었다.
- **"게스트 OS를 ring 1로"라는 서술은 원문에서 직접 확인했다.** [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]]도 같은 내용을 32비트 x86 한정으로 적어 두 자료가 일치한다.
- 수집 범위는 앞 6쪽이라, 뒤쪽 성능 평가 수치(벤치마크 표)는 이 위키에 실려 있지 않다.

## 출처 정보

- raw: raw/xen-sosp-2003-paper.md
- URL: https://www.cl.cam.ac.uk/research/srg/netos/papers/2003-xensosp.pdf
- 저자: Paul Barham, Boris Dragovic, Keir Fraser, Steven Hand, Tim Harris, Alex Ho, Rolf Neugebauer, Ian Pratt, Andrew Warfield (University of Cambridge Computer Laboratory)
- 발표: ACM SOSP '03 (2003)
- 수집일: 2026-09-22
- 범위: PDF 앞 6쪽 발췌 — 초록·서론·접근 개요·상세 설계 앞부분. 성능 평가 절은 포함하지 않았다.

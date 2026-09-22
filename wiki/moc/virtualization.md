---
title: 주제 관문 — 가상화
type: overview
created: 2026-09-22
updated: 2026-09-22
sources: []
tags: [관문, 가상화, 하이퍼바이저]
---

# 주제 관문 — 가상화

> 한 대의 기계를 여러 대처럼 쓰는 기술을 모아 둔 관문이다. 1960년대 메인프레임에서 시작해 x86에서 다시 풀어야 했던 문제, 그 해법이 소프트웨어에서 하드웨어로 내려간 과정까지 이어진다.

## 여기서부터
1. [[concepts/virtualization|가상화]] — 무엇이고 왜 생겼는지
2. [[concepts/hypervisor|하이퍼바이저]] — 자원을 나눠 주는 중재자와 타입 1·2
3. [[concepts/virtualization-internals|가상화 작동 원리]] — 작동 원리를 끝까지 파고들 때

## 개념
- [[concepts/virtualization|가상화]] — 하드웨어를 소프트웨어로 갈라 쓰는 기술. 탄생 배경·유형 6가지·운영 과제·앞날(DPU·마이크로VM)
- [[concepts/hypervisor|하이퍼바이저]] — VM에 자원을 나눠 주는 중재자. 타입 1 vs 타입 2, 관리 도구, **구분이 흐려지는 자리**
- [[concepts/virtualization-internals|가상화 작동 원리]] — Popek·Goldberg 3요건부터 trap-and-emulate·바이너리 변환·반가상화·VT-x·EPT·virtio·SR-IOV까지

## 엔티티
- [[entities/kvm|KVM]] — 리눅스 커널을 하이퍼바이저로 만드는 모듈. VM이 리눅스 프로세스, **타입 논쟁 모순** 보존
- [[entities/xen|Xen]] — 반가상화를 대중화한 x86 VMM(2003, 케임브리지). Domain0·하이퍼콜
- [[entities/qemu|QEMU]] — KVM의 유저스페이스 짝. 장치 에뮬레이션과 VM 프로세스를 맡는다(스텁)

## 분석
- [[analysis/vm-vs-container|가상 머신 vs 컨테이너]] — 격리 수준·부팅·오버헤드 비교와 마이크로VM이 메우는 자리

## 출처
- [[sources/aws-what-is-virtualization|#35 AWS 가상화 개요]] — 2026-09-22 흡수, AWS 개념 문서. 가상화 정의·하이퍼바이저 타입·유형 7가지·컨테이너 대비
- [[sources/oracle-virtualization-explained|#36 오라클 가상화 해설]] — 2026-09-22 흡수, 오라클 종합 해설. 운영 과제 7가지·마이그레이션·DPU와 마이크로VM 전망
- [[sources/redhat-what-is-kvm|#37 레드햇 KVM]] — 2026-09-22 흡수, 레드햇 토픽 문서. KVM 연혁·VM은 리눅스 프로세스·sVirt·라이브 마이그레이션·관리 도구
- [[sources/geeksforgeeks-virtualization-types|#38 GfG 가상화 유형]] — 2026-09-22 흡수, 커뮤니티 튜토리얼. 유형 6종 정리. 역사 서술 오류와 범주 오류로 credibility low
- [[sources/ibm-what-is-virtualization|#39 IBM 가상화 개요]] — 2026-09-22 흡수, IBM Think. 1960년대 메인프레임 기원과 x86 재부상 서사
- [[sources/wikipedia-virtualization-foundations|#40 위키백과 가상화 기초]] — 2026-09-22 흡수, 위키백과 7편 묶음. Popek·Goldberg 정리, x86 하드웨어 보조 계보, CP/CMS
- [[sources/xen-sosp-2003-paper|#41 Xen 논문 2003]] — 2026-09-22 흡수, SOSP'03 논문 앞 6쪽. 반가상화 설계 1차 자료(ring 1·하이퍼콜·Domain0)
- [[sources/kernel-kvm-docs|#42 KVM 커널 문서]] — 2026-09-22 흡수, 리눅스 커널 공식 문서 발췌. `/dev/kvm` ioctl 3계층과 vCPU 실행 모델
- [[sources/virtio-and-firecracker-docs|#43 virtio·파이어크래커]] — 2026-09-22 흡수, 커널 virtio 문서 + Firecracker 설계 문서. 반가상 I/O와 마이크로VM 1차 자료

## 함께 보기
- [[moc/infrastructure|인프라와 웹 기술]] — 가상화 위에 올라가는 컨테이너·클러스터
- [[concepts/kubernetes|쿠버네티스]] — 컨테이너 쪽 대비 축

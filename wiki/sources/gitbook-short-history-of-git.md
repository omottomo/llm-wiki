---
title: "Git의 짧은 역사 — Pro Git 1.2"
label: "#45 Pro Git Git 역사"
type: source
credibility: high
volatility: warm
created: 2026-09-22
updated: 2026-09-22
sources: [gitbook-short-history-of-git]
tags: [Git, 리눅스커널, 역사, 오픈소스]
---

# Git의 짧은 역사 — Pro Git 1.2

## 한 줄 요약

리눅스 커널 공동체와 BitKeeper 개발사의 관계가 틀어진 2005년 사건에서 [[entities/git|Git]]이 어떻게 태어났고, 처음부터 어떤 목표를 걸고 설계됐는지를 한 쪽 분량으로 적은 절이다.

## 핵심 내용

- **1991–2002년** — 리눅스 커널 초기에는 변경을 패치와 압축 파일 형태로 주고받으며 보관했다. 버전 관리 도구 없이 굴러간 시기다.
- **2002년** — 리눅스 커널 프로젝트가 독점(proprietary) 분산 버전 관리 도구인 BitKeeper를 쓰기 시작했다.
- **2005년** — 커널 개발 공동체와 BitKeeper를 만든 상용 회사의 관계가 깨지면서 무료 사용권이 철회됐다. 이 일이 커널 공동체, 특히 리눅스를 만든 [[entities/linus-torvalds|Linus Torvalds]]가 BitKeeper를 쓰며 배운 교훈을 바탕으로 자체 도구를 만들게 한 계기가 됐다.
- **설계 목표 다섯 가지** — 속도, 단순한 설계, 비선형 개발(수천 개의 병렬 브랜치)에 대한 강력한 지원, 완전한 분산, 리눅스 커널 같은 대형 프로젝트를 효율적으로(속도와 데이터 크기 양쪽에서) 다룰 것.
- **그 뒤** — 2005년 탄생 이후 Git은 쓰기 쉽게 다듬어지면서도 초기의 이 성질들을 유지했다고 문서는 정리한다.

## 주요 주장 / 데이터

- **"약간의 창조적 파괴와 격렬한 논쟁에서 시작됐다"** — 절의 첫 문장이 Git의 출발을 사고가 아니라 갈등으로 못 박는다.
- **목표 목록 자체가 설계 근거다** — 오늘날 Git의 특징으로 흔히 꼽는 것들(가벼운 브랜치, 로컬 연산 속도, 완전 복제)이 나중에 생긴 장점이 아니라 2005년에 명시적으로 내건 요구사항이었다.
- **"이름의 유래"는 이 절에 없다** — Git이라는 이름의 뜻이나 작명 경위는 원문에 나오지 않는다. 이 자료만으로는 쓸 수 없는 항목이다.

## 기존 위키와의 연결

- 강화: [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]이 설명한 분산 VCS의 장점이 "왜 그렇게 설계됐는가"로 이어진다. 완전 분산은 결과가 아니라 최초 요구사항이었다.
- 모순: 없음.
- 신규: [[entities/git|Git]]·[[entities/linus-torvalds|Linus Torvalds]] 엔티티 페이지 신설.

## 출처 정보

- raw: raw/gitbook-short-history-of-git.md
- 저자/발행처: Scott Chacon, Ben Straub — Pro Git 2nd ed. (Apress, CC BY-NC-SA 3.0)
- 수집일: 2026-09-22
- URL: https://git-scm.com/book/en/v2/Getting-Started-A-Short-History-of-Git
- 범위: 1.2절 본문 전체. 짧은 절이라 잘라낸 부분이 없다.

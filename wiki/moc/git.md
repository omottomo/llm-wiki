---
title: 주제 관문 — Git과 버전 관리
type: overview
created: 2026-09-22
updated: 2026-09-22
sources: []
tags: [관문, Git, 버전관리]
---

# 주제 관문 — Git과 버전 관리

> 파일의 역사를 기록하고 여러 갈래의 작업을 합치는 도구를 모아 둔 관문이다. 원리(객체 모델)를 먼저 잡고, 명령은 비슷한 것끼리 묶어 차이만 본다.

## 여기서부터
1. [[concepts/version-control|버전 관리 시스템]] — 왜 버전 관리가 필요한지
2. [[concepts/git-object-model|Git 동작 원리]] — Git이 무엇을 저장하는지 — 나머지가 여기서 갈린다
3. [[concepts/git-branch-integration|브랜치 합치기]] — 합치기 세 명령의 차이

## 개념
- [[concepts/version-control|버전 관리 시스템]] — 로컬 → 중앙집중(CVCS) → 분산(DVCS) 계보와 분산이 주는 것
- [[concepts/git-object-model|Git 동작 원리]] — 델타가 아닌 스냅샷, 해시 키-값 저장소, blob·tree·commit, refs·HEAD, 세 트리
- [[concepts/git-branch-integration|브랜치 합치기]] — merge·rebase·cherry-pick의 차이와 "푼 커밋은 리베이스하지 않는다"
- [[concepts/git-remote-sync|원격 저장소 동기화]] — clone·fetch·pull·push. pull 기본값을 둘러싼 **공식 문서끼리의 모순** 보존
- [[concepts/git-undo|되돌리기]] — reset 세 단계·revert·restore·switch·stash. 데이터를 실제로 지우는 건 `--hard` 하나

## 엔티티
- [[entities/git|Git]] — 2005년 BitKeeper 사용권 철회에서 태어난 분산 버전 관리 도구
- [[entities/linus-torvalds|Linus Torvalds]] — 리눅스 커널 창시자이자 Git 최초 개발자(스텁)

## 분석
- [[analysis/merge-vs-rebase|merge vs rebase]] — 이력 모양·충돌·되돌리기·공유 안전성 비교, "기록 대 이야기" 양쪽 보존

## 출처
- [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]] — 2026-09-22 흡수, Pro Git 1.1. 로컬·중앙집중·분산 VCS 계보
- [[sources/gitbook-short-history-of-git|#45 Pro Git Git 역사]] — 2026-09-22 흡수, Pro Git 1.2. BitKeeper 사건과 Git 설계 목표 4가지
- [[sources/gitbook-what-is-git|#46 Pro Git Git이란]] — 2026-09-22 흡수, Pro Git 1.3. 스냅샷 모델·세 상태·거의 모든 연산이 로컬
- [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]] — 2026-09-22 흡수, Pro Git 8개 장 묶음. 브랜치·머지·리베이스·리모트·스태시·리셋·객체·레퍼런스
- [[sources/gitscm-docs-git|#48 git 명령 레퍼런스]] — 2026-09-22 흡수, git-scm 공식 매뉴얼. 명령 분류(주요·보조·저수준)와 전역 옵션
- [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]] — 2026-09-22 흡수, 공식 man page 11편 묶음. merge·rebase·fetch·pull·cherry-pick·reset·revert·stash·switch·restore·checkout
- [[sources/kodekloud-how-git-works|#50 KodeKloud Git 내부]] — 2026-09-22 흡수, KodeKloud 블로그. 내부 구조 해설. 상태 서술 2건이 공식 문서와 충돌
- [[sources/tistory-inpa-git-concept|#51 Inpa Git 개념]] — 2026-09-22 흡수, Inpa 블로그. 해시 인덱싱 비유가 좋은 입문. `.git/HEAD` 설명 오류로 credibility low

## 함께 보기
- [[moc/ai-coding-agents|AI 코딩 에이전트]] — 에이전트가 커밋·브랜치를 다루는 방식

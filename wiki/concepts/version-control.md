---
title: 버전 관리 시스템 (VCS)
type: concept
created: 2026-09-22
updated: 2026-09-22
sources: [gitbook-about-version-control, tistory-inpa-git-concept, gitbook-what-is-git, kodekloud-how-git-works]
aliases: [version control system, VCS, 형상관리]
tags: [버전관리, Git, 분산버전관리, 기초개념]
---

# 버전 관리 시스템 (VCS)

## 한눈에 요약

- 파일의 변경을 시간에 따라 기록해 뒀다가 나중에 원하는 시점의 버전을 다시 꺼내는 시스템이다. 소스 코드만이 아니라 이미지나 문서에도 똑같이 쓸 수 있다.
- 구조는 세 세대를 거쳤다. 내 컴퓨터 안에서만 돌던 로컬, 서버 한 대에 모으는 중앙집중식, 저장소를 통째로 복제하는 분산 순이다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).
- 앞 두 세대의 공통 약점은 **역사가 한 곳에만 있다는 것**이었다. 그 한 곳이 죽으면 전부 잃는다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).
- 분산 방식에서는 복제본 하나하나가 완전한 백업이고, 그래서 오프라인에서도 일이 된다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]·[[sources/gitbook-what-is-git|#46 Pro Git Git이란]]).
- [[entities/git|Git]]은 이 세 번째 세대에 속한다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

## 왜 필요한가

정의보다 경험이 빠르다. 레포트를 `report.txt`로 저장했다가 고치면서 `report_final.txt`, 다시 `report_final_final.txt`로 이름을 늘려 본 적이 있을 것이다. 그 복사·백업·저장 행위가 이미 원시적인 버전 관리다 (→ [[sources/tistory-inpa-git-concept|#51 Inpa Git 개념]]).

문제는 이 방식이 **틀리기 쉽다**는 데 있다. 지금 어느 디렉터리에 있는지 잊고 엉뚱한 파일에 쓰거나, 덮을 생각이 없던 파일을 복사로 덮어 버린다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

제대로 된 버전 관리 시스템(Version Control System, 줄여서 VCS)을 쓰면 이게 기능으로 바뀐다. 파일 하나만 이전 상태로 되돌리기, 프로젝트를 통째로 되돌리기, 시간에 따른 변경 비교, 문제를 일으킨 사람과 시점 추적, 잃어버린 파일 복구가 모두 가능해진다. Pro Git은 이걸 "아주 적은 오버헤드로" 얻는다고 표현한다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

## 세 세대 — 로컬·중앙집중식·분산

세 세대는 기술 유행이 아니라 **그 앞 세대가 못 풀던 문제**를 하나씩 풀면서 나왔다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

| 세대 | 대표 | 푼 문제 | 남은 약점 |
|---|---|---|---|
| 로컬 VCS | RCS | 디렉터리 복사의 실수를 DB로 대체 | 내 컴퓨터 밖의 사람과 협업이 안 된다 |
| 중앙집중식(CVCS) | CVS · Subversion · Perforce | 여러 개발자가 한 서버에서 협업 | 서버가 단일 장애점이다 |
| 분산(DVCS) | Git · Mercurial · Darcs | 역사까지 통째로 복제 | (문서가 이 절에서 약점을 따로 들지 않는다) |

### 로컬 VCS

변경분을 담는 간단한 데이터베이스를 두는 방식이다. 대표 도구 RCS는 파일 사이의 차이, 즉 패치 셋(patch set, 변경된 줄만 모아 둔 것)을 특수 형식으로 디스크에 보관한다. 과거 상태가 필요하면 패치를 차례로 더해 그 시점 파일을 재현한다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

### 중앙집중식 VCS

다음 벽은 "다른 컴퓨터의 개발자와 같이 일해야 한다"였다. 그래서 서버 한 대가 모든 버전 파일을 갖고 클라이언트들이 거기서 체크아웃하는 구조가 나왔고, 오랫동안 이게 표준이었다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

장점은 분명하다. 누가 무슨 작업을 하는지 서로 어느 정도 보이고, 관리자가 권한을 세밀하게 통제하기 쉽고, 클라이언트마다 로컬 DB를 관리하는 것보다 운영이 간단하다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

> 문제는 중앙 서버가 곧 단일 장애점이라는 것이다. 한 시간 멈추면 그동안 아무도 협업하거나 버전을 저장하지 못한다. 중앙 DB 디스크가 깨지고 백업이 없으면 프로젝트 역사 전체를 잃는다. 로컬 VCS도 같은 위험을 진다 — 역사가 한 곳에만 있으면 언제나 그렇다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

## 분산이 바꾼 것

분산 VCS에서 클라이언트는 최신 스냅샷만 받아 오지 않는다. **역사를 포함해 저장소 전체를 그대로 복제한다**. 그래서 서버가 죽어도 아무 클라이언트의 복제본을 서버로 되올리면 복구된다. 쉽게 말하면 clone 한 번이 곧 백업 한 부다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

여기서 두 번째 효과가 따라온다. 역사 전체가 로컬 디스크에 있으니 로그를 보거나 한 달 전 파일과 비교하는 일을 서버에 묻지 않고 즉시 처리한다. 비행기 안에서도, VPN이 안 붙는 집에서도 커밋을 계속 쌓다가 연결되면 올리면 된다 (→ [[sources/gitbook-what-is-git|#46 Pro Git Git이란]]).

세 번째는 협업 모양이다. 원격 저장소를 여러 개 두고 서로 다른 그룹과 다른 방식으로 동시에 일할 수 있다. 중앙집중식에서는 불가능한 계층형 워크플로 같은 것이 이때 열린다 (→ [[sources/gitbook-about-version-control|#44 Pro Git 버전관리란]]).

다만 "분산"이 곧 "서버가 없다"는 뜻은 아니다. 실제로는 팀이 모여 밀고 당기는 공용 저장소를 두고 쓰는 것이 보통이다 (→ [[sources/kodekloud-how-git-works|#50 KodeKloud Git 내부]]·[[sources/tistory-inpa-git-concept|#51 Inpa Git 개념]]). 그 동기화가 어떻게 도는지는 [[concepts/git-remote-sync|원격 저장소 동기화]]에서 다룬다.

## 함께 읽기

- [[entities/git|Git]] — 이 계보의 분산 세대가 2005년에 어떤 사건에서 나왔는지
- [[concepts/git-object-model|Git 동작 원리]] — 분산이 가능하려면 데이터를 어떻게 저장해야 하는지
- [[concepts/git-remote-sync|원격 저장소 동기화]] — 복제본끼리 다시 맞추는 방법

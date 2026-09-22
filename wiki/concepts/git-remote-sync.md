---
title: 원격 저장소 동기화 — clone·fetch·pull·push
type: concept
created: 2026-09-22
updated: 2026-09-22
sources: [gitbook-branching-and-internals, gitscm-command-manpages, kodekloud-how-git-works]
aliases: [git fetch, git pull, git push, remote tracking branch]
tags: [Git, 원격저장소, 협업, 동기화]
---

# 원격 저장소 동기화 — clone·fetch·pull·push

## 한눈에 요약

- 분산 방식에서는 저장소 복제본이 여러 벌 존재하므로, 그 복제본끼리 다시 맞추는 절차가 따로 필요하다. 그 절차가 clone·fetch·pull·push다.
- `origin/main` 같은 이름은 내 브랜치가 아니라 **마지막으로 통신했을 때 서버가 어디였는지** 적어 둔 책갈피다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).
- fetch는 내려받기만 하고 내 브랜치나 작업 디렉터리를 건드리지 않는다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).
- pull은 fetch에 통합을 붙인 것이고, 통합 방법을 지정하지 않으면 `--ff-only`가 기본이라 갈라진 경우 실패한다 (2026-09 기준) (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).
- push는 내가 clone 한 뒤 남이 먼저 올렸으면 거절된다. 먼저 받아서 합친 다음 다시 올려야 한다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## 리모트와 원격 추적 브랜치

원격 저장소(remote repository)는 인터넷이나 네트워크 어딘가에 있는 내 프로젝트의 다른 판본이다. 여러 개를 둘 수 있고, 각각은 보통 읽기 전용이거나 읽기·쓰기 권한을 갖는다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

> "원격"이 꼭 멀리 있다는 뜻은 아니다. 같은 컴퓨터에 있는 저장소를 리모트로 둘 수도 있다. 다른 곳에 있다는 뜻일 뿐, 거리와는 상관없다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

clone 하면 그 서버가 `origin`이라는 이름으로 자동 등록된다. `origin`은 관례일 뿐 특별한 이름은 아니고, `git remote add <이름> <URL>`로 얼마든지 더 붙일 수 있다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

그리고 여기서 헷갈리기 쉬운 이름이 하나 나온다. `origin/main` 같은 원격 추적 브랜치다. 이건 내 브랜치가 아니라 **마지막으로 그 서버와 통신했을 때 그쪽 브랜치가 어디에 있었는지**를 적어 둔 책갈피다. `refs/remotes/` 아래에 있고 읽기 전용으로 취급된다. 체크아웃은 되지만 커밋으로 갱신되지는 않는다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## fetch — 가져오기만 한다

`git fetch <리모트>`는 그 저장소에서 브랜치와 태그, 그리고 그 역사를 완성하는 데 필요한 객체를 내려받고 원격 추적 브랜치를 갱신한다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

중요한 건 **하지 않는 일** 쪽이다. fetch는 내 로컬 브랜치를 옮기지 않고, 지금 작업 중인 내용도 건드리지 않는다. 합치는 일은 내가 준비됐을 때 따로 해야 한다. 그래서 "일단 서버에 뭐가 올라왔는지만 보자"는 상황에 fetch가 맞는다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

받아온 참조 이름과 객체 이름은 `.git/FETCH_HEAD`에 기록된다. 스크립트나 다른 Git 명령, 특히 `git pull`이 이 정보를 읽어 간다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

서버에서 사라진 브랜치의 흔적이 내 쪽에 남는 문제는 `--prune`이 맡는다. fetch 전에, 원격에 더 이상 존재하지 않는 원격 추적 참조를 지운다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

## pull — fetch + 통합

`git pull`은 먼저 같은 인자로 `git fetch`를 돌리고, 통합할 원격 브랜치를 정한 다음, 그것을 현재 브랜치에 통합한다. 즉 pull은 하나의 동작이 아니라 **두 동작의 묶음**이다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

통합 방법은 네 가지이고, 아무것도 지정하지 않았을 때의 기본은 `--ff-only`다 (2026-09 기준) (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

| 방식 | 하는 일 | 갈라졌을 때 |
|---|---|---|
| `--ff-only` (기본) | fast-forward 갱신만 | **실패한다** |
| `--rebase` | `git rebase` 실행 | 내 커밋을 재적용 |
| `--no-rebase` | `git merge` 실행 | 머지 커밋 생성 |
| `--squash` | `git merge --squash` 실행 | 변경만 스테이징 |

매번 손으로 붙이고 싶지 않으면 설정으로 굳힌다. `pull.rebase`·`pull.squash`·`pull.ff`가 각각 그 역할을 한다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]). 특히 남이 강제로 밀어 올린 역사를 받아야 하는 상황에서는 `git config --global pull.rebase true`가 뒤처리를 덜 아프게 만든다고 Pro Git이 권한다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

> **주의 — 자료에 따라 pull의 기본값이 다르게 적혀 있다.** Pro Git 2.5절은 pull을 "fetch 후 merge"로 설명한다. 그리고 `pull.rebase`를 false로 두는 것이 "가능하면 fast-forward, 아니면 머지 커밋"이라는 Git의 기본 동작이라고 적는다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]). 반면 현행 `git-pull` 매뉴얼은 `--ff-only`가 기본이라고 못 박는다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]). 둘 다 공식 문서이므로 어느 쪽도 지우지 않았고, **시점 차이로 본다**. 지금 동작의 근거로는 매뉴얼 쪽을 따른다 (2026-09 기준).

## push — 그리고 거절당할 때

공유할 준비가 되면 `git push <리모트> <브랜치>`로 올린다. clone 하면 리모트 이름과 추적 관계가 대개 자동으로 잡히고, 로컬 브랜치가 그에 대응하는 원격 브랜치를 추적하도록 설정된다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

이 명령은 두 조건이 맞을 때만 성공한다. 쓰기 권한이 있어야 하고, **그 사이에 아무도 먼저 올리지 않았어야** 한다. 나와 다른 사람이 동시에 clone 했는데 상대가 먼저 push 했다면 내 push는 정당하게 거절된다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

해법은 순서를 지키는 것뿐이다. 먼저 상대 작업을 받아 와 내 작업에 통합한 뒤에야 올릴 수 있다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]). 통합 방법을 merge로 할지 rebase로 할지는 [[concepts/git-branch-integration|브랜치 합치기]]의 문제로 넘어간다.

> 거절을 강제로 뚫는 `--force` 계열은 서버의 역사를 덮어쓴다. 남이 그 커밋 위에 작업했다면 rebase 황금률을 어기는 것과 같은 사고가 난다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## 리모트 관리

리모트 자체를 들여다보고 손보는 명령도 몇 개 있다. 자주 쓰는 것만 추리면 이렇다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

| 명령 | 하는 일 |
|---|---|
| `git remote -v` | 등록된 리모트의 짧은 이름과 읽기·쓰기 URL을 본다 |
| `git remote show <이름>` | 추적 관계, 서버에만 있는 브랜치, 낡은 참조까지 보여 준다 |
| `git remote rename` | 짧은 이름을 바꾼다. 원격 추적 브랜치 이름도 함께 바뀐다 |
| `git remote remove <이름>` | 리모트와 그에 딸린 원격 추적 브랜치·설정을 함께 지운다 |

`git remote show origin`은 특히 쓸모가 많다. "이 브랜치에서 pull 하면 무엇이 합쳐지고, push 하면 어디로 가는지"를 한눈에 알려 주기 때문이다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## 함께 읽기

- [[concepts/git-branch-integration|브랜치 합치기]] — pull이 내부에서 부르는 merge와 rebase
- [[concepts/version-control|버전 관리 시스템]] — 왜 복제본을 여러 벌 두는 구조가 됐는지
- [[concepts/git-object-model|Git 동작 원리]] — 원격 추적 브랜치도 결국 참조 파일 하나다

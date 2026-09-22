---
title: 되돌리기 — reset·revert·restore·stash
type: concept
created: 2026-09-22
updated: 2026-09-22
sources: [gitbook-branching-and-internals, gitscm-command-manpages, gitscm-docs-git, kodekloud-how-git-works]
aliases: [git reset, git revert, git restore, git stash]
tags: [Git, 되돌리기, 복구, 세트리]
---

# 되돌리기 — reset·revert·restore·stash

## 한눈에 요약

- 이름이 비슷한 되돌리기 명령이 여럿인 이유는, 되돌릴 대상이 브랜치인지 파일인지 공유된 역사인지가 서로 다르기 때문이다.
- `reset`은 브랜치를 옮기는 명령이고, 어디까지 따라 덮을지를 `--soft`·`--mixed`·`--hard`가 정한다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).
- 이 중 실제로 데이터를 파괴하는 것은 `--hard`뿐이다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).
- `revert`는 반대 방향 커밋을 새로 쌓는 방식이라 이미 공유된 이력에도 안전하다 (→ [[sources/gitscm-docs-git|#48 git 명령 레퍼런스]]).
- `stash`는 되돌리기가 아니라 잠깐 치워 두기다. 지저분한 작업 디렉터리를 스택에 얹어 두고 깨끗한 상태로 돌아간다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

## 먼저, 무엇을 되돌리려는지 정한다

공식 매뉴얼은 이름이 헷갈리는 세 명령을 아예 한 절에 모아 분업을 밝혀 둔다. 이 문장 셋이 선택의 대부분을 끝낸다 (→ [[sources/gitscm-docs-git|#48 git 명령 레퍼런스]]).

| 명령 | 다루는 대상 | 역사에 하는 일 |
|---|---|---|
| `revert` | 다른 커밋이 만든 변경 | 되돌리는 **새 커밋을 만든다** |
| `restore` | 작업 트리(와 인덱스)의 파일 | 브랜치를 갱신하지 않는다 |
| `reset` | 브랜치 그 자체 | 끝점을 옮겨 커밋을 더하거나 뺀다 |

쉽게 말하면 이렇다. 남들이 이미 받아 간 것을 무르려면 `revert`, 내 파일만 되살리려면 `restore`, 내 브랜치의 커밋 자체를 물리려면 `reset`이다.

## reset — 세 트리를 순서대로 덮는다

`reset`을 이해하려면 [[concepts/git-object-model|Git 동작 원리]]의 세 트리(HEAD·인덱스·작업 디렉터리)를 먼저 떠올려야 한다. reset은 이 셋을 정해진 순서로 덮되, 어디서 멈출지를 옵션이 정한다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

절차는 세 단계다. ① HEAD가 가리키는 **브랜치를** 대상 커밋으로 옮긴다 → ② 인덱스를 새 HEAD와 같게 만든다 → ③ 작업 디렉터리를 인덱스와 같게 만든다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

| 옵션 | 어디까지 | 실제 효과 |
|---|---|---|
| `--soft` | ①에서 멈춤 | 커밋만 무른다. 스테이징된 내용은 그대로 남는다 |
| `--mixed` (기본) | ②에서 멈춤 | 커밋과 `git add`까지 무른다. 파일 수정분은 남는다 |
| `--hard` | ③까지 | 커밋·스테이징·작업 디렉터리 수정까지 전부 날린다 |

`--soft`가 유용한 자리는 분명하다. 마지막 커밋 하나를 `HEAD~`로 무르고 인덱스를 손봐 다시 커밋하면 `commit --amend`와 같은 일이 된다. 최근 다섯 커밋을 하나로 합치는 것도 같은 방식이다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]·[[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

> **`--hard`만이 위험하다.** Pro Git은 이 플래그를 "reset을 위험하게 만드는 유일한 옵션이자, Git이 실제로 데이터를 파괴하는 몇 안 되는 경우"라고 적는다. 다른 형태의 reset은 대체로 되돌릴 수 있지만 `--hard`는 작업 디렉터리 파일을 강제로 덮어쓴다. 커밋해 둔 것이면 reflog로 되찾을 수 있지만, **커밋하지 않은 변경은 복구 수단이 없다** (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

매뉴얼은 사정거리를 한 줄 더 넓게 적는다. `--hard`는 추적되지 않는 파일까지 덮어쓸 수 있고, 대상 커밋에 없는 추적 파일은 지운다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

경로를 주면 이야기가 달라진다. `git reset <파일>`은 ①단계를 건너뛰고 인덱스만 HEAD 내용으로 되돌린다. 결과적으로 `git add`의 정확한 반대, 즉 스테이징 해제가 된다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## reset과 checkout은 무엇이 다른가

둘 다 세 트리를 건드리는데 차이가 딱 두 가지다. 이 둘만 기억하면 헷갈릴 일이 없다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

첫째, **작업 디렉터리 안전성**이다. `checkout <브랜치>`는 고쳐 둔 파일을 날리게 되는지 먼저 확인하고, 안 바뀐 파일만 갱신하는 식으로 조심스럽게 움직인다. `reset --hard`는 확인 없이 전부 갈아 끼운다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

둘째, **무엇을 옮기는가**다. reset은 HEAD가 가리키는 **브랜치를** 옮기고, checkout은 **HEAD 자체를** 옮겨 다른 브랜치를 가리키게 한다. 둘 다 "HEAD가 A 커밋을 보게 된다"로 보이지만 남는 결과가 다르다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## revert — 공유된 이력에 안전한 되돌리기

`revert`는 커밋을 지우지 않는다. 그 커밋이 들여온 변경을 되돌리는 **새 커밋을 앞에 쌓는다** (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

이 차이가 협업에서 결정적이다. reset은 브랜치 끝점을 옮겨 커밋 역사를 바꾸므로, 남이 이미 받아 간 커밋에 쓰면 rebase 황금률을 어기는 것과 같은 사고가 난다. revert는 역사를 더하기만 하니 그런 문제가 없다 (→ [[sources/gitscm-docs-git|#48 git 명령 레퍼런스]]·[[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

머지 커밋에는 단서가 붙는다. 어느 쪽이 주 갈래인지 알 수 없으므로 `-m <부모번호>`로 지정해야 한다. 그리고 머지를 revert 한다는 것은 **"이 머지가 들여온 트리 변경을 앞으로도 원하지 않는다"는 선언**이다. 그래서 이후 머지는 되돌린 머지의 조상이 아닌 커밋의 변경만 가져온다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

## restore와 switch — checkout이 하던 두 일을 나눴다

`checkout` 매뉴얼은 스스로 "주 모드가 둘 있다"고 적는다. 브랜치를 바꾸는 모드와 파일의 다른 버전을 복원하는 모드다. 하나의 명령이 전혀 다른 두 일을 하니 헷갈릴 수밖에 없었다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

지금은 그 두 모드에 각각 이름이 붙어 있다. Git 2.23부터 `switch`로 브랜치를 바꾸고 `restore`로 파일을 되살릴 수 있다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]·[[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

| 명령 | 하는 일 | 알아 둘 점 |
|---|---|---|
| `switch <브랜치>` | 브랜치 전환. 작업 트리와 인덱스를 그 브랜치에 맞춘다 | 로컬 변경을 잃게 되면 중단된다 |
| `switch -c <새브랜치>` | 만들면서 전환 | `checkout -b`와 같은 일 |
| `restore <파일>` | 인덱스 내용으로 작업 트리 파일 복원 | 브랜치를 갱신하지 않는다 |
| `restore --staged <파일>` | HEAD 내용으로 인덱스 복원 | 스테이징 해제에 해당 |
| `restore --source=<커밋>` | 지정한 커밋에서 파일을 꺼내 온다 | 커밋 안 된 변경은 덮인다 |

> `restore`는 기본적으로 커밋하지 않은 변경을 덮어쓴다. `revert` 매뉴얼도 이 점을 경고하며 "`reset --hard`와 `restore --source` 둘 다 조심하라"고 적는다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

## stash — 되돌리는 게 아니라 치워 두는 것

작업이 반쯤 된 상태에서 급한 다른 일이 들어올 때가 있다. 반토막 작업을 커밋하기는 싫고, 그렇다고 버릴 수도 없다. 이때 쓰는 게 `stash`다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

`git stash`는 작업 디렉터리의 지저분한 상태, 즉 수정된 추적 파일과 스테이징된 변경을 스택에 얹어 두고 작업 디렉터리를 HEAD 커밋과 같게 되돌린다. 인자 없이 쓰면 `git stash push`와 같다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

꺼내 쓰는 방법이 두 가지인데 차이가 중요하다. `apply`는 적용만 하고 스택에 그대로 남기고, `pop`은 적용한 뒤 바로 버린다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

| 명령 | 하는 일 |
|---|---|
| `git stash list` | 쌓아 둔 스태시 목록 |
| `git stash apply` | 가장 최근 것을 적용(스택에 남음) |
| `git stash apply --index` | 스테이징 상태까지 되살려 적용 |
| `git stash pop` | 적용 후 스택에서 제거 |
| `git stash drop <이름>` | 적용하지 않고 버린다 |

저장한 브랜치에서만 꺼낼 수 있는 것도 아니다. 한 브랜치에서 넣어 두고 다른 브랜치로 옮겨 가 적용할 수 있으며, 그때 깔끔히 적용되지 않으면 충돌로 알려 준다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

> 기본 `apply`는 스테이징 상태를 되살리지 않는다. 넣기 전에 `git add`까지 해 뒀다면 `--index`를 붙여야 원래 자리로 정확히 돌아온다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## 함께 읽기

- [[concepts/git-object-model|Git 동작 원리]] — 세 트리를 모르면 reset의 옵션은 외울 수밖에 없다
- [[concepts/git-branch-integration|브랜치 합치기]] — 합치다 멈췄을 때 빠져나오는 `--abort` 계열
- [[concepts/git-remote-sync|원격 저장소 동기화]] — 이미 push 한 것을 무를 때 reset 대신 revert를 쓰는 이유

---
title: "git 명령 매뉴얼 11편 묶음 — merge·rebase·fetch·pull 외"
label: "#49 git 매뉴얼 11편"
type: source
credibility: high
volatility: warm
created: 2026-09-22
updated: 2026-09-22
sources: [gitscm-command-manpages]
tags: [Git, 공식문서, 명령어, 되돌리기, 머지]
---

# git 명령 매뉴얼 11편 묶음 — merge·rebase·fetch·pull 외

## 한 줄 요약

`merge`·`rebase`·`fetch`·`pull`·`cherry-pick`·`reset`·`revert`·`stash`·`switch`·`restore`·`checkout` 열한 개 명령의 공식 매뉴얼을 한 파일로 묶은 자료로, 각 명령의 **현행 기본값**을 확인하는 데 쓰는 1차 출처다.

## 핵심 내용

- **merge** — 갈라진 뒤의 변경을 현재 브랜치로 가져와 **부모 두 개의 이름과 함께** 새 커밋에 기록한다. 작업 전에 `ORIG_HEAD`를 현재 브랜치 끝점으로 세팅한다. 자동 해결이 안 되는 충돌이 나면 멈추고, 거기서 `--abort`나 `--continue`를 고를 수 있다.
- **rebase** — "일련의 커밋을 다른 출발점으로 이식한다". 동작을 네 단계로 요약해 준다. ① 갈라진 뒤의 커밋 목록을 만들고 ② 대상을 detach 상태로 체크아웃한 뒤 ③ 커밋을 하나씩 순서대로 재적용하고(각 커밋에 `cherry-pick`을 도는 것과 비슷하다) ④ 브랜치를 마지막 커밋으로 옮긴다. 충돌 시 `--continue`·`--abort`·`--skip` 셋 중 하나를 고른다.
- **fetch** — 다른 저장소에서 브랜치와 태그, 그리고 그 역사를 완성하는 데 필요한 객체를 내려받고 원격 추적 브랜치를 갱신한다. 받아온 참조 이름과 객체 이름은 `.git/FETCH_HEAD`에 기록되며, `git pull` 같은 명령이 이 정보를 쓴다. `--prune`은 원격에서 사라진 원격 추적 참조를 fetch 전에 정리한다.
- **pull** — 먼저 같은 인자로 `git fetch`를 돌리고, 통합할 원격 브랜치를 정한 뒤, 그것을 현재 브랜치에 통합한다. 통합 방식은 네 가지이고 **`--ff-only`가 기본**이다. 내 브랜치가 원격과 갈라졌으면 실패한다. 나머지는 `--rebase`(rebase 실행)·`--no-rebase`(merge 실행)·`--squash`이며, `pull.rebase`·`pull.squash`·`pull.ff` 설정으로 기본 동작을 바꾼다.
- **cherry-pick** — 기존 커밋 하나 이상이 만든 변경을 적용하고 **각각에 대해 새 커밋을 기록**한다. 작업 트리가 깨끗해야 한다. 충돌하면 브랜치와 HEAD는 마지막 성공 지점에 머물고 `CHERRY_PICK_HEAD`가 문제 커밋을 가리킨다.
- **reset** — `git reset [<mode>] <commit>`은 HEAD가 가리키는 지점을 바꿔 commit·merge·rebase·pull 같은 작업을 되돌린다. 경로를 주면 대신 지정한 파일의 스테이징 상태를 갱신한다. 모드 기본값은 `--mixed`다.
- **revert** — 기존 커밋이 들여온 변경을 되돌리는 **새 커밋을 기록**한다. 매뉴얼은 "작업 디렉터리의 커밋 안 된 변경을 버리고 싶으면 `reset --hard`를, 다른 커밋의 파일을 꺼내고 싶으면 `restore --source`를 보라"고 안내하면서, 그 둘은 커밋 안 된 변경을 버리니 조심하라고 덧붙인다.
- **stash** — 작업 디렉터리와 인덱스의 현재 상태를 기록해 두고 작업 디렉터리를 HEAD 커밋과 같게 되돌린다. 최신 스태시는 `refs/stash`에 있고 과거 것들은 그 reflog에 있어 `stash@{0}` 식으로 부른다. 인자 없는 `git stash`는 `git stash push`와 같다.
- **switch / restore** — `switch`는 브랜치를 바꾸며 작업 트리와 인덱스를 그 브랜치에 맞춘다. 인덱스·작업 트리가 깨끗할 필요는 없지만 로컬 변경을 잃게 되는 경우에는 중단된다. `restore`는 복원 소스(기본은 인덱스, `--staged`면 HEAD)에서 작업 트리 파일을 되살리며, `--staged`로 인덱스만 되살릴 수도 있다.
- **checkout** — 매뉴얼 스스로 "두 가지 주 모드가 있다"고 적는다. 브랜치를 바꾸는 모드와 파일의 다른 버전을 복원하는 모드다. `switch`·`restore`가 갈라 맡은 것이 정확히 이 두 모드다.

## 주요 주장 / 데이터

- **기본 머지 전략은 `ort`다 (2026-09 기준).** `-s` 옵션이 없으면 내장 목록이 쓰이는데, 헤드 하나를 머지할 때는 `ort`, 그 이상은 `octopus`다. `ort`는 "Ostensibly Recursive's Twin"의 두문자어이고, 이전 기본 알고리즘 `recursive`를 대체하려고 쓰였다는 데서 온 이름이다.
- **`recursive`의 이력 (2026-09 기준)** — 지금은 `ort`의 동의어다. v2.49.0까지는 별도 구현이었다가 v2.50.0에서 `ort`를 뜻하도록 돌려졌다. 그 이전, v0.99.9k부터 v2.33.0까지는 헤드 둘을 합칠 때의 기본 전략이었다.
- **머지 커밋은 그냥 cherry-pick 할 수 없다.** 어느 쪽을 주 갈래로 볼지 알 수 없기 때문이며, `-m <부모번호>`(`--mainline`)로 주 갈래를 지정해야 한다. `revert`도 같은 제약과 같은 옵션을 갖는다.
- **머지 커밋을 revert 하는 것은 "이 머지가 들여온 트리 변경을 앞으로도 영영 원하지 않는다"는 선언이다.** 이후 머지는 되돌린 머지의 조상이 아닌 커밋의 변경만 가져오게 된다.
- **`reset --hard`의 사정거리** — 모든 파일과 디렉터리를 대상 커밋의 판본으로 덮어쓰며 **추적되지 않는 파일까지 덮어쓸 수 있다**. 대상 커밋에 없는 추적 파일은 삭제된다.
- **3-way 머지의 알려진 함정** — 양쪽에서 같은 변경을 했다가 한쪽에서 되돌린 경우, 머지 결과에는 그 변경이 남는다. 머지는 두 끝점과 merge base만 보고 중간 커밋들을 보지 않기 때문이다. 매뉴얼이 "헷갈린다고들 한다"며 직접 적어 둔 항목이다.
- **`ort` 전략일 때만 `AUTO_MERGE` 참조가 쓰인다.** 충돌 표식을 포함한 현재 작업 트리 상태에 해당하는 트리를 가리킨다.

## 기존 위키와의 연결

- 강화: [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]의 rebase 설명(공통 조상 이후의 diff를 차례로 재적용)을 매뉴얼의 4단계 요약이 거의 그대로 확인해 준다.
- 모순: 같은 자료의 2.5절이 적은 `git pull` 기본 동작("fetch 후 merge")과 이 매뉴얼의 "`--ff-only`가 기본"이 어긋난다. 둘 다 공식 문서라 어느 쪽도 지우지 않고 시점 차이로 남겼다. 현행 동작은 매뉴얼 쪽이다 (2026-09 기준).
- 신규: [[concepts/git-branch-integration|브랜치 합치기]]·[[concepts/git-undo|되돌리기]]·[[concepts/git-remote-sync|원격 저장소 동기화]] 세 개념 페이지의 명령별 사실 대부분이 이 자료에서 나왔다.

## 출처 정보

- raw: raw/gitscm-command-manpages.md
- 저자/발행처: git-scm.com — Git 공식 문서(man page)
- 수집일: 2026-09-22
- URL: https://git-scm.com/docs/git-merge (외 10편: git-rebase, git-fetch, git-pull, git-cherry-pick, git-reset, git-revert, git-stash, git-switch, git-restore, git-checkout)
- 범위: 11개 매뉴얼의 본문 전체. `git-push` 매뉴얼은 이번 수집에 포함되지 않아, push 거절에 대한 서술은 [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]에만 기댄다.

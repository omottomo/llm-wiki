---
title: "분석 — merge vs rebase: 언제 무엇을 쓰나"
type: analysis
created: 2026-09-22
updated: 2026-09-22
sources: [gitbook-branching-and-internals, gitscm-command-manpages]
tags: [분석, Git, 머지, 리베이스, 비교]
---

# 분석 — merge vs rebase: 언제 무엇을 쓰나

## 결론 먼저

> merge와 rebase는 같은 결과 스냅샷을 만들고 역사의 모양만 다르게 남기므로, 둘 중 하나가 옳은 것이 아니라 **커밋이 이미 밖으로 나갔는지**가 선택을 가른다. 아직 내 컴퓨터 안에 있으면 rebase로 정리해도 되고, 남이 그 위에 작업했을 수 있으면 merge를 쓴다. Pro Git은 여기서 한쪽 편을 들지 않고 "역사는 기록인가 이야기인가"라는 두 입장을 나란히 적는다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## 비교표

| 축 | merge | rebase |
|---|---|---|
| 이력 모양 | 갈래가 갈라졌다 합쳐진 그대로 남는다 | 한 줄로 펴진다 |
| 새로 생기는 커밋 | 부모 둘인 머지 커밋 1개 (fast-forward면 0개) | 재적용된 커밋들, 해시가 전부 새것 |
| 충돌이 멈추는 자리 | 합치는 지점에서 한 번 | 문제가 된 커밋마다 |
| 되돌리기 | 머지 커밋 하나를 revert (`--mainline` 필요) | 원래 커밋이 참조에서 떨어져 나간다 |
| 공유 브랜치 안전성 | 안전 | **이미 push 했다면 금지** |

### 이력 모양과 결과물

두 명령의 최종 결과 스냅샷은 같다. Pro Git이 직접 확인하는 대목이다 — rebase 뒤 fast-forward로 합친 커밋이 가리키는 스냅샷은 merge로 만든 머지 커밋의 스냅샷과 정확히 같다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

다른 것은 역사뿐이다. rebase를 거치면 병렬로 일어난 작업이 순서대로 일어난 것처럼 보이고, merge를 쓰면 갈라졌다 합쳐진 자취가 그대로 남는다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

### 충돌이 멈추는 자리

merge는 두 브랜치 끝과 공통 조상, 세 지점만 본다. 그래서 충돌도 합치는 그 지점에서 한 번 난다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

rebase는 커밋을 하나씩 순서대로 다시 적용한다. 매뉴얼은 충돌이 나면 "첫 번째 문제 커밋에서 멈춘다"고 적고 `--continue`로 이어 가게 한다. 즉 멈추는 지점이 커밋 단위로 생길 수 있다는 뜻이다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

> 이 항목은 자료가 "여러 번 멈춘다"고 못 박은 게 아니라, 한 커밋씩 재적용한다는 동작 설명에서 따라 나오는 읽기다. 실제 횟수는 갈래가 얼마나 겹쳤는지에 달렸다.

### 되돌리기

merge 쪽은 문이 분명하다. 머지 커밋 하나를 revert 하면 된다. 다만 어느 쪽이 주 갈래인지 `--mainline`으로 지정해야 하고, 그 순간 "이 머지가 들여온 트리 변경을 앞으로도 원하지 않는다"는 선언이 된다. 이후 머지는 되돌린 머지의 조상이 아닌 커밋의 변경만 가져온다 (→ [[sources/gitscm-command-manpages|#49 git 매뉴얼 11편]]).

rebase 쪽은 더 번거롭다. rebase는 기존 커밋을 버리고 비슷하지만 다른 커밋을 새로 만들기 때문에, 원래 커밋은 어느 브랜치도 가리키지 않는 상태가 된다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]). 참조가 끊긴 커밋을 되찾는 수단으로 Pro Git이 소개하는 것은 reflog인데, 이 소개는 `reset --hard` 복구 맥락에서 나온다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

### 공유 브랜치 안전성

여기가 진짜 갈림길이다. 원문의 황금률은 한 줄이다. "내 저장소 밖에 나가 있고 남이 그 위에 작업했을 수 있는 커밋은 rebase 하지 않는다" (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

어기면 무슨 일이 나는지도 자료가 사례로 보여 준다. 누군가 push 한 작업을 rebase 해서 강제로 덮어쓰면, 그 커밋 위에 작업하던 사람은 같은 내용을 다시 머지해야 한다. 그 결과 작성자·날짜·메시지가 똑같은 커밋이 역사에 둘씩 보인다. 그걸 다시 올리면 상대가 지우려던 커밋들이 서버에 되살아난다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

> 이미 사고가 났다면 손이 아주 없지는 않다. Git은 커밋 해시 외에 변경분만으로 계산한 patch-id를 갖고 있어서, `git pull --rebase`로 받으면 무엇이 내 것이고 무엇이 다시 쓰인 것인지 상당 부분 가려낸다. 다만 상대가 만든 커밋과 그 사본이 거의 같은 패치일 때만 통한다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## 역사는 기록인가, 이야기인가

이 논쟁은 기술 문제가 아니라 역사관 문제라, Pro Git은 결론을 내리는 대신 두 입장을 나란히 적는다. 어느 쪽도 틀렸다고 하지 않는다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

| 입장 | 주장 | 따라 나오는 습관 |
|---|---|---|
| 역사는 **기록**이다 | 저장소의 커밋 역사는 실제로 일어난 일의 기록이며 그 자체로 가치 있는 사료다. 손대는 것은 일어난 일을 거짓말하는 셈이다 | 지저분한 머지 커밋이 남아도 그대로 둔다 |
| 역사는 **이야기**다 | 커밋 역사는 프로젝트가 만들어진 이야기다. 책의 초고를 그대로 출판하지는 않듯, 세상에 보여 줄 때는 A에서 B로 가는 앞뒤 맞는 이야기로 다듬는다 | 주 브랜치에 넣기 전에 rebase로 정리한다 |

문서가 내리는 유일한 판단은 "그렇게 간단하지 않다"는 것이다. Git은 역사에 많은 일을 할 수 있게 해 주지만 팀과 프로젝트가 저마다 다르니, 양쪽 동작을 알고 난 다음 상황에 맞게 고르라고 맺는다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## 그래서 실무에서는

자료가 제시하는 타협안이 하나 있고, 이게 사실상 표준 조언이다. **밖으로 내보내기 전의 로컬 커밋은 rebase로 정리하고, 한 번이라도 push 한 것은 절대 rebase 하지 않는다.** 그러면 양쪽의 좋은 점을 다 가져갈 수 있다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

| 상황 | 권장 | 근거 |
|---|---|---|
| 아직 push 하지 않은 내 커밋 정리 | rebase | 황금률에 걸리지 않고 역사가 깔끔해진다 |
| 남의 프로젝트에 패치를 보내기 전 | 대상 브랜치 위로 rebase | 받는 쪽이 fast-forward나 깨끗한 적용만 하면 된다 |
| 이미 push 한 브랜치를 주 브랜치에 통합 | merge | 남이 그 커밋 위에 작업했을 수 있다 |
| 팀이 역사 보존을 원칙으로 정한 경우 | merge | 기술 판단이 아니라 팀 합의의 영역이다 |

세 번째 줄과 네 번째 줄이 다른 이유를 짚어 둘 만하다. 앞은 사고를 막는 기술적 제약이고, 뒤는 위의 두 역사관 중 어느 쪽을 택했느냐의 문제다. 전자는 어기면 협업자가 다치고, 후자는 어겨도 취향 차이로 끝난다.

> 한 가지 더. `git pull`을 rebase 방식으로 쓰려면 `pull.rebase` 설정을 켜면 된다. 팀이 강제 푸시 사고를 겪은 뒤라면 모두에게 `git pull --rebase`를 쓰게 하라고 자료가 권한다 (→ [[sources/gitbook-branching-and-internals|#47 Pro Git 브랜치·내부]]).

## 함께 읽기

- [[concepts/git-branch-integration|브랜치 합치기]] — 두 명령이 실제로 무슨 일을 하는지, cherry-pick까지 포함해
- [[concepts/git-remote-sync|원격 저장소 동기화]] — pull이 내부에서 어느 쪽을 부르는지
- [[concepts/git-object-model|Git 동작 원리]] — 왜 "해시가 새로 생긴다"가 이 논쟁의 전부인지

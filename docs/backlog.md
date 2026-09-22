# 흡수 백로그 (ingest backlog)

> 아직 위키에 넣지 않은 **흡수 후보**·미해결 질문·관찰 대상을 모아두는 대기열이다.
> `log.md`·`CLAUDE.md`와 마찬가지로 **발행되지 않는다**(사이트 콘텐츠 루트는 `wiki/` 뿐).
>
> **이 파일은 사실 근거가 아니다.** 여기 적힌 항목은 "언젠가 확인/흡수할 것"이라는 메모일 뿐,
> 위키 페이지의 주장을 뒷받침하는 출처로 인용해서는 안 된다. 사실은 흡수를 거쳐 `raw/` →
> `wiki/sources/`로 들어온 뒤에야 근거가 된다.
>
> 흡수를 마친 항목은 이 표에서 지우고(또는 상태를 `흡수완료`로 바꾸고) `log.md`에 ingest 줄을 남긴다.

| 후보 | 유형 | 상태 | 메모 |
|---|---|---|---|
| (예: https://example.com/article) | 아티클 | 대기 | 왜 넣고 싶은지 / 어느 개념과 연결되는지 |
| https://www.usenix.org/legacy/publications/library/proceedings/sec2000/robin.html (Robin & Irvine, USENIX Security 2000) | 논문 | 대기 | x86 의 "민감하지만 비특권" 명령 개수(17/18)의 원출처. 흡수하면 `concepts/virtualization-internals` 의 단서 문장을 2차 인용(#40)에서 1차 근거로 승격할 수 있다 |
| VMware, "A Comparison of Software and Hardware Techniques for x86 Virtualization" (Adams & Agesen, ASPLOS 2006) | 논문 | 대기 | 바이너리 변환 대 하드웨어 보조 비교의 1차 자료. 2026-09-22 기준 vmware.com·USENIX 미러 모두 404 — 다른 사본을 찾아야 한다 |
| docs.typesafe.ai 쿡북·SDK 페이지 (약 60쪽) | 공식 문서 | 대기 | 이번엔 코어 17쪽만 흡수했다. `confidence` 계산·일관성·RAG 패시지 분류 쿡북은 `concepts/jev-primitives` 를 실전 수준으로 늘릴 재료 |
| git-push 매뉴얼 | 공식 문서 | 대기 | #49 묶음에 빠져서 push 거절의 공식 용어(non-fast-forward)를 쓰지 못했다 |

## 미해결 질문

- **색인이 임계치를 넘었다.** `docs/rules/wiki-content.md` §2 의 확장 기준은 한 카테고리가 약 30개를 넘으면 MOC(Map of Content) 허브 페이지를 도입하라고 적는다. 2026-09-22 기준 Sources 56·Concepts 34·Entities 36 으로 세 카테고리가 모두 넘었다. 주제가 AI 코딩·IaC·가상화·Git·Jev 로 갈라졌으니 주제별 MOC 가 자연스러운 분할선이다 — 사람 결정 대기.

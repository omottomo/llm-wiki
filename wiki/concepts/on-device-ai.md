---
title: 온디바이스 AI
type: concept
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-rEamRUk7-pg]
tags: [온디바이스AI, Gemma, 로컬모델, API비용절감]
---

# 온디바이스 AI

**온디바이스 AI(On-Device AI)**는 클라우드 API 호출 없이 핸드폰 등 **엣지(edge) 기기 자체에서 AI 모델을 돌리는** 방식이다. 가장 큰 이점은 **API 비용이 0**이라는 점으로, 로컬에서 무료로 AI를 구동할 수 있다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]). 이 위키에서 온디바이스 AI는 주로 [[entities/google-gemma|구글 Gemma]] 모델을 통해 다뤄진다.

## 구글 Gemma — 사이즈 대비 퍼포먼스 지향

[[entities/google-gemma|Gemma]] 모델군은 고성능보다 **엣지에서 사용할 수 있는 AI**를 지향하며, 사이즈 대비 높은 퍼포먼스를 목표로 한다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]). 영상은 새로 나온 **Gemma 4** 모델을 다룬다.

- 베리에이션: 고성능 컴퓨팅용 31B·26B 모델과, 온디바이스용 **E2B(2B 파라미터)·E4B(4B 파라미터)** 모델이 있다. `E`는 엣지(Edge)를 뜻하는 것으로 추정된다 (자막상 발표자 추정) (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]).
- 기능: 어드밴스드 리즈닝, 에이전트 워크플로, 펑션 콜링, 코드 생성, 비전(이미지·오디오 인식)까지 지원한다. 컨텍스트는 **128K**까지, 언어는 **140개 이상**을 지원한다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]).

## Gemma 3 대비 체감 성능

발표자는 작년 말 Gemma 3 모델을 로컬에서 돌려봤을 때 한국어가 잘 안 되고, 속도가 너무 느리며, 램을 너무 많이 먹어 "도저히 쓸 수 없다"고 판단했었다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]). Gemma 4에서는 다음과 같이 개선됐다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]):

- **텍스트 생성**: 한국어가 꽤 잘 되고 속도도 크게 빨라졌다. 단순 텍스트 입출력이 필요한 요소는 쉽게 탑재해 볼 수준에 올라왔다. 2B보다 4B 모델이 더 사람 같고 자연스럽다.
- **멀티모달(이미지·오디오)**: 아직 부족하다. 이미지 인식은 (자막상) ChatGPT 3~3.5 정도 느낌으로, 4B 모델은 캔 음료 개수·색상까지 인식하지만 일부 글자를 못 읽는 한계가 있다. 한국어 음성 트랜스크라이브는 약 80% 정도 맞춘다.

## 메모리 요구량(에뮬레이터 기준)

에뮬레이터 테스트 기준 메모리 요구량은 다음과 같다(실제 기기·iOS는 미테스트, 발표자 추정) (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]):
- **E2B**: 약 6~8GB에서 동작.
- **E4B**: 약 16GB 필요. 8GB만 주면 로딩 중 앱이 죽는다.

4B보다 높은 모델은 사실상 온디바이스에 넣을 수 없으므로, 현재 멀티모달은 아직 부족하다는 결론이다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]).

## 전망

발표자는 Gemma 3 → 4의 성능 발전 폭이 매우 컸던 점을 들어, **Gemma 5**가 나오면 텍스트 입력 인지와 멀티모달 기능이 크게 향상되어, 한두 세대만 지나면 온디바이스 AI 활용이 크게 인기를 끌 것으로 본다 — API 비용을 안 내도 되기 때문이다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]). 앱 개발자에게는 백업이나 웹액 정도로라도 Gemma 4를 한번 써보길 권한다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]).

## 관련 문서
- [[entities/google-gemma|구글 Gemma]] — 이 페이지가 다루는 핵심 엔티티(온디바이스 모델군)
- [[concepts/llm-basics|LLM 기초]] — 모델 파라미터·컨텍스트 윈도우 등 기초 개념

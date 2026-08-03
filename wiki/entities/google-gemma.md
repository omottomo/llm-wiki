---
title: 구글 Gemma
type: entity
created: 2026-06-23
updated: 2026-08-04
sources: [youtube-rEamRUk7-pg]
tags: [모델, 온디바이스AI, 구글]
---
# 구글 Gemma

## 한눈에 요약

- 구글이 공개한 **경량 언어 모델 계열**이다. 큰 서버가 아니라 휴대폰이나 노트북에서 직접 돌리는 것을 목표로 만들어졌다.
- 모델을 작게 만들면 성능이 떨어지기 마련인데, **그 손해를 얼마나 줄였는지**가 관전 포인트다.
- 이 위키에서는 서버 사용료 없이 AI를 돌리는 온디바이스 방식의 대표 사례로 등장한다.

## 어떤 모델인가

구글의 경량 LLM 계열이다. 이 위키에서는 온디바이스 실행이 가능한 모델 **Gemma 4**로 등장한다.

## 이 위키에서의 등장
- **API 비용 0** — 온디바이스에서 동작해 API 비용이 사실상 0이 된다는 점이 강조된다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]).
- **온디바이스의 대표 사례** — [[concepts/on-device-ai|온디바이스 AI]] 문서에서 클라우드 API 의존을 줄이는 흐름의 근거로 제시된다 (→ [[sources/youtube-rEamRUk7-pg|#12 Gemma 4 온디바이스]]).

## 외부 검증 (2026-06-23, 웹)
- **확인 — Gemma 4는 실재하는 최신 버전.** 자막 오인식이 아니라 실제 모델이고 2026년 3월 31일 출시됐다. Gemma 3은 2025년 3월의 이전 세대다.
- **확인 — 사양도 부합.** 온디바이스 변형은 **E2B/E4B**, 컨텍스트는 **128K**(상위 모델 최대 256K)다. **140개 이상 언어**를 네이티브로 학습했고 텍스트·이미지·오디오·비디오 멀티모달을 지원한다. 자막 수치가 모두 맞다 (→ https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/ , https://ai.google.dev/gemma/docs/releases ).

## 함께 읽기

- [[concepts/on-device-ai|온디바이스 AI]] — 이 모델이 대표하는 개념
- [[concepts/llm-basics|LLM 기초]] — 파라미터와 컨텍스트 윈도우가 무엇인지

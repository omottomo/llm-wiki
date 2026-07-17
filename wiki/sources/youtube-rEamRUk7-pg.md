---
title: "#12 온디바이스 AI 끝판왕, Gemma 4로 API 비용 제로!"
label: "#12 Gemma 4 온디바이스"
type: source
created: 2026-06-23
updated: 2026-07-12
sources: [youtube-rEamRUk7-pg]
tags: [온디바이스AI, 구글Gemma, 멀티모달, API비용, 모바일앱]
---

## 한 줄 요약
구글 [[entities/google-gemma|구글 Gemma]] 4 모델을 모바일 에뮬레이터에 직접 탑재해 텍스트·이미지·음성을 실측 테스트하고, 텍스트 작업은 실사용 수준에 올라왔으나 멀티모달은 아직 부족하다고 평가한 [[concepts/on-device-ai|온디바이스 AI]] 데모 영상.

## 핵심 내용
- [[entities/google-gemma|구글 Gemma]] 4는 고성능보다 엣지(on-device) 활용을 지향하는 모델군. 핵심 관심 변형은 엣지용 E2B(2B 파라미터)·E4B(4B 파라미터).
- 기능: 리즈닝, 에이전트 워크플로우/펑션 콜링, 코드 생성, 비전(이미지·오디오) 인식, 컨텍스트 128K, 140개 이상 언어 지원.
- 발표자가 작년 말 Gemma 3로 미연시풍 여자친구 앱·일정관리 앱을 로컬 구동했으나 한국어 품질 저하·느린 속도·과도한 RAM으로 "쓸 수 없다"고 판단했었음. Gemma 4는 한국어·속도가 크게 개선.
- 텍스트 테스트(여자친구 컨셉 대화): 2B는 사무적 톤에 억지 감정을 입힌 느낌, 4B는 확연히 더 자연스럽고 사람 같음.
- 이미지/음성 멀티모달은 부분적 성공: 음료 캔 개수·색상은 4B가 정확히 인식했으나 글자("KV")는 계속 오인식, 애국가 음성 트랜스크립션은 약 80% 정확도로 일부 오류 — 아직 미흡.

## 주요 주장 / 데이터
- 메모리 요구: 에뮬레이터 기준 2B는 약 6~8GB, 4B는 16GB 정도 필요(8GB에서는 4B 로딩 중 앱이 죽음). 실기기·iOS 요구량은 미검증.
- 4B/2B 체감 성능은 "AI 초창기 + α" 수준이나, Gemma 3 대비 발전 폭이 매우 큼.
- 멀티모달용으로 4B보다 큰 모델은 온디바이스에 사실상 탑재 불가 → 현재 멀티모달은 한계.
- 한두 세대 더 지나면 온디바이스 AI 활용 방식이 크게 인기를 끌 것이며, 그 핵심 동기는 "API 비용 제로". 앱 개발자에게 백업/웹앱 용도로라도 테스트를 권장.

## 기존 위키와의 연결
- 강화: 재생목록 내 유일한 [[concepts/on-device-ai|온디바이스 AI]] / [[entities/google-gemma|구글 Gemma]] 출처로서 해당 개념·엔티티 페이지의 1차 근거. "API 비용 절감"이라는 실무 동기를 제공.
- 모순: 재생목록의 다른 영상들이 다루는 [[entities/claude-code|Claude Code]] 기반 [[concepts/harness-engineering|하네스 엔지니어링]] 흐름과는 별개 주제로, 직접적 모순 없음.
- 신규: 모바일 온디바이스 LLM 탑재의 메모리 임계치(2B≈6~8GB, 4B≈16GB)와 멀티모달 한계라는 구체 데이터 도입. [[entities/google-gemma|구글 Gemma]] 엔티티 신규 등장.

## 출처 정보
- raw: raw/youtube-rEamRUk7-pg.md
- URL: https://www.youtube.com/watch?v=rEamRUk7-pg
- 채널: 코드팩토리 (2026-07-12 yt-dlp 조회로 확인; 기존 표기 '미상')
- 재생목록: PLUGinkN1Rwv4KGXiVEmSBzglfAoTxyXd3 (순번 12)
- transcript_lang: ko (자동생성 자막 — "제마/재마/제맛" 등 Gemma 오인식 다수, 수치 신중 참고)

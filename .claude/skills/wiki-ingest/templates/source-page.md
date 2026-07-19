<!--
Source summary page template (wiki/sources/<slug>.md).
Structure keys are English; ALL content you fill in must be Korean.
This is the canonical form of the inline template in docs/rules/wiki-content.md §1,
extended with the 외부 검증 practice this wiki has adopted.
-->
---
title: "영상/문서 제목 (한국어)"
label: "#N 짧은 한글 라벨"   # 다른 페이지가 이 소스를 인용할 때 쓰는 별칭 (대괄호·$·| 금지)
type: source
credibility: medium        # high|medium|low — 소스 주장의 신뢰도, docs/rules/wiki-content.md §1 루브릭
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [<slug>]
tags: [태그1, 태그2]
---

## 한 줄 요약
(이 소스가 무엇을 말하는지 한 문장으로. 핵심 개념은 `[[concepts/...|한글 별칭]]` 으로 즉시 링크 — 별칭 규칙은 docs/rules/wiki-content.md §1.)

## 핵심 내용
- (3~7개 bullet. **자기 자신은 인용하지 않는다** — 페이지 전체가 이 소스다. 다른 페이지 인용은 `(→ [[sources/다른슬러그|라벨]])`.)
- (시점 의존적 주장 — 가격·모델명·도구 기능 — 에는 `(YYYY-MM 기준)` as-of 표기 필수)

## 주요 주장 / 데이터
- (수치·인용·사례 등 구체적 근거. 자막 오인식이 의심되는 고유명사는 "추정" 표시)

## 기존 위키와의 연결
- 강화: [[...]] 의 어떤 주장을 뒷받침하는지
- 모순: [[...]] 와 어떻게 충돌하는지 (양쪽 다 보존하고 명시적으로 플래그)
- 신규: 이 소스로 새로 생긴 [[...]] 페이지/스텁

## 외부 검증 (YYYY-MM-DD, 웹) <!-- optional — 자막 오인식 교정이나 웹 사실확인을 했을 때만 -->
- (예: 자막의 "André Capaci"는 Andrej Karpathy로 확인 — <URL>)

## 출처 정보
- raw: raw/<slug>.md
- URL: <원본 URL>
- 채널: <채널명 — 확인 불가 시 "미상" 또는 "(불확인)", 절대 추측 금지>
- 재생목록: <playlist_id> (순번 #N)   <!-- 해당 시에만 -->
- transcript_lang: ko (자동생성 자막 — 오탈자/오인식 주의)

---
title: DNS 레코드 종류 완벽 정리 (Inpa)
label: "#28 DNS 레코드 종류"
type: source
credibility: medium
volatility: cold
created: 2026-07-21
updated: 2026-07-21
sources: [tistory-inpa-dns-records]
tags: [DNS, 네트워크, 도메인, 웹인프라]
---

# DNS 레코드 종류 완벽 정리 (Inpa)

## 한 줄 요약
개인·실서비스 도메인 운용에 필요한 주요 DNS 레코드(A·AAAA·CNAME·PTR·NS·SOA·MX·TXT·SPF·CAA·HINFO·ISDN)의 역할과 A vs CNAME 트레이드오프, 그리고 nslookup·Dig 등 조회 도구를 예제 중심으로 정리한 웹 인프라 입문 글.

## 핵심 내용
- **A / AAAA**: 도메인 ↔ 서버 IP(IPv4 / IPv6) 직접 매핑. 일대다·다대일 가능하며 TTL만큼 캐시된다.
- **CNAME**: 도메인 → 다른 도메인 이중 매핑(별명). IP가 아닌 도메인만 등록 가능.
- **A vs CNAME**: A는 빠르지만 IP 변경 시 도메인마다 수정, CNAME은 IP 변경에 유연(메인 A 레코드 한 곳만 수정)하나 다단계 조회로 성능 저하 가능 — 장단점이 상반.
- **위임/권한**: NS(네임서버 위임), SOA(도메인당 1개, 영역 인증·타이머), PTR(IP→도메인 역방향, IP당 도메인 1개).
- **메일**: MX(메일 서버 지정), TXT(메모/검증), SPF(발신 인증 — 전용 타입은 deprecated, TXT에 기재).
- **조회 도구**: `nslookup -type=` , Dig(toolbox.googleapps.com), whatsmydns.net(전세계 전파 확인).

## 주요 주장 / 데이터
- SPF 문법: `v=spf1 ip4=... include:... -all` — `-all`(거부)/`~all`(스팸 표시 후 수락)/`+all`(전면 허용) 종결자, IP는 `IP4` 표기.
- SOA 예(naver): `ns1.naver.com webmaster.naver.com 2021012809 21600 1800 1209600 180` — serial·refresh·retry·expire·minimum.
- SPF 전용 레코드 타입은 공식 deprecated → 실제 설정은 TXT 레코드로.

## 기존 위키와의 연결
- 강화: 없음 — 이 위키에 DNS/네트워크 선행 페이지가 아직 없다. 웹 인프라 기초 영역을 새로 연다.
- 모순: 없음. (원문 A vs CNAME 요약 표의 A 레코드 "장점" 서술은 본문의 "빠르다" 프레이밍과 다소 어긋나는 내부 표현 차이가 있으나, 위키 개념 페이지에는 기술적으로 정확한 형태로 정리함.)
- 신규: [[concepts/dns-records|DNS 레코드]] 개념 페이지 신설. 선언적 설정으로 인프라를 관리한다는 결에서 [[concepts/infrastructure-as-code|코드형 인프라]]와 사상적으로 연결.

## 출처 정보
- raw: raw/tistory-inpa-dns-records.md
- 저자: Inpa (Inpa Dev 블로그, inpa.tistory.com)
- URL: https://inpa.tistory.com/entry/WEB-🌐-DNS-레코드-종류-★-알기-쉽게-정리
- 수집일: 2026-07-21
- credibility=medium: 널리 읽히는 개발 블로그의 2차 해설 글. 핵심 주장(SPF deprecated, 레코드 역할)이 Cloudflare 등 1차 출처와 부합. 단 오탈자("MX 레코든느", "Certificat")와 요약 표의 경미한 내부 표현 불일치가 있어 high는 아님.

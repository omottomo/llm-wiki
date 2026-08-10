# 📚 llm-wiki

> **LLM을 통해 구축하는 개인 지식 위키**

**<https://omotomo-llm-wiki.com>**

## 📄 프로젝트 소개

AI로 인해 기술은 빠르게 발전하고, 눈 떠보면 매일 새로운 기술과 개념이 등장하고 있습니다.
새로운 기술과 개념을 공부하고 체득한 뒤 이해한 내용을 글로 기록하는 기존의 학습 방법은 아직 필수적이라
생각합니다. 다만 변화하는 시대 흐름에 맞춰 지식을 학습하고 기록하는 방식도 어느 정도 변화할 필요가
있다고 느끼고 있었습니다.

그러다 **안드레이 카파시(Andrej Karpathy)의 "LLM wiki"** 개념을 접했습니다.
사람이 자료를 읽고 요약하는 것이 아닌 **AI가 사서처럼 읽고 분석하여 위키에 쌓게** 하자는 개념이었습니다.
그래서 새로운 학습 방법으로 나를 위한 llm-wiki를 만들게 되었습니다.

추구하는 목표는 두 가지입니다. 자료가 쌓일수록 wiki에서 얻는 답이 정교해질 것, 그리고 나만 보는
wiki가 아니라 **누구나 읽을 수 있는 사이트**로 남을 것.

## 📋 주요 기능

- **위키 흡수(`wiki-ingest`)**: 사용자가 입력한 원본 문서를 읽고 개념/인물/분석 페이지로 쪼개 위키링크로 엮음
- **위키 질의(`wiki-query`)**: 기존 페이지를 먼저 읽고 답하며, 남길 가치가 있는 답은 `analysis/`로 보존
- **위키 점검(`wiki-lint`)**: 모순·고아 페이지·끊긴 링크·오래된 서술 점검
- **위키 최신화(`wiki-refresh`)**: 살아있는 웹 자료의 변화를 재수집·비교, **사람 확인 후에만** 반영
- **위키 삭제(`wiki-delete`)**: 페이지 삭제 + 끊긴 링크 복구 (파괴적 — 범위 확인 필수)
- **모순 보존**: 새 자료가 기존 서술과 충돌하면 어느 쪽도 지우지 않고 양쪽을 남긴 뒤 표시
- **정적 사이트 발행**: 목차·백링크·인용 각주·태그 색인·사이트맵을 빌드 타임에 생성
- **한국어 전문 검색**: Pagefind 인덱스 (서버·데이터베이스 없음)
- **원본 격리**: 제3자 저작물(`raw/`)은 공개 저장소에 포함되지 않으며, 기계 검사가 경계를 지킴

## 🛠️ 기술 스택

### Content Pipeline

[![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](https://claude.com/claude-code)
[![Markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)](https://commonmark.org/)

### Site Generation

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![markdown-it-py](https://img.shields.io/badge/markdown--it--py-4.2.0-6E4C13?style=for-the-badge&logo=markdown&logoColor=white)](https://markdown-it-py.readthedocs.io/)
[![Pagefind](https://img.shields.io/badge/Pagefind-1.x-034AD8?style=for-the-badge&logo=algolia&logoColor=white)](https://pagefind.app/)
[![Node.js](https://img.shields.io/badge/Node.js-22-5FA04E?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![CSS](https://img.shields.io/badge/CSS-663399?style=for-the-badge&logo=css&logoColor=white)](https://developer.mozilla.org/docs/Web/CSS)

### Infrastructure & Deployment

[![AWS S3](https://img.shields.io/badge/AWS_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/)
[![CloudFront](https://img.shields.io/badge/CloudFront-8C4FFF?style=for-the-badge&logo=amazoncloudfront&logoColor=white)](https://aws.amazon.com/cloudfront/)
[![Route 53](https://img.shields.io/badge/Route_53-8C4FFF?style=for-the-badge&logo=amazonroute53&logoColor=white)](https://aws.amazon.com/route53/)
[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://developer.hashicorp.com/terraform)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows)

## 📁 프로젝트 구조

```
llm-wiki/
├── CLAUDE.md                    # 에이전트 공통 운영 규칙 — 두 모드, 스킬 라우팅, 언어 규칙
├── .claude/skills/              # 위키 스킬 5종
│   ├── wiki-ingest/             #   자료 흡수
│   ├── wiki-query/              #   질의 + 답변 보존
│   ├── wiki-lint/               #   점검
│   ├── wiki-refresh/            #   최신화 (사람 확인 게이트)
│   └── wiki-delete/             #   삭제 (파괴적)
│
├── raw/                         # 원본 자료 31건 — 읽기 전용, 비공개 중첩 저장소
│                                #   (여기엔 docs/raw-manifest.txt 목록만 존재)
├── wiki/                        # 에이전트가 쓰고 고치는 결과물 (79쪽)
│   ├── sources/                 #   자료별 요약 31쪽 (raw 1건 = 1쪽)
│   ├── concepts/                #   개념·주제 22쪽
│   ├── entities/                #   인물·조직·제품 21쪽
│   ├── analysis/                #   남길 가치가 있는 비교·분석 3쪽
│   └── index.md, overview.md    #   전체 목록과 도메인 개관
│
├── site/
│   ├── build.py                 # wiki/*.md → 정적 HTML + Pagefind 검색 (단일 스크립트)
│   ├── style.css                # 스타일 전부 (Pretendard, 한국어 줄바꿈)
│   ├── requirements.txt         # markdown-it-py 하나
│   └── test_build_site.py       # 빌드 산출물 불변식 테스트
├── scripts/
│   ├── lint_wiki.py             # 스키마 · 링크 · 고아 · raw↔sources 1:1 검사
│   ├── verify_site.py           # 발행 경계 감사 (원본 유출 · 절대경로 · 미해석 링크)
│   └── test_lint_wiki.py        # 골든/결함 픽스처 러너
├── tests/fixtures/              # golden-wiki(통과) + defects/(검사별 빨간 변형)
├── infra/                       # Terraform — S3 · CloudFront · ACM · Route 53 · OIDC 역할
├── .github/workflows/
│   ├── verify.yml               # PR 게이트 (verify · lint, paths 필터 없음)
│   └── deploy.yml               # main 배포 (lint → build → 감사 → S3 → 무효화)
└── docs/                        # 운영 문서 — 규칙 2종 · 단계별 계획 15개 · 작업 로그
```

## 🏗 아키텍처

![아키텍처](docs/architecture.svg)

## 🔐 원본 격리 경계

`raw/`에 기록되는 파일들은 제3자 저작물이라 이 공개 저장소에 포함하지 않습니다.

## 📚 문서

| | |
|---|---|
| [운영 규칙](CLAUDE.md) | 에이전트 공통 규칙 — 두 가지 모드, 스킬 라우팅, 언어 규칙 |
| [콘텐츠 규칙](docs/rules/wiki-content.md) | 페이지 작성 · 분류 · 쉬운글 규칙 · 인덱스 유지 |
| [사이트/코드 규칙](docs/rules/site-code.md) | 빌드 · 배포 · 검증 순서와 누적된 제약 |
| [문서 카탈로그](docs/index.md) | `docs/` 아래 전체 목록과 단계별 계획 15개 |
| [작업 로그](docs/log.md) | 날짜별 작업 이력 (append-only) |

## 📝 라이선스

| 대상 | 라이선스 |
|---|---|
| 코드 — `scripts/`, `site/`, `infra/`, `.github/`, `.claude/` | [MIT](LICENSE) |
| 위키 산문 — `wiki/` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ko) |

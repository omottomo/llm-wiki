# llm-wiki

에이전트가 사서(librarian) 역할을 맡아 운영하는 개인 지식 위키. 읽은 자료를 그때그때
요약하고 버리는 대신, 구조화된 위키 페이지로 **누적**하고 서로 연결한 뒤 정적 사이트로
발행한다.

읽을 수 있는 결과물: **<https://omotomo-llm-wiki.com>**

## 파이프라인

```
raw/  →  wiki/  →  site/dist/
```

1. **`raw/`** — 원본 자료(영상 자막, 기사, 문서)를 그대로 보관한다. 읽기 전용이고 절대 수정하지 않는다.
2. **`wiki/`** — 에이전트가 원본을 읽고 쓰는 곳. `sources/`(자료별 요약)·`concepts/`·`entities/`·`analysis/`로 나뉘며, 원본 1건에 요약 페이지 1쪽이 1:1로 대응한다. 새 자료가 기존 서술과 충돌하면 지우지 않고 양쪽을 남긴 뒤 모순으로 표시한다.
3. **`site/`** — `build.py`가 `wiki/*.md`만 읽어 정적 HTML로 렌더하고 Pagefind 전문 검색을 붙인다. 프레임워크 없는 단일 파이썬 스크립트. AWS S3 + CloudFront로 배포된다.

운영 규칙은 [`CLAUDE.md`](CLAUDE.md)와 [`docs/rules/`](docs/rules/)에, 작업 이력은
[`docs/log.md`](docs/log.md)에 있다.

## 원본 자료는 이 저장소에 없다

`raw/`는 제3자 저작물(타인의 영상 자막·기사 전문)이라 공개 저장소에 포함하지 않는다.
별도 비공개 저장소로 분리돼 있고, 이 저장소에는 파일 이름 목록만
[`docs/raw-manifest.txt`](docs/raw-manifest.txt)로 남아 `raw ↔ wiki/sources` 1:1 검사가
원본 없이도 돌아간다. `scripts/verify_site.py`가 `raw/`가 다시 추적되는 순간 빌드를 실패시킨다.

## 라이선스

성격이 다른 두 가지가 한 저장소에 있어 라이선스도 둘로 나뉜다.

| 대상 | 라이선스 |
|---|---|
| 코드 — `scripts/`, `site/`, `infra/`, `.github/`, `.claude/`, `tests/` | [MIT](LICENSE) |
| 위키 산문 — `wiki/` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ko) |

`wiki/` 페이지는 남의 영상과 글을 근거로 쓴 요약·재구성이고 모든 쪽이 frontmatter에
출처를 달고 있다. 그래서 출처 표시를 요구하는 CC BY를 쓴다.

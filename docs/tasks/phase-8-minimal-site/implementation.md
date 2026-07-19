# Phase 8 — Minimal Search-First Site: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `web/` — a hand-rolled minimal static site (search-first home, article pages with wikilinks/backlinks, tag pages, dark mode, Pagefind Korean full-text search) replacing both Quartz sites.

**Architecture:** One Python generator (`web/build.py`) that imports parsing helpers from `scripts/lint_wiki.py`, renders `wiki/*.md` through `markdown-it-py` into `web/dist/`, with templates as f-strings and all design in one hand-written `web/style.css`. Pagefind indexes `dist/` post-build. Design spec: `docs/tasks/phase-8-minimal-site/plan.md`.

**Tech Stack:** Python 3 (repo has 3.14), `markdown-it-py` (only pip dependency), Pagefind v1 via `npx` (build-time only, node 22 available), Cloudflare Pages.

## Global Constraints

- All visible site text (labels, headings, UI copy) is **Korean**; code/comments follow repo style (Korean docstrings match `scripts/` convention).
- **Never read or publish `raw/`** — the generator reads only `wiki/`; leak audit gates every build (CLAUDE.md core principle 1).
- Coding discipline per `docs/rules/site-code.md` §1: minimum code, surgical changes, no speculative flexibility.
- Verification order per site-code.md: lint → build → verify_site.py.
- Dependencies capped at: `markdown-it-py` (pip), `pagefind@1` (npx). Nothing else.
- Design language locked by spec §5: cold monochrome, one steel-blue accent, Pretendard, no cards, no animations, WCAG AA in both modes.
- Features locked by spec: wikilinks+backlinks, tags, dark mode. NO graph view, NO TOC.
- `wiki/` prose is never modified in this phase (content mode is out of scope).
- Each task ends with its test green, then a commit. Commit messages: conventional (`feat:`/`fix:`/`ci:`), Korean or English body per repo history.

---

### Task T01: Scaffold + core generator (article pages render)

**Files:**
- Create: `web/requirements.txt`
- Create: `web/build.py`
- Create: `web/test_build_site.py`
- Modify: `.gitignore` (add `web/dist/`)

**Interfaces:**
- Consumes: `scripts/lint_wiki.py` — `wiki_pages() -> list[Path]`, `page_key(Path) -> str` (`wiki/concepts/foo.md` → `"concepts/foo"`), `parse_frontmatter(str) -> dict|None`, `split_body(str) -> str`.
- Produces (later tasks rely on these exact names in `web/build.py`):
  - `load_pages() -> dict[str, dict]` — key → `{"key","title","type","updated","tags","body"}`
  - `parse_tags(value: str) -> list[str]`
  - `url_for(key: str) -> str` — `"concepts/mcp"` → `"/concepts/mcp/"` (percent-encoded)
  - `base_html(title: str, content: str) -> str`
  - `render_article(page: dict) -> str` (signature grows in T02)
  - `write_page(rel: str, html_text: str) -> None` — writes `dist/<rel>/index.html`
  - `main() -> int`
  - module constants `ROOT`, `WIKI`, `WEB`, `DIST`, `SITE_NAME`, `md`

- [ ] **Step 1: Install the build dependency and pin it**

```bash
pip3 install markdown-it-py
```

Create `web/requirements.txt` (check installed version with `pip3 show markdown-it-py`; pin what you got, e.g.):

```
markdown-it-py==4.0.0
```

- [ ] **Step 2: Write the failing test**

Create `web/test_build_site.py`:

```python
#!/usr/bin/env python3
"""web/build.py 불변식 테스트 — stdlib만 사용, scripts/test_lint_wiki.py와 같은 assert 러너.

사용법: python3 web/test_build_site.py   (빌드를 실제로 실행한 뒤 dist/를 검사)
종료 코드: 전부 통과 0, 아니면 traceback과 함께 비0.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "web" / "dist"

sys.path.insert(0, str(ROOT / "web"))
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402  (web/build.py — import 시 부수효과 없어야 한다)


def run_build() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "web" / "build.py")], capture_output=True, text=True
    )
    assert r.returncode == 0, f"build 실패:\n{r.stdout}\n{r.stderr}"


def test_all_articles_built() -> None:
    """wiki/의 모든 .md가 dist/<key>/index.html로 렌더된다."""
    for md_path in (ROOT / "wiki").rglob("*.md"):
        key = str(md_path.relative_to(ROOT / "wiki").with_suffix(""))
        out = DIST / key / "index.html"
        assert out.is_file(), f"누락: {out}"


def test_article_has_title_and_body() -> None:
    text = (DIST / "concepts" / "mcp" / "index.html").read_text(encoding="utf-8")
    assert "<title>MCP (모델 컨텍스트 프로토콜) · LLM 위키</title>" in text
    assert "MCP" in text  # 본문 렌더 확인


if __name__ == "__main__":
    run_build()
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"PASS {name}")
    print("모든 테스트 통과")
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python3 web/test_build_site.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'build'` (build.py doesn't exist yet).

- [ ] **Step 4: Write the generator core**

Create `web/build.py`:

```python
#!/usr/bin/env python3
"""wiki/ → web/dist/ 미니멀 정적 사이트 생성기 (phase-8).

빌드:        python3 web/build.py
검색 인덱스:  npx -y pagefind@1 --site web/dist   (빌드 후)

파싱은 scripts/lint_wiki.py의 검증된 헬퍼를 재사용한다. 템플릿은 f-string,
디자인은 web/style.css 하나. raw/는 절대 읽지 않는다.
"""
import html
import shutil
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import lint_wiki  # noqa: E402

from markdown_it import MarkdownIt  # noqa: E402

WIKI = ROOT / "wiki"
WEB = ROOT / "web"
DIST = WEB / "dist"
SITE_NAME = "LLM 위키"

# html=True: 위키 본문은 운영자 자신이 쓴 신뢰 콘텐츠라 인라인 HTML 허용
md = MarkdownIt("commonmark", {"html": True}).enable("table").enable("strikethrough")


def parse_tags(value: str) -> list[str]:
    """frontmatter 인라인 리스트 '[a, b]' → ['a', 'b']. 형식이 아니면 빈 리스트."""
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return []
    return [t.strip() for t in value[1:-1].split(",") if t.strip()]


def load_pages() -> dict[str, dict]:
    pages = {}
    for path in lint_wiki.wiki_pages():
        text = path.read_text(encoding="utf-8")
        fm = lint_wiki.parse_frontmatter(text) or {}
        key = lint_wiki.page_key(path)
        pages[key] = {
            "key": key,
            "title": fm.get("title", key),
            "type": fm.get("type", ""),
            "updated": fm.get("updated", ""),
            "tags": parse_tags(fm.get("tags", "")),
            "body": lint_wiki.split_body(text),
        }
    return pages


def url_for(key: str) -> str:
    return "/" + urllib.parse.quote(key) + "/"


def base_html(title: str, content: str) -> str:
    head_title = SITE_NAME if title == SITE_NAME else f"{title} · {SITE_NAME}"
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(head_title)}</title>
</head>
<body>
<header class="site-header"><a class="site-name" href="/">{SITE_NAME}</a></header>
{content}
</body>
</html>"""


def render_article(page: dict) -> str:
    body_html = md.render(page["body"])
    updated = f'<p class="meta">갱신 {page["updated"]}</p>' if page["updated"] else ""
    return base_html(page["title"], f"<main><article>{updated}\n{body_html}</article></main>")


def write_page(rel: str, html_text: str) -> None:
    out = DIST / rel / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")


def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    pages = load_pages()
    for page in pages.values():
        write_page(page["key"], render_article(page))
    print(f"기사 {len(pages)}쪽 생성 → {DIST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Note: `wiki/index.md` lands at `dist/index/index.html` (= route `/index/`, the full catalog per spec §4). The home page at `dist/index.html` comes in T03 — no collision.

- [ ] **Step 5: Add `web/dist/` to `.gitignore`**

Read `.gitignore`, append:

```
web/dist/
```

- [ ] **Step 6: Run test to verify it passes**

Run: `python3 web/test_build_site.py`
Expected: `PASS test_all_articles_built`, `PASS test_article_has_title_and_body`, `모든 테스트 통과`, exit 0. (67 wiki pages build; count printed by build.py.)

- [ ] **Step 7: Commit**

```bash
git add web/build.py web/test_build_site.py web/requirements.txt .gitignore
git commit -m "feat(web): phase-8 T01 — minimal generator core, article pages render"
```

---

### Task T02: Wikilinks + backlinks + dead-link handling

**Files:**
- Modify: `web/build.py` (add `link_wikilinks`; extend `render_article`, `main`)
- Modify: `web/test_build_site.py` (3 new tests)

**Interfaces:**
- Consumes: `lint_wiki.WIKILINK_RE` (`\[\[([^\]]+)\]\]`), `lint_wiki.normalize_target(str) -> str` (strips `\|`-alias and `#section`), `lint_wiki.build_inbound_map(pages: list[Path]) -> dict[str, set[str]]` (key format identical to `page_key`).
- Produces:
  - `link_wikilinks(body: str, existing) -> str` — `existing` is any container of page keys
  - `render_article(page: dict, pages: dict, inbound: dict) -> str` (signature CHANGES from T01)

- [ ] **Step 1: Write the failing tests**

Append to `web/test_build_site.py`:

```python
def test_no_literal_wikilinks() -> None:
    """어떤 출력 HTML에도 '[[' 리터럴이 남지 않는다 (verify_site.py와 같은 기준)."""
    offenders = [
        p.relative_to(DIST)
        for p in DIST.rglob("*.html")
        if "[[" in p.read_text(encoding="utf-8")
    ]
    assert not offenders, f"미해석 위키링크: {offenders[:5]}"


def test_wikilinks_resolve_and_backlinks_render() -> None:
    """overview는 harness-engineering을 링크하므로: (a) overview HTML에 해당 href가 있고
    (b) harness-engineering 페이지의 백링크 목록에 overview가 나타난다."""
    overview = (DIST / "overview" / "index.html").read_text(encoding="utf-8")
    assert 'href="/concepts/harness-engineering/"' in overview
    harness = (DIST / "concepts" / "harness-engineering" / "index.html").read_text(encoding="utf-8")
    assert "이 문서를 참조하는 문서" in harness
    assert 'href="/overview/"' in harness


def test_dead_wikilink_renders_muted() -> None:
    """대상 없는 위키링크는 <a>가 아니라 회색 <span>으로 렌더된다 (단위 테스트)."""
    out = build.link_wikilinks("[[없는페이지|라벨]]", set())
    assert out == '<span class="dead-link">라벨</span>'
    out2 = build.link_wikilinks("[[concepts/mcp|MCP]]", {"concepts/mcp"})
    assert out2 == '<a href="/concepts/mcp/">MCP</a>'
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 web/test_build_site.py`
Expected: FAIL — `test_no_literal_wikilinks` finds `[[` in output; `test_dead_wikilink_renders_muted` raises `AttributeError: module 'build' has no attribute 'link_wikilinks'`.

- [ ] **Step 3: Implement**

In `web/build.py`, add after `url_for`:

```python
def link_wikilinks(body: str, existing) -> str:
    """[[대상|별칭]]을 <a>로, 대상 없는 링크는 회색 <span>으로 치환한다.
    markdown 렌더 전에 실행되며 html=True라 그대로 통과한다."""
    # ponytail: 코드 펜스 안의 [[..]]도 치환된다. 현재 위키에 해당 사례 0건,
    # 생기면 lint_wiki.FENCE_RE로 펜스를 보호하는 전처리 추가.
    def repl(m):
        raw = m.group(1).replace("\\|", "|")
        target = lint_wiki.normalize_target(m.group(1))
        label = raw.split("|", 1)[1].strip() if "|" in raw else target
        if target in existing:
            return f'<a href="{url_for(target)}">{html.escape(label)}</a>'
        return f'<span class="dead-link">{html.escape(label)}</span>'

    return lint_wiki.WIKILINK_RE.sub(repl, body)
```

Replace `render_article` with:

```python
def render_article(page: dict, pages: dict, inbound: dict) -> str:
    body_html = md.render(link_wikilinks(page["body"], pages))
    updated = f'<p class="meta">갱신 {page["updated"]}</p>' if page["updated"] else ""
    back = sorted(inbound.get(page["key"], set()))
    back_html = ""
    if back:
        items = "\n".join(
            f'<li><a href="{url_for(k)}">{html.escape(pages[k]["title"])}</a></li>'
            for k in back
        )
        back_html = (
            '<section class="backlinks"><h2>이 문서를 참조하는 문서</h2>'
            f"<ul>{items}</ul></section>"
        )
    return base_html(
        page["title"],
        f"<main><article>{updated}\n{body_html}</article>\n{back_html}</main>",
    )
```

In `main()`, replace the render loop:

```python
    pages = load_pages()
    inbound = lint_wiki.build_inbound_map(lint_wiki.wiki_pages())
    for page in pages.values():
        write_page(page["key"], render_article(page, pages, inbound))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 web/test_build_site.py`
Expected: all PASS (T01 tests + 3 new), exit 0.

- [ ] **Step 5: Commit**

```bash
git add web/build.py web/test_build_site.py
git commit -m "feat(web): phase-8 T02 — wikilink resolution, backlinks, dead-link muting"
```

---

### Task T03: Home, section listings, tag pages, 404

**Files:**
- Modify: `web/build.py` (add `SECTIONS`, `tag_url`, `collect_tags`, `render_listing`, `render_home`, `render_404`; extend `render_article` with tag chips; extend `main`)
- Modify: `web/test_build_site.py` (3 new tests)

**Interfaces:**
- Produces:
  - `SECTIONS = [("concepts", "개념"), ("entities", "엔티티"), ("sources", "출처"), ("analysis", "분석")]`
  - `tag_url(tag: str) -> str` — `"/tags/<quoted>/"`
  - `collect_tags(pages: dict) -> dict[str, list[str]]` — tag → page keys
  - `render_listing(title: str, keys, pages: dict) -> str` — shared by section listings and tag pages
  - `render_home(pages: dict) -> str`, `render_404() -> str`
- Routes added: `/` (home), `/concepts/` `/entities/` `/sources/` `/analysis/` (listings), `/tags/<tag>/`, `/404.html`.

- [ ] **Step 1: Write the failing tests**

Append to `web/test_build_site.py`:

```python
def test_home_page() -> None:
    text = (DIST / "index.html").read_text(encoding="utf-8")
    assert '<div id="search">' in text          # 검색 중심 첫 화면
    assert "최근 갱신" in text
    for href in ["/overview/", "/concepts/", "/sources/", "/analysis/", "/index/"]:
        assert f'href="{href}"' in text, f"홈 진입점 누락: {href}"


def test_section_listing_and_tag_page() -> None:
    concepts = (DIST / "concepts" / "index.html").read_text(encoding="utf-8")
    assert 'href="/concepts/mcp/"' in concepts
    tag_mcp = (DIST / "tags" / "MCP" / "index.html").read_text(encoding="utf-8")
    assert 'href="/concepts/mcp/"' in tag_mcp   # concepts/mcp의 tags에 MCP 존재


def test_404_page() -> None:
    text = (DIST / "404.html").read_text(encoding="utf-8")
    assert '<div id="search">' in text
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 web/test_build_site.py`
Expected: FAIL — `dist/index.html` missing (`FileNotFoundError`).

- [ ] **Step 3: Implement**

In `web/build.py`, add after `SITE_NAME`:

```python
SECTIONS = [("concepts", "개념"), ("entities", "엔티티"), ("sources", "출처"), ("analysis", "분석")]
```

Add after `url_for`:

```python
def tag_url(tag: str) -> str:
    return "/tags/" + urllib.parse.quote(tag) + "/"


def collect_tags(pages: dict) -> dict[str, list[str]]:
    tags: dict[str, list[str]] = {}
    for p in pages.values():
        for t in p["tags"]:
            tags.setdefault(t, []).append(p["key"])
    return tags
```

Add the three templates:

```python
def render_listing(title: str, keys, pages: dict) -> str:
    items = "\n".join(
        f'<li><a href="{url_for(k)}">{html.escape(pages[k]["title"])}</a>'
        f'<span class="meta">{pages[k]["updated"]}</span></li>'
        for k in sorted(keys, key=lambda k: pages[k]["title"])
    )
    return base_html(
        title, f'<main><h1>{html.escape(title)}</h1><ul class="listing">{items}</ul></main>'
    )


def render_home(pages: dict) -> str:
    def count(prefix: str) -> int:
        return sum(1 for k in pages if k.startswith(prefix + "/"))

    entries = (
        [("/overview/", "개요", None)]
        + [(f"/{s}/", label, count(s)) for s, label in SECTIONS]
        + [("/index/", "전체 색인", None)]
    )
    entry_html = "\n".join(
        f'<a class="entry" href="{u}">{label}'
        + (f' <span class="count">{n}</span>' if n is not None else "")
        + "</a>"
        for u, label, n in entries
    )
    recent = sorted(
        (p for p in pages.values() if "/" in p["key"]),  # index/overview 제외
        key=lambda p: p["updated"],
        reverse=True,
    )[:5]
    recent_html = "\n".join(
        f'<li><a href="{url_for(p["key"])}">{html.escape(p["title"])}</a>'
        f'<span class="meta">{p["updated"]}</span></li>'
        for p in recent
    )
    content = f"""<main class="home">
<h1>{SITE_NAME}</h1>
<div id="search"></div>
<nav class="entries">{entry_html}</nav>
<section class="recent"><h2>최근 갱신</h2><ul>{recent_html}</ul></section>
</main>"""
    return base_html(SITE_NAME, content)


def render_404() -> str:
    content = f"""<main class="home">
<h1>페이지가 없습니다</h1>
<p class="meta">주소를 확인하거나 검색해 보세요.</p>
<div id="search"></div>
<p><a href="/">{SITE_NAME} 홈으로</a></p>
</main>"""
    return base_html("페이지 없음", content)
```

Extend `render_article` — insert tag chips between `{body_html}` and `</article>`:

```python
    tags_html = ""
    if page["tags"]:
        chips = " ".join(
            f'<a class="tag" href="{tag_url(t)}">{html.escape(t)}</a>' for t in page["tags"]
        )
        tags_html = f'<footer class="tags">{chips}</footer>'
    return base_html(
        page["title"],
        f"<main><article>{updated}\n{body_html}\n{tags_html}</article>\n{back_html}</main>",
    )
```

Extend `main()` after the article loop:

```python
    for s, label in SECTIONS:
        write_page(s, render_listing(label, [k for k in pages if k.startswith(s + "/")], pages))
    for tag, keys in collect_tags(pages).items():
        write_page(f"tags/{tag}", render_listing(f"태그: {tag}", keys, pages))
    (DIST / "index.html").write_text(render_home(pages), encoding="utf-8")
    (DIST / "404.html").write_text(render_404(), encoding="utf-8")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 web/test_build_site.py`
Expected: all PASS, exit 0.

- [ ] **Step 5: Commit**

```bash
git add web/build.py web/test_build_site.py
git commit -m "feat(web): phase-8 T03 — search-first home, section listings, tag pages, 404"
```

---

### Task T04: Design — style.css, page chrome, dark mode

**Files:**
- Create: `web/style.css`
- Modify: `web/build.py` (`base_html` gains stylesheet link, theme script, header toggle; `main` copies CSS)
- Modify: `web/test_build_site.py` (1 new test)

**Interfaces:**
- Produces: `dist/style.css`; `<html>` uses `data-theme` attribute (`"light"`/`"dark"`, absent = system); toggle button `id="theme-toggle"`.
- Design tokens (locked): light `--bg:#fafafa --text:#16181c --muted:#697077 --line:#e2e4e8 --accent:#3b6ea5`; dark `--bg:#111214 --text:#d9dce1 --muted:#8b919a --line:#26282d --accent:#7da7d9`. All pairs pass WCAG AA.

- [ ] **Step 1: Write the failing test**

Append to `web/test_build_site.py`:

```python
def test_design_chrome() -> None:
    assert (DIST / "style.css").is_file()
    article = (DIST / "concepts" / "mcp" / "index.html").read_text(encoding="utf-8")
    assert '<link rel="stylesheet" href="/style.css">' in article
    assert 'id="theme-toggle"' in article           # 다크모드 토글
    assert "localStorage.getItem" in article        # FOUC 방지 테마 스크립트
    css = (DIST / "style.css").read_text(encoding="utf-8")
    assert "--accent" in css and "Pretendard" in css
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 web/test_build_site.py`
Expected: FAIL — `dist/style.css` missing.

- [ ] **Step 3: Write `web/style.css`**

```css
/* LLM 위키 — cold monochrome, 단일 강조색(스틸 블루). 디자인 전체가 이 파일 하나. */
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css");

:root {
  --bg: #fafafa;
  --text: #16181c;
  --muted: #697077;
  --line: #e2e4e8;
  --accent: #3b6ea5;
  --code-bg: #f0f1f3;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #111214; --text: #d9dce1; --muted: #8b919a;
    --line: #26282d; --accent: #7da7d9; --code-bg: #1a1c1f;
  }
}
:root[data-theme="dark"] {
  --bg: #111214; --text: #d9dce1; --muted: #8b919a;
  --line: #26282d; --accent: #7da7d9; --code-bg: #1a1c1f;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: "Pretendard Variable", Pretendard, -apple-system, sans-serif;
  font-size: 17px;
  line-height: 1.75;
  word-break: keep-all;
}
a { color: var(--accent); text-decoration: none; transition: opacity 0.15s; }
a:hover { opacity: 0.75; }

/* ── 헤더: 얇게, 사이트명 + 토글만 ───────────────────────── */
.site-header {
  display: flex; align-items: center; justify-content: space-between;
  max-width: 46rem; margin: 0 auto; padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--line);
}
.site-name { color: var(--text); font-weight: 700; }
#theme-toggle {
  background: none; border: 1px solid var(--line); border-radius: 6px;
  color: var(--muted); cursor: pointer; padding: 0.2rem 0.6rem; font: inherit;
  font-size: 0.85rem;
}
#theme-toggle:hover { color: var(--text); }

/* ── 본문: 68ch 중앙, 카드 없음, hairline 구분 ───────────── */
main { max-width: 46rem; margin: 0 auto; padding: 2.5rem 1.25rem 5rem; }
article h1 { font-size: 1.7rem; line-height: 1.35; margin: 0 0 1.5rem; }
article h2 { font-size: 1.25rem; margin: 2.5rem 0 0.75rem; }
article h3 { font-size: 1.05rem; margin: 2rem 0 0.5rem; }
article p { max-width: 68ch; }
article blockquote {
  margin: 1.5rem 0; padding: 0 1.25rem;
  border-left: 2px solid var(--line); color: var(--muted);
}
article table { border-collapse: collapse; display: block; overflow-x: auto; }
article th, article td { border: 1px solid var(--line); padding: 0.4rem 0.75rem; }
article code {
  font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, monospace;
  font-size: 0.88em; background: var(--code-bg);
  padding: 0.1em 0.35em; border-radius: 4px;
}
article pre { background: var(--code-bg); padding: 1rem; border-radius: 6px; overflow-x: auto; }
article pre code { background: none; padding: 0; }
.meta { color: var(--muted); font-size: 0.85rem; }
.dead-link { color: var(--muted); border-bottom: 1px dotted var(--muted); }

/* ── 태그 · 백링크 ───────────────────────────────────────── */
.tags { margin-top: 3rem; padding-top: 1.25rem; border-top: 1px solid var(--line); }
.tag { font-size: 0.85rem; color: var(--muted); margin-right: 0.75rem; }
.tag:hover { color: var(--accent); }
.backlinks { margin-top: 2.5rem; }
.backlinks h2 { font-size: 0.95rem; color: var(--muted); font-weight: 600; }
.backlinks ul { list-style: none; padding: 0; }
.backlinks li { padding: 0.3rem 0; }

/* ── 홈: 검색 중심 ───────────────────────────────────────── */
.home { text-align: center; padding-top: 14vh; }
.home h1 { font-size: 2rem; margin-bottom: 2rem; }
.home #search { max-width: 34rem; margin: 0 auto 2.5rem; text-align: left; }
.entries { display: flex; flex-wrap: wrap; gap: 0.6rem; justify-content: center; }
.entry {
  border: 1px solid var(--line); border-radius: 999px;
  padding: 0.35rem 1rem; color: var(--text); font-size: 0.9rem;
}
.entry:hover { border-color: var(--accent); color: var(--accent); opacity: 1; }
.entry .count { color: var(--muted); font-size: 0.8rem; }
.recent { margin-top: 4rem; text-align: left; }
.recent h2 { font-size: 0.95rem; color: var(--muted); font-weight: 600; }
.recent ul, .listing { list-style: none; padding: 0; }
.recent li, .listing li {
  display: flex; justify-content: space-between; gap: 1rem;
  padding: 0.55rem 0; border-bottom: 1px solid var(--line);
}

/* ── Pagefind UI를 팔레트에 맞춤 ─────────────────────────── */
:root {
  --pagefind-ui-scale: 0.9;
  --pagefind-ui-primary: var(--accent);
  --pagefind-ui-text: var(--text);
  --pagefind-ui-background: var(--bg);
  --pagefind-ui-border: var(--line);
  --pagefind-ui-border-width: 1px;
  --pagefind-ui-border-radius: 8px;
  --pagefind-ui-font: "Pretendard Variable", Pretendard, sans-serif;
}
```

- [ ] **Step 4: Wire the chrome into `base_html` and copy the CSS**

Replace `base_html` in `web/build.py`:

```python
def base_html(title: str, content: str) -> str:
    head_title = SITE_NAME if title == SITE_NAME else f"{title} · {SITE_NAME}"
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(head_title)}</title>
<link rel="stylesheet" href="/style.css">
<script>const t = localStorage.getItem("theme"); if (t) document.documentElement.dataset.theme = t;</script>
</head>
<body>
<header class="site-header">
<a class="site-name" href="/">{SITE_NAME}</a>
<button id="theme-toggle" aria-label="테마 전환">명암</button>
</header>
{content}
<script>
document.querySelector("#theme-toggle").addEventListener("click", () => {{
  const root = document.documentElement;
  const cur = root.dataset.theme
    || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  const next = cur === "dark" ? "light" : "dark";
  root.dataset.theme = next;
  localStorage.setItem("theme", next);
}});
</script>
</body>
</html>"""
```

(Note the doubled `{{ }}` inside the f-string for literal braces.)

In `main()`, before the final `print`:

```python
    shutil.copy(WEB / "style.css", DIST / "style.css")
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 web/test_build_site.py`
Expected: all PASS, exit 0.

- [ ] **Step 6: Visual smoke check (agent-side, not the human QA gate)**

```bash
cd web/dist && python3 -m http.server 8123
```

Open `http://localhost:8123/` — confirm: home renders search-first, article typography readable, toggle switches theme without flash. Stop the server. (Full visual QA is T07, human.)

- [ ] **Step 7: Commit**

```bash
git add web/style.css web/build.py web/test_build_site.py
git commit -m "feat(web): phase-8 T04 — cold-monochrome design, Pretendard, dark-mode toggle"
```

---

### Task T05: Pagefind search integration

**Files:**
- Modify: `web/build.py` (`base_html` gains Pagefind assets + init; `render_article` marks `data-pagefind-body`)
- Modify: `web/test_build_site.py` (2 new tests; runner gains a pagefind step)

**Interfaces:**
- Consumes: Pagefind v1 CLI (`npx -y pagefind@1 --site web/dist`) — generates `dist/pagefind/pagefind-ui.js`, `pagefind-ui.css`, index files.
- Produces: every page's `<head>` loads `/pagefind/pagefind-ui.css` + `/pagefind/pagefind-ui.js`; init script instantiates `PagefindUI` on `#search` when present; article pages (except the `/index/` catalog — noise) carry `data-pagefind-body`.

- [ ] **Step 1: Write the failing tests**

Append to `web/test_build_site.py`:

```python
def test_pagefind_wiring() -> None:
    home = (DIST / "index.html").read_text(encoding="utf-8")
    assert "/pagefind/pagefind-ui.js" in home
    assert "new PagefindUI" in home
    mcp = (DIST / "concepts" / "mcp" / "index.html").read_text(encoding="utf-8")
    assert "data-pagefind-body" in mcp
    catalog = (DIST / "index" / "index.html").read_text(encoding="utf-8")
    assert "data-pagefind-body" not in catalog  # 색인 페이지는 검색 노이즈라 제외


def test_pagefind_index_built() -> None:
    """npx가 있으면 인덱스 생성까지 검증, 없으면 SKIP (CI에는 node 22 존재)."""
    import shutil as _sh
    if not _sh.which("npx"):
        print("SKIP test_pagefind_index_built (npx 없음)")
        return
    r = subprocess.run(
        ["npx", "-y", "pagefind@1", "--site", str(DIST)], capture_output=True, text=True
    )
    assert r.returncode == 0, f"pagefind 실패:\n{r.stdout}\n{r.stderr}"
    assert (DIST / "pagefind" / "pagefind-ui.js").is_file()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 web/test_build_site.py`
Expected: FAIL — no `/pagefind/` references in HTML yet.

- [ ] **Step 3: Implement**

In `base_html`, add to `<head>` after the stylesheet link:

```html
<link rel="stylesheet" href="/pagefind/pagefind-ui.css">
<script src="/pagefind/pagefind-ui.js"></script>
```

Add before `</body>` (inside the f-string; keep `{{ }}` doubling):

```html
<script>
window.addEventListener("DOMContentLoaded", () => {{
  const el = document.querySelector("#search");
  if (el && window.PagefindUI)
    new PagefindUI({{ element: "#search", showSubResults: true, translations: {{ placeholder: "검색..." }} }});
}});
</script>
```

In `render_article`, mark the body for indexing (catalog excluded):

```python
    pagefind_attr = "" if page["key"] == "index" else " data-pagefind-body"
    return base_html(
        page["title"],
        f"<main><article{pagefind_attr}>{updated}\n{body_html}\n{tags_html}</article>\n{back_html}</main>",
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 web/test_build_site.py`
Expected: all PASS (pagefind step prints its indexing summary; Korean pages indexed), exit 0.

- [ ] **Step 5: Search smoke check**

```bash
cd web/dist && python3 -m http.server 8123
```

Open `http://localhost:8123/`, search `하네스` — expect results with Korean excerpts and highlights. Stop the server.

- [ ] **Step 6: Commit**

```bash
git add web/build.py web/test_build_site.py
git commit -m "feat(web): phase-8 T05 — Pagefind Korean full-text search on home and articles"
```

---

### Task T06: Internal link check, leak audit, CI

**Files:**
- Modify: `web/build.py` (add `HREF_RE`, `check_internal_links`; `main` fails on broken links)
- Modify: `scripts/verify_site.py` (web/ support: dist output dir + artifact list)
- Modify: `.github/workflows/verify-site.yml` (new `verify-web` job; `web/**` path trigger)
- Modify: `web/test_build_site.py` (1 new test)

**Interfaces:**
- Produces: `check_internal_links() -> list[str]` in `web/build.py` (empty list = pass); `python3 scripts/verify_site.py web` audits `web/dist`.

- [ ] **Step 1: Write the failing test**

Append to `web/test_build_site.py`:

```python
def test_verify_site_web() -> None:
    """raw/ 경계 감사가 web/dist에 대해 통과한다 (누출 0)."""
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "verify_site.py"), "web"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"verify_site 실패:\n{r.stdout}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 web/test_build_site.py`
Expected: FAIL — verify_site.py looks for `web/public` (doesn't exist → checks SKIP, but `check_artifacts_ignored` FAILs on `web/node_modules` not being git-ignored).

- [ ] **Step 3: Implement the link checker in `web/build.py`**

Add near the top (after `md = ...`):

```python
import re
HREF_RE = re.compile(r'href="(/[^"#?]*)')
```

(Move the `import re` up to the stdlib import block.)

Add after `write_page`:

```python
def check_internal_links() -> list[str]:
    """dist/ 안 모든 내부 href가 실제 파일을 가리키는지 검사. /pagefind/는 빌드 후 생성이라 제외."""
    broken = []
    for page in DIST.rglob("*.html"):
        for href in HREF_RE.findall(page.read_text(encoding="utf-8")):
            if href.startswith("/pagefind/"):
                continue
            target = DIST / urllib.parse.unquote(href).strip("/")
            if not (target.is_file() or (target / "index.html").is_file()):
                broken.append(f"{page.relative_to(DIST)}: {href}")
    return broken
```

In `main()`, before the final `print`:

```python
    broken = check_internal_links()
    if broken:
        print(f"깨진 내부 링크 {len(broken)}건:", *broken[:10], sep="\n  ", file=sys.stderr)
        return 1
```

- [ ] **Step 4: Teach `scripts/verify_site.py` about web/**

In `main()`, replace `public = site / "public"`:

```python
    # web/은 Quartz가 아니라 자체 생성기라 출력 디렉터리 이름이 다르다 (phase-8)
    public = site / ("dist" if site.name == "web" else "public")
```

In `check_artifacts_ignored`, replace the fixed list:

```python
def check_artifacts_ignored(site: Path) -> None:
    if site.name == "web":
        artifacts = [site / "dist"]
    else:
        artifacts = [site / "node_modules", site / "public", site / ".quartz"]
    for artifact in artifacts:
```

(`check_symlink` already skips non-`site/` directories; the remaining checks operate on `public` generically.)

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 web/test_build_site.py`
Expected: all PASS including `test_verify_site_web` (symlink SKIP, artifacts PASS, wikilink/leak/path/user-path checks PASS), exit 0.

Also run the full existing gate to confirm no regression:

```bash
python3 scripts/verify_site.py site && python3 scripts/lint_wiki.py && python3 scripts/test_lint_wiki.py
```

Expected: all exit 0.

- [ ] **Step 6: Add the CI job**

In `.github/workflows/verify-site.yml`, add `"web/**"` to `on.push.paths`, and append a job:

```yaml
  # phase-8 minimal site: build + invariant tests + boundary audit.
  verify-web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Setup Node
        uses: actions/setup-node@v6
        with:
          node-version: 22

      - name: Setup Python
        uses: actions/setup-python@v6
        with:
          python-version: "3"

      - name: Install build dependency
        run: pip install -r web/requirements.txt

      - name: Build web + search index + run test suite
        run: python3 web/test_build_site.py

      - name: Run raw/ boundary audit
        run: python3 scripts/verify_site.py web
```

(The test suite itself runs the build and `npx pagefind`, so the job needs no separate build step.)

- [ ] **Step 7: Commit**

```bash
git add web/build.py web/test_build_site.py scripts/verify_site.py .github/workflows/verify-site.yml
git commit -m "ci(web): phase-8 T06 — internal link check, web/ leak audit, verify-web job"
```

---

### Task T07: Deploy + human QA (manual gate)

**Files:**
- Modify: `docs/rules/site-code.md` (record the web/ build command + deploy config under "Accumulated rules" once live)
- Modify: `log.md` (ONE `site` line at phase close-out)
- Modify: `docs/index.md`, `docs/tasks/phase-8-minimal-site/prd.json` (statuses)

**Steps (human-in-the-loop; agent prepares, human clicks):**

- [ ] **Step 1: Cloudflare Pages configuration (human)**

New or repointed Pages project:
- Build command: `pip install -r web/requirements.txt && python3 web/build.py && npx -y pagefind@1 --site web/dist`
- Output directory: `web/dist`
- (Python 3 + Node are preinstalled in the CF Pages v2 build image.)

- [ ] **Step 2: Human QA checklist (the spec's manual AC — agent CANNOT self-verify)**

- First screen: does a first-time visitor immediately understand "search here"?
- Korean search feel: query `하네스`, `MCP`, `클로드` — relevant results, readable excerpts?
- Typography/readability in BOTH light and dark mode, desktop + mobile width.
- Toggle persists across reloads; no flash of wrong theme.

- [ ] **Step 3: Close out (after human approval)**

- Append ONE `site` line to `log.md` (Korean, per CLAUDE.md §2), e.g.:
  `## [DATE] site | phase-8-minimal-site — 자체 생성기 web/ 신축(검색 중심 홈·백링크·태그·다크모드·Pagefind 한국어 검색)`
- Update `prd.json` statuses and the phase row in `docs/index.md`.
- Decision gate (separate user confirmation, NOT part of this task): delete `site/`, `site-test/` and their CI matrix entries.

---

## Self-Review Notes

- **Spec coverage:** spec §3 architecture → T01; §4 routes → T01 (articles+catalog), T03 (home/listings/tags/404); §5 design → T04; §6 search → T05; §7 edge cases → T02 (dangling links, double-title avoidance via body-h1 rendering), T01 (frontmatter title in `<title>` only), T03 (Korean tag URLs), T01 (dates); §8 verification 1–4 → T01/T06, §8.5 human QA → T07. Section listing pages (`/concepts/` etc.) are an addition the spec's home entry points imply — noted as deviation-by-necessity (entry points need a target).
- **Type consistency:** `render_article(page, pages, inbound)` after T02; `render_listing(title, keys, pages)` shared by T03 twice; `link_wikilinks(body, existing)` unit-tested in T02 with both container types (set literal). `write_page(rel, html_text)` used for articles, listings, tags; home/404 write directly to `DIST` root.
- **Known ceilings (deliberate):** wikilinks inside code fences would be rewritten (ponytail comment in T02; zero occurrences today). Recent-5 sort is lexical on `updated` (ISO dates — correct). Pretendard via jsdelivr CDN (self-hosting is a follow-up if offline/perf demands).

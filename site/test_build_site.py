#!/usr/bin/env python3
"""site/build.py 불변식 테스트 — stdlib만 사용, scripts/test_lint_wiki.py와 같은 assert 러너.

사용법: python3 site/test_build_site.py   (빌드를 실제로 실행한 뒤 dist/를 검사)
종료 코드: 전부 통과 0, 아니면 traceback과 함께 비0.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"

sys.path.insert(0, str(ROOT / "site"))
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402  (site/build.py — import 시 부수효과 없어야 한다)


def run_build() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "site" / "build.py")], capture_output=True, text=True
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


def test_design_chrome() -> None:
    assert (DIST / "style.css").is_file()
    article = (DIST / "concepts" / "mcp" / "index.html").read_text(encoding="utf-8")
    assert '<link rel="stylesheet" href="/style.css">' in article
    assert 'id="theme-toggle"' in article           # 다크모드 토글
    assert "localStorage.getItem" in article        # FOUC 방지 테마 스크립트
    css = (DIST / "style.css").read_text(encoding="utf-8")
    assert "--accent" in css and "Pretendard" in css


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


def test_verify_site() -> None:
    """raw/ 경계 감사가 site/dist에 대해 통과한다 (누출 0)."""
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "verify_site.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"verify_site 실패:\n{r.stdout}"


if __name__ == "__main__":
    run_build()
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"PASS {name}")
    print("모든 테스트 통과")

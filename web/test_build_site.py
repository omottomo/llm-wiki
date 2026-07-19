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


if __name__ == "__main__":
    run_build()
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"PASS {name}")
    print("모든 테스트 통과")

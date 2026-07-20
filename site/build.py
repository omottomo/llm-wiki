#!/usr/bin/env python3
"""wiki/ → site/dist/ 미니멀 정적 사이트 생성기 (phase-8).

빌드:        python3 site/build.py
검색 인덱스:  npx -y pagefind@1 --site site/dist   (빌드 후)

파싱은 scripts/lint_wiki.py의 검증된 헬퍼를 재사용한다. 템플릿은 f-string,
디자인은 site/style.css 하나. raw/는 절대 읽지 않는다.
"""
import html
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import lint_wiki  # noqa: E402

from markdown_it import MarkdownIt  # noqa: E402

WIKI = ROOT / "wiki"
SITE = ROOT / "site"
DIST = SITE / "dist"
SITE_NAME = "LLM 위키"
SECTIONS = [("concepts", "개념"), ("entities", "엔티티"), ("sources", "출처"), ("analysis", "분석")]

# html=True: 위키 본문은 운영자 자신이 쓴 신뢰 콘텐츠라 인라인 HTML 허용
md = MarkdownIt("commonmark", {"html": True}).enable("table").enable("strikethrough")

HREF_RE = re.compile(r'href="(/[^"#?]*)')


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


def tag_url(tag: str) -> str:
    return "/tags/" + urllib.parse.quote(tag) + "/"


def collect_tags(pages: dict) -> dict[str, list[str]]:
    tags: dict[str, list[str]] = {}
    for p in pages.values():
        for t in p["tags"]:
            tags.setdefault(t, []).append(p["key"])
    return tags


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


def base_html(title: str, content: str) -> str:
    head_title = SITE_NAME if title == SITE_NAME else f"{title} · {SITE_NAME}"
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(head_title)}</title>
<link rel="stylesheet" href="/pagefind/pagefind-ui.css">
<link rel="stylesheet" href="/style.css">
<script src="/pagefind/pagefind-ui.js"></script>
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
<script>
window.addEventListener("DOMContentLoaded", () => {{
  const el = document.querySelector("#search");
  if (el && window.PagefindUI)
    new PagefindUI({{ element: "#search", showSubResults: true, translations: {{ placeholder: "검색..." }} }});
}});
</script>
</body>
</html>"""


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
    tags_html = ""
    if page["tags"]:
        chips = " ".join(
            f'<a class="tag" href="{tag_url(t)}">{html.escape(t)}</a>' for t in page["tags"]
        )
        tags_html = f'<footer class="tags">{chips}</footer>'
    pagefind_attr = "" if page["key"] == "index" else " data-pagefind-body"
    return base_html(
        page["title"],
        f"<main><article{pagefind_attr}>{updated}\n{body_html}\n{tags_html}</article>\n{back_html}</main>",
    )


def write_page(rel: str, html_text: str) -> None:
    out = DIST / rel / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")


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


def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    pages = load_pages()
    inbound = lint_wiki.build_inbound_map(lint_wiki.wiki_pages())
    for page in pages.values():
        write_page(page["key"], render_article(page, pages, inbound))
    for s, label in SECTIONS:
        write_page(s, render_listing(label, [k for k in pages if k.startswith(s + "/")], pages))
    for tag, keys in collect_tags(pages).items():
        write_page(f"tags/{tag}", render_listing(f"태그: {tag}", keys, pages))
    (DIST / "index.html").write_text(render_home(pages), encoding="utf-8")
    (DIST / "404.html").write_text(render_404(), encoding="utf-8")
    shutil.copy(SITE / "style.css", DIST / "style.css")
    broken = check_internal_links()
    if broken:
        print(f"깨진 내부 링크 {len(broken)}건:", *broken[:10], sep="\n  ", file=sys.stderr)
        return 1
    print(f"기사 {len(pages)}쪽 생성 → {DIST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

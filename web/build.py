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
</head>
<body>
<header class="site-header"><a class="site-name" href="/">{SITE_NAME}</a></header>
{content}
</body>
</html>"""


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


def write_page(rel: str, html_text: str) -> None:
    out = DIST / rel / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")


def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    pages = load_pages()
    inbound = lint_wiki.build_inbound_map(lint_wiki.wiki_pages())
    for page in pages.values():
        write_page(page["key"], render_article(page, pages, inbound))
    print(f"기사 {len(pages)}쪽 생성 → {DIST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

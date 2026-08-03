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
SITE_URL = "https://omotomo-llm-wiki.com"
# 사이트가 소유한 카피 — wiki/overview.md를 옮겨 적지 않는다(문서가 바뀌어도 첫인상 문구는 사이트가 관리).
SITE_DESCRIPTION = "직접 고른 자료를 읽고 정리해 쌓아 올리는 개인 지식 위키입니다"
START_PATH = [
    ("/overview/", "위키 개요", "이 위키가 무엇을 다루는지 한 페이지로 훑습니다."),
    ("/analysis/ai-coding-evolution/", "AI 코딩의 4단계 진화",
     "프롬프트에서 에이전트까지, 전체 흐름을 한자리에서 비교합니다."),
    ("/index/", "전체 색인", "카테고리별 페이지 목록에서 관심 있는 주제를 고릅니다."),
]
SECTIONS = [("concepts", "개념"), ("entities", "엔티티"), ("sources", "출처"), ("analysis", "분석")]

# html=True: 위키 본문은 운영자 자신이 쓴 신뢰 콘텐츠라 인라인 HTML 허용
md = MarkdownIt("commonmark", {"html": True}).enable("table").enable("strikethrough")

HREF_RE = re.compile(r'href="(/[^"#?]*)')
CITATION_RE = re.compile(r"\(→ ([^)]*)\)")     # 인라인 인용 괄호 한 덩어리
LEADING_LINKS_RE = re.compile(r"^(?:\[\[[^\]]+\]\][·,;\s]*)+")  # 괄호 맨 앞 링크 나열
CITE_NUMBER_RE = re.compile(r"#(\d+)")

# 렌더에서 제외하는 사서 전용 구획 (docs/rules/site-code.md §2.4)
INTERNAL_SECTION = "## 기존 위키와의 연결"
SOURCE_INFO_SECTION = "## 출처 정보"
RAW_BULLET_RE = re.compile(r"^\s*[-*]\s+raw:")

SUMMARY_MAX = 100
SUMMARY_SOURCE_RE = re.compile(r"^## 한 줄 요약\s*\n+(?!#)(.+?)(?=\n\s*\n|\n#|\Z)", re.M | re.S)
SUMMARY_LEAD_RE = re.compile(r"^# .+?\n\s*\n(?!#)(.+?)(?=\n\s*\n|\n#|\Z)", re.M | re.S)
MARKUP_RE = re.compile(r"[*`>]|\[|\]\([^)]*\)")   # 강조·인라인코드·인용부호·마크다운 링크


def parse_tags(value: str) -> list[str]:
    """frontmatter 인라인 리스트 '[a, b]' → ['a', 'b']. 형식이 아니면 빈 리스트."""
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return []
    return [t.strip() for t in value[1:-1].split(",") if t.strip()]


def extract_summary(body: str, page_type: str) -> str:
    """페이지 한 줄 설명 — frontmatter 스키마를 늘리지 않고 본문에서 뽑는다.

    source 페이지는 '## 한 줄 요약'의 첫 문장, 나머지는 H1 다음 첫 문단의 첫 문장.
    해당 구획이 없으면 빈 문자열."""
    pattern = SUMMARY_SOURCE_RE if page_type == "source" else SUMMARY_LEAD_RE
    found = pattern.search(body)
    if not found:
        return ""
    text = CITATION_RE.sub("", found.group(1))
    text = lint_wiki.WIKILINK_RE.sub(
        lambda m: m.group(1).replace("\\|", "|").split("|")[-1].split("#")[0].strip(), text
    )
    text = MARKUP_RE.sub("", text)
    text = re.sub(r"\s+([.,;)])", r"\1", " ".join(text.split()))  # 인용을 걷어낸 자리의 공백
    sentence = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
    if len(sentence) > SUMMARY_MAX:
        sentence = sentence[:SUMMARY_MAX].rstrip() + "…"
    return sentence


def load_pages() -> dict[str, dict]:
    pages = {}
    for path in lint_wiki.wiki_pages():
        text = path.read_text(encoding="utf-8")
        fm = lint_wiki.parse_frontmatter(text) or {}
        key = lint_wiki.page_key(path)
        body = lint_wiki.split_body(text)
        pages[key] = {
            "key": key,
            "title": fm.get("title", key),
            "type": fm.get("type", ""),
            "updated": fm.get("updated", ""),
            "tags": parse_tags(fm.get("tags", "")),
            "body": body,
            "summary": extract_summary(body, fm.get("type", "")),
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


def outside_fences(body: str, transform) -> str:
    """코드 펜스(```) 바깥 텍스트에만 transform을 적용한다. 펜스 안 [[..]]·(→ ..)은 예시라 보존."""
    parts, pos = [], 0
    for fence in lint_wiki.FENCE_RE.finditer(body):
        parts.append(transform(body[pos : fence.start()]))
        parts.append(fence.group(0))
        pos = fence.end()
    parts.append(transform(body[pos:]))
    return "".join(parts)


def render_citations(body: str) -> str:
    """인라인 인용 (→ [[sources/슬러그|#13 라벨]])을 각주 칩 <a class="cite">13</a>으로 접는다.

    인용만 든 괄호는 통째로 걷어내고, 뒤에 산문이 붙은 괄호는 괄호와 산문을 남긴다.
    sources/ 가 아닌 위키링크는 손대지 않는다(뒤의 link_wikilinks가 일반 링크로 처리).
    이 파서는 docs/rules/wiki-content.md의 인용 규약과 짝을 이룬다 — 한쪽을 바꾸면 다른 쪽도 바꾼다."""

    def chip(m) -> str:
        target = lint_wiki.normalize_target(m.group(1))
        if not target.startswith("sources/"):
            return m.group(0)
        raw = m.group(1).replace("\\|", "|")
        label = raw.split("|", 1)[1].strip() if "|" in raw else target
        number = CITE_NUMBER_RE.match(label)
        text = number.group(1) if number else label[:6]
        return (
            f'<a class="cite" href="{url_for(target)}" '
            f'title="{html.escape(label)}">{html.escape(text)}</a>'
        )

    def group(m) -> str:
        inner = m.group(1)
        links = list(lint_wiki.WIKILINK_RE.finditer(inner))
        only_sources = bool(links) and all(
            lint_wiki.normalize_target(link.group(1)).startswith("sources/") for link in links
        )
        tail = LEADING_LINKS_RE.sub("", inner, count=1).strip()
        if only_sources and not tail:
            return " ".join(chip(link) for link in links)
        return "(" + lint_wiki.WIKILINK_RE.sub(chip, inner) + ")"

    return outside_fences(body, lambda text: CITATION_RE.sub(group, text))


def strip_internal_sections(body: str) -> str:
    """사서 전용 구획을 렌더 직전에 걷어낸다 — wiki/ 원본은 절대 건드리지 않는다.

    ① '## 기존 위키와의 연결' 섹션 전체(다음 '## ' 헤딩 또는 파일 끝까지)
    ② '## 출처 정보' 안의 'raw:' 불릿 (raw/ 경로는 공개 대상이 아니다)
    둘 다 wiki-query·wiki-lint가 읽는 정보라 원본에는 반드시 남아 있어야 한다."""
    kept, section, in_fence, skipping = [], "", False, False
    for line in body.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("## "):
            section = line.strip()
            skipping = section == INTERNAL_SECTION
        if skipping:
            continue
        if not in_fence and section == SOURCE_INFO_SECTION and RAW_BULLET_RE.match(line):
            continue
        kept.append(line)
    return "\n".join(kept)


def link_wikilinks(body: str, existing) -> str:
    """[[대상|별칭]]을 <a>로, 대상 없는 링크는 회색 <span>으로 치환한다.
    markdown 렌더 전에 실행되며 html=True라 그대로 통과한다."""

    def repl(m):
        raw = m.group(1).replace("\\|", "|")
        target = lint_wiki.normalize_target(m.group(1))
        label = raw.split("|", 1)[1].strip() if "|" in raw else target
        if target in existing:
            return f'<a href="{url_for(target)}">{html.escape(label)}</a>'
        return f'<span class="dead-link">{html.escape(label)}</span>'

    return outside_fences(body, lambda text: lint_wiki.WIKILINK_RE.sub(repl, text))


def base_html(title: str, content: str, summary: str = "", path: str = "/") -> str:
    head_title = SITE_NAME if title == SITE_NAME else f"{title} · {SITE_NAME}"
    description = html.escape(summary or SITE_DESCRIPTION, quote=True)
    page_url = html.escape(SITE_URL + path, quote=True)
    escaped_title = html.escape(head_title, quote=True)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(head_title)}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{escaped_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{page_url}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary">
<link rel="canonical" href="{page_url}">
<link rel="stylesheet" href="/pagefind/pagefind-ui.css">
<link rel="stylesheet" href="/style.css">
<script src="/pagefind/pagefind-ui.js"></script>
<script>const t = localStorage.getItem("theme"); if (t) document.documentElement.dataset.theme = t;</script>
</head>
<body>
<header class="site-header">
<a class="site-name" href="/">{SITE_NAME}</a>
<div id="header-search" class="header-search"></div>
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
  // #search는 홈·404의 큰 검색창, #header-search는 모든 페이지의 헤더 검색창 (서로 다른 인스턴스)
  for (const id of ["#search", "#header-search"]) {{
    if (document.querySelector(id) && window.PagefindUI)
      new PagefindUI({{ element: id, showSubResults: true, translations: {{ placeholder: "검색..." }} }});
  }}
}});
</script>
</body>
</html>"""


def summary_html(page: dict) -> str:
    """한 줄 설명 — 비어 있으면 빈 요소를 만들지 않는다."""
    if not page["summary"]:
        return ""
    return f'<span class="summary">{html.escape(page["summary"])}</span>'


def render_listing(title: str, keys, pages: dict, path: str) -> str:
    items = "\n".join(
        f'<li><a href="{url_for(k)}">{html.escape(pages[k]["title"])}</a>'
        f'{summary_html(pages[k])}'
        f'<span class="meta">{pages[k]["updated"]}</span></li>'
        for k in sorted(keys, key=lambda k: pages[k]["title"])
    )
    return base_html(
        title,
        f'<main><h1>{html.escape(title)}</h1><ul class="listing">{items}</ul></main>',
        path=path,
    )


def render_tag_index(pages: dict) -> str:
    """전체 태그 목록. 여러 페이지가 쓰는 태그를 먼저, 한 번만 쓰인 태그는 접어 둔다."""
    ordered = sorted(collect_tags(pages).items(), key=lambda item: (-len(item[1]), item[0]))

    def chip(tag: str, keys: list) -> str:
        return (
            f'<a class="tag" href="{tag_url(tag)}">{html.escape(tag)}'
            f' <span class="count">{len(keys)}</span></a>'
        )

    shared = [chip(t, k) for t, k in ordered if len(k) > 1]
    single = [chip(t, k) for t, k in ordered if len(k) == 1]
    content = f"""<main><h1>태그</h1>
<div class="tag-index">{" ".join(shared)}</div>
<details class="tag-single"><summary>한 페이지에만 쓰인 태그 {len(single)}개</summary>
<div class="tag-index">{" ".join(single)}</div></details></main>"""
    return base_html("태그", content, path="/tags/")


def render_home(pages: dict) -> str:
    def count(prefix: str) -> int:
        return sum(1 for k in pages if k.startswith(prefix + "/"))

    entries = (
        [("/overview/", "개요", None)]
        + [(f"/{s}/", label, count(s)) for s, label in SECTIONS]
        + [("/tags/", "태그", len(collect_tags(pages))), ("/index/", "전체 색인", None)]
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
        f'{summary_html(p)}'
        f'<span class="meta">{p["updated"]}</span></li>'
        for p in recent
    )
    start_html = "\n".join(
        f'<li><a href="{u}">{label}</a><span class="summary">{note}</span></li>'
        for u, label, note in START_PATH
    )
    content = f"""<main class="home">
<h1>{SITE_NAME}</h1>
<p class="intro">{SITE_DESCRIPTION}</p>
<div id="search"></div>
<section class="start"><h2>처음이면 순서대로</h2><ol>{start_html}</ol></section>
<nav class="entries">{entry_html}</nav>
<section class="recent"><h2>최근 갱신</h2><ul>{recent_html}</ul></section>
</main>"""
    return base_html(SITE_NAME, content, summary=SITE_DESCRIPTION, path="/")


def render_404() -> str:
    content = f"""<main class="home">
<h1>페이지가 없습니다</h1>
<p class="meta">주소를 확인하거나 검색해 보세요.</p>
<div id="search"></div>
<p><a href="/">{SITE_NAME} 홈으로</a></p>
</main>"""
    return base_html("페이지 없음", content, path="/404.html")


def render_article(page: dict, pages: dict, inbound: dict) -> str:
    crumb = ""
    section = page["key"].split("/")[0] if "/" in page["key"] else ""
    label = dict(SECTIONS).get(section)
    if label:
        crumb = (
            '<nav class="breadcrumb"><a href="/">홈</a> / '
            f'<a href="/{section}/">{label}</a> / '
            f'<span>{html.escape(page["title"])}</span></nav>'
        )
    body = render_citations(strip_internal_sections(page["body"]))
    body_html = md.render(link_wikilinks(body, pages))
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
        f"<main>{crumb}<article{pagefind_attr}>{updated}\n{body_html}\n{tags_html}</article>\n{back_html}</main>",
        summary=page["summary"],
        path=url_for(page["key"]),
    )


def write_page(rel: str, html_text: str) -> None:
    out = DIST / rel / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")


def write_sitemap_and_robots(pages: dict) -> None:
    """생성한 모든 페이지의 sitemap.xml과 robots.txt. 404는 색인 대상이 아니라 제외한다."""
    entries = [("/", "")]
    entries += [(url_for(p["key"]), p["updated"]) for p in pages.values()]
    entries += [(f"/{s}/", "") for s, _ in SECTIONS]
    entries += [(tag_url(tag), "") for tag in collect_tags(pages)]
    entries += [("/tags/", "")]
    urls = "\n".join(
        f"  <url><loc>{html.escape(SITE_URL + path)}</loc>"
        + (f"<lastmod>{lastmod}</lastmod>" if lastmod else "")
        + "</url>"
        for path, lastmod in entries
    )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )


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
        keys = [k for k in pages if k.startswith(s + "/")]
        write_page(s, render_listing(label, keys, pages, f"/{s}/"))
    for tag, keys in collect_tags(pages).items():
        write_page(f"tags/{tag}", render_listing(f"태그: {tag}", keys, pages, tag_url(tag)))
    write_page("tags", render_tag_index(pages))
    (DIST / "index.html").write_text(render_home(pages), encoding="utf-8")
    (DIST / "404.html").write_text(render_404(), encoding="utf-8")
    write_sitemap_and_robots(pages)
    shutil.copy(SITE / "style.css", DIST / "style.css")
    broken = check_internal_links()
    if broken:
        print(f"깨진 내부 링크 {len(broken)}건:", *broken[:10], sep="\n  ", file=sys.stderr)
        return 1
    print(f"기사 {len(pages)}쪽 생성 → {DIST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

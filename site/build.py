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
    ("/overview/", "위키 개요", "이 위키가 어떻게 만들어지는지 한 페이지로."),
    ("/categories/", "카테고리", "다섯 갈래 주제에서 고르기."),
]
SECTIONS = [("categories", "카테고리"), ("concepts", "개념"), ("entities", "엔티티"), ("sources", "출처"), ("analysis", "분석")]
CATEGORY_SECTION = "categories"   # 페이지별 줄을 들고 있는 카테고리 페이지들. 나머지 목록은 이걸로 묶는다.
# 홈 카테고리 띠에 붙는 한 줄 설명 — 사이트가 소유한 카피
SECTION_NOTES = {
    "categories": "주제별로 묶은 길잡이",
    "concepts": "하네스 · 컨텍스트 · 루프 엔지니어링",
    "entities": "인물 · 조직 · 도구",
    "sources": "자료 한 건당 요약 한 편",
    "analysis": "비교 · 판단 기록",
}

# html=True: 위키 본문은 운영자 자신이 쓴 신뢰 콘텐츠라 인라인 HTML 허용
md = MarkdownIt("commonmark", {"html": True}).enable("table").enable("strikethrough")

_default_fence = md.renderer.rules["fence"]


def _fence(self, tokens, idx, options, env):
    """```mermaid 펜스만 <pre class="mermaid">로 — 소스는 이스케이프해 넣고 브라우저가 textContent로 되돌린다."""
    token = tokens[idx]
    if token.info.strip() == "mermaid":
        return f'<pre class="mermaid" data-pagefind-ignore>{html.escape(token.content)}</pre>\n'
    return _default_fence(tokens, idx, options, env)


md.add_render_rule("fence", _fence)


def mermaid_script_for(body_html: str) -> str:
    """그림이 있는 페이지에만 Mermaid 모듈 스크립트를 붙인다 — 없는 페이지는 CDN 요청 0."""
    return MERMAID_SCRIPT if 'class="mermaid"' in body_html else ""


def copy_assets(src: Path = WIKI / "assets", dst: Path = DIST / "assets") -> int:
    """wiki/assets/ (라이선스 있는 공식 문서 그림)를 dist/assets/로 그대로 복사. 복사한 파일 수."""
    if not src.is_dir():
        return 0
    shutil.copytree(src, dst, dirs_exist_ok=True)
    return sum(1 for p in dst.rglob("*") if p.is_file())


HREF_RE = re.compile(r'href="(/[^"#?]*)')
CITATION_RE = re.compile(r"\(→ ([^)]*)\)")     # 인라인 인용 괄호 한 덩어리
LEADING_LINKS_RE = re.compile(r"^(?:\[\[[^\]]+\]\][·,;\s]*)+")  # 괄호 맨 앞 링크 나열
CITE_NUMBER_RE = re.compile(r"#(\d+)")

# 렌더에서 제외하는 사서 전용 구획 (docs/rules/site-code.md §2.4)
INTERNAL_SECTION = "## 기존 위키와의 연결"
SOURCE_INFO_SECTION = "## 출처 정보"
RAW_BULLET_RE = re.compile(r"^\s*[-*]\s+raw:")

SUMMARY_MAX = 100
SUMMARY_MIN = 45   # 이보다 짧으면 다음 문장을 이어 붙인다 (불릿 발췌가 토막나는 것 방지)
SUMMARY_SOURCE_RE = re.compile(r"^## 한 줄 요약\s*\n+(?!#)(.+?)(?=\n\s*\n|\n#|\Z)", re.M | re.S)
SUMMARY_LEAD_RE = re.compile(r"^# .+?\n\s*\n(?!#)(.+?)(?=\n\s*\n|\n#|\Z)", re.M | re.S)
# phase-14: 리드 문단을 걷어낸 뒤로는 페이지 첫 요약 구획이 발췌원이다.
# concept·entity 는 '## 한눈에 요약'의 불릿, analysis 는 '## 결론 먼저'의 인용문.
SUMMARY_GLANCE_RE = re.compile(
    r"^## (?:한눈에 요약|결론 먼저)\s*\n+((?:[-*>] .+\n?)+)", re.M
)
MARKUP_RE = re.compile(r"[*`>]|\[|\]\([^)]*\)")   # 강조·인라인코드·인용부호·마크다운 링크

# Mermaid 그림 (docs/rules/wiki-content.md §1.4) — 그림이 있는 페이지에만 이 스크립트를 붙인다.
MERMAID_VERSION = "11.17.2"
MERMAID_CDN = f"https://cdn.jsdelivr.net/npm/mermaid@{MERMAID_VERSION}/dist/mermaid.esm.min.mjs"
MERMAID_SCRIPT = (
    '<script type="module">\n'
    f'import mermaid from "{MERMAID_CDN}";\n'
    """const blocks = [...document.querySelectorAll("pre.mermaid")];
// Mermaid는 색을 SVG에 박아 넣으므로 CSS로 테마를 못 따른다 — 테마 전환 때 원본에서 다시 그린다.
// 파싱 실패 시 Mermaid의 오류 그림 대신 원본 텍스트만 보이게 suppressErrorRendering.
const draw = async () => {
  const light = document.documentElement.dataset.theme === "light";
  mermaid.initialize({ suppressErrorRendering: true, startOnLoad: false, theme: light ? "neutral" : "dark" });
  for (const [i, el] of blocks.entries()) {
    if (el.dataset.src === undefined) el.dataset.src = el.textContent;
    try {
      const { svg } = await mermaid.render(`mmd-${i}-${Date.now()}`, el.dataset.src);
      el.innerHTML = svg;
      el.classList.remove("mermaid-error");
    } catch (err) {
      el.textContent = el.dataset.src;   // 렌더 실패 시 원본 텍스트라도 보이게
      el.classList.add("mermaid-error");
    }
  }
};
draw();
document.querySelector("#theme-toggle").addEventListener("click", draw);
</script>"""
)


def parse_tags(value: str) -> list[str]:
    """frontmatter 인라인 리스트 '[a, b]' → ['a', 'b']. 형식이 아니면 빈 리스트."""
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return []
    return [t.strip() for t in value[1:-1].split(",") if t.strip()]


def extract_summary(body: str, page_type: str) -> str:
    """페이지 한 줄 설명 — frontmatter 스키마를 늘리지 않고 본문에서 뽑는다.

    source 페이지는 '## 한 줄 요약'의 첫 문장. 나머지는 '## 한눈에 요약'의 첫 불릿들이며,
    아직 리드 문단만 있는 미개정 페이지는 H1 다음 첫 문단으로 폴백한다.
    해당 구획이 없으면 빈 문자열."""
    if page_type == "source":
        found = SUMMARY_SOURCE_RE.search(body)
    else:
        found = SUMMARY_GLANCE_RE.search(body) or SUMMARY_LEAD_RE.search(body)
    if not found:
        return ""
    text = re.sub(r"^[-*>] ", "", found.group(1), flags=re.M)
    text = CITATION_RE.sub("", text)
    text = lint_wiki.WIKILINK_RE.sub(
        lambda m: m.group(1).replace("\\|", "|").split("|")[-1].split("#")[0].strip(), text
    )
    text = MARKUP_RE.sub("", text)
    text = re.sub(r"\s+([.,;)])", r"\1", " ".join(text.split()))  # 인용을 걷어낸 자리의 공백
    # 불릿 하나는 한 문장이라 짧다 — SUMMARY_MIN 을 넘길 때까지 다음 문장을 붙인다.
    sentence = ""
    for part in re.split(r"(?<=[.!?])\s", text):
        if sentence and len(sentence) >= SUMMARY_MIN:
            break
        sentence = f"{sentence} {part}".strip()
    if len(sentence) > SUMMARY_MAX:
        sentence = sentence[:SUMMARY_MAX].rstrip() + "…"
    return sentence


def load_pages() -> dict[str, dict]:
    pages = {}
    for path in lint_wiki.wiki_pages():
        key = lint_wiki.page_key(path)
        if key == "index":
            # 스킬·lint 가 읽는 관문 목록일 뿐이다 — 독자에게는 카테고리 페이지가 그 역할을 한다.
            continue
        text = path.read_text(encoding="utf-8")
        fm = lint_wiki.parse_frontmatter(text) or {}
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


def nav_html(path: str) -> str:
    """헤더 섹션 내비 — 현재 보고 있는 섹션을 표시한다."""
    items = [(f"/{s}/", label) for s, label in SECTIONS] + [("/tags/", "태그")]
    return "".join(
        f'<a href="{url}"' + (' aria-current="page"' if path.startswith(url) else "")
        + f">{label}</a>"
        for url, label in items
    )


def search_form(form_id: str) -> str:
    """검색어를 /search/?q= 로 넘기는 입력창. 결과는 드롭다운이 아니라 결과 페이지에서 본다."""
    return (
        f'<form id="{form_id}" class="search-form" action="/search/" role="search">'
        '<input type="search" name="q" placeholder="검색..." aria-label="검색"></form>'
    )


def base_html(title: str, content: str, summary: str = "", path: str = "/", extra_scripts: str = "") -> str:
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
<script>document.documentElement.dataset.theme = localStorage.getItem("theme") || "dark";</script>
</head>
<body>
<header class="site-header">
<a class="site-name" href="/">{SITE_NAME}</a>
<nav class="site-nav">{nav_html(path)}</nav>
{search_form("header-search")}
<button id="theme-toggle" aria-label="밝은 화면과 어두운 화면 전환" title="밝은 화면과 어두운 화면 전환"></button>
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
// 목차 스크롤 하이라이트: 화면 상단을 지난 마지막 헤딩을 활성으로 표시한다.
window.addEventListener("DOMContentLoaded", () => {{
  const toc = document.querySelector(".toc");
  if (!toc) return;
  const links = new Map();
  for (const a of toc.querySelectorAll("a"))
    links.set(decodeURIComponent(a.hash.slice(1)), a);
  const heads = [...document.querySelectorAll("article h2[id], article h3[id]")]
    .filter((h) => links.has(h.id));
  if (!heads.length) return;
  let active = null, ticking = false;
  const spy = () => {{
    ticking = false;
    let cur = heads[0];
    for (const h of heads) {{
      if (h.getBoundingClientRect().top > 80) break;
      cur = h;
    }}
    if (cur === active) return;
    if (active) links.get(active.id).classList.remove("active");
    links.get(cur.id).classList.add("active");
    active = cur;
  }};
  addEventListener("scroll", () => {{
    if (!ticking) {{ ticking = true; requestAnimationFrame(spy); }}
  }}, {{ passive: true }});
  spy();
}});
</script>
{extra_scripts}
</body>
</html>"""


def summary_html(page: dict) -> str:
    """한 줄 설명 — 비어 있으면 빈 요소를 만들지 않는다."""
    if not page["summary"]:
        return ""
    return f'<span class="summary">{html.escape(page["summary"])}</span>'


CATEGORY_SUFFIX = " — 카테고리"


def category_name(page: dict) -> str:
    """카테고리 페이지 제목 '가상화 — 카테고리' 에서 이름만."""
    return page["title"].removesuffix(CATEGORY_SUFFIX)


def category_intro(page: dict) -> str:
    """카테고리 페이지 첫 인용 블록의 첫 문장 — 홈·카테고리 목록의 카드 설명."""
    m = re.search(r"^> (.+)$", page["body"], re.M)
    if not m:
        return ""
    first = re.split(r"(?<=다\.)\s", m.group(1).strip(), maxsplit=1)[0]
    return MARKUP_RE.sub("", first)


def category_map(pages: dict) -> list[tuple[str, list[str]]]:
    """카테고리 페이지 순서(wiki/index.md 의 링크 순서)대로 (카테고리 키, 소속 페이지 키 목록).

    소속은 카테고리 페이지 본문의 위키링크에서 읽는다 — 별도 frontmatter 없이 카테고리 페이지가 곧
    소속 기록이다(docs/rules/wiki-content.md §2). 두 카테고리에 걸친 페이지는 양쪽에 들어간다."""
    index_text = (WIKI / "index.md").read_text(encoding="utf-8")
    order = []
    for raw in lint_wiki.WIKILINK_RE.findall(index_text):
        key = lint_wiki.normalize_target(raw)
        if key.startswith(CATEGORY_SECTION + "/") and key in pages and key not in order:
            order.append(key)
    result = []
    for cat in order:
        members = []
        for raw in lint_wiki.WIKILINK_RE.findall(pages[cat]["body"]):
            key = lint_wiki.normalize_target(raw)
            if key in pages and not key.startswith(CATEGORY_SECTION + "/") and key not in members:
                members.append(key)
        result.append((cat, members))
    return result


def listing_item(page: dict) -> str:
    return (
        f'<li data-title="{html.escape(page["title"], quote=True)}" data-updated="{page["updated"]}">'
        f'<a href="{url_for(page["key"])}">{html.escape(page["title"])}'
        f'{summary_html(page)}'
        f'<span class="meta">{page["updated"][5:]}</span></a></li>'
    )


SORT_CONTROL = (
    '<div class="sort" role="group" aria-label="정렬">'
    '<button type="button" data-sort="title" aria-pressed="true">제목순</button>'
    '<button type="button" data-sort="updated" aria-pressed="false">최근 갱신순</button></div>'
)
# 정렬은 그룹 안에서만 바꾼다 — 그룹(카테고리) 순서는 index.md 가 정한 그대로. 선택은 테마처럼 localStorage 에 남긴다.
SORT_SCRIPT = """<script>
(() => {
  const KEY = "listing-sort";
  const apply = (mode) => {
    document.querySelectorAll("ul.listing").forEach((ul) => {
      const items = Array.from(ul.children);
      items.sort((a, b) => mode === "updated"
        ? b.dataset.updated.localeCompare(a.dataset.updated) || a.dataset.title.localeCompare(b.dataset.title, "ko")
        : a.dataset.title.localeCompare(b.dataset.title, "ko"));
      items.forEach((li) => ul.appendChild(li));
    });
    document.querySelectorAll(".sort button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.sort === mode)));
  };
  let mode = "title";
  try { mode = localStorage.getItem(KEY) || "title"; } catch (e) {}
  if (mode !== "title") apply(mode);
  document.querySelectorAll(".sort button").forEach((b) => b.addEventListener("click", () => {
    apply(b.dataset.sort);
    try { localStorage.setItem(KEY, b.dataset.sort); } catch (e) {}
  }));
})();
</script>"""


def render_listing(title: str, keys, pages: dict, path: str) -> str:
    """종류별·태그별 목록 — 카테고리로 묶고, 그룹 안은 제목순(정렬 토글로 최근 갱신순 전환)."""
    keys = list(keys)
    remaining = set(keys)
    groups = []
    for cat, members in category_map(pages):
        hit = [k for k in members if k in remaining]
        if hit:
            groups.append((category_name(pages[cat]), url_for(cat), hit))
            remaining -= set(hit)
    if remaining:  # lint 가 막지만, 혹시 빠진 페이지가 있어도 목록에서 사라지지는 않게
        groups.append(("분류 없음", "", sorted(remaining)))
    # 기본은 접힘 — 카테고리 이름과 편수만 보이고, 펼쳐야 페이지가 나온다. JS 없이 <details> 로.
    sections = "\n".join(
        '<details class="group"><summary>'
        + f'<span class="name">{html.escape(name)}</span><span class="count">{len(members)}</span>'
        + (f'<a class="more" href="{href}">카테고리 페이지 →</a>' if href else "")
        + '</summary><ul class="listing">'
        + "".join(listing_item(pages[k]) for k in sorted(members, key=lambda k: pages[k]["title"]))
        + "</ul></details>"
        for name, href, members in groups
    )
    return base_html(
        title,
        f'<main><div class="listing-head"><h1>{html.escape(title)}</h1>'
        f'<p class="meta">{len(keys)}편 · 카테고리 {len(groups)}개</p>{SORT_CONTROL}</div>'
        f"{sections}</main>",
        path=path,
        extra_scripts=SORT_SCRIPT,
    )


def category_cards(pages: dict) -> str:
    return "\n".join(
        f'<a class="entry" href="{url_for(cat)}">'
        f'<span class="label"><span class="name">{html.escape(category_name(pages[cat]))}</span>'
        f'<span class="count">{len(members)}</span></span>'
        f'<span class="note">{html.escape(category_intro(pages[cat]))}</span></a>'
        for cat, members in category_map(pages)
    )


def render_category_index(pages: dict) -> str:
    """/categories/ — 카드 5장. 페이지별 줄은 각 카테고리 페이지에 있다."""
    return base_html(
        "카테고리",
        '<main><div class="listing-head"><h1>카테고리</h1>'
        f'<p class="meta">{SECTION_NOTES[CATEGORY_SECTION]}</p></div>'
        f'<nav class="entries categories">{category_cards(pages)}</nav></main>',
        path=f"/{CATEGORY_SECTION}/",
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

    entry_html = "\n".join(
        f'<a class="entry" href="/{s}/">'
        f'<span class="label"><span class="name">{label}</span>'
        f'<span class="count">{count(s)}</span></span>'
        f'<span class="note">{SECTION_NOTES[s]}</span></a>'
        for s, label in SECTIONS
        if s != CATEGORY_SECTION  # 홈 띠는 페이지 종류만 — 카테고리는 헤더 내비와 시작 경로로 간다
    )
    recent = sorted(
        # overview 와 카테고리 페이지 제외 — 목록·안내는 '최근 갱신' 이 아니다
        (p for p in pages.values() if "/" in p["key"] and not p["key"].startswith(CATEGORY_SECTION + "/")),
        key=lambda p: p["updated"],
        reverse=True,
    )[:5]
    recent_html = "\n".join(
        f'<li><a href="{url_for(p["key"])}">{html.escape(p["title"])}'
        f'{summary_html(p)}'
        f'<span class="meta">{p["updated"][5:]}</span></a></li>'
        for p in recent
    )
    start_html = "\n".join(
        f'<li><a href="{u}">{label}</a><span class="summary">{note}</span></li>'
        for u, label, note in START_PATH
    )
    latest = max((p["updated"] for p in pages.values() if p["updated"]), default="")
    content = f"""<main class="home">
<section class="hero">
<div>
<h1>LLM Wiki</h1>
{search_form("search")}
<p class="stats"><span>문서 <strong>{len(pages)}</strong>편</span>
<span>출처 <strong>{count("sources")}</strong>건</span>
<span>마지막 갱신 <strong>{latest}</strong></span></p>
</div>
<section class="start"><h2>처음이신가요?</h2><ol>{start_html}</ol></section>
</section>
<nav class="entries" aria-label="페이지 종류">{entry_html}</nav>
<section class="recent"><h2>최근 갱신<a class="more" href="/categories/">카테고리 →</a></h2>
<ul>{recent_html}</ul></section>
</main>"""
    return base_html(SITE_NAME, content, summary=SITE_DESCRIPTION, path="/")


def render_404() -> str:
    content = f"""<main class="home">
<section class="hero">
<div>
<h1>페이지가 없습니다</h1>
{search_form("search")}
<p class="stats"><span>주소를 확인하거나 검색해 보세요.</span>
<span><a href="/">{SITE_NAME} 홈으로</a></span></p>
</div>
</section>
</main>"""
    return base_html("페이지 없음", content, path="/404.html")


SEARCH_SCRIPT = """<script src="/pagefind/pagefind-ui.js"></script>
<script>
window.addEventListener("DOMContentLoaded", () => {
  const q = new URLSearchParams(location.search).get("q") || "";
  const ui = new PagefindUI({
    element: "#search-results", showSubResults: true, showImages: false, autofocus: !q,
    translations: { placeholder: "검색..." },
    // 입력이 바뀌면 주소의 ?q=도 바꿔, 결과를 공유하거나 뒤로 가기로 돌아올 수 있게 한다
    processTerm: (term) => {
      const url = new URL(location.href);
      if (term) url.searchParams.set("q", term); else url.searchParams.delete("q");
      history.replaceState(null, "", url);
      return term;
    },
  });
  if (q) {
    ui.triggerSearch(q);
    document.querySelector("#header-search input").value = q;
  }
});
</script>"""


def render_search() -> str:
    content = """<main class="search-page">
<h1>검색</h1>
<div id="search-results"></div>
</main>"""
    return base_html("검색", content, path="/search/", extra_scripts=SEARCH_SCRIPT)


HEADING_RE = re.compile(r"<h([23])>(.*?)</h\1>", re.S)
TAG_RE = re.compile(r"<[^>]+>")
SLUG_DROP = re.compile(r"[^0-9A-Za-z가-힣\s-]")


def slugify(text: str) -> str:
    s = SLUG_DROP.sub("", text).strip()
    return re.sub(r"\s+", "-", s).lower() or "section"


H1_RE = re.compile(r"<h1>.*?</h1>", re.S)


def split_h1(body_html: str) -> tuple[str, str]:
    """렌더된 본문에서 첫 H1을 떼어낸다. 목차를 <article> 밖 사이드 칼럼에 놓기 위함."""
    m = H1_RE.search(body_html)
    if not m:
        return "", body_html
    return m.group(0), body_html[: m.start()] + body_html[m.end() :]


def add_toc(body_html: str) -> tuple[str, str]:
    """H2·H3에 id를 달고 (본문, 목차 HTML)을 돌려준다. 항목 3개 미만이면 목차는 빈 문자열."""
    items: list[tuple[str, str, str]] = []
    used: dict[str, int] = {}

    def anchor(match: re.Match) -> str:
        level, inner = match.group(1), match.group(2)
        text = html.unescape(TAG_RE.sub("", inner)).strip()
        slug = slugify(text)
        used[slug] = used.get(slug, 0) + 1
        if used[slug] > 1:
            slug = f"{slug}-{used[slug]}"
        items.append((level, slug, text))
        return f'<h{level} id="{slug}">{inner}</h{level}>'

    out = HEADING_RE.sub(anchor, body_html)
    if len(items) < 3:
        return out, ""
    lis = "".join(
        f'<li class="toc-h{level}"><a href="#{urllib.parse.quote(slug)}">'
        f"{html.escape(text)}</a></li>"
        for level, slug, text in items
    )
    return out, f'<nav class="toc"><p class="toc-title">목차</p><ul>{lis}</ul></nav>'


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
    body_html, toc_html = add_toc(md.render(link_wikilinks(body, pages)))
    h1_html, body_html = split_h1(body_html)
    updated = f'<p class="meta">갱신 {page["updated"]}</p>' if page["updated"] else ""
    back = sorted(inbound.get(page["key"], set()))
    back_html = ""
    if back:
        items = "\n".join(
            f'<li><a href="{url_for(k)}">{html.escape(pages[k]["title"])}</a></li>'
            for k in back
        )
        back_html = (
            '<section class="backlinks"><details>'
            f"<summary>이 문서를 참조하는 문서 {len(back)}개</summary>"
            f"<ul>{items}</ul></details></section>"
        )
    tags_html = ""
    if page["tags"]:
        chips = " ".join(
            f'<a class="tag" href="{tag_url(t)}">{html.escape(t)}</a>' for t in page["tags"]
        )
        tags_html = f'<footer class="tags">{chips}</footer>'
    # 카테고리 페이지는 링크 목록이라 검색 노이즈다 — 본문은 색인하지 않는다(제목은 남는다)
    is_listing = page["key"].startswith(CATEGORY_SECTION + "/")
    pagefind_attr = "" if is_listing else " data-pagefind-body"
    # h1이 <article> 밖으로 나갔으므로 Pagefind가 제목을 계속 색인하도록 같은 표시를 단다.
    if pagefind_attr and h1_html:
        h1_html = h1_html.replace("<h1>", "<h1 data-pagefind-body>", 1)
    return base_html(
        page["title"],
        f'<main class="{"has-toc" if toc_html else ""}">{crumb}{h1_html}{toc_html}'
        f"<article{pagefind_attr}>{updated}\n{body_html}\n{tags_html}</article>\n{back_html}</main>",
        summary=page["summary"],
        path=url_for(page["key"]),
        extra_scripts=mermaid_script_for(body_html),
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
        if s == CATEGORY_SECTION:
            write_page(s, render_category_index(pages))
            continue
        keys = [k for k in pages if k.startswith(s + "/")]
        write_page(s, render_listing(label, keys, pages, f"/{s}/"))
    for tag, keys in collect_tags(pages).items():
        write_page(f"tags/{tag}", render_listing(f"태그: {tag}", keys, pages, tag_url(tag)))
    write_page("tags", render_tag_index(pages))
    write_page("search", render_search())
    (DIST / "index.html").write_text(render_home(pages), encoding="utf-8")
    (DIST / "404.html").write_text(render_404(), encoding="utf-8")
    write_sitemap_and_robots(pages)
    shutil.copy(SITE / "style.css", DIST / "style.css")
    copy_assets()
    broken = check_internal_links()
    if broken:
        print(f"깨진 내부 링크 {len(broken)}건:", *broken[:10], sep="\n  ", file=sys.stderr)
        return 1
    print(f"기사 {len(pages)}쪽 생성 → {DIST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

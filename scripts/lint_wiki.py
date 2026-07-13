#!/usr/bin/env python3
"""위키 결정적(deterministic) lint — LLM 판단이 필요 없는 기계적 검사를 수행한다.

wiki-lint 스킬의 1단계로 실행된다. 모순·낡은 주장 탐지 같은 의미 판단은
여전히 LLM(에이전트)의 몫이고, 이 스크립트는 다음만 검사한다:

  1. 위키링크 무결성 — 모든 [[...]] 대상 페이지가 실제로 존재하는가
  2. raw/ ↔ wiki/sources/ 1:1 패리티
  3. frontmatter 필수 키 (title/type/created/updated/sources/tags) + type 값 +
     sources/·concepts/ 페이지 title의 한글 포함 여부(entities/ 는 예외)
  4. index.md 등재 여부 — 모든 페이지가 색인에 올라 있는가
  5. 고아 페이지 — index.md 외에 아무 페이지도 링크하지 않는 페이지
  6. 링크 형식 (docs/rules/wiki-content.md §1) — 본문 위키링크의 한글 별칭 누락,
     소스 페이지의 자기 인용, 소스 페이지 frontmatter의 label 키 누락/형식 오류,
     본문 내 서식 없는 '#숫자' 인용(Quartz가 태그로 오인식)

사용법: python3 scripts/lint_wiki.py   (repo 루트 기준 상대 경로도 동작)
종료 코드: 문제 0건이면 0, 있으면 1

--inbound <경로|슬러그> 를 주면 전체 lint 대신 해당 페이지로 들어오는
인바운드 링크(고아 페이지 검사와 동일한 기준으로 계산) 목록만 출력하고 종료한다.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"

REQUIRED_KEYS = ["title", "type", "created", "updated", "sources", "tags"]
VALID_TYPES = {"entity", "concept", "source", "analysis", "overview"}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
LABEL_CONTENT_RE = re.compile(r"^#\d+ \S")
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
BARE_CITATION_RE = re.compile(r"#\d+")
HANGUL_RE = re.compile(r"[가-힣]")

issues = []


def add(category: str, message: str) -> None:
    issues.append((category, message))


def normalize_target(raw_target: str) -> str:
    r"""[[대상|별칭]] / [[대상\|별칭]] / [[대상#섹션]] → '대상'만 남긴다."""
    target = raw_target.replace("\\|", "|").split("|")[0].split("#")[0].strip()
    return target


def label_issue(value: str) -> str | None:
    """소스 페이지 frontmatter의 label 값이 잘 정형화되어 있으면 None, 아니면 문제 사유를 반환한다.
    정형화된 값: backslash 없음 + 따옴표가 없거나 앞뒤로 균형 있게 한 쌍만 있음 +
    (따옴표를 벗겨낸) 본문이 '#숫자 제목' 형태로 시작."""
    if "\\" in value:
        return "backslash 문자 포함"

    quote_positions = [i for i, c in enumerate(value) if c in "\"'"]
    if quote_positions:
        if (
            len(quote_positions) != 2
            or quote_positions[0] != 0
            or quote_positions[1] != len(value) - 1
            or value[0] != value[-1]
        ):
            return "따옴표가 불균형하거나 남아있음"
        content = value[1:-1]
    else:
        content = value

    if not LABEL_CONTENT_RE.match(content):
        return "'#숫자 제목' 형식이 아님"
    return None


def resolve(target: str) -> Path:
    return WIKI / f"{target}.md"


def wiki_pages():
    return sorted(WIKI.rglob("*.md"))


def page_key(path: Path) -> str:
    """wiki/concepts/foo.md → 'concepts/foo' (위키링크 대상 표기)"""
    return str(path.relative_to(WIKI).with_suffix(""))


def parse_frontmatter(text: str):
    """의존성 없는 최소 파싱: 첫 '---' 블록 안의 최상위 'key:' 들을 모은다."""
    if not text.startswith("---"):
        return None
    lines = text.split("\n")
    keys = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return keys
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if m:
            keys[m.group(1)] = m.group(2).strip()
    return None  # 닫는 --- 없음


def check_wikilinks(pages):
    existing = {page_key(p) for p in pages}
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for raw_target in WIKILINK_RE.findall(text):
            target = normalize_target(raw_target)
            if not target:
                continue
            if target not in existing:
                add("고아 링크", f"{page.relative_to(ROOT)} → [[{target}]] 대상 페이지 없음")


def check_parity():
    raw_slugs = {p.stem for p in RAW.glob("*.md")}
    source_slugs = {p.stem for p in (WIKI / "sources").glob("*.md")}
    for slug in sorted(raw_slugs - source_slugs):
        add("패리티", f"raw/{slug}.md 에 대응하는 wiki/sources/{slug}.md 없음 (누락된 소스 페이지)")
    for slug in sorted(source_slugs - raw_slugs):
        add("패리티", f"wiki/sources/{slug}.md 에 대응하는 raw/{slug}.md 없음 (원본 없는 소스 페이지)")
    return len(raw_slugs), len(source_slugs)


def check_frontmatter(pages):
    for page in pages:
        fm = parse_frontmatter(page.read_text(encoding="utf-8"))
        rel = page.relative_to(ROOT)
        if fm is None:
            add("frontmatter", f"{rel} — frontmatter 블록 없음/닫히지 않음")
            continue
        missing = [k for k in REQUIRED_KEYS if k not in fm]
        if missing:
            add("frontmatter", f"{rel} — 필수 키 누락: {', '.join(missing)}")
        if "type" in fm and fm["type"] not in VALID_TYPES:
            add("frontmatter", f"{rel} — 잘못된 type 값: '{fm['type']}'")
        key = page_key(page)
        if (key.startswith("sources/") or key.startswith("concepts/")) and "title" in fm:
            if not HANGUL_RE.search(fm["title"]):
                add("frontmatter", f"{rel} — title에 한글 없음(영문 제목): {fm['title']}")


def check_index_coverage(pages):
    index_path = WIKI / "index.md"
    if not index_path.exists():
        add("색인", "wiki/index.md 자체가 없음")
        return
    index_targets = {normalize_target(t) for t in WIKILINK_RE.findall(index_path.read_text(encoding="utf-8"))}
    for page in pages:
        key = page_key(page)
        if key in ("index", "overview"):
            continue
        if key not in index_targets:
            add("색인", f"wiki/{key}.md 가 index.md 에 등재되어 있지 않음")


def build_inbound_map(pages) -> dict:
    """페이지별 인바운드 링크 소스 페이지 집합. index.md 는 소스로 집계하지 않는다(고아 페이지 검사 기준과 동일).
    한 페이지가 같은 대상을 [[대상]]과 [[대상#섹션]]처럼 서로 다른 형태로 여러 번 링크해도 소스는 1건으로 센다."""
    inbound = {page_key(p): set() for p in pages}
    for page in pages:
        src = page_key(page)
        if src == "index":
            continue
        text = page.read_text(encoding="utf-8")
        for raw_target in set(WIKILINK_RE.findall(text)):
            target = normalize_target(raw_target)
            if target in inbound and target != src:
                inbound[target].add(src)
    return inbound


def check_orphans(pages):
    """index.md 를 제외한 다른 페이지로부터 인바운드 링크가 0인 페이지."""
    inbound = build_inbound_map(pages)
    for key, sources in sorted(inbound.items()):
        if key in ("index", "overview"):
            continue
        if not sources:
            add("고아 페이지", f"wiki/{key}.md — index.md 외 인바운드 링크 0건")


def split_body(text: str) -> str:
    """frontmatter 블록을 잘라내고 본문만 돌려준다."""
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


def check_link_format(pages):
    """docs/rules/wiki-content.md §1 링크·인용 형식 검사."""
    for page in pages:
        text = page.read_text(encoding="utf-8")
        rel = page.relative_to(ROOT)
        body = split_body(text)
        src_key = page_key(page)

        # (a) 본문 위키링크는 반드시 별칭([[대상|별칭]] 또는 표 안 [[대상\|별칭]])을 가진다
        for raw_target in WIKILINK_RE.findall(body):
            if "|" not in raw_target.replace("\\|", "|"):
                add("링크 형식", f"{rel} — [[{raw_target}]] 별칭 없음 (슬러그가 그대로 렌더링됨)")

        # (b) 소스 페이지는 자기 자신을 인용하지 않는다
        if src_key.startswith("sources/") and f"[[{src_key}" in body:
            add("링크 형식", f"{rel} — 자기 자신을 인용함 ([[{src_key}...]])")

        # (c) 소스 페이지 frontmatter에는 인용 라벨(label)이 있어야 하고, 값의 형식도 올바라야 한다
        fm = parse_frontmatter(text)
        if src_key.startswith("sources/") and fm is not None:
            if "label" not in fm:
                add("링크 형식", f"{rel} — frontmatter에 label(짧은 인용 라벨) 없음")
            else:
                reason = label_issue(fm["label"])
                if reason:
                    add("링크 형식", f"{rel} — label 값 형식 오류({reason}): {fm['label']}")


def check_bare_citations(pages):
    """맨 '#숫자' 본문 인용 검사 (docs/rules/wiki-content.md) — Quartz가 이를 태그로 파싱해
    쓰레기 태그 페이지를 만든다. 위키링크(별칭 포함)·인라인 코드·펜스 코드블록·frontmatter 내부는 제외."""
    for page in pages:
        body = split_body(page.read_text(encoding="utf-8"))
        cleaned = WIKILINK_RE.sub("", FENCE_RE.sub("", body))
        cleaned = INLINE_CODE_RE.sub("", cleaned)
        matches = BARE_CITATION_RE.findall(cleaned)
        if matches:
            rel = page.relative_to(ROOT)
            uniq = ", ".join(sorted(set(matches)))
            add(
                "링크 형식",
                f"{rel} — 본문에 서식 없는 '#숫자' 인용 {len(matches)}건 ({uniq}) — 위키링크 별칭 형태로 바꿀 것",
            )


def resolve_page_key(arg: str, pages) -> str | None:
    """경로('wiki/concepts/hooks.md', 'concepts/hooks.md') 또는 슬러그('concepts/hooks')를
    page_key 형식으로 정규화한다. 대상 페이지가 없으면 None."""
    candidate = arg.strip()
    if candidate.startswith("wiki/"):
        candidate = candidate[len("wiki/"):]
    if candidate.endswith(".md"):
        candidate = candidate[: -len(".md")]
    existing = {page_key(p) for p in pages}
    return candidate if candidate in existing else None


def print_inbound(target_arg: str) -> int:
    pages = wiki_pages()
    key = resolve_page_key(target_arg, pages)
    if key is None:
        print(f"오류: '{target_arg}' 에 해당하는 위키 페이지를 찾을 수 없습니다.", file=sys.stderr)
        return 2

    inbound = build_inbound_map(pages)
    sources = sorted(inbound.get(key, []))
    print(f"## wiki/{key}.md 인바운드 링크 ({len(sources)}건)")
    if not sources:
        print("(없음)")
    else:
        for src in sources:
            print(f"- wiki/{src}.md")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="위키 결정적 lint / 인바운드 링크 조회")
    parser.add_argument(
        "--inbound",
        metavar="PAGE",
        help="전체 lint 대신, 지정한 페이지(경로 또는 슬러그)로 들어오는 인바운드 링크만 출력하고 종료",
    )
    args = parser.parse_args()

    if not WIKI.is_dir() or not RAW.is_dir():
        print(f"오류: {ROOT} 아래에 wiki/ 또는 raw/ 가 없습니다.", file=sys.stderr)
        return 2

    if args.inbound is not None:
        return print_inbound(args.inbound)

    pages = wiki_pages()
    check_wikilinks(pages)
    n_raw, n_src = check_parity()
    check_frontmatter(pages)
    check_index_coverage(pages)
    check_orphans(pages)
    check_link_format(pages)
    check_bare_citations(pages)

    print(f"## 결정적 lint 결과 — 페이지 {len(pages)}개, raw {n_raw}건 ↔ sources {n_src}건")
    if not issues:
        print("문제 없음 ✅ (고아 링크 0 · 패리티 일치 · frontmatter 통과 · 색인 완비 · 고아 페이지 0 · 링크 형식 통과)")
        return 0

    by_cat = {}
    for cat, msg in issues:
        by_cat.setdefault(cat, []).append(msg)
    for cat, msgs in by_cat.items():
        print(f"\n### {cat} ({len(msgs)}건)")
        for msg in msgs:
            print(f"- {msg}")
    print(f"\n총 {len(issues)}건 — 위 항목을 wiki-lint 절차에 따라 처리하세요.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

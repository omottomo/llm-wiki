#!/usr/bin/env python3
"""위키 결정적(deterministic) lint — LLM 판단이 필요 없는 기계적 검사를 수행한다.

wiki-lint 스킬의 1단계로 실행된다. 모순·낡은 주장 탐지 같은 의미 판단은
여전히 LLM(에이전트)의 몫이고, 이 스크립트는 다음만 검사한다:

  1. 위키링크 무결성 — 모든 [[...]] 대상 페이지가 실제로 존재하는가
  2. raw/ ↔ wiki/sources/ 1:1 패리티
  3. frontmatter 필수 키 (title/type/created/updated/sources/tags) + type 값
  4. index.md 등재 여부 — 모든 페이지가 색인에 올라 있는가
  5. 고아 페이지 — index.md 외에 아무 페이지도 링크하지 않는 페이지

사용법: python3 scripts/lint_wiki.py   (repo 루트 기준 상대 경로도 동작)
종료 코드: 문제 0건이면 0, 있으면 1
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"

REQUIRED_KEYS = ["title", "type", "created", "updated", "sources", "tags"]
VALID_TYPES = {"entity", "concept", "source", "analysis", "overview"}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

issues = []


def add(category: str, message: str) -> None:
    issues.append((category, message))


def normalize_target(raw_target: str) -> str:
    r"""[[대상|별칭]] / [[대상\|별칭]] / [[대상#섹션]] → '대상'만 남긴다."""
    target = raw_target.replace("\\|", "|").split("|")[0].split("#")[0].strip()
    return target


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


def check_orphans(pages):
    """index.md 를 제외한 다른 페이지로부터 인바운드 링크가 0인 페이지."""
    inbound = {page_key(p): 0 for p in pages}
    for page in pages:
        if page_key(page) == "index":
            continue
        text = page.read_text(encoding="utf-8")
        src = page_key(page)
        for raw_target in set(WIKILINK_RE.findall(text)):
            target = normalize_target(raw_target)
            if target in inbound and target != src:
                inbound[target] += 1
    for key, count in sorted(inbound.items()):
        if key in ("index", "overview"):
            continue
        if count == 0:
            add("고아 페이지", f"wiki/{key}.md — index.md 외 인바운드 링크 0건")


def main() -> int:
    if not WIKI.is_dir() or not RAW.is_dir():
        print(f"오류: {ROOT} 아래에 wiki/ 또는 raw/ 가 없습니다.", file=sys.stderr)
        return 2

    pages = wiki_pages()
    check_wikilinks(pages)
    n_raw, n_src = check_parity()
    check_frontmatter(pages)
    check_index_coverage(pages)
    check_orphans(pages)

    print(f"## 결정적 lint 결과 — 페이지 {len(pages)}개, raw {n_raw}건 ↔ sources {n_src}건")
    if not issues:
        print("문제 없음 ✅ (고아 링크 0 · 패리티 일치 · frontmatter 통과 · 색인 완비 · 고아 페이지 0)")
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

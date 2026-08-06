#!/usr/bin/env python3
"""Deterministic post-build checks for the static site (site/, built by build.py → site/dist/).

Companion to lint_wiki.py, but for code-mode (site/) instead of wiki prose.
Run after `python3 site/build.py`. Checks that need the built output are skipped
(not failed) if no build has run yet.

Usage: python3 scripts/verify_site.py
Exit code: 0 if all checks pass, 1 otherwise.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
SITE = ROOT / "site"
DIST = SITE / "dist"

# A citation line like "raw: raw/youtube-xxx.md" or "raw 경로: <code>raw/xxx.md</code>"
# (wiki-content.md source-page template) is a legitimate relative reference to
# the source file, not a leak. Amended 2026-07-12: a literal grep for "raw/"
# alone false-positives on this citation metadata, so the audit must exclude
# it explicitly. An ABSOLUTE path (e.g. "/Users/x/.../raw/xxx.md") does not
# match this whitelist and is correctly still flagged — it leaks the local
# operator's filesystem path, which the citation template never intends.
LEGITIMATE_RAW_CITATION = re.compile(r"raw(?:\s*경로)?:\s*(?:<code>)?raw/[\w.\-]+\.md")

passed = True


def report(ok: bool, message: str) -> None:
    global passed
    print(("PASS: " if ok else "FAIL: ") + message)
    if not ok:
        passed = False


def repo_rel(path: Path) -> str:
    """Path as it is written in this script's messages: repo-root-relative, POSIX."""
    return path.relative_to(ROOT).as_posix()


def check_raw_untracked() -> None:
    """The raw/ boundary's first leg (site-code.md §2.1): the source documents live in a
    separate private repo, so they must never be tracked here. This makes a `git add -f
    raw/...` slip fail the build instead of riding a merge into the public remote."""
    inside = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"], cwd=ROOT, capture_output=True, text=True
    )
    if inside.returncode != 0:
        print("SKIP: no raw/-tracked check (not a git work tree)")
        return
    result = subprocess.run(["git", "ls-files", "raw/"], cwd=ROOT, capture_output=True, text=True)
    tracked = result.stdout.split()
    report(not tracked, f"raw/ not tracked by git ({len(tracked)} tracked path(s): {tracked[:5]})")


def check_artifacts_ignored() -> None:
    result = subprocess.run(["git", "check-ignore", "-q", repo_rel(DIST)], cwd=ROOT)
    report(result.returncode == 0, f"{repo_rel(DIST)} git-ignored")


def check_no_unresolved_wikilinks(out: Path) -> None:
    if not out.exists():
        print(f"SKIP: no unresolved-wikilink check ({repo_rel(out)} missing, run a build first)")
        return
    offenders = [
        html.relative_to(ROOT)
        for html in out.rglob("*.html")
        if "[[" in html.read_text(errors="ignore")
    ]
    report(not offenders, f"no literal '[[' left in built HTML ({len(offenders)} offending file(s): {offenders[:5]})")


def check_raw_leak(out: Path) -> None:
    if not out.exists():
        print(f"SKIP: no raw/ leak audit ({repo_rel(out)} missing, run a build first)")
        return
    suspicious = []
    for html in out.rglob("*.html"):
        for line in html.read_text(errors="ignore").splitlines():
            if "raw/" in line and not LEGITIMATE_RAW_CITATION.search(line):
                suspicious.append(f"{html.relative_to(ROOT)}: {line.strip()[:120]}")
    report(not suspicious, f"no raw/ leak beyond legitimate source citations ({len(suspicious)} suspicious line(s): {suspicious[:10]})")


def check_no_raw_public_path(out: Path) -> None:
    """Lead ruling (2026-07-12), part 1: no rendered page path is derived from raw/ —
    i.e. no site/dist/raw* directory or file exists at all."""
    if not out.exists():
        print(f"SKIP: no raw/-path check ({repo_rel(out)} missing, run a build first)")
        return
    offenders = [
        p.relative_to(ROOT)
        for p in out.rglob("*")
        if "raw" in {part.lower() for part in p.relative_to(out).parts}
    ]
    report(not offenders, f"no {repo_rel(out)} path named 'raw' ({len(offenders)} offender(s): {offenders[:5]})")


def _distinctive_transcript_phrase(md_text: str) -> str | None:
    """Pick one long line from the middle of a raw transcript's '## Transcript'
    section, to use as a spot-check needle. Deterministic: same file -> same line."""
    marker = "## Transcript"
    idx = md_text.find(marker)
    body = md_text[idx + len(marker) :] if idx != -1 else md_text
    lines = [line.strip() for line in body.splitlines() if len(line.strip()) >= 20]
    if not lines:
        return None
    return lines[len(lines) // 2]


def check_raw_content_leak(out: Path) -> None:
    """Lead ruling (2026-07-12), part 2: no transcript CONTENT from raw/ in the
    built output. Spot-checks one distinctive mid-file line per raw/*.md transcript
    against every built HTML page; zero matches required."""
    if not out.exists():
        print(f"SKIP: no raw-content leak audit ({repo_rel(out)} missing, run a build first)")
        return
    if not RAW.exists():
        print("SKIP: no raw-content leak audit (raw/ missing)")
        return

    html_texts = [html.read_text(errors="ignore") for html in out.rglob("*.html")]

    leaked = []
    for md_path in sorted(RAW.glob("*.md")):
        phrase = _distinctive_transcript_phrase(md_path.read_text(errors="ignore"))
        if not phrase:
            continue
        if any(phrase in html_text for html_text in html_texts):
            leaked.append(f"{md_path.relative_to(ROOT)}: {phrase[:80]!r} found in built output")
    report(not leaked, f"no raw transcript content found verbatim in built output ({len(leaked)} leak(s): {leaked[:5]})")


def check_no_local_user_path(out: Path) -> None:
    """A local absolute path (e.g. /Users/<name>/...) in built output leaks the
    operator's username/filesystem layout into public HTML and the search index.
    (wiki/sources/*.md fixed in commit 67ce92e; this guards against regressions.)"""
    if not out.exists():
        print(f"SKIP: no local-user-path check ({repo_rel(out)} missing, run a build first)")
        return
    offenders = []
    for html in out.rglob("*.html"):
        if "/Users/" in html.read_text(errors="ignore"):
            offenders.append(html.relative_to(ROOT))
    report(not offenders, f"no '/Users/' absolute path in built output ({len(offenders)} offending file(s): {offenders[:5]})")


def main() -> int:
    check_raw_untracked()
    check_artifacts_ignored()
    check_no_unresolved_wikilinks(DIST)
    check_raw_leak(DIST)
    check_no_raw_public_path(DIST)
    check_raw_content_leak(DIST)
    check_no_local_user_path(DIST)
    print("\nAll checks passed." if passed else "\nSome checks failed.")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

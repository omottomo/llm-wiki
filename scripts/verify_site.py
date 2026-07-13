#!/usr/bin/env python3
"""Deterministic post-build checks for site/ (Quartz output).

Companion to lint_wiki.py, but for code-mode (site/) instead of wiki prose.
Run after `cd site && npx quartz build`. Checks that need public/ to exist
are skipped (not failed) if no build has run yet.

Usage: python3 scripts/verify_site.py
Exit code: 0 if all checks pass, 1 otherwise.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
PUBLIC = SITE / "public"
RAW = ROOT / "raw"

# A citation line like "raw: raw/youtube-xxx.md" or "raw 경로: <code>raw/xxx.md</code>"
# (CLAUDE.md source-page template, §2) is a legitimate relative reference to
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


def check_symlink() -> None:
    content = SITE / "content"
    if not content.is_symlink():
        report(False, "site/content is not a symlink")
        return
    target = str(content.readlink())
    report(target == "../wiki", f"site/content -> {target} (expected ../wiki)")


def check_artifacts_ignored() -> None:
    for rel in ["site/node_modules", "site/public", "site/.quartz"]:
        result = subprocess.run(["git", "check-ignore", "-q", rel], cwd=ROOT)
        report(result.returncode == 0, f"{rel} git-ignored")


def check_no_unresolved_wikilinks() -> None:
    if not PUBLIC.exists():
        print("SKIP: no unresolved-wikilink check (site/public missing, run a build first)")
        return
    offenders = [
        html.relative_to(ROOT)
        for html in PUBLIC.rglob("*.html")
        if "[[" in html.read_text(errors="ignore")
    ]
    report(not offenders, f"no literal '[[' left in built HTML ({len(offenders)} offending file(s): {offenders[:5]})")


def check_raw_leak() -> None:
    if not PUBLIC.exists():
        print("SKIP: no raw/ leak audit (site/public missing, run a build first)")
        return
    suspicious = []
    for html in PUBLIC.rglob("*.html"):
        for line in html.read_text(errors="ignore").splitlines():
            if "raw/" in line and not LEGITIMATE_RAW_CITATION.search(line):
                suspicious.append(f"{html.relative_to(ROOT)}: {line.strip()[:120]}")
    report(not suspicious, f"no raw/ leak beyond legitimate source citations ({len(suspicious)} suspicious line(s): {suspicious[:10]})")


def check_no_raw_public_path() -> None:
    """Lead ruling (2026-07-12), part 1: no rendered page path is derived from raw/ —
    i.e. no site/public/raw* directory or file exists at all."""
    if not PUBLIC.exists():
        print("SKIP: no raw/-path check (site/public missing, run a build first)")
        return
    offenders = [
        p.relative_to(ROOT)
        for p in PUBLIC.rglob("*")
        if "raw" in {part.lower() for part in p.relative_to(PUBLIC).parts}
    ]
    report(not offenders, f"no site/public path named 'raw' ({len(offenders)} offender(s): {offenders[:5]})")


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


def check_raw_content_leak() -> None:
    """Lead ruling (2026-07-12), part 2: no transcript CONTENT from raw/ in the
    built output. Spot-checks one distinctive mid-file line per raw/*.md transcript
    against every built HTML page; zero matches required."""
    if not PUBLIC.exists():
        print("SKIP: no raw-content leak audit (site/public missing, run a build first)")
        return
    if not RAW.exists():
        print("SKIP: no raw-content leak audit (raw/ missing)")
        return

    html_texts = [html.read_text(errors="ignore") for html in PUBLIC.rglob("*.html")]

    leaked = []
    for md_path in sorted(RAW.glob("*.md")):
        phrase = _distinctive_transcript_phrase(md_path.read_text(errors="ignore"))
        if not phrase:
            continue
        if any(phrase in html_text for html_text in html_texts):
            leaked.append(f"{md_path.relative_to(ROOT)}: {phrase[:80]!r} found in built output")
    report(not leaked, f"no raw transcript content found verbatim in built output ({len(leaked)} leak(s): {leaked[:5]})")


def check_no_local_user_path() -> None:
    """A local absolute path (e.g. /Users/<name>/...) in built output leaks the
    operator's username/filesystem layout into public HTML and the search index.
    (wiki/sources/*.md fixed in commit 67ce92e; this guards against regressions.)"""
    if not PUBLIC.exists():
        print("SKIP: no local-user-path check (site/public missing, run a build first)")
        return
    offenders = []
    for html in PUBLIC.rglob("*.html"):
        if "/Users/" in html.read_text(errors="ignore"):
            offenders.append(html.relative_to(ROOT))
    report(not offenders, f"no '/Users/' absolute path in built output ({len(offenders)} offending file(s): {offenders[:5]})")


def main() -> int:
    check_symlink()
    check_artifacts_ignored()
    check_no_unresolved_wikilinks()
    check_raw_leak()
    check_no_raw_public_path()
    check_raw_content_leak()
    check_no_local_user_path()
    print("\nAll checks passed." if passed else "\nSome checks failed.")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

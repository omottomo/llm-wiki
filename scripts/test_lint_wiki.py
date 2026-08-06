#!/usr/bin/env python3
"""lint_wiki.py 회귀 테스트 러너 (stdlib, 프레임워크 없음).

golden-wiki 와 no-raw-wiki 는 lint 통과(exit 0)해야 하고, tests/fixtures/defects/ 아래의
각 결함 픽스처는 lint 실패(exit 1)하며 그 dir 의 expect.txt 부분문자열이
lint 출력에 나타나야 한다. 결함 dir 은 동적으로 발견하므로 결함을 추가해도
러너를 고칠 필요가 없다.

사용법: python3 scripts/test_lint_wiki.py   (어느 디렉터리에서 실행해도 동작)
종료 코드: 전부 통과면 0, 하나라도 불일치면 1.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LINT = REPO / "scripts" / "lint_wiki.py"
GOLDEN = REPO / "tests" / "fixtures" / "golden-wiki"
NO_RAW = REPO / "tests" / "fixtures" / "no-raw-wiki"
DEFECTS = REPO / "tests" / "fixtures" / "defects"


def run_lint(root: Path):
    r = subprocess.run(
        [sys.executable, str(LINT), "--root", str(root)],
        capture_output=True, text=True,
    )
    return r.returncode, r.stdout


def main() -> int:
    fails = 0

    # 1) golden must lint clean
    code, _ = run_lint(GOLDEN)
    if code == 0:
        print(f"[PASS] golden-wiki → exit 0")
    else:
        fails += 1
        print(f"[FAIL] golden-wiki → exit {code} (expected 0)")

    # 1b) raw/ 없는 트리(공개 클론이 타는 경로)도 매니페스트로 패리티를 보고하며 통과해야 한다
    code, out = run_lint(NO_RAW)
    if code == 0 and "raw 2건 ↔ sources 2건" in out:
        print(f"[PASS] no-raw-wiki → exit 0, 매니페스트로 패리티 보고")
    else:
        fails += 1
        reason = f"exit {code} (expected 0)" if code != 0 else "패리티 라인 없음"
        print(f"[FAIL] no-raw-wiki → {reason}")

    # 2) each defect must fail with its expected substring
    n_defects = 0
    for defect in sorted(d for d in DEFECTS.iterdir() if d.is_dir()):
        n_defects += 1
        expect = (defect / "expect.txt").read_text(encoding="utf-8").strip()
        code, out = run_lint(defect)
        if code == 1 and expect in out:
            print(f"[PASS] defects/{defect.name} → exit 1, '{expect}'")
        else:
            fails += 1
            reason = f"exit {code} (expected 1)" if code != 1 else f"missing substring '{expect}'"
            print(f"[FAIL] defects/{defect.name} → {reason}")

    total = 2 + n_defects
    print(f"\n{total - fails}/{total} passed" + ("" if not fails else f", {fails} FAILED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

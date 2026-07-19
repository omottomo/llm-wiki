#!/usr/bin/env python3
"""lint_wiki.py 회귀 테스트 러너 (stdlib, 프레임워크 없음).

golden-wiki 는 lint 통과(exit 0)해야 하고, tests/fixtures/defects/ 아래의
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

    # 2) each defect must fail with its expected substring
    for defect in sorted(d for d in DEFECTS.iterdir() if d.is_dir()):
        expect = (defect / "expect.txt").read_text(encoding="utf-8").strip()
        code, out = run_lint(defect)
        if code == 1 and expect in out:
            print(f"[PASS] defects/{defect.name} → exit 1, '{expect}'")
        else:
            fails += 1
            reason = f"exit {code} (expected 1)" if code != 1 else f"missing substring '{expect}'"
            print(f"[FAIL] defects/{defect.name} → {reason}")

    total = 1 + sum(1 for d in DEFECTS.iterdir() if d.is_dir())
    print(f"\n{total - fails}/{total} passed" + ("" if not fails else f", {fails} FAILED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

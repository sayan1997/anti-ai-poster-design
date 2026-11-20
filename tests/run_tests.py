#!/usr/bin/env python3
"""Sanity tests: the linter must flag the deliberately bad poster and pass the clean ones.

    python tests/run_tests.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "anti-ai-poster-design"
LINT = SKILL / "scripts" / "poster_lint.py"


def lint(path):
    r = subprocess.run([sys.executable, str(LINT), str(path)], capture_output=True, text=True)
    return r.returncode, r.stdout


def main():
    failures = []

    code, out = lint(ROOT / "tests" / "fixtures" / "ai_style_example.html")
    if code != 1:
        failures.append("ai_style_example.html should FAIL the lint")
    for tid in ("T1", "T2", "T4", "D3", "T8", "D5"):
        if f"] {tid}" not in out and f"{tid}:" not in out:
            failures.append(f"expected tell {tid} to be reported on the bad fixture")

    clean = [SKILL / "assets" / "template.html"] + sorted((SKILL / "examples").glob("*.html"))
    for p in clean:
        code, out = lint(p)
        if code != 0:
            failures.append(f"{p.name} should pass the lint\n{out}")

    if failures:
        print("FAILED")
        for f in failures:
            print(" -", f)
        return 1
    print(f"OK: bad fixture flagged, {len(clean)} clean posters pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())

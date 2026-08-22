#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess
import sys
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-dir", type=Path, required=True)
    args = p.parse_args()
    base = args.base_dir.expanduser().resolve()

    here = Path(__file__).resolve().parent
    build_script = here / "build_study1_cohort_data.py"
    validate_script = here / "validate_study1_cohort_data.py"

    for script in [build_script, validate_script]:
        if not script.exists():
            raise FileNotFoundError(f"Missing script: {script}")

    print("\n=== BUILD STUDY 1 COHORT DATA ===")
    subprocess.run(
        [sys.executable, str(build_script), "--base-dir", str(base)],
        check=True,
    )

    print("\n=== VALIDATE STUDY 1 COHORT DATA ===")
    subprocess.run(
        [sys.executable, str(validate_script), "--base-dir", str(base)],
        check=True,
    )

if __name__ == "__main__":
    main()

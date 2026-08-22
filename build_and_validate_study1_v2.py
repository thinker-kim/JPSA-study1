#!/usr/bin/env python3
import argparse, subprocess, sys
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("--base-dir",type=Path,required=True)
a=p.parse_args()
base=a.base_dir.expanduser().resolve()
here=Path(__file__).resolve().parent

subprocess.run(
    [sys.executable,str(here/"build_study1_cohort_data_v2.py"),"--base-dir",str(base)],
    check=True
)
subprocess.run(
    [sys.executable,str(here/"validate_study1_cohort_data_v2.py"),"--base-dir",str(base)],
    check=True
)

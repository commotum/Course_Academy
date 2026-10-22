"""Retained author_reported_limitation regression, including earlier math repair.

History has event codes but no named finding IDs. Keep the exact latest
counterexample, the general construction witness, and the earlier grouping and
source replay checks executable against the current generator.
"""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
for name in ['check_shortcuts.py','check_roles.py','validate_math.py']:
    subprocess.run([sys.executable,str(ROOT/'checks'/name)],cwd=ROOT,check=True)

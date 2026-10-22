"""Retained packaging event and the demonstrated family-wide repair regressions."""
import subprocess
import sys
from pathlib import Path
W=Path(__file__).resolve().parents[1]
for script in ('check_cli_contract.py','check_repair.py','check_delivery_current.py','check_inventory.py'):
    subprocess.run([sys.executable,str(W/'checks'/script)],cwd=W,check=True)

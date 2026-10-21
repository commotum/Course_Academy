"""Strict minimal regression. Current exit 1; repaired grading must exit 0.
Run from any cwd: python3 /absolute/path/to/evidence_root/reproduce-sine.py
Native engine is database free; both input and result remain in evidence_root.
"""
from pathlib import Path
import subprocess,json
E=Path(__file__).resolve().parent
engine=Path('/home/jake/Developer/Course_Academy/generate/runs/current/check-engine')
cmd=[str(engine),str(E/'delivered-sine-strict-input.json'),str(E/'sine-reproduction-native-report.json')]
p=subprocess.run(cmd,capture_output=True,text=True)
(E/'sine-reproduction-result.json').write_text(json.dumps({'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expected_after_repair':0},indent=2)+'\n')
print(p.stdout+p.stderr,end='')
raise SystemExit(p.returncode)

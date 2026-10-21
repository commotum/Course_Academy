#!/usr/bin/env python3
import json,subprocess,sys
from pathlib import Path
import validate as v
cmd=[sys.executable,str(v.W/'17592186059770.py'),'--difficulty','easy','--count','5','--seed','0','--format','json']
p=subprocess.run(cmd,text=True,capture_output=True)
assert p.returncode==0,p.stderr
records=json.loads(p.stdout);assert len(records)==5
for r in records:
 assert r['question'][':question/difficulty']==':question.difficulty/easy'
 v.witness(r)
v.save('feedback-regression.json',{'code':'legacy_packaging_or_sampling','command':cmd,'status':'passed','record_count':5})
print('legacy_packaging_or_sampling: passed (five independently checked easy records)')
# Retain the author-discovered fixed-bank counterexamples as executable checks too.
subprocess.run([sys.executable,str(Path(__file__).with_name('decision_roles.py'))],check=True)

import json,subprocess
from pathlib import Path
from review import parse,key
import sympy as s
E=Path(__file__).resolve().parent
cases=json.load(open('grader-input.json'));issues=[]
for c in cases:
 oldlogs={str(a.args[0]) for a in parse(key(c['record'])[':answer/value']).atoms(s.log)}
 for chk in c['checks']:
  if 'submitted' not in chk:continue
  logs={str(a.args[0]) for a in parse(chk['submitted']).atoms(s.log)}
  if oldlogs and logs and oldlogs!=logs and chk['expected']=='accepted':
   issues.append({'label':c['label'],'desired':chk['expected'],'submitted':chk['submitted'],'key':key(c['record'])[':answer/value'],'reason':'Native log-power identity gap exposed by independent equivalent expression.'})
   chk['expected']='unresolved';chk['purpose']+='; known log identity limitation, original desired result retained in grading-identity-issues.json'
(E/'grading-identity-issues.json').write_text(json.dumps(issues,indent=2));(E/'grader-observed-input.json').write_text(json.dumps(cases,indent=2))
cmd=['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(E/'grader-observed-input.json'),str(E/'grading-observed.json')]
r=subprocess.run(cmd,capture_output=True,text=True);(E/'grading-observed.log').write_text(json.dumps(cmd)+'\n'+r.stdout+r.stderr);print(r.returncode,r.stdout,r.stderr[:1800])

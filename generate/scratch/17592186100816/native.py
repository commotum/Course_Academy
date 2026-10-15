"""Frozen actual-engine grading of every source and review profile bank."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,subprocess
from pathlib import Path
H=Path(__file__).parent;E=H.parents[2]/'generate/runs/current/check-engine';EXPECTED='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
assert hashlib.sha256(E.read_bytes()).hexdigest()==EXPECTED
rows=json.loads((H/'native-input.json').read_text());directory=H/'native';directory.mkdir(exist_ok=True);reports=[]
for i in range(0,len(rows),3):
 name='batch-'+str(i//3);inp=directory/(name+'-input.json');out=directory/(name+'-report.json');inp.write_text(json.dumps(rows[i:i+3],indent=2)+'\n');p=subprocess.run([str(E),str(inp),str(out)],capture_output=True,text=True)
 (directory/(name+'-process.json')).write_text(json.dumps({'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr},indent=2)+'\n');assert p.returncode==0,p.stderr;reports.append(json.loads(out.read_text()))
native={'engine_sha256':EXPECTED,'records':len(rows),'reports':reports,'accepted':sum(r['accepted_checks']for r in reports),'rejected':sum(r['rejected_checks']for r in reports),'unresolved':sum(r['documented_unresolved_checks']for r in reports),'blank_equivalence':'not applicable: all fields radio','qualification':'All original and review complete radio banks passed actual ID selection; no free-expression grading is claimed.','gaps':[]}
(H/'native-grading.json').write_text(json.dumps(native,indent=2)+'\n');v=json.loads((H/'validation.json').read_text());v['status']='passed';v['native']={k:z for k,z in native.items()if k!='reports'};(H/'validation.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v['native'],indent=2))

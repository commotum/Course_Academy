"""Affected boundary, input-contract and relocation checks after bank-domain tightening."""
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import generator as G
import validate as T
out=Path('evidence')
boundaries=[]
for profile in ('P','R','B'):
 for n in ((3,7) if profile=='R' else (2,6)):
  for s in (-1,1):
   for k in (-6,-1,1,6):
    r=G.build(G.instance(profile,n,s,k,'t' if profile=='B' else 'x',k>0),random.Random(n+k+s))
    T.verify(r);boundaries.append(r)
(out/'boundaries.json').write_text(json.dumps(boundaries,indent=2)+'\n')
cases=json.loads((out/'grader-input.json').read_text())
cases=[c for c in cases if not c['label'].startswith('boundary ')]
cases.extend(T.make_checks(r,'boundary '+str(j)) for j,r in enumerate(boundaries))
(out/'grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
bad=[{'offset':0},{'offset':4},{'offset':-4},{'factors':['1','2']},{'factors':['2','2']},{'factors':['-1','2']},{'omitted_col':0},{'omitted_row':2}]
for kw in bad:
 try:G.instance('P',3,1,4,**kw)
 except ValueError:pass
 else:raise AssertionError(kw)
try:G.instance('R',3,1,-1,offset=1)
except ValueError:pass
else:raise AssertionError('zero wrong constant accepted')
assert G.generate(count=5,seed=84153)==G.generate(count=5,seed=84153)
for r in G.generate(count=9,seed=21):T.verify(r)
with tempfile.TemporaryDirectory(dir=out.resolve(),prefix='relocate-') as directory:
 for f in json.loads(Path('package.json').read_text())['files']:shutil.copy(f,directory)
 p=subprocess.run([sys.executable,'generator.py','--difficulty','moderate','--count','5','--seed','84153','--format','json'],cwd=directory,capture_output=True,text=True,check=True)
 assert json.loads(p.stdout)==G.generate(count=5,seed=84153)
report={'boundary_records':48,'invalid_bank_assignments_rejected':9,'small_regression':9,'relocation':True,'determinism':True,'passes':True}
(out/'final-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))

#!/usr/bin/env python3
"""Characterize real natural-log notation/equivalence limitations separately."""
import sys
sys.dont_write_bytecode=True
import json,subprocess,re,hashlib
from pathlib import Path
H=Path(__file__).parent;E=H.parents[2]/'generate/runs/current/check-engine'
assert hashlib.sha256(E.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
rows=[v for v in json.loads((H/'engine-input.json').read_text())if v['record']['generation']['template']in('q-336717','q-336729')];out=[]
for row in rows:
 endpoint=next(c['submitted']for c in row['checks']if c['purpose'].startswith('true uncollected'))
 for name,t in [('ln',endpoint),('log',endpoint.replace('\\ln','\\log'))]:
  i=len(out);item={'label':row['label']+' '+name,'record':row['record'],'checks':[{'submitted':t,'expected':'accepted','purpose':'equivalent natural-log notation characterization'}]};inp=H/'engine'/('notation-'+str(i)+'-input.json');report=H/'engine'/('notation-'+str(i)+'-report.json');inp.write_text(json.dumps([item],indent=2)+'\n');p=subprocess.run([str(E),str(inp),str(report)],capture_output=True,text=True)
  actual='accepted'
  if p.returncode:
   match=re.search(r'expected accepted, got (rejected|unresolved)',p.stderr);assert match,p.stderr;actual=match[1]
  out.append({'label':item['label'],'notation':name,'submitted':t,'requested':'accepted','actual':actual,'mathematically_valid':True,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'report':json.loads(report.read_text())if p.returncode==0 else None})
(H/'notation-probe.json').write_text(json.dumps(out,indent=2)+'\n')
summary={name:{outcome:sum(r['notation']==name and r['actual']==outcome for r in out)for outcome in ['accepted','rejected','unresolved']}for name in ['ln','log']}
v=json.loads((H/'validation.json').read_text());v['notation_probe']=summary;v['native']['additional_log_equivalent_gaps']=summary['log']['rejected']+summary['log']['unresolved'];(H/'validation.json').write_text(json.dumps(v,indent=2)+'\n');print('Additional natural-log notation probes:',summary)

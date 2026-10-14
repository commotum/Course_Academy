"""Independent displayed-mathematics/native checks at both numeric boundaries."""
import importlib.util,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('v',HERE/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g
items=[]
for t,(level,_) in g.TEMPLATES.items():
 for bound in (2,12):
  p={k:(value if k=='point' or k=='base' and 'common' in t else bound) for k,value in g.PARAMETERS[t].items()}
  if t=='scaled-log':p['base']=3 if bound==2 else 11
  if 'wrong_expbase' in p:p['wrong_expbase']=3 if bound==2 else 11
  r=g.generate(level,0,t,parameters=p);v.inspect_record(r);items.append(v.checks(r,t+'/boundary/'+str(bound)))
(HERE/'boundary-input.json').write_text(json.dumps(items,indent=2)+'\n')
subprocess.run([str(v.ROOT/'generate/runs/current/check-engine'),str(HERE/'boundary-input.json'),str(HERE/'boundary-report.json')],check=True)
print('Displayed mathematical and native checks passed at both bounds for all13 templates')

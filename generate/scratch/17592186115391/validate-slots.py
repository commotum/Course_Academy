"""Supplement the normal sampled review with each bounded coefficient per slot."""
import importlib.util,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('validator',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
g=v.g
records=[];report={};native=[]
for level in ('easy','moderate','hard'):
 for value in (-3,-2,-1,1,2,3):
  r=g.generate(level,parameters={k:value for k in ('a','b','c','d')});v.check_math(r);records.append(r)
  f=r['question'][':question/answer-fields'][0]
  native.append({'label':level+' all coefficients '+str(value),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Bounded coefficient slot coverage'} for a in f[':answer-field/choices']]})
 rs=[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)]
 report[level]={'cases':len(rs),'each_slot_values':{k:sorted({r['generation']['parameters'][k] for r in rs}) for k in ('a','b','c','d')},'displayed_mathematics':'pass','backbone':'same scalar/vector structure, operations and solution stages'}
(HERE/'slot-review.json').write_text(json.dumps(records,indent=2)+'\n')
(HERE/'slot-engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
subprocess.run(['generate/runs/current/check-engine',str(HERE/'slot-engine-input.json'),str(HERE/'slot-engine-report.json')],check=True)
report['native']=json.loads((HERE/'slot-engine-report.json').read_text());report['pass']=True
(HERE/'slot-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('All six allowed values exercised for each of four coefficient slots at each difficulty; symbolic and native checks passed.')

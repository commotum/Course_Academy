import json,re,runpy
from pathlib import Path
H=Path(__file__).resolve().parent
ns=runpy.run_path(str(H/'propose_formulas.py'));canon=ns['canonical'];out=[]
for r in json.loads((H/'comparison.json').read_text()):
 s=r['best']
 if not s or len(s['formulas'])!=len(r['current']):continue
 for i,(old,new)in enumerate(zip(r['current'],s['formulas'])):
  if (r'\cdot'in old or '⋅'in old) and (r'\times'in new or '×'in new):
   a=canon(old).replace(r'\cdot',r'\times').replace('⋅',r'\times');b=canon(new)
   out.append({'entity':r['entity'],'identity':r['identity'],'attribute':r['attribute'],'index':i,'before_tex':old,'source_tex':new,'source_path':s['path'],'only_operator_and_notation_difference':a==b})
(H/'operator-candidate-review.json').write_text(json.dumps(out,indent=2)+'\n')
print('all',len(out),'operator-only',sum(r['only_operator_and_notation_difference']for r in out));print([(r['identity'],r['attribute'],r['index'],r['only_operator_and_notation_difference'])for r in out])

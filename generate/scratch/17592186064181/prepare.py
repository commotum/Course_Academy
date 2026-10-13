import json,re
from pathlib import Path
D=Path(__file__).resolve().parent
s=json.loads((D/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in s['record'][':knowledge-point/questions']}
t={}
for mid,params in [('q-113947',{'a':5}),('q-71663',{'a':3}),('q-71664',{}),('q-49121',{'a':3,'b':2})]:
 q=qs[mid];f=q[':question/answer-fields'][0];values=[a[':answer/value'] for a in f[':answer-field/choices']]
 def convert(x):
  for k,v in params.items():
   # The exponent 3 in q-49121's last distractor is fixed, not inferred from coefficient a.
   x=re.sub(r'(?<![\d{])'+str(v)+r'(?![\d}])',lambda m:'{'+k+'}',x)
  return x
 t[mid]={'difficulty':q[':question/difficulty'][':db/ident'].split('/')[-1],'parameters':params,'variable':'theta' if mid=='q-113947' else ('y' if mid.startswith('q-716') else 'x'),'problem':convert(q[':question/problem']),'solution':convert(q[':question/worked-solution']),'choices':[convert(v) for v in values],'correct_index':values.index(f[':answer-field/correct'][':answer/value']),'field_type':'radio','provenance':'observed complete source bank'}
q=qs['q-113958']
# This extension preserves the rated three-term hard method. Missing source fields cannot be replayed.
p=q[':question/problem'].replace(r'\operatorname{sec}x',r'{acoef}\operatorname{sec}x').replace('2{csc}','{b}{csc}').replace(r'+\operatorname{sin}x',r'+{ccoef}\operatorname{sin}x')
sol=q[':question/worked-solution'].replace(r'\int sin\,',r'\int sin x\,')
# Preserve identities in the recall block; parameterize the calculation block only.
pre,calc=sol.split('Therefore, we get')
calc=calc.replace(r'\operatorname{sec}x',r'{acoef}\operatorname{sec}x').replace('2{csc}','{b}{csc}').replace('2\\int','{b}\\int').replace('2(-','{b}(-').replace('2\\operatorname{cot}','{b}\\operatorname{cot}')
calc=calc.replace(r'+\operatorname{sin}x',r'+{ccoef}\operatorname{sin}x').replace(r'+\int \operatorname{sin}x',r'+{ccoef}\int \operatorname{sin}x').replace(r'+(-\operatorname{cos}x)',r'+{ccoef}(-\operatorname{cos}x)').replace(r'-\operatorname{cos}x+C',r'-{ccoef}\operatorname{cos}x+C')
t['hard-extension']={'difficulty':'hard','parameters':{'a':1,'b':2,'c':1},'variable':'x','problem':p,'solution':pre+'Therefore, we get'+calc,'choices':[r'{acoef}\operatorname{sec}x+{b}\operatorname{cot}x-{ccoef}\operatorname{cos}x+C',r'-{acoef}\operatorname{sec}x+{b}\operatorname{cot}x-{ccoef}\operatorname{cos}x+C',r'{acoef}\operatorname{sec}x-{b}\operatorname{cot}x-{ccoef}\operatorname{cos}x+C',r'{acoef}\operatorname{sec}x+{b}\operatorname{cot}x+{ccoef}\operatorname{cos}x+C',r'-{acoef}\operatorname{sec}x-{b}\operatorname{cot}x+{ccoef}\operatorname{cos}x+C'],'correct_index':0,'field_type':'radio','provenance':'authored bank extension; rated q-113958 prompt and solution, observed radio convention; no source bank existed','source_id':'q-113958'}
(D/'templates.json').write_text(json.dumps(t,indent=2)+'\n')

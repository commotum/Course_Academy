"""Extract exact source slots and complete observed banks; never alters source."""
import json,re
from pathlib import Path
P=Path(__file__).resolve().parent
s=json.loads((P/'source.json').read_text())
specs={'q-49097':('reciprocal',{'n':9}), 'q-29838':('radical',{'n':2}), 'q-71098':('negative_rational',{'a':2,'b':5}), 'q-72059':('negative_radical',{'n':7})}
def slots(text,p):
 return re.sub(r'(?<!\d)\d+(?!\d)',lambda m: next(('@@'+k+'@@' for k,v in p.items() if str(v)==m[0]),m[0]),text)
t={}
for q in s['record'][':knowledge-point/questions']:
 mid=q[':question/math-academy-id']
 if mid not in specs:continue
 kind,p=specs[mid];f=q[':question/answer-fields'][0];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
 t[mid]={'difficulty':'easy','kind':kind,'parameters':p,'source_db_id':q[':db/id'],'problem':slots(q[':question/problem'],p),'solution':slots(q[':question/worked-solution'],p),'values':[slots(a[':answer/value'],p) for a in f[':answer-field/choices']],'correct_index':ci,'field_type':'radio','field_key':f[':answer-field/key'],'profile':mid}
(P/'templates.json').write_text(json.dumps(t,indent=2)+'\n')

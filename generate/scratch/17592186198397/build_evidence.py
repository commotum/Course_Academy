"""Compile full source prose into component masks (private evidence builder)."""
import json,re
from pathlib import Path
D=Path(__file__).resolve().parent
cap=json.loads((D/'source.json').read_text());qs=cap['record'][':knowledge-point/questions']
raw={};cases=[]
for q in qs:
 sid=q[':question/math-academy-id'];key=sid
 f=q[':question/answer-fields'][0]
 spec={'source_id':sid,'problem':q[':question/problem'],'answers':[a[':answer/value'] for a in f[':answer-field/choices']],'components':{}}
 if ':question/worked-solution' in q:spec['solution']=q[':question/worked-solution']
 if ':question/difficulty' in q:spec['difficulty']=q[':question/difficulty'][':db/ident']
 if ':answer-field/correct' in f:spec['correct_index']=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
 spec['height']={'q-38941':2,'q-39054':1,'q-161880':3,'q-39057':4,'q-161879':2}[sid]
 # All answer fragments receive independently variable common-amplitude masks.
 for i,a in enumerate(spec['answers']):
  if sid=='q-38941':
   # Preserve exact historical integrand token w 2, rather than reinterpret power.
   comp='3 w 2' if '3 w 2' in a else '3 w'
   spec['components']['A'+str(i)]=comp;spec['answers'][i]=a.replace(comp,'@@A'+str(i)+'@@')
  else:
   spec['components']['A'+str(i)]=a;spec['answers'][i]='@@A'+str(i)+'@@'
 # Prompt and solution complete mathematical components. Longest first avoids
 # inserting a short subexpression into an unrelated variable argument.
 if sid=='q-38941':components=[r'3\sqrt{z}']
 elif sid=='q-39054':components=[r'\sin (2x + y)\cos (y + z)']
 elif sid=='q-161880':components=[r'2(x+y){e}^{y-x}',r'2u{e}^{v}',r'u{e}^{v}']
 elif sid=='q-39057':components=[r'(2x+z)\operatorname{ln}⁡({x}^{2}+y)',r'\operatorname{sin}⁡u\operatorname{cos}⁡v',r'v\operatorname{ln}⁡u',r'\frac{1}{2}v\operatorname{ln}⁡u']
 else:components=[r'{cos}^{2}⁡(x+z)\operatorname{cos}⁡(z-3y)',r'{cos}^{2}⁡(u+v)\operatorname{cos}⁡v',r'\frac{1}{3}{cos}^{2}⁡(u+v)\operatorname{cos}⁡v']
 for i,c in enumerate(sorted(components,key=len,reverse=True)):
  name='P'+str(i);spec['components'][name]=c
  for field in ('problem','solution'):
   if field in spec:spec[field]=spec[field].replace(c,'@@'+name+'@@')
 # Raw family integral amplitude varies, exact component spelling preserved.
 raw[key]=spec
 cases.append({'source_id':sid,'source_db_id':q[':db/id'],'template':key,'level':'hard' if sid=='q-38941' else 'easy','parameters':{'scale':1,'height':spec['height']},'bank_profile':'raw'})
(D/'raw-templates.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n')
(D/'source-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')

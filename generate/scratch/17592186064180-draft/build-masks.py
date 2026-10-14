"""Extract complete source-owned masks, not sampled source records."""
from pathlib import Path
import json
D=Path(__file__).resolve().parent
s=json.load(open(D/'source.json'));old=json.load(open(D.parent/'17592186064180/templates.json'))
profiles={};cases=[]
for q in s['record'][':knowledge-point/questions']:
 if ':question/math-academy-id' not in q:continue
 mid=q[':question/math-academy-id'];r={k:v for k,v in q.items() if k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields')}
 def enums(x):
  if isinstance(x,dict):
   if ':db/ident' in x:return x[':db/ident']
   return {k:enums(v) for k,v in x.items() if k not in (':db/id',':answer/id',':answer-field/id')}
  if isinstance(x,list):return [enums(v) for v in x]
  return x
 r=enums(r)
 if mid in old:
  t=old[mid];p=t['parameters'];r[':question/problem']=t['problem'];r[':question/worked-solution']=t['solution']
  for a,v in zip(r[':question/answer-fields'][0][':answer-field/choices'],t['choices']):a[':answer/value']=v
  r[':question/answer-fields'][0][':answer-field/correct']=t['choices'][t['correct_index']]
  def convert(x):
   if isinstance(x,str):return x.replace('{a}','@a@').replace('{b}','@b@')
   if isinstance(x,dict):return {k:convert(v) for k,v in x.items()}
   if isinstance(x,list):return [convert(v) for v in x]
   return x
  r=convert(r)
 elif mid=='q-2035':
  p={'a':3}
  r[':question/problem']=r[':question/problem'].replace('3','@a@')
  for a in r[':question/answer-fields'][0][':answer-field/choices']:a[':answer/value']=a[':answer/value'].replace('3','@a@')
 elif mid=='q-49118':
  p={'a':8};r[':question/problem']=r[':question/problem'].replace('8','@a@')
  for a in r[':question/answer-fields'][0][':answer-field/choices']:a[':answer/value']=a[':answer/value'].replace('8','@a@').replace('4','@half@')
 elif mid=='q-113935':
  p={'n':3,'d':2}
  for k in (':question/problem',':question/worked-solution'):r[k]=r[k].replace(r'\frac{3}{2}',r'\frac{@n@}{@d@}')
 elif mid=='q-2162':
  p={'a':2}
  for k in (':question/problem',':question/worked-solution'):r[k]=r[k].replace('2{sec}','@a@{sec}').replace(r'2\operatorname{tan}',r'@a@\operatorname{tan}').replace(r'2\int',r'@a@\int')
 elif mid=='q-2165':
  p={'b':1};r[':question/problem']=r[':question/problem'].replace('{sec}^{2}x','@coef@{sec}^{2}x')
  opening,chain=r[':question/worked-solution'].split('Therefore, we have',1)
  chain=chain.replace('{sec}^{2}x','@coef@{sec}^{2}x').replace(r'-\int',r'-@coef@\int').replace(r'-\operatorname{tan}',r'-@coef@\operatorname{tan}')
  # Extracting b before the formal integral is the operative stage.
  chain=chain.replace(r'-@coef@\int @coef@{sec}',r'-@coef@\int {sec}')
  r[':question/worked-solution']=opening+'Therefore, we have'+chain
 level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/'+('easy' if mid=='q-2035' else 'moderate')).split('/')[-1]
 profiles[mid]={'level':level,'parameters':p,'record_mask':r,'evidence_only':mid in ('q-2035','q-49118','q-113935','q-2162','q-2165'),'parameter_constraints':'positive magnitudes 1..9; nonunit easy coefficient a>=2; reduced fractions n,d in 2..9, n!=d; q-49118 even a to preserve integral half-coefficient','interpretation':'q-49118 half-scale/cross-function opaque; retained expression pattern only, no claimed recovered error intent.' if mid=='q-49118' else 'Complete observed expression bank and operative source stages.'}
 cases.append({'source_id':mid,'template':mid,'profile':'raw:'+mid,'level':level,'parameters':p})
(D/'source-profiles.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')

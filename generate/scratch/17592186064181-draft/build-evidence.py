from pathlib import Path
import json,hashlib,copy,re
D=Path(__file__).resolve().parent;R=D.parents[2];K=17592186064181
files=[D.parent/f'{K}.py']+sorted(p for p in (D.parent/str(K)).rglob('*') if p.is_file())
baseline={'paths':[str(p.relative_to(R)) for p in files],'sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(D/'registered-baseline-hashes.json').write_text(json.dumps(baseline,indent=2)+'\n')
S=R/'generate/runs/current/refresh-2026-10-14'
for dest,src in [('source.json',S/f'sources/{K}.json'),('topic.json',S/'topics/17592186048777.json'),('lesson.json',S/'lessons/17592186048777.json')]: (D/dest).write_bytes(src.read_bytes())
s=json.load(open(D/'source.json'));old=json.load(open(D.parent/str(K)/'templates.json'))
def enums(x):
 if isinstance(x,dict):
  if ':db/ident' in x:return x[':db/ident']
  return {k:enums(v) for k,v in x.items() if k not in (':db/id',':answer/id',':answer-field/id')}
 if isinstance(x,list):return [enums(v) for v in x]
 return x
profiles={};cases=[]
for q in s['record'][':knowledge-point/questions']:
 mid=q.get(':question/math-academy-id')
 if not mid:continue
 r=enums({k:v for k,v in q.items() if k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields')})
 if ':question/answer-fields' in r:
  for f,of in zip(r[':question/answer-fields'],q[':question/answer-fields']):
   if ':answer-field/correct' in f:f[':answer-field/correct']=of[':answer-field/correct'][':answer/value']
 if mid in old:
  t=old[mid];p=t['parameters'];r[':question/problem']=t['problem'];r[':question/worked-solution']=t['solution']
  for a,v in zip(r[':question/answer-fields'][0][':answer-field/choices'],t['choices']):a[':answer/value']=v
  r[':question/answer-fields'][0][':answer-field/correct']=t['choices'][t['correct_index']]
  def conv(x):
   if isinstance(x,str):return x.replace('{a}','@a@').replace('{b}','@b@')
   if isinstance(x,list):return [conv(v) for v in x]
   if isinstance(x,dict):return {k:conv(v) for k,v in x.items()}
   return x
  r=conv(r)
 elif mid in ('q-2037','q-49093'):
  p={'a':2}
  def conv(x):
   if isinstance(x,str):return x.replace('2', '@a@') if mid=='q-49093' else x.replace('2\\', '@a@\\')
   if isinstance(x,list):return [conv(v) for v in x]
   if isinstance(x,dict):return {k:conv(v) for k,v in x.items()}
   return x
  r=conv(r)
 elif mid=='q-113948':
  p={'n':5,'d':2}
  for k in (':question/problem',':question/worked-solution'):r[k]=r[k].replace(r'\frac{5}{2}',r'\frac{@n@}{@d@}')
 elif mid=='q-113952':
  p={'a':3,'b':4}
  for k in (':question/problem',':question/worked-solution'):r[k]=r[k].replace('3','@a@').replace('4','@b@')
 elif mid=='q-113958':
  p={'a':1,'b':2,'c':1}
  r[':question/problem']=r[':question/problem'].replace(r'\operatorname{sec}x\operatorname{tan}x',r'@acoef@\operatorname{sec}x\operatorname{tan}x').replace('-2','-@b@').replace('+2','+@b@').replace(r'\operatorname{sin}x',r'@ccoef@\operatorname{sin}x')
  opening,chain=r[':question/worked-solution'].split('Therefore, we get',1)
  chain=chain.replace(r'\operatorname{sec}x\operatorname{tan}x',r'@acoef@\operatorname{sec}x\operatorname{tan}x').replace('-2','-@b@').replace('+2','+@b@').replace(r'+\operatorname{sin}x',r'+@ccoef@\operatorname{sin}x').replace(r'+\int \operatorname{sin}x',r'+@ccoef@\int \operatorname{sin}x').replace(r'(-\operatorname{cos}x)',r'@ccoef@(-\operatorname{cos}x)').replace(r'-\operatorname{cos}x+C',r'-@ccoef@\operatorname{cos}x+C')
  # Primitive substitution of sec and its final simplified term retain coefficient a.
  chain=chain.replace(r'=\operatorname{sec}x',r'=@acoef@\operatorname{sec}x')
  r[':question/worked-solution']=opening+'Therefore, we get'+chain
 elif mid in ('q-143522','q-167569'):
  n=4 if mid=='q-143522' else 2;p={'a':n}
  r[':question/worked-solution']=r[':question/worked-solution'].replace(str(n),'@a@').replace('^{@a@}','^{2}')
  f=r[':question/answer-fields'][0];f[':answer-field/correct']=f[':answer-field/correct'].replace(str(n),'@a@')
  f[':answer-field/choices'][0][':answer/value']=f[':answer-field/choices'][0][':answer/value'].replace(str(n),'@a@')
 elif mid=='q-71666':
  p={'b':5}
  def conv(x):
   if isinstance(x,str):return x.replace('5','@b@')
   if isinstance(x,list):return [conv(v) for v in x]
   if isinstance(x,dict):return {k:conv(v) for k,v in x.items()}
   return x
  r=conv(r)
 else:raise ValueError(mid)
 level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/'+('easy' if mid=='q-2037' else 'moderate')).split('/')[-1]
 profiles[mid]={'level':level,'parameters':p,'record_mask':r,'provenance':'Exact MA evidence parameterized without repairing absent or malformed data.'}
 cases.append({'source_id':mid,'template':mid,'profile':'raw:'+mid,'level':level,'parameters':p})
(D/'source-profiles.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
ind=[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Distinct current generated inventory record sharing the direct-primitive templates; preserved exactly and excluded from MA source and difficulty evidence counts.'} for q in s['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
(D/'independent-inventory.json').write_text(json.dumps({'basis':s['basis'],'lineage':s['lineage'],'questions':ind},ensure_ascii=False,indent=2)+'\n')

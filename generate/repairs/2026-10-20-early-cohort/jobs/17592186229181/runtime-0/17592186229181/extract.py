"""One-time frozen-source mask extraction. No database access."""
import json,re
from decimal import Decimal
from pathlib import Path
D=Path(__file__).parent
src=json.loads((D/'source.json').read_text())['record']
base={17592186229724:(750,30,'.03',6,None),17592186229725:(900,30,'.02',10,6),17592186377242:(720,12,'.03',3,5),17592186377256:(500,25,'.02',7,None),17592186377263:(400,20,'.03',3,None),17592186377279:(450,30,'.02',2,None),17592186377286:(350,25,'.02',8,4)}
def marker(k):return '⟦'+k+'⟧'
profiles={};cases=[]
for q in src[':knowledge-point/questions']:
 sid=q[':db/id'];V,r,c,q0,T=base[sid];c=Decimal(c); E=c*V;B=Decimal(q0)-E; F=c*r
 p=q[':question/problem']; numbers=list(re.finditer(r'\d+(?:\.\d+)?',p)); roles=['V','q0','c','r','r']+(['T'] if T else [])
 assert len(numbers)==len(roles),(sid,numbers)
 for m,k in reversed(list(zip(numbers,roles))):p=p[:m.start()]+marker(k)+p[m.end():]
 sol=q.get(':question/worked-solution')
 if sol:
  # Complete component masks for implicit unit coefficients and supplied fractions.
  sol=sol.replace(r'\frac{1}{2}',marker('F_fraction'))
  sol=sol.replace('A & ='+str(int(B)) if B==int(B) else 'A & ='+format(B,'f').rstrip('0').rstrip('.'),'A & ='+marker('B'))
  if B==1:
   sol=sol.replace('+{e}^{',marker('Bterm')+'{e}^{')
  ms=list(re.finditer(r'(?<![\d.])\d+(?:\.\d+)?(?!\d)',sol))
  for m in reversed(ms):
   n=m.group();v=Decimal(n);before=sol[max(0,m.start()-15):m.start()];after=sol[m.end():m.end()+70];key=None
   if before.endswith('**Step '):continue
   if v==c:key='c'
   elif v==V:key='V'
   elif v==r and ('text{L}' in after[:40] or 'text{L/min}' in after[:40] or after.startswith('Q}')):key='r'
   elif v==F:key='F'
   elif v==E:key='E'
   elif v==abs(B) and before.endswith('-'):key='absB'
   elif v==q0:key='q0'
   elif T and v==T and (before.endswith('$') or before.endswith('Q(') or before.endswith('^{-')):key='T'
   if '≈' in before and not after.startswith('/'):key='rounded'
   if key:sol=sol[:m.start()]+marker(key)+sol[m.end():]
  # Never transform fixed degree, derivative zeros, tau, or formal 1/tau numerators.
 bank=[]
 for a in q[':question/answer-fields'][0][':answer-field/choices']:
  v=a[':answer/value']; vals=[]
  if v.startswith('Q(t)'):
   cutoff=v.index('e');head=v[:cutoff];tail=v[cutoff:]
   for i,m in enumerate(re.finditer(r'\d+(?:\.\d+)?',head)):vals.append(m.group())
   for i,m in reversed(list(enumerate(re.finditer(r'\d+(?:\.\d+)?',head)))):head=head[:m.start()]+marker('mass_'+str(i))+head[m.end():]
   mask=head+tail
  else:
   m=re.match(r'\d+(?:\.\d+)?',v);vals=[m.group()];mask=marker('mass_0')+v[m.end():]
  bank.append({'mask':mask,'mass_values':vals,'original_value':v,'original_id':a[':answer/id']})
 f=q[':question/answer-fields'][0];level=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or ('moderate' if T else 'easy')
 profiles[str(sid)]={'prompt_mask':p,'solution_mask':sol,'bank':bank,'field_key':f[':answer-field/key'],'has_correct':':answer-field/correct' in f,'correct_index':next((i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')),None),'difficulty_present':':question/difficulty' in q,'level':level,'base':{'V':str(V),'r':str(r),'c':str(c),'q0':str(q0),'T':str(T) if T else None},'source_id':sid,'source_ma_id':q[':question/math-academy-id']}
 cases.append({'source_id':sid,'template':'source_'+str(sid),'parameters':{'mass_scale':'1','flow_scale':'1'},'bank_profile':'raw_'+str(sid),'level':level})
(D/'masks.json').write_text(json.dumps(profiles,indent=2,ensure_ascii=False)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')

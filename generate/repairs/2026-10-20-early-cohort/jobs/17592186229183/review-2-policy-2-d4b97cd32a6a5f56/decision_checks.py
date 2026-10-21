import sys
sys.dont_write_bytecode=True
import json,random,importlib.util,re
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch
from decimal import Decimal,ROUND_HALF_UP
from collections import Counter
R=Path(__file__).resolve().parent;P=R.parent/'workspace'
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def load(n):return json.loads((R/n).read_text())
spec=importlib.util.spec_from_file_location('candidate',P/'17592186229183.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def num(s):
 m=re.search(r'\\frac\{(\d+)\}\{(\d+)\}',s)
 return F(int(m[1]),int(m[2])) if m else F(re.search(r'\d+(?:\.\d+)?',s)[0])
def info(r):
 f=r['question'][':question/answer-fields'][0];a=f[':answer-field/choices'];vals=[num(x[':answer/value']) for x in a];k=f[':answer-field/correct'][1];i=next(i for i,x in enumerate(a) if x[':answer/id']==k)
 ordered=sorted(vals);mu=sum(vals)/5
 v=lambda z:next(j for j,x in enumerate(vals) if x==z)
 strategies={f'position {j+1}':j for j in range(5)}|{f'numeric rank {j+1}':v(ordered[j]) for j in range(5)}
 strategies|={'nearest mean':v(min(ordered,key=lambda x:abs(x-mu))),'smallest nearest-neighbor gap':v(min(ordered,key=lambda x:min(abs(x-y) for y in vals if y!=x))),'largest nearest-neighbor gap':v(max(ordered,key=lambda x:min(abs(x-y) for y in vals if y!=x)))}
 elig=[j for j,x in enumerate(vals) if max(abs(x-y) for y in vals)<=2]
 if len(elig)==1:strategies['unique 2 lb radius center']=elig[0]
 return {'question_id':r['question'][':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'key_value':str(vals[i]),'rank':ordered.index(vals[i])+1,'position':i+1,'ordered':[str(x) for x in ordered],'strategies':{k:{'correct':j==i,'selected_id':a[j][':answer/id']} for k,j in strategies.items()}}
Real=random.Random
class Shape(Real):
 def __init__(self,seed):super().__init__(seed);self.i=0
 def randint(self,a,b):
  self.i+=1
  if self.i==1:return super().randint(a,b)
  assert (a,b)==(1,20)
  return 10
seeds={}
for seed in range(58001,58101):seeds.setdefault(Real(seed).randint(1,5),seed)
assert len(seeds)==5
controls=[]
for rank,seed in sorted(seeds.items()):
 p={'H':'100','v':'50','q':str(1+4*(rank-1)),'c':'0.4','rin':'6','rout':'4'}
 with patch.object(g.random,'Random',Shape):r=g.generate('easy',seed=seed,template='q-336506',parameters=p)
 H,v,q,c,ri,ro=[num(z) for z in re.findall(r'\$([^$]+)\$',r['question'][':question/problem'])[:6]]
 exact=c*H+(q-c*v)*(v/H)**2;rounded=(Decimal(exact.numerator)/Decimal(exact.denominator)).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
 z=info(r);assert F(z['key_value'])==F(rounded);assert z['rank']==rank
 assert re.search(r'[≈=]'+str(rounded)+r'\\,',r['question'][':question/worked-solution'])
 controls.append(r)
assert len({tuple(info(r)['ordered']) for r in controls})==1
save('same-bank-records.json',controls)
# Low eligible physical boundary: replay all key roles; rejection retains rank.
low=[g.generate('easy',seed=seeds[j],template='q-336506',parameters={'H':'20','v':'10','q':'1','c':'0.4','rin':'6','rout':'4'}) for j in range(1,6)]
assert [info(r)['rank'] for r in low]==list(range(1,6));save('low-boundary-records.json',low)
sets={'fresh sample before':load('sample-records.json'),'fresh sample after':load('delivery-sample/accepted.json'),'exact batch before':load('batch-records.json'),'exact batch after':load('delivery-batch/accepted.json'),'same bank':controls,'low mass boundary':low}
results={};probes=[]
for label,rs in sets.items():
 rows=[info(r) for r in rs];groups={'all':rows}
 if 'sample' in label or 'batch' in label:
  groups|={t:[z for z in rows if z['template']==t] for t in sorted({z['template'] for z in rows})}
 results[label]={'rows':rows,'groups':{}}
 for group,zs in groups.items():
  counts={}
  for name in sorted(set().union(*(z['strategies'] for z in zs))):
   eligible=[z for z in zs if name in z['strategies']];n=len(eligible);c=sum(z['strategies'][name]['correct'] for z in eligible);counts[name]={'correct':c,'total':n,'baseline':.2}
  results[label]['groups'][group]=counts
save('decision-results.json',{'command':sys.argv,'seed_by_rank':seeds,'shape_draws':[10,10,10,10],'results':results,'assessment':'All five keys are possible with the same visible bank. The fixed radius, numerical rank, mean and nearest-neighbor geometric selectors fail under changed relevant evidence. Batch is evaluated independently; finite chance imbalances are not structural guarantees.'})
# Merge all learner grading into one native invocation.
cases=load('grader-input.json')
for label,rs in [('same-bank',controls),('low-mass',low)]:
 for r in rs:
  z=info(r);f=r['question'][':question/answer-fields'][0]
  cases.append({'label':label+' / rank '+str(z['rank']),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if num(a[':answer/value'])==F(z['key_value']) else 'rejected','purpose':'independent mass calculation, all displayed choices'} for a in f[':answer-field/choices']]})
save('grader-input.json',cases)
save('render-records.json',load('delivery-batch/accepted.json')+load('counterfactual-records.json')+controls+low[-1:]+[load('sample-records.json')[i*4] for i in range(len(g.MASKS))])
print(json.dumps({'seed_by_rank':seeds,'same_bank_keys':[info(r)['key_value'] for r in controls],'batch_probes':results['exact batch after']['groups']['all'],'native_cases':len(cases)}))

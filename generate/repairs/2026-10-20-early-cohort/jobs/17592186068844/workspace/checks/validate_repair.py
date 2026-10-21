"""Executable regression for 6343bb7c5cb9de00ecc6. Reads displayed math.

Checks the exact old probe and all five coefficient decisions with the other
mathematical data held fixed, across every retained template. No runtime writes.
"""
import collections, importlib.util, json, re, sys
from pathlib import Path
import audit as a
W=Path(__file__).resolve().parent.parent
E=W/'evidence';E.mkdir(exist_ok=True)
def save(name,obj):(E/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def key_value(r):return next(z[':answer/value'] for z in a.field(r)[':answer-field/choices'] if z[':answer/id']==a.answer_id(a.field(r)))
def bank(r):return sorted(z[':answer/value'] for z in a.field(r)[':answer-field/choices'])
def stages(r):
 # Differentiate every evaluated intermediate equation, including separation.
 q=r['question'];rhs=a.parse(q[':question/problem'].split('=')[1].split('$')[0].rstrip('., '))
 p=r['generation']['parameters'];u,v=a.s.symbols('u v',positive=True)
 sub={a.x:u-p.get('h',0),a.y:v-p.get('k',0)}
 count=0
 for block in re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',q[':question/worked-solution']):
  for row in block.split(r'\\'):
   if r'\int' in row:continue
   l,rr=row.split('& =');l=l.strip();rr=rr.strip().rstrip('.,').replace('K','C')
   if a.g.D in l:
    factor=l.replace(a.g.D,'').strip() or '1'
    assert a.zero(a.parse(factor)*rhs-a.parse(rr)),(l,rr)
   else:
    left=a.parse(l).subs(sub,simultaneous=True);right=a.parse(rr).subs(sub,simultaneous=True)
    assert a.zero(a.s.diff(left,v)*rhs.subs(sub,simultaneous=True)-a.s.diff(right,u)),(l,rr)
   count+=1
 return count

def main():
 exact=a.g.generate_easy(seed=101,template='exp_linear',parameters={'h':0,'k':0})
 assert a.shortcut(exact)!=[a.answer_id(a.field(exact))], 'original shortcut persists'
 source=json.loads((a.JOB/'source/source.json').read_text())['material']['kp']
 replay=[];records=[];groups=[];math=[];intermediate=0;shuffles=[]
 for t,(level,sid) in a.g.TEMPLATES.items():
  p={'h':0,'k':0} if sid else {'a':3,'b':-2,**({'d':2} if level=='hard' else {})}
  if sid:
   q=next(q for q in source[':knowledge-point/questions'] if q[':question/math-academy-id']==sid)
   r=a.g.generate(level,101,t,parameters=p,profile='observed');f=q[':question/answer-fields'][0]
   assert r['question'][':question/problem']==q[':question/problem']
   assert r['question'][':question/worked-solution']==q[':question/worked-solution']
   assert bank(r)==sorted(z[':answer/value'] for z in f[':answer-field/choices'])
   assert key_value(r)==f[':answer-field/correct'][':answer/value']
   replay.append({'template':t,'source_id':q[':question/id'],'complete_bank':5,'exact':True})
  group=[a.g.generate(level,seed=101,template=t,parameters={**p,'c':c}) for c in (-2,-1,1,2,3)]
  assert len({json.dumps(bank(r)) for r in group})==1
  assert len({key_value(r) for r in group})==5
  assert len({r['question'][':question/problem'] for r in group})==5
  assert len({r['question'][':question/worked-solution'] for r in group})==5
  assert all(a.shortcut(r)!=[a.answer_id(a.field(r))] for r in group)
  # All five distinct keys share identical ordered visible choices for this seed.
  assert len({tuple(z[':answer/value'] for z in a.field(r)[':answer-field/choices']) for r in group})==1
  groups.append({'template':t,'roles':[-2,-1,1,2,3],'identical_ordered_visible_bank':True,'distinct_correct_values':5,'best_choice_only_prediction':{'successes':1,'attempts':5}})
  for r in group:
   z=a.inspect_record(r);assert z['passed'],z;math.append(z);intermediate+=stages(r)
  # Mathematical equivalence checks ignore metadata and read every displayed side.
  for r in group:
   relations=[a.relation(z[':answer/value']) for z in a.field(r)[':answer-field/choices']]
   for i,(l,rr) in enumerate(relations):
    for ll,rrr in relations[i+1:]:
     assert not a.zero(a.deriv(l,a.y)*a.deriv(rrr,a.x)-a.deriv(ll,a.y)*a.deriv(rr,a.x))
  shuffled=a.g.generate(level,seed=102,template=t,parameters={**p,'c':1})
  one=group[2]
  assert key_value(shuffled)==key_value(one)
  assert shuffled['question'][':question/problem']==one['question'][':question/problem']
  assert shuffled['question'][':question/worked-solution']==one['question'][':question/worked-solution']
  shuffles.append((one,shuffled))
  records.extend(group)
 # Small ordinary sample plus translated boundary cases; no exhaustive seed sweep.
 sampled=[a.g.generate_easy(seed=829331+i) for i in range(22)]
 boundaries=[a.g.generate_easy(77,t,parameters={'h':0 if 'autonomous' in t else h,'k':h,'c':c}) for t,(level,sid) in a.g.TEMPLATES.items() if sid for h,c in [(-6,-2),(6,3)]]
 for r in sampled+boundaries:
  z=a.inspect_record(r);assert z['passed'],z;math.append(z);intermediate+=stages(r)
 assert all(r==a.g.generate_easy(seed=r['generation']['seed']) for r in sampled)
 for r in sampled:
  replayed=a.g.generate('easy',r['generation']['seed'],r['generation']['template'],parameters=r['generation']['parameters'])
  assert replayed['question'][':question/id']==r['question'][':question/id'] and bank(replayed)==bank(r)
 save('source-replay.json',replay);save('controlled-records.json',records);save('test-records.json',records+sampled+boundaries)
 save('math-results.json',math)
 cases=[]
 for i,r in enumerate(records+sampled+boundaries):
  f=a.field(r)
  cases.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==a.answer_id(f) else 'rejected','purpose':'displayed equation independently differentiated'} for z in f[':answer-field/choices']]})
 for one,shuffled in shuffles:
  cases.append({'label':'irrelevant shuffle '+shuffled['generation']['template'],'record':shuffled,'checks':[{'submitted_answer_id':a.answer_id(a.field(one)),'expected':'accepted','purpose':'unchanged correct response after irrelevant option-order change'}]})
 save('grader-input.json',cases)
 save('repair-results.json',{'finding':'6343bb7c5cb9de00ecc6','exact_counterexample_passed':True,'source_banks':replay,'controlled_groups':groups,'math_records':len(math),'evaluated_solution_rows':intermediate,'natural_seed_sample':22,'boundary_cases':22,'limitations':['Complete-bank canonical-example replay unavailable: source has no answer bank.','Live learner history and weighted selection are not accessible offline.']})
 print(json.dumps({'passed':True,'source_banks':len(replay),'controlled_groups':len(groups),'math_records':len(math),'solution_rows':intermediate}))
if __name__=='__main__':main()

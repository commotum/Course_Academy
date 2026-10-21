"""Offline source replay, printed mathematics, controlled cases and shortcut audit.
Run with the job Python. Writes only evidence files; no services or DB access.
"""
import sys,json,pathlib,importlib.util,collections,re
sys.dont_write_bytecode=True
P=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'checks'))
import math_witness as w
g=w.g
E=P/'evidence';E.mkdir(exist_ok=True)
SOURCE=P.parent/'source/source.json'
def save(name,x):(E/name).write_text(json.dumps(x,indent=2)+'\n')
def key(r):
 f=r['question'][':question/answer-fields'][0]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def score(r):
 env=w.physics(r);f=r['question'][':question/answer-fields'][0]
 values=[w.algebra(a[':answer/value'],env) for a in f[':answer-field/choices']]
 k=w.algebra(key(r),env)
 return dict(rank=sorted(values).index(k)+1,position=next(i+1 for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]),single_digit=all(x.is_Integer and 0<x<10 for x in values),same_length=len({len(a[':answer/value']) for a in f[':answer-field/choices']})==1)
def coverage(records):
 groups=collections.defaultdict(list)
 for r in records:
  a=score(r);groups[r['generation']['template']].append(a)
  if a['single_digit']:groups[r['generation']['template']+':single-digit'].append(a)
  if a['same_length']:groups[r['generation']['template']+':same-length'].append(a)
  else:groups[r['generation']['template']+':mixed-length'].append(a)
 return {name:{'count':len(rows),'ranks':dict(collections.Counter(x['rank'] for x in rows)),'positions':dict(collections.Counter(x['position'] for x in rows)),'second_smallest_successes':sum(x['rank']==2 for x in rows)} for name,rows in groups.items()}
def run():
 src=json.loads(SOURCE.read_text())['material']['kp'][':knowledge-point/questions']
 replays=[];fidelity=[]
 for q in src:
  ma=q[':question/math-academy-id'];m=g.M[ma];r=g.generate(m['level'],1943,template=ma,parameters=m['parameters'],profile='observed:'+ma);rq=r['question'];f=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
  for name in [':question/problem',':question/worked-solution',':question/requires-calculator']:
   assert rq.get(name)==q.get(name),(ma,name)
  expected=q.get(':question/difficulty',{}).get(':db/ident');assert rq.get(':question/difficulty')==expected
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in rf)
  if ':answer-field/correct' in f:assert key(r)==f[':answer-field/correct'][':answer/value']
  w.check_math(r);w.formatting(r);replays.append(r);fidelity.append({'source_id':q[':question/id'],'template':ma,'prompt_solution_bank_difficulty_calculator':True,'choice_count':5,'missing_key_preserved':':answer-field/correct' not in f})
 save('source-replays.json',replays);save('source-replay-results.json',fidelity)
 records=[];signs=collections.defaultdict(set);samples=[]
 # Three sign branches for each source-supported presentation and exponent.
 for ma,m in g.M.items():
  p=m['parameters'];alpha=g.exact(p['c'])*g.exact(p['V'])
  for q in [alpha-1,alpha,alpha+1]:
   if 1<=q<=50:
    r=g.generate(m['level'],619,template=ma,parameters=dict(p,q0=str(q)))
    env=w.check_math(r);w.formatting(r);signs[ma].add(int(w.sp.sign(env['beta'])));records.append(r)
  for seed in range(5):
   r=g.generate(m['level'],seed,template=ma);env=w.check_math(r);w.formatting(r);records.append(r);samples.append(r)
 # Exact retained counterexamples, including binary float input interpreted as decimal.
 for ma,p in [('q-336439',dict(V=100,q0=3,c='.04',rin=8,rout=12)),('q-336439',dict(V=240,q0=15,c='.05',rin=16,rout=24)),('q-339400',dict(V=320,q0=2.2,c='.05',rin=8,rout=4,T=5)),('q-336746',g.M['q-336746']['parameters']),('q-336744',g.M['q-336744']['parameters'])]:
  r=g.generate(g.M[ma]['level'],8114,template=ma,parameters=p);w.check_math(r);w.formatting(r);records.append(r)
 # Target/evidence counterfactuals: initial mass changes; unrelated physical data change.
 base=dict(V=100,q0=3,c='.04',rin=8,rout=12)
 changed=g.generate('easy',733,parameters=dict(base,q0=4));original=g.generate('easy',733,parameters=base)
 irrelevant=g.generate('easy',733,parameters=dict(base,V=200,c='.025',rin=16,rout=24))
 assert key(changed)!=key(original) and key(irrelevant)==key(original)
 # Hold physical data fixed and change requested source-supported coefficient role.
 target=g.generate('moderate',733,template='q-339394',parameters=base)
 assert key(target)!=key(original)
 for r in [original,changed,irrelevant,target]:w.check_math(r);w.formatting(r)
 controls=[original,changed,irrelevant,target];records+=controls
 # Focused within-template probe: enough eligible single-digit banks to be nonvacuous.
 probes=[]
 for q in range(3,10):
  for seed in range(8):
   r=g.generate('easy',seed,parameters=dict(base,q0=q));w.check_math(r);probes.append(r)
 c=coverage(probes);single=c['q-336439:single-digit']
 assert single['count']>=5 and len(single['ranks'])>=3 and single['second_smallest_successes']<single['count']
 assert len(c['q-336439']['ranks'])==5 and len(c['q-336439']['positions'])==5
 for ma,sg in signs.items():assert sg=={-1,0,1},(ma,sg)
 # Boundary cases are permitted, and structurally invalid cases remain rejected.
 for p in [dict(V=100,q0=1,c='.01',rin=8,rout=12),dict(V=1200,q0=50,c='.08',rin=16,rout=24)]:
  r=g.generate('easy',61,parameters=p);w.check_math(r);records.append(r)
 for p in [dict(base,c=0),dict(base,rin=12),dict(base,T=1),dict(base,q0=-1)]:
  try:g.generate('easy',1,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('invalid physical instance accepted',p))
 records+=probes
 save('records.json',records);save('controls.json',controls);save('probes.json',probes)
 save('representatives.json',[original,changed,records[0],next(r for r in records if r['generation']['template']=='q-336746'),next(r for r in records if r['generation']['template']=='q-339400' and r['generation']['parameters']['q0']=='2.2')])
 save('coverage-before.json',coverage(records));save('math.json',{'records_checked':len(records)+len(replays),'source_replays':len(replays),'all_printed_solution_equalities_checked':True,'sign_coverage':{k:sorted(v) for k,v in signs.items()},'source_rational_cases':True,'counterfactuals':{'changed_initial_amount':[key(original),key(changed)],'irrelevant_physical_data':[key(original),key(irrelevant)],'same_data_different_coefficient_target':[key(original),key(target)]}})
 # Full response banks batched through the real learner engine, including controls.
 engine=[]
 for i,r in enumerate(records+replays):
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  engine.append({'label':str(i)+':'+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'visible complete radio bank; independently checked numeric key'} for a in f[':answer-field/choices']]})
 save('grader-input.json',engine)
 for level in ['easy','moderate','hard']:save('delivery-'+level+'-input.json',[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)])
 print(json.dumps({'checked_records':len(records),'replays':len(replays),'signs':{k:sorted(v) for k,v in signs.items()},'single_digit_probe':single,'engine_cases':len(engine)}))
if __name__=='__main__':run()

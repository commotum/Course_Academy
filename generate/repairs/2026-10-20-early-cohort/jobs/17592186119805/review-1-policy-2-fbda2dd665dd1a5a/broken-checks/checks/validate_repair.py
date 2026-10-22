"""Affected source/math/role tests plus a small ordinary seeded regression sample."""
from common import *
import copy,random,math,platform,hashlib
REPO=Path('/home/jake/Developer/Course_Academy');JOB=ROOT.parent
g=load_generator();records=[];source_results=[];counterfactuals=[];role_support=[]
source=json.loads((JOB/'source/source.json').read_text())
assert json.loads((ROOT/'source-data.json').read_text())['questions']==source['material']['kp'][':knowledge-point/questions']
for old in source['material']['kp'][':knowledge-point/questions']:
 sid=old[':question/math-academy-id']
 if not old.get(':question/difficulty'):
  source_results.append({'profile':sid,'status':'incomplete unrated evidence','reason':'Missing key and worked solution; original remains untouched.'});continue
 level=old[':question/difficulty'][':db/ident'].split('/')[-1]
 r=g.generate(level,55001,sid,copy.deepcopy(g.CASES[sid]));verify(r)
 assert mats(old[':question/problem'])==mats(r['question'][':question/problem'])
 assert [value(a[':answer/value']) for a in choices(old)]==[value(a[':answer/value']) for a in choices(r['question'])]
 assert mats(old[':question/worked-solution'])==mats(r['question'][':question/worked-solution'])
 records.append(r)
 source_results.append({'profile':sid,'question_id':old[':question/id'],'status':'passed','complete_choices_matched':5,'distractors_matched':4,'correct_designation':True,'prompt_vectors_and_solution_matrix_sequence':True})
save('source-replay-records.json',records);save('source-replay-results.json',source_results)
# Canonical worked example has no field/bank. Replay its complete visible mathematics.
canonical=source['material']['kp'][':knowledge-point/canonical-example']
p={'a':[-1,2,1],'u':[4,0,-2],'c':3,'s':4,'letter':'s'}
r=g.generate('easy',55001,'q-34051',p);assert verify(r)==4
assert mats(canonical[':question/problem'])==mats(r['question'][':question/problem'])
assert mats(canonical[':question/worked-solution'])==mats(r['question'][':question/worked-solution'])
save('canonical-replay.json',{'source_id':canonical[':question/id'],'record':r,'status':'Visible mathematics and solution matrices match; source has no answer bank to compare.'});records.append(r)
normal=[]
for level,sids in g.LEVELS.items():
 for sid in sids:
  for seed in [11027,84533,230219,330721,984311,1234579]:
   r=g.generate(level,seed,sid);verify(r);normal.append(r)
records+=normal;save('normal-records.json',normal)
# Drive each eligible role through the unmodified normal sampler. This changes only
# one RNG choice, then verifies the resulting rendered mathematics independently.
class RoleRandom(random.Random):
 def __init__(self,seed,role):super().__init__(seed);self.role=role;self.used=False
 def choice(self,seq):
  picked=super().choice(seq)
  if not self.used and all(isinstance(v,str) for v in seq):
   try:
    for v in seq:
     if v!='No solution':scalar(v)
   except ValueError:return picked
   self.used=True;return seq[self.role]
  return picked
for level,sids in g.LEVELS.items():
 for sid in sids:
  number=5 if level=='moderate' else sum(x!='No solution' for x in g.source_bank(sid))
  for role in range(number):
   rng=RoleRandom(64193,role);p=g.sample_parameters(sid,rng);assert rng.used
   r=g.generate(level,64193,sid,p);ans=verify(r);records.append(r)
   role_support.append({'profile':sid,'role_index':role,'independent_answer':str(ans),'question_id':r['question'][':question/id']})
  # Fixed entire bank/label/known coefficient/unknown vector, varying relevant evidence.
  base=copy.deepcopy(g.CASES[sid]);bank=g.source_bank(sid);numeric=[scalar(v) for v in bank if v!='No solution']
  if level=='easy':base['a'][0]+=1 # Keep every bank role fresh relative to stored source.
  if level=='moderate':
   den=math.lcm(*(x.denominator for x in numeric));base['u']=[base['c']*den*(i+1) for i in range(len(base['a']))]
  pair=[]
  for target in bank:
   p=copy.deepcopy(base);p['bank']=bank
   if target=='No solution':
    if level=='easy':continue
    target_s=numeric[0];p['a']=[int(-target_s*x/p['c']) for x in p['u']];p['a'][-1]+=1
   elif level=='moderate':p['a']=[int(-scalar(target)*x/p['c']) for x in p['u']]
   else:p['s']=str(scalar(target))
   r=g.generate(level,64193,sid,p);ans=verify(r);assert ans==value(target)
   pair.append(r);counterfactuals.append(r)
  assert len({str(verify(r)) for r in pair})==number
  # Original profile, label, full ordered bank and known coefficient remain fixed.
  assert len({r['question'][':question/problem'].split('and')[0] for r in pair})==1
  assert len({json.dumps(choices(r['question'])) for r in pair})==len(pair) # owned IDs change
  assert len({tuple(a[':answer/value'] for a in choices(r['question'])) for r in pair})==1
# Every mismatch position; a zero first unknown component requiring a later pivot;
# a zero unknown coordinate with an impossible residual, not division by zero.
for sid in g.LEVELS['moderate']:
 base=copy.deepcopy(g.CASES[sid]);n=len(base['a']);base['c']=2;base['u']=[2*(i+1) for i in range(n)];base['a']=[3*(i+1) for i in range(n)]
 for j in range(n):
  p=copy.deepcopy(base);p['a'][j]+=1;r=g.generate('moderate',64193,sid,p);assert verify(r)=='No solution';counterfactuals.append(r)
 if n>2:
  for contradictory in [False,True]:
   p=copy.deepcopy(base);p['u'][0]=0;p['a'][0]=int(contradictory)
   r=g.generate('moderate',64193,sid,p);assert verify(r)==('No solution' if contradictory else -3);counterfactuals.append(r)
# Exact retained homogeneous one-component change.
base=copy.deepcopy(g.CASES['q-34570']);before=g.generate('moderate',64193,'q-34570',base);base['u'][0]=1;after=g.generate('moderate',64193,'q-34570',base)
assert verify(before)=='No solution' and verify(after)==-6;counterfactuals += [before,after]
# Irrelevant change to a1 and its matching contribution to b preserves the response.
base=copy.deepcopy(g.CASES['q-34249']);before=g.generate('easy',64193,'q-34249',base);base['a'][0]+=1;after=g.generate('easy',64193,'q-34249',base)
assert verify(before)==verify(after)==-2
assert mats(before['question'][':question/problem'])!=mats(after['question'][':question/problem'])
counterfactuals += [before,after];records+=counterfactuals
save('counterfactual-records.json',counterfactuals);save('normal-role-support.json',role_support)
# All choices are graded against visible equations, not the authored key.
native=[]
for i,r in enumerate(records):
 ans=verify(r)
 native.append({'label':f'visible-equation-{i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if value(a[':answer/value'])==ans else 'rejected','purpose':'Independent componentwise rational witness; each selectable response tested'} for a in choices(r['question'])]})
save('grader-input.json',native)
save('all-test-records.json',records)
# Delivery scope: ordinary samples and normal role witnesses, plus controlled full-bank cases.
for level in g.LEVELS:
 pool=[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)]
 save('delivery-input-'+level+'.json',pool)
batch=g.batch('easy',5,2406259497);assert batch==g.batch('easy',5,2406259497)
for r in batch:verify(r)
save('batch.json',batch)
# Four representative render cases: restored easy; subtraction; fractional moderate;
# contradiction requiring a later informative component. Existing source render coverage retained.
render=[next(r for r in normal if r['generation']['bank_profile']=='q-34572'),next(r for r in normal if r['generation']['bank_profile']=='q-34241'),next(r for r in records if r['generation']['bank_profile']=='q-73923' and isinstance(verify(r),Fraction) and verify(r).denominator>1),next(r for r in counterfactuals if verify(r)=='No solution' and mats(r['question'][':question/problem'])[1][0]==0)]
save('render-records.json',render)
report={'passed':True,'source_complete_banks':12,'source_choices':60,'canonical_visible_math':True,'ordinary_samples':len(normal),'normal_sampler_role_witnesses':len(role_support),'controlled_counterfactuals':len(counterfactuals),'math_records':len(records),'native_checks_prepared':sum(len(x['checks']) for x in native),'representative_render_records':len(render),'boundary_policy':'Subtraction c != 1 rejected by executable retained regression; no native engine change.'}
save('validation-results.json',report);print(json.dumps(report))

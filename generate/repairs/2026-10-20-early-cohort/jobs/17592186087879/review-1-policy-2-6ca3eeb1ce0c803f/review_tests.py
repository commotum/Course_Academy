"""Targeted independent audit. Run PYTHONDONTWRITEBYTECODE=1 <job python> review_tests.py."""
import sys,json,shutil,subprocess,collections,hashlib,random
sys.dont_write_bytecode=True
from audit import *
PYTHON=str(ROOT/'.venv/bin/python')
old=B/'review-0-policy-2-9fd429c4c6a56bf5'
# Source recipe code is unchanged. Verify all nine current replays against the prior complete records.
prior=json.load(open(old/'source-replays.json'));replays=[];replay=[]
for before in prior:
 z=before['generation'];after=g.generate(before['question'][':question/difficulty'].split('/')[-1],seed=z['seed'],template=z['template'],parameters=z['parameters'],profile=z['profile'])
 replays.append(after);replay.append({'template':z['template'],'same_complete_record_as_previous_independent_replay':before==after})
save('source-replays.json',replays);save('source-replay-current.json',replay)
assert all(z['same_complete_record_as_previous_independent_replay'] for z in replay)
# Fresh seeds chosen independently; small unchanged-family regression, focus on revised easy banks.
rows=[g.generate('easy',seed=630071+i) for i in range(48)]
for tid,(lev,fam) in g.AUTH.items():
 if lev!='easy':rows.append(g.generate(lev,seed=630131,template=tid))
save('independent-samples.json',rows);save('runner-batch.json',json.load(open(B/'samples.json')))
# Relevant a,h changes and irrelevant seed/bank-order change. All use held b=2.
pairs=[g.generate('easy',seed=27181,parameters={'a':a,'b':2,'h':h}) for a,h in [(1,-1),(2,-1),(6,-1),(2,3)]]
pairs.append(g.generate('easy',seed=27182,parameters={'a':2,'b':2,'h':-1}))
save('counterfactual-records.json',pairs)
# Boundary and rejection cases focus revised construction. Equilibrium/h=0 rejection inherited unchanged.
boundaries=[];rejected=[]
for a,b,h in [(1,1,-6),(6,6,-6),(1,1,6),(6,6,5),(6,1,6),(1,6,1)]:
 boundaries.append(g.generate('easy',seed=27183,parameters=dict(a=a,b=b,h=h)))
for label,params in [('a below',dict(a=0,b=2,h=-1)),('a above',dict(a=7,b=2,h=-1)),('h below',dict(a=2,b=2,h=-7)),('equilibrium',dict(a=2,b=2,h=2)),('zero initial',dict(a=2,b=2,h=0))]:
 try:g.generate('easy',seed=27183,parameters=params);rejected.append({'case':label,'rejected':False})
 except ValueError as e:rejected.append({'case':label,'rejected':True,'exception':str(e)})
save('boundary-records.json',boundaries);save('rejection-results.json',rejected);assert all(v['rejected'] for v in rejected)
allrows=rows+json.load(open(R/'runner-batch.json'))+pairs+boundaries
mathresults=[mathcheck(z) for z in allrows];save('math-results.json',mathresults)
assert all(z['passed'] for z in mathresults),[z for z in mathresults if not z['passed']]
# Native grading: all choices, classification derived from visible ODE/IC independently.
cases=[]
for ri,r in enumerate(allrows):
 p,q,t,h=promptdata(r);checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   v=expr(a[':answer/value']);valid=eq(s.diff(v,x),p*v) and v!=0 if fi==0 else eq(s.diff(v,x)+p*v,q) and eq(v.subs(x,t),h)
   checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if valid else 'rejected','purpose':'Exact displayed ODE and IC, not generator key'})
 cases.append({'label':str(ri)+' '+r['question'][':question/id'],'record':r,'checks':checks})
save('grader-input.json',cases)
# Counterfactual values and rendered dependent content.
def answer(r,fi):
 f=r['question'][':question/answer-fields'][fi];return expr(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
cf=[]
for i,j,kind in [(0,1,'coefficient'),(1,2,'coefficient boundary'),(1,3,'initial value'),(1,4,'irrelevant seed')]:
 a,b=pairs[i],pairs[j];samep=a['question'][':question/problem']==b['question'][':question/problem'];sames=a['question'][':question/worked-solution']==b['question'][':question/worked-solution']
 sameI=eq(answer(a,0),answer(b,0));sameY=eq(answer(a,1),answer(b,1));expected=([False,False] if 'coefficient' in kind else [True,False] if kind=='initial value' else [True,True])
 cf.append({'pair_indices':[i,j],'kind':kind,'IF_preserved':sameI,'solution_preserved':sameY,'prompt_preserved':samep,'worked_solution_preserved':sames,'actual_answers':[[str(answer(z,f)) for f in [0,1]] for z in [a,b]],'passed':[sameI,sameY]==expected and samep==(kind=='irrelevant seed') and sames==(kind=='irrelevant seed'),'grader_all_choices_case_indices':[allrows.index(a),allrows.index(b)]})
save('counterfactual-results.json',cf);assert all(z['passed'] for z in cf)
# Track actual sampler rejection without altering its code: wrap sample and restore.
trace=[];original_sample=g.sample
for aseed in range(630171,630183):
 attempted=[]
 def traced(f,level,r):
  p=original_sample(f,level,r);attempted.append(dict(p));return p
 g.sample=traced
 try: out=g.generate('easy',seed=aseed)
 finally:g.sample=original_sample
 trace.append({'seed':aseed,'attempted':attempted,'accepted':out['generation']['parameters'],'record':out})
save('resampling-traces.json',trace)
save('runtime-results.json',{'python':sys.version.split()[0],'sympy':s.__version__,'declared':json.load(open(P/'package.json'))['dependencies'],'deterministic_replay':rows[0]==g.generate('easy',seed=630071),'external_assets':'None: generated content and choices are text/math only.'})
# Execute author retained check safely on copies, and require it to fail on old package.
commands=[]
for label,origin in [('author-current',P),('author-old',old/'relocated-package')]:
 target=R/label;shutil.copytree(origin,target,dirs_exist_ok=True)
 if label=='author-old':shutil.copytree(P/'checks',target/'checks',dirs_exist_ok=True)
 cmd=[PYTHON,str(target/'checks/coefficient_regression.py')];res=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 commands.append({'label':label,'command':cmd,'exit_code':res.returncode,'stdout':res.stdout,'stderr':res.stderr})
save('retained-check-results.json',commands)
assert commands[0]['exit_code']==0 and commands[1]['exit_code']!=0
save('render-records.json',[*pairs,boundaries[1],rows[0]])
(R/'session-state.md').write_text('Source replays match previous independent records exactly. Current visible math, all fresh/batch/counterfactual/boundary choices checked with exact arithmetic. Retained author regression passed current copy and failed old copy. Native grader, delivery and UI rendering pending.\n')
print(json.dumps({'source_replays':len(replays),'fresh_samples':len(rows),'math_cases':len(mathresults),'math_failures':sum(not z['passed'] for z in mathresults),'retained_current_old_exits':[z['exit_code'] for z in commands]}))

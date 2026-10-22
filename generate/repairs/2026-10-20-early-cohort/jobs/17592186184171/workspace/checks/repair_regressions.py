#!/usr/bin/env python3
"""Source-derived, visible-record regressions. No services or runtime mutations.

Run from any directory with the job Python and -B. Writes only workspace/evidence.
"""
import collections, importlib.util, json, pathlib, re, shutil, subprocess, sys
import sympy as sp
sys.dont_write_bytecode=True
W=pathlib.Path(__file__).resolve().parents[1]; E=W/'evidence'; E.mkdir(exist_ok=True)
sys.path.insert(0,str(W))
spec=importlib.util.spec_from_file_location('candidate',W/'17592186184171.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
SOURCE=W.parent/'source/source.json';INVENTORY=W.parent/'source/inventory.json'
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def field(r):return r['question'][':question/answer-fields'][0]
def values(r):return sorted(int(a[':answer/value']) for a in field(r)[':answer-field/choices'])
def answer(r):
 f=field(r);return next(int(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def parse(problem):
 if 'basis of' in problem:
  m,n=map(int,re.search(r'(\d+)\\times\s*(\d+)',problem).groups());k=len(re.findall(r'\{b\}_\{\d+\}',problem));return 'easy',{'m':m,'n':n,'k':k},n-k
 raw=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',problem,re.S)[1]
 rows=raw.split('\\\\');indices=sorted(set(map(int,re.findall(r'\{x\}_\{(\d+)\}',raw))));xs=[sp.Symbol('x'+str(i)) for i in indices]
 exprs=[sp.sympify(re.sub(r'\{x\}_\{(\d+)\}',r'*x\1',t.strip()).replace('+*','+').replace('-*','-').lstrip('*'),locals={str(x):x for x in xs}) for t in rows]
 C=sp.Matrix([[ex.coeff(x) for x in xs] for ex in exprs]);return 'moderate',{'matrix':[[int(x) for x in row] for row in C.tolist()],'indices':indices},len(rows)-C.rank()
def verify(r):
 q=r['question'];level,p,a=parse(q[':question/problem']);sol=q[':question/worked-solution'];v=values(r)
 assert answer(r)==a and len(set(v))==5 and min(v)>=0
 if level=='easy':
  n,k=p['n'],p['k'];assert 1<=k<=min(p['m'],n-1)
  assert f"n={n}," in sol and f"rank}}(A)={k}." in sol
 else:
  n=len(p['matrix']);k=sp.Matrix(p['matrix']).rank()
  mats=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',sol,re.S)
  columns=[[int(t.strip()) for t in mat.split('\\\\')] for mat in mats]
  assert columns==list(map(list,zip(*p['matrix'])))
  assert f"n={n}," in sol and f"nullity}}(A)={k}." in sol
 assert f'{n}-{k}' in sol and int(re.search(r'&\s*=\s*(-?\d+)\.\\end\{aligned\}',sol)[1])==a
 return {'id':q[':question/id'],'level':level,'independent_answer':int(a),'passed':True}

def shortcuts(records):
 groups=collections.defaultdict(list);exact=collections.defaultdict(set)
 for r in records:
  v=values(r);a=answer(r);level,p,_=parse(r['question'][':question/problem']);gap=tuple(b-a for a,b in zip(v,v[1:]));template=r['generation']['template']
  group=(level,template,gap)
  groups[group].append(v.index(a));exact[(level,template,tuple(v))].add(a)
 result=[]
 for key,ranks in sorted(groups.items()):
  c=collections.Counter(ranks);result.append({'cue':str(key),'count':len(ranks),'correct_numeric_positions':dict(c),'best_fixed_position_successes':max(c.values()),'fixed_position_predicts_all':len(c)==1})
 return {'groups':result,'all_tested_shape_groups_vary':all(not x['fixed_position_predicts_all'] for x in result),'exact_bank_groups_with_multiple_correct_values':sum(len(a)>1 for a in exact.values()),'singletons_are_not_evidence_of_a_predictor':True}

# Reproduce retained source rejection first. All three must replay with full banks.
src=json.loads(SOURCE.read_text())['material']['kp'][':knowledge-point/questions']
replays=[];fidelity=[]
for q in src:
 level,p,a=parse(q[':question/problem']);ma=q[':question/math-academy-id']
 r=g.generate(level,seed=63271,template=ma,parameters=p)
 expected=sorted(int(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices'])
 assert values(r)==expected and answer(r)==a==int(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])
 assert field(r)[':answer-field/type']==':answer-field.type/radio'
 assert parse(r['question'][':question/problem'])==parse(q[':question/problem'])
 verify(r);replays.append(r)
 fidelity.append({'source_id':q[':question/id'],'ma_id':ma,'bank':expected,'matched_choices':5,'matched_distractors':4,'correct':int(a),'passed':True})
save('source-replay-records.json',replays);save('source-replay.json',{'complete_banks':len(fidelity),'matched_choices':5*len(fidelity),'matched_distractors':4*len(fidelity),'cases':fidelity,'presentation':'Fixed-size set braces and variable-index ordering normalize the captured equivalent TeX. Prompt dimension/expression and solution decomposition are parsed independently.'})
canonical=g.generate('easy',parameters={'m':3,'n':5,'k':3},template='q-35305');verify(canonical)
save('canonical-replay.json',{'source_id':'10cc01a6-af19-5340-9743-ade4d5e252dc','independent_dimensions':[3,5,3],'correct':answer(canonical),'passed':answer(canonical)==2})

# The exact old gapped bank is retained, but its alleged key now has a
# mathematical counterexample with identical m,n,bank and a different k.
old=g.generate('easy',seed=63271,profile='offset-minus2',parameters={'m':2,'n':4,'k':2},bank_anchor=0)
changed=g.generate('easy',seed=63271,profile='offset-minus2',parameters={'m':2,'n':4,'k':1},bank_anchor=0)
assert values(old)==values(changed)==[0,2,3,4,5] and [answer(old),answer(changed)]==[2,3]
witnesses=[old,changed]
# Each exact translated bank can select different numeric positions under the
# same matrix dimensions. Test the prior dimension-bank rule, too.
for profile in g.PROFILES['easy']:
 for anchor in (0,1):
  for a in [anchor+i for i in {'dimensions':[0,2,4,6,10],'offset-minus2':[0,2,3,4,5]}.get(profile,[0,1,2,3,4])]:
   if 1<=8-a<=7:
    witnesses.append(g.generate('easy',seed=63271,profile=profile,parameters={'m':7,'n':8,'k':8-a},bank_anchor=anchor,bank_scale=2 if profile=='dimensions' else 1))
save('shortcut-witness-records.json',witnesses)

# Modest stratified normal sample, not seeded source literals.
easy=[g.generate('easy',seed=946700+i,profile=p) for p in g.PROFILES['easy'] for i in range(12)]
moderate=[g.generate('moderate',seed=947100+i,profile=p,template=t) for p in g.PROFILES['moderate'] for t in ['null-space-inline','null-space-display'] for i in range(8)]
assert {len(r['generation']['parameters']['matrix']) for r in moderate}=={4,5}
assert {tuple(r['generation']['parameters']['indices']) for r in moderate}=={(1,2),(2,3),(1,2,3)}
normal=easy+moderate;save('normal-records.json',normal)
for level,rs in [('easy',easy),('moderate',moderate)]:save(f'{level}-records.json',rs)
raw=shortcuts(normal);assert raw['all_tested_shape_groups_vary']

# Regenerate exactly the five seeds used by the reviewed runner batch.
oldbatch=json.loads((W.parent/'samples.json').read_text())
batch=[g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed']) for r in oldbatch]
save('batch.json',batch)

# Relevant and irrelevant evidence changes with the bank fixed.
cf=[g.generate('easy',seed=5481,parameters=p,profile='small',bank_anchor=0) for p in [{'m':4,'n':6,'k':3},{'m':4,'n':7,'k':3},{'m':5,'n':6,'k':3},{'m':4,'n':6,'k':2}]]
C=[[1,0],[0,1],[1,1],[0,0]]
cf += [g.generate('moderate',seed=5482,parameters={'matrix':c,'indices':inds},profile='zero-through4',template='null-space-display') for c,inds in [(C,[2,3]),(C+[[0,0]],[2,3]),([[2,0],[0,1],[1,1],[0,0]],[2,3]),([[1,0,0],[0,1,0],[1,1,1],[0,0,0]],[1,2,3])]]
assert [answer(r)for r in cf]==[3,4,3,4,2,3,2,1]
assert cf[0]['question'][':question/worked-solution']==cf[2]['question'][':question/worked-solution']
save('counterfactual-records.json',cf)
checks=[verify(r) for r in replays+normal+witnesses+cf+batch]
save('math-results.json',{'checks':checks,'passed':True,'method':'Independently parse visible matrix dimensions/basis cardinality or null-space coefficient matrix; exact rank and solution decomposition/subtraction, without reading generation parameters.'})

# Actual publication filters; no publication, services or database mutation.
def deliver(name,records,level):
 save(name+'-input.json',records)
 cmd=[sys.executable,'-B',str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/(name+'-input.json')),'--source',str(SOURCE),'--inventory',str(INVENTORY),'--difficulty',level,'--output',str(E/name),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math']
 p=subprocess.run(cmd,capture_output=True,text=True);save(name+'-command.json',{'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,p.stderr
 return json.loads((E/name/'accepted.json').read_text())
accepted_easy=deliver('delivery-easy',easy+witnesses,'easy')
accepted_moderate=deliver('delivery-moderate',moderate,'moderate')
accepted_batch=deliver('delivery-batch',batch,'easy')
post=shortcuts(accepted_easy+accepted_moderate);assert post['all_tested_shape_groups_vary']
# Every exact bank in the controlled cue witnesses must retain two different
# keys after filtering (duplicate source content may be removed).
for r in (old,changed):assert any(values(s)==values(r) and answer(s)==answer(r) for s in accepted_easy)
# Keep the reviewer's exact bank-only strategy as an executable regression.
def old_strategy(r):
 v=values(r);gaps=[b-a for a,b in zip(v,v[1:])]
 if gaps==[2,1,1,1] or 0 not in v:return v[1]
 if gaps!=[1,1,1,1]:return v[-2]
 return 2
strategy_stages={}
for name,rs in [('raw',easy+witnesses),('delivered',accepted_easy),('batch_raw',batch),('batch_delivered',accepted_batch)]:
 hits=sum(old_strategy(r)==answer(r) for r in rs)
 assert hits<len(rs),name
 strategy_stages[name]={'correct':hits,'total':len(rs),'uniform_five_choice_baseline':0.2}
# Check feasible alternatives by parsing the public record, independent of
# generator metadata or its candidate enumeration.
for r in easy+witnesses:
 _,p,_=parse(r['question'][':question/problem'])
 feasible=[v for v in values(r) if 1<=p['n']-v<=min(p['m'],p['n']-1)]
 assert len(feasible)>=2
save('retained-bank-strategy.json',{'strategy':'gaps 2,1,1,1 or bank lacks zero -> second-smallest; other nonconsecutive bank -> second-largest; otherwise numeric 2','stages':strategy_stages,'visible_bank_alternative_support':{'records':len(easy+witnesses),'every_bank_has_at_least_two_feasible_answers_at_fixed_m_n':True},'old_exact_record':'Still correctly answers 2; a same-bank/same-dimensions k=1 case correctly answers 3. The faulty family invariant is removed, rather than deliberately falsifying a mathematically correct record.'})

save('shortcut-results.json',{'before':shortcuts(easy+witnesses+moderate),'before_normal_only':raw,'after':post,'old_gap_rule':{'same_bank':values(old),'correct_values':[answer(old),answer(changed)],'second_smallest_rule_successes':1,'attempts':2},'batch':{'records':len(batch),'delivered':len(accepted_batch),'answers':[answer(r)for r in batch],'positions':[values(r).index(answer(r)) for r in batch]},'limits':'No finite sample proves absence of every predictor. Every normal easy bank is constructed with >=2 feasible correct values at fixed m,n; controlled visible records demonstrate the supported assignment change.'})

# Probe conditional endpoints/ranks within each profile/layout, and n within
# moderate. Count semantic tasks, not UUIDs, layouts, or seeds.
coverage={}
for level,rs in [('easy',easy),('moderate',moderate)]:
 tasks=set();by=collections.defaultdict(set)
 for r in rs:
  _,p,a=parse(r['question'][':question/problem'])
  task=(p['n'],p['k']) if level=='easy' else (len(p['matrix']),tuple(tuple(row) for row in sp.Matrix(p['matrix']).T.rref()[0].tolist()))
  tasks.add(task)
  cue=(r['generation']['profile'],r['generation']['template'],len(p['matrix']) if level=='moderate' else 'all-n')
  by[cue].add((int(a),values(r).index(a)))
 assert all(len(v)>1 for v in by.values()),by
 coverage[level]={'semantic_instances':len(tasks),'conditional_answers_and_positions':{str(k):sorted(v) for k,v in by.items()}}
save('pedagogical-variation.json',{'coverage':coverage,'counterfactual_answers':[answer(r) for r in cf],'irrelevant_easy_m_preserves_solution':True,'moderate_coefficient_change_preserves_answer':answer(cf[4])==answer(cf[6]),'selection':'Shared delivery filtering run on all sampled easy/moderate records and exact five-seed batch. question_selection.rs selects by fresh identity/difficulty, then stable seeded draw, not answer content. Missing live learner history and policy mean no claim about any particular future learner sequence. Arbitrary history can leave a single candidate. Generator rejection checks full column rank only; normal easy banks are chosen before correct value with two feasible assignments.','source_replay':'Source banks retained as exact complete banks; translated shapes in ordinary generation support different correct positions.'})

# Native grader input, all choices on source-rejection repairs, bank witnesses,
# controlled changes and five-seed batch; run in one native process externally.
grade=[]
selected=[r for r in replays if r['generation']['source_replay'] in ('q-142489','q-79350','q-79351')]+[old,changed]+cf+batch
for i,r in enumerate(selected):
 _,_,a=parse(r['question'][':question/problem'])
 grade.append({'label':f'independent {i}','record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if int(c[':answer/value'])==a else 'rejected','purpose':'Independent visible prompt calculation; test every numeric option'} for c in field(r)[':answer-field/choices']]})
save('grader-input.json',grade)
save('render-records.json',batch+[r for r in replays if r['generation']['source_replay'] in ('q-142489','q-79350')]+[cf[7]])

# Inventory contains originals only; never label those as generated.
inv=json.loads(INVENTORY.read_text());ids={q[':question/id'] for q in src};inv_ids={q[':question/id'] for q in inv['questions']}
assert ids==inv_ids and not any(any('generat' in k for k in q) for q in inv['questions'])
save('inventory-audit.json',{'basis':inv['basis'],'total':len(inv_ids),'original_source_only':True,'generated_instances':0,'conclusion':'Verified absence of stored generated instances in the supplied inventory; all 15 stored IDs are original source IDs. No original is marked generated. No claim about later database state.'})
save('affected-inventory.json',{'affected_questions':[]})

# Strict invalid math rejection and deterministic normal CLI replay, relocation.
invalid=[('easy',{'m':2,'n':4,'k':3},'small'),('moderate',{'matrix':[[1,2],[2,4],[0,0],[0,0],[0,0]],'indices':[1,2]},'one-through5')]
for l,p,profile in invalid:
 try:g.generate(l,parameters=p,profile=profile)
 except ValueError:pass
 else:raise AssertionError('invalid math accepted')
assert all(g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],profile=r['generation']['profile'],template=r['generation']['template'])==r for r in normal)
m=json.loads((W/'package.json').read_text());rel=E/'relocated';rel.mkdir(exist_ok=True)
for f in m['files']:
 target=rel/f;target.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(W/f,target)
cmd=[sys.executable,'-B',str(rel/m['entrypoint']),'--difficulty','easy','--count','5','--seed','63271','--format','json'];p=subprocess.run(cmd,cwd=rel,capture_output=True,text=True)
assert p.returncode==0,p.stderr
assert json.loads(p.stdout)==[g.generate('easy',63271+i) for i in range(5)]
assert m['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sp.__version__}}
save('packaging.json',{'command':cmd,'relocation':True,'deterministic_replay':True,'exact_dependencies':m['dependencies'],'runtime_files':m['files'],'invalid_math_rejected':True})
save('regression-results.json',{'findings':{'6ead0de29c9ae7ec2652':'passed: exact old bank has different independently verified keys before and after delivery; all normal shape groups vary','78f2da5e200ade794205':'passed: all 15 full source banks including the three 5-component cases'},'math_checks':len(checks),'normal_records':len(normal),'delivery_counts':{'easy':len(accepted_easy),'moderate':len(accepted_moderate),'batch':len(accepted_batch)},'passed':True})
print(json.dumps({'source_banks':len(replays),'math_checks':len(checks),'normal_records':len(normal),'delivery_easy':len(accepted_easy),'delivery_moderate':len(accepted_moderate),'batch':len(accepted_batch),'passed':True}))

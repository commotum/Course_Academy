#!/usr/bin/env python3
"""Independent targeted review. Reproduce with the job Python, -B review.py."""
import sys,json,re,pathlib,importlib.util,hashlib,collections,subprocess,shutil,difflib
import sympy as sp
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent; J=E.parent; W=J/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python'
PREV=J/'review-0-policy-2-7c4a527c23b0b64b'
def save(n,x):
 p=E/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,default=str)+'\n')
def load(n):return json.loads((E/n).read_text())
sys.path.insert(0,str(W));spec=importlib.util.spec_from_file_location('review_candidate',W/'17592186184171.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def field(r):return r['question'][':question/answer-fields'][0]
def values(r):return sorted(int(c[':answer/value']) for c in field(r)[':answer-field/choices'])
def answer(r):
 f=field(r);return next(int(c[':answer/value']) for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
def parse(t):
 if 'basis of' in t:
  m,n=map(int,re.search(r'(\d+)\\times\s*(\d+)',t).groups());k=len(re.findall(r'\{b\}_\{\d+\}',t));return 'easy',{'m':m,'n':n,'k':k},n-k
 raw=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',t,re.S)[1];rows=raw.split('\\\\')
 inds=sorted(set(map(int,re.findall(r'\{x\}_\{(\d+)\}',raw))));xs=[sp.Symbol('x'+str(i)) for i in inds]
 es=[sp.sympify(re.sub(r'\{x\}_\{(\d+)\}',r'*x\1',x.strip()).replace('+*','+').replace('-*','-').lstrip('*'),locals={str(x):x for x in xs}) for x in rows]
 C=sp.Matrix([[e.coeff(x) for x in xs] for e in es]);return 'moderate',{'matrix':[[int(v) for v in row] for row in C.tolist()],'indices':inds},len(rows)-C.rank()
def verify(r):
 q=r['question'];level,p,a=parse(q[':question/problem']);sol=q[':question/worked-solution'];v=values(r)
 assert answer(r)==a and len(v)==len(set(v))==5 and min(v)>=0
 assert field(r)[':answer-field/type']==':answer-field.type/radio'
 if level=='easy':
  n,k=p['n'],p['k'];assert 1<=k<=min(p['m'],n);assert f'rank}}(A)={k}.' in sol
 else:
  n=len(p['matrix']);k=sp.Matrix(p['matrix']).rank()
  mats=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',sol,re.S)
  cols=[[int(x.strip()) for x in t.split('\\\\')] for t in mats];assert cols==list(map(list,zip(*p['matrix'])))
  assert f'nullity}}(A)={k}.' in sol
 assert f'n={n},' in sol and f'{n}-{k}' in sol
 assert int(re.search(r'&\s*=\s*(-?\d+)\.\\end\{aligned\}',sol)[1])==a
 return {'question_id':q[':question/id'],'level':level,'independent_answer':int(a),'passed':True}
def norm(t):return re.sub(r'\s+','',t.replace('\\left','').replace('\\right',''))
source=json.loads((J/'source/source.json').read_text());src=source['material']['kp'][':knowledge-point/questions']
replays=[];fidelity=[]
for q in src:
 level,p,a=parse(q[':question/problem']);r=g.generate(level,seed=751903,template=q[':question/math-academy-id'],parameters=p)
 bank=sorted(int(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices'])
 assert values(r)==bank and answer(r)==a==int(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])
 assert parse(r['question'][':question/problem'])==parse(q[':question/problem']);verify(r)
 # Compare exact prose/TeX as well as independent mathematical content. Equivalent
 # term reordering and delimiter sizes are the only observed differences.
 diffs={k:list(difflib.ndiff(q[k].splitlines(),r['question'][k].splitlines())) for k in [':question/problem',':question/worked-solution'] if norm(q[k])!=norm(r['question'][k])}
 fidelity.append({'source_id':q[':question/id'],'ma_id':q[':question/math-academy-id'],'bank':bank,'correct':int(a),'complete_bank_match':True,'presentation_differences':diffs})
 replays.append(r)
save('source-replay-records.json',replays);save('source-replay.json',{'cases':fidelity,'presentation_review':'Delimiters normalized to fixed-size sets, x terms reordered in ascending index, and prose whitespace normalized. Exact coefficient-vector checks establish same null spaces; theorem, dimension explanation, expansion, substitution, subtraction preserved.'})
canonical=g.generate('easy',seed=751904,parameters={'m':3,'n':5,'k':3},template='q-35305');verify(canonical)
save('canonical-record.json',[canonical]);save('canonical-replay.json',{'source_id':source['material']['kp'][':knowledge-point/canonical-example'][':question/id'],'correct':answer(canonical),'stages':['theorem','n=5','rank=3 from basis','5-3=2'],'limitation':'No canonical answer bank captured; practice source q-35305 supplies the bank.'})
# Fresh stratified seeds; chosen without observing outcomes.
easy=[g.generate('easy',seed=830217+i,profile=p) for p in ['small','offset-minus1','offset-minus2','dimensions','one-through5'] for i in range(12)]
moderate=[g.generate('moderate',seed=930417+i,profile=p,template=t) for p in ['zero-through4','one-through5'] for t in ['null-space-inline','null-space-display'] for i in range(6)]
batch=json.loads((J/'samples.json').read_text());save('batch-records.json',batch);save('sample-easy.json',easy);save('sample-moderate.json',moderate)
# Fixed-bank role interventions, including the prior counterexample.
cf=[g.generate('easy',seed=751905,profile='small',parameters=p,bank_anchor=0) for p in [{'m':4,'n':6,'k':3},{'m':4,'n':7,'k':3},{'m':5,'n':6,'k':3},{'m':4,'n':6,'k':2}]]
C=[[1,0],[0,1],[1,1],[0,0]]
cf += [g.generate('moderate',seed=751906,profile='zero-through4',template='null-space-display',parameters={'matrix':c,'indices':inds}) for c,inds in [(C,[2,3]),(C+[[0,0]],[2,3]),([[2,0],[0,1],[1,1],[0,0]],[2,3]),([[1,0,0],[0,1,0],[1,1,1],[0,0,0]],[1,2,3]),(C,[1,2])]]
assert list(map(answer,cf))==[3,4,3,4,2,3,2,1,2]
assert values(cf[0])==values(cf[1])==values(cf[2])==values(cf[3]);assert cf[0]['question'][':question/worked-solution']==cf[2]['question'][':question/worked-solution']
save('counterfactual-records.json',cf)
witness=[]
for profile in ['small','offset-minus1','offset-minus2','dimensions','one-through5']:
 vals={'offset-minus2':[0,2,3,4,5],'dimensions':[0,2,4,6,10]}.get(profile,list(range(5)))
 for a in vals:
  if 1<=8-a<=7:
   witness.append(g.generate('easy',seed=751907,profile=profile,parameters={'m':7,'n':8,'k':8-a},bank_anchor=0,bank_scale=2 if profile=='dimensions' else 1))
# Minimal old record and a role change with its exact same bank and dimensions.
witness += [g.generate('easy',seed=63271,profile='offset-minus2',parameters={'m':2,'n':4,'k':k},bank_anchor=0) for k in [2,1]]
assert list(map(answer,witness[-2:]))==[2,3] and values(witness[-1])==values(witness[-2])==[0,2,3,4,5]
save('role-witness-records.json',witness);save('minimal-pair.json',witness[-2:])
checks=[{'set':name,'index':i,**verify(r)} for name,rs in [('source',replays),('easy',easy),('moderate',moderate),('batch',batch),('counterfactual',cf),('role_witness',witness)] for i,r in enumerate(rs)]
save('math-results.json',{'method':'Visible prompt parsing, independent exact coefficient-matrix rank and solution expansion/subtraction verification; no generation metadata used for correctness.','checks':checks,'passed':True})
# Old-failure replay, with the independent earlier scripts and bound old runtime.
old=E/'old-counterexamples';old.mkdir(exist_ok=True)
shutil.copyfile(PREV/'reproduce.py',old/'reproduce.py')
old_runs=[]
for case in ['source','shortcut']:
 cmd=[str(PY),'-B',str(old/'reproduce.py'),case,'--package',str(PREV/'relocated')]
 p=subprocess.run(cmd,capture_output=True,text=True);old_runs.append({'case':case,'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 assert p.returncode!=0
assert 'parameter/profile constraint' in old_runs[0]['stderr'] and 'Incidental bank gap pattern' in old_runs[1]['stderr']
save('retained-failure-replay.json',{'provenance':'Previous independent reproduce.py copied unchanged; old relocated generator retained in previous review, matched original binding.','old_runs':old_runs,'current_source_cases':[x['ma_id'] for x in fidelity if x['ma_id'] in ['q-142489','q-79350','q-79351']],'current_shortcut_witness':'minimal-pair.json','interpretation':'The old single-record shortcut assertion also fails on a correct new record with answer 2; it alone is not a valid repaired-family test. Fixed-bank role intervention now changes the correct numeric position, while original mathematics stays correct.'})
# Relocation and dependency check: only manifest runtime files copied.
m=json.loads((W/'package.json').read_text());rel=E/'relocated';rel.mkdir(exist_ok=True)
for f in m['files']:
 target=rel/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,target)
cmd=[str(PY),'-B',str(rel/m['entrypoint']),'--difficulty','all','--seed','751908','--count','3'];p=subprocess.run(cmd,cwd=E,capture_output=True,text=True);assert p.returncode==0,p.stderr
relrecords=json.loads(p.stdout);assert relrecords==[g.generate(l,751908+i) for l in ['easy','moderate'] for i in range(3)];save('relocated-records.json',relrecords)
assert m['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sp.__version__}}
assert all(g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],profile=r['generation']['profile'],template=r['generation']['template'])==r for r in easy+moderate)
assert all(g.generate('easy',r['generation']['seed'])==r for r in batch)
reject=[]
for label,l,pa,pr in [('infeasible basis','easy',{'m':2,'n':4,'k':3},'small'),('noninteger','easy',{'m':3,'n':5,'k':1.5},'small'),('dependent parameters','moderate',{'matrix':[[1,2],[2,4],[0,0],[0,0],[0,0]],'indices':[1,2]},'one-through5')]:
 try:g.generate(l,parameters=pa,profile=pr)
 except ValueError as ex:reject.append({'case':label,'parameters':pa,'error':str(ex),'passed':True})
 else:raise AssertionError(label)
boundary=[]
for pa in [{'m':2,'n':4,'k':1},{'m':2,'n':4,'k':2},{'m':7,'n':12,'k':1},{'m':7,'n':12,'k':7}]:
 for pr in ['small','offset-minus1','offset-minus2','dimensions','one-through5']:
  r=g.generate('easy',seed=751909,parameters=pa,profile=pr);verify(r);boundary.append(r)
save('boundary-records.json',boundary);save('packaging.json',{'command':cmd,'relocation':True,'deterministic_replay':True,'exact_dependencies':m['dependencies'],'rejections':reject,'boundary_checks':len(boundary),'external_output':'Stdout JSON only; no asset or database writes; no external files needed beyond declared files. No replenishment script executed.','sampler':'Easy chooses bank with >=2 feasible values then selects qualifying value uniformly. Moderate retries until full column rank (10000 bound); 4/5 rows, 2/3 independent columns; no answer-based rejection.'})
# Native grader cases, all options; radio controls accept IDs, no free input.
grade=[]
for label,rs in [('batch',batch),('cf',cf),('witness',witness[-2:]),('repaired_source',[r for r in replays if r['generation']['source_replay'] in ['q-142489','q-79350','q-79351']])]:
 for i,r in enumerate(rs):
  a=parse(r['question'][':question/problem'])[2]
  grade.append({'label':f'{label}-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if int(c[':answer/value'])==a else 'rejected','purpose':'Independent visible prompt calculation; every numeric choice tested, including before/after intervention values.'} for c in field(r)[':answer-field/choices']]})
save('grader-input.json',grade)
# Render entire batch, controlled before/after pairs, all 3 repaired sources.
render=batch+cf+[r for r in replays if r['generation']['source_replay'] in ['q-142489','q-79350','q-79351']]+witness[-2:]
save('render-records.json',render)
inv=json.loads((J/'source/inventory.json').read_text());srcids={q[':question/id'] for q in src};invids={q[':question/id'] for q in inv['questions']}
assert srcids==invids and not any(any('generat' in k for k in q) for q in inv['questions'])
save('inventory-audit.json',{'basis':inv['basis'],'lineage':inv['lineage'],'total':len(invids),'original_source_ids_only':True,'generated_instances':0,'conclusion':'Verified absence of generated records in captured 15-question inventory. Original sources are not marked generated. No claim about later changing inventory.'});save('affected-inventory.json',{'affected_questions':[]})
save('scope-analysis.json',{'source_analysis':'source-analysis.json','easy':'Same count-basis, identify column count, subtract; m2..7,n4..12,k1..7 retain short basis and integer subtraction. Positive dimensions retain nontrivial source scope.','moderate':'4/5 components and 2/3 independent parameters; coefficients -3..3. Independence is required, consistent with source. Expansion length comparable to supplied q-35434; no dependent/redundant parameters added.','response':'Single five-option integer radio selection throughout. Targets fixed by the source-supported inference direction and difficulty, not by incidental numeric results.','passed':True})
(E/'session-state.md').write_text('Source confirmed first. Prior defects reproduced on bound old runtime. Current complete source replay, independent math, fresh stratified samples, role interventions, boundary rejection, replay/relocation, and inventory checks pass. Native grading, actual UI rendering, delivery filtering and selection/shortcut finalization pending. No package edits.\n')
print(json.dumps({'source_replays':len(replays),'math_checks':len(checks),'easy':len(easy),'moderate':len(moderate),'batch':len(batch),'render':len(render),'old_failures_reproduced':len(old_runs),'packaging':'passed'}))

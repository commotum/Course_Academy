#!/usr/bin/env python3
"""Independent database-free review. Run with the job's declared Python and -B."""
import sys,json,re,pathlib,importlib.util,hashlib,collections,subprocess,shutil
import sympy as sp
E=pathlib.Path(__file__).resolve().parent
J=E.parent;W=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python'
sys.dont_write_bytecode=True
sys.path.insert(0,str(W))
spec=importlib.util.spec_from_file_location('reviewed_generator',W/'17592186184171.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
save('package-before.json',hashes())
source=json.loads((J/'source/source.json').read_text());src=source['material']['kp'][':knowledge-point/questions'];batch=json.loads((J/'samples.json').read_text());save('batch-records.json',batch)
def field(r):return r['question'][':question/answer-fields'][0]
def values(r):return [int(c[':answer/value']) for c in field(r)[':answer-field/choices']]
def correct(r):
 f=field(r);return next(int(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def parse(problem):
 if 'basis of' in problem:
  m,n=map(int,re.search(r'(\d+)\\times (\d+)',problem).groups());k=len(re.findall(r'\{b\}_\{\d+\}',problem));return 'easy',{'m':m,'n':n,'k':k},n-k
 raw=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',problem,re.S)[1]
 rows=raw.split('\\\\');indices=sorted(set(map(int,re.findall(r'\{x\}_\{(\d+)\}',raw))));xs=[sp.Symbol('x'+str(i)) for i in indices]
 exprs=[sp.sympify(re.sub(r'\{x\}_\{(\d+)\}',r'x\1',t.strip()).replace('}{','}*{'),locals={str(x):x for x in xs},evaluate=True) if False else sp.sympify(re.sub(r'\{x\}_\{(\d+)\}',r'*x\1',t.strip()).replace('+*','+').replace('-*','-').lstrip('*'),locals={str(x):x for x in xs}) for t in rows]
 C=sp.Matrix([[ex.coeff(x) for x in xs] for ex in exprs]);return 'moderate',{'matrix':[[int(x) for x in row] for row in C.tolist()],'indices':indices},len(rows)-C.rank()
def norm(t):return re.sub(r'\s+','',t.replace('\\left','').replace('\\right','').replace('\\mathbb{R}','R'))
replay=[];replay_records=[]
for q in src:
 level,p,expected=parse(q[':question/problem']);bank=[int(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
 entry={'source_id':q[':question/id'],'ma_id':q[':question/math-academy-id'],'level':level,'parameters':p,'independent_correct':int(expected),'source_bank':bank,'attempts':[]}
 for profile in g.PROFILES[level]:
  try:
   r=g.generate(level,seed=8801,parameters=p,profile=profile,template='column-basis' if level=='easy' else 'null-space-display' if '\n' in q[':question/problem'] else 'null-space-inline')
   if sorted(values(r))!=sorted(bank):continue
   replay_records.append(r);entry['matched_profile']=profile;entry['record_id']=r['question'][':question/id'];entry['correct_matches']=correct(r)==int(expected)==int(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']);entry['prompt_matches']=norm(r['question'][':question/problem'])==norm(q[':question/problem']);entry['solution_matches']=norm(r['question'][':question/worked-solution'])==norm(q[':question/worked-solution']);break
  except ValueError as ex:entry['attempts'].append({'profile':profile,'error':str(ex)})
 else:entry['failure']='No supported profile accepts these source parameters with its complete bank.'
 replay.append(entry)
save('source-replay.json',replay);save('source-replay-records.json',replay_records)
# Fresh, stratified modest sample. Selected before evaluating shortcut success.
easy=[g.generate('easy',seed=946700+i,profile=profile) for profile in g.PROFILES['easy'] for i in range(16)]
moderate=[g.generate('moderate',seed=947100+i,profile=profile,template=template) for profile in g.PROFILES['moderate'] for template in ['null-space-inline','null-space-display'] for i in range(8)]
save('sample-easy.json',easy);save('sample-moderate.json',moderate)
# Controlled changes with most evidence fixed, including an option that changes truth.
cf=[g.generate('easy',seed=5481,parameters=p,profile='small') for p in [{'m':4,'n':6,'k':3},{'m':4,'n':7,'k':3},{'m':5,'n':6,'k':3},{'m':4,'n':6,'k':2}]]
C=[[1,0],[0,1],[1,1],[0,0]]
cf += [g.generate('moderate',seed=5482,parameters={'matrix':c,'indices':inds},profile='zero-through4',template='null-space-display') for c,inds in [(C,[2,3]),([[2,0],[0,1],[1,1],[0,0]],[2,3]),([[1,0,0],[0,1,0],[1,1,1],[0,0,0]],[1,2,3])]]
save('counterfactual-records.json',cf)
math_results=[]
for label,records in [('batch',batch),('easy',easy),('moderate',moderate),('counterfactual',cf),('replay',replay_records)]:
 for i,r in enumerate(records):
  level,p,expected=parse(r['question'][':question/problem']);q=r['question'];sol=q[':question/worked-solution'];a=correct(r)
  ok=a==expected and len(set(values(r)))==5 and a in values(r)
  if level=='easy':
   ok &= p['k']<=min(p['m'],p['n']) and f"{p['n']}-{p['k']}" in sol and f"={a}." in sol
  else:
   mats=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',sol,re.S)
   coeffs=[[int(t.strip()) for t in mat.split('\\\\')] for mat in mats]
   expectedcols=list(map(list,zip(*p['matrix'])))
   ok &= coeffs==expectedcols and f"{len(p['matrix'])}-{len(p['indices'])}" in sol and f"={a}." in sol
  math_results.append({'set':label,'index':i,'question_id':q[':question/id'],'expected':int(expected),'stored':a,'passed':bool(ok)})
save('math-results.json',{'method':'Parse rendered prompt dimensions/basis list or parameter coefficient matrix independently; exact SymPy rank; independently compare solution coefficient vectors and subtraction.','checks':math_results,'passed':all(r['passed'] for r in math_results)})
# Generator validation boundaries and deterministic replay.
reject=[]
for label,level,p,profile in [('infeasible rank','easy',{'m':2,'n':4,'k':3},'small'),('noninteger','easy',{'m':3,'n':5,'k':2.5},'small'),('missing correct in small bank','easy',{'m':3,'n':10,'k':2},'small'),('duplicate dimension distractors','easy',{'m':3,'n':6,'k':2},'dimensions'),('dependent coefficient vectors','moderate',{'matrix':[[1,2],[2,4],[0,0],[0,0]],'indices':[2,3]},'zero-through4')]:
 try:g.generate(level,parameters=p,profile=profile);reject.append({'case':label,'rejected':False})
 except ValueError as ex:reject.append({'case':label,'rejected':True,'error':str(ex)})
replay_ok=all(g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],profile=r['generation']['profile'],template=r['generation']['template'])==r for r in easy+moderate) and all(g.generate('easy',r['generation']['seed'])==r for r in batch)
save('rejection-replay.json',{'rejections':reject,'deterministic_replay':replay_ok,'code_rule':'sample() proposes dimensions/coefficient entries and retries up to 10000; valid() rejects infeasible dimensions, rank-deficient coefficients or malformed banks. No post-answer branch in the sampled scope.'})
# Native grader: all alternatives, controlled changed option, and shortcut actions.
grade=[]
for label,records in [('batch',batch),('counterfactual',cf),('easy',easy[:4]),('moderate',moderate[:4])]:
 for i,r in enumerate(records):
  _,_,a=parse(r['question'][':question/problem']);grade.append({'label':f'{label}-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if int(c[':answer/value'])==a else 'rejected','purpose':'Select independently derived answer or plausible distractor; all five choices tested.'} for c in field(r)[':answer-field/choices']]})
save('grader-input.json',grade)
# UI includes all exact batch members and counterfactual pairs, plus both moderate layouts.
save('render-records.json',batch+cf+moderate[:1]+moderate[8:9])
# Inventory contains source objects only: do not relabel them generated.
inv=json.loads((J/'source/inventory.json').read_text());generated=[q for q in inv['questions'] if any('generat' in k for k in q)]
save('inventory-audit.json',{'basis':inv['basis'],'total':len(inv['questions']),'source_ids':[q[':question/id'] for q in src],'inventory_ids':[q[':question/id'] for q in inv['questions']],'all_ids_are_original_source':set(q[':question/id'] for q in src)==set(q[':question/id'] for q in inv['questions']),'generation_key_records':len(generated),'conclusion':'Captured bank contains exactly the 15 source questions. No stored generated record is present to reproduce as affected. This is a verified absence in this snapshot, not a claim about later inventory.'})
save('affected-inventory.json',{'affected_questions':[]})
# Runtime and relocation to independent directory under evidence only.
manifest=json.loads((W/'package.json').read_text());reloc=E/'relocated';reloc.mkdir(exist_ok=True)
for path in ['17592186184171.py','math_format.py','17592186184171/reference/source.json']:
 target=reloc/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/path,target)
p=subprocess.run([str(PY),'-B',str(reloc/'17592186184171.py'),'--difficulty','easy','--seed','946700','--count','2'],cwd=E,capture_output=True,text=True)
if p.returncode==0:save('relocated-records.json',json.loads(p.stdout))
save('packaging.json',{'manifest_dependencies':manifest['dependencies'],'actual_dependencies':{'python':sys.version.split()[0],'packages':{'sympy':sp.__version__}},'versions_match':manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sp.__version__}},'all_manifest_files_exist':all((W/f).is_file() for f in manifest['files']),'relocation':{'command':[str(PY),'-B',str(reloc/'17592186184171.py'),'--difficulty','easy','--seed','946700','--count','2'],'returncode':p.returncode,'stderr':p.stderr,'records':len(json.loads(p.stdout)) if not p.returncode else 0},'external_output':'No generator assets or file-writing calls; stdout JSON only. Imports use Python -B to suppress bytecode writes. No database helper or replenishment script executed.','history':'repair-history.json and repair-preflight.json absent; no retained repair finding supplied.'})
(E/'session-state.md').write_text('Independent source account completed first. audit.py saved fresh samples, source replay, exact math, rejection/replay, counterfactuals, grader and renderer inputs, inventory and packaging evidence. Source replay excludes three n=5 moderate cases. Delivery/grader/render runs pending. Package remains untouched.\n')
print(json.dumps({'replay_cases':len(replay),'replay_missing':[x['ma_id'] for x in replay if 'failure'in x],'replay_mismatches':[{k:v for k,v in x.items() if k not in ['parameters','attempts']} for x in replay if x.get('matched_profile') and not all(x[k] for k in ['correct_matches','prompt_matches','solution_matches'])],'math':all(r['passed'] for r in math_results),'math_checks':len(math_results),'deterministic_replay':replay_ok,'relocation':p.returncode}))

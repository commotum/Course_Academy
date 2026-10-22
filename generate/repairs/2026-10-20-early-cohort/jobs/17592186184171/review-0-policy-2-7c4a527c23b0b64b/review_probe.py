import sys,os,json,re,hashlib,importlib.util,subprocess,shutil,platform
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent; JOB=ROOT.parent; PKG=JOB/'workspace'; REPO=Path('/home/jake/Developer/Course_Academy'); PY=REPO/'.venv/bin/python'
os.chdir(ROOT);sys.path.insert(0,str(PKG))
def save(p,x): (ROOT/p).write_text(json.dumps(x,indent=2,default=str))
def hashpkg():return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}
save('package-hashes-before.json',hashpkg())
spec=importlib.util.spec_from_file_location('reviewed_generator',PKG/'17592186184171.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as sp
src=json.load(open(JOB/'source/source.json')); qs=src['material']['kp'][':knowledge-point/questions']
def field(r):return r['question'][':question/answer-fields'][0]
def answer(r):
 f=field(r);return int(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
def texmat(text):
 z=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S).group(1)
 rows=re.split(r'\\\\',z)
 out=[]
 for row in rows:
  row=re.sub(r'\{x\}_\{(\d+)\}',r'x\1',row.strip());row=re.sub(r'(?<=\d)(?=x)', '*',row)
  out.append(sp.sympify(row))
 return out
source_results=[];replays=[]
for q in qs:
 level=q[':question/difficulty'][':db/ident'].split('/')[-1];p=q[':question/problem'];bank=[int(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices']]
 if level=='easy':
  m,n=map(int,re.search(r'(\d+)\\times\s*(\d+)',p).groups());k=len(re.findall(r'\{b\}_\{\d+\}',p));params={'m':m,'n':n,'k':k};expected=n-k
 else:
  v=texmat(p);inds=sorted({int(str(s)[1:]) for e in v for s in e.free_symbols});C=[[int(e.coeff(sp.Symbol('x'+str(i)))) for i in inds] for e in v];params={'matrix':C,'indices':inds};expected=len(v)-sp.Matrix(C).rank()
 row={'source_id':q[':question/id'],'ma_id':q[':question/math-academy-id'],'level':level,'parameters':params,'independent_answer':expected,'source_answer':q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],'source_bank':bank,'attempts':[]}
 for profile in g.PROFILES[level]:
  try:
   r=g.generate(level,seed=802103,parameters=params,profile=profile);replays.append(r)
   same=sorted(bank)==sorted(int(c[':answer/value']) for c in field(r)[':answer-field/choices']); row['attempts'].append({'profile':profile,'accepted':True,'same_bank':same,'correct':answer(r),'record_id':r['question'][':question/id']})
  except ValueError as e:row['attempts'].append({'profile':profile,'accepted':False,'error':str(e)})
 row['complete_bank_replay']=any(a.get('same_bank') and a.get('correct')==expected for a in row['attempts']);source_results.append(row)
save('source-replay.json',source_results);save('source-replay-records.json',replays)
records=[g.generate(level,seed=s) for level in ['easy','moderate'] for s in range(931047,931107)]
save('independent-samples.json',records);batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch)
def mathcheck(r):
 p=r['question'][':question/problem'];sol=r['question'][':question/worked-solution'];level=r['question'][':question/difficulty'].split('/')[-1]
 if level=='easy':
  m,n=map(int,re.search(r'(\d+)\\times\s*(\d+)',p).groups());k=len(re.findall(r'\{b\}_\{\d+\}',p));expected=n-k;consistent=0<=k<=min(m,n)
 else:
  v=texmat(p);syms=sorted(set().union(*(e.free_symbols for e in v)),key=str);C=sp.Matrix([[e.coeff(s) for s in syms] for e in v]);n=len(v);k=C.rank();expected=n-k;consistent=True
  vectors=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',sol,re.S)
  D=sp.Matrix.hstack(*[sp.Matrix([sp.sympify(t.strip()) for t in re.split(r'\\\\',vv)]) for vv in vectors]);consistent=D==C
 vals=[int(c[':answer/value']) for c in field(r)[':answer-field/choices']]
 final=int(re.search(r'&\s*=\s*(-?\d+)\.\\end\{aligned\}',sol).group(1))
 return {'id':r['question'][':question/id'],'expected':expected,'stored':answer(r),'solution_final':final,'valid':consistent and answer(r)==expected==final and len(set(vals))==5}
math_results=[mathcheck(r) for r in records+batch+replays];save('math-checks.json',math_results)
# Explicit controlled pairs; stored choices retain the same values in the small bank.
pairs=[g.generate('easy',seed=71003,parameters=p,profile='small') for p in [{'m':4,'n':5,'k':2},{'m':4,'n':6,'k':2},{'m':6,'n':5,'k':2}]]
save('counterfactual-records.json',pairs)
cf={'relevant':{'change':'n 5 to 6, fixed m=4,k=2,small bank','answers':[answer(pairs[i]) for i in [0,1]],'prompt_changed':pairs[0]['question'][':question/problem']!=pairs[1]['question'][':question/problem'],'solution_changed':pairs[0]['question'][':question/worked-solution']!=pairs[1]['question'][':question/worked-solution']},'irrelevant':{'change':'m 4 to 6, fixed n=5,k=2,small bank','answers':[answer(pairs[i]) for i in [0,2]],'prompt_changed':pairs[0]['question'][':question/problem']!=pairs[2]['question'][':question/problem'],'solution_preserved':pairs[0]['question'][':question/worked-solution']==pairs[2]['question'][':question/worked-solution']}}
save('counterfactual-checks.json',cf)
# A minimal failing bank and minimal prohibited but feasible zero-nullity case.
minimal=g.generate('easy',seed=1,parameters={'m':2,'n':4,'k':1},profile='offset-minus1');save('minimal-shortcut-records.json',[minimal])
rejects=[]
for label,kw in [('zero-nullity',dict(level='easy',parameters={'m':4,'n':4,'k':4},profile='small')),('negative-rank',dict(level='easy',parameters={'m':2,'n':4,'k':3},profile='small')),('dependent-parameters',dict(level='moderate',parameters={'matrix':[[1,1],[0,0],[0,0],[0,0]],'indices':[2,3]},profile='zero-through4')),('hard',dict(level='hard'))]:
 try:g.generate(seed=1,**kw);rejects.append({'label':label,'kwargs':kw,'rejected':False})
 except ValueError as e:rejects.append({'label':label,'kwargs':kw,'rejected':True,'error':str(e)})
save('rejections.json',rejects)
# Native grader: every option; controlled old-response transfer by value.
cases=[]
for idx,r in enumerate([minimal]+batch+records[:4]+records[60:64]+pairs):
 checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if int(c[':answer/value'])==answer(r) else 'rejected','purpose':'independently computed integer response'} for c in field(r)[':answer-field/choices']]
 cases.append({'label':f'question {idx} answer {answer(r)}','record':r,'checks':checks})
save('grader-input.json',cases)
# Replay and packaging in a new path, including CLI defaults.
replay=all(g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed'])==r for r in records)
rel=ROOT/'relocated';rel.mkdir(exist_ok=True)
for f in ['17592186184171.py','math_format.py','17592186184171/reference/source.json']:
 d=rel/f;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PKG/f,d)
cmd=[str(PY),'-B',str(rel/'17592186184171.py'),'--difficulty','easy','--seed','931047','--count','1'];p=subprocess.run(cmd,capture_output=True,text=True);save('relocated-cli.json',json.loads(p.stdout) if p.returncode==0 else {'error':p.stderr});
manifest=json.load(open(PKG/'package.json'));save('packaging.json',{'command':cmd,'exit':p.returncode,'relocation_equal':p.returncode==0 and json.loads(p.stdout)[0]==records[0],'deterministic_replay':replay,'installed':{'python':platform.python_version(),'packages':{'sympy':sp.__version__}},'declared':manifest['dependencies'],'manifest_versions_match':manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':sp.__version__}},'external_outputs':'No generated assets or output files; CLI emits JSON stdout. Imports SymPy and declared local math_format/source snapshot.','history_and_preflight':'Neither file exists; no retained findings.'})
save('render-records.json',[minimal]+batch+pairs+[records[60],records[61]])
save('affected-inventory.json',{'affected_questions':[]});save('inventory-audit.json',{'captured_basis':json.load(open(JOB/'source/inventory.json'))['basis'],'question_count':len(json.load(open(JOB/'source/inventory.json'))['questions']),'source_question_ids':[q[':question/id'] for q in qs],'verified_all_inventory_are_original_source':set(q[':question/id'] for q in json.load(open(JOB/'source/inventory.json'))['questions'])==set(q[':question/id'] for q in qs),'conclusion':'No stored generated instances exist in captured inventory. Original source questions are excluded from affected-generated-inventory, even where their bank pattern inspired the generator defect.'})
(ROOT/'session-state.md').write_text('Milestone 2: source replay, fresh seed samples, exact independent math, controlled pairs, strict rejection cases, package versions and relocation saved by review_probe.py. Source family omissions and numeric-bank shortcuts demonstrated; package remains unchanged. Native grader, delivery and renderer pending.\n')
print(json.dumps({'source_cases':len(source_results),'failed_replays':[x['ma_id'] for x in source_results if not x['complete_bank_replay']],'math_cases':len(math_results),'math_failures':sum(not x['valid'] for x in math_results),'minimal_bank':[c[':answer/value'] for c in field(minimal)[':answer-field/choices']],'minimal_answer':answer(minimal),'replay':replay,'relocation_exit':p.returncode}))

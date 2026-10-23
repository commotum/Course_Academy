import sys,os,json,pathlib,importlib.util,re,hashlib,collections,platform,shutil,subprocess
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent; W=R.parent/'workspace'; PY='/home/jake/Developer/Course_Academy/.venv/bin/python'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(W));spec=importlib.util.spec_from_file_location('reviewed_generator',W/'17592186115242.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as s
x,y,k=s.symbols('x y k')
def write(n,obj):(R/n).write_text(json.dumps(obj,indent=2,default=str))
def expr(t):
 t=t.strip().replace(' ','').replace('\\,','').replace('−','-')
 while '\\frac' in t:
  t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 t=re.sub(r'(\d)([xyk])',r'\1*\2',t); t=re.sub(r'([xyk]|\))([xyk])',r'\1*\2',t)
 return s.sympify(t,locals={'x':x,'y':y,'k':k})
def rows(q):
 body=q[':question/problem'].split('\\begin{aligned}')[1].split('\\end{aligned}')[0]
 out=[]
 for line in body.split('\\\\'):
  a,b=line.replace('&','').replace(',','').split('=');out.append(s.expand(expr(a)-expr(b)))
 return out

def audit(rec):
 q=rec['question']; rr=rows(q);A,b=s.linear_eq_to_matrix(rr,[x,y]);roots=s.solve(A.det(),k);assert len(roots)==1
 root=roots[0];f=q[':question/answer-fields'][0]; choices=f[':answer-field/choices'];good=[z for z in choices if s.simplify(expr(z[':answer/value'].split('=')[1])-root)==0]
 assert len(good)==1 and good[0][':answer/id']==f[':answer-field/correct'][1]
 rank=A.subs(k,root).rank(); aug=A.row_join(b).subs(k,root).rank();dep='consistent dependent' in q[':question/problem'];assert (rank==aug==1) if dep else (rank<aug)
 # Every printed augmented matrix must be row-equivalent at a nonsingular and the singular k value.
 matrices=re.findall(r'\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}',q[':question/worked-solution'],re.S)
 for m in matrices:
  M=s.Matrix([[expr(z) for z in row.split('&')] for row in m.split('\\\\')]);assert M.shape==(2,3)
  for t in [root,root+1]: assert M.subs(k,t).rref()[0]==A.row_join(b).subs(k,t).rref()[0]
 final=re.findall(r'when\s+\$(.*?)\$',q[':question/worked-solution'])[-1].rstrip('.,');assert s.simplify(expr(final.split('=')[1])-root)==0
 return {'id':q[':question/id'],'root':str(root),'rank':rank,'augmented_rank':aug,'matrices_checked':len(matrices),'correct_position':choices.index(good[0]),'template':rec['generation']['template']}

sources=json.load(open(R/'source-cases.json')); profiles=json.load(open(W/'17592186115242/recipes.json'))
replays=[];replay_report=[]
for q in sources:
 rr=rows(q);A,b=s.linear_eq_to_matrix(rr,[x,y]);p=dict(a=int(A[0,0]),b=int(A[0,1]),c=int(b[0]),d=int(A[1,0]),u=int(s.diff(A[1,1],k)),v=int(A[1,1].subs(k,0)),e=int(b[1]));profile=q.get(':question/math-academy-id');level='hard' if 'consistent dependent' in q[':question/problem'] else 'moderate'
 try:
  if profile=='e-4712': r=g.generate(level,seed=822101,parameters=p,template='inconsistent_bare')
  else:r=g.generate(level,seed=822101,parameters=p,profile=profile)
  assert rows(r['question'])==rr
  if q.get(':question/answer-fields'):
   f=q[':question/answer-fields'][0];expected=sorted(str(expr(a[':answer/value'].split('=')[1].replace('\\\\','\\'))) for a in f[':answer-field/choices']); actual=sorted(str(expr(a[':answer/value'].split('=')[1])) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']);assert expected==actual
  replays.append(r);replay_report.append({'source_id':q[':question/id'],'profile':profile,'parameters':p,'status':'passed','scope':'prompt equations, complete mathematical bank, keyed root; solution math checked separately'})
 except Exception as e:replay_report.append({'source_id':q[':question/id'],'profile':profile,'parameters':p,'status':'failed','error':str(e)})
write('source-replays.json',replays);write('source-replay-report.json',replay_report)
samples=[]
for level,templates in g.TEMPLATES.items():
 for t in templates:
  for seed in range(822101,822101+(24 if level=='easy' else 4)):samples.append(g.generate(level,seed=seed,template=t))
write('samples.json',samples);batch=json.load(open(R.parent/'samples.json'));write('runner-batch.json',batch)
math=[]
for r in samples+batch+replays:
 try:math.append(dict(status='passed',**audit(r)))
 except Exception as e:math.append({'status':'failed','id':r['question'][':question/id'],'error':repr(e)})
write('math-results.json',math)
# Explicit relevant coefficient pair and irrelevant constant pair, same seed and all other slots.
p=dict(a=1,b=2,c=1,d=2,u=1,v=3,e=3)
pairs=[g.generate('moderate',seed=822157,template='inconsistent_shift',parameters=z) for z in [p,dict(p,v=1),dict(p,e=4)]]
write('counterfactual-records.json',pairs)
rejections=[]
for label,level,template,p0 in [('zero_root','moderate','inconsistent_shift',dict(p,v=4)),('new_source_fractional_bare','hard','dependent_fractional',dict(a=2,b=-2,c=4,d=-3,u=1,v=0,e=-6)),('invalid_easy_zero_residual','easy','inconsistent_easy',dict(a=1,b=2,c=1,d=2,u=1,v=0,e=2)),('invalid_pivot','easy','inconsistent_easy',dict(a=0,b=2,c=1,d=2,u=1,v=0,e=3))]:
 try:r=g.generate(level,seed=822157,template=template,parameters=p0); result='accepted'
 except Exception as e:result=type(e).__name__+': '+str(e)
 rejections.append(dict(label=label,level=level,template=template,parameters=p0,result=result))
write('rejections.json',rejections)
# Native radio UI contract: every choice on runner batch, representative templates, pairs and source replays.
grader=[]
for ix,r in enumerate(batch+[next(z for z in samples if z['generation']['template']==t) for tt in g.TEMPLATES.values() for t in tt]+pairs+replays):
 f=r['question'][':question/answer-fields'][0];grader.append({'label':f'independent radio {ix}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Printed-equation independent key; all bank members exercised'} for a in f[':answer-field/choices']]})
write('grader-input.json',grader)
write('render-records.json',batch[:2]+[next(z for z in samples if z['generation']['template']==t) for tt in g.TEMPLATES.values() for t in tt]+pairs)
# Package test: deterministic replay, relocation without bytecode, exact dependencies, source manifest hashes.
rel=R/'relocated';rel.mkdir(exist_ok=True)
for name in json.load(open(W/'package.json'))['files']+['package.json']:
 dst=rel/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/name,dst)
def cli(path):return subprocess.run([PY,'-B',str(path),'--difficulty','easy','--seed','822101','--count','2','--format','json'],capture_output=True,text=True)
one=cli(W/'17592186115242.py');two=cli(rel/'17592186115242.py');write('packaging.json',{'python':platform.python_version(),'sympy':s.__version__,'manifest_dependencies':json.load(open(W/'package.json'))['dependencies'],'deterministic_replay':samples[0]==g.generate('easy',seed=822101,template='inconsistent_easy'),'cli_exit':one.returncode,'relocation_exit':two.returncode,'relocation_same':one.stdout==two.stdout,'stderr':one.stderr+two.stderr,'package_hashes':{str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [W/n for n in json.load(open(W/'package.json'))['files']+['package.json']]}})
print('source replay',collections.Counter(z['status'] for z in replay_report),'math',collections.Counter(z['status'] for z in math),'samples',len(samples),'rejections',rejections)

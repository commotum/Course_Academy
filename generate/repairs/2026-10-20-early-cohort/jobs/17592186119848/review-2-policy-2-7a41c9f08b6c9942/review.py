import sys,os,json,re,hashlib,importlib.util,shutil,subprocess,platform
from pathlib import Path
from fractions import Fraction
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent
J=E.parent; W=J/'workspace'; R=Path('/home/jake/Developer/Course_Academy'); PY=R/'.venv/bin/python'
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def load(p):return json.loads(Path(p).read_text())
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
save('package-before.json',hashes())
sys.path.insert(0,str(W));spec=importlib.util.spec_from_file_location('audited_generator',W/'17592186119848.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def norm(t):
 t=t.replace('\\\\begin','\\begin').replace('\\\\end','\\end');return t.replace('\\\\\\\\','\\\\')
pat=re.compile(r'([A-E])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def matrices(q):
 texts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  texts.append(f[':answer-field/key']);texts.extend(a[':answer/value'] for a in f[':answer-field/choices'])
 ans={}
 for t in texts:
  for label,body in pat.findall(norm(t)):ans[label]=[[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
 return ans
def rank(m):
 a=[list(map(Fraction,row)) for row in m];r=0
 for c in range(len(a[0])):
  k=next((i for i in range(r,len(a)) if a[i][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
  for i in range(r+1,len(a)):
   v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
def correct(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def labels(t):return sorted(set(re.findall(r'\$([A-E])\$',t)))
def expected(q,f):
 r=int(re.search(r'rank of \$(\d+)',q[':question/problem'])[1]);ms=matrices(q);matches=sorted(k for k,m in ms.items() if rank(m)==r)
 def right(a):
  if f[':answer-field/type'].endswith('/checkbox'):
   labs=list(matrices({':question/problem':f[':answer-field/key']}));truth=labs[0] in matches if labs else not matches
   return a[':answer/value']==str(truth).lower()
  am=matrices({':question/problem':a[':answer/value']})
  return list(am)==matches if am else labels(a[':answer/value'])==matches
 return [a for a in f[':answer-field/choices'] if right(a)]
source=load(J/'source/source.json');qs=source['material']['kp'][':knowledge-point/questions']
sourceres=[];replays=[]
for q in qs:
 sid=q[':question/math-academy-id'];ms=matrices(q);r=int(re.search(r'rank of \$(\d+)',q[':question/problem'])[1]);row={'source_id':q[':question/id'],'profile':sid,'ranks':{k:rank(m) for k,m in ms.items()},'target':r}
 if sid in g.CASES:
  rec=g.generate('easy',179,sid,{'matches':[k for k,m in sorted(ms.items()) if rank(m)==r],'scale':1},source_replay=True);replays.append(rec);new=rec['question']
  row['matrix_equal']=matrices(new)==ms; row['field_count_equal']=len(new[':question/answer-fields'])==len(q[':question/answer-fields'])
  row['banks_equal']=[[(a[':answer/type'][':db/ident'],norm(a[':answer/value']).replace('  ',' ')) for a in f[':answer-field/choices']]==[(a[':answer/type'],norm(a[':answer/value']).replace('  ',' ')) for a in nf[':answer-field/choices']] for f,nf in zip(q[':question/answer-fields'],new[':question/answer-fields'])]
  # Strip normalized whitespace and presentation before source solution comparison.
  canon=lambda t: re.sub(r'\s+','',norm(t).replace('coumns','columns'))
  row['solution_equal']=canon(q[':question/worked-solution'])==canon(new[':question/worked-solution']);row['record_id']=new[':question/id']
 else:row['supported']=False;row['gap']='Captured key and solution absent; ranks and complete bank independently inspected. Not claimed as exact replay.'
 sourceres.append(row)
save('source-replay.json',sourceres);save('replays.json',replays)
cat=g.catalog();save('catalog.json',cat)
fresh=[g.generate('easy',seed) for seed in [1763,5281,14653,62003,91283,134669]];save('fresh.json',fresh)
batch=load(J/'samples.json');save('batch.json',batch)
# Controlled changes on q-34823: same dimensions and coefficients except one pivot role; scalar rescaling is irrelevant to rank.
pairs=[g.generate('easy',521,'q-34823',{'matches':x,'scale':scale}) for x,scale in [(['A'],1),(['C'],1),(['A'],2)]];save('counterfactual-records.json',pairs)
records=cat+fresh+batch+pairs+replays
mathrows=[];cases=[]
for i,rec in enumerate(records):
 q=rec['question'];ms=matrices(q);rr={k:rank(m) for k,m in ms.items()};r=int(re.search(r'rank of \$(\d+)',q[':question/problem'])[1]);errors=[]
 checks=[]
 for fi,f in enumerate(q[':question/answer-fields']):
  exp=expected(q,f)
  if len(exp)!=1 or exp[0][':answer/id']!=correct(f)[':answer/id']:errors.append({'field':fi,'expected':[a[':answer/value'] for a in exp],'actual':correct(f)[':answer/value']})
  for a in f[':answer-field/choices']:
   checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a in exp else 'rejected','purpose':'Fraction elimination from visible matrices, not generator metadata'})
 for lab,val in re.findall(r'\\(?:text|textrm)\{rank\}\(([A-E])\)\s*=\s*(\d+)',q[':question/worked-solution']):
  if int(val)!=rr[lab]:errors.append({'stale_solution':lab,'claimed':val,'rank':rr[lab]})
 mathrows.append({'index':i,'question_id':q[':question/id'],'profile':rec['generation']['source_id'],'ranks':rr,'matches':sorted(k for k,v in rr.items() if v==r),'errors':errors})
 cases.append({'label':str(i)+' '+rec['generation']['source_id'],'record':rec,'checks':checks})
save('math-results.json',{'cases':len(records),'failures':[x for x in mathrows if x['errors']],'results':mathrows});save('grader-input.json',cases)
# Source-backed, strict relevant and irrelevant pair assertions on visible records.
paircheck={'relevant':{'before_ranks':{k:rank(m) for k,m in matrices(pairs[0]['question']).items()},'after_ranks':{k:rank(m) for k,m in matrices(pairs[1]['question']).items()},'before_answer':correct(pairs[0]['question'][':question/answer-fields'][0])[':answer/value'],'after_answer':correct(pairs[1]['question'][':question/answer-fields'][0])[':answer/value'],'excluded_B_unchanged':matrices(pairs[0]['question'])['B']==matrices(pairs[1]['question'])['B'],'solution_changed':pairs[0]['question'][':question/worked-solution']!=pairs[1]['question'][':question/worked-solution']},'irrelevant':{'change':'multiply all entries by 2','ranks_preserved':all(rank(matrices(pairs[0]['question'])[k])==rank(matrices(pairs[2]['question'])[k]) for k in 'ABC'),'answer_preserved':correct(pairs[0]['question'][':question/answer-fields'][0])[':answer/value']==correct(pairs[2]['question'][':question/answer-fields'][0])[':answer/value'],'solution_preserved':pairs[0]['question'][':question/worked-solution']==pairs[2]['question'][':question/worked-solution']}}
save('counterfactual-results.json',paircheck)
# Declared-only relocation, subprocess replay and boundaries. Never run author test in the package (it writes there).
rel=E/'relocated';rel.mkdir(exist_ok=True);manifest=load(W/'package.json');shutil.copy2(W/'package.json',rel/'package.json')
for name in manifest['files']:
 d=rel/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/name,d)
cmd=[str(PY),'-B',str(rel/manifest['entrypoint']),'--seed','21077','--count','5'];env={k:v for k,v in os.environ.items() if k not in ('PYTHONPATH','PYTHONHOME')};env['PYTHONDONTWRITEBYTECODE']='1';env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(E/'external-assets')
a=subprocess.run(cmd,cwd=E,env=env,text=True,capture_output=True);b=subprocess.run(cmd,cwd=E,env=env,text=True,capture_output=True);save('relocation-sample.json',json.loads(a.stdout) if a.returncode==0 else [])
pack={'command':cmd,'cwd':str(E),'returncode':a.returncode,'stderr':a.stderr,'deterministic':a.stdout==b.stdout,'dependencies':{'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'declared':manifest['dependencies'],'boundaries':[]}
for desc,func in [('count0',lambda:g.batch('easy',0,7)),('count25',lambda:g.batch('easy',25,7)),('count-1',lambda:g.batch('easy',-1,7)),('hard',lambda:g.generate('hard',7)),('invalid subset',lambda:g.generate('easy',7,'q-34823',{'matches':['B']}))]:
 try:out=func();pack['boundaries'].append({'case':desc,'returned_count':len(out)})
 except Exception as e:pack['boundaries'].append({'case':desc,'error':type(e).__name__+': '+str(e)})
# Copy author's regression and run it in the evidence relocation; constrain tempfile location.
(rel/'checks').mkdir(exist_ok=True);(rel/'evidence').mkdir(exist_ok=True);shutil.copy2(W/'checks/check_runtime.py',rel/'checks/check_runtime.py');env['TMPDIR']=str(E)
runtime=subprocess.run([str(PY),'-B',str(rel/'checks/check_runtime.py')],cwd=E,env=env,text=True,capture_output=True);pack['retained_check']={'returncode':runtime.returncode,'stdout':runtime.stdout,'stderr':runtime.stderr}
# Demonstrate its retained failure branch using an isolated explicit unresolved import.
entry=rel/manifest['entrypoint'];original=entry.read_text();entry.write_text('import scripts\n'+original.replace('#!/usr/bin/env python3\n','',1))
bad=subprocess.run([str(PY),'-B',str(rel/'checks/check_runtime.py')],cwd=E,env=env,text=True,capture_output=True);entry.write_text(original);pack['retained_failing_fixture']={'mutation':'prepend import scripts to evidence copy','returncode':bad.returncode,'stderr':bad.stderr};save('packaging-results.json',pack)
save('package-after.json',hashes());print(json.dumps({'catalog':len(cat),'fresh':len(fresh),'math_failures':len([x for x in mathrows if x['errors']]),'source_cases':len(sourceres),'package_unchanged':hashes()==load(E/'package-before.json'),'retained_check':runtime.returncode,'negative_control':bad.returncode,'batch_scales':[x['generation']['parameters']['scale'] for x in batch],'catalog_scales':sorted(set(x['generation']['parameters']['scale'] for x in cat))}))
(E/'session-state.md').write_text('Completed source replay, Fraction-rank checking, grader input, controlled pair construction, declared-file relocation and retained regression positive/negative fixtures. Package unchanged. Next: actual delivery, native grader, renderer, shortcut measurements.\n')

import os,sys,json,re,hashlib,importlib.util,pathlib,subprocess,shutil,copy
import sympy as sp
E=pathlib.Path(__file__).resolve().parent
B=E.parent; W=B/'workspace'; R=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=R/'.venv/bin/python'
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True;sys.path.insert(0,str(W))
spec=importlib.util.spec_from_file_location('review_g',W/'17592186184172.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def run(cmd,cwd=E):
 p=subprocess.run(list(map(str,cmd)),cwd=cwd,env={**os.environ,'PYTHONPATH':'','PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 return {'command':list(map(str,cmd)),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def val(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
def label(ts):
 a=[s for s,t in zip(['I','II','III'],ts) if t]
 return 'None' if not a else 'I, II, and III' if len(a)==3 else ' and '.join(a)+' only'
def parse(r):
 q=r['question'];p=q[':question/problem'];fs=q[':question/answer-fields'];n,m=map(int,re.search(r'(\d+)\s*\\times\s*(\d+)',p).groups());assert n==m
 ms=list(re.finditer(r'(?<![A-Z])(III|II|I)\.\s*',p))
 if len(fs)==1:
  assert [x[1] for x in ms]==['I','II','III'];prefix=p[:ms[0].start()];st=[p[m.end():ms[i+1].start() if i<2 else len(p)].strip() for i,m in enumerate(ms)]
 else:prefix=p;st=[f[':answer-field/key'] for f in fs]
 vectors=[]
 for m in re.finditer(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',prefix,re.S):
  if '&' in m[1]:continue
  cells=[re.sub(r'\{x\}_\{(\d)\}',r'x\1',s.strip()) for s in m[1].split(r'\\')]
  cells=[re.sub(r'(?<=\d)(?=[abx])','*',s) for s in cells]
  v=sp.Matrix([sp.sympify(s) for s in cells]);assert v.rows==n
  variables=v.free_symbols
  vectors.extend([v.diff(x) for x in sorted(variables,key=str)] if variables else [v])
 if vectors:
  u=int(sp.Matrix.hstack(*vectors).rank());rank=n-u
 else:
  count,kind=re.search(r'\$(\d+)\$\s+(non-pivot|pivot) column',prefix).groups();rank=n-int(count) if kind=='non-pivot' else int(count);u=n-rank
 assert 0<=rank<=n
 def truth(s):
  z=s.replace('$','').replace('**','').replace('\\\\','\\').replace('\\textrm','\\text').strip().rstrip('.')
  x=re.search(r'\\text\{(rank|nullity)\}\(A\)=(\d+)',z)
  if x:return (rank if x[1]=='rank' else u)==int(x[2])
  x=re.search(r'(\d+)-dimensional.*?\^\{?(\d+)',z)
  if x:return (rank,n)==tuple(map(int,x.groups()))
  if 'non-pivot columns' in z:return u==int(re.search(r'equal to\s*(\d+)',z)[1])
  x=re.search(r'has\s*(\d+)\s*pivot col',z)
  if x:return rank==int(x[1])
  if 'invertible' in z:return rank<n if re.search(r'\bnot\b',z) else rank==n
  if 'det(A)' in z:return rank==n if '\\ne' in z else rank<n
  if 'Col}' in z:return rank!=n if '\\ne' in z else rank==n
  raise ValueError(z)
 ts=list(map(truth,st));observed=[val(f) for f in fs];expected=[label(ts)] if len(fs)==1 else [str(t).lower() for t in ts]
 errors=[]
 if observed!=expected:errors.append({'expected':expected,'actual':observed})
 sol=q[':question/worked-solution']
 if 'truths' in r['generation']['parameters']:
  facts=re.search(r'Hence \$\\text\{rank\}\(A\)=(\d+)\$ and \$\\text\{nullity\}\(A\)=(\d+)\$',sol)
  if not facts or tuple(map(int,facts.groups()))!=(rank,u):errors.append('Incorrect concrete facts')
  for i,(s,t) in enumerate(zip(st,ts)):
   part=['I','II','III'][i] if len(fs)==1 else '“'+s+'”'
   if '- Statement '+part+' is '+str(t).lower()+'.' not in sol:errors.append('Bad statement evaluation '+part)
 return {'id':q[':question/id'],'template':r['generation']['template'],'n':n,'rank':rank,'nullity':u,'truths':ts,'label':label(ts),'statements':st,'errors':errors}

def native(rows):
 out=[]
 for r in rows:
  d=parse(r);assert not d['errors'],d
  checks=[]
  for i,f in enumerate(r['question'][':question/answer-fields']):
   expected=d['label'] if len(r['question'][':question/answer-fields'])==1 else str(d['truths'][i]).lower()
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==expected else 'rejected','purpose':'All choices; truth calculated from prompt, not generator metadata'} for a in f[':answer-field/choices'])
  out.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
 return out

source=json.load(open(B/'source/source.json'));src={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
# Do not use any author validation scripts or their oracle.
replay=[];replay_results=[]
for key,q in src.items():
 level=enum(q[':question/difficulty']).split('/')[-1];n=int(re.search(r'(\d+)\s*\\times',q[':question/problem'])[1]);p={'diagonal':[1]*n} if '\\begin' in q[':question/problem'] else {'scale':1}
 r=g.generate(level,512904,key,p);replay.append(r)
 checks={'problem':r['question'][':question/problem']==q[':question/problem'],'solution':r['question'][':question/worked-solution']==q[':question/worked-solution'],'difficulty':r['question'][':question/difficulty']==enum(q[':question/difficulty'])}
 sf=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
 checks['complete_fields']=len(sf)==len(r['question'][':question/answer-fields']) and all((f[':answer-field/key'],enum(f[':answer-field/type']),[a[':answer/value'] for a in f[':answer-field/choices']],f[':answer-field/correct'][':answer/value'])==(h[':answer-field/key'],h[':answer-field/type'],[a[':answer/value'] for a in h[':answer-field/choices']],val(h)) for f,h in zip(sf,r['question'][':question/answer-fields']))
 replay_results.append({'source_id':q[':question/id'],'template':key,'checks':checks,'math':parse(r)})
save('replay-records.json',replay);save('source-replay-results.json',{'cases':replay_results,'canonical_gap':'78547385-d46f-5a2a-bfc1-39e040208ca0 is not a generator profile; no captured canonical bank. Method is covered by other null-space profiles.'})
rows=[]
for i,key in enumerate(sorted(src)):
 level=enum(src[key][':question/difficulty']).split('/')[-1]
 for j in range(12):rows.append(g.generate(level,719333+101*i+j,key))
save('fresh-records.json',rows)
batch=json.load(open(B/'samples.json'));save('runner-batch.json',batch)
# Controlled comparisons use explicit choices, no random truth oracle.
pairs=[];controlled=[]
for key,p1,p2,kind in [
 ('q-34934',{'scale':1,'count':3,'truths':[True,False,True]},{'scale':1,'count':4,'truths':[True,False,True]},'relevant_count'),
 ('q-34934',{'scale':1,'count':3,'truths':[True,False,True]},{'scale':1,'count':3,'truths':[True,True,False]},'relevant_claim'),
 ('q-143533',{'diagonal':[1,1,1],'truths':[True,False,True]},{'diagonal':[3,2,1],'truths':[True,False,True]},'irrelevant_coordinate')]:
 level=enum(src[key][':question/difficulty']).split('/')[-1];rs=[g.generate(level,382991,key,p) for p in [p1,p2]];ds=[parse(r) for r in rs];controlled.extend(rs)
 pairs.append({'kind':kind,'parameters':[p1,p2],'records':[r['question'][':question/id'] for r in rs],'derived':ds,'keys_changed':[val(f) for f in rs[0]['question'][':question/answer-fields']]!=[val(f) for f in rs[1]['question'][':question/answer-fields']]})
save('counterfactual-records.json',controlled);save('counterfactual-results.json',pairs)
# Boundaries and explicit invalid-parameter rejection.
bounds=[];reject=[]
for key in sorted(src):
 level=enum(src[key][':question/difficulty']).split('/')[-1];n=int(re.search(r'(\d+)\s*\\times',src[key][':question/problem'])[1])
 if '\\begin' not in src[key][':question/problem']:
  for scale in [1,3]:
   for count in [0,n*scale]:bounds.append(g.generate(level,10007,key,{'scale':scale,'count':count,'truths':next(parse(r)['truths'] for r in replay if r['generation']['template']==key)}))
for level,key,p in [('easy',None,None),('moderate','q-34934',{'scale':0}),('moderate','q-34934',{'scale':1,'count':-1}),('moderate','q-34934',{'scale':1,'count':5}),('moderate','q-143533',{'diagonal':[0,1,1]}),('moderate','q-143533',{'diagonal':[1,1,1],'truths':[False]*3})]:
 try:g.generate(level,17,key,p);result='accepted'
 except Exception as e:result=type(e).__name__+': '+str(e)
 reject.append({'difficulty':level,'template':key,'parameters':p,'result':result})
save('boundary-records.json',bounds);save('rejection-results.json',reject)
allrows=replay+rows+batch+controlled+bounds
results=[parse(r) for r in allrows];save('math-results.json',{'count':len(results),'failures':[r for r in results if r['errors']],'cases':results})
# Check batch replay including complete metadata.
save('determinism.json',{'fresh_repeat':all(g.generate(enum(src[r['generation']['template']][':question/difficulty']).split('/')[-1],r['generation']['seed'],r['generation']['template'])==r for r in rows),'runner_batch_replay':all(g.generate('moderate',r['generation']['seed'],r['generation']['template'],r['generation']['parameters'])==r for r in batch)})
save('native-input.json',native(allrows));save('render-records.json',batch+controlled+[replay[0],next(r for r in rows if len(r['question'][':question/answer-fields'])==3 and r['question'][':question/difficulty'].endswith('/hard'))])
# Runtime closure and original failing executable counterexample.
manifest=json.load(open(W/'package.json'));dest=E/'relocated';dest.mkdir(exist_ok=True)
for name in manifest['files']:
 p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,p)
pack=[]
for level in ['moderate','hard']:
 x=run([PY,'-I',dest/manifest['entrypoint'],'--difficulty',level,'--count','5','--seed','982013'],dest)
 # -I intentionally removes script directory as well; normal contract uses no -I.
 normal=run([PY,dest/manifest['entrypoint'],'--difficulty',level,'--count','5','--seed','982013'],dest);save('relocated-'+level+'.json',json.loads(normal['stdout']) if normal['exit']==0 else normal)
 pack.append({'level':level,'normal_exit':normal['exit'],'normal_stderr':normal['stderr'],'isolated_exit':x['exit'],'isolated_stderr':x['stderr']})
legacy=E/'legacy';legacy.mkdir(exist_ok=True);shutil.copyfile(W/'evidence/original-generator.py',legacy/'17592186184172.py');(legacy/'17592186184172').mkdir(exist_ok=True);shutil.copyfile(W/'17592186184172/source.json',legacy/'17592186184172/source.json')
old=run([PY,legacy/'17592186184172.py','--difficulty','moderate','--count','5','--seed','0'],legacy)
save('packaging-results.json',{'manifest':manifest,'actual_versions':{'python':sys.version.split()[0],'packages':{'sympy':sp.__version__}},'relocations':pack,'legacy_failure':old,'retained_check_assessment':'checks/packaging.py tests current closure only, not a failing original. checks/reproduce_legacy_import.py exists and targets the original StopIteration; reproduced independently here. Supplied repair-preflight.json absent; no retained findings in repair-history.json.'})
# Inventory provenance: exact original sources are not generated defects.
inv=json.load(open(B/'source/inventory.json'));iq=inv['questions'];original_ids={q[':question/id'] for q in src.values()};save('inventory-inspection.json',{'basis':inv['basis'],'count':len(iq),'original_source_ids':sum(q[':question/id'] in original_ids for q in iq),'non_source_records':[q for q in iq if q[':question/id'] not in original_ids],'question_keys':sorted(set(k for q in iq for k in q))})
save('affected-inventory.json',{'affected_questions':[]})
(E/'session-state.md').write_text('Source account saved before package inspection. Independently sampled 180 records across 15 profiles; replayed 15 exact source prompts, solutions and full banks. Native input, counterfactuals, boundary cases, math, relocation and inventory evidence saved by audit.py. Next: shared delivery, native grader, actual rendering and conditional shortcut assessment.\n')
print(json.dumps({'replay':len(replay),'replay_failures':[r for r in replay_results if not all(r['checks'].values())],'math_records':len(results),'math_failures':sum(bool(r['errors']) for r in results),'inventory_count':len(iq),'packaging':pack,'counterfactuals':pairs},default=str))

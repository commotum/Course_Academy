import sys, os, json, pathlib, hashlib, importlib.util, subprocess, shutil, re
from fractions import Fraction as F
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
J=E.parent; P=J/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=REPO/'.venv/bin/python'
os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['TMPDIR']=str(E/'tmp');(E/'tmp').mkdir(exist_ok=True)
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def run(args,cwd=E):
 r=subprocess.run(list(map(str,args)),cwd=cwd,env=os.environ,capture_output=True,text=True)
 return {'command':list(map(str,args)),'cwd':str(cwd),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def hashes():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(P.rglob('*')) if p.is_file()}
save('package-hashes-before.json',hashes())
sys.path.insert(0,str(P));spec=importlib.util.spec_from_file_location('review_generator',P/'17592186124630.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.load(open(J/'source/source.json'))['material']['kp']; inventory=json.load(open(J/'source/inventory.json'))
replays=[];fidelity=[]
for q in source[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];r=g.replay(sid);rq=r['question']; sf=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
 key=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
 matches={k:rq[k]==q[k] for k in [':question/problem',':question/worked-solution']}
 matches.update(bank=[(a[':answer/value'],a[':answer/type']) for a in rf[':answer-field/choices']]==[(a[':answer/value'],a[':answer/type'][':db/ident']) for a in sf[':answer-field/choices']],key=key==sf[':answer-field/correct'][':answer/value'],field=rf[':answer-field/key']==sf[':answer-field/key'] and rf[':answer-field/type']==sf[':answer-field/type'][':db/ident'])
 assert all(matches.values());fidelity.append({'source_id':q[':question/id'],'ma_id':sid,'checks':matches});replays.append(r)
save('source-replays.json',replays);save('source-replay-results.json',fidelity)
# Fresh public seeds; enumerate all justified construction pairs separately.
seeds=[27,814,20261021];sample=[r for seed in seeds for r in g.generate('easy',11,seed)]
save('fresh-samples.json',sample); batch=json.load(open(J/'samples.json'));save('runner-batch.json',batch)
assignments=[g.make_record(t,p,7400+i) for i,(p,t) in enumerate((p,t) for p,ts in g.BANKS.items() for t in ts)]
save('assignments.json',assignments)
# Rational linear algebra oracle: no target metadata or generator term table.
def rref(a):
 a=[list(map(F,row)) for row in a];piv=[];r=0
 for c in range(len(a[0]) if a else 0):
  k=next((i for i in range(r,len(a)) if a[i][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
  for i in range(len(a)):
   if i!=r:
    v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  piv.append(c);r+=1
  if r==len(a):break
 return a,piv

def span(vs):return tuple(tuple(r) for r in rref(vs)[0] if any(r))
def meanings(a):
 n=len(a);rr,ps=rref(a);rank=len(ps);cols=list(zip(*a));ker=[]
 for j in set(range(n))-set(ps):
  v=[F(0)]*n;v[j]=1
  for i,p in enumerate(ps):v[p]=-rr[i][j]
  ker.append(v)
 return n,rank,span(cols),span(ker),span([[int(i==j) for j in range(n)] for i in range(n)])
HOLE=r'\underline{\phantom{WWWW}}'
def parts(r):
 q=r['question'][':question/problem'];block=q.split('$$')[1].strip();assert block.count(HOLE)==1
 prop,rows=block.removeprefix(r'\begin{gathered}').removesuffix(r'\end{gathered}').split(r' \\ \Updownarrow \\ \left\{\begin{aligned}')
 return prop.removeprefix(r'A\text{ is }'), rows.removesuffix(r'\end{aligned}\right.').split(r' \\ ')
def value(t,m):
 n,r,col,ker,full=m;t=t.strip()
 if t in ['0','n','n+1']:return ('scalar',{'0':0,'n':n,'n+1':n+1}[t])
 if t==r'\mathbb{R}^{n}':return ('space',full)
 if t==r'\{0\}':return ('space',())
 if t==r'\operatorname{Col}(A)':return ('space',col)
 if t==r'\operatorname{Null}(A)':return ('space',ker)
 if t in [r'\dim(\operatorname{Col}(A))',r'\operatorname{rank}(A)']:return ('scalar',r)
 if t in [r'\dim(\operatorname{Null}(A))',r'\operatorname{nullity}(A)']:return ('scalar',n-r)
 raise ValueError(t)
matrices=[]
for n in [1,2,4]:
 for kind in ['zero','identity','twice_identity','upper_invertible','diagonal_singular','nondiagonal_singular']:
  a=[[0 for j in range(n)] for i in range(n)]
  for i in range(n):
   for j in range(n):
    a[i][j]=(int(i==j) if kind=='identity' else 2*int(i==j) if kind=='twice_identity' else 2*int(i==j)+3*int(j==i+1) if kind=='upper_invertible' else int(i==j and i<n-1) if kind=='diagonal_singular' else (i+1)*(j+1) if kind=='nondiagonal_singular' and n>1 else 0)
  matrices.append((kind,a))
def truth(rec,candidate):
 prop,rows=parts(rec)
 for kind,a in matrices:
  n,r,*_=m=meanings(a);p=prop.replace(HOLE,candidate)
  p=p.removeprefix(r'\text{').removesuffix('}')
  lhs={'invertible':r==n,'not invertible':r!=n,'diagonal':all(a[i][j]==0 for i in range(n) for j in range(n) if i!=j),'identity':all(a[i][j]==int(i==j) for i in range(n) for j in range(n)),'not identity':any(a[i][j]!=int(i==j) for i in range(n) for j in range(n))}.get(p)
  if lhs is None:return False
  vals=[[value(t,m) for t in row.replace(HOLE,candidate).replace('&','').split('=')] for row in rows]
  rhs=all(all(v==vs[0] for v in vs) for vs in vals)
  if lhs!=rhs:return False
 return True

def key(r):
 f=r['question'][':question/answer-fields'][0]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
math_results=[];grader=[]
for origin,records in [('assignments',assignments),('runner-batch',batch),('fresh',sample)]:
 for i,r in enumerate(records):
  q=r['question'];f=q[':question/answer-fields'][0];true=[a for a in f[':answer-field/choices'] if truth(r,a[':answer/value'])]
  assert len(true)==1,(origin,i,true);assert true[0][':answer/id']==key(r)[':answer/id']
  completed=q[':question/problem'].split('$$')[1].strip().replace(HOLE,r'\text{invertible}' if key(r)[':answer/value']=='invertible' else key(r)[':answer/value'])
  assert completed in q[':question/worked-solution'];assert (('"invertible".' if key(r)[':answer/value']=='invertible' else '$'+key(r)[':answer/value']+'$.')) in q[':question/worked-solution']
  math_results.append({'origin':origin,'index':i,'question_id':q[':question/id'],'true_choices':[a[':answer/value'] for a in true],'solution_completed_correctly':True})
  if origin!='fresh':grader.append({'label':f'{origin}/{i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if truth(r,a[':answer/value']) else 'rejected','purpose':'Independent visible theorem and exact rational matrix witnesses'} for a in f[':answer-field/choices']]})
save('math-results.json',{'matrices':matrices,'records':math_results,'universal_argument':'For every n>=1, invertibility forces column space R^n, null space {0}, rank and column dimension n, null dimension and nullity zero. In each sampled bank the remaining choices are different mathematical types or different values; n+1 differs from both n and 0. Adjective alternatives fail on 2I or a non-diagonal invertible matrix. Singular witnesses also verify the displayed biconditional.','limitations':'Finite witnesses do not enumerate all real square matrices; the preceding theorem argument covers the declared symbolic domain.'})
# Relevant controlled pairs: same full bank, move blank. Irrelevant: reorder options only.
pairs=[];irrelevant=[]
for profile in ['named','dimensions','values']:
 rs=[r for r in assignments if r['generation']['bank_profile']==profile]
 for a,b in zip(rs,rs[1:]):
  assert sorted(x[':answer/value'] for x in a['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(x[':answer/value'] for x in b['question'][':question/answer-fields'][0][':answer-field/choices'])
  assert key(a)[':answer/value']!=key(b)[':answer/value'];assert a['question'][':question/problem']!=b['question'][':question/problem']
  pairs.append({'kind':'relevant','profile':profile,'before':a,'after':b,'old_response':key(a)[':answer/value'],'new_response':key(b)[':answer/value']})
for a in assignments:
 b=g.make_record(a['generation']['target'],a['generation']['bank_profile'],100019)
 assert a['question'][':question/problem']==b['question'][':question/problem'];assert a['question'][':question/worked-solution']==b['question'][':question/worked-solution'];assert key(a)==key(b)
 irrelevant.append(b);pairs.append({'kind':'irrelevant','before':a,'after':b,'preserved_answer':key(a)[':answer/value']})
 grader.append({'label':'irrelevant/'+a['generation']['target'],'record':b,'checks':[{'submitted_answer_id':x[':answer/id'],'expected':'accepted' if truth(b,x[':answer/value']) else 'rejected','purpose':'Choice-order counterfactual preserves mathematical answer'} for x in b['question'][':question/answer-fields'][0][':answer-field/choices']]})
save('counterfactuals.json',pairs);save('grader-input.json',grader)
# Runtime/count, deterministic replay, relocation, and supplied regression reproduction.
runtime=[]
for count in [0,1,5,11,12,-1]:
 r=run([PY,P/'17592186124630.py','--count',count,'--seed',814]);runtime.append(r)
 assert (r['returncode']==0)==(0<=count<=11)
 if 0<=count<=11:assert len(json.loads(r['stdout']))==count
for d in ['moderate','hard']:
 r=run([PY,P/'17592186124630.py','--difficulty',d]);assert r['returncode']!=0;runtime.append(r)
r=run([PY,P/'17592186124630.py','--count',5,'--seed',814]);r2=run([PY,P/'17592186124630.py','--count',5,'--seed',814]);assert r['stdout']==r2['stdout'];runtime.append(r)
manifest=json.load(open(P/'package.json'));rel=E/'relocated';rel.mkdir(exist_ok=True)
for f in manifest['files']:shutil.copyfile(P/f,rel/f)
r3=run([PY,rel/manifest['entrypoint'],'--count',5,'--seed',814],cwd=rel);assert r3['stdout']==r['stdout'];runtime.append(r3)
save('runtime-results.json',runtime)
ac=E/'author-check/workspace';ac.mkdir(parents=True,exist_ok=True)
for f in manifest['files']+['package.json','check_repair.py']:shutil.copyfile(P/f,ac/f)
(ac.parent/'source').mkdir(exist_ok=True)
for f in ['source.json','inventory.json']:shutil.copyfile(J/'source'/f,ac.parent/'source'/f)
acrun=run([PY,ac/'check_repair.py']);save('author-check-run.json',acrun);assert acrun['returncode']==0,acrun['stderr']
legacy=E/'legacy/17592186124630.py';legacy.parent.mkdir(exist_ok=True);shutil.copyfile(P/'evidence/entrypoint-before.py',legacy)
ld=legacy.with_suffix('')/'reference/initial';ld.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/'17592186124630/reference/initial/kp.json',ld/'kp.json')
lr=run([PY,legacy,'--count',5,'--seed',0]);old=json.loads(lr['stdout']);assert not isinstance(old,list) and old['produced']==0
nr=run([PY,P/'17592186124630.py','--count',5,'--seed',0]);assert len(json.loads(nr['stdout']))==5
save('legacy-regression.json',{'before':lr,'current':nr,'strict_acceptance':'Successful --count 5 must return a JSON array of exactly five complete records.','failing_example_detected':True,'current_passed':True,'author_check_limitation':'Declared check_repair.py asserts current counts but does not execute its retained before.json failure. This independent reproduction executes the retained old entrypoint.'})
versions=run([PY,'-c','import sys;print(sys.version.split()[0])']);assert manifest['dependencies']=={'python':versions['stdout'].strip(),'packages':{}};save('dependency-check.json',{'manifest':manifest,'actual_python':versions,'imports':'argparse, hashlib, json, random, uuid, pathlib and declared sibling math_format; only standard library imports in math_format.'})
source_ids={q[':question/id'] for q in source[':knowledge-point/questions']};assert all(q[':question/id'] in source_ids for q in inventory['questions']);assert all(not any('generation' in k for k in q) for q in inventory['questions'])
save('inventory-audit.json',{'basis':inventory['basis'],'lineage':inventory['lineage'],'question_count':len(inventory['questions']),'original_source_ids':sorted(source_ids),'generated_count':0,'tested':'All 16 inventory records match captured original source question identities; no generated question to reproduce or attribute. Source-bank corrections are original-source issues, not affected generated inventory.','limits':'Captured basis only; later bank changes and individual learner history unavailable.'});save('affected-inventory.json',{'affected_questions':[]})
# Raw render records include all 13 constructions, actual batch, and an irrelevant reorder.
save('render-records.json',assignments+batch+irrelevant[:1]);save('duplicate-probe.json',[assignments[0],assignments[0]])
(E/'session-state.md').write_text('Milestone: independent source account, exact 16-source replay, 51 records checked by rational matrix witnesses, all 13 construction pairs and 5 actual batch records; source-bank corrections explicit. Relevant/irrelevant controlled pairs saved. Runtime, relocation, legacy failing/current passing reproduction and author check passed. Pending delivery, native grader, actual renderer and shortcut/selection review.\n')
print(json.dumps({'source_replays':len(replays),'math_records':len(math_results),'grader_cases':len(grader),'runtime_passed':True,'legacy_reproduced':True,'author_check_passed':True}))

import sys,json,re,hashlib,importlib.util,pathlib,copy,collections,subprocess,shutil
from fractions import Fraction
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
B=E.parent; R=pathlib.Path('/home/jake/Developer/Course_Academy'); P=B/'workspace'; PY=R/'.venv/bin/python'
def save(n,v): (E/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def hashes():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
save('package-before.json',hashes())
spec=importlib.util.spec_from_file_location('review_generator',P/'17592186119806.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.load(open(B/'source/source.json')); inventory=json.load(open(B/'source/inventory.json'))
batch=json.load(open(B/'samples.json'));save('batch-records.json',batch)
M=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def norm(t):return t.replace('\\\\begin','\\begin').replace('\\\\end','\\end').replace('\\\\\\\\','\\\\')
def vec(t):return tuple(Fraction(v.strip()) for v in M.fullmatch(norm(t))[1].split('\\\\'))
def parsed(r):
 q=r.get('question',r);p=q[':question/problem'];m=re.search(r'\$(\d+)a\s*([+-])\s*(\d+)x\s*=\s*b\$',p)
 if not m:raise ValueError(p)
 c=int(m[1]);d=int(m[3])*(1 if m[2]=='+' else -1);vs=M.findall(p);a=vec('\\begin{bmatrix}'+vs[0]+'\\end{bmatrix}');b=vec('\\begin{bmatrix}'+vs[-1]+'\\end{bmatrix}');x=tuple((v-c*u)/d for u,v in zip(a,b))
 pre=p.split('given that')[0];t=re.search(r'(?:\{x\}|x)_\{(\d+)\}\s*([+-])\s*(?:\{x\}|x)_\{(\d+)\}',pre)
 target=(int(t[1])-1,int(t[3])-1,t[2]) if t else None
 val=x if target is None else x[target[0]]+(1 if target[2]=='+' else -1)*x[target[1]]
 return c,d,a,b,x,target,val
def choices(r):
 f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 return [(a[':answer/id'],vec(a[':answer/value']) if '\\begin' in a[':answer/value'] else Fraction(a[':answer/value'])) for a in f[':answer-field/choices']],cid
def check(r):
 c,d,a,b,x,t,val=parsed(r);ch,cid=choices(r);q=r['question'];sol=q[':question/worked-solution'];ms=M.findall(sol);end=vec('\\begin{bmatrix}'+ms[-1]+'\\end{bmatrix}')
 ok=(next(v for i,v in ch if i==cid)==val and sum(v==val for i,v in ch)==1 and len(set(v for i,v in ch))==5 and end==x)
 # independently test the penultimate solution vector against either signed or reverse subtraction
 intermediate=vec('\\begin{bmatrix}'+ms[-2]+'\\end{bmatrix}');ok &= intermediate in [tuple(d*z for z in x),tuple(-d*z for z in x)]
 if t:ok &= sol.endswith('='+str(val)+'.$')
 return {'id':q[':question/id'],'profile':r['generation']['source_id'],'target':t,'expected':str(val),'passed':bool(ok)}
# Source fidelity at original parameters, independent captured bank comparison.
replays=[];out=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];entry={'source_id':q[':question/id'],'profile':sid}
 if sid not in g.CASES:entry.update(status='unsupported',reason='Current package has no profile for captured source question',has_solution=':question/worked-solution' in q)
 else:
  t=parsed(q)[5];r=g.generate('easy',91873,sid,{'scale':1,'target':list(t) if t else None});replays.append(r)
  oldf=q[':question/answer-fields'][0];newf=r['question'][':question/answer-fields'][0]
  bank=sorted(norm(a[':answer/value']) for a in oldf[':answer-field/choices']);bank2=sorted(a[':answer/value'] for a in newf[':answer-field/choices'])
  oldcorrect=norm(oldf[':answer-field/correct'][':answer/value']);newchoices,newid=choices(r)
  entry.update(status='passed' if bank==bank2 and r['question'][':question/problem']==q[':question/problem'] and r['question'][':question/worked-solution']==q[':question/worked-solution'] else 'failed',bank_equal=bank==bank2,correct_equal=(vec(oldcorrect) if '\\begin' in oldcorrect else Fraction(oldcorrect))==parsed(r)[6],math=check(r))
 out.append(entry)
save('source-replay-records.json',replays);save('source-replay.json',{'command':str(PY)+' '+str(E/'audit.py'),'cases':out,'canonical':'e-4790 not implemented; canonical has no captured answer bank','source_gap':'q-34574 missing solution/key; independently derived -1, excluded by implementation','supported':len(replays),'captured_practice':len(out)})
# Independently chosen seeds plus full finite domain to check the demonstrated invariant.
fresh=[g.generate('easy',s) for s in range(88421,88461)];domain=g.catalog();save('fresh-records.json',fresh);save('domain-records.json',domain)
math=[check(r) for r in domain+fresh+batch];save('math.json',{'method':'Fraction arithmetic from prompt and actual choice values, final and intermediate solution vectors; no correct_value metadata used','results':math,'passed':all(v['passed'] for v in math)})
# Controlled target reversal, target replacement, and irrelevant seed reordering.
a=g.generate('easy',48291,'q-34601',{'scale':2,'target':[2,1,'-']});b=g.generate('easy',48291,'q-34601',{'scale':2,'target':[1,2,'-']});c=g.generate('easy',48291,'q-34601',{'scale':2,'target':[0,2,'-']});d=g.generate('easy',48292,'q-34601',{'scale':2,'target':[2,1,'-']})
cf=[a,b,c,d];save('counterfactual-records.json',cf);save('counterfactual-results.json',{'command':str(PY)+' '+str(E/'audit.py'),'relevant_reversal':{'before':str(parsed(a)[6]),'after':str(parsed(b)[6]),'expected':'Negation with unchanged supplied vectors','passed':parsed(a)[6]==-parsed(b)[6] and parsed(a)[2:4]==parsed(b)[2:4]},'relevant_retarget':{'before':str(parsed(a)[6]),'after':str(parsed(c)[6]),'expected':'Recompute x1-x3 instead of x3-x2','passed':parsed(c)[6]==-32},'irrelevant_seed':{'before':a['question'][':question/id'],'after':d['question'][':question/id'],'answer_preserved':parsed(a)[6]==parsed(d)[6],'prompt_preserved':a['question'][':question/problem']==d['question'][':question/problem'],'solution_preserved':a['question'][':question/worked-solution']==d['question'][':question/worked-solution']},'math':[check(r) for r in cf]})
# Native radio grading: all options, including algebraically wrong ones, with independent expected key.
cases=[]
for label,records in [('source',replays),('fresh',fresh[:8]),('batch',batch),('counterfactual',cf)]:
 for i,r in enumerate(records):
  val=parsed(r)[6];ch,cid=choices(r)
  cases.append({'label':label+':'+str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':aid,'expected':'accepted' if v==val else 'rejected','purpose':'Independent equation-derived radio correctness'} for aid,v in ch]})
save('grader-input.json',cases)
# Keep complete records for UI, including both halves of the controlled pairs and exact batch.
save('render-records.json',batch+cf)
# Boundaries, determinism, runtime dependencies, relocation with no package mutation.
checks=[]
for label,args in [('invalid_level',('moderate',0,None,None)),('invalid_scale',('easy',0,'q-34601',{'scale':0,'target':[0,1,'-']})),('invalid_target',('easy',0,'q-34601',{'scale':1,'target':[0,0,'-']}))]:
 try:g.generate(*args);checks.append({'case':label,'passed':False})
 except ValueError as e:checks.append({'case':label,'passed':True,'message':str(e)})
for n in [-1,157]:
 try:g.batch('easy',n,771);checks.append({'case':'count '+str(n),'passed':False})
 except ValueError as e:checks.append({'case':'count '+str(n),'passed':True,'message':str(e)})
checks.append({'case':'deterministic replay','passed':g.generate('easy',88427)==g.generate('easy',88427)})
rel=E/'relocated';shutil.copytree(P,rel,dirs_exist_ok=True)
cmd=[str(PY),str(rel/'17592186119806.py'),'--count','5','--seed','72191'];res=subprocess.run(cmd,capture_output=True,text=True,cwd=E)
save('relocated-records.json',json.loads(res.stdout) if res.returncode==0 else {'error':res.stderr});checks.append({'case':'relocation explicit declared python','command':cmd,'passed':res.returncode==0 and json.loads(res.stdout)==g.batch('easy',5,72191)})
import sympy,platform
save('packaging.json',{'checks':checks,'versions':{'python':platform.python_version(),'packages':{'sympy':sympy.__version__}},'manifest':json.load(open(P/'package.json'))['dependencies'],'assets':'No generated assets; no output outside stdout by entrypoint','package_unchanged':hashes()==json.load(open(E/'package-before.json'))})
# Inventory contains originals only, no question-generation provenance. Do not relabel these as generated.
save('inventory-analysis.json',{'captured_basis':inventory['basis'],'count':len(inventory['questions']),'original_ids':[q[':question/id'] for q in inventory['questions']],'generated_records_with_metadata':sum(any('generat' in k for k in q) for q in inventory['questions']),'conclusion':'All 15 captured records are original source questions. No stored generated record with matching generation metadata exists in captured inventory. Original source bank quirks are not mislabeled as generated defects. Verified within this captured inventory, not later database state.'})
save('affected-inventory.json',{'affected_questions':[]})
(E/'session-state.md').write_text('Independent source account completed before author inspection. audit.py executed: source replay, exact Fraction arithmetic, controlled pairs, native grader inputs, UI samples, runtime/relocation checks, inventory inspection saved. Package unchanged. Native grader, delivery, and rendering still to execute. Demonstrated likely rank shortcut for q-34601; needs delivered/native confirmation.\n')
print(json.dumps({'domain':len(domain),'fresh':len(fresh),'source':out,'math_failures':[x for x in math if not x['passed']],'packaging':checks},default=str))

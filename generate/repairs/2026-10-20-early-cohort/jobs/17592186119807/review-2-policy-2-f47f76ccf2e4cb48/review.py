import os,sys,json,pathlib,hashlib,importlib.util,re,collections,subprocess,platform,shutil,itertools
from fractions import Fraction as F
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent; J=E.parent; P=J/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=REPO/'.venv/bin/python'
def save(n,x):
 p=E/n;p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(x,indent=2,default=str)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def hashes():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
def module(path,name):
 sys.path.insert(0,str(path.parent));s=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);return g
before=hashes();save('package-hashes-before.json',before)
g=module(P/'17592186119807.py','current_generator')
def num(s):
 s=re.sub(r'\s+','',s);s=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}',r'\1/\2',s)
 return F(s)
def vectors(r):return [tuple(num(v) for v in m.split(r'\\')) for m in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',r.get('question',r)[':question/problem'],re.S)]
def truth(r):
 a,c,b=vectors(r)
 for i,j in itertools.combinations(range(3),2):
  d=a[i]*c[j]-a[j]*c[i]
  if d:
   x=(b[i]*c[j]-b[j]*c[i])/d;y=(a[i]*b[j]-a[j]*b[i])/d
   return str(x+y) if all(a[k]*x+c[k]*y==b[k] for k in range(3)) else 'No solution'
 raise ValueError('dependent columns')
def choices(r):return r['question'][':question/answer-fields'][0][':answer-field/choices']
def key(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in choices(r) if a[':answer/id']==f[':answer-field/correct'][1])
def canon(s):return s if s=='No solution' else str(num(s))
def rank(r):return None if key(r)=='No solution' else sorted(num(a[':answer/value']) for a in choices(r) if a[':answer/type']==':answer.type/math').index(num(key(r)))+1
def params(residual=0,rank=2,t=0):return {'translation':t,'residual':residual,'rank':rank,'gaps':[1,2,3]}
def check(r):
 assert canon(key(r))==truth(r)
 assert len(choices(r))==5 and len({canon(a[':answer/value']) for a in choices(r)})==5
 return {'id':r['question'][':question/id'],'source_id':r['generation']['source_id'],'parameters':r['generation']['parameters'],'truth':truth(r),'key':key(r),'passed':True}
def metrics(rs):
 return {'n':len(rs),'consistent':sum(truth(r)!='No solution' for r in rs),'ranks':dict(collections.Counter(str(rank(r)) for r in rs)),'second_largest_success':sum(rank(r)==len([a for a in choices(r) if a[':answer/type']==':answer.type/math'])-1 for r in rs),'no_solution_success':sum(truth(r)=='No solution' for r in rs)}
source=load(J/'source/source.json');src=source['material']['kp'];batch=load(J/'samples.json');save('batch.json',batch)
replay=[];replays=[]
for q in src[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];r=g.generate('moderate',509,sid,{'translation':0});check(r)
 bank=lambda cc:sorted((canon(a[':answer/value']),a[':answer/type'].get(':db/ident') if isinstance(a[':answer/type'],dict) else a[':answer/type']) for a in cc)
 sol=q[':question/worked-solution'];correction=sid=='q-105163'
 if correction:
  assert r'-\frac{33}{2} & =-8' in sol
  sol=sol.replace(r'-\frac{33}{2} & =-8',r'-\frac{39}{2} & =-11')
  assert -3+3*F(-11,2)==F(-39,2)!=-11
 checks={'vectors':vectors(q)==vectors(r),'bank':bank(q[':question/answer-fields'][0][':answer-field/choices'])==bank(choices(r)),'key':canon(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])==truth(r),'problem':g.normalize_prose(q[':question/problem'])==r['question'][':question/problem'],'solution':g.normalize_prose(sol)==r['question'][':question/worked-solution']}
 assert all(checks.values()),(sid,checks)
 replay.append({'source_id':sid,'source_question_id':q[':question/id'],'checks':checks,'supported_correction':correction});replays.append(r)
save('source-replay.json',replay);save('source-records.json',replays)
# Controlled repaired branches and ranks at fixed coefficient columns and seed.
controls=[];pairs=[]
for sid in sorted(g.CASES):
 rs=[g.generate('moderate',509,sid,params(res,rk)) for res in (0,1) for rk in range(1,5)]
 assert {truth(r)=='No solution' for r in rs}=={False,True}
 assert {rank(r) for r in rs[:4]}=={1,2,3,4}
 assert len({r['question'][':question/problem'] for r in rs[:4]})==1
 a,b=rs[0],rs[4];av,bv=vectors(a),vectors(b)
 assert av[:2]==bv[:2] and sum(x!=y for x,y in zip(av[2],bv[2]))==1
 assert a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']
 controls+=rs;pairs.append({'profile':sid,'one_rhs_component_changes':True,'before':truth(a),'after':truth(b),'numeric_ranks':[rank(r) for r in rs[:4]]})
# Exact earlier target counterexample and irrelevant choice order: seed does not set content under explicit parameters.
bad=g.generate('moderate',509,'q-34568',params(-2));good=g.generate('moderate',509,'q-34568',params(0));irrelevant=g.generate('moderate',510,'q-34568',params(0))
assert vectors(bad)[2]==(3,4,5) and vectors(good)[2]==(3,4,7)
assert truth(bad)=='No solution' and truth(good)=='2'
assert good['question'][':question/problem']==irrelevant['question'][':question/problem']
assert good['question'][':question/worked-solution']==irrelevant['question'][':question/worked-solution']
assert choices(good)!=choices(irrelevant) and truth(good)==truth(irrelevant)
cf=[bad,good,irrelevant];save('counterfactual-records.json',cf)
save('counterfactual-results.json',{'command':str(PY)+' review.py','seed':509,'relevant':{'profile':'q-34568','parameters':[params(-2),params(0)],'rhs':[[3,4,5],[3,4,7]],'answers':[truth(bad),truth(good)],'prompt_solution_follow':True},'irrelevant':{'seeds':[509,510],'same_prompt_solution_truth':True,'order_changed':True},'profile_pairs':pairs})
fresh=[g.generate('moderate',seed,sid) for sid in sorted(g.CASES) for seed in (104729,)]
boundaries=[g.generate('moderate',727,sid,params(res,rk,t)) for sid in ('q-105163','q-34242','q-105165') for res,rk,t in [(-20,1,-2),('1/2',4,2),(20,2,2)]]
save('controlled-records.json',controls);save('fresh-records.json',fresh);save('boundary-records.json',boundaries)
allrecords=replays+controls+fresh+boundaries+cf+batch
save('math-results.json',[dict(group=label,index=i,**check(r)) for label,rs in [('source',replays),('controls',controls),('fresh',fresh),('boundary',boundaries),('counterfactual',cf),('batch',batch)] for i,r in enumerate(rs)])
# Verify replay and runtime dependency contract; no package caches or writes.
invalid=[]
for label,args in [('difficulty',('hard',)),('profile',('moderate',509,'absent')),('translation',('moderate',509,'q-34568',params(t=3))),('boolean',('moderate',509,'q-34568',params(t=True))),('rank',('moderate',509,'q-34568',params(rank=5))),('gaps',('moderate',509,'q-34568',dict(params(),gaps=[0,1,2]))),('residual',('moderate',509,'q-34568',params('1/3'))),('unknown slot',('moderate',509,'q-34568',{'target':[3,4,7]}))]:
 try:g.generate(*args);ok=False
 except ValueError:ok=True
 invalid.append({'case':label,'rejected':ok});assert ok
assert g.batch('moderate',5,291807)==g.batch('moderate',5,291807)
# Actual relocation of only manifest files to evidence_root.
rel=E/'relocated';rel.mkdir(exist_ok=True)
manifest=load(P/'package.json')
for f in manifest['files']:shutil.copy2(P/f,rel/f)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def cli(path,seed=291807):
 r=subprocess.run([str(PY),str(path),'--count','5','--seed',str(seed)],capture_output=True,text=True,check=True,env=env,cwd=E);return json.loads(r.stdout)
relocated=cli(rel/manifest['entrypoint']);assert relocated==g.batch('moderate',5,291807);save('relocation-records.json',relocated)
assert platform.python_version()==manifest['dependencies']['python'];assert g.sp.__version__==manifest['dependencies']['packages']['sympy']
save('packaging-results.json',{'python':platform.python_version(),'sympy':g.sp.__version__,'manifest':manifest,'deterministic':True,'relocation_identical':True,'invalid':invalid,'external_assets':0,'batch_replay':all(r==g.generate('moderate',r['generation']['seed'],r['generation']['source_id'],r['generation']['parameters']) for r in batch)})
# Negative controls prove retained tests detect old failures, rather than only accepting current outputs.
oldpath=J/'review-0-policy-2-a7f24163c8f738a6/relocated/17592186119807.py';old=module(oldpath,'old_generator')
neg=[]
for sid in ['q-105163','q-105165','q-105164','q-73957']:
 try:old.generate('moderate',509,sid,{'translation':0});failure=False
 except ValueError:failure=True
 neg.append({'old_missing_profile':sid,'detected':failure});assert failure
oldcat=old.catalog();oldbatch=load(J/'review-0-policy-2-a7f24163c8f738a6/batch.json')
assert all(key(r)=='No solution' for r in oldcat if '{c}_{1}' in r['question'][':question/problem'])
assert metrics(oldbatch)['second_largest_success']==5
assert any('{c}_{1}' in r['question'][':question/problem'] and truth(r)!='No solution' for r in controls)
assert metrics(batch)['second_largest_success']<len(batch)
save('retained-regressions.json',{'negative_control':{'missing':neg,'cd_label_all_no_solution':True,'old_batch':metrics(oldbatch)},'current':{'source_profiles':len(replay),'cd_has_consistent':True,'actual_batch':metrics(batch)},'old_entrypoint':str(oldpath)})
inv=load(J/'source/inventory.json');orig={q[':question/id'] for q in src[':knowledge-point/questions']};nonorig=[q for q in inv['questions'] if q[':question/id'] not in orig]
assert not nonorig
save('inventory-audit.json',{'basis':inv['basis'],'count':len(inv['questions']),'source_original_count':len(orig),'nonoriginal_count':len(nonorig),'verified_absence':'All captured question IDs match original source questions. No stored generated instances to reproduce; originals are not marked generated.'})
save('affected-inventory.json',{'affected_questions':[]})
save('raw-records.json',controls+fresh+boundaries+cf)
save('coverage.json',{'controls':metrics(controls),'fresh':metrics(fresh),'batch':metrics(batch),'profiles':{s:metrics([r for r in controls if r['generation']['source_id']==s]) for s in sorted(g.CASES)}})
save('scope-results.json',{'method':'Read source and new render solutions; independent Fraction solving on displayed vectors.','moderate_invariants':'2 unknowns, 3 rows, 5-choice radio, same elimination/substitution route, remaining-row check','fixed_source_columns':'Conservative reuse retains arithmetic method; targets cover both consistency branches, translated sums and all four numeric ranks. Coefficient-matrix diversity was not changed by this repair.','boundary_domain':'Residual +/-20 and half-integer tested; ordinary sampler uses -1,0,1; no new operators or prerequisites.'})
save('package-integrity.json',{'unchanged':before==hashes(),'files':len(before)});assert before==hashes()
(E/'session-state.md').write_text('Verified source analysis and all 14 complete source replays. Independent Fraction math, repaired controlled branches/ranks, fresh seeds, boundary inputs, prior negative controls, inventory identities, determinism and relocation pass. Pending actual delivery, learner grading, renderer and final shortcut assessment.\n')
print(json.dumps({'records_checked':len(allrecords),'source_replays':len(replay),'controlled_profiles':len(pairs),'batch':metrics(batch),'package_unchanged':before==hashes()}))

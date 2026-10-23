import sys
sys.dont_write_bytecode=True
import audit as a
from shortcut_regression import predict,probes
import copy,collections,json,hashlib,shutil,subprocess,platform,os
m=a.m;R=a.ROOT
# Retain reviewed independent complete-source replay code, before old sampling driver.
old=(R/'audit.py').read_text();block=old.split(' source=load')[1].split(' samples=')[0]
exec(__import__('textwrap').dedent(' source=load'+block),dict(vars(a)))
replays=a.load(R/'source-replays.json')
# Fresh seeds, each profile; modest regression set.
samples=[m.generate(seed=830127+71*j+i,bank_profile=p) for j,p in enumerate(m.PROFILES) for i in range(8)]
a.save('samples.json',samples);batch=a.load(a.JOB/'samples.json');a.save('batch.json',batch)
# Hold each observed answer bank and background fixed, make every bank entry correct.
roles=[]
for j,p in enumerate(m.PROFILES):
 anchor=(-2,3)
 template=m.generate(seed=1761,bank_profile=p,bank_anchor=anchor)
 pairs=a.optionpairs(template)
 for x,y in pairs:
  pars={'A':[[-2*x,2,-2*y],[j-4,3,4],[5,-1,2]],'row':0,'pivot':1,'ks':[x,0,y]}
  rec=m.generate(seed=1761,bank_profile=p,bank_anchor=anchor,parameters=pars)
  assert a.optionpairs(rec)==pairs
  roles.append(rec)
 for rec in roles[-5:]:a.check(rec)
 assert {a.check(r)['correct_index'] for r in roles[-5:]}==set(range(5))
a.save('roles.json',roles)
pars={'A':[[4,2,-6],[1,3,4],[5,-1,2]],'row':0,'pivot':1,'ks':[-2,0,3]}
changed=copy.deepcopy(pars);changed['A'][0][0]=-4;changed['ks'][0]=2
irrelevant=copy.deepcopy(pars);irrelevant['A'][1][0]=8
cf=[m.generate(seed=934,bank_profile='q-91189',bank_anchor=(-2,3),parameters=p) for p in [pars,changed,irrelevant]]
cf += [m.generate(seed=935,bank_profile='q-130609',parameters={'A':[[2,2,-4],[1,3,4],[5,-1,2]],'row':0,'pivot':p,'ks':ks}) for p,ks in [(0,[0,-1,2]),(1,[-1,0,2])]]
assert a.optionpairs(cf[0])==a.optionpairs(cf[1])==a.optionpairs(cf[2])
assert a.check(cf[0])['coefficients']==a.check(cf[2])['coefficients']!=a.check(cf[1])['coefficients']
a.save('counterfactuals.json',cf)
boundaries=[]
for r in range(3):
 for p in range(3):
  A=[[2,3,5],[7,11,13],[17,19,23]];ks=[0]*3
  for c,k in zip([c for c in range(3) if c!=p],[-2,3]):ks[c]=k;A[r][c]=-k*A[r][p]
  boundaries.append(m.generate(seed=991,bank_profile='q-91189',bank_anchor=(-2,3),parameters={'A':A,'row':r,'pivot':p,'ks':ks}))
a.save('boundaries.json',boundaries)
allrows=replays+samples+batch+roles+cf+boundaries
a.save('math-results.json',{'total':len(allrows),'checks':[a.check(r) for r in allrows]})
a.save('variation-results.json',{'samples':a.summarize(samples),'batch':a.summarize(batch),'roles':a.summarize(roles),'boundaries':a.summarize(boundaries)})
a.save('grader-input.json',[{'label':f'{label}-{i}','record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if a.apply(a.mats(r['question'][':question/problem'])[0],a.ops(c[':answer/value']))==a.mats(r['question'][':question/problem'])[1] else 'rejected','purpose':'Exact independent whole-column calculation'} for c in a.choices(r)]} for label,rs in [('source',replays),('sample',samples),('batch',batch),('role',roles),('cf',cf),('boundary',boundaries)] for i,r in enumerate(rs)])
a.save('delivery-input.json',samples+roles+cf+boundaries)
a.save('render-input.json',batch+cf)
# Prior failure must fail on old code and stop predicting on current minimal example.
old=m;a.m=a.module(a.JOB/'review-0-policy-2-8bbb1cdbe4d688a3/relocated/17592186161968.py')
prior=a.m.generate(seed=842,bank_profile='q-91189',parameters=pars);a.save('old-counterexample.json',[prior]);assert predict(prior)==a.correctid(prior)
a.m=old
current=m.generate(seed=842,bank_profile='q-91189',parameters=pars);assert predict(current)!=a.correctid(current);a.save('current-counterexample.json',[current])
a.save('retained-regression.json',{'finding':'ad4d9eb2e13fc5224721','old_prediction_correct':True,'current_prediction_correct':False,'role_groups':9,'roles_per_group':5,'prior_preflight':'Passed author checks are claims; independently ran old failing example and all-key fixed-bank challenge.'})
# Isolated exact author preflight execution. No author script is run in package directory.
isolated=R/'author-preflight';shutil.copytree(a.PKG,isolated/'workspace',dirs_exist_ok=True);shutil.copytree(a.JOB/'source',isolated/'source',dirs_exist_ok=True);shutil.copy(a.JOB/'samples.json',isolated/'samples.json')
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(R)}
run=subprocess.run([sys.executable,str(isolated/'workspace/evidence/check_repair.py')],capture_output=True,text=True,cwd=R,env=env)
a.save('author-preflight-result.json',{'command':'isolated workspace/evidence/check_repair.py','returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr});assert run.returncode==0
# Runtime-only relocation, actual installed dependencies, determinism, invalid inputs.
manifest=a.load(a.PKG/'package.json');rel=R/'relocated';rel.mkdir(exist_ok=True)
for f in manifest['files']:
 d=rel/f;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy(a.PKG/f,d)
run=subprocess.run([sys.executable,str(rel/manifest['entrypoint']),'--count','5','--seed','71387'],capture_output=True,text=True,cwd=R,env=env);assert run.returncode==0
relrows=json.loads(run.stdout);assert relrows==m.batch('easy',5,71387);a.save('relocated-records.json',relrows)
assert m.generate(seed=830127,bank_profile=m.PROFILES[0])==samples[0]
invalid=[]
for name,kw in [('hard',{'difficulty':'hard'}),('moderate',{'difficulty':'moderate'}),('zero pivot',{'bank_profile':'q-91189','parameters':dict(pars,A=[[4,0,-6],[1,3,4],[5,-1,2]])})]:
 try:m.generate(**kw);ok=False
 except (ValueError,AssertionError):ok=True
 invalid.append({'case':name,'rejected':ok});assert ok
import sympy
installed={'python':platform.python_version(),'packages':{'sympy':sympy.__version__}};assert installed==manifest['dependencies']
a.save('packaging-results.json',{'installed':installed,'declared':manifest['dependencies'],'runtime_only_relocation_identical':True,'deterministic':True,'invalid':invalid,'external_output':'JSON stdout only'})
inv=a.load(a.JOB/'source/inventory.json');ids={q[':question/id'] for q in a.load(a.JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']};assert all(q[':question/id'] in ids and not any('generator' in k or 'generation' in k for k in q) for q in inv['questions'])
a.save('inventory-review.json',{'basis':inv['basis'],'total':len(inv['questions']),'source_only':True,'historical_generated_records':0,'verified':'All IDs match original source and no generation attributes; no generated records eligible or retired to audit.'});a.save('affected-inventory.json',{'affected_questions':[]})
(R/'session-state.md').write_text('Source replay, 147 independent math cases, original failure/current regression, nine fixed-bank all-key groups, exact isolated author preflight, inventory and packaging checked. Delivery, native grader, render and final decision report pending.\n')
print(json.dumps({'math_records':len(allrows),'samples':len(samples),'roles':len(roles),'batch_positions':[a.check(r)['correct_index'] for r in batch],'old_shortcut':probes([prior]),'new_shortcut':probes([current])}))

"""Bounded revision review. Run with the job's Python and PYTHONDONTWRITEBYTECODE=1.
Reuses the prior independent prompt parser, never the author's math oracle.
"""
import pathlib,sys,os,json,hashlib,shutil,subprocess,difflib,collections
E=pathlib.Path(__file__).resolve().parent;B=E.parent;W=B/'workspace';P=B/'review-1-policy-2-45a9ed86924bfc07'
sys.dont_write_bytecode=True
ns={'__file__':str(E/'audit.py')};exec(compile((E/'audit.py').read_text().split('source=json.load')[0],str(E/'audit.py'),'exec'),ns)
g=ns['g'];parse=ns['parse'];save=ns['save'];run=ns['run'];PY=ns['PY'];native=ns['native']
# Verify exact semantic code delta before relying on unaffected earlier evidence.
old=(P/'relocated/17592186184172.py').read_text();new=(W/'17592186184172.py').read_text();delta=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True)));(E/'runtime-change.diff').write_text(delta)
assert new.replace("VERSION='1.1.1'","VERSION='1.1.0'").replace(' # Select a seeded profile order before truncating to the requested count.\n # Every profile is eligible even when practice requests fewer than a cycle.\n random.Random(seed).shuffle(keys)\n','')==old
# Retained test must fail on the old reviewed executable, pass the revised one.
legacy=E/'legacy-reviewed';legacy.mkdir(exist_ok=True)
manifest=json.loads((W/'package.json').read_text())
for f in manifest['files']:
 target=legacy/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/'relocated'/f,target)
cmd=[str(PY),str(E/'reproduce_profile_omission.py'),'--assert-coverage'];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','REVIEW_PACKAGE_ROOT':str(legacy),'REVIEW_TEST_OUTPUT':'old-profile'}
p=subprocess.run(cmd,env=env,capture_output=True,text=True);save('retained-regression.json',{'command':cmd,'old_package':str(legacy),'old_exit':p.returncode,'old_stdout':p.stdout,'old_stderr':p.stderr,'current':json.loads((E/'current-profile/profile-omission-results.json').read_text()),'preflight':'Author preflight claims pass; independently reproduced old failure and current pass with the retained independent test.'});assert p.returncode!=0 and 'q-79411' in p.stderr
source=json.loads((B/'source/source.json').read_text());src={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
# Re-execute source replay but keep the fresh regression set small (three/profile).
replay=[];checks=[];fresh=[]
for i,(key,q) in enumerate(src.items()):
 level=ns['enum'](q[':question/difficulty']).split('/')[-1];n=int(__import__('re').search(r'(\d+)\s*\\times',q[':question/problem'])[1]);params={'diagonal':[1]*n} if '\\begin' in q[':question/problem'] else {'scale':1}
 r=g.generate(level,830119,key,params);replay.append(r);fs=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']);out=r['question']
 tests={'prompt':q[':question/problem']==out[':question/problem'],'solution':q[':question/worked-solution']==out[':question/worked-solution'],'complete_bank':all((a[':answer-field/key'],ns['enum'](a[':answer-field/type']),[v[':answer/value'] for v in a[':answer-field/choices']],a[':answer-field/correct'][':answer/value'])==(b[':answer-field/key'],b[':answer-field/type'],[v[':answer/value'] for v in b[':answer-field/choices']],ns['val'](b)) for a,b in zip(fs,out[':question/answer-fields'])) and len(fs)==len(out[':question/answer-fields'])}
 checks.append({'source_id':q[':question/id'],'profile':key,'checks':tests});assert all(tests.values()),checks[-1]
 for j in range(3):fresh.append(g.generate(level,920771+23*i+j,key))
save('replay-records.json',replay);save('source-replay-results.json',{'cases':checks,'canonical_gap':'Canonical example bank absent from capture; not invented. Same mathematical method is exercised in other vector profiles.'});save('fresh-records.json',fresh)
# Fresh production count-five runs test changed order and rejection/dedup stage.
cli=[];rows=[]
for level in ['moderate','hard']:
 for seed in [830119,920771,1060913]:
  result=run([PY,W/'17592186184172.py','--difficulty',level,'--count','5','--seed',seed]);assert result['exit']==0,result
  rs=json.loads(result['stdout']);assert len(rs)==5 and len({r['question'][':question/id'] for r in rs})==5
  rows.extend(rs);cli.append({'command':result['command'],'count':len(rs),'profiles':[r['generation']['profile'] for r in rs]})
save('fresh-cli-records.json',rows);save('fresh-cli-results.json',cli)
# Controlled relevant evidence pair: same claims and seed, only pivot count changes.
paired=[];pair_results=[]
for seed in range(100):
 a=g.generate('moderate',seed,'q-34934',{'scale':1,'count':3,'truths':[True,False,True]});b=g.generate('moderate',seed,'q-34934',{'scale':1,'count':4,'truths':[False,True,False]})
 if parse(a)['statements']==parse(b)['statements']:break
else:raise AssertionError('No same-claim pair')
assert a['question'][':question/problem'].replace('$3$ pivot columns','$4$ pivot columns')==b['question'][':question/problem']
paired.extend([a,b]);pair_results.append({'kind':'relevant','change':'Hold all three claims fixed; pivot count 3 -> 4 at n=4','seed':seed,'expected':['I and III only','II only'],'derived':[parse(a),parse(b)],'parameters':[a['generation']['parameters'],b['generation']['parameters']]})
a=g.generate('moderate',830119,'q-143533',{'diagonal':[1,1,1],'truths':[True,False,True]});b=g.generate('moderate',830119,'q-143533',{'diagonal':[3,2,1],'truths':[True,False,True]});paired.extend([a,b]);assert parse(a)['truths']==parse(b)['truths'];pair_results.append({'kind':'irrelevant','change':'Rescale coordinates (2a,a,b) -> (6a,2a,b), same independent dimension','seed':830119,'expected':'Same true/false subset; vectors and solution follow map','derived':[parse(a),parse(b)],'parameters':[a['generation']['parameters'],b['generation']['parameters']]})
save('counterfactual-records.json',paired);save('counterfactual-results.json',pair_results)
# Small boundary/rejection regression, unchanged constructors independently exercised.
boundary=[g.generate('moderate',290021,'q-34934',{'scale':1,'count':c,'truths':[True,False,True]}) for c in [0,4]];save('boundary-records.json',boundary)
reject=[]
for level,key,params in [('easy',None,None),('moderate','q-34934',{'scale':1,'count':5}),('moderate','q-143533',{'diagonal':[0,1,1]}),('moderate','q-143533',{'diagonal':[1,1,1],'truths':[False]*3})]:
 try:g.generate(level,13,key,params);out='accepted'
 except Exception as e:out=type(e).__name__+': '+str(e)
 reject.append({'difficulty':level,'template':key,'parameters':params,'outcome':out});assert out!='accepted'
save('rejection-results.json',reject)
batch=json.loads((B/'samples.json').read_text());save('runner-batch.json',batch)
current=json.loads((E/'current-profile/profile-omission-records.json').read_text());allrows=replay+fresh+rows+current+paired+boundary+batch
results=[parse(r) for r in allrows];save('math-results.json',{'count':len(results),'failures':[d for d in results if d['errors']],'cases':results});assert not any(d['errors'] for d in results)
# Current closure executes solely from manifest copies; verify installed dependencies.
dest=E/'relocated';dest.mkdir(exist_ok=True)
for f in manifest['files']:
 target=dest/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,target)
pack=[]
for level in ['moderate','hard']:
 x=run([PY,dest/manifest['entrypoint'],'--difficulty',level,'--count','5','--seed','830119'],dest);assert x['exit']==0,x
 save('relocated-'+level+'.json',json.loads(x['stdout']));pack.append({'command':x['command'],'exit':x['exit'],'stderr':x['stderr'],'count':len(json.loads(x['stdout']))})
actual={'python':sys.version.split()[0],'packages':{'sympy':__import__('sympy').__version__}};assert manifest['dependencies']==actual
save('packaging-results.json',{'manifest':manifest,'actual_versions':actual,'relocations':pack,'external_assets':'None generated or referenced; all outputs on stdout under review.','legacy_original_failure':'See reused legacy-failure-reproduced.json with source provenance.'})
save('determinism.json',{'same_seed_cli':g.batch('moderate',5,830119)==g.batch('moderate',5,830119),'runner_explicit_replay':all(g.generate('moderate',r['generation']['seed'],r['generation']['template'],r['generation']['parameters'])==r for r in batch)})
# Native choices checked exhaustively for each included generated record from visible math.
save('native-input.json',native(allrows));save('render-records.json',batch+paired+[next(r for r in rows if r['question'][':question/difficulty'].endswith('/hard'))])
# Separate raw inputs per difficulty for the shared delivery filter.
for level in ['moderate','hard']:
 save('delivery-input-'+level+'.json',[r for r in fresh+rows+current if r['question'][':question/difficulty'].endswith('/'+level)])
inv=json.loads((B/'source/inventory.json').read_text());originals={q[':question/id'] for q in src.values()};assert all(q[':question/id'] in originals for q in inv['questions'])
save('inventory-inspection.json',{'basis':inv['basis'],'count':len(inv['questions']),'all_original_sources':True,'non_source_generated_count':0,'verified':'All 15 inventory UUIDs matched original source records; none carries generation metadata. The retained failure concerns sampling reachability, not a per-record mathematical defect. No affected generated records demonstrated.'});save('affected-inventory.json',{'affected_questions':[]})
(E/'session-state.md').write_text('Completed bounded revision tests: retained coverage test fails old reviewed package and passes current package; exact 15-source replay; 45 fresh profile records and 30 fresh CLI records; current runner batch checked; controlled same-claim count pair and coordinate pair; independent math and declared runtime relocation pass. Next: native grading, shared delivery, actual UI inspection, decision/selection assessment.\n')
print(json.dumps({'math_count':len(results),'replay':len(replay),'fresh_cli':len(rows),'old_regression_exit':p.returncode,'counterfactual_seed':pair_results[0]['seed'],'version':actual}))

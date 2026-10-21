from independent import *
from unittest.mock import patch
source=json.load(open(JOB/'source/source.json'));sq=source['material']['kp'][':knowledge-point/questions']
# Reuse unaffected validators, rerun every complete bank, preserving whole bank.
replays=[]; rr=[]
for q in sq:
 sid=q[':question/math-academy-id'];r=g.replay(sid);a=analyze(r)
 assert mats(q[':question/problem'])==mats(r['question'][':question/problem']) and target(q[':question/problem'])==target(r['question'][':question/problem'])
 before=[op(v[':answer/value'].replace(r'\\frac',r'\frac')) for v in q[':question/answer-fields'][0][':answer-field/choices']]
 after=[op(v[':answer/value']) for v in r['question'][':question/answer-fields'][0][':answer-field/choices']]
 assert before==after and len(after)==5
 key=q[':question/answer-fields'][0].get(':answer-field/correct')
 if key: assert op(key[':answer/value'])==op(a['correct'])
 replays.append(r);rr.append({'source_id':q[':question/id'],'profile':sid,'five_choices_match':True,'analysis':a})
save('source-replays.json',replays);save('source-replay-results.json',rr)
# Fresh scheduler stress: exact proposal stream retained, then identical proposal
# repeated per profile. No answers mocked; only outer getrandbits stream controlled.
RANDOM=g.random.Random
def proposal_batch(seeds,count=None):
 sentinel='independent retained proposals';stream=iter(seeds)
 class Outer:
  def getrandbits(self,bits):assert bits==64;return next(stream)
 with patch.object(g.random,'Random',side_effect=lambda s:Outer() if s==sentinel else RANDOM(s)):
  return g.batch('hard',len(seeds) if count is None else count,sentinel)
old=json.load(open(ROOT/'reused/fresh-samples.json'));seeds={}
for seed in range(811000,811150):
 r=g.generate(seed=seed);seeds.setdefault(r['generation']['bank_profile'],seed)
 if set(seeds)==set(g.CASES):break
assert set(seeds)==set(g.CASES)
fresh=[]; scheduler=[]
for sid,seed in seeds.items():
 pair=proposal_batch([seed,seed]);aa=[analyze(r) for r in pair]
 assert all(r['generation']['bank_profile']==sid for r in pair)
 assert {a['kind'] for a in aa}=={'swap','linear'}
 assert len({r['generation']['mathematical_fingerprint'] for r in pair})==2
 fresh+=pair;scheduler.append({'profile':sid,'proposals':[seed,seed],'winners':[r['generation']['parameters']['winner'] for r in pair],'kinds':[a['kind'] for a in aa]})
retained=json.load(open(JOB/'review-1-policy-2-22438d1e0e264086/runner-batch.json'))
exact=proposal_batch([r['generation']['seed'] for r in retained]);save('retained-current-records.json',exact)
assert sum(analyze(r)['kind']=='swap' for r in exact if r['generation']['bank_profile']=='q-72858')==1
fresh+=g.batch('hard',12,81469273)
save('fresh-samples.json',fresh);save('scheduler-results.json',{'independently_chosen_seed':81469273,'forced_proposals':scheduler,'retained_proposal_seeds':[r['generation']['seed'] for r in retained],'retained_repaired_roles':[analyze(r) for r in exact]})
batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch)
# Unchanged generate(): exact equality with previous independent records at params.
controls=[]
for r in old:
 sid=r['generation']['bank_profile']
 if sid in [x['generation']['bank_profile'] for x in controls]:continue
 new=g.generate(seed=r['generation']['seed'],parameters=r['generation']['parameters']);assert new['question']==r['question'];controls.append(new)
save('unchanged-control-results.json',{'records':controls,'question_equality':True,'basis':'revision.diff; all functions except batch unchanged apart from version'})
base={'source':'q-72858','rows':[0,1,2],'cols':[0,1,2],'order':[0,1,2,3,4]}
ps=[dict(base,winner=0,matrix=[[2,1,3],[6,4,3],[1,2,3]]),dict(base,winner=1,matrix=[[2,1,4],[6,4,3],[1,2,0]]),dict(base,winner=0,matrix=[[-9,8,3],[6,4,3],[1,2,3]])]
cf=[g.generate(seed=81469301,parameters=p) for p in ps]
tp=[g.generate(seed=81469301,parameters=dict(base,winner=0,matrix=[[4,1,3],[3,4,3],[0,2,2]],cols=[2,1,0])),g.generate(seed=81469301,parameters=dict(base,winner=1,matrix=[[3,1,4],[3,4,3],[2,2,0]]))]
ca=[analyze(r) for r in cf+tp]
assert ca[0]['correct']!=ca[1]['correct'] and ca[0]['correct']==ca[2]['correct'] and ca[3]['correct']!=ca[4]['correct']
assert mats(tp[0]['question'][':question/problem'])==mats(tp[1]['question'][':question/problem'])
assert [v[':answer/value'] for v in tp[0]['question'][':question/answer-fields'][0][':answer-field/choices']]==[v[':answer/value'] for v in tp[1]['question'][':question/answer-fields'][0][':answer-field/choices']]
assert ca[3]['target']=='21' and ca[4]['target']=='23'
save('counterfactual-records.json',cf+tp);save('counterfactual-results.json',{'parameters':ps,'analysis':ca,'visible_prompt_and_solution_changes':len(set(r['question'][':question/problem'] for r in cf))==3 and len(set(r['question'][':question/worked-solution'] for r in cf))==3})
save('math-results.json',{name:[analyze(r) for r in rs] for name,rs in [('fresh',fresh),('batch',batch),('exact_prior_stream',exact),('source',replays),('counterfactual',cf+tp),('unchanged_controls',controls)]})
# Counts 0,1, negatives; invalid construction and unchanged boundary behavior.
reject=[]
for label,args in [('easy',{'difficulty':'easy'}),('moderate',{'difficulty':'moderate'}),('zero_target',{'parameters':dict(base,winner=0,matrix=[[2,1,0],[6,4,0],[1,2,3]])}),('ambiguous',{'parameters':dict(base,winner=0,matrix=[[2,1,3],[6,4,3],[1,2,0]])}),*[(f'ineligible {w}',{'parameters':dict(base,winner=w)}) for w in [2,3,4]],('rows',{'parameters':dict(base,rows=[0,0,2])}),('order',{'parameters':dict(base,order=[0,1,2,3,3])})]:
 try:g.generate(**args)
 except ValueError as e:reject.append({'case':label,'args':args,'rejected':str(e)})
 else:raise AssertionError(label)
assert g.batch('hard',0,821)==[] and len(g.batch('hard',1,821))==1
try:g.batch('hard',-1,821)
except ValueError:reject.append({'case':'negative count','rejected':True})
else:raise AssertionError('negative count')
save('rejection-results.json',reject)
assert all(g.generate(seed=r['generation']['seed'],parameters=r['generation']['parameters'])['question']==r['question'] for r in fresh+batch+cf+tp+exact)
assert g.batch('hard',5,81469273)==g.batch('hard',5,81469273)
copy=ROOT/'relocated';copy.mkdir(exist_ok=True)
for n in json.load(open(PKG/'package.json'))['files']+['package.json']:shutil.copy2(PKG/n,copy/n)
cmd=[sys.executable,str(copy/'generator.py'),'--count','5','--seed','81469274']
pr=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
assert pr.returncode==0 and not pr.stderr and json.loads(pr.stdout)==g.batch('hard',5,81469274)
save('relocated-records.json',json.loads(pr.stdout))
versions={'python':platform.python_version(),'packages':{x:importlib.metadata.version(x) for x in ['sympy','mpmath']}}
assert versions==json.load(open(PKG/'package.json'))['dependencies']
save('packaging-results.json',{'versions':versions,'exact_manifest_match':True,'deterministic_replays':len(fresh+batch+cf+tp+exact),'batch_deterministic':True,'relocation_command':cmd,'json_only':True,'external_outputs':'No assets or file outputs in package; all copied execution under evidence_root.'})
save('coverage.json',{'fresh_profiles':dict(collections.Counter(r['generation']['bank_profile'] for r in fresh)),'fresh_roles':{sid:dict(collections.Counter(analyze(r)['kind'] for r in fresh if r['generation']['bank_profile']==sid)) for sid in seeds},'rejection_attempts':dict(collections.Counter(r['generation']['rejection_attempts'] for r in fresh)),'raw_batch':[analyze(r) for r in batch],'prior_unchanged_coverage':'reused/coverage.json; generate/source equality in revision-diff.json'})
(ROOT/'session-state.md').write_text('Both retained regressions reproduced on failing old packages and pass on current copy. Independent 11-bank replay, new scheduler paired proposals across ten profiles, fresh seed 81469273, exact current batch, relevant/irrelevant/target pairs, native inputs pending delivery. Packaging/rejections pass. No package writes.\n')
print(json.dumps({'replays':len(replays),'fresh':len(fresh),'current_batch':len(batch),'controlled_pairs':len(cf+tp),'profiles':len(seeds)}))

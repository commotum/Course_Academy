"""Delivery, cue probes, inventory inspection and packaging; no services or DB writes."""
import hashlib,importlib.util,json,os,platform,shutil,subprocess,sys,tempfile
from pathlib import Path
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;W=E.parent;sys.path.insert(0,str(W))
# Reuse only the independent reading helpers, without executing regressions again.
helpers=(W/'regressions.py').read_text().split('# Exact retained counterexample')[0]
ns={ '__file__':str(W/'regressions.py')};exec(helpers,ns)
g=ns['g'];expected=ns['expected'];answer=ns['answer'];vectors=ns['vectors'];numeric_rank=ns['numeric_rank'];check=ns['check'];sp=ns['sp']
def save(n,d):(E/n).write_text(json.dumps(d,indent=2,default=str)+'\n')
def probes(rs):
 groups=defaultdict(list)
 for r in rs:groups[r['generation']['template']].append(r)
 result={}
 for sid,rs in groups.items():
  tests=Counter();ranks=Counter();positions=Counter();answers=[]
  for r in rs:
   q=r['question'];f=q[':question/answer-fields'][0];opts=f[':answer-field/choices'];a=answer(q);correct=a[':answer/id'];A,b=vectors(q);nums=[o for o in opts if o[':answer/type']==':answer.type/math'];rank=numeric_rank(q);ranks[rank]+=1;positions[next(i+1 for i,o in enumerate(opts) if o[':answer/id']==correct)]+=1
   answers.append(a[':answer/value'])
   for i,o in enumerate(opts):tests['position-'+str(i+1)]+=o[':answer/id']==correct
   ordered=sorted(nums,key=lambda o:sp.Rational(o[':answer/value']))
   for i,o in enumerate(ordered):tests['numeric-rank-'+str(i+1)]+=o[':answer/id']==correct
   for name,key in [('least-absolute',lambda o:abs(sp.Rational(o[':answer/value']))),('greatest-absolute',lambda o:-abs(sp.Rational(o[':answer/value'])))]+[(name,lambda o,t=t:abs(sp.Rational(o[':answer/value'])-t)) for name,t in [('closest-b1',b[0]),('closest-b2',b[1]),('closest-b3',b[2]),('closest-b-sum',sum(b))]]:
    vals=[key(o) for o in nums];best=min(vals);winners=[o for o,v in zip(nums,vals) if v==best]
    # Count tied correct choices as successes: conservative upper bound on cue utility.
    tests[name]+=any(o[':answer/id']==correct for o in winners)
  result[sid]={'n':len(rs),'ranks':dict(ranks),'positions':dict(positions),'semantic_instances':len({r['question'][':question/problem'] for r in rs}),'cue_successes':dict(tests),'max_cue_success':max(tests.values()),'answers':answers}
 return result
fresh=json.loads((E/'fresh-moderate.json').read_text());accepted=json.loads((E/'delivery-fresh/accepted.json').read_text());batch=json.loads((E/'batch.json').read_text());delivered_batch=json.loads((E/'delivery-batch/accepted.json').read_text())
before=probes(fresh);after=probes(accepted)
assert before==after and all(v['max_cue_success']<v['n'] for v in after.values())
for i,r in enumerate(delivered_batch):check(r,'delivered-batch-'+str(i))
old=json.loads((W.parent/'samples.json').read_text());old_ranks={r['generation']['template']:numeric_rank(r['question']) for r in old}
old_strategy=sum(numeric_rank(r['question'])==old_ranks.get(r['generation']['template']) for r in delivered_batch)
# No per-template conclusion is possible from singleton groups in five records.
save('pedagogical-variation.json',{'before_delivery':before,'after_delivery':after,'delivery_identical':True,'batch':probes(delivered_batch),'old_template_rank_rule':{'successes':old_strategy,'attempts':len(delivered_batch),'unknown_templates':sum(r['generation']['template'] not in old_ranks for r in delivered_batch)},'controlled_rank_cases':'controlled-bank-records.json','counterfactuals':'counterfactual-records.json','limits':['Five-record batch has one record per matrix; use the 64-record conditional audit for within-template claims.','Cue tests are bounded probes, not a proof against all possible strategies.','Moderate has unique solutions; hard intentionally preserves source-only contradictory-system cases.']})
# Read-only selection model: rated moderate candidates are uniformly selected within band.
pool=sorted(accepted,key=lambda r:r['question'][':question/id']);selected=[]
for i in range(64):
 digest=hashlib.sha256(f'course-academy/question-selection/v1/author-repair-{i}'.encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);selected.append(pool[int(u*len(pool))])
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs select: positive moderate band, unique candidate IDs sorted, SHA256 second uniform chooses within band. This uses question UUID lexical order as a local surrogate for unavailable DB entity IDs.','candidate_count':len(pool),'draws':len(selected),'selected_rank_counts':dict(Counter(numeric_rank(r['question']) for r in selected)),'limits':['No generated DB entity IDs, learner history or policy snapshot are available. Actual learner reservation/selection is not executed.','Freshness may remove any previously seen item; no guarantee of rank variation in arbitrary small history-conditioned subsets.','Band weighting does not directly inspect option ranks or positions.']})
inv=json.loads((W.parent/'source/inventory.json').read_text());src=json.loads((W.parent/'source/source.json').read_text())['material']['kp'];source_ids={q[':question/id'] for q in src[':knowledge-point/questions']};others=[q for q in inv['questions'] if q[':question/id'] not in source_ids]
assert not others
(W/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
save('inventory-audit.json',{'basis':inv['basis'],'questions':len(inv['questions']),'original_source_id_matches':len(inv['questions']),'stored_generated_instances':0,'conclusion':'Verified absence of stored generated instances in the supplied capture: every question ID is an original supplied practice source ID with MA provenance; do not relabel originals as generated. No claim about live inventory.'})
# Runtime package relocation and declared dependency/version checks.
manifest=json.loads((W/'package.json').read_text());assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':sp.__version__}}
hashes=lambda:{f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in manifest['files']}
before_hashes=hashes();target=E/'relocated';target.mkdir(exist_ok=True)
for f in manifest['files']+['package.json']:
 dst=target/f;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,dst)
cmd=[sys.executable,str(target/manifest['entrypoint']),'--difficulty','moderate','--count','5','--seed','3719145341','--format','json']
p=subprocess.run(cmd,cwd=target,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True);assert p.returncode==0,p.stderr
rel=json.loads(p.stdout);assert rel==batch
assert g.batch('moderate',5,3719145341)==batch
profile_selection={str(seed):[r['generation']['template'] for r in g.batch('moderate',5,seed)] for seed in range(5)}
assert len({sid for group in profile_selection.values() for sid in group})==8
save('batch-profile-selection.json',profile_selection)
invalid=[]
for call in [lambda:g.generate('easy',1),lambda:g.batch('moderate',0,1),lambda:g.generate('moderate',1,'q-34566'),lambda:g.generate('hard',1,'q-74011',{'b':[1,-1,0]}),lambda:g.generate('moderate',1,'q-34243',{'b':[2,3,1],'numeric_rank':0})]:
 try:call()
 except (ValueError,AssertionError):invalid.append(True)
 else:raise AssertionError('Invalid request accepted')
assert hashes()==before_hashes
save('packaging.json',{'manifest_files':manifest['files'],'runtime_hashes':before_hashes,'python':platform.python_version(),'sympy':sp.__version__,'relocation_command':cmd,'relocation_exit':p.returncode,'relocated_batch_matches':True,'deterministic':True,'invalid_requests_rejected':len(invalid),'runtime_unchanged_by_checks':True})
# Render affected families, signed target and inconsistency with actual UI.
source_record=lambda sid:next(c['record'] for c in json.loads((E/'grader-input.json').read_text()) if c['record']['generation']['template']==sid and c['label'].split('-')[0] not in ['0','1'])
render=[next(r for r in fresh if r['generation']['template']=='q-34243'),next(r for r in fresh if r['generation']['template']=='q-74028'),source_record('q-74043'),source_record('q-74011')]
save('render-input.json',render)
# Native check the regenerated exact batch separately from the larger regression sample.
save('batch-grader-input.json',[{'label':'delivered-batch-'+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==expected(r['question']) else 'rejected','purpose':'Every option after actual delivery filtering'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]} for i,r in enumerate(delivered_batch)])
save('batch-math-results.json',{'checks':ns['rows']})
print(json.dumps({'delivered_fresh':len(accepted),'delivered_batch':len(delivered_batch),'old_rank_strategy_successes':old_strategy,'conditional_max_cue_success':{s:v['max_cue_success'] for s,v in after.items()},'relocation':'passed','render_records':len(render)}))

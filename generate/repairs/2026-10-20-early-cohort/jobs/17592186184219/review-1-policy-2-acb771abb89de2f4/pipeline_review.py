import json,sys,collections,hashlib,pathlib,subprocess
sys.dont_write_bytecode=True
from review_generator import *
rules={(x['target'],tuple(x['sorted_adjacent_gaps'])):x['choose_sorted_rank_1_based']-1 for x in json.loads((E/'shortcut-rules.json').read_text())}
def load(f):return json.loads((E/f).read_text())
def probe(rs):
 groups=collections.defaultdict(lambda:collections.Counter());roles=collections.Counter();shapes=collections.Counter();success=collections.Counter();rows=[]
 for r in rs:
  d=independent(r);v=sorted(d['values']);role=v.index(d['c']);sig=signature(r);old=v[rules[sig]] if sig in rules else None
  strategies={'old_target_gap_lookup':old==d['c'],'choose_second_largest':v[-2]==d['c'],'choose_largest':v[-1]==d['c'],'choose_smallest':v[0]==d['c'],'choose_first_stored':d['values'][0]==d['c']}
  for name,hit in strategies.items():success[name]+=hit
  groups[str(sig)]['total']+=1;groups[str(sig)]['old_hits']+=old==d['c'];groups[str(sig)]['role_'+str(role)]+=1
  roles[d['target']]+=1;shapes['square' if d['m']==d['n'] else 'tall' if d['m']>d['n'] else 'wide']+=1
  rows.append({'id':r['question'][':question/id'],'profile':r['generation']['profile'],'signature':str(sig),'correct_sorted_role':role,'old_prediction':old,'answer':d['c'],'all_offered_values_feasible':all(0<=(v if d['target']=='rank' else d['n']-v)<=min(d['m'],d['n']) for v in d['values'])})
 return {'total':len(rs),'successes':dict(success),'baseline':.2,'conditional':dict(groups),'targets':dict(roles),'shapes':dict(shapes),'rows':rows}
raw=load('independent-samples.json');rawbatch=load('runner-batch.json');control=load('delivery-control/accepted.json');batch=load('delivery-batch/accepted.json');cf=load('counterfactuals.json');cfd=load('delivery-counterfactual/accepted.json')
results={key:probe(rs) for key,rs in [('raw_control',raw),('delivered_control',control),('raw_batch',rawbatch),('delivered_batch',batch),('delivered_counterfactual',cfd)]};save('delivery-shortcut-results.json',results)
# Native learner-grader: every authored choice, including changed roles and publication IDs.
cases=[]
for group,rs in [('source',load('source-replay-records.json')),('raw-counterfactual',[x['record'] for x in cf]),('delivered-counterfactual',cfd),('raw-batch',rawbatch),('delivered-batch',batch),('fresh',raw[:8]),('old-consecutive-counterexample',load('prior-counterexamples.json')['consecutive_rank_records']),('old-seed-829013',[load('prior-counterexamples.json')['seed_829013']])]:
 for i,r in enumerate(rs):
  d=independent(r);checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if int(a[':answer/value'])==d['n']-d['k'] else 'rejected','purpose':'independent visible n minus given; complete five-choice bank'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  cases.append({'label':group+'/'+(cf[i]['label'] if group=='raw-counterfactual' else str(i)),'record':r,'checks':checks})
save('grader-input.json',cases)
# Render the exact batch, all counterfactuals (all profiles/roles), and canonical numerical parameters.
render_records=rawbatch+[x['record'] for x in cf]+[load('canonical-example.json')['record']]
save('render-records.json',render_records)
inv=json.loads((JOB/'source/inventory.json').read_text());source=json.loads((JOB/'source/source.json').read_text());source_ids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
ivs=[]
for q in inv['questions']:
 ivs.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in source_ids,'generation_keys':[k for k in q if 'generat' in k]})
assert all(x['original_source'] and not x['generation_keys'] for x in ivs)
save('inventory-audit.json',{'basis':inv['basis'],'questions':ivs,'verified_generated_count':0,'result':'All 14 captured questions are original source records. No stored generated instances exist in captured inventory, so no affected generated records can be demonstrated. Live changing inventory unexamined.'});save('affected-inventory.json',{'affected_questions':[]})
# Faithful all-easy conditional reproduction of select(); unknown live learner/history is explicit.
ids={x[':db/id']:x[':question/id'] for x in inv['questions']};base=max(ids)+1000
for i,r in enumerate(batch):ids[base+i]=r['question'][':question/id']
scenarios=[]
for label,excluded in [('all-fresh',set()),('sources-seen',{q[':db/id'] for q in inv['questions']}),('batch-first-two-seen',{base,base+1})]:
 pool=sorted(set(ids)-excluded);draws=[]
 for i in range(64):
  seed=f'independent-revision-review/{i}';h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53);qid=pool[int(u*len(pool))];draws.append({'seed':seed,'entity_id':qid,'question_id':ids[qid]})
 count=collections.Counter(x['question_id'] for x in draws); selected=[r for r in batch if r['question'][':question/id'] in count]
 scenarios.append({'case':label,'excluded':sorted(excluded),'eligible_count':len(pool),'draws':draws,'batch_selection_counts':{r['question'][':question/id']:count[r['question'][':question/id']] for r in batch},'selected_unique_batch_coverage':probe(selected),'no_policy_fallback':ids[pool[0]],'zero_easy_weight':None})
save('learner-selection.json',{'implementation':'question_selection.rs select: sorted unique candidates; no-policy first; positive easy band SHA256 bytes8..16 >>11 within-band uniform; zero easy with no unrated => None. seen_before_task/current prefix exclude before selection.','implementation_sha256':sha(REPO/'engine/rust/question_selection.rs'),'assumptions':'Captured sources and batch all easy. Generated entity IDs hypothetical; actual future IDs/learner policy/history unavailable. 64 deterministic seeds illustrate conditional selection, not predicted real learner draws.','scenarios':scenarios,'limits':['No publication/preparation.json exists. Shared read-only delivery uses captured inventory basis 5446.','Selection can remove unseen cases for a particular learner; no per-task role balance guarantee exists. Positive-easy selection does not use target, profile or answer role. No-policy lowest ID and zero-easy exclusion tested explicitly.','History scenarios are illustrative; no actual learner state is supplied.']})
# Retained independent regressions copied unchanged except stale docstring.
s=(JOB/'review-0-policy-2-f24f201976da522d/regression_tests.py').read_text().replace('Current package must fail both.','Both must pass on a repaired package.')
(E/'regression_tests.py').write_text(s)
cmd=[str(PY),'-B',str(E/'regression_tests.py')];cp=subprocess.run(cmd,cwd=E,capture_output=True,text=True);(E/'independent-regressions.txt').write_text(cp.stdout+cp.stderr);assert cp.returncode==0
save('commands.json',{'independent':f'{PY} -B {E}/review_generator.py','pipeline':f'{PY} -B {E}/pipeline_review.py','regressions':cmd,'delivery':[f'{PY} -B {REPO}/generate/pipeline/check_delivery.py --input {i} --source {JOB}/source/source.json --inventory {JOB}/source/inventory.json --difficulty easy --output {o} --asset-root {E} --math-root /media/jake/SSD/EDB/math' for i,o in [('independent-samples.json','delivery-control'),('runner-batch.json','delivery-batch'),('counterfactual-records.json','delivery-counterfactual')]],'grader':f'{REPO}/generate/runs/current/check-engine {E}/grader-input.json {E}/grader-report.json','renderer':f'{PY} -B {REPO}/generate/pipeline/render_preview.py --input {E}/render-records.json --output {E}/render --asset-root {E} --math-root /media/jake/SSD/EDB/math'})
(E/'session-state.md').write_text('Shared delivery complete: control 170 ->166 (4 duplicates), batch 5 ->5, controlled records 80 ->78 (2 duplicate target/base cases). Inventory verified 14 originals and 0 generated. Independent retained regressions pass. Grader and UI inputs ready.\n')
print(json.dumps({k:{'total':v['total'],'successes':v['successes'],'targets':v['targets'],'shapes':v['shapes']} for k,v in results.items()}))

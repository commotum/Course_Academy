import sys,os,json,hashlib,shutil,subprocess,collections,re
from pathlib import Path
sys.dont_write_bytecode=True
import review as R
E=R.ROOT;g=R.g
load=lambda p:json.load(open(E/p))
records=load('domain-records.json');easy=load('easy-records.json');batch=load('batch-records.json');accepted=load('delivery-domain/accepted.json');accepted_batch=load('delivery-batch/accepted.json')
# This table is learned at scale=1, tested against distinct RHS scales.
train=[r for r in records if r['generation']['parameters']['rhs_scale']==1]
lookup={R.profile(r):r['question'][':question/answer-fields'][0][':answer-field/choices'][R.correct_index(r)][':answer/value']=='No solution' for r in train}
def strategy(r):
 a=R.equations(r['question']);f=r['question'][':question/answer-fields'][0]
 if lookup[R.profile(r)]:return next(c[':answer/id'] for c in f[':answer-field/choices'] if c[':answer/value']=='No solution')
 # On predicted consistent templates ignore the entire second equation. Only
 # solve first row to distinguish the four vector families.
 candidates=[]
 for c in f[':answer-field/choices']:
  if c[':answer/value']=='No solution':continue
  vv=R.mats(c[':answer/value'])[1]
  if R.S.simplify((a[0,:2]*vv)[0]-a[0,2])==0:candidates.append(c[':answer/id'])
 assert len(candidates)==1
 return candidates[0]
def measure(rs):
 successes=sum(strategy(r)==r['question'][':question/answer-fields'][0][':answer-field/choices'][R.correct_index(r)][':answer/id'] for r in rs)
 return {'correct':successes,'total':len(rs),'baseline':.2,'solution_types':dict(collections.Counter('no_solution' if r['question'][':question/answer-fields'][0][':answer-field/choices'][R.correct_index(r)][':answer/value']=='No solution' else 'infinite' for r in rs)),'profiles':dict(collections.Counter(r['generation']['template'] for r in rs))}
measurements={name:measure(rs) for name,rs in [('full_domain',records),('held_out_scales',[r for r in records if r['generation']['parameters']['rhs_scale']!=1]),('easy_before_delivery',easy),('easy_after_delivery',accepted),('runner_batch_before_delivery',batch),('runner_batch_after_delivery',accepted_batch)]}
conditional=[]
for sid in sorted(g.CASES):
 rs=[r for r in records if r['generation']['template']==sid];a=R.equations(rs[0]['question']);inconsistent=lookup[R.profile(rs[0])]
 conditional.append({'template':sid,'visible_coefficient_signature':a[:,:2].tolist(),'strategy':'Choose No solution without reading either RHS' if inconsistent else 'Ignore second equation; choose the bank vector satisfying the first equation','correct':8,'total':8,'baseline':.2,'disposition':'defect','held_out_scales_correct':7,'solution_type_is_fixed':True,'after_easy_delivery':measure([r for r in accepted if r['generation']['template']==sid]) if rs[0]['question'][':question/difficulty'].endswith('/easy') else None})
# Check rejection/dedup in the real batch constructor, independent seed.
constructed=g.batch('easy',500,7331);R.save('constructor-records.json',constructed)
measurements['constructor_after_internal_fingerprint_dedup']=measure(constructed)
for name in ['domain','batch']:
 report=load('delivery-'+name+'/delivery.json');measurements[name+'_pipeline_counts']={k:report[k] for k in ['input_count','duplicate_count','accepted_count','inventory_basis']}
R.save('shortcut-results.json',{'command':f'{sys.executable} {E}/finish_review.py','training':'one scale=1 question per visible coefficient signature; RHS values ignored in consistency prediction; held-out scales test over all remaining scales','measurements':measurements,'conditional_probes':conditional,'minimal_case':{'template':'q-42157','seed':7331,'parameters':[{'rhs_scale':-4},{'rhs_scale':2}],'strategy':'Recognize first-row coefficient -6 and choose the text No solution. Coefficient -6 alone gives no mathematical information about consistency.','after_delivery_correct':7,'after_delivery_total':7},'batch_strategy':'Visible coefficient signature predicts No solution for q-73749 and q-42163. For q-73750 and q-20783, ignore second equation and select the vector satisfying the first equation. All five native correct choices found; independent of UI choice order.'})
# Selection is a subset operation and cannot break an invariant true of each
# candidate. Retain concrete read-only draws plus the exact assumptions.
inv=json.load(open(R.JOB/'source/inventory.json'));inventory=inv['questions'];source_ids={q[':question/id'] for q in json.load(open(R.JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']}
R.save('inventory-records.json',inventory)
R.save('affected-inventory.json',{'affected_questions':[]})
R.save('inventory-audit.json',{'basis':inv['basis'],'questions_tested':len(inventory),'original_source_questions':sum(q[':question/id'] in source_ids for q in inventory),'non_source_questions':[q[':question/id'] for q in inventory if q[':question/id'] not in source_ids],'generated_metadata_present':sum(any('generat' in k for k in q) for q in inventory),'result':'Verified absence of stored generated instances in captured inventory, rather than untested inventory. All 17 questions match original source IDs; do not relabel them generated. No affected generated record can be reproduced here.','captured_records':'inventory-records.json','limits':'Only captured math basis 5364; later database contents may differ.'})
# Faithful reproduction of selection.rs select's easy-only branch, explicit
# fixture entity IDs for unpublished candidates; learner histories are variable.
fixtures=[{'fixture_entity_id':1000000+i,'record':r} for i,r in enumerate(accepted_batch)]
def select_fixture(candidates,seed,weighted=True):
 candidates=sorted(candidates,key=lambda c:c['fixture_entity_id'])
 if not weighted:return candidates[0]
 h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53)
 return candidates[int(u*len(candidates))]
draws=[]
for fresh in [fixtures,fixtures[1:],fixtures[2:]]:
 for seed in ['independent-selection-'+str(i) for i in range(64)]:
  selected=select_fixture(fresh,seed);draws.append({'seed':seed,'fresh_entity_ids':[f['fixture_entity_id'] for f in fresh],'chosen_fixture_entity_id':selected['fixture_entity_id'],'question_id':selected['record']['question'][':question/id'],'strategy_correct':strategy(selected['record'])==selected['record']['question'][':question/answer-fields'][0][':answer-field/choices'][R.correct_index(selected['record'])][':answer/id']})
R.save('selection-results.json',{'source_file':'engine/rust/question_selection.rs:select and seen_before_task','candidate_fixtures':fixtures,'weights':[1,0,0],'draws':draws,'passed':all(d['strategy_correct'] for d in draws),'unweighted_fallback':select_fixture(fixtures,'unused',False)['fixture_entity_id'],'invariant_proof':'For every delivered record, the coefficient-signature shortcut succeeds. Selection only removes seen candidates, partitions them by difficulty and chooses one; it does not rewrite a record or diversify its consistency. Thus every nonempty fresh subset of the generated easy pool retains the shortcut regardless of actual policy weights, task seeds, or entity IDs. Fixture simulations validate easy-only draws but are not claimed to be live learner sessions.','limits':['Policy weights, learner histories, and future entity IDs are absent. No claim about live draw frequencies or final publication is made.','Original source questions are separate from the proposed generated pool; finite original material is not reported as a generated-inventory defect.']})
# Relocation and direct CLI output, capturing every mutation under evidence.
rel=E/'relocated-package'
if rel.exists():shutil.rmtree(rel)
shutil.copytree(R.PKG,rel)
cmd=[sys.executable,str(rel/'17592186105746.py'),'--difficulty','easy','--seed','7331','--count','5','--output',str(E/'relocated-records.json')]
rr=subprocess.run(cmd,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},cwd=E,capture_output=True,text=True)
relrecords=load('relocated-records.json') if rr.returncode==0 else []
p=load('packaging-results.json');p.update({'relocation_command':cmd,'relocation_exit':rr.returncode,'relocation_stdout':rr.stdout,'relocation_stderr':rr.stderr,'relocation_equals_original':relrecords==g.batch('easy',5,7331),'no_assets_generated':True,'package_unchanged':load('package-before.json')=={str(p.relative_to(R.PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in R.PKG.rglob('*') if p.is_file()}});R.save('packaging-results.json',p)
# Scope established directly from parsed prompts, not generator's labels.
R.save('scope-results.json',{'cases':len(records),'easy':len(easy),'moderate':len(records)-len(easy),'all_two_equations_two_variables':all(R.equations(r['question']).shape==(2,3) for r in records),'all_singular_rank_one':all(R.equations(r['question'])[:,:2].rank()==1 for r in records),'easy_first_pivot_one':all(R.equations(r['question'])[0,0]==1 for r in easy),'largest_absolute_displayed_easy_entry':max(abs(int(z)) for r in easy for z in R.equations(r['question'])),'response_contract':'all one five-choice radio field','assessment':'No demonstrated unsupported prerequisite or method: easy still performs one integer elimination, moderate normalizes first pivot. Main defect is restriction/shortcut, not scope drift.','refs':['source-analysis.json','domain-records.json','math-results.json']})
# Record actual UI's option permutation; reject a stored-position shortcut claim.
report=load('render-all/rendering.json');render_input=load('render-records.json');order=[]
for c,r in zip(report['cases'],render_input):
 text=c['text'];before=text.split('Correct choice selected.')[0]
 order.append({'index':c['index'],'stored_correct_index':R.correct_index(r),'actual_ui_correct_index':before.count('Incorrect choice left unselected.'),'template':r['generation']['template']})
R.save('ui-order-results.json',{'mechanism':'ui/learning.js choiceOrder hashes itemId:fieldId:choiceId. Stored order is not display order.','observations':order,'conclusion':'Stored fixed answer position is not a valid learner-facing defect. The demonstrated No solution action is independent of displayed position.','rendering_report':'render-all/rendering.json'})
(E/'session-state.md').write_text('Completed source account, 16/17 replay (q-20964 absent), exact finite-domain math, native grading 685 checks, shared delivery (64 -> 56 easy; runner 5 -> 5), selection subset analysis and 192 fixture draws, relocation/dependencies, original-only inventory inspection. Renderer completed all 11 records; screenshot inspection and final pedagogical evidence/report remain. Package hash map unchanged.\n')
print(json.dumps({'measurements':measurements,'packaging':p,'inventory_generated_count':0,'selection_draws':len(draws),'rendered':len(report['cases'])},default=str))

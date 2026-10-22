"""Supplement reused independent checks with changed sampler and stage evidence."""
import collections, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent
# Reuse the independent visible-text parser, not the generator truth metadata.
parser=(E/'audit.py').read_text();exec(parser[parser.index('def val('):parser.index('src=json.load')])
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
prefix=json.load(open(E/'decision-prefix.json'))
report=[];native=[c for c in json.load(open(E/'native-input.json')) if not str(c['label']).startswith('prefix-')]
for i,r in enumerate(prefix):
 expected=visible(r);actual=bits(r);assert expected==actual
 # Check every worked conditional against the same independently read premise
 # and compare the stated true/false labels with actual proposition values.
 clauses=re.findall(r'- The following statement is (true|false):\s*\n\s*\*If ([^\n]+)\*',r['question'][':question/worked-solution'])
 assert len(clauses)==3
 assert [v=='true' for v,_ in clauses]==expected
 report.append({'index':i,'id':r['question'][':question/id'],'independent_truths':expected,'solution_truths':[v for v,_ in clauses]})
 tests=[]
 for j,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   tests.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==val(f) else 'rejected','purpose':'Changed selection pass, independently verified visible theorem implications; test every option'})
 native.append({'label':'prefix-'+str(i),'record':r,'checks':tests})
save('prefix-math-results.json',report);save('native-input.json',native)
# Check pair relationships on printed content, stored solutions and field actions.
pairs=json.load(open(E/'counterfactual-records.json'))
def ss(r):return [f[':answer-field/key'] for f in r['question'][':question/answer-fields']]
assert ss(pairs[0])==ss(pairs[2])==ss(pairs[3])
assert ss(pairs[0])[1:]==ss(pairs[1])[1:] and ss(pairs[0])[0]!=ss(pairs[1])[0]
assert bits(pairs[0])==bits(pairs[2])==[True,False,True]
assert bits(pairs[1])==[False,False,True] and bits(pairs[3])==[False,True,False]
assert all(visible(r)==bits(r) for r in pairs)
for r in pairs:
 q=r['question'];pr=q[':question/problem'];sol=q[':question/worked-solution']
 stem=pr.split('*If ',1)[1].split(' then',1)[0]
 assert sol.count(stem)==3
 assert re.findall(r'- The following statement is (true|false):',sol)==[str(b).lower() for b in bits(r)]
save('counterfactual-results.json',{'command':'python -B current_checks.py','records':'counterfactual-records.json','base':0,'relevant_conclusion_polarity':{'after':1,'change':'Only determinant conclusion changes; other two are identical','before':[True,False,True],'after_truths':[False,False,True]},'relevant_premise':{'after':3,'change':'Full rank becomes deficient; all three printed conclusions are identical','before':[True,False,True],'after_truths':[False,True,False]},'irrelevant_equivalent_premise':{'after':2,'change':'rank=7 replaced by nullity=0; all conclusions identical','before_and_after':[True,False,True]},'solutions':'Each of three conditional statements quotes its current premise; truth markers equal independent visible implications.','grader':'native-input.json labels 102..105 exercise every true and false field choice; native-report.json supplies actual outcomes.','render':'render/question-006.html through question-009.html are the actual rendered pair prompts and solutions.'})
# Verify filtering did not change semantic decision coverage.
stages={}
for name,input_file,accepted in [('batch','runner-batch.json','delivery-batch/accepted.json'),('controls','independent-samples.json','delivery-samples/accepted.json'),('prefix','decision-prefix.json','delivery-prefix/accepted.json')]:
 before=json.load(open(E/input_file));after=json.load(open(E/accepted))
 assert len(before)==len(after)
 assert [(r['question'][':question/problem'],bits(r)) for r in before]==[(r['question'][':question/problem'],bits(r)) for r in after]
 stages[name]={'input':len(before),'surviving':len(after),'decision_masks_preserved':True,'requested_difficulty':'moderate'}
save('delivery-comparison.json',stages)
inv=json.load(open(E.parent/'source/inventory.json'));src=json.load(open(E.parent/'source/source.json'))
ids={q[':question/id'] for q in src['material']['kp'][':knowledge-point/questions']}
assert all(q[':question/id'] in ids for q in inv['questions'])
save('inventory-assessment.json',{'basis':inv['basis'],'records_examined':len(inv['questions']),'all_original_source_ids':True,'generated_records':sum(any('generat' in k for k in q) for q in inv['questions']),'assessment':'Verified captured inventory contains only original instructional questions, so no affected stored generated instance of the retained batch shortcut is demonstrated. Original questions are not relabelled as generated. Later live inventory is untested.','questions':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'classification':'original source'} for q in inv['questions']]})
save('affected-inventory.json',{'affected_questions':[]})
save('selection-analysis.json',{'basis':inv['basis'],'source':'engine/rust/question_selection.rs select(), seen_before_task()','examined':'Read current source. Candidates are sorted/deduplicated; prior learner tasks and current prefix exclude seen IDs. Positive weighted bands are chosen before uniform draw within a band; absent policy chooses first ID. Unknown ratings fallback only without eligible positive rated bands.','current_delivery':'All five current survivors and 73 prefix records are moderate. With fresh history and positive moderate weight every delivered candidate remains eligible; selection uses no truth-mask or template filter. Unique first-pass masks remain unique after any removal of candidates, so selection cannot recreate the retained duplicate-mask subgroup within this batch.','limits':'Actual learner history, live combined pool and active policy weights absent. Exact per-learner order/probabilities and later changing inventory are not claimed.'})
print(json.dumps({'prefix_math':len(report),'native_cases':len(native),'native_submissions':sum(len(c['checks']) for c in native),'stages':stages,'inventory_originals':len(inv['questions'])}))

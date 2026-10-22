"""Read-only reproduction of the three captured generated inventory instances."""
from visible_records import *
inventory=json.loads((W.parent/'source/inventory.json').read_text())
source=json.loads((W.parent/'source/source.json').read_text())
source_ids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
prior=json.loads((E/'inventory-prior-records.json').read_text())
non_source=[q for q in inventory['questions'] if q[':question/id'] not in source_ids]
assert {q[':question/id'] for q in non_source}=={r['question'][':question/id'] for r in prior}
def authored(q):
 def field(f):return (f[':answer-field/key'],kind(f[':answer-field/type']),sorted((kind(a[':answer/type']),a[':answer/value']) for a in f[':answer-field/choices']),correct(f))
 return (q[':question/problem'],q[':question/worked-solution'],kind(q[':question/difficulty']),sorted(map(field,q[':question/answer-fields'])))
records=[];affected=[];rows=[]
for stored in non_source:
 old=next(r for r in prior if r['question'][':question/id']==stored[':question/id'])
 profile=old['generation']['profile'];parameters=old['generation']['parameters']
 fresh=g.generate_moderate(seed=0,profile=profile,parameters=parameters)
 assert authored(fresh['question'])==authored(stored),(profile,'full authored content changed')
 # The preceding reproduction is independent of stored IDs; reattach capture for traceability.
 fresh_id=fresh['question'][':question/id'];fresh['question']=copy.deepcopy(stored)
 fresh['generation'].update(evidence_only=True,eligible_for_learning=False)
 fresh['generation']['reproduction']={'command':'python checks/inventory_audit.py','method':'current generator explicit parameters; full prompt, solution, fields, banks and correct values asserted equal ignoring identity and field order; captured IDs then reattached','captured_entity_id':stored[':db/id'],'captured_basis':inventory['basis'],'original_seed':'not captured','reconstruction_seed':0,'fresh_generator_question_id':fresh_id,'historical_generator_version':old['generation']['version'],'identity_binding':'captured stored question/field/answer IDs; not generated from the fresh identity function'}
 st=inspect(fresh);predicted=('A',) if st['dimensions'][0]==4 else ('A','B')
 assert st['answer']==predicted
 records.append(fresh)
 affected.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'finding':'The captured generated three-matrix family admits a dimension-only predictor: A if A is 4x4, otherwise A and B. All three generated inventory records match, bypassing forbidden-side inspection.','reproduction':'python checks/inventory_audit.py; explicit profile and matrices are in generated-records.json generation.parameters','evidence_path':'generated-records.json'})
 rows.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'profile':profile,'full_authored_content_reproduced':True,'predicted':predicted,'answer':st['answer']})
save('generated-records.json',records);save('affected-inventory.json',{'affected_questions':affected})
save('inventory-audit.json',{'basis':inventory['basis'],'questions':len(inventory['questions']),'source_excluded':len(source_ids),'generated_tested':len(records),'affected':len(affected),'untested_non_source':0,'cases':rows,'limits':['Original generated seeds and publication metadata were not captured. Explicit-parameter reproduction with verified full authored content and captured identity reattachment is reported transparently. No original source question is marked as generated.']})
print(json.dumps({'tested':len(records),'affected':len(affected),'untested_non_source':0}))

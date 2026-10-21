import sys
sys.dont_write_bytecode=True
import review as a
import collections,hashlib,copy,json
E=a.E
source=a.read(a.JOB/'source/source.json');a.SIGNATURES={q[':question/math-academy-id']:a.sign(a.matrix(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],True)[0]) for q in source['material']['kp'][':knowledge-point/questions']}
def candidates(r,kind):
 bank=a.bank(r)
 if kind.startswith('position_'):return [int(kind[-1])]
 if kind=='source_sign_mask':return [i for i,m in enumerate(bank) if a.sign(m)==a.SIGNATURES[r['generation']['template']]]
 if kind=='negative_corner':return [i for i,m in enumerate(bank) if m[-1][-1]<0]
 if kind=='positive_corner':return [i for i,m in enumerate(bank) if m[-1][-1]>0]
 if kind=='zero_corner':return [i for i,m in enumerate(bank) if m[-1][-1]==0]
 if kind=='one_corner':return [i for i,m in enumerate(bank) if m[-1][-1]==1]
 if kind=='negative_top_left':return [i for i,m in enumerate(bank) if m[0][0]<0]
 if kind=='max_at_top_left':return [i for i,m in enumerate(bank) if abs(m[0][0])==max(abs(v) for row in m for v in row)]
 if kind=='max_at_corner':return [i for i,m in enumerate(bank) if abs(m[-1][-1])==max(abs(v) for row in m for v in row)]
 raise ValueError(kind)
strategies=['source_sign_mask','negative_corner','positive_corner','zero_corner','one_corner','negative_top_left','max_at_top_left','max_at_corner']+[f'position_{i}' for i in range(5)]
def probes(rs,label,ref):
 groups={'ALL':rs};groups.update({p:[r for r in rs if r['generation']['template']==p] for p in sorted({r['generation']['template'] for r in rs})});groups.update({mode:[r for r in rs if r['generation'].get('mode')==mode] for mode in sorted({r['generation'].get('mode') for r in rs if r['generation'].get('mode')})})
 rows=[]
 for group,records in groups.items():
  for strategy in strategies:
   wins=0;attempts=0
   for r in records:
    ix=candidates(r,strategy)
    if len(ix)==1:
     attempts+=1;wins+=a.field(r)[':answer-field/choices'][ix[0]][':answer/id']==a.correct_id(a.field(r))
   rows.append({'stage':label,'subgroup':group,'strategy':strategy,'correct':wins,'total':len(records),'unique_candidate_attempts':attempts,'baseline':.2,'sample_refs':[ref]})
 return rows
samples=a.read(E/'independent-samples.json');delivered=a.read(E/'delivery-easy/accepted.json')+a.read(E/'delivery-moderate/accepted.json');batch=a.read(E/'runner-batch.json');accepted=a.read(E/'delivery-batch/accepted.json');historical=a.read(E/'generated-records.json')
rows=[]
for rs,label,ref in [(samples,'raw','independent-samples.json'),(delivered,'filtered','delivery-easy/accepted.json'),(batch,'batch_raw','runner-batch.json'),(accepted,'batch_filtered','delivery-batch/accepted.json'),(historical,'historical','generated-records.json')]:
 ps=probes(rs,label,ref)
 if label=='filtered':
  for p in ps:p['sample_refs'].append('delivery-moderate/accepted.json')
 rows+=ps
a.save('shortcut-results.json',rows)
coverage=[]
for p in sorted(a.g.PROFILES):
 rs=[r for r in samples if r['generation']['template']==p];masks={str(a.sign(a.correct_matrix(r))) for r in rs};banks=[a.bank(r) for r in rs]
 coverage.append({'profile':p,'count':len(rs),'modes':dict(collections.Counter(r['generation']['mode'] for r in rs)),'correct_sign_masks':len(masks),'row_roles':sorted({str(r['generation']['row_order']) for r in rs}),'variable_roles':sorted({str(r['generation']['variable_order']) for r in rs}),'positions':dict(collections.Counter(next(i for i,c in enumerate(a.field(r)[':answer-field/choices']) if c[':answer/id']==a.correct_id(a.field(r))) for r in rs)),'distinct_correct_matrices':len({str(a.correct_matrix(r)) for r in rs}),'same_mask_banks':sum(len({str(a.sign(m)) for m in bank})==1 for bank in banks)})
a.save('coverage-results.json',coverage)
# Historical findings: source masks still identify these exact stored generated records.
affected=[]
for r in historical:
 wins,n=a.sign_strategy(r);assert wins and n==1
 affected.append({'question_id':r['question'][':question/id'],'entity_id':r['inventory_reproduction']['entity_id'],'finding':'Historical generated '+r['generation']['template']+': memorized source sign mask uniquely identifies keyed matrix; this persists in captured stored content, separate from repaired sampler.','reproduction':str(a.PY)+' -B reproduce_inventory.py && '+str(a.PY)+' -B variation.py; archived seed '+str(r['generation']['seed'])+', parameters '+json.dumps(r['generation']['parameters'],sort_keys=True),'evidence_path':'generated-records.json'})
a.save('affected-inventory.json',{'affected_questions':affected})
# Reuse unchanged learner-selection conclusions only after checking source hash and captured IDs.
oldsel=a.read(a.PREV/'learner-selection-results.json');qpath=a.REPO/'engine/rust/question_selection.rs'
oldsel['current_verification']={'source_sha256':hashlib.sha256(qpath.read_bytes()).hexdigest(),'captured_basis':5352,'reproduced_historical_ids_match':set(oldsel['hypothetical_fresh_usable_entity_ids'])=={r['inventory_reproduction']['entity_id'] for r in historical},'current_batch':'All 5 are easy and survive delivery; with positive easy weight, each has positive conditional uniform support within the selected easy band. Actual IDs/order after publication unavailable. Unconfigured policy selects smallest fresh usable entity ID; actual learner exclusions and weights uncaptured.'}
a.save('learner-selection-results.json',oldsel)
# Demonstrate rejection with adjacent valid controls, hold everything but the coefficient literal fixed.
base={'2':2,'3':4};tests=[];records=[]
for value in [2,1,-1,-2]:
 ps={**base,'2':value}
 try:
  r=a.g.generate('easy',941713401,profile='q-71722',parameters=ps);a.check_math(r);records.append(r);result='returned correct complete record'
 except Exception as ex:result=type(ex).__name__+': '+str(ex)
 tests.append({'parameters':ps,'result':result})
a.save('boundary-counterexample-records.json',records)
a.save('boundary-counterexample.json',{'seed':941713401,'profile':'q-71722','source_id':'dfed30ca-4b53-5a19-b938-cfe31a91deda','tests':tests,'valid_problem':'x-4=y; 1+y=-x','expected_matrix':[[1,-1,4],[1,1,-1]],'expected_bank_capacity':'Four permutations preserving signs and zeros plus a fifth source-scope coefficient/constant reading distractor; current fallback supplies it.','reason':'Latest repair accepts both +/-1 literal assignments, retaining distinct permutations and adding a same-mask magnitude-reading error. Strict old-package failure and current acceptance recorded separately.','command':str(a.PY)+' -B variation.py'})
print(json.dumps({'probe_rows':len(rows),'coverage_profiles':len(coverage),'historical_affected':len(affected),'batch_perfect_probes':[(p['subgroup'],p['strategy'],p['total']) for p in rows if p['stage']=='batch_filtered' and p['correct']==p['total']],'boundary_cases':tests}))

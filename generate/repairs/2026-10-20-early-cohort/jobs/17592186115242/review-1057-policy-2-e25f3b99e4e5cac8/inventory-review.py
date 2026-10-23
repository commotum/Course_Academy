"""Replay previously affected records and check current retirement eligibility. No database writes."""
import sys,json,pathlib,importlib.util,hashlib
sys.dont_write_bytecode=True
import math_helper as v
R=v.R; B=R.parent; oldR=B/'review-0-policy-2-7164cf0480f72dae'
spec=importlib.util.spec_from_file_location('archived_generator',oldR/'relocated/17592186115242.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
inv=json.load(open(B/'source/inventory.json'));original=json.load(open(B/'source/source.json'))['material']['kp'][':knowledge-point/questions'];original_ids={q[':question/id'] for q in original}; records=[];cases=[];affected=[]
for saved in json.load(open(oldR/'generated-records.json')):
 gen=saved['generation'];r=old.generate('easy',seed=gen['seed'],template=gen['template'],parameters=gen['parameters']);assert all(gen[k]==z for k,z in r['generation'].items());r['generation']=gen
 q=next(q for q in inv['questions'] if q[':question/id']==r['question'][':question/id']);rq=r['question'];assert q[':question/id'] not in original_ids
 assert q[':question/problem']==rq[':question/problem'] and q[':question/worked-solution']==rq[':question/worked-solution']
 f=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
 assert sorted((a[':answer/id'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/id'],a[':answer/value']) for a in rf[':answer-field/choices'])
 assert f[':answer-field/correct'][':answer/id']==rf[':answer-field/correct'][1]
 v.audit(r);p=gen['parameters'];pred=(max if p['b']*p['d']>0 else min)(rf[':answer-field/choices'],key=lambda a:v.expr(a[':answer/value'].split('=')[1]));assert pred[':answer/id']==rf[':answer-field/correct'][1]
 retired=q.get(':question/retired',False);cases.append(dict(question_id=q[':question/id'],entity_id=q[':db/id'],retired=retired,eligible=not retired,exact_replay=True,archived_shortcut=True));records.append(r)
 if not retired:affected.append(dict(question_id=q[':question/id'],entity_id=q[':db/id'],finding='Selectable historical sign-extremum shortcut',reproduction='job-python -B inventory-review.py',evidence_path='generated-records.json'))
unknown=[q[':question/id'] for q in inv['questions'] if q[':question/id'] not in original_ids|{r['question'][':question/id'] for r in records}]
assert not unknown
v.write('generated-records.json',records);v.write('affected-inventory.json',dict(affected_questions=affected));v.write('inventory-audit.json',dict(basis=inv['basis'],total=len(inv['questions']),source_questions=len(original),cases=cases,untested_generated_ids=unknown,eligible_affected=len(affected),retirement_rule='engine/rust/learning.rs validate_practice_question lines 149-153 rejects retired; fresh selection callers at 600,1580,1674 invoke validation.',limits=['Snapshot basis only; future inventory may differ. Retired defects remain preserved history, not selectable practice. Source questions are not classified as generated.']))
print(json.dumps(dict(reproduced=len(records),retired=sum(c['retired'] for c in cases),eligible_affected=len(affected),unknown=len(unknown))))

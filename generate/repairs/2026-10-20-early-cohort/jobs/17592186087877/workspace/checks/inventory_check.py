"""Read-only verification of complete historical generated records against capture."""
import audit as A
import json,pathlib
E=A.PKG/'evidence'
job=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186087877')
inv=A.load(job/'source/inventory.json');stored={q[':question/id']:q for q in inv['questions']}
# These complete records were reproduced at v2 by the independent review.
# Rechecking their visible fields avoids falsely regenerating stored v2 as v3.
records=A.load(job/'review-0-policy-2-34bbd6ba8ad34ac5/generated-records.json')
historical=A.load(A.PKG/'17592186087877/reference/replenishment/basis-2009/generated.json')
old_by_id={r['question'][':question/id']:r for r in historical}
affected=[];checks=[]
for r in records:
    q=r['question'];qid=q[':question/id'];sq=stored[qid];f=A.field(r);sf=sq[':question/answer-fields'][0]
    assert r['generation']==old_by_id[qid]['generation']
    for k in [':question/problem',':question/worked-solution']:assert q[k]==sq[k]
    assert {a[':answer/value'] for a in f[':answer-field/choices']}=={a[':answer/value'] for a in sf[':answer-field/choices']}
    assert A.key(r)==sf[':answer-field/correct'][':answer/id']
    defect=q[':question/difficulty'].endswith('/easy') and A.shortcut(r)==A.key(r)
    checks.append({'question_id':qid,'entity_id':sq[':db/id'],'stored_fields_and_historical_metadata_match':True,'demonstrated_shortcut':defect})
    if defect:affected.append({'question_id':qid,'entity_id':sq[':db/id'],'finding':'v2 easy bank uniquely exposes I through the doubled exponent relationship, without reading the ODE.','reproduction':f'{__import__("sys").executable} checks/inventory_check.py; inspect historical generation parameters and bank-only double-exponent prediction in evidence/generated-records.json','evidence_path':'../workspace/evidence/generated-records.json'})
assert len(records)==9 and len(stored)==17 and len(affected)==3
(E/'generated-records.json').write_text(json.dumps(records,indent=2)+'\n')
(A.PKG/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
(E/'inventory-results.json').write_text(json.dumps({'basis':inv['basis'],'checked_generated_records':len(records),'source_questions_not_marked_generated':8,'checks':checks,'limits':'Verified against supplied basis 5319 capture and complete independently reproduced v2 records. No live database reads; other-band shortcuts were not re-audited.'},indent=2)+'\n')
print(json.dumps({'historical_records_verified':9,'affected_easy_records':3,'source_questions_excluded':8}))

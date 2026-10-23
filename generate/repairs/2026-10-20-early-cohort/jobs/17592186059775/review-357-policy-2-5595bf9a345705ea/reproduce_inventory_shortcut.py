"""Strict failing acceptance test: run context Python -B from evidence_root.
Only writes its own counterexample and report alongside this script.
"""
from review_helpers import *
legacy=loadmod('legacy',W/'evidence/legacy/17592186059775.py')
inv=json.load(open(J/'source/inventory.json'))
stored=next(q for q in inv['questions'] if q[':question/id']=='f98461ac-7c48-536e-aa56-fcc53a0bd592')
record=legacy.generate('moderate',59775,'q-1060',['q-1060',3])
assert q(record)[':question/id']==stored[':question/id']
assert q(record)[':question/problem']==stored[':question/problem']
assert q(record)[':question/worked-solution']==stored[':question/worked-solution']
assert not stored.get(':question/retired',False)
for a in f(record)[':answer-field/choices']:
    sa=next(c for c in stored[':question/answer-fields'][0][':answer-field/choices'] if c[':answer/id']==a[':answer/id'])
    assert mats(sa[':answer/value'])==mats(a[':answer/value'])
    a[':answer/value']=sa[':answer/value']
assert key(record)[':answer/id']==stored[':question/answer-fields'][0][':answer-field/correct'][':answer/id']
family=[legacy.generate('moderate',59775,'q-1060',p) for p in legacy.domain('q-1060')]
hits=sum(rank(r)==2 for r in family)
save('inventory-minimal-record.json',[record])
report={'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'basis':inv['basis'],'retired':False,'strategy':'Choose median lower-right candidate; ignore input matrix.','stored_hit':rank(record)==2,'family_correct':hits,'family_total':len(family),'random_baseline':0.2,'parameters':['q-1060',3],'seed':59775}
save('inventory-strict-results.json',report)
print(json.dumps(report))
assert not (rank(record)==2 and hits==len(family)), 'Eligible stored legacy family still has the demonstrated median-answer shortcut'

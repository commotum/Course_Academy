"""Read-only regression. --historical-control models the former eligible state."""
from review_helpers import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--historical-control',action='store_true');args=p.parse_args()
inv=json.load(open(J/'source/inventory.json'));arch=json.load(open(E/'generated-records.json'))
legacy=loadmod('legacy',W/'evidence/legacy/17592186059775.py')
sid='f98461ac-7c48-536e-aa56-fcc53a0bd592';stored=next(z for z in inv['questions'] if z[':question/id']==sid)
r=next(z for z in arch if q(z)[':question/id']==sid)
assert q(r)[':question/problem']==stored[':question/problem']
assert r['generation']['parameters']==['q-1060',3]
family=[legacy.generate('moderate',59775,'q-1060',p) for p in legacy.domain('q-1060')]
hits=sum(rank(z)==2 for z in family)
retired=False if args.historical_control else stored.get(':question/retired',False)
result={'basis':inv['basis'],'question_id':sid,'entity_id':stored[':db/id'],'actual_retired':stored.get(':question/retired',False),'modeled_retired':retired,'historical_control':args.historical_control,'control_explanation':'Only eligibility flag is restored to the prior reviewed value; complete reproduced historical record is unchanged. No DB write.','legacy_family_correct':hits,'legacy_family_total':len(family),'stored_hit':rank(r)==2,'eligible_defect':not retired and rank(r)==2 and hits==len(family),'record_evidence':'generated-records.json','selection_rule':'learning.rs:149-153 rejects retired questions before fresh practice'}
save('inventory-control-results.json' if args.historical_control else 'inventory-strict-results.json',result)
print(json.dumps(result));assert not result['eligible_defect'],'Eligible historical family preserves the median shortcut'

"""Read-only prospective hard-band selection from the actual accepted batch.

Mirrors select() digest and within-band draw. Newly published entity IDs and live
weights/history are unavailable; use deterministic prospective entity ordering.
No claim that an unconfigured policy or exhausted history preserves both roles.
"""
import sys,json,pathlib,hashlib,importlib.util,collections
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('role',ROOT/'checks/test_role_exchange.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
records=r.load(ROOT/'evidence/role-regression/delivery/accepted.json')
# Any actual entity ordering gives uniform mass to each candidate in this band.
records=sorted(records,key=lambda q:q['question'][':question/id'])
scenarios=[]
for name,pool in [('fresh',records),('some_seen',records[3:]),('only_second_resonant_remains',[q for q in records if r.visible_role(q)==1])]:
 selected=[]
 for i in range(32):
  digest=hashlib.sha256(('course-academy/question-selection/v1/repair-'+str(i)).encode()).digest()
  u=(int.from_bytes(digest[8:16],'big')>>11)/2**53
  selected.append(pool[int(u*len(pool))])
 counts=collections.Counter('none' if r.visible_role(q) is None else str(r.visible_role(q)+1) for q in selected)
 if name in ('fresh','some_seen'):assert counts['1'] and counts['2']
 scenarios.append({'scenario':name,'eligible_count':len(pool),'draws':32,'resonance_positions_selected':dict(counts)})
p=pathlib.Path('/home/jake/Developer/Course_Academy/engine/rust/question_selection.rs')
r.save(ROOT/'evidence','selection-results.json',{'selection_implementation':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scenarios':scenarios,'policy_assumption':'hard has positive weight and eligible fresh hard candidates; within-band choice is uniform. Prospective ordering by UUID substitutes for future entity IDs.','limits':['No database writes/publication or live learner histories were exercised.','Unconfigured policy selects the smallest entity ID; role coverage per learner is not guaranteed.','History exclusions can remove one role. Existing historical pool remains unchanged; four mixed originals have the demonstrated shortcut.'],'generator_rejection':'No rejection loop: mixed role chosen first and compatible rates sampled directly. Two invalid explicit mixed cases reject; both valid positions pass.'})
print(json.dumps(scenarios,indent=2))

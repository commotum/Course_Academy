"""Read-only execution of the retained original generator for exact historical witnesses."""
from common import *
import types,copy
JOB=ROOT.parent
# Give the frozen original its original resource location, without changing its text.
g=types.ModuleType('original');g.__file__=str(ROOT/'17592186119805.py')
exec(compile((E/'generator-before.py').read_text(),str(E/'generator-before.py'),'exec'),g.__dict__)
runner=json.loads((JOB/'samples.json').read_text());reproduced=[]
for old in runner:
 meta=old['generation'];r=g.generate('easy',meta['seed'],meta['bank_profile'],meta['parameters'])
 assert r==old
 reproduced.append(r)
assert reproduced[0]['question'][':question/id']=='b713577b-6986-5a32-9f22-4f4d35b1455e'
shortcuts=[old_shortcut(r['question'])==value(key(r['question'])) for r in reproduced]
assert all(shortcuts)
p=copy.deepcopy(g.CASES['q-34241']);p['c']=2
bad=g.generate('easy',64193,'q-34241',p);answer=solve(bad['question'])[0]
assert answer=='No solution' and key(bad['question'])=='2'
p=copy.deepcopy(g.CASES['q-34570']);p['u'][0]=1
try:g.generate('moderate',64193,'q-34570',p)
except AssertionError:consistent_failure=True
else:consistent_failure=False
assert consistent_failure
inventory=json.loads((JOB/'source/inventory.json').read_text());affected=[];historical=[];originals=0
for q in inventory['questions']:
 if q.get(':question/math-academy-id'):originals+=1;continue
 a,u,*_=mats(q[':question/problem']);c=int(re.search(r'if \$(\d+)',q[':question/problem'])[1])
 p={'a':list(map(int,a)),'u':list(map(int,u)),'c':c,'s':None,'letter':'k'}
 r=g.generate('moderate',64193,'q-34570',p)
 assert r['question'][':question/id']==q[':question/id']
 assert r['question'][':question/problem']==q[':question/problem'] and key(r['question'])==key(q)
 verify(r);historical.append(r)
 affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Stored generated homogeneous question belongs to a family forced to answer No solution, allowing the zero-RHS shortcut. Its individual arithmetic is correct.','reproduction':f'{sys.executable} checks/reproduce_before.py; frozen original q-34570, seed=64193, parameters='+json.dumps(p,sort_keys=True),'evidence_path':'generated-records.json'})
save('generated-records.json',historical)
save('affected-inventory.json',{'affected_questions':affected,'audit_scope':{'captured_questions':len(inventory['questions']),'original_source_questions_not_marked_generated':originals,'generated_questions_reproduced':len(historical),'status':'All non-source captured inventory entries tested; absence of other defects not claimed.'}})
save('before-exact-records.json',reproduced+[bad])
save('before-exact-results.json',{'runner_records_reproduced_exactly':len(reproduced),'shortcut_successes':sum(shortcuts),'subtraction_c2_independent_answer':str(answer),'subtraction_c2_authored_key':key(bad['question']),'consistent_homogeneous_assertion':consistent_failure,'missing_complete_profiles':[sid for sid in ['q-34572','q-105153','q-105156'] if sid not in g.PROFILES],'inventory_generated_reproductions':len(historical)})
print(json.dumps({'exact_runner_reproductions':len(reproduced),'shortcuts':sum(shortcuts),'affected_inventory':len(affected)}))

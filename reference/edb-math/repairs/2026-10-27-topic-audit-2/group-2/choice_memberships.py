import json
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());out=[]
for qid,fid,remove in[(17592186311586,17592186311122,17592186310249),(17592186311625,17592186311228,17592186310565)]:
 q=next(q for q in D['questions']if q[':db/id']==qid);f=next(f for f in q[':question/answer-fields']if f[':db/id']==fid);old=sorted(a[':db/id']for a in f[':answer-field/choices']);canon=f[':answer-field/correct'];duplicate=next(a for a in f[':answer-field/choices']if a[':db/id']==remove)
 assert canon[':answer/value'].replace('⁡','')==duplicate[':answer/value'].replace('⁡','');assert canon[':db/id']!=remove
 out.append({'entity':fid,'attribute':'answer-field/choices','before':old,'after':[e for e in old if e!=remove],'reason':'Detach mathematically identical noncanonical select option introduced by historical upsert; source proves original bank has four distinct displayed alternatives. Preserve canonical and detached answer identities and every learner history reference.','evidence':{'basis':9122,'question':qid,'identity':q[':question/math-academy-id'],'canonical':canon[':db/id'],'canonical_value':canon[':answer/value'],'detached':remove,'detached_value':duplicate[':answer/value'],'proof':'Only difference is zero-width function application marker U+2061; all operands, powers and signs identical. Both values solve the same target, so presenting both is ambiguous.'},'confidence':'high'})
(H/'choice-membership-proposals.json').write_text(json.dumps(out,indent=2)+'\n');print(len(out))

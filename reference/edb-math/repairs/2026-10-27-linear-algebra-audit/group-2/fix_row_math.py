import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;P=json.loads((H/'proposals.json').read_text());D=json.loads((H/'current.json').read_text());q=next(q for q in D['questions']if q[':db/id']==17592186455442);entry=next((p for p in P if p['entity']==q[':db/id']and p['attribute']=='question/worked-solution'),None)
if entry is None:
 entry={'entity':q[':db/id'],'attribute':'question/worked-solution','before':q[':question/worked-solution'],'after':q[':question/worked-solution'],'reason':'independent-math-check','evidence':[],'confidence':'high'};P.append(entry)
s=entry['after'];edits=[('2 & 2 & -1 & -6','2 & 2 & -1 & 6',2),('0 & -1 & -2 & 7','0 & -1 & -2 & -7',1),('{R}_{3}+(-2){R}_{2}','{R}_{3}+(-2){R}_{1}',1)]
for a,b,count in edits:assert s.count(a)==count,(a,s.count(a));s=s.replace(a,b)
entry['after']=s;entry['reason']+=',incorrect-intermediate-row-reduction-signs-and-row-label';entry['evidence'].append({'independent_math':'Target x=(6,11,6), so the augmented initial RHS is +6 in row 3. R2-3R1 gives -7; R3-2R1 gives -6. Original displayed initial/middle row3 RHS -6, middle row2 RHS +7, and R3-2R2 annotation are incorrect. Final coefficient vector (1,3,2) and existing correct answer x1=1 are unchanged.','exact_replacements':edits});(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');print('repaired intermediate derivation',q[':db/id'])

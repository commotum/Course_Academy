import json
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());qs={q[':db/id']:q for q in D['questions']}
fixes={
17592186241024:[(r':=-\frac{1}{2}{R}_{2}',r':=\frac{1}{2}{R}_{2}',1)],
17592186348105:[(r'{R}_{3}+2{R}_{1}',r'{R}_{3}+2{R}_{2}',1)],
17592186247256:[('0 & -1 & -5 & 11','0 & -1 & 5 & 11',2),(r'{R}_{4}+\left(-\frac{3}{7}\right){R}_{2}',r'{R}_{4}+\left(-\frac{3}{7}\right){R}_{3}',1),(r'{x}_{1}-3{x}_{2}',r'{x}_{1}-3{x}_{3}',1),(r'13{x}_{3}',r'-7{x}_{3}',1)],
17592186386599:[(r'{R}_{1} & :={R}_{1}+{R}_{2}',r'{R}_{2} & :={R}_{2}+{R}_{1}',1)],
17592186119670:[(r':=\frac{1}{8}{R}_{2}',r':=-\frac{1}{8}{R}_{2}',1)],
17592186247191:[(r'{R}_{3}-2{R}_{1}',r'{R}_{3}-2{R}_{2}',1)],
17592186247199:[(r'{R}_{3} & :={R}_{2}+3{R}_{1}',r'{R}_{3} & :={R}_{3}+3{R}_{1}',1),(r'0 &=8',r'0 &=-8',1),('$0=8.$','$0=-8.$',1)],
17592186408162:[(r'{R}_{3} & :={R}_{3}+2{R}_{2}',r'{R}_{2} & :={R}_{2}+2{R}_{1}',1),(r'{x}_{3}+{x}_{4} &=-8',r'{x}_{3}+{x}_{4} &=8',1)],
17592186408165:[(r'{R}_{2} & :={R}_{2}-7{R}_{1}',r'{R}_{3} & :={R}_{3}-7{R}_{1}',1)],
17592186430002:[(r'{R}_{3} & :={R}_{2}+{R}_{1}',r'{R}_{3} & :={R}_{3}+{R}_{1}',1)]}
for e,edits in fixes.items():
 q=qs[e];entry=next((p for p in P if p['entity']==e and p['attribute']=='question/worked-solution'),None)
 if entry is None:entry={'entity':e,'attribute':'question/worked-solution','before':q[':question/worked-solution'],'after':q[':question/worked-solution'],'reason':'independent-math-check','evidence':[],'confidence':'high'};P.append(entry)
 v=entry['after']
 for old,new,count in edits:assert v.count(old)==count,(e,old,v.count(old));v=v.replace(old,new)
 entry['after']=v;entry['reason']+=',incorrect-row-operation-or-system-transcription';ev={'source_identity':q.get(':question/math-academy-id'),'method':'Each stated operation was independently applied to the preceding exact augmented matrix and compared with the next displayed matrix. Follow-on systems also corrected where transcription conflicts were visible. Existing final correct answer unchanged.','exact_replacements':edits}
 entry['evidence']=entry['evidence']+[ev]if isinstance(entry['evidence'],list)else[entry['evidence'],ev]
# Correct a draft-only domain-font replacement that accidentally duplicated an existing command.
for p in P:p['after']=p['after'].replace(r'\mathbb\mathbb{R}',r'\mathbb{R}')
(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');print('10row-operation/system corrections;proposals',len(P))

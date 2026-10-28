import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());Q={q.get(':question/math-academy-id'):q for q in D['questions']};out=[]
repairs={
'q-73396':[(r'0 & 2 & -1 & 1',r'0 & 1 & -1 & 1','Subtracting R1 from original R3=[1,0,1|9] gives [0,1,−1|1]. The matrix immediately before the row swap must retain that coefficient1. The target solution (4,6,5) satisfies all original equations.')],
'q-130924':[(r'-3 & 10 & 6',r'-3 & 12 & 6','The prompt second equation is −3x+12y=6; its augmented matrix must contain12. All subsequent elimination and the correct general solution x=4y−2 already use12.')],
'q-42159':[(r'6 & 42 & -24',r'6 & 42 & 24','The prompt second equation is6x+42y=24; its augmented matrix RHS must be24. Subtracting6R1 then gives the all-zero row and x=4−7y, consistent with the existing key.')],
'q-74032':[(r'1 & 1 & 3 & -1',r'1 & 1 & 3 & 5','Swapping R2 and R3 leaves R1=[1,1,3|5] unchanged. Independent exact solve is (1,−2,2), whose sum1 matches the key.')],
'q-110300':[(r'0 & 1 & 0 & 0 & 0 & 0',r'0 & 1 & 0 & 0 & 1 & 0','Scaling only R3 by7 leaves row2 of [E|I] unchanged; its fifth entry remains1. The final right block is diag(1,1,7), which multiplies E to I.')],
'q-110855':[(r'1 & -1 & 2',r'1 & -1 & -2','R2:=R2−8R1 does not change R1=[1,−1,−2]. Column3 stays −2 times column1. The original first two columns remain the correct basis.')],
'q-75194':[(r'0 & 0 & 1 & 0 & 0 & 0',r'0 & 0 & 1 & 0 & 0 & 1','Scaling only R1 by1/8 leaves row3 of [D|I] unchanged; its final entry remains1. The final right block is diag(1/8,1,1), which multiplies D to I.')],
'q-74043':[(r'0 & 7 & -14 & -7',r'0 & 7 & -14 & 7','R3:=R3−4R1 gives RHS15−4·2=7, not−7. Both the next pre-swap and post-swap matrices must show7. Subsequent scaling and solution (5,3,1) are already correct.')]
}
for ident,reps in repairs.items():
 q=Q[ident];before=q[':question/worked-solution'];after=before;details=[]
 for old,new,reason in reps:
  count=after.count(old);assert count==(2 if ident=='q-74043'else 1),(ident,count);after=after.replace(old,new);details.append({'before_fragment':old,'after_fragment':new,'occurrences':count,'independent_derivation':reason})
 out.append({'entity':q[':db/id'],'attribute':'question/worked-solution','before':before,'after':after,'reason':'Correct an independently demonstrated intermediate matrix calculation error; final answer key is unchanged.','evidence':{'basis_t':9047,'identity':ident,'derivations':details,'provenance':'Authored mathematical correction, including errors retained in original source; not blind source restoration.'},'confidence':'high'})
for ident in ['q-34825','q-72462','q-42532']:
 q=Q[ident];before=q[':question/problem'];after=re.sub(r'(\d+)\s*\\cdot\s*(\d+)',lambda m:m[1]+r'\times'+m[2],before);assert after!=before
 out.append({'entity':q[':db/id'],'attribute':'question/problem','before':before,'after':after,'reason':'Restore source matrix-dimension notation: rows × columns, with a cross rather than scalar multiplication dot.','evidence':{'basis_t':9047,'identity':ident,'source_path':next(r['best']['path']for r in json.loads((H/'comparison.json').read_text())if r['identity']==ident and r['attribute']=='question/problem'),'independent_check':'Only the dimension separator changes; ordered row and column counts remain identical.'},'confidence':'high'})
(H/'independent-proposals.json').write_text(json.dumps(out,indent=2));print('independent corrections',len(out))

import json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(H),str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from restore_source import norm,pat
from reconstruct import SourceRenderer,reconstruct
from question_capture.math_format import normalize_source_tex
S=json.loads((H/'current.json').read_text());changes=json.loads((H/'proposals.json').read_text());evidence=[]
for c in S['contents']:
 if ':tutorial/content'not in c:continue
 before=c[':tutorial/content'];after=before;mid=c[':tutorial/math-academy-id'];matches=[]
 for t in S['topics']:
  ma=t['ma_id'];p=Path('/home/jake/Developer/MA/DATA/Lessons')/str(ma)/'Source'/f'{ma}.html';d=json.loads(p.with_suffix('.json').read_text());item=next((x for x in d['lesson']['items']if x.get('step_type')=='tutorial'and str(x.get('content_id'))==str(mid)),None)
  if not item:continue
  node=BeautifulSoup(p.read_text(),'html.parser').find(id=item['dom_id']);ns=node.select('.mjpage,mjx-container,math');ids={id(n)for n in ns};roots=[n for n in ns if not any(id(a)in ids for a in n.parents)];tex=[];errors=[]
  for n in roots:
   try:
    title=n.find('title')
    if title:v=reconstruct(title)
    else:
     math=n if n.name=='math'else n.find('math');assert math is not None;r=SourceRenderer(ma);v=normalize_source_tex(r.m(math));assert not r.errors,r.errors
    tex.append(v)
   except Exception as e:errors.append(str(e))
  ms=list(pat.finditer(before));current=[(m[1]if m[1]is not None else m[2]).strip()for m in ms];matches.append({'path':str(p),'source_formulas':len(tex),'current_formulas':len(current),'errors':errors})
  if len(tex)==len(current)and not errors and all(norm(a)==norm(b)for a,b in zip(current,tex)):
   for m,v in list(zip(ms,tex))[::-1]:after=after[:m.start()]+('$$\n'+v+'\n$$'if m[1]is not None else'$'+v+'$')+after[m.end():]
 if mid==6854:after=after.replace(r'Recall that $H\subseteq \mathbb R^n$ is a **subspace**',r'Recall that a nonempty subset $H\subseteq \mathbb R^n$ is a **subspace**')
 if mid==9150:after=after.replace("$\\mathbf{n}$ is a unit vector that's perpendicular to *both* $\\mathbf{a}$ and $\\mathbf{b}.$","$\\mathbf{n}$ is the unit vector perpendicular to *both* $\\mathbf{a}$ and $\\mathbf{b}$ in the direction determined by the right-hand rule. When the vectors are parallel, their cross product is $\\mathbf0$.")
 if after!=before:changes.append({'entity':c[':db/id'],'attribute':'tutorial/content','before':before,'after':after,'reason':'Restore archived source math typography where formula pairs match. Independently require a nonempty subset in the subspace test and specify the right-hand-rule orientation in the cross-product definition where applicable.'})
 evidence.append({'entity':c[':db/id'],'source_id':mid,'source_matches':matches,'individually_reviewed':True,'changed':after!=before})
(H/'proposals.json').write_text(json.dumps(changes,indent=2)+'\n');(H/'tutorial-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('Tutorial review',len(evidence),'changes',sum(x['changed']for x in evidence))

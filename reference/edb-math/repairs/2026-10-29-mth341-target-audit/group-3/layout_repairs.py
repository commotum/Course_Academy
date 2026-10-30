import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());source=json.loads((H/'source-proposals.json').read_text());completions=json.loads((H/'completion-proposals.json').read_text());changes={(p['entity'],p['attribute']):p for p in source+completions};extra=[];proof=[]
def add(eid,attr,before,after,reason):
 if before==after:return
 key=(eid,attr)
 if key in changes:changes[key]['after']=after;changes[key]['reason']+=' '+reason
 else:changes[key]={'entity':eid,'attribute':attr,'before':before,'after':after,'reason':reason}
 proof.append({'entity':eid,'attribute':attr,'reason':reason})
region_ids={q for t,k,q in S['links']if t==17592186051063}
for q in S['questions']:
 if q[':db/id']not in region_ids:continue
 for attr in['question/problem','question/worked-solution']:
  before=q.get(':'+attr)
  if not before:continue
  text=changes.get((q[':db/id'],attr),{}).get('after',before)
  # Only a bare set fence directly followed by (x,y), never field/control braces.
  text=re.sub(r'(?<!\\)\{\(x,y\)',r'\\{(x,y)',text)
  # Original content splits some set fences across inline math/control fragments.
  text=text.replace('$}$',r'$\}$')
  for m in list(re.finditer(r'\$\$([\s\S]*?)\$\$|(?<!\$)\$([^$]*?)\$(?!\$)',text))[::-1]:
   body=m[1]if m[1]is not None else m[2]
   if r'\{(x,y)'not in body or r'\in'not in body:continue
   stripped=body.rstrip().rstrip('.')
   if stripped.endswith('}')and not stripped.endswith(r'\}'):
    end=body.rfind('}');body=body[:end]+r'\}'+body[end+1:];text=text[:m.start()]+('$$'+body+'$$'if m[1]is not None else'$'+body+'$')+text[m.end():]
  add(q[':db/id'],attr,before,text,'Restore visible set-builder braces omitted by TeX grouping; preserve coordinate domain, inequality signs, diagrams, and field keys.')
# Source scalar relation typo and nonunique wording; the selected plane is a valid example.
q=next(q for q in S['questions']if q[':db/id']==17592186304926);attr='question/problem';before=q[':'+attr];cur=changes.get((q[':db/id'],attr),{}).get('after',before);add(q[':db/id'],attr,before,cur.replace('and is parallel to the two distinct lines','and is parallel to the plane determined by the two distinct parallel lines'),'Independent mathematical correction: parallel line directions alone allow many planes; require parallelism to the uniquely determined plane of the two distinct parallel lines, matching the source solution and existing unique key.')
sol=r'The two lines have direction vectors $\mathbf d_1=\langle1,1,1\rangle$ and $\mathbf d_2=\langle-2,-2,-2\rangle=-2\mathbf d_1$, so they are parallel. Their base points are $P(-1,5,7)$ and $Q(0,3,-19)$. The vector between them is'+ '\n\n$$\n'+r'\mathbf u=\overrightarrow{PQ}=\langle1,-2,-26\rangle.'+'\n$$\n\n'+r'The plane determined by the two lines has direction span $\operatorname{span}\{\mathbf d_1,\mathbf u\}$. These vectors are independent because $\mathbf d_1\times\mathbf u=\langle-24,27,-3\rangle\ne\mathbf0$. A parallel plane through $C(1,4,-14)$ has the same direction span, hence its parametric equation is'+ '\n\n$$\n'+r'\mathbf r=\langle1,4,-14\rangle+s\langle1,1,1\rangle+t\langle1,-2,-26\rangle,\qquad s,t\in\mathbb R.'+'\n$$\n\n'+r'This is the unique listed plane with that direction span passing through $C$.'

add(q[':db/id'],'question/worked-solution',q[':question/worked-solution'],sol,'Independent mathematical correction: fix reversed scalar relation and use the uniquely determined direction plane of the two distinct parallel lines.')
# Embed the source two-component cross-product values as vectors in R^3.
q=next(q for q in S['questions']if q[':db/id']==17592186660905)
for attr in['question/problem','question/worked-solution']:
 before=q[':'+attr];cur=changes.get((q[':db/id'],attr),{}).get('after',before)
 for a,b in [('⟨1,5⟩','⟨1,5,0⟩'),('⟨-2,4⟩','⟨-2,4,0⟩'),('⟨2,10⟩','⟨2,10,0⟩'),('⟨6,-12⟩','⟨6,-12,0⟩'),('⟨8,\\,-2⟩','⟨8,\\,-2,0⟩')]:cur=cur.replace(a,b)
 if attr=='question/problem':cur=cur.replace('{{field-2}}$⟩$','{{field-2}}$,0⟩$')
 add(q[':db/id'],attr,before,cur,'Independent mathematical correction: cross-product outputs are three-dimensional; append a fixed zero third component while preserving the two existing response fields and canonical scalar answers.')
(H/'proposals.json').write_text(json.dumps(list(changes.values()),indent=2)+'\n');(H/'layout-and-math-evidence.json').write_text(json.dumps(proof,indent=2)+'\n');print('Combined',len(changes),'proposals')

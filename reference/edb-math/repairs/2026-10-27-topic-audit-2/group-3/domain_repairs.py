import json
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};props={(r['entity'],r['attribute']):r for r in json.loads((H/'proposals.json').read_text())};changes=[]
def add(e,a,after,proof):
 q=Q[e];before=q[':'+a];ev={'classification':'authored mathematical domain/completeness repair; original source also omits this condition','source_identity':q.get(':question/math-academy-id'),'proof':proof,'keys_choices_ids_unchanged':True};r={'entity':e,'attribute':a,'before':before,'after':after,'reason':'State the branch/domain needed by the existing separated family and account for excluded equilibrium solutions.','evidence':ev,'confidence':'high'};props[e,a]=r;changes.append(r)
for e,condition,proof in [
 (17592186069532,r'x^2+x+C>0','Taking square roots of y=((x²+x+C)/2)² recovers (x²+x+C)/2 only on the positive branch; y=0 is explicitly excluded by the prompt.'),
 (17592186348253,r'\frac{x^{3/2}}3+K>0','The original sqrt(xy) has real domain xy>0. Splitting it into sqrt(x)sqrt(y) requires x>0,y>0. On x<0,y<0 another family is y=−((−x)^(3/2)/3+K)² with positive bracket.'),
 (17592186351479,r'3\sqrt{x}+K>0','The original sqrt(xy) has real domain xy>0. The source splitting requires x>0,y>0. On x<0,y<0 another family is y=−(3sqrt(−x)+K)^(2/3) with positive bracket.')]:
 q=Q[e];s=props.get((e,'question/worked-solution'),{}).get('after',q[':question/worked-solution']);s+='\n\nUse this family on a connected interval where $'+condition+'$. This condition preserves the positive square-root branch used before raising both sides to a power.'
 if e!=17592186069532:
  s+=' The calculation above works in the stated positive quadrant; $\\sqrt{xy}=\\sqrt{x}\\sqrt{y}$ is valid there.';p=q[':question/problem']+' Work in the region $x>0$ and $y>0$.';add(e,'question/problem',p,proof)
 add(e,'question/worked-solution',s,proof)
for e in [17592186275108,17592186357461]:
 q=Q[e];p=q[':question/problem'].replace('find the general solution','find the nonzero solution family');s=props.get((e,'question/worked-solution'),{}).get('after',q[':question/worked-solution']);s+='\n\nThe division by $v$ assumes $y\\ne0$. The equilibrium solution $y=0$ also satisfies the original differential equation on any interval with $x\\ne0$; it is not represented by the logarithmic family above.';proof='Direct substitution gives yprime=0 and RHS=0 for y=0,x≠0. The source transformation divides by v (equivalently y), so the logarithmic family excludes this valid equilibrium.';add(e,'question/problem',p,proof);add(e,'question/worked-solution',s,proof)
(H/'proposals.json').write_text(json.dumps(list(props.values()),indent=2));(H/'domain-proposals.json').write_text(json.dumps(changes,indent=2));print('authored domain/completeness repairs',len(changes),'all props',len(props))

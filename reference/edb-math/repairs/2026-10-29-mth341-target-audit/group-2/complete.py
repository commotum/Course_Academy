import json,re,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from algebra import scalar,matrices
sys.path.insert(0,str(H.parents[4]/'scripts'));from question_capture.math_format import matrix_tex
S=json.loads((H/'current.json').read_text());qs={q[':db/id']:q for q in S['questions']};owners={q:k for t,k,q in S['links']};ks={k[':db/id']:k for k in S['knowledge_points']};proposals=[];proof=[]
T=lambda a:matrix_tex([[sp.latex(c)for c in row]for row in a.tolist()]);D=lambda s:'\n\n$$\n'+s+'\n$$\n\n'
fixed={17592186115813:17592186113817,17592186115851:17592186114047,17592186120402:17592186118527,17592186120404:17592186118540,17592186125012:17592186122676,17592186125016:17592186122697}
for eid,q in qs.items():
 if q.get(':question/worked-solution'):continue
 a=matrices(q[':question/problem'])[0]['matrix'];kp=ks[owners[eid]];f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];pr={};name='B'if eid==17592186115758 else'C'
 if eid in[17592186115756,17592186115758]:
  aug=a.row_join(sp.eye(4));rows=[(0,2,-3),(3,0,-5)]if eid==17592186115756 else[(2,1,1),(3,2,-5)];sol='Augment the matrix with the identity, and use row operations to turn the left side into $I$.'+D('['+name+r'\mid I]='+T(aug))
  for target,source,factor in rows:
   old=aug.copy();aug[target,:]=old[target,:]+factor*old[source,:];sol+='Apply $R_{'+str(target+1)+'}:=R_{'+str(target+1)+'}'+('+'if factor>=0 else'')+str(factor)+'R_{'+str(source+1)+'}$:'+D(T(aug))
  inv=aug[:,4:];assert aug[:,:4]==sp.eye(4) and a*inv==inv*a==sp.eye(4);sol+='The right side is the inverse, so'+D(name+'^{-1}='+T(inv)+'.');right=next(c for c in choices if matrices(c[':answer/value'])[0]['matrix']==inv);pr={'inverse':inv.tolist(),'both_products_identity':True,'row_operations':rows}
 elif eid==17592186115813:
  b=a.copy();b.row_swap(2,3);c=b.copy();c[1,:]=b[1,:]-2*b[3,:];assert c==sp.eye(4);right=next(c for c in choices if c[':db/id']==fixed[eid]);sol='First interchange the third and fourth rows:'+D(r'R_3\leftrightarrow R_4:\quad'+T(a)+r'\sim'+T(b))+r'Then subtract twice the new fourth row from the second row:'+D(r'R_2:=R_2-2R_4:\quad'+T(b)+r'\sim'+T(c)+'.')+'Thus, the required operations are $R_3\leftrightarrow R_4$ followed by $R_2:=R_2-2R_4$.';pr={'intermediate':b.tolist(),'final_identity':c.tolist()}
 elif eid==17592186115851:
  vals=[];sol='Apply the two operations in the stated order, using the new first row in the second operation.'
  for label,m in zip('ABC',matrices(q[':question/problem'])):
   b=m['matrix'].copy();b[0,:]=b[0,:]-b[1,:];c=b.copy();c[1,:]=b[1,:]-2*b[0,:];vals.append(c==sp.eye(2));sol+=D(label+':\quad'+T(m['matrix'])+r'\sim'+T(b)+r'\sim'+T(c))
  assert vals==[False,False,True];right=next(c for c in choices if c[':db/id']==fixed[eid]);sol+='Only $C$ becomes the identity matrix.';pr={'A_B_C_identity_results':vals}
 elif eid in[17592186120402,17592186120404,17592186120425]:
  i=1;terms=[]
  if eid==17592186120404:
   # Canonical column expansion family: use column 3.
   j=2;terms=[sp.latex(a[ii,j])+r'(-1)^{'+str(ii+1)+'+'+str(j+1)+'}'+T(a.minor_submatrix(ii,j)).replace('bmatrix','vmatrix')for ii in range(4)if a[ii,j]!=0];method='third column'
  else:terms=[sp.latex(a[i,j])+r'(-1)^{'+str(i+1)+'+'+str(j+1)+'}'+T(a.minor_submatrix(i,j)).replace('bmatrix','vmatrix')for j in range(4)if a[i,j]!=0];method='second row'
  sol='Expand along the '+method+'. Terms with a zero entry vanish. The cofactor signs are $(-1)^{i+j}$.'+D(r'\det(A)='+ '+'.join(terms)+'.');det=a.det();sol+='Evaluating the smaller determinants gives'+D(r'\det(A)='+sp.latex(det)+'.');right=next(c for c in choices if c[':db/id']==fixed[eid])if eid in fixed else next(c for c in choices if scalar(c[':answer/value'])==det);pr={'matrix':a.tolist(),'determinant':det,'method':method}
 elif eid in[17592186125012,17592186125016]:
  l=sp.Symbol('lambda');poly=(a-l*sp.eye(3)).det();roots=sorted(a.eigenvals().keys());right=next(c for c in choices if c[':db/id']==fixed[eid]);sol=r'The eigenvalues satisfy the characteristic equation $\det(A-\lambda I)=0$. We have'+D(r'A-\lambda I='+T(a-l*sp.eye(3))+'.')
  if eid==17592186125012:sol+='This matrix is triangular, so its determinant is the product of the diagonal entries.'
  else:sol+='Expanding the determinant and factoring gives'
  sol+=D(r'\det(A-\lambda I)='+sp.latex(sp.expand(poly))+'='+sp.latex(sp.factor(poly))+'=0.')+'Therefore, the real eigenvalues are $'+', '.join(sp.latex(v)for v in roots)+'$.';pr={'characteristic_polynomial':poly,'factorization':sp.factor(poly),'eigenvalues':roots}
 else:raise AssertionError(eid)
 assert not f.get(':answer-field/correct');proposals.extend([{'entity':f[':db/id'],'attribute':'answer-field/correct','before':None,'after':right[':db/id'],'reason':'Complete missing correct link with independently solved existing owned choice.'},{'entity':eid,'attribute':'question/worked-solution','before':None,'after':sol.strip(),'reason':'Authored completion using the owning KP canonical example method and exact algebra.'}]);proof.append({'question':eid,'canonical_example':kp[':knowledge-point/canonical-example'][':db/id'],'knowledge_point':kp[':db/id'],'correct_choice':right[':db/id'],'authored_not_observed':True,'proof':pr})
(H/'completion-proposals.json').write_text(json.dumps(proposals,default=str,indent=2)+'\n');(H/'completion-evidence.json').write_text(json.dumps(proof,default=str,indent=2)+'\n');print('Completed',len(proof))

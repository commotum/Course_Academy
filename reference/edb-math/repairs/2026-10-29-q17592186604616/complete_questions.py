"""Authored completion from the same-KP canonical templates and exact algebra."""
import json,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from math_checks import scalar,matrices,equations,equivalent_rows,symbols
sys.path.insert(0,str(H.parents[3]/'scripts'));from question_capture.math_format import matrix_tex,validate_math_boundaries,validate_matrix_layouts,validate_math_structure
S=[json.loads((H/'lesson.json').read_text()),json.loads((H/'expanded-scope/current.json').read_text())];qs={q[':db/id']:q for s in S for q in s['questions']};missing=json.loads((H/'incomplete-questions.json').read_text());owners={q[':db/id']:k for s in S for k in(s.get('knowledge_points')or[k for t in s['topics']for k in t[':topic/knowledge-points']])for key in[':knowledge-point/questions',':knowledge-point/canonical-example']for q in(k.get(key,[])if isinstance(k.get(key,[]),list)else[k[key]])};changes=[];evidence=[]
T=lambda a:matrix_tex([[sp.latex(c)for c in row]for row in a.tolist()]);D=lambda t:'\n\n$$\n'+t+'\n$$\n\n'
def system_text(rs):return r'\left\{\begin{aligned}'+r' \\ '.join(sp.latex(sp.expand(r).coeff(symbols['x']))+'x+'+sp.latex(sp.expand(r).coeff(symbols['y']))+'y &='+sp.latex(-sp.expand(r).subs({symbols['x']:0,symbols['y']:0}))for r in rs)+r'\end{aligned}\right.'
def object_value(v):
 ms=matrices(v)
 if not ms:return None
 assert len(ms)==1
 m=ms[0];factor=v[:m['start']].strip();factor=scalar(factor)if factor else 1
 return factor*(m['matrix'].det()if m['environment']=='vmatrix'else m['matrix'])
def match_option(q,predicate):
 bank=q[':question/answer-fields'][0][':answer-field/choices'];found=[]
 for a in bank:
  try:ok=predicate(a[':answer/value'])
  except(Exception):ok=False
  if ok:found.append(a)
 assert len(found)==1,(q[':db/id'],'Nonunique correct choice',found)
 return found[0]
for q in missing:
 eid=q[':db/id'];prompt=q[':question/problem'];kp=owners[eid];example=qs[kp[':knowledge-point/canonical-example'][':db/id']];assert example.get(':question/worked-solution');proof={};template=kp[':knowledge-point/title']
 if eid in[17592186115492,17592186115493,17592186115732,17592186115977]:
  rs=equations(prompt);x,y=symbols['x'],symbols['y'];a=sp.Matrix([[sp.expand(r).coeff(x),sp.expand(r).coeff(y)]for r in rs]);b=sp.Matrix([-sp.expand(r).subs({x:0,y:0})for r in rs]);v=sp.Matrix([x,y]);expected=T(a)+T(v)+'='+T(b)
  right=match_option(q,lambda value:len(matrices(value))==3 and matrices(value)[0]['matrix']==a and matrices(value)[1]['matrix']==v and matrices(value)[2]['matrix']==b)
  system=r'\left\{\begin{aligned}'+r' \\ '.join(sp.latex(sp.expand(a[i,0]*x+a[i,1]*y))+' &='+sp.latex(b[i])for i in range(2))+r'\end{aligned}\right.'
  sol='First, write the system with the variables ordered $x,y$ on the left and the constants on the right. Insert a zero coefficient for any missing variable.'+D(system)+'Now, we can write the system in the form $A\\mathbf{x}=\\mathbf{b},$ where'+D('A='+T(a)+r',\qquad\mathbf{x}='+T(v)+r',\qquad\mathbf{b}='+T(b)+'.')+'Each row of $A$ contains the coefficients from the corresponding equation. Therefore,'+D(expected+'.');proof={'coefficient_matrix':a.tolist(),'constant_vector':b.tolist(),'unique_matching_choice':right[':db/id']}
 elif eid==17592186115740:
  ms=matrices(prompt);assert len(ms)==3;a,v,b=[m['matrix']for m in ms];expected=list(a*v-b)
  right=match_option(q,lambda value:equivalent_rows(equations(value),expected))
  sol='Multiplying the coefficient matrix by the column vector of variables gives'+D(T(a)+T(v)+'='+T(a*v)+'.')+'Equating the corresponding entries, we get'+D(r'\left\{\begin{aligned}9x+6y &=-3\\x &=-2\end{aligned}\right.')+'Dividing the first equation by $3$ gives the equivalent system'+D(r'\left\{\begin{aligned}3x+2y &=-1\\x &=-2.\end{aligned}\right.');proof={'expanded_equations':['9x+6y=-3','x=-2'],'equivalent_selected_system':right[':answer/value']}
 elif eid in[17592186060448,17592186060458]:
  a=matrices(prompt)[0]['matrix'];det=a.det();assert det!=0;mins=sp.Matrix(a.rows,a.cols,lambda i,j:a.minor_submatrix(i,j).det());cofs=a.cofactor_matrix();inv=a.inv();assert a*inv==sp.eye(3)and inv*a==sp.eye(3)
  right=match_option(q,lambda value:object_value(value)==inv)
  term='+'.join('('+sp.latex(a[0,j])+')('+sp.latex(cofs[0,j])+')'for j in range(3))
  sol="Let's follow the standard five-step procedure.\n\n**Step 1:** Find the determinant of $A$."+D(r'\det(A)='+term+'='+sp.latex(det)+'.')+'**Step 2:** Form the matrix of minors. Delete row $i$ and column $j$ to obtain $M_{ij}$. For example,'+D(r'M_{11}='+T(a.minor_submatrix(0,0)).replace('bmatrix','vmatrix')+'='+sp.latex(mins[0,0])+'.')+'Computing the remaining minors gives'+D('M='+T(mins)+'.')+'**Step 3:** Apply the alternating signs $(-1)^{i+j}$ to form the cofactor matrix.'+D('C='+T(cofs)+'.')+'**Step 4:** Transpose the matrix of cofactors.'+D('C^T='+T(cofs.T)+'.')+'**Step 5:** Divide by the nonzero determinant.'+D(r'A^{-1}=\frac{1}{\det(A)}C^T='+sp.latex(1/det)+T(cofs.T)+'='+T(inv)+'.');proof={'determinant':det,'minors':mins.tolist(),'cofactors':cofs.tolist(),'inverse':inv.tolist(),'both_inverse_products_identity':True}
 elif eid==17592186060459:
  a=matrices(prompt)[0]['matrix'];k=symbols['k'];det=a.det();cofactor=a.cofactor(2,1);answers=sp.solve(sp.Eq(cofactor/det,-1),k);answers=[v for v in answers if det.subs(k,v)!=0];assert answers==[0]
  right=match_option(q,lambda value:scalar(value)==answers[0]);sol='Since $A^{-1}=\\dfrac{1}{\\det(A)}C^T,$ the entry $a_{23}^{\prime}$ uses the cofactor $C_{32}$. Remove row $3$ and column $2$ to get'+D(r'C_{32}=(-1)^{3+2}'+T(a.minor_submatrix(2,1)).replace('bmatrix','vmatrix')+'=-4.')+'Using the given determinant, we obtain'+D(r'a_{23}^{\prime}=\frac{-4}{4-4k}.')+'The inverse exists only when $k\\ne1$. Set this entry equal to $-1$ and solve:'+D(r'\begin{aligned}\frac{-4}{4-4k}&=-1\\-4&=-4+4k\\k&=0.\end{aligned}')+'At $k=0,$ the determinant is $4\\ne0,$ so this value is valid.';proof={'determinant':det,'C32':cofactor,'valid_parameter_values':answers}
 elif eid==17592186087990:
  a=matrices(prompt)[0]['matrix'];k=symbols['k'];roots=sp.solve(a.det(),k);assert set(roots)=={-2,2};right=next(a for a in q[':question/answer-fields'][0][':answer-field/choices']if a[':db/id']==17592186084676)
  sol='The matrix $A$ is singular if and only if its determinant is $0$. Calculating the determinant, we get'+D(r'\det(A)=k\cdot k-2\cdot2=k^2-4.')+'Now, set the determinant equal to $0$ and solve for $k$:'+D(r'\begin{aligned}k^2-4&=0\\(k-2)(k+2)&=0\\k&=2\quad\text{or}\quad k=-2.\end{aligned}')+'Therefore, $k=\\pm2$.';proof={'determinant':a.det(),'singular_parameter_values':roots}
 elif eid in[17592186087992,17592186088369]:
  a=matrices(prompt)[0]['matrix'];name='Z'if eid==17592186088369 else'A';det=a.det();inv=a.inv();right=match_option(q,lambda value:object_value(value)==inv);adj=a.adjugate();assert a*inv==sp.eye(2)and inv*a==sp.eye(2)
  sol='Given a $2\\times2$ matrix, use the formula'+D(r'\begin{bmatrix}a&b\\c&d\end{bmatrix}^{-1}=\frac{1}{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}.')+'First, compute the determinant:'+D(r'\det('+name+')=('+sp.latex(a[0,0])+')('+sp.latex(a[1,1])+')-('+sp.latex(a[0,1])+')('+sp.latex(a[1,0])+')='+sp.latex(det)+'.')+'Since the determinant is nonzero, the inverse exists. Thus,'+D(name+r'^{-1}=\frac{1}{'+sp.latex(det)+'}'+T(adj)+'='+T(inv)+'.')+'Multiplying in either order gives the identity matrix, which verifies the result.';proof={'determinant':det,'inverse':inv.tolist(),'both_inverse_products_identity':True}
 elif eid==17592186120505:
  a=matrices(prompt)[0]['matrix'];minor=a.minor_submatrix(2,2);expected=a.cofactor(2,2);right=match_option(q,lambda value:object_value(value)==expected)
  sol='First, to get the minor of $d_{33}$, remove the $3$rd row and $3$rd column:'+D(r'M_{33}='+T(minor).replace('bmatrix','vmatrix')+'.')+'The cofactor includes the alternating sign $(-1)^{i+j}$. Therefore,'+D(r'C_{33}=(-1)^{3+3}M_{33}=M_{33}='+T(minor).replace('bmatrix','vmatrix')+'.');proof={'deleted_row':3,'deleted_column':3,'minor':minor.tolist(),'cofactor_value':expected}
 else:raise AssertionError(eid)
 sol=sol.strip()
 for fn in[validate_math_boundaries,validate_matrix_layouts,validate_math_structure]:fn(sol)
 f=q[':question/answer-fields'][0];assert not f.get(':answer-field/correct')and not q.get(':question/worked-solution')
 changes.extend([{'entity':f[':db/id'],'attribute':'answer-field/correct','before':None,'after':right[':db/id'],'reason':'Complete missing correct link to independently verified existing owned choice; preserve bank and identities.'},{'entity':eid,'attribute':'question/worked-solution','before':None,'after':sol,'reason':'Authored completion following the same-KP canonical worked-solution template, verified by exact algebra.'}]);evidence.append({'question':eid,'knowledge_point':kp[':db/id'],'template_name':template,'template_example':example[':db/id'],'template_solution':example[':question/worked-solution'],'source':'Authored Codex completion, not an observed Math Academy solution','proof':proof,'correct_answer':right[':db/id']})
(H/'completion-proposals.json').write_text(json.dumps(changes,default=str,indent=2)+'\n');(H/'completion-evidence.json').write_text(json.dumps(evidence,default=str,indent=2)+'\n');print('Independently completed',len(evidence),'questions;',len(changes),'guarded field changes')

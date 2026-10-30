"""Authored completions; retain existing entities and all option values."""
import json
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());evidence=[]
def put(e,a,before,after,reason,proof):
 p=next((p for p in P if p['entity']==e and p['attribute']==a),None)
 if p:p['after']=after;p['reason']+=','+reason;p.setdefault('additional_evidence',[]).append(proof)
 else:P.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':reason,'evidence':proof})
solutions={
'q-34331':(17592186118080,r'''A vector $\mathbf b$ lies in $\operatorname{Null}(A)$ exactly when $A\mathbf b=\mathbf0$. Compute each product:

$$
A\mathbf b_1=\begin{bmatrix}16\\-13\end{bmatrix},\qquad A\mathbf b_2=\begin{bmatrix}14\\0\end{bmatrix},\qquad A\mathbf b_3=\begin{bmatrix}-10\\2\end{bmatrix}.
$$

None of these is the zero vector, so none of the three vectors lies in $\operatorname{Null}(A)$.'''),
'q-34390':(17592186118135,r'''A vector $\mathbf b$ lies in $\operatorname{Null}(A)$ exactly when $A\mathbf b=\mathbf0$. Compute each product:

$$
A\mathbf b_1=\begin{bmatrix}0\\0\\0\end{bmatrix},\qquad A\mathbf b_2=\begin{bmatrix}0\\0\\0\end{bmatrix},\qquad A\mathbf b_3=\begin{bmatrix}4\\8\\2\end{bmatrix}.
$$

Therefore, $\mathbf b_1$ and $\mathbf b_2$ only lie in $\operatorname{Null}(A)$.'''),
'q-35141':(17592186118372,r'''Starting from $\mathbf u\cdot\mathbf v=11$, compute the dot product and solve:

$$
\begin{aligned}\frac4{x^2}x^4+4\cdot0+8x+7(-7)&=11\\4x^2+8x-60&=0\\x^2+2x-15&=0\\(x+5)(x-3)&=0.\end{aligned}
$$

The vector requires $x\ne0$, and both roots satisfy this restriction. Since $x<0$, the required root is $x=-5$.'''),
'q-47586':(17592186123605,r'''Since $\det(A)\ne0$, the matrix $A$ is invertible. Thus statement I is false.

The homogeneous equation $A\mathbf x=\mathbf0$ has only the trivial solution, so $\operatorname{Null}(A)=\{\mathbf0\}$. The empty set is linearly independent and its span is $\{\mathbf0\}$, so it is a basis of this null space. Thus the corrected statement II is true.

An invertible $n\times n$ matrix has a pivot in every column, so statement III is true. Therefore, the correct answer is II and III only.'''),
'q-39483':(17592186131368,r'''To extend the orthonormal set, find a unit vector $\mathbf x$ orthogonal to both given vectors. The equations are

$$
\frac{x_1-2x_3}{\sqrt5}=0,\qquad \frac{2x_1+2x_2+x_3}{3}=0.
$$

Hence $x_1=2x_3$ and $x_2=-\frac52x_3$, so $\mathbf x=t\begin{bmatrix}4\\-5\\2\end{bmatrix}$. Its norm is $3\sqrt5|t|$, so the unit-vector condition gives $|t|=\frac1{3\sqrt5}$. Therefore,

$$
|x_1|+|x_2|+|x_3|=\frac{4+5+2}{3\sqrt5}=\frac{11}{3\sqrt5}.
$$'''),
'q-39490':(17592186131375,r'''A set is orthogonal when every pair of distinct vectors has dot product zero. Denoting the vectors in each displayed set by subscripts, we obtain

$$
\begin{aligned}u_1\cdot u_2&=1+6-1-6=0,&u_1\cdot u_3&=2-2+2-2=0,&u_2\cdot u_3&=2-3-2+3=0,\\v_1\cdot v_2&=2-4+2=0,&v_1\cdot v_3&=-12+0+12=0,&v_2\cdot v_3&=-6+0+6=0,\\w_1\cdot w_2&=-8+2=-6.\end{aligned}
$$

Thus $U$ and $V$ are orthogonal, while $W$ is not. The correct answer is $U$ and $V$ only.'''),
'q-34524':(17592186149996,r'''To find a basis of the column space, reduce $A$ and select the corresponding pivot columns of the original matrix. Its reduced row echelon form is

$$
\begin{bmatrix}1&0&\frac32\\0&1&\frac12\\0&0&0\end{bmatrix}.
$$

The pivot columns are columns 1 and 2. Therefore,

$$
\mathcal B=\left\{\begin{bmatrix}2\\1\\3\end{bmatrix},\begin{bmatrix}-6\\-1\\1\end{bmatrix}\right\}
$$

is a basis of $\operatorname{Col}(A)$. The third column equals $\frac32$ times the first plus $\frac12$ times the second.'''),
'q-35676':(17592186150010,r'''Swap rows 1 and 3, divide row 2 by 3, and subtract twice row 2 from row 1. This gives the reduced row echelon form

$$
\begin{bmatrix}1&0&0\\0&0&1\\0&0&0\end{bmatrix}.
$$

Columns 1 and 3 are pivot columns. Select those columns from the original matrix:

$$
\mathcal B=\left\{\begin{bmatrix}0\\0\\1\end{bmatrix},\begin{bmatrix}0\\3\\2\end{bmatrix}\right\}.
$$

These independent vectors span the column space. A basis cannot include the zero second column.'''),
'q-75603':(17592186150836,r'''The first two columns are $\mathbf a_1=(1,0,1)^T$ and $\mathbf a_2=(0,5,0)^T$. Every linear combination has equal first and third components. However, $\mathbf a_4=(1,5,2)^T$ does not have equal first and third components, so it is outside their span.

Thus $\{\mathbf a_1,\mathbf a_2\}$ does not span $\operatorname{Col}(A)$ and is not a basis. The conditional request for $x_1x_2$ does not apply.''')}
for q in D['questions']:
 sid=q.get(':question/math-academy-id')
 if sid not in solutions:continue
 aid,solution=solutions[sid];assert not q.get(':question/worked-solution')
 owner=next(k for t,k,e in D['links']if e==q[':db/id']);kp=next(k for k in D['knowledge_points']if k[':db/id']==owner);canonical=kp.get(':knowledge-point/canonical-example',{}).get(':db/id');f=q[':question/answer-fields'][0];assert aid in [a[':db/id']for a in f[':answer-field/choices']]
 proof={'identity':sid,'basis_t':D['basis_t'],'authorship':'Locally authored completion; not an observed MA solution','canonical_example':canonical,'source_paths':sorted({s['path']for s in json.loads((H/'sources.json').read_text())if s['identity']==sid}),'correct_owned_answer':aid,'derivation':solution}
 put(q[':db/id'],'question/worked-solution',None,solution,'authored-completion',proof);put(f[':db/id'],'answer-field/correct',None,aid,'key-existing-owned-answer',proof);evidence.append(proof)
 if sid=='q-47586':
  current=next((p['after']for p in P if p['entity']==q[':db/id']and p['attribute']=='question/problem'),q[':question/problem']);after=current.replace('$Null(A)$ has no basis',r'$\operatorname{Null}(A)$ has the empty set as a basis');assert current!=after
  put(q[':db/id'],'question/problem',q[':question/problem'],after,'authored-mathematical-correction-empty-basis',{'source_defect':'Original has no basis is false; missing III-only answer. Clarify true empty-basis statement to preserve every answer value and all identities.','truths':[False,True,True],'all_options':{'I only':False,'I, II, and III':False,'II and III only':True,'I and II only':False,'II only':False}})
# Retained duplicate fields are still active, so link each to its own equivalent existing answer.
for fid,aid,proof in[(17592186118083,17592186118087,'Null(A)={(−2t,t):t∈R}; A(-2t,t)=0 and rank(A)=1.'),(17592186183181,17592186183186,'The missing axioms are A8 (distribution over vector addition) and A3 (addition of zero).'),(17592186183187,17592186183192,'Nonnegative functions are not closed under negative scalar multiplication; f=1, scalar −1 proves failure.')]:put(fid,'answer-field/correct',None,aid,'key-existing-owned-answer',{'independent_derivation':proof,'retained_duplicate_field':True})
(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');(H/'completion-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('Completions',len(evidence),'total proposals',len(P))

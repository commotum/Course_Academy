import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import validate_math_structure
D=json.loads((H/'current.json').read_text());Q={q[':question/math-academy-id']:q for q in D['questions']if':question/math-academy-id'in q};C={r['target']:r for r in json.loads((H/'completion-context.json').read_text())}
# Authored completions follow the same target KP methods; observed answers/IDs are reused.
solutions={
'q-43504':(17592186114093,r'''An elementary matrix is obtained by applying exactly one elementary row operation to the identity matrix $I_3$.

- $A$ is obtained by $R_3:=R_3+5R_1$.
- $C$ is obtained by $R_2:=R_2+5R_1$.
- $B$ requires both adding a multiple of $R_1$ to $R_3$ and scaling the diagonal entry in $R_3$. One row swap, one row scaling, or one row addition cannot produce both changes from $I_3$.

Therefore, $A$ and $C$ only are elementary matrices.'''),
'q-34250':(17592186118016,r'''Using the properties of addition/subtraction and scalar multiplication of vectors to isolate the $q$ term, we get

$$
\begin{aligned}
q a_2&=b-7a_1\\
q\begin{bmatrix}8\\6\end{bmatrix}
&=\begin{bmatrix}32\\17\end{bmatrix}-7\begin{bmatrix}0\\-1\end{bmatrix}\\
&=\begin{bmatrix}32\\24\end{bmatrix}.
\end{aligned}
$$

Both coordinates give $q=4$.'''),
'q-34464':(17592186118158,r'''We need a linearly independent subset that has the same span. Place the given vectors in the columns of a matrix:

$$
\begin{bmatrix}5&-1&2\\0&7&-14\\0&0&0\end{bmatrix}.
$$

This matrix is already in row echelon form, with pivots in the first and second columns. The third column is $-2$ times the second, so $a_3=-2a_2$ can be removed without changing the span. Select the first and second columns from the original matrix:

$$
B=\left\{\begin{bmatrix}5\\0\\0\end{bmatrix},\begin{bmatrix}-1\\7\\0\end{bmatrix}\right\}.
$$'''),
'q-34574':(17592186118223,r'''Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x$, we get

$$
\begin{aligned}
2a-6x&=b\\
x&=\frac16(2a-b)\\
&=\frac16\left(\begin{bmatrix}-4\\10\\2\\6\end{bmatrix}-\begin{bmatrix}8\\4\\-22\\-6\end{bmatrix}\right)\\
&=\frac16\begin{bmatrix}-12\\6\\24\\12\end{bmatrix}
=\begin{bmatrix}-2\\1\\4\\2\end{bmatrix}.
\end{aligned}
$$

Therefore, $x_1+x_2=-2+1=-1$.'''),
'q-34807':(17592186118302,r'''A matrix with rank $4$ must have at least four rows and four columns. This excludes $A$, $C$, and $E$, which have fewer than four rows or columns.

The remaining matrices are in row echelon form. Matrix $D$ has three nonzero rows, hence three pivot columns, so its rank is $3$. Matrix $B$ has four nonzero rows with pivots in columns $1$, $2$, $3$, and $4$, so its rank is $4$.

Therefore, the correct matrix is $B$.'''),
'q-34825':(17592186118315,r'''The rank of a matrix is the number of its pivot columns. Since $P$ has $5$ pivot columns,

$$
\operatorname{rank}(P)=5.
$$'''),
'q-35270':(17592186118419,r'''The rank is the number of pivot columns in row echelon form.

Matrix $A$ has only two rows, so its rank is at most $2$.

For $B$, apply $R_2:=R_2-3R_3$ to obtain a row with entries $0,0,0,-5,-1$. This row, together with the rows whose last two entries are $2,3$ and $0,3$, spans a two-dimensional space in columns $4$ and $5$. Along with the pivots in columns $1$ and $3$, this gives four pivot columns. Thus $\operatorname{rank}(B)=4$.

For $C$, the second column is zero. The first, third, and fourth columns are independent: a $3\times3$ minor using rows $1$, $2$, and $4$ has determinant $-2$. Hence $\operatorname{rank}(C)=3$.

Therefore, $B$ only has rank $4$.'''),
'q-72462':(17592186119191,r'''Multiplying an $n\times n$ matrix by a scalar $k$ multiplies each of its $n$ rows by $k$. Consequently,

$$
\det(kA)=k^n\det(A).
$$

Here $k=5$, $n=3$, and $\det(A)=4$, so

$$
\det(5A)=5^3\cdot4=125\cdot4=500.
$$'''),
'q-74723':(17592186119221,r'''A basis is a linearly independent set that spans the given space. By inspection,

$$
a_1=\begin{bmatrix}3\\1\end{bmatrix}
=\begin{bmatrix}2\\2\end{bmatrix}+\begin{bmatrix}1\\-1\end{bmatrix}
=a_2+a_3.
$$

Thus $a_1$ can be removed without changing the span. The vectors $a_2$ and $a_3$ are not parallel, so they are linearly independent. Therefore, a basis is

$$
B=\left\{\begin{bmatrix}2\\2\end{bmatrix},\begin{bmatrix}1\\-1\end{bmatrix}\right\}.
$$'''),
'q-74724':(17592186119227,r'''A basis is a linearly independent set that spans the given space. By inspection,

$$
a_3=\begin{bmatrix}3\\3\end{bmatrix}
=\begin{bmatrix}2\\0\end{bmatrix}+\begin{bmatrix}1\\3\end{bmatrix}
=a_1+a_2.
$$

Thus $a_3$ can be removed without changing the span. The vectors $a_1$ and $a_2$ are not parallel, so they are linearly independent. Therefore, a basis is

$$
B=\left\{\begin{bmatrix}2\\0\end{bmatrix},\begin{bmatrix}1\\3\end{bmatrix}\right\}.
$$'''),
'q-75580':(17592186119253,r'''We want to find coefficients $x_1,x_2$ such that $a_3=x_1a_1+x_2a_2$. Equating coordinates gives

$$
\left\{\begin{aligned}x_1-x_2&=2\\-2x_1+4x_2&=-2.\end{aligned}\right.
$$

Add twice the first equation to the second to obtain $2x_2=2$, so $x_2=1$. The first equation then gives $x_1=3$.

The coefficient matrix has a pivot in both columns, so $a_1$ and $a_2$ are linearly independent. Also $a_3=3a_1+a_2$, so they span the same space as the three given vectors. Thus $B$ is a basis, and

$$
x_1x_2=3\cdot1=3.
$$'''),
'q-35707':(17592186122005,r'''To test linear dependence, solve

$$
x_1p_1(t)+x_2p_2(t)=0.
$$

Substituting the given polynomials and collecting coefficients gives

$$
( x_1+2x_2 )+(-x_1-3x_2)t+x_1t^2=0.
$$

This identity holds for all $t$ only if every coefficient is zero. The coefficient of $t^2$ gives $x_1=0$, and the constant coefficient then gives $2x_2=0$, so $x_2=0$.

The only solution is the zero solution. Therefore, the set is linearly independent; there is no nonzero solution from which to form the requested ratio.'''),
'q-94851':(17592186124068,r'''Examine the statements in turn.

- Statement I is true. If $c_1+c_2t+c_3t^3=0$ for every $t$, comparison of coefficients gives $c_1=c_2=c_3=0$. Thus $\{1,t,t^3\}$ is linearly independent.
- Statement II is false. Every linear combination of $1,t,t^3$ has coefficient $0$ on $t^2$, whereas $-5t^3+t^2+t$ has coefficient $1$ on $t^2$.
- Statement III is false. The set does not span $\mathbb{R}_3[t]$ because, for example, it cannot represent $t^2$.

Therefore, the correct answer is I only.'''),
'q-42532':(17592186132416,r'''To find the elementary matrix $E$, apply the given row operation to the identity matrix:

$$
I_3=\begin{bmatrix}1&0&0\\0&1&0\\0&0&1\end{bmatrix}
\quad\xrightarrow{R_2:=-\frac13R_2}\quad
E=\begin{bmatrix}1&0&0\\0&-\frac13&0\\0&0&1\end{bmatrix}.
$$

Applying a row operation to $A$ is equivalent to multiplying on the left by the corresponding elementary matrix. Therefore, the required product is

$$
EA=\begin{bmatrix}1&0&0\\0&-\frac13&0\\0&0&1\end{bmatrix}A.
$$''')}
links=[];proposals=[]
for ident,(aid,solution)in solutions.items():
 q=Q[ident];assert not q.get(':question/worked-solution');fs=q[':question/answer-fields'];assert len(fs)==1;f=fs[0];assert ':answer-field/correct'not in f;a=next(a for a in f[':answer-field/choices']if a[':db/id']==aid);validate_math_structure(solution)
 context=C[ident];evidence={'basis_t':9047,'kp':context['kp'],'canonical_example':context['canonical'][':db/id'],'nearby_example':context['nearby'][':db/id']if context['nearby']else None,'provenance':'Authored completion; independently solved from target values, following canonical KP method. Not represented as recovered original source.'}
 links.append({'question':q[':db/id'],'source':ident,'field':f[':db/id'],'attribute':'answer-field/correct','before':None,'after':aid,'answer':aid,'answer_uuid':a[':answer/id'],'answer_value':a[':answer/value'],'evidence':evidence,'confidence':'high'})
 proposals.append({'entity':q[':db/id'],'attribute':'question/worked-solution','before':None,'after':solution,'reason':'Complete missing worked solution using the target KP method and independently verified target values.','evidence':evidence,'confidence':'high'})
q=Q['q-42156'];f=next(f for f in q[':question/answer-fields']if f[':db/id']==17592186104026);a=next(a for a in f[':answer-field/choices']if a[':db/id']==17592186104028)
links.append({'question':q[':db/id'],'source':'q-42156','field':f[':db/id'],'attribute':'answer-field/correct','before':None,'after':a[':db/id'],'answer':a[':db/id'],'answer_uuid':a[':answer/id'],'answer_value':a[':answer/value'],'evidence':{'basis_t':9047,'derivation':'Independent solve of x−2y=1: x=1+2y for arbitrary real y. A particular solution alone is not the requested general solution. The existing worked solution states the same result.','ownership_issue':'Two radio fields share key selection; preserving both IDs and banks for parent review.'},'confidence':'high'})
(H/'missing-key-proposals.json').write_text(json.dumps(links,indent=2));(H/'completion-proposals.json').write_text(json.dumps(proposals,indent=2));print('proposed',len(links),'keys',len(proposals),'solutions')

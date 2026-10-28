import json,re,sys,copy,collections
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells,matrix_tex,system_tex,validate_math_structure
old=(R/'reference/edb-math/repairs/2026-10-27-lesson-1171/audit_math.py').read_text();helper=old[old.index('def scalar(s):'):old.index('for q in Q:')];helper=helper.replace("s=s.replace('⁡','')","s=re.sub(r'x_\\{(\\d+)\\}',r'x\\1',s);s=s.replace('⁡','')").replace("r'a\\d+'","r'[ax]\\d+'").replace("n.startswith('a')","n.startswith(('a','x'))").replace("{'b','c','d'}","{'b','c','d','k'}").replace("'b','c','d'}","'b','c','d','k'}");exec(helper)
D=json.loads((H/'current.json').read_text());contexts=json.loads((H/'completion-context.json').read_text());ps=json.loads((H/'proposals.json').read_text());keys=[];proof=[]
# Each solution follows its recorded canonical example's method, with independently evaluated target parameters.
solutions={
'q-157694':('3',r'''Construct the matrix $M$ whose columns are $a,b,c,d$. The volume equals $|\det(M)|$.

$$
\det(M)=\begin{vmatrix}2&1&-2&1\\0&-1&0&0\\-1&1&3&-2\\3&2&0&0\end{vmatrix}
=-\begin{vmatrix}2&-2&1\\-1&3&-2\\3&0&0\end{vmatrix}
=-3\begin{vmatrix}-2&1\\3&-2\end{vmatrix}=-3(4-3)=-3.
$$

Therefore, the volume is $|-3|=3$.'''),
'q-42471':('-27',r'The matrix $A=-3I_3$ is diagonal. The determinant of a triangular matrix is the product of its diagonal entries, so $\det(A)=(-3)(-3)(-3)=-27$.'),
'q-42884':('-50',r'The determinant of a triangular matrix is the product of its diagonal entries. Therefore, the determinant is $2\cdot5\cdot(-1)\cdot5=-50$.'),
'q-42955':('12',r'''The third row contains three zeros, so expand along that row:

$$
\det(A)=2(-1)^{3+2}\begin{vmatrix}1&1&2\\2&4&2\\1&0&0\end{vmatrix}
=-2\begin{vmatrix}1&2\\4&2\end{vmatrix}
=-2(2-8)=12.
$$'''),
'q-34936':('II only',r'''Since $\operatorname{Col}(A)=\mathbb{R}^6$, the invertible matrix theorem gives $\operatorname{rank}(A)=6$, $A$ invertible, and $\dim(\operatorname{Null}(A))=0$.

Statement I is false, statement II is true, and statement III is false. Therefore, the correct answer is "II only."'''),
'q-176873':('I, II, and III',r'''Statement I is true because $A$ is $2\times2$. Also,

$$
AA^T=\begin{bmatrix}-1&0\\0&1\end{bmatrix}\begin{bmatrix}-1&0\\0&1\end{bmatrix}=I_2.
$$

Thus statement II is true. A square matrix with $AA^T=I$ is orthogonal, so statement III is true. The correct answer is "I, II, and III."'''),
'q-176874':('I only',r'''Statement I is true because $A$ is $3\times3$. However,

$$
AA^T=\begin{bmatrix}\frac54&0&0\\0&1&0\\0&0&\frac54\end{bmatrix}\ne I_3.
$$

Therefore, statement II is false and $A$ is not orthogonal, so statement III is false. The correct answer is "I only."'''),
'q-39865':(r'\begin{bmatrix}-\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{bmatrix}',r'''The inverse of an orthogonal matrix equals its transpose. Therefore,

$$
D^{-1}=D^T=\begin{bmatrix}-\frac{1}{\sqrt2}&\frac{1}{\sqrt2}\\-\frac{1}{\sqrt2}&-\frac{1}{\sqrt2}\end{bmatrix}.
$$'''),
'q-43066':(r'A^{-1} = \begin{bmatrix}1 & 3 & 9 \\ 0 & 1 & 2 \\ 0 & 0 & -1\end{bmatrix}',r'''Write $A$ beside $I_3$ and perform the same row operations on both sides:

$$
[A\mid I_3]=\left[\begin{array}{ccc|ccc}1&-3&3&1&0&0\\0&1&2&0&1&0\\0&0&-1&0&0&1\end{array}\right].
$$

Apply $R_3\leftarrow-R_3$, then $R_2\leftarrow R_2-2R_3$, then $R_1\leftarrow R_1-3R_3$, and finally $R_1\leftarrow R_1+3R_2$. This gives

$$
[I_3\mid A^{-1}]=\left[\begin{array}{ccc|ccc}1&0&0&1&3&9\\0&1&0&0&1&2\\0&0&1&0&0&-1\end{array}\right].
$$

Therefore, $A^{-1}=\begin{bmatrix}1&3&9\\0&1&2\\0&0&-1\end{bmatrix}$.'''),
'q-78749':('$R_{3}:=R_{3} + 4R_{1}$\n$and$\n$R_{2}:=\\frac{1}{5}R_{2}$',r'''To change the first entry of row 3 from $-4$ to $0$, add four times row 1:

$$
R_3\leftarrow R_3+4R_1.
$$

To change the second-row pivot from $5$ to $1$, multiply row 2 by $\frac15$:

$$
R_2\leftarrow\frac15R_2.
$$

These operations give exactly the two displayed intermediate matrices. The final operation $R_3\leftarrow R_3+3R_2$ then produces $[I_3\mid Q^{-1}]$.'''),
'q-42004':(r'\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}',r'''Apply the distributive law $BA+BC=B(A+C)$. Here $C=-A$, so $A+C=0_{3\times3}$. Therefore,

$$
BA+BC=B0_{3\times3}=\begin{bmatrix}0&0&0\\0&0&0\\0&0&0\end{bmatrix}.
$$'''),
'q-42257':(r'\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}',r'''By the associative law, $ABC=A(BC)$. Compute the smaller product first:

$$
BC=\begin{bmatrix}2&-1&-2\\5&-5&-5\end{bmatrix}\begin{bmatrix}1\\0\\1\end{bmatrix}=\begin{bmatrix}0\\0\end{bmatrix}.
$$

Therefore, $ABC=A\begin{bmatrix}0\\0\end{bmatrix}=\begin{bmatrix}0\\0\\0\end{bmatrix}$.'''),
'q-32319':(r'\begin{bmatrix}1 & 20 \\ -40 & 41\end{bmatrix}',r'''To find $A^2$, multiply $A$ by itself:

$$
A^2=\begin{bmatrix}3&2\\-4&7\end{bmatrix}\begin{bmatrix}3&2\\-4&7\end{bmatrix}
=\begin{bmatrix}9-8&6+14\\-12-28&-8+49\end{bmatrix}
=\begin{bmatrix}1&20\\-40&41\end{bmatrix}.
$$'''),
'q-36317':(r'\begin{bmatrix}-12 & -9 \\ 12 & -15\end{bmatrix}',r'''Interpret the constant term as a multiple of the identity matrix: $f(A)=A^2+2A-3I_2$. First,

$$
A^2=\begin{bmatrix}1&-3\\4&0\end{bmatrix}^2=\begin{bmatrix}-11&-3\\4&-12\end{bmatrix}.
$$

Hence,

$$
f(A)=\begin{bmatrix}-11&-3\\4&-12\end{bmatrix}+\begin{bmatrix}2&-6\\8&0\end{bmatrix}-\begin{bmatrix}3&0\\0&3\end{bmatrix}=\begin{bmatrix}-12&-9\\12&-15\end{bmatrix}.
$$'''),
'q-31963':('$B$ and $C$ only',r'''An elementary matrix is obtained from $I_2$ by exactly one elementary row operation.

Matrix $B$ is obtained by $R_2\leftarrow4R_2$. Matrix $C$ is obtained by $R_2\leftarrow R_2+2R_1$. Matrix $A$ requires both adding a multiple of row 1 to row 2 and scaling row 2, so it is not elementary.

Therefore, the correct answer is "$B$ and $C$ only."'''),
'q-42601':(r'\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}',r'''The matrix $E$ interchanges the two rows. To transform $E$ back into $I_2$, interchange the rows again. Applying that operation to the right half of $[E\mid I_2]$ gives

$$
E^{-1}=\begin{bmatrix}0&1\\1&0\end{bmatrix}.
$$'''),
'q-34762':('2',r'''Find $x_1,x_2,x_3$ such that $x_1b_1+x_2b_2+x_3b_3=x$. The corresponding system is

$$
\left\{\begin{aligned}x_1+2x_2&=5\\-2x_1+x_2&=10\\4x_1-2x_2+3x_3&=-17.\end{aligned}\right.
$$

Adding twice the first equation to the second gives $5x_2=20$, so $x_2=4$. Then $x_1=5-8=-3$. The third equation becomes $-12-8+3x_3=-17$, giving $x_3=1$.

Thus $[x]_B=\begin{bmatrix}-3\\4\\1\end{bmatrix}$, and $x_1+x_2+x_3=-3+4+1=2$.'''),
'q-35233':('-54',r'''Find $x_1,x_2$ such that $x_1b_1+x_2b_2=x$. This gives

$$
\left\{\begin{aligned}x_1-3x_2&=10\\4x_1-10x_2&=8\\-2x_1+6x_2&=-20.\end{aligned}\right.
$$

Subtracting four times the first equation from the second gives $2x_2=-32$, so $x_2=-16$. Then $x_1=10+3(-16)=-38$. These values also satisfy the third equation.

Therefore, $[x]_B=\begin{bmatrix}-38\\-16\end{bmatrix}$ and $x_1+x_2=-54$.'''),
'q-35239':(r'\begin{bmatrix}1 \\ -18 \\ 4\end{bmatrix}',r'''The entries of $[x]_B$ are the coefficients of $b_1$ and $b_2$. Therefore,

$$
x=5b_1-7b_2=5\begin{bmatrix}3\\2\\5\end{bmatrix}-7\begin{bmatrix}2\\4\\3\end{bmatrix}=\begin{bmatrix}15-14\\10-28\\25-21\end{bmatrix}=\begin{bmatrix}1\\-18\\4\end{bmatrix}.
$$'''),
'q-75845':('1',r'''The order of the basis vectors matters. Here

$$
x=1b_1+0b_2-3b_3.
$$

Therefore, $[x]_B=\begin{bmatrix}1\\0\\-3\end{bmatrix}$, so $x_1=1$.'''),
'q-34258':('3',r'''To decide whether $b\in\operatorname{Col}(B)$, solve $B\mathbf{x}=b$:

$$
\left\{\begin{aligned}2x_1-x_2&=1\\4x_1&=-4.\end{aligned}\right.
$$

The second equation gives $x_1=-1$. Substitution into the first gives $x_2=-3$. Thus the system is consistent, so $b\in\operatorname{Col}(B)$, and $x_1x_2=(-1)(-3)=3$.'''),
'q-34260':('0',r'''Solve $C\mathbf{x}=b$ using Gaussian elimination:

$$
\left[\begin{array}{ccc|c}1&-1&3&2\\2&0&4&-1\\1&-3&0&7\end{array}\right]
\sim\left[\begin{array}{ccc|c}1&-1&3&2\\0&2&-2&-5\\0&-2&-3&5\end{array}\right]
\sim\left[\begin{array}{ccc|c}1&-1&3&2\\0&2&-2&-5\\0&0&-5&0\end{array}\right].
$$

Back-substitution gives $x_3=0$, $x_2=-\frac52$, and $x_1=-\frac12$. The system is consistent, so $b\in\operatorname{Col}(C)$. Finally, $x_1x_2x_3=0$.'''),
'q-35568':('6',r'''For $b$ to lie in $\operatorname{Col}(A)$, the system $A\mathbf{x}=b$ must be consistent. Subtract twice row 1 from row 2 and five times row 1 from row 3:

$$
\left[\begin{array}{cc|c}1&-2&1\\2&-2&3\\5&-8&k\end{array}\right]
\sim\left[\begin{array}{cc|c}1&-2&1\\0&2&1\\0&2&k-5\end{array}\right]
\sim\left[\begin{array}{cc|c}1&-2&1\\0&2&1\\0&0&k-6\end{array}\right].
$$

The last row requires $0=k-6$, so $k=6$.'''),
}
for ctx in contexts:
 q=ctx['q'];ident=q[':question/math-academy-id']
 if ident not in solutions:continue
 value,solution=solutions[ident];fs=q[':question/answer-fields'];assert len(fs)==1;f=fs[0];matches=[a for a in f[':answer-field/choices']if a[':answer/value']==value];assert len(matches)==1,(ident,value);a=matches[0];validate_math_structure(solution)
 keys.append({'question':q[':db/id'],'field':f[':db/id'],'answer':a[':db/id'],'answer_uuid':a[':answer/id'],'before':None,'evidence':{'source_identity':ident,'canonical_entity':ctx['canonical'][':db/id']if ctx['canonical']else None,'method':ctx['title'],'independently_derived_value':value},'confidence':'high'})
 ps.append({'entity':q[':db/id'],'attribute':'question/worked-solution','before':None,'after':solution,'reason':'authored-missing-solution','evidence':keys[-1]['evidence'],'confidence':'high'})
# Independent exact checks on all numeric completions and blank matrix questions.
qmap={q[':question/math-academy-id']:q for q in D['questions']if q.get(':question/math-academy-id')}
expect={}
for ident in ['q-157694','q-42955','q-39865','q-43066','q-42004','q-42257','q-32319','q-36317','q-42601','q-34762','q-35233','q-35239','q-75845','q-34258','q-34260','q-35568']:
 q=qmap[ident];ms=list(map(mat,grids(q[':question/problem'])));v=None
 if ident=='q-157694':v=abs(S.Matrix.hstack(*ms).det())
 elif ident=='q-42955':v=ms[0].det()
 elif ident in ['q-39865','q-43066','q-42601']:v=ms[0].inv()
 elif ident=='q-42004':v=ms[1]*(ms[0]+ms[2])
 elif ident=='q-42257':v=ms[0]*ms[1]*ms[2]
 elif ident=='q-32319':v=ms[0]**2
 elif ident=='q-36317':v=ms[0]**2+2*ms[0]-3*S.eye(2)
 elif ident in ['q-34762','q-35233']:v=sum(S.Matrix.hstack(*ms[:-2]).gauss_jordan_solve(ms[-2])[0])
 elif ident=='q-35239':v=S.Matrix.hstack(*ms[:-1])*ms[-1]
 elif ident=='q-75845':v=S.Matrix.hstack(*ms[:-2]).gauss_jordan_solve(ms[-2])[0][0]
 elif ident in ['q-34258','q-34260']:v=S.prod(ms[0].gauss_jordan_solve(ms[1])[0])
 elif ident=='q-35568':v=S.Matrix([[1,-2],[2,-2]]).inv()*S.Matrix([1,3]);v=(ms[0]*v)[2]
 want=solutions[ident][0];gs=grids(want);got=mat(gs[0])if gs else scalar(want);assert same(v,got)if isinstance(v,S.MatrixBase)else S.simplify(v-got)==0,(ident,v,want);proof.append({'identity':ident,'derived':str(v),'passed':True})
for q in D['questions']:
 p=q[':question/problem'];fs=q.get(':question/answer-fields',[])
 if not fs or fs[0][':answer-field/type'][':db/ident']!=':answer-field.type/blank' or not re.search(r'(?m)^\|',p):continue
 ms=list(map(mat,grids(p)));label=None
 op=re.search(r'\$(AB\+AC|BA\+BC|AC\+BC|AC-BC|CB-CA|ABC)\$',p)
 if op:
  label=op[1];A,B,C=ms[:3];expected={'AB+AC':lambda:A*(B+C),'BA+BC':lambda:B*(A+C),'AC+BC':lambda:(A+B)*C,'AC-BC':lambda:(A-B)*C,'CB-CA':lambda:C*(B-A),'ABC':lambda:A*B*C}[label]()
 else:
  power=re.search(r'Find \$\{?([A-Z])\}?\^\{(\d+)\}',p)
  if power:label=power[1]+'^{'+power[2]+'}';expected=ms[0]**int(power[2])
  else:
   poly=re.search(r'f\(X\)=\{?X\}?\^\{2\}([+-](?:\d+)?X)([+-]\d+)',p)
   assert poly,(q[':db/id'],p)
   c=poly[1][:-1];c=int(c+'1'if c in ['+','-']else c);d=int(poly[2]);expected=ms[0]**2+c*ms[0]+d*S.eye(ms[0].rows);name=re.search(r'matrix \$([A-Z])=',p)[1];label='f('+name+')'
 bykey={f[':answer-field/key']:f for f in fs};table=p[p.index('|'):];rows=[];header=bool(re.search(r'Column\s*1',table))
 for line in table.splitlines():
  raw=[c.strip()for c in line.strip().strip('|').split('|')]
  if all(re.fullmatch(r':?-+:?',c)for c in raw):continue
  if header:
   if not any('{{'in c or re.fullmatch(r'\$[^$]+\$',c)for c in raw[1:]):continue
   raw=raw[1:]
  else:
   raw=[c for c in raw if c and not re.fullmatch(r'\$[^$]*=\s*(?:\\,\s*)*\$',c)]
  if not raw:continue
  row=[c if '{{'in c else c[1:-1]for c in raw];rows.append(row)
 assert len(rows)==expected.rows and all(len(row)==expected.cols for row in rows),(q[':db/id'],rows,expected)
 for i,row in enumerate(rows):
  for j,c in enumerate(row):
   key=re.fullmatch(r'\{\{([^{}]+)\}\}',c);value=bykey[key[1]][':answer-field/correct'][':answer/value']if key else c;assert S.simplify(scalar(value)-expected[i,j])==0,(q[':db/id'],i,j,value,expected[i,j])
 proof.append({'entity':q[':db/id'],'expression':label,'shape':list(expected.shape),'all_existing_blank_answers_and_supplied_entries_verified':True,'table_role':'authored-labeled-table'if header else'answer-matrix'})
 if not header:
  from question_capture.math_format import matrix_answer
  entry=next((x for x in ps if x['entity']==q[':db/id']and x['attribute']=='question/problem'),None);old=entry['after']if entry else p;cut=old.index('|')if '|'in old else old.index('<div class="matrix-answer">');after=old[:cut]+matrix_answer(label,rows)
  evidence={'independent_result':str(expected),'shape':list(expected.shape),'all_blanks_and_supplied_entries_match':True,'keys_in_source_row_order':True}
  if entry:entry['after']=after;entry['confidence']='high';entry['evidence']=entry['evidence']+[evidence]if isinstance(entry['evidence'],list)else[entry['evidence'],evidence]
  else:ps.append({'entity':q[':db/id'],'attribute':'question/problem','before':p,'after':after,'reason':'source-mixed-entry-matrix-answer-grid','evidence':evidence,'confidence':'high'})
(H/'proposals.json').write_text(json.dumps(ps,indent=2)+'\n');(H/'missing-key-repairs.json').write_text(json.dumps(keys,indent=2)+'\n');(H/'math-verification.json').write_text(json.dumps(proof,indent=2)+'\n');print('completions',len(keys),'math verifications',len(proof))

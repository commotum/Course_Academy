import json,uuid,copy
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;B=H/'bank-closure';D=json.loads((B/'current.json').read_text());Q={q[':db/id']:q for q in D['questions']};x,y,C,K=S.symbols('x y C K',real=True);P=x*x*y;R=-x**3-2*y**4
solution1=r'''For $x\ne0$, write the equation in Bernoulli form:

$$
y'+\frac1x y=\frac1{x^2}y^4.
$$
We seek the nonzero real solutions, so divide by $y^4$ and set $z=y^{-3}$. The chain rule gives $z'=-3y^{-4}y'$, hence

$$
z'-\frac3x z=-\frac3{x^2}.
$$
On any interval avoiding $x=0$, an integrating factor is $I(x)=x^{-3}$, because $I'/I=-3/x$. Multiplying and integrating gives

$$
\begin{aligned}
(x^{-3}z)'&=-3x^{-5},\\
x^{-3}z&=\frac3{4x^4}+K,\\
z&=\frac3{4x}+Kx^3.
\end{aligned}
$$
Now substitute $z=y^{-3}$ and absorb the factor $4$ into the arbitrary constant, writing $C=4K$:

$$
y^3=\frac{4x}{3+Cx^4},\qquad
\boxed{y=\sqrt[3]{\frac{4x}{3+Cx^4}}}.
$$
The cube root is the **real** cube root, so its argument may be negative. Use intervals with $x\ne0$ and $3+Cx^4\ne0$; on these intervals the family is real, finite and nonzero. The invertible substitution $z=y^{-3}$ recovers every nonzero solution there.

To verify the result without imposing a positive branch, put $g(x)=4x/(3+Cx^4)$. Since $y^3=g(x)\ne0$, implicit differentiation gives $y'=yg'/(3g)$, and

$$
x^2y'-y^4+xy
=y\left(\frac{x^2g'}{3g}-g+x\right)=0.
$$
The original equation also admits the equilibrium solution $y=0$. It is excluded only by the question's explicit **nonzero** condition; it was lost when dividing by $y^4$ and must be checked separately.'''
solution2=r'''For an integrating factor depending only on $y$, use

$$
I(y)=\exp\left(-\int\frac{P_y-Q_x}{P}\,\mathrm dy\right).
$$
The displayed quotient is evaluated where $P\ne0$. Since it simplifies to $4/y$, we can choose

$$
I(y)=e^{-4\ln|y|}=\frac1{y^4},\qquad y\ne0.
$$
Multiplication gives

$$
\frac{x^2}{y^3}\,\mathrm dx+
\left(-\frac{x^3}{y^4}-2\right)\,\mathrm dy=0.
$$
This equation is exact, because

$$
\frac{\partial}{\partial y}\left(\frac{x^2}{y^3}\right)
=-\frac{3x^2}{y^4}
=\frac{\partial}{\partial x}\left(-\frac{x^3}{y^4}-2\right).
$$
To find a potential $F(x,y)$, integrate its $x$-derivative while holding $y$ fixed:

$$
F_x=\frac{x^2}{y^3}
\quad\Longrightarrow\quad
F(x,y)=\frac{x^3}{3y^3}+G(y).
$$
Differentiate with respect to $y$ and match the other coefficient:

$$
-\frac{x^3}{y^4}+G'(y)=-\frac{x^3}{y^4}-2,
\qquad G'(y)=-2.
$$
Therefore the requested implicit general solution is

$$
\boxed{\frac{x^3}{3y^3}-2y=c},\qquad y\ne0.
$$
Indeed, $\mathrm dF=y^{-4}(P\,\mathrm dx+Q\,\mathrm dy)$, so the level curves give the original differential equation on the stated regions. Although the quotient formula initially requires $P\ne0$, the resulting integrating factor and exact equation extend to $x=0$ whenever $y\ne0$.

The original equation also admits $y=0$. That solution lies outside the question's explicit $y\ne0$ region, where the integrating factor is undefined. The factor $1/3$ in the potential is necessary: omitting it changes $F_x$ and does not merely rename the arbitrary constant.'''
problem1=r'''Find the general **nonzero real** solution to the differential equation

$$
x^2\frac{\mathrm dy}{\mathrm dx}=y^4-xy.
$$

Work on an interval with $x\ne0$ where the solution is finite. Interpret cube roots as real cube roots.'''
q2=Q[17592186217793];problem2=q2[':question/problem']+r'''

Use the displayed quotient only where it is defined, and use the integrating-factor method on regions with $y\ne0$.'''
# This authored closure preserves every original choice and identity.
new_specs=[(17592186147726,17592186144119,r'y=\sqrt[3]{\frac{4x}{3+Cx^4}}'),(17592186217793,17592186216612,r'\frac{x^3}{3y^3}-2y=c')];new=[];cas=[]
for qid,fid,value in new_specs:
 q=Q[qid];f=next(f for f in q[':question/answer-fields']if f[':db/id']==fid);assert not f.get(':answer-field/correct');aid=str(uuid.uuid5(uuid.UUID(f[':answer-field/id']),'answer.type/math\n'+value))
 new.append({'question':qid,'field':fid,'field_uuid':f[':answer-field/id'],'field_type':f[':answer-field/type'][':db/id'],'field_type_ident':f[':answer-field/type'][':db/ident'],'expected_choices':sorted(a[':db/id']for a in f[':answer-field/choices']),'expected_correct':None,'answer_uuid':aid,'type':'answer.type/math','value':value,'reason':'Narrowly authored correction of a source-origin bank with no valid existing answer; retain every existing answer and history identity','evidence':{'basis':9169,'question_identity':q[':question/math-academy-id'],'source_frame':'bank-closure/source-'+q[':question/math-academy-id'].replace('-','')+'.html','authored':True,'stable_identity':'UUID5(existing field UUID, answer.type/math + newline + exact canonical value)'}})
for qid,problem,solution in[(17592186147726,problem1,solution1),(17592186217793,problem2,solution2)]:
 q=Q[qid]
 for attr,value in [('question/problem',problem),('question/worked-solution',solution)]:cas.append({'entity':qid,'attribute':attr,'before':q.get(':'+attr),'after':value,'reason':'Authored source correction: state necessary nonzero/domain scope transparently and supply independently derived complete worked solution','evidence':{'basis':9169,'source_identity':q[':question/math-academy-id'],'source_archive':'2522/Source/2522.html'if qid==17592186147726 else'6353/Source/6353.html','multistep_parents':[],'assigned_problem_parents':[],'canonical_template':17592186147391 if qid==17592186147726 else 17592186216980,'authored':True},'confidence':'high'})
cas.append({'entity':17592186216607,'attribute':'answer-field/correct','before':None,'after':17592186216608,'reason':'Reuse unique existing field-owned integrating factor y^-4; independent exactness residual is zero','evidence':{'basis':9169,'question':17592186217793,'value':r'\frac1{y^4}','authored':True},'confidence':'high'})
plan={'basis':9169,'source':'agent/codex','questions':[17592186147726,17592186217793],'cas':cas,'new_answers':new,'detach':[],'preservation':'Add one owned answer to each expected nonempty bank. No existing answer/value/type/ID, membership, learner response or history record is changed or removed.'}
(H/'supplemental-bank-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
prospective=copy.deepcopy(D['questions']);entities={q[':db/id']:q for q in prospective}
for q in prospective:
 for f in q[':question/answer-fields']:
  entities[f[':db/id']]=f
  for a in f[':answer-field/choices']:entities[a[':db/id']]=a
for p in cas:
 entities[p['entity']][':'+p['attribute']]=copy.deepcopy(entities[p['after']])if p['attribute']=='answer-field/correct'else p['after']
for p in new:
 a={':answer/id':p['answer_uuid'],':answer/type':{':db/id':17592186045498,':db/ident':':answer.type/math'},':answer/value':p['value']};f=entities[p['field']];f[':answer-field/choices'].append(a);f[':answer-field/correct']=a
(B/'prospective-questions.json').write_text(json.dumps(prospective,indent=2)+'\n')
# Independent mathematics: all transformation/intermediate identities and bank uniqueness.
g=4*x/(3+C*x**4);z=3/(4*x)+K*x**3;mu=y**-4;F=x**3/(3*y**3)-2*y
proof={'basis':9169,'q106074':{'linearized_residual':str(S.simplify(S.diff(z,x)-3*z/x+3/x**2)),'integrating_factor_residual':str(S.simplify(S.diff(x**-3,x)+3*x**-4)),'integration_step_residual':str(S.simplify(S.diff(3/(4*x**4)+K,x)+3*x**-5)),'cubic_solution_original_residual_factor':str(S.simplify(x*x*S.diff(g,x)/(3*g)-g+x)),'zero_equilibrium_residual':'0','domain':'x≠0, 3+Cx⁴≠0, real cube root of either sign','all_nonzero_solutions':'z=y^-3 is a differentiable bijection of nonzero real y to nonzero real z. General linear z solution has arbitrary real K; C=4K preserves its full one-parameter freedom.'},'q337099':{'P':str(P),'Q':str(R),'F':str(F),'F_x_minus_muP':str(S.simplify(S.diff(F,x)-mu*P)),'F_y_minus_muQ':str(S.simplify(S.diff(F,y)-mu*R)),'exactness_residual':str(S.simplify(S.diff(mu*P,y)-S.diff(mu*R,x))),'domain':'y≠0; quotient theorem used where P≠0, factor and potential extend to x=0','zero_equilibrium_pullback':'For the curve y(x)=0, P dx+Q dy=0; it is excluded only from the explicitly nonzero integrating-factor region.'}}
# Old Bernoulli options cannot represent the requested family. Use z=y^-3;
# cube-root options give z=1/(their cubed expression), valid for the real root.
old_y=[((2+x**3)/(C+x*x))**3,(C-2*x*x)/(3*x**3),(C+3*x*x)/x**3];old_z=[v**-3 for v in old_y]+[(C-2*x*x)/(2*x**3),(C-x*x)/x**3]
proof['q106074']['existing_bank_checks']=[]
for a,zz in zip(Q[17592186147726][':question/answer-fields'][0][':answer-field/choices'],old_z):
 residual=S.factor(S.diff(zz,x)-3*zz/x+3/x**2);assert residual!=0;proof['q106074']['existing_bank_checks'].append({'answer':a[':db/id'],'linearized_residual':str(residual),'valid_general_family':False})
proof['q337099']['existing_factor_checks']=[{'power':n,'exactness_residual':str(S.factor(S.diff(P*y**-n,y)-S.diff(R*y**-n,x))),'valid':n==4}for n in[4,2,3,1]]
old_F=[x**4/y**4-2*y,x**3/y**3-2*y,x*x/(y*y)-2*y*y,x**4/y**4-2*y**3];field2=next(f for f in Q[17592186217793][':question/answer-fields']if f[':db/id']==17592186216612);proof['q337099']['existing_potential_checks']=[]
for a,ff in zip(field2[':answer-field/choices'],old_F):
 residual=S.factor(S.diff(ff,x)*R-S.diff(ff,y)*P);assert residual!=0;proof['q337099']['existing_potential_checks'].append({'answer':a[':db/id'],'parallel_gradient_residual':str(residual),'valid_general_potential':False})
assert all(proof['q106074'][k]=='0'for k in['linearized_residual','integrating_factor_residual','integration_step_residual','cubic_solution_original_residual_factor']);assert all(proof['q337099'][k]=='0'for k in['F_x_minus_muP','F_y_minus_muQ','exactness_residual'])
(B/'math-verification.json').write_text(json.dumps(proof,indent=2)+'\n');print('cas',len(cas),'new answers',len(new),'all independent identities/bank uniqueness passed');print([(p['field'],p['answer_uuid'])for p in new])

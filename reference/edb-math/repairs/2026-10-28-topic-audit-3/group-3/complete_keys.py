import json,math,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};rows=json.loads((H/'genuine-missing-keys.json').read_text());by={r['source']:r for r in rows};entries={}
def add(sid,aid,solution,proof,checks=None):
 r=by[sid];q=Q[r['question']];f=r['field'];assert any(a[':db/id']==aid for a in f[':answer-field/choices']);assert not q.get(':question/worked-solution');entries[sid]={'qid':q[':db/id'],'field':f[':db/id'],'aid':aid,'solution':solution,'proof':proof,'independent_checks':checks or[]}
add('q-1355',17592186056546,r'''Multiply corresponding components and add:

$$
a\cdot b=(-1)(10)+(0)(2)+(6)(-5)=-10-30=-40.
$$''','dot product (-1,0,6)·(10,2,-5)=−40')
add('q-19021',17592186057569,r'''Perpendicular vectors have dot product zero. Thus

$$
u\cdot v=x^2+(-2)(2)=x^2-4=0.
$$

The roots are $x=\pm2$. Since $x>0$, the required value is $x=2$.''','x²−4=0, positive root2')
add('q-19022',17592186057573,r'''Since $a\perp b$, their dot product is zero:

$$
a\cdot b=x^2-6x+9=(x-3)^2=0.
$$

Therefore $x=3$.''','x²−6x+9=(x−3)²')
add('q-11376',17592186093793,r'''Divide the vector by its magnitude:

$$
\widehat a=\frac{a}{|a|}=\frac15a.
$$

Its magnitude is $\frac15|a|=1$, and the positive scalar multiple has the same direction as $a$.''','positive scale1/5 timesnorm5 givesunitlength')
add('q-12184',17592186094228,r'''The horizontal and vertical vectors are perpendicular, so

$$
|a+b|=\sqrt{3^2+4^2}=5.
$$

Dividing by this magnitude gives the required unit vector:

$$
\frac{a+b}{|a+b|}=\frac15(a+b).
$$''','a=(3,0),b=(0,−4); sum norm5')
add('q-12185',17592186094232,r'''North-east and south-east directions are perpendicular. Hence

$$
|a+b|=\sqrt{20^2+13^2}=\sqrt{569}.
$$

The unit vector in the direction of $a+b$ is

$$
\frac{a+b}{\sqrt{569}}.
$$''','NE=(1,1)/sqrt2,SE=(1,−1)/sqrt2, dot0 andsum normsqrt569')
add('q-12202',17592186094247,r'''A unit vector in the direction of $\overrightarrow{AB}$ is obtained by dividing by its magnitude:

$$
\frac{\overrightarrow{AB}}{|\overrightarrow{AB}|}=\frac17\overrightarrow{AB}.
$$

Its magnitude is $\frac17(7)=1$.''','ABnorm7;divideby7')
add('q-19276',17592186094943,r'''The scale shows that two grid squares represent one unit. Reading the displacements from the diagram gives

$$
q=\left\langle\frac52,-\frac32\right\rangle,
\qquad r=\left\langle\frac32,3\right\rangle.
$$

Thus $q+r=\langle4,\frac32\rangle$ and

$$
|q+r|=\sqrt{4^2+\left(\frac32\right)^2}=\frac{\sqrt{73}}2.
$$

The required unit vector is

$$
\frac{q+r}{|q+r|}=\frac{2(q+r)}{\sqrt{73}}.
$$''','Visually inspected retainedgraph: oneunit=two squares; q=(5/2,−3/2),r=(3/2,3), AB=(4,3/2).','image:images/9d/9dfaf74a497a2fd22428e09a4c26d573e184c9728ccf67f11ebb9d6a2a44f4c6.png')
add('q-20407',17592186095040,r'''The scale shows that two grid squares represent one unit. The vector moves four grid squares right and seven down, so

$$
c=\left\langle2,-\frac72\right\rangle,
\qquad |c|=\sqrt{2^2+\left(-\frac72\right)^2}=\frac{\sqrt{65}}2.
$$

Dividing by the magnitude gives

$$
\frac{c}{|c|}=\frac{2c}{\sqrt{65}}.
$$''','Visually inspectedretainedgraph:oneunit=twosquares, displacement(4,−7)squares=(2,−7/2).','image:images/13/1319298a994d5daf26853baf7d255490827ada4123debdf0b4374db1ed03f7af.png')
add('q-126501',17592186102119,r'''The scalar projections are

$$
\operatorname{comp}_{d}c=\frac{c\cdot d}{|d|},
\qquad \operatorname{comp}_{c}d=\frac{d\cdot c}{|c|}.
$$

Here $c\cdot d=-2+2+4=4$, while $|c|=|d|=3$. Therefore

$$
\operatorname{comp}_{d}c+\operatorname{comp}_{c}d=\frac43+\frac43=\frac83.
$$''','c·d4;bothnorm3;8/3')
add('q-19136',17592186102537,r'''Use the scalar-projection formula:

$$
\operatorname{comp}_{d}c=|c|\cos\theta=14\cos60^\circ=14\left(\frac12\right)=7.
$$''','14cospi/3=7')
add('q-20003',17592186102607,r'''The area of the parallelogram is $|a\times b|$. Compute

$$
a\times b=
\begin{vmatrix}i&j&k\\-2&-3&-1\\1&2&1\end{vmatrix}
=-i+j-k.
$$

Hence the area is

$$
\sqrt{(-1)^2+1^2+(-1)^2}=\sqrt3.
$$''','cross(−2,−3,−1),(1,2,1)=(−1,1,−1);normsqrt3')
add('q-20016',17592186102612,r'''Take two sides with common initial point $A$:

$$
\overrightarrow{AB}=\langle2,1,2\rangle,
\qquad\overrightarrow{AC}=\langle0,1,1\rangle.
$$

Their cross product is $\langle-1,-2,2\rangle$, with magnitude $3$. A triangle has half the area of the parallelogram, so

$$
\operatorname{Area}(\triangle ABC)=\frac12(3)=\frac32.
$$''','cross(2,1,2),(0,1,1)=(−1,−2,2);norm3;half3/2')
add('q-20028',17592186102629,r'''Use $PQ$ as the base. The side vectors are

$$
\overrightarrow{PQ}=\langle2,4,0\rangle,
\qquad\overrightarrow{PR}=\langle1,3,1\rangle.
$$

The altitude from $R$ to the line $PQ$ is

$$
RH=\frac{|\overrightarrow{PQ}\times\overrightarrow{PR}|}{|\overrightarrow{PQ}|}
=\frac{|\langle4,-2,2\rangle|}{2\sqrt5}
=\frac{2\sqrt6}{2\sqrt5}=\frac{\sqrt{30}}5.
$$''','height=sqrt24/sqrt20=sqrt30/5')
add('q-35988',17592186122241,r'''Differentiate with respect to each variable, holding the other fixed:

$$
\begin{aligned}
f_x&=\frac{3(x-y)-(3x+2y)}{(x-y)^2}=-\frac{5y}{(x-y)^2},\\
f_y&=\frac{2(x-y)+(3x+2y)}{(x-y)^2}=\frac{5x}{(x-y)^2}.
\end{aligned}
$$

Thus, for $x\ne y$,

$$
\nabla f=-\frac5{(x-y)^2}(yi-xj).
$$''','quotientrule gradient(−5y,5x)/(x−y)², x≠y')
add('q-37466',17592186123040,r'''The product is $fg=x^2y^2\ln x\ln y$, defined for $x>0$ and $y>0$. Applying the product rule separately to each variable gives

$$
\begin{aligned}
(fg)_x&=xy^2\ln y(2\ln x+1),\\
(fg)_y&=x^2y\ln x(2\ln y+1).
\end{aligned}
$$

Therefore

$$
\nabla(fg)=xy^2\ln y(2\ln x+1)i+x^2y\ln x(2\ln y+1)j.
$$''','directpartialderivativesofx²y²lnxlny;positivelogdomains')
add('q-160373',17592186126533,r'''Choose $u=xy$ and $v=y/x$. The boundary curves become $1\le u\le2$ and $1\le v\le2$. In the first quadrant this transformation is one-to-one, with inverse $x=\sqrt{u/v}$ and $y=\sqrt{uv}$. Its Jacobian is

$$
\frac{\partial(u,v)}{\partial(x,y)}=
\begin{vmatrix}y&x\\-y/x^2&1/x\end{vmatrix}
=\frac{2y}{x}=2v.
$$

Using the absolute inverse Jacobian,

$$
\operatorname{Area}(D)=\int_1^2\int_1^2\frac1{2v}\,dv\,du=\frac12\ln2.
$$''','u=xy,v=y/x;Jac2v;rect1≤u,v≤2;area(ln2)/2')
add('q-160379',17592186126540,r'''The given substitution turns the boundaries into $1\le u\le2$ and $1\le v\le4$. It is one-to-one in the first quadrant: $x=(v/u)^{1/3}$ and $y=u^{1/3}v^{2/3}$. The Jacobian is

$$
\frac{\partial(u,v)}{\partial(x,y)}=
\begin{vmatrix}-2y/x^3&1/x^2\\y&x\end{vmatrix}
=-\frac{3y}{x^2}=-3u.
$$

Area uses its absolute inverse, so

$$
\operatorname{Area}(D)=\int_1^2\int_1^4\frac1{3u}\,dv\,du=\ln2.
$$''','Jac−3u, absoluteinverse1/(3u),rectu1²v1⁴⇒ln2')
add('q-38374',17592186127343,r'''Under $u=x-y$ and $v=y$, the parabola becomes $v=u^2$ and the line becomes $v=1$. They meet at $u=\pm1$. The inverse is $x=u+v$, $y=v$, with Jacobian $1$. Thus

$$
\operatorname{Area}(D)=\int_{-1}^1\int_{u^2}^1 1\,dv\,du
=\int_{-1}^1(1-u^2)\,du=\frac43.
$$''','inversex=u+v,y=v det1;boundsu±1,v=u²to1;4/3')
add('q-124119',17592186130645,r'''The arrows show the counter-clockwise arc from $(0,3)$ through the left and lower portions of the circle to $(3,0)$. With the supplied parametrization, its parameter runs from $\pi/2$ to $2\pi$. Substituting gives

$$
x=3\cos t,\qquad y=3\sin t,\qquad dx=-3\sin t\,dt.
$$

Therefore

$$
\int_Cx^2y\,dx=-81\int_{\pi/2}^{2\pi}\cos^2t\sin^2t\,dt.
$$''','Retainedgrapharroworientationπ/2→2π; x²y dx=−81cos²t sin²t dt')
add('q-15803',17592186149119,r'''The diagram shows an ellipse centered at the origin, with horizontal radius $3$ and vertical radius $5$. A parametrization is

$$
x=3\cos\theta,\qquad y=5\sin\theta,\qquad0\le\theta<2\pi.
$$

Indeed, these coordinates satisfy $x^2/9+y^2/25=1$ and trace the entire ellipse. Swapping the radii would produce a horizontally stretched ellipse.''','Retainedgraphinterceptsx±3,y±5;paramx3cos,y5sin')
add('q-78679',17592186151281,r'''The dashed lines locate the center at $(2,1)$. The horizontal endpoints are $x=-2$ and $x=6$, while the vertical endpoints are $y=-1$ and $y=3$. Hence the radii are $4$ horizontally and $2$ vertically. Therefore

$$
x=4\cos\theta+2,\qquad y=2\sin\theta+1,\qquad0\le\theta<2\pi.
$$''','White-compositedretainedgraphcenter(2,1),radii(4,2); imageinspectionartifactcompletion-ellipse-q78679.png')
add('q-122264',17592186168514,r'''At the three indicated points, evaluate the components of $F(x,y)=\langle x^2,-2y\rangle$:

$$
\begin{aligned}
F(-2,1)&=\langle4,-2\rangle,\\
F(2,3)&=\langle4,-6\rangle,\\
F(0,-2)&=\langle0,4\rangle.
\end{aligned}
$$

The matching diagram has a right-and-down arrow from each of the first two points and an upward arrow from $(0,-2)$, with the displayed component displacements.''','Visuallyinspectedall5plots;selected514endpoints(2,−1),(6,−3),(0,2) frompoints(−2,1),(2,3),(0,−2) respectively.')
add('q-122296',17592186168520,r'''Every arrow points downward. Its horizontal component points left for $x<0$, vanishes on the $y$-axis, and points right for $x>0$. These features match

$$
F(x,y)=xi-j=\langle x,-1\rangle.
$$

The constant vector fields would have the same direction everywhere, while $-xi+yj$ would point upward in the upper half-plane and inward horizontally.''','Retainedvectorfieldarrowsmatchhorizontalcomponentx,vertical−1,allrowsindependentofy.')
add('q-123920',17592186168620,r'''Region I is a filled ellipse, so it is convex and therefore simply connected. Region II is the plane with the entire line $y=x$ removed; it splits into the two disjoint half-planes $y>x$ and $y<x$, so it is not connected and hence not simply connected. Region III is the full plane, which is convex and simply connected. Thus I and III only are simply connected.''','Ellipseconvex;R²minuslinedisconnected;R²convex;IandIII')
add('q-122139',17592186177420,r'''Use $y=t$. Then $x=-t^2/16$, with $-8\le t\le4$, and

$$
ds=\sqrt{\left(-\frac t8\right)^2+1}\,dt=\frac{\sqrt{t^2+64}}8\,dt.
$$

Also $32xy=32(-t^2/16)t=-2t^3$. Hence

$$
\int_C32xy\,ds=-\frac14\int_{-8}^{4}t^3\sqrt{t^2+64}\,dt.
$$

The missing expression is $t^3\sqrt{t^2+64}$.''','Fullresponseframeincludesexternal−1/4;parameterx−t²/16,y=t,ds√(t²+64)/8;targett³√(t²+64)')
add('q-122399',17592186177455,r'''Differentiate the scalar function with respect to each coordinate:

$$
f_x=2x-y,\qquad f_y=-x+6y-4.
$$

Thus its gradient vector field is

$$
\nabla f=(2x-y)i+(6y-x-4)j.
$$''','directgradientofx²−xy+3y²−4y')
add('q-122446',17592186177485,r'''With $y=t$, the curve is $r(t)=\langle2t^3,t\rangle$, $0\le t\le2$. Thus

$$
ds=\sqrt{(6t^2)^2+1}\,dt=\sqrt{36t^4+1}\,dt,
\qquad xy^2=2t^5.
$$

Consequently

$$
\int_Cxy^2\,ds=2\int_0^2t^5\sqrt{36t^4+1}\,dt.
$$''','parameter(2t³,t),speedsqrt36t4+1,integrand2t5')
add('q-122579',17592186177506,r'''Choose the smooth parametrization $x=t$, $y=t^2$, $0\le t\le\sqrt2$. Then $ds=\sqrt{1+4t^2}\,dt$ and $4xy=4t^3$, so

$$
\int_C4xy\,ds=\int_0^{\sqrt2}4t^3\sqrt{1+4t^2}\,dt.
$$

Let $u=1+4t^2$. The bounds become $1$ and $9$, and $4t^3dt=(u-1)du/8$. Therefore

$$
\begin{aligned}
\int_C4xy\,ds&=\frac18\int_1^9(u-1)u^{1/2}\,du\\
&=\frac18\left[\frac25u^{5/2}-\frac23u^{3/2}\right]_1^9
=\frac{149}{15}.
\end{aligned}
$$''','Smoothparamx=t,y=t²;positivearclengthfactor;subu1+4t² integral149/15')
add('q-123128',17592186177562,r'''Parametrize the segment by

$$
r(t)=\langle1+t,3t,1-t\rangle,\qquad0\le t\le1.
$$

The speed is $|r'(t)|=\sqrt{1+9+1}=\sqrt{11}$, and $f(r(t))=2+3t$. Thus

$$
\int_C f\,ds=\sqrt{11}\int_0^1(2+3t)\,dt.
$$''','r=A+t(B−A),speed√11,f2+3t;scalararclengthnotorienteddr')
add('q-125364',17592186177773,r'''Along the segment from $A$ to $B$, both the field arrows and the direction of traversal point right. Their dot product is positive, so

$$
\int_C F\cdot dr>0.
$$

Reversing the path changes the sign of a vector line integral:

$$
\int_{-C}F\cdot dr=-\int_C F\cdot dr<0.
$$

Therefore statement I only is true.''','RetainedgraphpositivehorizontalfieldandAleftofB;Cpositive,-Cnegative;Ionly')
add('q-161434',17592186178169,r'''For the stream-function convention $F=\psi_y i-\psi_x j$, differentiate

$$
\psi_y=2x\cos y-e^y,\qquad\psi_x=2\sin y.
$$

Therefore

$$
F(x,y)=(2x\cos y-e^y)i-2\sin y\,j.
$$

Its divergence is $2\cos y-2\cos y=0$, as expected for a stream function.''','ConventionconfirmedwithsameKPtutorial: F=(ψ_y,−ψ_x),derivedpartialsdivergence0')
add('q-39954',17592186178608,r'''Parametrize the segment by $x=1+t$, $y=2-t$, $0\le t\le1$. Its speed is $\sqrt2$. Hence

$$
\begin{aligned}
\int_C2xy\,ds
&=2\sqrt2\int_0^1(1+t)(2-t)\,dt\\
&=2\sqrt2\left[2t+\frac{t^2}2-\frac{t^3}3\right]_0^1
=\frac{13\sqrt2}{3}.
\end{aligned}
$$''','segmentparam(1+t,2−t),speed√2;exactintegral13√2/3')
add('q-76200',17592186179214,r'''Use $r(t)=\langle1+t,2t,1+2t\rangle$, $0\le t\le1$. Its speed is $3$, so

$$
\begin{aligned}
\int_C\sin\left(\frac{\pi y}4\right)\,ds
&=3\int_0^1\sin\left(\frac{\pi t}2\right)\,dt\\
&=-\frac6\pi\left[\cos\left(\frac{\pi t}2\right)\right]_0^1
=\frac6\pi.
\end{aligned}
$$''','3Dsegmentdirection(1,2,2),speed3;sinπt/2 integral6/π')
add('q-76565',17592186179232,r'''The segment lies on $y=0$. Parametrize it by $x=1-2t$, $y=0$, $0\le t\le1$, giving $ds=2\,dt$. Then

$$
\int_C(2x-3y)\,ds=\int_0^1(2-4t)\,2\,dt
=\left[4t-4t^2\right]_0^1=0.
$$

The positive and negative contributions cancel. The arc-length factor is positive even though $x$ decreases.''','Scalarlineintegralorientationindependent;positive2dt;odd2xover[−1,1] gives0')
add('q-38129',17592186197559,r'''The substitution maps the region to $0\le u\le3$, $0\le v\le2$. Solving for the original coordinates gives

$$
x=\frac{u-v}2,\qquad y=\frac{u+v}2,
\qquad\left|\frac{\partial(x,y)}{\partial(u,v)}\right|=\frac12.
$$

The integrand becomes $y^2-x^2=(y-x)(y+x)=uv$. Therefore the transformed integral is

$$
\frac12\int_0^3\int_0^2uv\,dv\,du.
$$''','inverseJacabsolute1/2,integranduv,rectu0³v0²')
assert len(entries)==36,(len(entries),set(by)-set(entries));keys=[];solutions=[];proofdir=H/'completion-proofs';proofdir.mkdir(exist_ok=True);proofs=[]
for sid,e in entries.items():
 q=Q[e['qid']];f=next(f for f in q[':question/answer-fields']if f[':db/id']==e['field']);key={'question':e['qid'],'field':e['field'],'before':None,'answer':e['aid'],'source_identity':sid,'reason':'Independently solve the full problem and link its existing owned answer.','evidence':{'classification':'authored completion, not an observed original answer','proof':str(proofdir/(sid+'.json')),'canonical_examples':[kp[':knowledge-point/canonical-example'][':db/id']for kp in D['kps']if ':knowledge-point/canonical-example'in kp and any(k==kp[':db/id']and qq==e['qid']for t,k,qq in D['links'])]},'confidence':'high'};sol={'entity':e['qid'],'attribute':'question/worked-solution','before':None,'after':e['solution'],'reason':'Supply the independently derived worked solution for a missing-key completion.','evidence':key['evidence']|{'source_identity':sid},'confidence':'high'};proof={'question':q[':db/id'],'source_identity':sid,'basis_t':9837,'problem':q[':question/problem'],'field':f[':db/id'],'selected_existing_owned_answer':next(a for a in f[':answer-field/choices']if a[':db/id']==e['aid']),'derivation':e['proof'],'independent_checks':e['independent_checks'],'worked_solution':e['solution'],'authored':True};(proofdir/(sid+'.json')).write_text(json.dumps(proof,indent=2));keys.append(key);solutions.append(sol);proofs.append(proof)
for n,v in [('missing-key-completions',keys),('completion-solutions',solutions),('completion-evidence',proofs)]: (H/(n+'.json')).write_text(json.dumps(v,indent=2))
print('authored key+workedsolution completions',len(keys))

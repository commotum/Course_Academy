import copy,json,re,uuid
from pathlib import Path
H=Path(__file__).resolve().parent
contexts=json.loads((H/'completion-context.json').read_text());banks={x['question']:x for x in json.loads((H/'completion-banks.json').read_text())}
# Index, zero-based existing bank position, and independently derived worked solution.
DATA=r'''
1|0|Differentiate each component of the scalar product. First $u(t)g(t)=\langle3t^5,3t^3-t^4,3t^4\rangle$. Therefore $$(ug)'(t)=\langle15t^4,9t^2-4t^3,12t^3\rangle.$$
2|4|Differentiate componentwise: $h'(t)=\langle4t,1,3t^2\rangle$ and $g'(t)=\langle2t+2,0,6t^2\rangle$. Thus $$(3h-2g)'(2)=3\langle8,1,12\rangle-2\langle6,0,24\rangle=\langle12,3,-12\rangle.$$
4|0|The fundamental vector product is $r_u\times r_v$, in that order. We have $r_u=\langle1,\cos u,v\rangle$ and $r_v=\langle1,2v,u\rangle$. Expanding the cross product gives $$r_u\times r_v=\langle u\cos u-2v^2,v-u,2v-\cos u\rangle.$$
5|2|The first equation gives $q=3p-9$. Substitute into the second equation: $$5p+4(3p-9)=32\implies17p=68\implies p=4.$$ Hence $q=3(4)-9=3$. Substitution into both original equations gives $-9$ and $32$, as required.
6|4|The second equation gives $b=-a$. Substitute into the first equation: $$-7a+2(-a)=18\implies-9a=18\implies a=-2.$$ Then $b=2$. Indeed, $-7(-2)+2(2)=18$ and $6(-2)+6(2)=0$.
7|new|Substitute $y=x+5$ into the first equation: $$x+5(x+5)=13\implies6x=-12\implies x=-2.$$ Then $y=-2+5=3$. Both original equations hold, so the ordered solution is $(-2,3)$.
8|1|From $5q+55=0$, we obtain $q=-11$. Substituting into the second equation gives $2p-33+3=0$, so $p=15$. Therefore $p-q=15-(-11)=26$.
9|4|The second equation gives $b=2+4a$. Substitute into the first equation: $3a+2(2+4a)=4$, so $11a=0$. Thus $a=0$, $b=2$, and $a-b=-2$.
10|0|Use the slope formula: $$m=\frac{3-5}{2-4}=\frac{-2}{-2}=1.$$
11|4|The intercepts are $(0,4)$ and $(2,0)$. Hence $$m=\frac{0-4}{2-0}=-2.$$
12|0|The plotted line is horizontal: its $y$-coordinate stays constant as $x$ changes. Its rise is zero, so its slope is $0$.
13|2|The plotted line is vertical. Any two distinct points on it have zero horizontal change, so the slope would require division by zero. The slope is undefined.
14|0|The plotted points are $(1,0)$ and $(3,6)$. Thus $$m=\frac{6-0}{3-1}=3.$$
15|1|The intercepts are $(-4,0)$ and $(0,2)$. Hence $$m=\frac{2-0}{0-(-4)}=\frac12.$$
16|2|The line falls as we move from left to right. Thus its rise is negative for a positive run, and its slope is negative.
17|4|The line rises as we move from left to right. Thus its rise and run have the same sign, and its slope is positive.
18|0|The strict inequalities exclude both endpoints. Use parentheses at both ends: $x\in(3,7)$.
19|0|The lower endpoint $9$ is excluded, and the upper endpoint $13$ is included. Thus $x\in(9,13]$.
20|1|The square bracket includes $-5$ and the parenthesis excludes $2\sqrt2$. Therefore $-5\le y<2\sqrt2$.
21|3|The open circle at $-1$ excludes that endpoint, and the filled circle at $2$ includes that endpoint. The segment represents $x\in(-1,2]$.
22|1|Both endpoint circles, at $1$ and $4$, are open. The segment represents $x\in(1,4)$.
23|1|Both parentheses exclude their endpoints. Therefore $x\in(3,4)$ means $3<x<4$.
24|3|Both square brackets include their endpoints. Therefore $x\in[-2,1]$ means $-2\le x\le1$.
25|4|A scalar line integral with respect to arc length is unchanged by reversing orientation, so statement II is true and statement I is false. Also $r_2(u)=r_1(2u)$ for $0\le u\le\tfrac12$, which traverses the same curve once. Its scalar line integral is $2$, rather than $4$. Thus only II must be true.
26|1|The integral of $1$ with respect to arc length is the length of $C$. The diagram shows a quarter-circle arc of radius $2$ and its straight chord. The arc length is $2(\pi/2)=\pi$, and the chord length is $\sqrt{2^2+2^2}=2\sqrt2$. Hence $$\int_C ds=\pi+2\sqrt2.$$
27|0|The integral of $1$ with respect to arc length is the length of the curve. A semicircle of radius $3$ has length half of $2\pi(3)$, so $$\int_C ds=3\pi.$$
28|3|Scalar line integrals are independent of orientation, so I holds. Set $t=2\theta$; as $\theta$ runs from $0$ to $\pi$, $t$ runs from $0$ to $2\pi$. Both parametrizations therefore traverse the same circle once, giving the same integral $k$. Thus II holds. III does not hold for arbitrary $k$, so the statements that must be true are I and II.
29|0|Coplanarity means the scalar triple product is zero. Since $b\times c=\langle-8,-1,10\rangle$, we obtain $$a\cdot(b\times c)=-8k-1+10=9-8k=0.$$ Hence $k=\tfrac98$.
30|1|The volume is the absolute value of the scalar triple product. Here $b\times c=\langle17,-10,-11\rangle$, so $$V=|a\cdot(b\times c)|=|-3(17)-2(-11)|=|-29|=29.$$
31|0|Implicit differentiation gives $2x+8y\,y'=0$, so $y'=-x/(4y)$ wherever $y\ne0$. At $(\sqrt2,1)$, the slope is $$-\frac{\sqrt2}{4}=-\frac1{2\sqrt2}.$$
32|2|Implicit differentiation gives the tangent slope $-x/(4y)=-1/(2\sqrt2)$ at $(\sqrt2,1)$. The normal slope is its negative reciprocal, $2\sqrt2$. Thus the normal is $y-1=2\sqrt2(x-\sqrt2)$. Setting $y=0$ yields $$x=\sqrt2-\frac1{2\sqrt2}=\frac3{2\sqrt2}.$$ Therefore $P=(\tfrac3{2\sqrt2},0)$.
33|3|Differentiating gives $6x-4y\,y'=0$, hence the tangent slope at $(2,2)$ is $3/2$. The normal slope is $-2/3$, so its equation is $y-2=-\tfrac23(x-2)$. At $x=0$, $y=2+\tfrac43=\tfrac{10}3$. Thus $P=(0,\tfrac{10}3)$.
34|0|Differentiate implicitly: $3x^2+3y^2y'=0$. Hence $$\frac{dy}{dx}=-\frac{x^2}{y^2}$$ wherever the curve has a finite derivative, namely $y\ne0$.
35|2|Differentiate implicitly: $$-\sin y\,y'+4x-y'=10.$$ Solving for the derivative gives $$\frac{dy}{dx}=\frac{4x-10}{1+\sin y}=\frac{2(2x-5)}{\sin y+1},$$ where the denominator is nonzero.
36|2|Apply the product and chain rules: $y+xy'+2yy'=6x$. Thus $$(x+2y)y'=6x-y\implies\frac{dy}{dx}=\frac{6x-y}{x+2y},$$ where $x+2y\ne0$.
37|4|We require $x^2+y^2=4$ with $x=2\cos t$. The choice $y=2\sin t$ gives $$x^2+y^2=4\cos^2t+4\sin^2t=4.$$ It parametrizes the full circular cross-section while $z$ is free. It is the only listed component with this property.
38|3|Substitute $x=2\cos t$ into $9x^2+4z^2=36$. Choosing $z=3\sin t$ gives $$9(2\cos t)^2+4(3\sin t)^2=36.$$ The parameter $y$ is free, as required for the cylinder.
40|3|The equation $z=9y^2$ restricts $y$ and $z$, while $x$ is free. Thus $f(x,y)=\langle x,y,9y^2\rangle$, and its first component is $x$.
42|3|Set $y=\sqrt3\tan t$ and $z=2\sec t$. Then $$3z^2-4y^2=12\sec^2t-12\tan^2t=12.$$ On $-\pi/2<t<\pi/2$, $\sec t\ge1$, so $z\ge2$. Thus the required second component is $\sqrt3\tan t$.
43|2|The diagram is the circle $x^2+y^2=4$. Differentiating gives $2x+2yy'=0$, so $$\frac{dy}{dx}=-\frac{x}{y}$$ for $y\ne0$.
44|3|The diagram gives center $(1,-1)$ and radius $3$, so $(x-1)^2+(y+1)^2=9$. Differentiating gives $2(x-1)+2(y+1)y'=0$. Therefore $$\frac{dy}{dx}=-\frac{x-1}{y+1}$$ for $y\ne-1$.
45|4|The ellipse has horizontal and vertical semiaxes $3$ and $2$, so its equation is $x^2/9+y^2/4=1$. Differentiating yields $2x/9+yy'/2=0$, hence $$\frac{dy}{dx}=-\frac{4x}{9y}$$ for $y\ne0$.
46|2|The right-opening parabola has vertex $(0,0)$ and passes through $(1,2)$. Its equation is $y^2=4x$. Differentiate to obtain $2yy'=4$, so $$\frac{dy}{dx}=\frac2y$$ for $y\ne0$.
47|2|The center is the midpoint of the diameter: $((-4+2)/2,(2+2)/2)=(-1,2)$. The diameter has length $6$, so the radius is $3$. Thus $$(x+1)^2+(y-2)^2=9.$$
48|4|The center is the midpoint of $(6,4)$ and $(-4,2)$, namely $(1,3)$. The squared diameter is $10^2+2^2=104$, so the squared radius is $104/4=26$. Hence $$(x-1)^2+(y-3)^2=26.$$
49|1|The diagram gives center $(1,3)$ and radius $3$. Substitute into $(x-h)^2+(y-k)^2=r^2$ to obtain $$(x-1)^2+(y-3)^2=9.$$
50|3|The diagram gives center $(-2,5)$ and radius $7$. Therefore $$(x+2)^2+(y-5)^2=49.$$
51|1|The squared radius is the squared distance from $C(-1,2)$ to $X(2,3)$: $r^2=(2+1)^2+(3-2)^2=10$. Hence the circle is $$(x+1)^2+(y-2)^2=10.$$
52|0|Compare $(x+5)^2+(y+1)^2=4$ with $(x-h)^2+(y-k)^2=r^2$. The center is $(-5,-1)$ and the radius is $\sqrt4=2$.
53|0|Multiplying by $3$ preserves direction and triples length. Multiplying by $-1$ reverses direction and preserves length. The correct diagram therefore has a long vector pointing northeast labeled $3a$, and a vector one-third as long pointing southwest labeled $-a$.
54|0|Factor the first vector: $4a-12b=4(a-3b)$. Since this common vector is nonzero, equality with $\lambda(a-3b)$ implies $\lambda=4$.
55|4|We have $a-12b=-2(-0.5a+6b)$. Since the vectors are nonzero, equality requires $\lambda=-2$.
56|0|The vector $-\tfrac12a$ has half the length of $a$ and the opposite direction. The original vector points northeast, so the correct diagram shows a vector half as long pointing southwest.
57|3|The field has potential $\phi=(x^2+y^2+z^2)/2$. At the initial point, $\phi=1/2$; at $t=\pi$, $\phi=(1+4\pi)/2$. Hence $$\int_C F\cdot dr=\phi(r(\pi))-\phi(r(0))=2\pi.$$ Equivalently $F(r(t))\cdot r'(t)=2$ for $t>0$; its integral has the same finite limit at $t=0$.
58|0|Since $-1\le\sin(2x+1)\le1$, multiply by $3$ and subtract $4$ to obtain $-7\le y\le-1$. Thus the range is $[-7,-1]$.
59|0|The midline lies halfway between the minimum and maximum: $$y=\frac{-9+1}{2}=-4.$$
60|0|As $\cos(x+\pi/4)$ ranges from $-1$ to $1$, its negative also ranges from $-1$ to $1$. Adding $3$ gives the range $[2,4]$. The minimum is $2$.
61|3|For $A\cos x$, the amplitude is $|A|$. Here it is $|5|=5$.
62|2|Rewrite the function as $f(x)=3/13-(2/13)\cos x$. Its amplitude is the absolute value of the cosine coefficient, $2/13$.
63|4|For $A\cos(Bx)$, the period is $2\pi/|B|$. Here $B=1/3$, so the period is $6\pi$.
64|1|Use $x=r\cos\theta$, $y=r\sin\theta$. With $r=1$ and $\theta=5\pi/3$, the coordinates are $(\tfrac12,-\tfrac{\sqrt3}2)$.
65|2|The radius of $A$ is $r=\sqrt{10+10}=2\sqrt5$. Thus $B$ has radius $2r=4\sqrt5$ and angle $\pi/3$, giving $$B=(4\sqrt5\cos(\pi/3),4\sqrt5\sin(\pi/3))=(2\sqrt5,2\sqrt{15}).$$
66|4|The coordinates of $A$ give $\cos\theta=\sqrt2/2$ and $\sin\theta=-\sqrt2/2$, so $\theta=-\pi/4$ modulo $2\pi$. The angle of $B$ is $-\pi/2$ modulo $2\pi$, and its radius is $1$. Therefore $B=(0,-1)$.
67|4|The diagram puts $B$ counterclockwise from $A$ in the second quadrant. Its angle is $\pi/4+5\pi/12=2\pi/3$ and its radius is $8$. Therefore $$B=(8\cos(2\pi/3),8\sin(2\pi/3))=(-4,4\sqrt3).$$
68|2|The diagram puts $B$ clockwise from $A$ in the second quadrant. Its angle is $210^\circ-75^\circ=135^\circ$ and its radius is $6$. Thus $$B=(6\cos135^\circ,6\sin135^\circ)=(-3\sqrt2,3\sqrt2).$$
69|4|Use $x=r\cos\theta$, $y=r\sin\theta$. With $r=4$ and $\theta=\pi/4$, both coordinates equal $4\sqrt2/2=2\sqrt2$. Thus $P=(2\sqrt2,2\sqrt2)$.
70|0|With $r=8$ and $\theta=240^\circ$, $$P=(8\cos240^\circ,8\sin240^\circ)=(-4,-4\sqrt3).$$
71|4|With $r=5$ and $\theta=330^\circ$, $$P=(5\cos330^\circ,5\sin330^\circ)=(\tfrac{5\sqrt3}2,-\tfrac52).$$
73|4|The sides adjacent to the $20^\circ$ angle are $5$ and $13$. The triangle area is $$\frac12(5)(13)\sin20^\circ\approx11.11565466.$$ Rounded to two decimal places, the area is $11.12$.
74|1|Draw diagonal $BD$. In $\triangle ABD$, $$BD^2=10^2+6^2-2(10)(6)\cos62^\circ\approx79.66341.$$ In $\triangle BCD$, the cosine rule gives $BD^2=9^2+CD^2-18(CD)\cos51.8^\circ$. The convex configuration shown selects $CD\approx11.009953$; the other root gives a concave configuration. Add the two triangle areas: $$[ABCD]=\tfrac12(10)(6)\sin62^\circ+\tfrac12(9)(11.009953)\sin51.8^\circ\approx65.42354.$$ Rounded to the nearest integer, the area is $65$.
75|2|The large triangle $ABD$ has area $\tfrac12(12)(9)\sin117^\circ\approx48.11435\,\mathrm{in}^2$. The concave quadrilateral is the part remaining after removing $\triangle BCD$, so $$[BCD]=[ABD]-[ABCD]\approx48.11435-15=33.11435\,\mathrm{in}^2.$$ Rounded to the nearest integer, the answer is $33\,\mathrm{in}^2$.
76|3|The area formula gives $$\tfrac12(5)(6)\sin A=\tfrac{15\sqrt3}{2}\implies\sin A=\tfrac{\sqrt3}{2}.$$ The marked angle is acute in the given diagram, selecting $A=60^\circ$ rather than its obtuse supplement.
77|2|Split the convex quadrilateral along $BD$ into triangles with included angles $80^\circ$ and $50^\circ$. Add their areas: $$[ABCD]=\tfrac12(5)(8)\sin80^\circ+\tfrac12(10)(7)\sin50^\circ\approx46.50771.$$ Rounded to the nearest tenth, the area is $46.5$.
78|0|The plane $y=0$ fixes $y$, so the slope of the intersection curve is $f_x$. At $P$, $$f_x(\pi/2,0)=0\cos(\pi/2)+\cos0=1.$$
79|0|For a scalar line integral, substitute the parametrization and multiply by speed. Here $r'(t)=\langle2\sqrt t,t-1\rangle$, so $\|r'(t)\|=\sqrt{4t+(t-1)^2}=t+1$ on $[0,1]$. Also $3x=4t^{3/2}$. Thus $$\int_C3x\,ds=4\int_0^1(t^{5/2}+t^{3/2})\,dt=4\left(\frac27+\frac25\right)=\frac{96}{35}.$$
80|1|Differentiating gives $r'(t)=3t\langle\cos t,\sin t\rangle$, so the speed is $3t$ on $[0,2\pi]$. Also $x^2+y^2=9(1+t^2)$. Hence $$\int_C(x^2+y^2)\,ds=27\int_0^{2\pi}(t+t^3)\,dt=54\pi^2+108\pi^4=54\pi^2(1+2\pi^2).$$
81|4|Here $x=t$, $y=\sin t$, and $z=1$. The speed is $\sqrt{1+\cos^2t}$. Thus $$\int_C4yz\cos x\,ds=\int_0^{\pi/2}4\sin t\cos t\sqrt{1+\cos^2t}\,dt.$$ Set $u=1+\cos^2t$, so $du=-2\sin t\cos t\,dt$. The integral becomes $$2\int_1^2u^{1/2}\,du=\frac43(2\sqrt2-1).$$ The omitted endpoints have finite limits and do not change this value.
82|0|Substitute $x=2t$, $y=2-t$ to get $x^3-y=8t^3+t-2$. The speed is $\sqrt{2^2+(-1)^2}=\sqrt5$. Therefore $$\int_C(x^3-y)\,ds=\sqrt5\int_{-1}^{2}(8t^3+t-2)\,dt.$$
83|3|The gradient is $\nabla g=\langle2x/y,-x^2/y^2\rangle$, so $\nabla g(2,1)=\langle4,-4\rangle$. Normalize the direction: $u=\langle-1,3\rangle/\sqrt{10}$. Hence $$D_ug=\nabla g\cdot u=\frac{-4-12}{\sqrt{10}}=-\frac{8\sqrt{10}}5.$$
84|4|The direction from $A$ to $B$ is $\langle3,4\rangle$, with unit vector $u=\langle3,4\rangle/5$. Since $\nabla f=\langle2(x+y^2),4y(x+y^2)\rangle$, we have $\nabla f(-1,-2)=\langle6,-24\rangle$. Therefore $$D_uf=\frac{18-96}{5}=-\frac{78}{5}.$$
85|4|Acceleration is $a(t)=v'(t)=4-6t$. At $t=2$, $a=-8\,\mathrm{m/s^2}$. Newton's second law gives $F=2(-8)=-16\,\mathrm N$, so the requested magnitude is $16\,\mathrm N$.
86|2|Acceleration is $v'(t)=3t^2-2e^t$. Multiply by the mass $5\,\mathrm{kg}$: $$F(t)=5(3t^2-2e^t)=15t^2-10e^t,$$ measured in newtons.
88|3|Differentiate position twice: $s'(t)=t^{-1/2}$ and $s''(t)=-\tfrac12t^{-3/2}$. Thus $F(t)=8s''(t)=-4t^{-3/2}\,\mathrm N$. At $t=4$, the force is $-1/2\,\mathrm N$, whose magnitude is $1/2\,\mathrm N$.
91|3|For a parametric curve, $$L=\int_a^b\sqrt{(x')^2+(y')^2}\,dt.$$ Here $x'=4\cos4t$ and $y'=-4\sin t$. Therefore $$L=4\int_0^2\sqrt{\cos^2(4t)+\sin^2t}\,dt.$$
92|4|Differentiate: $x'=2t$ and $y'=3t^2+2$. Thus $$(x')^2+(y')^2=4t^2+(3t^2+2)^2=9t^4+16t^2+4.$$ Therefore $$L=\int_{-1}^1\sqrt{9t^4+16t^2+4}\,dt.$$
93|3|Differentiate: $x'=2t+2$, $y'=2t^2-2$. Their squared sum is $$4(t+1)^2+4(t^2-1)^2=4(t^4-t^2+2t+2).$$ Hence $$L=2\int_{-3}^2\sqrt{t^4-t^2+2t+2}\,dt.$$ The square root keeps the speed nonnegative on the entire interval, including where $t+1$ changes sign.
94|0|Integrate $f_x=2xy$ with respect to $x$: $f=x^2y+g(y,z)$. Matching $f_y=x^2+2z$ gives $g_y=2z$, so $g=2yz+h(z)$. Finally $f_z=2y+h'(z)=2y$, hence $h$ is constant. Therefore $$f=x^2y+2yz+C.$$ Its three partial derivatives reproduce all components of $F$.
95|0|Integrate $f_x=\cos x$: $f=\sin x+g(y)$. Then $f_y=g'(y)=\sin y$ gives $g(y)=-\cos y+C$. Thus $$f(x,y)=\sin x-\cos y+C,$$ whose gradient is exactly $\langle\cos x,\sin y\rangle$.
96|2|Use the Euclidean norm: $$\|v\|=\sqrt{4^2+(-1)^2}=\sqrt{17}.$$
97|3|First $a+3b=\langle-1,0\rangle+3\langle3,-2\rangle=\langle8,-6\rangle$. Its norm is $10$. Dividing by this positive norm preserves direction and gives the unit vector $\langle4/5,-3/5\rangle$.
98|3|Use the Euclidean norm: $$\|a\|=\sqrt{(-12)^2+3^2}=\sqrt{153}=3\sqrt{17}.$$
99|0|The displacement is $\overrightarrow{AB}=\langle3-(-4),0-1\rangle=\langle7,-1\rangle$. Its length is $$\sqrt{7^2+(-1)^2}=\sqrt{50}=5\sqrt2.$$
100|4|The displacement is $\overrightarrow{PQ}=\langle3-(-2),3-2\rangle=\langle5,1\rangle$. Its length is $$\sqrt{5^2+1^2}=\sqrt{26}.$$
101|3|The norm of $a$ is $\sqrt{3^2+8^2}=\sqrt{73}$. Dividing by this positive number preserves direction and gives $$\frac{a}{\|a\|}=\begin{bmatrix}3/\sqrt{73}\\8/\sqrt{73}\end{bmatrix}.$$
102|2|The square root requires $9-x^2-y^2\ge0$, and the denominator requires $x+y\ne0$. Thus $$D=\{(x,y)\in\mathbb R^2:x^2+y^2\le9,\ x+y\ne0\}.$$ This is the closed disk of radius $3$, with the line $x+y=0$ removed.
103|3|The logarithm requires $x+2>0$, hence $x>-2$. The denominator requires $y-2\ne0$, hence $y\ne2$. The correct diagram shades the half-plane to the right of $x=-2$, excludes that boundary, and removes the horizontal line $y=2$.
'''
cas=[];keys=[];new=[];proof=[]
for line in DATA.strip().splitlines():
 idx,choice,solution=line.split('|',2);idx=int(idx);ctx=contexts[idx];q=ctx['q'];mid=q[':question/math-academy-id'];fs=q[':question/answer-fields'];assert len(fs)==(2 if choice=='new' else 1)
 assert not q.get(':question/worked-solution'),mid
 evidence={'basis':9837,'identity':mid,'authorship':'Locally derived completion, not an observed Math Academy worked solution','canonical_example':ctx.get('canonical',{}).get(':db/id')if isinstance(ctx.get('canonical'),dict)else ctx.get('canonical'),'matching_nearby':[v.get(':db/id')for v in ctx.get('nearby',[])],'independent_derivation':solution,'template':'Use the owning KP method; solve the unchanged target parameters, then verify response shape and each complete existing bank choice. Visual targets use completion-visual-index.json and contact sheets.'}
 cas.append({'entity':q[':db/id'],'attribute':'question/worked-solution','before':None,'after':solution,'reason':'Author missing worked solution from independently solved target and owning KP teaching context','evidence':evidence,'confidence':'high'})
 if choice=='new':
  for f in fs:
   value='-2'if f[':answer-field/key']=='field-1'else'3';assert not f.get(':answer-field/choices')
   aid=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:authored-canonical:'+f[':answer-field/id']+':math:'+value))
   new.append({'question':q[':db/id'],'math_academy_id':mid,'field':f[':db/id'],'field_uuid':f[':answer-field/id'],'field_key':f[':answer-field/key'],'field_type':f[':answer-field/type'][':db/id'],'expected_choices':[],'answer_id':aid,'answer_type':17592186045498,'value':value,'correct_before':None,'worked_solution':solution,'evidence':evidence})
 else:
  f=fs[0];a=f[':answer-field/choices'][int(choice)];assert not f.get(':answer-field/correct')
  keys.append({'entity':f[':db/id'],'attribute':'answer-field/correct','before':None,'after':a[':db/id'],'question':q[':db/id'],'math_academy_id':mid,'reason':'Link uniquely correct existing owned answer after independent solution and complete-bank review','evidence':dict(evidence,canonical_value=a[':answer/value'],owned_choices=[x[':db/id']for x in f[':answer-field/choices']]),'confidence':'high'})
 proof.append({'question':q[':db/id'],'math_academy_id':mid,'problem':q[':question/problem'],'canonical':ctx.get('canonical'),'nearby':ctx.get('nearby'),'derivation':solution,'correct_answer_values':([n['value']for n in new if n['question']==q[':db/id']]if choice=='new'else[a[':answer/value']]),'proof_kind':'Exact algebra/calculus or visually verified geometry plus complete-bank comparison','evidence':evidence})
(H/'completion-cas.json').write_text(json.dumps(cas,indent=2)+'\n');(H/'key-proposals.json').write_text(json.dumps(keys,indent=2)+'\n');(H/'new-answer-plan.json').write_text(json.dumps({'basis':9837,'cas':[],'new_answers':new},indent=2)+'\n');(H/'completion-proofs.json').write_text(json.dumps(proof,indent=2)+'\n')
print('solutions',len(cas),'keys',len(keys),'new',len(new))

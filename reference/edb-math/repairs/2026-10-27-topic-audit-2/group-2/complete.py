import json,uuid,copy
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());Q={q[':question/math-academy-id']:q for q in D['questions']if q.get(':question/math-academy-id')};CTX={x['q'][':question/math-academy-id']:x for x in json.loads((H/'completion-context.json').read_text())}
# All values are existing field-owned answers. Each target was solved independently;
# canonical/nearby examples supply method and response shape, not its answer.
K={17540:[17592186085093],334915:[17592186085474,17592186085469],334916:[17592186085480,17592186085485],335069:[17592186085493,17592186085496],335392:[17592186085501,17592186085506],8546:[17592186087273],132252:[17592186189639],158465:[17592186190980],158466:[17592186190986],159724:[17592186191031],70024:[17592186192186],132241:[17592186121314],132257:[17592186121324],158413:[17592186121443],159604:[17592186121458],108446:[17592186144142],108447:[17592186144147],1117:[17592186107247],66808:[17592186109954],66830:[17592186109961],969:[17592186110282],318659:[17592186216443,17592186216448],337143:[17592186216625],337212:[17592186216636,17592186216639,17592186216629,17592186216642],337692:[17592186216648,17592186216653],332878:[17592186164406,17592186164408],332880:[17592186164414,17592186164419],141055:[17592186098273],141117:[17592186098291],36435:[17592186113836],47069:[17592186114207],47071:[17592186114214],47080:[17592186114219],54486:[17592186114350],339217:[17592186174938],339225:[17592186174941],339241:[17592186174951],339244:[17592186174953],339269:[17592186174961],339309:[17592186174973],2425:[17592186061866]}
S={
17540:r'''The equation is in standard form with $P(x)=1$ and $Q(x)=\cos x$. An integrating factor is
$$
I(x)=e^{\int 1\,\mathrm{d}x}=e^x.
$$
Multiplying through by $e^x$ and using the product rule gives
$$
e^xy'+e^xy=e^x\cos x,\qquad \frac{\mathrm{d}}{\mathrm{d}x}(ye^x)=e^x\cos x.
$$''',
8546:r'''Here $P(x)=2x$, so an integrating factor is
$$
I(x)=e^{\int 2x\,\mathrm{d}x}=e^{x^2}.
$$
Multiplication by $I(x)$ gives the exact derivative
$$
\frac{\mathrm{d}}{\mathrm{d}x}(ye^{x^2})=e^{x^2}\cdot 2xe^{-x^2}.
$$
The product rule verifies the left side is $e^{x^2}(y'+2xy)$.''',
334915:r'''For $x>0$, an integrating factor is
$$
I(x)=e^{\int(2/x)\,\mathrm{d}x}=e^{2\ln x}=x^2.
$$
Multiplying by $x^2$ and integrating gives
$$
(x^2y)'=3x^2,\qquad x^2y=x^3+C,\qquad y=x+\frac{C}{x^2}.
$$
Differentiation gives $y'+2y/x=3$, as required.''',
334916:r'''An integrating factor is $I(x)=e^x$. Thus
$$
(e^xy)'=e^x,\qquad e^xy=e^x+C,\qquad y=1+Ce^{-x}.
$$
The initial condition gives $-3=1+C$, so $C=-4$. Therefore
$$
y(x)=1-4e^{-x}=1-\frac4{e^x}.
$$
This satisfies both $y'+y=1$ and $y(0)=-3$.''',
335069:r'''First divide by $2$:
$$
y'+\frac12y=\frac32x.
$$
An integrating factor is $I(x)=e^{x/2}$. Integration by parts gives
$$
(ye^{x/2})'=\frac32xe^{x/2},\qquad ye^{x/2}=3(x-2)e^{x/2}+C.
$$
Hence
$$
y=3(x-2)+Ce^{-x/2}.
$$
Substitution verifies $2y'+y=3x$.''',
335392:r'''An integrating factor is $I(x)=e^{-2x}$. Multiplying and integrating gives
$$
(ye^{-2x})'=x^2,\qquad ye^{-2x}=\frac{x^3}{3}+C.
$$
Therefore
$$
y=\frac{x^3e^{2x}}3+Ce^{2x}.
$$
Differentiating verifies $y'-2y=x^2e^{2x}$.''',
132252:r'''Treat $x$ and $y$ as constants and apply the chain rule:
$$
\frac{\partial f}{\partial z}=y\cdot\frac12(x^2+z^2)^{-1/2}\cdot 2z=\frac{yz}{\sqrt{x^2+z^2}}.
$$
The formula holds when $x^2+z^2>0$. At $x=z=0$, this partial derivative exists only when $y=0$.''',
158465:r'''Treat $x$ as constant. The product rule gives
$$
\frac{\partial f}{\partial y}=0+x\left(\sin y+y\cos y\right)=x(\sin y+y\cos y).
$$''',
158466:r'''Using the quotient rule while holding $y$ fixed,
$$
f_x(x,y)=\frac{-(x+y)\sin x-\cos x}{(x+y)^2}.
$$
At $(\pi,0)$, the denominator is nonzero and
$$
f_x(\pi,0)=\frac{-\pi\sin\pi-\cos\pi}{\pi^2}=\frac1{\pi^2}.
$$''',
159724:r'''The quotient rule gives
$$
f_y=\frac{(2ye^{y^2})(x^2-2y)-e^{y^2}(-2)}{(x^2-2y)^2}
=\frac{(2x^2y-4y^2+2)e^{y^2}}{(x^2-2y)^2}.
$$
Thus $h(x,y)=2x^2y-4y^2+2$. The derivative is defined where $x^2-2y\ne0$.''',
70024:r'''Treat $x$ as constant and apply the chain rule:
$$
f_y=e^{4x-x^4y}\frac{\partial}{\partial y}(4x-x^4y)=-x^4e^{4x-x^4y}.
$$''',
132241:r'''Hold $x$ constant and differentiate term by term:
$$
f_y=\frac{\partial}{\partial y}(xy^2)+\frac{\partial}{\partial y}(x^2\cos y)=2xy-x^2\sin y.
$$''',
132257:r'''Treat $y$ as constant:
$$
f_x=y^2\sec^2x-\frac{y}{x^2}.
$$
Since $\sec^2\pi=1$,
$$
f_x(\pi,2)=4-\frac2{\pi^2}.
$$''',
158413:r'''The partial derivative with respect to $y$ keeps $x$ fixed and increments only $y$. Its defining difference quotient is
$$
\frac{\partial f}{\partial y}=\lim_{h\to0}\frac{f(x,y+h)-f(x,y)}{h}=\lim_{h\to0}\frac{x\sqrt{y+h}-x\sqrt y}{h}.
$$
For the usual two-sided derivative, this limit is taken at $y>0$.''',
159604:r'''Treat $y$ as constant:
$$
f_x=2^x\ln2\tan y-\frac{2y}{\pi x^3}.
$$
At $(1,\pi/4)$, $\tan(\pi/4)=1$, so
$$
f_x(1,\pi/4)=2\ln2-\frac{2(\pi/4)}\pi=2\ln2-\frac12.
$$''',
108446:r'''A Bernoulli equation has the form $y'+P(x)y=Q(x)y^n$ with $n\ne0,1$.

I has this form with $n=2$. II has a $y^2$ term instead of the required linear $P(x)y$ term. III has this form with $n=-1/2$, on its real domain $y>0$.

Therefore the correct selection is **I and III only**.''',
108447:r'''A Bernoulli equation has the form $y'+P(x)y=Q(x)y^n$ with $n\ne0,1$.

For I, division by $y$ gives $y'+x^2y^2=e^xy^3$, which still has two nonlinear powers. For II, division by $y^2$ gives
$$
y'+x^2y=e^xy^2,
$$
which is Bernoulli with $n=2$ on intervals where $y\ne0$. The original II also admits $y=0$, which should be checked separately when solving. III contains trigonometric functions of $y$ and does not have Bernoulli form.

Therefore the correct selection is **II only**.''',
1117:r'''Isolate the exponential term and take logarithms:
$$
10^{2x}=62,\qquad 2x\ln10=\ln62,\qquad x=\frac{\ln62}{2\ln10}\approx0.896196.
$$
Rounded to three decimal places, $x=0.896$.''',
66808:r'''Take logarithms of both positive sides:
$$
(2-3x)\ln2=\ln12,\qquad x=\frac{2-\ln12/\ln2}{3}\approx-0.528321.
$$
Rounded to three decimal places, $x=-0.528$.''',
66830:r'''Isolate $3^y$:
$$
4\cdot3^y=24,\qquad3^y=6.
$$
Since $3^y$ is strictly increasing, the unique real solution is
$$
y=\log_3 6=\frac{\ln6}{\ln3}.
$$''',
969:r'''Take natural logarithms:
$$
y\ln3=\ln23,\qquad y=\frac{\ln23}{\ln3}\approx2.854050.
$$
Rounded to three decimal places, $y=2.854$.''',
332393:r'''Try $y_p=Be^{2x}$, so $y_p'=2Be^{2x}$. Substitution gives
$$
9(2Be^{2x})+18Be^{2x}=4e^{2x},\qquad36B=4.
$$
Therefore
$$
y_p(x)=\frac19e^{2x}.
$$
Direct substitution verifies the equation; the complementary term is not included in this particular solution.''',
332426:r'''Try $y_p=Be^{2x}$. Substitution into $y'-6y=8e^{2x}$ gives $(2-6)B=8$, so $B=-2$. Adding the complementary solution,
$$
y=Ae^{6x}-2e^{2x}.
$$
The initial condition gives $1=A-2$, so $A=3$ and
$$
y(x)=3e^{6x}-2e^{2x}.
$$
Its residual $y'-6y-8e^{2x}$ is zero and $y(0)=1$.''',
332532:r'''The forcing term has the same exponential form as the complementary solution, so try $y_p=Bxe^{4x}$. Then
$$
y_p'=Be^{4x}+4Bxe^{4x},\qquad y_p'-4y_p=Be^{4x}.
$$
Thus $B=3$. Adding the complementary solution gives
$$
y(x)=(A+3x)e^{4x},\qquad A\in\mathbb R.
$$
This family satisfies $y'-4y=3e^{4x}$.''',
332645:r'''Try $y_p=Be^{-3x}$, so $y_p'=-3Be^{-3x}$. Substituting gives
$$
5(-3Be^{-3x})+10Be^{-3x}=15e^{-3x},\qquad-5B=15.
$$
Therefore
$$
y_p(x)=-3e^{-3x}.
$$
Direct substitution verifies the equation.''',
332797:r'''Because $e^{3x}$ already occurs in the complementary solution, try $y_p=Bxe^{3x}$. Substitution gives
$$
y_p'-3y_p=Be^{3x}=9e^{3x},
$$
so $B=9$. The general solution is $y=(A+9x)e^{3x}$. The condition $y(0)=2$ gives $A=2$, hence
$$
y(x)=(2+9x)e^{3x}.
$$
Both the differential equation and initial condition are satisfied.''',
318659:r'''For $P\,\mathrm dx+Q\,\mathrm dy=0$, an integrating factor $I(x)$ must satisfy
$$
I P_y=I'Q+I Q_x,\qquad \frac{I'}I=\frac{P_y-Q_x}{Q}=g(x).
$$
Consequently
$$
I(x)=\exp\left(\int g(x)\,\mathrm dx\right).
$$
For this equation take $P=x-2xy$, $Q=1$. Then $g(x)=-2x$ and $I(x)=e^{-x^2}$; direct differentiation verifies exactness. The ratio criterion is used where its denominator is nonzero.''',
337143:r'''Multiply each coefficient of the original equation by $I(y)=e^y$. The equation to test is
$$
((y+x)e^y)\,\mathrm dx+(xe^y)\,\mathrm dy=0.
$$
This is the required transformed equation. In fact,
$$
\frac{\partial}{\partial y}((y+x)e^y)=(1+x+y)e^y,\qquad\frac{\partial}{\partial x}(xe^y)=e^y.
$$
These are not identically equal, so $e^y$ does **not** make this equation exact. Selecting the product equation alone does not establish that it is an integrating factor.''',
337212:r'''For an integrating factor depending only on $x$, exactness requires
$$
\frac{I'}I=\frac{P_y-Q_x}{Q}=g(x),\qquad I(x)=\exp\left(\int g(x)\,\mathrm dx\right).
$$
Here $P=7x-4xy$ and $Q=1$, so
$$
P_y=-4x,\qquad Q_x=0.
$$
Thus $g(x)=-4x$ and $I(x)=e^{-2x^2}$. These identify the four requested selections in their existing fields.''',
337692:r'''For an integrating factor depending only on $y$, exactness requires
$$
I P_y+I'P=I Q_x,\qquad\frac{I'}I=-\frac{P_y-Q_x}{P}=-h(y).
$$
Therefore the requested selections are
$$
h(y)=\frac{P_y-Q_x}{P},\qquad I(y)=\exp\left(-\int h(y)\,\mathrm dy\right).
$$
Here $P=x(y^2+1)$, $Q=1$, giving $h(y)=2y/(1+y^2)$ where the ratio is defined. Hence $I(y)=1/(1+y^2)$; this factor extends to every real $y$ and makes the equation exact even at $x=0$.''',
332878:r'''Set $c_1=1$ and $c_2=0$ in the general solution. This gives
$$
x(t)=-2\sin(6t),\qquad y(t)=3\cos(6t).
$$
The frequency is $6$ in both coordinates: $x'=-12\cos(6t)=-4y$ and $y'=-18\sin(6t)=9x$. Thus these two existing choices satisfy the system. The original source's $2t$ in the second coordinate is a typographical error.''',
332880:r'''Set $c_1=1$ and $c_2=0$:
$$
x(t)=e^{2t}\cos(3t),\qquad y(t)=e^{2t}\sin(3t).
$$
Differentiating gives $x'=2x-3y$ and $y'=3x+2y$, so this pair satisfies the system.''',
141055:r'''Substitute the initial condition into the given family:
$$
3=Ae^{2\cdot1},\qquad A=\frac3{e^2}.
$$
For this value, $y(1)=3$, and $y'=2Ae^{2x}=2y$ verifies the differential equation.''',
141117:r'''Substitute $x=1$ and $y=4$:
$$
4=\frac1{A-1},\qquad A-1=\frac14,\qquad A=\frac54.
$$
The resulting solution satisfies $y'=1/(5/4-x)^2=y^2$ on the interval $x<5/4$ containing the initial point $x=1$.''',
36435:r'''Exponential functions are continuous, and the denominator is nonzero at $x=0$. Direct substitution gives
$$
\lim_{x\to0}\frac{4^x-5}{2^x-2}=\frac{1-5}{1-2}=4.
$$''',
47069:r'''By continuity of the exponential function,
$$
\lim_{x\to3}10^{3x-7}=10^{3\cdot3-7}=10^2=100.
$$''',
47071:r'''As $x\to\infty$, the exponent $2x+4$ tends to $\infty$. Since the base $2>1$,
$$
\lim_{x\to\infty}2^{2x+4}=\infty.
$$''',
47080:r'''Write $8^{-x}=1/8^x$. Since $8^x\to\infty$ as $x\to\infty$,
$$
\lim_{x\to\infty}8^{-x}=0.
$$''',
54486:r'''Because $6>1$, $6^x\to0$ as $x\to-\infty$. Multiplication by the constant $-7$ preserves this limit:
$$
\lim_{x\to-\infty}(-7\cdot6^x)=0.
$$''',
339217:r'''The model has solution $P(t)=P_0e^{rt}$. Doubling after ten years gives $e^{10r}=2$, so $r=\ln2/10$. For tripling,
$$
e^{rt}=3,\qquad t=\frac{\ln3}{r}=\frac{10\ln3}{\ln2}\approx15.8496.
$$
It took **15.8 years**, to one decimal place.''',
339225:r'''The model has solution $T(t)=T_0e^{-rt}$. Reducing **by** four-fifths leaves one-fifth, so $e^{-2r}=1/5$ and $r=\ln5/2$. Reducing to one-fifteenth requires
$$
e^{-rt}=\frac1{15},\qquad t=\frac{\ln15}{r}=\frac{2\ln15}{\ln5}\approx3.3652.
$$
The required time is **3.4 minutes**, to one decimal place.''',
339241:r'''For $P'=-0.1P$, populations four years apart satisfy
$$
P(9)=P(5)e^{-0.1(9-5)}=3200e^{-0.4}\approx2145.024.
$$
Thus the model predicts approximately **2145 penguins**, to the nearest whole penguin.''',
339244:r'''The model is $P(t)=P_0e^{0.09t}$. At $t=18$,
$$
8000=P_0e^{1.62},\qquad P_0=8000e^{-1.62}\approx1583.190.
$$
The initial population was approximately **1583 fish**, to the nearest whole fish.''',
339269:r'''With $P(0)=150000$, the solution is $P(t)=150000e^{0.055t}$. Set $P(t)=400000$ and solve:
$$
t=\frac{\ln(400000/150000)}{0.055}\approx17.8333.
$$
Rounded to the nearest year, the answer is **18 years**.''',
339309:r'''With $N(0)=150000$, the solution is $N(t)=150000e^{-0.05t}$. Reaching $50000$ particles requires
$$
e^{-0.05t}=\frac13,\qquad t=\frac{\ln3}{0.05}\approx21.9722.
$$
Rounded to the nearest year, this is **22 years**.''',
2425:r'''Use integration by parts with $u=x$ and $\mathrm dv=2^x\,\mathrm dx$. Then $\mathrm du=\mathrm dx$ and $v=2^x/\ln2$, so
$$
\int x2^x\,\mathrm dx=\frac{x2^x}{\ln2}-\frac1{\ln2}\int2^x\,\mathrm dx
=\frac{2^x}{\ln2}\left(x-\frac1{\ln2}\right)+C.
$$
Differentiating the result gives $x2^x$, which verifies the antiderivative.'''
}
new={332393:r'\frac19e^{2x}',332426:r'3e^{6x}-2e^{2x}',332532:r'(A+3x)e^{4x}',332645:r'-3e^{-3x}',332797:r'(2+9x)e^{3x}'}
content=[];keys=[];creation=[];evidence=[]
for n,solution in S.items():
 ident='q-'+str(n);q=Q[ident];ctx=CTX[ident];ev={'basis':9122,'question':q[':db/id'],'source_identity':ident,'kp':ctx['kp'],'canonical':ctx['canonical'].get(':db/id')if isinstance(ctx['canonical'],dict)else ctx['canonical'],'method':'Independently derived target; canonical and nearby examples supply instructional template; derivation and domain/units in authored solution','authored':True}
 if not q.get(':question/worked-solution'):content.append({'entity':q[':db/id'],'attribute':'question/worked-solution','before':None,'after':solution,'reason':'Authored missing worked solution using independent target calculation and matching KP canonical template','evidence':ev,'confidence':'high'})
 if n in K:
  for aid in K[n]:
   f=next(f for f in q[':question/answer-fields']if any(a[':db/id']==aid for a in f.get(':answer-field/choices',[])));assert not f.get(':answer-field/correct');a=next(a for a in f[':answer-field/choices']if a[':db/id']==aid)
   keys.append({'entity':f[':db/id'],'attribute':'answer-field/correct','before':None,'after':aid,'reason':'Unique existing field-owned answer independently proved by authored solution','evidence':{**ev,'key':f[':answer-field/key'],'value':a[':answer/value']},'confidence':'high'})
 if n in new:
  f=q[':question/answer-fields'][0];assert not f.get(':answer-field/choices')and not f.get(':answer-field/correct');value=new[n];answeruuid=str(uuid.uuid5(uuid.UUID(f[':answer-field/id']),'answer.type/math\n'+value))
  creation.append({'question':q[':db/id'],'question_identity':ident,'field':f[':db/id'],'field_uuid':f[':answer-field/id'],'key':f[':answer-field/key'],'before_choices':[],'before_correct':None,'answer_uuid':answeruuid,'answer_type':'answer.type/math','value':value,'canonical_solution':solution,'evidence':ev,'confidence':'high'})
 evidence.append({'question':q[':db/id'],'identity':ident,'solution':solution,'key_ids':K.get(n,[]),'new_blank_value':new.get(n),'evidence':ev})
# Existing completed six-field scaffold: a source dropdown's text choice was
# incorrectly attached as the key to two older mathematical banks.
q=Q['q-337133']
for fid,aid in [(17592186311416,17592186310402),(17592186311317,17592186310263)]:
 f=next(f for f in q[':question/answer-fields']if f[':db/id']==fid);assert any(a[':db/id']==aid for a in f[':answer-field/choices']);keys.append({'entity':fid,'attribute':'answer-field/correct','before':f[':answer-field/correct'][':db/id'],'after':aid,'reason':'Repair foreign text is key attached to existing mathematical bank; multiplication and partial differentiation prove unique existing answer','evidence':{'question':q[':db/id'],'basis':9122,'source':'archive6353 and q337133-after capture','derivation':'I=y/x^3, P=-y, Q=x => IP=-y^2/x^3, IQ=y/x^2, (IP)_y=(IQ)_x=-2y/x^3'},'confidence':'high'})
(H/'completion-proposals.json').write_text(json.dumps(content,indent=2)+'\n');(H/'key-proposals.json').write_text(json.dumps(keys,indent=2)+'\n');(H/'new-blank-answer-proposals.json').write_text(json.dumps(creation,indent=2)+'\n');(H/'completion-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('solutions',len(content),'keys',len(keys),'new blanks',len(creation))

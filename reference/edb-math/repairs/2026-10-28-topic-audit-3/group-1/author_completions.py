import json,uuid
from pathlib import Path
H=Path(__file__).resolve().parent
D=json.loads((H/'current.json').read_text());I={q.get(':question/math-academy-id'):q for q in D['questions']}
# Independently derived results. Graph choices use the separately retained visual panels.
rows=r'''
54286|17592186053452|The line has slope $2$ and vertical intercept $-4$. It passes through $(0,-4)$ and $(2,0)$, so choose the graph with these intercepts and positive slope $2$.
59676|17592186053816|Substituting $x=0,1,2,3$ into $y=-x+1$ gives $y=1,0,-1,-2$. The required graph passes through these four points and slopes downward.
59678|17592186053819|The equation $y=\frac12x-2$ has vertical intercept $-2$ and horizontal intercept $4$. Choose the line through $(0,-2)$ and $(4,0)$.
1578|17592186056787|Using $\sin^2\theta+\cos^2\theta=1$, the expression simplifies to $2$.
1579|17592186056795|On the domain of the original expression, rationalize and simplify:
$$\frac{\cos\theta}{1-\sin\theta}-\tan\theta=\frac{1+\sin\theta}{\cos\theta}-\frac{\sin\theta}{\cos\theta}=\frac1{\cos\theta}=\sec\theta.$$
23522|17592186057999|Use a common denominator and the Pythagorean identity:
$$\cos\theta+\frac{\sin^2\theta}{\cos\theta}=\frac{\cos^2\theta+\sin^2\theta}{\cos\theta}=\sec\theta.$$
65162|17592186058684|Where the original denominator is nonzero,
$$\cos^2\theta\left(1+\frac{\sin^2\theta}{\cos^2\theta}\right)=\cos^2\theta+\sin^2\theta=1.$$
65163|17592186058687|Factor out $\cos\theta$:
$$\cos^3\theta+\cos\theta\sin^2\theta=\cos\theta(\cos^2\theta+\sin^2\theta)=\cos\theta.$$
65165|17592186058697|On the domain of the original fraction,
$$\frac{\cos^2\theta\sin^2\theta+\sin^4\theta}{\cos\theta\sin\theta}=\frac{\sin^2\theta(\cos^2\theta+\sin^2\theta)}{\cos\theta\sin\theta}=\tan\theta.$$
65166|17592186058699|For the original expression, $\sin\theta\ne0$. Factoring its denominator gives
$$\frac{\sin^2\theta}{\sin^3\theta+\sin\theta\cos^2\theta}=\frac{\sin^2\theta}{\sin\theta(\sin^2\theta+\cos^2\theta)}=\sin\theta.$$
65193|17592186058721|Factor and apply the Pythagorean identity:
$$\sin^2\theta\cos^3\theta+\sin^4\theta\cos\theta=\sin^2\theta\cos\theta(\cos^2\theta+\sin^2\theta)=\sin^2\theta\cos\theta.$$
1304|17592186056513|Subtract corresponding components:
$$\langle12,5\rangle-\langle9,-2\rangle=\langle12-9,5-(-2)\rangle=\langle3,7\rangle.$$
1323|17592186056527|Subtract corresponding components:
$$\langle4,1\rangle-\langle1,-4\rangle=\langle3,5\rangle.$$
1386|17592186056609|Multiply each component by $3$:
$$3\langle8,-7\rangle=\langle24,-21\rangle.$$
17611|17592186057068|First scale, then add components:
$$\langle-2,1\rangle+2\langle4,-1\rangle=\langle-2+8,1-2\rangle=\langle6,-1\rangle.$$
18040|17592186057103|Compute $2\mathbf b-3\mathbf c=\langle6,6\rangle-\langle-24,12\rangle=\langle30,-6\rangle$. Therefore
$$\mathbf a-(2\mathbf b-3\mathbf c)=\langle4,-2\rangle-\langle30,-6\rangle=\langle-26,4\rangle.$$
18041|17592186057113|Compute $2\mathbf b+5\mathbf c=\langle8,2\rangle+\langle-5,10\rangle=\langle3,12\rangle$. Therefore
$$\mathbf a-(2\mathbf b+5\mathbf c)=\langle1,1\rangle-\langle3,12\rangle=\langle-2,-11\rangle.$$
70401|17592186058978|Collect the corresponding components:
$$(7\mathbf i-6\mathbf j)+(3\mathbf i+2\mathbf j)=10\mathbf i-4\mathbf j.$$
70402|17592186058984|Distribute the scalar and collect components:
$$2(4\mathbf i+2\mathbf j)+(6\mathbf i-4\mathbf j)=14\mathbf i.$$
1408|17592186056644|The source asks for the cross product. Expanding its determinant gives
$$\mathbf u\times\mathbf v=\left\langle9(3)-6(-3),\ 6(0)-\frac13(3),\ \frac13(-3)-9(0)\right\rangle=\langle45,-1,-1\rangle.$$
19783|17592186057623|The source condition is the magnitude of a cross product. Compute
$$\mathbf a\times\mathbf b=\langle-7x,11x,-5\rangle.$$
Squaring the magnitude equation gives $170x^2+25=705$, so $x^2=4$ and $x=\pm2$.
29634|17592186062334|An antiderivative of $x^3$ is $x^4/4$. Thus
$$\int_{-2}^{2}x^3\,dx=\left[\frac{x^4}{4}\right]_{-2}^{2}=4-4=0.$$
29639|17592186062344|Since $x\ge0$ on the interval, $\sqrt{x^5}=x^{5/2}$. Hence
$$\int_0^4\sqrt{x^5}\,dx=\left[\frac27x^{7/2}\right]_0^4=\frac27(128)=\frac{256}{7}.$$
49222|17592186063177|Apply the power rule:
$$\int_1^2x^{-4}\,dx=\left[-\frac1{3x^3}\right]_1^2=-\frac1{24}+\frac13=\frac7{24}.$$
49228|17592186063190|On this nonnegative interval, the integrand is $x^{3/5}$. Thus
$$\int_0^1\sqrt[5]{x^3}\,dx=\left[\frac58x^{8/5}\right]_0^1=\frac58.$$
15558|17592186080170|At $t=-1$, the point is $(0,1)$, while $x'(t)=4t^3+1=-3$ and $y'(t)=2t=-2$. The tangent slope is $2/3$, so the normal slope is $-3/2$. The normal is $y=1-3x/2$; setting $y=0$ gives $x=2/3$.
21206|17592186080748|Since $dx/dt=1$ and $dy/dt=3t^2$, we have $dy/dx=3t^2$. A horizontal tangent requires $dy/dx=0$, which gives $t=0$.
6862|17592186082412|At $t=-1$ the point is $(3,-1)$. The tangent slope is
$$\frac{dy}{dx}=\frac{5t^4}{2t-2}=-\frac54.$$
Hence its equation is $y+1=-\frac54(x-3)$.
16203|17592186084915|The square root requires $t\ge0$. Therefore $y=\sqrt t\ge0$ and $x=t(t+6)\ge0$, so the curve lies in the first quadrant together with the origin.
16205|17592186084922|Complete the square:
$$x=t^2-4t=(t-2)^2-4\ge-4.$$
The lower bound is attained at $t=2$.
6827|17592186086272|Substitute the indicated parameter values: $a=(-2)^2+(-2)=2$, $b=0^2-0=0$, and $c=3^2+3=12$. Thus $a+b+c=14$.
70341|17592186086344|Using $-1\le\cos\theta,\sin\theta\le1$, we obtain $-4\le x\le2$ and $0\le y\le4$.
15799|17592186084855|Eliminating the parameter gives
$$(x+3)^2+(y-5)^2=9^2(\cos^2t+\sin^2t)=81.$$
This is a circle centered at $(-3,5)$ with radius $9$.
15804|17592186084865|The standard counterclockwise circle of radius $8$ about the origin is $x=8\cos t$, $y=8\sin t$. At $t=0$ it starts at $(8,0)$, and its initial velocity points upward as required.
15851|17592186084869|The parametrization $x=6\cos t$, $y=6\sin t$ satisfies $x^2+y^2=36$, giving the circle of radius $6$ about the origin.
78205|17592186086785|Translate the standard radius-$2$ circle to center $(-1,2)$:
$$x=2\cos t-1,\qquad y=2\sin t+2.$$
At $t=0$ it starts at $(1,2)$ and moves counterclockwise.
79205|17592186086864|The displayed arc lies in the third quadrant, from $(-4,0)$ to $(0,-4)$. In $x=4\cos\theta$, $y=4\sin\theta$, these endpoints occur at $\theta=\pi$ and $\theta=3\pi/2$, respectively. Use $\pi\le\theta\le3\pi/2$.
15755|17592186098600|From $x=t-2$ we have $t=x+2$. Substitution into $y=t^2$ gives $y=(x+2)^2$, with no restriction on real $x$.
20051|17592186102635|The source asks for $\mathbf a\cdot(\mathbf b\times\mathbf c)$. Compute
$$\mathbf b\times\mathbf c=\langle-22,8,2\rangle,$$
then $\langle3,1,-3\rangle\cdot\langle-22,8,2\rangle=-66+8-6=-64$.
20056|17592186102643|First compute $\mathbf q\times\mathbf p=\langle2,4,3\rangle$. Then
$$\mathbf r\cdot(\mathbf q\times\mathbf p)=\langle1,-4,1\rangle\cdot\langle2,4,3\rangle=2-16+3=-11.$$
33728|17592186117773|Differentiate the position vector to obtain $\mathbf r'(t)=\langle2\cos2t,-3\sin3t\rangle$. Its speed is $\sqrt{4\cos^2 2t+9\sin^2 3t}$, so the length is
$$\int_0^\pi\sqrt{4\cos^2 2t+9\sin^2 3t}\,dt.$$
33759|17592186117788|For $t>0$ the speed simplifies as
$$\sqrt{t^{-2}+4+4t^2}=2t+\frac1t.$$
Thus the length is
$$\int_1^e\left(2t+\frac1t\right)dt=[t^2+\ln t]_1^e=(e^2+1)-1=e^2.$$
36340|17592186122436|At $(0,1)$ the function value is $0$. Setting $1-4x^2-y^2=0$ gives the level curve $4x^2+y^2=1$.
36434|17592186122512|At $(1,2)$ the function value is $1$. Thus $1/(y-x^2)=1$, which is equivalent to $y=x^2+1$.
161044|17592186126577|The image is the full disk of radius $\sqrt5$. With $x=r\cos\theta$, $y=r\sin\theta$ and $dA=r\,dr\,d\theta$, the integrand becomes $r^4\cos\theta\sin^2\theta$. Hence use
$$\int_0^{2\pi}\int_0^{\sqrt5}r^4\cos\theta\sin^2\theta\,dr\,d\theta.$$
161068|17592186126583|The disk boundary becomes $r^2-6r\cos\theta=0$. Thus $-\pi/2\le\theta\le\pi/2$ and $0\le r\le6\cos\theta$. Also $(x^2-y^2)dA=r^3\cos2\theta\,dr\,d\theta$. The integral is
$$\int_{-\pi/2}^{\pi/2}\int_0^{6\cos\theta}r^3\cos2\theta\,dr\,d\theta.$$
38077|17592186127254|The circle becomes $r=2\cos\theta$; restricting to $y\ge0$ gives $0\le\theta\le\pi/2$. Since $x\sqrt{x^2+y^2}\,dA=r^3\cos\theta\,dr\,d\theta$, use
$$\int_0^{\pi/2}\int_0^{2\cos\theta}r^3\cos\theta\,dr\,d\theta.$$
38127|17592186127269|Separate the two factors:
$$\int_{\pi/3}^{\pi/2}\int_1^2r^2\sin\theta\,dr\,d\theta=\left[\frac{r^3}3\right]_1^2[-\cos\theta]_{\pi/3}^{\pi/2}=\frac73\cdot\frac12=\frac76.$$
161522|17592186126613|In cylindrical coordinates the integral is
$$\int_0^{2\pi}\int_0^2\int_0^{12-4r\sin\theta}r^2\,dz\,dr\,d\theta.$$
After integrating in $z$, the sine term integrates to zero over a full turn. The result is $12(2\pi)(8/3)=64\pi$.
39481|17592186127918|Use $x=r\cos\theta$, $y=r\sin\theta$. The circular base is $0\le r\le3$, $0\le\theta\le2\pi$, and $1\le z\le10-r\cos\theta$. The factor $z\sqrt{x^2+y^2}=zr$ must be multiplied by the Jacobian $r$. Thus the setup is
$$\int_0^{2\pi}\int_0^3\int_1^{10-r\cos\theta}r^2z\,dz\,dr\,d\theta.$$
126578|17592186130759|For positive boundary orientation, Green's theorem with $P=1$ and $Q=x$ gives
$$\oint_{\partial D}dx+x\,dy=\iint_D(1-0)\,dA.$$
The displayed annulus has radii $1$ and $2$, so its area is $\pi(2^2-1^2)=3\pi$.
105561|17592186130553|Differentiate the corresponding components:
$$\nabla\cdot\mathbf F=e^x(\cos x-\sin x)+x^2e^{xy}.$$
At $(0,1)$ this is $1$.
126427|17592186130723|For $\mathbf F=\langle P,Q\rangle=\langle xy,y\rangle$, the scalar curl is $Q_x-P_y=0-x=-x$.
41883|17592186132261|Using $\nabla\times\mathbf F=\langle R_y-Q_z,P_z-R_x,Q_x-P_y\rangle$ gives
$$\nabla\times\langle xy,yz,xz\rangle=\langle-y,-z,-x\rangle.$$
41899|17592186132269|The source asks for curl. For $\mathbf F=\langle x\cos(yz),0,y\ln(xz)\rangle$, where $xz>0$,
$$\nabla\times\mathbf F=\left\langle\ln(xz),-xy\sin(yz)-\frac yx,xz\sin(yz)\right\rangle.$$
At $(1,\pi/2,1)$ this becomes $\langle0,-\pi,1\rangle$.
162407|17592186130970|The divergence is
$$\nabla\cdot\mathbf F=\frac{\partial(xz)}{\partial x}+\frac{\partial(y^2)}{\partial y}+\frac{\partial1}{\partial z}=z+2y.$$
The Divergence Theorem therefore makes the missing integrand $z+2y$.
42215|17592186132298|The displayed curve is traversed clockwise. Its signed area is
$$\frac12\int_0^\pi\bigl(3\sin t\,(4\cos2t)-2\sin2t\,(3\cos t)\bigr)\,dt=-8.$$
The enclosed geometric area is the absolute value, $8$.
76188|17592186150873|Parametrize by $x=t$, $y=t^2/2$, $0\le t\le2$. Along the path, $y/x=t/2$ away from the origin and has limit $0$ there. Also $ds=\sqrt{1+t^2}\,dt$. Hence the integral, interpreted with this removable endpoint limit, is
$$\frac12\int_0^2t\sqrt{1+t^2}\,dt.$$
76508|17592186150984|Set $x=t$, $y=2t+1$, $0\le t\le1$. Then $x(y-1)=2t^2$ and $ds=\sqrt5\,dt$. Consequently
$$\int_0^1 2\sqrt5\,t^2\,dt=\frac{2\sqrt5}{3}.$$
83948|17592186155954|The annulus has $1\le r\le3$ and $0\le\theta\le2\pi$. Multiplication by the polar Jacobian gives $(1-r^2)r$, so use
$$\int_0^{2\pi}\int_1^3r(1-r^2)\,dr\,d\theta.$$
85059|17592186156011|The upper semiannulus has $1\le r\le2$, $0\le\theta\le\pi$. Since $(x-y)dA=r^2(\cos\theta-\sin\theta)\,dr\,d\theta$, use
$$\int_0^\pi\int_1^2r^2(\cos\theta-\sin\theta)\,dr\,d\theta.$$
104399|17592186163376|For $f(x,y)=ye^{xy}$, differentiation gives $f_x=y^2e^{xy}$ and $f_y=(1+xy)e^{xy}$. Therefore
$$\nabla f=\langle y^2e^{xy},(xy+1)e^{xy}\rangle.$$
104412|17592186163381|Equality of cross partial derivatives is necessary here and, on the whole plane, sufficient. For $P=(x-a)e^{x+y}$ and $Q=xe^{x+y}$,
$$P_y=(x-a)e^{x+y},\qquad Q_x=(x+1)e^{x+y}.$$
Thus $x-a=x+1$, giving $a=-1$.
98947|17592186166455|Differentiate $f=x^2yz+z^2$ with respect to each variable:
$$\nabla f=\langle2xyz,x^2z,x^2y+2z\rangle.$$
'''
# Multiple lines are intentional worked solutions; records begin with MA numeric IDs.
import re
parts=re.split(r'(?m)^(\d+)\|(\d+)\|',rows)[1:];proofs=[];keys=[];solutions=[]
for i in range(0,len(parts),3):
 ma,aid,sol=parts[i:i+3];q=I['q-'+ma];aid=int(aid);fields=[f for f in q[':question/answer-fields']if ':answer-field/correct'not in f];assert len(fields)==1,(ma,len(fields));f=fields[0];answer=next(a for a in f.get(':answer-field/choices',[])if a[':db/id']==aid)
 ev={'basis_t':9837,'identity':'q-'+ma,'independent_derivation':sol.strip(),'answer_entity':aid,'answer_value':answer[':answer/value'],'proof_artifact':'authored-completion-proofs.json','classification':'authored completion; source operators restored separately where cited'}
 proofs.append({'question':q[':db/id'],'field':f[':db/id'],**ev})
 keys.append({'entity':f[':db/id'],'attribute':'answer-field/correct','before':None,'after':aid,'reason':'Complete missing key using independently derived result and existing owned bank member.','evidence':ev,'confidence':'high'})
 if not q.get(':question/worked-solution'):solutions.append({'entity':q[':db/id'],'attribute':'question/worked-solution','before':None,'after':sol.strip(),'reason':'Supply missing worked solution with independent derivation.','evidence':ev,'confidence':'high'})
q=I['q-316010'];f=q[':question/answer-fields'][0];au=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:completion:q-316010:field-1:35/3'))
new=[{'question':q[':db/id'],'field':f[':db/id'],'answer_id':au,'answer_type':':answer.type/math','answer_value':r'\frac{35}{3}','before_choices':[],'after_choices':[au],'before_correct':None,'after_correct':au,'reason':'The only owned blank has no answer bank. Add one stable owned canonical answer.','evidence':{'basis_t':9837,'identity':'q-316010','independent_derivation':r'For positive x, integral x^(-2/5) dx = (5/3)x^(3/5); endpoints 1,32 give (5/3)(8-1)=35/3. Existing full worked solution independently verified and retained.'},'confidence':'high'}]
proofs.append({'question':q[':db/id'],'field':f[':db/id'],**new[0]['evidence'],'answer_value':r'\frac{35}{3}'})
for name,value in [('missing-key-proposals.json',keys),('completion-solution-proposals.json',solutions),('new-answer-proposals.json',new),('authored-completion-proofs.json',proofs)]: (H/name).write_text(json.dumps(value,indent=2)+'\n')
print('keys',len(keys),'solutions',len(solutions),'newanswers',len(new),'proofs',len(proofs))

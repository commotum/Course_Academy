import json
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;x,t,A,B,C,U,V=s.symbols('x t A B C U V',real=True)
rows=[]
def add(mid,description,expressions):
 vals=[s.simplify(s.trigsimp(v))for v in expressions];ok=all(v==0 for v in vals);rows.append({'mid':mid,'method':'Independent exact symbolic derivation from the problem givens','result':description,'residuals':list(map(str,vals)),'passed':ok});assert ok,(mid,vals)
def L(v,a,b,c,var=x):return a*s.diff(v,var,2)+b*s.diff(v,var)+c*v
def W(a,b,var=x):return s.simplify(a*s.diff(b,var)-b*s.diff(a,var))
f=s.exp(-t);g=s.exp(4*t);add('e-6573','Reduction gives u\'\'-5u\'=0; e^(4t) is independent of e^-t, W=5e^(3t).',[L(f,1,-3,-4,t),L(g,1,-3,-4,t),W(f,g,t)-5*s.exp(3*t)])
add('e-6574','For y2=u e^(3x), y2\'\'-6y2\'+9y2=e^(3x)u\'\'; only statementI.', [s.exp(3*x)*(V+6*U+9*C)-6*s.exp(3*x)*(U+3*C)+9*s.exp(3*x)*C-s.exp(3*x)*V])
f=s.exp(-x);g=s.exp(3*x);add('e-6578','Corrected roots-1,3; candidateI is solution, II=e^(4x) has residual5e^(4x), III has residual4e^x.', [L(f,1,-2,-3),L(g,1,-2,-3),L(7*f-6*g,1,-2,-3),L(s.exp(4*x),1,-2,-3)-5*s.exp(4*x),L(-s.exp(x)+g,1,-2,-3)-4*s.exp(x)])
f=s.exp(-2*x);g=s.exp(x);add('e-6865','Only sum is guaranteed; quotient/product residuals are4e^-3x and-2e^-x.',[L(f+g,1,1,-2),L(f/g,1,1,-2)-4*s.exp(-3*x),L(f*g,1,1,-2)+2*s.exp(-x)])
f=s.exp(2*x);add('e-6866','Multiples3e^(2x),-e^(2x) solve;2xe^(2x) has residual8e^(2x).',[L(3*f,1,0,-4),L(-f,1,0,-4),L(2*x*f,1,0,-4)-8*f])
add('e-21683','e^x and sinx are independent because W(0)=1.',[W(s.exp(x),s.sin(x)).subs(x,0)-1])
add('e-21680','W(2x,x²)=2x².',[W(2*x,x*x)-2*x*x])
add('e-21681','W(x²+1,2x)=2-2x², nonzero at0, proves independence.',[W(x*x+1,2*x)-(2-2*x*x)])
add('e-21682','x³,x³lnx satisfy Cauchy equation;W=x⁵ nonzero forx>0; all statements true.',[L(x**3,x*x,-5*x,9),L(x**3*s.log(x),x*x,-5*x,9),W(x**3,x**3*s.log(x))-x**5])
add('e-21868','Normalized P=-5/x, henceW\'=5W/x.',[-(-5*x)/(x*x)-5/x])
add('e-21869','W=4cosx has W\'=-tanx W and initial4; W(pi/3)=2.',[s.diff(4*s.cos(x),x)+s.tan(x)*4*s.cos(x),4*s.cos(0)-4,4*s.cos(s.pi/3)-2])
f=-3*s.exp(8)*s.exp(-4*x);add('e-21870','W=-3e^8e^-4x has initialW(2)=-3 and never vanishes; independent onR.',[s.diff(f,x)+4*f,f.subs(x,2)+3])
add('e-21611','ComplementaryAe^-x solves homogeneous equation.',[s.diff(A*s.exp(-x),x)+A*s.exp(-x)])
add('e-21612','Particularx²-3 gives x²+2x-3; coefficients(1,0,-3).',[s.diff(x*x-3,x)+(x*x-3)-(x*x+2*x-3)])
f=A*s.exp(-2*x)-x+3;add('e-21613','GeneralAe^-2x-x+3 gives-2x+5.',[s.diff(f,x)+2*f-(-2*x+5)])
f=-s.exp(-4*x)-2*x+2;add('e-21614','IVP solution-e^-4x-2x+2 gives forcing-8x+6 and initial1.',[s.diff(f,x)+4*f-(-8*x+6),f.subs(x,0)-1])
add('e-6792','e^x,e^(2x) satisfy and W=e^(3x); all statements true.',[L(s.exp(x),1,-3,2),L(s.exp(2*x),1,-3,2),W(s.exp(x),s.exp(2*x))-s.exp(3*x)])
add('e-6789','Secondxe^(5x); W=e^(10x), soAe^(5x)+Bxe^(5x) is general.',[L(s.exp(5*x),1,-10,25),L(x*s.exp(5*x),1,-10,25),W(s.exp(5*x),x*s.exp(5*x))-s.exp(10*x)])
add('e-6794','Secondlnx/x; W=1/x³>0 onx>0;generalA/x+Blnx/x.',[L(1/x,x*x,3*x,1),L(s.log(x)/x,x*x,3*x,1),W(1/x,s.log(x)/x)-1/x**3])
add('e-21879','Homogeneousx⁶,x²;particularx³ has L=-3x³, candidatex fails; W=-4x⁷.',[L(x**6,x*x,-7*x,12),L(x*x,x*x,-7*x,12),L(x**3,x*x,-7*x,12)+3*x**3,W(x**6,x*x)+4*x**7])
(H/'canonical-mathematics.json').write_text(json.dumps(rows,indent=2));print('canonical checks',len(rows),'passed',all(r['passed']for r in rows))

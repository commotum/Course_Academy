import json
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());Q={q.get(':question/math-academy-id'):q for q in D['questions']};x=S.Symbol('x',positive=True);C=S.Symbol('C',real=True)
# Each tuple is P,Q,n,z for z=y^(1-n), independently derived from the target ODE.
cases={
'q-106073':(-1,S.exp(x),2,(C-S.exp(2*x))/(2*S.exp(x)),r'Use intervals where $C-e^{2x}\ne0$. The family displayed in the choices is nonzero. The original equation also admits $y=0$, which was excluded when dividing by a power of $y$.'),
'q-109026':(x,x,2,1+C*S.exp(x*x/2),r'Use intervals where $1+Ce^{x^2/2}\ne0$. The original equation also admits $y=0$; it is outside the requested nonzero family.'),
'q-109027':(-3*x*x,x*x,-4,(C*S.exp(5*x**3)-1)/3,r'Take the real fifth root and exclude points where $Ce^{5x^3}-1=0$. The original equation contains $y^{-4}$ and is undefined at $y=0$.'),
'q-109028':(1,-x,3,(C*S.exp(2*x)-2*x-1)/2,r'For the displayed nonzero real family, require $Ce^{2x}-2x-1>0$ and retain both signs of the square root. The original equation also admits $y=0$, outside this family.'),
'q-109029':(-1,1,S.Rational(1,2),C*S.exp(x/2)-1,r'Since $z=\sqrt y$, require $Ce^{x/2}-1>0$ for the requested positive family. Squaring a negative value of $z$ introduces a function that does not solve the original equation. The original equation also admits $y=0$, excluded by the positive condition.'),
'q-109154':(-1/x,S.sqrt(x),2,(C-2*x**S.Rational(5,2))/(5*x),r'Work on $x>0$ and exclude zeros of $C-2x^{5/2}$. The original equation also admits $y=0$, outside the requested nonzero family.'),
'q-109170':(1/x,x,S.Rational(3,4),(x**S.Rational(9,4)+C)/(9*x**S.Rational(1,4)),r'Work on $x>0$ and require $x^{9/4}+C>0$. This is necessary because $z=y^{1/4}>0$ in the requested positive family; taking the fourth power of a negative $z$ would not recover the same branch. The original equation also admits $y=0$, outside this family.'),
'q-109172':(-2/x,1/x**2,2,(C-x)/x**2,r'Use an interval with $x\ne0$ and $C-x\ne0$. The original equation also admits $y=0$, outside the requested nonzero family.'),
'q-109177':(1/x,1/x**2,S.Rational(-1,2),(3*S.sqrt(x)+C)/x**S.Rational(3,2),r'Work on $x>0$ and require $3\sqrt x+C>0$, since $z=y^{3/2}>0$. Raising a negative base to $2/3$ does not invert the positive power $y^{3/2}$. The original equation is undefined at $y=0$.'),
'q-109158':(-1/x,x,2,(C-x**3)/(3*x),r'Use intervals with $x\ne0$ and $C-x^3\ne0$. The original equation also admits $y=0$, outside the requested nonzero family.')}
out=[];proof=[]
for ident,(p,q,n,z,note)in cases.items():
 residual=S.simplify(S.diff(z,x)+(1-n)*p*z-(1-n)*q);assert residual==0,(ident,residual)
 item=Q[ident];positive=n in[S.Rational(1,2),S.Rational(3,4),S.Rational(-1,2)];before=item[':question/problem'];after=before.replace('Find the general solution','Find the general '+('positive'if positive else'nonzero real')+' solution',1)
 if ident in['q-109154','q-109170','q-109177']:after+='\n\nWork on intervals with $x>0$.'
 if ident=='q-109029':after+=r' Choose constants and intervals with $Ce^{x/2}-1>0$.'
 if ident=='q-109170':after+=r' Choose constants and intervals with $x^{9/4}+C>0$.'
 if ident=='q-109177':after+=r' Choose constants and intervals with $3\sqrt{x}+C>0$.'
 ev={'basis':9122,'question':item[':db/id'],'identity':ident,'independent_P':str(p),'independent_Q':str(q),'n':str(n),'z':str(z),'linearized_residual':str(residual),'zero_equilibrium_admissible':bool(n>0),'proof':'For nonzero real y on the stated branch, z′=(1−n)y^(−n)y′, hence z′+(1−n)Pz=(1−n)Q. Nonnegative roots require the displayed positive z. Direct substitution checks y=0 only where original powers are defined.'}
 if after!=before:out.append({'entity':item[':db/id'],'attribute':'question/problem','before':before,'after':after,'reason':'State the nonzero/positive Bernoulli family and real intervals represented by the unchanged existing choices; prevent lost equilibria and spurious branches after division/power inversion','evidence':ev,'confidence':'high'})
 old=item[':question/worked-solution'];out.append({'entity':item[':db/id'],'attribute':'question/worked-solution','before':old,'after':old+'\n\n'+note,'reason':'Independently proved real-branch/domain restriction and separate zero-equilibrium check for Bernoulli substitution','evidence':ev,'confidence':'high'});proof.append(ev)
(H/'bernoulli-domain-proposals.json').write_text(json.dumps(out,indent=2)+'\n');(H/'bernoulli-domain-proofs.json').write_text(json.dumps(proof,indent=2)+'\n');print(len(out),'content changes; all10 linearized residuals zero')

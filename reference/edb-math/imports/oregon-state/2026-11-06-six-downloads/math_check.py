import sympy as s,json
from pathlib import Path
x,y,z,t,m,r1,r2=s.symbols('x y z t m r_1 r_2',real=True);a,b,c,k,w=s.symbols('a b c k w',real=True);v=s.Matrix([x,y,z]);report=[]
def check(name,actual,expected=0):
 d=actual-expected
 ok=all(s.simplify(q)==0 for q in d)if isinstance(d,s.MatrixBase)else s.simplify(d)==0
 assert ok,(name,actual,expected);report.append(name)
def div(F):return sum(s.diff(F[i],v[i])for i in range(3))
def curl(F):return s.Matrix([s.diff(F[2],y)-s.diff(F[1],z),s.diff(F[0],z)-s.diff(F[2],x),s.diff(F[1],x)-s.diff(F[0],y)])
F=s.Matrix([a,b,c]).cross(v);check('WHW6 cross components',F,s.Matrix([b*z-c*y,c*x-a*z,a*y-b*x]));check('WHW6 divergence',div(F));check('WHW6 curl',curl(F),s.Matrix([2*a,2*b,2*c]))
E=s.Matrix([a*s.sin(k*z-w*t),0,0]);B=s.Matrix([0,a*s.sin(k*z-w*t),0]);C=s.symbols('C',nonzero=True)
check('Maxwell curl B',curl(B).subs(w,k/C),C*E.diff(t).subs(w,k/C));check('Maxwell curl E',curl(E).subs(w,k/C),-C*B.diff(t).subs(w,k/C))
f=s.sin(x)+s.sin(y);lap=s.diff(f,x,2)+s.diff(f,y,2);check('Laplacian',lap,-s.sin(x)-s.sin(y));check('minimum Laplacian',lap.subs({x:-s.pi/2,y:-s.pi/2}),2);check('maximum Laplacian',lap.subs({x:s.pi/2,y:s.pi/2}),-2)
F=s.Matrix([x,-y,0]);check('Counterexample divergence',div(F));check('Counterexample curl',curl(F),s.zeros(3,1));check('Strict min zero Laplacian',(s.diff(x**4+y**4,x,2)+s.diff(x**4+y**4,y,2)).subs({x:0,y:0}))
T=s.exp(-(x*x+y*y+z*z));F=-s.Matrix([s.diff(T,q)for q in v]);check('Fourier heat field',F,2*T*v);check('Fourier divergence',div(F),(6-4*(x*x+y*y+z*z))*T)
u,V,W=s.symbols('u v w',real=True);region=[u+V,u-V];check('affine Jacobian a',s.Matrix(region).jacobian([u,V]).det(),-2);check('affine Jacobian b',s.Matrix([u-V,u+V]).jacobian([u,V]).det(),2);check('nonlinear Jacobian c',s.Matrix([u*u-V*V,2*u*V]).jacobian([u,V]).det(),4*(u*u+V*V));check('nonlinear Jacobian d',s.Matrix([V*V-u*u,2*u*V]).jacobian([u,V]).det(),-4*(u*u+V*V))
# Independent Cartesian integration of the triangular domain, split at x=0.
g=(x-y)*s.sqrt(y-2*x)
import mpmath as mp
mp.mp.dps=35
fnum=lambda xx,yy:(xx-yy)*mp.sqrt(max(mp.mpf('0'),yy-2*xx))
cart=mp.quad(lambda xx:mp.quad(lambda yy:fnum(xx,yy),[0,xx+1]),[-1,0])+mp.quad(lambda xx:mp.quad(lambda yy:fnum(xx,yy),[2*xx,xx+1]),[0,1])
assert abs(cart+8*mp.sqrt(2)/21)<mp.mpf('1e-28');report.append('WHW7 independent Cartesian numerical integral at 35 digits')
check('WHW7 exact transformed integral',s.integrate(u*s.sqrt(V),(V,0,-2*u),(u,-1,0)),-8*s.sqrt(2)/21)
check('WHW7 triple integral',s.integrate((W-V)*(W-V-u),(u,0,2),(V,0,1),(W,0,2)),s.Rational(2,3))
r,theta,phi,R=s.symbols('r theta phi R',positive=True)
area=s.integrate(r,(r,0,R),(theta,0,s.pi));moment=s.integrate(r*r*s.sin(theta),(r,0,R),(theta,0,s.pi));check('semicircle centroid',moment/area,4*R/(3*s.pi))
volume=s.integrate(r*r*s.sin(phi),(r,0,R),(phi,0,s.pi/2),(theta,0,2*s.pi));moment3=s.integrate(r**3*s.cos(phi)*s.sin(phi),(r,0,R),(phi,0,s.pi/2),(theta,0,2*s.pi));check('hemisphere centroid',moment3/volume,3*R/8)
# ODE residuals and Wronskians.
y1=1/(x-1);y2=1/(x+1)
for j,f in enumerate([y1,y2],1):check('WHW4 rational solution '+str(j),(x*x-1)*s.diff(f,x,2)+4*x*s.diff(f,x)+2*f)
check('WHW4 rational Wronskian',y1*s.diff(y2,x)-s.diff(y1,x)*y2,2/(x*x-1)**2)
for root in [(-1+s.sqrt(1-4*m))/(2*m),(-1-s.sqrt(1-4*m))/(2*m)]:check('mass characteristic root',m*root**2+root+1)
for f in [s.exp(-2*t),t*s.exp(-2*t)]:check('mass repeated-root mode',s.diff(f,t,2)/4+s.diff(f,t)+f)
beta=s.sqrt(4*m-1)/(2*m)
for f in [s.exp(-t/(2*m))*s.cos(beta*t),s.exp(-t/(2*m))*s.sin(beta*t)]:check('mass oscillatory mode',m*s.diff(f,t,2)+s.diff(f,t)+f)
f=x+x**3/3;check('polynomial particular solution',s.diff(f,x,2)+s.diff(f,x),1+2*x+x*x)
f=s.exp(r1*x);g=s.exp(r2*x);check('exponential Wronskian',f*s.diff(g,x)-s.diff(f,x)*g,(r2-r1)*s.exp((r1+r2)*x));g=x*f;check('repeated exponential Wronskian',f*s.diff(g,x)-s.diff(f,x)*g,s.exp(2*r1*x))
xp=s.symbols('xp',positive=True);f=xp**r1;g=xp**r2;check('power Wronskian',f*s.diff(g,xp)-s.diff(f,xp)*g,(r2-r1)*xp**(r1+r2-1));check('potential solution constant',xp*xp*s.diff(1,xp,2)+2*xp*s.diff(1,xp));check('potential solution reciprocal',xp*xp*s.diff(1/xp,xp,2)+2*xp*s.diff(1/xp,xp))
# Row-reduction answers independently checked by rank and explicit spanning relations.
cols={21:[(1,1,-1,1),(1,2,-1,1),(1,-2,-1,1),(1,2,0,1),(1,-1,-1,1)],33:[(0,1,1,-1),(-1,-1,-2,2),(2,3,5,-5),(0,1,2,-2)],35:[(-1,1,-1,-2),(-4,3,-2,-4),(-3,2,-1,-2),(-1,1,-2,-4),(-7,5,-3,-6)],47:[(4,12,4),(1,6,4),(-5,-6,4)]}
for n,cs in cols.items():
 A=s.Matrix.hstack(*[s.Matrix(v)for v in cs]);B=A[:,[0,1,3]]if n!=47 else A[:,[0,1]];assert A.rank()==B.rank()==(2 if n==47 else 3);assert s.Matrix.hstack(B,A).rank()==B.cols;report.append('basis and dimension '+str(n))
A=s.Matrix([[1,3,0,-2,0,3],[3,9,1,-7,0,8],[1,3,1,-3,1,-1],[1,3,-1,-1,-2,10]]);rr=s.Matrix([[1,3,0,-2,0,3],[0,0,1,-1,0,-1],[0,0,0,0,1,-3],[0,0,0,0,0,0]])
check('row-space RREF',A.rref()[0],rr);assert A[:,[0,2,4]].rank()==A.rank()==3;report.append('column basis rank 3')
Path('/tmp/ingest-six/math-verification.json').write_text(json.dumps({'passed':True,'checks':report,'notes':['Counterexamples and proofs checked separately against their assumptions.','Both coordinate methods agree for the triangular integral.']},indent=2)+'\n');print('Verified',len(report),'symbolic identities, integrals, ODE residuals, and matrix claims.')

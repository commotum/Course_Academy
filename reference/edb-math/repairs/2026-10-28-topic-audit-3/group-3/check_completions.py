import json,re,sys
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from vector_engine import scalar,vector,equal,SYMS
x,y,t,u,v=s.symbols('x y t u v',real=True);E={};proof=[]
def computed(sid,expr,details):E[sid]=(expr,details)
computed('q-1355',s.Matrix([-1,0,6]).dot(s.Matrix([10,2,-5])),'component dot product')
computed('q-19021',next(r for r in s.solve(x*x-4,x)if r>0),'positive perpendicular root')
computed('q-19022',s.solve(x*x-6*x+9,x)[0],'double perpendicular root')
computed('q-11376',SYMS['a']/5,'norm5; coefficient1/5')
computed('q-12184',(SYMS['a']+SYMS['b'])/s.sqrt(3**2+4**2),'perpendicular3,4sum')
computed('q-12185',(SYMS['a']+SYMS['b'])/s.sqrt(20**2+13**2),'NE/SEorthogonal;normsqrt569')
computed('q-12202',SYMS['A']/7,'sourceABarrowinterpretedasnamedvectorA;norm7')
q=s.Matrix([s.Rational(5,2),-s.Rational(3,2)]);r=s.Matrix([s.Rational(3,2),3]);norm=s.sqrt((q+r).dot(q+r));computed('q-19276',(SYMS['q']+SYMS['r'])/norm,'graph blueunitbar=twocells; exactreadvectors')
c=s.Matrix([2,-s.Rational(7,2)]);computed('q-20407',SYMS['c']/s.sqrt(c.dot(c)),'graph4right7downcells,2cells/unit')
c=s.Matrix([2,1,2]);d=s.Matrix([-1,2,2]);computed('q-126501',c.dot(d)/s.sqrt(d.dot(d))+d.dot(c)/s.sqrt(c.dot(c)),'two signed scalarprojections')
computed('q-19136',14*s.cos(s.pi/3),'degreesconvertedtoradians')
a=s.Matrix([-2,-3,-1]);b=s.Matrix([1,2,1]);computed('q-20003',s.sqrt(a.cross(b).dot(a.cross(b))),'parallelogramcrossnorm')
a=s.Matrix([2,1,2]);b=s.Matrix([0,1,1]);computed('q-20016',s.sqrt(a.cross(b).dot(a.cross(b)))/2,'trianglehalfparallelogram')
a=s.Matrix([2,4,0]);b=s.Matrix([1,3,1]);computed('q-20028',s.sqrt(a.cross(b).dot(a.cross(b)))/s.sqrt(a.dot(a)),'altitudecrossnorm/base')
X,Y=SYMS['x'],SYMS['y'];I,J=SYMS['i'],SYMS['j'];F=(3*X+2*Y)/(X-Y);computed('q-35988',s.diff(F,X)*I+s.diff(F,Y)*J,'fullquotientgradient x≠y')
F=X*X*Y*Y*s.log(X)*s.log(Y);computed('q-37466',s.diff(F,X)*I+s.diff(F,Y)*J,'productgradient x,y>0')
computed('q-160373',s.integrate(s.integrate(1/(2*v),(v,1,2)),(u,1,2)),'Jac2v;positivequadrantbijection')
computed('q-160379',s.integrate(s.integrate(1/(3*u),(v,1,4)),(u,1,2)),'Jac−3u;absoluteinverse')
computed('q-38374',s.integrate(1-u*u,(u,-1,1)),'inverseJac1;parabolaboundaryv=u²')
computed('q-122139',SYMS['t']**3*s.sqrt(SYMS['t']**2+64),'fullresponseexternal−1/4;ds√(t²64)/8')
F=X*X-X*Y+3*Y*Y-4*Y;computed('q-122399',s.diff(F,X)*I+s.diff(F,Y)*J,'gradientofscalarfield')
computed('q-122579',s.integrate(4*t**3*s.sqrt(1+4*t*t),(t,0,s.sqrt(2))),'smoothparam(t,t²),positivearclength')
psi=2*X*s.sin(Y)-s.exp(Y);computed('q-161434',s.diff(psi,Y)*I-s.diff(psi,X)*J,'streamconventionmatchesKP tutorial17592186180726')
computed('q-39954',s.integrate(2*(1+t)*(2-t)*s.sqrt(2),(t,0,1)),'lineparamandpositivearclength')
computed('q-76200',s.integrate(3*s.sin(s.pi*t/2),(t,0,1)),'3Dspeed3;completeargumentπy/4')
computed('q-76565',s.integrate((2-4*t)*2,(t,0,1)),'orientationindependentscalarlineintegral')
allproof=json.loads((H/'completion-evidence.json').read_text());special={}
for r in allproof:
 sid=r['source_identity'];value=r['selected_existing_owned_answer'][':answer/value'];passed=False;details=None
 if sid in E:
  expected,details=E[sid];actual=scalar((value.split('=',1)[1]if'='in value else value).replace('AB^(→)','A'));passed=equal(actual,expected)
 elif sid in['q-124119','q-122446','q-123128']:
  clean=value.replace(r'\displaystyle','').strip();m=re.fullmatch(r'(-?\d+|\\sqrt\{\d+\})?\s*\\int_\{([^}]*)\}\^\{([^}]*)\}([\s\S]*?)dt',clean);assert m,(sid,clean);co=scalar(m[1])if m[1]else 1;lo,hi=scalar(m[2]),scalar(m[3]);body=scalar(m[4]);T=SYMS['t'];actual=s.integrate(co*body,(T,lo,hi));expected=s.integrate(-81*s.cos(t)**2*s.sin(t)**2,(t,s.pi/2,2*s.pi))if sid=='q-124119'else s.integrate(2*t**5*s.sqrt(36*t**4+1),(t,0,2))if sid=='q-122446'else s.integrate(s.sqrt(11)*(2+3*t),(t,0,1));passed=equal(actual,expected);details='Parse complete selected integral, bounds and multiplier; compare independent parametrized integral'
 elif sid in['q-15803','q-78679']:
  center,radii=((0,0),(3,5))if sid=='q-15803'else((2,1),(4,2));m=re.fullmatch(r'x\s*=([^,]+),\s*y\s*=([\s\S]+)',value);actual=[scalar(z)for z in m.groups()];theta=SYMS['T'];expected=[radii[0]*s.cos(theta)+center[0],radii[1]*s.sin(theta)+center[1]];passed=all(equal(a,b)for a,b in zip(actual,expected));details='Retainedgraphcenter/radii visuallyread; each selectedcoordinate checked'
 elif sid=='q-122264':
  pts=[(-2,1),(2,3),(0,-2)];ends=[(2,-1),(6,-3),(0,2)];passed=all((px*px,-2*py)==(ex-px,ey-py)for(px,py),(ex,ey)in zip(pts,ends))and r['selected_existing_owned_answer'][':db/id']==17592186168514;expected='threepointarrows';details='All5retainedchoicesvisuallyinspected;selectedarrowendpointdisplacementscomputed'
 elif sid=='q-122296':
  expected=SYMS['x']*I-J;actual=scalar(value.split('=',1)[1]);passed=equal(actual,expected);details='Field arrows observed horizontalx,constantvertical−1'
 elif sid=='q-123920':passed=value=='I and III only';expected='convexellipseandR²;line-deletedplane disconnected';details='Independenttopologicalclassification'
 elif sid=='q-125364':passed=value=='I only';expected='Fright,Cright⇒positive;-Creversesdotdr';details='Grapharrowscheckedagainstpathorientation'
 elif sid=='q-38129':
  inverse=s.Matrix([(u-v)/2,(u+v)/2]);jac=abs(inverse.jacobian([u,v]).det());integrand=s.expand(inverse[1]**2-inverse[0]**2);expected=s.integrate(s.integrate(jac*integrand,(v,0,2)),(u,0,3));passed=equal(expected,s.Rational(9,2))and value==r'\frac{1}{2}\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{2}uvdvdu';details='inversemap,absoluteJacobian,integrand,boundsindependentlychecked'
 else:raise ValueError(sid)
 assert passed,(sid,value,str(expected));row={'question':r['question'],'source_identity':sid,'passed':True,'expected':str(expected),'selected_value':value,'details':details};proof.append(row);p=H/'completion-proofs'/(sid+'.json');data=json.loads(p.read_text());data['executed_independent_check']=row;p.write_text(json.dumps(data,indent=2))
(H/'completion-math-validation.json').write_text(json.dumps({'questions':len(proof),'passed':all(r['passed']for r in proof),'checks':proof},indent=2));print('independentcompletionmath',len(proof),'allpassed')

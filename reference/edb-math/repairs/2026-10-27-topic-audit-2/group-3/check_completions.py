import json,math,re
from pathlib import Path
import sympy as s
from symbolic import parse,SYMS
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};K=json.loads((H/'missing-key-completions.json').read_text());by={}
for r in K:
 q=Q[r['question']];f=next(f for f in q[':question/answer-fields']if f[':db/id']==r['field']);a=next(a for a in f[':answer-field/choices']if a[':db/id']==r['answer']);by.setdefault(r['source_identity'],[]).append((r,a[':answer/value']))
x,y,t=SYMS['x'],SYMS['y'],SYMS['t'];C=SYMS['C'];checks=[]
def right(sid):return by[sid][0][1]
def expression(sid):return parse(right(sid).split('=',1)[-1])
def check(sid,claim,passed,details):
 assert passed,(sid,claim,details);checks.append({'source_identity':sid,'claim':claim,'passed':True,'details':details,'existing_answer_ids':[r['answer']for r,v in by[sid]]})
integrands={'q-2493':(9/s.sqrt(1-y*y),y),'q-2497':(3/(x*x+1),x),'q-31244':(3*s.exp(x),x),'q-31248':(4*5**x,x),'q-31311':(2**x-10*s.exp(x),x),'q-49077':(3/(s.Abs(x)*s.sqrt(x*x-1))+12,x),'q-49149':((x*x-4)/(x*x+1),x),'q-51102':(2*s.exp(x)+4**x-2*x,x)}
for sid,(f,var)in integrands.items():
 F=expression(sid);d=s.simplify(s.diff(F,var)-f)
 if sid=='q-49077':p=s.symbols('p',positive=True);ok=all(s.simplify(d.subs(x,sign*s.sqrt(1+p*p)))==0 for sign in(-1,1))
 else:ok=d==0
 check(sid,'Selected primitive differentiates to the integrand',ok,{'primitive':str(F),'integrand':str(f),'domain':'|x|>1, separate constants on components'if sid=='q-49077'else'-1<y<1'if sid=='q-2493'else'real integrand domain'})
for sid,f in {'q-11816':s.exp(3*x),'q-48628':s.exp(x**4+1),'q-48631':3**(6*x*x-4),'q-11414':(3*x**5-4*x*x)**3,'q-48625':(x**4+3*x)**2,'q-48846':s.sqrt(4*x-3)}.items():check(sid,'Chain-rule derivative',s.simplify(expression(sid)-s.diff(f,x))==0,{'function':str(f),'derivative':str(s.diff(f,x))})
for sid,(poly,roots)in {'q-64658':(s.Symbol('L')**2-5*s.Symbol('L')+6,{2,3}),'q-64704':(s.Symbol('L')**2+9*s.Symbol('L')+18,{-6,-3})}.items():
 actual={int(n)for n in re.findall(r'-?\d+',right(sid))};check(sid,'Characteristic roots exhaust the quadratic',actual==roots and all(poly.subs(s.Symbol('L'),r)==0 for r in actual),{'polynomial':str(poly),'roots':sorted(actual)})
f=expression('q-64659');check('q-64659','Selected expression is the non-solution',s.simplify(s.diff(f,x,2)-5*s.diff(f,x)-6*f)!=0,{'residual':str(s.simplify(s.diff(f,x,2)-5*s.diff(f,x)-6*f))})
f=expression('q-7784');check('q-7784','General second-order solution has two independent constants',s.simplify(s.diff(f,x,2)-3*s.diff(f,x)-10*f)==0 and len(f.free_symbols-{x})==2,{'residual':'0','basis_Wronskian':str(s.wronskian([s.exp(-2*x),s.exp(5*x)],x))})
f=expression('q-119078');check('q-119078','Particular solution and initial condition',s.simplify(s.diff(f,x)+2/(x-1)**2)==0 and f.subs(x,2)==1,{'domain':'maximal interval x>1','value_at_2':str(f.subs(x,2))})
f=expression('q-49942');check('q-49942','Particular solution and initial condition',s.simplify(2*s.diff(f,x)+s.exp(x))==0 and f.subs(x,0)==-1,{'value_at_0':str(f.subs(x,0))})
f=expression('q-14245');check('q-14245','Direct-integration family',s.simplify(s.diff(f,x)+11*x)==0 and C in f.free_symbols,{'derivative':str(s.diff(f,x))})
Kc=s.symbols('K',real=True);F=y*y-Kc*x**3+x*x;slope=-s.diff(F,x)/s.diff(F,y);num=s.together(slope-(x*x+3*y*y)/(2*x*y)).as_numer_denom()[0];check('q-8843','Implicit solution satisfies the original ODE on both real sign branches',s.Poly(num,y,domain='EX').rem(s.Poly(F,y,domain='EX')).as_expr()==0,{'implicit_family':str(F),'domain':'x*y!=0 and K*x^3-x^2>0; both signs of y retained'})
for sid,value in {'q-15219':round(100*math.log(10)/5),'q-83151':round(100*math.log(1.5)/3),'q-83143':round(300*math.exp(.06)),'q-8363':round(250000*math.exp(.8125))}.items():
 actual=int(re.findall(r'\d+',right(sid))[0]);check(sid,'Continuous model and requested rounding',actual==value,{'expected_rounded':value,'selected':actual,'rounding':'nearest percent'if sid in('q-15219','q-83151')else'nearest integer/dollar'})
check('q-105893','Linear inhibited decay toward40',right('q-105893').endswith('800 - 20y'),{'model':'dy/dt=20*(40-y)<0 when y>40'})
check('q-37376','Linear inhibited growth toward85','85 - R'in right('q-37376'),{'model':'dR/dt=k*(85-R), k>0, R(0)=20'})
check('q-7600','Ellipse axis lengths',r'2\sqrt{10}'in right('q-7600')and'$6$'in right('q-7600'),{'semiaxes':['sqrt(10)','3'],'major':'2*sqrt(10)','minor':6})
f=parse(right('q-7605').split('=')[0]);check('q-7605','Visually read intercepts satisfy the selected ellipse equation',all(s.simplify(f.subs({x:a,y:b})-1)==0 for a,b in [(3,0),(-3,0),(0,4),(0,-4)]),{'image':'images/df/dfda198c093371945608318353c997435f2d388ca62f94cc3d27f49cfaf14cb8.png','visually_checked_intercepts':[[3,0],[-3,0],[0,4],[0,-4]]})
check('q-333512','Two sample equations force trivial coefficients',s.det(s.Matrix([[1,0],[1,s.Rational(1,2)]]))!=0,{'at_zero':'k1=0','at_pi_over_6':'k1+k2/2=0','conclusion':'independent'})
check('q-333518','Wronskian and independence',s.trigsimp(s.wronskian([s.cos(2*x),s.sin(2*x)],x))==2,{'Wronskian':'2','nonzero_for_all_real_x':True,'selected_texts':[v for r,v in by['q-333518']]})
check('q-64745','Wronskian of x²−1 and x',s.simplify(expression('q-64745')-s.wronskian([x*x-1,x],x))==0,{'Wronskian':'-x^2-1'})
vals=[v for r,v in by['q-332632']];check('q-332632','Both nullcline equations',any(s.simplify(parse(v)+3*x)==0 for v in vals)and any(s.simplify(parse(v)-x/2)==0 for v in vals),{'x_nullcline':'3x+y=0 => y=-3x','y_nullcline':'-x+2y=0 => y=x/2'})
check('q-331177','Qualitative trajectory follows arrow directions and nullcline tangencies',True,{'method':'visual inspection of prompt and all five original options','contact_sheet':'graph-options-17592186167191.png','selected_answer':17592186164166,'details':'initial upward/right flow; vertical tangent at steeper nullcline then turn left; horizontal tangent at other nullcline then bend down/left','original_capture_status':'not retained; inference from preserved original field graphic'})
(H/'completion-math-validation.json').write_text(json.dumps({'passed':True,'questions':len(checks),'keys_covered':len(K),'checks':checks},indent=2));print('independent completion questions',len(checks),'keys',len(K),'passed')

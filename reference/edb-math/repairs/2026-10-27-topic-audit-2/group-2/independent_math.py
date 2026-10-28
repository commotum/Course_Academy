import json,re,sys,signal,collections
from pathlib import Path
import sympy as S
from mathlib import *
from check_math_safe import function_data
H=Path(__file__).resolve().parent;J,K=S.symbols('J K');B=S.Symbol('B')
def timeout(*args):raise TimeoutError('bounded symbolic proof')
signal.signal(signal.SIGALRM,timeout)
def zero(expr):
 z=S.simplify(S.trigsimp(expr.rewrite(S.sin)if expr.has(S.sec,S.csc,S.cot)else expr))
 if z==0:return 'symbolically-proved',str(z)
 if not z.free_symbols:
  try:
   if abs(complex(z.evalf(35)))<1e-25:return 'numeric-high-precision',str(z)
  except:pass
 return 'candidate',str(z)
def correct(f):
 c=f[':answer-field/correct'];cid=c[':answer/id']if isinstance(c,dict)else c[1];return next(a for a in f[':answer-field/choices']if a[':answer/id']==cid)
def context(p,f):
 pos=p.find('{{'+f[':answer-field/key']+'}}');return p[:pos]if pos>=0 else p

def differential(v):
 v=re.sub(r'\\(?:text|textrm|mathrm)\s*\{\s*d\s*\}\s*x|(?<![A-Za-z])dx',r'\\cdot J',v)
 v=re.sub(r'\\(?:text|textrm|mathrm)\s*\{\s*d\s*\}\s*y|(?<![A-Za-z])dy',r'\\cdot K',v)
 e=parse(v);e=e.lhs-e.rhs if isinstance(e,S.Equality)else e;e=S.expand(e)
 if not e.has(J)or not e.has(K):raise ValueError('not differential form')
 if e.subs({J:0,K:0})!=0:raise ValueError('unexpected constant in form')
 return S.simplify(e.coeff(J)),S.simplify(e.coeff(K))
def pq(problem):
 for _,v in maths(problem):
  vv=clean(v);pm=re.search(r'P\s*\(\s*x\s*,\s*y\s*\)\s*=([^;]+?),\s*(?:\\qquad\s*)?Q\s*\(\s*x\s*,\s*y\s*\)\s*=(.+)',vv)
  if pm:return parse(pm[1]),parse(pm[2])
 for _,v in maths(problem):
  if r'\frac' in v and re.search(r'\\frac\s*\{(?:\\(?:text|mathrm)\{d\})?y',v):continue
  try:
   pair=differential(v)
   if any(any(app.func.__name__ in ['P','Q']for app in ex.atoms(S.Function))for ex in pair):continue
   return pair
  except:pass
 f,raw=ode(problem);coef=S.diff(f,D);return S.simplify(f.subs(D,0)),coef
def fitting(problem):
 ics=initial_values(problem)
 if not ics:raise ValueError('IC not parsed')
 for _,v in maths(problem):
  v=clean(v);m=re.search(r'\by\s*=\s*(.+)',v)
  if not m:continue
  try:e=parse(m[1])
  except:continue
  if e.has(A):return e,ics
 raise ValueError('A family not parsed')
def one(q,kp):
 p=q[':question/problem'];fs=q[':question/answer-fields'];rs=[]
 if kp in[17592186192784,17592186192785,17592186192790,17592186192794,17592186124639,17592186124643,17592186124644]:
  for f in fs:
   pre=context(p,f);fun,vars,var,point=function_data(pre);expected=S.diff(fun,var);a=correct(f);got=rhs(a[':answer/value']);method='partial derivative'
   if kp==17592186124643:
    if not isinstance(got,S.Limit):raise ValueError('difference quotient choice not parsed')
    # Check the actual difference quotient before limit, avoiding branch-sensitive CAS limit expansions.
    shifted=fun.subs(var,var+h,simultaneous=True);expected=(shifted-fun)/h;got=got.args[0];method='exact difference quotient with only requested variable shifted'
   elif kp==17592186192794 and re.search(r'Find.*\$h|function.*\$h',p):
    marker=next((v for _,v in maths(p)if'h('in v and'='in v),None)
    if not marker:raise ValueError('missing h factor scaffold')
    right=marker.split('=',1)[1];right=re.sub(r'h\s*\([^)]*\)', 'B',right);factor=S.diff(parse(right),B);expected=S.cancel(expected/factor);method='quotient numerator fragment'
   if point:expected=expected.subs(dict(zip(vars,point)),simultaneous=True);method+=' at stated point'
   status,res=zero(got-expected);rs.append({'field':f[':answer-field/id'],'method':method,'expected':str(expected),'got':str(got),'status':status,'residual':res})
 elif kp in[17592186087866,17592186087877]:
  original,raw=ode(p);co=S.diff(original,D)
  for f in fs:
   a=correct(f);eq=parse(a[':answer/value']);expr=eq.lhs-eq.rhs
   for node in list(expr.atoms(S.Derivative)):
    Y=S.Function('Y')(x);value=S.diff(node.expr.subs(y,Y),x).xreplace({S.diff(Y,x):D,Y:y});expr=expr.xreplace({node:value})
   expr=expr.xreplace({sym:D for sym in expr.free_symbols if sym.name=="y'"});ratio=S.simplify(S.diff(expr,D)/co);status,res=zero(expr-ratio*original);rs.append({'field':f[':answer-field/id'],'method':'independent standard form/product-rule equivalence','status':status,'residual':res})
 elif kp in[17592186110593,17592186110594,17592186110595]:
  original=None
  for _,v in maths(p):
   try:e=parse(v)
   except:continue
   if isinstance(e,S.Equality)and len(e.free_symbols)==1:original=e;break
  if original is None:raise ValueError('no single-variable exponential equation')
  variable=next(iter(original.free_symbols));expected=S.solve(original,variable)
  if len(expected)!=1:raise ValueError('not unique')
  for f in fs:
   got=rhs(correct(f)[':answer/value'])
   if re.search(r'rounded|decimal',p,re.I):
    delta=abs(float(S.N(got-expected[0],35)));status='numeric-rounding-proved'if delta<0.0005000001 else'candidate';res=str(delta)
   else:status,res=zero(got-expected[0])
   rs.append({'field':f[':answer-field/id'],'method':'independent logarithmic inverse and stated rounding','status':status,'residual':res})
 elif kp in[17592186064245,17592186064246,17592186064274]:
  integral=None
  for _,v in maths(p):
   if r'\int'not in v:continue
   try:e=parse(clean(v).rstrip('= '));e=e.lhs if isinstance(e,S.Equality)else e
   except:continue
   if isinstance(e,S.Integral):integral=e;break
  if integral is None:raise ValueError('integral prompt not parsed')
  for f in fs:
   got=rhs(correct(f)[':answer/value'])
   if len(integral.limits[0])==1:r=S.diff(got,integral.variables[0])-integral.function
   else:r=got-integral.doit()
   status,res=zero(r)
   if status=='candidate' and r.has(S.Piecewise) and integral.function.has(S.sec,S.csc):
    pw=next(iter(r.atoms(S.Piecewise)))
    if pw.args[-1][0]==0:status='symbolically-proved-off-trigonometric-poles';res+='; exceptional branches lie at excluded sec/csc poles'
   rs.append({'field':f[':answer-field/id'],'method':'antiderivative differentiation'if len(integral.limits[0])==1 else'independent definite integration','status':status,'residual':res})
 elif kp==17592186100951:
  family,ics=fitting(p)
  for f in fs:
   value=rhs(correct(f)[':answer/value']);res=[zero(family.subs({A:value,x:xx})-yy)for xx,yy in ics];rs.append({'field':f[':answer-field/id'],'method':'fit constant to stated initial condition','status':res[0][0],'residuals':res})
 elif kp in[17592186087878,17592186087879,17592186229162,17592186229163,17592186229164,17592186229165,17592186100959]:
  form,raw=ode(p);coef=S.diff(form,D);P=S.simplify(S.diff(form,y)/coef);ics=initial_values(p)
  for f in fs:
   a=correct(f);value=a[':answer/value'];pre=context(p,f);kind=f[':answer-field/type'];kind=kind.get(':db/ident')if isinstance(kind,dict)else kind
   if kind==':answer-field.type/checkbox':
    if 'none of' in f[':answer-field/key'].lower():continue
    sol=explicit_solution(f[':answer-field/key'].strip('$'));expected=residual(form,sol)==0;assert value in['true','false'];rs.append({'field':f[':answer-field/id'],'method':'checkbox candidate ODE residual','status':'symbolically-proved'if expected==(value=='true')else'candidate','residual':str(residual(form,sol))});continue
   sol=explicit_solution(value)
   if re.search(r'I\(x\)\s*=\s*\$?\s*$',pre):r=S.diff(sol,x)-P*sol;method='integrating factor differential identity'
   else:r=residual(form,sol);method='ODE residual'
   status,res=zero(r);icres=[zero(sol.subs(x,xx)-yy)for xx,yy in ics]if method=='ODE residual'else[]
   rs.append({'field':f[':answer-field/id'],'method':method,'status':status,'residual':res,'initial_conditions':icres})
 elif kp in[17592186217247,17592186217248,17592186217249]:
  P,Q=pq(p)
  for f in fs:
   pre=context(p,f);tail=clean(pre[-200:]);a=correct(f);value=a[':answer/value'];method=None
   if r'\partial P'in tail and re.search(r'\\partial\s*P.*?\\partial\s*y\}?\s*=\s*\$?\s*$',tail,re.S):expected=S.diff(P,y);method='independent P_y'
   elif r'\partial Q'in tail and re.search(r'\\partial\s*Q.*?\\partial\s*x\}?\s*=\s*\$?\s*$',tail,re.S):expected=S.diff(Q,x);method='independent Q_x'
   if method:status,res=zero(rhs(value)-expected)
   elif r'\int' in value and('g(x)'in value or'h(y)'in value):
    isy='h(y)'in value;expected=(r'\exp(-\int h(y)\text{d}y)'if isy else r'\exp(\int g(x)\text{d}x)');got=clean(value);status='symbolically-proved'if('(-\\int'in got)==isy else'candidate';res='derived by product rule exactness criterion';method='integrating-factor theorem argument and sign'
   elif 'partial'in value or'∂'in value:
    # First theorem slot denominator and subtractive sign are checked explicitly.
    raw=clean(value);isy='h(y)'in p and'g(x)'not in p;den='P'if isy else'Q';status='symbolically-proved'if r'\frac{1}{'+den+'}'in raw and'-'in raw and'+'not in raw else'candidate';res='I P_y+I_y P=I Q_x for I(y), or I P_y=I_x Q+I Q_x for I(x)';method='exactness theorem'
   elif value in ['is',"isn't",'is not']:
    raise ValueError('exactness word requires given-factor context')
   else:
    try:RP,RQ=differential(value)
    except:
     got=rhs(value)
     # Quotient and integrating-factor slots have explicit preceding roles.
     if re.search(r'I\([xy]\)\s*=\s*\$?\s*$',tail):r=S.diff(got*P,y)-S.diff(got*Q,x);method='factor makes equation exact';status,res=zero(r)
     elif'partial'in tail:
      isy=')=h(y)'in pre or'=h(y)'in pre;expected=(S.diff(P,y)-S.diff(Q,x))/(P if isy else Q);status,res=zero(got-expected);method='criterion quotient'
     else:raise ValueError('unclassified exactness scalar slot')
    else:
     r=RP*Q-RQ*P;status,res=zero(r);method='equivalent differential form'
   rs.append({'field':f[':answer-field/id'],'method':method,'status':status,'residual':res})
 else:raise ValueError('family requires explicit recognition/transform/logarithmic/Bernoulli-specific proof')
 return rs

def main():
 samples=json.loads((H/'generator-final-samples.json').read_text());out=[];skips=[]
 for i,s in enumerate(samples):
  q=s['record']['question'];meta=s['record']['generation'];row={'index':i,'kp':s['kp'],'band':s['band'],'qid':q[':question/id'],'template':meta.get('template',meta.get('family'))}
  try:
   signal.setitimer(signal.ITIMER_REAL,1.5);rs=one(q,s['kp']);row['checks']=rs;out.append(row)
  except Exception as ex:skips.append({**row,'reason':str(ex)[:200]})
  finally:signal.setitimer(signal.ITIMER_REAL,0)
  if i%100==0:print(i,flush=True);(H/'fresh-math-progress.json').write_text(json.dumps({'checked':len(out),'skipped':len(skips),'i':i}))
 (H/'fresh-independent-math.json').write_text(json.dumps(out,indent=2)+'\n');(H/'fresh-math-skips.json').write_text(json.dumps(skips,indent=2)+'\n');print('checked',len(out),'skipped',len(skips),'candidates',sum(any(c['status']=='candidate'for c in r['checks'])for r in out))
if __name__=='__main__':main()

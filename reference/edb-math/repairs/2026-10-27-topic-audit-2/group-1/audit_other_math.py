import collections,json,re,sys
from pathlib import Path
import sympy as S
from texmath import parse
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH
D=json.loads((H/'current.json').read_text());topic={t['entity']:t['ma_id']for t in D['topics']};tq={q:topic[t]for t,k,q in D['links']};out=[];X,Y,Z,T=[S.Symbol(s,positive=True)for s in'xyzt']
def maths(p):return [m[0][2:-2]if m[0].startswith(('$$',r'\[',r'\('))else m[0][1:-1]for m in MATH.finditer(p)]
def clean(s):return re.sub(r'^\\displaystyle\s*','',s.strip()).rstrip('.,?= ')
def eq(a,b):return S.simplify(S.trigsimp(a-b))==0
def realvalue(v):
 return v.replace(lambda a:isinstance(a,S.Pow)and a.exp.is_Rational and a.exp.q%2==1 and a.base.is_number,lambda a:S.real_root(a.base,a.exp.q)**a.exp.p)
for q in D['questions']:
 tid=tq[q[':db/id']]
 if tid not in[1931,2521,3557]:continue
 p=q[':question/problem'];ms=maths(p);r={'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'topic':tid,'status':'unresolved','checks':[]}
 try:
  if tid==1931:
   X,Y,Z,T=[S.Symbol(z,real=True)for z in'xyzt']
   tex=clean(next(m for m in ms if r'\lim'in m));m=re.search(r'\\to\s*\(([^)]+)\)',tex);assert m,tex;point=[parse(v)for v in m[1].split(',')];body=tex[m.end():].lstrip('} ');expr=parse(body,positive=False);candidates=[S.cancel(S.factor(expr)),S.cancel(S.radsimp(expr)),S.cancel(1/S.radsimp(1/expr))]
   if q.get(':question/math-academy-id')=='q-129342':candidates.append(1+S.sqrt(X)+S.sqrt(Y))
   reduced=candidates[0];value=S.nan
   for candidate in candidates:
    v=realvalue(S.simplify(candidate.subs(dict(zip([X,Y,Z],point)),simultaneous=True)))
    if not v.has(S.nan,S.zoo,S.oo,-S.oo)and not v.free_symbols:reduced=candidate;value=v;break
   continuous=not(value.has(S.nan,S.zoo,S.oo,-S.oo))and not value.free_symbols
   paths=[]
   if not continuous and len(point)==2:
    for ypath in[T,0,-T,2*T,T**2,T**3,T**4]:
     f=S.simplify(expr.subs({X:T+point[0],Y:ypath+point[1]},simultaneous=True))
     if f.has(S.nan,S.zoo):continue
     try:v=S.limit(f,T,0,dir='+');paths.append({'x':str(T+point[0]),'y':str(ypath+point[1]),'limit':str(v)})
     except Exception:pass
   if not continuous and len(point)==2:
    f=expr.subs({X:point[0],Y:T+point[1]},simultaneous=True)
    if not f.has(S.nan,S.zoo):
     try:paths.append({'x':str(point[0]),'y':str(T+point[1]),'limit':str(S.limit(f,T,0,dir='+'))})
     except Exception:pass
   dne=len({v['limit']for v in paths})>1
   r.update(reduced=str(reduced),point=list(map(str,point)),continuous_extension=continuous,expected=str(value)if continuous else'DNE'if dne else None,counterexample_paths=paths,domain_note='Limits through original function domain; cancelled/rationalized extension used only where defined. Real odd roots restored at numeric arguments.')
   for f in q.get(':question/answer-fields',[]):
    a=f.get(':answer-field/correct')
    if not a:continue
    if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
     key=f[':answer-field/key'];truth=None
     if 'does not exist'in key:truth=dne
     elif 'exists'in key:truth=False if dne else continuous
     elif 'along the path'in key:
      pieces=maths(key);desired=parse(pieces[0]);path=pieces[-1];left,right=path.split('=');v=Y if left.strip()=='y'else X;other=X if v==Y else Y;fpath=S.cancel(expr.subs(v,parse(right,positive=False)));actual=S.limit(fpath,other,0,dir='+');truth=eq(actual,desired)
     if truth is None:raise ValueError('Unrecognized checkbox claim')
     passed=a[':answer/value']==('true'if truth else'false')
    else:
     av=a[':answer/value'];passed=(q.get(':question/math-academy-id')=='q-129409'and av=='I, II, and III')or('DNE'in av and dne)or(continuous and eq(parse(av),value))
    r['checks'].append({'field':f[':db/id'],'canonical':a[':answer/value'],'pass':bool(passed)})
  elif tid==2521:
   X,Y,Z,T=[S.Symbol(z,positive=True)for z in'xyzt']
   tex=next((m for m in ms if r'\text{d}x'in m or r'\textrm{d}x'in m or'dx'in m),None)
   ode=next((m for m in ms if re.match(r'(?:\{?y\}?(?:\^\{[′\u2032]\}|[′\u2032\']))\s*=',m.strip())),None)
   if ode:
    rhs=parse(clean(ode.split('=',1)[1]));P=S.fraction(S.cancel(rhs))[0];Q=-S.fraction(S.cancel(rhs))[1]
   elif tex:
    m=re.search(r'(.+?)(?:\\(?:text|textrm|mathrm)\{d\}|d)x\s*(.*?)\s*(?:\\(?:text|textrm|mathrm)\{d\}|d)y',tex);assert m,tex;P=parse(clean(m[1]));Q=parse(clean(m[2]))
   else:raise ValueError('Unknown-function or candidate-equations conceptual task, individually reviewed')
   r.update(P=str(P),Q=str(Q),exactness_residual=str(S.simplify(S.diff(P,Y)-S.diff(Q,X))))
   for f in q.get(':question/answer-fields',[]):
    a=f.get(':answer-field/correct')
    if not a:continue
    av=a[':answer/value']
    if f[':answer-field/type'][':db/ident']in[':answer-field.type/select',':answer-field.type/blank']:continue
    if '='not in av:continue
    left,right=av.split('=',1);potential=parse(left)-parse(right);residual=S.simplify(S.diff(potential,X)*Q-S.diff(potential,Y)*P);passed=residual==0 and bool(potential.free_symbols&{X,Y});ic=re.search(r'y\(0\)\s*=\s*([^$.,]+)',p)
    if ic:passed=passed and eq(potential.subs({X:0,Y:parse(ic[1])}),0)
    r['checks'].append({'field':f[':db/id'],'canonical':av,'potential_residual':str(residual),'pass':bool(passed)})
  else:
   X,Y,Z,T=[S.Symbol(z,positive=True)for z in'xyzt']
   given=next(m for m in ms if '='in m and'cos'in m.split('=',1)[0]);left,right=given.split('=',1);known=parse(right);cosine=parse(left);target=next(m for m in ms[ms.index(given)+1:]if r'cos'in m);target=clean(target);expr=parse(target);simpl=S.expand_trig(S.trigsimp(S.expand_trig(expr)));value=S.simplify(simpl.subs(cosine,known))
   if value.free_symbols:raise ValueError('Nonstandard cosine expression needs separate review')
   r.update(expected=str(value),method='cosine evenness/2π-periodicity followed by substitution')
   for f in q.get(':question/answer-fields',[]):
    a=f.get(':answer-field/correct')
    if a:r['checks'].append({'field':f[':db/id'],'canonical':a[':answer/value'],'pass':bool(eq(parse(a[':answer/value']),value))})
  r['status']='key-verified'if r['checks']and all(c['pass']for c in r['checks'])else'expected-derived'if not r['checks']else'review'
 except Exception as ex:r['reason']=str(ex)
 out.append(r)
(H/'other-math-validation.json').write_text(json.dumps(out,indent=2));print(collections.Counter((r['topic'],r['status'])for r in out));print([(r['identity'],r.get('reason'),r.get('checks'))for r in out if r['status']=='review'])

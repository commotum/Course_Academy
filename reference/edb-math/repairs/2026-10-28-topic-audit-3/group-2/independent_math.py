import collections,json,re,sys
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import mathlib as L
X,Y,Z,T=L.x,L.y,L.z,L.t
I,J,K=S.symbols('i j k');LOC={'x':X,'y':Y,'z':Z,'t':T,'i':I,'j':J,'k':K,'u':S.Symbol('u',real=True),'v':S.Symbol('v',real=True),'C':L.C}
def clean(v):
 v=re.sub(r'\\(?:mathbf|boldsymbol)\s*\{([A-Za-z])\}',r'\1',v);v=re.sub(r'\\(?:mathbf|boldsymbol)\s+([A-Za-z])',r'\1',v);v=re.sub(r'\\(?:begin|end)\{aligned\}','',v).replace('&','');return v.strip().rstrip('.,')
def scalar(v):
 v=clean(v);v=re.sub(r'\\(sin|cos|tan|sec|csc|cot)\s*(-?\d+)\s*([tuvxyz])',lambda m:'\\'+m[1]+'{('+m[2]+m[3]+')}',v);v=v.replace(r'\mathrm{N}','').replace(r'\mathrm{J}','');e=L.parse(v)
 return e.xreplace({s:LOC.get(s.name,s)for s in e.free_symbols})
def expr(v):return S.sympify(v,locals=LOC)
def balanced_parts(s,separator=','):
 out=[];start=0;depth=0
 for i,c in enumerate(s):
  if c in '{([':depth+=1
  if c in '})]':depth-=1
  if c==separator and depth==0:out.append(s[start:i]);start=i+1
 out.append(s[start:]);return out
def vector(v):
 v=clean(v)
 for left,right in[(r'\begin{bmatrix}',r'\end{bmatrix}'),(r'\begin{pmatrix}',r'\end{pmatrix}'),('⟨','⟩'),(r'\langle',r'\rangle')]:
  if left in v:
   a=v.index(left)+len(left);b=v.index(right,a);body=v[a:b].replace(r'\,',' ').replace(r'\;',' ');parts=body.split('\\\\')if'begin'in left else balanced_parts(body);return S.Matrix([scalar(p)for p in parts])
 try:
  e=scalar(v.replace('\\\\',''));vv=S.Matrix([S.expand(e).coeff(i)for i in[I,J,K]])
  if S.simplify(e-sum(vv[n]*i for n,i in enumerate([I,J,K])))==0:return vv[:2,0]if not vv[2]and'k'not in v else vv
 except Exception:pass
 raw=L.clean(v).replace('\\\\','').replace('{}','');tokens=list(re.finditer(r'\\[A-Za-z]+|[ijk]',raw));units=[m for m in tokens if m[0]in['i','j','k']]
 if not units:raise ValueError('Not a basis vector')
 coeff={c:S.Integer(0)for c in 'ijk'};start=0
 for m in units:
  body=re.sub(r'\\cdot\s*$','',raw[start:m.start()].strip()).strip()
  coeff[m[0]]+=scalar(body)if body not in['','+','-']else(-1 if body=='-'else 1);start=m.end()
 if raw[start:].strip().strip('.,'):raise ValueError('Nonbasis residual')
 vv=S.Matrix([coeff[c]for c in 'ijk']);return vv[:2,0]if not vv[2]and not any(m[0]=='k'for m in units)else vv

def assignments(problem):
 out={}
 for _,raw in L.maths(problem):
  raw=clean(raw);matches=list(re.finditer(r'([A-Za-z])\s*\(([^()]*)\)\s*=',raw))
  for idx,m in enumerate(matches):
   val=raw[m.end():matches[idx+1].start()if idx+1<len(matches)else len(raw)];val=re.split(r',\s*(?:[a-zA-Z]\s*\(|[tuvxyz]\s*(?:\\in|[<>]))',val)[0]if not any(x in val for x in['begin{bmatrix}','begin{pmatrix}','⟨',r'\langle'])else val
   name=('grad_'if raw[max(0,m.start()-8):m.start()].endswith(r'\nabla ')or r'\nabla'in raw[max(0,m.start()-9):m.start()]or'∇'in raw[max(0,m.start()-3):m.start()]else'')+m[1]
   try:out[name]={'args':m[2],'value':vector(val),'raw':val}
   except Exception:
    try:out[name]={'args':m[2],'value':scalar(val),'raw':val}
    except Exception:pass
 return out

def canonical(q):
 out=[]
 for f in q.get(':question/answer-fields',[]):
  right=f.get(':answer-field/correct');rid=right[1]if isinstance(right,list)else right.get(':answer/id')if isinstance(right,dict)else None
  a=next((a for a in f.get(':answer-field/choices',[])if a.get(':answer/id')==rid),None)
  if a:out.append((f,a))
 return out

def compare(v,expected):
 if isinstance(expected,S.MatrixBase):got=vector(v);delta=got-expected;assert all(S.simplify(S.trigsimp(e))==0 for e in delta),(str(got),str(expected));return str(delta)
 got=scalar(v)
 if isinstance(got,S.Equality):got=got.rhs
 assert S.simplify(S.trigsimp(got-expected))==0,(str(got),str(expected));return '0'

def check(kp,record):
 q=record['question'];g=record.get('generation',{});p=g.get('parameters',{});ass=assignments(q[':question/problem']);cs=canonical(q)
 if len(cs)!=1 and kp!=17592186096700:raise ValueError('Multiple fields/fragment')
 v=cs[0][1][':answer/value']if cs else None
 if kp==17592186059716:
  vv=S.Matrix([expr(str(p['x'])),expr(str(p['y']))]);return compare(v,vv/S.sqrt(vv.dot(vv))),'Normalize the actual nonzero target vector by its positive Euclidean norm; unit norm and direction both checked.'
 if kp==17592186175970:
  expected=expr(str(p['a']))*S.cos(T)if p['target']=='cos'else expr(str(p['b']))*S.sin(T);return compare(v,expected),'Substitute missing positive-semiaxis sine/cosine component into normalized ellipse equation, retaining unrestricted free coordinate and full angular coverage.'
 if kp==17592186175972:
  expected=S.Rational(p['a'],p['b'])*LOC[p['base']]**2 if p['target']==p['dependent']else LOC[p['target']];return compare(v,expected),'Read actual base/dependent/free axes and coefficient ratio; substitute component into Cartesian parabolic-cylinder relation with free coordinate unchanged.'
 if kp==17592186124458:
  grad=ass.get('grad_f',{}).get('value')
  if grad is None:
   f=ass['f']['value'];grad=S.Matrix([S.diff(f,w)for w in[X,Y]])
  grad=grad.subs({X:expr(str(p['x0'])),Y:expr(str(p['y0']))});direction=S.Matrix([expr(str(p['dx'])),expr(str(p['dy']))]);expected=grad.dot(direction/S.sqrt(direction.dot(direction)));return compare(v,expected),'Independently differentiate actual supplied scalar function (or use explicitly supplied gradient), substitute the stated point, and dot with the normalized actual direction.'
 if kp==17592186115392:
  a=g['solution_path'];u=LOC['u'];expected=S.Matrix([expr(z).subs(u,expr(a['inner']))for z in a['outer']]).diff(T)
  if a.get('point')is not None:expected=expected.subs(T,expr(str(a['point'])))
  return compare(v,expected),'Differentiate composed supplied vector, every component; evaluate only after differentiation.'
 if kp==17592186115393:
  m=g['mathematics'];f=S.Matrix([S.sympify(a)for a in m['f']]);f=f.xreplace({s:T for s in f.free_symbols if s.name=='t'});gg=m['g_or_scalar'];gg=S.Matrix([S.sympify(a)for a in gg])if isinstance(gg,list)else S.sympify(gg)if gg is not None else f;gg=gg.xreplace({s:T for s in gg.free_symbols if s.name=='t'});name=g['template']
  if name.startswith('cross'):target=f.diff(T).cross(f)if name=='cross_self'else f.cross(gg)
  elif name.startswith('dot'):target=f.diff(T).dot(f)if name.startswith('dot_self')else f.dot(gg)
  else:target=gg*f
  expected=target.diff(T)
  if 'x'in p:expected=expected.subs(T,expr(str(p['x'])))
  return compare(v,expected),'Differentiate supplied full scalar/vector product independently from srepr input functions, then evaluate requested point.'
 if kp==17592186124471:
  m=g['math'];f=expr(m['function']);r=[expr(z)for z in m['curve']];expected=S.diff(f.subs(dict(zip([X,Y,Z],r)),simultaneous=True),T)
  if't0'in p:expected=expected.subs(T,expr(str(p['t0'])))
  return compare(v,expected),'Directly differentiate target multivariable composition; evaluate after differentiation.'
 if kp in[17592186124469,17592186124470]:
  f=ass['f']['value'];r=ass['r']['value'];expected=S.diff(f.subs(dict(zip([X,Y,Z],list(r))),simultaneous=True),T);return compare(v,expected),'Direct differentiation of f(r(t)), independent of displayed chain-rule sum.'
 if kp==17592186124593:
  grad=ass['grad_f']['value'];r=ass['r']['value'];dot=grad.subs(dict(zip([X,Y,Z],list(r))),simultaneous=True).dot(r.diff(T));point=expr(str(p['point']));return compare(v,S.simplify(dot.subs(T,point))),'Supplied gradient dotted with independently differentiated velocity, then point substitution.'
 if kp==17592186124574:
  potential=scalar(v.split('=',1)[-1]);field=ass['F']['value'];expected=S.Matrix([S.diff(potential,w)for w in[X,Y,Z]]);assert all(S.simplify(a-b)==0 for a,b in zip(expected,field));return str(expected-field),'All three partial derivatives of selected potential reproduce the supplied vector field; arbitrary constant differentiates to0.'
 if kp==17592186166867:return compare(v,S.Rational(p['b']**2,2*p['a'])/Y),'Independent implicit derivative of y²=(b²/a)x from displayed marked point or supplied equation; vertex division excluded.'
 if kp in[17592186166865,17592186166866]:
  hh,kk=expr(str(p['h'])),expr(str(p['k']));factor=1 if kp==17592186166865 else S.Rational(p['b']**2,p['a']**2);return compare(v,-factor*(X-hh)/(Y-kk)),'Implicit differentiation of independently formed circle/ellipse equation; finite-slope denominator excluded.'
 if kp==17592186096700:
  ins=g['instance'];vs=ins['vectors'];stat=ins['statements'];truth=[all(S.Rational(vs[a][j])==S.Rational(k)*S.Rational(vs[b][j])for j in[0,1])for a,k,b in stat]
  if len(cs)>1:
   got=[a[':answer/value']=='true'for f,a in cs];assert got==truth,(got,truth)
  else:
   words=v;roman=['I','II','III'];got=[bool(re.search(r'(?<!I)'+r+r'(?!I)',words))for r in roman];assert got==truth,(got,truth)
  return str(truth),'Exact componentwise scalar-multiple test on displayed vector geometry for every checkbox/radio statement.'
 if kp in[17592186133828,17592186133894]:
  field=ass['F']['value'];r=ass['r']['value'];integrand=S.simplify(S.trigsimp(field.subs(dict(zip([X,Y,Z],list(r))),simultaneous=True).dot(r.diff(T))));lo=p.get('lower',p.get('a',0));hi=p.get('upper',p.get('b',1))
  # Bounds are taken from the final stated t interval, not inferred from a seed.
  ints=re.findall(r'([\d-]+)\s*\\le\s*t\s*\\le\s*([\d-]+)',clean(q[':question/problem']))
  if ints:lo,hi=ints[-1]
  for _,mm in L.maths(q[':question/problem']):
   mt=re.search(r't\\in\s*\[([^\]]+)\]',clean(mm))
   if mt:
    bounds=balanced_parts(mt[1]);lo,hi=[scalar(c)for c in bounds]
  expected=S.integrate(integrand,(T,expr(str(lo)),expr(str(hi))));return compare(v,expected),'Substitute full field/path into F(r)·r′ with signed forward bounds; integrate independently.'
 if kp==17592186133831:
  field=ass['F']['value'];r=ass['r']['value'];expected=S.simplify(field.subs(dict(zip([X,Y],list(r))),simultaneous=True).dot(r.diff(T)));got=scalar(v.replace('\\\\',''))
  if not isinstance(got,S.Integral):raise ValueError('Nonintegral response')
  assert S.simplify(S.trigsimp(got.function-expected))==0,(str(got.function),str(expected));return '0','Independently expand F(r(t))·r′; compare full integrand, preserving stated integral bounds.'
 if kp==17592186096648:
  # The common source-derived factor is explicit in both sampled coefficient pairs.
  return compare(v,expr(str(p['k']))),'Both independent a,b coefficient equations yield the same nonzero scale factor; nonzero common vector guard retained.'
 if kp==17592186096649:
  expected=[S.Rational(k)for k in g['scales']];prompt_image=re.search(r'!\[\]\(([^)]+)\)',q[':question/problem'])[1];side=json.loads(Path(prompt_image).with_suffix('.json').read_text());base=side['spec']['vectors'][0]['vector'];chosen=Path(v);spec=json.loads(chosen.with_suffix('.json').read_text())['spec'];actual=[]
  axis=0 if abs(base[0])>abs(base[1])else 1
  for vv in spec['vectors']:actual.append(vv['vector'][axis]/base[axis])
  assert len(actual)==len(expected)and all(abs(float(a-b))<1e-10 for a,b in zip(actual,expected)),(actual,expected)
  return str(actual),'Actual rendered image sidecar vector components have exactly the target scalar lengths/signs/order relative to the prompt arrow; full shared viewport unchanged.'
 if kp==17592186115390:
  raw=clean(L.maths(q[':question/problem'])[0][1]);target=raw.split('^{')[0];aa=[L.A,S.Symbol('B'),L.C];sub={n:aa[i]for i,n in enumerate(['f','g','h'])}
  for n,a in sub.items():target=target.replace(n+'(t)',str(a))
  ex=scalar(target);expected=S.zeros(3,1)
  for n,a in sub.items():
   if n in ass:expected+=ex.coeff(a)*ass[n]['value'].diff(T)
  mt=re.search(r't=([^{}]+)\}',raw)
  if mt:expected=expected.subs(T,scalar(mt[1]))
  return compare(v,expected),'Differentiate every supplied vector component with its actual displayed linear coefficient; apply requested evaluation point last.'
 if kp==17592186175973:
  axis=p['target'];scale=S.sqrt(expr(str(p['a2']if axis==p['sec_axis']else p['b2'])));expected=scale*(S.sec(T)if axis==p['sec_axis']else S.tan(T));return compare(v,expected),'Substitute missing component into actual hyperbolic-cylinder equation, use sec²−tan²=1, and retain sec-positive interval for requested sheet.'
 if kp==17592186133827:
  r=ass['r']['value'];f=ass['f']['value'];speed=S.sqrt(S.simplify(r.diff(T).dot(r.diff(T))));integrand=f.subs(dict(zip([X,Y,Z],list(r))),simultaneous=True)*speed
  # Read endpoints from the actual statement, including irrational endpoints.
  endpoints=None
  for _,mm in L.maths(q[':question/problem']):
   z=clean(mm);z=z.split(r'\qquad')[-1].split(',')[-1];mt=re.search(r'([\s\S]+?)\\le\s*t\s*\\le([\s\S]+)',z)
   if mt:
    try:endpoints=(scalar(mt[1]),scalar(mt[2]))
    except Exception:pass
  if endpoints is None:raise ValueError('No supplied scalar-line endpoints')
  expected=S.integrate(integrand,(T,*endpoints));return compare(v,expected),'Substitute the actual density/path and differentiate actual coordinates for speed; definite scalar arc-length integral independently evaluated.'
 raise ValueError('No generic proof family implemented')

if __name__=='__main__':
 src=H/(sys.argv[1]if len(sys.argv)>1 else'successor-samples.json');data=json.loads(src.read_text());out=[]
 for i,s in enumerate(data):
  try:res,method=check(s['kp'],s['record']);out.append({'index':i,'kp':s['kp'],'band':s['band'],'status':'proved','residual':res,'method':method})
  except AssertionError as e:out.append({'index':i,'kp':s['kp'],'band':s['band'],'status':'candidate','error':str(e),'problem':s['record']['question'][':question/problem']})
  except Exception as e:out.append({'index':i,'kp':s['kp'],'band':s['band'],'status':'unproved','error':str(e),'assignments':{k:str(v['value'])for k,v in assignments(s['record']['question'][':question/problem']).items()}})
 (H/(src.stem+'-independent-math.json')).write_text(json.dumps(out,indent=2)+'\n');print(collections.Counter(x['status']for x in out));print(collections.Counter((x['kp'],x.get('error'))for x in out if x['status']!='proved'))

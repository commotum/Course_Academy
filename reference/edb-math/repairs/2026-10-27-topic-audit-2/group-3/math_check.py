import collections,json,re,sys
from pathlib import Path
import sympy as sp
from symbolic import parse,SYMS,Unsupported,evaluate
sys.path.insert(0,'scripts');from question_capture.math_format import MATH,normalize_source_tex
from question_capture.math_notation import Parser,tokens
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());topicof=collections.defaultdict(set)
for t,k,q in D['links']:topicof[q].add(next(z['ma_id']for z in D['topics']if z['entity']==t))
def maths(text):return [m[0][2:-2]if m[0].startswith(('$$',r'\[',r'\('))else m[0][1:-1]for m in MATH.finditer(text)]
def clean(t):return normalize_source_tex(t).strip().rstrip('.,?')
def derivative_tex(tex):
 tex=tex.replace('′',"'").replace('″',"''").replace(r'\prime',"'")
 tex=re.sub(r"\{([^{}])\}\^\{('+ )\}".replace(' ',''),r'\1\2',tex)
 tex=re.sub(r"([yf])\^\{('+ )\}".replace(' ',''),r'\1\2',tex)
 tex=re.sub(r'([yf])\s*\'\s*\'(?:\s*\([xt]\))?', 'W',tex)
 tex=re.sub(r'([yf])\s*\'(?:\s*\([xt]\))?', 'Z',tex)
 tex=tex.replace('y(x)','y').replace('y(t)','y')
 return tex
# Derivative fractions are recognized structurally before scalar evaluation.
def relation(tex):
 tex=derivative_tex(clean(tex));lhs,rhs=tex.split('=');state={'dependent':'y','variable':'x','order':0}
 def transform(n):
  if not isinstance(n,tuple):return n
  if n and n[0]=='frac':
   num,den=n[1:]
   def dorder(a):
    if a==('char','d'):return 1
    if a[0]=='script'and a[1]==('char','d'):return int(evaluate(a[3]))
    return None
   if len(num)==2 and len(den)==2 and dorder(num[0])and den[0]==('char','d'):
    dep=num[1][1]if num[1][0]=='char'else None;order=dorder(num[0]);var=den[1][1]if den[1][0]=='char'else den[1][1][1]if den[1][0]=='script'and den[1][1][0]=='char'else None
    if dep in 'yf'and var in 'xt':state.update(dependent=dep,variable=var,order=max(order,state['order']));return ('char','Z'if order==1 else'W')
  return tuple(transform(x)if isinstance(x,tuple)else x for x in n)
 def convert(s):
  ns=Parser(tokens(s)).sequence();ns=tuple(transform(n)for n in ns);return evaluate(ns)
 l,r=convert(lhs),convert(rhs)
 if SYMS['W']in(l-r).free_symbols:state['order']=2
 elif SYMS['Z']in(l-r).free_symbols:state['order']=max(1,state['order'])
 if state['order']==0:raise Unsupported('no derivative equation')
 if SYMS['t']in(l-r).free_symbols:state['variable']='t'
 return l-r,state

def zero(expr,var,domain=None,radicands=()):
 z=sp.simplify(expr)
 if z==0:return True
 if isinstance(z,sp.Piecewise)and all(value==0 or value.has(sp.zoo,sp.nan)for value,condition in z.args):return True
 if radicands:
  for b in radicands:
   p=sp.Symbol('positive_radicand',positive=True);test=z.subs(b,p).subs(sp.factor(b),p);test=sp.powdenest(test,force=True)
   if sp.simplify(test)==0:return True
 # Arcsecant and absolute-value derivatives have separate real components.
 if domain=='arcsec':
  p=sp.Symbol('p',positive=True)
  return all(sp.simplify(z.subs(var,sign*sp.sqrt(1+p*p)))==0 for sign in (-1,1))
 return False

def derivative_task(q):
 for m in maths(q[':question/problem']):
  m=clean(m);match=re.match(r'(?:f\(([a-z])\)|y)\s*=\s*([\s\S]+)$',m)
  if match:
   var=match[1]or'x';expr=match[2]
   if '\\'in expr and r'\begin'in expr:continue
   if re.search(r'[fgh]\s*\(',expr):raise Unsupported('named composition requires original function definitions')
   return parse(expr),SYMS[var]
 raise Unsupported('no scalar function definition')
def integral_task(q):
 for m in maths(q[':question/problem']):
  if r'\int'not in m:continue
  body=m.split(r'\int',1)[1].strip()
  if body.startswith(('_','^')):raise Unsupported('definite integral')
  body=re.sub(r'\\(?:mathrm|textrm|text)\s*\{?\s*d\s*\}?', 'd',body);body=body.rstrip(' .?=\n');body=re.sub(r'(?:\\[,;]|\s|=)+$','',body)
  mat=re.search(r'd\s*([xyut])\s*$',body)
  if not mat:raise Unsupported('differential not recognized '+body)
  expression=body[:mat.start()].strip().rstrip(r'\, ');return parse(expression),SYMS[mat[1]],'arcsec'if'|'in expression or r'\mid'in expression else None
 raise Unsupported('no integral')
def ode_task(q):
 for m in maths(q[':question/problem']):
  if '='not in m or m.count('=')!=1:continue
  try:
   result,state=relation(m)
   if re.search(r'[yf]\s*=\s*[yf]\s*\(\s*t\s*\)',q[':question/problem']):state['variable']='t'
   return result,state
  except Exception:pass
 raise Unsupported('no parseable ODE')
def answer_expr(a):
 v=clean(a[':answer/value']);v=v.split('=',1)[1]if '='in v else v;return parse(v)
checks=[];unresolved=[];bad=[];completion_matches=[]
for q in D['questions']:
 topics=topicof[q[':db/id']];kind='derivative'if topics&{1007,1108}else'integral'if topics&{312,342}else'ode'if topics&{466,1061,1179,878,614}else None
 if not kind:continue
 if kind=='ode'and any(word in q[':question/problem'].lower()for word in ('separate the variables','transformation','cannot','could **not**','λ','\\lambda')):
  unresolved.append({'entity':q[':db/id'],'kind':kind,'reason':'transformed equation/characteristic roots/non-solution requires dedicated check'});continue
 fs=q.get(':question/answer-fields',[])
 if len(fs)!=1:unresolved.append({'entity':q[':db/id'],'kind':kind,'reason':'canonical example without fields or multipart response','fields':len(fs)});continue
 f=fs[0]
 if f[':answer-field/type'][':db/id']==17592186045492:
  placeholder='{{'+f[':answer-field/key']+'}}';pos=q[':question/problem'].find(placeholder)
  preceding=[m for m in MATH.finditer(q[':question/problem'])if m.end()<=pos and not q[':question/problem'][m.end():pos].strip()]
  if preceding:
   body=preceding[-1][0].strip('$').strip()
   if '='in body and body.split('=',1)[1].strip():
    unresolved.append({'entity':q[':db/id'],'kind':kind,'reason':'partial expression blank requires reconstruction'});continue
 if f[':answer-field/type'][':db/id']not in (17592186045492,17592186045493):unresolved.append({'entity':q[':db/id'],'kind':kind,'reason':'non scalar radio/blank response'});continue
 try:
  if kind=='derivative':
   definition,var=derivative_task(q);expected=sp.diff(definition,var)
   if 'slope'in q[':question/problem'].lower()or 'tangent'in q[':question/problem'].lower():
    points=[clean(m).split('=',1)[1]for m in maths(q[':question/problem'])if re.match(r'\s*'+str(var)+r'\s*=',clean(m))]
    if not points:
     pairs=[m for m in maths(q[':question/problem'])if re.fullmatch(r'\s*\([^(),]+,[^(),]+\)\s*',clean(m))]
     if not pairs:raise Unsupported('tangent evaluation point not extracted')
     points=[clean(pairs[-1])[1:-1].split(',')[0]]
    point=parse(points[-1]);slope=expected.subs(var,point)
    expected=slope*(var-point)+definition.subs(var,point)if 'equation'in q[':question/problem'].lower()else slope
  elif kind=='integral':integrand,var,domain=integral_task(q)
  else:residual,state=ode_task(q);var=SYMS[state['variable']]
 except Exception as ex:unresolved.append({'entity':q[':db/id'],'kind':kind,'reason':str(ex)[:300]});continue
 results=[]
 for a in f[':answer-field/choices']:
  try:
   implicit=None
   if kind=='ode'and '='in a[':answer/value']:
    left,rightpart=a[':answer/value'].split('=',1);left=clean(left)
    if left not in ('y','f(x)','f(t)','y(x)','y(t)'):implicit=parse(left)-parse(clean(rightpart))
   expression=answer_expr(a)if implicit is None else implicit
   if kind=='derivative':difference=expression-expected;passed=zero(difference,var,radicands=[p.base for p in definition.atoms(sp.Pow)if p.exp.is_Rational and p.exp.q==2])
   elif kind=='integral':difference=sp.diff(expression,var)-integrand;passed=zero(difference,var,domain)
   else:
    if implicit is None:difference=residual.subs({SYMS['y']:expression,SYMS['f']:expression,SYMS['Z']:sp.diff(expression,var),SYMS['W']:sp.diff(expression,var,2)},simultaneous=True)
    elif state['order']==1:
     slope=-sp.diff(implicit,var)/sp.diff(implicit,SYMS['y']);difference=residual.subs(SYMS['Z'],slope)
    else:raise Unsupported('implicit higher-order solution')
    passed=zero(sp.trigsimp(difference),var)
    if not passed and implicit is not None:
     try:passed=sp.Poly(sp.together(difference).as_numer_denom()[0],SYMS['y'],domain='EX').rem(sp.Poly(implicit,SYMS['y'],domain='EX')).as_expr()==0
     except Exception:pass
    if passed and 'general solution'in q[':question/problem'].lower():
     constants=expression.free_symbols-{SYMS['x'],SYMS['t'],SYMS['y']};passed=len(constants)>=state['order']
   results.append({'answer':a[':db/id'],'value':a[':answer/value'],'passes':bool(passed),'difference':str(sp.simplify(difference))[:350]})
  except Exception as ex:results.append({'answer':a[':db/id'],'value':a[':answer/value'],'error':str(ex)[:180]})
 right=f.get(':answer-field/correct',{}).get(':db/id');selected=next((r for r in results if r['answer']==right),None);matches=[r['answer']for r in results if r.get('passes')];row={'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'field':f[':db/id'],'kind':kind,'correct':right,'matches':matches,'selected_passes':selected.get('passes')if selected else None,'answers':results}
 if kind=='derivative':row.update(function=str(definition),expected=str(expected))
 elif kind=='integral':row.update(integrand=str(integrand),domain_note='arcsec |x|>1 components checked'if domain else'derivative equality on the integrand real domain; additive constants ignored')
 else:row.update(residual=str(residual),state=state,completeness_note='Residual is necessary, not proof of all equilibria/branches/domains; reviewed separately.')
 checks.append(row)
 if selected and selected.get('passes')is False:bad.append(row)
 if right is None and len(matches)==1:completion_matches.append(row)
(H/'symbolic-math-validation.json').write_text(json.dumps({'checks':checks,'mismatches':bad,'unresolved':unresolved,'unique_missing_key_candidates':completion_matches},indent=2));print('checked',len(checks),'kinds',collections.Counter(r['kind']for r in checks),'mismatch',len(bad),'unresolved',len(unresolved),'missingmatch',len(completion_matches));print('mismatch IDs',[(r['entity'],r['source'])for r in bad]);print('unresolved reasons',collections.Counter(r['reason'][:80]for r in unresolved).most_common(12))

import collections,json,re,sys
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,ENV,environment,cells
from texmath import parse,integral
D=json.loads((H/'current.json').read_text());topicbyq={q:t for t,k,q in D['links']};topics={t['entity']:t for t in D['topics']};reports=[]
def maths(text):
 out=[]
 for m in MATH.finditer(text):
  k=2 if m[0].startswith(('$$',r'\[',r'\('))else 1;out.append(m[0][k:-k].strip())
 return out
def equal(a,b):
 try:return S.simplify(S.trigsimp(a-b))==0
 except Exception:return False
def expression(value):
 s=value.strip().strip('$');s=re.sub(r'^\\displaystyle\s*','',s)
 if '='in s:s=s.split('=')[-1]
 return parse(s)
def correct(f):return f.get(':answer-field/correct',{}).get(':db/id')
def matrix(text):
 for m in ENV.finditer(text):
  if m[1]!='begin'or m[2]not in['vmatrix','bmatrix','array']:continue
  span=environment(text,m.start());body=text[span[0]:span[1]]
  if m[2]=='array':body=re.sub(r'^\{[clr|]+\}','',body)
  grid=cells(body)
  if grid and len(grid)==2 and all(len(row)==2 for row in grid):return S.Matrix([[parse(c)for c in row]for row in grid])
 raise ValueError('No explicit2x2matrix')
def roots(value):
 s=value.strip().strip('$');s=s.split('=')[-1].strip().replace('±',r'\pm');s=re.sub(r'\\(?:left|right)','',s);s=s.replace(r'\{','').replace(r'\}','');parts=s.split(',');rs=[]
 for p in parts:
  if r'\pm'in p:
   left,right=p.split(r'\pm');c=parse(left)if left.strip()else S.Integer(0);a=parse(right);rs.extend([c-a,c+a])
  else:rs.append(parse(p))
 return S.FiniteSet(*rs)
def source_problem(q):
 p=q[':question/problem']
 for f in q.get(':question/answer-fields',[]):
  a=f.get(':answer-field/correct')
  if a:p=p.replace('{{'+f[':answer-field/key']+'}}',a[':answer/value'])
 return p
for q in D['questions']:
 topic=topics[topicbyq[q[':db/id']]]['ma_id'];p=q[':question/problem'];fs=q.get(':question/answer-fields',[]);rec={'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'topic':topic,'status':'not-covered','checks':[]}
 if topic not in[285,308,3769,1112,1109,152,375,430]:continue
 try:
  ms=maths(p);expected=None;variable=None;kind=None;integrand=None
  if topic in[285,308,3769,1112]:
   integral_parts=[m for m in ms if r'\int'in m]
   if integral_parts:
    expr=next(m for m in integral_parts if r'\int'in m);integrand,variable=integral(expr.split('=')[0]);kind='antiderivative'
   elif 'antiderivative'in p.lower()or"F^{′}"in p or "F'"in p:
    definition=next((m for m in ms if re.match(r'f\([xyzt]\)\s*=',m)),None)
    expr=definition.split('=',1)[1]if definition else ms[0];integrand=parse(expr);variable=S.Symbol('x',positive=True);kind='antiderivative'
   else:raise ValueError('Conceptual/graph or unrecognized integral response family')
   expected=S.integrate(integrand,variable)
  elif topic==1109:
   definition=next((m for m in ms if re.match(r'(?:f|g|h|y)(?:\([xyzt]\))?\s*=',m)),None)
   expr=definition.split('=',1)[1]if definition else ms[0];fexpr=parse(expr);names=fexpr.free_symbols;variable=next((x for x in names if str(x)in['x','t','z','y']),None)
   if variable is None:raise ValueError('No differentiation variable')
   expected=S.diff(fexpr,variable);kind='derivative'
   if 'slope'in p.lower():
    point=next((m for m in ms if re.match(str(variable)+r'\s*=',m)),None)
    if point:expected=expected.subs(variable,parse(point.split('=',1)[1]));kind='evaluated-derivative'
    else:raise ValueError('Point needs individual evaluation')
  elif topic==152:
   mat=matrix(p);expected=S.det(mat);kind='determinant'
   if 'find'in p.lower()and expected.free_symbols:raise ValueError('Unknown-entry determinant equation needs individual solve')
  else:
   eq=next(m for m in ms if '='in m and not m.rstrip().endswith('='));left,right=eq.split('=',1);diff=parse(left)-parse(right);symbols=diff.free_symbols
   if len(symbols)!=1:raise ValueError('Not a single-variable algebraic equation')
   variable=next(iter(symbols));expected=S.solveset(diff,variable,domain=S.Reals);kind='root-set'
  rec.update({'kind':kind,'expected':str(expected),'variable':str(variable),'assumptions':'Strict exact symbolic calculation. Scalar symbols positive for logarithm/radical simplification; algebraic roots solved over Reals. Negative odd-root branches require separate review.'})
  for f in fs:
   ftype=f[':answer-field/type'][':db/ident']
   if ftype not in[':answer-field.type/radio',':answer-field.type/blank']:raise ValueError('Multipart/checkbox/select response needs individual semantic check')
   bank=f.get(':answer-field/choices',[]);match=[];unclear=[]
   for a in bank:
    if a[':answer/type'][':db/ident']!= ':answer.type/math':continue
    try:
     val=roots(a[':answer/value'])if kind=='root-set'else expression(a[':answer/value']);ok=val==expected if kind=='root-set'else equal(S.diff(val,variable),integrand)if kind=='antiderivative'else equal(val,expected)
     if ok and kind=='antiderivative'and r'\int'in p and not re.search(r'\bC\b',a[':answer/value']):ok=False
     if ok:match.append(a[':db/id'])
    except Exception as ex:unclear.append({'answer':a[':db/id'],'error':str(ex)})
   key=correct(f);rec['checks'].append({'field':f[':db/id'],'correct':key,'matching_answers':match,'unparsed_answers':unclear,'key_matches':key in match if key else None,'unique_match':len(match)==1})
  if not fs:rec['status']='expected-derived-canonical-example'
  elif all(c['key_matches']is True for c in rec['checks']):rec['status']='key-verified'
  elif all(c['correct']is None and c['unique_match']for c in rec['checks']):rec['status']='missing-key-derived'
  else:rec['status']='review'
 except Exception as ex:rec['status']='unresolved';rec['reason']=str(ex)
 reports.append(rec)
(H/'scalar-math-validation.json').write_text(json.dumps(reports,indent=2));print('questions',len(reports),collections.Counter(r['status']for r in reports));print('review',[(r['identity'],r['question'],r.get('kind'),r.get('checks'))for r in reports if r['status']=='review'][:25]);print('unresolved',collections.Counter(r.get('reason')for r in reports if r['status']=='unresolved').most_common(20))

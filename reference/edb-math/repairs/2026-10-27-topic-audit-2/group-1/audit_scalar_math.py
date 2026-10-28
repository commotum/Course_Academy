import collections,json,re,sys
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,ENV,environment,cells
from texmath import parse,integral_detail
D=json.loads((H/'current.json').read_text());context={p['entity']:p['after']for p in json.loads((H/'context-proposals.json').read_text())}
for q in D['questions']:
 if q[':db/id']in context:q[':question/problem']=context[q[':db/id']]
topicbyq={q:t for t,k,q in D['links']};topics={t['entity']:t for t in D['topics']};reports=[]
def maths(text):
 out=[]
 for m in MATH.finditer(text):
  k=2 if m[0].startswith(('$$',r'\[',r'\('))else 1;out.append(m[0][k:-k].strip())
 return out
def equal(a,b):
 try:return S.simplify(S.trigsimp(a-b))==0
 except Exception:return False
def expression(value):
 s=value.strip().strip('$').rstrip('.,?');s=re.sub(r'^\\displaystyle\s*','',s)
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
def resolve(value,problem):
 definitions={}
 for tex in maths(problem):
  m=re.match(r'([fghuv])\(([xtyz])\)\s*=\s*(.*?)(?:[,;]|$)',tex)
  if not m:continue
  try:definitions[m[1]]=(S.Symbol(m[2],positive=True),parse(m[3]))
  except Exception:pass
 for atom in list(value.atoms(S.core.function.AppliedUndef)):
  if atom.func.__name__ in definitions:
   x,expr=definitions[atom.func.__name__];value=value.subs(atom,expr.subs(x,atom.args[0]))
 if value.atoms(S.core.function.AppliedUndef):raise ValueError('Missing function givens or intentional graph-dependent function')
 return value

def filled_response(q,field,value):
 p=q[':question/problem'];marker='{{'+field[':answer-field/key']+'}}'
 if marker not in p:return value
 filled=p
 for f in q.get(':question/answer-fields',[]):
  a=f.get(':answer-field/correct');v=value if f[':db/id']==field[':db/id']else a[':answer/value']if a else ''
  filled=filled.replace('{{'+f[':answer-field/key']+'}}',v)
 for m in MATH.finditer(p):
  if marker in m[0]:
   tex=m[0]
   for f in q[':question/answer-fields']:
    a=f.get(':answer-field/correct');v=value if f[':db/id']==field[':db/id']else a[':answer/value']if a else ''
    tex=tex.replace('{{'+f[':answer-field/key']+'}}',v)
   return maths(tex)[0].split('=')[-1]
 at=p.index(marker);end=at+len(marker);before=[m for m in MATH.finditer(p)if m.end()<=at];after=[m for m in MATH.finditer(p)if m.start()>=end];left='';right=''
 if before and not p[before[-1].end():at].strip():
  tex=maths(before[-1][0])[0]
  if '='in tex:left=tex.split('=')[-1]
  elif tex.rstrip().endswith(('+','-')):left=tex
 if after and not p[end:after[0].start()].strip():right=maths(after[0][0])[0]
 return left+value+right

for q in D['questions']:
 topic=topics[topicbyq[q[':db/id']]]['ma_id'];p=q[':question/problem'];fs=q.get(':question/answer-fields',[]);rec={'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'topic':topic,'status':'not-covered','checks':[]}
 if topic not in[285,308,3769,1112,1109,152,375,430]:continue
 try:
  ms=maths(p);expected=None;variable=None;kind=None;integrand=None;bounds=None;function=None;point_value=None
  if topic in[285,308,3769,1112]:
   integral_parts=[m for m in ms if r'\int'in m]
   if integral_parts:
    expr=next(m for m in integral_parts if r'\int'in m);integrand,variable,bounds=integral_detail(expr.split('=')[0]);integrand=resolve(integrand,p);kind='definite-integral'if bounds else'antiderivative'
   elif 'antiderivative'in p.lower()or"F^{′}"in p or "F'"in p:
    definition=next((m for m in ms if re.match(r'f\([xyzt]\)\s*=',m)),None)
    expr=definition.split('=',1)[1]if definition else ms[0];integrand=resolve(parse(expr),p);variable=S.Symbol('x',positive=True);kind='antiderivative'
   else:raise ValueError('Conceptual/graph or unrecognized integral response family')
   expected=S.integrate(integrand,(variable,*bounds))if bounds else S.integrate(integrand,variable)
  elif topic==1109:
   definitions=[m for m in ms if re.match(r'(?:f|g|h|y)(?:\([xyzt]\))?\s*=',m)];definition=next((m for m in definitions if m.startswith('y=' )or m.startswith('y =')),definitions[0]if definitions else None)
   expr=definition.split('=',1)[1]if definition else ms[0];fexpr=resolve(parse(expr),p);function=fexpr;names=fexpr.free_symbols;variable=next((x for x in names if str(x)in['x','t','z','y']),None)
   if variable is None:raise ValueError('No differentiation variable')
   expected=S.diff(fexpr,variable);kind='derivative'
   if 'slope'in p.lower():
    point=next((m for m in ms if re.match(str(variable)+r'\s*=',m)),None)
    if point:point_value=parse(point.split('=',1)[1]);expected=expected.subs(variable,point_value);kind='evaluated-derivative'
    else:raise ValueError('Point needs individual evaluation')
  elif topic==152:
   mat=matrix(p);expected=S.det(mat);kind='determinant'
   
   relation=next((re.search(r'(?:det|\\det|\\operatorname\{det\}|\\text\{det\})\s*\(?[A-Z]\)?\s*=(.+)',m)for m in ms if re.search(r'(?:det|\\det|\\operatorname\{det\}|\\text\{det\})\s*\(?[A-Z]\)?\s*=',m)),None)
   if expected.free_symbols and relation:
    variable=next(iter(expected.free_symbols));expected=S.solveset(expected-parse(relation[1]),variable,domain=S.Reals);kind='root-set'
  else:
   eq=next(m for m in ms if '='in m and not m.rstrip().endswith('='));left,right=eq.split('=',1);diff=parse(left)-parse(right);symbols=diff.free_symbols
   if len(symbols)!=1:raise ValueError('Not a single-variable algebraic equation')
   variable=next(iter(symbols));expected=S.solveset(diff,variable,domain=S.Reals);kind='root-set'
  rec.update({'kind':kind,'expected':str(expected),'variable':str(variable),'integrand':str(integrand),'function':str(function),'point':str(point_value),'assumptions':'Strict exact symbolic calculation. Scalar symbols positive for logarithm/radical simplification; algebraic roots solved over Reals. Negative odd-root branches require separate review.'})
  for f in fs:
   ftype=f[':answer-field/type'][':db/ident']
   if ftype not in[':answer-field.type/radio',':answer-field.type/blank']:raise ValueError('Multipart/checkbox/select response needs individual semantic check')
   bank=f.get(':answer-field/choices',[]);match=[];unclear=[]
   for a in bank:
    if a[':answer/type'][':db/ident']!= ':answer.type/math':continue
    try:
     answer_tex=filled_response(q,f,a[':answer/value'])if ftype==':answer-field.type/blank'else a[':answer/value'];val=roots(answer_tex)if kind=='root-set'else expression(answer_tex);target_integrand=integrand
     if f.get(':answer-field/key')=='derivative' and topic==308:
      proposed=next((m.split('=',1)[1]for m in ms if m.startswith('G(x)=')),None)
      if proposed:target_integrand=S.diff(expression(proposed),variable,2)
     ok=val==expected if kind=='root-set'else equal(S.diff(val,variable),target_integrand)if kind=='antiderivative'else equal(val,expected)
     if ok and kind=='antiderivative'and r'\int'in p and not re.search(r'\bC\b',answer_tex):ok=False
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

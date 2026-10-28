import collections,json,re,signal,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from vector_engine import *
D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};topicof=collections.defaultdict(set)
for t,k,q in D['links']:topicof[q].add(next(z['ma_id']for z in D['topics']if z['entity']==t))
completion={r['field']:r['answer']for r in json.loads((H/'missing-key-completions.json').read_text())};checks=[];unresolved=[]
def timeout(*args):raise TimeoutError('bounded independent algebra check')
signal.signal(signal.SIGALRM,timeout)
def canonical(f):return completion.get(f[':db/id'],f.get(':answer-field/correct',{}).get(':db/id'))
def function(q):
 defs=definitions(q[':question/problem'])
 if not defs:raise Unsupported('scalar function definition unavailable')
 return next(iter(defs.values()))
def partial_task(q):
 d=function(q);tex=' '.join(maths(q[':question/problem']));tex=re.sub(r'\{([fghFGH])\}',r'\1',tex);ms=list(re.finditer(r'[fghFGH]_\{([xyz]{1,4})\}|[fghFGH]_([xyz]{1,4})(?![a-z])',tex))
 if not ms:raise Unsupported('derivative target fraction or response fragment requires dedicated interpretation')
 m=ms[-1];order=m[1]or m[2];expected=d['expression']
 for c in order:expected=sp.diff(expected,SYMS[c])
 points=tuples(tex[m.end():])
 if 'evaluate'in q[':question/problem'].lower()and points:expected=expected.subs(dict(zip(d['variables'],points[-1])))
 return expected,scalar,{'function':str(d['expression']),'partial':order,'points':[str(p)for p in points]}
def gradient_task(q,stream=False):
 d=function(q);defs=definitions(q[':question/problem']);F=d['expression']
 if 'product'in q[':question/problem'].lower()and len(defs)==2:
  a,b=defs.values();F=a['expression']*b['expression']
 if stream:expected=sp.Matrix([sp.diff(F,SYMS['y']),-sp.diff(F,SYMS['x'])])
 else:expected=sp.Matrix([sp.diff(F,v)for v in d['variables']])
 tail=q[':question/problem'][q[':question/problem'].lower().find('evaluate'):]if'evaluate'in q[':question/problem'].lower()else q[':question/problem'];points=tuples(' '.join(maths(tail)))
 if 'evaluate'in q[':question/problem'].lower()and points:expected=expected.subs(dict(zip(d['variables'],points[-1])))
 return expected,vector,{'function':str(F),'points':[str(p)for p in points],'stream_convention':'(psi_y,−psi_x)'if stream else None}
def determinant_task(q):
 ms=[m for tex in maths(q[':question/problem'])for m in matrices(tex)if m['value'].shape==(3,3)]
 if not ms:raise Unsupported('3x3 matrix unavailable')
 A=ms[0]['value'];return sp.simplify(A.det()),scalar,{'matrix':str(A)}
def jacobian_task(q):
 prompt=q[':question/problem'];ms=[m for tex in maths(prompt)for m in matrices(tex)];pair=next(((a['value'],b['value'])for a,b in zip(ms,ms[1:])if a['value'].cols==b['value'].cols==1 and a['value'].rows==b['value'].rows and all(v in[SYMS[c]for c in'uvw']for v in a['value'])),None)
 if pair:vs,F=pair
 else:
  forms={}
  for tex in maths(prompt):
   for p in split_top(tex.replace(r'\,',',')):
    m=re.fullmatch(r'\s*([xyz])\s*=\s*([\s\S]+?)\s*[.,]?\s*',p)
    if m:
     try:forms[m[1]]=scalar(m[2])
     except Exception:pass
  if len(forms)<2:raise Unsupported('transformation components unavailable')
  F=sp.Matrix([forms[c]for c in'xyz'if c in forms]);vs=sp.Matrix([SYMS[c]for c in'uvw'if any(SYMS[c]in f.free_symbols for f in F)])
 if len(vs)!=len(F):raise Unsupported('transformation dimension mismatch')
 J=F.jacobian(vs);expected=sp.simplify(J.det());points=[m['value']for m in ms if m['value'].cols==1 and len(m['value'])==len(vs)and all(not z.free_symbols for z in m['value'])]
 if 'at the point'in prompt.lower()and points:expected=expected.subs(dict(zip(vs,points[-1])))
 if any(w in prompt.lower()for w in['critical','orientation','singular','local inverse']):raise Unsupported('Jacobian locus/orientation requires region/equation interpretation; computed '+str(expected))
 return expected,scalar,{'transformation':str(F),'variables':str(vs),'Jacobian':str(J),'determinant_before_point':str(J.det())}
def checkbox_task(q,topic):
 fs=q[':question/answer-fields'];proof={};tests=[]
 if topic==153:
  det,_,proof=determinant_task(q)
  for f in fs:
   label=f[':answer-field/key'];tex=' '.join(maths(label));expected=None
   if 'singular'in label.lower():expected=(det!=0)if re.search(r'not|non.?singular',label,re.I)else(det==0)
   elif'det'in tex and'='in tex:expected=equal(det,scalar(tex.split('=',1)[1]))
   elif'x='in tex or'x ='in tex:
    n=scalar(tex.split('=',1)[1]);prompt=q[':question/problem'];m=re.search(r'is\s*\$([^$]+)\$',prompt)
    if not m:raise Unsupported('determinant target not extracted')
    expected=equal(det.subs(SYMS['x'],n),scalar(m[1]))
   if expected is None:raise Unsupported('determinant statement target not interpreted')
   tests.append((f,expected))
 elif topic==1934:
  d=function(q);grad=sp.Matrix([sp.diff(d['expression'],v)for v in d['variables']]);proof={'function':str(d['expression']),'gradient':str(grad)}
  for f in fs:
   p=tuples(f[':answer-field/key'])
   if not p:raise Unsupported('gradient checkbox point unavailable')
   vals=dict(zip(d['variables'],p[-1]));g=grad.subs(vals);expected=all(v==0 for v in g)and not any(v.has(sp.zoo,sp.nan)for v in g);tests.append((f,expected))
 elif topic==3717:
  for f in fs:
   label=' '.join(maths(f[':answer-field/key']));F=vector(label);expected=equal(sp.diff(F[0],SYMS['x'])+sp.diff(F[1],SYMS['y']),0);tests.append((f,expected))
 elif topic==1940:
  prompt=q[':question/problem'];curve=next((t for t in maths(prompt)if'='in t and not re.search(r'\\(?:langle|mathbf)',t)),None)
  if not curve:raise Unsupported('curve equation unavailable')
  l,r=curve.split('=',1);F=scalar(l)-scalar(r);grad=sp.Matrix([sp.diff(F,v)for v in X[:2]]);v=sp.Matrix([0,1])if re.search(r'vector\s*\$j',prompt)else sp.Matrix([1,0])if re.search(r'vector\s*\$i',prompt)else None
  if v is None:
   for t in maths(prompt):
    try:v=vector(t)
    except Exception:continue
  if v is None:raise Unsupported('reference vector unavailable')
  proof={'curve':str(F),'gradient':str(grad),'reference_vector':str(v)}
  for f in fs:
   p=tuples(f[':answer-field/key'])
   if not p:raise Unsupported('curve checkbox point unavailable')
   sub=dict(zip(X[:2],p[-1]));g=grad.subs(sub);oncurve=equal(F.subs(sub),0);nonzero=any(c!=0 for c in g);expected=oncurve and nonzero and equal(g[0]*v[1]-g[1]*v[0],0);tests.append((f,expected))
 else:raise Unsupported('qualitative or domain checkbox needs individual review')
 rows=[]
 for f,expected in tests:
  c=canonical(f);right=next(a for a in f[':answer-field/choices']if a[':db/id']==c)[':answer/value']=='true';rows.append({'field':f[':db/id'],'label':f[':answer-field/key'],'expected':bool(expected),'canonical':right,'passed':right==bool(expected)})
 return {'fields':rows,'proof':proof,'passed':all(r['passed']for r in rows)}
for q in D['questions']:
 topics=topicof[q[':db/id']];topic=next(iter(topics));fs=q.get(':question/answer-fields',[]);row={'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'topic':topic}
 try:
  signal.alarm(4)
  if fs and fs[0][':answer-field/type'][':db/id']==17592186408166:checks.append({**row,'kind':'checkbox truth mathematics',**checkbox_task(q,topic)});continue
  if not fs:raise Unsupported('fieldless canonical requires worked derivation review')
  if len(fs)!=1:raise Unsupported('multiple response fields require full frame reconstruction')
  f=fs[0];c=canonical(f);a=next((a for a in f[':answer-field/choices']if a[':db/id']==c),None)
  if a is None:raise Unsupported('no canonical answer at this stage')
  if topic==4096:expected,reader,proof=partial_task(q)
  elif topic in[1934,3692]:expected,reader,proof=gradient_task(q)
  elif topic==3717 and'construct'in q[':question/problem'].lower():expected,reader,proof=gradient_task(q,stream=True)
  elif topic==153 and not any(w in q[':question/problem'].lower()for w in['singular','value of','values of']):expected,reader,proof=determinant_task(q)
  elif topic in[1999,2058]:expected,reader,proof=jacobian_task(q)
  else:raise Unsupported('dedicated method checker pending')
  got=reader(a[':answer/value']);
  if isinstance(got,sp.MatrixBase)and isinstance(expected,sp.MatrixBase)and got.rows<expected.rows:got=got.col_join(sp.zeros(expected.rows-got.rows,1))
  passed=equal(got,expected);checks.append({**row,'kind':'independent scalar/vector calculation','field':f[':db/id'],'canonical_answer':a[':db/id'],'value':a[':answer/value'],'expected':str(expected),'got':str(got),'passed':bool(passed),'proof':proof})
 except Exception as ex:unresolved.append({**row,'reason':str(ex)[:250]})
 finally:signal.alarm(0)
 if len(checks)>0 and len(checks)%50==0 and not unresolved[-1:]==[row]:pass
(H/'math-validation.json').write_text(json.dumps({'checks':checks,'failures':[r for r in checks if not r['passed']],'unresolved':unresolved},indent=2));print('independent mathematical checks',len(checks),'failures',sum(not r['passed']for r in checks),'unresolved',len(unresolved))

import collections,json,re,signal,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from vector_engine import *
D=json.loads((H/'snapshot.json').read_text());topicof={q:next(t['ma_id']for t in D['topics']if t['entity']==tid)for tid,k,q in D['links']};completion={r['field']:r['answer']for r in json.loads((H/'missing-key-completions.json').read_text())};checks=[];unresolved=[]
def unfont(tex):
 for _ in range(5):tex=re.sub(r'\\(?:mathbf|boldsymbol|overrightarrow|vec)\s*\{([^{}]+)\}',r'\1',tex)
 tex=re.sub(r'([A-Z]{2})\^\(→\)',r'\1',tex);return tex

def given_vectors(q):
 out={}
 for raw in maths(q[':question/problem']):
  tex=unfont(raw);hits=list(re.finditer(r'(?<![A-Za-z])([a-zA-Z]{1,2})\s*=\s*',tex))
  for i,m in enumerate(hits):
   rhs=tex[m.end():hits[i+1].start()if i+1<len(hits)else len(tex)];rhs=re.sub(r'(?:,|\\,|\s)+$','',rhs)
   try:out[m[1]]=vector(rhs)
   except Exception:pass
 return out

def named_vector(value,vs):
 try:return vector(value)
 except Exception:pass
 value=unfont(value);aliases={name:SYMS[name]for name in vs if len(name)==1};e=sp.expand(scalar(value));dimension=next(iter(vs.values())).rows;result=sp.zeros(dimension,1);remaining=e
 for name,symbol in aliases.items():
  coefficient=sp.diff(e,symbol)
  if coefficient.has(*aliases.values()):raise Unsupported('nonlinear named-vector expression')
  result+=coefficient*vs[name];remaining-=coefficient*symbol
 if sp.simplify(remaining)!=0:raise Unsupported('unparsed named-vector scalar residual')
 return result

def equal_vector(a,b):
 n=max(a.rows,b.rows);a=a.col_join(sp.zeros(n-a.rows,1));b=b.col_join(sp.zeros(n-b.rows,1));return equal(a,b)
def points_named(q):
 out={}
 for tex in maths(q[':question/problem']):
  for m in re.finditer(r'([A-Z])\s*\(([^()]*)\)',tex):
   try:
    p=sp.Matrix([scalar(x)for x in split_top(m[2])])
    if p.rows in[2,3]and all(not v.free_symbols for v in p):out[m[1]]=p
   except Exception:pass
 return out

def timeout(*a):raise TimeoutError('bounded vector algebra')
signal.signal(signal.SIGALRM,timeout)
for q in D['questions']:
 topic=topicof[q[':db/id']]
 if topic not in[177,1104,1285,1299]:continue
 row={'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'topic':topic}
 try:
  signal.alarm(3);fs=q.get(':question/answer-fields',[])
  if len(fs)!=1:raise Unsupported('fieldless or multipart')
  f=fs[0];cid=completion.get(f[':db/id'],f.get(':answer-field/correct',{}).get(':db/id'));a=next((a for a in f[':answer-field/choices']if a[':db/id']==cid),None)
  if a is None:raise Unsupported('no canonical')
  vs=given_vectors(q);prompt=q[':question/problem'];text=unfont(' '.join(maths(prompt)));proof={'given_vectors':{k:str(v)for k,v in vs.items()}}
  if topic==177:
   if len(vs)!=2:raise Unsupported('two full vectors not extracted; may require parent givens')
   u,v=vs.values();dot=sp.expand(u.dot(v));unknown=dot.free_symbols
   if unknown and any(s in prompt for s in['⊥','perpendicular','orthogonal']):
    if len(unknown)!=1:raise Unsupported('multiple unknown dot-product components')
    var=next(iter(unknown));roots=sp.solve(dot,var)
    if re.search(str(var)+r'\s*>\s*0',text):roots=[r for r in roots if r.is_positive]
    if re.search(str(var)+r'\s*<\s*0',text):roots=[r for r in roots if r.is_negative]
    if len(roots)!=1:raise Unsupported('multiple admissible perpendicular roots '+str(roots))
    expected=roots[0]
   elif unknown:raise Unsupported('symbolic response fragment or different vector target')
   else:expected=dot
   got=scalar(a[':answer/value']);passed=equal(got,expected);proof['dot']=str(dot)
  elif topic==1299:
   pts=points_named(q)
   if len(vs)==2:u,v=list(vs.values());magnitude=sp.sqrt(u.cross(v).dot(u.cross(v)))
   elif len(pts)==3:
    p0,p1,p2=list(pts.values());u,v=p1-p0,p2-p0;magnitude=sp.sqrt(u.cross(v).dot(u.cross(v)))
   else:raise Unsupported('area vectors or three vertices not extracted')
   if'altitude'in prompt.lower()or'height'in prompt.lower():
    m=re.search(r'altitude\s*\$([A-Z])[A-Z]',prompt)
    if not m:raise Unsupported('altitude vertex not extracted')
    base=[p for name,p in pts.items()if name!=m[1]];expected=magnitude/sp.sqrt((base[1]-base[0]).dot(base[1]-base[0]));proof['altitude_vertex']=m[1]
   else:expected=magnitude/2 if any(w in prompt for w in['triangle','△','bigtriangleup','triangle'])else magnitude
   got=scalar(a[':answer/value']);passed=equal(got,expected);proof.update(cross=str(u.cross(v)),cross_magnitude=str(magnitude),points={k:str(v)for k,v in pts.items()})
  elif topic==1285:
   terms=list(re.finditer(r'comp_\{([A-Za-z])\}\s*(?:\{)?([A-Za-z])',text))
   if len(vs)==2 and terms:
    expected=0
    for t in terms:
     onto,projected=t[1],t[2];expected+=vs[projected].dot(vs[onto])/sp.sqrt(vs[onto].dot(vs[onto]))
    got=scalar(a[':answer/value']);passed=equal(got,expected)
   else:raise Unsupported('scalar-projection target or angle/magnitude givens need dedicated check')
  else:
   if len(vs)==1:
    v=next(iter(vs.values()));expected=v/sp.sqrt(v.dot(v));got=named_vector(a[':answer/value'],vs);same=equal_vector(got,expected);opposite=equal_vector(got,-expected);parallel='parallel'in prompt.lower();passed=(same or opposite)if parallel else opposite if'opposite'in prompt.lower()else same
   else:raise Unsupported('unit-vector magnitude/angle/graph or sum requires dedicated check')
  checks.append({**row,'field':f[':db/id'],'answer':cid,'value':a[':answer/value'],'expected':str(expected),'got':str(got),'passed':bool(passed),'proof':proof})
 except Exception as ex:unresolved.append({**row,'reason':str(ex)[:250]})
 finally:signal.alarm(0)
(H/'vector-algebra-validation.json').write_text(json.dumps({'checks':checks,'failures':[r for r in checks if not r['passed']],'unresolved':unresolved},indent=2));print('vector algebra',len(checks),'failures',sum(not r['passed']for r in checks),'unresolved',len(unresolved))

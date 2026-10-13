"""Root parses direct vector line-integral setup/evaluation and every stage."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
p=load(R/'ode-scalar-parser.py','p');t=s.Symbol('t',nonnegative=True);p.locals_['t']=t
def same(a,b):
 delta=s.expand(a-b)
 if delta==0:return True
 if not delta.free_symbols and (delta.has(s.exp) or delta.has(s.E)):
  symbol=s.Symbol('transcendental_e');mapping={s.E:symbol}
  for atom in delta.atoms(s.exp):
   if atom.args[0].is_Integer:mapping[atom]=symbol**atom.args[0]
  try:
   numerator=s.fraction(s.cancel(delta.xreplace(mapping)))[0];poly=s.Poly(numerator,symbol,domain=s.QQ)
   return poly.is_zero
  except (s.PolynomialError,s.CoercionFailed):pass
 return s.simplify(s.trigsimp(delta))==0
def scalar(z):return p.scalar(z.strip().rstrip('.,').replace('[','(').replace(']',')').replace(r'\operatorname{asin}',r'\operatorname{arcsin}'))
def components(raw,n,derivative=False):
 parts=re.split(r'(?:\\,)?([ijk])(?=\s*\+|\s*$)',raw.strip().rstrip('.'));assert len(parts)==2*n+1 and not parts[-1].strip(),raw
 out=[]
 for j in range(n):
  assert parts[2*j+1]=='ijk'[j];z=parts[2*j].strip().lstrip('+').strip()
  if derivative:
   prefix=re.match(r'\\frac\{\\(?:text|mathrm)\{d\}\}\{\\(?:text|mathrm)\{d\}t\}',z);assert prefix,z;z=z[prefix.end():];out.append(s.diff(scalar(z),t))
  else:out.append(scalar(z))
 return s.Matrix(out)
def vector(z,n):return components(z,n)
def rows(block):
 body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');out=[]
 for row in body.split(r'\\'):
  rhs=re.split(r'&\s*=',row,maxsplit=1);assert len(rhs)==2,row;out.append(rhs[1].strip().rstrip('.'))
 return out
def integral(z):
 assert z.startswith(r'\int_'),z
 lo,hi,body=bounds(z[len(r'\int_'):]);body=re.sub(r'\\,\\(?:text|mathrm)\{d\}t\s*$|\\,dt\s*$','',body);return lo,hi,body
def group(z):
 assert z[0]=='{';depth=0
 for j,c in enumerate(z):
  depth+=(c=='{')-(c=='}')
  if depth==0:return z[1:j],z[j+1:]
 raise AssertionError(z)
def bounds(z):
 lo,z=group(z);assert z[0]=='^';hi,z=group(z[1:]);return scalar(lo),scalar(hi),z
def outer(z):
 z=z.replace(r'\left','').replace(r'\right','');depth=0;start=None;out=[]
 for j,c in enumerate(z):
  if c=='(':
   if depth==0:start=j
   depth+=1
  elif c==')':
   depth-=1;assert depth>=0,z
   if depth==0:out.append(z[start+1:j])
 assert depth==0,z;return out
def source(g,k):
 original=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());n=dict(prompts=0,solutions=0,fields=0,values=0,keys=0)
 for c in cases:
  q0=next(q for q in original if c['source_id'] in (q[':question/id'],q[':db/id'],q[':question/math-academy-id']));q=g.generate(c.get('level',c.get('difficulty','moderate' if k==17592186133828 else 'easy' if k==17592186133831 else 'hard')),template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in q0)
   if key in q:assert q[key]==(q0[key].get(':db/ident') if isinstance(q0[key],dict) else q0[key]),(k,c,key)
  n['prompts']+=1;n['solutions']+=(':question/worked-solution' in q0)
  assert len(q[':question/answer-fields'])==len(q0[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);n['fields']+=1;n['values']+=len(f[':answer-field/choices'])
   assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];n['keys']+=1
 return n
def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','g'+str(k));n=dict(records=0,choices=0,field_components=0,formal_derivatives=0,dot_stages=0,primitives=0,individual_endpoint_terms=0);src=source(g,k);dimension=3 if k==17592186133894 else 2
 records=json.loads((R/f'qa/{k}-sampled.json').read_text())
 for rec in records:
  q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];axes=(p.x,p.y,p.z)[:dimension]
  F=vector(re.search(r'F\(x,y(?:,z)?\)=(.*?)\$ and',prompt)[1],dimension);curve=vector(re.search(r'r\(t\)=(.*?)\$ for',prompt)[1],dimension);a,b=map(scalar,re.search(r't\s*\\in\s*\[(.*?),(.*?)\]',prompt).groups());assert b>a and a>=0
  dr=curve.diff(t);fr=F.subs(dict(zip(axes,curve)),simultaneous=True);dot=s.trigsimp(fr.dot(dr));answer=s.simplify(s.integrate(dot,(t,a,b)))
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==6
  coords=re.split(r',\\(?:,|quad|qquad)\s*',blocks[1].strip().rstrip('.'));assert len(coords)==dimension
  for axis,z,want in zip('xyz',coords,curve):assert z.strip().startswith(axis+'=') and same(scalar(z.split('=',1)[1]),want)
  fieldrows=rows(blocks[2]);assert len(fieldrows)>=2
  for j,row in enumerate(fieldrows):
   actual=vector(row,dimension)
   if j==0:actual=actual.subs(dict(zip(axes,curve)),simultaneous=True)
   assert all(same(v,w) for v,w in zip(actual,fr));n['field_components']+=dimension
  drows=rows(blocks[3]);assert len(drows)==3
  slots=re.findall(r'\\frac\{\\(?:text|mathrm)\{d\}([xyz])\}\{\\(?:text|mathrm)\{d\}t\}(?:\\,)?([ijk])',drows[0]);assert slots==list(zip('xyz'[:dimension],'ijk'[:dimension])),drows[0]
  actual=components(drows[1],dimension,True);assert all(same(v,w) for v,w in zip(actual,dr));n['formal_derivatives']+=dimension
  assert all(same(v,w) for v,w in zip(vector(drows[2],dimension),dr))
  dotrows=rows(blocks[4]);m=re.fullmatch(r'(.*)\\cdot\s*(.*)',dotrows[0]);assert m
  def unwrap(z):return z.replace(r'\left','').replace(r'\right','').removeprefix('(').removesuffix(')')
  left=vector(unwrap(m[1]),dimension);right=vector(unwrap(m[2]),dimension)
  assert all(same(v,w) for v,w in zip(left,fr)) and all(same(v,w) for v,w in zip(right,dr))
  products_display=outer(dotrows[1])
  if len(products_display)==2*dimension:
   for j in range(dimension):assert same(scalar(products_display[2*j]),fr[j]) and same(scalar(products_display[2*j+1]),dr[j])
  else:
   assert len(products_display)==dimension
   for j,z in enumerate(products_display):assert same(scalar(z),fr[j]*dr[j])
  for row in dotrows[1:]:assert same(scalar(row),dot),(k,rec['generation']['template'],row,dot);n['dot_stages']+=1
  last=rows(blocks[5]);lo,hi,body=integral(last[0]);assert lo==a and hi==b and body==r'F(r(t))\cdot r^{\prime}(t)'
  lo,hi,body=integral(last[1]);assert lo==a and hi==b and same(scalar(body),dot)
  if k!=17592186133831:
   assert last[2].startswith(r'\left[');body,tail=last[2][len(r'\left['):].split(r'\right]_');lo,hi,rest=bounds(tail);assert not rest
   primitive=scalar(body);assert lo==a and hi==b and same(s.diff(primitive,t),dot);n['primitives']+=1
   terms=list(s.Add.make_args(s.expand(primitive)))
   if k==17592186133828:
    endpoint=outer(last[3]);assert len(endpoint)==2
    for z,end in zip(endpoint,(b,a)):
     vals=outer(z);assert len(vals)==len(terms),(z,terms)
     expected=sorted((s.simplify(v.subs(t,end)) for v in terms),key=s.default_sort_key);actual=sorted(map(scalar,vals),key=s.default_sort_key);assert all(same(v,w) for v,w in zip(actual,expected));n['individual_endpoint_terms']+=len(vals)
   else:
    unevaluated=outer(last[3]);evaluated=outer(last[4]);assert len(unevaluated)==len(evaluated)==2*len(terms)
    expected=[]
    for term in terms:expected.extend((term.subs(t,b),-term.subs(t,a)))
    def bank_equal(xs,ys):
     ys=list(ys)
     for v in xs:
      match=next((j for j,w in enumerate(ys) if same(v,w)),None)
      if match is None:return False
      ys.pop(match)
     return not ys
    assert bank_equal([scalar(v) for v in unevaluated],expected) and bank_equal([scalar(v) for v in evaluated],expected);n['individual_endpoint_terms']+=len(evaluated)
   for row in last[3:]:assert same(scalar(row),answer)
  f=q[':question/answer-fields'][0];vals=[]
  for option in f[':answer-field/choices']:
   if k==17592186133831:
    lo,hi,body=integral(option[':answer/value']);assert lo==a and hi==b;value=scalar(body);scalarvalue=s.simplify(s.integrate(value,(t,lo,hi)));criterion=same(value,dot);vals.append(scalarvalue)
   else:value=scalar(option[':answer/value']);criterion=same(value,answer);vals.append(value)
   assert criterion==(option[':answer/id']==f[':answer-field/correct'][1]);n['choices']+=1
  assert all(not same(v,w) for j,v in enumerate(vals) for w in vals[:j])
  if k==17592186133831:
   expected=[dot,-dot,fr[0]*dr[0],fr[1]*dr[1],sum(fr)];expected=[s.integrate(v,(t,a,b)) for v in expected];assert all(any(same(v,w) for w in expected) for v in vals)
  elif k==17592186133828:
   X,Y=curve;dx,dy=dr;FP,FQ=fr;kind=rec['generation']['template'];P0,Q0=F
   if kind=='rotation':wrong=[FP*dx,FP*dx-FQ*dy,2*FP*dx+FQ*dy,2*dot]
   elif kind=='offset_circle':wrong=[FQ*dy,FP*dx+(FQ+P0/p.x)*dy,FP*dx-FQ*dy,FP+FQ]
   elif kind=='spiral':
    c=s.cancel(P0/p.x);wrong=[c*X*t*s.cos(t)-c*Y*t*s.sin(t),2*c*X*s.sin(t)+c*X*t*s.cos(t)+2*c*Y*s.cos(t)-c*Y*t*s.sin(t),c*s.sin(t)*dx+c*s.cos(t)*dy,FP*(dx-s.sin(t))+FQ*dy]
   elif kind=='arcsine':
    c=s.cancel(P0/(p.y*s.sin(p.x)));wrong=[FP,2*c*t/(1-t*t),-FP*dx,2*c*t*s.sqrt(1-t*t)]
   elif kind=='parabola':wrong=[FP*dy+FQ*dx,FP*dx+2*FQ,FQ*dy,FP*dx]
   elif kind=='log':wrong=[FP+FQ*dy,FQ*dy,-FP*dx+FQ*dy,FP*dx+FQ/2]
   else:wrong=[FP+FQ*dy,FP*dx if kind in ('polynomial','rational') else FP*dx+FQ,FQ*dy,FP*dx-FQ*dy]
   expected=[answer]+[s.integrate(s.trigsimp(z),(t,a,b)) for z in wrong];assert all(any(same(v,w) for w in expected) for v in vals)
  else:
   products=[s.expand(v*w) for v,w in zip(fr,dr)];kind=rec['generation']['template']
   integrate=lambda e:s.simplify(s.integrate(s.simplify(e),(t,a,b)))
   if kind in ('constant_affine','diagonal_power'):expected=[answer,-answer,*[integrate(dot-z) for z in products]]
   elif kind in ('product','mixed_polynomial','exp_cancel_xy','exp_cancel_yz'):expected=[answer,*[integrate(dot-z) for z in products],integrate(sum(fr))]
   elif kind=='trig_cancel':
    A2=s.cancel(curve[0]**2/s.sin(t)**2);expected=[answer,-answer,2*answer,A2*(s.sin(b)-s.sin(a))/2,-A2*s.cos(2*b)/4]
   elif kind=='radical_power':
    radical=integrate(products[0]+products[1]);zterm=integrate(products[2]);expected=[answer,zterm,radical,radical+zterm/2,-answer]
   elif kind=='quotient_exp':
    C=s.cancel(curve[2]/t);kr=s.cancel(dr[0]/curve[0]);lr=s.cancel(dr[1]/curve[1]);expected=[answer,C*(b-a),integrate(products[0]+products[1]),integrate(C*kr*t*s.exp(-kr*t)+products[1]+C),integrate(C*kr*t*s.exp(-kr*t)+C*lr*t*s.exp(-lr*t)+C)]
   elif kind=='helix_root':
    C=s.cancel(curve[2]/s.sqrt(t));expected=[answer,0,2*answer,C*C*(s.sqrt(b)-s.sqrt(a)),C*C*(b*b-a*a)/4]
   else:raise AssertionError(kind)
   assert all(any(same(v,w) for w in expected) for v in vals)
  n['records']+=1
 report=dict(status='passed',kp_id=k,source=src,readback=n,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)

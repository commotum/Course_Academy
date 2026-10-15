"""Parent definite log readback: actual bounds, domains, primitives and fragments."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186100818;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest();G=load('root_deflog_gen',D.with_suffix('.py'));A=load('root_deflog_scalar',R/'based-log-integral-readback.py');E=A.E;B=load('root_deflog_def',R/'definite-elementary-readback.py');H=load('root_deflog_measure',R/'inverse-substitution-readback.py');x,u=A.x,A.u;scalar=A.scalar;B.scalar=scalar
def clean(raw):return B.clean(H.measure_text(raw)).replace(r'\displaystyle','').replace(r'\big','').replace('[','(').replace(']',')')
def integral(raw):
 text=clean(raw);at=text.index(r'\int');i=at+4
 while text[i].isspace():i+=1
 assert text[i]=='_';lo,i=B.group(text,i+1);assert text[i]=='^';hi,i=B.group(text,i+1);m=re.search(E.DIFF,text[i:]);assert m
 body=text[i:i+m.start()].strip();body=body[:-len(r'\cdot')]if body.endswith(r'\cdot')else body;outside=text[:at]+'(i)'+text[i+m.end():];value=scalar(outside);symbol=E.P.locals_['i'];coef=s.expand(value).coeff(symbol);assert s.simplify(value-coef*symbol)==0 and not coef.has(x,u);return coef*scalar(body),E.P.locals_[m[1]],scalar(lo),scalar(hi)
def bar(raw):
 text=clean(raw);m=re.search(r'\|_',text);assert m,text;before=text[:m.start()];after=text[m.end():];lo,j=B.group(after,0);assert after[j]=='^';hi,j=B.group(after,j+1);suffix=after[j:];assert re.fullmatch(r'\)*',suffix);before+=suffix
 before+='}'*max(0,before.count('{')-before.count('}'))
 return scalar(before),scalar(lo),scalar(hi)
def signed_pair(raw):
 text=clean(raw);depth=0
 for i,c in enumerate(text):
  if c in '+-'and i>0 and depth==0 and text[i-1]not in '+-*/^':return scalar(text[:i]),(1 if c=='+'else-1)*scalar(text[i+1:])
  depth+=(c in '({')-(c in ')}')
 depth=0
 for i,c in enumerate(text):
  if c=='('and depth==0 and text.endswith(')'):
   pair=signed_pair(text[i+1:-1])
   if pair is not None:
    prefix=text[:i].strip();prefix=prefix[:-len(r'\cdot')]if prefix.endswith(r'\cdot')else prefix;coef=scalar(prefix)if prefix not in('','-')else s.Integer(-1 if prefix=='-'else 1);return tuple(coef*z for z in pair)
  depth+=(c in '({')-(c in ')}')
 return None
def terms(sol):
 for block in B.blocks(sol):
  if r'\int'not in block and r'\begin{aligned}'not in block:continue
  for row in re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','').split(r'\\'):
   for term in row.split('='):
    if term.strip():yield term.strip().replace(r'\,','').rstrip('.,?')
@lru_cache(maxsize=20000)
def equal(a,b):return s.simplify(s.expand_log(a-b))==0
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
N=dict(records=0,source_banks=0,source_values=0,source_keys=0,differentials=0,formal_inputs=0,primitive_stages=0,bounds=0,signed_endpoint_components=0,values=0,pairs=0,fragment_contexts=0,improper_endpoints=0,descending_intervals=0);tasks={l:set()for l in('easy','moderate','hard')}
def check(rec,sid=None):
 q=rec['question'];sol=q[':question/worked-solution'];given=next(b for b in B.blocks(q[':question/problem'])if r'\int'in b).split('=')[0].replace(r'\,','').strip().rstrip('.,?');F,v,L,U=integral(given);assert v==x and L>0 and U>0 and L!=U;N['descending_intervals']+=bool(L>U)
 V=scalar(re.search(r'\$u\s*=(.*?)\$',sol)[1]);log=next(z for z in V.atoms(s.log)if z.args[0].has(x));arg=log.args[0];poly=s.Poly(arg,x);assert len(poly.terms())==1;n=poly.degree();a=poly.LC();base_log=s.cancel(log/V);assert n>0 and a>0 and base_log>0;der=s.diff(V,x);assert equal(der,n/(x*base_log));ul,uh=map(lambda z:s.simplify(s.expand_log(z)),[V.subs(x,L),V.subs(x,U)]);assert min(ul,uh)>=0
 w=s.Symbol('root_definite_log_coordinate',positive=True);replacement=s.exp((w*base_log-s.log(a))/n)
 @lru_cache(maxsize=3000)
 def eqreal(a,b):return s.simplify(s.expand_log((a-b).subs(x,replacement)))==0
 kernel=s.simplify(s.expand_log((F/der).subs(x,replacement)));p=next((p for p in[-2,-1,s.Rational(-1,2),s.Rational(1,2),1]if not s.cancel(kernel/w**p).has(w)),None);assert p is not None;co=s.cancel(kernel/w**p);assert co>0
 if p<=-1:assert min(ul,uh)>0
 prim=co*s.log(u)if p==-1 else co*u**(p+1)/(p+1);expected=s.simplify(prim.subs(u,uh)-prim.subs(u,ul))
 if min(ul,uh)==0 and p<0:assert p>-1 and s.limit(prim,u,0,dir='+').is_finite;N['improper_endpoints']+=1
 dm=next(b for b in B.blocks(sol)if r'\frac{\text{d}u}{\text{d}x}'in b);left,right=re.split(r'⟹|\\(?:Longrightarrow|Rightarrow)',dm)
 for term in left.split('=')[1:]:assert eqreal(scalar(term.replace(r'\,','')),der),(V,dm,term,der);N['differentials']+=1
 def measure(raw):return scalar(re.sub(E.DIFF,lambda m:'(j)'if m[1]=='u'else'(k)',H.measure_text(raw))).subs({E.P.locals_['j']:der,E.P.locals_['k']:1})
 dl,dr=right.rstrip('.').split('=');assert eqreal(measure(dl),measure(dr));N['differentials']+=1
 table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M);assert[t[0]for t in table]==['x','u'];assert all(equal(scalar(z),target)for z,target in zip(table[0][1:]+table[1][1:],[L,U,ul,uh]));N['bounds']+=4
 seen=False;signed=False
 for term in terms(sol):
  if r'\int'in term:
   body,var,lo,hi=integral(term);assert var in(x,u);assert equal(lo,L if var==x else ul)and equal(hi,U if var==x else uh);effective=body if var==x else body.subs(u,V)*der;assert eqreal(effective,F),('actual definite log operand',term,effective,F);N['formal_inputs']+=1;N['bounds']+=2
  elif '|_'in clean(term):
   actual,lo,hi=bar(term);assert equal(lo,ul)and equal(hi,uh)and equal(actual,prim);assert eqreal(E.derivative(actual,x,V),F);N['primitive_stages']+=1;N['bounds']+=2;seen=True
  else:
   assert seen and equal(scalar(term),expected),('actual endpoint/collected stage',term,expected)
   pair=signed_pair(term)
   if pair is not None and not signed:
    target=(prim.subs(u,uh),-prim.subs(u,ul));assert(equal(pair[0],target[0])and equal(pair[1],target[1]))or(equal(pair[0],target[1])and equal(pair[1],target[0])),('independent endpoint components',term,pair,target);N['signed_endpoint_components']+=2;signed=True
 assert seen and signed
 fs=q[':question/answer-fields'];assert len(fs)==1;f=fs[0];vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];key=f[':answer-field/correct'][1];correct=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==key)
 if f[':answer-field/type'].endswith('/blank'):
  def response(value):return scalar(q[':question/problem'].split('=',1)[1].replace('$','').replace('{{'+f[':answer-field/key']+'}}','('+value+')'))
  assert all(equal(response(a[':answer/value']),expected)for a in f[':answer-field/choices']);N['fragment_contexts']+=1
 else:
  assert[a[':answer/id']for a,val in zip(f[':answer-field/choices'],vals)if equal(val,expected)]==[key]
  for i,val in enumerate(vals):
   for z in vals[:i]:assert not equal(val,z);N['pairs']+=1
 if sid:
  of=olds[sid][':question/answer-fields'][0];ov=[scalar(a[':answer/value'])for a in of[':answer-field/choices']];remaining=vals[:];assert len(ov)==len(vals)
  for val in ov:
   i=next(i for i,z in enumerate(remaining)if equal(val,z));remaining.pop(i)
  if ':answer-field/correct'in of:assert equal(scalar(of[':answer-field/correct'][':answer/value']),scalar(correct));N['source_keys']+=1
  N['source_banks']+=1;N['source_values']+=len(vals)
 N['values']+=len(vals);N['records']+=1;tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(s.expand_log(F.subs(x,s.Symbol('positive_original_x',positive=True)))),str(L),str(U)))
for sid in olds:
 print('Source',sid,flush=True);check(G.generate(G.CONFIG[sid],template=sid,parameters=G.original(sid)),sid)
 check(G.generate(G.CONFIG[sid],template=sid,parameters={'coefficient_num':2,'coefficient_den':3,'x_scale':4}))
for level in tasks:
 for r in G.generate_batch(level,714,12):check(r)
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
result=dict(status='passed',script_sha256=SCRIPT_SHA,source_and_readback=N,sampled_actual_tasks={l:len(t)for l,t in tasks.items()},domain_proof='Independently read monomial logargument, positive base/argument and actual interval orientation. Increasing u, nonnegative u throughout sorted interval; reciprocals stay strictly positive, sqrt endpoint singularities proved integrable by finite primitive limit. Descending source integrals retained. Every formal operand/bounds, primitivebar and separate signed endpoint and supplied blank suffix checked.',scope='Same observed definite natural/generalbase logarithm substitution and unit-power/log primitive, independent external rational coefficient and positive x-rescaling; normalized endpoint roles fixed, no extra skills.',native_limitations='136canonical accepted480rejected0unresolved, including32genuine normal blank equivalent-entry false rejections explicitly retained. Parentgeneric54accepted156rejected0gaps; no pruning/engine edits.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

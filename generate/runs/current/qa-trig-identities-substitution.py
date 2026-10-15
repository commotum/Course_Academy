"""Parent actual nonlinear substitution operands, domain holes and endpoint terms."""
import sys,json,hashlib,importlib.util,re,copy
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064227;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_ident_sub_gen',D.with_suffix('.py'));E=load('root_ident_sub_elem',R/'elementary-integral-readback.py');B=load('root_ident_sub_def',R/'definite-elementary-readback.py');T=load('root_ident_sub_trig',R/'trig-primitive-readback.py');H=load('root_ident_sub_inverse',R/'inverse-substitution-readback.py');x,u=E.x,E.u
def scalar(raw):
 raw=re.sub(r'\\(?:operatorname|text)\{(sin|cos|tan|sec|cot|csc)\}',lambda m:'\\'+m[1]+' ',raw)
 raw=re.sub(r'\{(sin|cos|tan|sec|cot|csc)\}',lambda m:'\\'+m[1]+' ',raw)
 raw=re.sub(r'(?<![A-Za-z\\])(sin|cos|tan|sec|cot|csc)(?![A-Za-z])',lambda m:'\\'+m[1]+' ',raw)
 return E.scalar(raw)
B.scalar=scalar
base_derivative=E.derivative
def real_derivative(value,var,inner=None):
 # d log(|g|^r)=r*g'/g on each actual real g!=0 component.
 value=value.replace(lambda z:z.func==s.log and z.args[0].is_Pow and z.args[0].base.func==s.Abs,lambda z:z.args[0].exp*s.log(z.args[0].base))
 return base_derivative(value,var,inner)
E.derivative=real_derivative
def zero(a,b=0):
 delta=s.cancel(a-b)
 if delta==0:return True
 try:return T.zero(delta)
 except s.PolynomialError:return s.simplify(s.trigsimp(delta))==0
def equal(a,b):return s.simplify(s.expand_log(a-b))==0
def clean(raw):return B.clean(H.measure_text(raw)).replace(r'\big','')
def integral(raw):
 text=clean(raw);at=text.index(r'\int');i=at+4
 while text[i].isspace():i+=1
 assert text[i]=='_';lo,i=B.group(text,i+1);assert text[i]=='^';hi,i=B.group(text,i+1)
 m=re.search(E.DIFF,text[i:]);assert m;body=scalar(text[i:i+m.start()]);outside=text[:at]+'(i)'+text[i+m.end():];value=scalar(outside);symbol=E.P.locals_['i'];coef=s.expand(value).coeff(symbol);assert equal(value,coef*symbol)and not coef.has(x,u)
 return s.Integer(1),coef*body,E.P.locals_[m[1]],scalar(lo),scalar(hi),''
def parts(sol):
 for block in B.blocks(sol):
  if r'\begin{aligned}'not in block:continue
  for row in re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','').split(r'\\'):
   for term in row.split('='):
    if term.strip():yield term
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
    prefix=text[:i].strip();coeff=scalar(prefix)if prefix not in('','-')else s.Integer(-1 if prefix=='-'else 1);return tuple(coeff*a for a in pair)
  depth+=(c in '({')-(c in ')}')
 return None
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
N=dict(records=0,source_banks=0,source_values=0,source_keys=0,formal_inputs=0,primitive_stages=0,differentials=0,bounds=0,individual_endpoint_components=0,values=0,pairs=0);tasks={l:set()for l in G.LEVELS}
def check(rec,sid=None):
 q=rec['question'];sol=q[':question/worked-solution'];given=clean(next(b for b in B.blocks(q[':question/problem'])if r'\int'in b).split('=')[0].strip().rstrip('.,?'));definite=bool(re.search(r'\\int\s*_',given))
 if definite:c,F,v,L,U,end=integral(given);F=c*F;assert not end and v==x and L<U
 else:F,ops=E.side(given,x);assert len(ops)==1;L=U=None
 sm=re.search(r'\$u=(.*?)\$',sol);assert sm;V=scalar(sm[1]);der=s.diff(V,x)
 dm=next((b for b in B.blocks(sol)if r'\frac{\text{d}u}{\text{d}x}'in b),None)
 if dm:
  left,right=re.split(r'⟹|\\(?:Longrightarrow|Rightarrow)',dm);assert zero(scalar(left.split('=',1)[1]),der)
  def measure(raw):
   raw=raw.strip().rstrip('.').replace(r'\,','');raw=re.sub(E.DIFF,lambda m:'(j)'if m[1]=='u'else'(k)',raw);val=scalar(raw);j,k=E.P.locals_['j'],E.P.locals_['k'];assert s.diff(val,j,2)==0 and s.diff(val,k,2)==0;return val.subs({j:der,k:1})
  a,b=right.split('=');assert zero(measure(a),measure(b));N['differentials']+=2
 else:
  dm=re.search(r'\$(\\text\{d\}x=.*?)\$',sol);assert dm
  a,b=dm[1].rstrip('.').split('=');j,k=E.P.locals_['j'],E.P.locals_['k']
  measure=lambda raw:scalar(re.sub(E.DIFF,lambda m:'(j)'if m[1]=='u'else'(k)',raw)).subs({j:der,k:1})
  assert zero(measure(a),measure(b));N['differentials']+=1
 terms=list(parts(sol));prim=None;expected=None;ul=uh=None
 if definite:
  table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M);assert[t[0]for t in table]==['x','u'];ul,uh=map(scalar,table[1][1:]);assert all(equal(scalar(a),b)for a,b in zip(table[0][1:]+table[1][1:],[L,U,V.subs(x,L),V.subs(x,U)]));N['bounds']+=4
  # Every actual trig angle lies in one positive sin/cos component. This also
  # certifies square-root/log branches and the original uncancelled poles.
  angles={a.args[0]for a in F.atoms(s.sin,s.cos,s.tan,s.cot,s.sec,s.csc)}
  for arg in angles:assert 0<=arg.subs(x,L)<arg.subs(x,U)<=s.pi/2
  # Inspect original bound primitive before any endpoint simplification.
  token=next(clean(t)for t in terms if '|_'in clean(t));_,info=B.value(token);assert info[0]=='bar';_,prim,a,b=info;assert equal(a,ul)and equal(b,uh)and zero(E.derivative(prim,x,V),F);expected=s.simplify(prim.subs(u,uh)-prim.subs(u,ul));N['bounds']+=2
 endpoint_seen=False
 for term in terms:
  text=clean(term)
  if not definite:
   actual,ops=E.side(text,x,V);assert zero(actual,F),('operative integral/primitive',term,actual,F);N['formal_inputs']+=len(ops);N['primitive_stages']+=not bool(ops)
  elif r'\int'in text:
   c,body,v,a,b,end=integral(text);assert not end and v in(x,u);assert equal(a,L if v==x else ul)and equal(b,U if v==x else uh);effective=c*body if v==x else c*body.subs(u,V)*der;assert zero(effective,F),('operative definite integral',term,effective,F);N['formal_inputs']+=1;N['bounds']+=2
  elif '|_'in text:N['primitive_stages']+=1
  else:
   assert equal(scalar(text),expected),('definite value',term,expected)
   pair=signed_pair(text)
   if pair is not None and not endpoint_seen:
    target=(prim.subs(u,uh),-prim.subs(u,ul));assert(equal(pair[0],target[0])and equal(pair[1],target[1]))or(equal(pair[0],target[1])and equal(pair[1],target[0])),('independent signed endpoints',term,pair,target);N['individual_endpoint_components']+=2;endpoint_seen=True
 if definite:assert endpoint_seen
 for f in q[':question/answer-fields']:
  vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];key=f[':answer-field/correct'][1];same=equal if definite else lambda a,b:zero(E.derivative(a-b,x));good=[equal(v,expected)if definite else zero(E.derivative(v,x),F)for v in vals];correct_ids=[a[':answer/id']for a,ok in zip(f[':answer-field/choices'],good)if ok];assert key in correct_ids
  if f[':answer-field/type'].endswith('/radio'):
   assert correct_ids==[key]
   for i,v in enumerate(vals):
    for w in vals[:i]:assert not same(v,w);N['pairs']+=1
  else:assert all(good)
  if sid:
   of=olds[sid][':question/answer-fields'][0];ov=[scalar(a[':answer/value'])for a in of[':answer-field/choices']];remaining=vals[:];assert len(ov)==len(vals)
   for v in ov:
    i=next(i for i,w in enumerate(remaining)if same(v,w));remaining.pop(i)
   oldcorrect=scalar(of[':answer-field/correct'][':answer/value']);newcorrect=next(v for a,v in zip(f[':answer-field/choices'],vals)if a[':answer/id']==key);assert same(oldcorrect,newcorrect);N['source_banks']+=1;N['source_values']+=len(vals);N['source_keys']+=1
  N['values']+=len(vals)
 N['records']+=1;tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(s.trigsimp(F.rewrite(s.sin))),str(L),str(U)))
for sid,o in olds.items():
 check(G.generate(G.PROFILES[sid]['difficulty'],template=sid,parameters={'a':1,'k':1}),sid)
 for a,k in [(2,1),(1,-2),(6,6),(6,-6)]:check(G.generate(G.PROFILES[sid]['difficulty'],template=sid,parameters={'a':a,'k':k}))
for l in tasks:
 for r in G.batch(l,18,792):check(r)
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_tasks={l:len(t)for l,t in tasks.items()},scope='Full source trig identities and linear/nonlinear substitution, exact source ordered operands/differential relations, same source powers/logarithms/radicals and definite endpoint roles. Independent positive argument frequency and signed external numerator slots; no added operators/branches.',native_limitations='See frozen native evidence for genuine normal blank equivalent-entry failures; canonical and incorrect entries independently checked; no valid-math pruning or engine edits.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

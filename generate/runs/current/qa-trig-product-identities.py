"""Parent readback of identity reductions, primitives and signed endpoint values."""
import sys,json,hashlib,importlib.util,re,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064225;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_product_ids_gen',D.with_suffix('.py'));E=load('root_product_elem',R/'elementary-integral-readback.py');B=load('root_product_definite',R/'definite-elementary-readback.py');T=load('root_product_trig',R/'trig-primitive-readback.py');I=load('root_product_inverse',R/'inverse-substitution-readback.py');x,u=E.x,E.u;scalar=E.scalar
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
N=dict(records=0,source_banks=0,source_values=0,source_keys=0,identities=0,formal_inputs=0,primitive_stages=0,individual_endpoint_components=0,bounds=0,differentials=0,values=0,pairs=0);tasks={l:set()for l in G.SUPPORTED_LEVELS}
def zero(a,b=0):return T.zero(a-b)
def eq(a,b):return s.simplify(a-b)==0
def clean(raw):return B.clean(I.measure_text(raw)).replace(r'\big','')
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
    prefix=text[:i].strip();prefix=prefix[:-len(r'\cdot')]if prefix.endswith(r'\cdot')else prefix;co=scalar(prefix)if prefix not in('','-')else s.Integer(-1 if prefix=='-'else 1);return tuple(co*z for z in pair)
  depth+=(c in '({')-(c in ')}')
 return None
def stages(text):
 for block in B.blocks(text):
  if r'\begin{aligned}'not in block:continue
  for row in re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','').split(r'\\'):
   for term in row.split('='):
    if term.strip():yield term
def prose(text):
 text=re.sub(r'\$\$.*?\$\$',' [calculation] ',text,flags=re.S);text=re.sub(r'\$.*?\$',' [math] ',text,flags=re.S);text=re.sub(r'^\|.*$','',text,flags=re.M);return re.sub(r'\s+',' ',text).strip()
def check(rec,sid=None):
 q=rec['question'];sol=q[':question/worked-solution'];given=clean(next(b for b in B.blocks(q[':question/problem'])if r'\int'in b).rstrip('= .'));definite=r'\int_'in given
 if definite:
  c,F,var,lo,hi,end=B.integral(given);assert not end and var==x;F=c*F
 else:F,var,_=E.integrand(given);lo=hi=None;assert var==x
 sub=re.search(r'\$u=(.*?)\$',sol);U=scalar(sub[1])if sub else None;k=s.diff(U,x)if U is not None else s.Integer(1)
 if U is not None:
  assert not k.has(x)and k>0 and eq(U,k*x)
  dm=re.search(r'\$\\text\{d\}x=(.*?)\\text\{d\}u\.\$',sol);assert dm and eq(scalar(dm[1])*k,1);N['differentials']+=1
  table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M);assert[t[0]for t in table]==['x','u'];assert all(eq(scalar(a),b)for a,b in zip(table[0][1:]+table[1][1:],[lo,hi,U.subs(x,lo),U.subs(x,hi)]));N['bounds']+=4
 for b in B.blocks(sol):
  if '='not in b or r'\int'in b or r'\begin'in b or r'\text{d}'in b or b.strip().startswith('u='):continue
  a,z=b.split('=',1);assert zero(scalar(a),scalar(z));N['identities']+=1
 terms=list(stages(sol));prim=None;expected=None;bounds=None
 if definite:
  # Read the displayed primitive independently and check its derivative before
  # using its values to assess every endpoint and response.
  token=next(clean(t)for t in terms if '|_'in clean(t));i=token.index('|_');suffix=token[i+2:];a,j=B.group(suffix,0);assert suffix[j]=='^';b,j=B.group(suffix,j+1);assert not suffix[j:];prim=scalar(token[:i]);a,b=scalar(a),scalar(b);var=u if U is not None else x;bounds=(a,b)
  assert eq(a,U.subs(x,lo)if U is not None else lo)and eq(b,U.subs(x,hi)if U is not None else hi);assert zero(E.derivative(prim,x,U),F);expected=s.simplify(prim.subs(var,b)-prim.subs(var,a));N['bounds']+=2
  # The actual argument interval stays within a pole-free cos component;
  # cancellation in the simplified integrand does not erase original holes.
  args={f.args[0]for f in F.atoms(s.sin,s.cos,s.tan,s.cot,s.sec,s.csc)};assert len(args)==1;arg=next(iter(args));assert -s.pi/2<arg.subs(x,lo)<arg.subs(x,hi)<s.pi/2
 for term in terms:
  text=clean(term)
  if not definite:
   derivative,ops=E.side(text,x,U);assert zero(derivative,F),('operative integral/primitive',term,derivative,F);N['formal_inputs']+=len(ops);N['primitive_stages']+=not bool(ops)
  elif r'\int'in text:
   c,body,v,a,b,end=B.integral(text);assert not end and v in(x,u);assert eq(a,lo if v==x else U.subs(x,lo))and eq(b,hi if v==x else U.subs(x,hi));effective=c*body if v==x else c*body.subs(u,U)*k;assert zero(effective,F),('actual formal operand',term,effective,F);N['formal_inputs']+=1;N['bounds']+=2
  elif '|_'in text:N['primitive_stages']+=1
  else:
   assert eq(scalar(text),expected),('endpoint/collected value',term,expected)
   pair=signed_pair(text)
   if pair is not None and ('('in text or re.search(r'\\(?:sin|cos|tan|sec|csc|cot)',text)):
    target=(prim.subs(var,bounds[1]),-prim.subs(var,bounds[0]));assert(eq(pair[0],target[0])and eq(pair[1],target[1]))or(eq(pair[0],target[1])and eq(pair[1],target[0])),('actual signed endpoint contributions',term,pair,target);N['individual_endpoint_components']+=2
 f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];correct=f[':answer-field/correct'][1];same=(lambda a,b:zero(s.diff(a-b,x)))if not definite else eq;good=[eq(v,expected)if definite else zero(s.diff(v,x),F)for v in vals];assert[a[':answer/id']for a,ok in zip(f[':answer-field/choices'],good)if ok]==[correct]
 for i,v in enumerate(vals):
  for w in vals[:i]:assert not same(v,w);N['pairs']+=1
 N['values']+=len(vals)
 if sid:
  old=olds[sid];of=old[':question/answer-fields'][0];ov=[scalar(a[':answer/value'])for a in of[':answer-field/choices']];assert len(ov)==len(vals)and all(sum(same(v,w)for w in vals)==1 for v in ov);assert same(scalar(of[':answer-field/correct'][':answer/value']),next(v for a,v in zip(f[':answer-field/choices'],vals)if a[':answer/id']==correct));assert prose(old[':question/worked-solution'])==prose(sol);N['source_banks']+=1;N['source_values']+=len(ov);N['source_keys']+=1
 N['records']+=1;tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(s.trigsimp(F.rewrite(s.sin))),str(lo),str(hi)))
for sid,o in olds.items():
 p=G.PROFILES[sid][1];original=G.generate(G.level(sid),template=sid,parameters=p);check(original,sid)
 import copy
 raw=copy.deepcopy(original);raw['question'][':question/problem']=G.fmt.normalize_prose(o[':question/problem']);raw['question'][':question/worked-solution']=G.fmt.normalize_prose(o[':question/worked-solution']);check(raw)
 for seed in range(4):check(G.generate(G.level(sid),seed,template=sid))
 if 'l'in p:
  for l,h in itertools.combinations(G.ANGLES,2):
   try:r=G.generate(G.level(sid),template=sid,parameters=dict(p,l=l,h=h))
   except ValueError as error:assert 'collides'in str(error);continue
   check(r)
for l in tasks:
 for r in G.batch(l,20,774):check(r)
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_tasks={l:len(t)for l,t in tasks.items()},scope='Observed product-distribution and reciprocal/quotient trig identities, direct known primitives; existing source linear substitutions and changed definite bounds retained. All14profiles cover6E5M3H, no authored new operation; independently varied eligible endpoint pairs in same pole-free component and small coefficients.',native_limitations='45accepted144rejected0unresolved, includes15 mathematically valid normal blank uncollected-equivalent false rejections preserved as qualified local grader limitations. Generic54accepted94rejected0gaps. No pruning/no engine edits.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

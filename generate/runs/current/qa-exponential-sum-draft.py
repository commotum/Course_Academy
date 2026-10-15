"""Root actual termwise operands, both real components, source banks and C contract."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ID=17592186064177;D=R.parents[2]/f'generate/scratch/{ID}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_expsum_gen',D.with_suffix('.py'));P=load('root_expsum_math',R/'elementary-integral-readback.py');x,C=P.x,P.C
scalar=P.scalar
@lru_cache(maxsize=20000)
def eq(a,b):
 d=a-b
 if d==0:return True
 substitutions={}
 for term in d.atoms(s.exp):
  exponent=term.args[0];slope=s.diff(exponent,x);offset=s.expand(exponent-slope*x);assert slope.is_Rational and not offset.has(x)
  substitutions[term]=s.exp(offset)*s.Symbol('root_E',positive=True)**slope
 for term in d.atoms(s.Pow):
  base,exponent=term.args
  if base.is_Rational and base>0 and exponent.has(x):
   slope=s.diff(exponent,x);offset=s.expand(exponent-slope*x);assert slope.is_Rational and not offset.has(x)
   f=s.factorint(base.p);g=s.factorint(base.q);factors=set(f)|set(g);substitutions[term]=base**offset*s.prod(s.Symbol('root_P'+str(p),positive=True)**(slope*(f.get(p,0)-g.get(p,0)))for p in factors)
 d=s.expand_log(d.xreplace(substitutions));w=s.Symbol('root_positive_x',positive=True)
 return all(s.cancel(s.expand_log(d.subs(x,sign*w)))==0 for sign in(-1,1))

source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{ID}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};N=dict(raw=0,source_banks=0,source_values=0,source_keys=0,records=0,formal_operands=0,term_checks=0,primitive_stages=0,values=0,pairs=0,definition_bindings=0,blank_external_C=0);tasks={l:set()for l in G.SUPPORTED_LEVELS}
def side(raw):
 text=P.fraction_measure(raw.strip().rstrip('.,'));formal=[]
 while r'\int'in text:
  at=text.index(r'\int');operand,var,match=P.integrand(text[at:]);assert var==x and len(formal)<4;token=('i','j','k','z')[len(formal)];symbol=P.P.locals_[token];formal.append((symbol,operand));text=text[:at]+'('+token+')'+text[at+match.end():]
 value=scalar(text);rest=value;actual=s.Integer(0);ops=[]
 for symbol,operand in formal:
  coeff=s.expand(value).coeff(symbol);assert not coeff.has(x,*[t for t,_ in formal]);actual+=coeff*operand;rest-=coeff*symbol;ops.append((operand,x,coeff))
 rest=s.expand(rest);assert not rest.has(*[t for t,_ in formal]);return actual+P.derivative(rest,x),ops

def check(r,sid=None):
 q,m=r['question'],r['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];defs={name:raw for name,raw in re.findall(r'\b([fg])\(x\)=([^$]+)',prompt)}
 for name,raw in defs.items():scalar(raw);N['definition_bindings']+=1
 def resolved(t):
  for name,raw in defs.items():t=t.replace(name+'(x)','('+raw+')')
  return t
 F,var=P.prompt(resolved(prompt));assert var==x;f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];derivatives=[P.derivative(v,x)for v in values];assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],derivatives)if eq(v,F)]==[f[':answer-field/correct'][1]]
 for i,v in enumerate(derivatives):
  for w in derivatives[:i]:assert not eq(v,w);N['pairs']+=1
 if f[':answer-field/type'].endswith('/blank'):
  assert len(values)==1
  if '+C'in prompt.replace(r'\,','').replace(' ',''):assert not values[0].has(C);N['blank_external_C']+=1
  else:assert values[0].coeff(C)==1
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==1;body=re.sub(r'\\(?:begin|end)\{aligned\}','',resolved(blocks[0]));last=None
 for row in body.split(r'\\'):
  for part in row.replace('&','').split('='):
   if not part.strip():continue
   value,ops=side(part);assert eq(value,F),('actual sum integral/primitive stage',m['template'],part,F,value)
   if ops:
    pieces=[]
    for operand,var,coef in ops:
     assert var==x;pieces.extend(s.Add.make_args(s.expand(coef*operand)));N['formal_operands']+=1
    target=list(s.Add.make_args(s.expand(F)));assert len(pieces)==len(target)
    for piece in pieces:
     hits=[i for i,z in enumerate(target)if eq(z,piece)];assert len(hits)==1,('individual termwise operand',piece,target);target.pop(hits[0]);N['term_checks']+=1
   else:
    last=scalar(part);assert last.coeff(C)in(0,1);N['primitive_stages']+=1
 assert last is not None and last.coeff(C)==1
 if sid:
  o=olds[sid]
  for of in o.get(':question/answer-fields',[]):
   ov=[scalar(a[':answer/value'])for a in of[':answer-field/choices']];assert len(ov)==len(values)and all(sum(eq(v,w)for w in values)==1 for v in ov);N['source_banks']+=1;N['source_values']+=len(values)
   if ':answer-field/correct'in of:assert eq(P.derivative(scalar(of[':answer-field/correct'][':answer/value']),x),F);N['source_keys']+=1
 N['records']+=1;N['values']+=len(values);tasks[q[':question/difficulty'].split('/')[-1]].add(s.srepr(s.expand(F)))
raws=json.load(open(D/'raw-replay.json'))
for sid,o in olds.items():
 raw=next(q for q in raws if q['source_id']==sid);assert raw['record']==o;N['raw']+=1
 if sid in('q-31311','q-51102','q-31261','q-167332','q-167786','q-166079'):assert raw['raw_generation_eligible']is False
 level,base=G.SPECS[sid];check(G.generate(level,template=sid,parameters={'base':base}if base else{}),sid)
for i,row in enumerate(json.load(open(D/'engine-input.json'))):
 if i%50==0:print('Root exponential-sum record',i,flush=True)
 check(row['record'])
for level in G.SUPPORTED_LEVELS:
 for seed in range(24):check(G.generate(level,seed))
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_integrands={l:len(t)for l,t in tasks.items()},scope='Termwise sums of known e^x/general-base exponentials and observed polynomial/constant/reciprocal terms; no linear exponent or new substitution skills. Authored absent hard uses four terms at fixed same-method workload. Both real signs checked for log absolute values.',source_repairs='Two unrated missing-key/solution records, one fieldless source, three undefined-f/g prompts are raw-ineligible. Normal authored completions give explicit functions and respect supplied external +C versus whole primitive blank.',native_limitations='Private220accepted775rejected0gaps plus generic54accepted188rejected0gaps; true uncollected primitive equivalents checked, constant shifts never wrong probes.',database_writes=0);(R/f'qa/{ID}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

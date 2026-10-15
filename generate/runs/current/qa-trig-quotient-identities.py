"""Parent rendered quotient integrals and author-calibrated definite two-term banks."""
import sys,json,hashlib,importlib.util,re,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064226;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_quotient_ids_gen',D.with_suffix('.py'));E=load('root_quotient_ids_elem',R/'elementary-integral-readback.py');B=load('root_quotient_ids_def',R/'definite-elementary-readback.py');T=load('root_quotient_ids_trig',R/'trig-primitive-readback.py');H=load('root_quotient_ids_inverse',R/'inverse-substitution-readback.py');x,u=E.x,E.u
def clean(raw):
 raw=re.sub(r'(?<![A-Za-z])\{(sin|cos|tan|sec|cot|csc)\}',lambda m:'\\'+m[1]+' ',raw)
 text=B.clean(H.measure_text(raw)).replace(r'\big','').replace('[','(').replace(']',')')
 return re.sub(r'(?<![A-Za-z\\])(sin|cos|tan|sec|cot|csc)(?=\\|\s|\()',lambda m:'\\'+m[1],text)
def scalar(raw):return E.scalar(clean(raw))
def zero(a,b=0):return T.zero(a-b)
def equal(a,b):return s.simplify(a-b)==0
def integral(raw):
 text=clean(raw);at=text.index(r'\int');i=at+4
 while text[i].isspace():i+=1
 lo=hi=None
 if text[i]=='_':lo,i=B.group(text,i+1);assert text[i]=='^';hi,i=B.group(text,i+1);lo,hi=scalar(lo),scalar(hi)
 m=re.search(E.DIFF,text[i:]);assert m;text_body=text[i:i+m.start()];var=E.P.locals_[m[1]];end=i+m.end();outside=text[:at]+'(i)'+text[end:];v=scalar(outside);symbol=E.P.locals_['i'];coef=s.expand(v).coeff(symbol);assert equal(v,coef*symbol)and not coef.has(x,u);body=scalar(text_body);return coef*body,var,lo,hi
def bar(raw):
 text=clean(raw);m=re.search(r'\|_',text);assert m,text;before=text[:m.start()];after=text[m.end():];a,i=B.group(after,0);assert after[i]=='^';b,i=B.group(after,i+1);suffix=after[i:];assert re.fullmatch(r'\)*',suffix);before+=suffix
 if before.startswith('{')and before.count('{')>before.count('}'):before=before[1:]
 prim=scalar(before);return prim,scalar(a),scalar(b)
def parts(sol):
 for block in B.blocks(sol):
  if r'\int'not in block and r'\begin{aligned}'not in block:continue
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
    prefix=text[:i].strip();prefix=prefix[:-len(r'\cdot')]if prefix.endswith(r'\cdot')else prefix;coef=scalar(prefix)if prefix not in('','-')else s.Integer(-1 if prefix=='-'else 1);return tuple(coef*z for z in pair)
  depth+=(c in '({')-(c in ')}')
 return None
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
N=dict(records=0,source_banks=0,source_values=0,source_keys=0,formal_inputs=0,primitive_stages=0,differentials=0,bounds=0,individual_endpoint_components=0,values=0,pairs=0,domain_conditions=0,improper_endpoint_checks=0);tasks={l:set()for l in('easy','moderate','hard')}
def check(rec,sid=None):
 q=rec['question'];sol=q[':question/worked-solution'];given=next(b for b in B.blocks(q[':question/problem'])if r'\int'in b).split('=')[0].strip().rstrip('.,?');F,v,L,U=integral(given);assert v==x;definite=L is not None
 sm=re.search(r'Let \$u=(.*?)\$',sol);V=scalar(sm[1])if sm else None;k=s.diff(V,x)if V is not None else s.Integer(1)
 if V is not None:
  assert equal(V,k*x)and k>0 and not k.has(x)
  dm=re.search(r'Then \$(.*?)\$',sol);assert dm;d=clean(dm[1]);left,right=d.split('=')
  def measure(z):
   z=re.sub(E.DIFF,lambda m:'(j)'if m[1]=='u'else'(k)',z);return scalar(z).subs({E.P.locals_['j']:k,E.P.locals_['k']:1})
  assert equal(measure(left),measure(right));N['differentials']+=1
  if definite:
   table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M);assert[t[0]for t in table]==['x','u'];assert all(equal(scalar(a),b)for a,b in zip(table[0][1:]+table[1][1:],[L,U,V.subs(x,L),V.subs(x,U)]));N['bounds']+=4
 terms=list(parts(sol));prim=None;expected=None;bl=bh=None;var=x
 if definite:
  prim,bl,bh=bar(next(t for t in terms if '|_'in clean(t)));var=u if prim.has(u)else x;assert zero(E.derivative(prim,x,V),F);assert equal(bl,L if var==x else V.subs(x,L))and equal(bh,U if var==x else V.subs(x,U));expected=s.simplify(prim.subs(var,bh)-prim.subs(var,bl));N['bounds']+=2
  conditions=[s.denom(F)]+[s.cos(t.args[0])if t.func in(s.tan,s.sec)else s.sin(t.args[0])for t in F.atoms(s.tan,s.sec,s.cot,s.csc)]
  for cond in conditions:
   if cond==1:continue
   roots=s.solveset(cond,x,domain=s.Interval(L,U));assert roots==s.EmptySet or isinstance(roots,s.FiniteSet),(cond,roots)
   for root in roots:
    assert root in(L,U),('interior original pole',cond,root);value=s.limit(s.trigsimp(F),x,root,dir='+'if root==L else'-');assert value.is_finite;N['improper_endpoint_checks']+=1
   N['domain_conditions']+=1
 endpoint_seen=False
 for term in terms:
  if r'\int'in term:
   body,v,a,b=integral(term);assert v in(x,u);assert(a,b)==((L,U)if v==x else(V.subs(x,L),V.subs(x,U))if definite else(None,None));assert zero(body if v==x else body.subs(u,V)*k,F);N['formal_inputs']+=1;N['bounds']+=2 if definite else 0
  elif definite and '|_'in clean(term):N['primitive_stages']+=1
  elif definite:
   assert equal(scalar(term),expected),('endpoint equality',term,expected)
   pair=signed_pair(term)
   if pair is not None and not endpoint_seen:
    target=(prim.subs(var,bh),-prim.subs(var,bl));assert(equal(pair[0],target[0])and equal(pair[1],target[1]))or(equal(pair[0],target[1])and equal(pair[1],target[0])),('separate signed endpoints',term,pair,target);endpoint_seen=True;N['individual_endpoint_components']+=2
  else:assert zero(E.derivative(scalar(term),x,V),F);N['primitive_stages']+=1
 if definite:assert endpoint_seen
 f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];key=f[':answer-field/correct'][1];same=equal if definite else lambda a,b:zero(E.derivative(a-b,x));good=[equal(v,expected)if definite else zero(E.derivative(v,x),F)for v in vals];assert[a[':answer/id']for a,ok in zip(f[':answer-field/choices'],good)if ok]==[key]
 for i,v in enumerate(vals):
  for w in vals[:i]:assert not same(v,w),(rec['generation']['template'],v,w,vals,F);N['pairs']+=1
 if sid:
  of=olds[sid][':question/answer-fields'][0];ov=[scalar(a[':answer/value'])for a in of[':answer-field/choices']];
  if sid=='q-74279':ov[3]=-s.csc(4*x)**2/2+E.C
  assert len(ov)==len(vals)and all(sum(same(v,w)for w in vals)==1 for v in ov);assert same(scalar(of[':answer-field/correct'][':answer/value']),next(v for a,v in zip(f[':answer-field/choices'],vals)if a[':answer/id']==key));N['source_banks']+=1;N['source_values']+=len(vals);N['source_keys']+=1
 N['records']+=1;N['values']+=len(vals);tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(s.trigsimp(F.rewrite(s.sin))),str(L),str(U)))
for sid in olds:
 check(G.generate(G.level(sid),template=sid,parameters={'scale':1}),sid)
 for scale in(-5,8):check(G.generate(G.level(sid),template=sid,parameters={'scale':scale}))
for template in('authored-h-cos-cot','authored-h-tan-sin'):
 for a,b,ends in itertools.product((-4,1,4),(-4,1,4),G.ENDPOINTS):check(G.generate('hard',template=template,parameters={'a':a,'b':b,'lower':list(ends[:2]),'upper':list(ends[2:])}))
for l in tasks:
 for r in G.batch(l,18,489):check(r)
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,source_repair='Raw19banks71choices52distractors preserved; normal18unchangedbanks and1explicit duplicate-primitive distractor repair; normal70/71sourcechoices51/52distractors unchanged.',sampled_actual_tasks={l:len(t)for l,t in tasks.items()},scope='Source E/M quotient identities, known basic trig primitives and only observed linear substitutions. Missing H authored from observed two-term cubic/quotient reductions with independent signed coefficients and observed definite-evaluation method, exact safe endpoints; more arithmetic same KP rather than new substitution/logarithm branch.',native_limitations='631accepted1600rejected0unresolved;462genuine mathematically valid normal blank equivalent `(canonical)+0` false rejections retained and qualified. Parentgeneric canonical/wrong checks separate. No engine edits or output pruning.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

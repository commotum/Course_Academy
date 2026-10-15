"""Parent positive-domain substitution, actual formal inputs, bars and signed endpoints."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ID=17592186100874;FOLDER=R.parents[2]/f'generate/scratch/{ID}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_defrational_gen',FOLDER.with_suffix('.py'));D=load('root_defrational_reader',R/'definite-elementary-readback.py');P=D.P;x,u=P.x,P.u
scalar=D.scalar

def equal(a,b):return s.simplify(s.expand_log(a-b))==0
source=json.load(open(FOLDER/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{ID}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};N=dict(raw=0,banks=0,values_original=0,keys_original=0,records=0,differential_relations=0,bounds=0,formal_integrands=0,bars=0,individual_endpoint_components=0,equalities=0,values=0,pairs=0);tasks={l:set()for l in('easy','moderate','hard')}

def split_signed(text):
 text=D.clean(text);depth=0
 for i,c in enumerate(text):
  if c in '+-'and i>0 and depth==0 and text[i-1]not in '+-*/^':return scalar(text[:i]),(1 if c=='+'else-1)*scalar(text[i+1:])
  depth+=(c in '({')-(c in ')}')
 # Preserve separate contributions inside a constant-denominator fraction.
 for match in re.finditer(r'\\frac\{',text):
  numerator,end=D.group(text,match.end()-1);denominator,end=D.group(text,end);pair=split_signed(numerator)
  if pair is None:continue
  prefix=text[:match.start()].strip();suffix=text[end:].strip()
  prefix=prefix.removesuffix(r'\cdot').strip()
  coeff=scalar(prefix)if prefix else s.Integer(1);tail=scalar(suffix)if suffix else s.Integer(1);den=scalar(denominator);assert den!=0
  return tuple(coeff*v*tail/den for v in pair)
 # Coefficient times an explicit pair of endpoint contributions.
 start=text.find('(')
 if start>=0 and text.endswith(')'):
  pair=split_signed(text[start+1:-1])
  if pair is None:return None
  prefix=text[:start].removesuffix(r'\cdot').strip();coeff=scalar(prefix)if prefix else s.Integer(1);return tuple(coeff*z for z in pair)

 return None

def check(rec,source_id=None):
 q,m=rec['question'],rec['generation'];given=next(b for b in D.blocks(q[':question/problem'])if r'\int'in b).rstrip('= .');co,F,var,L,H,end=D.integral(given);F=co*F;assert var==x and not end and L<H;sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==4
 rows=lambda b:[r.replace('&','').strip()for r in re.sub(r'\\(?:begin|end)\{aligned\}','',b).split(r'\\')]
 rr=rows(blocks[0]);U=scalar(rr[0].split('=',1)[1]);der=s.diff(U,x);poly=s.Poly(U,x);assert poly.degree()in(1,2,3,4);crit=[L,H]+[v for v in s.solve(der,x)if v.is_real and L<=v<=H];z=s.Symbol('root_inner_positive',positive=True)
 def eqreal(a,b):
  if s.cancel(a-b)==0:return True
  if equal((a-b).xreplace({U:z}),0):return True
  if L>=0 or H<=0:
   certified=s.Symbol('root_certified_x',positive=True);return equal((a-b).subs(x,certified if L>=0 else-certified),0)
  return False
 assert scalar(rr[1].split('=',1)[1])==der;N['differential_relations']+=1
 def measure(raw):
  mm=re.search(P.DIFF,D.clean(raw));assert mm and not D.clean(raw)[mm.end():].strip();prefix=D.clean(raw)[:mm.start()].strip();coeff=s.Integer(1)if not prefix else scalar(prefix);return coeff*(der if mm[1]=='u'else 1)
 for row in rr[2:]:a,b=row.split('=');assert equal(measure(a),measure(b));N['differential_relations']+=1
 table=[row.split('&')for row in re.sub(r'\\(?:begin|end)\{aligned\}','',blocks[1]).split(r'\\')];table=[[v.strip()for v in row]for row in table];assert len(table)==2;assert table[0][0]=='x'and table[1][0]=='u';xl,xh=map(scalar,table[0][1:]);ul,uh=map(scalar,table[1][1:]);assert xl==L and xh==H and U.subs(x,L)==ul and U.subs(x,H)==uh ;N['bounds']+=4
 candidates=[]
 for power in(s.Rational(1,2),s.Rational(3,2),s.Integer(2),s.Integer(3)):
  ratio=s.simplify(((F/der)/U**power).xreplace({U:z}))
  if ratio.has(x)and(L>=0 or H<=0):
   certified_x=s.Symbol('root_x_positive',positive=True);ratio=s.simplify(ratio.subs(x,certified_x if L>=0 else-certified_x))
  if ratio.is_Rational and ratio!=0:candidates.append((power,ratio))
 assert len(candidates)==1,('cannot independently recover power kernel',F,U,der,candidates)
 exponent,ratio=candidates[0]
 if exponent.q==2:assert all(U.subs(x,v)>=0 for v in crit)
 prim=ratio*u**(exponent+1)/(exponent+1)
 expected=s.simplify(prim.subs(u,uh)-prim.subs(u,ul));kernel=u**exponent
 def primitive(body,variable):
  if variable==x:
   multiplier=s.simplify(s.cancel(body/F).xreplace({U:z}));assert not multiplier.has(x,z),('root original integral normalization',m['template'],body,F,U,multiplier);return multiplier*prim.subs(u,U)
  assert variable==u;zp=s.Symbol('root_u_positive',positive=True);multiplier=s.simplify((body/kernel).subs(u,zp));assert not multiplier.has(u,zp);return multiplier*u**(exponent+1)/(exponent+1)
 D.primitive=primitive
 # Conversion equality plus the exact original/transformed bounds on every integral.
 bar=None;endpoint_count=0
 for bi,b in enumerate(blocks[2:],start=2):
  for row_index,row in enumerate(rows(b)):
   for part in row.split('='):
    if not part.strip():continue
    part=part.replace(r'{\cdot',r'\cdot')
    # Source MathML braces group the primitive and evaluation bar; retain math
    # while removing that one unmatched grouping delimiter before the bar.
    if r'|_'in D.clean(part):
     cleanpart=D.clean(part);before,after=cleanpart.split(r'|_',1)
     while before.count('{')>before.count('}'):
      depth=0;unmatched=[]
      for at,char in enumerate(before):
       if char=='{':unmatched.append(at)
       elif char=='}':unmatched.pop()
      at=unmatched[0];before=before[:at]+before[at+1:]
     part=before+r'|_'+after
    value,info=D.value(part);assert equal(value,expected),('actual definite stage',m['template'],part,value,expected);N['equalities']+=1
    if info[0]=='integral':
     _,body,ivar,lo,hi=info;assert lo==(L if ivar==x else ul)and hi==(H if ivar==x else uh);effective=body if ivar==x else body.subs(u,U)*der;assert eqreal(effective,F);N['formal_integrands']+=1;N['bounds']+=2
    elif info[0]=='bar':
     _,bar,lo,hi=info;assert lo==ul and hi==uh and eqreal(P.derivative(bar,x,U),F);N['bars']+=1;N['bounds']+=2
    elif bar is not None and row_index<len(rows(b))-1:
     pair=split_signed(part)
     if pair:
      target=(bar.subs(u,uh),-bar.subs(u,ul));assert(equal(pair[0],target[0])and equal(pair[1],target[1]))or(equal(pair[0],target[1])and equal(pair[1],target[0])),('separate endpoint arithmetic',part,pair,target);endpoint_count+=2
 assert bar is not None and endpoint_count>=2;N['individual_endpoint_components']+=endpoint_count
 f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if equal(v,expected)]==[f[':answer-field/correct'][1]]
 for i,v in enumerate(vals):
  for w in vals[:i]:assert not equal(v,w);N['pairs']+=1
 if source_id:
  old=olds[source_id];of=old[':question/answer-fields'][0];ov=[scalar(a[':answer/value'])for a in of[':answer-field/choices']];assert len(ov)==len(vals)and all(sum(equal(v,w)for w in vals)==1 for v in ov);N['banks']+=1;N['values_original']+=len(vals)
  if ':answer-field/correct'in of:assert equal(scalar(of[':answer-field/correct'][':answer/value']),expected);N['keys_original']+=1
 N['records']+=1;N['values']+=len(vals);tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(F),str(L),str(H)))
def source_normal(q):
 q=json.loads(json.dumps(q));q.pop(':db/id',None)
 if ':question/difficulty'in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  if ':answer-field/correct'in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident']
 return q
for sid,o in olds.items():
 level='easy'if G.LEVELS[sid]=='unrated'else G.LEVELS[sid]
 raw=G.generate(level,template=sid,profile='observed_raw');assert raw['question']==source_normal(o);N['raw']+=1
 check(G.generate(level,template=sid,parameters=G.defaults(sid),profile='blank'if G.SPECS[sid][3]=='blank'else'observed'),sid)
for r in json.load(open(FOLDER/'review-cases.json')):
 if 'question'in r and not r['generation'].get('evidence_only',False):check(r)
# Changed opaque observed profiles preserve transformed endpoints and scale the
# ENTIRE original bank by the independently recovered differential multiplier.
opaque_values=0
for sid in('q-49610','q-49613','q-49622','q-17103'):
 original=G.defaults(sid);n=int(G.SPECS[sid][0]);a0,b0,c0=original['a'],original['b'],original['c'];lo0,hi0=map(scalar,(original['l'],original['h']));UL=a0*lo0**n+b0;UH=a0*hi0**n+b0
 parameters=([dict(a=a,b=b,c=1,l=str((UL-b)/a),h=str((UH-b)/a))for a,b in[(2,-6),(10,7),(7,0)]]if n==1 else[dict(a=a,b=1,c=c,l='0',h='2'if a==1 else'1')for a,c in[(1,1),(1,9),(8,1),(8,9)]])
 for params in parameters:
  r=G.generate(G.LEVELS[sid],template=sid,parameters=params,profile='observed');check(r);factor=s.Rational(params['c']*a0,c0*params['a']);old=[scalar(z[':answer/value'])*factor for z in olds[sid][':question/answer-fields'][0][':answer-field/choices']];new=[scalar(z[':answer/value'])for z in r['question'][':question/answer-fields'][0][':answer-field/choices']];assert len(old)==len(new)and all(sum(equal(v,w)for w in new)==1 for v in old);opaque_values+=len(new)
N['changed_opaque_profile_values']=opaque_values
for l in tasks:
 for seed in range(24):check(G.generate(l,seed))
result=dict(status='passed',script_sha256=hashlib.sha256(FOLDER.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_tasks={l:len(t)for l,t in tasks.items()},domain_proof='Actual polynomial extrema certify radicand>=0 over whole closed original interval; integer powers permit signed inners. Each original/transformed bound, primitive bar and individual signed endpoint evaluated separately; zero radicands allowed by continuity of the positive-power primitive.',scope='Observed positive powers and radicals only, fixed linear/cubic/quadratic/quartic substitution and source level workload; no following rational-log KP skills. Complete opaque observed banks vary by exact homogeneous multiplier with original transformed bounds fixed; method banks separately authored.',native_limitations='Private75accepted118rejected0gaps, genuine power/radical equivalents accepted. Parent generic report additionalcanonical/ownedIDs.',database_writes=0);(R/f'qa/{ID}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

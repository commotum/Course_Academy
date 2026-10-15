"""Parent positive-domain substitution, actual formal inputs, bars and signed endpoints."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ID=17592186100877;FOLDER=R.parents[2]/f'generate/scratch/{ID}'
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
 # Coefficient times an explicit pair of endpoint contributions.
 start=text.find('(')
 if start>=0 and text.endswith(')'):
  pair=split_signed(text[start+1:-1])
  if pair is None:return None
  coeff=scalar(text[:start])if text[:start].strip()else s.Integer(1);return tuple(coeff*z for z in pair)
 return None

def check(rec,source_id=None):
 q,m=rec['question'],rec['generation'];given=next(b for b in D.blocks(q[':question/problem'])if r'\int'in b).rstrip('= .');co,F,var,L,H,end=D.integral(given);F=co*F;assert var==x and not end and L<H;sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==4
 rows=lambda b:[r.replace('&','').strip()for r in re.sub(r'\\(?:begin|end)\{aligned\}','',b).split(r'\\')]
 rr=rows(blocks[0]);U=scalar(rr[0].split('=',1)[1]);der=s.diff(U,x);poly=s.Poly(U,x);assert poly.degree()in(1,2,3,4);crit=[L,H]+[v for v in s.solve(der,x)if v.is_real and L<=v<=H];assert all(U.subs(x,v)>0 for v in crit);z=s.Symbol('root_inner_positive',positive=True)
 def eqreal(a,b):return equal((a-b).xreplace({U:z}),0)
 assert scalar(rr[1].split('=',1)[1])==der;N['differential_relations']+=1
 def measure(raw):
  mm=re.search(P.DIFF,D.clean(raw));assert mm and not D.clean(raw)[mm.end():].strip();prefix=D.clean(raw)[:mm.start()].strip();coeff=s.Integer(1)if not prefix else scalar(prefix);return coeff*(der if mm[1]=='u'else 1)
 for row in rr[2:]:a,b=row.split('=');assert equal(measure(a),measure(b));N['differential_relations']+=1
 table=rows(blocks[1]);assert len(table)==2;table=[[v.strip()for v in row.split()]for row in table];assert table[0][0]=='x'and table[1][0]=='u';xl,xh=map(scalar,table[0][1:]);ul,uh=map(scalar,table[1][1:]);assert xl==L and xh==H and U.subs(x,L)==ul and U.subs(x,H)==uh and ul>0 and uh>0;N['bounds']+=4
 hard=r'\sqrt'in given
 if hard:
  ratio=s.simplify((F*s.sqrt(U**3)/der).xreplace({U:z}));assert not ratio.has(x,z);prim=-2*ratio/s.sqrt(u)
 else:
  ratio=s.cancel(F*U/der);assert ratio.is_Rational;prim=ratio*s.log(u)
 expected=s.simplify(prim.subs(u,uh)-prim.subs(u,ul));kernel=1/u**s.Rational(3,2)if hard else 1/u
 def primitive(body,variable):
  if variable==x:
   multiplier=s.simplify(s.cancel(body/F).xreplace({U:z}));assert not multiplier.has(x,z),('root original integral normalization',m['template'],body,F,U,multiplier);return multiplier*prim.subs(u,U)
  assert variable==u;zp=s.Symbol('root_u_positive',positive=True);multiplier=s.simplify((body/kernel).subs(u,zp));assert not multiplier.has(u,zp);return multiplier*(-2/s.sqrt(u)if hard else s.log(u))
 D.primitive=primitive
 # Conversion equality plus the exact original/transformed bounds on every integral.
 bar=None;endpoint_count=0
 for bi,b in enumerate(blocks[2:],start=2):
  for row_index,row in enumerate(rows(b)):
   for part in row.split('='):
    if not part.strip():continue
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
for sid,o in olds.items():
 assert next(r for r in json.load(open(FOLDER/'raw-source-replay.json'))if r['source_id']==sid)['raw']==o;N['raw']+=1;check(G.generate(G.CONFIG[sid][0],template=sid,parameters=G.parameters(G.CONFIG[sid][2]),profile='observed'),sid)
for l in tasks:
 for seed in range(24):check(G.generate(l,seed))
result=dict(status='passed',script_sha256=hashlib.sha256(FOLDER.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_tasks={l:len(t)for l,t in tasks.items()},domain_proof='Actual polynomial extrema certify inner>0 on whole original closed interval, including even degree crossing zero. Root/rational equalities use a positive-inner symbol only after that certificate. Each signed endpoint term and primitive bound independently matched without forced log laws.',scope='Actual source labels linear logarithm, derivative-matched degree2/3/4 logarithm, and original quadratic inner under the square root of its cube. Fixed operative stages and perfect-power endpoint roles preserved.',native_limitations='See frozen native evidence: 12 genuine source-style natural-log TeX equivalent-entry rejections; supplemental log spellings yield 3 accepts and 3 genuine unresolved, so the limitation includes equivalence as well as notation; no valid-output pruning.',database_writes=0);(R/f'qa/{ID}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

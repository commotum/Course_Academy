"""Root source whole banks, linear trig substitution and actual signed endpoints."""
import sys,json,hashlib,importlib.util,re,copy
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068915;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_sincos_affine_gen',D.with_suffix('.py'));T=load('root_sincos_affine_math',R/'trig-affine-integral-readback.py');A=load('root_sincos_vars',R/'affine-power-integral-readback.py');P=T.P;x=P.x
@T.lru_cache(maxsize=6000)
def primitive(F,var):
 for fun in F.atoms(s.sin,s.cos):
  arg=fun.args[0];a=s.diff(arg,var)
  if a==0 or a.has(var):continue
  coeff=s.cancel(F/(a*fun))
  if not coeff.has(var):return coeff*(-s.cos(arg)if fun.func==s.sin else s.sin(arg))
 raise AssertionError(('outside affine sin/cos',F))
T.primitive=primitive;T.D.primitive=primitive
def adapt(q):
 q=copy.deepcopy(q)
 for k in(':question/problem',':question/worked-solution'):
  if k in q:q[k]=A.mathnorm(q[k])
 return q
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,prompts=0,missing=0)
def prose(t):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$[^$]*\$','<MATH>',t,flags=re.S)).strip().rstrip('.')
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];r=G.generate(c['difficulty'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];assert prose(q[':question/problem'])==prose(o[':question/problem']);F,l,h=T.given(adapt(q));of,ol,oh=T.given(adapt(o));assert T.eq(F,of)and(l is None and ol is None or T.eq(l,ol)and T.eq(h,oh));fidelity['prompts']+=1
 if ':question/worked-solution'in o:
  assert prose(q[':question/worked-solution'])==prose(o[':question/worked-solution']);T.check(adapt(o),False);fidelity['solutions']+=1
 else:fidelity['missing']+=1
 f=q[':question/answer-fields'][0];old=o[':question/answer-fields'][0];assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']and f[':answer-field/key']==old[':answer-field/key'];nv=[P.scalar(A.mathnorm(a[':answer/value']))for a in f[':answer-field/choices']];ov=[P.scalar(A.mathnorm(a[':answer/value']))for a in old[':answer-field/choices']];assert len(ov)==len(nv)and all(sum(T.eq(v,w)for w in nv)==1 for v in ov)
 if ':answer-field/correct'in old:assert T.eq(P.scalar(A.mathnorm(old[':answer-field/correct'][':answer/value'])),next(v for a,v in zip(f[':answer-field/choices'],nv)if a[':answer/id']==f[':answer-field/correct'][1]));fidelity['keys']+=1
 fidelity['banks']+=1;fidelity['values']+=len(ov)
N=dict(records=0,values=0,pairs=0,blanks=0);seen={l:set()for l in('easy','moderate','hard')}
def check(r):
 q,m=r['question'],r['generation'];F,expected,counts=T.check(adapt(q),False)
 for k,v in counts.items():N[k]=N.get(k,0)+v
 f=q[':question/answer-fields'][0];vals=[P.scalar(A.mathnorm(a[':answer/value']))for a in f[':answer-field/choices']];ds=[P.derivative(v,x)if expected is None else v for v in vals];answer=F if expected is None else expected;assert [a[':answer/id']for a,d in zip(f[':answer-field/choices'],ds)if T.eq(d,answer)]==[f[':answer-field/correct'][1]]
 for i,d in enumerate(ds):
  for e in ds[:i]:assert not T.eq(d,e);N['pairs']+=1
 assert m['eligible_for_learning']==not_reference(m)and m['evidence_only']==(not not_reference(m));N['records']+=1;N['values']+=len(vals);N['blanks']+=f[':answer-field/type'].endswith('/blank');seen[q[':question/difficulty'].split('/')[-1]].add(str(F)+'|'+str(T.given(adapt(q))[1:]))
def not_reference(m):return not(m['template']=='q-2204'and m['bank_profile']=='observed')
for c in json.load(open(D/'source-cases.json')):check(G.generate(c['difficulty'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
for i,e in enumerate(json.load(open(D/'engine-input.json'))):
 check(e['record'])
 if i%40==0:print('Root affine sin/cos read',i,flush=True)
for level in('easy','moderate','hard'):
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,coverage='All source anchors,87 native output representatives and54fresh default samples. Worker separately exhausts complete finite banks and actual displayed slot coverage E264/M302/H144; hard overlaps moderate workload.',native_limitations={'ordinary_wrong_responses_unresolved':3,'cases':'submission1 vs4/pi,2sqrt(3)/pi,3/pi','observed_wording_equivalents_rejected':2,'separate_malformed_unresolved':1},approval_scope='Local docs3–7 with precise frozen native comparison limitations; no engine changes.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

"""Root source whole banks, affine substitution/poles/limits and endpoint signs."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068916;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_recip_trig_gen',D.with_suffix('.py'));T=load('root_recip_trig_math',R/'trig-affine-integral-readback.py');P=T.P;x=P.x
N=dict(records=0,integral_sides=0,primitive_sides=0,primitive_bars=0,bound_references=0,endpoint_components=0,differentials=0,values=0,pairs=0,blanks=0,reference_only=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fidelity=dict(banks=0,values=0,keys=0,solutions=0,prompts=0,reference_only=0)
def prose(t):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$[^$]*\$','<MATH>',t,flags=re.S)).strip().rstrip('.')
def rhs_profiles(sol):
 block=next(b for b in T.D.blocks(sol)if r'\begin{aligned}'in b);rows=re.sub(r'\\(?:begin|end)\{aligned\}','',block).split(r'\\');result=[]
 for row in rows:
  rhs=row.split('=',1)[1]
  if r'\int'in rhs:result.append(('integral','u'if re.search(P.DIFF,rhs)[1]=='u'else'x'))
  elif re.search(r'(?:\||\{\|\})_',T.D.clean(rhs)):result.append(('bar',))
  else:result.append(('value',))
 return result
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];r=G.generate(c['difficulty'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];assert prose(q[':question/problem'])==prose(o[':question/problem']);F,l,h=T.given(q);of,ol,oh=T.given(o);assert T.eq(F,of)and(l is None and ol is None or T.eq(l,ol)and T.eq(h,oh));fidelity['prompts']+=1
 if ':question/worked-solution'in o:
  assert prose(q[':question/worked-solution'])==prose(o[':question/worked-solution']);assert rhs_profiles(q[':question/worked-solution'])==rhs_profiles(o[':question/worked-solution']);T.check(o);fidelity['solutions']+=1
 f=q[':question/answer-fields'][0];old=o[':question/answer-fields'][0];assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']and f[':answer-field/key']==old[':answer-field/key'];nv=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];ov=[P.scalar(a[':answer/value'])for a in old[':answer-field/choices']];assert len(ov)==len(nv)and all(sum(T.eq(v,w)for w in nv)==1 for v in ov)
 if ':answer-field/correct'in old:assert T.eq(P.scalar(old[':answer-field/correct'][':answer/value']),next(v for a,v in zip(f[':answer-field/choices'],nv)if a[':answer/id']==f[':answer-field/correct'][1]));fidelity['keys']+=1
 fidelity['banks']+=1;fidelity['values']+=len(ov);fidelity['reference_only']+=bool(c.get('reference_only'))
def check(r):
 q,m=r['question'],r['generation'];F,A,counts=T.check(q)
 for key,v in counts.items():N[key]+=v
 assert m['eligible_for_learning']==(m['template']!='q-113983')and m['evidence_only']==(m['template']=='q-113983');N['reference_only']+=not m['eligible_for_learning']
 assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];values=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];criteria=[P.derivative(v,x)if A is None else v for v in values];answer=F if A is None else A;hits=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],criteria)if T.eq(v,answer)];assert hits==[f[':answer-field/correct'][1]],(m['template'],m['parameters'],answer,criteria)
 for i,v in enumerate(criteria):
  for w in criteria[:i]:assert not T.eq(v,w);N['pairs']+=1
 N['records']+=1;N['values']+=len(values);N['blanks']+=f[':answer-field/type'].endswith('/blank')
for c in json.load(open(D/'source-cases.json')):check(G.generate(c['difficulty'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
for i,e in enumerate(json.load(open(D/'engine-input.json'))):
 check(e['record'])
 if i%80==0:print('Root reciprocal trig records read',i,flush=True)
for item in json.load(open(D/'observed-bank-variants.json')):
 r=item.get('record',item)
 if 'question'in r:check(r)
for level in ('easy','moderate','hard'):
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

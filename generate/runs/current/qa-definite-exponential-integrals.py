"""Root given/bounds/substitution/every endpoint-component and full-bank audit."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186184352;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_def_gen',D.with_suffix('.py'));P=load('root_def_math',R/'definite-elementary-readback.py')
N=dict(records=0,rows=0,integral_inputs=0,primitive_bars=0,individual_endpoints=0,bound_references=0,differentials=0,values=0,pairs=0,banks=0,blanks=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fidelity=dict(prompts=0,solutions=0,banks=0,values=0,keys=0,source_rows=0)
def prose(t):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$[^$]*\$','<MATH>',t,flags=re.S)).strip().rstrip('.')
def operative_profile(sol):
 block=next(b for b in P.blocks(sol)if r'\begin{aligned}'in b);block=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','');result=[]
 for row in block.split(r'\\'):
  rhs=row.split('=',1)[1];v,info=P.value(rhs)
  if info[0]=='integral':result.append(('integral',str(info[2])))
  elif info[0]=='bar':result.append(('bar',))
  else:result.append(('arithmetic',))
 return result
for case in json.load(open(D/'source-cases.json')):
 o=olds[case['source_id']];q=G.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert prose(q[':question/problem'])==prose(o[':question/problem'])
 oldtext=next(b for b in P.blocks(o[':question/problem'])if r'\int'in b).rstrip('= .');newtext=next(b for b in P.blocks(q[':question/problem'])if r'\int'in b).rstrip('= .');a,F,var,l,h,e=P.integral(oldtext);b,H,v,ll,hh,ee=P.integral(newtext);assert not e and not ee and var==v and P.equal(a*F,b*H)and P.equal(l,ll)and P.equal(h,hh);fidelity['prompts']+=1
 if ':question/worked-solution'in o:
  assert prose(q[':question/worked-solution'])==prose(o[':question/worked-solution']);assert operative_profile(q[':question/worked-solution'])==operative_profile(o[':question/worked-solution']);fidelity['solutions']+=1;fidelity['source_rows']+=len(operative_profile(o[':question/worked-solution']))
  P.stages({**q,':question/problem':o[':question/problem'],':question/worked-solution':o[':question/worked-solution']})
 for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
  assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']and f[':answer-field/key']==of[':answer-field/key'];ov=[P.scalar(a[':answer/value'])for a in of[':answer-field/choices']];nv=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert len(ov)==len(nv)and all(sum(P.equal(a,b)for b in nv)==1 for a in ov)
  if ':answer-field/correct'in of:assert P.equal(P.scalar(of[':answer-field/correct'][':answer/value']),next(v for a,v in zip(f[':answer-field/choices'],nv)if a[':answer/id']==f[':answer-field/correct'][1]));fidelity['keys']+=1
  fidelity['banks']+=1;fidelity['values']+=len(ov)
def check(r):
 q=r['question'];answer,counts=P.stages(q)
 for key,value in counts.items():N[key]+=value
 assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];values=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];hits=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if P.equal(v,answer)];assert hits==[f[':answer-field/correct'][1]],(r['generation'],answer,values)
 for i,v in enumerate(values):
  for w in values[:i]:assert not P.equal(v,w);N['pairs']+=1
 N['records']+=1;N['values']+=len(values);N['banks']+=1;N['blanks']+=f[':answer-field/type'].endswith('/blank')
for i,entry in enumerate(json.load(open(D/'native-input.json'))):
 r=entry.get('record',entry);check(r)
 if i%150==0:print('Root definite records read',i,flush=True)
for level in G.LEVELS:
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),grading_limitations=['Valid log-difference equivalence is not established by frozen native grader; canonical and tested unreduced endpoint-ratio forms pass. Historical source-presentation wording restricts answer forms; normal exact instruction fixes that restriction.'],database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

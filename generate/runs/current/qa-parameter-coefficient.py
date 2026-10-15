"""Root observed coefficient/shift banks, contradiction conditions and full solution rows."""
import sys,json,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186204090;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_pc_gen',D.with_suffix('.py'));P=load('root_pc_math',R/'no-solution-parameter-readback.py');X,U=P.X,P.U
N=dict(records=0,rows=0,bindings=0,equation_rows=0,condition_rows=0,annotations=0,values=0,pairs=0,banks=0,contradictions=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fidelity=dict(prompts=0,solutions=0,fields=0,values=0,refs=0)
for tid,o in olds.items():
 assert G.observed_raw(tid,G.DEFAULTS[tid])['question']==o;fidelity['prompts']+=1;fidelity['solutions']+=1
 for f in o[':question/answer-fields']:fidelity['fields']+=1;fidelity['values']+=len(f[':answer-field/choices']);fidelity['refs']+=1
def check(r):
 q,m=r['question'],r['generation'];tid=m['template'];p=m['parameters'];variable,parameter,lhs,rhs,coefficient,constant,answer=P.givens(q[':question/problem']);c,shift,b=[s.Integer(p[k]) for k in ('c','s','b')]
 assert s.expand(lhs-c*(U+shift)*X)==0 and rhs==b and coefficient.subs(U,answer)==0 and answer==-shift;N['contradictions']+=1
 for key,value in P.stages(q[':question/worked-solution'],variable,parameter,lhs,rhs,coefficient,constant).items():N[key]+=value
 f=q[':question/answer-fields'][0];assert f[':answer-field/type'].endswith('/radio');vals=[P.scalar(z[':answer/value'],variable,parameter) for z in f[':answer-field/choices']];assert len(vals)==5 and all(not z.free_symbols for z in vals)
 assert sum(z==answer for z in vals)==1 and next(z for z,a in zip(vals,f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])==answer
 for a,b1 in itertools.combinations(vals,2):assert a!=b1;N['pairs']+=1
 if tid=='q-287665':expected=[0,b,1/c,1,c]
 elif tid=='q-288135':expected=[0,c,b,1/abs(b),-1/c]
 elif tid=='q-288107':expected=[c,abs(b),0,1,1/c]
 elif tid=='q-288593':expected=[1/b,-b,b/2,-shift,0]
 elif tid=='q-288596':expected=[1/shift,b,-shift,-b,-1/b]
 elif tid=='q-288143':expected=[0,c,-c,shift,-shift]
 elif tid=='q-288144':expected=[c/shift,b,-1/c,-shift,c]
 else:raise AssertionError(tid)
 assert set(vals)==set(map(s.sympify,expected));N['values']+=5;N['banks']+=1;N['records']+=1
for level in G.LEVELS:
 for seed in range(18):check(G.generate(level,seed))
 for tid,(l,_) in G.PROFILES.items():
  if l!=level:continue
  params=G.domain(level,tid)
  for row in (params[0],params[len(params)//2],params[-1]):check(G.generate(level,template=tid,parameters=dict(zip(('c','s','b'),row))))
  check(G.generate(level,template=tid,parameters=G.DEFAULTS[tid]))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

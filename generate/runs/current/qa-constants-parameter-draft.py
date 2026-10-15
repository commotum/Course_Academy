"""Root constant collection, signed scale cancellation and complete scalar blank answers."""
import sys,json,hashlib,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186204091;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_cs_gen',D.with_suffix('.py'));P=load('root_cs_math',R/'no-solution-parameter-readback.py');X,U=P.X,P.U
N=dict(records=0,rows=0,bindings=0,equation_rows=0,condition_rows=0,annotations=0,values=0,blanks=0,contradictions=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q};fidelity=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0)
for tid,old in olds.items():
 assert G.replay_source(tid)==old;fidelity['prompts']+=1;fidelity['solutions']+=(':question/worked-solution' in old);fidelity['unrated']+=(':question/difficulty' not in old)
 for f in old.get(':question/answer-fields',[]):fidelity['fields']+=1;fidelity['values']+=len(f.get(':answer-field/choices',[]));fidelity['refs']+=(':answer-field/correct' in f);fidelity['missing_refs']+=(':answer-field/correct' not in f)
def check(r):
 q,m=r['question'],r['generation'];p=m['parameters'];assert '⏟' not in q[':question/worked-solution'];variable,parameter,lhs,rhs,coefficient,constant,answer=P.givens(q[':question/problem']);assert variable==p['variable'] and parameter==p['parameter']
 assert s.expand(lhs-(p['scale']*(U+p['shift'])*X+p['left']))==0 and rhs==p['right'];assert constant==p['right']-p['left']!=0 and coefficient.subs(U,answer)==0 and answer==-p['shift'];N['contradictions']+=1
 for key,value in P.stages(q[':question/worked-solution'],variable,parameter,lhs,rhs,coefficient,constant).items():N[key]+=value
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type'].endswith('/blank') and len(f[':answer-field/choices'])==1 and '{{field-1}}' in q[':question/problem'];value=f[':answer-field/choices'][0];assert P.scalar(value[':answer/value'],variable,parameter)==answer and f[':answer-field/correct']==[':answer/id',value[':answer/id']];N['values']+=1;N['blanks']+=1;N['records']+=1
for level in G.SUPPORTED_LEVELS:
 for seed in range(18):check(G.generate(level,seed))
 for t in G.CATALOG[level]:
  p=dict(zip(('scale','shift','left','right'),t));p.update(variable='x',parameter='p');check(G.generate(level,parameters=p))
for tid,old in olds.items():
 if ':question/difficulty' not in old or ':question/worked-solution' not in old:continue
 level=old[':question/difficulty'][':db/ident'].split('/')[-1];check(G.generate(level,parameters=G.source_parameters(old)))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

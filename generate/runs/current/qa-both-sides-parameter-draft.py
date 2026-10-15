"""Root parameter conditions, affine cancellation, annotations and full ratio banks."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186204092;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_bs_gen',D.with_suffix('.py'));P=load('root_bs_math',R/'no-solution-parameter-readback.py');X,U=P.X,P.U
N=dict(records=0,rows=0,bindings=0,equation_rows=0,condition_rows=0,annotations=0,values=0,pairs=0,banks=0,blanks=0,contradictions=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q};fidelity=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0)
for tid,old in olds.items():
 assert G.observed_raw(tid)['question']==old;fidelity['prompts']+=1;fidelity['solutions']+=(':question/worked-solution' in old);fidelity['unrated']+=(':question/difficulty' not in old)
 for field in old.get(':question/answer-fields',[]):fidelity['fields']+=1;fidelity['values']+=len(field.get(':answer-field/choices',[]));fidelity['refs']+=(':answer-field/correct' in field);fidelity['missing_refs']+=(':answer-field/correct' not in field)
def check(r):
 q,m=r['question'],r['generation'];variable,parameter,lhs,rhs,coef,constant,answer=P.givens(q[':question/problem']);p=m['parameters'];assert variable==p['variable'] and parameter==p['parameter'];assert s.expand(lhs-(p['a']*U*X+p['b']))==0 and s.expand(rhs-(p['c']*X+p['d']))==0
 assert s.expand(coef.subs(U,answer))==0 and constant!=0;N['contradictions']+=1
 for key,value in P.stages(q[':question/worked-solution'],variable,parameter,lhs,rhs,coef,constant).items():N[key]+=value
 f=q[':question/answer-fields'][0];vals=[P.scalar(z[':answer/value'],variable,parameter) for z in f[':answer-field/choices']];assert all(not z.free_symbols for z in vals)
 assert sum(z==answer for z in vals)==1 and next(z for z,a in zip(vals,f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])==answer
 for a,b in itertools.combinations(vals,2):assert a!=b;N['pairs']+=1
 if f[':answer-field/type'].endswith('/radio'):
  c,a=p['c'],p['a'];expected=[s.Rational(c,a),s.Rational(a,c),s.Rational(c-1,a),s.Rational(c,c-1),s.Integer(c-1)];assert len(vals)==5 and set(vals)==set(expected);assert p['b']==0
 else:assert vals==[answer] and '{{field-1}}' in q[':question/problem'];N['blanks']+=1
 assert m['domain']['kind']=='explicit finite parameter catalog' and p['a']!=0 and p['b']!=p['d']
 N['values']+=len(vals);N['banks']+=1;N['records']+=1
for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
for level in G.SUPPORTED_LEVELS:
 for p in G.CATALOG[level]:
  for template in (('right-constant',) if level=='easy' else ('both-constants','both-constants-ax-layout')):check(G.generate(level,template=template,parameters=p))
for tid,old in olds.items():
 if ':question/difficulty' not in old or ':question/worked-solution' not in old:continue
 level=old[':question/difficulty'][':db/ident'].split('/')[-1];p=G.parser.prompt_parameters(old[':question/problem'])
 for template in (('right-constant',) if level=='easy' else ('both-constants','both-constants-ax-layout')):check(G.generate(level,template=template,parameters=p))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

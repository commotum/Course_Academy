"""Root check of second-order Leibnitz operators and the actual blank fragment."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059678;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_leib_gen',D.with_suffix('.py'));P=load('root_leib_math',R/'higher-derivative-readback.py');x=P.x
N=dict(records=0,equalities=0,operands=0,targets=0,values=0,pairs=0,banks=0,blanks=0,partial_blanks=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id'in q};fidelity=dict(raw=0,served=0,values=0,solutions=0)
def presentation(t):
 t=t.replace('\u2061','');t=re.sub(r'(?<![A-Za-z\\])(sin|cos|ln)(?=x)',lambda m:'\\'+m[1]+' ',t);return t
for sid,old in olds.items():assert G.observed_raw(sid)['question']==old;fidelity['raw']+=1
for profile,level in G.PROFILES.items():
 if profile not in olds:continue
 old=olds[profile];n=len(G.candidates(profile)[0]['multipliers']);r=G.generate(level,template=profile,parameters={'multipliers':['1']*n});q=r['question'];assert q[':question/problem']==G.fmt.normalize_prose(presentation(old[':question/problem']));assert q[':question/worked-solution']==G.fmt.normalize_prose(presentation(old[':question/worked-solution']));fidelity['solutions']+=1
 for f,o in zip(q[':question/answer-fields'],old[':question/answer-fields']):
  assert f[':answer-field/key']==o[':answer-field/key'] and f[':answer-field/type']==o[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(G.fmt.normalize_tex(presentation(a[':answer/value'])) for a in o[':answer-field/choices']);assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==G.fmt.normalize_tex(presentation(o[':answer-field/correct'][':answer/value']));fidelity['values']+=len(f[':answer-field/choices'])
 fidelity['served']+=1
seen={level:set()for level in G.SUPPORTED_LEVELS}
def check(r):
 q,m=r['question'],r['generation'];positive=m['domain']=='x>0';name,base,fun=P.givens(q[':question/problem'],positive);assert name=='y' and base==0;assert re.search(r'@D2y@',P.clean(q[':question/problem']));answer=s.diff(fun,x,2)
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==2
 for order,block in enumerate(blocks,1):
  for key,count in P.stage(block,fun,name,base,order,positive=positive).items():N[key]+=count
 assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];suffix=''
 if f[':answer-field/type'].endswith('/blank'):
  mfield=re.search(r'\{\{'+re.escape(f[':answer-field/key'])+r'\}\}(.*)',q[':question/problem'],re.S);assert mfield;after=re.findall(r'\$(.*?)\$',mfield[1],re.S);assert len(after)<=1;suffix=after[0]if after else'';N['partial_blanks']+=bool(suffix)
 values=[P.scalar(a[':answer/value']+suffix,positive)for a in f[':answer-field/choices']];hits=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if P.eq(v,answer,positive)];assert hits==[f[':answer-field/correct'][1]],(m['profile'],answer,values)
 for i,v in enumerate(values):
  for w in values[:i]:assert not P.eq(v,w,positive);N['pairs']+=1
 N['records']+=1;N['values']+=len(values);N['banks']+=1;N['blanks']+=f[':answer-field/type'].endswith('/blank');seen[m['source_basis']if False else q[':question/difficulty'].split('/')[-1]].add(str(s.expand(fun)))
for level in G.SUPPORTED_LEVELS:
 for profile,p in G.catalog(level):check(G.generate(level,template=profile,parameters=p))
 assert len(seen[level])==len(G.catalog(level)),('cosmetic/alias capacity inflation',level,len(seen[level]),len(G.catalog(level)))
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

"""Root displayed rational-log substitutions, complete banks and real log domains."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068724;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_rational_log_gen',D.with_suffix('.py'));P=load('root_rational_log_math',R/'elementary-integral-readback.py');x,u=P.x,P.u
norm=lambda text:re.sub(r'(?<![A-Za-z\\])K(?![A-Za-z])','C',re.sub(r'(?<![A-Za-z\\])t(?![A-Za-z])','x',text))
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,incomplete=0)
for c in G.CASES:
 sid,level=c[:2];o=olds[sid];q=G.generate(level,template=sid,parameters=G.defaults(c))['question'];assert q[':question/problem']==o[':question/problem']and q[':question/worked-solution']==o[':question/worked-solution'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices']);fidelity['keys']+=1;fidelity['solutions']+=1
assert G.generate('easy',template='q-12500',profile='reference')['question']==olds['q-12500'];fidelity['incomplete']=1
N=dict(records=0,substitutions=0,differentials=0,integral_sides=0,primitive_sides=0,formal_inputs=0,values=0,pairs=0,blanks=0);seen={l:set()for l in G.SUPPORTED_LEVELS}
def check(r):
 q,m=r['question'],r['generation'];sol=q[':question/worked-solution'];F,var=P.prompt(norm(q[':question/problem']));assert var==x;U=P.scalar(norm(re.search(r'Let \$u=([^$]+)\$',sol)[1]));v=s.diff(U,x);assert v!=0
 blocks=[norm(b)for b in re.findall(r'\$\$(.*?)\$\$',sol,re.S)];assert len(blocks)==2;left,right=blocks[0].split('⟹');assert P.clean(left.split('=',1)[0])==r'\frac{\text{d}u}{\text{d}x}'and P.eq(P.scalar(left.split('=',1)[1]),v);ll,rr=right.strip().rstrip('.,').split('=');lm=re.fullmatch('(.*?)'+P.DIFF,ll.strip());rm=re.fullmatch('(.*?)'+P.DIFF,rr.strip());assert lm and rm and{lm[2],rm[2]}=={'x','u'}
 def co(m):return P.scalar(m[1])if P.clean(m[1])else s.Integer(1)
 assert P.eq(co(lm)*(v if lm[2]=='u'else 1),co(rm)*(v if rm[2]=='u'else 1));N['differentials']+=2;N['substitutions']+=1
 counts=P.stages(norm(sol),F,x,U)
 for k,vv in counts.items():N[k]+=vv
 f=q[':question/answer-fields'][0];vals=[P.scalar(norm(a[':answer/value']))for a in f[':answer-field/choices']];ds=[P.derivative(a,x)for a in vals];hits=[a[':answer/id']for a,d in zip(f[':answer-field/choices'],ds)if P.eq(d,F)];assert hits==[f[':answer-field/correct'][1]],('actual bank',m,ds,F)
 for i,d in enumerate(ds):
  for e in ds[:i]:assert not P.eq(d,e);N['pairs']+=1
 if f[':answer-field/type'].endswith('/blank'):
  assert s.Poly(U,x).degree()==2 and s.Poly(U,x).LC()>0 and U.subs(x,0)>0 and s.diff(U,x,1).subs(x,0)==0;N['blanks']+=1
 N['records']+=1;N['values']+=len(vals);seen[q[':question/difficulty'].split('/')[-1]].add(s.srepr(s.cancel(F)))
for i,e in enumerate(json.load(open(D/'native-input.json'))):
 check(e['record'])
 if i%40==0:print('Root rational-log actual stages read',i,flush=True)
for level in G.SUPPORTED_LEVELS:
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},native_equivalence_limitations={'valid_extra_entries':57,'accepted':19,'rejected':9,'unresolved':29,'scope':'Canonical, explicit-multiplication and +0 entries pass; log power rewrites and scaled log arguments that change only additive constants have actual frozen engine limitations. These are not math errors or foreign-ID checks.'},approval_scope='Local generator creation docs3–7 with native equivalence limitations disclosed; no engine changes or DB writes.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

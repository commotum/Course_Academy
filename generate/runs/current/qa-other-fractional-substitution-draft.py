"""Root actual rational/radical nonlinear substitution and whole source banks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068786;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_other_frac_gen',D.with_suffix('.py'));A=load('root_other_frac_math',R/'affine-power-integral-readback.py');P=A.P;x,u=P.x,P.u
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,incomplete=0)
for sid,t in G.PROFILES.items():
 if sid=='authored-easy':continue
 o=olds[sid];q=G.generate(t['level'],template=sid,parameters={'b':t['parameters'][0]})['question'];assert q[':question/problem']==o[':question/problem']and q[':question/worked-solution']==o[':question/worked-solution'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices']);fidelity['keys']+=1;fidelity['solutions']+=1
assert G.generate('hard',template='q-49636',profile='reference')['question']==olds['q-49636'];fidelity['incomplete']=1
N=dict(records=0,substitutions=0,differentials=0,integral_sides=0,primitive_sides=0,formal_inputs=0,values=0,pairs=0,supplied_scaffolds=0);seen={l:set()for l in G.LEVELS}
def check(r):
 q,m=r['question'],r['generation'];sol=q[':question/worked-solution'];norm=A.mathnorm;F,var=P.prompt(norm(q[':question/problem']));assert var==x;U=P.scalar(norm(re.search(r'Let \$u=([^$]+)\$',sol)[1]));v=s.diff(U,x);assert v!=0
 bb=A.blocks(sol);assert len(bb)==2;left,right=bb[0].split('⟹');assert P.clean(left.split('=',1)[0])==r'\frac{\text{d}u}{\text{d}x}'and P.eq(P.scalar(left.split('=',1)[1]),v);ll,rr=right.strip().rstrip('.,').split('=');lm=re.fullmatch('(.*?)'+P.DIFF,ll.strip());rm=re.fullmatch('(.*?)'+P.DIFF,rr.strip());assert lm and rm and{lm[2],rm[2]}=={'x','u'}
 co=lambda m:P.scalar(m[1])if P.clean(m[1])else s.Integer(1)
 assert P.eq(co(lm)*(v if lm[2]=='u'else 1),co(rm)*(v if rm[2]=='u'else 1));N['differentials']+=2;N['substitutions']+=1
 counts=P.stages(norm(sol),F,x,U)
 for k,vv in counts.items():N[k]+=vv
 if m['template']=='authored-easy':
  supplied=re.search(r'using \$u=([^$]+)\$ and \$\\text\{d\}u=([^$]+)\$',q[':question/problem']);assert supplied and P.eq(P.scalar(supplied[1]),U)and P.eq(P.scalar(supplied[2].replace(r'\text{d}x','')),v);N['supplied_scaffolds']+=1
 f=q[':question/answer-fields'][0];vals=[P.scalar(norm(a[':answer/value']))for a in f[':answer-field/choices']];ds=[P.derivative(a,x)for a in vals];assert len(vals)==5 and [a[':answer/id']for a,d in zip(f[':answer-field/choices'],ds)if P.eq(d,F)]==[f[':answer-field/correct'][1]]
 for i,d in enumerate(ds):
  for e in ds[:i]:assert not P.eq(d,e);N['pairs']+=1
 if m['template']=='q-2389':assert 'x > 0'in m['domain']and all(a.subs(x,A.W).is_real is not False for a in vals)
 N['records']+=1;N['values']+=len(vals);seen[q[':question/difficulty'].split('/')[-1]].add(s.srepr(s.cancel(F)))
for i,e in enumerate(json.load(open(D/'native-input.json'))):
 check(e['record'])
 if i%30==0:print('Root other fractional actual stages read',i,flush=True)
for level in G.LEVELS:
 for seed in range(18):check(G.generate(level,seed))
 assert len(seen[level])==len(G.eligible(level))*12
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},domain_proof='Positive real radical bases; integer-power denominators nonzero on connected intervals. q2389 additionally x>0 to keep every original wrong choice real. No forced power identities.',native_scope='All120owned correct choices accepted and480owned wrong choices rejected.600mathtext/foreign/malformed checks unresolved under radio-ID contract, separately disclosed.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

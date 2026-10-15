"""Root full served banks and actual fractional stages on declared real branches."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064205;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_frac_power_gen',D.with_suffix('.py'));A=load('root_frac_power_math',R/'affine-power-integral-readback.py');P=A.P;x=P.x
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(raw=0,banks=0,values=0,keys=0,solutions=0,incomplete=0)
for sid,o in olds.items():
 assert G.source_record(sid,raw=True)==o;fidelity['raw']+=1;t=G.PROFILES[sid];r=G.generate(t['difficulty'],template=sid,parameters={'b':t['b']});q=r['question'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0]
 assert sorted(re.sub(r'\s+','',a[':answer/value'])for a in f[':answer-field/choices'])==sorted(re.sub(r'\s+','',G.normalize_tex(a[':answer/value']))for a in of[':answer-field/choices']),(sid,[a[':answer/value']for a in f[':answer-field/choices']],[a[':answer/value']for a in of[':answer-field/choices']]);assert re.sub(r'\s+','',q[':question/problem'])==re.sub(r'\s+','',G.normalize_prose(o[':question/problem']));fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
 if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==G.normalize_tex(of[':answer-field/correct'][':answer/value']);fidelity['keys']+=1
 if ':question/worked-solution'in o:
  old=o[':question/worked-solution']
  if sid=='q-17019':old=old.replace('^{3/2}','^{2/3}')
  old=old.replace('final answer in terms of $u$ at the very end','final answer in terms of $'+t['variable']+'$ at the very end');assert q[':question/worked-solution']==G.normalize_prose(old),(sid,'source solution repaired fidelity');fidelity['solutions']+=1
 else:fidelity['incomplete']+=1
N={};seen={l:set()for l in G.LEVELS}
def check(r):
 q,m=r['question'],r['generation'];domain=m['domain'];lower=domain['base_lower_exclusive'];assert lower in(0,2);F,U,n=A.check(q,lower,positive=True);a=s.diff(U,x);b=U.subs(x,0);assert s.Rational(domain['boundary'])==(lower-b)/a and domain['relation']==('>'if a>0 else'<');assert domain['number_system']=='real';fp=s.srepr(s.simplify(F.subs(x,A.coordinate(U,lower))))+'|'+str(a)+'|'+str(b);level=q[':question/difficulty'].split('/')[-1];seen[level].add(fp)
 for k,v in n.items():N[k]=N.get(k,0)+v
for i,e in enumerate(json.load(open(D/'native-input.json'))):
 check(e['record'])
 if i%100==0:print('Root fractional actual stages read',i,flush=True)
for level in G.LEVELS:
 for seed in range(18):check(G.generate(level,seed))
 assert len(seen[level])==G.capacity(level),(level,len(seen[level]),G.capacity(level))
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},branch_proof='All comparisons substitute actual affine base W+lower with W positive; no forced power identities outside declared real interval.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

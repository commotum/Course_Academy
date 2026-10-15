"""Root actual primitive families, K>0, arbitrary-C rewrite and both real intervals."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186105720;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_log_constant_gen',D.with_suffix('.py'));P=load('root_log_constant_math',R/'elementary-integral-readback.py');x=P.x;kc=P.P.locals_['k'];kp=s.Symbol('positive_K',positive=True);W=s.Symbol('positive_x',positive=True);oldscalar=P.scalar
P.scalar=lambda t:oldscalar(re.sub(r'(?<![A-Za-z\\])K(?![A-Za-z])','k',t))
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,incomplete=0)
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];q=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile'])['question'];assert q[':question/problem']==o[':question/problem'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
 if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fidelity['keys']+=1
 else:assert ':answer-field/correct'not in f
 if ':question/worked-solution'in o:assert q[':question/worked-solution']==o[':question/worked-solution'];fidelity['solutions']+=1
 else:assert ':question/worked-solution'not in q;fidelity['incomplete']+=1
@lru_cache(maxsize=40000)
def branch(expr,sign):return s.expand_log(expr.subs(kc,kp).subs(x,sign*W))
@lru_cache(maxsize=40000)
def eq(a,b,sign):
 delta=branch(a-b,sign);return delta==0 or s.cancel(delta)==0 or s.simplify(delta)==0
N=dict(records=0,interval_checks=0,constant_definitions=0,integral_sides=0,primitive_sides=0,formal_inputs=0,primitive_family_equalities=0,values=0,pairs=0);seen={l:set()for l in G.SUPPORTED_LEVELS}
def check(r):
 q,m=r['question'],r['generation'];assert not m['evidence_only']and m['eligible_for_learning'];assert 'positive'in m['domain']['K'];F,var=P.prompt(q[':question/problem']);assert var==x;sol=q[':question/worked-solution'];c=s.residue(F,x,0);assert c!=0
 cm=re.search(r'\$C=([^$]+)\$',sol);assert cm;relation=P.scalar(cm[1]);assert eq(relation,c*s.log(kc),1);N['constant_definitions']+=1
 f=q[':question/answer-fields'][0];vals=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];correct=next(v for a,v in zip(f[':answer-field/choices'],vals)if a[':answer/id']==f[':answer-field/correct'][1]);ds=[P.derivative(v,x)for v in vals]
 for sign in(-1,1):
  assert[a[':answer/id']for a,d in zip(f[':answer-field/choices'],ds)if eq(d,F,sign)]==[f[':answer-field/correct'][1]]
  for i,d in enumerate(ds):
   for e in ds[:i]:assert not eq(d,e,sign);N['pairs']+=1
  for b in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
   if r'\int'not in b:continue
   text=re.sub(r'\\(?:begin|end)\{aligned\}','',b).replace('&','')
   for row in text.split(r'\\'):
    for part in row.split('='):
     if not part.strip():continue
     value,formal=P.side(part,x);assert eq(value,F,sign),('actual reciprocal/log stage',m['template'],m['parameters'],sign,part,value,F);N['integral_sides'if formal else'primitive_sides']+=1;N['formal_inputs']+=len(formal)
     if not formal:
      actual=P.scalar(part).subs(P.C,relation);assert eq(actual,correct,sign),('arbitrary constant rewrite',m['template'],part,actual,correct);N['primitive_family_equalities']+=1
  N['interval_checks']+=1
 N['records']+=1;N['values']+=len(vals);seen[q[':question/difficulty'].split('/')[-1]].add(s.srepr(s.cancel(F)))
for i,e in enumerate(json.load(open(D/'native-input.json'))):
 check(e['record'])
 if i%60==0:print('Root reciprocal logarithmic constant read',i,flush=True)
for level in G.SUPPORTED_LEVELS:
 for seed in range(18):check(G.generate(level,seed))
expected=json.load(open(D/'capacity.json'));print('Expected capacity evidence',expected)
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},constant_proof='Actual residue c at x=0 matches printed C=c ln K with K>0 and c!=0, a bijective reparameterization. Every primitive row equals the designated K-family after this relation on each connected real interval; every formal integral and wrong bank independently differentiated on both signs.',native_limitations='All306radio correct IDs accepted1224wrong IDs rejected;612foreign/malformed transport errors separate. Diagnostic blank K-in-log parser fails, external-C canonical/products pass but legitimate constant shifts/log-argument scaling rejected and log-power rewrites unresolved. No blank normal output or claim that these mathematically valid equivalents are wrong.',approval_scope='Local docs3–7 with true freeform parser/equivalence limits disclosed, all normal response fields radio. No engine edits.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

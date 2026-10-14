"""Root actual direct sin/cos functions, full source banks and point substitutions."""
import sys,importlib.util,json,re,hashlib,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059675;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
P=load(R/'direct-derivative-readback.py','root_sin_cos_reader');G=load(D.with_suffix('.py'),'root_sin_cos_generator');x=P.x
N=dict(records=0,given_formal_inputs=0,formal_derivative_inputs=0,derivative_equalities=0,conclusions=0,values=0,pairs=0,whole_banks=0,blank_completions=0,domains=0,normal_source_anchors=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));snapshot=R/manifest['source_snapshot_roots'][str(source['basis'])];assert source==json.load(open(snapshot/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
F=dict(prompts=0,solutions=0,values=0,refs=0,unrated=0,missing_refs=0)
for t,o in olds.items():
 raw=G.generate('easy',template=t,profile='observed_raw');assert raw['question']==o and raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning'];F['prompts']+=1;F['solutions']+=(':question/worked-solution' in o);F['unrated']+=(':question/difficulty' not in o)
 for f in o[':question/answer-fields']:F['values']+=len(f[':answer-field/choices']);F['refs']+=(':answer-field/correct' in f);F['missing_refs']+=(':answer-field/correct' not in f)
def check(rec):
 q,m=rec['question'],rec['generation'];t=m['template'];prompt=q[':question/problem'];fun,point,name=P.given(prompt);P.stages(q[':question/worked-solution'],fun,point,name,N)
 ans=s.diff(fun,x) if point is None else s.simplify(s.diff(fun,x).subs(x,point));f=q[':question/answer-fields'][0];vals=[P.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert sum(P.eq(v,ans) for v in vals)==1
 assert P.eq(next(v for v,a in zip(vals,f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]),ans)
 for a,b in itertools.combinations(vals,2):assert not P.eq(a,b);N['pairs']+=1
 if f[':answer-field/type'].endswith('blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt and len(vals)==1;N['blank_completions']+=1
 p=m['parameters'];a,b,n=p.get('a'),p.get('b'),p.get('n')
 if t=='q-1847':assert P.eq(fun,a*s.cos(x)+b*s.sin(x));expected=[fun,b*s.cos(x)+a*s.sin(x),ans,-fun,a*s.cos(x)-b*s.sin(x)]
 elif t=='q-30991':assert P.eq(fun,a*(x**n-s.cos(x))+5);expected=[ans,a*x**(n-1)+a*s.sin(x),a*n*x**(n-1)-a*s.sin(x),a*n*x**(n-1)-s.sin(x),a*n*x**(n-1)+s.sin(x)]
 elif t=='q-341383':assert P.eq(fun,s.Rational(a,4)*s.sin(x)+s.Rational(b,4)*x**n);expected=[ans]
 elif t=='q-47985':assert P.eq(fun,-a*s.cos(x)+b*x**(-n));expected=[a*s.sin(x)-b*n*x**(-n+1),-a*s.sin(x)-b*n*x**(-n-1),ans,-a*s.sin(x)+b*n*x**(-n-1),-a*s.sin(x)-b*n*x**(-n)]
 elif t=='q-1900':k=p['k'];assert P.eq(fun,k*(2*x-5*s.cos(x))) and point==s.pi/6;expected=[s.Rational(11,2)*k,s.Rational(21,5)*k,-s.Rational(21,6)*k,ans,s.Rational(9,4)*k]
 elif t=='independent-easy':assert P.eq(fun,a*getattr(s,p['trig'])(x)+b*x**n);expected=[ans]
 elif t=='independent-moderate':assert P.eq(fun,a*getattr(s,p['trig'])(x)+b*x);assert point==s.sympify(p['point']);expected=[ans]
 elif t=='independent-hard':assert P.eq(fun,a*s.cos(x)+b*s.sin(x)+p['c']*x**n+p['d']*x**(-p['m']));expected=[ans]
 else:raise AssertionError(t)
 assert len(expected)==len(vals) and all(sum(P.eq(v,e) for v in vals)==1 for e in expected);N['whole_banks']+=1
 assert 'real x' in m['domain'] and 'radians' in m['domain']
 if t in ('q-47985','independent-hard'):assert 'x != 0' in m['domain']
 N['domains']+=1;N['records']+=1;N['values']+=len(vals)
for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
for t,(level,params) in G.PROFILES.items():
 r=G.generate(level,template=t,parameters=params);check(r);q=r['question'];o=olds[t];assert q[':question/problem']==G.normalize_prose(o[':question/problem'])
 sol=o[':question/worked-solution']
 if t=='q-1900':sol=sol.replace('{f}^{′}(30)',r'{y}^{′}(\frac{\pi }{6})').replace('{f}^{′}(x)','{y}^{′}(x)')
 assert q[':question/worked-solution']==G.normalize_prose(sol);N['normal_source_anchors']+=1
for level,templates in G.LEVEL_TEMPLATES.items():
 for t in templates:
  for seed in (260,261,262):check(G.generate(level,seed,template=t))
for trig in ('sin','cos'):
 for point in ('0','pi/6','pi/3','pi/2','pi','3*pi/2'):
  try:r=G.generate('moderate',template='independent-moderate',parameters={'a':-3,'b':6,'trig':trig,'point':point})
  except ValueError:assert (trig=='cos' and point in ('0','pi')) or (trig=='sin' and point in ('pi/2','3*pi/2'));continue
  check(r)
report=dict(status='passed',source=F,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(report)

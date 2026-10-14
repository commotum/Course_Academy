"""Root actual tangent differentiation, full source/error banks and point stages."""
import sys,importlib.util,json,re,hashlib,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059676;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
P=load(R/'direct-derivative-readback.py','root_tan_reader');G=load(D.with_suffix('.py'),'root_tan_generator');x=P.x
N=dict(records=0,given_formal_inputs=0,formal_derivative_inputs=0,derivative_equalities=0,conclusions=0,values=0,pairs=0,whole_banks=0,blank_completions=0,domains=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));snapshot=R/manifest['source_snapshot_roots'][str(source['basis'])];assert source==json.load(open(snapshot/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
F=dict(prompts=0,solutions=0,values=0,refs=0,unrated=0,missing_refs=0)
for t,o in olds.items():
 raw=G.generate('easy',template=t,profile='observed_raw');assert raw['question']==o and not raw['generation']['eligible'];F['prompts']+=1;F['solutions']+=(':question/worked-solution' in o);F['unrated']+=(':question/difficulty' not in o)
 for f in o[':question/answer-fields']:F['values']+=len(f[':answer-field/choices']);F['refs']+=(':answer-field/correct' in f);F['missing_refs']+=(':answer-field/correct' not in f)
def check(rec):
 q,m=rec['question'],rec['generation'];t=m['template'];prompt=q[':question/problem'];fun,point,name=P.given(prompt);P.stages(q[':question/worked-solution'],fun,point,name,N)
 ans=s.diff(fun,x) if point is None else s.simplify(s.diff(fun,x).subs(x,point));f=q[':question/answer-fields'][0];vals=[P.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert sum(P.eq(v,ans) for v in vals)==1
 assert P.eq(next(v for v,a in zip(vals,f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]),ans)
 for a,b in itertools.combinations(vals,2):assert not P.eq(a,b);N['pairs']+=1
 if f[':answer-field/type'].endswith('blank'):
  assert '{{'+f[':answer-field/key']+'}}' in prompt and len(vals)==1;N['blank_completions']+=1
 a=m['parameters']['a'];b=m['parameters'].get('b',1);c=m['parameters'].get('c',4);sec=s.sec(x)**2
 if t in ('q-341495','q-47983'):
  assert P.eq(fun,a*s.sqrt(x)+b*s.tan(x));assert 'x>0' in m['domain']
  expected=[ans] if t=='q-341495' else [(a+b*s.sqrt(x)*sec)/(2*s.sqrt(x)),(a+2*b*s.sec(s.sqrt(x))**2)/(2*s.sqrt(x)),(a+2*b*x*sec)/(2*s.sqrt(x)),(a+2*b*s.sqrt(x)*s.sec(x))/(2*s.sqrt(x)),ans]
 elif t=='q-70911':
  assert P.eq(fun,a*(x*x-b*s.tan(x))+c);expected=[2*a-a*s.cos(x)**2+c,a-a*b*sec,2*a*x-b*sec,ans,x-a*s.sec(x)+c]
 elif t=='q-30990':expected=[-a*s.csc(x)**2-b*x,-a*sec-b*x,ans,a*s.csc(x)**2+b,a*s.csc(x)-b];assert P.eq(fun,a*s.tan(x)-b*x)
 elif t=='q-47905':expected=[a*s.sec(x)-b*s.cos(x),ans,a*s.sec(x)+b*s.cos(x),a*sec+b*s.cos(x),-a*sec+b*s.cos(x)];assert P.eq(fun,a*s.tan(x)-b*s.sin(x))
 elif t=='q-103081':expected=[b+2*a,b,b-a*s.sqrt(2),-b-2*a,ans];assert point==s.pi/4 and P.eq(fun,b*x-a*s.tan(x))
 elif t=='q-17912':expected=[ans,-a*s.sqrt(2),a/s.sqrt(3),a*s.sqrt(2),a];assert point==s.pi and P.eq(fun,-a*s.tan(x))
 elif t=='q-341825':expected=[ans];assert point==0 and P.eq(fun,a*s.tan(x)-b*x*x)
 elif t=='q-341858':expected=[ans];assert point==0 and P.eq(fun,a*s.tan(x)+b*s.sin(x))
 elif t=='authored-point':
  assert P.eq(fun,b*x-a*s.tan(x));assert point in (0,s.pi/4,-s.pi/4,s.pi,-s.pi);sv=s.sec(point);expected=[ans,b+a*sv**2,b,b-a*sv,-b-a*sv**2]
 elif t=='authored-four-term':
  d,n=m['parameters']['d'],m['parameters']['n'];assert P.eq(fun,a*(s.tan(x)+b*s.sin(x)-c*s.cos(x))+d*x**n)
  expected=[ans,a*(s.sec(x)+b*s.cos(x)+c*s.sin(x))+d*n*x**(n-1),a*(sec+b*s.cos(x)-c*s.sin(x))+d*n*x**(n-1),a*(sec+b*s.cos(x)+c*s.sin(x))+d*x**(n-1),sec+b*s.cos(x)+c*s.sin(x)+d*n*x**(n-1)]
 else:raise AssertionError(t)
 if f[':answer-field/type'].endswith('blank'):expected=[ans]
 assert len(expected)==len(vals) and all(sum(P.eq(v,e) for v in vals)==1 for e in expected);N['whole_banks']+=1
 assert 'cos(x)!=0' in m['domain'];N['domains']+=1;N['records']+=1;N['values']+=len(vals)
for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
for t in G.LEVEL_TEMPLATES['easy']+G.LEVEL_TEMPLATES['moderate']+G.LEVEL_TEMPLATES['hard']:
 level=next(l for l,ts in G.LEVEL_TEMPLATES.items() if t in ts)
 for seed in (220,221,222):check(G.generate(level,seed,template=t))
 for params in ([G.PROFILES[t][1]] if t in G.PROFILES else []):check(G.generate(level,template=t,parameters=params))
for point in range(5):
 for kind in ('blank','radio'):
  try:rec=G.generate('moderate',template='authored-point',parameters={'a':2,'b':3,'point':point},field_type=kind)
  except ValueError:assert kind=='radio' and point in (0,3,4);continue
  check(rec)
for n in (2,3,4):
 for kind in ('blank','radio'):check(G.generate('hard',template='authored-four-term',parameters={'a':3,'b':2,'c':2,'d':3,'n':n},field_type=kind))
report=dict(status='passed',source=F,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(report)

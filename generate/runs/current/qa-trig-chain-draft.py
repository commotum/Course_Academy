"""Root readback of actual trig chain inputs, bindings/factors and complete source banks."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064281;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 z=importlib.util.spec_from_file_location(name,path);a=importlib.util.module_from_spec(z);z.loader.exec_module(a);return a
G=load('root_chain_generator',D.with_suffix('.py'));P=load('root_chain_math',R/'trig-chain-readback.py');F=load('root_chain_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D);x,u=P.x,P.u
N=dict(records=0,composite_bindings=0,outer_derivatives=0,inner_derivatives=0,chain_rows=0,evaluation_rows=0,tangent_rows=0,values=0,pairs=0,whole_banks=0,blank_completions=0,domains=0)
def check(rec):
 q,meta=rec['question'],rec['generation'];t=meta['template'];fun,at,y0=P.givens(q[':question/problem']);defs,label,outer,inner=P.bindings(q[':question/worked-solution'],fun);der=s.diff(fun,x);termder=s.diff(defs[label],x);N['composite_bindings']+=1
 sol=P.clean(q[':question/worked-solution']);body=sol.split('Differentiating gives',1)[1].split('We now apply',1)[0]
 # Actual formal derivative identities bind the printed outer variable u and inner x.
 for name,var,wanted in ((label,'u',s.diff(outer,u)),('u','x',s.diff(inner,x))):
  m=re.search(r'\\frac\{\\mathrm\{d\}'+name+r'\}\{\\mathrm\{d\}'+var+r'\}\s*=\s*(.*?)(?=,|\$\$|\\\])',body,re.S);assert m,(name,var,body)
  assert P.eq(P.scalar(m[1]),wanted);N['outer_derivatives' if var=='u' else 'inner_derivatives']+=1
 chain=sol.split('We now apply',1)[1].split('Evaluating at',1)[0]
 if 'Next, we differentiate' in chain:chain=chain.split('Next, we differentiate',1)[0]
 for b in re.findall(r'\$\$(.*?)\$\$',chain,re.S):
  for row in b.split(r'\\'):
   if '=' not in row:continue
   parts=row.replace('&','').split('=');vals=[P.value(z,defs,label,outer,inner).subs(u,inner) for z in parts if z.strip()];assert vals and all(P.eq(z,termder) for z in vals),(t,row,vals,termder);N['chain_rows']+=1
 if at is not None:
  evaluated=s.simplify(der.subs(x,at));evalpart=sol.split('Evaluating at',1)[1].split('Finally,',1)[0]
  for b in re.findall(r'\$\$(.*?)\$\$',evalpart,re.S):
   for row in b.split(r'\\'):
    if '=' not in row:continue
    parts=row.replace('&','').split('=');vals=[P.value(z,defs,label,outer,inner) for z in parts if z.strip() and z.strip()!='m'];assert vals and all(P.eq(z,evaluated) for z in vals),(t,row,vals,evaluated);N['evaluation_rows']+=1
 else:evaluated=der
 tangent='tangent at the point' in q[':question/worked-solution'] or 'equation of the tangent' in q[':question/problem']
 answer=evaluated
 if tangent:
  assert at is not None and y0 is not None;answer=s.simplify(evaluated*x+y0-evaluated*at)
  part=sol.split('Finally,',1)[1]
  # Formal first point-slope identity, followed by actual point/m/line identities.
  assert re.search(r'y\s*-\s*(?:\{y\}_?\{?1\}?|y_1)\s*&?\s*=\s*m\s*\(x\s*-\s*(?:\{x\}_?\{?1\}?|x_1)\)',part),part
  for b in re.findall(r'\$\$(.*?)\$\$',part,re.S):
   for row in b.split(r'\\'):
    if '=' not in row or '_1' in row or '_{1}' in row:continue
    parts=row.replace('&','').split('=');vals=[]
    for a in parts:
     a=a.strip()
     if not a:continue
     vals.append(P.scalar(a).subs(P.P.y,answer))
    assert len(vals)>=2 and all(P.eq(z,vals[0]) for z in vals[1:]),(t,row,vals);N['tangent_rows']+=1
 fs=q[':question/answer-fields'];assert len(fs)==1;field=fs[0];values=[P.scalar(a[':answer/value'].split('=')[-1].strip('$')) for a in field[':answer-field/choices']]
 assert sum(P.eq(v,answer) for v in values)==1 and P.eq(next(v for v,a in zip(values,field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1]),answer)
 for a,b in itertools.combinations(values,2):assert not P.eq(a,b);N['pairs']+=1
 if field[':answer-field/type'].endswith('blank'):assert len(values)==1 and '{{'+field[':answer-field/key']+'}}' in q[':question/problem'];N['blank_completions']+=1
 p=meta['parameters'];a,b,A=p.get('a'),p.get('b'),p.get('A')
 if t=='authored-affine-sine':expected=[answer,A*s.cos(inner),-answer,A*a*s.sin(inner),A*a*s.cos(a*x-b)]
 elif t=='q-1943':expected=[x*s.sin(2*a*x),-x*s.sin(inner),answer,a*x*x*s.sin(2*a*x),a*x*x*s.cos(inner)]
 elif t=='q-1946':expected=[a*s.csc(inner)**2,a*s.cot(inner),answer,a*s.sec(inner),s.sec(inner)**2]
 elif t=='q-31153':expected=[answer,-answer,b*s.cos(2),b*s.cos(6+b),-b*s.cos(6+b)]
 elif t=='q-31163':expected=[-2*s.sin(inner)-9*x*x,-s.cos(inner)-9*x*x,s.sin(inner)-18*x*x,2*s.cos(inner)-18*x*x,answer]
 elif t=='q-51026':expected=[x-s.pi-(A+1),x+s.pi-A,answer,-A*x+A*s.pi,s.Integer(0)]
 else:expected=[answer]
 assert len(expected)==len(values) and all(sum(P.eq(v,e) for v in values)==1 for e in expected);N['whole_banks']+=1
 domain=meta['domain'];assert 'real x' in domain
 if fun.has(s.tan):assert 'cos(' in domain and ') != 0' in domain
 N['domains']+=1;N['records']+=1;N['values']+=len(values)
for rec in json.load(open(R/f'qa/{K}-sampled.json')):check(rec)
for t,l in G.LEVELS.items():
 params=G.parameters_for(t)
 for p in (params[0],params[len(params)//2],params[-1]):check(G.generate(l,template=t,parameters=p))
report=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(report)

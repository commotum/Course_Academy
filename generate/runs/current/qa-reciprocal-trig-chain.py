"""Root readback of actual trig chain inputs, bindings/factors and complete source banks."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064282;D=R.parents[2]/f'generate/scratch/{K}'
def load(name,path):
 z=importlib.util.spec_from_file_location(name,path);a=importlib.util.module_from_spec(z);z.loader.exec_module(a);return a
G=load('root_chain_generator',D.with_suffix('.py'));P=load('root_chain_math',R/'trig-chain-readback.py');F=load('root_chain_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D);x,u=P.x,P.u
N=dict(records=0,composite_bindings=0,outer_derivatives=0,inner_derivatives=0,chain_rows=0,evaluation_rows=0,tangent_rows=0,values=0,pairs=0,whole_banks=0,blank_completions=0,domains=0,sum_rule_rows=0)
def check(rec):
 q,meta=rec['question'],rec['generation'];t=meta['template'];fun,at,y0=P.givens(q[':question/problem']);P.TARGET=at;defs,label,outer,inner=P.bindings(q[':question/worked-solution'],fun);der=s.diff(fun,x);termder=s.diff(defs[label],x);N['composite_bindings']+=1
 sol=P.clean(q[':question/worked-solution']);body=sol.split('Differentiating gives',1)[1].split('We now apply',1)[0]
 # Actual formal derivative identities bind the printed outer variable u and inner x.
 for name,var,wanted in ((label,'u',s.diff(outer,u)),('u','x',s.diff(inner,x))):
  m=re.search(r'\\frac\{\\mathrm\{d\}'+(name if name in ('u','g') else '[fy]')+r'\}\{\\mathrm\{d\}'+var+r'\}\s*=\s*(.*?)(?=,|\$\$|\\\])',body,re.S);assert m,(name,var,body)
  assert P.eq(P.scalar(m[1]),wanted);N['outer_derivatives' if var=='u' else 'inner_derivatives']+=1
 chain=sol.split('We now apply',1)[1].split('Evaluating at',1)[0].split('Therefore, the slope',1)[0]
 if 'Next, we differentiate' in chain:chain=chain.split('Next, we differentiate',1)[0]
 for b in re.findall(r'\$\$(.*?)\$\$',chain,re.S):
  for row in b.split(r'\\'):
   if '=' not in row:continue
   parts=row.replace('&','').split('=');vals=[P.value(z,defs,label,outer,inner).subs(u,inner) for z in parts if z.strip()];assert vals and all(P.eq(z,termder) for z in vals),(t,row,vals,termder);N['chain_rows']+=1
 # Sum-family h derivative and full derivative remain operative source stages.
 if 'h' in defs:
  tail=sol.split('Next, we differentiate',1)[1].split('Evaluating at',1)[0]
  for block in re.findall(r'\$\$(.*?)\$\$',tail,re.S):
   previous=None
   for row in block.split(r'\\'):
    parts=row.replace('&','').split('=')
    if len(parts)<2:continue
    values=[P.value(v,defs,label,outer,inner).subs(u,inner) for v in parts if v.strip()]
    if not parts[0].strip():assert previous is not None;values.insert(0,previous)
    assert all(P.eq(z,values[0]) for z in values[1:]),(t,row,values)
    previous=values[-1];N['sum_rule_rows']+=1
 if at is not None:
  evaluated=s.simplify(der.subs(x,at))
  evalpart=(sol.split('Evaluating at',1)[1] if 'Evaluating at' in sol else sol.split('Therefore, the slope',1)[1]).split('Finally,',1)[0]
  for b in re.findall(r'\$\$(.*?)\$\$',evalpart,re.S):
   for row in b.split(r'\\'):
    if '=' not in row:continue
    row=re.sub(r'\{\|\}_\{x=[^}]*\}', '@@AT_POINT@@',row)
    parts=row.replace('&','').split('=');vals=[]
    for part in parts:
     if not part.strip() or part.strip()=='m':continue
     bar='@@AT_POINT@@' in part;v=P.value(part.replace('@@AT_POINT@@',''),defs,label,outer,inner)
     if bar:v=v.subs(x,at)
     vals.append(v)
    assert vals and all(P.eq(z,evaluated) for z in vals),(t,row,vals,evaluated);N['evaluation_rows']+=1
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
 fs=q[':question/answer-fields'];assert len(fs) in (1,2)
 values=[P.scalar(a[':answer/value'].split('=')[-1].strip('$')) for field in fs for a in field[':answer-field/choices']]
 if len(fs)==2:
  assert tangent and {f[':answer-field/key'] for f in fs}=={'field-1','field-2'}
  for field in fs:
   expected=evaluated if field[':answer-field/key']=='field-1' else s.simplify(y0-evaluated*at)
   assert len(field[':answer-field/choices'])==1 and P.eq(P.scalar(field[':answer-field/choices'][0][':answer/value']),expected)
   assert field[':answer-field/correct']==[':answer/id',field[':answer-field/choices'][0][':answer/id']]
   N['blank_completions']+=1
  # Both inserted fragments form the actual printed y=m*x+intercept equation.
  prompt=q[':question/problem'].split('\n\n',1)[1]
  for field in fs:prompt=prompt.replace('{{'+field[':answer-field/key']+'}}','('+field[':answer-field/choices'][0][':answer/value']+')')
  rhs=prompt.replace('$','').replace('\n','').replace(r'\:','').split('=',1)[1]
  assert P.eq(P.scalar(rhs),answer)
 else:
  field=fs[0];assert sum(P.eq(v,answer) for v in values)==1 and P.eq(next(v for v,a in zip(values,field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1]),answer)
  for a,b in itertools.combinations(values,2):assert not P.eq(a,b);N['pairs']+=1
  if field[':answer-field/type'].endswith('blank'):assert len(values)==1 and '{{'+field[':answer-field/key']+'}}' in q[':question/problem'];N['blank_completions']+=1
 params=meta['parameters'];a=params['a']
 if t=='q-31320':B=2*a;expected=[-B*s.sec(inner)*s.tan(inner),-B*s.csc(inner)*s.tan(inner),s.sec(inner)*s.tan(inner),answer,-B*s.sec(x)*s.tan(x)]
 elif t=='q-31338':expected=[-(a+2),a+2,at,s.Integer(-1),s.Integer(1)]
 elif t=='q-31340':expected=[s.Integer(0),s.Integer(-1),2*a+3,s.Integer(1),-(2*a+3)]
 elif t=='q-48512':expected=[at,s.Integer(0),x-at,evaluated*x-at,answer]
 elif len(fs)==2:expected=[evaluated,s.simplify(y0-evaluated*at)]
 else:expected=[answer]
 assert len(expected)==len(values) and all(sum(P.eq(v,e) for v in values)==1 for e in expected);N['whole_banks']+=1
 domain=meta['domain'];assert 'Real x' in domain
 trig=next(iter(fun.atoms(s.sec,s.csc,s.cot)));assert ('cos(' if trig.func==s.sec else 'sin(') in domain and ') != 0' in domain
 N['domains']+=1;N['records']+=1;N['values']+=len(values)
for rec in json.load(open(R/f'qa/{K}-sampled.json')):check(rec)
for t,l in G.LEVELS.items():
 if l=='unrated':continue
 for a in (1,4,8 if t=='q-310222' else 9):check(G.generate(l,template=t,parameters={'a':a}))
try:G.generate('easy',template='q-310222',parameters={'a':9})
except ValueError:pass
else:raise AssertionError('unsupported native bound served')
report=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(report)

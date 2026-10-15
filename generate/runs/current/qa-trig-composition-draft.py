"""Root nested-trig bindings, full/fragment banks, actual targets and pole roles."""
import sys,importlib.util,json,re,itertools,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064284;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 z=importlib.util.spec_from_file_location(name,path);a=importlib.util.module_from_spec(z);z.loader.exec_module(a);return a
G=load('root_composition_generator',D.with_suffix('.py'));P=load('root_composition_math',R/'trig-chain-readback.py');F=load('root_composition_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D);x,u=P.x,P.u;C=load('root_composition_fast',R/'chain-combination-readback.py');P.eq=C.eq
N=dict(records=0,composite_bindings=0,formal_outer_derivatives=0,formal_inner_derivatives=0,chain_rows=0,evaluation_rows=0,tangent_rows=0,values=0,pairs=0,whole_banks=0,fragment_completions=0,domains=0)
def check(rec):
 q,m=rec['question'],rec['generation'];t=m['template'];assert m['parameters']['b']==0;fun,at,y0=P.givens(q[':question/problem']);P.TARGET=at;defs,label,outer,inner=P.bindings(q[':question/worked-solution'],fun);der=s.diff(fun,x);N['composite_bindings']+=1
 sol=P.clean(q[':question/worked-solution']);body=sol.split('Differentiating gives',1)[1].split('We now apply',1)[0]
 for name,var,wanted in ((label,'u',s.diff(outer,u)),('u','x',s.diff(inner,x))):
  match=re.search(r'\\frac\{\\mathrm\{d\}'+name+r'\}\{\\mathrm\{d\}'+var+r'\}\s*=\s*(.*?)(?=,|\$\$|\\\])',body,re.S);assert match,(name,var,body);assert P.eq(P.scalar(match[1]),wanted);N['formal_outer_derivatives' if var=='u' else 'formal_inner_derivatives']+=1
 chain=sol.split('We now apply',1)[1].split('Evaluating at',1)[0]
 for block in re.findall(r'\$\$(.*?)\$\$',chain,re.S):
  for row in block.split(r'\\'):
   parts=row.replace('&','').split('=');values=[P.value(z,defs,label,outer,inner).subs(u,inner) for z in parts if z.strip()];assert values and all(P.eq(z,der) for z in values),(t,row,values,der);N['chain_rows']+=1
 tangent=t=='q-48644';answer=der
 if tangent:
  assert at is not None and y0 is not None;rate=s.simplify(der.subs(x,at));answer=s.simplify(rate*x+y0-rate*at)
  for block in re.findall(r'\$\$(.*?)\$\$',sol.split('Evaluating at',1)[1].split('Finally,',1)[0],re.S):
   for row in block.split(r'\\'):
    values=[P.value(z,defs,label,outer,inner) for z in row.replace('&','').split('=') if z.strip()];assert all(P.eq(z,rate) for z in values),(row,values,rate);N['evaluation_rows']+=1
  for block in re.findall(r'\$\$(.*?)\$\$',sol.split('Finally,',1)[1],re.S):
   for row in block.split(r'\\'):
    if '_1' in row or '_{1}' in row:continue
    parts=row.replace('&','').split('=');values=[P.scalar(z).subs(P.P.y,answer) for z in parts if z.strip()];assert len(values)>=2 and all(P.eq(z,values[0]) for z in values[1:]),(row,values);N['tangent_rows']+=1
 fs=q[':question/answer-fields'];isradio=fs[0][':answer-field/type'].endswith('radio')
 if isradio:
  assert len(fs)==1 and len(fs[0][':answer-field/choices'])==5;f=fs[0];values=[P.scalar(a[':answer/value']) for a in f[':answer-field/choices']]
  assert sum(P.eq(v,answer) for v in values)==1 and P.eq(next(v for v,a in zip(values,f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]),answer)
  for a,b in itertools.combinations(values,2):assert not P.eq(a,b);N['pairs']+=1
  z=x+m['parameters']['b'];S=s.sin(z);C=s.cos(z);a=m['parameters'].get('a',1)
  if t=='authored-easy':
   oname,iname=m['parameters']['outer'],m['parameters']['inner'];outerfun=getattr(s,oname)(u);innerfun=getattr(s,iname)(x);od=s.diff(outerfun,u);id=s.diff(innerfun,x);other=s.cos(x) if iname=='sin' else s.sin(x);expected=[der,a*od.subs(u,innerfun),-der,a*outerfun.subs(u,innerfun)*id,a*od.subs(u,other)*id]
  elif t=='q-31356':expected=[a*S*s.cot(C)**2,der,a*s.csc(z)*s.sin(C)**2,a*S*s.cos(s.csc(z))**2,a*s.csc(z)*s.cos(S)**2]
  elif t=='q-48643':expected=[-a*C*s.sin(C),der,-a*S*s.cos(S),-a*C*s.cos(S),-a*S*s.sin(C)]
  elif t=='q-72161':expected=[-a*C*s.csc(C)**2,der,-a*s.csc(S)**2,a*s.csc(C)**2,a*C*s.csc(C)**2]
  elif t=='q-72173':expected=[a*s.sec(z)*s.tan(-S),a*S*s.sec(-S)*s.tan(-S),a*C*s.sec(C)*s.tan(C),a*S*s.sec(z)*s.tan(C),der]
  else:raise AssertionError(t)
  assert all(sum(P.eq(v,e) for v in values)==1 for e in expected);N['whole_banks']+=1
 else:
  assert all(f[':answer-field/type'].endswith('blank') and len(f[':answer-field/choices'])==1 for f in fs)
  values=[P.scalar(f[':answer-field/choices'][0][':answer/value']) for f in fs]
  for f in fs:assert f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][0][':answer/id']]
  text=q[':question/problem'].split('\n\n',1)[1]
  for f in fs:text=text.replace('{{'+f[':answer-field/key']+'}}','('+f[':answer-field/choices'][0][':answer/value']+')')
  text=text.replace('$','').replace('\n','').replace(r'\,','');left,right=text.split('=',1);assert P.eq(P.scalar(right),answer),(t,text,answer);N['fragment_completions']+=len(fs)
 domain=m['domain'];assert domain['real_x'];restr=domain['restriction'];on,inn=(m['parameters']['outer'],m['parameters']['inner']) if t=='authored-easy' else G.OPS[t]
 if inn in ('csc','cot'):assert 'sin' in restr and '!= 0' in restr
 if inn in ('sec','tan'):assert 'cos' in restr and '!= 0' in restr
 if on in ('cot','csc'):assert 'sin(' in restr and '!= 0' in restr
 if on in ('tan','sec'):assert 'cos(' in restr and '!= 0' in restr
 if on not in ('cot','csc','sec','tan') and inn not in ('cot','csc','sec','tan'):assert restr=='all real x'
 N['records']+=1;N['values']+=len(values);N['domains']+=1
for rec in json.load(open(R/f'qa/{K}-sampled.json')):check(rec)
for t,level in G.LEVELS.items():
 if t in ('q-72163','q-72170','q-342436'):continue
 params=G.parameters_for(t)
 for p in (params if t=='authored-easy' else (params[0],params[len(params)//2],params[-1])):check(G.generate(level,template=t,parameters=p))
for t in ('q-72163','q-72170','q-342436'):
 try:G.generate('moderate',template=t)
 except ValueError:pass
 else:raise AssertionError('native-unsupported template served')
report=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(report)

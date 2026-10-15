"""Root normal-equation fields, operative derivative inputs and full source banks."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186092240;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_ne_gen',D.with_suffix('.py'));P=load('root_ne_math',R/'qa-normal-intercept-draft.py');F=load('root_ne_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D);x,y=P.x,P.y
N=dict(records=0,points=0,bindings=0,formal_targets=0,formal_operands=0,equalities=0,normal_equations=0,values=0,pairs=0,banks=0,completed_fields=0,contexts=0,domains=0)
def check(r):
 q,m=r['question'],r['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];profile=m['profile'];context='y=f(x)' in prompt;P.POSITIVE=not context
 bindings={}
 if context:
  defs=re.search(r'Use \$f\(x\)=(.*?)\$ and \$h\(x\)=(.*?)\$',prompt);assert defs;bindings={'f':P.scalar(defs[1]),'h':P.scalar(defs[2])};fun=bindings['f']*bindings['h'];at=s.pi;y0=s.simplify(fun.subs(x,at));N['contexts']+=1
  givenheight=re.search(r'\$y\(\\pi\)=(.*?)\$',prompt);givenslope=re.search(r'\$m=(.*?)\$',prompt);assert givenheight and givenslope
  assert P.eq(P.scalar(givenheight[1]),y0) and P.eq(P.scalar(givenslope[1]),s.diff(fun,x).subs(x,at))
 else:
  match=re.search(r'\$y\s*=\s*(.*?)\$',prompt);assert match;fun=P.scalar(match[1]);match=re.search(r'point \$(.*?)\$',prompt);assert match;at,y0=P.point(match[1].rstrip('.'));assert P.eq(fun.subs(x,at),y0);N['points']+=1
 df=s.diff(fun,x);slope=s.simplify(df.subs(x,at));assert slope.is_finite and slope!=0;normal=x+slope*y-(at+slope*y0);coeff={'p':slope,'q':at+slope*y0,'a':-1/slope,'b':y0+at/slope}
 def value(raw):
  raw=P.clean(raw).replace('{y}_{1}','('+s.latex(y0)+')').replace('{x}_{1}','('+s.latex(at)+')')
  for name,expr in bindings.items():
   def named(match):
    arg=P.scalar(match[1]);assert P.eq(arg,at),('prior-part function target',arg,at);return '('+s.latex(expr.subs(x,arg),root_notation=False)+')'
   raw=re.sub(name+r'\((.*?)\)',named,raw)
  def namedcurve(match):
   arg=P.scalar(match[1]);assert P.eq(arg,at);return '('+s.latex(fun.subs(x,arg),root_notation=False)+')'
  raw=re.sub(r'y\((.*?)\)',namedcurve,raw)
  for name,expr in coeff.items():raw=re.sub(r'(?<![A-Za-z])'+name+r'(?![A-Za-z])',lambda _: '('+s.latex(expr,root_notation=False)+')',raw)
  before=dict(P.N);answer=P.value(raw,fun,at,slope);N['formal_targets']+=P.N['derivative_targets']-before['derivative_targets'];N['formal_operands']+=P.N['derivative_operands']-before['derivative_operands'];return answer
 let=re.search(r'Let \$f\(x\)=(.*?)\$',sol)
 if let:assert P.eq(P.scalar(let[1]),fun);N['bindings']+=1
 for pt in re.findall(r'point \$(.*?)\$',sol):
  pp,yy=P.point(pt.rstrip(':'));assert P.eq(pp,at) and P.eq(yy,y0);N['points']+=1
 text=P.clean(sol)
 for op in P.P.DERS:
  if op in text:
   pos=text.index(op)+len(op)
   while text[pos].isspace():pos+=1
   operand,_=P.P.group(text,pos);assert P.eq(P.scalar(operand),fun);break
 for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
  block=re.sub(r'\\(?:begin|end)\{aligned\}','',block);carry=None
  for row in block.split(r'\\'):
   parts=row.replace('&','').split('=');assert len(parts)>=2,(profile,row)
   if parts[0].strip():carry=parts[0]
   else:assert carry is not None;parts[0]=carry
   vals=[value(z) for z in parts]
   for a,b in zip(vals,vals[1:]):
    residual=s.expand(a-b)
    if P.eq(residual,0):pass
    else:ratio=s.cancel(residual/normal);assert not ratio.free_symbols and ratio!=0,(profile,row,residual);N['normal_equations']+=1
    N['equalities']+=1
 for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',sol,re.S):
  if re.match(r'^(?:a\+b|p\+q|p-q|q-p)=',inline):
   vals=[value(z) for z in inline.split('=')];assert all(P.eq(z,vals[0]) for z in vals)
 fields=q[':question/answer-fields'];allblank=all(f[':answer-field/type'].endswith('/blank') for f in fields)
 if len(fields)==2:
  tail=prompt.split('\n\n',1)[1]
  for f in fields:tail=tail.replace('{{'+f[':answer-field/key']+'}}','('+f[':answer-field/choices'][0][':answer/value']+')')
  left,right=tail.replace('$','').replace('\n','').split('=');ratio=s.cancel((P.scalar(left)-P.scalar(right))/normal);assert not ratio.free_symbols and ratio!=0;N['completed_fields']+=2
  lead=re.search(r'\$([^$]*x[^$]*[+-])\$\s*\{\{field-1\}\}',prompt);assert lead;L=P.scalar(lead[1][:-1]).coeff(x);answers={'field-1':abs(L*slope),'field-2':L*(at+slope*y0)};assert (lead[1][-1]=='+')==(slope>0)
 elif context:answers={fields[0][':answer-field/key']:-1/slope*(x-at)+y0};N['completed_fields']+=1
 else:
  target=re.search(r'Find the value of \$(.*?)\$',prompt);assert target;wanted=value(target[1]);answers={fields[0][':answer-field/key']:wanted}
 for f in fields:
  vals=[P.scalar(z[':answer/value']) for z in f[':answer-field/choices']];answer=answers[f[':answer-field/key']];assert sum(P.eq(z,answer) for z in vals)==1 and P.eq(next(z for z,a in zip(vals,f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]),answer)
  for a,b in itertools.combinations(vals,2):assert not P.eq(a,b);N['pairs']+=1
  if not allblank:
   if profile=='q-47406':expected=[77,74,66,56,58]
   elif profile=='q-47408':expected=[y0+1/(2*slope),answer,y0+2/slope,y0+4/slope,y0+1/slope]
   elif profile=='q-103546':expected=[-slope*y0,answer,-at,-y0,y0-at]
   elif profile=='q-47409':expected=[coeff['p']+coeff['q'],answer,-coeff['p']-coeff['q'],at,-2*slope+y0]
   elif profile=='q-47410':expected=[coeff['q'],coeff['q']-slope,-slope-coeff['q'],slope+coeff['q'],-coeff['q']]
   else:raise AssertionError(profile)
   assert len(vals)==len(expected) and all(sum(P.eq(z,w) for z in vals)==1 for w in expected)
  N['values']+=len(vals);N['banks']+=1
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
 if fun.has(s.Pow) and any(not power.exp.is_integer or power.exp.is_negative for power in fun.atoms(s.Pow) if power.base.has(x)):assert at>0
 N['domains']+=1;N['records']+=1
for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
for level in ('easy','moderate','hard'):
 ps=G.authored_parameters(level)
 for p in (ps[0],ps[len(ps)//2],ps[-1]):check(G.generate(level,parameters=p))
for profile in G.T:
 for p in G.source_parameters(profile):check(G.generate('moderate',profile=profile,parameters=p))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

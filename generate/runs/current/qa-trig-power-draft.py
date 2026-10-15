"""Root power-chain actual function/variable roles, operators, whole banks and fragments."""
import sys,json,re,hashlib,importlib.util,copy,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064283;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 z=importlib.util.spec_from_file_location(name,path);a=importlib.util.module_from_spec(z);z.loader.exec_module(a);return a
G=load('root_power_generator',D.with_suffix('.py'));P=load('root_power_math',R/'trig-chain-readback.py');F=load('root_power_fidelity',R/'root-source-fidelity.py');M=load('root_power_markdown',R.parents[2]/'scripts/question_capture/math_format.py');originals,fidelity=F.check(G,K,D);x,u=P.x,P.u
N=dict(records=0,source_expression_rows=0,composite_bindings=0,outer_derivatives=0,inner_derivatives=0,chain_rows=0,values=0,pairs=0,whole_banks=0,fragment_completions=0,velocity_roles=0,domains=0)
def canonical_math(text,velocity):
 if not velocity:return text
 def remap(m):
  v=m[0];v=v.replace('a(t)',"f'(x)").replace('v(t)','f(x)')
  return re.sub(r'\\(?:operatorname|text|mathrm)\{[^}]*\}|\\[A-Za-z]+|\{(?:sin|cos|tan|cot|sec|csc)\}|[vt]|.',lambda z:{'v':'f','t':'x'}.get(z[0],z[0]),v,flags=re.S)
 return M.MATH.sub(remap,text)
def check(rec):
 q,meta=rec['question'],rec['generation'];t=meta['template'];velocity=bool(re.search(r'\$v\(t\)=',q[':question/problem']));prompt=canonical_math(q[':question/problem'],velocity);sol=canonical_math(q[':question/worked-solution'],velocity);fun,at,y0=P.givens(prompt);assert at is None;P.TARGET=None;defs,label,outer,inner=P.bindings(sol,fun)
 trig=list(fun.atoms(s.sin,s.cos,s.csc));assert len(trig)==1 and trig[0].args[0]==x;base=trig[0];n=fun.as_powers_dict()[base];c=s.cancel(fun/base**n);assert c.is_Integer and n.is_Integer and n>0;der=s.diff(fun,x);N['composite_bindings']+=1
 text=P.clean(sol);head=text.split('Now, we see',1)[0]
 for block in re.findall(r'\$\$(.*?)\$\$',head,re.S):
  parts=block.split('=');assert len(parts)==2 and all(P.eq(P.value(z,defs,label,outer,inner),fun) for z in parts);N['source_expression_rows']+=1
 body=text.split('Differentiating, we get',1)[1].split('We now apply',1)[0]
 for name,var,wanted in ((label,'u',s.diff(outer,u)),('u','x',s.diff(inner,x))):
  m=re.search(r'\\frac\{\\mathrm\{d\}'+name+r'\}\{\\mathrm\{d\}'+var+r'\}\s*=\s*(.*?)(?=,|\$\$|\\\])',body,re.S);assert m,(t,body);assert P.eq(P.scalar(m[1]),wanted);N['outer_derivatives' if var=='u' else 'inner_derivatives']+=1
 for block in re.findall(r'\$\$(.*?)\$\$',text.split('We now apply',1)[1],re.S):
  for row in block.split(r'\\'):
   values=[P.value(z,defs,label,outer,inner).subs(u,inner) for z in row.replace('&','').split('=') if z.strip()];assert values and all(P.eq(z,der) for z in values),(t,row,values,der);N['chain_rows']+=1
 field=q[':question/answer-fields'][0];values=[P.scalar(a[':answer/value'].strip('$')).subs(P.P.t,x) if velocity else P.scalar(a[':answer/value'].strip('$')) for a in field[':answer-field/choices']]
 answer=der/s.cot(x) if velocity else der;assert sum(P.eq(v,answer) for v in values)==1 and P.eq(next(v for a,v in zip(field[':answer-field/choices'],values) if a[':answer/id']==field[':answer-field/correct'][1]),answer)
 for a,b in itertools.combinations(values,2):assert not P.eq(a,b);N['pairs']+=1
 S,C=s.sin(x),s.cos(x);A=abs(c);k=A*n
 if t in ('q-48562','q-48385'):expected=[-n*C**(n-1)*S,-n*S**(n-1),n*C*S**(n-1),n*C**(n-1)*S,n*C**(n-1)]
 elif t=='q-48560':expected=[-S*C,-2*C**2,-2*S*C,2*S*C,C**2]
 elif t=='q-72154':expected=[-A*S*C,2*A*S*C,-A*C**2,2*A*S*C**2,2*A*S]
 elif t=='q-72156':expected=[-A*S**(n-1),A*C*S**(n-1),-k*C*S**(n-1),-k*C**(n-1)*S,k*C**(n-1)]
 elif t=='q-72157':expected=[-k*C*S**(n-1),-k*C**(n-1)*S,-k*S**(n-1),A*C*S**(n-1),A*C**(n-1)]
 else:expected=[answer]
 assert len(expected)==len(values) and all(sum(P.eq(v,e) for v in values)==1 for e in expected);N['whole_banks']+=1
 if field[':answer-field/type'].endswith('blank'):
  text=prompt.split('\n\n',1)[1].replace('{{'+field[':answer-field/key']+'}}','('+canonical_math('$'+field[':answer-field/choices'][0][':answer/value']+'$',velocity).strip('$')+')').replace('$','').replace('\n','');rhs=text.split('=',1)[1];assert P.eq(P.scalar(rhs),der),(t,rhs,der);N['fragment_completions']+=1
 domain=meta['domain'];assert domain['variable']==('t' if velocity else 'x')
 if base.func==s.csc:assert domain['restriction']=='sin('+domain['variable']+') != 0'
 else:assert domain['restriction']=='all real x'
 if velocity:N['velocity_roles']+=1
 N['domains']+=1;N['values']+=len(values);N['records']+=1
for rec in json.load(open(R/f'qa/{K}-sampled.json')):check(rec)
for t,level in G.LEVELS.items():
 params=G.parameters_for(t)
 for p in (params[0],params[len(params)//2],params[-1]):check(G.generate(level,template=t,parameters=p))
report=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(report)

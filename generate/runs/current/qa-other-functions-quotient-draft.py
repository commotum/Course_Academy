"""Root quotient audit: actual ordered operands, every equality, fields and source banks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096621;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);sys.modules[n]=m;z.loader.exec_module(m);return m
G=load('root_otherquotient_gen',D.with_suffix('.py'));P=load('root_otherquotient_scalar',R/'ode-scalar-parser.py');B=load('root_otherquotient_groups',R/'direct-derivative-readback.py');x=P.x
@lru_cache(maxsize=10000)
def parse(t):return P.scalar(t.strip().rstrip('.,').replace('[','(').replace(']',')').replace(r'\cancel',''))
@lru_cache(maxsize=20000)
def eq(a,b):
 d=a-b
 if d==0:return True
 w=s.Symbol('root_circle_w',real=True);circle={s.sin(x):2*w/(1+w*w),s.cos(x):(1-w*w)/(1+w*w),s.tan(x):2*w/(1-w*w),s.sec(x):(1+w*w)/(1-w*w)}
 assert all(f.args[0]==x for f in d.atoms(s.sin,s.cos,s.tan,s.sec))
 # Exact transcendental substitutions keep the rational proof small. e^(kx)
 # becomes E0^k with E0=e^x; log(x) is kept independent. No forced log laws.
 e0=s.Symbol('root_E0',positive=True);l0=s.Symbol('root_L0',real=True)
 replacements={s.log(x):l0}
 numerator=d.as_numer_denom()[0]
 for term in numerator.atoms(s.exp):
  k=s.cancel(term.args[0]/x)
  if k.is_Integer:replacements[term]=e0**k
 numerator=numerator.xreplace(circle).xreplace(replacements)
 numerator=s.together(numerator).as_numer_denom()[0]
 return s.expand(numerator)==0
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};N=dict(raw_records=0,records=0,bindings=0,formal_derivatives=0,stages=0,points=0,values=0,pairs=0,fragment_contexts=0,source_banks=0,source_values=0,source_keys=0,scaled_bank_values=0);tasks={l:set()for l in G.SUPPORTED_LEVELS}
def quotient(raw):
 raw=raw.strip().rstrip('.,');assert raw.startswith(r'\frac');a,e=B.group(raw,5);b,e=B.group(raw,e);assert not raw[e:];return parse(a),parse(b)
def given(prompt):
 if '$h(x)='in prompt:
  u=parse(re.search(r'\$f\(x\)=(.*?)\$',prompt)[1]);v=parse(re.search(r'\$h\(x\)=(.*?)\$',prompt)[1])
 else:
  given=re.search(r'\$[fy](?:\(x\))?\s*=\s*(.*?)\$',prompt);assert given;u,v=quotient(given[1])
 point=re.search(r'\$x=(.*?)\$',prompt);return u,v,parse(point[1])if point else None

def formal(t,u,v):
 args=[];subs={};suffix=r'^{\prime}'
 while suffix in t:
  end=t.index(suffix);assert t[end-1]==')';start=end-2;depth=1
  while depth:
   depth+=(t[start]==')')-(t[start]=='(');start-=1
  start+=1;arg=parse(t[start+1:end-1]);token=('i','j')[len(args)];args.append(arg);subs[P.locals_[token]]=s.diff(arg,x);t=t[:start]+token+t[end+len(suffix):]
 assert len(args)==2 and eq(args[0],u)and eq(args[1],v);N['formal_derivatives']+=2
 return parse(t).subs(subs)
RULE=r'\frac{u^{\prime}(x)\cdot v(x)-u(x)\cdot v^{\prime}(x)}{[v(x)]^{2}}'
def check(r,sid=None):
 q,m=r['question'],r['generation'];u,v,point=given(q[':question/problem']);df=s.diff(u/v,x);ans=df if point is None else s.simplify(df.subs(x,point));sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert blocks
 for name,want in [('u',u),('v',v)]:
  binding=re.search(r'\$'+name+r'\(x\)=(.*?)\$',sol)
  if binding:assert eq(parse(binding[1]),want);N['bindings']+=1
 if sol.startswith('Recall'):
  for name,want in [('f',u),('h',v)]:assert eq(parse(re.search(r'\$'+name+r'\(x\)=(.*?)\$',sol)[1]),want);N['bindings']+=1
 count=0
 for bi,block in enumerate(blocks):
  evaluation=point is not None and bi==len(blocks)-1
  if evaluation:
   lhs=block.split('&',1)[0];target=re.search(r'\((.*)\)',lhs);assert target and eq(parse(target[1]),point);assert v.subs(x,point)!=0;N['points']+=1
  for ri,row in enumerate(block.split(r'\\')):
   _,rhs=row.split('&=',1);rhs=rhs.strip();count+=1
   if bi==0 and ri==0:assert rhs==RULE;continue
   val=formal(rhs,u,v)if r'^{\prime}'in rhs else parse(rhs);assert eq(val,ans if evaluation else df),('rendered quotient stage',m['template'],rhs,val,df,point);N['stages']+=1
 counts={'q-17921':5,'q-47999':5,'q-340318':8,'q-9908':11,'q-167328':5,'q-167782':5,'q-166075':5,'q-2385':5,'q-340308':4,'q-340309':4,'q-340316':7,'q-47943':4,'q-47998':5,'q-48504':8,'q-48507':9,'authored-hard-sums':5};assert count==counts[m['template']]
 if point is not None:
  stated=re.search(r'Therefore, the slope of the tangent line(?: at \$x=.*?\$)? is \$(.*?)\$',sol);assert stated and eq(parse(stated[1]),ans)
 f=q[':question/answer-fields'][0];values=[parse(a[':answer/value'])for a in f[':answer-field/choices']];target=ans
 if m['template']=='q-167782':
  table=[z for z in q[':question/problem'].splitlines()if z.startswith('|')];assert len(table)==3;num=table[0].split('|')[2].replace('$','').replace('{{'+f[':answer-field/key']+'}}','('+f[':answer-field/choices'][0][':answer/value']+')');den=table[2].split('|')[2].replace('$','');assert eq(parse(num)/parse(den),df);target=s.cos(x)-s.sin(x);N['fragment_contexts']+=1
 assert[a[':answer/id']for a,z in zip(f[':answer-field/choices'],values)if eq(z,target)]==[f[':answer-field/correct'][1]]
 for i,z in enumerate(values):
  for w in values[:i]:assert not eq(z,w);N['pairs']+=1
 if sid:
  o=olds[sid]
  for of in o.get(':question/answer-fields',[]):
   original=[parse(a[':answer/value'])for a in of[':answer-field/choices']];assert len(values)==len(original)and all(sum(eq(z,w)for w in values)==1 for z in original);N['source_banks']+=1;N['source_values']+=len(values)
   if ':answer-field/correct'in of:assert eq(parse(of[':answer-field/correct'][':answer/value']),target);N['source_keys']+=1
 N['records']+=1;N['values']+=len(values);tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(s.cancel(u/v)),str(point)))
for sid,o in olds.items():
 print('source',sid,flush=True)
 assert G.replay_raw(sid)['question']==o;N['raw_records']+=1;p=G.original_parameters(sid);check(G.generate(G.SPEC[sid][3],template=sid,parameters=p),sid)
 if o.get(':question/answer-fields') and sid!='q-167782':
  q=G.generate(G.SPEC[sid][3],template=sid,parameters=dict(p,scale=2))['question'];orig=[parse(a[':answer/value'])for a in o[':question/answer-fields'][0][':answer-field/choices']];vals=[parse(a[':answer/value'])for a in q[':question/answer-fields'][0][':answer-field/choices']];assert len(orig)==len(vals)and all(sum(eq(2*z,w)for w in vals)==1 for z in orig);N['scaled_bank_values']+=len(vals)
for i,r in enumerate(json.load(open(D/'sample-records.json'))):
 if i>=80 or i%20==0:print('root sample',i,flush=True)
 check(r)
for l in G.SUPPORTED_LEVELS:
 for seed in range(24):check(G.generate(l,seed))
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_tasks={l:len(t)for l,t in tasks.items()},scope='Observed complete quotients, original real domains and exact-point slopes; authored hard two-sum quotient uses same quotient and known basic derivatives without chain extension. Every source bank and coefficient-doubled bank independently read; partial numerator response substituted into actual table.',native_limitations='One genuine -2ln2 versus -ln4 equivalent unresolved; canonical, wrong owned options and response diagnostics separate. Qualified local approval, no engine change.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

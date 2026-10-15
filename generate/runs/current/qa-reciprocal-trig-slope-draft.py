"""Root slope readback: actual points, every nested D operand and scalar banks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
from mpmath import iv
sys.dont_write_bytecode=True;iv.dps=55
R=Path(__file__).resolve().parent;K=17592186115193;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_slope_gen',D.with_suffix('.py'));H=load('root_slope_scalar',R/'direct-derivative-readback.py');x=H.x
parse=lambda t:H.scalar(t.replace('[','(').replace(']',')'))
def interval(e):
 if e==s.pi:return iv.pi
 if e==s.E:return iv.e
 if e.is_Rational:return iv.mpf(int(e.p))/int(e.q)
 if e.is_Add:return sum((interval(a)for a in e.args),iv.mpf(0))
 if e.is_Mul:
  v=iv.mpf(1)
  for a in e.args:v*=interval(a)
  return v
 if e.is_Pow:return interval(e.base)**interval(e.exp)
 if e.func in(s.sin,s.cos,s.tan,s.exp,s.log):return{s.sin:iv.sin,s.cos:iv.cos,s.tan:iv.tan,s.exp:iv.exp,s.log:iv.ln}[e.func](interval(e.args[0]))
 if e.func in(s.sec,s.csc,s.cot):return 1/{s.sec:iv.cos,s.csc:iv.sin,s.cot:iv.tan}[e.func](interval(e.args[0]))
 raise AssertionError(e)
@lru_cache(maxsize=20000)
def eq(a,b):
 d=s.expand(a-b)
 if d==0:return True
 if not d.free_symbols:
  v=interval(d)
  if v.a>0 or v.b<0:return False
 return s.trigsimp(d,method='fu')==0 or s.simplify(d)==0
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fid=dict(records=0,banks=0,values=0,keys=0,solutions=0,fieldless=0)
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];q=G.generate(c['difficulty'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question'];assert q[':question/problem']==o[':question/problem']and q.get(':question/worked-solution')==o.get(':question/worked-solution');fid['records']+=1;fid['solutions']+=':question/worked-solution'in o
 for key in(':question/answer-fields',':question/difficulty',':question/worked-solution'):assert(key in q)==(key in o)
 if not o.get(':question/answer-fields'):fid['fieldless']+=1
 for f,of in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
  assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fid['banks']+=1;fid['values']+=len(f[':answer-field/choices']);assert(':answer-field/correct'in f)==(':answer-field/correct'in of)
  if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fid['keys']+=1
ROWS={'q-1886':(4,2),'q-1905':(2,4),'q-104437':(3,3),'q-340642':(3,3),'q-104442':(2,4),'q-1904':(3,3),'q-340630':(2,3),'q-340660':(5,3),'q-70874':(3,4),'canonical-quotient':(4,4)}
N=dict(records=0,formal_operands=0,stages=0,values=0,pairs=0,points=0,correct_zero=0,correct_one=0);tasks={l:set()for l in('easy','moderate','hard')}
def value(raw,F,name,at,operands):
 t=H.clean(raw).replace(r'\,','');bindings={};df=s.diff(F,x)
 for der in H.DERS:
  while der in t:
   pos=t.index(der);arg,end=H.group(t,pos+len(der));operand=parse(arg);operands.append(operand);token=('i','j','k')[len(bindings)];bindings[H.P.locals_[token]]=s.diff(operand,x);t=t[:pos]+'('+token+')'+t[end:]
 dy=r'\frac{\text{d}y}{\text{d}x}'
 if dy in t:
  pos=t.index(dy);end=pos+len(dy);v=df
  if t.startswith('{|}_',end):
   actual,j=H.group(t,end+len('{|}_'));assert eq(parse(actual),at);v=df.subs(x,at);end=j
  token=('i','j','k')[len(bindings)];bindings[H.P.locals_[token]]=v;t=t[:pos]+'('+token+')'+t[end:]
 pattern=r"\{?([fgh])\}?(?:\^\{['′]\}|')\("
 while (m:=re.search(pattern,t)):
  assert m[1]==name;arg,end=H.group(t,m.end()-1);actual=parse(arg);assert eq(actual,x)or eq(actual,at);token=('i','j','k')[len(bindings)];bindings[H.P.locals_[token]]=df.subs(x,actual);t=t[:m.start()]+'('+token+')'+t[end:]
 if t=='m':return df.subs(x,at)
 return parse(t).subs(bindings)
def check(r):
 q=r['question'];m=r['generation'];sid=m['template'];prompt=q[':question/problem'];match=re.search(r'\$([fgh])\(x\)=(.*?)\$',prompt);assert match;name=match[1];F=parse(match[2]);point=re.search(r'at \$x=(.*?)\$',prompt);assert point;at=parse(point[1]);df=s.diff(F,x);answer=s.simplify(df.subs(x,at));assert at.is_real and F.subs(x,at).is_finite
 if F.has(s.sec,s.tan):assert not eq(s.cos(at),0)
 if F.has(s.csc,s.cot):assert not eq(s.sin(at),0)
 N['points']+=1;sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2;rows=[b.split(r'\\')for b in blocks];assert tuple(map(len,rows))==ROWS[sid];operands=[]
 for bi,rr in enumerate(rows):
  for row in rr:
   for part in row.replace('&','').split('='):
    if part.strip():assert eq(value(part,F,name,at,operands),df if bi==0 else answer),('actual slope stage',sid,part,answer);N['stages']+=1
 expected=[F,F]if sid=='q-1886'else[F,*s.fraction(F)]if sid in('q-340660','canonical-quotient')else[F];assert len(operands)==len(expected)and all(eq(a,b)for a,b in zip(operands,expected));N['formal_operands']+=len(operands)
 rhs=lambda bi,ri:rows[bi][ri].split('=')[-1]
 if sid=='q-1886':assert '{x}^{-1}'in rhs(0,1)
 if sid=='q-340642':assert '+'in rhs(0,1)and ')('in rhs(0,1)and '+'in rhs(0,2)
 if sid=='q-340660':assert r'\sec'in rhs(0,3)and '(1-x'in rhs(0,3)and r'\sec'in rhs(0,4)
 if sid=='canonical-quotient':assert r'\csc^2 x'in rhs(0,2)and r'\csc^2 x'not in rhs(0,3)
 points=re.findall(r'substitute \$x=(.*?)\$',sol);assert len(points)==1 and eq(parse(points[0]),at)
 f=q[':question/answer-fields'][0];vals=[parse(a[':answer/value'])for a in f[':answer-field/choices']];assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if eq(v,answer)]==[f[':answer-field/correct'][1]]
 for i,v in enumerate(vals):
  for w in vals[:i]:assert not eq(v,w);N['pairs']+=1
 if f[':answer-field/type'].endswith('/blank'):assert prompt.split('\n\n',1)[1].startswith('$m=$\n')and '{{'+f[':answer-field/key']+'}}'in prompt
 if answer==0:N['correct_zero']+=1
 if answer==1:N['correct_one']+=1
 N['records']+=1;N['values']+=len(vals)
 if m['profile']==G.default_profile(sid):tasks[q[':question/difficulty'].split('/')[-1]].add(s.srepr(F)+'|'+str(at))
for i,r in enumerate(json.load(open(D/'bounded-records.json'))):
 check(r)
 if i%100==0:print('Root reciprocal-trig slopes read',i,flush=True)
for level in('easy','moderate','hard'):
 for seed in range(18):check(G.generate(level,seed))
assert {l:len(v)for l,v in tasks.items()}==dict(easy=120,moderate=95,hard=72)and N['correct_zero']and N['correct_one']
result=dict(status='passed',source=fid,readback=N,capacity={l:len(v)for l,v in tasks.items()},scope='Observed fixed-point first derivatives retain source reciprocal rewrites, product and quotient factoring and angle arithmetic. Missing hard canonical e3648 quotient, fixed four differentiation/four evaluation stages at pi6/4/3. All arguments x; no chain/higher derivatives/tangent equation. q1905 opaque bank evidence-only with separate method bank, correct0/1 retained.',native_limitations='See frozen native-validation.json; no engine changes.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

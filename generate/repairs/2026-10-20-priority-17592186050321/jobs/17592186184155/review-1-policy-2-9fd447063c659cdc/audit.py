import os,sys,json,re,hashlib,pathlib,importlib.util,subprocess,random,itertools,collections,shutil
from fractions import Fraction as F
E=pathlib.Path(__file__).resolve().parent
JOB=E.parent; W=JOB/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=str(REPO/'.venv/bin/python')
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
sys.path.insert(0,str(W));import generator as g

def save(n,d): (E/n).write_text(json.dumps(d,indent=2)+'\n')
def hash_package(): return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
def add(a,b):
 d=a.copy()
 for p,c in b.items():d[p]=d.get(p,F(0))+c
 return {p:c for p,c in d.items() if c}
def mul(a,b):
 d={}
 for p,c in a.items():
  for q,v in b.items():d[p+q]=d.get(p+q,F(0))+c*v
 return {p:c for p,c in d.items() if c}
def pw(a,n):
 if n.denominator==1 and n>=0:
  out={F(0):F(1)}
  for _ in range(int(n)):out=mul(out,a)
  return out
 assert len(a)==1,(a,n)
 p,c=next(iter(a.items()))
 if n.denominator!=1:
  assert c==1,(c,n)
 return {p*n:c**n.numerator if n.denominator==1 else F(1)}
def integ(a):
 assert -1 not in a
 return {p+1:c/(p+1) for p,c in a.items()}
def derivative(a):return {p-1:p*c for p,c in a.items() if p*c}
class Parser:
 def __init__(self,s):
  s=re.sub(r'\\(?:mathrm|text|textrm)\{d\}\s*x','',s)
  s=s.replace('dx','')
  for t in ['\\left','\\right','\\,','\\quad','\\displaystyle']:s=s.replace(t,'')
  s=s.replace('\\cdot','*').replace('\\times','*')
  self.ts=re.findall(r'\\[a-zA-Z]+|\d+|[^\s]',s);self.i=0
 def peek(self):return self.ts[self.i] if self.i<len(self.ts) else ''
 def pop(self,t=None):
  a=self.peek();assert a and (t is None or a==t),(a,t,self.ts,self.i)
  self.i+=1;return a
 def expr(self):
  a=self.prod()
  while self.peek() in ('+','-'):
   sign=self.pop();b=self.prod();a=add(a,b if sign=='+' else {p:-c for p,c in b.items()})
  return a
 def prod(self):
  a=self.unary()
  while self.peek() and self.peek() not in ('+','-',')','}',']','=',',','.'):
   if self.peek()=='/':self.pop();a=mul(a,pw(self.unary(),F(-1)))
   else:
    if self.peek()=='*':self.pop()
    a=mul(a,self.unary())
  return a
 def unary(self):
  if self.peek() in ('+','-'):
   sign=self.pop();a=self.unary();return a if sign=='+' else {p:-c for p,c in a.items()}
  return self.power()
 def power(self):
  a=self.atom()
  if self.peek()=='^':
   self.pop();b=self.unary();assert not b or list(b)==[F(0)],b;a=pw(a,b.get(F(0),F(0)))
  return a
 def atom(self):
  t=self.pop()
  if t in ('{','('):
   a=self.expr();self.pop('}' if t=='{' else ')');return a
  if t.isdigit():return {} if int(t)==0 else {F(0):F(t)}
  if t=='x':return {F(1):F(1)}
  if t=='C':return {}
  if t=='\\frac':
   a=self.atom();b=self.atom();return mul(a,pw(b,F(-1)))
  if t=='\\sqrt':
   d=F(2)
   if self.peek()=='[':self.pop();d=F(self.pop());self.pop(']')
   return pw(self.atom(),1/d)
  if t=='\\int':return integ(self.power())
  raise AssertionError(('unknown token',t,self.ts))
def parse(s):
 p=Parser(s.strip().rstrip('.'));a=p.expr();assert not p.peek(),(p.peek(),p.ts,p.i);return a

def qparts(r):
 q=r['question'];f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];key=next(i for i,c in enumerate(cs) if c[':answer/id']==f[':answer-field/correct'][1]);return q,cs,key

def visible(r):
 q,cs,key=qparts(r);ss=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',q[':question/problem'],re.S)[0]
 return (derivative(parse(ss)) if r'\int' in ss else parse(ss)),[parse(c[':answer/value']) for c in cs],key

def check(r):
 integrand,bank,key=visible(r);correct=[i for i,a in enumerate(bank) if derivative(a)==integrand]
 assert correct==[key],(r['generation'],correct,key)
 assert len({tuple(sorted(a.items())) for a in bank})==5
 # Evaluate every displayed equality independently; row continuations form one stage.
 s=r['question'][':question/worked-solution'];body=s.split('$$')[1]
 body=re.sub(r'\\(?:begin|end)\{aligned\}','',body).replace('\\\\','').replace('&','')
 stages=body.split('=')
 for stage in stages:assert derivative(parse(stage))==integrand,('solution stage',stage,integrand)
 return {'id':r['question'][':question/id'],'key':key,'stages':len(stages),'template':r['generation']['template']}

def command(args,out):
 r=subprocess.run(args,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});save(out,{'command':args,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});return r

if __name__=='__main__':
 save('package-before.json',hash_package())
 records=[g.generate(seed) for seed in range(730019,730259)]
 # Six explicit endpoints across both profiles; all six term orders sampled separately below.
 boundaries=[]
 for profile in ['negative_fractional','positive_fractional']:
  for d in [3,5,7]:
   terms=[[-6,F(-d-1,d) if profile=='negative_fractional' else F(d-1,d)],[6,7],[-6,-6]]
   design={'profile':profile,'order':[2,1,0],'states':[[0,1,1],[1,0,1],[1,1,0],[1,1,1]]}
   boundaries.append(g.generate(4411,parameters=terms,design=design))
 save('sampled.json',records);save('boundaries.json',boundaries)
 batch=json.loads((JOB/'samples.json').read_text());save('runner-batch.json',batch)
 replay=[g.replay_source(name) for name in ['q-2250','q-29830','q-113848','q-113850']];save('source-replays.json',replay)
 src=json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
 fidelity=[]
 for r in replay:
  original=next(q for q in src if q[':question/math-academy-id']==r['generation']['source_name']);q,cs,key=qparts(r)
  oldbank=original[':question/answer-fields'][0][':answer-field/choices']
  assert parse(re.findall(r'\$(.*?)\$',q[':question/problem'],re.S)[0])==parse(re.findall(r'\$(.*?)\$',original[':question/problem'],re.S)[0])
  assert all(parse(a[':answer/value'])==parse(b[':answer/value']) for a,b in zip(cs,oldbank))
  norm=lambda t:re.sub(r'\s|&|\\\\','',t)
  if ':question/worked-solution' in original:assert norm(original[':question/worked-solution'])==norm(q[':question/worked-solution'])
  fidelity.append({'source':r['generation']['source_name'],'all_five_options_equal':True,'prompt_equal':q[':question/problem']==original[':question/problem'],'key':key,'solution_origin':r['generation']['solution_origin']})
 save('source-replay-results.json',{'cases':fidelity,'unsupported':['e-373: absent answer fields','q-2252: absent answer fields','q-49173: absent answer fields']})
 results=[];fail=[]
 for kind,rs in [('sampled',records),('boundary',boundaries),('batch',batch),('source',replay)]:
  for i,r in enumerate(rs):
   try:results.append({'kind':kind,'index':i,**check(r)})
   except Exception as e:fail.append({'kind':kind,'index':i,'error':repr(e)})
 save('math-results.json',{'command':f'{PY} audit.py','method':'Independent sparse rational-power TeX parser: differentiate every visible choice and every worked equality; do not use generator bank metadata. C treated as arbitrary constant. Odd-root monomial identities valid on each real half-line.','checked':len(results),'failures':fail,'results':results})
 print(json.dumps({'math_checked':len(results),'failures':fail[:3],'replays':fidelity}))

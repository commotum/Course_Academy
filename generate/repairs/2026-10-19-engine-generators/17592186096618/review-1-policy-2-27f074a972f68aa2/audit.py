import os,sys,json,re,hashlib,random,shutil,subprocess
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
ROOT=Path('/home/jake/Developer/Course_Academy'); E=Path(__file__).resolve().parent; W=E.parent/'workspace';sys.path.insert(0,str(W))
import generator as g
import sympy as s
X=s.Symbol('x',positive=True)
def save(n,v): (E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
# Small independent TeX arithmetic parser; no generator expression metadata used.
class Parser:
 def __init__(self,z):
  z=re.sub(r'\\operatorname\{(\w+)\}',r'\\\1 ',z)
  z=z.replace('\\\\','\\').replace('⁡','').replace('\\left','').replace('\\right','').replace('\\,','').replace('\\!','').replace('\\cdot','*').replace('\\times','*')
  z=re.sub(r'(?<!\\)(sin|cos|tan|sec|ln|log)',r'\\\1 ',z)
  z=re.sub(r'\{\\?(log|sec)\s*\}',r'\\\1 ',z)
  self.ts=re.findall(r'\\[A-Za-z]+|\d+|[^\s]',z);self.i=0
 def peek(self):return self.ts[self.i] if self.i<len(self.ts) else ''
 def pop(self):v=self.peek();self.i+=1;return v
 def atom(self):
  a=self.pop()
  if a in ('{','('):
   v=self.expr();assert self.pop()==('}' if a=='{' else ')');return v
  if a=='\\frac':return self.atom()/self.atom()
  if a=='\\sqrt':return s.sqrt(self.atom())
  if a in ('\\ln','\\log','\\sin','\\cos','\\tan','\\sec'):
   b=None
   if self.peek()=='_':self.pop();b=self.atom()
   power=None
   if self.peek()=='^':self.pop();power=self.atom()
   v=self.atom()
   f={'\\ln':s.log,'\\log':s.log,'\\sin':s.sin,'\\cos':s.cos,'\\tan':s.tan,'\\sec':s.sec}[a]
   val=f(v)/(s.log(b) if b is not None else s.log(10) if a=='\\log' else 1)
   return val**power if power is not None else val
  if a=='x':return X
  if a=='e':return s.E
  if a.isdigit():return s.Integer(a)
  raise ValueError(('atom',a,self.ts,self.i))
 def power(self):
  v=self.atom()
  if self.peek()=='^':self.pop();v=v**self.unary()
  return v
 def unary(self):
  if self.peek() in ('+','-'):
   a=self.pop();return self.unary()*(1 if a=='+' else -1)
  return self.power()
 def product(self):
  v=self.unary()
  while self.peek() and self.peek() not in ('+','-',')','}'):
   if self.peek() in ('*','/'):
    a=self.pop();z=self.unary();v=v*z if a=='*' else v/z
   else:v*=self.unary()
  return v
 def expr(self):
  v=self.product()
  while self.peek() in ('+','-'):
   a=self.pop();z=self.product();v=v+z if a=='+' else v-z
  return v
 def parse(self):
  v=self.expr();assert self.i==len(self.ts),(self.ts,self.i);return v
def parse(z):return Parser(z).parse()
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0
def key(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def inspect(r):
 q=r['question'];pr=q[':question/problem']; product=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',pr)[1].rstrip(' ,');f=parse(product)
 full=s.diff(f,X);answer=parse(key(r));ft=q[':question/answer-fields'][0][':answer-field/type'];out={'id':q[':question/id'],'template':r['generation']['template'],'product':str(f),'derivative':str(full),'answer':str(answer),'failures':[]}
 if ft.endswith('blank'):
  after=pr.split('{{field-1}}');last=after[0].rsplit('$',2)
  if after[1].strip():
   z=re.search(r'\$(.*?)\$',after[1])[1].replace('\\,','');sign=-1 if z.strip().startswith('-') else 1;known=parse(z.lstrip(' +-'));total=answer+sign*known
  else:
   z=re.findall(r'\$(.*?)\$',after[0],re.S)[-1].rsplit('=',1)[1].replace('\\,','').strip();sign=-1 if z.endswith('-') else 1;known=parse(z[:-1]);total=known+sign*answer
  if not equal(total,full):out['failures'].append('blank+printed known != derivative')
 else:
  if not equal(answer,full):out['failures'].append('radio key != derivative')
  vals=[parse(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
  if sum(equal(v,full) for v in vals)!=1:out['failures'].append('nonunique radio key')
 final=q[':question/worked-solution'].split('& =')[-1].split('\\end{aligned}')[0].strip()
 if not equal(parse(final),full):out['failures'].append('solution final != derivative')
 return out
if __name__=='__main__':
 save('package-before.json',hashes())
 records=[];requests=[]
 for i,t in enumerate(g.TEMPLATES):
  for seed in (7419,22817,51043,99107,620211,812345):
   kw={'seed':seed+i*17,'template':t};records.append(g.generate(**kw));requests.append(kw)
  for high in (False,True):
   p=g.defaults(t)
   for k in p:
    p[k]=({'b':10,'d':10,'c':6,'h':5,'n':-1 if t=='power_log_radio' else 4,'k':1 if t.startswith('base_log') or t=='power_exp_radio' else 3} if high else {'b':2,'d':2,'c':2 if t=='log_log_radio' else 1,'h':1,'n':-4 if t=='power_log_radio' else 2,'k':-1 if t.startswith('base_log') else 1})[k]
   kw={'seed':41021,'template':t,'parameters':p};records.append(g.generate(**kw));requests.append(kw)
 save('samples.json',records);save('requests.json',requests)
 src=json.loads((E.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];replays=[];fidelity=[]
 for q in src:
  sid=q[':question/math-academy-id'];t=next(t for t,v in g.TEMPLATES.items() if sid in v[2]);p=g.defaults(t)
  if sid=='q-319903':p={'c':5,'n':2,'k':1}
  r=g.generate(seed=17291,template=t,parameters=p,replay=True);replays.append(r)
  banks=[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
  if sid=='q-320824':banks=[z for z in banks if not z.startswith('2x')]
  expected=[parse(z) for z in banks];actual=[parse(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  fidelity.append({'source_id':sid,'expected_choices':len(expected),'actual_choices':len(actual),'bank_equal':len(expected)==len(actual) and all(any(equal(a,b) for b in actual) for a in expected),'source_prompt':q[':question/problem'],'replayed_prompt':r['question'][':question/problem'],'source_solution':q.get(':question/worked-solution'),'replayed_solution':r['question'][':question/worked-solution']})
 save('replays.json',replays);save('source-replay.json',fidelity)
 pairs=[]
 for label,t,p,ta,tb,p2 in [('target','base_cos_left_blank',{'b':7},'left','right',None),('sign','base_log_left_blank',{'b':5,'d':7,'k':1},'left','left',{'b':5,'d':7,'k':-1}),('irrelevant-h','polynomial_log_blank',{'n':3,'h':1},'left','left',{'n':3,'h':5}),('relevant-h','polynomial_log_blank',{'n':3,'h':1},'right','right',{'n':3,'h':5}),('log-equivalence','base_log_right_blank',{'b':4,'d':4,'k':1},'right','right',None)]:
  a=g.generate(seed=92381,template=t,parameters=p,target=ta);b=g.generate(seed=92381,template=t,parameters=p2 or p,target=tb);pairs.append({'label':label,'before':a,'after':b,'response_equal':equal(parse(key(a)),parse(key(b)))})
 save('counterfactuals.json',pairs);save('counterfactual-records.json',[r for p in pairs for r in (p['before'],p['after'])])
 batch=json.loads((E.parent/'samples.json').read_text());save('runner-batch.json',batch)
 allr=records+replays+batch+[r for p in pairs for r in (p['before'],p['after'])];results=[]
 for r in allr:
  try:results.append(inspect(r))
  except Exception as e:results.append({'id':r['question'][':question/id'],'template':r['generation']['template'],'failures':['parse/error: '+str(e)]})
 save('math-results.json',results)
 cases=[]
 for idx,r in enumerate(records+batch+[r for p in pairs for r in (p['before'],p['after'])]):
  f=r['question'][':question/answer-fields'][0];checks=[]
  if f[':answer-field/type'].endswith('radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently validated complete radio bank'} for a in f[':answer-field/choices']]
  else:
   ans=parse(key(r));checks=[{'submitted':key(r),'expected':'accepted','purpose':'canonical fragment'},{'submitted':s.latex(ans*2/2,ln_notation=True),'expected':'accepted','purpose':'independently parsed equivalent fragment'},{'submitted':s.latex(ans+1,ln_notation=True),'expected':'rejected','purpose':'off by one fragment'},{'submitted':'0','expected':'rejected','purpose':'zero wrong fragment'}]
  cases.append({'label':'sample-'+str(idx),'record':r,'checks':checks})
 # Exercise valid change-of-base simplification, instead of marking a known engine gap unresolved.
 r=pairs[-1]['before'];cases.append({'label':'valid ln4=2ln2 equivalent','record':r,'checks':[{'submitted':r'\frac{4^x}{2x\ln(2)}','expected':'accepted','purpose':'exact positive-base logarithm identity'}]})
 for p in pairs[:4]:
  for side,other in [('before','after'),('after','before')]:
   cases.append({'label':p['label']+' cross '+side,'record':p[side],'checks':[{'submitted':key(p[other]),'expected':'accepted' if p['response_equal'] else 'rejected','purpose':'controlled relevant/irrelevant cross response'}]})
 save('grader-input.json',cases)
 save('render-input.json',batch+[p[side] for p in pairs[:4] for side in ['before','after']]+[next(r for r in records if r['generation']['template']=='sqrt_exp_radio')])
 save('runtime.json',{'python':sys.version.split()[0],'packages':{'sympy':s.__version__},'manifest':json.loads((W/'package.json').read_text())})
 print('samples',len(records),'replays',len(replays),'math',len(results),'failures',sum(bool(v['failures']) for v in results),'fidelity mismatches',sum(not v['bank_equal'] for v in fidelity))
 print('first failures',[v for v in results if v['failures']][:3])

"""Read-only independent revision audit: PYTHONDONTWRITEBYTECODE=1 <job python> review-current.py"""
import sys,pathlib,json,hashlib,importlib.util,subprocess,shutil,re,copy,os
from collections import Counter
E=pathlib.Path(__file__).resolve().parent;J=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');W=J/'workspace';sys.dont_write_bytecode=True;sys.path.insert(0,str(E/'deps'))
import sympy as S
from independent_math import solve_check,parse,linear_residual,x,y,C,D

def save(n,v):(E/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def load(p):return json.loads(p.read_text())
def module(p):
 spec=importlib.util.spec_from_file_location('g'+hashlib.md5(str(p).encode()).hexdigest(),p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):return field(r)[':answer-field/correct'][1]
def normalize(v):return v.replace(r'\left','').replace(r'\right','')
def keyval(r):return next(a[':answer/value'] for a in field(r)[':answer-field/choices'] if a[':answer/id']==key(r))
allrecords=load(E/'math-records.json')
math=[];fail=[]
for i,r in enumerate(allrecords):
 q=r['question'];h=r['generation']['parameters']['shift'];f=field(r)
 try:
  result=copy.deepcopy(solve_check(q[':question/problem'],tuple(a[':answer/value'] for a in f[':answer-field/choices']),h))
  valid=[a['is_solution'] for a in result['choices']];expected=[a[':answer/id']==key(r) for a in f[':answer-field/choices']]
  assert valid==expected,{'valid':valid,'key':expected}
  if not r['generation']['evidence_only']:
   sol=q[':question/worked-solution'];ztext=re.search(r'\$\$z=([\s\S]*?)\$\$',sol)[1]
   z=parse(ztext).subs(x,x-h);assert linear_residual(z,S.sympify(result['p'],locals={'x':x}),S.sympify(result['q'],locals={'x':x}),S.sympify(result['n']))==0
   final=re.search(r'\$\$y=([\s\S]*?)\$\$',sol)[1].rstrip('.')
   assert final==keyval(r).split('=',1)[1]
  result.update({'question_id':q[':question/id'],'template':r['generation']['template'],'passed':True});math.append(result)
 except Exception as ex:
  fail.append({'index':i,'question_id':q[':question/id'],'generation':r['generation'],'error':repr(ex)})
 if i%10==0:save('math-results.json',{'tested':len(math),'failures':fail,'cases':math});print('math',i+1,'failures',len(fail),flush=True)
save('math-results.json',{'tested':len(math),'failures':fail,'cases':math,'method':'Prior independent reviewer parser, exact Bernoulli transformed residual for every displayed choice, unique-key check; derived z and final answer checked from solution. Positive-base restrictions applied for fractional powers.'})
save('math-records.json',allrecords)

assert not fail, fail
print({'tested':len(math),'failed':len(fail)})

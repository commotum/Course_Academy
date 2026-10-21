import os,sys,json,pathlib,importlib.util,hashlib,subprocess,copy,re,platform
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
ROOT=pathlib.Path('/home/jake/Developer/Course_Academy'); JOB=ROOT/'generate/repairs/2026-10-20-early-cohort/jobs/17592186100894'; E=pathlib.Path(__file__).parent; W=JOB/'workspace'
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str))
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
# Package baseline retained from first execution
sys.path.insert(0,str(W))
spec=importlib.util.spec_from_file_location('reviewed_generator',W/'17592186100894.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z=S.symbols('x y z',real=True)
# Independent recursive TeX-to-SymPy converter. No author parser or models used in mathematical checks.
def expr(t):
 t=t.replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(r'\cdot','*').replace(r'\times','*').replace(r'\dfrac',r'\frac')
 t=re.sub(r'\\(?:operatorname|textrm|mathrm)\{([^{}]*)\}',lambda m:'\\'+m[1],t)
 t=re.sub(r'\\ln\s*([0-9]+)',r'\\ln{\1}',t)
 t=t.strip().rstrip('.,');i=0
 def group():
  nonlocal i
  while i<len(t) and t[i].isspace():i+=1
  if t[i]=='{':
   i+=1;r=seq('}');return r
  if t[i]=='\\':return atom()
  a=t[i];i+=1;return a
 def atom():
  nonlocal i
  if t[i]!='\\':return group()
  i+=1;m=re.match('[A-Za-z]+',t[i:]);name=m[0];i+=len(name)
  if name=='frac':a=group();b=group();return '(('+a+')/('+b+'))'
  if name=='sqrt':a=group();return 'sqrt('+a+')'
  if name=='pi':return 'pi'
  if name in ['sin','cos','tan','cot','ln','log','exp','arcsin']:return {'ln':'log','arcsin':'asin'}.get(name,name)
  raise ValueError('unsupported command '+name)
 def seq(end=None):
  nonlocal i
  out=''
  while i<len(t):
   c=t[i]
   if end and c==end:i+=1;return out
   if c=='{':out+='('+group()+')'
   elif c=='\\':out+=atom()
   elif c=='|':
    i+=1;out+='Abs('+seq('|')+')'
   else:out+=c;i+=1
  if end:raise ValueError('unclosed '+end)
  return out
 st=seq();return parse_expr(st,local_dict={'x':x,'y':y,'z':z,'e':S.E,'pi':S.pi,'C':S.Symbol('C'),'K':S.Symbol('K'),'ln':S.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def relation(t):
 a,b=t.split('=');return expr(a)-expr(b)
def prompt_data(r):
 p=r['question'][':question/problem'];blocks=re.findall(r'\$\$?(.*?)\$\$?',p,flags=re.S);ode=blocks[0].strip()
 ode=ode.replace(r'\frac{\text{d}y}{\text{d}x}','z').replace(r'\dfrac {\textrm{d}y} {\textrm{d}x}','z').replace('{y}^{′}','z').replace("y'",'z')
 ode=re.split(r',\\,y\(',ode)[0].strip().rstrip('.,');ic=None
 for b in blocks:
  b=b.replace(r'\left','').replace(r'\right','')
  for m in re.finditer(r'y\(',b):
   start=m.end();depth=1;j=start
   while depth and j<len(b):
    if b[j]=='(':depth+=1
    if b[j]==')':depth-=1
    j+=1
   arg=b[start:j-1]
   if b[j:j+1]!='=' or 'x' in arg:continue
   ic=(expr(arg),expr(b[j+1:].strip().rstrip('.,')));break
  if ic:break
 if not ic:raise ValueError('IC not found '+p)
 return relation(ode),ic

def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);cid=f[':answer-field/correct'][1];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def answer_residual(r,v):
 mid=r['generation']['template'];h=r['generation']['parameters']['h']
 if '=' in v:return relation(v)
 f=expr(v)
 if mid=='q-355576':return y-S.log(f)
 if mid=='q-355560':
  # Read numerator from the displayed scaffold, rather than a generator model.
  t=r['question'][':question/problem'].split('$y(x)=',1)[1].split(r'\frac{',1)[1];depth=1;j=0
  while depth:
   if t[j]=='{':depth+=1
   if t[j]=='}':depth-=1
   j+=1
  return y-expr(t[:j-1])/f
 return y-f

def simplify(v):return S.simplify(S.trigsimp(v))
def explicit(r,v):
 f=answer_residual(r,v)
 if '=' not in v:
  if r['generation']['template']=='q-355576':return S.log(expr(v))
  if r['generation']['template']=='q-355560':return S.solve(f,y)[0]
  return expr(v)
 lhs,rhs=v.split('=');a,b=expr(lhs),expr(rhs)
 if a==y:return b
 if a==y**2:return S.sqrt(b)
 if a==y**3:return b**S.Rational(1,3)
 raise ValueError('unexpected explicit relation '+v)

def math_check(r):
 ode,(a,b)=prompt_data(r);sol=explicit(r,correct(r))
 residual=simplify(ode.subs({z:S.diff(sol,x),y:sol},simultaneous=True));at=simplify(sol.subs(x,a)-b);candidates=[]
 for av in field(r)[':answer-field/choices']:
  zsol=explicit(r,av[':answer/value'])
  rr=simplify(ode.subs({z:S.diff(zsol,x),y:zsol},simultaneous=True));aa=simplify(zsol.subs(x,a)-b)
  candidates.append({'value':av[':answer/value'],'IC':str(aa),'ODE':str(rr),'valid':aa==0 and rr==0})
 return {'id':r['question'][':question/id'],'template':r['generation']['template'],'h':r['generation']['parameters']['h'],'IC':str(at),'ODE':str(residual),'passed':at==0 and residual==0,'valid_choice_count':sum(c['valid'] for c in candidates),'choices':candidates}

batch=json.load(open(JOB/'samples.json'));save('batch.json',batch)
replays=[];samples=[];failures=[]
for i,mid in enumerate(g.MODELS):
 replays.append(g.generate(g.level(mid),seed=93211+i,template=mid,replay=True))
 if mid not in g.UNGRADABLE:
  for h in (-4,1,4):samples.append(g.generate(g.level(mid),seed=61301+i,template=mid,parameters={'h':h}))
# Explicitly exercise excluded source families; keep strict grading tests.
excluded=[g.generate(g.level(mid),seed=77071+i,template=mid,parameters={'h':1}) for i,mid in enumerate(g.UNGRADABLE)]
save('source-replay-records.json',replays);save('samples.json',samples);save('excluded-records.json',excluded)
replay_results=[];source=json.load(open(JOB/'source/source.json'));orig={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
for r in replays:
 mid=r['generation']['template'];f=field(r);q=orig[mid];sf=q[':question/answer-fields'][0];banks=set(g.normalize_tex(a[':answer/value']) for a in sf[':answer-field/choices']);rbanks=set(a[':answer/value'] for a in f[':answer-field/choices'])
 replay_results.append({'mid':mid,'full_bank_equal':banks==rbanks,'key_equal':correct(r)==g.normalize_tex(sf[':answer-field/correct'][':answer/value']),'prompt_equal':r['question'][':question/problem']==g.normalize_prose(q[':question/problem']),'solution_equal':r['question'][':question/worked-solution']==g.normalize_prose(q[':question/worked-solution'])})
save('source-replay.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python audit.py','results':replay_results,'missing':[{'mid':m,'id':q[':question/id'],'reason':g.EXCLUDED.get(m,'not implemented')} for m,q in orig.items() if m not in g.MODELS],'canonical_example':'Not implemented as a separate family','documented_repairs':g.REPAIRS})
checks=[]
for r in samples+batch+excluded:
 try:checks.append(math_check(r))
 except Exception as e:checks.append({'id':r['question'][':question/id'],'template':r['generation']['template'],'error':str(e)})
save('math-results.json',checks)
# Rejection, deterministic replay, explicit source restrictions.
rejections=[]
for label,kw in [('bad shift',{'parameters':{'h':5}}),('boolean shift',{'parameters':{'h':True}}),('extra parameter',{'parameters':{'h':1,'y0':2}}),('hard',{'difficulty':'hard'}),('new source sqrt',{'difficulty':'moderate','template':'q-128199'}),('sine source',{'template':'q-126765'}),('change IC',{'template':'q-104064','parameters':{'h':1,'y0':'1/9'}})]:
 try:g.generate(**kw);rejections.append({'label':label,'accepted':True})
 except Exception as e:rejections.append({'label':label,'accepted':False,'error':str(e)})
save('runtime-results.json',{'python':platform.python_version(),'sympy':S.__version__,'manifest':json.load(open(W/'package.json'))['dependencies'],'deterministic_replay':samples[0]==g.generate(g.level(samples[0]['generation']['template']),seed=samples[0]['generation']['seed'],template=samples[0]['generation']['template'],parameters=samples[0]['generation']['parameters']),'rejections':rejections})
print(json.dumps({'sample_count':len(samples),'replay_count':len(replays),'math_checked':len(checks),'math_errors':[c for c in checks if 'error'in c or not c.get('passed') or c.get('valid_choice_count')!=1]},indent=2))

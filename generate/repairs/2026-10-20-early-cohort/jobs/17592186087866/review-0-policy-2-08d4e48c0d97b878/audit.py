import os,sys,json,hashlib,importlib.util,re,copy,subprocess,shutil,platform
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
E=Path(__file__).resolve().parent
JOB=E.parent; REPO=Path('/home/jake/Developer/Course_Academy'); PKG=JOB/'workspace'; PY=REPO/'.venv/bin/python'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed',PKG/'17592186087866.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def hashfiles():return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}
if not (E/'package-before.json').exists():save('package-before.json',hashfiles())
x,y,D=S.symbols('x y D');local={'x':x,'y':y,'D':D,'e':S.E,'sin':S.sin,'cos':S.cos,'tan':S.tan,'cot':S.cot,'sec':S.sec,'csc':S.csc}
def group(st,i):
 assert st[i]=='{',(st,i)
 depth=1;j=i+1
 while depth:
  if st[j]=='{':depth+=1
  if st[j]=='}':depth-=1
  j+=1
 return st[i+1:j-1],j

def clean(t):
 for derivative in [r'\frac{\text{d}y}{\text{d}x}',r'\frac{dy}{dx}',r'\dfrac {\textrm{d}y} {\textrm{d}x}']:t=t.replace(derivative,'D')
 t=t.replace('⁡','').replace(r'\left','').replace(r'\right','')
 t=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc)\}',r'\\\1',t)
 t=re.sub(r'\\(sin|cos|tan|cot|sec|csc)\s*(2?)x',lambda m:'\\'+m[1]+'{'+m[2]+'x}',t)
 t=re.sub(r'\\(?:,|;|!|quad|qquad)', '',t)
 t=t.strip().rstrip('.,')
 # remove annotations while retaining their contents
 while r'\underbrace' in t:
  i=t.index(r'\underbrace');j=i+len(r'\underbrace');v,k=group(t,j);assert t[k:k+2]=='_{';_,end=group(t,k+1);t=t[:i]+'{'+v+'}'+t[end:]
 return t

def infix(t):
 out='';i=0
 while i<len(t):
  c=t[i]
  if c=='{':v,i=group(t,i);out+='('+infix(v)+')';continue
  if c=='\\':
   m=re.match(r'\\([A-Za-z]+)',t[i:]);assert m,t[i:];cmd=m[1];i+=len(m[0])
   if cmd in ['frac','dfrac']:
    while t[i].isspace():i+=1
    a,i=group(t,i)
    while t[i].isspace():i+=1
    b,i=group(t,i);out+='(('+infix(a)+')/('+infix(b)+'))'
   elif cmd in ['sin','cos','tan','cot','sec','csc']:
    while t[i].isspace():i+=1
    power=''
    if t[i]=='^':
     i+=1
     if t[i]=='{':power,i=group(t,i)
     else:power=t[i];i+=1
    while i<len(t) and t[i].isspace():i+=1
    if t[i]=='{':a,i=group(t,i)
    elif t[i]=='(':
     depth=1;j=i+1
     while depth:
      if t[j]=='(':depth+=1
      if t[j]==')':depth-=1
      j+=1
     a=t[i+1:j-1];i=j
    else:raise ValueError('unwrapped trig '+t[i:])
    out+='('+cmd+'('+infix(a)+'))'+('**('+infix(power)+')' if power else '')
   else:raise ValueError('unknown command '+cmd)
   continue
  out+= '**' if c=='^' else c;i+=1
 return out

def expr(t):return parse_expr(infix(clean(t)),local_dict=local,transformations=standard_transformations+(implicit_multiplication_application,))
def equation(t):
 t=t.replace('&','');t=re.split(r'\\(?:,,?\s*)?\s*[xy]\\ne',t)[0];t=t.split(r'\,,')[0]
 l,r=t.split('=',1);return expr(l),expr(r)
def residual(pair):return S.expand(pair[0]-pair[1])
def norm(pair):
 r=residual(pair);a=r.coeff(D)
 return S.trigsimp(S.cancel(r/a))
def is_standard(pair):
 l,r=pair
 return S.expand(l).coeff(D)==1 and not r.has(y,D) and S.simplify(l-D).subs(y,0)==0 and S.diff(l-D,y,2)==0

def check_record(r):
 q=r['question'];prompt=q[':question/problem'].split('$$')[1];p=equation(prompt);n=norm(p);f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1];tests=[]
 for a in f[':answer-field/choices']:
  e=equation(a[':answer/value']);ok=bool(is_standard(e) and S.trigsimp(S.expand_trig(norm(e)-n))==0)
  tests.append({'id':a[':answer/id'],'equivalent_standard':ok,'keyed':a[':answer/id']==correct})
 sol=q[':question/worked-solution'];rows=sol.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r' \\ ')
 row_tests=[]
 for row in rows:
  e=equation(row);row_tests.append(bool(S.trigsimp(S.expand_trig(norm(e)-n))==0))
 return {'question_id':q[':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'choices':tests,'solution_rows_equivalent':row_tests,'passed':all(t['equivalent_standard']==t['keyed'] for t in tests) and all(row_tests)}

def main():
 source=json.loads((JOB/'source/source.json').read_text());qs=source['material']['kp'][':knowledge-point/questions'];replays=[];replay_tests=[]
 def strip(q):
  if isinstance(q,list):return sorted([strip(v) for v in q],key=lambda v:json.dumps(v,sort_keys=True))
  if not isinstance(q,dict):return q
  return {k:strip(v) for k,v in q.items() if k not in [':db/id',':question/id',':question/math-academy-id',':answer-field/id',':answer/id']}
 def src_shape(q):
  q=copy.deepcopy(q)
  for f in q.get(':question/answer-fields',[]):
   if isinstance(f.get(':answer-field/correct'),list):
    ident=f[':answer-field/correct'][1];f[':answer-field/correct']=next(a for a in f[':answer-field/choices'] if a[':answer/id']==ident)
  def enums(o):
   if isinstance(o,dict):
    if set(o)=={':db/ident'}:return o[':db/ident']
    return {k:enums(v) for k,v in o.items()}
   if isinstance(o,list):return [enums(v) for v in o]
   return o
  return strip(enums(q))
 for q in qs:
  t=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
  r=g.generate(level,seed=9101,template=t,parameters={'n':1},profile='observed-raw');replays.append(r)
  a,b=src_shape(q),src_shape(r['question']);replay_tests.append({'source_id':q[':question/id'],'template':t,'passed':a==b,'source_fields':len(q[':question/answer-fields']),'complete_bank_sizes':[len(f[':answer-field/choices']) for f in q[':question/answer-fields']]})
 save('source-replays.json',replays);save('source-replay-results.json',replay_tests)
 records=[];generation_cases=[]
 for level,ts in g.FAMILIES.items():
  for t in ts:
   for seed in [9101,9109,9137]:
    r=g.generate(level,seed,template=t);records.append(r)
   low={z:(2 if t=='q-79699' or (t in ['q-16400','rational-collect'] and z=='a') else 1) for z in g.ORIGINAL[t]}
   high={z:(5 if t=='q-16400' and z!='h' else 6 if t=='q-16401' and z!='b' else 4 if t=='q-16401' else 8) for z in g.ORIGINAL[t]}
   for p in [low,high]:
    try:records.append(g.generate(level,9200,template=t,parameters=p));generation_cases.append({'level':level,'template':t,'parameters':p,'result':'accepted'})
    except Exception as e:generation_cases.append({'level':level,'template':t,'parameters':p,'result':str(e)})
   for p in [{z:0 for z in g.ORIGINAL[t]},{z:99 for z in g.ORIGINAL[t]},{z:1.5 for z in g.ORIGINAL[t]}]:
    try:g.generate(level,seed=9201,template=t,parameters=p);result='unexpected acceptance'
    except ValueError as e:result='rejected: '+str(e)
    generation_cases.append({'level':level,'template':t,'parameters':p,'result':result})
 # Exhaust finite one-dimensional families, not just a random sample.
 for t in g.FAMILIES['easy']:
  if len(g.ORIGINAL[t])==1:
   key=next(iter(g.ORIGINAL[t]))
   for value in range(2 if t=='q-79699' else 1,9):records.append(g.generate('easy',9300+value,t,parameters={key:value}))
 save('independent-records.json',records);save('independent-easy.json',[r for r in records if r['generation']['difficulty']=='easy']);save('generation-boundaries.json',generation_cases)
 maths=[]
 for r in records+json.loads((JOB/'samples.json').read_text()):
  try:maths.append(check_record(r))
  except Exception as e:maths.append({'question_id':r['question'][':question/id'],'error':repr(e),'passed':False})
 save('math-results.json',maths)
 # Counterfactuals change one coefficient (relevant), or only answer order (irrelevant).
 pairs=[];pair_records=[]
 for t,p1,p2 in [('q-16400',{'a':2,'b':3,'c':1,'h':4},{'a':2,'b':3,'c':2,'h':4}),('q-8359',{'k':1},{'k':2}),('q-103349',{'n':1},{'n':2})]:
  before=g.generate('easy',9401,t,parameters=p1);after=g.generate('easy',9401,t,parameters=p2);irrelevant=g.generate('easy',9402,t,parameters=p1)
  pair_records.extend([before,after,irrelevant]);pairs.append({'template':t,'before':before['question'][':question/id'],'relevant_after':after['question'][':question/id'],'irrelevant_after':irrelevant['question'][':question/id'],'parameters_before':p1,'parameters_after':p2})
 save('counterfactual-records.json',pair_records);save('counterfactual-pairs.json',pairs)
 render=[]
 for t in g.FAMILIES['easy']:
  render.append(next(r for r in records if r['generation']['template']==t))
 render.extend([r for r in records if r['generation']['difficulty']!='easy'][:1]);render.extend(pair_records);save('render-records.json',render)
 # All actual selection choices for each template, counterfactual and runner sample.
 cases=[]
 for i,r in enumerate(render+json.loads((JOB/'samples.json').read_text())):
  f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  cases.append({'label':f'{i}:{r["generation"]["template"]}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'independent displayed equivalence and standard form'} for a in f[':answer-field/choices']]})
 save('grader-input.json',cases)
 # Source-faithful radio profiles and ineligible raw profiles have been examined separately.
 save('runtime.json',{'python':platform.python_version(),'sympy':S.__version__,'manifest':json.loads((PKG/'package.json').read_text())['dependencies'],'deterministic':g.generate('easy',9191)==g.generate('easy',9191),'command':str(PY)+' '+str(E/'audit.py')})
 print(json.dumps({'replay_passed':sum(t['passed'] for t in replay_tests),'replay_total':len(replay_tests),'math_passed':sum(t['passed'] for t in maths),'math_total':len(maths),'math_failures':[t for t in maths if not t['passed']][:3],'records':len(records)}))
if __name__=='__main__':main()

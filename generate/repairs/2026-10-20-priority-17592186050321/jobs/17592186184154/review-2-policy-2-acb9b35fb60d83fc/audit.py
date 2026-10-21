import os,sys,json,pathlib,hashlib,importlib.util,re,collections,subprocess,shutil
from functools import lru_cache
sys.dont_write_bytecode=True
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor,rationalize
E=pathlib.Path(__file__).resolve().parent
JOB=E.parent; W=JOB/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
save('package-before.json',hashes())
sys.path.insert(0,str(W)); import generator as g
x=S.Symbol('x',positive=True); C=S.Symbol('C')
def tex(t):
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\displaystyle','').replace(r'\,','').replace(r'\!','')
 def arg(i):
  if t[i]!='{':raise ValueError(('expected brace',t,i))
  level=1;j=i+1
  while level:
   if t[j]=='{':level+=1
   if t[j]=='}':level-=1
   j+=1
  return t[i+1:j-1],j
 out='';i=0
 while i<len(t):
  if t.startswith(r'\frac',i) or t.startswith(r'\dfrac',i):
   i+=6 if t.startswith(r'\dfrac',i) else 5
   a,i=arg(i);b,i=arg(i);out+='(('+tex(a)+')/('+tex(b)+'))'
  elif t.startswith(r'\sqrt',i):
   a,i=arg(i+5);out+='(sqrt('+tex(a)+'))'
  else:out+=t[i];i+=1
 return out.replace('{','(').replace('}',')').replace('^','**')
@lru_cache(None)
def parse(t):
 return parse_expr(tex(t),local_dict={'x':x,'C':C,'sqrt':S.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor,rationalize))
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 f=field(r);return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def func(r):
 p=r['question'][':question/problem'];m=re.search(r'Given \$f\(x\)=(.*?)\$ and',p)
 return parse(m[1]) if m else None
@lru_cache(None)
def primitive(t):return S.integrate(parse(t),x)
def integral_eval(t,r):
 if 'f(x)' in t:t=t.replace('f(x)','('+S.sstr(func(r))+')')
 # SymPy string f substitution is already plain and uses ** powers.
 def sub(m):return '('+S.sstr(primitive(m[1]))+')'
 t=re.sub(r'\\int (.*?)\\,\\mathrm\{d\}x',sub,t)
 return parse(t)
def check(r):
 p=r['question'][':question/problem']; integrand=re.search(r'\\int (.*?)\\,\\mathrm\{d\}x',p)[1]
 f=parse(integrand) if 'f(x)' not in integrand else func(r)/x**r['generation']['parameters']['degree']
 answers=[parse(a[':answer/value']) for a in field(r)[':answer-field/choices']]
 correct=[S.simplify(S.diff(a,x)-f)==0 for a in answers]
 assert sum(correct)==1,('unique',p,correct)
 assert correct[[a[':answer/id'] for a in field(r)[':answer-field/choices']].index(key(r)[':answer/id'])],('key',p)
 solution=r['question'][':question/worked-solution'];body=solution.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
 for row in body.split(r'\\'):
  sides=row.split('&=')
  for side in sides:
   if not side.strip():continue
   val=integral_eval(side.strip().rstrip('.'),r)
   assert S.simplify(S.diff(val,x)-f)==0,('solution',row,val,f)
 return {'qid':r['question'][':question/id'],'template':r['generation']['template'],'integrand':str(f),'primitive':str(answers[correct.index(True)]),'choice_count':len(answers),'all_solution_rows_checked':True}
source=json.load(open(JOB/'source/source.json')); batch=json.load(open(JOB/'samples.json')); save('runner-batch.json',batch)
# Fresh deterministic sample and controlled coverage at each sign/role.
audit={};sample=g.sample(240,420106731,audit=audit);save('sample.json',sample)
controlled=[]
for family in ['quotient','radical']:
 for role in range(5):
  for sa,sb in [(-1,-1),(-1,1),(1,-1),(1,1)]:
   controlled.append(g.generate(family,sa*(3 if family=='quotient' else 4),sb*(8 if family=='quotient' else 4),p=3 if sa<0 else 5,target=role,seed=713091))
for d in [2,3]:
 for a,b in [(-4,-8),(-4,8),(4,-8),(4,8)]:controlled.append(g.generate('blank',a,b,degree=d,seed=713091))

for pairing in g.QUOTIENT_PAIRINGS:
 for p in [3,4,5]:
  for role in range(5):
   controlled.append(g.generate('quotient',-3,8,p=p,target=role,reciprocal_exponents=pairing,seed=713091))
save('controlled.json',controlled);save('sampling.json',{'seed':420106731,'count':240,'audit':audit,'counter':dict(collections.Counter(r['generation']['template']+':'+str(r['generation']['parameters']['target']) for r in sample))})
replays=[g.generate('quotient',1,7,p=4),g.generate('radical',1,2),g.generate('blank',1,2,degree=3),g.generate('blank',1,2,degree=3),g.generate('blank',2,-4,degree=2)]
ids=['q-49059','q-49063','q-167635','q-167587','q-167617'];save('source-replays.json',replays)
replay_report=[]
for sid,r in zip(ids,replays):
 q=next(q for q in source['material']['kp'][':knowledge-point/questions'] if q[':question/math-academy-id']==sid)
 sf=q[':question/answer-fields'][0]
 want=[parse(a[':answer/value']) for a in sf[':answer-field/choices']]; got=[parse(a[':answer/value']) for a in field(r)[':answer-field/choices']]
 assert len(want)==len(got) and all(any(S.simplify(a-b)==0 for b in got) for a in want)
 replay_report.append({'source_id':sid,'uuid':q[':question/id'],'all_bank_choices_matched':True,'count':len(got),'correct_matched':S.simplify(parse(sf[':answer-field/correct'][':answer/value'])-parse(key(r)[':answer/value']))==0,'prompt_repair':'Explicitly state f(x) from source solution; remove orphaned A/B references.' if sid.startswith('q-167') else 'Normalize TeX, add domain assumption; same integral.','solution_stages':'algebraic rewrite, separation, constant extraction, power rule, final primitive (checked independently)'})
save('source-replay-results.json',{'supported_band':'moderate','cases':replay_report,'unsupported':'Easy, unclassified source bank questions and hard are not claimed supported; source gaps recorded in source-analysis.json.'})
# Relevant role changes hold all bank entries fixed. Coefficient change and irrelevant degree/order pairs.
pairs=[]
for fam in ['quotient','radical']:
 for target in range(1,5):pairs.append({'label':f'{fam}-role-0-to-{target}','kind':'relevant','before':g.generate(fam,1,2,target=0),'after':g.generate(fam,1,2,target=target),'expected':'different'})
pairs += [ {'label':'blank-sign','kind':'relevant','before':g.generate('blank',2,4,degree=2),'after':g.generate('blank',2,-4,degree=2),'expected':'different'}, {'label':'blank-degree','kind':'irrelevant','before':g.generate('blank',2,4,degree=2),'after':g.generate('blank',2,4,degree=3),'expected':'same'}, {'label':'radio-order','kind':'irrelevant','before':g.generate('radical',1,2),'after':g.generate('radical',1,2,order=[4,3,2,1,0]),'expected':'same'} ]
for p in pairs:
 same=S.simplify(parse(key(p['before'])[':answer/value'])-parse(key(p['after'])[':answer/value']))==0
 assert same==(p['expected']=='same')
 assert p['before']['question'][':question/problem']!=p['after']['question'][':question/problem'] or p['label']=='radio-order'
save('counterfactuals.json',pairs)
allrecords=sample+controlled+replays+batch+[r for p in pairs for r in [p['before'],p['after']]]
results=[];failures=[]
for i,r in enumerate(allrecords):
 try:results.append(check(r))
 except Exception as e:failures.append({'index':i,'qid':r['question'][':question/id'],'error':str(e)})
save('math-results.json',{'records':len(allrecords),'passed':len(results),'failures':failures,'results':results,'method':'Parse actual prompt, choices and every aligned solution expression; exact SymPy differentiation of each expression. Metadata only supplies blank denominator power, separately compared by rendering; no generator bank/expression helper used.'})
# Native grading in one batch, including every control, replay and counterfactual.
cases=[]
for i,r in enumerate(controlled+replays+batch):
 f=field(r);ks=key(r);checks=[]
 if f[':answer-field/type'].endswith('radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ks[':answer/id'] else 'rejected','purpose':'all independently differentiated options'} for a in f[':answer-field/choices']]
 else:
  correct=parse(ks[':answer/value']); equivalent=S.factor(correct)
  checks=[{'submitted':str(correct),'expected':'accepted','purpose':'independent plain arithmetic equivalent'}, {'submitted':str(equivalent),'expected':'accepted','purpose':'factored rational equivalent'}, {'submitted':str(correct+1/x),'expected':'rejected','purpose':'wrong reciprocal coefficient'}, {'submitted':str(S.diff(correct,x)),'expected':'rejected','purpose':'integrand instead of primitive'}]
 cases.append({'label':f'control-replay-batch-{i}','record':r,'checks':checks})
for p in pairs:
 for label in ['before','after']:
  r=p[label];other=p['after' if label=='before' else 'before'];f=field(r)
  if f[':answer-field/type'].endswith('radio'):
   otherid=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==key(other)[':answer/value']);checks=[{'submitted_answer_id':key(r)[':answer/id'],'expected':'accepted','purpose':'current response'}, {'submitted_answer_id':otherid,'expected':'accepted' if p['expected']=='same' else 'rejected','purpose':'paired old response'}]
  else:checks=[{'submitted':str(parse(key(z)[':answer/value'])),'expected':'accepted' if z is r or p['expected']=='same' else 'rejected','purpose':'current or paired response'} for z in [r,other]]
  cases.append({'label':p['label']+'-'+label,'record':r,'checks':checks})
for case in cases:
 for ck in case['checks']:
  if 'submitted' in ck:ck['submitted']=ck['submitted'].replace('**','^')
save('grader-input.json',cases)
# Renderer includes all decision role forms plus complete controlled pairs and source representatives.
render=replays[:2]+[controlled[i] for i in range(0,40,4)]+[r for p in pairs for r in [p['before'],p['after']]]
save('render-records.json',render)
# Relocation, CLI boundary rejection, deterministic replay; all writes in E.
manifest=json.load(open(W/'package.json'));rel=E/'relocated';rel.mkdir(exist_ok=True)
for n in manifest['files']:shutil.copy2(W/n,rel/n)
command=[sys.executable,str(W/'generator.py'),'--count','5','--seed','8207419','--difficulty','moderate','--format','json']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
a=subprocess.run(command,cwd=E,env=env,capture_output=True,text=True);b=subprocess.run([sys.executable,str(rel/'generator.py')]+command[2:],cwd=E,env=env,capture_output=True,text=True)
cli=[]
for args in [['--count','0'],['--count','-1'],['--count','1001'],['--difficulty','easy'],['--difficulty','hard']]:
 c=subprocess.run([sys.executable,str(rel/'generator.py')]+args,cwd=E,env=env,capture_output=True,text=True)
 cli.append({'args':args,'exit':c.returncode,'stdout':c.stdout,'stderr':c.stderr})
save('packaging-results.json',{'command':command,'actual_dependencies':{'python':'.'.join(map(str,sys.version_info[:3])),'packages':{'sympy':S.__version__}},'manifest_dependencies':manifest['dependencies'],'same_after_relocation':a.returncode==b.returncode==0 and json.loads(a.stdout)==json.loads(b.stdout),'replay_same':g.sample(240,420106731)==sample,'cli_cases':cli,'runtime_files':manifest['files'],'external_output':'no asset or file-output arguments; source inspection finds only JSON stdout; bytecode disabled; working directory is evidence_root.'})
save('relocation-sample.json',json.loads(b.stdout));save('package-after-initial.json',hashes())
print(json.dumps({'math':{'records':len(allrecords),'passed':len(results),'failures':failures[:3]},'sample_audit':audit,'replay_cases':len(replay_report),'grader_records':len(cases),'render_records':len(render),'package_unchanged':hashes()==json.load(open(E/'package-before.json'))}))

import json, re, sys, hashlib, importlib.util, pathlib, subprocess, shutil
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
R=pathlib.Path(__file__).resolve().parent
JOB=R.parent
PKG=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else JOB/'workspace'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed',PKG/'17592186096613.py'); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
x=s.Symbol('x',positive=True)
def save(n,v): (R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
def expr(t):
 t=t.replace('\u2061','').replace(r'\dfrac',r'\frac').replace(r'\operatorname{ln}',r'\ln').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 def group(i):
  assert t[i]=='{',t
  j=i+1; depth=1
  while depth:
   depth+=(t[j]=='{')-(t[j]=='}'); j+=1
  return t[i+1:j-1],j
 while r'\frac' in t:
  i=t.rfind(r'\frac'); a,j=group(i+5); b,k=group(j); t=t[:i]+'(('+a+')/('+b+'))'+t[k:]
 t=re.sub(r'(?:\\ln|ln)\s*x', ' log(x)',t).replace('^','**').replace('{','(').replace('}',')').strip().rstrip('.,')
 return parse_expr(t,local_dict={'x':x,'e':s.E,'log':s.log},transformations=standard_transformations+(implicit_multiplication_application,))
def fn(q):return expr(re.search(r'\$y\s*=\s*(.*?)\$',q[':question/problem'])[1])
def correct(q):
 f=q[':question/answer-fields'][0]; key=f[':answer-field/correct']; key=key[1] if isinstance(key,list) else key[':answer/id']; return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key)
def norm(t):return re.sub(r'\s+','',t.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln').replace('lnx',r'\lnx'))
source=json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']
source_results=[]; replay=[]
for q in source:
 sid=q[':question/math-academy-id']; c=s.simplify(fn(q)/s.log(x)); n,d=s.fraction(c/s.E if c.has(s.E) else c); p={'n':int(n),'d':int(d),'k':int(c.has(s.E))}
 try:
  a=g.generate_easy(seed=17,profile='raw-'+sid,parameters=p); replay.append(a)
  aq=a['question']; oldbank=[expr(v[':answer/value']) for f in q.get(':question/answer-fields',[]) for v in f[':answer-field/choices']]; newbank=[expr(v[':answer/value']) for f in aq.get(':question/answer-fields',[]) for v in f[':answer-field/choices']]
  result={'id':q[':question/id'],'sid':sid,'parameters':p,'prompt':norm(aq[':question/problem'])==norm(q[':question/problem']),'bank':sorted(map(str,oldbank))==sorted(map(str,newbank)),'solution':norm(aq.get(':question/worked-solution',''))==norm(q.get(':question/worked-solution',''))}
 except ValueError as e:result={'id':q[':question/id'],'sid':sid,'parameters':p,'error':str(e)}
 source_results.append(result)
save('source-replay.json',{'results':source_results,'records':replay})
# independently selected small profile/boundary sample, not an exhaustive sampler audit
records=[g.generate_easy(seed=i) for i in range(91820,91850)]
params=[('integer',-30,1,0),('integer',30,1,0),('fraction',29,12,0),('fraction',2,3,0),('euler',-30,1,1),('euler',30,1,1),('canonical',-29,12,0),('equivalent-entry',29,12,0)]
records += [g.generate_easy(seed=997,profile=b,parameters={'n':n,'d':d,'k':k}) for b,n,d,k in params]
pairs=[g.generate_easy(seed=17,profile='integer',parameters={'n':n,'d':1,'k':0}) for n in [7,-7]]
pairs+=[g.generate_easy(seed=18,profile='integer',parameters={'n':7,'d':1,'k':0})]
save('counterfactual-records.json',pairs)
save('independent-records.json',records)
batch=json.load(open(sys.argv[2] if len(sys.argv)>2 else JOB/'samples.json')); save('batch-records.json',batch)
checks=[]; grader=[]
for label,rs in [('sample',records),('batch',batch),('counterfactual',pairs)]:
 for i,r in enumerate(rs):
  q=r['question']; f=q[':question/answer-fields'][0]; target=s.diff(fn(q),x); answer=expr(correct(q)); vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']]; last=expr(q[':question/worked-solution'].split('& =')[-1].split(r'\end')[0])
  checks.append({'set':label,'i':i,'id':q[':question/id'],'target':str(target),'key_ok':s.simplify(answer-target)==0,'solution_ok':s.simplify(last-target)==0,'unique_radio_key':sum(s.simplify(v-target)==0 for v in vals)==1 if f[':answer-field/type'].endswith('radio') else True})
  responses=[]
  if f[':answer-field/type'].endswith('radio'):
   for a,v in zip(f[':answer-field/choices'],vals):responses.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if s.simplify(v-target)==0 else 'rejected','purpose':'independent differentiation of visible prompt'})
  else:
   c=s.simplify(target*x); n,d=s.fraction(c)
   for text,expect in [(f'{n}/({d}*x)','accepted'),(f'({n}/{d})*x^(-1)','accepted'),(f'{2*n}/({2*d}*x)','accepted'),(str(-target),'rejected'),(str(c*x),'rejected'),('0','rejected')]:responses.append({'submitted':text,'expected':expect,'purpose':'equivalent or plausible wrong expression'})
  grader.append({'label':f'{label}-{i}','record':r,'checks':responses})
save('math-results.json',checks);save('grader-input.json',grader)
# Minimal missing family regression; expected successful generation, current errors retained.
restr=[]
for profile in [None,'fraction','canonical','raw-q-70887']:
 try: r=g.generate_easy(seed=17,profile=profile,parameters={'n':1,'d':4,'k':0}); restr.append({'profile':profile,'record':r,'passed':s.simplify(fn(r['question'])-s.log(x)/4)==0})
 except ValueError as e:restr.append({'profile':profile,'error':str(e),'passed':False})
save('missing-reciprocal-family.json',{'command':'../.venv/bin/python review_tests.py PACKAGE [CANDIDATE_RECORDS] (use job python absolute path)','source_id':'4890c920-695d-52f8-8b20-5f7886a5c8be','expected':'Generate ln(x)/4 and derivative 1/(4x), preserving five-option reciprocal bank and rewrite stage','cases':restr})
rejection=[]
for p in [{'n':0,'d':1,'k':0},{'n':2,'d':4,'k':0},{'n':31,'d':1,'k':0},{'n':2,'d':13,'k':0},{'n':2,'d':1,'k':2}]:
 try:g.generate_easy(seed=17,parameters=p); rejection.append({'parameters':p,'rejected':False})
 except ValueError as e:rejection.append({'parameters':p,'rejected':True,'error':str(e)})
save('packaging-tests.json',{'python':sys.version.split()[0],'sympy':s.__version__,'manifest':json.load(open(PKG/'package.json'))['dependencies'],'deterministic':records[0]==g.generate_easy(seed=91820),'batch_replay':batch==[g.generate_easy(seed=3129290382+i) for i in range(5)],'invalid_parameters':rejection,'package_hashes':{str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}})
save('render-records.json',batch+pairs+[records[-3]])
print(json.dumps({'source':source_results,'math_cases':len(checks),'math_failures':[v for v in checks if not all(v[k] for k in ['key_ok','solution_ok','unique_radio_key'])],'missing_reciprocal':restr,'sample_profiles':{b:sum(r['generation']['bank_profile']==b for r in records) for b in ['integer','fraction','euler','canonical','equivalent-entry']}},indent=2))

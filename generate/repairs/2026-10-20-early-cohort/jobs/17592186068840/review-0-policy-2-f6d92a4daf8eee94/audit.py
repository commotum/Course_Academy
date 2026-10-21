import os,sys,json,hashlib,importlib.util,platform,shutil,subprocess,collections,re
from pathlib import Path
E=Path(__file__).resolve().parent
B=E.parent; W=B/'workspace'; REPO=Path('/home/jake/Developer/Course_Academy')
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('audit_generator',W/'17592186068840.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def qbank(r):
 f=r['question'][':question/answer-fields'][0];return f,[(a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][1]) for a in f[':answer-field/choices']]
manifest=json.load(open(W/'package.json'))
save('package-baseline.json',{'files':{f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in manifest['files']+['package.json']},'python':platform.python_version(),'sympy':g.s.__version__,'dependencies':manifest['dependencies']})
source=json.load(open(B/'source/source.json'))['material']['kp']
# independently match by MA source identifier, not mutable entity IDs
by_ma={t['source'][':question/math-academy-id']:n for n,t in g.TEMPLATES.items() if 'source' in t}
replays=[]; results=[]
for q in source[':knowledge-point/questions']:
 ma=q[':question/math-academy-id'];name=by_ma.get(ma)
 if not name:
  results.append({'source_id':q[':question/id'],'ma_id':ma,'status':'unsupported','problem':q[':question/problem']});continue
 p={'a':1} if name=='autonomous_tan' else {'rate':'0.03','ambient':25} if name=='temperature_blank' else {'h':0}
 r=g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],71021,name,parameters=p,profile='observed_'+name);replays.append(r)
 f,bank=qbank(r);sf=q[':question/answer-fields'][0]
 clean=lambda v:v.replace('\u2061','')
 eq={'prompt':clean(q[':question/problem'])==clean(r['question'][':question/problem']),'solution':clean(q[':question/worked-solution'])==clean(r['question'][':question/worked-solution']),'complete_bank':sorted(clean(a[':answer/value']) for a in sf[':answer-field/choices'])==sorted(clean(v) for v,c in bank),'correct':clean(sf[':answer-field/correct'][':answer/value'])==clean(next(v for v,c in bank if c))}
 results.append({'source_id':q[':question/id'],'ma_id':ma,'template':name,'checks':eq,'status':'passed' if all(eq.values()) else 'failed'})
save('source-replay-records.json',replays);save('source-replay.json',results)
# small independently selected seed sample, plus explicit boundaries of supported easy slots
records=[];errors=[]
for seed in range(71021,71045):
 try: records.append(g.generate_easy(seed))
 except Exception as ex: errors.append({'seed':seed,'error':str(ex)})
for name in ['autonomous_tan','reciprocal_cube','negative_exp','cube_power']:
 for value in ([1,5] if name=='autonomous_tan' else [-8,0,8]):
  try:records.append(g.generate_easy(71057,name,parameters={'a' if name=='autonomous_tan' else 'h':value}))
  except Exception as ex:errors.append({'template':name,'value':value,'error':str(ex)})
# test moderate boundaries once per family, including blank
for name,t in g.TEMPLATES.items():
 if t['level']=='moderate':records.append(g.generate_moderate(71081,name,parameters={'rate':'0.06','ambient':35} if name=='temperature_blank' else {'h':-8}))
save('independent-records.json',records);save('sampling.json',{'seed_range':[71021,71044],'errors':errors,'counts':dict(collections.Counter(r['generation']['template'] for r in records))})
batch=json.load(open(B/'samples.json'));save('batch-records.json',batch)
# Most data held fixed. Relevant: sign-sensitive changed shift and coefficient. Irrelevant: shuffle seed.
pairs=[g.generate_easy(71101,'reciprocal_cube',parameters={'h':0}),g.generate_easy(71101,'reciprocal_cube',parameters={'h':1}),g.generate_easy(71102,'reciprocal_cube',parameters={'h':0}),g.generate_easy(71101,'autonomous_tan',parameters={'a':1}),g.generate_easy(71101,'autonomous_tan',parameters={'a':2}),g.generate_moderate(71101,'temperature_blank',parameters={'rate':'0.03','ambient':25}),g.generate_moderate(71101,'temperature_blank',parameters={'rate':'0.03','ambient':35})]
save('counterfactual-records.json',pairs)
# Actual grader checks every candidate, plus equivalent and wrong blank responses.
cases=[]
for i,r in enumerate(records+batch+pairs+replays):
 f,bank=qbank(r)
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independent choice selection contract'} for a in f[':answer-field/choices']]
 else:
  rate=r['generation']['parameters']['rate'];n=int(rate[-2:]);checks=[{'submitted':v,'expected':expected,'purpose':why} for v,expected,why in [(f'e^(-{n}t/100)','accepted','rational exponent equivalent'),(f'e^(-{rate}t)','accepted','baseline decimal exponent'),(f'e^({rate}t)','rejected','wrong exponent sign'),('0','rejected','zero factor loses general family')]]
 cases.append({'label':str(i)+':'+r['generation']['template'],'record':r,'checks':checks})
# Reciprocal exponential still satisfies single exponential equivalence as a learner notation, and source places no syntax restriction.
tr=next(r for r in replays if r['generation']['template']=='temperature_blank')
cases.append({'label':'source valid reciprocal exponential','record':tr,'checks':[{'submitted':'1/e^{0.03t}','expected':'accepted','purpose':'equivalent nonzero factor; no source syntax restriction'},{'submitted':'e^{-0.03t}','expected':'accepted','purpose':'control'}]})
save('grader-input.json',cases)
# Valid coefficients deliberately absent from construction domain. Keep failing acceptance requests.
restrictions=[]
for name,p in [('autonomous_tan',{'a':-1}),('reciprocal_cube',{'h':0,'a':-1}),('negative_exp',{'h':0,'a':-1}),('cube_power',{'h':0,'a':-1}),('canonical_root',{'h':0,'a':1,'n':1})]:
 try:g.generate_easy(71101,name,parameters=p);out='accepted'
 except Exception as ex:out=type(ex).__name__+': '+str(ex)
 restrictions.append({'template':name,'parameters':p,'outcome':out})
save('restriction-tests.json',restrictions)
# Replay, package relocation and runtime dependencies
r=g.generate_easy(71109); deterministic=r==g.generate_easy(71109)
rel=E/'relocated';rel.mkdir(exist_ok=True);shutil.copy2(W/'17592186068840.py',rel/'17592186068840.py');(rel/'17592186068840').mkdir(exist_ok=True);shutil.copy2(W/'17592186068840/source.json',rel/'17592186068840/source.json')
p=subprocess.run([sys.executable,str(rel/'17592186068840.py'),'--difficulty','easy','--seed','71109','--format','json'],cwd='/tmp',capture_output=True,text=True)
save('packaging.json',{'deterministic':deterministic,'relocation_command':p.args,'relocation_rc':p.returncode,'relocation_equal':json.loads(p.stdout)==[r] if p.returncode==0 else False,'stderr':p.stderr,'dependencies_exact':manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':g.s.__version__}},'history_exists':(B/'repair-history.json').exists(),'preflight_exists':(B/'repair-preflight.json').exists()})
print('source replay',collections.Counter(x['status'] for x in results),'sample',len(records),'errors',len(errors),'grader cases',len(cases))

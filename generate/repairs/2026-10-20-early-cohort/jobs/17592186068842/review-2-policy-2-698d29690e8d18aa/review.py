import os,sys,json,hashlib,importlib.util, pathlib,re,copy,subprocess,platform
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent; REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PKG=JOB/'workspace'
def save(n,x): (ROOT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False))
def load(n):return json.load(open(n))
def module(path):
 spec=importlib.util.spec_from_file_location('reviewed',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=module(PKG/'17592186068842.py')
# Preserve the package content binding before any executable tests.
save('package-before.json',{str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()})
s=load(ROOT/'source-extract.json');source=[];replay=[]
for q in s['questions']:
 t=next(t for t,d in m.TEMPLATES.items() if d[1]==q[':question/math-academy-id']);d=m.TEMPLATES[t];r=m.generate(d[0],62983,t,parameters=d[2],profile='observed');source.append(r)
 f=q[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
 norm=lambda x: x.replace(r'\left','').replace(r'\right','').replace(' ','').replace('\n','')
 original=[norm(a[':answer/value']) for a in f[':answer-field/choices']];generated=[norm(a[':answer/value']) for a in gf[':answer-field/choices']]
 cv=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])
 replay.append({'source_id':q[':question/id'],'template':t,'prompt_match':norm(q[':question/problem'])==norm(r['question'][':question/problem']),'complete_bank_match':sorted(original)==sorted(generated),'correct_match':norm(f[':answer-field/correct'][':answer/value'])==norm(cv),'solution_match':norm(q[':question/worked-solution'])==norm(r['question'][':question/worked-solution'])})
save('source-replay-records.json',source);save('source-replay.json',{'cases':replay,'canonical_radical_supported':False,'canonical_answer_bank_captured':False})
records=[];errors=[]
for t,(level,src,default) in m.TEMPLATES.items():
 for label,p in [('lower',{k:(2 if t=='double_factor' and k in ('b','c','d') else 2 if k=='base' or k=='n' and t in ('polynomial_factor','sqrt_quotient','double_factor') else 1) for k in default}),('upper',{k:(4 if k=='n' else 5) for k in default}),('fresh',None)]:
  try:records.append(m.generate(level,867209,t,parameters=p))
  except Exception as e: errors.append({'template':t,'case':label,'parameters':p,'exception':repr(e)})
batch=load(JOB/'samples.json');save('batch.json',batch);save('independent-records.json',records);save('generation-errors.json',errors)
# Controlled relevant changes to dependent evidence; seed-only changes affect only choice order.
pairs=[]
for label,p,seed in [('before',{'n':2,'a':2},9106),('relevant',{'n':3,'a':2},9106),('irrelevant',{'n':2,'a':2},9107)]:pairs.append(m.generate_easy(seed,'rational_product',parameters=p))
save('counterfactual-records.json',pairs)
# Exact runtime contract and relocation; only a review copy is executed.
import sympy as sp,shutil
manifest_files=load(PKG/'package.json')['files']
relocated=ROOT/'relocated';relocated.mkdir(exist_ok=True)
for name in manifest_files:
 (relocated/name).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PKG/name,relocated/name)
mr=module(relocated/'17592186068842.py');r=m.generate_easy(812773);rr=mr.generate_easy(812773)
reject=[]
for kwargs in [dict(template='simple_quotient',parameters={'n':0}),dict(template='sqrt_quotient',parameters={'n':3,'a':1}),dict(template='simple_quotient',parameters={'n':True}),dict(template='simple_quotient',parameters={'n':1,'a':2}),dict(template='simple_quotient',field_type='free'),dict(template='exp_sum')]:
 try:m.generate_easy(21,**kwargs);reject.append({'input':kwargs,'rejected':False})
 except (ValueError,AssertionError) as e:reject.append({'input':kwargs,'rejected':True,'message':str(e)})
manifest=load(PKG/'package.json');save('packaging.json',{'python':platform.python_version(),'sympy':sp.__version__,'declared':manifest['dependencies'],'replay_identical':r==m.generate_easy(812773),'relocation_identical':r==rr,'rejection_cases':reject,'files_missing':[n for n in manifest['files'] if not (PKG/n).is_file()],'runtime_output':'JSON records only; no generated image assets or external writes in implementation.'})
save('generation-summary.json',{'count':len(records),'errors':errors,'templates':dict(__import__('collections').Counter(r['generation']['template'] for r in records))})
print('sampled',len(records),'errors',errors,'source mismatches',[x for x in replay if not all(x[k] for k in ['prompt_match','complete_bank_match','correct_match','solution_match'])])

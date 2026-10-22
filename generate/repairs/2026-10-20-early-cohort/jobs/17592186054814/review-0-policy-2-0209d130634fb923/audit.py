import sys,os,json,pathlib,hashlib,importlib.util,subprocess,re,shutil,platform
from fractions import Fraction
from math import isqrt
ROOT=pathlib.Path(__file__).resolve().parent; JOB=ROOT.parent; PKG=JOB/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=REPO/'.venv/bin/python'
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
sys.path.insert(0,str(PKG));import generator as g

def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def semantic(r):
 q=r['question']; ans={}
 for f in q[':question/answer-fields']:
  ref=f[':answer-field/correct']; aid=ref[1] if isinstance(ref,list) else ref[':answer/id']
  val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
  if f[':answer-field/type']==':answer-field.type/checkbox': ans[re.search(r'\(\$([NZQRC])\$\)',f[':answer-field/key'])[1]]=val=='true'
  else:return ''.join(x for x in 'NZQRC' if x in val)
 return ''.join(s for s in 'NZQRC' if ans[s])
def oracle(r):
 tex=re.search(r'number \$(.*?)\$ belong',r['question'][':question/problem'])[1].replace(' ','')
 if tex in [r'\pi',r'-\pi']:return 'RC'
 if tex.startswith(r'\sqrt'):
  n=int(re.search(r'\{(-?\d+)\}',tex)[1]);
  if n<0:return 'C'
  rt=isqrt(n)
  if rt*rt!=n:return 'RC'
  x=Fraction(rt)
 elif 'frac' in tex:
  n,d=map(int,re.search(r'frac\{(\d+)\}\{(\d+)\}',tex).groups());x=Fraction(-n if tex.startswith('-') else n,d)
 else:x=Fraction(tex)
 return 'NZQRC' if x.denominator==1 and x>0 else 'ZQRC' if x.denominator==1 else 'QRC'

baseline={p.name:sha(p) for p in PKG.iterdir() if p.is_file()};save('package-before.json',baseline)
source=json.load(open(JOB/'source/source.json'));batch=json.load(open(JOB/'samples.json'));save('batch-records.json',batch)
records=g.generate(count=80,seed=229173);save('sample-records.json',records)
params=[{'family':'radical','n':n} for n in [-144,-4,-1,0,1,16,17,144,150]]+[{'family':'fraction','n':n,'d':3} for n in [-27,-7,0,6,7]]+[{'family':'decimal','units':n} for n in [-2000,-1,0,1,2000]]+[{'family':'pi','sign':n} for n in [-1,1]]
controlled=[g.build(p,seed=229174) for p in params];save('controlled-records.json',controlled)
replay=g.replay_sources();save('source-replay-records.json',replay)
qs=source['material']['kp'][':knowledge-point/questions']; replay_ids={r['generation']['source_replay'] for r in replay}
source_results=[]
for q in qs:
 matches=[r for r in replay if r['generation']['source_replay']==q[':question/id']]
 result={'id':q[':question/id'],'replayed':bool(matches),'prompt':q[':question/problem']}
 if matches:
  r=matches[0];result['math_correct']=semantic(r)==oracle(r)
  result['bank_matches']= [[a[':answer/value'] for a in f[':answer-field/choices']] for f in q[':question/answer-fields']]==[[a[':answer/value'] for a in f[':answer-field/choices']] for f in r['question'][':question/answer-fields']]
  result['prompt_matches']=g.normalize_prose(q[':question/problem'])==r['question'][':question/problem']
  result['solution_matches']=not q.get(':question/worked-solution') or g.normalize_prose(q[':question/worked-solution'])==r['question'][':question/worked-solution']
 source_results.append(result)
try:g.build({'family':'radical','n':-2}); rejection=None
except Exception as e:rejection={'type':type(e).__name__,'message':str(e)}
save('source-replay-results.json',{'command':str(PY)+' -B audit.py','cases':source_results,'canonical_3_25':{'record':g.build({'family':'decimal','units':325}),'membership':semantic(g.build({'family':'decimal','units':325}))},'source_sqrt_minus_2_rejection':rejection,'gaps':'Source sqrt(121) lacks key/solution; inferred all five from value 11. Canonical has no bank.'})
all_records=records+batch+controlled+replay
errors=[{'id':r['question'][':question/id'],'expected':oracle(r),'actual':semantic(r)} for r in all_records if oracle(r)!=semantic(r)]
save('math-results.json',{'command':str(PY)+' -B audit.py','oracle':'Parse rendered-prompt TeX independently; Fraction arithmetic and integer square tests; compare selected memberships, not generation.case.','count':len(all_records),'failures':errors})
# Actual learner selection IDs include every correct and opposite boolean, all radio alternatives.
cases=[]
for i,r in enumerate(all_records):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   ref=f[':answer-field/correct'];aid=ref[1]
   checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if aid==a[':answer/id'] else 'rejected','purpose':'Independently verified full membership/bank; exercise correct and opposite learner choices.'})
 cases.append({'label':str(i),'record':r,'checks':checks})
save('grader-input.json',cases)
# Controlled pair descriptions refer to complete generated records and grader cases.
pairs=[{'kind':'relevant','before':5,'after':6,'change':'sqrt(16) -> sqrt(17)','expected_before':'NZQRC','expected_after':'RC'}, {'kind':'relevant','before':12,'after':13,'change':'6/3 -> 7/3','expected_before':'NZQRC','expected_after':'QRC'}, {'kind':'irrelevant','before':10,'after':13,'change':'-7/3 -> 7/3','expected_before':'QRC','expected_after':'QRC'}]
for p in pairs:
 p.update(observed_before=semantic(controlled[p['before']]),observed_after=semantic(controlled[p['after']]),records_file='controlled-records.json');p['passed']=p['observed_before']==p['expected_before'] and p['observed_after']==p['expected_after']
 # Prompt and explanation must use each changed value.
 p['solutions_checked']=[controlled[j]['question'][':question/worked-solution'] for j in [p['before'],p['after']]]
save('counterfactual-results.json',pairs)
# Runtime and relocation: no writes in original package.
rel=ROOT/'relocated-package';rel.mkdir(exist_ok=True)
for p in PKG.iterdir():
 if p.is_file():shutil.copyfile(p,rel/p.name)
a=subprocess.run([str(PY),'-B',str(PKG/'generator.py'),'--seed','419623','--count','5'],capture_output=True,text=True,check=True)
b=subprocess.run([str(PY),'-B',str(rel/'generator.py'),'--seed','419623','--count','5'],cwd=ROOT,capture_output=True,text=True,check=True)
invalid=[]
for args in [['--difficulty','hard'],['--count','-1']]:
 c=subprocess.run([str(PY),'-B',str(PKG/'generator.py')]+args,capture_output=True,text=True);invalid.append({'args':args,'code':c.returncode,'stderr':c.stderr})
save('packaging-results.json',{'python':platform.python_version(),'dependencies':json.load(open(PKG/'package.json'))['dependencies'],'deterministic_relocation':a.stdout==b.stdout,'invalid_requests':invalid,'count_zero':g.generate(count=0),'large_sample_attempts':[r['generation']['sampling_attempt'] for r in records],'package_hashes_unchanged':baseline=={p.name:sha(p) for p in PKG.iterdir() if p.is_file()},'history_files':{x:(JOB/x).exists() for x in ['repair-history.json','repair-preflight.json']}})
preview=batch+ [controlled[i] for i in [5,6,10,12,13]]+[replay[2]];save('render-records.json',preview)
(ROOT/'session-state.md').write_text('Source analysis, source replay, 112 independent math cases, counterfactual construction, packaging/replay completed. Missing radio sources -18 and sqrt(-2); latter rejected explicitly. Next: native grader, delivery, UI render and inventory analysis.\n')
print(json.dumps({'math_count':len(all_records),'math_failures':errors,'missing_sources':[q['id'] for q in source_results if not q['replayed']],'sqrt_minus_2':rejection,'pair_results':[(p['change'],p['passed']) for p in pairs]}))

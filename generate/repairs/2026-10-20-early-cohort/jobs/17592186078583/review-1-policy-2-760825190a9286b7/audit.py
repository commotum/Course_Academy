import sys,os,json,hashlib,importlib.util,re,collections,platform,shutil,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path('/home/jake/Developer/Course_Academy');JOB=ROOT/'generate/repairs/2026-10-20-early-cohort/jobs/17592186078583';PKG=JOB/'workspace';OUT=Path(__file__).resolve().parent
import sympy as sp

def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def hashes():return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}
def load_module(path):
 spec=importlib.util.spec_from_file_location('reviewed',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=load_module(PKG/'17592186078583.py');save('package-before.json',hashes())
s=json.load(open(JOB/'source/source.json'));bank=s['material']['kp'][':knowledge-point/questions'];batch=json.load(open(JOB/'samples.json'));save('batch.json',batch)
replay=[];rr=[]
for q in bank:
 sid=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 nums=list(map(int,re.findall(r'\$\{(\d+)\}\^',q[':question/problem'])))
 params={'S':nums[-1]}
 if level=='moderate':params['I']=nums[0]
 try:
  r=m.generate(level,seed=90271,profile=sid,parameters=params);replay.append(r);f=r['question'][':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
  comparisons={'prompt':r['question'][':question/problem']==q[':question/problem'],'solution':r['question'][':question/worked-solution']==q[':question/worked-solution'],'complete_bank':sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']),'correct_value':next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']}
  rr.append({'source_id':q[':question/id'],'template':sid,'parameters':params,'comparisons':comparisons})
 except Exception as e:rr.append({'source_id':q[':question/id'],'template':sid,'parameters':params,'error':str(e)})
save('source-replay-records.json',replay);save('source-replay.json',{'command':'/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186078583/review-1-policy-2-760825190a9286b7/audit.py','cases':rr,'canonical':'Not a supported template; canonical bank absent in source; same law solution covered by source cases.'})
samples=[]
for level,templates in m.DEFAULT_TEMPLATES.items():
 for template in templates:
  for seed in range(104729,104733):samples.append(m.generate(level,seed,template=template))
  unit=m.TEMPLATES[template]['unit'];lo,hi=(10,40) if unit=='C' else (50,85)
  for ambient in (lo,hi):
   p={'S':ambient}
   if level=='moderate':p['I']=max(m.INITIAL_BOUNDS[template][0],ambient+10)
   samples.append(m.generate(level,104759,template=template,parameters=p))
save('samples.json',samples)
# Independent polynomial construction, using prompt temperatures rather than metadata.
T,k=sp.symbols('T k')
def expr(value):
 rhs=value.split('=')[1].replace(' ','').replace('kT','k*T').replace('k(','k*(').replace('T(','T*(')
 rhs=re.sub(r'(\d)([Tk(])',r'\1*\2',rhs)
 return sp.sympify(rhs,locals={'T':T,'k':k})
def correct_value(r):
 f=r['question'][':question/answer-fields'][0];return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
math=[]
for index,r in enumerate(samples+batch):
 q=r['question'];ambient=int(re.findall(r'\$\{(\d+)\}\^',q[':question/problem'])[-1]);f=q[':question/answer-fields'][0];expected=-k*(T-ambient)
 equations=[expr(c[':answer/value']) for c in f[':answer-field/choices']]
 hits=[i for i,e in enumerate(equations) if sp.expand(e-expected)==0]
 key=f[':answer-field/correct'][1];good=len(hits)==1 and f[':answer-field/choices'][hits[0]][':answer/id']==key
 solution_ok=f'-k(T-{ambient})' in q[':question/worked-solution']
 math.append({'index':index,'id':q[':question/id'],'ambient_from_prompt':ambient,'key_correct':good,'solution_correct':solution_ok,'unique_choices':len({str(sp.expand(e)) for e in equations})==5})
save('math.json',{'command':'/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186078583/review-1-policy-2-760825190a9286b7/audit.py','cases':math,'failed':[x for x in math if not all(x[y] for y in ['key_correct','solution_correct','unique_choices'])]})
# Relevant and irrelevant controlled changes, same seed/template.
cf=[m.generate('easy',92817,template='q-105917',parameters={'S':22}),m.generate('easy',92817,template='q-105917',parameters={'S':29}),m.generate('moderate',92817,template='q-37365',parameters={'S':64,'I':100}),m.generate('moderate',92817,template='q-37365',parameters={'S':65,'I':100}),m.generate('moderate',92817,template='q-37365',parameters={'S':64,'I':101})]
save('counterfactual-records.json',cf)
save('counterfactual-results.json',{'easy_relevant':[correct_value(r) for r in cf[:2]],'moderate_relevant':[correct_value(r) for r in cf[2:4]],'irrelevant_initial':[correct_value(cf[i]) for i in [2,4]],'irrelevant_solution_preserved':cf[2]['question'][':question/worked-solution']==cf[4]['question'][':question/worked-solution'],'seed':92817})
# Radio outcome checks for every choice, keyed independently by polynomial equality.
grader=[]
for i,r in enumerate(samples+batch+cf):
 ambient=int(re.findall(r'\$\{(\d+)\}\^',r['question'][':question/problem'])[-1]);f=r['question'][':question/answer-fields'][0]
 grader.append({'label':f'independent-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if sp.expand(expr(a[':answer/value'])+k*(T-ambient))==0 else 'rejected','purpose':'Independently derive model from ambient in prompt'} for a in f[':answer-field/choices']]})
save('grader-input.json',grader)
# Invalid parameters must fail; a valid missing source family must not be hidden here.
reject=[]
for level,template,params in [('easy','q-105917',{'S':9}),('easy','q-105917',{'S':41}),('easy','q-105917',{'S':22.5}),('moderate','q-37365',{'S':64,'I':64}),('moderate','q-37365',{'S':64,'I':111})]:
 try:m.generate(level,0,template=template,parameters=params);reject.append({'level':level,'template':template,'parameters':params,'rejected':False})
 except ValueError as e:reject.append({'level':level,'template':template,'parameters':params,'rejected':True,'message':str(e)})
# Relocate only runtime-required package files to evidence root; exercise unrelated cwd.
rel=OUT/'relocated';(rel/'17592186078583').mkdir(parents=True,exist_ok=True)
for source,target in [(PKG/'17592186078583.py',rel/'17592186078583.py'),(PKG/'17592186078583/templates.json',rel/'17592186078583/templates.json')]:shutil.copy2(source,target)
rm=load_module(rel/'17592186078583.py')
pack={'runtime':{'python':platform.python_version(),'packages':{'sympy':sp.__version__}},'declared':json.load(open(PKG/'package.json'))['dependencies'],'deterministic_replay':all(m.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters'] if r['generation']['seed']==104759 else None)==r for r in samples),'relocation':m.generate_easy(946123)==rm.generate_easy(946123),'rejections':reject,'external_outputs':'No files emitted by generate; runtime loads adjacent templates.json; sympy is only third-party import.'}
save('packaging.json',pack)
# Representative actual-UI records include full controlled pairs and each easy bank.
render=cf+[batch[0]]+[next(r for r in samples if r['generation']['template']==t) for t in ['q-106936','q-106878','q-106932']]
save('render-records.json',render)
save('package-after.json',hashes())
print(json.dumps({'source_replay':rr,'sample_count':len(samples),'math_failures':len([x for x in math if not x['key_correct'] or not x['solution_correct']]),'packaging':pack},indent=2))

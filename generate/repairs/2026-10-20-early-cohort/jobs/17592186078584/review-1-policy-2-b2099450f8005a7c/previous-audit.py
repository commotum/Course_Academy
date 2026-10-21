import sys, pathlib, json, importlib.util, hashlib, re, math, shutil, subprocess, collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
J=E.parent
P=J/'workspace'
R=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False))
def load(n): return json.loads(pathlib.Path(n).read_text())
def package_hashes():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
save('package-hashes-before.json',package_hashes())
spec=importlib.util.spec_from_file_location('reviewed',P/'17592186078584.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def num(a): return int(re.search(r'-?\d+',a[':answer/value']).group())
def info(r):
 q=r['question'];f=q[':question/answer-fields'][0];c=f[':answer-field/correct']; cid=c[1] if isinstance(c,list) else c[':answer/id'];ch=f[':answer-field/choices'];a=next(a for a in ch if a[':answer/id']==cid)
 return {'id':q[':question/id'],'template':r.get('generation',{}).get('template'),'answer':num(a),'rank':sorted(num(a) for a in ch).index(num(a))+1,'position':next(i+1 for i,a in enumerate(ch) if a[':answer/id']==cid),'values':[num(a) for a in ch]}
samples=[]
for template,level in g.TEMPLATES.items():
 if level=='hard':continue
 for seed in range(84101,84111 if level=='easy' else 84104): samples.append(g.generate(level,seed,template))
save('fresh-samples.json',samples)
batch=load(J/'samples.json');save('runner-batch.json',batch)
profiles=[];replays=[]
src=load(J/'source/source.json')['material']['kp']
def norm(s):
 return re.sub(r'\s+','',s.replace('\\\\','\\').replace('\\left','').replace('\\right','').replace('\\,',''))
for sid,(template,p) in g.ORIGINALS.items():
 r=g.generate(g.TEMPLATES[template],84153,template,parameters=p,profile=sid);profiles.append(r)
 original=next(q for q in src[':knowledge-point/questions'] if q[':question/math-academy-id']==sid)
 f=original[':question/answer-fields'][0];a=info(r)
 replays.append({'source_id':original[':question/id'],'ma_id':sid,'prompt_match':norm(original[':question/problem'])==norm(r['question'][':question/problem']),'solution_match':norm(original[':question/worked-solution'])==norm(r['question'][':question/worked-solution']),'bank_match':sorted(num(z) for z in f[':answer-field/choices'])==sorted(a['values']),'answer_match':num(f[':answer-field/correct'])==a['answer']})
missing=[{'source_id':q[':question/id'],'ma_id':q[':question/math-academy-id'],'reason':'Not in ORIGINALS, SOURCE_Q or template catalog'} for q in src[':knowledge-point/questions'] if q[':question/math-academy-id'] not in g.ORIGINALS]
save('source-replay.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python audit.py','replays':replays,'unsupported':missing,'canonical':'No bulb template or canonical bank captured; canonical parameters can use a different context but source wording cannot replay.'});save('source-replay-records.json',profiles)
# Independently calculate from printed prompt, not generation answer/parameters.
math_results=[]
for r in samples+batch+profiles:
 q=r['question'];s=q[':question/problem'];v=info(r)
 if q[':question/difficulty'].endswith('/easy'):
  rate,ambient=re.search(r'=-([\d.]+)\(T-(\d+)\)',s).groups();initial=int(re.search(r'initial temperature.*?\$\{(\d+)',s).group(1)); t=int(re.search(r'after \$(\d+)\$ minutes',s).group(1)); expected=math.floor(int(ambient)+(initial-int(ambient))*math.exp(-float(rate)*t)+.5)
 else:
  temps=[int(v) for v in re.findall(r'\$\{(\d+)\}\^\{∘\}[CF]',s)]
  if r['generation']['template']=='tea':I,O,Z,A=temps[:4]
  else:I,A,O,Z=temps[:4]
  t=int(re.search(r'After \$(\d+)\$ minutes',s).group(1)); expected=math.floor(t*math.log((Z-A)/(I-A))/math.log((O-A)/(I-A))+.5)
 math_results.append({'id':v['id'],'expected':expected,'actual':v['answer'],'passed':expected==v['answer'],'basis':'independent formula applied to printed prompt parse'})
save('math-results.json',math_results)
# Controlled changes with most of the instance held fixed.
p=dict(ambient=25,initial=100,rate='0.05',time=6)
cf=[g.generate('easy',84161,'coffee',parameters=p),g.generate('easy',84161,'coffee',parameters={**p,'time':9}),g.generate('easy',84161,'compressor',parameters=p)]
save('counterfactual-records.json',cf)
save('counterfactual-results.json',{'relevant':{'change':'time 6 ->9','before':info(cf[0]),'after':info(cf[1]),'expected':[81,73],'solution_checks':['T(6)=25+75' in cf[0]['question'][':question/worked-solution'],'T(9)=25+75' in cf[1]['question'][':question/worked-solution']]},'irrelevant':{'change':'coffee -> compressor, same scale and givens','before':info(cf[0]),'after':info(cf[2]),'response_preserved':info(cf[0])['answer']==info(cf[2])['answer']}})
# Real grader: every option for batch, fresh representatives and controlled pairs.
cases=[]
for i,r in enumerate(batch+samples[::10]+cf+profiles):
 f=r['question'][':question/answer-fields'][0];v=info(r);correct_id=f[':answer-field/correct'][1]
 cases.append({'label':f'review-{i}-{v["id"]}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct_id else 'rejected','purpose':'independently computed correct integer or plausible wrong option'} for a in f[':answer-field/choices']]})
save('grader-input.json',cases)
# Packaging, deterministic replay, relocation, and exact boundary rejection.
rejections=[]
for label,params in [('zero_time',{**p,'time':0}),('equilibrium_initial',{**p,'initial':25}),('negative_rate',{**p,'rate':'-0.05'}),('lower_valid_rate',{**p,'rate':'0.02'}),('upper_valid_rate',{**p,'rate':'0.25'})]:
 try:r=g.generate('easy',84161,'coffee',parameters=params);rejections.append({'case':label,'accepted':True,'record':r})
 except Exception as e:rejections.append({'case':label,'accepted':False,'error':str(e)})
rel=E/'relocated';(rel/'17592186078584').mkdir(parents=True,exist_ok=True)
shutil.copy2(P/'17592186078584.py',rel/'17592186078584.py');shutil.copy2(P/'17592186078584/source.json',rel/'17592186078584/source.json')
cmd=[sys.executable,'-B',str(rel/'17592186078584.py'),'--difficulty','easy','--seed','84101','--count','1','--format','json']
a=subprocess.run(cmd,cwd=E,capture_output=True,text=True);b=subprocess.run(cmd,cwd=E,capture_output=True,text=True)
if a.returncode==0:save('relocated-records.json',json.loads(a.stdout))
import sympy
save('packaging.json',{'declared':load(P/'package.json')['dependencies'],'actual':{'python':sys.version.split()[0],'packages':{'sympy':sympy.__version__}},'command':cmd,'relocation_exit':a.returncode,'relocation_stderr':a.stderr,'deterministic':a.stdout==b.stdout,'boundary_tests':rejections,'package_unchanged':package_hashes()==load(E/'package-hashes-before.json')})
save('raw-coverage.json',{'fresh':[info(r) for r in samples],'batch':[info(r) for r in batch],'profiles':[info(r) for r in profiles]})
print(json.dumps({'fresh':len(samples),'batch':len(batch),'replay':replays,'missing':missing,'math_failures':[z for z in math_results if not z['passed']],'cf':[info(r) for r in cf],'ranks':{t:dict(collections.Counter(info(r)['rank'] for r in samples if r['generation']['template']==t)) for t in g.TEMPLATES},'packaging':a.returncode},indent=2))
(E/'session-state.md').write_text('Source account complete. Fresh samples, source replays, independent numeric checks, controlled pairs, native grader input and packaging checks saved by audit.py. Demonstrated easy bank median shortcut across 50 fresh easy records and runner batch; delivery/native grading/rendering next. Missing latest body and pork source profiles. No repair history or preflight file exists.\n')

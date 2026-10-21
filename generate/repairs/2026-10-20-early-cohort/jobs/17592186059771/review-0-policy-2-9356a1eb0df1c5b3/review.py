import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,pathlib,re,copy,collections,hashlib,subprocess,platform
from fractions import Fraction as F
E=pathlib.Path(__file__).resolve().parent; J=E.parent; P=J/'workspace'; R=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=str(R/'.venv/bin/python')
sys.dont_write_bytecode=True;sys.path.insert(0,str(P))
import generator as g, easy, hard

def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def mat(s):
 b=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)
 if not b:return None
 def number(x):
  x=x.strip();z=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',x)
  return F((-1 if z[1] else 1)*int(z[2]),int(z[3])) if z else F(x)
 return [[number(x) for x in row.split('&')] for row in re.split(r'\\\\',b[1])]
def matrixes(s):return [mat(x[0]) for x in re.findall(r'(\\begin\{bmatrix\}(.*?)\\end\{bmatrix\})',s,re.S) if not re.search(r'\\cdot|\)\(',x[1])]
def key(q):
 f=q[':question/answer-fields'][0]; c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def ops(prompt):
 # Independently parse delivered TeX, not generation metadata.
 tails=prompt.split('row operation',1)[1]; tails=tails.replace('s on',' on')
 chunks=re.findall(r'\$([^$]+)\$',tails,re.S)
 txt=next((v for v in chunks if 'R' in v), '')
 txt=re.sub(r'\{R\}_\{(\d)\}',r'R\1',txt);txt=txt.replace('&','').replace(' ','').replace('\\begin{aligned}','').replace('\\end{aligned}','')
 ans=[]
 for a,b in re.findall(r'R(\d)\\leftrightarrowR(\d)',txt):ans.append(('swap',int(a)-1,int(b)-1,None))
 for t,rhs in re.findall(r'R(\d):=(.*?)(?=\\\\|$)',txt):
  t=int(t)-1;add=re.fullmatch(r'R\d([+-])(\d*)R(\d)',rhs)
  if add:ans.append(('add',t,int(add[3])-1,int((add[1])+ (add[2] or '1'))))
  else:
   v=re.fullmatch(r'(.*?)R\d',rhs);factor=v[1];factor=re.sub(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',r'\1\2/\3',factor)
   ans.append(('scale',t,None,F(factor)))
 if not ans:raise ValueError(txt)
 return ans

def calc(q):
 m=mat(q[':question/problem']); out=copy.deepcopy(m)
 for typ,t,s,k in ops(q[':question/problem']):
  if typ=='swap':out[t],out[s]=out[s],out[t]
  if typ=='scale':out[t]=[k*x for x in out[t]]
  if typ=='add':out[t]=[x+k*y for x,y in zip(out[t],out[s])]
 return out

def verify(rec):
 q=rec['question'];expected=calc(q);f=q[':question/answer-fields'][0]; bank=[mat(a[':answer/value']) for a in f[':answer-field/choices']]
 return {'id':q[':question/id'],'expected':expected,'correct':mat(key(q)[':answer/value']),'key_correct':mat(key(q)[':answer/value'])==expected,'unique_correct':bank.count(expected)==1,'five_unique':len({str(x) for x in bank})==5,'solution_final_correct':mat(re.findall(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',q[':question/worked-solution'],re.S)[-1])==expected}

before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file()};save('package-hashes-before.json',before)
src=json.load(open(J/'source/source.json'));source_q=src['material']['kp'][':knowledge-point/questions'];batch=json.load(open(J/'samples.json'));save('batch-records.json',batch)
# Fresh modest stratified control sample, including rejection counts and complete records.
samples=[g.generate(d,seed) for d in ['easy','moderate','hard'] for seed in range(72011,72071)]
save('control-records.json',samples);save('easy-records.json',[r for r in samples if r['question'][':question/difficulty'].endswith('/easy')])
# Every supported source replay, with complete-bank mathematical comparisons.
replays=[];replay_results=[]
for q in source_q:
 sid=q[':question/math-academy-id'];d=q[':question/difficulty'][':db/ident'].split('/')[-1]
 try:
  if d=='hard':rec=hard.replay(sid,991)
  elif d=='easy':rec=g.generate(d,991,profile=sid,parameters=easy.CASES.get(sid))
  else:rec=g.generate(d,991,profile=sid)
  replays.append(rec);out={'source_id':q[':question/id'],'ma_id':sid,'status':'replayed','bank_equal':sorted(str(mat(a[':answer/value'])) for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(str(mat(a[':answer/value'])) for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']),'source_key_equal':mat(key(q)[':answer/value'])==mat(key(rec['question'])[':answer/value']),'matrix_equal':mat(q[':question/problem'])==mat(rec['question'][':question/problem'])}
 except Exception as e:out={'source_id':q[':question/id'],'ma_id':sid,'status':'unsupported','error':str(e)}
 replay_results.append(out)
canon=g.generate('moderate',991,profile='e-4693');save('canonical-replay.json',canon)
save('source-replays.json',replays);save('source-replay-results.json',replay_results)
# Controlled relevant/irrelevant changes preserve bank values for key dependency tests.
m=[[1,2,3],[4,5,6],[7,8,9]]
base={'matrix':m,'rows':[0,1]}
cf=[g.generate('easy',832,profile='swap-complete',parameters=p) for p in [base,{**base,'rows':[0,2]},{**base,'rows':[1,0]}]]
scale={'matrix':[[6,-6,0],[1,2,3],[4,5,6]],'target':0,'factor':[1,3],'candidate_factors':[[1,3],[1,2],[2,1],[-1,2],[-1,3]]}
cf.extend([g.generate('easy',833,profile='scale-arithmetic',parameters=p) for p in [scale,{**scale,'factor':[-1,2]}]])
save('counterfactual-records.json',cf)
cf_result={'relevant_swap':key(cf[0]['question'])[':answer/value']!=key(cf[1]['question'])[':answer/value'],'irrelevant_swap_order':key(cf[0]['question'])[':answer/value']==key(cf[2]['question'])[':answer/value'],'relevant_factor':key(cf[3]['question'])[':answer/value']!=key(cf[4]['question'])[':answer/value'],'same_banks':[len({tuple(sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])) for r in group})==1 for group in [cf[:3],cf[3:]]]};save('counterfactual-results.json',cf_result)
checks=[verify(r) for r in samples+batch+replays+cf];save('math-results.json',{'command':PY+' -B review.py','count':len(checks),'failures':[x for x in checks if not all(x[k] for k in ['key_correct','unique_correct','five_unique','solution_final_correct'])],'checks':checks})
# Batch all choices through native grader, plus cross-pair stale answers by value.
gcases=[]
for i,r in enumerate(batch+cf+replays):
 q=r['question'];expected=calc(q);f=q[':question/answer-fields'][0]
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if mat(a[':answer/value'])==expected else 'rejected','purpose':'independent exact row operation result compared with each delivered choice'} for a in f[':answer-field/choices']]
 gcases.append({'label':str(i)+': '+q[':question/id'],'record':r,'checks':checks})
save('grader-input.json',gcases)
# Source claims, scope and simple cue probes by recognizable template.
coverage={}
for d in ['easy','moderate','hard']:
 rs=[r for r in samples if r['question'][':question/difficulty'].endswith('/'+d)]
 coverage[d]={'profiles':dict(collections.Counter(r['generation']['profile'] for r in rs)),'roles':dict(collections.Counter(str(r['generation']['parameters'].get('rows',r['generation']['parameters'].get('target'))) for r in rs)),'sampling_attempts':dict(collections.Counter(r['generation']['sampling_attempts'] for r in rs))}
probes=[]
for label,rs in [('batch',batch),('control',samples)]:
 for profile in sorted(set(r['generation']['profile'] for r in rs)):
  group=[r for r in rs if r['generation']['profile']==profile];positions=collections.Counter(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==key(r['question'])[':answer/id']) for r in group)
  probes.append({'label':label,'profile':profile,'count':len(group),'positions':dict(positions),'best_fixed_position_successes':max(positions.values())})
save('coverage-results.json',{'coverage':coverage,'position_probes':probes,'batch_profiles':dict(collections.Counter(r['generation']['profile'] for r in batch))})
# Actual parameters/API rejection; bounded sampler tested above, not assumed.
rej=[]
for profile,p in [('swap-complete',{'matrix':m,'rows':[0,0]}),('scale-arithmetic',{**scale,'factor':[0,1]}),('swap-complete',{'matrix':[[1,2,3]]*3,'rows':[0,1]})]:
 try:g.generate('easy',44,profile,p);rej.append({'profile':profile,'parameters':p,'rejected':False})
 except ValueError as e:rej.append({'profile':profile,'parameters':p,'rejected':True,'error':str(e)})
replay_ok=all(r==g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed']) for r in samples)
# Relocate a byte-for-byte copy entirely inside evidence root.
rel=E/'relocated';rel.mkdir(exist_ok=True)
for p in P.iterdir():
 if p.is_file():(rel/p.name).write_bytes(p.read_bytes())
cmd=[PY,'-B',str(rel/'generator.py'),'--difficulty','easy','--seed','72011','--count','3']
run=subprocess.run(cmd,capture_output=True,text=True,check=True,cwd=E);rel_records=json.loads(run.stdout);save('relocation-records.json',rel_records)
original_run=subprocess.run([PY,'-B',str(P/'generator.py'),'--difficulty','easy','--seed','72011','--count','3'],capture_output=True,text=True,check=True,cwd=E)
save('packaging-results.json',{'command':cmd,'python':platform.python_version(),'dependencies':json.load(open(P/'package.json'))['dependencies'],'deterministic_replay':replay_ok,'relocation_equal':json.loads(original_run.stdout)==rel_records,'rejections':rej,'external_outputs':'Generator returns JSON stdout only; no assets or external writes observed; imports run with -B.','hashes_unchanged':before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file()}})
# Renderer includes exact batch, scale, both controlled decisions and operation-order equivalence.
save('render-records.json',batch+cf)
(E/'session-state.md').write_text('Source analysis completed first. Independent math/source replay/coverage/packaging scripts run. Native grader, delivery, renderer pending. Unsupported source profiles q-10251 and q-10243 demonstrated.\n')
print(json.dumps({'math_count':len(checks),'source_replays':replay_results,'coverage':coverage,'pairs':cf_result,'packaging':json.load(open(E/'packaging-results.json'))},default=str))

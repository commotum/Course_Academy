import sys,json,re,pathlib,hashlib,importlib.util,subprocess,shutil,collections,platform
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
JOB=E.parent
W=JOB/'workspace'
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PY=REPO/'.venv/bin/python'
def save(name,x):
 p=E/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def loadg(p):
 spec=importlib.util.spec_from_file_location('reviewed_generator',p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
def read(record):
 q=record.get('question',record);s=q[':question/problem'];m,n=map(int,re.search(r'(\d+)\s*\\times\s*(\d+)',s).groups());k=int(re.search(r'=(\d+)',s).group(1));t='rank' if s.rfind('rank')>s.rfind('nullity') else 'nullity'
 # dim(Null) is only in given side, so final occurrence is rank.
 f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'];cid=correct[':answer/id'] if isinstance(correct,dict) else correct[1]
 vals=[int(a[':answer/value']) for a in f[':answer-field/choices']];c=next(int(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==cid)
 return dict(m=m,n=n,k=k,target=t,c=c,values=vals,correct_id=cid)
def independent(r):
 d=read(r);m,n,k,t,c=(d[x] for x in ('m','n','k','target','c'));q=r['question'];f=q[':question/answer-fields'][0]
 assert c==n-k,(d,'subtraction');rank=k if t=='nullity' else c
 assert 0<=rank<=min(m,n) and 0<=k<=n,(d,'feasibility')
 assert len(d['values'])==len(set(d['values']))==5 and min(d['values'])>=0
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 s=re.sub(r'\s','',q[':question/worked-solution']);assert f'$n={n}.$' in s
 lhs=(r'\text{rank}(A)+'+str(k)) if t=='rank' else (str(k)+r'+\text{nullity}(A)')
 assert lhs+f'&={n}' in s
 assert r'\text{'+t+r'}(A)&='+f'{n}-{k}' in s and f'&={c}.' in s
 assert 'rank-nullitytheorem' in s and r'\text{rank}(A)+\text{nullity}(A)' in s
 return d
def signature(r):
 d=read(r);v=sorted(d['values']);return d['target'],tuple(b-a for a,b in zip(v,v[1:]))
def main():
 manifest=json.loads((W/'package.json').read_text());paths=[W/'package.json']+[W/f for f in manifest['files']]
 save('package-before.json',{str(p.relative_to(W)):sha(p) for p in paths})
 g=loadg(W/manifest['entrypoint']);source=json.loads((JOB/'source/source.json').read_text());qs=source['material']['kp'][':knowledge-point/questions'];source_by={q[':question/math-academy-id']:q for q in qs}
 replay=[];rr=[]
 for q in qs:
  mid=q[':question/math-academy-id'];d=read(q);p={k:d[k] for k in ('m','n','k','target')}
  case={'source_id':q[':question/id'],'ma_id':mid,'parameters':p,'source_choices':d['values'],'expected':d['n']-d['k']}
  try:r=g.generate('easy',seed=61403,template=mid,parameters=p);independent(r);rr.append(r)
  except Exception as exc:case.update(status='failed',error=repr(exc))
  else:
   rq=r['question'];norm=lambda x:re.sub(r'\s','',x)
   case.update(prompt_match=norm(q[':question/problem'])==norm(rq[':question/problem']),solution_match=norm(q[':question/worked-solution'])==norm(rq[':question/worked-solution']),bank_match=sorted(d['values'])==sorted(read(r)['values']),correct_match=d['c']==read(r)['c'])
   case['status']='passed' if all(case[k] for k in ('prompt_match','solution_match','bank_match','correct_match')) else 'failed'
  replay.append(case)
 save('source-replay.json',replay);save('source-replay-records.json',rr)
 fresh=[g.generate('easy',seed=s) for s in range(829001,829221)]
 forced=[g.generate('easy',seed=921103+i,template=g.ORIGINAL[p]['target'],profile=p) for p in g.PROFILES for i in range(4)]
 records=fresh+forced
 save('independent-samples.json',records)
 batch=json.loads((JOB/'samples.json').read_text());save('runner-batch.json',batch)
 for r in records+batch:independent(r)
 boundaries=[]
 for t,p in [('rank','q-139981'),('nullity','q-139981'),('nullity','q-34931'),('rank','q-142480')]:
  for params in [dict(m=2,n=2,k=2,target=t),dict(m=12,n=12,k=0,target=t),dict(m=2,n=12,k=0,target=t),dict(m=12,n=2,k=1,target=t)]:
   rank=params['k'] if t=='nullity' else params['n']-params['k'];feasible=0<=rank<=min(params['m'],params['n'])
   try:r=g.generate('easy',seed=4,template=t,profile=p,parameters=params);independent(r);boundaries.append({'parameters':params,'profile':p,'mathematically_feasible':feasible,'result':'emitted','record':r})
   except ValueError as exc:boundaries.append({'parameters':params,'profile':p,'mathematically_feasible':feasible,'result':'rejected','reason':str(exc)})
 save('boundary-tests.json',boundaries)
 # Exact controlled pairs, plus a role swap with a valid source profile for each target.
 cf=[]
 for t,p in [('rank','q-142480'),('nullity','q-142483')]:
  for label,m,n,k in [('base',8,8,3),('relevant-given',8,8,4),('irrelevant-rows',10,8,3),('relevant-columns',8,9,3)]:
   r=g.generate('easy',seed=123,template=t,profile=p,parameters={'m':m,'n':n,'k':k,'target':t});independent(r);cf.append({'label':t+'/'+label,'record':r})
 for t,p in [('rank','q-142480'),('nullity','q-142483')]:cf.append({'label':'target-swap/'+t,'record':g.generate('easy',seed=123,template=t,profile=p,parameters={'m':8,'n':8,'k':3,'target':t})})
 save('counterfactuals.json',cf);save('counterfactual-records.json',[x['record'] for x in cf])
 # Build a bank-only strategy from one replay per source. Detect conflicting signatures.
 rules={};collisions=[]
 for r in rr:
  sig=signature(r);d=read(r);pos=sorted(d['values']).index(d['c'])
  if sig in rules and rules[sig]!=pos:collisions.append([sig,rules[sig],pos])
  rules[sig]=pos
 assert not collisions
 save('shortcut-rules.json',[{'target':t,'sorted_adjacent_gaps':list(gaps),'choose_sorted_rank_1_based':pos+1} for (t,gaps),pos in rules.items()])
 def probe(rs):
  groups=collections.defaultdict(lambda:[0,0]);bad=[]
  for r in rs:
   sig=signature(r);d=read(r);prediction=sorted(d['values'])[rules[sig]] if sig in rules else None;hit=prediction==d['c'];key=f'{sig[0]}/{sig[1]}'
   groups[key][0]+=hit;groups[key][1]+=1
   if not hit:bad.append(r['question'][':question/id'])
  return {'correct':sum(v[0] for v in groups.values()),'total':len(rs),'baseline':.2,'conditional':{k:{'correct':v[0],'total':v[1]} for k,v in groups.items()},'failures':bad}
 save('shortcut-results-raw.json',{'strategy':'Read target word only; sort five numerical options; match adjacent-gap tuple to shortcut-rules.json; choose its assigned numerical rank. Ignore shape and supplied dimension. UI shuffling cannot change sorted numerical values.','control':probe(records),'runner_batch':probe(batch)})
 # Native grader inputs: entire five-choice banks for source replay, small fresh sample, batch, all paired records.
 chosen=rr+[records[i] for i in [0,1,2,3,4,20,50,90,140,200]]+batch+[x['record'] for x in cf]
 inp=[]
 for i,r in enumerate(chosen):
  d=independent(r);f=r['question'][':question/answer-fields'][0]
  checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if int(a[':answer/value'])==d['n']-d['k'] else 'rejected','purpose':'independent n minus supplied integer; test every authored choice'} for a in f[':answer-field/choices']]
  sig=signature(r);pv=sorted(d['values'])[rules[sig]];pa=next(a for a in f[':answer-field/choices'] if int(a[':answer/value'])==pv)
  checks.append({'field_index':0,'submitted_answer_id':pa[':answer/id'],'expected':'accepted','purpose':'prompt-blind bank-signature action'})
  inp.append({'label':f'case-{i}','record':r,'checks':checks})
 save('grader-input.json',inp)
 # Per-slot realized coverage, including conditional bank restrictions (not pretending all feasible values occur).
 coverage={}
 for p in g.PROFILES:
  rs=[r for r in records if r['generation']['profile']==p];ds=[read(r) for r in rs]
  coverage[p]={'count':len(rs),'target':g.ORIGINAL[p]['target'],'m':sorted(set(d['m'] for d in ds)),'n':sorted(set(d['n'] for d in ds)),'k':sorted(set(d['k'] for d in ds)),'answers':sorted(set(d['c'] for d in ds)),'shapes':dict(collections.Counter('square' if d['m']==d['n'] else 'tall' if d['m']>d['n'] else 'wide' for d in ds))}
 save('math-and-coverage.json',{'checked_records':len(records)+len(batch),'math_failures':[],'coverage':coverage,'supported_profiles':list(g.PROFILES),'current_source_profiles':list(source_by),'missing_profiles':sorted(set(source_by)-set(g.PROFILES)),'random_seed_range':[829001,829220],'forced_seed_range':[921103,921106]})
 # Public rejection API and deterministic replay; no author validators are executed.
 invalid=[{'level':'moderate'},{'level':'hard'},{'level':'easy','field_type':'free'},{'level':'easy','template':'rank','profile':'q-34931'},{'level':'easy','template':'nullity','profile':'q-34931','parameters':{'m':2,'n':8,'k':5,'target':'nullity'}},{'level':'easy','template':'rank','profile':'q-34833','parameters':{'m':8,'n':8,'k':True,'target':'rank'}}]
 rejection=[]
 for kw in invalid:
  try:g.generate(**kw)
  except (ValueError,TypeError) as exc:rejection.append({'input':kw,'rejected':True,'reason':str(exc)})
  else:rejection.append({'input':kw,'rejected':False})
 assert all(x['rejected'] for x in rejection)
 deterministic=all(g.generate('easy',seed=r['generation']['seed'])==r for r in fresh[:10])
 save('rejection-and-replay.json',{'deterministic':deterministic,'invalid_inputs':rejection,'sampler':'Select target, eligible profile, then reject candidate triples for up to 2000 draws; every independent seed emitted. Rejection checks complete bank nonnegativity and matrix feasibility. Profile selection occurs before rejection.'})
 # Relocate full manifest under evidence, invoke public CLI there with no bytecode writes.
 relocation=E/'relocated-package';relocation.mkdir(exist_ok=True)
 for p in paths:
  out=relocation/p.relative_to(W);out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out)
 command=[str(PY),'-B',str(relocation/manifest['entrypoint']),'--difficulty','easy','--seed','829001','--count','5']
 cp=subprocess.run(command,capture_output=True,text=True,cwd=E);(E/'relocation-stdout.json').write_text(cp.stdout);(E/'relocation-stderr.txt').write_text(cp.stderr or '(empty)\n');relocated=json.loads(cp.stdout) if cp.returncode==0 else []
 import sympy
 versions={'python':platform.python_version(),'packages':{'sympy':sympy.__version__}}
 save('packaging-tests.json',{'command':command,'exit_code':cp.returncode,'relocation_matches':relocated==fresh[:5],'runtime_versions':versions,'manifest_dependencies':manifest['dependencies'],'exact_dependencies_match':versions==manifest['dependencies'],'external_output':'JSON stdout only; no assets or plots; relocated copy remains under evidence','hashes_before':'package-before.json'})
 assert versions==manifest['dependencies'] and relocated==fresh[:5]
 save('commands.json',{'review_script':f'{PY} -B {E}/review_generator.py','delivery':f'{PY} -B {REPO}/generate/pipeline/check_delivery.py --input INPUT --source {JOB}/source/source.json --inventory {JOB}/source/inventory.json --difficulty easy --output OUTPUT --asset-root {E} --math-root /media/jake/SSD/EDB/math','grader':f'{REPO}/generate/runs/current/check-engine {E}/grader-input.json {E}/grader-report.json'})
 (E/'session-state.md').write_text('Source analysis and generator tests complete. Source replay fails 3 missing current profiles; bank-signature strategy is perfect on fresh controls and runner batch. Math, counterfactual records, packaging and native grader inputs saved. Next: shared delivery, native grader, actual UI rendering, inventory/learner selection and report.\n')
 print(json.dumps({'source_replay':collections.Counter(x['status'] for x in replay),'missing_profiles':sorted(set(source_by)-set(g.PROFILES)),'math_checked':len(records)+len(batch),'shortcut_control':probe(records),'shortcut_batch':probe(batch),'packaging':'passed'}))
if __name__=='__main__':main()

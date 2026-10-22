# Reused read/parser/math helpers from previous independent review; new test driver below.
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
 g=loadg(W/'17592186184219.py'); source=json.loads((JOB/'source/source.json').read_text()); qs=source['material']['kp'][':knowledge-point/questions']
 norm=lambda s:re.sub(r'\s','',s)
 replay=[];rr=[]
 for q in qs:
  d=read(q);p={k:d[k] for k in ('m','n','k','target')};mid=q[':question/math-academy-id']
  r=g.generate('easy',seed=67519,template=mid,parameters=p);independent(r);rr.append(r)
  row={'source_id':q[':question/id'],'profile':mid,'parameters':p,'prompt':norm(q[':question/problem'])==norm(r['question'][':question/problem']),'solution':norm(q[':question/worked-solution'])==norm(r['question'][':question/worked-solution']),'bank':sorted(d['values'])==sorted(read(r)['values']),'correct':d['c']==read(r)['c']}
  assert all(row[k] for k in ('prompt','solution','bank','correct')); replay.append(row)
 save('source-replay.json',replay);save('source-replay-records.json',rr)
 canonical=g.generate('easy',seed=67519,template='nullity',profile='q-34931',parameters=dict(m=8,n=6,k=5,target='nullity'));independent(canonical)
 save('canonical-example.json',{'source_id':'9615d8af-b005-5449-be4b-a7487375c98f','record':canonical,'result':'8 by 6, rank 5, nullity 1; same theorem/substitution/subtraction stages. No canonical bank exists; target-question wording differs, documented source gap.'})
 fresh=[g.generate('easy',seed=s) for s in range(1073901,1074001)]
 # Same complete bank/shape across all five answer roles, every profile.
 witness=[];cf=[];coverage={}
 for i,mid in enumerate(g.PROFILES):
  t=g.ORIGINAL[mid]['target'];rs=[g.generate('easy',seed=78013+i,template=t,profile=mid,bank_role=role) for role in range(5)]
  ds=[independent(r) for r in rs]
  assert len({(d['m'],d['n'],tuple(sorted(d['values']))) for d in ds})==1
  assert {d['c'] for d in ds}==set(ds[0]['values'])
  # Every candidate feasible: no answer obtainable merely by ruling out impossible dimensions.
  for d in ds:
   assert all(0 <= (v if t=='rank' else d['n']-v)<=min(d['m'],d['n']) for v in d['values'])
  witness+=rs
  coverage[mid]={'correct_sorted_roles':[sorted(d['values']).index(d['c']) for d in ds],'m':ds[0]['m'],'n':ds[0]['n'],'bank':sorted(ds[0]['values']),'given_values':[d['k'] for d in ds]}
  cf += [{'label':mid+'/role-'+str(role),'record':r} for role,r in enumerate(rs)]
 for t,p in [('rank','q-141220'),('nullity','q-34931')]:
  for label,m,n,k in [('base',10,9,3),('relevant-given',10,9,4),('irrelevant-rows',12,9,3),('relevant-columns',10,10,3)]:
   r=g.generate('easy',seed=29017,template=t,profile=p,parameters=dict(m=m,n=n,k=k,target=t));independent(r);cf.append({'label':t+'/'+label,'record':r})
 # Same given and dimensions with swapped requested and supplied roles.
 for t,p in [('rank','q-141220'),('nullity','q-34931')]:
  cf.append({'label':'target-swap/'+t,'record':g.generate('easy',seed=29017,template=t,profile=p,parameters=dict(m=10,n=9,k=3,target=t))})
 prior=[g.generate('easy',seed=s,template='rank',profile='q-141220') for s in range(829001,829017)]
 seed829013=g.generate('easy',seed=829013)
 save('prior-counterexamples.json',{'seed_829013':seed829013,'consecutive_rank_records':prior,'second_largest_hits':sum(read(r)['c']==sorted(read(r)['values'])[-2] for r in prior),'total':len(prior)})
 batch=json.loads((JOB/'samples.json').read_text());save('runner-batch.json',batch)
 records=fresh+witness
 save('independent-samples.json',records);save('counterfactuals.json',cf);save('counterfactual-records.json',[x['record'] for x in cf]);save('coverage.json',coverage)
 for r in records+batch+prior+[seed829013]:independent(r)
 save('math-and-coverage.json',{'checked_records':len(records+batch+prior+[seed829013]+[x['record'] for x in cf]+rr+[canonical]),'fresh_seeds':[1073901,1074000],'witness_seeds':[78013,78026],'all_profiles':list(coverage),'failures':[],'operations':'Parsed visible prompts, independently checked feasibility, exact subtraction, 5 distinct nonnegative choices, correct UUID, theorem, substituted values and subtraction/result in solution. Generator metadata was not the oracle.','coverage':coverage})
 boundaries=[]
 for t,mid in [('rank','q-141220'),('nullity','q-34931')]:
  for m,n,k in [(2,2,0),(2,2,2),(12,12,0),(12,12,12),(2,12,12),(12,2,1),(2,12,0)]:
   p=dict(m=m,n=n,k=k,target=t);rank=k if t=='nullity' else n-k;feasible=0<=rank<=min(m,n)
   try:r=g.generate('easy',seed=619,template=t,profile=mid,parameters=p);independent(r);result={'record':r,'emitted':True};assert feasible
   except ValueError as ex:result={'error':str(ex),'emitted':False};assert not feasible
   boundaries.append({'parameters':p,'feasible':feasible,**result})
 save('boundary-tests.json',boundaries)
 bad=[{'level':'moderate'},{'level':'hard'},{'level':'easy','field_type':'free'},{'level':'easy','template':'rank','profile':'q-34931'},{'level':'easy','template':'rank','parameters':dict(m=8,n=8,k=True,target='rank')},{'level':'easy','bank_role':5},{'level':'easy','bank_role':True}]
 reject=[]
 for kw in bad:
  try:g.generate(**kw)
  except (TypeError,ValueError) as ex:reject.append({'input':kw,'rejected':True,'reason':str(ex)})
  else:reject.append({'input':kw,'rejected':False})
 assert all(x['rejected'] for x in reject)
 save('rejection-and-replay.json',{'deterministic':all(g.generate('easy',seed=r['generation']['seed'])==r for r in fresh[:8]),'invalid_inputs':reject,'sampling':'New sampler chooses role uniformly before independent bank translation, then dimensions admitting every bank member. No rejection/resampling loop remains. Boundary invalid explicit inputs reject; 100 independently chosen ordinary seeds all emit.','explicit_parameter_limit':'A bank role forcing negative integer distractors rejects; every profile permits all roles in feasible ordinary construction.'})
 # Original independent bank-signature strategy, unchanged from prior review.
 shutil.copyfile(JOB/'review-0-policy-2-f24f201976da522d/shortcut-rules.json',E/'shortcut-rules.json')
 # Runtime and relocation from only declared delivery files.
 manifest=json.loads((W/'package.json').read_text());dest=E/'relocated-package';dest.mkdir(exist_ok=True)
 for f in ['package.json']+manifest['files']:shutil.copyfile(W/f,dest/f)
 cmd=[str(PY),'-B',str(dest/manifest['entrypoint']),'--difficulty','easy','--seed','1073901','--count','5']
 cp=subprocess.run(cmd,cwd=E,capture_output=True,text=True);(E/'relocation-stdout.json').write_text(cp.stdout);(E/'relocation-stderr.txt').write_text(cp.stderr or '(empty)\n')
 versions={'python':platform.python_version(),'packages':{}}
 assert cp.returncode==0 and json.loads(cp.stdout)==fresh[:5] and manifest['dependencies']==versions
 save('packaging-tests.json',{'command':cmd,'exit_code':cp.returncode,'relocation_matches':True,'runtime_versions':versions,'manifest_dependencies':manifest['dependencies'],'exact_versions_match':True,'declared_imports':'Only Python standard library; external input is adjacent runtime-source.json declared in manifest. No external writes, assets, or database access.','deterministic_replay':True})
 (E/'session-state.md').write_text('Source replay: all 14 complete banks pass. Fresh math, boundary/rejection, relocation pass. 70 controlled witnesses vary every bank role across 14 profiles. Old counterexamples generated. Next: delivery filters, native grading and actual UI.\n')
 print(json.dumps({'source_replay':len(replay),'fresh':len(fresh),'controlled_role_witnesses':len(witness),'math_failures':0,'prior_consecutive_second_largest':sum(read(r)['c']==sorted(read(r)['values'])[-2] for r in prior),'prior_total':len(prior)}))
if __name__=='__main__':main()

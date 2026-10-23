import json,re,sys,importlib.util,collections,hashlib,pathlib,copy,platform,subprocess,shutil
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent; JOB=ROOT.parent; PKG=JOB/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(p,x): (ROOT/p).write_text(json.dumps(x,indent=2,default=str))
def load(p):return json.load(open(p))
def module(p):
 s=importlib.util.spec_from_file_location('review_gen',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module(PKG/'17592186161968.py')
def mats(s):return [[[int(v.strip()) for v in row.split('&')] for row in raw.split(r'\\')] for raw in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)]
def ops(s):
 s=re.sub(r'\s+','',s).replace('{C}','C').replace('{','').replace('}','').replace(':&=',':=')
 out=[]
 for i,j,sign,n,p in re.findall(r'C_(\d):=C_(\d)([+-])(\d*)C_(\d)',s):
  assert i==j
  out.append((int(i)-1,int(p)-1,int(sign+(n or '1'))))
 return out

def apply(A,os):
 B=copy.deepcopy(A)
 for i,p,k in os:
  for r in range(3): B[r][i]+=k*B[r][p]
 return B

def field(rec):return rec['question'][':question/answer-fields'][0]
def choices(rec):return field(rec)[':answer-field/choices']
def correctid(rec):
 k=field(rec)[':answer-field/correct'];return k[1] if isinstance(k,list) else k[':answer/id']
def optionpairs(rec):return [tuple(x[2] for x in ops(c[':answer/value'])) for c in choices(rec)]
def check(rec):
 q=rec['question']; A,B=mats(q[':question/problem']); cs=choices(rec)
 truth=[apply(A,ops(c[':answer/value']))==B and len(ops(c[':answer/value']))==2 for c in cs]
 assert sum(truth)==1 and cs[truth.index(True)][':answer/id']==correctid(rec)
 sm=mats(q[':question/worked-solution']);co=ops(cs[truth.index(True)][':answer/value'])
 assert sm==[A,apply(A,co[:1]),B]
 assert ops(q[':question/worked-solution'])==co+co
 return {'id':q[':question/id'],'correct_index':truth.index(True),'coefficients':optionpairs(rec)[truth.index(True)],'matrix_check':True,'solution_check':True}

def modal(rec):
 pairs=optionpairs(rec);freq=[collections.Counter(t[i] for t in pairs) for i in range(2)]
 modes=[[k for k,v in f.items() if v==max(f.values())] for f in freq]
 indices=[i for i,t in enumerate(pairs) if all(t[j] in modes[j] for j in range(2))]
 unique=len(modes[0])==len(modes[1])==len(indices)==1
 chosen=indices[0] if unique else None
 return {'unique_component_modes':unique,'selected_index':chosen,'correct':chosen is not None and choices(rec)[chosen][':answer/id']==correctid(rec),'pairs':pairs,'frequencies':[dict(x) for x in freq]}

def summarize(records):
 groups={}
 for r in records:
  p=r['generation']['bank_profile'];g=groups.setdefault(p,{'count':0,'mode_attempts':0,'mode_correct':0,'correct_positions':collections.Counter(),'row_pivot':set(),'signs':set()});g['count']+=1
  c=check(r);pr=modal(r);g['mode_attempts']+=pr['unique_component_modes'];g['mode_correct']+=pr['correct'];g['correct_positions'][c['correct_index']]+=1
  pa=r['generation']['parameters'];g['row_pivot'].add((pa['row'],pa['pivot']));g['signs'].add(tuple(1 if k>0 else -1 for k in c['coefficients']))
 for g in groups.values():g['row_pivot']=sorted(g['row_pivot']);g['signs']=sorted(g['signs'])
 return groups

def main():
 manifest=load(PKG/'package.json');save('package-before.json',{p:hashlib.sha256((PKG/p).read_bytes()).hexdigest() for p in ['package.json']+manifest['files']})
 source=load(JOB/'source/source.json')['material']['kp'];replays=[];replayreport=[]
 for q in source[':knowledge-point/questions']:
  A,B=mats(q[':question/problem']);p=next(p for p in range(3) if all(A[r][p]==B[r][p] for r in range(3)));cols=[c for c in range(3) if c!=p];row=next(r for r in range(3) if A[r][p] and all(A[r][c] and B[r][c]==0 for c in cols));ks=[-A[row][c]//A[row][p] if c!=p else 0 for c in range(3)]
  profile=q[':question/math-academy-id'];profile=profile if profile in m.PROFILES else 'q-130609'
  rec=m.generate(seed=761,bank_profile=profile,parameters={'A':A,'row':row,'pivot':p,'ks':ks});check(rec);assert mats(rec['question'][':question/problem'])==[A,B]
  banks=[]
  for f in q[':question/answer-fields']:
   assert sorted(ops(c[':answer/value']) for c in f[':answer-field/choices'])==sorted(ops(c[':answer/value']) for c in choices(rec));banks.append(len(f[':answer-field/choices']))
  replays.append(rec);replayreport.append({'source':q[':question/id'],'profile':profile,'bank_sizes':banks,'matrices_and_complete_banks_match':True,'solution_stages_match':mats(q[':question/worked-solution'])==mats(rec['question'][':question/worked-solution'])})
 canonical=m.generate(seed=762,bank_profile='q-130609',parameters={'A':[[-6,-5,1],[8,3,-4],[9,7,-2]],'row':0,'pivot':2,'ks':[6,5,0]});check(canonical);replays.append(canonical)
 save('source-replays.json',replays);save('source-replay-results.json',{'practice':replayreport,'canonical':check(canonical),'corrections':load(ROOT/'source-analysis.json')['source_corrections'],'missing_profile_note':'q-130614 is a duplicate mathematical bank of q-130609, replayed with that profile.'})
 samples=[m.generate(seed=491003+101*j+i,bank_profile=p) for j,p in enumerate(m.PROFILES) for i in range(24)]
 save('samples.json',samples);save('batch.json',load(JOB/'samples.json'));batch=load(ROOT/'batch.json')
 cfpars=[{'A':[[4,2,-6],[1,3,4],[5,-1,2]],'row':0,'pivot':1,'ks':[-2,0,3]}]
 cfpars.append(copy.deepcopy(cfpars[0]));cfpars[1]['A'][0][0]=-4;cfpars[1]['ks'][0]=2
 cfpars.append(copy.deepcopy(cfpars[0]));cfpars[2]['A'][1][0]=8
 cf=[m.generate(seed=842,bank_profile='q-91189',parameters=p) for p in cfpars]
 for p,ks in [(0,[0,-1,2]),(1,[-1,0,2])]:cf.append(m.generate(seed=843,bank_profile='q-130609',parameters={'A':[[2,2,-4],[1,3,4],[5,-1,2]],'row':0,'pivot':p,'ks':ks}))
 save('counterfactuals.json',cf)
 grid=[]
 for row in range(3):
  for pivot in range(3):
   A=[[2,3,5],[7,11,13],[17,19,23]];cols=[c for c in range(3) if c!=pivot];ks=[0]*3
   for c,k in zip(cols,[-2,3]):ks[c]=k;A[row][c]=-k*A[row][pivot]
   grid.append(m.generate(seed=900+3*row+pivot,bank_profile='q-91189',parameters={'A':A,'row':row,'pivot':pivot,'ks':ks}))
 save('boundaries.json',grid)
 allrows=replays+samples+batch+cf+grid
 save('math-results.json',{'checks':[check(r) for r in allrows],'total':len(allrows),'method':'Parse visible matrices and operation choices independently; exact Python integer column updates and all intermediate/final matrices; compare key and final conclusion.'})
 save('variation-results.json',{'independent_samples':summarize(samples),'runner_batch':summarize(batch),'counterfactuals':[{'math':check(r),'modal':modal(r),'parameters':r['generation']['parameters']} for r in cf]})
 grades=[]
 for label,rs in [('sample',samples),('batch',batch),('cf',cf),('source',replays),('boundary',grid)]:
  for i,r in enumerate(rs):
   A,B=mats(r['question'][':question/problem']);grades.append({'label':f'{label}-{i}','record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if apply(A,ops(c[':answer/value']))==B else 'rejected','purpose':'Independent exact matrix transformation for each radio option'} for c in choices(r)]})
 save('grader-input.json',grades)
 # Counterfactual relevant change flips first operation; old pair remains an explicitly wrong distractor.
 old=ops(next(c[':answer/value'] for c in choices(cf[0]) if c[':answer/id']==correctid(cf[0])))
 assert old in [ops(c[':answer/value']) for c in choices(cf[1]) if c[':answer/id']!=correctid(cf[1])]
 assert optionpairs(cf[0])==optionpairs(cf[2])
 assert cf[0]['question'][':question/problem']!=cf[2]['question'][':question/problem']
 # Explicit invalid construction and rejection boundaries.
 invalid=[]
 for label,kwargs in [('moderate',{'difficulty':'moderate'}),('hard',{'difficulty':'hard'}),('zero pivot',{'bank_profile':'q-91189','parameters':dict(cfpars[0],A=[[4,0,-6],[1,3,4],[5,-1,2]])}),('collision bank',{'bank_profile':'q-130609','parameters':{'A':[[2,2,2],[1,3,4],[5,-1,2]],'row':0,'pivot':1,'ks':[-1,0,-1]}})]:
  try:m.generate(**kwargs);invalid.append({'case':label,'rejected':False})
  except Exception as e:invalid.append({'case':label,'rejected':True,'exception':type(e).__name__})
 assert all(x['rejected'] for x in invalid)
 assert m.generate(seed=491003,bank_profile=m.PROFILES[0])==samples[0]
 relocation=ROOT/'relocated';shutil.copytree(PKG,relocation,dirs_exist_ok=True)
 run=subprocess.run([sys.executable,str(relocation/'17592186161968.py'),'--count','5','--seed','69181'],capture_output=True,text=True,cwd=ROOT,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'});assert run.returncode==0
 relocated=json.loads(run.stdout);assert relocated==m.batch('easy',5,69181);save('relocated-records.json',relocated)
 import sympy
 save('packaging-results.json',{'manifest_dependencies':manifest['dependencies'],'installed':{'python':platform.python_version(),'packages':{'sympy':sympy.__version__}},'relocation_identical':True,'deterministic_replay':True,'invalid_inputs':invalid,'external_outputs':'None; CLI JSON stdout; package contains all required source data. Imports tested with declared interpreter.','history':'No repair-history.json, repair-preflight.json or repair-regressions.json exists.'})
 inv=load(JOB/'source/inventory.json');save('inventory-review.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'generated_count':sum(any('generation' in k or 'generator' in k for k in q) for q in inv['questions']),'source_ids':[q[':question/id'] for q in inv['questions']],'conclusion':'All ten captured questions are original source questions; no generated historical question is in this captured inventory. Do not reclassify original sources as generated.'});save('affected-inventory.json',{'affected_questions':[]})
 save('render-input.json',batch+cf+[samples[24*j] for j in range(5,9)])
 (ROOT/'session-state.md').write_text('Source reconstruction, complete source-bank replay, independent exact math, 216 seeded samples, 5 batch records, 5 controlled counterfactuals, nine row/pivot boundaries, dependency and relocation checks complete. Modal-component shortcut identified; native grader, delivery and UI rendering pending. All scripts/outputs inside evidence root.\n')
 print(json.dumps({'records_checked':len(allrows),'profiles':len(m.PROFILES),'batch':summarize(batch),'modal_by_profile':{p:(v['mode_correct'],v['mode_attempts'],v['count']) for p,v in summarize(samples).items()}},indent=2))
if __name__=='__main__':main()

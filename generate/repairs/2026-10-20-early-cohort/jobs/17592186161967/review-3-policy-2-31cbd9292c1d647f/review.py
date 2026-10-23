import sys,json,pathlib,importlib.util,collections,copy,platform,hashlib,shutil,re
sys.dont_write_bytecode=True
from helpers import mats,ops,apply,check
ROOT=pathlib.Path(__file__).resolve().parent;JOB=ROOT.parent;PKG=JOB/'workspace'
s=importlib.util.spec_from_file_location('subject',PKG/'17592186161967.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(n,x):(ROOT/n).write_text(json.dumps(x,indent=2,default=int)+'\n')
def bank(r):return [tuple(o[2] for o in ops(a[':answer/value'])) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
def analyze(r):
 bb=bank(r);ci=check(r);modal=[collections.Counter(abs(z[i]) for z in bb).most_common(1)[0][0] for i in [0,1]]
 extra=next(z for z in bb if list(map(abs,z))!=modal)
 shape='unit-first' if abs(extra[0])!=modal[0] and abs(extra[1])==modal[1] else 'unit-second' if abs(extra[0])==modal[0] and abs(extra[1])!=modal[1] else 'swap'
 # Guess first coefficient from the extra choice; compute only second using A.
 first=- (1 if extra[0]>0 else -1)*modal[0]
 A,B=mats(r['question'][':question/problem']);p=next(i for i in range(3) if A[i]==B[i]);tt=[i for i in range(3) if i!=p];c=next(c for c in range(3) if A[p][c] and all(B[t][c]==0 for t in tt));second=-A[tt[1]][c]//A[p][c]
 guessed=bb.index((first,second)); return {'id':r['question'][':question/id'],'profile':r['generation']['bank_profile'],'seed':r['generation']['seed'],'shape':shape,'bank':bb,'extra':extra,'correct_pair':bb[ci],'guess_pair':bb[guessed],'success':guessed==ci,'guess_id':r['question'][':question/answer-fields'][0][':answer-field/choices'][guessed][':answer/id'],'correct_index':ci}
def metrics(rr):
 aa=[analyze(r) for r in rr];groups={}
 for group in ['all','unit-first','unit-second','swap',*g.PROFILES]:
  ss=[z for z in aa if group=='all' or z['shape']==group or z['profile']==group]
  if ss:groups[group]={'correct':sum(z['success'] for z in ss),'total':len(ss)}
 return {'groups':groups,'details':aa,'pivots':dict(collections.Counter(r['generation']['parameters']['pivot'] for r in rr)),'columns':dict(collections.Counter(r['generation']['parameters']['column'] for r in rr)),'signs':dict(collections.Counter(str(tuple(k>0 for k in r['generation']['parameters']['ks'] if k)) for r in rr)),'positions':dict(collections.Counter(check(r)+1 for r in rr))}
src=json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']
replays=[];results=[]
for q in src:
 A,B=mats(q[':question/problem']);p=next(i for i in range(3) if A[i]==B[i]);c=int(re.search(r'(?:\{a\}|a)_\{\d(\d)\}',q[':question/worked-solution']).group(1))-1;ks=[0 if i==p else -A[i][c]//A[p][c] for i in range(3)]
 r=g.generate(seed=94739,bank_profile=q[':question/math-academy-id'],parameters={'A':A,'pivot':p,'column':c,'ks':ks});check(r)
 for f in q[':question/answer-fields']:
  assert sorted(ops(z[':answer/value']) for z in f[':answer-field/choices'])==sorted(ops(z[':answer/value']) for z in r['question'][':question/answer-fields'][0][':answer-field/choices'])
  if ':answer-field/correct' in f:assert apply(A,ops(f[':answer-field/correct'][':answer/value']))==B
 assert mats(r['question'][':question/problem'])==[A,B]
 replays.append(r);results.append({'source_id':q[':question/id'],'all_banks_match':True,'key_valid':True,'solution_arithmetic':True})
save('source-replays.json',replays);save('source-replay-results.json',results)
fresh=[g.generate(seed=73691+i,bank_profile=p) for p in g.PROFILES for i in range(4)]
batch=json.load(open(JOB/'samples.json'));save('fresh-samples.json',fresh);save('batch.json',batch)
base={'A':[[1,2,3],[2,5,4],[-3,7,8]],'pivot':0,'column':0,'ks':[0,-2,3]}
rel=copy.deepcopy(base);rel['A'][1][0]=-2;rel['ks'][1]=2
irr=copy.deepcopy(base);irr['A'][1][1]=6
# Fixed A permits distinct pivot and cleared-column targets.
A=[[1,1,3],[2,1,5],[4,3,7]]
params=[base,rel,irr]+[{'A':A,'pivot':p,'column':c,'ks':[0 if r==p else -A[r][c]//A[p][c] for r in range(3)]} for p,c in [(0,0),(0,1),(1,1)]]
pairs=[g.generate(seed=472,bank_profile='q-42531',parameters=x) for x in params]
assert bank(pairs[0])==bank(pairs[1])==bank(pairs[2]);assert check(pairs[0])!=check(pairs[1]);assert check(pairs[0])==check(pairs[2])
save('counterfactual-records.json',pairs)
boundaries=[]
for p in range(3):
 for c in range(3):
  A=[[2,4,7],[3,5,8],[1,6,9]];A[p][c]=-3;tt=[r for r in range(3) if r!=p];ks=[0,0,0];ks[tt[0]]=4;ks[tt[1]]=-4
  for r in tt:A[r][c]=-ks[r]*A[p][c]
  boundaries.append(g.generate(seed=79213,bank_profile='q-42531',parameters={'A':A,'pivot':p,'column':c,'ks':ks}))
canonical=g.generate(seed=94739,bank_profile='q-130444',parameters={'A':[[1,4,-7],[2,2,-8],[-3,-2,1]],'pivot':0,'column':0,'ks':[0,-2,3]})
assert mats(canonical['question'][':question/problem'])[1]==[[1,4,-7],[0,-6,6],[0,10,-20]]
boundaries.append(canonical);save('boundary-records.json',boundaries)
# One quartet per profile: fixed seed and bank, changed signs of the two cancellation entries.
quartets=[]
for p in g.PROFILES:
 rr=[]
 for a,b in [(-2,-3),(-2,3),(2,-3),(2,3)]:
  pp=copy.deepcopy(base);pp['A'][1][0]=-a;pp['A'][2][0]=-b;pp['ks']=[0,a,b]
  rr.append(g.generate(seed=98641,bank_profile=p,parameters=pp))
 assert len({json.dumps(bank(r)) for r in rr})==1 and len({check(r) for r in rr})==4
 quartets+=rr
save('fixed-bank-records.json',quartets)
grades=[]
for name,rr in [('source',replays),('fresh',fresh),('batch',batch),('counterfactual',pairs),('boundary',boundaries),('fixed-bank',quartets)]:
 for i,r in enumerate(rr):
  ci=check(r);f=r['question'][':question/answer-fields'][0]
  oo=ops(r['question'][':question/worked-solution']);assert oo[:2]==oo[2:]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==ci else 'rejected','purpose':'Independent full-row arithmetic'} for j,a in enumerate(f[':answer-field/choices'])]
  if name in ['batch','fresh','fixed-bank']:
   z=analyze(r);checks.append({'submitted_answer_id':z['guess_id'],'expected':'accepted' if z['success'] else 'rejected','purpose':'Outlier-first-sign shortcut; computes only second operation'})
  grades.append({'label':name+'-'+str(i),'record':r,'checks':checks})
save('grader-input.json',grades);save('math-results.json',{'records':len(grades),'all_banks_unique_and_keyed':True,'all_solution_stages_exact':True,'counterfactual_relevant_changes_key':True,'irrelevant_preserves_key':True,'fixed_bank_four_keys_each_profile':True})
save('shortcut-results.json',{n:metrics(rr) for n,rr in [('fresh',fresh),('batch',batch),('fixed-bank',quartets)]})
# Trace candidate construction, without replacing RNG or sampling decisions.
resampling=[]
for p in g.PROFILES:
 counts=[]
 def trace(frame,event,arg):
  if event=='line' and frame.f_code.co_filename==str(PKG/'17592186161967.py') and frame.f_lineno==74:counts.append(1)
  return trace
 sys.settrace(trace);r=g.generate(seed=73691,bank_profile=p);sys.settrace(None)
 assert r==g.generate(seed=73691,bank_profile=p)
 resampling.append({'profile':p,'seed':73691,'candidate_attempts':len(counts),'record':r})
save('resampling.json',resampling)
reject=[]
for kwargs in [{'difficulty':'hard'},{'difficulty':'moderate'},{'bank_profile':'missing'},{'parameters':dict(base,ks=[0,2,3])},{'parameters':dict(base,pivot=3)},{'parameters':dict(base,A=[[0,2,3],[2,5,4],[-3,7,8]])}]:
 try:g.generate(**kwargs);ok=False;exc=None
 except Exception as e:ok=True;exc=type(e).__name__
 reject.append({'parameters':kwargs,'rejected':ok,'exception':exc})
assert all(x['rejected'] for x in reject)
manifest=json.load(open(PKG/'package.json'));assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}}
for r in fresh+batch:
 m=r['generation'];assert g.generate(seed=m['seed'],bank_profile=m['bank_profile'])['question']==r['question'];assert g.generate(seed=m['seed'],bank_profile=m['bank_profile'],parameters=m['parameters'])['question']==r['question']
reloc=ROOT/'relocated';reloc.mkdir(exist_ok=True)
for f in manifest['files']:
 dest=reloc/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PKG/f,dest)
save('packaging.json',{'dependencies':manifest['dependencies'],'deterministic_and_parameter_replay':True,'rejections':reject,'external_outputs':'Only stdout; no images or external file outputs','relocation_pending':True})
inv=json.load(open(JOB/'source/inventory.json'));assert {q[':question/id'] for q in inv['questions']}=={q[':question/id'] for q in src}
save('inventory-inspection.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'original_source_ids':[q[':question/id'] for q in inv['questions']],'generated_count':0,'finding':'All stored questions are original instructional sources. No generated record is present, eligible or retired; verified absence of eligible generated defects for this captured inventory.'});save('affected-inventory.json',{'affected_questions':[]})
save('render-records.json',[batch[0],batch[2],*pairs])
(ROOT/'session-state.md').write_text('Completed source replay, independent math, controlled variations, fresh seed sample and dependency/rejection checks. Delivery, native grading, rendering and retained checks pending.\n')
print(json.dumps({'math_records':len(grades),'shortcut':{n:metrics(rr)['groups'] for n,rr in [('batch',batch),('fresh',fresh),('fixed-bank',quartets)]}}))

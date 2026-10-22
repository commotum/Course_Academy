"""Boundary, cue, selection and relocation checks for the repaired package."""
from visible_records import *
import hashlib
import os
import shutil
import tempfile
m=json.loads((W/'package.json').read_text())
assert m['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':g.sp.__version__}}
assert (W/'requirements.txt').read_text().strip()=='sympy=='+g.sp.__version__
for f in m['files']:assert not Path(f).is_absolute() and '..' not in Path(f).parts and (W/f).is_file()
args=['--difficulty','easy','--count','5','--seed','1311091129','--format','json']
cmd=[str(PY),str(W/m['entrypoint'])]+args
base=subprocess.run(cmd,capture_output=True,text=True,check=True).stdout
assert base==subprocess.run(cmd,capture_output=True,text=True,check=True).stdout
with tempfile.TemporaryDirectory(prefix='relocation-',dir=E) as tmp:
 root=Path(tmp)
 for f in m['files']:
  (root/f).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/f,root/f)
 asset=root/'output-assets';asset.mkdir()
 env=dict(os.environ,COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(asset),PYTHONDONTWRITEBYTECODE='1')
 result=subprocess.run([str(PY),str(root/m['entrypoint'])]+args,cwd=root,env=env,capture_output=True,text=True,check=True)
 assert result.stdout==base
 for r in json.loads(result.stdout):inspect(r)
save('relocated-records.json',json.loads(base))
# Slot boundaries: each forbidden coordinate of each size, in both orientations.
slots=[]
for profile,target in [('q-126354','A'),('q-68743','A'),('q-42111','A')]:
 r=g.recipe(profile);level=r['level'];labels=sorted(r['matrices']);good=next(x for x in labels if x!=target)
 for criterion in ('upper','lower'):
  n=len(r['matrices'][target]);coords=[(i,j) for i in range(n) for j in range(n) if (i>j if criterion=='upper' else i<j)]
  for i,j in coords:
   mats={}
   for k,label in enumerate(labels):
    size=len(r['matrices'][label]);a=[[0]*size for _ in range(size)]
    for t in range(size):a[t][t]=k-2
    if label!=good:
     x,y=(size-1,0) if criterion=='upper' else (0,size-1)
     if label==target:x,y=i,j
     a[x][y]=-11
    mats[label]=a
   record=g.generate(level,seed=11,profile=profile,parameters={'criterion':criterion,'matrices':mats})
   assert inspect(record)['answer']==(good,)
   slots.append(record)
save('boundary-records.json',slots)
# Unsupported mathematical instances must fail rather than acquire a wrong key.
rejections=[]
p=copy.deepcopy(json.loads((E/'minimal-failing-case.json').read_text())['parameters'])
for a in p['matrices'].values():a[1][0]=1
try:g.generate_easy(profile='q-126354',parameters=p)
except ValueError as e:rejections.append(str(e))
else:raise AssertionError('zero-correct radio bank accepted')
p=copy.deepcopy(p);p['matrices']['A'][0][0]=12
try:g.generate_easy(profile='q-126354',parameters=p)
except ValueError as e:rejections.append(str(e))
else:raise AssertionError('out-of-range entry accepted')
# Actual zero matrix and decimal source, plus changed qualifying zero label.
p={'criterion':'upper','matrices':copy.deepcopy(g.recipe('q-42111')['matrices'])}
p['matrices']['A']=[[0]*4 for _ in range(4)]
p['matrices']['B'][2][0]=4
r=g.generate_moderate(seed=5,profile='q-42111',parameters=p);assert inspect(r)['answer']==('A','C')
save('zero-role-record.json',[r])
# Incidental strategies, conditional on each recognizable easy profile, before/after delivery.
def cue_report(records):
 groups=defaultdict(list)
 for record in records:groups[record['generation']['profile']].append(record)
 out={}
 for profile,rs in groups.items():
  rows=[]
  for record in rs:
   st=inspect(record);f=record['question'][':question/answer-fields'][0]
   matrices={}
   for a in f[':answer-field/choices']:matrices.update(parse(a[':answer/value']))
   labels=sorted(matrices);actual=st['answer'][0]
   features={x:{'trace':sum(a[i][i] for i in range(len(a))),'dimension':len(a),'diagonal_zeros':sum(a[i][i]==0 for i in range(len(a))),'all_zeros':sum(v==0 for row in a for v in row)} for x,a in matrices.items()}
   score={}
   for feature in ['trace','dimension','diagonal_zeros','all_zeros']:
    for extreme,sign in [('minimum',1),('maximum',-1)]:
     predicted=min(labels,key=lambda label:(sign*features[label][feature],label))
     score[extreme+'_'+feature]=predicted==actual
   rows.append((st,score))
  scores={k:sum(row[1][k] for row in rows) for k in rows[0][1]}
  positions=Counter(st['correct_position'] for st,_ in rows)
  assert max(scores.values())<len(rows),(profile,scores)
  assert max(positions.values())<len(rows),(profile,positions)
  out[profile]={'n':len(rows),'predictor_successes':scores,'fixed_position_successes':dict(positions),'random_label_baseline':0.2}
 return out
raw=json.loads((E/'delivery-control-input.json').read_text());accepted=json.loads((E/'delivery-control/accepted.json').read_text())
save('additional-shortcuts.json',{'before_delivery':cue_report(raw),'after_delivery':cue_report(accepted),'tie_break':'alphabetical label; no predictor selects based on forbidden-side entries'})
# Faithful single-band read-only selection: positively weighted easy band, no prior history.
# Native select() sorts/deduplicates entity IDs, then takes digest bytes 8..16 within band.
draws=[];pool=list(range(1,len(accepted)+1))
for seed in range(32):
 bits=int.from_bytes(hashlib.sha256(('course-academy/question-selection/v1/'+str(seed)).encode()).digest()[8:16],'big')>>11
 index=int((bits/(1<<53))*len(pool));record=accepted[pool[index]-1]
 draws.append({'seed':seed,'proxy_entity':pool[index],'profile':record['generation']['profile'],'answer':inspect(record)['answer']})
assert len({tuple(x['answer']) for x in draws})>1
save('selection-results.json',{'draws':draws,'assumptions':'fresh easy pool with positive configured easy weight; proxy entity ordering 1..N; single-band native SHA256 selection rule reproduced read-only','unconfigured':'Native select chooses the lowest eligible entity, so no sequence-wide diversity claim applies to repeated unconfigured selection.','limits':['Actual learner histories, policy weights, and future publication entity IDs were not supplied. The pool retains all easy roles after delivery; no claim of live per-learner balance.']})
save('packaging-results.json',{'dependencies':m['dependencies'],'declared_runtime_files':m['files'],'deterministic':True,'relocation':True,'source_files_hashes':{f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in m['files']},'cli_args':args,'boundary_records':len(slots),'invalid_cases_rejected':rejections,'images':'none; output asset directory remains empty'})
print(json.dumps({'relocation':True,'determinism':True,'boundary_cases':len(slots),'zero_role_counterfactual':True,'cue_probes':'passed before/after delivery','selection_draws':len(draws)}))

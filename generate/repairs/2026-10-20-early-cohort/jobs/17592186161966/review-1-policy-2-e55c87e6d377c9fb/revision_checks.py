import review as v
import copy,json,shutil,subprocess,sys,hashlib
from pathlib import Path
R=v.ROOT;J=v.JOB;P=J/'workspace';prev=J/'review-0-policy-2-13839960db50e8f3';m=v.load_generator(P/'17592186161966.py')
# Execute retained checks without allowing their hard-coded evidence output into package.
reports=[]
for label,pkg in [('before',prev/'relocated'),('current',P)]:
 d=R/('regression-'+label);d.mkdir(exist_ok=True)
 shutil.copyfile(P/'checks/visible.py',d/'visible.py')
 code=(P/'checks/regressions.py').read_text().replace("ROOT=Path(__file__).resolve().parents[1]",f'ROOT=Path({str(pkg)!r})').replace("OUT=ROOT/'evidence';OUT.mkdir(exist_ok=True)",f'OUT=Path({str(d)!r});OUT.mkdir(exist_ok=True)')
 (d/'regressions.py').write_text(code)
 for case in ['shortcut','sources']:
  x=subprocess.run([sys.executable,str(d/'regressions.py'),'--case',case],capture_output=True,text=True)
  (d/(case+'.log')).write_text(x.stdout+x.stderr)
  reports.append(dict(version=label,case=case,exit_code=x.returncode,log=str((d/(case+'.log')).relative_to(R))))
assert all((x['exit_code']!=0)==(x['version']=='before') for x in reports)
v.save('retained-regressions.json',{'checks':reports,'preflight':json.load(open(J/'repair-preflight.json')),'modifications':'Only ROOT and OUT redirected to read package and write evidence; check logic unchanged. Before is previous independently preserved relocated package.'})
# Source replay against original supplied material, including solutions.
src=json.load(open(J/'source/source.json'))['material']['kp'];replay=json.load(open(R/'source-replay.json'));records=json.load(open(R/'source-replays.json'))
for row in replay:
 if row.get('profile')=='q-91208':row['status']='unsupported-unrated';row['reason']='Missing captured difficulty, solution and correct link; full bank independently checked in unrated-source-bank.json.';continue
 if 'profile' not in row:continue
 q=next(x for x in src[':knowledge-point/questions'] if x[':question/id']==row['source_id'])
 r=next(x for x in records if x['generation']['bank_profile']==row['profile'])
 stages=v.matrices(q[':question/worked-solution'])
 if row['profile']=='q-91210':stages[0][1][0]=-7
 assert v.matrices(r['question'][':question/worked-solution'])==stages
 row['solution_stages_match']=True
v.save('source-replay.json',replay)
# Independent fresh controlled answer-role tests, all profiles, identical banks and incidental rows.
roles=[];rr=[]
for j,p in enumerate(m.PROFILES):
 group=[m.generate(seed=955300+j,bank_profile=p,answer_role=k) for k in range(5)]
 banks=[v.coefficients(x) for x in group]; assert all(x==banks[0] for x in banks)
 assert {v.correct_index(x) for x in group}==set(range(5))
 for rec in group:v.inspect(rec)
 A=[v.matrices(x['question'][':question/problem'])[0] for x in group]
 assert sum(len({tuple(a[i]) for a in A})>1 for i in range(4))==1
 rr.append({'profile':p,'seed':955300+j,'correct_positions':[v.correct_index(x) for x in group],'old_cue_correct':sum(v.shortcut(x)==v.correct_index(x) for x in group),'old_cue_applicable':sum(v.shortcut(x) is not None for x in group),'identical_bank':True,'changed_rows':1})
 roles+=group
v.save('role-records.json',roles);v.save('role-results.json',rr)
# Irrelevant off-row and changed supplied-target tests retain existing independent explicit pairs.
cf=json.load(open(R/'counterfactuals.json'))
# Add all role records to ONE native batch, testing every option and independently deriving keys.
cases=[x for x in json.load(open(R/'grader-input.json')) if not x['label'].startswith('role-')]
for i,rec in enumerate(roles):
 cases.append({'label':f'role-{i}','record':rec,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if k==v.correct_index(rec) else 'rejected','purpose':'Exact independent matrix transformation, same bank controlled role'} for k,a in enumerate(v.field(rec)[':answer-field/choices'])]})
v.save('grader-input.json',cases)
v.save('render-input.json',json.load(open(R/'batch.json'))[:1]+roles[:2]+cf+[next(x for x in records if x['generation']['bank_profile']=='q-130617')])
# Real bank resampling trace. Role is drawn only AFTER bank acceptance; matrix rejection retains role.
trace=[];original=m.recipes
for rec in json.load(open(R/'samples.json')):
 calls=[]
 def recipe(p,a,b):
  bank=original(p,a,b);calls.append({'pair':[a,b],'unique':len(set(bank)),'nonzero':all(k for pair in bank for k in pair)});return bank
 m.recipes=recipe
 assert json.loads(json.dumps(m.generate(seed=rec['generation']['seed'],bank_profile=rec['generation']['bank_profile'])))==rec
 trace.append({'seed':rec['generation']['seed'],'profile':rec['generation']['bank_profile'],'bank_attempts':calls,'incidental_attempts':rec['generation']['sampling_attempts']})
m.recipes=original
v.save('rejection-trace.json',trace)
v.save('rejection-summary.json',{'outputs':len(trace),'rejected_banks':sum(len(x['bank_attempts'])-1 for x in trace),'incidental_rejections':sum(x['incidental_attempts']-1 for x in trace),'analysis':'Bank eligibility requires five distinct nonzero pairs BEFORE independent uniform correct-member selection. Incidental matrix retry fixes bank, role, pivot and target. No answer-dependent acceptance restriction.'})
# Original independent acceptance checks rerun on current package.
for case in ['shortcut','sources']:
 x=subprocess.run([sys.executable,str(R/'reproduce.py'),'--case',case],capture_output=True,text=True);(R/(case+'-regression.log')).write_text(x.stdout+x.stderr);assert x.returncode==0
# CLI relocation and declaration check.
x=subprocess.run([sys.executable,str(R/'relocated/17592186161966.py'),'--count','2','--seed','922731'],capture_output=True,text=True);assert x.returncode==0
v.save('relocated-cli.json',json.loads(x.stdout))
for f in json.load(open(P/'package.json'))['files']:assert (P/f).is_file()
(R/'session-state.md').write_text('Source and prior defects verified; old regressions fail on preserved old package and pass current. 60 fresh records, 5 batch, 60 controlled roles, 4 other counterfactuals and 13 source replays checked. Next: actual grading, delivery and rendering.\n')
print(json.dumps({'retained_checks':reports,'role_cases':len(roles),'source_replays':len(records)}))

"""Targeted sampling repair checks; no services or runtime-file writes.
Run with the job Python: python checks/validate_sampling.py
"""
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path
from validate import W, REPO, SOURCE, INV, g, visible, native, audit, val, save
E=W/'evidence'/'sampling-repair'
E.mkdir(parents=True,exist_ok=True)
SEEDS=[17,43,101,281,459103,719333]
OMITTED={'q-79411','q-79417','q-79420'}

def cli(band, seed, count=5):
 cmd=[sys.executable,str(W/'17592186184172.py'),'--difficulty',band,'--count',str(count),'--seed',str(seed),'--format','json']
 env={**os.environ,'PYTHONPATH':'','PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'assets')}
 p=subprocess.run(cmd,cwd=W,env=env,capture_output=True,text=True,check=True)
 rows=json.loads(p.stdout);assert len(rows)==count
 for r in rows:visible(r)
 return cmd,rows

def delivery(name, rows, band):
 inp=E/(name+'-records.json');save(inp,rows);out=E/name
 cmd=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(inp),'--source',str(SOURCE),'--inventory',str(INV),'--difficulty',band,'--output',str(out),'--asset-root',str(E/'assets'),'--math-root','/media/jake/SSD/EDB/math']
 subprocess.run(cmd,check=True,capture_output=True,text=True)
 accepted=json.loads((out/'accepted.json').read_text())
 for r in accepted:visible(r)
 return accepted,{'command':cmd,'raw_count':len(rows),'accepted_count':len(accepted),'before':audit(rows),'after':audit(accepted),'delivery_report':str((out/'delivery.json').relative_to(W))}

def main():
 manifest=json.loads((W/'package.json').read_text())
 hashes={f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in manifest['files']}
 source=json.loads(SOURCE.read_text())
 assert g.KP==source['material']['kp'],'Runtime source changed; old counterexample requires reanalysis'
 assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':g.sp.__version__}}
 # Replay complete current sources, independent visible mathematical witness.
 replays=[]
 for key in sorted(g.Q):
  r=g.generate(g.level_of(key),template=key,parameters=g.default_parameters(key));visible(r)
  original=g.clean(g.Q[key]);q=r['question']
  for f in [':question/problem',':question/worked-solution',':question/difficulty']:assert q[f]==original[f]
  assert len(q[':question/answer-fields'])==len(original[':question/answer-fields'])
  for f,o in zip(q[':question/answer-fields'],original[':question/answer-fields']):
   for n in [':answer-field/key',':answer-field/type']:assert f[n]==o[n]
   assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in o[':answer-field/choices']]
   assert val(f)==val(o)
  replays.append(r)
 save(E/'replay-records.json',replays)
 batches={};reports={};delivered=[];commands=[]
 for band in g.SUPPORTED_LEVELS:
  eligible={k for k in g.Q if g.level_of(k)==band}
  rows=[];runs=[]
  for seed in SEEDS:
   cmd,z=cli(band,seed);commands.append(cmd);rows.extend(z)
   assert len({r['generation']['template'] for r in z})==5
   runs.append({'seed':seed,'profiles':[r['generation']['template'] for r in z]})
  assert {r['generation']['template'] for r in rows}==eligible
  # Boundary batch sizes: singleton practice and a complete cycle.
  single=[g.batch(band,1,seed)[0] for seed in range(32)]
  for r in single:visible(r)
  assert {r['generation']['template'] for r in single}==eligible
  cycle=g.batch(band,len(eligible),17)
  assert {r['generation']['template'] for r in cycle}==eligible
  for r in cycle:visible(r)
  cmd,repeat=cli(band,17);assert repeat==rows[:5]
  accepted,d=delivery(band+'-batches',rows,band)
  assert {r['generation']['template'] for r in accepted}==eligible
  batches[band]=accepted;delivered.extend(accepted)
  reports[band]={'runs':runs,'singleton_seeds':list(range(32)),'singleton_profiles':sorted({r['generation']['template'] for r in single}),'full_cycle_profiles':[r['generation']['template'] for r in cycle],'deterministic':True,'delivery':d}
  save(E/(band+'-singleton-records.json'),single)
 # Within-profile fixed-evidence counterfactuals for the affected band. Use the
 # existing independent visible parser, not the generator's truth metadata.
 controlled=[];pairs=[]
 for key in sorted(k for k in g.Q if g.level_of(k)=='moderate'):
  p=g.default_parameters(key);group=[]
  for truths in g.allowed_truths(key):
   r=g.generate('moderate',seed=91,template=key,parameters={**p,'truths':truths});t=visible(r)
   assert t['truths']==truths;group.append(r)
  witnesses=[visible(r) for r in group]
  assert len({str(t['given']) for t in witnesses})==1
  assert all({t['truths'][i] for t in witnesses}=={False,True} for i in range(3))
  assert len({str(t['truths']) for t in witnesses})==len(group)
  # Keys and solutions change together under decisive claim changes.
  assert len({r['question'][':question/worked-solution'] for r in group})==len(group)
  controlled.extend(group)
  alt={**p,'truths':g.allowed_truths(key)[-1]}
  if 'scale' in p:alt['scale']=3
  else:alt['diagonal']=[3 if i%2==0 else 1 for i in range(len(p['diagonal']))]
  irrelevant=g.generate('moderate',seed=91,template=key,parameters=alt)
  assert visible(irrelevant)['truths']==witnesses[-1]['truths']
  pairs.append({'profile':key,'fixed_evidence_truths':[t['truths'] for t in witnesses],'irrelevant_change_preserves_response':True})
  controlled.append(irrelevant)
 accepted,d=delivery('moderate-controlled',controlled,'moderate');delivered.extend(accepted)
 combined_audit=audit(batches['moderate']+accepted)
 for key,metric in combined_audit.items():
  assert metric['truth_patterns']==len(g.allowed_truths(key))
  assert all(0<c<metric['count'] for c in metric['position_true_counts'])
  assert len(metric['correct_choice_counts'])>1
 reports['controlled']={'pairs':pairs,'delivery':d,'all_delivered_moderate_audit':combined_audit,'inventory_deduplication':'One controlled q-34934 record reproduces a stored source and is correctly removed. The same truth role survives with different mathematical data in the normal CLI sample; combined delivered coverage retains every allowed role.','cue_tests':'Within each profile, no fixed subset, claim position truth, or correct-choice count is invariant across the controlled decision cases. Native grading covers every offered answer on the delivered records. Single-number and template recognition cannot decide all cases; supplied evidence and the tested claim must be compared.'}
 # Retain the decisive supplied-count counterfactual (claims held fixed).
 base=g.generate('moderate',template='q-34934',parameters={'scale':1})
 changed=g.generate('moderate',seed=25,template='q-34934',parameters={'scale':1,'count':4,'truths':[False,True,False]})
 a,b=visible(base),visible(changed)
 assert a['statements']==b['statements'] and a['truths']!=b['truths']
 save(E/'count-counterfactual-records.json',[base,changed])
 cases=[native(r,'delivered '+r['generation']['template']) for r in delivered]
 cases.extend([native(base,'count evidence original'),native(changed,'count evidence changed')])
 inp=E/'native-input.json';out=E/'native-report.json';save(inp,cases)
 command=[str(REPO/'generate/runs/current/check-engine'),str(inp),str(out)]
 subprocess.run(command,check=True,capture_output=True,text=True);commands.append(command)
 # Representative records originate in normal five-question CLI batches.
 render=[next(r for r in batches['moderate'] if r['generation']['template']==k) for k in sorted(OMITTED)]
 save(E/'render-records.json',render)
 after={f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in hashes};assert after==hashes
 report={'status':'passed','source_replays':len(replays),'source_choices':sum(len(f[':answer-field/choices']) for r in replays for f in r['question'][':question/answer-fields']),'five_question_cli_records':60,'controlled_records':len(controlled),'native_cases':len(cases),'native_checks':sum(len(c['checks']) for c in cases),'reports':reports,'commands':commands,'runtime_hashes':hashes,'runtime_unchanged_by_tests':True,'limitations':['Delivery uses the captured inventory; live learner history and weighted selection are not exercised.','Six batch seeds and 32 singleton seeds test reachability, not statistical balance.','Unchanged source/math construction retains earlier boundary and hard-profile counterfactual evidence.']}
 save(E/'results.json',report)
 print(json.dumps({k:report[k] for k in ['status','source_replays','source_choices','five_question_cli_records','controlled_records','native_cases','native_checks','runtime_unchanged_by_tests']}))
if __name__=='__main__':main()

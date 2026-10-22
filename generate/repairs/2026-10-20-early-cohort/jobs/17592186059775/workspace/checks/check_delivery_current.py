"""Shared actual delivery filters, followed by independent shortcut/grader probes."""
import sys
sys.dont_write_bytecode=True
import importlib.util
import json
from pathlib import Path
import subprocess
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W/'checks'))
from check_repair import g,probes,v,E,JOB,REPO,save
records=json.loads((E/'test-records.json').read_text())
# Refuse stale evidence: every input must still equal current generation.
for r in records:
 assert r==g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],parameters=r['generation']['parameters'])
reports={};native=[]
for difficulty in ('easy','moderate'):
 subset=[r for r in records if r['question'][':question/difficulty'].endswith('/'+difficulty)]
 save(difficulty+'-records.json',subset)
 out=E/('delivery-'+difficulty)
 cmd=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/(difficulty+'-records.json')),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty',difficulty,'--output',str(out),'--asset-root',str(E/'assets'),'--math-root','/media/jake/SSD/EDB/math']
 subprocess.run(cmd,check=True)
 accepted=json.loads((out/'accepted.json').read_text());raw=probes(subset);after=probes(accepted)
 assert set(raw)==set(after)
 for sid in raw:
  assert set(map(int,after[sid]['correct_numeric_ranks']))==set(range(5)),(sid,'Target lost after filtering')
  assert after[sid]['unique_consistency_selector']==0
 reports[difficulty]={'command':cmd,'before':raw,'after':after,'delivery':json.loads((out/'delivery.json').read_text())}
 # Check actual normalized identities, all candidate decisions in one easy
 # profile and one moderate profile. Raw native checks already cover all rows.
 sid='q-1059' if difficulty=='easy' else 'q-1060'
 for r in accepted:
  if r['generation']['template']==sid and r['generation']['parameters'][1]==1:
   native.append({'label':'delivered '+str(r['generation']['parameters']),'record':r,'checks':v.checks(r)})
save('native-delivered-input.json',native)
subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'native-delivered-input.json'),str(E/'native-delivered-report.json')],check=True)
# Check the actual five-question runner sample passes all delivery stages.
cmd=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'runner-sample.json'),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty','easy','--output',str(E/'delivery-runner'),'--asset-root',str(E/'assets'),'--math-root','/media/jake/SSD/EDB/math']
subprocess.run(cmd,check=True)
runner=json.loads((E/'delivery-runner/delivery.json').read_text());assert runner['accepted_count']==5
save('delivery-variation.json',{'bands':reports,'runner_sample':runner,'native_delivered_responses':sum(len(c['checks']) for c in native),'generator_rejection':'No rejection/resampling in the normal catalog. Finite explicit domains, validated parameter rejection, semantic fingerprint dedup in batch.','learner_selection':'Read question_selection.rs: configured weights select a difficulty then uniformly select fresh candidates in that band; no content rank/position filter. Live learner history and policy weights are unavailable; no live selection claim.'})
print('PASS: all five target ranks survive each profile; runner sample accepts 5/5')

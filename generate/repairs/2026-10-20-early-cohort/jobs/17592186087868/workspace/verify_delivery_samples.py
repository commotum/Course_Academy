#!/usr/bin/env python3
"""Native grade delivered identities; duplicate/source exclusion and five-item CLI."""
import json,subprocess,sys,random,importlib.util
from pathlib import Path
W=Path(__file__).resolve().parent;E=W/'evidence';R=Path('/home/jake/Developer/Course_Academy');J=R/'generate/repairs/2026-10-20-early-cohort/jobs/17592186087868'
def save(path,d):path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('g',W/'17592186087868.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rs=json.load(open(E/'render-records.json'));replays=json.load(open(E/'source-replay.json'));reports={};resampling=[]
for level in ['easy','moderate']:
 # Preserve all six inspected records with a separate filtering receipt.
 render=[r for r in rs if r['question'][':question/difficulty'].endswith('/'+level)]
 normal=[g.generate(level,seed) for seed in range(12)]
 original=next(r for r in replays if r['question'][':question/difficulty'].endswith('/'+level))
 test=normal+render+[normal[0]]
 inp=E/('selection-input-'+level+'.json');out=E/('selection-delivery-'+level);save(inp,test)
 subprocess.run([sys.executable,str(R/'generate/pipeline/check_delivery.py'),'--input',str(inp),'--source',str(J/'source/source.json'),'--inventory',str(J/'source/inventory.json'),'--difficulty',level,'--output',str(out),'--asset-root',str(E/'assets'),'--math-root','/media/jake/SSD/EDB/math'],check=True,stdout=subprocess.DEVNULL)
 accepted=json.load(open(out/'accepted.json'));report=json.load(open(out/'delivery.json'));assert report['duplicate_count']>=1
 assert not any(r['generation']['evidence_only'] for r in accepted)
 for r in render:assert r in accepted
 def bits(r):
  return tuple(next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in r['question'][':question/answer-fields'])
 before=[bits(r) for r in normal];after=[bits(r) for r in accepted]
 assert len(set(after))>1 and all(0<sum(b[i] for b in after)<len(after) for i in range(3))
 reports[level]={'normal_seed_range':[0,11],'input_count':len(test),'duplicate_count':report['duplicate_count'],'accepted_count':len(accepted),'source_inventory_filter_applied':True,'all_inspected_render_records_delivered':True,'normal_subsets_before':sorted({str(b) for b in before}),'subsets_after':sorted({str(b) for b in after}),'correct_counts_after':sorted({sum(b) for b in after})}
 for seed in range(12):
  initial=g.sample_current(level,random.Random(seed))
  try:g.validate_current(level,initial)
  except ValueError as exc:resampling.append({'level':level,'seed':seed,'first_candidate_rejected':str(exc),'returned_valid_parameters':normal[seed]['generation']['parameters']})
runner=json.load(open(E/'delivery-runner-five/accepted.json'));assert len(runner)==5
cases=[]
for i,r in enumerate(rs+runner):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Delivered field-owned checkbox identity'})
 cases.append({'label':'delivered '+str(i),'record':r,'checks':checks})
save(E/'delivered-engine-input.json',cases)
subprocess.run([str(R/'generate/runs/current/check-engine'),str(E/'delivered-engine-input.json'),str(E/'delivered-engine-report.json')],check=True,stdout=subprocess.DEVNULL)
save(E/'delivery-samples.json',{'passed':True,'runner_requested_five_delivered':5,'native_delivered_records':len(cases),'selection_filter_audits':reports,'observed_seeded_rejections':resampling,'scope':'No learner history or live weighted-policy snapshot available. Captured inventory was supplied to the shared filter; no normal sample collided with a source fingerprint. Explicit generated duplicates skipped. Source replay retains its protected Math Academy identity and is not delivery input.'})
print(json.dumps({'passed':True,'delivered_graded':len(cases),'seeded_resampling':len(resampling)}))

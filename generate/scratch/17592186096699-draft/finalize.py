"""Refresh review selection, confirm the registered baseline, then freeze hashes."""
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import json,hashlib,importlib.util
from datetime import datetime,timezone
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
report=json.loads((H/'validation.json').read_text());assert report['status']=='pass';baseline=v.baseline();assert baseline['status']=='unchanged'
data=json.loads((H/'review.json').read_text());normal=data['generated']
md='# Basis-2275 particular-solution draft review\n\nOriginal replay preserves missing attributes and documented source errors. Original raw banks retain all captured bytes at unit scale and wrap complete expression prototypes under changed scale. Repaired and normal values use standard-TeX normalization separately. Decoded format diagnostics remain in source-format-audit.json. All observed banks are evidence-only. Independent inventory is separately labeled.\n\n'
for item in data['originals']:
 md+='## '+item['source_id']+' — '+('unrated' if item['source_id'] in ('q-119078','q-49942') else item['level'])+' original raw replay\n\n'+v.g.markdown(item['raw'])+'\n\n'
 md+='### '+item['level']+' generated observed-pattern variant (scale 2; repaired and ineligible)\n\n'+v.g.markdown(item['variants'][1])+'\n\n'
 r=next(r for r in normal if r['generation']['template']==item['source_id'] and r['generation']['parameters']=={'scale':-2,'target':7})
 md+='### '+item['level']+' generated normal family variant (authored method bank)\n\n'+v.g.markdown(r)+'\n\n'
for level in ('easy','moderate','hard'):
 examples=[];seen=set()
 for r in reversed(normal):
  fp=r['generation']['mathematical_fingerprint']
  if r['question'][':question/difficulty'].endswith('/'+level) and fp not in seen:examples.append(r);seen.add(fp)
  if len(examples)==2:break
 assert len(examples)==2 and len(seen)==2
 for i,r in enumerate(examples):md+='## '+level+' generated default variant '+str(i+1)+'\n\n'+v.g.markdown(r)+'\n\n'
(H/'review.md').write_text(md)
# Confirm fresh public calls reproduce every reviewed source/normal question;
# no expensive mathematical recheck is needed for a selection-only rewrite.
records=[item['raw'] for item in data['originals']]+[item['repaired'] for item in data['originals']]+[r for item in data['originals'] for r in item['variants']]+normal
for record in records:
 m=record['generation'];level=record['question'].get(':question/difficulty',':question.difficulty/easy').split('/')[-1]
 current=v.g.generate(level,seed=m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'],field_type=record['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1])
 assert current['question']==record['question'],'review/public API mismatch'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
producers=[H.with_suffix('.py'),H/'validate.py',H/'build_docs.py',Path(__file__).resolve()]
manifest={'frozen_at':datetime.now(timezone.utc).isoformat(),'producers_stopped':True,'database':'math','basis':2275,'registered_baseline':baseline,'producer_hashes':{str(p):sha(p) for p in producers},'artifact_hashes':{str(p):sha(p) for p in sorted(H.rglob('*')) if p.is_file() and p.name!='frozen-manifest.json'},'shared_math_format_sha256':sha(Path('scripts/question_capture/math_format.py')),'native_engine_sha256':sha(Path('generate/runs/current/check-engine')),'native_engine_source_sha256':sha(Path('generate/runs/current/check-engine.rs')),'counts':report,'public_replay_records_verified':len(records)}
(H/'frozen-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'generator_sha256':manifest['producer_hashes'][str(H.with_suffix('.py'))],'public_replay_records_verified':len(records),'baseline':baseline,'fidelity':report['fidelity'],'normal_math_instances':report['normal_math_instances'],'native':report['native']},indent=2))

#!/usr/bin/env python3
"""Hash freeze the finished private pair and verify the full registered tree."""
import sys
sys.dont_write_bytecode=True
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((HERE/name).read_text())
baseline=read('registered-baseline.json');original=ROOT/'generate/scratch/17592186096621';current={str(p) for p in original.rglob('*') if p.is_file()}|{str(original.with_suffix('.py'))};assert current=={z['path'] for z in baseline},'registered tree file set changed'
for row in baseline:assert sha(Path(row['path']))==row['sha256'],'registered immutable file changed: '+row['path']
validation=read('validation.json');native=read('native-report.json');generator=HERE.with_suffix('.py');gh=sha(generator)
assert validation['generator_sha256']==native['generator_sha256']==gh,'test results are not for the current generator'
assert not validation['failures'];fidelity=read('source-fidelity.json');assert len(fidelity)==15 and sum(z['matched_options'] for z in fidelity)==42
assert len(read('source-cases.json'))==21 and len(read('raw-replays.json'))==21
# Drop stale exploratory native files; retain the final suite's input/report
# files and the one actual gap's observed prefix and corrected continuation.
for path in (HERE/'native').iterdir():
 parts=path.name.split('-');ri,part=map(int,parts[:2]);tail='-'.join(parts[2:]);keep=(0<=ri<35 and part==0 and tail in ['input.json','report.json']) or (ri==21 and ((part==0 and tail in ['prefix.json','gap.json','gap-report.json']) or (part==1 and tail in ['input.json','report.json'])))
 if not keep:path.unlink()
old=HERE/'first-validation.json'
if old.exists():old.unlink()
# Aggregate native outcomes including the observed passing prefix from the
# interrupted small batch. A mismatch stops the native binary immediately.
counts={'accepted':0,'rejected':0,'unresolved':0}
for batch in native['batches']:
 if 'observed_passing_prefix_checks' in batch:
  for check in batch['checks']:counts[check['expected']]+=1
 else:
  for record in batch['records']:
   for check in record['checks']:counts[check['outcome']]+=1
assert sum(counts.values())==native['actual_checks']==191
summary={'generator_sha256':gh,'registered_baseline_files':len(baseline),'registered_unchanged':True,'ma_sources':15,'existing_non_ma_inventory':6,'source_case_records':21,'matched_ma_values':42,'complete_radio_banks':7,'captured_singleton_blanks':7,'missing_field_authored_blank':1,'review_families':16,'review_records':48,'rendered_records':validation['records'],'rendered_stages':validation['rendered_stages'],'formal_derivative_inputs':validation['formal_derivative_inputs'],'boundary_records':validation['boundary_records'],'structural_mutations':len(read('mutation-tests.json')),'native_fixtures':native['fixtures'],'native_checks':native['actual_checks'],'native_outcomes':counts,'native_legitimate_gaps':len(native['documented_engine_gaps']),'native_engine_sha256':native['engine_sha256'],'database_writes':0,'registration_changes':0,'engine_changes':0}
(HERE/'final-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
files=[generator]+[p for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='freeze.json']
manifest={'summary':summary,'files':[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in files]}
(HERE/'freeze.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(summary,indent=2));print('freeze_sha256',sha(HERE/'freeze.json'))

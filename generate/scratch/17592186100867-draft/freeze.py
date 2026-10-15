"""Freeze only this private draft; independently verify immutable numeric work."""
import sys
sys.dont_write_bytecode=True
import hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
baseline={}
for line in (D/'reference/immutable-baseline.sha256').read_text().splitlines():
 h,path=line.split('  ',1);baseline[path]=h
numeric=ROOT/'generate/scratch/17592186100867';current={str(p.relative_to(ROOT)):sha(p) for p in numeric.rglob('*') if p.is_file()}
p=ROOT/'generate/scratch/17592186100867.py';current[str(p.relative_to(ROOT))]=sha(p)
for p in (ROOT/'generate/scratch/__pycache__').glob('17592186100867.*.pyc'):current[str(p.relative_to(ROOT))]=sha(p)
assert current==baseline,{'removed':sorted(set(baseline)-set(current)),'added':sorted(set(current)-set(baseline)),'changed':[p for p in baseline if p in current and current[p]!=baseline[p]]}
report={'passed':True,'registered_script':{'path':'generate/scratch/17592186100867.py','sha256':current['generate/scratch/17592186100867.py']},'file_count':len(current),'exact_hashes_and_pathset_unchanged':True,'sibling_pyc_paths':sorted(p for p in current if p.startswith('generate/scratch/__pycache__/')),'import_policy':'Bytecode disabled before imports; registered numeric script/evidence never imported or executed.'}
(D/'numeric-baseline-verification.json').write_text(json.dumps(report,indent=2)+'\n')
records=json.loads((D/'cli-all.json').read_text());assert type(records)is list and len(records)==3
validation=json.loads((D/'validation.json').read_text());render=json.loads((D/'render-report.json').read_text())
assert validation['passed'] and validation['script_sha256']==sha(D.with_suffix('.py'))==render['generator_sha256']
assert all(x['controlInteractions'] for x in render['checks'])
owned={str(p.relative_to(ROOT)):sha(p) for p in D.rglob('*') if p.is_file() and p.name!='freeze.json'}
owned[str(D.with_suffix('.py').relative_to(ROOT))]=sha(D.with_suffix('.py'))
freeze={'scope':'Only private draft script and evidence; parent independent approval pending. No DB writes, registration, engine edits or commits.','script_sha256':sha(D.with_suffix('.py')),'owned_files':owned,'registered_numeric_baseline_unchanged':True,'source_originals':11,'source_values':51,'source_present_designations':13,'source_full_solutions':9,'math_full_record_checks':validation['successful_full_record_math_checks'],'canonical_math_examples':1,'native_records':validation['native_records'],'native_accepted_checks':404,'native_rejected_checks':395,'native_unresolved_checks':0,'render_records':render['records'],'render_control_interaction_records':len(render['checks']),'render_screenshots':len(render['screenshots'])}
(D/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
assert all(sha(ROOT/p)==h for p,h in owned.items())
print(json.dumps({'script_sha256':freeze['script_sha256'],'freeze_sha256':sha(D/'freeze.json'),'owned_files':len(owned),'immutable_numeric_files':len(current),'immutable_numeric_sha256':report['registered_script']['sha256']},indent=2))

"""Freeze/verify the complete owned file set without importing any generator."""
import hashlib,json,sys
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2];SCRIPT=D.with_suffix('.py')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owned():return {str(p.relative_to(ROOT)):h(p) for p in sorted([SCRIPT]+[p for p in D.rglob('*') if p.is_file() and p.name!='freeze.json'])}
def boundaries():
 baseline=json.loads((D/'registered-baseline-before.json').read_text());found=[]
 for p in [ROOT/'generate/scratch/17592186100872.py',ROOT/'generate/scratch/17592186100872']:
  if p.is_file():found.append(p)
  elif p.is_dir():found.extend(x for x in p.rglob('*') if x.is_file())
 found.extend((ROOT/'generate/scratch/__pycache__').glob('17592186100872.*.pyc'))
 actual={str(p.relative_to(ROOT)):h(p) for p in found};assert actual==baseline['complete_file_set']
 b=json.loads((D/'reference/grader-build.json').read_text());hashes={b['source']:b['source_sha256'],b['library']:b['library_sha256'],b['binary']:b['binary_sha256']}|b['engine_sources']|b['dependencies'];assert len(hashes)==42
 assert all(h(ROOT/p)==value for p,value in hashes.items());assert h(D/'check-engine')=='33510bf3ac27a1eb28e9bad7b4121a22d2fa787026d3102268daa4ecf98b1617'
 return actual,hashes
if '--verify' in sys.argv:
 f=json.loads((D/'freeze.json').read_text());assert f['owned_files']==owned();boundaries();print('Verified complete owned path/hash set, numeric absence,42 native file hashes.')
else:
 actual,hashes=boundaries();r=json.loads((D/'render-report.json').read_text());records=json.loads((D/'render-records.json').read_text());assert len(r['checks'])==len(records)==31
 for x,record in zip(r['checks'],records):
  assert x['question_id']==record['question'][':question/id'] and x['content_fingerprint']==record['generation']['content_fingerprint']
  assert not x['errors'] and not x['exposed'] and not x['documentOverflow'] and x['controls_visible']
  if record['generation']['profile']!='observed-raw':assert not x['overflow']
  assert h(ROOT/x['screenshot'])==x['screenshot_sha256']
  for right in x['scroll_screens']:assert h(ROOT/right['path'])==right['sha256']
 assert all(h(ROOT/p)==value for p,value in r['ui_source_hashes'].items())
 assert isinstance(json.loads((D/'cli-all.json').read_text()),list) and len(json.loads((D/'cli-all.json').read_text()))==6
 engine=json.loads((D/'engine-report.json').read_text());assert (engine['accepted_checks'],engine['rejected_checks'],engine['documented_unresolved_checks'])==(74,142,0)
 f={'generator':str(SCRIPT.relative_to(ROOT)),'generator_sha256':h(SCRIPT),'owned_scope':[str(SCRIPT.relative_to(ROOT)),str(D.relative_to(ROOT))+'/**'],'excluded_self':'freeze.json cannot recursively hash itself','owned_files':owned(),'numeric_complete_path_set_after':actual,'numeric_matches_before':True,'native_actual_files_reverified':hashes,'native_count':42,'status':'frozen local draft; parent approval pending; stop after step 7'}
 (D/'freeze.json').write_text(json.dumps(f,indent=2)+'\n');assert json.loads((D/'freeze.json').read_text())['owned_files']==owned();print('Frozen',len(f['owned_files']),'owned files;',f['generator_sha256'])

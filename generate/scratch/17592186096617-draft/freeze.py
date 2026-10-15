"""Freeze all owned private artifacts after validating immutable baseline."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,runpy
D=Path(__file__).resolve().parent
m=runpy.run_path(str(D/'validate.py'),run_name='freeze-helper')
expected=json.loads((D/'registered-baseline.json').read_text())['files'];assert m['baseline']()==expected
m['verify_native']()
validation=json.loads((D/'validation.json').read_text());render=json.loads((D/'render-report.json').read_text());boundaries=json.loads((D/'boundary-validation.json').read_text());current=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
assert validation['pass'] and validation['generator_sha256']==current
assert render['generator_sha256']==current and render['errors']==render['overflow']==0
assert boundaries['pass'] and boundaries.get('metadata_refresh_generator_sha256',boundaries['generator_sha256'])==current
paths=[D.with_suffix('.py')]+sorted(p for p in D.rglob('*') if p.is_file() and p.name!='freeze.json')
result={'status':'pending root independent approval','generator_sha256':current,'source_sha256':validation['source_sha256'],'source_basis':validation['source_provenance'],'registered_numeric_baseline_files_unchanged':len(expected),'artifacts':{str(p.relative_to(Path.cwd())):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'database_writes':0,'engine_edits':0,'registration':False}
(D/'freeze.json').write_text(json.dumps(result,indent=2)+'\n')
# Recheck hashes and complete pathset after the freeze itself is written.
for path,sha in result['artifacts'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha,path
assert set(result['artifacts'])=={str(p.relative_to(Path.cwd())) for p in [D.with_suffix('.py')]+list(p for p in D.rglob('*') if p.is_file() and p.name!='freeze.json')}
assert m['baseline']()==expected
print(json.dumps({'frozen_files':len(paths),'generator_sha256':current,'baseline_files_unchanged':len(expected),'freeze_sha256':hashlib.sha256((D/'freeze.json').read_bytes()).hexdigest()},indent=2))

"""Verify unchanged registration and freeze all owned implementation/evidence bytes."""
from pathlib import Path
import hashlib,json,datetime
H=Path(__file__).resolve().parent
baseline=json.loads((H/'reference/registered-baseline.json').read_text())
expected={f['path']:f['sha256']for f in baseline['files']}
actual={str(p)for p in Path('generate/scratch/17592186059827').rglob('*')if p.is_file()}|{'generate/scratch/17592186059827.py'}|{str(p)for p in Path('generate/scratch/__pycache__').glob('17592186059827*')if p.is_file()}
assert set(expected)==actual
for path,digest in expected.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
validation=json.loads((H/'validation.json').read_text());browser=json.loads((H/'browser-rendering.json').read_text());readback=json.loads((H/'rendered-readback.json').read_text())
assert validation['passed'] and browser['passed'] and readback['passed']
files=[H.with_suffix('.py')]+sorted(p for p in H.rglob('*')if p.is_file()and p.name!='freeze-manifest.json')
manifest={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owned_script':str(H.with_suffix('.py')),'owned_script_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),'registered_script_sha256':expected['generate/scratch/17592186059827.py'],'prior_root_approved_sha256':'c8a15cd921fbaf38c14fb5e6dff091be329f8af9a30bdc7fbaf591fc180f54fa','registered_files_including_caches_unchanged':len(expected),'source_basis':2275,'source_sha256':hashlib.sha256((H/'source.json').read_bytes()).hexdigest(),'source_original_banks':validation['complete_banks'],'source_original_choices':validation['choices_matched'],'native_accepted':validation['native']['accepted_checks'],'native_rejected':validation['native']['rejected_checks'],'native_unresolved':validation['native']['documented_unresolved_checks'],'browser_records':len(browser['records']),'browser_math_expressions':sum(r['rendered_math']for r in browser['records']),'rendered_readback':readback,'database_writes':0,'root_independent_QA_required':True,'files':{str(p):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size}for p in files}}
(H/'freeze-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('FROZEN',manifest['owned_script_sha256'],len(files),'owned/reference files;',len(expected),'registered files unchanged')

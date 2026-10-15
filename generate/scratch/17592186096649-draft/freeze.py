"""Read-only registered baseline verification and full owned artifact freeze."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;ROOT=D.parents[2];B=D.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((D/'registered-baseline.json').read_text());paths=[B/'17592186096649.py']+list((B/'17592186096649').rglob('*'))+list((B/'__pycache__').glob('17592186096649.*.pyc'))
assert sorted(str(p.relative_to(ROOT)) for p in paths)==baseline['paths'],'registered exact path set changed'
assert {str(p.relative_to(ROOT)):sha(p) for p in paths if p.is_file()}==baseline['files'],'registered file bytes changed'
source=ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186096649.json';assert (D/'source.json').read_bytes()==source.read_bytes()
meta=json.loads((D/'reference/grader-build.json').read_text());hashes={meta['source']:meta['source_sha256'],meta['library']:meta['library_sha256'],meta['binary']:meta['binary_sha256'],**meta['engine_sources'],**meta['dependencies']};assert all(sha(ROOT/p)==h for p,h in hashes.items())
assert sha(D/'check-engine')==meta['binary_sha256'];assert sha(D/'reference/libcourse_academy_engine.rlib')==meta['library_sha256']
report={'status':'pass','registered_files_unchanged':len(baseline['files']),'registered_exact_path_set_unchanged':True,'frozen_source_exact':True,'frozen_source_sha256':sha(D/'source.json'),'current_helper_recorded_hashes_verified':len(hashes),'current_helper_sha256':sha(D/'check-engine')}
(D/'immutability.json').write_text(json.dumps(report,indent=2)+'\n')
files=[D.with_suffix('.py')]+[p for p in D.rglob('*') if p.is_file() and p.name!='freeze-manifest.json']
manifest={'status':'local steps3–7 validated; independent root QA pending; no registration or database writes','generator_sha256':sha(D.with_suffix('.py')),'source_sha256':sha(D/'source.json'),'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)}}
(D/'freeze-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(report);print('Full owned freeze',len(files),'files; generator',manifest['generator_sha256'])

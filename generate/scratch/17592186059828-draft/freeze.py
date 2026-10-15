"""Freeze complete owned tree; verify registered pathset/bytes and provenance."""
from pathlib import Path
import hashlib,json,datetime
H=Path(__file__).resolve().parent;R=H.parents[2]
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads((H/p).read_text())
baseline=load('immutable-baseline.json')['files'];scratch=R/'generate/scratch';actual={str(p.relative_to(R)) for p in (scratch/'17592186059828').rglob('*') if p.is_file()}|{'generate/scratch/17592186059828.py'}|{str(p.relative_to(R)) for p in (scratch/'__pycache__').glob('17592186059828.*.pyc') if p.is_file()}
assert actual==set(baseline)
for p,h in baseline.items():assert digest(R/p)==h,p
assert (H/'source.json').read_bytes()==(R/'generate/runs/current/refresh-2026-10-14/sources/17592186059828.json').read_bytes()
source=load('source.json')['record'][':knowledge-point/questions'];original=[q for q in source if ':question/math-academy-id' in q];inventory=[q for q in source if ':question/math-academy-id' not in q]
assert [c['record']for c in load('source-cases.json')]==original
assert [c['record']for c in load('independent-inventory.json')['questions']]==inventory
p=load('reference/grader-build.json');checks={p['source']:p['source_sha256'],p['library']:p['library_sha256'],p['binary']:p['binary_sha256'],**p['engine_sources'],**p['dependencies']}
for path,h in checks.items():assert digest(R/path)==h,path
assert digest(H/'reference/check-engine-current')==p['binary_sha256']
v=load('validation.json');b=load('browser-rendering.json');pixels=load('rendered-readback.json');visual=load('visual-review.json');identity=load('identity-preservation.json')
assert v['passed'] and b['passed'] and pixels['passed'] and visual['passed'] and identity['matched']==identity['total']==26
assert all(im['width']>0 for record in b['records'] for im in record['images'])
files=[H.with_suffix('.py')]+sorted(p for p in H.rglob('*')if p.is_file()and p.name!='freeze-manifest.json')
external=sorted({x['path']for x in pixels['records'] if not Path(x['path']).is_relative_to(H)})
manifest={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owned_script':str(H.with_suffix('.py')),'owned_script_sha256':digest(H.with_suffix('.py')),'registered_script_sha256':baseline['generate/scratch/17592186059828.py'],'prior_root_approved_sha256':'14b06fe077b535df04a6e9a4adc447c0913d106a088a9b2a2b2cba064a5d2ddf','registered_files_including_caches_unchanged':len(baseline),'original_MA_banks':4,'original_MA_choices':20,'available_original_keys':2,'available_full_original_solutions':2,'missing_original_keys_and_solutions':2,'independent_inventory_banks':14,'independent_inventory_choices':70,'legacy_normal_ids_preserved':26,'finite_task_catalogs':v['finite_task_catalogs'],'whole_bank_profile_pairs':v['semantic_bank_sweep']+v['source_style_complete_bank_and_two_stage_sweep'],'native_accepted':v['native_grading']['accepted_checks']+v['additional_native_grading']['accepted_checks'],'native_rejected':v['native_grading']['rejected_checks']+v['additional_native_grading']['rejected_checks'],'native_unsupported':v['native_grading']['documented_unresolved_checks']+v['additional_native_grading']['documented_unresolved_checks'],'browser_records':len(b['records']),'browser_math_expressions':sum(r['rendered_math']for r in b['records']),'PNG_records':len(pixels['records']),'unique_PNGs':pixels['actual_pngs'],'source_basis':2275,'source_sha256':digest(H/'source.json'),'current_runner_sha256':p['binary_sha256'],'current_runner_provenance_paths_reverified':len(checks),'database_writes':0,'root_independent_QA_required':True,'limitations':v['limitations'],'external_assets':{p:{'sha256':digest(p),'read_only':True}for p in external},'files':{str(p.relative_to(R)):{'sha256':digest(p),'size':p.stat().st_size}for p in files}}
(H/'freeze-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('FROZEN',manifest['owned_script_sha256'],len(files),'owned files;',len(baseline),'registered files unchanged;',manifest['native_accepted'],'accepted',manifest['native_rejected'],'rejected',manifest['native_unsupported'],'unsupported')

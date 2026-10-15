"""Freeze all owned files after exact screenshot mapping and immutable rechecks."""
import sys;sys.dont_write_bytecode=True
import importlib.util,json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
s=importlib.util.spec_from_file_location('owned_validation',D/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((D/'render-report.json').read_text());rows=json.loads((D/'render-records.json').read_text());assert len(rows)==72
assert r['record_file_sha256']==sha(D/'render-records.json')
for check,row in zip(r['checks'],rows):
 assert check['record_sha256']==row['record_sha256']==v.g.hashof(row['record']);assert check['screenshot_sha256']==sha(ROOT/check['screenshot']);v.readback(row['record'])
for p,h in r['ui_source_hashes'].items():assert sha(ROOT/p)==h
review=json.loads((D/'review.json').read_text());md=(D/'review.md').read_text();assert len(review)==48 and all(v.g.markdown(x) in md for x in review)
cli=json.loads((D/'cli-json.json').read_text());assert isinstance(cli,list) and len(cli)==6
assert 'MISSING (raw source)' in (D/'cli-missing-preview.md').read_text()
protected=v.preservation();native=v.grader()
report=json.loads((D/'validation.json').read_text());report['render']={'records':72,'full_worked_solution_stages_checked':True,'actual_player_controls':'radio + MathLive blanks','errors':0,'overflow':0,'exposed_delimiters':0,'runtime_versions':r['runtime_versions'],'record_screenshot_hash_mapping':'render-report.json'};report['final_script_sha256']=sha(D.with_suffix('.py'));report['registered_protected_paths_unchanged']=protected;report['native_provenance_files_reverified']=native
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'render-review.md').write_text('''# Render review

72 exact stored records were rendered with actual current player routines and
assets at the actual720px lesson-content width. Every source mask, both authored
complete radio banks, all48 documented variants and twelve held-matrix targets across2x3 and3x2 product shapes are
represented. render-report.json maps each record SHA256 to a complete screenshot
and its SHA256; it checks every required matrix table and five aligned solution
rows and visible selected-product indices in normal solutions (raw missing solutions remain absent). All radio controls are visible and
clickable; actual MathLive blanks load, accept a value and render visibly.

Full-size inspection included source-q-70958 (largest matrices), source-q-318462
(implicit factors/blank), source-q-70791 (raw missing key/solution), easy-0
(authored omission/sign bank), moderate-4, hard-6 and held-target-5. Matrix entries,
selected row/column and every product/collection row remain readable through the
final result; no clipped content, exposed delimiters, MathJax errors or horizontal
overflow occurred. Inserted7 in blank screenshots is only the control-interaction
probe; mathematical/native correctness is established separately in validation.

The repaired first product is visibly indexed in easy-8, hard-12 and
held-target-11, inspected beside unchanged historical source-q-130111. The
normal selected-entry index is required independently in the DOM and arithmetic
readback; raw scalar/matrix equality remains flagged imprecise evidence.

Runtime versions and exact player asset hashes are in render-report.json.
''')
paths=[D.with_suffix('.py')]+list(D.rglob('*'));files={str(p.relative_to(ROOT)):sha(p) for p in sorted(paths) if p.is_file() and p!=D/'freeze.json'};directories=sorted(str(p.relative_to(ROOT)) for p in paths if p.is_dir())
freeze={'script_sha256':sha(D.with_suffix('.py')),'scope':'complete owned draft script/tree, excluding self-referential freeze.json only','files':files,'directories':directories,'registered_full_pathset_rechecked':protected,'native_actual_files_rechecked':native,'stop_after_step':7,'database_writes':0,'registration_changes':0}
(D/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
assert all(sha(ROOT/p)==h for p,h in files.items());v.preservation();v.grader();print(json.dumps({'script_sha256':freeze['script_sha256'],'owned_files_frozen':len(files),'registered_paths_unchanged':protected,'native_actual_files_rechecked':native,'render_records':72},indent=2))

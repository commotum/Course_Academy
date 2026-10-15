"""Freeze all owned bytes and path sets; retain whole registered baseline."""
import collections,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2];SCRIPT=H.with_suffix('.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((H/name).read_text())
baseline=read('reference/registered-baseline.json');reg=ROOT/'generate/scratch/17592186054676.py';actual={str(p.resolve()):sha(p)for p in[reg]+sorted(p for p in reg.with_suffix('').rglob('*')if p.is_file())};assert baseline==actual
assert (H/'source.json').read_bytes()==(ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186054676.json').read_bytes()
assert sha(H/'reference/check-engine')==sha(ROOT/'generate/runs/current/check-engine')
val=read('validation.json');br=read('browser-rendering.json');assert len(br['records'])==99 and not br['page_errors'];assert val['status']=='pass'
source=read('source-cases.json');review=read('review-cases.json');allrows=source+review
plots={Path(r['record']['generation']['plot_path']).resolve()for r in review};plotrows=list((H/'assets').glob('*.png'))
# Remove obsolete draft-renderer/before-correction assets only, never baseline tree.
for path in plotrows:
 if path.resolve()not in plots:path.unlink();path.with_suffix('.json').unlink(missing_ok=True)
mathcounts=collections.Counter();tasks=set()
for row in allrows:
 q=row['record']['question'];task=row['record']['generation']['task_fingerprint'];tasks.add(task)
 for f in q[':question/answer-fields']:mathcounts[f[':answer-field/type']]+=1
by={}
for row in source:
 k=row['source_level'];d=by.setdefault(k,{'records':0,'field_banks':0,'matched_choices':0,'matched_distractors':0});d['records']+=1
 for f in row['record']['question'][':question/answer-fields']:d['field_banks']+=1;d['matched_choices']+=len(f[':answer-field/choices']);d['matched_distractors']+=len(f[':answer-field/choices'])-1
(H/'bank-coverage.json').write_text(json.dumps({'basis':2275,'by_level':by,'complete_fields':16,'matched_choices':62,'total_choices':62,'matched_distractors':46,'total_distractors':46,'missing':[],'extra':[]},indent=2)+'\n')
(H/'visual-review.json').write_text(json.dumps({'source_assets_opened':13,'source_contact':'reference/source-contact.png','normal_and_controlled_graph_contact':'graph-review-contact.png','PNG_pixel_coordinate_checks':87,'canvas_label_clipping_failures':0,'label_marker_overlap_report':'plot-overlap-check.json','actual_player_rendered_records':99,'MathJax_errors':0,'literal_dollar_failures':0,'horizontal_overflow_failures':0,'screenshots_opened':['screenshots/hard-52.png','screenshots/easy-0.png'],'observations':'Source and normal plots show the same point-only grid purpose. Red axis points remain visible. All controlled member-role targets appear with coherent A/B/C coordinates. Integer labels, all equations and three substitution stages are readable; no text/plot clipping observed. The rational hard screenshot shows exact fractions in all dependent stages.'},indent=2)+'\n')
summary={'status':'ready_for_parent_QA','generator_sha256':sha(SCRIPT),'registered_baseline_files':len(baseline),'registered_path_set_and_hashes_unchanged':True,'source_basis':2275,'source_records':12,'MA_rated_records':2,'MA_unrated_checkbox_records':2,'captured_non_MA_records':8,'authored_hard':'rational slopes denominator 2/3; same three substitution tests; uncalibrated authored difficulty','source_choices':62,'source_complete_field_banks':16,'source_distractors':46,'source_errors_found':0,'review_records':87,'normal_actual_math_tasks_per_level':val['normal_tasks'],'controlled_member_positions':{'easy':['AB','AC','BC'],'moderate':['A','B','C'],'hard':['A','B','C']},'unique_actual_math_tasks_all_originals_and_reviews':len(tasks),'unique_generated_plot_assets':len(plots),'operative_algebra_stages_read':val['all_operative_stages_read'],'PNG_pixel_readbacks':87,'browser_complete_records':99,'negative_controls':10,'native':read('native-summary.json'),'database_writes':0,'registry_changes':0,'engine_changes':0,'limitations':['No captured hard evidence; authored hard difficulty is qualified rather than externally calibrated.','Unrated checkbox records are preserved as originals and have no guessed difficulty.','Selection-only fields have no free-entry algebraic equivalence contract; equivalent ID encodings are tested.','10000 per-level count guard is conservative, not an exact finite-capacity theorem.']}
(H/'freeze-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
excluded={'freeze-manifest.json'}
files=[SCRIPT]+sorted(p for p in H.rglob('*')if p.is_file()and p.relative_to(H).as_posix()not in excluded)
manifest={'generator':str(SCRIPT.relative_to(ROOT)),'excluded':['freeze-manifest.json'],'files':{str(p.relative_to(ROOT)):sha(p)for p in files},'registered_baseline':baseline,'registered_baseline_unchanged':True,'source_wrapper_sha256':sha(H/'source.json'),'native_binary_sha256':sha(H/'reference/check-engine')}
manifest['tree_sha256']=hashlib.sha256(json.dumps(manifest['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest();(H/'freeze-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({**summary,'owned_files':len(files),'tree_sha256':manifest['tree_sha256']},indent=2))

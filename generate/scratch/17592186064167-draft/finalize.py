"""Verify and freeze only this owned draft. No generation, DB, or shared mutation."""
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent;ROOT=D.parents[2];SCRIPT=D.with_suffix('.py');K='17592186064167'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
before=json.loads((D/'registered-before.json').read_text())
paths=[ROOT/'generate/scratch'/f'{K}.py',*list((ROOT/'generate/scratch'/K).rglob('*')),*list((ROOT/'generate/scratch/__pycache__').glob(K+'.*.pyc'))]
now={str(p.relative_to(ROOT)):sha(p) for p in paths if p.is_file()}
assert sorted(now)==sorted(before['pathset']);assert now==before['sha256']
write('registered-baseline-verification.json',{'exact_pathset_unchanged':True,'all_sha256_unchanged':True,'registered_file_count':len(now),'before_manifest_sha256':sha(D/'registered-before.json'),'pathset':sorted(now),'sha256':dict(sorted(now.items()))})
F=ROOT/'generate/runs/current/refresh-2026-10-14'
for a,b in [(D/'source.json',F/'sources'/f'{K}.json'),(D/'reference/topic.json',F/'topics/17592186049481.json'),(D/'reference/lesson.json',F/'lessons/17592186049481.json')]:assert a.read_bytes()==b.read_bytes()
source=json.loads((D/'source.json').read_text());records=source['record'][':knowledge-point/questions'];ma=[q for q in records if q.get(':question/math-academy-id')];non=[q for q in records if not q.get(':question/math-academy-id')]
assert [v['record'] for v in json.loads((D/'source-cases.json').read_text())]==ma
assert [v['record'] for v in json.loads((D/'independent-inventory.json').read_text())['questions']]==non
v=json.loads((D/'validation.json').read_text());assert v['generator_sha256']==sha(SCRIPT)
manifest=json.loads((D/'reference/grader-build.json').read_text())
for p,h in {**manifest['engine_sources'],**manifest['dependencies']}.items():assert sha(ROOT/p)==h
for role in ['binary','library']:assert sha(ROOT/manifest[role])==manifest[role+'_sha256']
rr=json.loads((D/'render-report.json').read_text());assert rr['errors']==rr['overflow']==rr['exposed_delimiters']==0
for p,h in rr['ui_source_hashes'].items():assert sha(ROOT/p)==h
native=v['native'];sn=json.loads((D/'source-native-report.json').read_text());api=json.loads((D/'public-api-checks.json').read_text());assert api['generator_sha256']==sha(SCRIPT);assert api['all_count1']==3 and api['dedup_across_level_aliases']
write('readiness.json',{'status':'ready for independent root QA; approval pending','generator_sha256':sha(SCRIPT),'source':v['source_counts'],'source_exact_byte_wrapper':True,'topic_and_lesson_exact_byte_wrappers':True,'math':{'finite_instances':v['full_finite_normal_instances'],'equations':v['parsed_math']['equations'],'options':v['parsed_math']['options'],'negative_controls':len(v['negative_controls']),'preserved_previous_normal_records':v['preserved_previous_normal_review_instances']},'native':{'entry_point':native['entry_point'],'normal_accepted':native['accepted_checks'],'normal_rejected':native['rejected_checks'],'normal_records':len(native['records']),'known_equivalent_arbitrary_C_rejections':24,'source_and_inventory_accepted':sn['accepted_checks'],'source_and_inventory_rejected':sn['rejected_checks'],'source_fieldless_qualified_gaps':len(json.loads((D/'source-native-gaps.json').read_text())),'current_engine_sources_library_binary_verified':True},'render':{'records':rr['records'],'screenshots':len(rr['screenshots']),'actual_player_controls':True,'errors':0,'visually_inspected':len(json.loads((D/'visual-qa.json').read_text())['inspected'])},'registered_exact_pathset_and_sha_unchanged':True,'limitations':v['limitations'],'database_writes':0,'registrations':0,'candidate_reruns':0})
files=[SCRIPT]+[p for p in D.rglob('*') if p.is_file() and p!=D/'freeze.json'];hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(files)}
write('freeze.json',{'status':'frozen draft; independent root QA/approval pending','generator_sha256':sha(SCRIPT),'registered_immutable_verified':True,'owned_files':len(hashes),'sha256':hashes,'freeze_self_excluded':True})
print(json.dumps(json.loads((D/'readiness.json').read_text()),indent=2))

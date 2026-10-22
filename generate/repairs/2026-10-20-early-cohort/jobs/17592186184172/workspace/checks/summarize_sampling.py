"""Collect tested artifacts and verify unchanged runtime hashes; no runtime writes."""
import json,hashlib,difflib
from validate import W as w,visible

e=w/'evidence/sampling-repair'
current=(w/'17592186184172.py').read_text()
prior=current.replace("VERSION='1.1.1'","VERSION='1.1.0'").replace(' # Select a seeded profile order before truncating to the requested count.\n # Every profile is eligible even when practice requests fewer than a cycle.\n random.Random(seed).shuffle(keys)\n','')
hash_before=hashlib.sha256(prior.encode()).hexdigest()
assert hash_before=='0a0cea68a7af2518a91985ff4710935500515ac32406209990259c3511aa0d95'
(e/'reviewed-generator-before.py').write_text(prior)
(e/'runtime-change.diff').write_text(''.join(difflib.unified_diff(prior.splitlines(True),current.splitlines(True),fromfile='reviewed/17592186184172.py',tofile='17592186184172.py')))
r=json.loads((e/'results.json').read_text());n=json.loads((e/'native-report.json').read_text());render=json.loads((e/'render/rendering.json').read_text())
assert render['passed']
for f,h in r['runtime_hashes'].items():assert hashlib.sha256((w/f).read_bytes()).hexdigest()==h
old_hashes=json.loads((w.parent/'review-1-policy-2-45a9ed86924bfc07/runtime-file-hashes.json').read_text())['files']
assert all(r['runtime_hashes'][f['file']]==f['package_sha256'] for f in old_hashes if f['file']!='17592186184172.py')
semantics=set()
for name in ['moderate-batches','hard-batches','moderate-controlled']:
 for record in json.loads((e/name/'accepted.json').read_text()):semantics.add(visible(record)['semantic'])
summary={'finding_id':'a9f111072c7a682655bb','status':'passed','repair':'Seeded profile ordering before batch truncation; preserves every supported source profile and existing per-instance construction.','before_entrypoint_sha256':hash_before,'source_fidelity':{'questions':r['source_replays'],'choices':r['source_choices'],'unchanged_source_and_helpers':True},'math':'Independent visible-record parser passed every replay, sample and controlled case.','grading':{k:n[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks','database_writes']},'variation':{'normal_cli_records':60,'moderate_profiles':8,'hard_profiles':7,'controlled_records':r['controlled_records'],'distinct_delivered_semantic_instances':len(semantics),'all_previously_omitted_profiles_survive_delivery':True,'singleton_and_complete_cycles':'passed','counterfactuals_and_within_profile_shortcuts':'passed before and after shared delivery filters'},'rendering':{'passed':True,'visually_inspected_screenshots':['render/question-001.png','render/question-002.png','render/question-003.png']},'packaging':'Manifest-only relocation and determinism pass for moderate and hard. Python 3.13.5, SymPy 1.14.0.','inventory':'All 15 captured entries independently verified as original sources; no affected generated instance demonstrated.','limitations':r['limitations']}
(e/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'status':'passed','distinct_delivered_semantic_instances':len(semantics),'accepted_grader_checks':n['accepted_checks'],'rejected_grader_checks':n['rejected_checks'],'unrelated_runtime_files_unchanged':True}))

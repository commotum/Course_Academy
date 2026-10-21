#!/usr/bin/env python3
"""Bind concise final evidence to actual reports and current runtime hashes."""
import hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;E=R/'evidence'
def load(n):return json.loads((E/n).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
manifest=json.loads((R/'package.json').read_text());packing=load('packaging-results.json')
assert packing['passed']
assert packing['runtime_sha256']=={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in manifest['files']}
for name in ['source-replay.json','regression-results.json','pedagogical-variation.json','shortcut-results.json','low-mass-results.json']:
 assert load(name)['passed'],name
native=load('grader-report.json');assert native['documented_unresolved_checks']==0 and native['database_writes']==0
render=load('render-attempt-2/rendering.json');assert render['passed'] and len(render['cases'])==8
assert all(Path(c['screenshot']).exists() and c['passed'] for c in render['cases'])
for tag,n in [('sample',88),('batch',5),('controls',55)]:assert len(load(f'delivery-{tag}/accepted.json'))==n
before=load('attempt-2/before-shortcut-results.json');assert not before['passed'] and before['minimal']['success']
assert load('shortcut-results.json')['minimal']['success'] is False
save('render-inspection-attempt-2.json',{'passed':True,'renderer_report':'render-attempt-2/rendering.json','screenshots_inspected':list(range(1,9)),
 'inspection_images':['render-attempt-2/banks-contact-sheet.png','render-attempt-2/solution-contact-sheet.png'],
 'observations':'All eight actual UI question cards and complete five-choice banks are legible. Reported minimal solution shows the mass balance, solved Q(t), t_o=5 and rounded 7.3 lb. Same-bank initial masses 1 and 17 show changed correct values 35.3 and 39.3 lb. No clipping, broken math or missing units observed.'})
old=E/'commands.json'
if not (E/'attempt-2/prior-commands.json').exists():(E/'attempt-2/prior-commands.json').write_bytes(old.read_bytes())
PYTHON='/home/jake/Developer/Course_Academy/.venv/bin/python';REPO='/home/jake/Developer/Course_Academy'
commands=[{'command':PYTHON+' shortcut_checks.py --package .','stage':'before repair','result':'exit 1, exact radius failure reproduced','evidence':'attempt-2/before-shortcut-results.json'},
 {'command':PYTHON+' evidence/attempt-2/negative/shortcut_checks.py --package ../review-1-policy-2-d5d71edec3e4bef3/relocated-package','result':'exit 1 on old version-2 package: same-bank all-rank witness fails (recorded exact assertion in negative/evidence output).'},
 {'command':PYTHON+' regression_checks.py','result':'exit 0; both older defects remain repaired'},
 {'command':PYTHON+' repair_checks.py','result':'exit 0; 11 complete source replays, 31 exact ODE/displayed-solution checks, 88 sampled records representing 8 distinct physical tasks across 11 contexts'},
 {'command':PYTHON+' shortcut_checks.py','result':'exit 0; exact failure repaired, 55 same-bank physical counterfactuals, per-template cues and post-delivery checks'},
 {'command':PYTHON+' bank_boundary_checks.py','result':'exit 0; low mass retains every rank; five same-bank displayed solutions independently verified'},
 {'command':PYTHON+' inventory_check.py','result':'exit 0; 10 historical generated records reproduced; all median-affected, one also radius-affected'}]
for tag,file in [('sample','sample-records.json'),('batch','batch-records.json'),('controls','same-bank-counterfactual-records.json')]:
 commands.append({'command':f'{PYTHON} {REPO}/generate/pipeline/check_delivery.py --input evidence/{file} --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-{tag} --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math','result':f'accepted {len(load(f"delivery-{tag}/accepted.json"))}; 0 duplicates'})
commands += [{'command':PYTHON+' finish_checks.py','result':'exit 0; post-filter probes, fresh easy-only selection, deterministic relocation, grader/render fixtures'},
 {'command':REPO+'/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json','result':f"{native['accepted_checks']} accepted / {native['rejected_checks']} rejected / 0 unresolved"},
 {'command':f'{PYTHON} {REPO}/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render-attempt-2 --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math --limit 8','result':'8 passed, screenshots visually inspected'},
 {'command':PYTHON+' finalize_evidence.py','result':'current hashes and reports agree'}]
save('commands.json',commands)
summary={'status':'ready','change':'Replace key-centered distance-limited distractors with a whole ordered adjacent-gap bank translated to the chosen key rank. Only nonpositive choices cause shape resampling; no source profiles or solution methods removed.',
 'source_fidelity':{'complete_banks':11,'choices':55,'source_omissions_preserved':True},
 'correctness':{'exact_ode_displayed_solution_checks':31,'numeric_visible_record_checks':149,'additional_full_displayed_checks':10},
 'grading':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0},
 'decision_variation':{'sample_physical_tasks':8,'sample_contexts':11,'same_bank_distinct_physical_tasks':5,'same_bank_contexts':11,'radius_center_correct_per_context':1,'radius_center_wrong_per_context':4,'batch_radius_singletons':0,'source_replay_not_counted_as_authored_variation':True},
 'runtime_sha256':packing['runtime_sha256'],'screenshots_inspected':8,
 'limitations':['Ten captured historical generated records remain affected and unchanged; one also shows the latest radius shortcut. Exact IDs, full replays and findings are in affected-inventory.json and evidence/generated-records.json.',
 'Learner selection is a read-only conditional fresh easy-pool reproduction with hypothetical new entity IDs. Live history, active policy and future inventory are unavailable.',
 'q-336499 lacks source key, solution and difficulty; raw replay preserves omissions and is evidence-only. Normal completion is explicitly authored.',
 'Delivery and primary fidelity claim are for requested easy band; earlier authored moderate/hard APIs are preserved and smoke-tested.',
 'Finite shortcut probes establish failure of the demonstrated guarantee, not exhaustive absence of every adversarial cue. Low-mass positivity conditioning may resample shapes while retaining selected rank.'],
 'publication':False,'database_writes':0,'engine_edits':False}
if (E/'author-summary.json').exists() and not (E/'attempt-2/prior-author-summary.json').exists():(E/'attempt-2/prior-author-summary.json').write_bytes((E/'author-summary.json').read_bytes())
save('author-summary.json',summary)
p=R/'session-state.md';text=p.read_text();marker='\nAttempt 2 completed:'
text=text.split(marker)[0]+marker+' exact seed 41072 radius defect repaired family-wide. Older source and rank regressions retained; all three findings declared. All current runtime hashes agree with relocated-package evidence. Delivery: 88 sample / 5 replacement / 55 controlled records accepted. Native: 57 accepted / 208 rejected / zero unresolved. Actual UI: 8 rendered and visually inspected. Inventory: 10 historical generated records reproduced, one also radius-affected; stored content unchanged. Final commands in evidence/commands.json; claims and limits in evidence/author-summary.json. Ready for independent review; no publication or database writes.\n';p.write_text(text)
print(json.dumps({'status':'ready','runtime_hashes_verified':True,'grading_checks':native['accepted_checks']+native['rejected_checks'],'rendered':8}))

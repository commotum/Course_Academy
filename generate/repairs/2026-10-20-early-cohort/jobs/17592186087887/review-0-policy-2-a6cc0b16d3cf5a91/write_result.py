import json,pathlib
E=pathlib.Path(__file__).resolve().parent
load=lambda n:json.loads((E/n).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
a=load('source-analysis.json')
save('minimal-failing-record.json',[load('counterfactuals.json')[0]['before']])
def check(status,paths,details):return {'status':status,'evidence_paths':paths,'details':details}
result={
'verdict':'revise',
'summary':'Bank-only rules answer all 54 easy instances, all 5 runner records, all 4 deduplicated survivors, and 5 reproduced stored generated questions. Mathematics and native grading pass; the practice design permits bypassing the intended ODE reasoning. Package unchanged.',
'source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
'checks':{
'source_replay':check('passed',['source-analysis.json','source-replay.json','source-replay-records.json','source-images.png'],'All three explicitly easy sources replay their equations and complete five-choice banks. Nine implemented source cases replay mathematically; original missing key and source typo are documented. Canonical quadratic and additional moderate arctangent cases are explicitly unsupported; this verdict concerns requested easy delivery.'),
'math':check('passed',['math.json','counterfactual-results.json'],'Independent prompt parsing and symbolic directional derivatives verify all 54 easy instances and the exact 5-record runner batch; each bank has exactly one general solution. Relevant coefficient and integration-branch pairs update the solution correctly.'),
'variety':check('failed',['packaging.json','independent-samples.json','shortcut-results.json','shortcut-regression.json','delivery-batch/delivery.json'],'All 54 finite coefficient slots and both signs are covered, but every recognizable family preserves an incidental bank-only answer rule. The exact runner batch scores 5/5 and its four deduplicated survivors score 4/4 using those rules; numeric uniqueness does not establish meaningful practice.'),
'scope':check('passed',['source-analysis.json','scope.json','math.json'],'Easy variations preserve y=vx, separation, elementary integration and one radio response. Signed coefficients introduce no additional technique or reasoning stage.'),
'grading':check('passed',['grader-final-input.json','grader-final-results.json','math.json'],'Actual native learning::grade_field: 186 accepted and 276 rejected checks, zero unresolved. Every alternative is tested on sampled/runner records and controlled pairs; additional checks submit bank-only predictions on raw, delivered and reconstructed inventory records. Free-entry equivalence is inapplicable to this radio contract.'),
'rendering':check('passed',['render/rendering.json','render-delivered/rendering.json','render-inspection.json','render/question-001.png','render/question-005.png','render/question-006.png','render-delivered/question-004.png'],'Unmodified actual UI renders 10 controlled instances and all four runner survivors without reported errors. Representative full screenshots and the contact sheet were inspected; notation, controls and worked solutions display correctly. UI choice shuffling does not defeat shape cues.'),
'packaging':check('passed',['packaging.json','package-integrity.json','commands.json'],'Installed Python exactly 3.13.5 matches manifest; third-party packages object is correctly empty. Deterministic replay, relocation, invalid-parameter rejection and JSON stdout pass. Package file hashes remain unchanged.'),
'decision_variation':check('failed',['pedagogical-variation.json','counterfactuals.json','counterfactual-results.json','shortcut-regression.json','selection.json','affected-inventory.json','generated-records.json','inventory-assessment.json'],'Relevant and irrelevant counterfactual dependencies pass, but conditional bank-shape strategies each score 18/18, versus 0.2 random-choice baseline. Combined strategy scores 49/49 after actual delivery filtering. Captured basis-5449 inventory contains five exactly reproduced affected generated questions. Native selection rules do not remove these eligible easy cases; live learner proportions are not asserted.')
},
'findings':[{
'kind':'decision_shortcut',
'description':'The easy-family bank construction reveals the correct candidate without inspecting the differential equation: cube_root always has one cube-root candidate; linear_log has one candidate containing both x ln|x| and +Cx; affine always makes the smaller-magnitude linear coefficient among its two Cx^2 candidates correct. Each rule scores 18/18 across both coefficient signs. The combined rule answers the entire supplied batch and every survivor. Five stored generated questions reproduce the same defects with matching UUIDs and publisher fingerprints.',
'source_refs':['2b4ed6f3-beb2-5be5-83cb-e8d41e7b8f3b','ed854c8a-5a47-5533-b48c-04deb7b81625','73b06f86-eb7f-5333-916f-45bb6952f791','tutorial fe0a9e9e-ab23-5364-99bb-cddbfd67a4a4: x dv/dx=F(v)-v','generate/principles.md: meaningful variety and incidental shortcuts'],
'reproduction':"From evidence_root, run PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_shortcut.py (expected exit 1). Minimal case: generator.generate('cube_root', 2, seed=826033), saved in minimal-failing-record.json. For y'=(2x^3+y^3)/(xy^2), select the sole cube-root candidate y=x sqrt[3](6 ln|x|+C) without reading the equation. With a=-2 the same action selects the new correct answer; the learner never needs to determine 3a. Native acceptance is retained in grader-final-results.json. Full reproduction commands are in commands.json.",
'requested_change':'Change the family-wide extension-bank rules so eligible correct-answer roles are not identifiable from candidate shapes or fixed coefficient comparisons. Include plausible same-shape distractors requiring calculation of the surviving term and integration coefficient; vary affine distractor magnitudes so choosing the smaller one is not sufficient. Preserve source replay and difficulty. Regenerate the supplied batch and retain the failing bank-only regression as an acceptance test; do not rely on position shuffling or remove source families.'
}]
}
save('review.json',result)
# Validate the actual evidence contract, keeping its result as evidence.
import jsonschema
schema=json.loads(pathlib.Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json').read_text())
jsonschema.validate(load('pedagogical-variation.json'),schema)
paths=[]
for c in result['checks'].values():paths.extend(c['evidence_paths'])
paths.extend(result['source_analysis']['evidence_paths'])
pv=load('pedagogical-variation.json')
for section in ['coverage','counterfactuals','shortcut_probes']:
 for row in pv[section]:paths.extend(row['sample_refs'])
paths.extend(pv['delivery']['sample_refs'])
missing=[p for p in paths if not (E/p).is_file() or (E/p).stat().st_size==0]
assert not missing,missing
assert load('package-integrity.json')['unchanged']
assert len(load('affected-inventory.json')['affected_questions'])==5
save('evidence-validation.json',{'pedagogical_schema_valid':True,'all_referenced_evidence_nonempty':True,'referenced_paths':sorted(set(paths)),'affected_inventory_entries':5,'package_unchanged':True,'verdict':'revise','strict_regression_exit_code':1})
(E/'session-state.md').write_text('Review complete: verdict revise, saved review.json. Independent source account precedes package inspection. All 54 easy slots and exact runner batch checked; math passes, native grader 186 accepted/276 rejected; 10 controlled UI instances and four delivered survivors rendered. Shape-only answer rules solve 54/54 raw,49/49 survivors,5/5 runner,4/4 runner survivors,5/5 stored generated. Strict reproduce_shortcut.py exits1. affected-inventory.json contains all five exact reconstructed generated records; no source originals marked generated. Pedagogical schema and all evidence paths validated; package unchanged. No publication or database writes.\n')
print(json.dumps({'verdict':result['verdict'],'checks':{k:v['status'] for k,v in result['checks'].items()},'evidence_contract':'valid'}))

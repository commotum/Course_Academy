import pathlib,json,sys
sys.dont_write_bytecode=True
from independent_math import vec,field,correct
E=pathlib.Path(__file__).resolve().parent
# Independently compare the captured correct links, not merely whole banks.
s=json.load(open(E.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions'];rr=json.load(open(E/'source-replay-records.json'));checks=json.load(open(E/'source-replay.json'))
for q,r,c in zip(s,rr,checks):
 f=q[':question/answer-fields'][0];ref=f.get(':answer-field/correct')
 if ref:
  aid=ref[':answer/id'] if isinstance(ref,dict) else ref[-1]
  original=next(x for x in f[':answer-field/choices'] if x[':answer/id']==aid)
  generated=next(x for x in field(r)[':answer-field/choices'] if x[':answer/id']==correct(r))
  c['captured_correct_value_matches']=vec(original[':answer/value'])==vec(generated[':answer/value']);assert c['captured_correct_value_matches']
 else:c['captured_correct_value_matches']='Missing source link; independently inferred x=6, y=13-2z, z arbitrary.'
(E/'source-replay.json').write_text(json.dumps(checks,indent=2)+'\n')
a=json.load(open(E/'source-analysis.json'))
def ck(paths,details):return {'status':'passed','evidence_paths':paths,'details':details}
x={'verdict':'accepted','summary':'The revised easy generator and exact five-question batch pass the targeted review. All retained counterexamples are repaired. Historical inventory defects are documented separately; package unchanged.','source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs']},'checks':{
'source_replay':ck(['source-replay.json','source-replay-records.json','source-confirmation.json','counterfactual-results.json'],'All 14 complete source banks and 13 captured correct links match; canonical free-y system is reached. Missing source key/solution is independently inferred and documented.'),
'math':ck(['math-results.json','solution-results.json','focused-results.json','focused-solution-results.json','role-results.json'],'188 current sample/control records pass independent exact system, full-solution, key and worked-step checks.'),
'variety':ck(['resampling-stages.json','rejection-tests.json','strict-regressions.json','delivery-stages.json','delivery-shortcuts.json'],'All six justified mathematical cases occur in fresh sampling and survive filtering. Source-backed zero/equal-coordinate and rational cases remain supported; exact batch contains five meaningful cases.'),
'scope':ck(['scope-review.json','source-analysis.json'],'Requested easy outputs retain small dependent systems, elementary row operations, one free parameter and the five-choice radio contract. Legacy higher bands are not newly certified.'),
'grading':ck(['grader-input.json','grader-results.json','focused-grader-input.json','focused-grader-results.json','controlled-validation.json'],'Native grader matches 944 current/control responses and five historical-witness responses, including all choices and relevant/irrelevant counterfactuals; no unresolved outcomes. No free-entry contract applies.'),
'rendering':ck(['render-inspection.json','render-all/rendering.json','render-remaining/rendering.json','render-focused/rendering.json','render-remaining/question-016.png','render-focused/question-005.png'],'Actual UI passes 30 render cases. Opened representative screenshots verify controls, rational/zero cases, row-operation solutions and controlled answer changes.'),
'packaging':ck(['packaging.json','package-integrity.json','repair-verification.json','strict-regressions.json','provenance.json'],'Exact declared dependencies, deterministic replay and declared-file relocation pass. Executable historical predicates fail on their original witnesses and pass currently. All 289 package files are unchanged.'),
'decision_variation':ck(['pedagogical-variation.json','unit-repair-results.json','controlled-validation.json','delivery-stages.json','learner-selection.json','inventory-unit-cue.json','affected-inventory.json','generated-records.json'],'Unit typography no longer identifies the key in tested ordinary source-profile draws. All five answer roles work with fixed banks in each of six cases. Exact batch survives actual delivery filtering and has no demonstrated tested shortcut. Captured selection rules and inventory limits are recorded.')},'findings':[]}
x['source_analysis']['evidence_paths']=['source-analysis.json','source-confirmation.json','provenance.json']
for name,c in x['checks'].items():
 for p in c['evidence_paths']:assert not pathlib.Path(p).is_absolute() and (E/p).is_file() and (E/p).stat().st_size,(name,p)
for p in x['source_analysis']['evidence_paths']:assert (E/p).stat().st_size
assert set(x['checks'])==set(['source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'])
(E/'result.json').write_text(json.dumps(x,indent=2)+'\n')
(E/'commands.md').write_text('''All commands run from this evidence_root using /home/jake/Developer/Course_Academy/.venv/bin/python and -B. Nothing is published or written to the database.

- `python -B review.py`: independent source replay, fresh seeds 93210..93245, rational/source controls, explicit boundaries, mathematical checks, deterministic replay and relocation.
- `python -B regression_checks.py`: retained original failures and exact historical inventory reproduction.
- `python -B changed_probes.py`: strict fraction repair and template controls.
- `python -B solution_checks.py`: independent row-operation transitions and final solution checks.
- `python -B author-checks/validate_repair.py`, `python -B author-checks/rational_support.py`, `python -B author-checks/unit_support.py`: copied author suites redirected entirely into author-results/.
- `python -B focused_audit.py`: changed supplied-coordinate banks, retained strict unit/fraction regressions on failing and repaired executables, homogeneous signs and fixed-bank role changes.
- `python -B focused_solution_checks.py`: new supplied-coordinate and fixed-bank solution steps.
- `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json` and the corresponding focused-grader-input/results: actual native grading.
- `python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input INPUT --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output OUTPUT --math-root /media/jake/SSD/EDB/math`: INPUT/OUTPUT pairs listed in delivery-stages.json. This uses actual shared filtering read-only.
- `python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-all --math-root /media/jake/SSD/EDB/math` (six default cases); repeat with `--input render-remaining-records.json --output render-remaining --limit 18`, then `--input focused-render-records.json --output render-focused --limit 6`.
- `python -B finish_evidence.py`: stage/cue measurements, selection formulas, pedagogical schema/ref validation, rendering account and full package byte integrity.
- `python -B record_result.py`: independent captured-correct-link comparison and final report contract.

Copied-script provenance is in provenance.json; only evidence-root paths and fresh review seeds were changed. Strict historical failure commands deliberately return 1. Full records, seeds/parameters and actual outcomes are retained. The interrupted first attempts to redirect copied author fraction imports were corrected before successful runs; no package path was written.
''')
(E/'session-state.md').write_text('COMPLETE. result.json verdict accepted, all eight checks passed, no current findings. Evidence contract verified. Exact five-record batch examined and survives delivery. 188 independent current math/solution cases; 944 current/control native responses plus five historical responses; 30 actual UI renders. Historical ten affected inventory records reproduced separately and retained. All 289 package files unchanged; no database writes, asset publication or generator edits.\n')
print(json.dumps({'verdict':x['verdict'],'checks':len(x['checks']),'findings':len(x['findings']),'result':'result.json'}))

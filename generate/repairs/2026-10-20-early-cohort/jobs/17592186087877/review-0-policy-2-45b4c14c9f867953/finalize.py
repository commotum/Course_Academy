import audit as a
import json,pathlib
src=a.load(a.EVID/'source-analysis.json')
def ck(status,paths,details):return {'status':status,'evidence_paths':paths,'details':details}
report={
 'verdict':'revise',
 'summary':'All three easy templates expose a perfect answer-bank-only shortcut. It survives delivery filtering and is reproduced in three stored generated questions. Package files remain unchanged.',
 'source_analysis':{k:src[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
 'checks':{
  'source_replay':ck('passed',['source-analysis.json','source-replay-records.json','source-replay-results.json','source-prose-results.json'],'All eight supplied five-choice banks replay; all prompt prose and six available solution stage/prose masks match. Missing source keys/solutions, malformed historical distractor and supported sign/domain corrections are explicitly distinguished.'),
  'math':ck('passed',['audit.py','math-results.json','delivery-math-results.json'],'Independent symbolic parsing verifies prompts, unique valid choices, normalized right sides, final solutions and expanded multiplication rows for 21 raw test records, eight source replays and 16 delivered records.'),
  'variety':ck('failed',['samples-independent.json','shortcut-results.json','selection-results.json'],'Signed coefficients, forcing and positions vary, but the same answer-producing bank role predicts 12/12 fresh easy answers, including 4/4 in each template. All 16 accepted delivery records retain it.'),
  'scope':ck('passed',['source-analysis.json','scope-results.json','packaging-results.json'],'Requested easy output retains constant-P integrating-factor transformation, five radio choices and source-comparable workload. All eight source families replay. Authored hard scope is outside this requested-easy delivery audit.'),
  'grading':ck('passed',['grader-input.json','grader-report.json','counterfactual-results.json'],'Actual native learning::grade_field accepts 37 independently verified valid radio choices and rejects 148 distractors, including normalized delivered records. No free-entry fields are used; free-entry equivalence is inapplicable.'),
  'rendering':ck('passed',['render-counterfactual/rendering.json','render-other/rendering.json','render-inspection.json'],'Unmodified actual UI renders all eight representative records successfully; all eight screenshots inspected, including controlled coefficient/shuffle pairs and complete worked solutions.'),
  'packaging':ck('passed',['packaging-results.json','package-before.json','package-after.json','review-commands.json'],'Exact manifest/runtime match: Python 3.13.5, SymPy 1.14.0 nested under packages. Deterministic replay, relocation through module and CLI, invalid parameters/field/level rejection pass. No assets or external output required; package hashes unchanged.'),
  'decision_variation':ck('failed',['pedagogical-variation.json','counterfactual-records.json','counterfactual-results.json','regression-shortcut.py','regression-shortcut-result.json','affected-inventory.json','generated-records.json'],'Relevant and irrelevant counterfactual dependencies pass, but the qualifying factor is always uniquely accompanied by its reciprocal and square. This bank-only cue bypasses reading P and Q; rejection, deduplication and positive-weight easy selection do not remove it.')
 },
 'findings':[{
  'kind':'decision_shortcut',
  'description':'The authored constant-P bank is always [I, 1/I, I^2, x, x^2]. Without inspecting the ODE, select the exponential whose reciprocal and square are also offered (equivalently, choose the smaller-magnitude exponent among the two with the same sign). This gives the correct answer for every allowed nonzero a in all three easy templates. Observed successes: 12/12 fresh, 5/5 runner, 12/12 delivered fresh, 4/4 delivered runner. Three stored generated easy records reproduce exactly; affected-inventory.json identifies them.',
  'source_refs':['question 65a9092a-d6a6-5192-82ca-c04151a6438f','question dba525fe-7e4d-5319-88bd-1b806feb0904','tutorial a6a381ed-e9ab-5deb-9d74-30900610edf1, steps 1-4','tutorial a7f8aa2e-e022-57eb-be82-5f539a4512f6: I prime=P I','generate/principles.md section 2','workspace/17592186087877.py factors(): authored constant-P branch'],
  'reproduction':'Run /home/jake/Developer/Course_Academy/.venv/bin/python regression-shortcut.py from evidence_root; expected current exit 1. Minimal instance: generate("easy", seed=99017, template="signed_constant_power", parameters={"a":"1","n":3}). Prompt y prime+y=x^3; offered factors x,e^(2x),x^2,e^x,e^(-x). The bank alone singles out e^x. Complete record: minimal-failing-record.json. Native acceptance and rendered evidence: grader-report.json and render-counterfactual/question-001.png.',
  'requested_change':'Change the family-wide authored easy bank-construction rule so the correct factor does not always occupy this unique reciprocal-and-square role. Vary which candidate qualifies using P while retaining valid complete banks, source method, five-choice response and difficulty; shuffling positions or changing a/Q is insufficient. Preserve the failing regression and add controlled cases where an unchanged candidate bank supports different correct factors as P changes, with native grading and subgroup shortcut checks.'
 }]
}
a.save('review.json',report)
# Nonempty, local evidence is mandatory for every check and every sample reference.
def validate_refs(obj):
 if isinstance(obj,dict):
  for k,v in obj.items():
   if k in ['evidence_paths','sample_refs']:
    for ref in v:
     p=a.EVID/ref;assert not pathlib.Path(ref).is_absolute() and p.is_file() and p.stat().st_size>0,ref
   else:validate_refs(v)
 elif isinstance(obj,list):
  for v in obj:validate_refs(v)
validate_refs(report);validate_refs(a.load(a.EVID/'pedagogical-variation.json'))
assert a.snap()==a.load(a.EVID/'package-before.json')
for n in ['render-counterfactual/rendering.json','render-other/rendering.json']:assert a.load(a.EVID/n)['passed']
assert a.load(a.EVID/'regression-shortcut-result.json')['defect_reproduced']
assert len(a.load(a.EVID/'affected-inventory.json')['affected_questions'])==3
(a.EVID/'session-state.md').write_text('COMPLETE: verdict revise in review.json. One demonstrated family-wide authored easy bank shortcut, strict runnable failing regression saved. Independent original-source analysis, eight full bank/prose replays, math checks, 37/148 native grader outcomes, eight rendered screenshots inspected, read-only delivery and learner-selection analysis, nine generated inventory replays with three affected records, exact dependency and relocation/rejection checks complete. Pedagogical schema and all relative nonempty evidence references verified. Package snapshot remains unchanged. No database or publishing operations.\n')
a.save('evidence-validation.json',{'pedagogical_variation_schema':'Validated with jsonschema against repo schema','all_relative_evidence_refs_nonempty':True,'package_unchanged':True,'strict_regression_defect_reproduced':True,'affected_stored_records':3,'verdict':'revise'})
print('Review finalized: revise; all eight checks have evidence; package unchanged.')

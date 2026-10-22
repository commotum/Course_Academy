"""Assemble the evidence contract after independent tests and visual inspection."""
import ast, hashlib, json, pathlib
E=pathlib.Path(__file__).resolve().parent
J=E.parent
W=J/'workspace'

def load(name):return json.load(open(E/name))
def save(name,x):(E/name).write_text(json.dumps(x,indent=2)+'\n')

native=load('grader-report-final.json')
assert native['accepted_checks']==120 and native['rejected_checks']==480
assert native['documented_unresolved_checks']==0 and native['database_writes']==0
before=load('package-before.json')
after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
assert before==after
save('package-integrity.json',dict(unchanged=True,files_checked=len(before),before=before,after=after))
preflight=json.load(open(J/'repair-preflight.json'))
assert hashlib.sha256((W/'check_restriction.py').read_bytes()).hexdigest()==preflight['checks'][0]['sha256']

inspections=[]
for folder in ['render','render-tail','render-repaired']:
    report=load(folder+'/rendering.json');assert report['passed']
    inspections.append(dict(folder=folder,cases=len(report['cases']),
        screenshots=[str(pathlib.Path(folder)/f'question-{i+1:03}.png') for i in range(len(report['cases']))],
        inspected=True,result='Legible dimensions, pivot/non-pivot emphasis, five distinct radio controls, selected key and worked rank equations. No clipping, TeX errors or broken assets observed.'))
save('render-inspection.json',dict(actual_UI=True,manual_visual_inspection=inspections,
    exact_runner_batch='render-tail/question-002.png through question-006.png',
    counterfactuals='All seven initial controls and three repaired-boundary controls inspected on both sides.',
    limits='Preview displays completed correct responses; actual acceptance/rejection was tested separately through native grader.'))

counterfactuals=[
 dict(kind='relevant',change='At fixed Q, 10 rows and 12 columns, pivot count 5 -> 4.',
      expected='Rank 5 -> 4; prompt, solution and native choice acceptance change together.',
      observed='Both delivered prompts, solutions and independent native checks agree; rendered controls show rank 5 and rank 4.',
      status='passed',justification='Tutorial c062d466-946c-526b-aba8-0a0895671218 defines rank as pivot-column count.',
      sample_refs=['counterfactual-tests.json','grader-input-final.json','grader-report-final.json','render/input.json','render/rendering.json']),
 dict(kind='relevant',change='At fixed Q and 10 rows, non-pivots 3 -> 2 with eight columns; separately columns 8 -> 9 with three non-pivots.',
      expected='Rank 5 -> 6 for either change; all dependent content and native outcomes must follow.',
      observed='Visible subtraction changes 8-3=5 to 8-2=6 or 9-3=6; all five responses graded per instance and all four controls rendered.',
      status='passed',justification='Canonical 7cce27e9-e2b2-599c-9f4e-437caf1a23ae teaches columns minus non-pivots.',
      sample_refs=['counterfactual-tests.json','grader-input-final.json','grader-report-final.json','render/input.json','render-tail/input.json']),
 dict(kind='irrelevant',change='Rename Q to T and change feasible rows 10 -> 11, holding column/count evidence fixed in each band.',
      expected='The numerical response remains 5; matrix letter and rows update in prompts/explanations.',
      observed='Both pairs preserve rank 5 through delivery, UI and actual learner grading despite changed field/choice IDs.',
      status='passed',justification='Rank from supplied column counts is independent of name and feasible row count (same tutorial and canonical example).',
      sample_refs=['counterfactual-tests.json','grader-input-final.json','grader-report-final.json','render/input.json']),
 dict(kind='irrelevant',change='q-79409 profile: change only rows 5 -> 4 at Q, columns 7, non-pivots 3, seed 517319.',
      expected='Both are feasible and rank stays 4 at full-row-rank boundary.',
      observed='Both generate, survive delivery and render; native grader accepts only rank 4. Captured old runtime fails the exact retained boundary tests.',
      status='passed',justification='Canonical example itself has rows=rank=4; rows=rank must not be excluded by distractor collisions.',
      sample_refs=['repaired-control-records.json','delivery-repaired-controls/accepted.json','counterfactual-tests.json','regression-tests.json','grader-report-final.json','render-repaired/input.json']),
 dict(kind='relevant',change='q-79409 at Q, rows 5, columns 7: non-pivots 3 -> 2, same seed 517319.',
      expected='Rank changes 4 -> 5 while workload stays one subtraction, including source-style/collision-completed banks.',
      observed='Delivered prompt, solution and rendered answer change to 7-2=5; all correct and incorrect UUID responses tested.',
      status='passed',justification='Same subtraction rule in source 186b4c12-6daf-5415-8147-526533c01a95; qualifying numeric answer is incidental.',
      sample_refs=['repaired-control-records.json','counterfactual-tests.json','grader-report-final.json','render-repaired/input.json'])]

variation=dict(
 learner_operation='Read whether the supplied count is pivot or non-pivot columns. Recall rank=pivots for easy, or compute total columns minus non-pivots for moderate, then select the matching integer.',
 fixed_features=[
  dict(feature='Target is matrix rank, with no explicit matrix or row reduction.',justification='All eleven source questions give counts; neighboring inspection/reduction knowledge points are separate lesson steps.'),
  dict(feature='Easy gives pivots; moderate gives non-pivots.',justification='The source difficulty labels separate direct definition recall from one subtraction.'),
  dict(feature='Five numeric radio options, one correct.',justification='All eleven full source fields use this response shape. Single correctness follows the unique rank; it is not an incidental count to randomize.'),
  dict(feature='Positive ranks 1..12 and dimensions 3..15 in the finite runtime.',justification='Conservative authored small-integer scope around positive source counts. Zero-rank and zero-nonpivot boundaries are permissible future same-method extensions but not necessary to establish variation in this declared positive family.')],
 answer_roles=[
  dict(role='Correct rank integer',eligible_variation='Change pivot count for easy, or columns/non-pivot pair for moderate within feasibility.',observed='All 12 declared easy ranks and 98 feasible moderate pairs occur and survive shared filtering. Exact batch has ranks 10,2,11,1,8.'),
  dict(role='Correct option identity, numeric order and displayed position',eligible_variation='Distinct banks and choice order may change independently of correctness.',observed='Within-profile fresh samples vary numerical orders; actual UI reorders choices. Exact batch displayed positions are 5,2,4,5,1, including 4,5,1 within its three q-34805 members.'),
  dict(role='Matrix dimensions/name',eligible_variation='Names and feasible rows are irrelevant to response; moderate total columns are relevant.',observed='Paired relevant and irrelevant tests change prompt and explanation consistently; full-row-rank boundary no longer blocks generation.')],
 coverage=[
  dict(case='All original question banks and canonical parameters',sample_refs=['source-replay-tests.json','source-replay-records.json','restriction-records.json'],result='Eleven complete banks reproduced. Canonical 4x7, three non-pivots now accepted in all six moderate profiles. Missing q-34825 key/solution and canonical answer field remain explicitly distinguished from reconstructed content.'),
  dict(case='Previously omitted collision and full-row-rank cases',sample_refs=['restriction.json','restriction-records.json','regression-tests.json','preflight-current/root-cause/restriction.json'],result='Independent seed 28907 accepts all eight targeted moderate parameter triples across six profiles; minimum/maximum easy counts also exercised. Retained strict checks fail bound old code and pass current.'),
  dict(case='Finite capacities and delivery domain',sample_refs=['cli-easy-12.json','cli-moderate-98.json','delivery-variation-tests.json'],result='12 easy and 98 moderate tasks survive filtering against basis 5404. Redundant profile samples deduplicate without losing their mathematical decision cases; source bank profiles are not separate skills.'),
  dict(case='Exact requested five',sample_refs=['runner-batch.json','delivery-runner-batch/accepted.json','render-order-tests.json','shortcut-tests.json'],result='All five survive, have different semantic pivot counts, and no fixed tested numeric order or actual displayed position answers the entire batch.'),
  dict(case='Apparent conditional predictor',sample_refs=['shortcut-tests.json','delivery-cli-moderate-98/accepted.json'],result='Choose-smallest answered 3/3 wide moderate items in a small subgroup, but only 8/49 delivered wide control items. Counterexample: 9x10, five non-pivots, bank 5,4,9,0,7; rank is 5, not smallest 0.')],
 counterfactuals=counterfactuals,
 shortcut_probes=load('shortcut-tests.json')['probes'],
 delivery=dict(stages_examined=['Mathematical feasibility independent of distractor collision',
      'Finite semantic-task selection without replacement; explicit capacity errors',
      'Bounded 16-sign bank enumeration and valid five-choice construction',
      'Shared requested-difficulty, normalization, identities, inventory and batch deduplication',
      'Captured usable inventory and learner-history exclusion under conditional selector scenarios',
      'Difficulty-weighted and unconfigured selection branches',
      'Actual UI choice order confirmed from rendered HTML'],
     sample_refs=['regression-tests.json','delivery-variation-tests.json','delivery-runner-batch/delivery.json','selection-tests.json','inventory-tests.json','render-order-tests.json'],
     result='All exact batch records and full finite task controls survive actual read-only preparation. Configured positive easy weights reach all five fresh members, or four after excluding one as seen; no-policy branch chooses the earliest entity and reaches none in these scenarios. No answer-based selector filter. Publication is absent; preparation was reproduced read-only.'),
 limitations=['Finite review cannot rule out every possible shortcut.',
     'Current inventory capture is basis 5404. Future inventory, learner histories, actual future task-item IDs and active weight policy are not supplied; conditional reachability is not a claim about a particular learner.',
     'Retained historical v1 q-79405 generated item still has the earlier ordering weakness. It is independently reproduced in affected-inventory.json; no current-v2 rule reproduces that invariant. Source originals were excluded from generated provenance claims.',
     'Only positive-rank finite scope is certified; zero rank, non-pivot count zero and unsupported hard difficulty are not claimed.',
     'A profile with one or two survivors cannot establish or refute a universal predictor on its own; raw bank order is not UI position.'])
save('pedagogical-variation.json',variation)

sa=load('source-analysis.json')
source_analysis={k:sa[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs']}
source_analysis['evidence_paths']=['source-analysis.json','provenance.json']
def check(paths,details):return dict(status='passed',evidence_paths=paths,details=details)
checks=dict(
 source_replay=check(['source-replay-tests.json','source-replay-records.json','restriction.json'],
   'All 11 complete banks replay; canonical mathematical case now admitted. Missing source fields and documented dimensional-notation correction are explicit.'),
 math=check(['math-tests.json','restriction-records.json','cli-moderate-98.json','counterfactual-tests.json'],
   '265 records checked from visible prompts using integer arithmetic: feasible rank, five distinct nonnegative choices, matching key and solution.'),
 variety=check(['restriction.json','regression-tests.json','delivery-variation-tests.json','shortcut-tests.json'],
   'Collision restrictions resolved across profiles; 12 easy ranks and 98 moderate tasks survive delivery. Fresh profile and exact-batch shortcut probes retained.'),
 scope=check(['source-analysis.json','independent-records.json','counterfactual-tests.json'],
   'Easy definition recall and moderate one subtraction preserve source workload and five-option response; no added row-reduction task.'),
 grading=check(['grader-input-final.json','grader-report-final.json'],
   'Actual native grader accepted 120 correct and rejected 480 wrong choice UUIDs, including all five responses on both sides of controlled pairs. No free-entry fields.'),
 rendering=check(['render/rendering.json','render-tail/rendering.json','render-repaired/rendering.json','render-inspection.json','render-order-tests.json'],
   '17 actual UI screenshots inspected, including every exact batch record, relevant/irrelevant pairs and repaired examples; HTML choice orders verified.'),
 packaging=check(['packaging.json','regression-tests.json','retained-results/validation.json','package-integrity.json'],
   'Exact Python 3.13.5/SymPy 1.14.0 match dependencies. Deterministic relocated runtime, runner envelope, capacities and invalid cases pass. Current preflight also fails the bound old runtime. Package unchanged.'),
 decision_variation=check(['pedagogical-variation.json','counterfactual-tests.json','shortcut-tests.json','delivery-variation-tests.json','selection-tests.json','affected-inventory.json'],
   'Eligible rank/count, bank and position roles vary. Relevant evidence changes decisions; feasible irrelevant changes preserve them through grading and rendering. Exact five-member pool checked separately; historical inventory weakness is recorded separately from current generator behavior.'))
result=dict(verdict='accepted',summary='The retained restriction is fixed. All eight checks pass for the current package and exact five-question batch. Package unchanged; one previously affected historical inventory item is documented separately.',source_analysis=source_analysis,checks=checks,findings=[])
save('result.json',result);save('review-result.json',result)
for name in ['audit.py','regression-driver.py','finish-tests.py','variation-tests.py','finalize-review.py']:
    ast.parse((E/name).read_text())
(E/'session-state.md').write_text('Review complete: accepted current package and exact five-question batch. '
    'All eight checks have saved evidence. 265 independent math records; native 120 accepted/480 rejected; '
    '17 UI screenshots inspected. Retained strict regression and preflight fail bound old runtime and pass current. '
    'Historical affected inventory record preserved in affected-inventory.json. Package hashes unchanged. '
    'result.json and review-result.json contain final structured report.\n')
print(json.dumps(dict(verdict=result['verdict'],checks={k:v['status'] for k,v in checks.items()},package_unchanged=True)))

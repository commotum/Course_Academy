import json,pathlib,sys
import audit as A
P=A.HERE
load=A.load
samples=load(P/'samples.json');easy=load(P/'easy-samples.json')
shortcut=load(P/'shortcut-results.json');delivery=load(P/'delivery-selection-results.json')
render=load(P/'render/rendering.json');grading=load(P/'grader-report.json')
assert render['passed'] and len(render['cases'])==6
assert len(grading['records'])==44 and grading['accepted_checks']==71 and grading['rejected_checks']==176
assert A.snapshot()==load(P/'package-before.json')
ref=['samples.json','shortcut-results.json']
probes=[]
for p in shortcut['probes']:
 probes.append({'cue':'Unique exponential whose doubled exponent also appears among the other choices',
  'subgroup':p['subgroup'],'scope':'within_template' if p['subgroup'] in ['constant_cos','scaled_constant_power','signed_constant_power'] else 'overall',
  'strategy':'Ignore the ODE. Choose e^h when e^(2h) is also offered.',
  'correct':p['correct'],'total':p['total'],'baseline':0.2,'disposition':'defect',
  'conclusion':'Uniform random choice among five options succeeds at rate 0.2; this answer-bank-only rule succeeds on every tested item in the subgroup. The code fixes this relationship for every nonzero easy coefficient. This bypasses identifying P and computing its integrating factor.',
  'sample_refs':['runner-batch.json','shortcut-results.json'] if p['subgroup']=='runner batch' else ref})
coverage=[]
for t in ['constant_cos','scaled_constant_power','signed_constant_power']:
 rows=[r for r in easy if r['generation']['template']==t]
 coverage.append({'case':t+'; both coefficient signs, shifted positions and small source-level values',
  'sample_refs':['samples.json','math-results.json','shortcut-results.json'],
  'result':f'{len(rows)} independently seeded examples; keys are mathematically correct but the same exponent-doubling bank cue predicts all of them.'})
coverage.extend([
 {'case':'Canonical constant P with exponential forcing','sample_refs':['canonical-candidates.json','canonical-coverage-results.json'],
  'result':'Canonical y\u2032+2y=2e^(-2x) is unreachable; all 12 reachable easy Q choices at P=2 fail to reproduce it. Nonconstant-P templates cannot supply it.'},
 {'case':'Observed source answer banks','sample_refs':['source-replay-records.json','source-replay-results.json','source-designation-results.json'],
  'result':'All 8 practice banks replayed, all 40 choices matched, 6 captured designations agree; 2 missing source keys inferred independently. Malformed raw dx^2 choice treated only as an observed shape.'}])
ped={
 'learner_operation':load(P/'source-analysis.json')['learner_operation'],
 'fixed_features':[
  {'feature':'Transform the ODE only as far as d(yI)/dx=IQ','justification':'Canonical example e-21741 and all eight practice prompts stop at this stage; solving y would add work from the next knowledge point.'},
  {'feature':'Single radio field containing five complete equations','justification':'All eight captured practice banks use this response contract. The number of correct selections is fixed by the single-choice task.'},
  {'feature':'Elementary P with nonzero normalization coefficient on the domain','justification':'The source requires constant, linear or reciprocal integration and the product rule. Restricting to a valid interval makes division/logarithms legitimate.'}],
 'answer_roles':[
  {'role':'Integrating factor coefficient/sign and correct choice position','eligible_variation':'Small positive/negative constants, fractions and powers, with the correct factor following P; permute answer positions.','observed':'Both signs, fractional coefficients and varied positions appear. Controlled +1 to -1 changes I from exp(x) to exp(-x).'},
  {'role':'Which recognizable bank relationship is assigned to the correct factor','eligible_variation':'Do not always make the correct factor the uniquely identifiable smaller member of an exponent-doubling pair. Use valid full banks whose superficial roles do not specify the key.','observed':'All easy templates fix [I,1/I,I^2,x,x^2]. Thus the correct I is recoverable from the bank alone for every nonzero allowed coefficient.'},
  {'role':'Forcing Q at fixed constant P','eligible_variation':'Source canonical permits Q=2exp(-2x); constant-P cosine and polynomial forcings are also observed, with no need to integrate QI.','observed':'Easy templates support only Q=cos(bx) or x^n. The canonical exponential-forcing assignment is missing.'}],
 'coverage':coverage,
 'counterfactuals':[
  {'kind':'relevant','change':'Hold signed_constant_power, n=2 and seed=8173 fixed; change a from +1 to -1.',
   'expected':'Prompt coefficient, solution P, integrating factor and correct transformed equation must change together; exp(x) becomes exp(-x).',
   'observed':'Printed equations and all three worked equation rows agree with each new prompt. Native grader accepts each new key and rejects the opposite-sign factor. UI screenshots show the changed signs and correct complete equations.',
   'status':'passed','justification':'P changes the defining condition I\u2032=PI (tutorial a7f8aa2e-e022-57eb-be82-5f539a4512f6).',
   'sample_refs':['counterfactual-records.json','counterfactual-results.json','counterfactual-integration-results.json','grader-input.json','grader-report.json','render/rendering.json']},
  {'kind':'irrelevant','change':'Keep a=1,n=2 and every mathematical datum fixed; change only shuffle seed from 8173 to 8174.',
   'expected':'The complete correct equation, its owned choice UUID, prompt and worked solution remain identical, while choice order changes.',
   'observed':'Those fields are equal; the ordering differs. Native grader accepts the same key. Rendered first and third previews display the same mathematical task with different choice positions.',
   'status':'passed','justification':'Answer order has no role in the lesson\u2019s product-rule identity. No substantive ODE datum is wholly irrelevant to the complete transformed equation.',
   'sample_refs':['counterfactual-records.json','counterfactual-integration-results.json','grader-report.json','render/rendering.json']}],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['Generator rejection/resampling','Requested easy difficulty','Actual publisher validation and normalization','Inventory and within-batch deduplication at captured basis 5319','Read-only reproduction of learner band/within-band selection and seen-question exclusion'],
  'sample_refs':['easy-samples.json','runner-batch.json','delivery-samples/accepted.json','delivery-samples/delivery.json','delivery-batch/accepted.json','delivery-batch/delivery.json','delivery-selection-results.json','generated-records.json'],
  'result':'Fresh easy samples: 24/24 survive, all predictable, one construction attempt each. Runner batch: 5 becomes 4 after one duplicate, all survivors predictable. All three affected stored easy instances are selectable under applicable easy-band/history scenarios. Original sources also remain in the current pool, so the entire pool is not claimed uniformly predictable.'},
 'limitations':['Finite tests cannot prove absence of other shortcuts; demonstrated rule applies structurally to all default easy banks.',
  'Policy weights and learner history are not captured. Selection was examined under explicit scenarios using real captured entity IDs, not asserted as a live learner trace.',
  'Inventory conclusions use basis 5319; later inventory can differ. No publication preparation exists, so check_delivery reproduced filtering read-only.',
  'Fresh focus is requested easy; moderate/hard have a small math regression sample, not a comprehensive shortcut audit.',
  'Canonical source has no captured answer field; missing practice keys/solutions and the malformed raw derivative are identified in source-analysis.json.']}
A.save('pedagogical-variation.json',ped)
A.save('render-inspection.json',{'report':'render/rendering.json','passed':True,'inspected_screenshots':[f'render/question-{i:03d}.png' for i in range(1,7)],
 'observations':['Read all six actual-UI screenshots. Prompt equations, five radio options, inline/display math and complete worked solutions are legible; no exposed TeX or clipped equation was seen.',
 'First/second previews show relevant sign change; first/third show irrelevant answer reordering with preserved full answer.',
 'Inline cosine, derivative normalization on x>0 and reciprocal/logarithmic factor choices render correctly.'],
 'limits':'Renderer default limit is six; the seventh input record linear_sin was not rendered and is not claimed inspected.'})
A.save('scope-results.json',{'requested_difficulty':'easy','passed':True,
 'source_refs':['1e3c0253-226d-596c-a831-7c68ec76b21c','65a9092a-d6a6-5192-82ca-c04151a6438f','dba525fe-7e4d-5319-88bd-1b806feb0904','tutorial a6a381ed-e9ab-5deb-9d74-30900610edf1 Steps 1-4'],
 'evidence':['All 24 easy samples require identifying constant P, integrating it, and recognizing the product derivative. Eight require one division by x on an explicit positive interval.',
 'Positive/negative integer and rational coefficients, n=1 and n=4, and trig frequencies 1 and 4 occur in the independent samples. They do not require integrating IQ, finding y, or imposing an initial condition.',
 'Each item has one radio selection and five complete equations. Shortcut and missing canonical coverage are separate failures, not prerequisite/workload drift.'],
 'limits':'Pass concerns requested easy output; the broader moderate/hard sampler received limited math regression checks.'})
sa=load(P/'source-analysis.json')
check=lambda status,paths,details:{'status':status,'evidence_paths':paths,'details':details}
result={'verdict':'revise',
 'summary':'Two demonstrated defects: every default easy bank reveals its correct factor without the ODE, and the canonical exponential-forcing source case is unreachable. Three stored generated easy questions are affected. Package unchanged; no database writes.',
 'source_analysis':{k:sa[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
 'checks':{
  'source_replay':check('failed',['source-analysis.json','source-replay-records.json','source-replay-results.json','source-designation-results.json','canonical-coverage-results.json','canonical-candidates.json'],
    'Eight practice banks and all 40 choices replay; six captured keys agree, two absent keys inferred. Canonical e-21741 has no reachable construction. Source sign/domain corrections are documented.'),
  'math':check('passed',['math-results.json','samples.json','counterfactual-records.json','runner-batch.json'],
    'Independent parsing/expansion verified unique correct choices and all three printed multiplication/final equation rows for 44 records. Includes signs, rational coefficients and easy boundaries; this does not certify variety.'),
  'variety':check('failed',['samples.json','shortcut-results.json','canonical-coverage-results.json','delivery-selection-results.json'],
    'Values, signs and positions vary, but every easy bank fixes the correct factor in the same recognizable doubled-exponent role. Constant-P exponential forcing from the canonical source is suppressed.'),
  'scope':check('passed',['scope-results.json','source-analysis.json','samples.json'],
    'Requested easy output preserves the source integration/product-rule stages and radio workload; no final solution or initial-value work is added.'),
  'grading':check('passed',['grader-input.json','grader-report.json','math-results.json','counterfactual-integration-results.json'],
    'Actual native grade_field: 71 accepted checks and 176 rejected checks on 44 records, including all five choices and shortcut-selected answers. Radio has no free-entry equivalence requirement.'),
  'rendering':check('passed',['render-input.json','render/rendering.json','render-inspection.json','render/question-001.png','render/question-002.png','render/question-003.png','render/question-004.png','render/question-005.png','render/question-006.png'],
    'Six actual-UI previews passed renderer checks and visual inspection, including controlled sign/permutation pairs and representative inline, scaled and reciprocal equations.'),
  'packaging':check('passed',['package-before.json','packaging-results.json','original-cli.json','relocated-cli.json','audit.py','pipeline_audit.py'],
    'Exact Python 3.13.5 and SymPy 1.14.0 match nested manifest dependencies. Determinism, invalid-input rejection, relocation and stdout output verified. Package content hashes remain unchanged.'),
  'decision_variation':check('failed',['pedagogical-variation.json','minimal-failing-records.json','minimal-failure-results.json','shortcut-results.json','delivery-selection-results.json','affected-inventory.json','generated-records.json'],
    'Bank-only rule succeeds 24/24 fresh easy cases, 8/8 within each easy template, 5/5 runner inputs and 4/4 post-filter records. Relevant and irrelevant counterfactuals work, but they preserve the incidental bank-to-key relationship. Three stored easy instances reproduce this weakness.')},
 'findings':[
  {'kind':'decision_shortcut','description':'All easy templates use factors [I,1/I,I^2,x,x^2]. The correct option is uniquely the exponential whose doubled exponent appears elsewhere. The learner can ignore the ODE. Shuffling choices and varying signs/fractions do not break this rule.',
   'source_refs':['dba525fe-7e4d-5319-88bd-1b806feb0904','65a9092a-d6a6-5192-82ca-c04151a6438f','c7fefc62-82f5-5578-9142-a780040dc0af','tutorial a7f8aa2e-e022-57eb-be82-5f539a4512f6: I\u2032=IP'],
   'reproduction':'Run /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_failures.py (expected exit 1). Minimal case: generate("easy", seed=8173, template="signed_constant_power", parameters={"a":"1","n":2}). Prompt y\u2032+y=x^2; factors exp(x),exp(-x),exp(2x),x,x^2. The bank alone identifies exp(x). Opposite-sign paired case also succeeds. See minimal-failing-records.json and native grader-report.json. affected-inventory.json lists 3 reproduced stored instances.',
   'requested_change':'Change the complete-bank construction rule shared by all three easy templates so superficial exponent relationships do not identify the key independently of P. Preserve legitimate coefficient signs/fractions, the source skill, five complete choices and unique correctness; retain conditional shortcut and native-grader regression tests.'},
  {'kind':'source_fidelity','description':'Canonical source e-21741, y\u2032+2y=2exp(-2x), is not reproducible. All constant-P templates force Q to cos(bx) or x^n. The only exponential-forcing templates require nonconstant P, so they cannot reproduce the canonical task.',
   'source_refs':['1e3c0253-226d-596c-a831-7c68ec76b21c','tutorial a6a381ed-e9ab-5deb-9d74-30900610edf1 Steps 1-4'],
   'reproduction':'Run /home/jake/Developer/Course_Academy/.venv/bin/python canonical_coverage.py (expected exit 1). It records all 12 reachable easy Q assignments at P=2; none matches the canonical equation. See canonical-candidates.json and canonical-coverage-results.json. Other supported templates have nonconstant P.',
   'requested_change':'Support and replay the canonical constant-coefficient exponential-forcing family through the normal construction path, deriving I, IQ, choices and the source solution stages together. Allow source-supported variation without adding a final ODE-solving step.'}]}
A.save('result.json',result)
A.save('commands.json',{'working_directory':str(P),'commands':[
 f'{sys.executable} audit.py',
 f'{sys.executable} {A.REPO}/generate/pipeline/check_delivery.py --input easy-samples.json --source {A.JOB}/source/source.json --inventory {A.JOB}/source/inventory.json --difficulty easy --output delivery-samples --math-root /media/jake/SSD/EDB/math',
 f'{sys.executable} {A.REPO}/generate/pipeline/check_delivery.py --input runner-batch.json --source {A.JOB}/source/source.json --inventory {A.JOB}/source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math',
 f'{A.REPO}/generate/runs/current/check-engine grader-input.json grader-report.json',
 f'{sys.executable} {A.REPO}/generate/pipeline/render_preview.py --input render-input.json --output render --limit 6 --math-root /media/jake/SSD/EDB/math',
 f'{sys.executable} pipeline_audit.py',f'{sys.executable} reproduce_failures.py  # expected exit 1',
 f'{sys.executable} canonical_coverage.py  # expected exit 1',f'{sys.executable} finalize_report.py'],
 'note':'run-review.sh is a reproducible sequence ending at the intentional shortcut regression failure; canonical coverage can be rerun separately. Reviewer parser fixes were completed before final successful audit.py run; early logs were overwritten with final results. No author validation was substituted for independent tests.'})
(P/'session-state.md').write_text('Review complete: revise. Two demonstrated defects: default easy bank shortcut and unreachable canonical exponential-forcing case. Independent source account saved before author inspection. All eight checks assessed in result.json. Native grader 71 accepted/176 rejected; 44 independently checked records; 6 UI screenshots visually inspected. Three affected stored easy instances reproduced with complete matching records in generated-records.json; affected-inventory.json is populated. Shared delivery and selection scenarios saved. Strict regression commands intentionally exit 1. All package content hashes unchanged; no database writes.\n')
print(json.dumps({'verdict':result['verdict'],'checks':{k:v['status'] for k,v in result['checks'].items()},'findings':len(result['findings']),'package_unchanged':True}))

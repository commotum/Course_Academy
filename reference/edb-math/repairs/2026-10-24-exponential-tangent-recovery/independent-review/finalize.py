"""Bind the completed independent checks and emit the validated review contract."""
from collections import Counter
import hashlib
import json
import re
import shutil
import sys
import review as a
import decision as d
import visible_math as v
from generator_review import validate_review

frozen=a.load(a.R/'evidence/frozen-candidate.json')
assert a.package_hash()==frozen['package_hash']
engine_files={str(p.relative_to(a.REPO)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in [*sorted((a.REPO/'engine/rust').rglob('*.rs')),
                        a.REPO/'generate/runs/current/check-engine']}
assert engine_files==a.load(a.E/'engine-files.json'), 'Engine changed during review; rerun affected checks'
binding={'policy_version':4,'package_hash':a.package_hash(),
         'batch_hash':a.digest(a.load(a.E/'requested.json')),
         'source_hash':a.digest(a.load(a.R/'fresh-source/source.json')),
         'inventory_hash':a.digest(a.load(a.R/'fresh-source/inventory.json')),
         'assets':{},'effective_difficulty':'hard','engine_hash':a.digest(engine_files)}
assert all(binding[k]==frozen[k] for k in ['package_hash','batch_hash','source_hash','inventory_hash'])

delivery={}
for name in ['requested','fresh']:
    original=a.load(a.E/(name+'.json'))
    accepted=a.load(a.E/('delivery-'+name)/'accepted.json')
    assert len(original)==len(accepted)
    assert [a.visible(r) for r in original]==[a.visible(r) for r in accepted]
    delivery[name]={'report':a.load(a.E/('delivery-'+name)/'delivery.json'),
                    'post_filter_visible_math':d.inspect(accepted)}
delivery['learner_selection']={
    'source':'engine/rust/question_selection.rs select and seen_before_task',
    'examined_rules':'Fresh/usable candidates supplied upstream; deduplicate entities, select a nonempty positive-weight difficulty band then uniform index within it using stable SHA256 draws. No mathematics/sign/bank-role balancing. Legacy unconfigured policies select first entity.',
    'limits':'Read-only captured inventory6469, no live history/policy snapshot or prediction of exact learner draw. Structural no-singleton-sign and no-repeated-slope guards survive any selection of these records. Exchangeability proof is for normal generator output, not arbitrary history-conditioned subsets.'}
a.save('delivery-analysis.json',delivery)

fmt=a.module('render_math_format',a.REPO/'scripts/question_capture/math_format.py')
render=a.load(a.E/'render/rendering.json'); records=a.load(a.E/'render-records.json')
assert render['passed'] and len(render['cases'])==3
render_rows=[]
for i,record in enumerate(records):
    solution=record['question'][':question/worked-solution']
    html=(a.E/f'render/question-{i+1:03}.html').read_text()
    expected_rows=sum(len(re.split(r'\\\\',block)) for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S))
    expected_math=sum(len(list(fmt.MATH.finditer(record['question'][field])))
                      for field in [':question/problem',':question/worked-solution'])+len(v.choices(record))+1
    actual_rows=html.count('data-mml-node="mtr"')
    assert expected_rows==actual_rows and expected_math==render['cases'][i]['mathContainers']
    render_rows.append({'index':i,'expected_rows':expected_rows,'actual_rows':actual_rows,
                        'expected_math_containers':expected_math,'actual_math_containers':render['cases'][i]['mathContainers']})
a.save('render-boundary-results.json',{'passed':True,'cases':render_rows,
    'visually_inspected':['render/question-001.png','render/question-002.png','render/question-003.png'],
    'observations':'Independently viewed all three screenshots: requested negative-slope base4 case, source-parameter fractional tangent with original solution, and explicit unit coefficient at point0. All five options and complete chain-rule/evaluation/point-slope solutions are visible and contained; no clipped rows, raw TeX or missing equations.'})

# Inspect the actual portable guard and rerun its affected assertions, retaining
# the original and newly found failing fixtures. The full CLI/delivery invocation
# is already separately evidenced; the independent CLI/delivery checks above use
# the same frozen request and an additional fresh sample.
guard_root=a.R/'workspace-regressions'
guard=a.module('reviewed_portable_regression',guard_root/'check_tangent_regression.py')
old_negative=a.load(guard_root/'tangent-negative.json')
assert guard.probe.probes(old_negative)['correct']==len(old_negative)==4
try:
    guard.inspect([a.load(guard_root/'sign-negative.json')])
except AssertionError as error:
    assert 'singleton slope sign' in str(error)
else:
    raise AssertionError('Retained sign negative incorrectly passes')
guard.inspect(a.load(a.E/'requested.json'))
reg=a.E/'regression-review';reg.mkdir(exist_ok=True)
for file in ['check_tangent_regression.py','tangent_probe.py','tangent-negative.json','sign-negative.json','repair-regressions.json']:
    shutil.copyfile(guard_root/file,reg/file)
mapping=a.load(reg/'repair-regressions.json')
assert mapping=={'findings':[{'id':'65f96ea95438cd2c7b13','script':'check_tangent_regression.py','args':[]}]}
shutil.copyfile(a.R/'evidence/portable-regression/regression.json',reg/'author-full-run.json')
assert a.load(reg/'author-full-run.json')['passed']
a.save('regression-mapping-review.json',{'passed':True,'finding_id':'65f96ea95438cd2c7b13',
    'script_sha256':hashlib.sha256((reg/'check_tangent_regression.py').read_bytes()).hexdigest(),
    'assessment':'Mapping matches the retained concrete decision_shortcut finding in repair-history. Original bank-only failing records remain and reproduce4/4; the later singleton-sign counterexample must fail the actual sign guard. Prospective checks use current CLI and actual delivery, inspect visible mathematics, all five alternate supported curves, sign2/3 and normal unit/nonunit key coverage. The original source was separately guarded-repaired, not retired or waived.',
    'limits':'This is scoped to the exponential tangent family and observed defects; it is not approval of a universal bank rule or a waiver of original-source protections.'})

decision=a.load(a.E/'decision-results.json')
normal=[row for name in ['requested','fresh','author-fresh'] for row in decision['sets'][name]['cases']]
all_rows=[row for report in decision['sets'].values() for row in report['cases']]
probes=[{'cue':'Old repeated-coefficient/majority-sign/positive-constant rule',
    'subgroup':'All tested normal and controlled hard tangent banks','scope':'within_template',
    'strategy':'Use only bank slope repetition, majority sign and rational constant sign; abstain when no unique candidate exists.',
    'correct':0,'total':len(all_rows),'baseline':0.2,'disposition':'not_predictive',
    'conclusion':'No repeated slopes remain; retained original negative still succeeds4/4.',
    'sample_refs':['decision-results.json','original-negative-records.json']},
   {'cue':'Sole slope with monotonicity sign inferred from the displayed exponent coefficient',
    'subgroup':'Normal hard output and explicit boundary controls','scope':'within_template',
    'strategy':'Infer increasing/decreasing from the positive base and exponent coefficient, then select only if one line has that sign.',
    'correct':0,'total':len(all_rows),'baseline':0.2,'disposition':'not_predictive',
    'conclusion':'Every bank has2or3choices of each sign, leaving at least two candidates. The rejected seed2 fixture selects the key by this rule and is retained.',
    'sample_refs':['decision-results.json','sign-only-fresh-counterexample.json','exchangeability.json']},
   {'cue':'Always choose the numerically smallest slope',
    'subgroup':'Normal CLI samples only','scope':'overall','strategy':'Order the visible x coefficients and choose the smallest; ignore the curve.',
    'correct':sum(row['rank']==0 for row in normal),'total':len(normal),'baseline':0.2,
    'disposition':'not_predictive','conclusion':'Observed keys occupy every rank; exact complete-bank conditioning gives each member probability1/5 in normal sampling.',
    'sample_refs':['decision-results.json','exchangeability.json']}]
for point in ['-1','0','1']:
    rows=[row for row in normal if row['point']==point]
    assert rows
    probes.append({'cue':'Fixed smallest-slope bank role within a visible point subgroup',
        'subgroup':'x='+point,'scope':'other_recognizable_subgroup',
        'strategy':'At this displayed point choose the smallest x coefficient without differentiating.',
        'correct':sum(row['rank']==0 for row in rows),'total':len(rows),'baseline':0.2,
        'disposition':'not_predictive','conclusion':'The finite proof conditions on point and evaluated exponent, so the same1/5 bank-key result applies within this group; finite observed counts are not a claim of exact empirical balance.',
        'sample_refs':['decision-results.json','exchangeability.json']})
a.save('pedagogical-variation.json',{
 'learner_operation':'Differentiate the general-base composite exponential, evaluate its tangent slope and ordinate, and match the resulting point-slope equation.',
 'fixed_features':[{'feature':'Hard linear exponent and five tangent equations','justification':'Directly supported by source q107463; changing coefficient, point and base preserves response scope.'},
                   {'feature':'Every candidate passes through the same target point','justification':'Matches repaired original bank. Point membership cannot select the key; the tangent slope remains necessary. This bank does not independently diagnose ordinate-evaluation errors.'}],
 'answer_roles':[{'role':'Slope sign, rank and answer position','eligible_variation':'Both signs, all five slope ranks and positions','observed':'All occur in normal requested/fresh output; every bank keeps at least two slopes of either sign.'},
                 {'role':'Unit and nonunit inner derivative','eligible_variation':'All guarded coefficients±1..±9','observed':'Normal unit keys and nonunit keys with unit distractors both occur; the coefficient pool is key-independent. Canonical e728 directly supports unit inner differentiation.'}],
 'coverage':[{'case':'Exact requested4 and independent fresh8 plus author fresh24','result':'Correct visible mathematics, distinct complete banks, oldcueabsent, no singleton slope sign; requested/fresh delivery preserves content.','sample_refs':['requested.json','fresh.json','author-fresh.json','decision-results.json','delivery-analysis.json']},
             {'case':'All supported point/exponent coefficient groups','result':'14groups,25292accepted bank instances across groups; each eligible coefficient occurs and every accepted bank has five possible uniformly weighted keys under normal sampling.','sample_refs':['exchangeability.json']},
             {'case':'Actual same-bank changed-target controls','result':'Independently rebuilt15cases: requested bank, former sign-shortcut target and unit-coefficient target each support every bank option as a distinct correct tangent.','sample_refs':['same-bank-controls.json','same-bank-results.json']},
             {'case':'Stored original question','result':'Fresh6469 bank equals independently approved four-value repair, replays correctly, and no excluded-source descendants occur.','sample_refs':['source-audit.json','source-replays.json','source-replay-results.json']}],
 'counterfactuals':[{'kind':'relevant','change':'Change evaluation point or inner derivative sign; alternatively change the curve while holding a complete bank fixed.',
    'expected':'Target tangent and corresponding key change with the displayed mathematics.',
    'observed':'All controlled pairs and15same-bank rebuilds agree with independent differentiation.',
    'status':'passed','justification':'These are answer-bearing changes within the source method.',
    'sample_refs':['counterfactual-results.json','controlled.json','same-bank-results.json']},
   {'kind':'irrelevant','change':'Change random seed with fixed curve and point.',
    'expected':'Correct tangent remains mathematically unchanged while order/distractors may change.',
    'observed':'Controlled records0and5 have the same exact target and native accepted solution.',
    'status':'passed','justification':'Seed is not a mathematical input.',
    'sample_refs':['counterfactual-results.json','controlled.json','grader-results.json']}],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['normal parameter guard and whole-bank rejection','exact CLI request','actual preparation/deduplication against inventory6469','post-filter visible bank','question-selection code'],
             'sample_refs':['packaging-results.json','delivery-analysis.json','exchangeability.json'],
             'result':'All4requested and8independent fresh records survive with identical visible content; the author portable run separately confirms24fresh. Selector has no bank-aware transformation.'},
 'limitations':['This scoped review does not prove absence of every conceivable human shortcut.',
                'Normal sampling exchangeability does not claim uniform keys for an arbitrary externally fixed-parameter workload or an arbitrary history-conditioned inventory subset.',
                'Recognizing monotonicity can eliminate opposite-sign distractors, but never uniquely selects an option in normal banks.',
                'All options share the point, so this response primarily discriminates tangent slopes; the solution still teaches ordinate evaluation and point-slope construction.',
                'Original-source automatic-retirement protections remain intact; the separately authorized four-value repair was verified, not waived.']})

source_analysis=a.load(a.E/'source-analysis.json')
source_analysis={k:source_analysis[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']}
def check(paths,details):return {'status':'passed','evidence_paths':paths,'details':details}
result={'verdict':'accepted',
 'summary':'Accept frozen e2ca3955 exponential tangent repair against source/inventory6469 and the exact requested hard batch. The original repeated-slope cue, newly found singleton-sign case and unit-only coefficient pool are repaired with retained negative controls. All eight checks pass; no live state was changed by this review.',
 'source_analysis':source_analysis,
 'checks':{
  'source_replay':check(['source-analysis.json','source-audit.json','source-prompt-comparison.json','source-replays.json','source-replay-results.json','lower-band-parity.json'],'Replayed all14 source/canonical profiles and independently compared complete captured banks. Fresh source differs only in the approved four distractor values; current hard replay uses basis6468 and matches source6469. Unchanged lower-band behavior has explicit parity evidence.'),
  'math':check(['review.py','visible_math.py','math-results.json','decision-results.json','same-bank-results.json'],'33 core records checked by parsing visible math and independent differentiation, with every option checked. Additional24 fresh and15 same-bank controls independently verified; no ambiguous radio keys or duplicate equations.'),
  'variety':check(['fresh.json','controlled.json','decision-results.json','counterfactual-results.json','exchangeability.json'],'Both signs, all positions and ranks, bases and points vary. Relevant changes update the key; irrelevant seed changes preserve the target. Supported unit cases remain available with source justification.'),
  'decision_variation':check(['pedagogical-variation.json','decision.py','decision-results.json','exchangeability.json','same-bank-results.json','delivery-analysis.json','regression-mapping-review.json'],'Retained originalcue and singleton-sign negatives still fail. Current normal banks have five distinct slopes,2/3sign balance and key-independent coefficient eligibility. Independent finite conditioning proof plus actual same-bank counterfactuals support1/5 conditional keys for normal sampling; limits are explicit.'),
  'scope':check(['solution-paths.json','prior-evidence/scope-negative-control.json','source-analysis.json'],'Displayed chain-rule, evaluation and point-slope steps reach each keyed field. Source teaches required log-power rewrites; source coefficient-fragment field stays correctly scoped. Prior equivalent-but-unshown negative control is retained.'),
  'grading':check(['grader-input.json','grader-results.json','engine-files.json'],'Current native grade_field accepted33 correct submissions, rejected114 wrong submissions, and produced0unresolved outcomes; includes every tested radio option and independent equivalent/doubled blank answers.'),
  'rendering':check(['boundary-results.json','render-records.json','render/rendering.json','render-boundary-results.json','render/question-001.png','render/question-002.png','render/question-003.png'],'Rendered and visually inspected3affected records through unmodified learning UI. Every expected math container and aligned row is present; no raw TeX, missing equations or clipping.'),
  'packaging':check(['packaging-results.json','package-before.json','package-after.json','relocated-batch.json','reviewed-inputs.json'],'Only declared files/dependencies used. Relocated CLI exactly reproduces saved count4/seed1072510293 batch; invalid parameter boundaries reject. Package and engine remained unchanged through review; exact binding retained.')},
 'findings':[]}
a.save('reviewed-inputs.json',{'binding':binding,'source_basis':6469,'source_repair_basis':6468,
   'request':{'difficulty':'hard','count':4,'seed':1072510293},
   'engine_identity_method':'Exact Pipeline.engine_identity: digest(relative engine/rust/*.rs and check-engine executable raw SHA256 map).',
   'reviewer':'Independent agent tangent_independent_review; not the generator author',
   'prior_evidence_provenance':'source-audit.json records copied evidence hashes and bounded reuse rationale.'})
a.save('result.json',result)
validate_review(result,a.E)
a.save('evidence-contract.json',{'valid':True,'validator':'generator_review.validate_review','verdict':'accepted','binding':binding})
(a.E/'session-state.md').write_text('COMPLETE: accepted frozen packagee2ca3955, exact hard count4/seed1072510293 batch23ed303c, source/inventory6469. All8checks and validate_review passed. Native33accepted/114rejected/0unresolved; requested4+fresh8 survive real delivery;3actualUI renders inspected. Original and c70c counterexamples retained,15same-bank controls rebuilt, normal conditional-key proof verified. reviewed-inputs.json contains exact Pipeline.review_binding and engine file map. Review directory frozen after this report; no live job/database/package edits.\n')
print(json.dumps({'verdict':'accepted','binding':binding,'checks':list(result['checks'])},indent=2))

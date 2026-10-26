"""Record the targeted verifier decision against the checked final package."""
import copy
import json
from pathlib import Path
import shutil
import sys

D = Path(__file__).resolve().parent
R = next(p for p in D.parents if (p / 'scripts/generator_pipeline.py').is_file())
E = D / 'review'
sys.path.insert(0, str(R / 'scripts'))
from generator_pipeline import Pipeline, digest
from generator_review import validate_review, REVIEW_POLICY_VERSION
from inventory_jobs import save

read = lambda path: json.loads(Path(path).read_text())
state = read(D / 'job.json')
pipeline = Pipeline(D, state['request'], None)
pipeline.verify_approval_inputs()
binding = read(E / 'final-binding.json')
assert binding == pipeline.review_binding()
render = read(E / 'render/rendering.json')
assert render['passed'] and len(render['cases']) == 15
grading = read(E / 'grading-report.json')
assert grading['accepted_checks'] == 90 and grading['rejected_checks'] == 60
assert grading['documented_unresolved_checks'] == 0
sampler = read(D / 'sampler-regression.json')
assert sampler['passed'] and sampler['source_replay_unchanged']
shutil.copy2(D / 'sampler-regression.json', E / 'sampler-regression.json')

variation = read(E / 'prior/pedagogical-variation.json')
def retain_refs(value):
    if isinstance(value, dict):
        return {k: ['prior/' + ref for ref in v] if k == 'sample_refs' else retain_refs(v)
                for k, v in value.items()}
    if isinstance(value, list):
        return [retain_refs(v) for v in value]
    return value
variation = retain_refs(variation)
variation['coverage'].append({'case': 'Diversity within an ordinary short batch',
    'result': 'Reported four-question failure now has four coefficients. All 78 checked five/seven-question batches have distinct coefficients. All 15 final records and their delivery survivors retain distinct coefficients within each band.',
    'sample_refs': ['sampler-regression.json', 'independent-math.json', 'delivery-summary.json']})
variation['delivery'] = {
    'stages_examined': ['Least-used eligible coefficient, then compatible constant, without replacement',
                        'Final all-band samples through actual publisher filtering against captured inventory'],
    'result': 'All 15 final records survive; every five-question band contains five coefficients and all remainder signs. Original generated forms, fixed mathematical invariants and retained counterfactual checks are unchanged.',
    'sample_refs': ['final-records.json', 'delivery-summary.json', 'sampler-regression.json']}
variation['limitations'].append('Coefficient balancing is per generator call. It does not impose history-aware spacing across separately generated batches or rewrite existing learner tasks. Retained counterfactual/shortcut observations concern the unchanged construction; current sampler observations are separately recorded.')
save(E / 'pedagogical-variation.json', variation)

analysis = read(E / 'source-analysis.json')
analysis.pop('independent_judgment', None)
report = {'verdict': 'accepted', 'summary': 'Repaired local batch sampling to vary linear coefficients before constants. Final easy/moderate/hard samples pass independent mathematics, native grading, actual UI rendering and delivery checks. Question construction and source replay are unchanged.',
          'source_analysis': analysis, 'checks': {}, 'findings': [], 'band_verification': {}}
def check(name, refs, details):
    report['checks'][name] = {'status': 'passed', 'evidence_paths': refs, 'details': details}
check('source_replay', ['sampler-regression.json', 'prior/source-replay-checks.json'],
      'Current replay is unchanged from the independently reviewed source/exemplar replay. Current instructional source identity also matches that review. Imports were not edited.')
check('math', ['independent-math.json'],
      'Independently parsed visible polynomials, expanded every displayed derivation row, and checked both keyed fragments for all 15 final records.')
check('variety', ['sampler-regression.json', 'delivery-summary.json'],
      'The reported repeated-coefficient batch is repaired. 78 short batches have unique coefficients, larger batches choose least-used eligible coefficients, and all 251/353/353 original mathematical cases remain available through finite exhaustion.')
check('decision_variation', ['pedagogical-variation.json', 'sampler-regression.json', 'independent-math.json'],
      'Coefficient choice now varies the actual halving/squaring work. Retained source-directed counterfactual and shortcut checks apply to identical construction; changed sampling and delivered variety are checked separately.')
check('scope', ['solution-paths.json', 'sampler-regression.json'],
      'Both answer fragments agree with the displayed completed square in every final record. Signed hard parameters and supplied-sign easy/moderate magnitudes retain the reviewed response scope.')
check('grading', ['grading-input.json', 'grading-report.json'],
      '150 current native learner-engine checks pass: 90 exact/equivalent fractions and decimals accepted, 60 nearby wrong values/sign errors rejected, no unresolved results.')
check('rendering', ['render/rendering.json', 'visual-inspection.json'],
      'All 15 final records render through the unmodified study UI. Representative easy, moderate and hard screenshots were inspected; equations, answer controls and worked solutions display correctly.')
check('packaging', ['final-binding.json', 'sampler-regression.json'],
      'Runner relocated the declared package, verified dependencies and replayed every final band deterministically. Package, source, inventory, batch and asset identities were checked before this acceptance.')
check('progression', ['prior/progression.json', 'final-records.json', 'sampler-regression.json'],
      'Unchanged construction retains easy procedural guidance, moderate retrieval and hard reordered terms with signed parameters. All three final bands contain positive, zero and negative remainders; original source calibration is unchanged.')
for band, batch in binding['verification_batches'].items():
    report['band_verification'][band] = {'status': 'passed', 'batch_sha256': batch['batch_hash'],
        'evidence_paths': ['final-' + band + '.json', 'independent-math.json', 'grading-report.json',
                           'render/rendering.json', 'delivery-' + band + '/delivery.json', 'sampler-regression.json'],
        'details': 'Five final records: five distinct coefficients, all three remainder signs; independent math, native grading, UI rendering and delivery passed.'}
validate_review(report, E, binding)
save(E / 'result.json', report)
pipeline.persist(review=str(E / 'result.json'), review_policy_version=REVIEW_POLICY_VERSION,
                 review_binding=digest(binding), stage='prepare')
print('Accepted the checked sampler repair for easy, moderate and hard.')

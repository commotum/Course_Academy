"""Capture current source/inventory for the isolated sampler repair."""
import json
from pathlib import Path
import shutil
import sys

D = Path(__file__).resolve().parent
R = next(p for p in D.parents if (p / 'scripts/generator_pipeline.py').is_file())
sys.path.insert(0, str(R / 'scripts'))
from generator_pipeline import Pipeline, digest, source_identity
from generator_publish import Publisher

J = R / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051/fb70ce916f07d15e3ae3687a82c9367c9f521efc5156a3f231453ccff290fe05.pipeline/2'
E = J / 'review-1-policy-6-475e7ecef511ef18'
p = Publisher.from_environment(database='math')
source = p.extract_source(17592186087687, D / 'source')
old_source = json.loads((J / 'source/source.json').read_text())
assert source_identity(source) == source_identity(old_source), 'Instructional source changed; inspect before retaining prior evidence'
reference = source['registered_generator'][':question-generator/script']
assert reference == 'generators/3e/3e5be0963253ecbaff9964bd7bbb72fade1cef7a5a1fe5d8f2f5716a3b59ee0a/generator.py'
pipeline = Pipeline(D, {'kp': 17592186087687, 'difficulty': 'hard', 'count': 5,
                       'job_kind': 'build', 'existing_entrypoint': None}, p,
                    environment=p.client.environment)
pipeline.persist(manifest='package.json', source_hash=digest(source), investigation_complete=True,
                 seed=1811058558, stage='sample')
pipeline.ensure_inventory()
review = D / 'review'
review.mkdir(exist_ok=True)
prior = review / 'prior'
prior.mkdir(exist_ok=True)
for name in ('source-analysis.json', 'source-replay.json', 'source-replay-records.json',
             'progression.json', 'pedagogical-variation.json', 'counterfactual-tests.json',
             'counterfactual-records.json', 'matched-progression-records.json', 'review_checks.py',
             'shortcut-probes.json', 'ui-shortcut-probes.json', 'result.json'):
    shutil.copy2(E / name, prior / name)
context = {'previous_job': str(J), 'previous_review': str(E / 'result.json'),
           'source_identity_unchanged': True, 'source_basis': source['basis'],
           'original_registration': reference, 'scope': 'Sampler repair; question construction and source replay retained.'}
(D / 'repair-context.json').write_text(json.dumps(context, indent=2) + '\n')
print(json.dumps(context, indent=2))

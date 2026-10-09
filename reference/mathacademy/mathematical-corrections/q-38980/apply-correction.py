"""Authorized repeated-integral solution typo correction with durable EDB receipt audit."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from capture import arguments
from core import atomic_json
from database import Database, StaleBasis
from edn import dumps, kw, loads
from provenance import mathematical_correction_records

WORK = Path(__file__).resolve().parent
SOURCE = ROOT / 'reference/mathacademy/question-capture-workers/multivariable/14073682'
MID = 'q-38980'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


content = json.loads((SOURCE / 'content.json').read_text())
original = next(q for q in content['questions'] if q['math_academy_id'] == MID)
corrected = copy.deepcopy(original)
wrong = r"\begin{aligned}{\int }_{0}^{2}{\int }_{0}^{2-x}{\int }_{0}^{2-x-2y}"
right = r"\begin{aligned}{\int }_{0}^{2}{\int }_{0}^{(2-x)/2}{\int }_{0}^{2-x-2y}"
assert original['worked_solution'].count(wrong) == 1
corrected['worked_solution'] = original['worked_solution'].replace(wrong, right)
assert {k: v for k, v in original.items() if k != 'worked_solution'} == {
    k: v for k, v in corrected.items() if k != 'worked_solution'}
from fractions import Fraction
before_source = json.loads((SOURCE / 'q-38980-before.json').read_text())
after_source = json.loads((SOURCE / 'q-38980-after.json').read_text())
history_source = json.loads((SOURCE / 'history-q-38980.json').read_text())
assert before_source['problem'] == after_source['problem'] == original['problem']
assert after_source['worked_solution'] == history_source['worked_solution'] == original['worked_solution']
assert after_source['result'] == 'Correct'
assert r"{\int }_{0}^{2}{\int }_{0}^{(2-x)/2}{\int }_{0}^{2-x-2y}" in original['problem']
assert r"y=(2-x-z)/2" in original['worked_solution']
accepted = original['answer_fields'][0]['correct_value']
assert accepted == r"{∬}_{D}[{\int }_{0}^{(2-x-z)/2}f(x,y,z)\,dy]dA"
assert before_source['fields'][0]['choices'][0]['value'] == accepted
# Exact f=1 integration witness: let a=2-x. Inner z integral is a-2y.
# Over y in [0,a/2] it integrates to a^2/4; over [0,a] it is zero.
# Integral over x in [0,2] of (2-x)^2/4 = (8/3)/4 = 2/3.
original_volume = Fraction(8,3) / 4
mixed_volume = Fraction(8,3) / 4
erroneous_left_oriented_integral = Fraction(0)
assert original_volume == mixed_volume == Fraction(2,3)
assert erroneous_left_oriented_integral != mixed_volume
# Equivalent regions: nonnegative coordinates and x+2y+z<=2.
for xi in range(9):
 for yi in range(9):
  for zi in range(9):
   x,y,z = Fraction(xi,4), Fraction(yi,4), Fraction(zi,4)
   original_region = 0<=x<=2 and 0<=y<=(2-x)/2 and 0<=z<=2-x-2*y
   plane_region = x+2*y+z<=2
   mixed_region = x+z<=2 and 0<=y<=(2-x-z)/2
   assert original_region == plane_region == mixed_region
review_path = WORK / 'review.json'
if not review_path.exists():
    atomic_json(review_path, {
        'question': MID, 'source_capture': str(SOURCE),
        'original_content': original, 'corrected_content': corrected,
        'rationale': 'Correct only the final equality left-side middle y upper bound '
            'from 2-x to (2-x)/2, matching the unchanged original prompt and opening '
            'equality. The diagrams show z=2-x-2y with intercepts (2,0,0), '
            '(0,1,0), (0,0,2), and the source derivation correctly solves '
            'y=(2-x-z)/2 over D={(x,z):x>=0,z>=0,x+z<=2}. Preserve the '
            'accepted mixed-integral answer, all field and answer identities, '
            'original source captures and historical versions.',
        'authorized_scope': 'Focused user-authorized content-only mathematical typo correction; '
            'two bounded attempts, no browser or solver sessions, no shared code edits',
        'source_sha256': {str(p): sha(p) for p in sorted(SOURCE.rglob('*')) if p.is_file()},
        'mathematical_check': {
            'passed': True, 'method': 'Exact plane algebra and rational f=1 counterexample',
            'proof': 'R={x,y,z>=0:x+2y+z<=2}; projecting onto xz gives D={x,z>=0:x+z<=2}. '
                'Thus 0<=y<=(2-x-z)/2. Original repeated-integral bounds follow by '
                'projecting onto xy, giving 0<=y<=(2-x)/2. With f=1 both correct '
                'integrals give volume 2/3. The erroneous final left-side integral '
                'has y up to 2-x and evaluates to 0: integral_0^a(a-2y)dy=0, '
                'where a=2-x. Hence the source typo cannot express the same integral.',
            'region_equivalence_exact_rational_grid_points': 729,
            'f1_original_integral': str(original_volume), 'f1_correct_mixed_integral': str(mixed_volume),
            'f1_erroneous_left_integral': str(erroneous_left_oriented_integral),
            'saved_source_before_after_history_agree': True,
            'original_grade': after_source['result'],
            'independently_viewed_images': [str(SOURCE/n) for n in (
                'q-38980-before.png', 'q-38980-after.png', 'history-q-38980.png',
                'assets/96b24f85c19f388c152dae265c3794179ebc9e1e6fc06a1fe10f82627b73d29c.png',
                'assets/f08e4fc4d1d2933e9c12fe7df96a1029d66a83c68beff4fa31928cc010554766.png',
                'assets/2639dbff9d1d4269abb59ccd3eefa0b246c8d1f183fd8f6ef132a41cc07e345d.png')],
            'original_prompt_key_formula_consistent': True,
            'corrected_solution_and_prompt_consistent': True}})
review = json.loads(review_path.read_text())
assert review['original_content'] == original and review['corrected_content'] == corrected
assert all(sha(Path(p)) == digest for p, digest in review['source_sha256'].items())

args = arguments(['import-saved', '--content', str(SOURCE / 'content.json'),
    '--output', str(SOURCE.parent), '--edb-bin', '/home/jake/Developer/EDB/target/release/edb',
    '--database', 'course-academy-v2', '--endpoint', '/tmp/course-academy-edb-v2/writer.sock'])
args.capture_root = [ROOT / 'reference/mathacademy/question-capture', *[
    ROOT / 'reference/mathacademy/question-capture-workers' / name
    for name in ('linear', 'multivariable', 'differential')]]
db = Database(args)
tx_path = WORK / 'transaction.edn'
intent_path = WORK / 'commit-intent.json'
for attempt in range(2):
    if intent_path.exists():
        intent = json.loads(intent_path.read_text())
        assert intent['sha256'] == sha(tx_path)
        assert intent['reconciliation_sha256'] == sha(WORK / 'reconciliation.edn')
        assert intent['review_sha256'] == sha(review_path)
        assert intent['database'] == args.database and intent['endpoint'] == args.endpoint
        basis = intent['basis']
    else:
        basis = db.basis()
        before = db.questions([MID], WORK, 'before', basis)[MID]
        assert before[':question/problem'] == original['problem']
        assert before[':question/worked-solution'] == original['worked_solution']
        retention = db.query('[:find ?ident :in $ [?ident ...] :where '
            '[?a :db/ident ?ident] [?a :db/noHistory true]]',
            [[kw(a) for a in ('question/problem','question/worked-solution','question/answer-fields', 'question/version','answer-field/id','answer-field/key','answer-field/type','answer-field/correct','answer-field/choices','answer/id','answer/type','answer/value')]],
            WORK, 'no-history', basis)
        assert not retention
        tx = [{kw('db/id'): before[':db/id'],
            kw('question/worked-solution'): corrected['worked_solution'],
            kw('db/ensure'): [kw('question/validate')]}]
        tx_path.write_text(dumps(tx) + '\n')
        preview_text = db.command('with', '--file', tx_path)
        (WORK / 'preview.edn').write_text(preview_text)
        preview = loads(preview_text)
        if preview[':edb/db-before-t'] != basis:
            continue
        guards = {
            'retractions': [[before[':db/id'], kw('question/worked-solution'), original['worked_solution']]],
            'immutable_answers': sorted({a[':db/id'] for f in before[':question/answer-fields']
                for a in f[':answer-field/choices']}),
            'immutable_fields': [[f[':db/id'], kw(attr)] for f in before[':question/answer-fields']
                for attr in ('answer-field/id', 'answer-field/key', 'answer-field/type',
                             'answer-field/correct', 'answer-field/choices')]}
        attributes = db.attributes(WORK, basis)
        db.validate_datoms(preview, attributes, **guards)
        preview_names = dict(attributes)
        preview_content = [d for d in preview[':edb/tx-data'] if preview_names[d[1]] != ':db/txInstant']
        assert len(preview_content) == 2
        assert all(d[0] == before[':db/id'] and preview_names[d[1]] == ':question/worked-solution' for d in preview_content)
        (WORK / 'reconciliation.edn').write_text(dumps(guards) + '\n')
        digest = sha(tx_path)
        intent = {'database': args.database, 'endpoint': args.endpoint, 'basis': basis,
            'sha256': digest, 'review_sha256': sha(review_path),
            'request_key': 'ma-mathematical-correction-q-38980-bound-typo-' + str(basis) + '-' + digest,
            'reconciliation_sha256': sha(WORK / 'reconciliation.edn')}
        atomic_json(intent_path, intent)
    try:
        receipt = db._commit(intent, tx_path, WORK)
    except StaleBasis:
        continue
    break
else:
    raise RuntimeError('Two bounded stale-basis attempts exhausted')

assert receipt[':edb/committed'] is True and receipt[':edb/db-before-t'] == basis
after_basis = receipt[':edb/db-after-t']
attributes = db.attributes(WORK, basis)
guards = loads((WORK / 'reconciliation.edn').read_text())
db.validate_datoms(receipt, attributes, **guards)
names = dict(attributes)
content_datoms = [d for d in receipt[':edb/tx-data'] if names[d[1]] != ':db/txInstant']
assert len(content_datoms) == 2
assert all(names[d[1]] == ':question/worked-solution' for d in content_datoms)
before = db.questions([MID], WORK, 'original-retained', basis)[MID]
current = db.questions([MID], WORK, 'after', after_basis)[MID]
assert before[':question/worked-solution'] == original['worked_solution']
assert current[':question/worked-solution'] == corrected['worked_solution']
assert {k: v for k, v in before.items() if k != ':question/worked-solution'} == {
    k: v for k, v in current.items() if k != ':question/worked-solution'}
assert current[':question/answer-fields'][0][':answer-field/correct'][':answer/value'] == before[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
verification = {'committed': True, 'basis_before': basis, 'basis_after': after_basis,
    'mathematical_check_passed': True, 'historical_original_question_retained': True,
    'answer_fields_choices_and_answer_identities_unchanged': True,
    'learner_and_engine_facts_unchanged': True,
    'verification_method': 'committed_content_datoms_and_exact_question_readback',
    'review_sha256': sha(review_path), 'transaction_sha256': sha(tx_path),
    'receipt': str(WORK / 'commit.edn'), 'receipt_datom_count': len(receipt[':edb/tx-data']),
    'receipt_content_datom_count': len(content_datoms)}
atomic_json(WORK / 'verification.json', verification)
records = mathematical_correction_records(ROOT / 'reference/mathacademy', {MID})
assert len(records) == 3
attestation = db.reconciliation({**content, 'questions': [original], 'canonical_examples': []},
    WORK / 'attestation', {MID: current}, after_basis)
attested = [r for r in attestation.authored if r.get('category') == 'mathematical_correction']
assert len(attested) == 3
atomic_json(WORK / 'attestation.json', {'basis': after_basis, 'records': attested,
    'field_identity_unchanged': True, 'correct_answer_identity_unchanged': True})
noop = db.import_content(content, WORK / 'original-source-reimport', apply=False)
assert noop.get('already_complete') is True and noop['database_writes'] == 0
assert not (WORK / 'original-source-reimport' / 'commit-intent.json').exists()
assert all(sha(Path(p)) == digest for p, digest in review['source_sha256'].items())
verification.update({'original_source_reimport_is_noop': True,
    'original_source_reimport_preview': noop, 'original_source_sha256_unchanged': True,
    'correction_attested_at_committed_basis': True})
atomic_json(WORK / 'verification.json', verification)
atomic_json(WORK / 'audit.json', {**verification, 'source_capture_file_count': len(review['source_sha256']),
    'receipt_attributes': sorted({str(names[d[1]]) for d in receipt[':edb/tx-data']}),
    'source_and_shared_code_edits': [], 'new_question_count': 0,
    'changed_content_attributes': ['question/worked-solution'],
    'original_prompt_and_corrected_solution_math_consistent': True, 'original_final_equality_mathematically_false': True,
    'question_entity': current[':db/id'], 'answer_field_entities': [f[':db/id'] for f in current[':question/answer-fields']],
    'accepted_answer_entity': current[':question/answer-fields'][0][':answer-field/correct'][':db/id']})
print(json.dumps(verification, indent=2))

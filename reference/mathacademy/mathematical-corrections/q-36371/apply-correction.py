"""Authorized solution-point typo correction with durable EDB receipt audit."""
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
SOURCE = ROOT / 'reference/mathacademy/question-capture-workers/multivariable/14044096'
MID = 'q-36371'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


content = json.loads((SOURCE / 'content.json').read_text())
original = next(q for q in content['questions'] if q['math_academy_id'] == MID)
corrected = copy.deepcopy(original)
assert original['worked_solution'].count('$P(1,1,0)$') == 1
corrected['worked_solution'] = original['worked_solution'].replace('$P(1,1,0)$', '$P(2,-3,3)$')
assert {k: v for k, v in original.items() if k != 'worked_solution'} == {
    k: v for k, v in corrected.items() if k != 'worked_solution'}
assert 6 * (2 - 1) == 6 and 6 * 2 - 9 == 3
assert original['answer_fields'][0]['correct_value'] == '⟨1,0,6⟩'
review_path = WORK / 'review.json'
if not review_path.exists():
    atomic_json(review_path, {
        'question': MID, 'source_capture': str(SOURCE),
        'original_content': original, 'corrected_content': corrected,
        'rationale': 'Correct only the isolated tangent-line prose point P(1,1,0) to '
            'P(2,-3,3), the point supplied in the unchanged prompt and consistently used '
            'in the derivative and point-slope calculation. Preserve the accepted answer, '
            'all answer fields and choices, source captures and historical versions.',
        'authorized_scope': 'MathAcademy heartbeat content-only correction',
        'source_sha256': {str(p): sha(p) for p in sorted(SOURCE.rglob('*')) if p.is_file()},
        'mathematical_check': {
            'passed': True, 'method': 'Exact substitution and intersection tangent parameterization',
            'proof': 'r(x)=(x,-3,f(x,-3)); r(2)=(2,-3,3) and r\'(2)=(1,0,6(2-1))=(1,0,6). '
                'The tangent line y=-3, z=6x-9 contains (2,-3,3). The source prose point '
                '(1,1,0) has y=1, so does not belong to the intersection plane. '
                '(0,1,0) cross (6,0,-1)=(-1,0,-6), whose negative is the unchanged accepted vector.',
            'original_calculation_and_key_consistent': True,
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
for attempt in range(3):
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
            [[kw('question/problem'), kw('question/worked-solution'), kw('question/answer-fields')]],
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
        (WORK / 'reconciliation.edn').write_text(dumps(guards) + '\n')
        digest = sha(tx_path)
        intent = {'database': args.database, 'endpoint': args.endpoint, 'basis': basis,
            'sha256': digest, 'review_sha256': sha(review_path),
            'request_key': 'ma-mathematical-correction-q-36371-point-typo-' + str(basis) + '-' + digest,
            'reconciliation_sha256': sha(WORK / 'reconciliation.edn')}
        atomic_json(intent_path, intent)
    try:
        receipt = db._commit(intent, tx_path, WORK)
    except StaleBasis:
        continue
    break
else:
    raise RuntimeError('Three bounded stale-basis attempts exhausted')

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
assert current[':question/answer-fields'][0][':answer-field/correct'][':answer/value'] == '⟨1,0,6⟩'
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
    'original_and_current_solution_math_consistent': True,
    'question_entity': current[':db/id'], 'answer_field_entities': [f[':db/id'] for f in current[':question/answer-fields']],
    'accepted_answer_entity': current[':question/answer-fields'][0][':answer-field/correct'][':db/id']})
print(json.dumps(verification, indent=2))

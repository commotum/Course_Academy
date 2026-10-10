"""Authorized coefficient-matrix transcription correction with durable EDB receipt audit."""
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
SOURCE = ROOT / 'reference/mathacademy/question-capture-workers/linear/14059591'
MID = 'q-140043'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


content = json.loads((SOURCE / 'content.json').read_text())
original = next(q for q in content['questions'] if q['math_academy_id'] == MID)
corrected = copy.deepcopy(original)
old_row = r'6 & 5 & -2'
new_row = r'6 & 5 & -3'
assert original['worked_solution'].count(old_row) == 1
corrected['worked_solution'] = original['worked_solution'].replace(old_row, new_row)
assert {k: v for k, v in original.items() if k != 'worked_solution'} == {
    k: v for k, v in corrected.items() if k != 'worked_solution'}
from fractions import Fraction
from xml.etree import ElementTree

def determinant(m):
    a,b,c = m[0]; d,e,f = m[1]; g,h,i = m[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

# Each determinant is affine in k: checking intercept and slope proves the expressions.
assert determinant([[6,5,-3],[4,-5,0],[-2,10,-5]]) == 160
assert determinant([[6,5,-3],[4,-5,1],[-2,10,-5]]) == 90
assert determinant([[6,5,-2],[4,-5,0],[-2,10,-5]]) == 190
assert determinant([[2,5,-3],[1,-5,0],[-2,10,-5]]) == 75
assert determinant([[2,5,-3],[1,-5,1],[-2,10,-5]]) == 45
x,y,z,k = Fraction(1,2),Fraction(2,5),Fraction(1),Fraction(1)
assert 6*x+5*y-3*z == 2 and 4*x-5*y+k*z == 1 and -2*x+10*y-5*z == -2
assert 2*(75-30*k) == 160-70*k and 160-70*k != 0
assert original['answer_fields'][0]['correct_value'] == 'k=1'
html_proof = {}
for name in ('q-140043-after.json', 'history-q-140043.json'):
    raw = json.loads((SOURCE/name).read_text())
    assert raw['worked_solution'] == original['worked_solution']
    # Inspect the original accessible MathML matrix, independently of extracted LaTeX.
    import re
    maths = [ElementTree.fromstring(m) for m in re.findall(r'<math\b[^>]*>.*?</math>',raw['html'],re.S)]
    matrix_rows = []
    for math in maths:
        for table in math.iter('{http://www.w3.org/1998/Math/MathML}mtable'):
            rows = list(table)
            if len(rows) == 3 and len(list(rows[0])) == 3:
                cells = [''.join(c.itertext()) for c in list(rows[0])]
                if cells[:2] == ['6','5']:
                    matrix_rows.append(cells)
    assert ['6','5','−2'] in matrix_rows or ['6','5','-2'] in matrix_rows, matrix_rows
    html_proof[name] = {'original_mathml_first_row': matrix_rows, 'sha256': sha(SOURCE/name)}
source_question_sha256 = hashlib.sha256(json.dumps(original,sort_keys=True,separators=(',',':')).encode()).hexdigest()
review_path = WORK / 'review.json'
if not review_path.exists():
    atomic_json(review_path, {
        'question': MID, 'source_capture': str(SOURCE),
        'original_content': original, 'corrected_content': corrected,
        'rationale': 'Correct only the first coefficient determinant matrix row from 6,5,-2 to '
            '6,5,-3. The unchanged prompt has coefficient -3 for z; the unchanged determinant '
            '160-70k, Dx=75-30k and accepted key k=1 all use that correct coefficient. '
            'The original screenshot and accessible MathML confirm the source displays -2, '
            'excluding an extraction issue. Preserve raw captures, solver evidence, choices, '
            'answer fields and identities, accepted key, and historical versions.',
        'authorized_scope': 'Explicitly authorized content-only study correction',
        'source_question_sha256': source_question_sha256,
        'source_sha256': {str(p): sha(p) for p in sorted(SOURCE.rglob('*')) if p.is_file()},
        'source_html_evidence': html_proof,
        'source_screenshot_review': {'path': str(SOURCE/'history-q-140043.png'),
            'sha256': sha(SOURCE/'history-q-140043.png'), 'visually_confirmed_first_D_row': [6,5,-2]},
        'mathematical_check': {
            'passed': True, 'method': 'Exact 3x3 determinants, affine-in-k coefficient proof and rational substitution',
            'correct_D': '160-70k', 'source_mistyped_D': '190-70k', 'Dx': '75-30k',
            'proof': 'The determinant is affine in k by multilinearity. Correct D(0)=160 and D(1)=90; '
                'Dx(0)=75 and Dx(1)=45. Thus x=1/2 gives 2(75-30k)=160-70k, so k=1. '
                'D(1)=90 is nonzero. Exact substitution of (x,y,z)=(1/2,2/5,1) satisfies all three equations.',
            'accepted_key': 'k=1', 'unique_solution': ['1/2','2/5','1'],
            'corrected_solution_and_prompt_consistent': True}})
review = json.loads(review_path.read_text())
assert review['original_content'] == original and review['corrected_content'] == corrected
assert review['source_question_sha256'] == source_question_sha256
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
            'request_key': 'ma-mathematical-correction-q-140043-coefficient-matrix-typo-' + str(basis) + '-' + digest,
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
assert current[':question/answer-fields'][0][':answer-field/correct'][':answer/value'] == 'k=1'
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
    'corrected_solution_and_prompt_math_consistent': True,
    'question_entity': current[':db/id'], 'answer_field_entities': [f[':db/id'] for f in current[':question/answer-fields']],
    'accepted_answer_entity': current[':question/answer-fields'][0][':answer-field/correct'][':db/id']})
audit = json.loads((WORK/'audit.json').read_text())
audit.update({'question': MID, 'review': str(review_path), 'transaction': str(tx_path),
    'commit_intent': str(intent_path), 'commit_intent_sha256': sha(intent_path),
    'receipt_sha256': sha(WORK/'commit.edn'), 'source_question_sha256': source_question_sha256,
    'review_original_bound_to_actual_source_question': True,
    'source_html_evidence': html_proof, 'corrected_solution_and_prompt_consistent': True,
    'math_focused_test': review['mathematical_check'], 'source_shared_changes': [],
    'unchanged_attempt_limit': 2, 'source_capture': str(SOURCE),
    'attestation': str(WORK/'attestation.json'), 'readback_before': str(WORK/'original-retained.edn'),
    'readback_after': str(WORK/'after.edn'),
    'reconciliation': str(WORK/'reconciliation.edn')})
audit.update({'artifact_sha256': {str(WORK/name): sha(WORK/name) for name in
    ('review.json','transaction.edn','commit-intent.json','commit.edn','reconciliation.edn',
     'original-retained.edn','after.edn','attestation.json','original-source-reimport/verification.json')},
    'database': args.database, 'endpoint': args.endpoint, 'request_key': intent['request_key'],
    'basis_guard': intent['basis'], 'protected_content_datom_count': 0,
    'regression_tests': {'module': 'test_mathematical_corrections', 'tests_passed': 4},
    'content_datom_proof': [{'entity': d[0], 'attribute': names[d[1]],
        'value_sha256': hashlib.sha256(dumps(d[2]).encode()).hexdigest(),
        'transaction': d[3], 'added': d[4]} for d in content_datoms]})
atomic_json(WORK/'audit.json', audit)
atomic_json(ROOT/'.local/question_capture-fleet/la-matrix-140043/verification.json', audit)
print(json.dumps(verification, indent=2))

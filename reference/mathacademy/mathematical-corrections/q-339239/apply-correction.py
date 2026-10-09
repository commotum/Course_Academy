"""Correct study precision explicitly while retaining original MA content."""
import copy
import hashlib
import json
import sys
from decimal import Decimal, localcontext, ROUND_HALF_UP
from pathlib import Path
from types import SimpleNamespace

ROOT = Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0, str(ROOT/'scripts/question_capture'))
from core import atomic_json, stable_id
from database import Database, StaleBasis
from edn import dumps, kw, loads

mid = 'q-339239'
capture = ROOT/'reference/mathacademy/question-capture-workers/differential/14045453'
directory = ROOT/'reference/mathacademy/mathematical-corrections'/mid
directory.mkdir(parents=True, exist_ok=True)
state = json.loads((capture/'state.json').read_text())
assert state.get('activity_complete') and state.get('history_complete') and state.get('import_complete')
content = json.loads((capture/'content.json').read_text())
original = next(q for q in content['questions'] if q['math_academy_id'] == mid)
assert original['answer_fields'][0]['correct_value'] == r'12\,547'
assert 'rounded to $3$ decimal places' in original['worked_solution']
corrected = copy.deepcopy(original)
corrected['problem'] += ' Round the final population to the nearest whole fish. Do not round intermediate values.'
corrected['worked_solution'] = r'''The solution of $P'(t)=0.09P(t)$ satisfies

$$P(t)=P(18)e^{0.09(t-18)}=8\,000e^{0.09(t-18)}.$$

Therefore,

$$P(23)=8\,000e^{0.45}\approx12\,546.49748392135.$$

Rounding only this final value to the nearest whole number gives approximately $12\,546$ fish.'''
f = corrected['answer_fields'][0]
assert f['key'] == 'selection' and f['type'] == 'radio'
assert sum(c['value'] == r'12\,547' for c in f['choices']) == 1
for choice in f['choices']:
    if choice['value'] == r'12\,547': choice['value'] = r'12\,546'
f['correct_value'] = r'12\,546'
f['correct_origin'] = 'reviewed_mathematical_correction'
with localcontext() as ctx:
    ctx.prec = 55
    exact = Decimal(8000)*Decimal('.45').exp()
    p0 = Decimal(8000)*Decimal('-1.62').exp()
    rounded_p0 = p0.quantize(Decimal('.001'), rounding=ROUND_HALF_UP)
    source_approx = rounded_p0*Decimal('2.07').exp()
    assert exact.quantize(Decimal(1), rounding=ROUND_HALF_UP) == 12546
    assert source_approx.quantize(Decimal(1), rounding=ROUND_HALF_UP) == 12547
source_paths = [capture/'content.json', capture/'q-339239-after.json', capture/'q-339239-after.png']
source_hashes = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
review = {'question':mid, 'source_capture':str(capture), 'original_content':original,
    'corrected_content':corrected,
    'rationale':'The source lesson rounds the initial constant to three decimal places, '
        'then rounds the resulting later population to 12,547. That is its documented '
        'approximation method, confirmed by the revealed source solution. The study prompt '
        'now explicitly requires final-only nearest-whole rounding, whose mathematically '
        'correct value is 12,546. Preserve original source content and its 12,547 key in '
        'historical question content and immutable old answer fields; create new study '
        'field and answer identities with matching prompt, solution, choice and key.',
    'authorized_scope':'MathAcademy heartbeat mathematically correct content-only study correction',
    'source_sha256':source_hashes,
    'mathematical_check':{'passed':True,'method':'Decimal 55-digit exponential evaluation and nearest-integer bounds',
        'exact_p23':str(exact),'exact_nearest_whole':12546,'source_rounded_p0':str(rounded_p0),
        'source_intermediate_rounded_p23':str(source_approx),'source_nearest_whole':12547}}
review_path = directory/'review.json'
if review_path.exists(): assert json.loads(review_path.read_text()) == review
else: atomic_json(review_path, review)
args = SimpleNamespace(edb_bin='/home/jake/Developer/EDB/target/release/edb',
    database='course-academy-v2', endpoint='/tmp/course-academy-edb-v2/writer.sock',
    capture_root=[str(ROOT/'reference/mathacademy/question-capture')]+[
        str(ROOT/'reference/mathacademy/question-capture-workers'/w) for w in ['linear','multivariable','differential']])
db = Database(args)
for attempt in range(3):
    intent_path, tx_path = directory/'commit-intent.json', directory/'transaction.edn'
    if intent_path.exists():
        intent = json.loads(intent_path.read_text())
        guards = loads((directory/'guards.edn').read_text())
        assert hashlib.sha256(tx_path.read_bytes()).hexdigest() == intent['sha256']
        basis = intent['basis']; old = db.questions([mid],directory,'before',basis)[mid]
        attributes = db.attributes(directory,basis)
    else:
        basis = db.basis(); old = db.questions([mid],directory,'before',basis)[mid]
        assert old[':question/problem'] == original['problem']
        assert old[':question/worked-solution'] == original['worked_solution']
        old_field, = old[':question/answer-fields']
        assert old_field[':answer-field/correct'][':answer/value'] == r'12\,547'
        no_history = db.query('[:find ?ident :in $ [?ident ...] :where '
            '[?a :db/ident ?ident] [?a :db/noHistory true]]',
            [[kw(a) for a in ['question/problem','question/worked-solution','question/answer-fields',
                'answer-field/correct','answer-field/choices','answer/value']]],directory,'history-retention',basis)
        assert not no_history
        token = mid+'/mathematical-correction-v1/selection'
        answer_tokens = [token+'/answer-'+str(i) for i in range(len(f['choices']))]
        correct_token = answer_tokens[next(i for i,c in enumerate(f['choices']) if c['value'] == f['correct_value'])]
        transaction = [[kw('db/retract'),old[':db/id'],kw('question/answer-fields'),old_field[':db/id']]]
        for answer_token, choice in zip(answer_tokens,f['choices']):
            transaction.append({kw('db/id'):answer_token,kw('answer/id'):stable_id('answer',answer_token),
                kw('answer/type'):kw('answer.type/'+choice['type']),kw('answer/value'):choice['value'],
                kw('db/ensure'):[kw('answer/validate')]})
        transaction.extend([
            {kw('db/id'):token,kw('answer-field/id'):stable_id('field',token),
                kw('answer-field/key'):'selection',kw('answer-field/type'):kw('answer-field.type/radio'),
                kw('answer-field/choices'):answer_tokens,kw('answer-field/correct'):correct_token,
                kw('db/ensure'):[kw('answer-field/validate')]},
            {kw('db/id'):old[':db/id'],kw('question/problem'):corrected['problem'],
                kw('question/worked-solution'):corrected['worked_solution'],
                kw('question/answer-fields'):[token],kw('db/ensure'):[kw('question/validate')]}])
        guards = {'retractions':[[old[':db/id'],kw('question/answer-fields'),old_field[':db/id']],
            [old[':db/id'],kw('question/problem'),old[':question/problem']],
            [old[':db/id'],kw('question/worked-solution'),old[':question/worked-solution']]],
            'immutable_answers':[a[':db/id'] for a in old_field[':answer-field/choices']],
            'immutable_fields':[[old_field[':db/id'],kw(a)] for a in
                ['answer-field/id','answer-field/key','answer-field/type','answer-field/correct']]}
        tx_path.write_text(dumps(transaction)+'\n');(directory/'guards.edn').write_text(dumps(guards)+'\n')
        preview_text = db.command('with','--file',tx_path);(directory/'preview.edn').write_text(preview_text)
        preview = loads(preview_text)
        if preview[':edb/db-before-t'] != basis: continue
        attributes = db.attributes(directory,basis);db.validate_datoms(preview,attributes,**guards)
        digest = hashlib.sha256(tx_path.read_bytes()).hexdigest()
        intent = {'database':args.database,'endpoint':args.endpoint,'basis':basis,'sha256':digest,
            'request_key':'ma-mathematical-correction-'+mid+'-'+str(basis)+'-'+digest}
        atomic_json(intent_path,intent)
    try: receipt = db._commit(intent,tx_path,directory)
    except StaleBasis:
        if attempt == 2: raise
        continue
    db.validate_datoms(receipt,attributes,**guards)
    break
else: raise RuntimeError('Database advanced during all three correction previews')
after_basis = receipt[':edb/db-after-t'];after = db.questions([mid],directory,'after',after_basis)[mid]
assert after[':question/problem'] == corrected['problem']
assert after[':question/worked-solution'] == corrected['worked_solution']
new_field, = after[':question/answer-fields'];old_field, = old[':question/answer-fields']
assert new_field[':answer-field/correct'][':answer/value'] == f['correct_value']
assert new_field[':db/id'] != old_field[':db/id']
assert {a[':answer/value'] for a in new_field[':answer-field/choices']} == {c['value'] for c in f['choices']}
assert not ({a[':db/id'] for a in new_field[':answer-field/choices']} & {a[':db/id'] for a in old_field[':answer-field/choices']})
retained = db.query('[:find (pull ?f [* {:answer-field/type [:db/ident]} '
    '{:answer-field/choices [* {:answer/type [:db/ident]}]} '
    '{:answer-field/correct [* {:answer/type [:db/ident]}]}]) :in $ ?f :where [?f :answer-field/id _]]',
    [old_field[':db/id']],directory,'retained-original-field',after_basis)
assert retained[0][0] == old_field
assert db.questions([mid],directory,'historical-original',basis)[mid] == old
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == digest for p,digest in source_hashes.items())
proof = {'committed':True,'basis_before':basis,'basis_after':after_basis,'mathematical_check_passed':True,
    'original_field_and_answer_retained':True,'historical_original_question_retained':True,
    'new_field_and_answer_identities':True,'learner_and_engine_facts_unchanged':True,
    'verification_method':'committed_content_datoms_and_exact_question_readback',
    'review_sha256':hashlib.sha256(review_path.read_bytes()).hexdigest(),
    'transaction_sha256':hashlib.sha256(tx_path.read_bytes()).hexdigest(),
    'original_source_sha256_unchanged':True,'original_source_correct_answer':r'12\,547',
    'correct_answer':f['correct_value'],'receipt':str(directory/'commit.edn')}
atomic_json(directory/'verification.json',proof)
single = {**content,'questions':[original],'canonical_examples':[]}
check = db.import_content(single,directory/'original-source-reimport-check',apply=False)
assert check.get('already_complete') and check['database_writes'] == 0, check
proof.update(original_source_reimport_is_noop=True,original_source_reimport_preview=check)
atomic_json(directory/'verification.json',proof)
print(json.dumps(proof,indent=2))

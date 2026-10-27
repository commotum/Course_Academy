import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import patch
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_publish import (Publisher, StaleBasis, SourceChanged, VerificationError, content_fingerprint,
    digest, dumps, enum, jsonable, kw, loads, normalized_question, stable_identities,
    validate_question, validate_report)
from generator_packages import publish_package

KP = 101
KP_UUID = uuid.UUID('11111111-1111-4111-8111-111111111111')
LINEAGE = '22222222-2222-4222-8222-222222222222'
PACKAGE = 'c' * 64
SCRIPT = f'generators/cc/{PACKAGE}/generate.py'


def record(number=2):
    aid = str(uuid.uuid5(KP_UUID, 'answer' + str(number)))
    return {'knowledge_point': KP, 'generation': {'parameters': {'number': number}}, 'question': {
        ':question/id': str(uuid.uuid4()), ':question/problem': f'Compute {number}+1.',
        ':question/worked-solution': f'Adding one gives {number+1}.',
        ':question/difficulty': ':question.difficulty/easy', ':question/answer-fields': [{
            ':answer-field/id': str(uuid.uuid4()), ':answer-field/key': 'answer',
            ':answer-field/type': ':answer-field.type/blank', ':answer-field/correct': [':answer/id', aid],
            ':answer-field/choices': [{':answer/id': aid, ':answer/type': ':answer.type/math', ':answer/value': str(number+1)}]}]}}


class MatrixLayoutPublicationTests(unittest.TestCase):
    def test_rejects_plain_limit_operator_and_relation_as_sized_bar(self):
        for value in (r'{lim}_{{x}\rightarrow2}f(x)', r'\big\mid A\big\mid'):
            q = record()['question']
            q[':question/worked-solution'] = '$$' + value + '$$'
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_question(q)

    def test_rejects_group_crossing_fake_determinant_and_ragged_grid(self):
        for value in (r'\frac{5\begin{vmatrix}x &}{3\mid y\end{vmatrix}}',
                      r'\begin{bmatrix}1&2\\3\end{bmatrix}'):
            q = record()['question']
            q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_question(q)

    def test_rejects_fenced_alignment_in_prompt_solution_and_answer(self):
        bad = r'|\begin{aligned}1&3\\2&-3\end{aligned}|'
        for key in (':question/problem', ':question/worked-solution'):
            q = record()['question']
            q[key] = '$$' + r'\begin{aligned}D &=' + bad + r'\\ &=-9\end{aligned}' + '$$'
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'matrix environment'):
                validate_question(q)
        for atype, value in ((':answer.type/math', bad), (':answer.type/text', '$' + bad + '$')):
            q = record()['question']
            a = q[':question/answer-fields'][0][':answer-field/choices'][0]
            a[':answer/type'], a[':answer/value'] = atype, value
            with self.subTest(atype=atype), self.assertRaisesRegex(ValueError, 'matrix environment'):
                validate_question(q)

    def test_accepts_real_matrix_and_preserves_wrapped_scalar(self):
        q = record()['question']
        q[':question/worked-solution'] = '$$' + r'\begin{aligned}D &=\begin{vmatrix}1&3\\2&-3\end{vmatrix}\\&=-9\end{aligned}' + '$$'
        validate_question(q)
        q[':question/worked-solution'] = '$$' + r'e^t\left(\begin{aligned}&x\\&{}+(y)\end{aligned}\right)' + '$$'
        validate_question(q)


class FakeClient:
    """Tiny source-aware transaction model; real native predicates are tested separately."""
    def __init__(self):
        self.basis = 12
        self.next_id = 2000
        self.receipts = {}
        self.calls = []
        self.lose_reply = False
        self.reject_stale = False
        self.fail_readback = False
        self.lessons = []
        self.excluded_sources = []
        self.entities = {}
        from generator_publish import ALLOWED
        refs = {'question/difficulty', 'question/answer-fields', 'answer-field/type', 'answer-field/choices',
                'answer-field/correct', 'answer/type', 'knowledge-point/questions', 'knowledge-point/question-generator'}
        names = sorted(ALLOWED | {'db/txInstant'})
        self.attributes = [[i + 1, kw(n), kw('db.type/ref' if n in refs else 'db.type/string')] for i, n in enumerate(names)]
        enums = [':application/ca-engine', ':question.difficulty/easy', ':question.difficulty/moderate',
                 ':question.difficulty/hard', ':answer-field.type/blank', ':answer.type/math', ':answer.type/image',
                 ':answer.type/text', ':answer-field.type/radio', ':agent/codex']
        self.idents = [[100 + i, kw(n)] for i, n in enumerate(enums)]
        self.kp = {':db/id': KP, ':knowledge-point/id': KP_UUID, ':knowledge-point/title': 'Add one',
                   ':knowledge-point/canonical-example': {':db/id': 99, ':question/id': uuid.uuid4(), ':question/problem': 'Compute 1+1.', ':question/worked-solution': 'Two.'},
                   ':knowledge-point/questions': []}
        self.initial_kp = copy.deepcopy(self.kp)

    def status(self):
        return {'database': 'math', 'lineage': LINEAGE, 'basis': self.basis}

    def query(self, query, inputs, directory, name, basis=None):
        Path(directory).mkdir(parents=True, exist_ok=True)
        if name == 'source-membership-attributes':
            return []
        if name == 'source-multipart-steps':
            return [[900]] if self.excluded_sources else []
        if name == 'source-multipart-roots':
            return [[q[':db/id']] for q in self.excluded_sources if not q.get(':question/retired')]
        if name.startswith('source-multipart-wrappers-'):
            return []
        if name == 'source-retired':
            return [[q[':db/id']] for q in self.excluded_sources if q.get(':question/retired')]
        if name == 'source-exclusions':
            return [[copy.deepcopy(q)] for q in self.excluded_sources
                    if not inputs or q[':db/id'] in inputs[0]]
        if name == 'kp':
            if self.fail_readback and self.basis > 12 and basis == self.basis:
                self.fail_readback = False
                raise ConnectionError('readback unavailable')
            return [[copy.deepcopy(self.kp if basis == self.basis else self.initial_kp)]]
        if name == 'attributes':
            return self.attributes
        if name == 'idents':
            return self.idents
        if name == 'generator-identity':
            return [[copy.deepcopy(e)] for e in self.entities.values() if e.get(':question-generator/id') == inputs[0]]
        if name == 'identity-collisions':
            return [[eid, value] for eid, entity in self.entities.items() for k, value in entity.items() if k in (':question/id', ':answer-field/id', ':answer/id') and value in inputs[0]]
        if name == 'lessons':
            return [[copy.deepcopy(l)] for l in self.lessons]
        if name == 'topics':
            return [[{':db/id': 600, ':topic/id': KP_UUID}]] if self.lessons else []
        if name == 'prerequisites':
            return []
        raise AssertionError(name)

    def command(self, command, *options, **kwargs):
        options = list(map(str, options))
        flags = dict(zip(options[::2], options[1::2]))
        tx = Path(flags['--file']).read_text()
        self.calls.append((command, tx, flags))
        key = flags.get('--request-key')
        if command == 'transact' and key in self.receipts:
            return dumps(self.receipts[key])
        if command == 'transact' and (self.reject_stale or int(flags['--basis']) != self.basis):
            raise StaleBasis('confirmed stale basis')
        forms = loads(tx)
        tempids = {}
        for form in forms:
            if form[0] == ':db/add' and isinstance(form[1], str) and form[1] not in tempids:
                tempids[form[1]] = self.next_id + len(tempids)
        idents = {str(i): e for e, i in self.idents}
        attrs = {str(n): (a, t) for a, n, t in self.attributes}
        def resolve(value):
            return tempids.get(value, idents.get(str(value), value)) if isinstance(value, str) else value
        data = []
        entities = copy.deepcopy(self.entities)
        kp = copy.deepcopy(self.kp)
        for form in forms:
            if form[0] != ':db/add':
                continue
            _, entity, attr, value = form
            eid = resolve(entity)
            aid, atype = attrs[str(attr)]
            value = resolve(value) if atype == ':db.type/ref' else value
            if str(attr) == ':knowledge-point/question-generator' and kp.get(str(attr)):
                data.append([eid, aid, kp[str(attr)][':db/id'], self.basis + 1, idents[flags['--source']], False])
            data.append([eid, aid, value, self.basis + 1, idents[flags['--source']], True])
            target = entities.setdefault(eid, {':db/id': eid})
            if str(attr) in (':answer-field/choices', ':question/answer-fields', ':knowledge-point/questions'):
                target.setdefault(str(attr), []).append(value)
            else:
                target[str(attr)] = value
        report = {':edb/committed': command == 'transact', ':edb/db-before-t': self.basis,
                  ':edb/db-after-t': self.basis + 1, ':edb/tempids': tempids, ':edb/tx-data': data}
        if command == 'transact':
            self.entities = entities
            self.basis += 1
            self.next_id += len(tempids)
            def pull(eid):
                result = copy.deepcopy(entities[eid])
                for attr, value in list(result.items()):
                    if attr in (':answer-field/choices', ':question/answer-fields'):
                        result[attr] = [pull(v) for v in value]
                    elif attr == ':answer-field/correct':
                        result[attr] = pull(value)
                    elif attr in (':answer/type', ':answer-field/type', ':question/difficulty'):
                        result[attr] = {':db/ident': next(i for e, i in self.idents if e == value)}
                return result
            delta = entities[KP]
            self.kp[':knowledge-point/questions'] += [pull(e) for e in delta.get(':knowledge-point/questions', [])]
            delta[':knowledge-point/questions'] = []
            if ':knowledge-point/question-generator' in delta:
                self.kp[':knowledge-point/question-generator'] = pull(delta[':knowledge-point/question-generator'])
            self.receipts[key] = report
            if self.lose_reply:
                self.lose_reply = False
                raise TimeoutError('reply lost after commit')
        return dumps(report)


class PublicationTests(unittest.TestCase):
    def test_radio_prompt_marker_is_rejected_before_publication(self):
        q = record()['question']
        f = q[':question/answer-fields'][0]
        f[':answer-field/type'] = ':answer-field.type/radio'
        other = copy.deepcopy(f[':answer-field/choices'][0])
        other.update({':answer/id': str(uuid.uuid4()), ':answer/value': '99'})
        f[':answer-field/choices'].append(other)
        q[':question/problem'] += '\n\n{{answer}}'
        with self.assertRaisesRegex(ValueError, 'Only blank/select'):
            validate_question(q)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.client = FakeClient()
        config = SimpleNamespace(database='math', source=':application/ca-engine', endpoint='/tmp/fake.sock',
                                 math_root=self.root / 'math', repo_root=self.root, postgres_url='fixture')
        self.publisher = Publisher(config, self.client)
        self.directory = self.root / 'publication'
        self.package = self.make_package('first')
        self.script = f'generators/{self.package[:2]}/{self.package}/generate.py'

    def test_delivery_inventory_includes_generated_stock_without_changing_instructional_identity(self):
        source = self.publisher.extract_source(KP, self.root / 'source-inventory')
        generated = record(12)['question']
        self.client.kp[':knowledge-point/questions'].append(generated)
        updated = self.publisher.extract_source(KP, self.root / 'source-inventory')
        self.assertEqual(source['source_sha256'], updated['source_sha256'])
        inventory = json.loads((self.root / 'source-inventory/inventory.json').read_text())
        self.assertEqual(inventory['basis'], self.client.basis)
        self.assertEqual(inventory['questions'], jsonable([generated]))
        self.assertIn(content_fingerprint(generated), inventory['fingerprints'])
        refreshed = self.publisher.extract_inventory(KP, self.root / 'inventory-refresh')
        self.assertEqual(refreshed, inventory)
        self.assertEqual(self.client.calls, [], 'delivery inventory extraction must not transact')

    def test_source_capture_excludes_multistep_and_retired_parts_but_retains_inventory(self):
        good=record()['question'];bad=record(3)['question']
        good.update({':db/id':800,':question/math-academy-id':'q-800'})
        bad.update({':db/id':801,':question/math-academy-id':'q-167637',':question/difficulty':':question.difficulty/hard'})
        self.client.kp[':knowledge-point/questions']=[good,bad]
        self.client.excluded_sources=[{':db/id':801,':question/id':bad[':question/id'],':question/math-academy-id':'q-167637'}]
        source=self.publisher.extract_source(KP,self.root/'source-filtered')
        self.assertEqual(source['material']['kp'][':knowledge-point/questions'],[good])
        self.assertEqual(source['available_difficulties'],['easy'])
        self.assertEqual(len(json.loads((self.root/'source-filtered/inventory.json').read_text())['questions']),2)
        previous=copy.deepcopy(source)
        previous['material'].pop('source_eligibility')
        previous['material']['kp'][':knowledge-point/questions'].append(bad)
        previous['source_sha256']=digest(previous['material'])
        with self.assertRaises(SourceChanged):
            self.publisher.prepare(KP,[record()],self.script,self.package,self.directory,source_snapshot=previous)

    def test_manual_publication_also_rejects_a_multistep_descendant(self):
        self.client.excluded_sources=[{':db/id':801,':question/id':str(uuid.uuid4()),':question/math-academy-id':'q-167637'}]
        generated=record();generated['generation']['source_ids']=['q-167637']
        with self.assertRaisesRegex(ValueError,'excluded standalone source'):
            self.prepare([generated])
        self.assertFalse(any(c[0]=='transact' for c in self.client.calls))

    def tearDown(self):
        self.temp.cleanup()

    def make_package(self, text):
        source = self.root / ('source-' + text)
        source.mkdir()
        (source / 'generate.py').write_text('# ' + text + '\n')
        return publish_package(source, 'generate.py', ['generate.py'], self.root / 'math').digest

    def prepare(self, records=None, package=None):
        package = package or self.package
        return self.publisher.prepare(KP, records if records is not None else [record()],
                                      f'generators/{package[:2]}/{package}/generate.py', package, self.directory)

    def test_normalized_duplicates_reuse_existing_without_content_writes(self):
        prepared = self.prepare([record(), record()])
        self.assertEqual(prepared['new_questions'], 1)
        self.assertEqual(prepared['duplicates'], 1)
        result = self.publisher.publish(self.directory)
        self.assertEqual(result['status'], 'verified')
        self.assertEqual(len(self.client.kp[':knowledge-point/questions']), 1)
        prepared = self.prepare([record()])
        self.assertEqual(prepared['new_questions'], 0)
        self.assertEqual(loads(prepared['batch_edn'])['forms'], [])
        result = self.publisher.publish(self.directory)
        self.assertEqual(result['status'], 'no_changes')

    def test_entered_blank_responses_do_not_defeat_content_deduplication(self):
        self.prepare()
        self.publisher.publish(self.directory)
        field = self.client.kp[':knowledge-point/questions'][0][':question/answer-fields'][0]
        field[':answer-field/choices'].append({':db/id': 909, ':answer/id': uuid.uuid4(),
            ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': 'wrong entered response'})
        prepared = self.prepare([record()])
        self.assertEqual(prepared['new_questions'], 0)
        self.assertEqual(prepared['duplicates'], 1)

    def test_lost_reply_retries_exact_request_after_database_advances(self):
        self.prepare()
        self.client.lose_reply = True
        with self.assertRaises(TimeoutError):
            self.publisher.publish(self.directory)
        original = json.loads((self.directory / 'request.json').read_text())
        with self.assertRaisesRegex(ValueError, 'Recover pending'):
            self.prepare()
        result = self.publisher.publish(self.directory)
        submissions = [call for call in self.client.calls if call[0] == 'transact']
        self.assertEqual(len(submissions), 2)
        self.assertEqual(submissions[0], submissions[1])
        self.assertEqual(result['request_key'], original['request_key'])
        self.assertEqual(len(self.client.kp[':knowledge-point/questions']), 1)
        count = len(self.client.calls)
        self.publisher.publish(self.directory)
        self.assertEqual(count, len(self.client.calls))

    def test_confirmed_commit_with_failed_readback_recovers_receipt(self):
        self.prepare()
        self.client.fail_readback = True
        with self.assertRaises(ConnectionError):
            self.publisher.publish(self.directory)
        self.assertTrue((self.directory / 'request.json').exists())
        self.publisher.publish(self.directory)
        self.assertEqual(sum(c[0] == 'transact' for c in self.client.calls), 1)

    def test_confirmed_stale_rejection_retires_request(self):
        self.prepare()
        self.client.reject_stale = True
        with self.assertRaises(StaleBasis):
            self.publisher.publish(self.directory)
        self.assertFalse((self.directory / 'request.json').exists())
        self.assertEqual(len(list((self.directory / 'requests').glob('*/result.json'))), 1)

    def test_package_replacement_retains_old_generator(self):
        self.prepare()
        self.publisher.publish(self.directory)
        old_id = self.client.kp[':knowledge-point/question-generator'][':db/id']
        self.prepare([], self.make_package('second'))
        self.publisher.publish(self.directory)
        self.assertIn(old_id, self.client.entities)
        self.assertEqual(self.client.entities[old_id][':question-generator/script'], self.script)
        self.assertNotEqual(self.client.kp[':knowledge-point/question-generator'][':db/id'], old_id)

    def test_edited_preparation_cannot_replace_pending_request(self):
        self.prepare()
        self.client.lose_reply = True
        with self.assertRaises(TimeoutError):
            self.publisher.publish(self.directory)
        path = self.directory / 'preparation.json'
        value = json.loads(path.read_text())
        value['package_sha256'] = 'e' * 64
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(VerificationError, 'preparation changed'):
            self.publisher.publish(self.directory)

    def test_source_change_requires_review_again(self):
        source = self.publisher.extract_source(KP, self.root / 'source')
        self.client.kp[':knowledge-point/title'] = 'Different method'
        with self.assertRaisesRegex(ValueError, 'source changed'):
            self.publisher.prepare(KP, [record()], self.script, self.package, self.directory, source_snapshot=source)

    def test_prepare_reuses_fresh_kp_pull_for_source_check(self):
        source = self.publisher.extract_source(KP, self.root / 'source')
        with patch.object(self.publisher, 'read_kp', wraps=self.publisher.read_kp) as pull, \
                patch.object(self.client, 'status', wraps=self.client.status) as status:
            self.publisher.prepare(KP, [record()], self.script, self.package, self.directory, source_snapshot=source)
        pull.assert_called_once_with(KP, self.directory / 'before', self.client.basis)
        status.assert_called_once_with()
        fresh = json.loads((self.directory / 'source-check/source.json').read_text())
        self.assertEqual(fresh, source)

    def test_refill_cannot_replace_a_changed_registration(self):
        self.client.kp[':knowledge-point/question-generator'] = {
            ':db/id': 77, ':question-generator/script': 'generators/newer/generate.py'}
        with self.assertRaisesRegex(ValueError, 'Registered generator changed'):
            self.publisher.prepare(KP, [record()], self.script, self.package, self.directory,
                                   expected_registered_generator=self.script)
        self.assertEqual(self.client.calls, [])
        self.assertFalse((self.directory / 'request.json').exists())

    def test_refill_accepts_unchanged_registration(self):
        self.client.kp[':knowledge-point/question-generator'] = {
            ':db/id': 77, ':question-generator/script': self.script}
        result = self.publisher.prepare(KP, [record()], self.script, self.package, self.directory,
                                        expected_registered_generator=self.script)
        self.assertEqual(result['new_questions'], 1)

    def test_images_are_localized_and_verified_after_commit(self):
        from PIL import Image
        image = self.root / 'figure.png'
        Image.new('RGB', (2, 2), 'red').save(image)
        rec = record()
        rec['question'][':question/problem'] += f' ![]({image})'
        field = rec['question'][':question/answer-fields'][0]
        field[':answer-field/type'] = ':answer-field.type/radio'
        field[':answer-field/choices'].append({':answer/id': str(uuid.uuid4()), ':answer/type': ':answer.type/text', ':answer/value': 'None of these'})
        answer = field[':answer-field/choices'][0]
        answer[':answer/type'] = ':answer.type/image'
        answer[':answer/value'] = str(image)
        prepared = self.prepare([rec])
        localized = prepared['records'][0]['question']
        value = localized[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
        self.assertEqual(value, f'images/{hashlib.sha256(image.read_bytes()).hexdigest()[:2]}/{hashlib.sha256(image.read_bytes()).hexdigest()}.png')
        self.assertIn(value, localized[':question/problem'])
        self.publisher.publish(self.directory)

    def test_corrupted_published_asset_is_rejected_before_commit(self):
        from PIL import Image
        image = self.root / 'figure.png'
        Image.new('RGB', (2, 2), 'blue').save(image)
        rec = record()
        rec['question'][':question/problem'] += f' ![]({image})'
        prep = self.prepare([rec])
        asset = next(iter(prep['records'][0]['assets'].values()))
        (self.root / 'math' / asset['path']).write_bytes(b'corrupt')
        with self.assertRaises(VerificationError):
            self.publisher.publish(self.directory)
        self.assertFalse((self.directory / 'request.json').exists())
        self.assertFalse(any(c[0] == 'transact' for c in self.client.calls))

    def test_incomplete_committed_receipt_is_recovered_with_original_request(self):
        self.prepare()
        self.client.fail_readback = True
        with self.assertRaises(ConnectionError):
            self.publisher.publish(self.directory)
        path = self.directory / 'receipt-request.json'
        envelope = json.loads(path.read_text())
        envelope['receipt_edn'] = dumps({kw('edb/committed'): True, kw('edb/report-error'): 'storage/read-failed'})
        path.write_text(json.dumps(envelope))
        self.publisher.publish(self.directory)
        submissions = [c for c in self.client.calls if c[0] == 'transact']
        self.assertEqual(len(submissions), 2)
        self.assertEqual(submissions[0], submissions[1])
        self.assertTrue((self.directory / 'receipt-incomplete.json').exists())

    def test_source_hash_ignores_operational_lesson_pool_and_registration_refs(self):
        self.client.lessons = [{':db/id': 700, ':activity/steps': [{':db/id': 701, ':step/content': {
            ':knowledge-point/id': KP_UUID, ':knowledge-point/title': 'Add one',
            ':knowledge-point/questions': [{':db/id': 800}], ':knowledge-point/question-generator': {':db/id': 900}}}]}]
        source = self.publisher.extract_source(KP, self.root / 'source-first')
        content = self.client.lessons[0][':activity/steps'][0][':step/content']
        content[':knowledge-point/questions'].append({':db/id': 801})
        content[':knowledge-point/question-generator'] = {':db/id': 901}
        fresh = self.publisher.extract_source(KP, self.root / 'source-again')
        self.assertEqual(source['source_sha256'], fresh['source_sha256'])
        # Previously captured evidence may include operational refs. Its own
        # hash must still verify before applying the instructional projection.
        older = copy.deepcopy(source)
        old_content = older['material']['lessons'][0][':activity/steps'][0][':step/content']
        old_content[':knowledge-point/questions'] = [{':db/id': 800}]
        old_content[':knowledge-point/question-generator'] = {':db/id': 900}
        older['source_sha256'] = digest(older['material'])
        self.publisher.prepare(KP, [record()], self.script, self.package, self.directory, source_snapshot=older)
        old_content[':knowledge-point/title'] = 'Unreviewed change'
        with self.assertRaisesRegex(ValueError, 'integrity check'):
            self.publisher.prepare(KP, [record()], self.script, self.package, self.directory, source_snapshot=older)

    def test_no_change_preparation_rechecks_current_database_basis(self):
        self.prepare()
        self.publisher.publish(self.directory)
        self.prepare([])
        self.client.basis += 1
        with self.assertRaises(StaleBasis):
            self.publisher.publish(self.directory)

    def test_changed_generator_package_is_rejected_before_commit(self):
        self.prepare()
        entrypoint = self.root / 'math' / self.script
        entrypoint.chmod(0o644)
        entrypoint.write_text('# changed after review\n')
        with self.assertRaisesRegex(ValueError, 'file changed'):
            self.publisher.publish(self.directory)
        self.assertFalse(any(c[0] == 'transact' for c in self.client.calls))

    def test_existing_question_identity_cannot_be_overwritten(self):
        rec = record()
        normalized = stable_identities(rec['question'], KP_UUID)
        self.client.entities[902] = {':question/id': uuid.UUID(normalized[':question/id'])}
        with self.assertRaisesRegex(ValueError, 'Existing identities'):
            self.prepare([rec])

    def test_configured_request_directory_is_used(self):
        self.publisher.config.request_directory = self.root / 'different-lock'
        self.prepare()
        self.publisher.publish(self.directory)
        self.assertTrue((self.root / 'different-lock/api.lock').exists())

    def test_unexpected_receipt_datoms_fail_exact_verification(self):
        prepared = self.prepare()
        batch = loads(prepared['batch_edn'])
        snapshot = loads(prepared['snapshot_edn'])
        self.publisher.publish(self.directory)
        receipt = copy.deepcopy(next(iter(self.client.receipts.values())))
        receipt[':edb/tx-data'].append([KP, 999999, 'unexpected', 13, 100, True])
        with self.assertRaisesRegex(VerificationError, 'protected or unknown'):
            validate_report(receipt, batch, snapshot, committed=True)

    def test_generator_knowledge_point_metadata_envelope_is_supported(self):
        for metadata in ({'db_id': KP, 'id': str(KP_UUID), 'title': 'Add one'},
                         {'db_id': str(KP)}, {'id': str(KP_UUID)}):
            with self.subTest(metadata=metadata):
                rec = record()
                rec['knowledge_point'] = metadata
                self.assertEqual(self.prepare([rec])['new_questions'], 1)

    def test_conflicting_or_unidentified_knowledge_point_metadata_is_rejected(self):
        for metadata in ({'db_id': KP + 1, 'id': str(KP_UUID)},
                         {'db_id': KP, 'id': str(uuid.uuid4())},
                         {'title': 'Add one'}, {}, {'db_id': None},
                         {'db_id': float(KP)}, {'id': 'not-a-uuid'}):
            with self.subTest(metadata=metadata):
                rec = record()
                rec['knowledge_point'] = metadata
                with self.assertRaises(ValueError):
                    self.prepare([rec])

    def test_missing_correct_answer_and_source_id_are_rejected(self):
        rec = record()
        rec['question'][':question/answer-fields'][0][':answer-field/correct'][1] = str(uuid.uuid4())
        with self.assertRaisesRegex(ValueError, 'Canonical answer'):
            self.prepare([rec])
        rec = record()
        rec['question'][':question/math-academy-id'] = 'q-10'
        with self.assertRaisesRegex(ValueError, 'source identity'):
            self.prepare([rec])


class NonemptyCheckboxPublicationTests(unittest.TestCase):
    def checkbox_question(self, values):
        q = record()['question']
        fields = []
        for index, expected in enumerate(values):
            fid = uuid.uuid4()
            choices = [{':answer/id': str(uuid.uuid5(fid, value)),
                        ':answer/type': ':answer.type/text', ':answer/value': value}
                       for value in ('false', 'true')]
            fields.append({':answer-field/id': str(fid), ':answer-field/key': f'Option {index}',
                           ':answer-field/type': ':answer-field.type/checkbox',
                           ':answer-field/choices': choices,
                           ':answer-field/correct': [':answer/id', choices[int(expected)][':answer/id']]})
        q[':question/answer-fields'] = fields
        return q

    def test_empty_checkbox_subset_is_rejected_before_publication(self):
        for size in (1, 3, 5):
            with self.subTest(size=size):
                with self.assertRaisesRegex(ValueError, 'at least one correct selectable option'):
                    validate_question(self.checkbox_question([False] * size))

    def test_nonempty_checkbox_subsets_are_publishable_in_both_pull_shapes(self):
        for mask in ([True], [False, True, False], [True, True, True]):
            q = self.checkbox_question(mask)
            validate_question(q)
            for f in q[':question/answer-fields']:
                aid = f[':answer-field/correct'][1]
                f[':answer-field/correct'] = next(a for a in f[':answer-field/choices'] if a[':answer/id'] == aid)
            validate_question(q)


class ExemplarPublicationTests(unittest.TestCase):
    setUp = PublicationTests.setUp
    tearDown = PublicationTests.tearDown
    make_package = PublicationTests.make_package

    def records(self):
        result = [record(number) for number in (21, 32, 43)]
        for item, band in zip(result, ('easy', 'moderate', 'hard')):
            item['question'][':question/difficulty'] = ':question.difficulty/' + band
        return result

    def publish_exemplars(self, records=None, directory=None):
        return self.publisher.publish_exemplars(KP, self.records() if records is None else records,
            directory or self.directory)

    def test_three_complete_questions_use_agent_provenance_without_registration_or_original_edits(self):
        original = {':db/id': 410, ':question/id': uuid.uuid4(), ':question/math-academy-id': 'q-410',
            ':question/problem': 'An incomplete imported question', ':question/difficulty': ':question.difficulty/moderate',
            ':question/answer-fields': [{':db/id': 411, ':answer-field/choices': [{':db/id': 412}]}]}
        self.client.kp[':knowledge-point/questions'].append(original)
        registration = {':db/id': 500, ':question-generator/id': uuid.uuid4(), ':question-generator/script': self.script}
        self.client.kp[':knowledge-point/question-generator'] = registration
        before = copy.deepcopy(self.client.kp)
        result = self.publish_exemplars()
        self.assertEqual(result['new_questions'], 3)
        self.assertEqual(result['source'], ':agent/codex')
        self.assertEqual(self.client.kp[':knowledge-point/questions'][0], before[':knowledge-point/questions'][0])
        self.assertEqual(self.client.kp[':knowledge-point/question-generator'], before[':knowledge-point/question-generator'])
        self.assertEqual(len(result['questions']), 3)
        self.assertEqual({enum(q[':question/difficulty']) for q in result['questions']},
            {':question.difficulty/' + band for band in ('easy', 'moderate', 'hard')})
        for question in result['questions']:
            validate_question(question)
            self.assertNotIn(':question/math-academy-id', question)
            self.assertTrue(all(key.startswith((':question/', ':db/')) for key in question))
        self.assertEqual(result['fresh_source']['material']['kp'][':knowledge-point/questions'], jsonable([original]))
        self.assertEqual(result['fresh_source']['available_difficulties'], ['moderate'])
        transaction = next(call for call in self.client.calls if call[0] == 'transact')
        self.assertEqual(transaction[2]['--source'], ':agent/codex')
        self.assertNotIn(':question-generator/', transaction[1])
        self.assertNotIn(':db/retract', transaction[1])

    def test_identical_exemplars_reuse_questions_across_new_directories_and_random_input_ids(self):
        first = self.publish_exemplars()
        count = sum(call[0] == 'transact' for call in self.client.calls)
        second = self.publish_exemplars(directory=self.root / 'next-investigation')
        self.assertEqual(second['status'], 'no_changes')
        self.assertEqual(second['new_questions'], 0)
        self.assertEqual([q[':question/id'] for q in first['questions']], [q[':question/id'] for q in second['questions']])
        self.assertEqual(sum(call[0] == 'transact' for call in self.client.calls), count)
        self.assertEqual(len(self.client.kp[':knowledge-point/questions']), 3)

    def test_lost_reply_recovers_exact_saved_exemplars_before_new_input(self):
        self.client.lose_reply = True
        with self.assertRaises(TimeoutError):
            self.publish_exemplars()
        request = json.loads((self.directory / 'request.json').read_text())
        changed = self.records()
        changed[0]['question'][':question/worked-solution'] = 'Changed after the unknown outcome.'
        result = self.publish_exemplars(changed)
        submissions = [call for call in self.client.calls if call[0] == 'transact']
        self.assertEqual(submissions[0], submissions[1])
        self.assertEqual(result['request_key'], request['request_key'])
        self.assertEqual(len(self.client.kp[':knowledge-point/questions']), 3)
        self.assertNotEqual(result['questions'][0][':question/worked-solution'], changed[0]['question'][':question/worked-solution'])

    def test_exemplar_readback_failure_recovers_confirmed_receipt_without_second_write(self):
        self.client.fail_readback = True
        with self.assertRaises(ConnectionError):
            self.publish_exemplars()
        self.assertTrue((self.directory / 'request.json').exists())
        result = self.publish_exemplars()
        self.assertTrue(result['passed'])
        self.assertEqual(sum(call[0] == 'transact' for call in self.client.calls), 1)

    def test_incomplete_exemplar_is_rejected_without_changing_incomplete_imports(self):
        records = self.records()
        records[1]['question'][':question/answer-fields'][0].pop(':answer-field/correct')
        with self.assertRaisesRegex(ValueError, 'Canonical answer'):
            self.publish_exemplars(records)
        self.assertFalse(any(call[0] == 'transact' for call in self.client.calls))

    def test_exactly_one_of_each_difficulty_is_required(self):
        records = self.records()
        records[2]['question'][':question/difficulty'] = ':question.difficulty/moderate'
        with self.assertRaisesRegex(ValueError, 'exactly one easy, moderate, and hard'):
            self.publish_exemplars(records)
        self.assertEqual(self.client.calls, [])

    def test_missing_agent_source_cannot_silently_use_application_source(self):
        self.client.idents = [row for row in self.client.idents if row[1] != ':agent/codex']
        with self.assertRaisesRegex(ValueError, 'Investigator contributor does not exist'):
            self.publish_exemplars()
        self.assertFalse(any(call[0] == 'transact' for call in self.client.calls))

    def test_changed_existing_exemplar_is_not_overwritten(self):
        self.publish_exemplars()
        self.client.kp[':knowledge-point/questions'][0][':question/worked-solution'] = 'Externally changed.'
        count = sum(call[0] == 'transact' for call in self.client.calls)
        with self.assertRaisesRegex(VerificationError, 'different content'):
            self.publish_exemplars(directory=self.root / 'new-attempt')
        self.assertEqual(sum(call[0] == 'transact' for call in self.client.calls), count)


if __name__ == '__main__':
    unittest.main()

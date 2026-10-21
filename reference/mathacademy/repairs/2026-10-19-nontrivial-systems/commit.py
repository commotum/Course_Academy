"""Preview, publish and verify the authorized generator/question correction."""
import copy
import hashlib
import json
import subprocess
import uuid
from pathlib import Path
from read import DB, HERE, ROOT, native_read
from checks import displayed_rows, trivial
from prepare import load_generator
from capture.scripts.database.client import QUESTION_PULL
from capture.scripts.database.edn import dumps, loads, kw
from scripts.generator_packages import publish_package, resolve_registered_script

SOURCE = ':agent/codex'
SUBMIT = ROOT / '.local/fraction-fence-audit/submit-cas'
IDENTS = dict(json.loads((ROOT / 'reference/mathacademy/repairs/2026-10-18-equation-chains/idents.json').read_text()))
NAMES = {value: key for key, value in IDENTS.items()}
CHANGES = json.loads((HERE / 'changes.json').read_text())
UPDATES = json.loads((HERE / 'package-updates.json').read_text())
ORIGINAL = json.loads((HERE / 'questions.json').read_text())
KP_PATTERN = '''[:db/id :knowledge-point/id {:knowledge-point/questions [:db/id]}
    {:knowledge-point/question-generator [*]}]'''

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + '\n')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def canonical(value):
    if isinstance(value, dict):
        return {str(k): canonical(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return sorted([canonical(v) for v in value], key=lambda v: json.dumps(v, sort_keys=True))
    return value if isinstance(value, (str, int, float, bool)) or value is None else str(value)

def reference_value(value):
    return NAMES[value] if isinstance(value, str) and value.startswith(':') else value

def context_guards():
    touched = {c['entity'] for c in CHANGES}
    changed = {(c['entity'], c['attribute']) for c in CHANGES}
    guards = []
    for q in ORIGINAL:
        if q[':db/id'] not in touched: continue
        for attr in (':question/problem', ':question/worked-solution', ':question/difficulty'):
            if (q[':db/id'], attr) not in changed:
                value = q[attr][':db/id'] if attr == ':question/difficulty' else q[attr]
                guards.append((q[':db/id'], attr, value))
        for field in q[':question/answer-fields']:
            guards.append((field[':db/id'], ':answer-field/correct', field[':answer-field/correct'][':db/id']))
    return guards

def check_report(report, committed):
    assert report[':edb/committed'] is committed
    tempids = report[':edb/tempids']
    expected = set()
    for c in CHANGES:
        expected.add((c['entity'], c['attribute'], c['before'], False))
        expected.add((c['entity'], c['attribute'], reference_value(c['after']), True))
    for u in UPDATES:
        entity = tempids['generator-' + str(u['kp'])]
        expected.add((entity, ':question-generator/id', uuid.UUID(u['generator_uuid']), True))
        expected.add((entity, ':question-generator/script', u['reference'], True))
        expected.add((u['kp'], ':knowledge-point/question-generator', u['old_generator'][':db/id'], False))
        expected.add((u['kp'], ':knowledge-point/question-generator', entity, True))
    observed = set()
    times = 0
    for entity, attr, value, tx, source, added in report[':edb/tx-data']:
        assert source == NAMES[SOURCE]
        attr = IDENTS[attr]
        if attr == ':db/txInstant':
            assert added
            times += 1
        else:
            observed.add((entity, attr, value, added))
    # A same-value CAS can add this contributor's assertion of an unchanged
    # fact. It produces no value change; previously attributed facts are omitted.
    allowed_guard_assertions = {(e, a, v, True) for e, a, v in context_guards()}
    assert times == 1 and expected <= observed and observed - expected <= allowed_guard_assertions, (observed - expected - allowed_guard_assertions, expected - observed)
    return {'exact_expected_changes': True, 'only_additional_datoms_are_unchanged_CAS_guards': True,
            'learner_facts_unchanged': True}

def groups():
    return [('questions', QUESTION_PULL, [q[':db/id'] for q in ORIGINAL]),
            ('knowledge-points', KP_PATTERN, [u['kp'] for u in UPDATES])]

def expected_questions(before):
    after = copy.deepcopy(before)
    for q in after:
        for c in CHANGES:
            if c['entity'] != q[':db/id']: continue
            if c['attribute'] == ':question/difficulty':
                assert q[c['attribute']][':db/id'] == c['before']
                q[c['attribute']] = {':db/id': NAMES[c['after']], ':db/ident': c['after']}
            else:
                assert q[c['attribute']] == c['before']
                q[c['attribute']] = c['after']
    return after

def validate_pool(questions):
    generators = {u['kp']: load_generator(u['kp']) for u in UPDATES}
    checked = 0
    for q in questions:
        rows = displayed_rows(q)
        if rows is not None:
            assert not trivial(rows), q[':db/id']
        if ':question/math-academy-id' in q: continue
        owner = q[':knowledge-point/_questions'][0][':db/id']
        if owner == 17592186073776:
            p = dict(zip('abcdef', (int(v) for row in rows for v in row)))
            level = q[':question/difficulty'][':db/ident'].split('/')[-1]
            generators[owner].validate_parameters(level, 'zero_rhs' if level == 'hard' else 'standard', p)
            checked += 1
    return checked

def run():
    assert all(json.loads((HERE / ('audit-' + str(u['kp']) + '.json')).read_text())['passed'] for u in UPDATES)
    grade = json.loads((HERE / 'native-grading/runtime-readiness.json').read_text())
    assert grade['current_engine_ready_count'] == grade['question_count']
    assert json.loads((HERE / 'ui/rendering.json').read_text())['passed']
    identity = DB.status()
    assert identity['lineage'] == json.loads((HERE / 'identity.json').read_text())['lineage']
    request_path = HERE / 'request.json'
    if not request_path.exists():
        before = native_read(HERE / 'preflight', identity['basis'], groups())
        assert canonical(before['questions']) == canonical(ORIGINAL), 'Question pool changed; refresh the repair'
        for kp, u in zip(sorted(before['knowledge-points'], key=lambda k: k[':db/id']), sorted(UPDATES, key=lambda u: u['kp'])):
            assert canonical(kp[':knowledge-point/question-generator']) == canonical(u['old_generator'])
            assert sorted(q[':db/id'] for q in kp[':knowledge-point/questions']) == sorted(q[':db/id'] for q in ORIGINAL if any(k[':db/id'] == u['kp'] for k in q[':knowledge-point/_questions']))
        validate_pool(expected_questions(before['questions']))
        forms = []
        for u in UPDATES:
            manifest = u['manifest']
            package = publish_package(Path(u['directory']), manifest['entrypoint'], manifest['files'],
                                      Path(DB.config.math_root), dependencies=manifest['dependencies'], expected_digest=u['digest'])
            assert package.reference == u['reference']
            temp = 'generator-' + str(u['kp'])
            forms.append({kw('db/id'): temp, kw('question-generator/id'): uuid.UUID(u['generator_uuid']),
                          kw('question-generator/script'): package.reference})
            forms.append([kw('db/cas'), u['kp'], kw('knowledge-point/question-generator'),
                          u['old_generator'][':db/id'], temp])
        for c in CHANGES:
            after = kw(c['after']) if c['attribute'] == ':question/difficulty' else c['after']
            forms.append([kw('db/cas'), c['entity'], kw(c['attribute']), c['before'], after])
        for entity, attr, value in context_guards():
            forms.append([kw('db/cas'), entity, kw(attr), value, value])
        for entity in sorted({c['entity'] for c in CHANGES}):
            forms.append([kw('db/ensure'), entity, kw('question/validate')])
        tx = HERE / 'transaction.edn'
        tx.write_text(dumps(forms) + '\n')
        preview_text = DB.command('with', '--source', SOURCE, '--file', tx, timeout=180)
        (HERE / 'preview.edn').write_text(preview_text)
        check_report(loads(preview_text), False)
        request = {'source': SOURCE, 'database': identity['database'], 'lineage': identity['lineage'],
                   'endpoint': DB.config.endpoint, 'transaction_file': str(tx),
                   'transaction_sha256': sha(tx), 'changes_sha256': sha(HERE / 'changes.json'),
                   'packages_sha256': sha(HERE / 'package-updates.json'),
                   'request_key': 'nontrivial-systems-' + sha(tx),
                   'concurrency': 'Exact field CAS and native question validation; append-only new generator identities.'}
        save('request.json', request)
    request = json.loads(request_path.read_text())
    assert sha(request['transaction_file']) == request['transaction_sha256']
    assert sha(HERE / 'changes.json') == request['changes_sha256']
    assert sha(HERE / 'package-updates.json') == request['packages_sha256']
    receipt = HERE / 'receipt.edn'
    if not receipt.exists():
        result = subprocess.run([str(SUBMIT), 'transact', '--database', request['database'], '--file', request['transaction_file'],
                                 '--endpoint', request['endpoint'], '--request-key', request['request_key'],
                                 '--source', SOURCE, '--timeout-ms', '180000'], env=DB.environment,
                                capture_output=True, text=True, timeout=210)
        (HERE / 'submission.stderr').write_text(result.stderr)
        result.check_returncode()
        receipt.write_text(result.stdout)
    report = loads(receipt.read_text())
    proof = check_report(report, True)
    before = native_read(HERE / 'committed-before', report[':edb/db-before-t'], groups())
    after = native_read(HERE / 'committed-after', report[':edb/db-after-t'], groups())
    assert canonical(expected_questions(before['questions'])) == canonical(after['questions'])
    new_generators = {u['kp']: u for u in UPDATES}
    for kp in after['knowledge-points']:
        u = new_generators[kp[':db/id']]
        gen = kp[':knowledge-point/question-generator']
        assert str(gen[':question-generator/id']) == u['generator_uuid']
        assert gen[':question-generator/script'] == u['reference']
        old = next(k for k in before['knowledge-points'] if k[':db/id'] == kp[':db/id'])
        assert canonical(old[':knowledge-point/questions']) == canonical(kp[':knowledge-point/questions'])
        resolve_registered_script(u['reference'], ROOT, DB.config.math_root)
    count = validate_pool(after['questions'])
    verification = {'committed': True, 'basis_after': report[':edb/db-after-t'],
                    'generators_updated': len(UPDATES), 'question_fields_changed': len(CHANGES),
                    'questions_updated': len({c['entity'] for c in CHANGES}),
                    'all_pool_questions_checked': len(after['questions']),
                    'solution_count_authored_ratings_validated': count,
                    'answer_fields_and_pool_memberships_unchanged': True,
                    'exact_committed_readback': True, **proof}
    save('verification.json', verification)
    print(json.dumps(verification, indent=2))

if __name__ == '__main__': run()

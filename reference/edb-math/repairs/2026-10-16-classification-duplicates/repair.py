"""Repair two question texts and atomically register new immutable generator versions."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import uuid

sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from scripts.generator_packages import resolve_registered_script
from capture.scripts.database.edn import dumps, loads, kw
from capture.scripts.database.client import StaleBasis

HERE = Path(__file__).resolve().parent
SOURCE = ':agent/gpt-6.1-sol-high'
PUBLISHER = Publisher.from_environment(source=SOURCE)
DB = PUBLISHER.client
BASE = loads((ROOT / (HERE / 'capture-directory.txt').read_text().strip() / 'snapshot.edn').read_text())
PATTERNS = BASE['patterns']
NATIVE = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'


def save(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')


def normalized(value):
    if isinstance(value, dict): return {str(k): normalized(v) for k, v in value.items()}
    if isinstance(value, list): return sorted((normalized(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True, default=str))
    return str(value) if isinstance(value, uuid.UUID) else value


def module(path, name):
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        result = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(result)
        return result
    finally:
        sys.path.pop(0)


def prepare(directory):
    packages = json.loads((HERE / 'published-packages.json').read_text())
    assert packages['all_verified'] and packages['old_packages_unchanged']
    identity = DB.status()
    assert identity['lineage'] == BASE['lineage']
    basis = identity['basis']
    ids = sorted(q[':db/id'] for [q] in BASE['questions'])
    kids = sorted(kp[':db/id'] for [kp] in BASE['scope'])

    def read(name, query, inputs):
        return DB.query(query, inputs, directory / 'evidence', name, basis)

    queries = {
        'questions': ('[:find (pull ?q ' + PATTERNS['questions'] + ') :in $ [?q ...] :where [?q :question/id _]]', [ids]),
        'items': ('[:find ?q (pull ?i ' + PATTERNS['items'] + ') :in $ [?q ...] :where [?i :task-item/content ?q]]', [ids]),
        'scope': ('[:find (pull ?kp ' + PATTERNS['scope'] + ') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]', [kids]),
        'attributes': ('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]', []),
        'source': ('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]', [kw(SOURCE)]),
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {name: pool.submit(read, name, *args) for name, args in queries.items()}
        data = {name: future.result() for name, future in futures.items()}
    assert normalized(data['questions']) == normalized(BASE['questions']), 'Reviewed question content changed'
    assert normalized(data['scope']) == normalized(BASE['scope']), 'Reviewed KP scope or generator registration changed'
    assert len(data['source']) == 1
    questions = {q[':db/id']: q for [q] in data['questions']}
    kps = {kp[':db/id']: kp for [kp] in data['scope']}
    changes, registrations, forms = [], [], []
    for package in packages['packages']:
        kid = package['kp_id']
        kp = kps[kid]
        old = kp[':knowledge-point/question-generator']
        assert old[':db/id'] == package['old_generator_eid'] and old[':question-generator/script'] == package['old_reference']
        old_path = resolve_registered_script(package['old_reference'], ROOT, PUBLISHER.config.math_root)
        new_path = resolve_registered_script(package['reference'], ROOT, PUBLISHER.config.math_root)
        original = module(old_path, f'original_{kid}')
        replacement = module(new_path, f'replacement_{kid}')
        if kid == 17592186198347:
            qid = 17592186567796
            before = original.generate(4, 9, 4, 9, False)['question']
            after = replacement.generate(4, 9, 4, 9, False)['question']
            kept = replacement.generate(-4, 1, -4, 1, True)['question']
            for attr in (':question/problem', ':question/worked-solution'):
                assert kept[attr] == questions[17592186567774][attr]
        else:
            assert kid == 17592186198348
            qid = 17592186567832
            before = original.generate((-2, -3, -9, -2, -3, -9), 'standard')['question']
            after = replacement.generate((-2, -3, -9, -4, -6, -18), 'standard')['question']
        actual = questions[qid]
        assert [p[':db/id'] for p in actual[':knowledge-point/_questions']] == [kid]
        assert after[':question/difficulty'] == actual[':question/difficulty'][':db/ident']
        for attr in (':question/problem', ':question/worked-solution'):
            assert actual[attr] == before[attr], (qid, attr, 'Generator replay differs from reviewed question')
            if before[attr] != after[attr]:
                change = {'entity': qid, 'attribute': attr, 'before': before[attr], 'after': after[attr]}
                changes.append(change)
                forms.append([kw('db/cas'), qid, kw(attr), before[attr], after[attr]])
        actual_fields = {f[':answer-field/key']: f for f in actual[':question/answer-fields']}
        for field in after[':question/answer-fields']:
            existing = actual_fields[field[':answer-field/key']]
            key = next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id'] == field[':answer-field/correct'][1])
            assert existing[':answer-field/correct'][':answer/value'] == key
            assert sorted(a[':answer/value'] for a in existing[':answer-field/choices']) == sorted(a[':answer/value'] for a in field[':answer-field/choices'])
            forms.append([kw('db/ensure'), existing[':db/id'], kw('answer-field/validate')])
        forms.append([kw('db/ensure'), qid, kw('question/validate')])
        generator_uuid = uuid.uuid5(kp[':knowledge-point/id'], 'generator-package:' + package['digest'])
        assert str(generator_uuid) == package['generator_uuid']
        rows = read(f'generator-identity-{kid}', '[:find (pull ?g [*]) :in $ ?uuid :where [?g :question-generator/id ?uuid]]', [generator_uuid])
        if rows:
            assert len(rows) == 1 and rows[0][0][':question-generator/script'] == package['reference']
            entity = rows[0][0][':db/id']
        else:
            entity = f'generator-{kid}'
            forms.append({kw('db/id'): entity, kw('question-generator/id'): generator_uuid,
                          kw('question-generator/script'): package['reference']})
        forms += [[kw('db/cas'), kid, kw('knowledge-point/question-generator'), old[':db/id'], entity],
                  [kw('db/ensure'), kid, kw('knowledge-point/validate')]]
        registrations.append({'kp_id': kid, 'old_eid': old[':db/id'], 'new_entity': entity,
                              'new_uuid': str(generator_uuid), 'new_reference': package['reference'],
                              'package_digest': package['digest']})
    assert len(changes) == 3 and {c['entity'] for c in changes} == {17592186567796, 17592186567832}
    groups = [['questions', PATTERNS['questions'], ids],
              ['items', PATTERNS['items'], sorted(item[':db/id'] for _, item in data['items'])],
              ['scope', PATTERNS['scope'], kids], ['old-generators', '[*]', [r['old_eid'] for r in registrations]]]
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    (directory / 'transaction.edn').write_text(dumps(forms) + '\n')
    sha = hashlib.sha256((directory / 'transaction.edn').read_bytes()).hexdigest()
    plan = {**identity, 'changes': changes, 'registrations': registrations, 'attributes': dict(data['attributes']),
            'source_eid': data['source'][0][0], 'transaction_sha256': sha}
    save(directory / 'plan.json', plan)
    (directory / 'snapshot.edn').write_text(dumps({**identity, **data}) + '\n')
    request = {**identity, 'source': SOURCE, 'endpoint': DB.config.endpoint, 'sha256': sha,
               'request_key': f'classification-no-duplicate-equations-b{basis}-{sha}',
               'transaction_file': str(directory / 'transaction.edn')}
    save(directory / 'prepared-request.json', request)
    return request


def verify_report(directory, report, committed):
    plan = json.loads((directory / 'plan.json').read_text())
    assert report[':edb/committed'] is committed and report[':edb/db-before-t'] == plan['basis']
    resolve = lambda v: report[':edb/tempids'].get(v, v) if isinstance(v, str) else v
    encoded = lambda v: json.dumps(resolve(v), sort_keys=True, default=str)
    expected = set()
    for form in loads((directory / 'transaction.edn').read_text()):
        if isinstance(form, dict):
            for attr, value in form.items():
                if attr != ':db/id': expected.add((resolve(form[':db/id']), str(attr), encoded(value), True))
        elif form[0] == ':db/cas':
            _, eid, attr, before, after = form
            expected |= {(eid, str(attr), encoded(before), False), (eid, str(attr), encoded(after), True)}
        else:
            assert form[0] == ':db/ensure'
    actual = set()
    for eid, aid, value, tx, source, added in report[':edb/tx-data']:
        assert source == plan['source_eid']
        attr = str(plan['attributes'][str(aid)])
        if attr == ':db/txInstant': assert added
        else: actual.add((eid, attr, encoded(value), added))
    assert actual == expected, (actual - expected, expected - actual)


def preview(directory, request):
    result = subprocess.run([str(NATIVE), str(directory), SOURCE, str(request['basis'])],
                            env=DB.environment, capture_output=True, text=True, timeout=150)
    (directory / 'preview.stderr').write_text(result.stderr)
    result.check_returncode()
    (directory / 'preview.edn').write_text(result.stdout)
    report = loads(result.stdout)
    verify_report(directory, report, False)
    plan = json.loads((directory / 'plan.json').read_text())
    updates = {(c['entity'], c['attribute']): c for c in plan['changes']}

    def expected(value):
        if isinstance(value, list): return [expected(v) for v in value]
        if not isinstance(value, dict): return value
        result = {k: expected(v) for k, v in value.items()}
        eid = result.get(':db/id')
        for key in list(result):
            if (eid, key) in updates:
                c = updates[eid, key]
                assert result[key] == c['before']
                result[key] = c['after']
        for r in plan['registrations']:
            if eid == r['kp_id'] and ':knowledge-point/question-generator' in result:
                entity = report[':edb/tempids'].get(r['new_entity'], r['new_entity'])
                result[':knowledge-point/question-generator'] = {':db/id': entity,
                    ':question-generator/id': r['new_uuid'], ':question-generator/script': r['new_reference']}
        return result

    for name, _, _ in loads((directory / 'native-pulls.edn').read_text()):
        before = loads((directory / f'preview-{name}-before.edn').read_text())
        after = loads((directory / f'preview-{name}-after.edn').read_text())
        assert normalized(expected(before)) == normalized(after), name
    subprocess.run([sys.executable, str(HERE / 'check_questions.py'), str(directory)], check=True)
    save(directory / 'preview-verification.json', {'passed': True, 'exact_allowed_datoms': True,
         'questions_reviewed': 16, 'questions_changed': 2, 'generator_versions_registered': 2,
         'old_generators_unchanged': True, 'learner_items_and_all_answer_fields_unchanged': True})


def execute(directory, commit):
    directory.mkdir(exist_ok=True)
    intent = directory / 'commit-intent.json'
    if intent.exists():
        request = json.loads(intent.read_text())
        if not commit: return
    else:
        if (directory / 'preview-verification.json').exists():
            request = json.loads((directory / 'prepared-request.json').read_text())
            assert json.loads((directory / 'preview-verification.json').read_text())['passed']
            verify_report(directory, loads((directory / 'preview.edn').read_text()), False)
        else:
            request = prepare(directory)
            preview(directory, request)
        if not commit: return
        save(intent, request)
    assert hashlib.sha256(Path(request['transaction_file']).read_bytes()).hexdigest() == request['sha256']
    assert DB.status()['lineage'] == request['lineage']
    receipt = directory / 'receipt.edn'
    if not receipt.exists():
        try:
            output = DB.command('transact', '--source', SOURCE, '--file', request['transaction_file'],
                '--basis', request['basis'], '--endpoint', request['endpoint'], '--request-key', request['request_key'],
                '--timeout-ms', '120000', timeout=150)
        except StaleBasis as error:
            save(directory / 'rejected.json', {'confirmed_stale_basis': True, 'reason': str(error)})
            raise
        receipt.write_text(output)
    report = loads(receipt.read_text())
    verify_report(directory, report, True)
    basis = report.get(':edb/db-after-t', report.get(':edb/basis-t'))
    speculative = loads((directory / 'preview.edn').read_text())
    mapping = {eid: report[':edb/tempids'][temp] for temp, eid in speculative[':edb/tempids'].items()}

    def durable(value):
        if isinstance(value, int): return mapping.get(value, value)
        if isinstance(value, list): return [durable(v) for v in value]
        if isinstance(value, dict): return {k: durable(v) for k, v in value.items()}
        return value

    for name, pattern, ids in loads((directory / 'native-pulls.edn').read_text()):
        query = '[:find (pull ?e ' + pattern + ') :in $ [?e ...] :where [?e _ _]]'
        actual = DB.query(query, [ids], directory / 'committed', name, basis)
        expected = durable(loads((directory / f'preview-{name}-after.edn').read_text()))
        assert normalized([q for [q] in actual]) == normalized(expected), name
        historical = DB.query(query, [ids], directory / 'committed', name + '-historical', request['basis'])
        assert normalized([q for [q] in historical]) == normalized(loads((directory / f'preview-{name}-before.edn').read_text()))
    plan = json.loads((directory / 'plan.json').read_text())
    for reg in plan['registrations']:
        resolve_registered_script(reg['new_reference'], ROOT, PUBLISHER.config.math_root)
    verification = {'committed': True, 'basis_before': request['basis'], 'basis_after': basis,
                    'lineage': request['lineage'], 'request_key': request['request_key'],
                    'transaction_sha256': request['sha256'], 'questions_updated': [17592186567796, 17592186567832],
                    'original_flagged_question_17592186567774_unchanged': True,
                    'new_generator_versions': plan['registrations'], 'old_generator_entities_and_packages_retained': True,
                    'native_grading_passed': True, 'exact_committed_and_historical_readback': True,
                    'question_field_answer_ids_difficulty_keys_and_learner_state_preserved': True,
                    'evidence_directory': str(directory.relative_to(ROOT))}
    save(directory / 'verification.json', verification)
    save(HERE / 'database-verification.json', verification)
    print(json.dumps(verification))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    execute(HERE / args.attempt, args.commit)

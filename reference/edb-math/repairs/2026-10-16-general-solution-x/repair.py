"""Scoped x-only notation repair, with retained entered answers and guarded commit."""
import argparse
import copy
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps, loads, kw, Tagged
from capture.scripts.database.client import StaleBasis

HERE = Path(__file__).resolve().parent
SOURCE = ':agent/gpt-6.1-sol-high'
DB = Publisher.from_environment(source=SOURCE).client
NATIVE = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
BASE = loads((HERE / 'capture-3261/snapshot.edn').read_text())
PATTERNS = BASE['patterns']
KP = 17592186073778


def save(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')


def by_id(rows):
    return {q[':db/id']: q for q in rows}


def normalize(value):
    if isinstance(value, dict):
        return {str(k): normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return sorted((normalize(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True, default=str))
    return str(value) if isinstance(value, uuid.UUID) else value


def rename_math(text, alias):
    return re.sub(r'(?<![A-Za-z\\])' + alias + r'(?![A-Za-z])', 'x', text)


def rename_prose(text, alias):
    return re.sub(r'\$\$.*?\$\$|\$[^$]*\$', lambda m: rename_math(m[0], alias), text, flags=re.S)


def prepare(directory):
    identity = DB.status()
    assert identity['lineage'] == BASE['lineage']
    basis = identity['basis']
    ids = sorted(q[':db/id'] for [q] in BASE['questions'])

    def read(name, query, inputs):
        return DB.query(query, inputs, directory / 'evidence', name, basis)

    queries = {
        'questions': ('[:find (pull ?q ' + PATTERNS['questions'] + ') :in $ [?q ...] :where [?q :question/id _]]', [ids]),
        'items': ('[:find ?q (pull ?i ' + PATTERNS['items'] + ') :in $ [?q ...] :where [?i :task-item/content ?q]]', [ids]),
        'scope': ('[:find (pull ?kp ' + PATTERNS['scope'] + ') :in $ ?kp :where [?kp :knowledge-point/id _]]', [KP]),
        'attributes': ('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]', []),
        'source': ('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]', [kw(SOURCE)]),
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {name: pool.submit(read, name, *args) for name, args in queries.items()}
        data = {name: future.result() for name, future in futures.items()}
    assert normalize(data['questions']) == normalize(BASE['questions']), 'Question content changed; re-review required'
    assert normalize(data['scope']) == normalize(BASE['scope']), 'KP inventory or registration changed'
    assert len(data['source']) == 1
    questions = by_id(q for [q] in data['questions'])
    field_owner, answer_owner, answers = {}, {}, {}
    for qid, q in questions.items():
        for field in q.get(':question/answer-fields', []):
            fid = field[':db/id']
            assert fid not in field_owner
            field_owner[fid] = qid
            for answer in field.get(':answer-field/choices', []):
                aid = answer[':db/id']
                assert aid not in answer_owner
                answer_owner[aid], answers[aid] = fid, answer
    items = {item[':db/id']: item for _, item in data['items']}
    item_questions = {item[':db/id']: qid for qid, item in data['items']}
    refs = sorted(set(field_owner) | set(answer_owner))
    incoming = read('incoming', '[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]',
                    [[Tagged('edb/ref', eid) for eid in refs]])
    attrs = dict(data['attributes'])
    for entity, attribute, target in incoming:
        name = str(attrs[attribute])
        if name == ':task-item/responses':
            assert entity in items and field_owner[answer_owner[target]] == item_questions[entity]
        elif name == ':question/answer-fields':
            assert field_owner[target] == entity
        else:
            assert name in (':answer-field/choices', ':answer-field/correct') and answer_owner[target] == entity
    changes, affected, aliases, forms, mappings, new_answers = [], [], {}, [], [], {}

    def change(eid, attr, old, new):
        if old != new:
            changes.append({'entity': eid, 'attribute': attr, 'before': old, 'after': new})
            forms.append([kw('db/cas'), eid, kw(attr), old, new])

    for qid, q in questions.items():
        solution = q.get(':question/worked-solution', '')
        found = re.findall(r'Let \$([tu])=x\$ be the free coordinate\.', solution)
        if not found:
            continue
        assert len(found) == 1 and ':question/math-academy-id' not in q
        assert [kp[':db/id'] for kp in q[':knowledge-point/_questions']] == [KP]
        alias = aliases[qid] = found[0]
        affected.append(qid)
        change(qid, ':question/problem', q[':question/problem'], rename_prose(q[':question/problem'], alias))
        introduction = f'\n\nLet ${alias}=x$ be the free coordinate.'
        assert solution.count(introduction) == 1
        change(qid, ':question/worked-solution', solution, rename_prose(solution.replace(introduction, ''), alias))
        assert len(q[':question/answer-fields']) == 1
        field = q[':question/answer-fields'][0]
        kind = str(field[':answer-field/type'][':db/ident'])
        assert kind in (':answer-field.type/radio', ':answer-field.type/blank')
        authored = field[':answer-field/choices'] if kind.endswith('/radio') else [field[':answer-field/correct']]
        for answer in authored:
            assert answer[':answer/type'][':db/ident'] == ':answer.type/math'
            change(answer[':db/id'], ':answer/value', answer[':answer/value'], rename_math(answer[':answer/value'], alias))
        if kind.endswith('/blank'):
            for item in items.values():
                if item_questions[item[':db/id']] != qid:
                    continue
                for answer in item.get(':task-item/responses', []):
                    old_value = answer[':answer/value']
                    new_value = rename_math(old_value, alias)
                    if old_value == new_value:
                        continue
                    aid = answer[':db/id']
                    assert aid != field[':answer-field/correct'][':db/id'], 'Entered canonical answer requires retained clone review'
                    assert not any(a[':answer/value'] == new_value for a in field[':answer-field/choices'])
                    temp = f'x-response-{aid}'
                    if temp not in new_answers:
                        new_uuid = uuid.uuid5(uuid.NAMESPACE_URL, f'course-academy/kp-{KP}/x-only-v1/response-{answer[":answer/id"]}')
                        record = {kw('db/id'): temp, kw('answer/id'): new_uuid,
                                  kw('answer/type'): answer[':answer/type'][':db/id'], kw('answer/value'): new_value}
                        forms += [record, [kw('db/add'), field[':db/id'], kw('answer-field/choices'), temp]]
                        new_answers[temp] = {'field': field[':db/id'], 'old_answer': aid, 'uuid': str(new_uuid),
                                             'value': new_value, 'type': answer[':answer/type']}
                    forms += [[kw('db/retract'), item[':db/id'], kw('task-item/responses'), aid],
                              [kw('db/add'), item[':db/id'], kw('task-item/responses'), temp]]
                    mappings.append({'item': item[':db/id'], 'old_answer': aid, 'tempid': temp})
        forms += [[kw('db/ensure'), qid, kw('question/validate')],
                  [kw('db/ensure'), field[':db/id'], kw('answer-field/validate')]]
    assert len(affected) == 11
    assert len(changes) == 54
    assert len(mappings) == 1 and mappings[0]['old_answer'] == 17592186574812
    assert not read('answer-uuid-collisions', '[:find ?a :in $ [?uuid ...] :where [?a :answer/id ?uuid]]',
                    [[uuid.UUID(a['uuid']) for a in new_answers.values()]])
    groups = [['questions', PATTERNS['questions'], ids], ['items', PATTERNS['items'], sorted(items)],
              ['scope', PATTERNS['scope'], [KP]], ['retained', '[*]', sorted({m['old_answer'] for m in mappings})]]
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    (directory / 'transaction.edn').write_text(dumps(forms) + '\n')
    sha = hashlib.sha256((directory / 'transaction.edn').read_bytes()).hexdigest()
    plan = {**identity, 'changes': changes, 'affected_questions': affected, 'aliases': aliases,
            'response_mappings': mappings, 'new_answers': new_answers, 'attributes': attrs,
            'source_eid': data['source'][0][0], 'transaction_sha256': sha}
    save(directory / 'plan.json', plan)
    (directory / 'snapshot.edn').write_text(dumps({**identity, **data, 'incoming': incoming}) + '\n')
    request = {**identity, 'source': SOURCE, 'endpoint': DB.config.endpoint, 'sha256': sha,
               'request_key': f'general-solution-x-only-b{basis}-{sha}',
               'transaction_file': str(directory / 'transaction.edn')}
    save(directory / 'prepared-request.json', request)
    return request


def verify_report(directory, report, committed):
    plan = json.loads((directory / 'plan.json').read_text())
    assert report[':edb/committed'] is committed and report[':edb/db-before-t'] == plan['basis']
    resolve = lambda value: report[':edb/tempids'].get(value, value) if isinstance(value, str) else value
    expected = set()
    canonical = lambda value: json.dumps(value, sort_keys=True, default=str)
    for form in loads((directory / 'transaction.edn').read_text()):
        if isinstance(form, dict):
            for attr, value in form.items():
                if attr != ':db/id':
                    expected.add((resolve(form[':db/id']), str(attr), canonical(resolve(value)), True))
        elif form[0] == ':db/cas':
            _, entity, attr, old, new = form
            expected |= {(entity, str(attr), canonical(old), False), (entity, str(attr), canonical(new), True)}
        elif form[0] in (':db/add', ':db/retract'):
            op, entity, attr, value = form
            expected.add((resolve(entity), str(attr), canonical(resolve(value)), op == ':db/add'))
    actual = set()
    for entity, attr, value, tx, source, added in report[':edb/tx-data']:
        assert source == plan['source_eid']
        attr = str(plan['attributes'][str(attr)])
        if attr == ':db/txInstant':
            assert added
        else:
            actual.add((entity, attr, canonical(value), added))
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
    changes = {(c['entity'], c['attribute']): c for c in plan['changes']}
    new = {temp: {':db/id': report[':edb/tempids'][temp], ':answer/id': a['uuid'],
                  ':answer/value': a['value'], ':answer/type': a['type']} for temp, a in plan['new_answers'].items()}

    def expected(value):
        if isinstance(value, list):
            return [expected(v) for v in value]
        if not isinstance(value, dict):
            return value
        result = {k: expected(v) for k, v in value.items()}
        eid = result.get(':db/id')
        for key in list(result):
            if (eid, key) in changes:
                change = changes[eid, key]
                assert result[key] == change['before']
                result[key] = change['after']
        for temp, a in plan['new_answers'].items():
            if eid == a['field'] and ':answer-field/choices' in result:
                result[':answer-field/choices'].append(copy.deepcopy(new[temp]))
        for mapping in plan['response_mappings']:
            if eid == mapping['item'] and ':task-item/responses' in result:
                result[':task-item/responses'] = [copy.deepcopy(new[mapping['tempid']]) if a[':db/id'] == mapping['old_answer'] else a
                                                 for a in result[':task-item/responses']]
        return result

    for name, _, _ in loads((directory / 'native-pulls.edn').read_text()):
        before = loads((directory / f'preview-{name}-before.edn').read_text())
        after = loads((directory / f'preview-{name}-after.edn').read_text())
        assert normalize(expected(before)) == normalize(after), name
    subprocess.run([sys.executable, str(HERE / 'check_math.py'), str(directory)], check=True)
    save(directory / 'preview-verification.json', {'passed': True, 'exact_allowed_datoms': True,
         'complete_preservation_readback': True, 'original_entered_answer_retained': True,
         'questions_checked': 18, 'questions_changed': 11, 'saved_responses_mapped': 1})


def execute(directory, commit):
    directory.mkdir(exist_ok=True)
    intent = directory / 'commit-intent.json'
    if intent.exists():
        request = json.loads(intent.read_text())
    else:
        if (directory / 'preview-verification.json').exists():
            request = json.loads((directory / 'prepared-request.json').read_text())
            assert json.loads((directory / 'preview-verification.json').read_text())['passed']
            verify_report(directory, loads((directory / 'preview.edn').read_text()), False)
        else:
            request = prepare(directory)
            preview(directory, request)
        if not commit:
            return
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
        assert normalize([q for [q] in actual]) == normalize(expected), name
        historical = DB.query(query, [ids], directory / 'committed', name + '-historical', request['basis'])
        assert normalize([q for [q] in historical]) == normalize(loads((directory / f'preview-{name}-before.edn').read_text()))
    plan = json.loads((directory / 'plan.json').read_text())
    verification = {'committed': True, 'basis_before': request['basis'], 'basis_after': basis,
                    'lineage': request['lineage'], 'request_key': request['request_key'],
                    'transaction_sha256': request['sha256'], 'questions_updated': 11,
                    'question_ids': plan['affected_questions'], 'saved_responses_mapped': 1,
                    'original_entered_answer_retained': True, 'native_grading_passed': True,
                    'exact_committed_and_historical_readback': True,
                    'question_field_and_authored_answer_ids_preserved': True,
                    'difficulty_correct_references_and_learner_state_preserved': True,
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

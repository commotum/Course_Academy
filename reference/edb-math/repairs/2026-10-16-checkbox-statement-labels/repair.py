"""Repair checkbox statement labels with guarded, previewed EDB transactions."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps, loads, kw, Tagged
from capture.scripts.database.client import StaleBasis
from audit_scope import PATTERNS, KP, SOURCE

HERE = Path(__file__).resolve().parent
PUBLISHER = Publisher.from_environment(source=SOURCE)
DB = PUBLISHER.client
NATIVE = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
GENERATOR = ROOT / 'generate/scratch/17592186100869-draft.py'
EMPTY = {17592186562892, 17592186562914}
NONE = 'None of these products is well defined.'
STATEMENT = re.compile(r'(?m)^(?:- \*\*)?(I{1,3})\.(?:\*\*)? (The product \$([A-Z])([A-Z])\$ is well defined)\.?[ \t]*$')
MATRIX = re.compile(r'([A-Z])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)

def save(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')

def normalized(value):
    if isinstance(value, dict): return {str(k): normalized(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)): return sorted((normalized(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True, default=str))
    return str(value) if isinstance(value, uuid.UUID) else value

def conclusion(products, truth):
    def words(names):
        terms = ['$' + p + '$' for p in names]
        return ' and '.join(terms) if len(terms) < 3 else ', '.join(terms[:-1]) + ', and ' + terms[-1]
    sentences = []
    for defined in (True, False):
        names = [p for p, good in zip(products, truth) if good == defined]
        if names:
            sentences.append(('The product ' if len(names) == 1 else 'The products ') + words(names) + (' is ' if len(names) == 1 else ' are ') + ('well defined.' if defined else 'undefined.'))
    if not any(truth): sentences.append('Select “None of these products is well defined.”')
    return ' '.join(sentences)

def prepare(directory):
    base = loads((ROOT / (HERE / 'capture-directory.txt').read_text().strip() / 'snapshot.edn').read_text())
    identity = DB.status()
    assert identity['lineage'] == base['lineage']
    ids = sorted(q[':db/id'] for [q] in base['questions'])
    def read(name, query, inputs): return DB.query(query, inputs, directory / 'evidence', name, identity['basis'])
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
    for name in ('questions', 'scope'):
        assert normalized(base[name]) == normalized(data[name]), 'Reviewed content changed: ' + name
    assert len(data['source']) == 1
    gen = data['scope'][0][0][':knowledge-point/question-generator']
    assert gen[':question-generator/script'] == str(GENERATOR.relative_to(ROOT))
    fields = {f[':db/id']: (q[':db/id'], f) for [q] in data['questions'] for f in q.get(':question/answer-fields', [])}
    answers = {a[':db/id']: fid for fid, (_, f) in fields.items() for a in f[':answer-field/choices']}
    incoming = read('incoming', '[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]', [[Tagged('edb/ref', e) for e in sorted(set(fields) | set(answers))]])
    attrs = dict(data['attributes'])
    items = {i[':db/id']: (qid, i) for qid, i in data['items']}
    for e, aid, target in incoming:
        attr = str(attrs[aid])
        if target in fields:
            assert attr == ':question/answer-fields' and fields[target][0] == e, (e, attr, target)
        elif attr in (':answer-field/choices', ':answer-field/correct'):
            assert answers[target] == e
        else:
            assert attr == ':task-item/responses' and e in items and items[e][0] == fields[answers[target]][0], (e, attr, target)
    changes, extras, mappings, forms = [], [], [], []
    def cas(entity, attr, before, after):
        if before != after:
            changes.append({'entity': entity, 'attribute': attr, 'before': before, 'after': after})
            forms.append([kw('db/cas'), entity, kw(attr), before, after])
    for [q] in sorted(data['questions'], key=lambda row: row[0][':db/id']):
        qid = q[':db/id']
        if not q.get(':question/answer-fields'): continue
        matches = list(STATEMENT.finditer(q[':question/problem']))
        assert len(matches) == 3 and [m[1] for m in matches] == ['I', 'II', 'III']
        bykey = {f[':answer-field/key']: f for f in q[':question/answer-fields']}
        assert set(bykey) == {'I', 'II', 'III'}
        dims = {name: (len(body.split(r'\\')), len(body.split(r'\\')[0].split('&'))) for name, body in MATRIX.findall(q[':question/problem'])}
        products, truth = [], []
        for match in matches:
            field = bykey[match[1]]
            assert field[':answer-field/type'][':db/ident'] == ':answer-field.type/checkbox'
            good = dims[match[3]][1] == dims[match[4]][0]
            assert field[':answer-field/correct'][':answer/value'] == str(good).lower()
            assert {a[':answer/value'] for a in field[':answer-field/choices']} == {'true', 'false'}
            products.append(match[3] + match[4]); truth.append(good)
            cas(field[':db/id'], ':answer-field/key', field[':answer-field/key'], match[2] + '.')
            forms.append([kw('db/ensure'), field[':db/id'], kw('answer-field/validate')])
        assert (not any(truth)) == (qid in EMPTY)
        prompt = re.sub(r'\n{3,}', '\n\n', STATEMENT.sub('', q[':question/problem'])).strip()
        prompt = prompt.replace('following statement are', 'following statements are')
        assert prompt.count('Select all that apply.') == 1 and 'The product $' not in prompt
        cas(qid, ':question/problem', q[':question/problem'], prompt)
        solution = q[':question/worked-solution']
        ending = solution.split('\n\n')[-1]
        assert ending.startswith(('Therefore, statement', 'We conclude that all three statements'))
        cas(qid, ':question/worked-solution', solution, solution[:-len(ending)] + conclusion(products, truth))
        if qid in EMPTY:
            fid = uuid.uuid5(q[':question/id'], 'checkbox-statement-labels-v1/none-defined')
            aids = {v: uuid.uuid5(fid, v) for v in ('false', 'true')}
            assert not read('none-field-' + str(qid), '[:find ?e :in $ ?id :where [?e :answer-field/id ?id]]', [fid])
            assert not read('none-answers-' + str(qid), '[:find ?e :in $ [?id ...] :where [?e :answer/id ?id]]', [list(aids.values())])
            ftemp = 'none-field-' + str(qid)
            atemps = {v: f'none-{v}-{qid}' for v in aids}
            for value, aid in aids.items():
                forms += [{kw('db/id'): atemps[value], kw('answer/id'): aid, kw('answer/type'): kw('answer.type/text'), kw('answer/value'): value}, [kw('db/ensure'), atemps[value], kw('answer/validate')]]
            forms += [{kw('db/id'): ftemp, kw('answer-field/id'): fid, kw('answer-field/key'): NONE,
                       kw('answer-field/type'): kw('answer-field.type/checkbox'), kw('answer-field/choices'): list(atemps.values()), kw('answer-field/correct'): atemps['true']},
                      [kw('db/ensure'), ftemp, kw('answer-field/validate')], [kw('db/add'), qid, kw('question/answer-fields'), ftemp]]
            extras.append({'question': qid, 'field_tempid': ftemp, 'field_uuid': str(fid), 'answer_tempids': atemps, 'answer_uuids': {v: str(a) for v, a in aids.items()}, 'field_type': bykey['I'][':answer-field/type'], 'answer_type': bykey['I'][':answer-field/correct'][':answer/type']})
            for item_id, (owner, item) in items.items():
                if owner != qid or not item.get(':task-item/responses'): continue
                response = item[':task-item/responses']
                assert len(response) == 3 and {answers[a[':db/id']] for a in response} == {f[':db/id'] for f in q[':question/answer-fields']}
                value = str(not any(a[':answer/value'] == 'true' for a in response)).lower()
                forms += [[kw('db/add'), item_id, kw('task-item/responses'), atemps[value]], [kw('db/ensure'), item_id, kw('task-item/validate')]]
                mappings.append({'item': item_id, 'question': qid, 'added_response': atemps[value], 'value': value, 'old_answers': [a[':db/id'] for a in response]})
        forms.append([kw('db/ensure'), qid, kw('question/validate')])
    assert len([c for c in changes if c['attribute'] == ':question/problem']) == 17
    groups = [['questions', PATTERNS['questions'], ids], ['items', PATTERNS['items'], sorted(items)], ['scope', PATTERNS['scope'], [KP]]]
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    (directory / 'transaction.edn').write_text(dumps(forms) + '\n')
    sha = hashlib.sha256((directory / 'transaction.edn').read_bytes()).hexdigest()
    plan = {**identity, 'changes': changes, 'extras': extras, 'mappings': mappings, 'attributes': attrs, 'source_eid': data['source'][0][0], 'transaction_sha256': sha, 'generator_sha256': hashlib.sha256(GENERATOR.read_bytes()).hexdigest()}
    save(directory / 'plan.json', plan)
    (directory / 'snapshot.edn').write_text(dumps({**identity, **data, 'incoming': incoming}) + '\n')
    request = {**identity, 'source': SOURCE, 'endpoint': DB.config.endpoint, 'sha256': sha, 'request_key': f'checkbox-statement-labels-b{identity["basis"]}-{sha}', 'transaction_file': str(directory / 'transaction.edn')}
    save(directory / 'prepared-request.json', request)
    return request

def verify_report(directory, report, committed):
    plan = json.loads((directory / 'plan.json').read_text())
    assert report[':edb/committed'] is committed and report[':edb/db-before-t'] == plan['basis']
    resolve = lambda v: report[':edb/tempids'].get(str(v), v) if isinstance(v, str) else v
    encoded = lambda v: json.dumps(resolve(v), sort_keys=True, default=str)
    expected = set()
    # Reference enum assertions are represented as resolved IDs in reports.
    enums = {':answer.type/text': plan['extras'][0]['answer_type'][':db/id'], ':answer-field.type/checkbox': plan['extras'][0]['field_type'][':db/id']}
    def scalar(attr, value): return enums.get(str(value), value) if str(attr) in (':answer/type', ':answer-field/type') else value
    for form in loads((directory / 'transaction.edn').read_text()):
        if isinstance(form, dict):
            for attr, value in form.items():
                if attr == ':db/id': continue
                values = value if attr == ':answer-field/choices' else [value]
                for val in values: expected.add((resolve(form[':db/id']), str(attr), encoded(scalar(attr, val)), True))
        elif form[0] == ':db/cas':
            _, eid, attr, before, after = form
            expected |= {(eid, str(attr), encoded(before), False), (eid, str(attr), encoded(after), True)}
        elif form[0] == ':db/add':
            _, eid, attr, value = form
            expected.add((resolve(eid), str(attr), encoded(value), True))
        else: assert form[0] == ':db/ensure'
    actual = set()
    for eid, aid, value, tx, source, added in report[':edb/tx-data']:
        assert source == plan['source_eid']
        attr = str(plan['attributes'][str(aid)])
        if attr == ':db/txInstant': assert added
        else: actual.add((eid, attr, encoded(value), added))
    assert actual == expected, (actual - expected, expected - actual)

def verify_pull_changes(directory, report):
    plan = json.loads((directory / 'plan.json').read_text())
    updates = {(c['entity'], c['attribute']): c for c in plan['changes']}
    new_fields, new_answers = {}, {}
    for e in plan['extras']:
        choices = []
        for value in ('false', 'true'):
            a = {':db/id': report[':edb/tempids'][e['answer_tempids'][value]], ':answer/id': e['answer_uuids'][value], ':answer/type': e['answer_type'], ':answer/value': value}
            choices.append(a); new_answers[e['answer_tempids'][value]] = a
        new_fields[e['question']] = {':db/id': report[':edb/tempids'][e['field_tempid']], ':answer-field/id': e['field_uuid'], ':answer-field/key': NONE, ':answer-field/type': e['field_type'], ':answer-field/choices': choices, ':answer-field/correct': choices[1]}
    mapped = {m['item']: new_answers[m['added_response']] for m in plan['mappings']}
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
        if ':question/answer-fields' in result and eid in new_fields: result[':question/answer-fields'].append(new_fields[eid])
        if ':task-item/responses' in result and eid in mapped: result[':task-item/responses'].append(mapped[eid])
        return result
    for name, _, _ in loads((directory / 'native-pulls.edn').read_text()):
        before = loads((directory / f'preview-{name}-before.edn').read_text())
        after = loads((directory / f'preview-{name}-after.edn').read_text())
        assert normalized(expected(before)) == normalized(after), name

def preview(directory, request):
    result = subprocess.run([str(NATIVE), str(directory), SOURCE, str(request['basis'])], env=DB.environment, capture_output=True, text=True, timeout=150)
    (directory / 'preview.stderr').write_text(result.stderr)
    result.check_returncode()
    (directory / 'preview.edn').write_text(result.stdout)
    report = loads(result.stdout)
    verify_report(directory, report, False)
    verify_pull_changes(directory, report)
    subprocess.run([sys.executable, str(HERE / 'check_questions.py'), str(directory)], check=True)
    save(directory / 'preview-verification.json', {'passed': True, 'exact_allowed_datoms': True, 'questions_reviewed': 18, 'questions_changed': 17, 'explicit_none_options': 2, 'original_field_and_answer_identities_preserved': True})

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
            output = DB.command('transact', '--source', SOURCE, '--file', request['transaction_file'], '--basis', request['basis'], '--endpoint', request['endpoint'], '--request-key', request['request_key'], '--timeout-ms', '120000', timeout=150)
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
    def verify_group(group):
        name, pattern, ids = group
        query = '[:find (pull ?e ' + pattern + ') :in $ [?e ...] :where [?e _ _]]'
        actual = DB.query(query, [ids], directory / 'committed', name, basis)
        assert normalized([q for [q] in actual]) == normalized(durable(loads((directory / f'preview-{name}-after.edn').read_text()))), name
        historical = DB.query(query, [ids], directory / 'committed', name + '-historical', request['basis'])
        assert normalized([q for [q] in historical]) == normalized(loads((directory / f'preview-{name}-before.edn').read_text())), name + '-historical'
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(verify_group, loads((directory / 'native-pulls.edn').read_text())))
    plan = json.loads((directory / 'plan.json').read_text())
    assert plan['generator_sha256'] == hashlib.sha256(GENERATOR.read_bytes()).hexdigest()
    verification = {'committed': True, 'basis_before': request['basis'], 'basis_after': basis, 'lineage': request['lineage'], 'request_key': request['request_key'], 'transaction_sha256': request['sha256'], 'questions_updated': sorted({c['entity'] for c in plan['changes'] if c['attribute'] == ':question/problem'}), 'explicit_none_options': sorted(EMPTY), 'saved_response_mappings': plan['mappings'], 'original_field_answer_ids_and_correct_refs_preserved': True, 'matrices_difficulty_and_memberships_preserved': True, 'native_grading_passed': True, 'exact_committed_and_historical_readback': True, 'generator_path': str(GENERATOR.relative_to(ROOT)), 'generator_sha256': plan['generator_sha256'], 'evidence_directory': str(directory.relative_to(ROOT))}
    save(directory / 'verification.json', verification)
    save(HERE / 'verification.json', verification)
    print(json.dumps(verification))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    execute(HERE / args.attempt, args.commit)

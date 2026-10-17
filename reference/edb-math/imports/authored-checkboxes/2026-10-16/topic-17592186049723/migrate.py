"""Guarded checkbox conversion with retained requests and exact-basis verification."""
import argparse
import collections
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from types import SimpleNamespace

import sympy as sp

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps, loads, kw, Tagged
from capture.scripts.database.client import StaleBasis

HERE = Path(__file__).resolve().parent
AUDIT = ROOT / 'reference/edb-math/audits/radio2checkbox/2026-10-16/entity-17592186124704'
LEGACY = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-12/finder-easy/prepare.py'
NATIVE = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native'
spec = importlib.util.spec_from_file_location('checkbox_migration', LEGACY)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
SOURCE = m.SOURCE
publisher = Publisher.from_environment(source=SOURCE)
DB = publisher.client
QUESTION = '''[* {:question/difficulty [:db/id :db/ident]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'''
ITEM = '''[* {:task-item/status [:db/id :db/ident]}
 {[:task-item/responses :limit nil] [* {:answer/type [:db/id :db/ident]}]}
 {[:learner-task/_items :limit nil] [:db/id :learner-task/status]}]'''
SCOPE = '''[* {[:topic/knowledge-points :limit nil] [*
 {[:knowledge-point/questions :limit nil] [:db/id]}
 {:knowledge-point/canonical-example [:db/id]}
 {:knowledge-point/question-generator [*]}]}]'''


def save(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')


def rows_by_id(rows):
    return {q[':db/id']: q for q in rows}


def subset(value):
    if value.startswith('All the columns'):
        return set(column_labels)
    selected = re.findall(r'\$(\d+)\$(?:st|nd|rd|th)', value)
    rest = re.sub(r'\$\d+\$(?:st|nd|rd|th)', '', value)
    rest = re.sub(r'\b(?:and|only)\b|[\s,.]', '', rest)
    assert selected and not rest, value
    result = {f'Column {n}' for n in selected}
    assert len(result) == len(selected) and result <= set(column_labels)
    return result


def labels_and_prompt(q, field):
    global column_labels
    problem = q[':question/problem']
    body = re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', problem, re.S)
    assert len(body) == 1 and 'number of pivot columns' not in problem.lower()
    matrix = sp.Matrix([[sp.Rational(v.strip()) for v in row.split('&')] for row in body[0].split(r'\\')])
    column_labels = [f'Column {i}' for i in range(1, matrix.cols + 1)]
    pivot_columns = {f'Column {i + 1}' for i in matrix.rref()[1]}
    correct = set(column_labels) - pivot_columns if '**non**-pivot' in problem else pivot_columns
    assert subset(field[':answer-field/correct'][':answer/value']) == correct
    assert 'Select all that apply.' not in problem
    return column_labels, problem.rstrip() + '\n\nSelect all that apply.'


def configure(directory):
    m.OUT = directory
    m.AUDIT = directory / 'audit-input.json'
    m.DB = SimpleNamespace(args=SimpleNamespace(endpoint=publisher.config.endpoint))
    m.kw, m.dumps, m.loads = kw, dumps, loads
    m.subset, m.labels_and_prompt = subset, labels_and_prompt
    m.read = lambda query, inputs, name, basis: DB.query(query, inputs, directory / 'evidence', name, basis)


def prepare(directory):
    configure(directory)
    assert not (directory / 'commit-intent.json').exists()
    old = loads((AUDIT / 'snapshot.edn').read_text())
    ledger = json.loads((AUDIT / 'ledger.json').read_text())
    ids = sorted(q['question_eid'] for q in ledger if q['strong_candidate'])
    all_ids = sorted(q['question_eid'] for q in ledger)
    identity = DB.status()
    assert identity['lineage'] == old['lineage']
    basis = identity['basis']
    def read(name, query, inputs):
        return DB.query(query, inputs, directory / 'evidence', name, basis)
    queries = {
        'questions': ('[:find (pull ?q ' + QUESTION + ') :in $ [?q ...] :where [?q :question/id _]]', [all_ids]),
        'items': ('[:find ?q (pull ?item ' + ITEM + ') :in $ [?q ...] :where [?item :task-item/content ?q]]', [all_ids]),
        'attributes': ('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]', []),
        'source': ('[:find (pull ?s [:db/id :db/ident :db/doc]) :in $ ?ident :where [?s :db/ident ?ident]]', [kw(SOURCE)]),
        'scope': ('[:find (pull ?topic ' + SCOPE + ') :in $ ?topic :where [?topic :topic/id _]]', [17592186049723]),
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {name: pool.submit(read, name, query, inputs) for name, (query, inputs) in queries.items()}
        captured = {name: future.result() for name, future in futures.items()}
    assert len(captured['source']) == 1
    before = rows_by_id(q for [q] in old['questions'])
    current = rows_by_id(q for [q] in captured['questions'])
    assert current == before, 'Current question content differs from the reviewed audit; re-review required'
    scope_ids = {q[':db/id'] for [topic] in captured['scope'] for kp in topic[':topic/knowledge-points']
                 for q in kp.get(':knowledge-point/questions', []) + [kp[':knowledge-point/canonical-example']]}
    assert scope_ids == set(all_ids), 'Topic question inventory changed; re-review required'
    refs = sorted({ref[':db/id'] for qid in ids for f in current[qid][':question/answer-fields']
                   for ref in [f] + f[':answer-field/choices']})
    incoming = read('incoming', '[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]',
                    [[Tagged('edb/ref', eid) for eid in refs]])
    attrs = dict(captured['attributes'])
    field_owner = {f[':db/id']: qid for qid in ids for f in current[qid][':question/answer-fields']}
    answer_owner = {a[':db/id']: f[':db/id'] for qid in ids for f in current[qid][':question/answer-fields'] for a in f[':answer-field/choices']}
    item_owner = {item[':db/id']: qid for qid, item in captured['items']}
    items_by_id = {item[':db/id']: item for _, item in captured['items']}
    users = []
    for entity, attribute, target in incoming:
        name = str(attrs[attribute])
        if name == ':task-item/responses':
            assert item_owner[entity] in ids and target in answer_owner
            assert field_owner[answer_owner[target]] == item_owner[entity]
            users.append([target, items_by_id[entity]])
        else:
            assert (name == ':question/answer-fields' and field_owner.get(target) == entity) or (
                name in (':answer-field/choices', ':answer-field/correct') and answer_owner.get(target) == entity)
    snapshot = {**identity, **captured, 'incoming': incoming, 'response_users': users}
    (directory / 'snapshot.edn').write_text(dumps(snapshot) + '\n')
    save(directory / 'snapshot.json', snapshot)
    selected = [current[qid] for qid in ids]
    audit = {'basis': basis, 'counts': {'secondary_questions': 0}, 'direct_candidates': [{'questions': [
        {'id': q[':db/id'], 'ma_id': q[':question/math-academy-id'],
         'kp': q[':knowledge-point/_questions'][0][':db/id'],
         'kp_title': q[':knowledge-point/_questions'][0][':knowledge-point/title'],
         'problem': q[':question/problem'], 'review_flags': []} for q in selected]}]}
    save(directory / 'audit-input.json', audit)
    m.plan()
    plan = json.loads((directory / 'plan.json').read_text())
    assert plan['counts']['questions'] == 47 and not plan['deferred']
    plan['notes'] = ['One checkbox per matrix column, including columns absent from old choices.',
        'All original options and saved responses map to their actual selected column subset.',
        'Solutions, difficulty, memberships, old fields/answers and learner state preserved.',
        'Solution corrections will be a separate subsequent guarded batch.']
    save(directory / 'plan.json', plan)
    request = json.loads((directory / 'prepared-request.json').read_text())
    request.update(lineage=identity['lineage'], request_key=f"pivot-columns-checkbox-v1-b{basis}-{plan['transaction_sha256']}")
    save(directory / 'prepared-request.json', request)
    forms = loads((directory / 'transaction.edn').read_text())
    for attr in ('answer/id', 'answer-field/id'):
        uuids = [form[kw(attr)] for form in forms if isinstance(form, dict) and kw(attr) in form]
        assert not read(attr.replace('/', '-') + '-collisions', '[:find ?e ?id :in $ [?id ...] :where [?e :' + attr + ' ?id]]', [uuids])
    groups = [['questions', QUESTION, all_ids], ['retained', '[*]', plan['retained_original_entities']],
              ['items', ITEM, sorted(items_by_id)], ['scope', SCOPE, [17592186049723]]]
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    return request


def preview(directory, request):
    result = subprocess.run([str(NATIVE / 'preview'), str(directory), SOURCE, str(request['basis'])],
                            env=DB.environment, capture_output=True, text=True, timeout=150)
    (directory / 'preview.stderr').write_text(result.stderr)
    result.check_returncode()
    (directory / 'preview.edn').write_text(result.stdout)
    report = loads(result.stdout)
    m.verify_preview(report)
    plan = json.loads((directory / 'plan.json').read_text())
    before = rows_by_id(loads((directory / 'preview-questions-before.edn').read_text()))
    after = rows_by_id(loads((directory / 'preview-questions-after.edn').read_text()))
    changed = {q['id']: q for q in plan['questions']}
    for eid, q in before.items():
        if eid not in changed:
            assert after[eid] == q
        else:
            assert after[eid][':question/problem'] == changed[eid]['problem_after']
            omit = lambda value: {k: v for k, v in value.items() if k not in (':question/problem', ':question/answer-fields')}
            assert omit(after[eid]) == omit(q)
    expected_items = {r['item']: r for r in plan['responses']}
    for old, new in zip(loads((directory / 'preview-items-before.edn').read_text()), loads((directory / 'preview-items-after.edn').read_text())):
        eid = old[':db/id']
        omit = lambda value: {k: v for k, v in value.items() if k != ':task-item/responses'}
        assert omit(old) == omit(new)
        if eid in expected_items:
            assert {r[':db/id'] for r in new[':task-item/responses']} == {report[':edb/tempids'][t] for t in expected_items[eid]['new_answer_tempids']}
        else:
            assert old == new
    for group in ('retained', 'scope'):
        assert loads((directory / f'preview-{group}-before.edn').read_text()) == loads((directory / f'preview-{group}-after.edn').read_text())
    grader_dir = directory / 'native'
    grader_dir.mkdir(exist_ok=True)
    checker = (NATIVE / 'check_native.py').read_text().replace("str(HERE / 'check-checkbox-engine')", repr(str(NATIVE / 'check-checkbox-engine')))
    (grader_dir / 'check_native.py').write_text(checker)
    subprocess.run([sys.executable, str(grader_dir / 'check_native.py')], check=True, env=DB.environment)
    save(directory / 'preview-preservation.json', {'passed': True, 'questions_checked': len(before),
         'original_entities_retained': len(plan['retained_original_entities']), 'learner_responses_mapped': len(plan['responses']),
         'solutions_difficulty_memberships_and_other_learner_state_preserved': True})


def finish(directory, request, report):
    configure(directory)
    assert report[':edb/committed'] is True
    m.verify_preview(report, committed=True)
    basis = report.get(':edb/db-after-t', report.get(':edb/basis-t'))
    predicted = loads((directory / 'preview.edn').read_text())
    mapping = {eid: report[':edb/tempids'][temp] for temp, eid in predicted[':edb/tempids'].items()}
    def durable(value):
        if isinstance(value, int): return mapping.get(value, value)
        if isinstance(value, list): return [durable(v) for v in value]
        if isinstance(value, dict): return {k: durable(v) for k, v in value.items()}
        return value
    for name, pattern, ids in loads((directory / 'native-pulls.edn').read_text()):
        query = '[:find (pull ?e ' + pattern + ') :in $ [?e ...] :where [?e _ _]]'
        actual = DB.query(query, [ids], directory / 'committed', name, basis)
        expected = durable(loads((directory / f'preview-{name}-after.edn').read_text()))
        assert rows_by_id(q for [q] in actual) == rows_by_id(expected), name
        historical = DB.query(query, [ids], directory / 'committed', name + '-historical', request['basis'])
        assert rows_by_id(q for [q] in historical) == rows_by_id(loads((directory / f'preview-{name}-before.edn').read_text())), name
    plan = json.loads((directory / 'plan.json').read_text())
    verification = {'committed': True, 'basis_before': request['basis'], 'basis_after': basis,
        'lineage': request['lineage'], 'source': SOURCE, 'request_key': request['request_key'],
        'transaction_sha256': request['sha256'], 'counts': plan['counts'], 'converted_ids': [q['id'] for q in plan['questions']],
        'exact_committed_readback': True, 'native_grading_passed': True,
        'original_fields_answers_retained_unchanged': True, 'saved_task_state_preserved': True,
        'solutions_difficulty_memberships_preserved': True, 'historical_readback_matches': True}
    save(directory / 'verification.json', verification)
    save(HERE / 'checkbox-verification.json', {**verification, 'evidence_directory': str(directory.relative_to(ROOT))})
    print(json.dumps(verification))


def execute(directory, commit):
    directory.mkdir(parents=True, exist_ok=True)
    configure(directory)
    if (directory / 'commit-intent.json').exists():
        request = json.loads((directory / 'commit-intent.json').read_text())
    else:
        request = prepare(directory)
        preview(directory, request)
        if not commit:
            return
        save(directory / 'commit-intent.json', request)
    assert hashlib.sha256(Path(request['transaction_file']).read_bytes()).hexdigest() == request['sha256']
    assert DB.status()['lineage'] == request['lineage']
    receipt_path = directory / 'receipt.edn'
    if not receipt_path.exists():
        try:
            output = DB.command('transact', '--source', request['source'], '--file', request['transaction_file'],
                '--basis', request['basis'], '--endpoint', request['endpoint'], '--request-key', request['request_key'],
                '--timeout-ms', '120000', timeout=150)
        except StaleBasis as error:
            save(directory / 'rejected.json', {'confirmed_stale_basis': True, 'reason': str(error)})
            raise
        receipt_path.write_text(output)
    finish(directory, request, loads(receipt_path.read_text()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    execute(HERE / args.attempt, args.commit)

"""Apply the reviewed solution-only CAS repairs after verified checkbox conversion."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

from migrate import DB, HERE, NATIVE, SOURCE, QUESTION, ITEM, SCOPE, AUDIT, ROOT, save, rows_by_id
from capture.scripts.database.edn import dumps, loads, kw
from capture.scripts.database.client import StaleBasis


def verify_report(directory, report, committed):
    plan = json.loads((directory / 'plan.json').read_text())
    assert report[':edb/committed'] is committed
    assert report[':edb/db-before-t'] == plan['basis']
    expected = {(c['question_eid'], ':question/worked-solution', c['before'], False) for c in plan['corrections']}
    expected |= {(c['question_eid'], ':question/worked-solution', c['after'], True) for c in plan['corrections']}
    attrs = {int(k): v for k, v in plan['attributes'].items()}
    actual = set()
    for entity, attribute, value, tx, source, added in report[':edb/tx-data']:
        assert source == plan['source_eid']
        name = attrs[attribute]
        if name == ':db/txInstant':
            assert added
        else:
            actual.add((entity, name, value, added))
    assert actual == expected, (actual - expected, expected - actual)


def prepare(directory):
    conversion = json.loads((HERE / 'checkbox-verification.json').read_text())
    assert conversion['committed'] and conversion['exact_committed_readback']
    corrections = json.loads((HERE / 'solution-repairs/corrections.json').read_text())['corrections']
    identity = DB.status()
    assert identity['lineage'] == conversion['lineage']
    basis = identity['basis']
    all_ids = [r['question_eid'] for r in json.loads((AUDIT / 'ledger.json').read_text())]
    def read(name, query, inputs):
        return DB.query(query, inputs, directory / 'evidence', name, basis)
    queries = {
        'questions': ('[:find (pull ?q ' + QUESTION + ') :in $ [?q ...] :where [?q :question/id _]]', [all_ids]),
        'items': ('[:find ?q (pull ?item ' + ITEM + ') :in $ [?q ...] :where [?item :task-item/content ?q]]', [all_ids]),
        'attributes': ('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]', []),
        'source': ('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]', [kw(SOURCE)]),
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {name: pool.submit(read, name, q, inputs) for name, (q, inputs) in queries.items()}
        captured = {name: future.result() for name, future in futures.items()}
    assert len(captured['source']) == 1
    questions = rows_by_id(q for [q] in captured['questions'])
    forms = []
    for correction in corrections:
        eid = correction['question_eid']
        assert questions[eid][':question/worked-solution'] == correction['before'], (eid, 'Reviewed solution changed')
        assert hashlib.sha256(correction['after'].encode()).hexdigest() == correction['after_sha256']
        forms += [[kw('db/cas'), eid, kw('question/worked-solution'), correction['before'], correction['after']],
                  [kw('db/ensure'), eid, kw('question/validate')]]
    (directory / 'transaction.edn').write_text(dumps(forms) + '\n')
    sha = hashlib.sha256((directory / 'transaction.edn').read_bytes()).hexdigest()
    plan = {**identity, 'source': SOURCE, 'source_eid': captured['source'][0][0],
            'corrections': corrections, 'attributes': dict(captured['attributes']), 'transaction_sha256': sha}
    save(directory / 'plan.json', plan)
    save(directory / 'snapshot.json', {**identity, **captured})
    groups = [['questions', QUESTION, all_ids], ['items', ITEM, [item[':db/id'] for _, item in captured['items']]],
              ['scope', SCOPE, [17592186049723]]]
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    request = {**identity, 'source': SOURCE, 'endpoint': DB.config.endpoint,
               'request_key': f'pivot-columns-solution-repairs-b{basis}-{sha}', 'sha256': sha,
               'transaction_file': str(directory / 'transaction.edn')}
    save(directory / 'prepared-request.json', request)
    result = subprocess.run([str(NATIVE / 'preview'), str(directory), SOURCE, str(basis)],
                            env=DB.environment, capture_output=True, text=True, timeout=150)
    (directory / 'preview.stderr').write_text(result.stderr)
    result.check_returncode()
    (directory / 'preview.edn').write_text(result.stdout)
    verify_report(directory, loads(result.stdout), False)
    expected = rows_by_id(loads((directory / 'preview-questions-before.edn').read_text()))
    for correction in corrections:
        expected[correction['question_eid']][':question/worked-solution'] = correction['after']
    assert expected == rows_by_id(loads((directory / 'preview-questions-after.edn').read_text()))
    for name in ('items', 'scope'):
        assert loads((directory / f'preview-{name}-before.edn').read_text()) == loads((directory / f'preview-{name}-after.edn').read_text())
    save(directory / 'preview-verification.json', {'passed': True, 'solution_corrections': len(corrections),
         'questions_checked': len(expected), 'only_reviewed_solutions_changed': True,
         'fields_keys_difficulty_memberships_and_learner_state_preserved': True})
    return request


def execute(directory):
    directory.mkdir(parents=True, exist_ok=True)
    intent_path = directory / 'commit-intent.json'
    if intent_path.exists():
        request = json.loads(intent_path.read_text())
    else:
        request = prepare(directory)
        save(intent_path, request)
    assert hashlib.sha256(Path(request['transaction_file']).read_bytes()).hexdigest() == request['sha256']
    assert DB.status()['lineage'] == request['lineage']
    receipt = directory / 'receipt.edn'
    if not receipt.exists():
        try:
            output = DB.command('transact', '--source', request['source'], '--file', request['transaction_file'],
                '--basis', request['basis'], '--endpoint', request['endpoint'], '--request-key', request['request_key'],
                '--timeout-ms', '120000', timeout=150)
        except StaleBasis as error:
            save(directory / 'rejected.json', {'confirmed_stale_basis': True, 'reason': str(error)})
            raise
        receipt.write_text(output)
    report = loads(receipt.read_text())
    verify_report(directory, report, True)
    basis = report.get(':edb/db-after-t', report.get(':edb/basis-t'))
    for name, pattern, ids in loads((directory / 'native-pulls.edn').read_text()):
        query = '[:find (pull ?e ' + pattern + ') :in $ [?e ...] :where [?e _ _]]'
        actual = DB.query(query, [ids], directory / 'committed', name, basis)
        assert rows_by_id(q for [q] in actual) == rows_by_id(loads((directory / f'preview-{name}-after.edn').read_text())), name
        historical = DB.query(query, [ids], directory / 'committed', name + '-historical', request['basis'])
        assert rows_by_id(q for [q] in historical) == rows_by_id(loads((directory / f'preview-{name}-before.edn').read_text())), name
    plan = json.loads((directory / 'plan.json').read_text())
    verified = {'committed': True, 'basis_before': request['basis'], 'basis_after': basis,
                'lineage': request['lineage'], 'source': SOURCE, 'request_key': request['request_key'],
                'transaction_sha256': request['sha256'], 'questions_repaired': len(plan['corrections']),
                'repaired_ids': [c['question_eid'] for c in plan['corrections']],
                'exact_committed_readback': True, 'only_reviewed_solutions_changed': True,
                'fields_keys_difficulty_memberships_and_learner_state_preserved': True,
                'historical_readback_matches': True, 'evidence_directory': str(directory.relative_to(ROOT))}
    save(directory / 'verification.json', verified)
    save(HERE / 'solution-verification.json', verified)
    print(json.dumps(verified))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    args = parser.parse_args()
    execute(HERE / 'solution-repairs' / args.attempt)

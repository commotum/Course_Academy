"""Submit the explicitly authorized batch once and verify its exact committed basis."""
import argparse
import hashlib
import json

import prepare as migration
from edn import loads

OUT = migration.OUT

def commit():
    manifest = json.loads((OUT / 'plan.json').read_text())
    preview = json.loads((OUT / 'preview.json').read_text())
    prepared = json.loads((OUT / 'prepared-request.json').read_text())
    digest = hashlib.sha256((OUT / 'transaction.edn').read_bytes()).hexdigest()
    assert preview['passed'] and preview['committed'] is False
    assert digest == preview['transaction_sha256'] == manifest['transaction_sha256'] == prepared['sha256']
    assert prepared['basis'] == preview['basis'] == manifest['basis']
    assert prepared['source'] == preview['source'] == manifest['source'] == migration.SOURCE
    assert manifest['counts']['questions'] == 220 and manifest['counts']['knowledge_points'] == 27
    path = OUT / 'commit-intent.json'
    if not path.exists():
        assert migration.DB.basis() == manifest['basis'], 'Database advanced; refresh snapshot/plan/preview before submitting'
        # Complete immutable request is retained before the first submission.
        migration.save('commit-intent.json', {**prepared, 'state': 'submission_requested'})
    intent = json.loads(path.read_text())
    assert intent['sha256'] == digest and intent['request_key'] == prepared['request_key']
    assert intent['source'] == migration.SOURCE and intent['basis'] == manifest['basis']
    report = migration.DB._commit(intent, OUT / 'transaction.edn', OUT)
    assert report[':edb/committed'] is True
    migration.verify_preview(report, committed=True)
    migration.save('commit-receipt.json', {
        'committed': True, 'basis_before': report[':edb/db-before-t'],
        'basis_after': report[':edb/db-after-t'], 'request_key': intent['request_key'],
        'source': intent['source'], 'transaction_sha256': digest,
        'tx_hash': report.get(':edb/tx-hash'), 'replayed': report.get(':edb/replayed'),
        'datoms': len(report[':edb/tx-data']), 'counts': manifest['counts']})
    print(json.dumps({'committed': True, 'basis_before': report[':edb/db-before-t'],
        'basis_after': report[':edb/db-after-t'], 'source': intent['source']}), flush=True)

def verify():
    report = loads((OUT / 'commit.edn').read_text())
    assert report[':edb/committed'] is True
    migration.verify_preview(report, committed=True)
    basis = report[':edb/db-after-t']
    manifest = json.loads((OUT / 'plan.json').read_text())
    snapshot = loads((OUT / 'snapshot.edn').read_text())
    before = {r[0][':db/id']: r[0] for r in snapshot['questions']}
    changes = {q['id']: q for q in manifest['questions']}
    query = '[:find (pull ?q ' + migration.QUESTION + ') :in $ [?q ...] :where [?q :question/id _]]'
    after = {r[0][':db/id']: r[0] for r in migration.batches(query, sorted(before), 'questions-after', basis)}
    assert set(after) == set(before)
    originals = {}
    total_fields = 0
    for qid, old in before.items():
        current = after[qid]
        if qid not in changes:
            assert current == old, ('Deferred question changed', qid)
            continue
        change = changes[qid]
        exempt = {':question/problem', ':question/answer-fields'}
        assert {k:v for k,v in current.items() if k not in exempt} == {k:v for k,v in old.items() if k not in exempt}
        assert current[':question/problem'] == change['problem_after']
        fields = {f[':answer-field/key']: f for f in current[':question/answer-fields']}
        assert len(fields) == len(current[':question/answer-fields']) == len(change['labels'])
        assert set(fields) == set(change['labels'])
        assert {f[':db/id'] for f in fields.values()} == {report[':edb/tempids'][t] for t in change['new_field_tempids']}
        for label, f in fields.items():
            token = change['ma_id'] + '/authored-checkbox-v1/' + label
            assert f[':answer-field/id'] == migration.stable_id('field', token)
            assert f[':answer-field/type'][':db/ident'] == ':answer-field.type/checkbox'
            bank = {a[':answer/value']: a for a in f[':answer-field/choices']}
            assert len(f[':answer-field/choices']) == 2 and set(bank) == {'false', 'true'}
            for value, answer in bank.items():
                assert answer[':answer/id'] == migration.stable_id('answer', token + '/' + value)
                assert answer[':answer/type'][':db/ident'] == ':answer.type/text'
            assert f[':answer-field/correct'] == bank[str(label in change['correct']).lower()]
            total_fields += 1
        for field in old[':question/answer-fields']:
            originals[field[':db/id']] = field
            originals.update({a[':db/id']: a for a in field[':answer-field/choices']})
    assert total_fields == manifest['counts']['new_checkbox_fields'] == 691
    original_pattern = '''[* {:answer/type [:db/id :db/ident]}
        {:answer-field/type [:db/id :db/ident]}
        {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}
        {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]'''
    retained = {r[0][':db/id']: r[0] for r in migration.batches(
        '[:find (pull ?e ' + original_pattern + ') :in $ [?e ...] :where (or [?e :answer/id _] [?e :answer-field/id _])]',
        sorted(originals), 'originals-after', basis, 64)}
    assert retained == originals, 'Original field/answer entities changed or disappeared'
    items_before = {item[':db/id']: (qid, item) for qid, item in snapshot['items']}
    items_after = {item[':db/id']: (qid, item) for qid, item in migration.batches(
        '[:find ?q (pull ?item ' + migration.ITEM + ') :in $ [?q ...] :where [?item :task-item/content ?q]]',
        sorted(changes), 'items-after', basis, 64)}
    assert set(items_after) == set(items_before)
    mapped = {r['item']: r for r in manifest['responses']}
    for itemid, (qid, old) in items_before.items():
        current_qid, current = items_after[itemid]
        assert qid == current_qid
        if itemid not in mapped:
            assert current == old
        else:
            assert {a[':db/id'] for a in current[':task-item/responses']} == {
                report[':edb/tempids'][t] for t in mapped[itemid]['new_answer_tempids']}
            assert {k:v for k,v in current.items() if k != ':task-item/responses'} == {
                k:v for k,v in old.items() if k != ':task-item/responses'}
    historical = {r[0][':db/id']: r[0] for r in migration.batches(
        query, sorted(before), 'questions-historical', manifest['basis'])}
    assert historical == before, 'Original historical view differs'
    migration.save('verification.json', {'passed': True, 'committed': True, 'basis_before': manifest['basis'],
        'basis_after': basis, 'source': migration.SOURCE, 'counts': manifest['counts'],
        'retained_original_entities': len(originals), 'unchanged_deferred_questions': len(before) - len(changes),
        'checks': ['All 220 converted questions read back with expected keys, Boolean banks and prompts.',
            'Question content, worked solutions, difficulty and KP/topic membership preserved.',
            'All deferred question records, original fields and answer entities unchanged.',
            'Learner presentations and grading preserved; response mappings checked.',
            'Original historical question view reproduced at the captured basis.',
            'Only intended datoms changed; agent source verified throughout.']})
    print(json.dumps({'verified': True, 'basis_after': basis, 'questions': len(changes),
        'checkbox_fields': total_fields, 'retained_original_entities': len(originals)}), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['commit', 'verify'])
    globals()[parser.parse_args().action]()

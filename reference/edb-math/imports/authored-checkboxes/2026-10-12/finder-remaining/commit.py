"""Submit the authorized logical transaction and verify its exact committed value."""
import argparse
import copy
import hashlib
import json

import prepare as migration

edb = migration.edb
OUT = migration.OUT


def commit():
    plan = json.loads((OUT / 'plan.json').read_text())
    preview = json.loads((OUT / 'preview.json').read_text())
    prepared = json.loads((OUT / 'prepared-request.json').read_text())
    digest = hashlib.sha256((OUT / 'transaction.edn').read_bytes()).hexdigest()
    assert preview['passed'] and preview['committed'] is False
    assert digest == preview['transaction_sha256'] == plan['transaction_sha256'] == prepared['sha256']
    assert hashlib.sha256((OUT / 'resolutions.json').read_bytes()).hexdigest() == plan['resolution_sha256']
    assert prepared['basis'] == preview['basis'] == plan['basis']
    assert prepared['source'] == preview['source'] == plan['source'] == edb.SOURCE
    assert plan['counts']['checkbox_conversions'] == 89 and plan['counts']['questions_changed'] == 90
    path = OUT / 'commit-intent.json'
    if not path.exists():
        assert edb.DB.basis() == plan['basis'], 'Database advanced; refresh dependencies before submission'
        edb.save('commit-intent.json', {**prepared, 'state': 'submission_requested'})
    intent = json.loads(path.read_text())
    assert intent['sha256'] == digest and intent['request_key'] == prepared['request_key']
    assert intent['source'] == edb.SOURCE and intent['basis'] == plan['basis']
    report = edb.DB._commit(intent, OUT / 'transaction.edn', OUT)
    assert report[':edb/committed'] is True
    # Retain confirmed outcome before any downstream validation can fail.
    edb.save('commit-receipt.json', {
        'committed': True, 'basis_before': report[':edb/db-before-t'],
        'basis_after': report[':edb/db-after-t'], 'request_key': intent['request_key'],
        'source': intent['source'], 'transaction_sha256': digest,
        'tx_hash': report.get(':edb/tx-hash'), 'replayed': report.get(':edb/replayed'),
        'datoms': len(report[':edb/tx-data']), 'counts': plan['counts']})
    print(json.dumps({'committed': True, 'basis_before': report[':edb/db-before-t'],
        'basis_after': report[':edb/db-after-t'], 'source': intent['source']}), flush=True)
    migration.inspect_report(report, committed=True)


def verify():
    report = edb.loads((OUT / 'commit.edn').read_text())
    assert report[':edb/committed'] is True
    migration.inspect_report(report, committed=True)
    basis = report[':edb/db-after-t']
    plan = json.loads((OUT / 'plan.json').read_text())
    snapshot = edb.loads((OUT / 'snapshot.edn').read_text())
    resolutions = json.loads((OUT / 'resolutions.json').read_text())
    before = {r[0][':db/id']: r[0] for r in snapshot['questions']}
    changes = {q['id']: q for q in plan['questions']}
    query = '[:find (pull ?q ' + edb.QUESTION + ') :in $ [?q ...] :where [?q :question/id _]]'
    after = {r[0][':db/id']: r[0] for r in edb.batches(query, sorted(before), 'questions-after', basis)}
    assert set(after) == set(before)
    originals = {}
    total_fields = 0
    for qid, old in before.items():
        current = after[qid]
        for field in old.get(':question/answer-fields', []):
            originals[field[':db/id']] = copy.deepcopy(field)
            originals.update({a[':db/id']: copy.deepcopy(a) for a in field[':answer-field/choices']})
        if qid not in changes:
            assert current == old, ('Retained question changed', qid)
            continue
        change = changes[qid]
        exempt = {':question/problem', ':question/answer-fields', ':question/worked-solution'}
        assert {k:v for k,v in current.items() if k not in exempt} == {k:v for k,v in old.items() if k not in exempt}
        expected_solution = old.get(':question/worked-solution')
        if change.get('authored_solution'):
            expected_solution = change['authored_solution']
        if change.get('worked_solution_repair'):
            expected_solution = change['worked_solution_repair']['after']
        assert current.get(':question/worked-solution') == expected_solution
        if change['action'] == 'retain_radio_repair_key':
            assert current[':question/problem'] == old[':question/problem']
            expected_field = originals[change['radio_field']]
            expected_field[':answer-field/correct'] = originals[change['correct_answer']]
            assert current[':question/answer-fields'] == [expected_field]
            continue
        assert change['action'] == 'convert_checkbox'
        assert current[':question/problem'] == change['problem_after']
        fields = {f[':answer-field/key']: f for f in current[':question/answer-fields']}
        assert len(fields) == len(current[':question/answer-fields']) == len(change['labels'])
        assert set(fields) == set(change['labels'])
        assert {f[':db/id'] for f in fields.values()} == {report[':edb/tempids'][t] for t in change['new_field_tempids']}
        for label, f in fields.items():
            token = change['ma_id'] + '/authored-checkbox-v1/' + label
            assert f[':answer-field/id'] == edb.stable_id('field', token)
            assert f[':answer-field/type'][':db/ident'] == ':answer-field.type/checkbox'
            bank = {a[':answer/value']: a for a in f[':answer-field/choices']}
            assert len(f[':answer-field/choices']) == 2 and set(bank) == {'false', 'true'}
            for value, answer in bank.items():
                assert answer[':answer/id'] == edb.stable_id('answer', token + '/' + value)
                assert answer[':answer/type'][':db/ident'] == ':answer.type/text'
            assert f[':answer-field/correct'] == bank[str(label in change['correct']).lower()]
            total_fields += 1
    assert total_fields == plan['counts']['new_checkbox_fields'] == 337
    database_keys_preserved = 0
    for resolved in resolutions['questions']:
        if not resolved['stored_keys']:
            continue
        current = after[resolved['id']]
        if resolved['action'] == 'convert_checkbox':
            actual_selected = {f[':answer-field/key'] for f in current[':question/answer-fields']
                if f[':answer-field/correct'][':answer/value'] == 'true'}
            for key in resolved['stored_keys']:
                mappings = [m for m in resolved['choice_mapping'] if m['old_value'] == key]
                assert mappings and all(set(m['selected']) == actual_selected for m in mappings)
        else:
            assert current[':question/answer-fields'][0][':answer-field/correct'][':answer/value'] in resolved['stored_keys']
        database_keys_preserved += 1
    assert database_keys_preserved == 50
    pattern = '''[* {:answer/type [:db/id :db/ident]}
        {:answer-field/type [:db/id :db/ident]}
        {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}
        {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]'''
    retained = {r[0][':db/id']:r[0] for r in edb.batches(
        '[:find (pull ?e ' + pattern + ') :in $ [?e ...] :where (or [?e :answer/id _] [?e :answer-field/id _])]',
        sorted(originals), 'originals-after', basis, 64)}
    assert retained == originals, 'Original field/answer entities changed beyond the explicit missing-key repair'
    assert set(originals) == set(plan['retained_original_entities'])
    items = edb.batches('[:find ?q (pull ?item ' + edb.ITEM + ') :in $ [?q ...] :where [?item :task-item/content ?q]]',
        sorted(before), 'items-after', basis, 64)
    assert items == snapshot['items'] == []
    answer_ids = sorted(aid for aid, entity in originals.items() if ':answer/id' in entity)
    users = edb.batches('[:find ?answer (pull ?item ' + edb.ITEM + ') :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',
        answer_ids, 'response-users-after', basis, 128)
    assert users == snapshot['response_users'] == []
    historical = {r[0][':db/id']:r[0] for r in edb.batches(query, sorted(before), 'questions-historical', plan['basis'])}
    assert historical == before, 'Historical view differs from the retained snapshot'
    edb.save('verification.json', {'passed':True, 'committed':True,
        'basis_before':plan['basis'], 'basis_after':basis, 'source':edb.SOURCE,
        'counts':plan['counts'], 'retained_original_entities':len(originals),
        'existing_database_keys_preserved':database_keys_preserved,
        'checks':['All 89 checkbox questions read back with the expected Boolean keys and prompts.',
            'All 50 existing database keys preserved under exact subset mappings.',
            'Radio questions preserved; only q-9852 receives its missing key and solution.',
            'Original answer/field entities retained, with only the explicitly planned radio-key addition.',
            'Authored solutions and five targeted worked-solution repairs match the plan.',
            'Question identity, KP membership and other content preserved.',
            'No learner presentation or response changed.',
            'Original historical question view reproduced at the captured basis.',
            'Committed datoms exactly match logical forms and use the agent source.']})
    print(json.dumps({'verified':True, 'basis_after':basis, 'checkbox_questions':89,
        'checkbox_fields':total_fields, 'database_keys_preserved':database_keys_preserved,
        'retained_original_entities':len(originals)}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['commit','verify'])
    globals()[parser.parse_args().action]()

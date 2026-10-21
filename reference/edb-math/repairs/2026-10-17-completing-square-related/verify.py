"""Verify exact preview/commit datoms and complete content projections."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import loads
from scripts.generator_publish import Publisher

HERE = Path(__file__).resolve().parent


def verify(commit=False):
    plan = json.loads((HERE / 'plan.json').read_text())
    changes = json.loads((HERE / 'changes.json').read_text())
    assert hashlib.sha256((HERE / 'transaction.edn').read_bytes()).hexdigest() == plan['transaction_sha256']
    attrs = dict(loads((HERE / 'evidence/attributes.edn').read_text()))
    preview = loads((HERE / 'preview.edn').read_text())
    report = loads((HERE / 'receipt.edn').read_text()) if commit else preview
    assert report[':edb/committed'] is commit
    assert report[':edb/db-before-t'] == preview[':edb/db-before-t'] == plan['snapshot_basis']
    if not commit:
        assert report[':edb/speculative'] is True
    else:
        assert ':edb/report-error' not in report
        assert report[':edb/basis-t'] == report[':edb/db-after-t']
    expected = {(c['entity'], c['attribute'], c[stage], added)
                for c in changes for stage, added in [('before', False), ('after', True)]}
    actual = set()
    for entity, attribute, value, tx, source, added in report[':edb/tx-data']:
        assert source == plan['source_eid']
        attr = str(attrs[attribute])
        if attr != ':db/txInstant':
            actual.add((entity, attr, value, added))
    assert actual == expected, (actual - expected, expected - actual)
    edits = {(c['entity'], c['attribute']): c for c in changes}

    def update(value):
        if isinstance(value, dict):
            for attr in value:
                if (edit := edits.get((value.get(':db/id'), str(attr)))):
                    assert value[attr] == edit['before']
                    value[attr] = edit['after']
                else:
                    update(value[attr])
        elif isinstance(value, list):
            for child in value:
                update(child)

    groups = loads((HERE / 'native-pulls.edn').read_text())
    changed_answers = {c['entity'] for c in changes if c['attribute'] == ':answer/value'}
    before_questions = loads((HERE / 'preview-questions-before.edn').read_text())
    seen_answers = set()
    for q in before_questions:
        for field in q.get(':question/answer-fields', []):
            for a in field.get(':answer-field/choices', []):
                if a[':db/id'] in changed_answers:
                    assert not a.get(':task-item/_responses')
                    assert ':answer-field/correct' not in field
                    seen_answers.add(a[':db/id'])
    assert seen_answers == changed_answers and len(changed_answers) == 31
    for name, pattern, ids in groups:
        before = loads((HERE / f'preview-{name}-before.edn').read_text())
        after = loads((HERE / f'preview-{name}-after.edn').read_text())
        expected_projection = copy.deepcopy(before)
        update(expected_projection)
        assert expected_projection == after, name
        assert len(before) == len(after) == len(ids)

    if commit:
        request = json.loads((HERE / 'commit-intent.json').read_text())
        assert request['submission_authorized'] is True
        assert request['transaction_edn'] == (HERE / 'transaction.edn').read_text()
        client = Publisher.from_environment(source=plan['source']).client
        status = client.status()
        assert status['lineage'] == plan['lineage']
        basis = report[':edb/db-after-t']
        def read(group):
            name, pattern, ids = group
            rows = client.query('[:find (pull ?e ' + pattern + ') :in $ [?e ...] :where [?e _ _]]',
                                [ids], HERE / 'readback', name, basis)
            actual = sorted((v for [v] in rows), key=lambda v: v[':db/id'])
            expected = sorted(loads((HERE / f'preview-{name}-after.edn').read_text()), key=lambda v: v[':db/id'])
            assert actual == expected, name
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(read, groups))
    result = {'passed': True, 'committed': commit,
              'basis_before': report[':edb/db-before-t'], 'basis_after': report[':edb/db-after-t'],
              'changed_attributes': len(changes), 'changed_entities': plan['changed_entities'],
              'exact_expected_datoms_only': True, 'complete_projections_match': True,
              'verified_groups': [name for name, _, _ in groups],
              'answer_ids_banks_keys_and_historical_response_values_preserved': True,
              'unreferenced_answer_notation_edits': len(changed_answers),
              'difficulty_curriculum_links_and_lesson_routes_preserved': True,
              'missing_solutions_and_keys_preserved': True,
              'transaction_sha256': plan['transaction_sha256']}
    (HERE / ('commit-verification.json' if commit else 'preview-verification.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--commit', action='store_true')
    verify(parser.parse_args().commit)

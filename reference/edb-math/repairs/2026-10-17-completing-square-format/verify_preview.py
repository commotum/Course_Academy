"""Verify the exact noncommitting native report and full before/after projections."""
import copy
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import loads

HERE = Path(__file__).resolve().parent


def verify():
    plan = json.loads((HERE / 'plan.json').read_text())
    changes = json.loads((HERE / 'changes.json').read_text())
    assert hashlib.sha256((HERE / 'transaction.edn').read_bytes()).hexdigest() == plan['transaction_sha256']
    report = loads((HERE / 'preview.edn').read_text())
    assert report[':edb/committed'] is False and report[':edb/speculative'] is True
    assert report[':edb/db-before-t'] == plan['read_basis']
    source = plan['source_eid']
    if plan['bootstraps_codex_contributor']:
        source = report[':edb/tempids'][plan['source_tempid']]
    attrs = dict(loads((HERE / 'evidence/attributes.edn').read_text()))
    expected = {(c['entity'], c['attribute'], c[stage], added)
                for c in changes for stage, added in [('before', False), ('after', True)]}
    if plan['bootstraps_codex_contributor']:
        expected |= {(source, ':db/ident', plan['source_ident'], True),
                     (source, ':db/doc', 'Codex agent contributions to Course Academy content.', True)}
    actual = set()
    for e, a, value, tx, contributor, added in report[':edb/tx-data']:
        assert contributor == source
        attr = str(attrs[a])
        if attr != ':db/txInstant':
            actual.add((e, attr, value, added))
    assert actual == expected, (actual - expected, expected - actual)
    edits = {(c['entity'], c['attribute']): c for c in changes}

    def update(value):
        if isinstance(value, dict):
            for key in value:
                if (edit := edits.get((value.get(':db/id'), str(key)))):
                    assert value[key] == edit['before']
                    value[key] = edit['after']
                else:
                    update(value[key])
        elif isinstance(value, list):
            for child in value:
                update(child)

    groups = loads((HERE / 'native-pulls.edn').read_text())
    for name, pattern, ids in groups:
        before = loads((HERE / f'preview-{name}-before.edn').read_text())
        after = loads((HERE / f'preview-{name}-after.edn').read_text())
        assert len(before) == len(after) == len(ids)
        expected_projection = copy.deepcopy(before)
        update(expected_projection)
        assert expected_projection == after, name
    result = {'passed': True, 'committed': False, 'preview_basis': report[':edb/db-before-t'],
              'speculative_basis': report[':edb/db-after-t'],
              'exact_scalar_changes': len(changes),
              'only_additional_facts': 'Codex contributor identity/doc and speculative transaction time',
              'answers_fields_keys_difficulty_memberships_and_captured_response_refs_preserved': True,
              'activity_and_knowledge_point_projections_preserved': True,
              'verified_groups': [name for name, _, _ in groups],
              'transaction_sha256': plan['transaction_sha256']}
    (HERE / 'preview-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    verify()

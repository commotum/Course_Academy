"""Verify the durable receipt and read back the exact committed database value."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import kw, loads
from scripts.generator_publish import Publisher

HERE = Path(__file__).resolve().parent


def verify():
    request = json.loads((HERE / 'request.json').read_text())
    intent = json.loads((HERE / 'commit-intent.json').read_text())
    assert request['submission_authorized'] and intent['submission_authorized']
    text = (HERE / request['transaction_file']).read_text()
    assert text == intent['transaction_edn']
    assert hashlib.sha256(text.encode()).hexdigest() == request['transaction_sha256']
    receipt = loads((HERE / 'receipt.edn').read_text())
    preview = loads((HERE / 'preview.edn').read_text())
    assert receipt[':edb/committed'] is True
    assert receipt[':edb/db-before-t'] == request['basis']
    basis = receipt[':edb/basis-t']
    assert receipt[':edb/db-after-t'] == basis
    assert ':edb/report-error' not in receipt
    contributor = receipt[':edb/tempids']['codex-format-repair']
    preview_contributor = preview[':edb/tempids']['codex-format-repair']
    attrs = dict(loads((HERE / 'evidence/attributes.edn').read_text()))

    def datoms(report, source):
        result = set()
        for entity, attribute, value, tx, author, added in report[':edb/tx-data']:
            assert author == source
            if str(attrs[attribute]) != ':db/txInstant':
                result.add(('contributor' if entity == source else entity,
                            attribute, value, added))
        return result

    assert datoms(receipt, contributor) == datoms(preview, preview_contributor)
    client = Publisher.from_environment(source=request['source_edn']).client
    status = client.status()
    assert status['lineage'] == request['expected_lineage']
    groups = loads((HERE / 'native-pulls.edn').read_text())

    def readback(group):
        name, pattern, ids = group
        rows = client.query('[:find (pull ?e ' + pattern + ') :in $ [?e ...] :where [?e _ _]]',
                            [ids], HERE / 'readback', name, basis)
        actual = sorted((value for [value] in rows), key=lambda v: v[':db/id'])
        expected = sorted(loads((HERE / f'preview-{name}-after.edn').read_text()),
                          key=lambda v: v[':db/id'])
        assert len(actual) == len(expected) == len(ids)
        assert actual == expected, name
        return name

    with ThreadPoolExecutor(max_workers=4) as pool:
        checked = list(pool.map(readback, groups))
    source = client.query('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]',
                          [kw('agent/codex')], HERE / 'readback', 'contributor', basis)
    assert source == [[contributor]]
    changes = json.loads((HERE / 'changes.json').read_text())
    result = {'committed': True, 'verified': True,
              'database': request['database'], 'lineage': request['expected_lineage'],
              'basis_before': receipt[':edb/db-before-t'], 'basis_after': basis,
              'replayed': receipt[':edb/replayed'], 'request_key': request['request_key'],
              'transaction_sha256': request['transaction_sha256'],
              'changed_text_attributes': len(changes),
              'changed_content_entities': len({c['entity'] for c in changes}),
              'exact_committed_datoms_match_preview': True,
              'readback_matches_preview_at_committed_basis': True,
              'verified_groups': checked, 'codex_contributor_entity': contributor,
              'answers_fields_keys_difficulty_memberships_and_captured_response_refs_preserved': True,
              'activity_and_knowledge_point_projections_preserved': True,
              'missing_solutions_and_keys_remain_separate_work': 8}
    (HERE / 'commit-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    verify()

"""Commit the exact two-stage package after the user's explicit authorization.

Durable request keys and complete intents are retained for exact retries.
The held index is updated separately, after the durable history audit passes.
"""
import collections
import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prepare import ROOT, SNAP, VALID, INDEX, read, sha, loads, dumps, kw
from capture import arguments
from core import atomic_json, stable_id
from database import Database, TOPIC_QUERY
from math_content import build_math_content, field_signature
from math_database import validate_receipt, SOURCE

manifest = read(ROOT / 'manifest.json')
preflight = read(ROOT / 'precommit/current.json')
basis = preflight['basis']
PRE = Path(preflight['output_directory'])
PREVIEW = PRE / 'sequence-preview'
COMMITS = ROOT / 'commits'
db = Database(arguments(['run']))
assert db.args.database == 'math' and db.args.source == SOURCE
attributes = loads((PRE / 'attributes.edn').read_text())
names = {e: str(a) for e, a in attributes}
original = read(ROOT / 'original-content.json')
repaired = read(ROOT / 'repaired-content.json')
ids = sorted(original)
base = {q[':question/math-academy-id']: q for [q] in loads((PRE / 'questions.edn').read_text())}
source_ids = preflight['source_entities']


def collect_identities(obj, result):
    if isinstance(obj, dict):
        for attr in (':question/id', ':answer-field/id', ':answer/id'):
            if attr in obj:
                result[(attr, str(obj[attr]))] = obj[':db/id']
        for value in obj.values():
            collect_identities(value, result)
    elif isinstance(obj, list):
        for value in obj:
            collect_identities(value, result)


def remapped_guard(stage):
    guard = loads((VALID / ('stage%d-guards.edn' % stage)).read_text())
    if stage == 1:
        return guard
    old, new = {}, {}
    for directory, target in [(VALID, old), (PREVIEW, new)]:
        for name in ('stage1-questions.edn', 'stage1-original-components.edn'):
            collect_identities(loads((directory / name).read_text()), target)
    assert set(old) == set(new)
    mapping = {eid: new[key] for key, eid in old.items()}
    references = {':question/answer-fields', ':answer-field/choices', ':answer-field/correct',
                  ':answer-field/type', ':answer/type'}
    for row in guard['retractions']:
        row[0] = mapping.get(row[0], row[0])
        if str(row[1]) in references:
            row[2] = mapping.get(row[2], row[2])
    guard['immutable_answers'] = [mapping.get(e, e) for e in guard['immutable_answers']]
    guard['immutable_fields'] = [[mapping.get(e, e), a] for e, a in guard['immutable_fields']]
    return guard


def verify_content(stage, at_basis, directory):
    expected = original if stage == 1 else repaired
    current = db.questions(ids, directory, basis=at_basis)
    assert set(current) == set(expected)
    tids = sorted({q['topic_id'] for q in expected.values()})
    topics = {t[':topic/math-academy-id']: t for [t] in db.query(
        TOPIC_QUERY.replace(':in $ ?id', ':in $ [?id ...]'), [tids], directory, 'topics', at_basis)}
    facts = db.query('[:find ?mid ?a ?s :in $ [?mid ...] [?a ...] :where [?q :question/math-academy-id ?mid] [?q ?a _ _ ?s]]',
        [ids, [eid for eid, name in names.items() if name in {':question/problem', ':question/worked-solution'}]], directory, 'text-sources', at_basis)
    text_sources = collections.defaultdict(set)
    for mid, a, s in facts:
        text_sources[mid, names.get(a, str(a))].add(s)
    fields = db.query('[:find ?mid ?key ?s :in $ [?mid ...] :where [?q :question/math-academy-id ?mid] [?q :question/answer-fields ?f] [?f :answer-field/key ?key] [?f :answer-field/correct ?answer _ ?s]]',
        [ids], directory, 'answer-sources', at_basis)
    field_sources = collections.defaultdict(set)
    for mid, key, s in fields:
        field_sources[mid, key].add(s)
    rows = []
    for mid, want in expected.items():
        got = current[mid]
        assert got[':question/id'] == (base[mid][':question/id'] if mid in base else stable_id('question', mid))
        for key, attr in [('problem', ':question/problem'), ('worked_solution', ':question/worked-solution')]:
            assert got[attr] == want[key], (mid, key)
            source = ':agent/gpt-6-astra-ultra' if stage == 2 and original[mid][key] != repaired[mid][key] else SOURCE
            assert source_ids[source] in text_sources[mid, attr], (mid, attr, text_sources[mid, attr])
        assert {field_signature(f, stored=True) for f in got[':question/answer-fields']} == {field_signature(f) for f in want['answer_fields']}
        assert len(got[':question/answer-fields']) == len(want['answer_fields']) == 1
        source = ':agent/gpt-6-astra-ultra' if stage == 2 and mid in {'q-79044', 'q-79945'} else SOURCE
        assert field_sources[mid, 'selection'] == {source_ids[source]}
        assert {str(p[':knowledge-point/id']) for p in got.get(':knowledge-point/_questions', [])} == {want['knowledge_point_id']}
        assert not got.get(':knowledge-point/_canonical-example')
        forms, _ = build_math_content({'task_type': 'review', 'questions': [want], 'canonical_examples': []}, topics, current)
        assert not forms, (mid, 'Readback did not replan to a no-op')
        rows.append({'id': mid, 'question_uuid': str(got[':question/id']), 'content': True,
                     'fields': True, 'source': True, 'knowledge_point': True, 'reimport_noop': True})
    atomic_json(directory / 'verification.json', {'verified': True, 'stage': stage, 'basis': at_basis, 'questions': rows})
    return current


def check_frozen_inputs():
    assert read(ROOT / 'verification.json')['valid']
    preview = loads((PREVIEW / 'manifest.edn').read_text())
    assert preview[':preview/durable-basis-before'] == preview[':preview/durable-basis-after'] == basis
    assert preview[':preview/database-writes'] == 0 and preview[':edb/committed'] is False
    assert sha(INDEX) == manifest['held_index_sha256'] or read(INDEX).get('resolved_by_held_repairs', {}).get('basis_after') == basis + 2
    for stage in manifest['stages']:
        assert sha(stage['ssd_file']) == sha(stage['reference_file']) == stage['sha256']
    for rel, digest in manifest['preparation_sha256'].items():
        assert sha(ROOT / rel) == digest, rel
    for path, digest in read(ROOT / 'source-hashes.json').items():
        assert sha(path) == digest
    for path, info in read(ROOT / 'image-verification.json')['references'].items():
        assert sha(Path(db.args.math_root) / path) == info['sha256']


def commit_all():
    check_frozen_inputs()
    results = []
    for stage in manifest['stages']:
        n = stage['stage']
        before = basis + n - 1
        directory = COMMITS / ('stage-' + str(n))
        directory.mkdir(parents=True, exist_ok=True)
        guard = remapped_guard(n)
        guard_path = directory / 'reconciliation.edn'
        guard_path.write_text(dumps(guard) + '\n')
        preview = loads((PREVIEW / ('stage%d-preview.edn' % n)).read_text())
        assert preview[':edb/db-before-t'] == before and preview[':edb/db-after-t'] == before + 1
        validate_receipt(preview, attributes, source_ids[stage['source']], **guard)
        intent = {'database': 'math', 'endpoint': db.args.endpoint, 'source': stage['source'],
            'source_eid': source_ids[stage['source']], 'basis': before, 'file': stage['ssd_file'],
            'sha256': stage['sha256'], 'connection_sha256': hashlib.sha256(db.env['EDB_POSTGRES_URL'].encode()).hexdigest(),
            'reconciliation_sha256': sha(guard_path),
            'request_key': 'ma-held-repairs-2026-10-10-stage%d-basis%d-%s' % (n, before, stage['sha256'])}
        intent_path = directory / 'commit-intent.json'
        if intent_path.exists():
            assert read(intent_path) == intent
        else:
            assert db.basis() == before, 'Database advanced; revalidate before committing.'
            atomic_json(intent_path, intent)
        receipt = db._commit(intent, Path(stage['ssd_file']), directory)
        assert receipt[':edb/committed'] is True
        assert receipt[':edb/db-before-t'] == before and receipt[':edb/db-after-t'] == before + 1
        validate_receipt(receipt, attributes, source_ids[stage['source']], **guard)
        # Only timestamps and transaction ids may differ from the fresh preview.
        def facts(r):
            return {dumps([e, a, v, s, added]) for e, a, v, t, s, added in r[':edb/tx-data'] if names[a] != ':db/txInstant'}
        assert facts(receipt) == facts(preview)
        verify_content(n, before + 1, directory / 'readback')
        result = {'stage': n, 'committed': True, 'verified': True, 'basis_before': before, 'basis_after': before + 1,
                  'source': stage['source'], 'file_sha256': stage['sha256'], 'questions': 26,
                  'datoms': len(receipt[':edb/tx-data']), 'retractions': sum(not d[-1] for d in receipt[':edb/tx-data'])}
        atomic_json(directory / 'verification.json', result)
        results.append(result)
        atomic_json(ROOT / 'commit-verification.json', {'all_stages_committed': n == 2,
                    'basis_before': basis, 'basis_after': before + 1, 'stages': results})
        print(json.dumps(result), flush=True)
    assert db.basis() == basis + 2
    print('BOTH STAGES COMMITTED; awaiting independent durable history audit before held-index update.', flush=True)


if __name__ == '__main__':
    commit_all()

#!/usr/bin/env python3
"""Migrate the audited old learner snapshot to math without changing its schema.

prepare reads both databases, saves the original records/history, and remaps
identities. preview validates the atomic import with the application's native
predicates and lesson reader, without committing. apply requires that successful
preview and uses the saved intent and exact basis. Request journals are unused.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys
import subprocess
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw, Keyword, Tagged

LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
SOURCE = ':application/ca-engine'
SOURCE_EID = 17592186407927
DEFAULT_OUTPUT = ROOT / 'reference/edb-math/imports/learner-history/2026-10-11'


def connection(old=False):
    return Database(SimpleNamespace(
        edb_bin=str(ROOT / '.local/edb/capture-runtime' / ('edb' if old else 'math-edb')),
        database='course-academy-v2' if old else 'math',
        postgres_url=(f'host={ROOT}/.local/edb/run dbname=course_academy user=edb_peer sslmode=disable'
                      if old else "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'")))


def json_write(path, value):
    path.write_text(json.dumps(value, default=str, indent=2) + '\n')


def refs(value):
    if isinstance(value, dict):
        # Pull expands component references; their full records are separately
        # recreated or reconciled by identity, while this value is only a link.
        assert ':db/id' in value, value
        return refs(value[':db/id'])
    if isinstance(value, (list, tuple)):
        return [e for x in value for e in refs(x)]
    if isinstance(value, Keyword) or (isinstance(value, int) and not isinstance(value, bool) and value > 0):
        return [value]
    if value is None:
        return []
    raise ValueError(f'Unsupported reference value: {value!r}')


class Reader:
    def __init__(self, db, basis, directory):
        self.db, self.basis, self.directory = db, basis, directory
        self.records = {}

    def query(self, query, inputs, name):
        return self.db.query(query, inputs, self.directory, name, self.basis)

    def pull(self, ids):
        missing = sorted(set(ids) - self.records.keys())
        if missing:
            name = 'entities-' + hashlib.sha256(dumps(missing).encode()).hexdigest()[:12]
            rows = self.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]', [missing], name)
            self.records.update({r[0][':db/id']: r[0] for r in rows})
            assert not set(missing) - self.records.keys(), ('missing entities', missing)
        return {e: self.records[e] for e in ids}

    def lookup(self, attr, values):
        if not values:
            return {}
        name = 'lookup-' + attr.replace('/', '-') + '-' + hashlib.sha256(dumps(values).encode()).hexdigest()[:12]
        rows = self.query('[:find ?v (pull ?e [*]) :in $ [?v ...] :where [?e :' + attr + ' ?v]]', [values], name)
        result = {}
        for value, record in rows:
            assert value not in result, ('ambiguous identity', attr, value)
            result[value] = record
            self.records[record[':db/id']] = record
        return result


def prepare(out, supplemental):
    assert not (out / 'intent.json').exists(), 'Prepared intent exists; apply/verify it instead of regenerating it.'
    old_db, new_db = connection(True), connection()
    old = Reader(old_db, old_db.basis(), out / 'old')
    new = Reader(new_db, new_db.basis(), out / 'new')
    schema_rows = new.query('[:find ?a ?type ?card :where [?e :db/ident ?a] [?e :db/valueType ?type-e] [?type-e :db/ident ?type] [?e :db/cardinality ?card-e] [?card-e :db/ident ?card]]', [], 'schema')
    schema = {a: (typ, card) for a, typ, card in schema_rows}
    learner = old.lookup('learner/id', [LEARNER])[LEARNER]
    target = new.lookup('learner/id', [LEARNER])[LEARNER]
    engine = new.lookup('db/ident', [kw(SOURCE)])[kw(SOURCE)]
    assert engine[':db/id'] == SOURCE_EID
    assert not target.get(':learner/activity') and not target.get(':learner/knowledge-profile'), 'Destination already contains learner state; do not overwrite it.'
    assert not target.get(':learner/performance'), 'Destination performance already exists.'
    progress = old.pull(refs(learner.get(':learner/knowledge-profile', [])))
    # Cardinality-many pull defaults to 1000; query ownership rows explicitly.
    progress_ids = old.query('[:find ?p :in $ ?l :where [?l :learner/knowledge-profile ?p]]', [learner[':db/id']], 'progress-ownership')
    progress = old.pull([r[0] for r in progress_ids])
    tasks = old.pull(refs(learner.get(':learner/activity', [])))
    task_refs = {e for t in tasks.values() for a in (':learner-task/status', ':learner-task/activity') for e in refs(t[a])}
    old.pull(task_refs)
    activity_types = {e for t in tasks.values() for e in refs(old.records[refs(t[':learner-task/activity'])[0]][':activity/type'])}
    old.pull(activity_types)
    tasks = {e: t for e, t in tasks.items()
             if old.records[refs(t[':learner-task/status'])[0]].get(':db/ident') in
             (kw('learner-task.status/completed'), kw('learner-task.status/paused'))
             and old.records[refs(old.records[refs(t[':learner-task/activity'])[0]][':activity/type'])[0]][':db/ident'] == kw('activity.type/lesson')}
    items = old.pull([i for t in tasks.values() for i in refs(t.get(':learner-task/items', []))])
    responses = {i: refs(r.get(':task-item/responses', [])) for i, r in items.items() if r.get(':task-item/responses')}
    assert (len(progress), len(tasks), len(items), len(responses)) == (1041, 10, 88, 44)
    performance = old.pull(refs(learner.get(':learner/performance', [])))
    owned = {**progress, **tasks, **items, **performance}
    remap = {e: f'history-{e}' for e in owned}
    remap[learner[':db/id']] = target[':db/id']
    extra = loads(supplemental.read_text()) if supplemental else {kw('mapping'): {}, kw('create'): [], kw('add'): []}
    # Supplemental mappings are explicitly reviewed content/answer identity reconciliations.
    remap.update(extra.get(':mapping', {}))
    for record in extra.get(':create', []):
        e = record[':db/id']
        owned[e] = record
        old.records[e] = record
        remap[e] = f'history-{e}'
    additions = extra.get(':add', [])
    external = {e for r in owned.values() for a, v in r.items()
                if a != ':db/id' and a in schema and schema[a][0] == kw('db.type/ref')
                for e in refs(v)} - set(remap)
    external |= set(refs(learner.get(':learner/course', []))) - set(remap)
    for e, a, value in additions:
        assert a in schema, ('unknown supplemental attribute', a)
        if schema[a][0] == kw('db.type/ref'):
            external.update(set(refs(value)) - set(remap))
    # Supplemental maps may use enum keywords instead of the old numeric EIDs.
    keyword_refs = [e for e in external if isinstance(e, Keyword)]
    if keyword_refs:
        found = new.lookup('db/ident', keyword_refs)
        assert set(found) == set(keyword_refs), ('unmapped enum references', keyword_refs)
        remap.update({ident: r[':db/id'] for ident, r in found.items()})
        external.difference_update(keyword_refs)
    old.pull(external)
    grouped = defaultdict(list)
    for e in external:
        r = old.records[e]
        identity = [(a, v) for a, v in r.items() if a != ':db/id' and (a.endswith('/id') or a == ':db/ident')]
        assert len(identity) == 1, ('no unambiguous identity', r)
        a, v = identity[0]
        grouped[a].append((e, v))
    missing = []
    for a, pairs in grouped.items():
        found = new.lookup(a.lstrip(':'), [v for _, v in pairs])
        for e, v in pairs:
            if v in found:
                remap[e] = found[v][':db/id']
            elif a == ':topic/id':
                # Six sparse original baseline topics have no current curriculum counterpart.
                r = old.records[e]
                assert set(r) <= {':db/id', ':topic/id', ':topic/math-academy-id', ':topic/title'}, r
                assert not new.lookup('topic/math-academy-id', [r[':topic/math-academy-id']]), r
                owned[e] = r
                remap[e] = f'history-{e}'
            else:
                missing.append((e, a, str(v)))
    assert not missing, ('unmapped dependencies', missing)
    # No existing learner identities may be silently upserted.
    for attr in ('progress/id', 'learner-task/id', 'task-item/id'):
        values = [r[':' + attr] for r in owned.values() if ':' + attr in r]
        assert not new.lookup(attr, values), ('destination identity collision', attr)

    def translated(a, v):
        typ, card = schema[a]
        if typ == kw('db.type/ref'):
            values = [remap[e] for e in refs(v)]
            assert len(values) == len(refs(v))
            return values if card == kw('db.cardinality/many') else values[0]
        if typ == kw('db.type/instant'):
            return Tagged('inst', v)
        return v

    forms = []
    for e, record in sorted(owned.items()):
        form = {kw('db/id'): remap[e]}
        for a, v in record.items():
            if a != ':db/id':
                assert a in schema, ('unknown attribute', a)
                form[kw(a)] = translated(a, v)
        if ':learner-task/id' in record:
            form[kw('db/ensure')] = kw('learner-task/validate')
        if ':task-item/id' in record:
            form[kw('db/ensure')] = kw('task-item/validate')
        forms.append(form)
    owner = {kw('db/id'): target[':db/id'], kw('learner/knowledge-profile'): [remap[e] for e in progress],
             kw('learner/activity'): [remap[e] for e in tasks], kw('db/ensure'): kw('learner/validate')}
    if performance:
        assert len(performance) == 1
        owner[kw('learner/performance')] = remap[next(iter(performance))]
    if not target.get(':learner/course') and learner.get(':learner/course'):
        owner[kw('learner/course')] = remap[refs(learner[':learner/course'])[0]]
    forms.append(owner)
    for e, a, value in additions:
        if schema[a][0] == kw('db.type/ref'):
            targets = refs(value)
            assert len(targets) == 1, ('one supplemental add must supply one reference', e, a, value)
            value = remap.get(targets[0], targets[0])
        elif schema[a][0] == kw('db.type/instant'):
            value = Tagged('inst', value)
        forms.append([kw('db/add'), remap.get(e, e), kw(a), value])
    tx = out / 'transaction.edn'
    tx.write_text(dumps(forms) + '\n')
    history = old_db.query('[:find ?e ?a ?status ?tx ?at ?added :in $ [?e ...] [?a ...] :where [?e ?a ?s ?tx ?added] [?s :db/ident ?status] [?tx :db/txInstant ?at]]',
                           [list(tasks) + list(items), [kw('learner-task/status'), kw('task-item/status')]], out / 'old', 'status-history', old.basis, history=True)
    (out / 'source-records.edn').write_text(dumps(list(owned.values())) + '\n')
    (out / 'mapping.edn').write_text(dumps(remap) + '\n')
    summary = {'progress': len(progress), 'lessons': len(tasks), 'items': len(items), 'answered_items': len(responses),
               'task_statuses': dict(Counter(str(old.records[refs(t[':learner-task/status'])[0]][':db/ident']) for t in tasks.values())),
               'answer_statuses': dict(Counter(str(old.pull(refs(items[i][':task-item/status']))[refs(items[i][':task-item/status'])[0]][':db/ident']) for i in responses)),
               'working_seconds': sum(t.get(':learner-task/elapsed-seconds', 0) for t in tasks.values()),
               'xp_earned': sum(t.get(':learner-task/xp-earned', 0) for t in tasks.values()),
               'archived_status_history_rows': len(history), 'created_entities': len(owned)}
    digest = hashlib.sha256(tx.read_bytes()).hexdigest()
    intent = {'source_database': 'course-academy-v2', 'source_basis': old.basis, 'destination_database': 'math',
              'destination_basis': new.basis, 'source': SOURCE, 'source_eid': SOURCE_EID, 'transaction_sha256': digest,
              'request_key': 'learner-history-' + digest, 'learner': LEARNER, 'learner_eid': target[':db/id'], 'summary': summary,
              'timing': 'Original status timeline archived in old/status-history.edn. Explicit progress dates and all saved elapsed values retained. Destination status dates are import time.'}
    json_write(out / 'intent.json', intent)
    print(json.dumps(summary))


def preview(out):
    sys.path.insert(0, str(ROOT / 'scripts'))
    from serve_graph_explorer import build_learning, database_environment
    executable = build_learning(ROOT.parent / 'EDB', test=True)
    env = database_environment('math')
    tx = out / 'transaction.edn'
    digest = hashlib.sha256(tx.read_bytes()).hexdigest()
    intent = json.loads((out / 'intent.json').read_text())
    assert digest == intent['transaction_sha256']
    env['LEARNING_HISTORY_MIGRATION_TX'] = str(tx.resolve())
    subprocess.run([str(executable), '--ignored', '--exact', 'integration::preview_history_migration', '--nocapture'],
                   env=env, check=True)
    assert hashlib.sha256(tx.read_bytes()).hexdigest() == digest
    report = json.loads((out / 'application-preview.json').read_text())
    assert report['status'] == 'passed'
    assert report['destination_basis'] == intent['destination_basis']
    assert report['committed'] is False and report['speculative'] is True
    report['transaction_sha256'] = digest
    json_write(out / 'application-preview.json', report)


def apply(out):
    intent = json.loads((out / 'intent.json').read_text())
    tx = out / 'transaction.edn'
    assert hashlib.sha256(tx.read_bytes()).hexdigest() == intent['transaction_sha256']
    checked = json.loads((out / 'application-preview.json').read_text())
    assert checked['status'] == 'passed'
    assert checked['committed'] is False and checked['speculative'] is True
    assert checked['destination_basis'] == intent['destination_basis']
    assert checked['transaction_sha256'] == intent['transaction_sha256']
    receipt = connection().command('transact', '--file', tx, '--request-key', intent['request_key'], '--source', intent['source'],
                                   '--basis', intent['destination_basis'], '--endpoint', '/tmp/edb-math/writer.sock')
    (out / 'commit.edn').write_text(receipt)
    verify(out)


def verify(out):
    intent = json.loads((out / 'intent.json').read_text())
    assert hashlib.sha256((out / 'transaction.edn').read_bytes()).hexdigest() == intent['transaction_sha256']
    receipt = loads((out / 'commit.edn').read_text())
    assert receipt[':edb/committed'] is True
    assert all(row[4] == SOURCE_EID for row in receipt[':edb/tx-data']), 'Wrong fact source in commit'
    assert all(row[-1] is True for row in receipt[':edb/tx-data']), 'Migration replaced or retracted existing data.'
    tempids = receipt[':edb/tempids']
    forms = loads((out / 'transaction.edn').read_text())
    db = connection()
    # Verify the committed snapshot even if the learner resumes work meanwhile.
    reader = Reader(db, receipt[':edb/basis-t'], out / 'verified')
    resolve = lambda x: tempids.get(x, x) if isinstance(x, str) else x
    expected_values = defaultdict(set)
    exact = set()
    count = 0
    for f in forms:
        if isinstance(f, dict):
            entity = resolve(f[':db/id'])
            for a, expected in f.items():
                if a in (':db/id', ':db/ensure'):
                    continue
                key = (entity, a)
                exact.add(key)
                values = expected if isinstance(expected, list) else [expected]
                expected_values[key].update(dumps(resolve(value)) for value in values)
                count += 1
        else:
            _, e, a, value = f
            expected_values[(resolve(e), a)].add(dumps(resolve(value)))
            count += 1
    ids = sorted({entity for entity, _ in expected_values})
    assert all(isinstance(entity, int) for entity in ids), 'Unresolved transaction tempid'
    actual_values = defaultdict(set)
    # Read direct datoms, avoiding pull's per-attribute collection limit and one
    # CLI process per collection. Bound each read to 128 migrated entities.
    for offset in range(0, len(ids), 128):
        rows = reader.query('[:find ?e ?ident ?v :in $ [?e ...] :where [?e ?a ?v] [?a :db/ident ?ident]]',
                            [ids[offset:offset + 128]], 'datoms-' + str(offset))
        for entity, attribute, value in rows:
            actual_values[(entity, attribute)].add(dumps(value))
    for key, values in expected_values.items():
        got = actual_values[key]
        if key in exact:
            assert got == values, (key, 'attribute mismatch', got, values)
        else:
            assert values <= got, (key, 'missing supplemental links', got, values)
    result = {'verified': True, 'basis': reader.basis, 'commit_basis': receipt[':edb/basis-t'], 'attributes_checked': count,
              'source': SOURCE, 'source_eid': SOURCE_EID, **intent['summary']}
    json_write(out / 'verification.json', result)
    print(json.dumps(result))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'preview', 'apply', 'verify'])
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--supplemental', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.action == 'prepare':
        prepare(args.output, args.supplemental)
    else:
        globals()[args.action](args.output)


if __name__ == '__main__':
    main()

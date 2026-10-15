"""Scoped additive EDB replenishment; application lock spans recheck to readback."""
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts/question_capture')]
from database import Database, StaleBasis
from edn import dumps, kw, loads
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('inventory_validation', HERE / 'validate_inventory.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '7e624f9de3799a28b6de38a3ff34b13a8368f0d1a88f69302b4ab8a1d176da81'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env = ENV
NATIVE = ROOT / '.local/graph-explorer/learning-c9743ced043e1fd7'
QUERY = (HERE / 'reference/initial/kp-query.edn').read_text()
USAGE = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''


def inventory(path):
    p = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=ENV, capture_output=True, text=True, check=True, timeout=90)
    result = json.loads(p.stdout)
    assert result['ok'] and result['data']['lineage'] == LINEAGE
    save(path, result['data'])
    return result['data']


def read_kp(path, basis):
    rows = DB.query(QUERY, [KP], path, 'kp', basis)
    assert len(rows) == 1
    kp = rows[0][0]
    assert str(kp[':knowledge-point/id']) == g.KP[':knowledge-point/id']
    return kp


def known_records():
    records = {}
    for p in OUT.glob('basis-*/generated.json'):
        for r in json.loads(p.read_text()):
            records[r['question'][':question/id']] = r
    return records


def counts(kp, path, basis):
    path.mkdir(parents=True, exist_ok=True)
    used = {row[0] for row in DB.query(USAGE, [KP, LEARNER], path, 'usage', basis)}
    validation = json.loads((HERE / 'reference/validation-current/validation.json').read_text())
    sources = {r['source_id']: r for r in validation['current_sources']}
    generated = known_records()
    levels = {l: [] for l in ('easy', 'moderate', 'hard')}
    excluded, grade = [], []
    tasks = {l: set() for l in levels}
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in used or q.get(':knowledge-point/_canonical-example'):
            excluded.append({'question_id': str(q[':question/id']), 'reason': 'shown, reserved, or canonical'})
            continue
        level = q.get(':question/difficulty', {}).get(':db/ident', '').split('/')[-1]
        mid, qid = q.get(':question/math-academy-id'), str(q[':question/id'])
        if mid in sources:
            assert sources[mid]['record_sha256'] == g.digest(v.normalized(q)), 'Source changed: reclassify before counting'
            record = v.source_record(q)
        elif qid in generated:
            record = generated[qid]
            assert v.normalized(q) == v.normalized(record['question'])
            v.check(record)
        else:
            raise ValueError('Unvalidated pool content: ' + qid)
        assert level in v.LEVELS
        tasks[level].add(v.fingerprint(q))
        levels[level].append(qid)
        grade.append(record)
    native = v.run_native(grade, path)
    result = {'basis': basis, 'distinct_available': {l: len(tasks[l]) for l in levels}, 'question_ids': levels, 'excluded': excluded, 'excluded_shown_or_reserved': sorted(used), 'actual_learner_grading': {k: native[k] for k in ('accepted_checks', 'rejected_checks', 'documented_unresolved_checks')}}
    save(path / 'counts.json', result)
    return result


def transaction(records, kp, gid):
    forms = []
    for r in records:
        q = r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'): a[':answer/id'], kw('answer/id'): uuid.UUID(a[':answer/id']), kw('answer/type'): kw(a[':answer/type']), kw('answer/value'): a[':answer/value'], kw('db/ensure'): kw('answer/validate')})
            forms.append({kw('db/id'): f[':answer-field/id'], kw('answer-field/id'): uuid.UUID(f[':answer-field/id']), kw('answer-field/key'): f[':answer-field/key'], kw('answer-field/type'): kw(f[':answer-field/type']), kw('answer-field/choices'): [a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'): f[':answer-field/correct'][1], kw('db/ensure'): kw('answer-field/validate')})
        forms.append({kw('db/id'): q[':question/id'], kw('question/id'): uuid.UUID(q[':question/id']), kw('question/problem'): q[':question/problem'], kw('question/worked-solution'): q[':question/worked-solution'], kw('question/difficulty'): kw(q[':question/difficulty']), kw('question/answer-fields'): [f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'): kw('question/validate')})
    generator = kp.get(':knowledge-point/question-generator')
    if generator:
        assert str(generator[':question-generator/id']) == gid and generator[':question-generator/script'] == SCRIPT
    else:
        forms.extend([{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid), kw('question-generator/script'): SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    if records:
        forms.append({kw('db/id'): KP, kw('knowledge-point/questions'): [r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms


def check_report(report, path, source):
    attrs = dict(DB.attributes(path, report[':edb/db-before-t']))
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for entity, attr, value, tx, contributor, added in report[':edb/tx-data']:
        name = str(attrs[attr])
        assert contributor == source and added, 'Unexpected attribution or retraction'
        if entity == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert entity in new and name in allowed, 'Unexpected existing entity or attribute'


def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path / 'receipt-check', intent['source_eid'])
    basis = report[':edb/db-after-t']
    kp = read_kp(path / 'readback', basis)
    before = loads((path / 'before.edn').read_text())
    old = {q[':db/id']: q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e, q in old.items()), 'Existing source or pool content changed'
    assert {k: x for k, x in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')} == {k: x for k, x in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path / 'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']): q for q in now.values()}
    for r in records:
        q = byid[r['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert v.normalized(q) == v.normalized(r['question'])
        v.check(r)
    after = counts(kp, path / 'readback', basis)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': basis, 'new_questions': len(records), 'unchanged_existing_questions': len(old), 'learner_history_unchanged': True, 'datoms_only_add_scoped_content': True, 'attribution_verified': SOURCE, 'generator_registration_verified': True, 'repeat_preparation_content_changes': 0, 'available_counts_after': after}
    save(path / 'verification.json', result)
    return result


def finish(path, intent, verification, inv):
    counts_after = verification['available_counts_after']['distinct_available']
    prep = json.loads((path / 'preparation.json').read_text())
    remaining = {l: max(0, 5 - counts_after[l]) for l in ('easy', 'moderate', 'hard')}
    result = {'outcome': 'finite-limit' if any(remaining.values()) else 'generated', 'knowledgePoint': KP, 'generator_path': SCRIPT, 'generator_id': intent['generator_id'], 'lineage': LINEAGE, 'verified_commit_basis': verification['basis_after'], 'new_questions': verification['new_questions'], 'supported_levels': list(v.LEVELS), 'unsupported_levels': ['hard'], 'available_counts_before': prep['counts_before']['distinct_available'], 'available_counts_after': counts_after, 'shortage_remaining': remaining, 'capability_exceptions': [{'difficulty': 'hard', 'kind': 'unsupported-within-extracted-package', 'missing': remaining['hard'], 'evidence': str((HERE / 'reference/current-classification.md').relative_to(ROOT)), 'reason': 'Existing hard draft adds xy outside the source expression backbone. Public generation rejects it. No claim that the hard reserve is filled.'}], 'unsupported_levels_filled': False, 'inventory_recheck_basis': inv['basis'], 'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP], 'evidence': [str(p.relative_to(ROOT)) for p in (path / 'verification.json', path / 'commit-intent.json', path / 'transaction.edn', path / 'commit.edn', path / 'preview.edn', path / 'preparation.json', path / 'inventory-after.json', HERE / 'reference/validation-current/validation.json', HERE / 'reference/current-classification.md')]}
    save(path / 'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps(result), flush=True)


def main():
    validation = json.loads((HERE / 'reference/validation-current/validation.json').read_text())
    assert validation['status'] == 'passed'
    for key, p in [('generator_sha256', HERE.with_suffix('.py')), ('validator_sha256', HERE / 'validate.py'), ('inventory_validator_sha256', HERE / 'validate_inventory.py'), ('engine_sha256', HERE / 'reference/check-engine-current')]:
        assert validation[key] == v.sha(p), key
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    print('Waiting for application api.lock', flush=True)
    with (ROOT / '.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        print('Application api.lock acquired', flush=True)
        inv = inventory(OUT / 'inventory-under-lock.json')
        for p in sorted(OUT.glob('basis-*')):
            if not (p / 'commit-intent.json').exists():
                continue
            intent = json.loads((p / 'commit-intent.json').read_text())
            assert intent['database'] == 'math' and intent['endpoint'] == DB.args.endpoint and intent['lineage'] == inv['lineage']
            assert intent['source'] == SOURCE and intent['exact_edn'] == (p / 'transaction.edn').read_text()
            assert intent['transaction_sha256'] == v.sha(p / 'transaction.edn') and intent['connection_sha256'] == hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
            report = DB._commit(intent, p / 'transaction.edn', p)
            finish(p, intent, verify(p, intent, report), inventory(p / 'inventory-after.json'))
            return
        basis = inv['basis']
        assert DB.basis() == basis
        path = OUT / ('basis-' + str(basis))
        path.mkdir(exist_ok=True)
        kp = read_kp(path, basis)
        (path / 'before.edn').write_text(dumps(kp) + '\n')
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', basis)
        assert len(source) == 1
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else v.GENERATOR_UUID
        orphan = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [uuid.UUID(gid)], path, 'generator-identity', basis)
        if orphan:
            assert orphan[0][0][':question-generator/script'] == SCRIPT
        available = counts(kp, path / 'counts-before', basis)
        needed = {l: max(0, 5 - available['distinct_available'][l]) for l in v.LEVELS}
        candidates = []
        # Only sample actual shortages, after current-basis availability checks.
        for level in v.LEVELS:
            if not needed[level]:
                continue
            for i in range(max(12, needed[level] * 3)):
                r = g.generate(level, 264800 + i)
                v.check(r)
                candidates.append(r)
        used = {v.fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(v.fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances', [])
        assert isinstance(instances, list)
        for r in instances:
            v.check(r)
        save(path / 'supplied-status.json', {'exists': supplied_path.exists(), 'validated_instances': len(instances)})
        records, added = [], {l: 0 for l in v.LEVELS}
        for r in instances + candidates:
            level = r['question'][':question/difficulty'].split('/')[-1]
            fp = v.fingerprint(r['question'])
            if added[level] < needed[level] and fp not in used:
                records.append(r)
                used.add(fp)
                added[level] += 1
        assert added == needed, 'Finite sampled capacity below supported shortage; retain explicit exception before submission'
        identifiers = [uuid.UUID(i) for r in records for i in [r['question'][':question/id']] + [f[':answer-field/id'] for f in r['question'][':question/answer-fields']] + [a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        matches = DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]', [identifiers], path, 'identity-matches', basis) if identifiers else []
        assert not matches, 'Existing content identity requires reconciliation'
        save(path / 'generated.json', records)
        v.run_native(records, path / 'grading')
        (path / 'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records) + '\n')
        save(path / 'preparation.json', {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE, 'counts_before': available, 'supported_missing': needed, 'new_by_level': added, 'hard_shortage_explicit': max(0, 5 - available['distinct_available']['hard']), 'distinct_generated_mathematical_tasks': len({v.fingerprint(r['question']) for r in records}), 'generator_sha256': v.sha(HERE.with_suffix('.py')), 'generator_id': gid, 'parameters': [r['generation'] for r in records], 'assets': [], 'source_read_basis': validation['source_read_basis']})
        forms = transaction(records, kp, gid)
        if not forms:
            verification = {'passed': True, 'basis_after': basis, 'new_questions': 0, 'available_counts_after': available, 'no_changes': True}
            save(path / 'verification.json', verification)
            finish(path, {'generator_id': gid}, verification, inv)
            return
        txpath = path / 'transaction.edn'
        tx = dumps(forms) + '\n'
        with txpath.open('w') as stream:
            stream.write(tx)
            stream.flush()
            os.fsync(stream.fileno())
        fresh = inventory(path / 'inventory-precommit.json')
        assert fresh['basis'] == basis and DB.basis() == basis
        p = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=ENV, capture_output=True, text=True, check=True, timeout=90)
        (path / 'preview.edn').write_text(p.stdout)
        pr = loads(p.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == basis
        check_report(pr, path / 'preview-check', source[0][0])
        assert DB.basis() == basis
        if '--prepare-only' in sys.argv:
            print('Native preview passed; prepared ' + str(path), flush=True)
            return
        intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': source[0][0], 'basis': basis, 'expected_basis': basis, 'request_key': 'surface-inventory-' + str(KP) + '-' + str(basis) + '-' + v.sha(txpath), 'transaction_sha256': v.sha(txpath), 'sha256': v.sha(txpath), 'exact_edn': tx, 'generator_id': gid, 'generator_path': SCRIPT, 'generator_sha256': v.sha(HERE.with_suffix('.py')), 'question_uuids': [r['question'][':question/id'] for r in records], 'connection_sha256': hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(ROOT / '.local/learning/requests/math/api.lock')}
        save(path / 'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        finish(path, intent, verify(path, intent, report), inventory(path / 'inventory-after.json'))


if __name__ == '__main__':
    main()

"""Replenish only this KP through the configured EDB writer and application lock."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
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
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('segment_validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '5f52cc3fa7329486ee6f9bf5857d25f90722bd4b54542bcff918b9b121e6285d'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = max((p for p in (ROOT / '.local/graph-explorer').glob('learning-*') if p.is_file() and p.stat().st_mode & 0o111), key=lambda p: p.stat().st_mtime)
QUERY = (HERE / 'reference/source-query.edn').read_text()
USAGE = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?task] [?task :learner-task/items ?item] [?item :task-item/content ?q])
  (and [?l :learner/activity ?task] [?task :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?task :learner-task/activity ?activity] [?activity :activity/steps ?step] [?step :step/content ?q]))]'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value, strip_evidence=False):
    if isinstance(value, dict):
        return {str(k): canonical(x, strip_evidence) for k, x in value.items()
                if not strip_evidence or (str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_'))}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x, strip_evidence) for x in value), key=lambda x: json.dumps(x, sort_keys=True))
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


def inventory(path):
    result = subprocess.run([str(NATIVE), 'math', LEARNER, ENV['EDB_ENDPOINT']], input='{"action":"inventory"}', env=ENV, capture_output=True, text=True, check=True, timeout=90)
    obj = json.loads(result.stdout)
    assert obj['ok'] and obj['data']['lineage'] == LINEAGE
    save(path, obj['data'])
    return obj['data']


def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]


def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in q[':question/answer-fields']:
        result[':question/answer-fields'].append({':answer-field/id': str(f[':answer-field/id']), ':answer-field/key': f[':answer-field/key'], ':answer-field/type': str(f[':answer-field/type'][':db/ident']), ':answer-field/correct': [':answer/id', str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices': [{':answer/id': str(a[':answer/id']), ':answer/type': str(a[':answer/type'][':db/ident']), ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']]})
    return result


def fingerprint(q):
    prompt = q[':question/problem']
    function = re.search(r'\$f\(x,y\)\s*=\s*(.*?),\$', prompt).group(1)
    function = function.replace(r'\sin{y}', 'sin(y)')
    f = v.expression(function)
    endpoints = re.search(r'from \$\((.*?)\)\$ to \$\((.*?)\)', prompt)
    ax, ay = [v.expression(x) for x in endpoints[1].split(',')]
    bx, by = [v.expression(x) for x in endpoints[2].split(',')]
    speed = g.s.sqrt((bx-ax)**2 + (by-ay)**2)
    pullback = g.s.expand(f.subs({g.X: ax+(bx-ax)*g.T, g.Y: ay+(by-ay)*g.T}, simultaneous=True))
    return g.task_fingerprint(pullback, speed)


def check(rec):
    assert rec['knowledge_point']['db_id'] == KP and rec['knowledge_point']['id'] == g.KP_UUID
    assert rec['generation']['eligible_for_learning'] is True
    assert rec['generation']['bank_profile'] == rec['generation']['template'] + '_method'
    level = rec['question'][':question/difficulty'].split('/')[-1]
    g.parameters_checked(level, rec['generation']['template'], rec['generation']['parameters'])
    replay = g.generate(level, template=rec['generation']['template'], parameters=rec['generation']['parameters'], profile=rec['generation']['bank_profile'])
    assert canonical(rec['question']) == canonical(replay['question']), 'Record differs from deterministic generator output'
    v.verify(rec)
    fp = fingerprint(rec['question'])
    assert fp == rec['generation']['mathematical_task_fingerprint']
    return fp


def native(rec):
    f = rec['question'][':question/answer-fields'][0]
    return {'label': rec['question'][':question/id'], 'record': rec, 'checks': [{'submitted_answer_id': a[':answer/id'], 'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected', 'purpose': 'Grade every field-owned radio answer through the learner grader'} for a in f[':answer-field/choices']]}


def as_record(q):
    mid = q.get(':question/math-academy-id')
    if mid:
        case = next(c for c in json.loads((HERE / 'source-cases.json').read_text()) if c['source_id'] == mid)
        rec = g.generate(case['level'], template=case['template'], parameters=case['parameters'], profile=case['bank_profile'])
    else:
        candidates = []
        for p in OUT.glob('basis-*/generated.json'):
            candidates.extend(json.loads(p.read_text()))
        rec = copy.deepcopy(next(r for r in candidates if r['question'][':question/id'] == str(q[':question/id'])))
    rec['question'] = normalize(q)
    return rec


def available_counts(path, kp, basis):
    unavailable = {r[0] for r in DB.query(USAGE, [KP, LEARNER], path, 'usage', basis)}
    unavailable.update(r[0] for r in DB.query(USAGE, [KP, LEARNER], path, 'retained-usage', basis, history=True))
    available = {level: [] for level in LEVELS}
    excluded = []
    grading = []
    for q in kp[':knowledge-point/questions']:
        level = str(q.get(':question/difficulty', {}).get(':db/ident', '')).split('/')[-1]
        reason = None
        if q[':db/id'] in unavailable:
            reason = 'Shown or reserved (including retained history)'
        elif q.get(':knowledge-point/_canonical-example'):
            reason = 'Canonical example'
        elif level not in available:
            reason = 'Unrated or unsupported difficulty'
        else:
            try:
                rec = as_record(q)
                v.verify(rec)
                fingerprint(q)
            except (AssertionError, ValueError, KeyError, TypeError, StopIteration) as error:
                reason = 'Incomplete or invalid: ' + str(error)
        if reason:
            excluded.append({'question_id': str(q[':question/id']), 'reason': reason})
        else:
            available[level].append(q)
            grading.append(native(rec))
    save(path / 'inventory-grade-input.json', grading)
    subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(path / 'inventory-grade-input.json'), str(path / 'inventory-grade-report.json')], check=True)
    report = json.loads((path / 'inventory-grade-report.json').read_text())
    assert report['documented_unresolved_checks'] == 0
    result = {'basis': basis, 'levels': {l: {'distinct_available_tasks': len({fingerprint(q) for q in qs}), 'rated_gradable_unseen_unreserved': len(qs), 'available_question_ids': [str(q[':question/id']) for q in qs]} for l, qs in available.items()}, 'excluded_shown_or_reserved': sorted(unavailable), 'excluded_questions': excluded}
    save(path / 'available-counts.json', result)
    return result


def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'): a[':answer/id'], kw('answer/id'): uuid.UUID(a[':answer/id']), kw('answer/type'): kw(a[':answer/type']), kw('answer/value'): a[':answer/value'], kw('db/ensure'): kw('answer/validate')})
            forms.append({kw('db/id'): f[':answer-field/id'], kw('answer-field/id'): uuid.UUID(f[':answer-field/id']), kw('answer-field/key'): f[':answer-field/key'], kw('answer-field/type'): kw(f[':answer-field/type']), kw('answer-field/choices'): [a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'): f[':answer-field/correct'][1], kw('db/ensure'): kw('answer-field/validate')})
        forms.append({kw('db/id'): q[':question/id'], kw('question/id'): uuid.UUID(q[':question/id']), kw('question/problem'): q[':question/problem'], kw('question/worked-solution'): q[':question/worked-solution'], kw('question/difficulty'): kw(q[':question/difficulty']), kw('question/answer-fields'): [f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'): kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    else:
        forms.extend([{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid), kw('question-generator/script'): SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    if records:
        forms.append({kw('db/id'): KP, kw('knowledge-point/questions'): [r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms


def check_report(report, path, source):
    attrs = {e: str(a) for e, a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e, a, value, tx, src, added in report[':edb/tx-data']:
        assert src == source and added, 'Unexpected source or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, 'Unexpected existing entity or attribute'


def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path / 'receipt-check', intent['source_eid'])
    basis = report[':edb/db-after-t']
    kp = read_kp(path / 'readback', basis)
    before = loads((path / 'before.edn').read_text())
    old = {q[':db/id']: q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e]) == canonical(q) for e, q in old.items()), 'Original question changed'
    skip = (':knowledge-point/questions', ':knowledge-point/question-generator')
    assert canonical({k: z for k, z in before.items() if k not in skip}) == canonical({k: z for k, z in kp.items() if k not in skip})
    records = json.loads((path / 'generated.json').read_text())
    byid = {str(q[':question/id']): q for q in now.values()}
    assert len(now) == len(old) + len(records)
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert canonical(normalize(q)) == canonical(rec['question'])
        actual = copy.deepcopy(rec)
        actual['question'] = normalize(q)
        check(actual)
    save(path / 'readback/native-input.json', [native(as_record(byid[r['question'][':question/id']])) for r in records])
    subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(path / 'readback/native-input.json'), str(path / 'readback/native-report.json')], check=True)
    assert not transaction([], kp, intent['generator_id']), 'Registration not idempotent'
    counts = available_counts(path / 'readback', kp, basis)
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': basis, 'new_questions': len(records), 'new_by_level': {l: sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS}, 'unchanged_source_questions': len(old), 'unchanged_canonical_example': True, 'only_scoped_additive_content_datoms': True, 'learner_history_unchanged': True, 'generator_registration_verified': True, 'repeat_preparation_content_changes': 0, 'available_counts_after': counts}
    save(path / 'verification.json', result)
    return result


def finish(path, gid, verified, inv):
    prep = json.loads((path / 'preparation.json').read_text())
    counts = verified['available_counts_after']
    shortage = {l: max(0, 5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result = {'outcome': 'finite-limit' if any(shortage.values()) else 'generated', 'knowledgePoint': KP, 'generator_path': SCRIPT, 'generator_id': gid, 'lineage': LINEAGE, 'verified_commit_basis': verified['basis_after'], 'new_questions': verified['new_questions'], 'new_by_level': verified.get('new_by_level', {l: 0 for l in LEVELS}), 'supported_levels': list(LEVELS), 'unsupported_levels': [], 'authored_levels': ['moderate', 'hard'], 'available_counts_before': prep['available_counts'], 'available_counts_after': counts, 'remaining_shortage': shortage, 'capability_exceptions': [{'kind': 'bounded-sampling-limit', 'attempt_limit': 1000, 'remaining': shortage}] if any(shortage.values()) else [], 'inventory_recheck_basis': inv['basis'], 'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP], 'evidence': [str(p.relative_to(ROOT)) for p in (path / 'verification.json', path / 'commit-intent.json', path / 'transaction.edn', path / 'commit.edn', path / 'preview.edn', path / 'preparation.json', path / 'native-report.json', path / 'inventory-after.json', HERE / 'reference/freeze.json', HERE / 'validation.json', HERE / 'classification.md', HERE / 'template-extraction.md')]}
    save(path / 'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k: result[k] for k in ('outcome', 'verified_commit_basis', 'new_by_level', 'remaining_jobs')}), flush=True)


def main():
    freeze = json.loads((HERE / 'reference/freeze.json').read_text())
    assert freeze['status'] == 'validated'
    assert all(sha(ROOT / p) == h for p, h in freeze['hashes'].items())
    preview = preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']), repo_root=ROOT, preview_bin=None), threading.Event())
    with (ROOT / '.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path / 'commit-intent.json').exists():
                intent = json.loads((path / 'commit-intent.json').read_text())
                assert intent['database'] == 'math' and intent['lineage'] == LINEAGE and intent['source'] == SOURCE
                assert intent['endpoint'] == ENV['EDB_ENDPOINT']
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                assert intent['exact_edn'] == (path / 'transaction.edn').read_text() and intent['transaction_sha256'] == sha(path / 'transaction.edn')
                report = DB._commit(intent, path / 'transaction.edn', path)
                verified = verify(path, intent, report)
                finish(path, intent['generator_id'], verified, inventory(path / 'inventory-after.json'))
                return
        inv = inventory(OUT / 'inventory-before.json')
        basis = inv['basis']
        assert DB.basis() == basis
        path = OUT / ('basis-' + str(basis))
        path.mkdir(exist_ok=True)
        kp = read_kp(path, basis)
        (path / 'before.edn').write_text(dumps(kp) + '\n')
        expected = json.loads((HERE / 'source.json').read_text())['record']
        current = {str(q[':question/id']): q for q in kp[':knowledge-point/questions']}
        for q in expected[':knowledge-point/questions']:
            assert canonical(q, True) == canonical(current[str(q[':question/id'])], True), 'Source changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example'], True) == canonical(expected[':knowledge-point/canonical-example'], True)
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', basis)
        assert len(source) == 1
        registration = DB.query('[:find (pull ?g [*]) :in $ ?p :where [?g :question-generator/script ?p]]', [SCRIPT], path, 'generator-by-script', basis)
        assert len(registration) <= 1
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else str(registration[0][0][':question-generator/id']) if registration else str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'question-generator'))
        registered = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [uuid.UUID(gid)], path, 'generator-identity', basis)
        assert not registered or registered[0][0][':question-generator/script'] == SCRIPT
        counts = available_counts(path, kp, basis)
        needed = {l: max(0, 5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances', [])
        if isinstance(instances, dict):
            instances = [instances]
        assert isinstance(instances, list)
        records = []
        added = {l: 0 for l in LEVELS}
        for rec in instances:
            fp = check(rec)
            level = rec['question'][':question/difficulty'].split('/')[-1]
            if fp not in used and added[level] < needed[level]:
                records.append(copy.deepcopy(rec))
                used.add(fp)
                added[level] += 1
        save(path / 'supplied-status.json', {'exists': supplied_path.exists(), 'instances_validated': len(instances), 'generator_error': supplied.get('generatorError')})
        for level in LEVELS:
            for offset in range(1000):
                if added[level] >= needed[level]:
                    break
                rec = g.generate(level, seed=1604336703+offset, template=g.FAMILIES[offset % len(g.FAMILIES)])
                fp = check(rec)
                if fp not in used:
                    records.append(rec)
                    used.add(fp)
                    added[level] += 1
        identities = {'question/id': [], 'answer-field/id': [], 'answer/id': []}
        for rec in records:
            q = rec['question']
            identities['question/id'].append(uuid.UUID(q[':question/id']))
            for f in q[':question/answer-fields']:
                identities['answer-field/id'].append(uuid.UUID(f[':answer-field/id']))
                identities['answer/id'].extend(uuid.UUID(a[':answer/id']) for a in f[':answer-field/choices'])
        for attr, ids in identities.items():
            if ids:
                assert len(ids) == len(set(ids))
                assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :' + attr + ' ?id]]', [ids], path, attr.replace('/', '-'), basis), 'Unexpected existing generated identity'
        save(path / 'generated.json', records)
        save(path / 'native-input.json', [native(r) for r in records])
        subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(path / 'native-input.json'), str(path / 'native-report.json')], check=True)
        save(path / 'preparation.json', {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE, 'generator_id': gid, 'available_counts': counts, 'needed_by_level': needed, 'new_by_level': added, 'remaining_shortage': {l: needed[l]-added[l] for l in LEVELS}, 'asset_hashes': [], 'source_evidence_unchanged': True, 'distinctness': 'Canonical weighted pullback on [0,1], minimized against t -> 1-t; excludes seed, order, profile, reversed traversal, and translations preserving the task.', 'validation_sha256': sha(HERE / 'validation.json')})
        if '--prepare-only' in sys.argv:
            print(json.dumps({'prepared_basis': basis, 'new_by_level': added, 'path': str(path)}), flush=True)
            return
        forms = transaction(records, kp, gid)
        if not forms:
            verified = {'passed': True, 'basis_after': basis, 'new_questions': 0, 'no_changes': True, 'available_counts_after': counts}
            save(path / 'verification.json', verified)
            finish(path, gid, verified, inv)
            return
        txpath = path / 'transaction.edn'
        tx = dumps(forms) + '\n'
        with txpath.open('w') as stream:
            stream.write(tx)
            stream.flush()
            os.fsync(stream.fileno())
        result = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, check=True, timeout=90)
        (path / 'preview.edn').write_text(result.stdout)
        pr = loads(result.stdout)
        assert pr[':edb/committed'] is False
        if pr[':edb/db-before-t'] != basis:
            save(path / 'stale-preparation.json', {'prepared_basis': basis, 'preview_basis': pr[':edb/db-before-t'], 'submitted': False, 'reason': 'Another writer advanced the basis; return to preparation.'})
            raise StaleBasis('Database advanced during the speculative preview')
        check_report(pr, path / 'preview-check', source[0][0])
        if DB.basis() != basis:
            save(path / 'stale-preparation.json', {'prepared_basis': basis, 'submitted': False, 'reason': 'Database advanced after preview; return to preparation.'})
            raise StaleBasis('Database advanced after preview')
        intent = {'database': 'math', 'endpoint': ENV['EDB_ENDPOINT'], 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': source[0][0], 'basis': basis, 'expected_basis': basis, 'request_key': 'segment-construction-replenish-' + str(KP) + '-' + str(basis) + '-' + sha(txpath), 'sha256': sha(txpath), 'transaction_sha256': sha(txpath), 'exact_edn': tx, 'generator_id': gid, 'generator_path': SCRIPT, 'generator_sha256': sha(HERE.with_suffix('.py')), 'question_uuids': [r['question'][':question/id'] for r in records], 'connection_sha256': hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(ROOT / '.local/learning/requests/math/api.lock')}
        save(path / 'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        verified = verify(path, intent, report)
        finish(path, gid, verified, inventory(path / 'inventory-after.json'))


if __name__ == '__main__':
    for attempt in range(3):
        try:
            main()
            break
        except StaleBasis:
            if attempt == 2:
                raise
            print('Confirmed stale basis; rechecking inventory and preparing again.', flush=True)

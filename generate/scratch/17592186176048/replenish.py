"""Scoped additive inventory commits through the existing EDB integration."""
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

spec = importlib.util.spec_from_file_location('cosine_validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '1fc4dc1522878b3acfabad62e93532117d0777bda410f4fff67994305ffb4b6b'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-80371ed6e5f3669c'
QUERY = (HERE / 'source-query.edn').read_text()
LOCK = ROOT / '.local/learning/requests/math/api.lock'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical(value):
    if isinstance(value, dict):
        return {str(k): canonical(x) for k, x in sorted(value.items())}
    if isinstance(value, list):
        return sorted([canonical(x) for x in value], key=lambda x: json.dumps(x, sort_keys=True))
    return str(value) if isinstance(value, uuid.UUID) else value

def fingerprint(q):
    """Read the given value and requested expression independently of metadata."""
    pieces = re.findall(r'\$(.*?)\$', q[':question/problem'])
    c = v.sp.simplify(v.parse(pieces[0].split('=', 1)[1].replace(r'\dfrac', r'\frac')))
    expression = v.parse(pieces[-1].strip().rstrip('=.'))
    cosines = list(expression.atoms(v.sp.cos))
    assert len(cosines) == 1
    cosine = cosines[0]
    shift = v.sp.simplify((cosine.args[0] - v.X) / v.sp.pi)
    assert shift.is_Integer and shift % 2 == 0
    a = v.sp.expand(expression).coeff(cosine)
    b = v.sp.simplify(expression - a * cosine)
    assert a.is_Integer and b.is_Integer
    return g.hash_data({'c': v.sp.srepr(c), 'reduced_angle': 'x', 'a': int(a), 'b': int(b)})

def inventory(path):
    request = {'action': 'inventory'}
    response = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input=json.dumps(request), env=ENV, capture_output=True, text=True, check=True, timeout=55)
    result = json.loads(response.stdout)
    assert result['ok'], result
    inv = result['data']
    assert inv['lineage'] == LINEAGE
    save(path, inv)
    return inv

def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]

def normalized(q):
    q = json.loads(json.dumps(q, default=str))
    out = {k: q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    d = q[':question/difficulty']
    out[':question/difficulty'] = d[':db/ident'] if isinstance(d, dict) else d
    fields = []
    for f in q[':question/answer-fields']:
        kind, correct = f[':answer-field/type'], f[':answer-field/correct']
        fields.append({':answer-field/id': f[':answer-field/id'], ':answer-field/key': f[':answer-field/key'], ':answer-field/type': kind[':db/ident'] if isinstance(kind, dict) else kind,
            ':answer-field/correct': [':answer/id', correct[':answer/id']] if isinstance(correct, dict) else correct,
            ':answer-field/choices': sorted([{':answer/id': a[':answer/id'], ':answer/value': a[':answer/value'], ':answer/type': a[':answer/type'][':db/ident'] if isinstance(a[':answer/type'], dict) else a[':answer/type']} for a in f[':answer-field/choices']], key=lambda a: a[':answer/value'])})
    out[':question/answer-fields'] = sorted(fields, key=lambda f: f[':answer-field/key'])
    return out

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
    if gen is None:
        forms.extend([{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid), kw('question-generator/script'): SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'): KP, kw('knowledge-point/questions'): [r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e: str(a) for e, a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e, a, value, tx, s, added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected contributor or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path / 'receipt-check', intent['source_eid'])
    kp = read_kp(path / 'readback', report[':edb/db-after-t'])
    before = loads((path / 'before.edn').read_text())
    old = {q[':db/id']: q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e]) == canonical(q) for e, q in old.items())
    assert canonical({k: x for k, x in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}) == canonical({k: x for k, x in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')})
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path / 'generated.json').read_text())
    byid = {str(q[':question/id']): q for q in now.values()}
    assert len(now) == len(old) + len(records)
    fps = set()
    previous = {fingerprint(q) for q in before[':knowledge-point/questions']}
    previous.add(fingerprint(before[':knowledge-point/canonical-example']))
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalized(q) == normalized(rec['question'])
        fp = fingerprint(q)
        assert fp == rec['generation']['parameter_fingerprint'] and fp not in previous and fp not in fps
        fps.add(fp)
        v.check(rec)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': report[':edb/db-after-t'], 'new_questions': len(records), 'by_level': {level: sum(r['question'][':question/difficulty'] == ':question.difficulty/' + level for r in records) for level in LEVELS}, 'unchanged_source_questions': len(old), 'unchanged_canonical_example': True, 'only_additive_scoped_content_datoms': True, 'learner_history_unchanged': True, 'generator_registration_verified': True, 'distinct_from_sources_and_each_other': True, 'repeat_preparation_content_changes': 0}
    save(path / 'verification.json', result)
    return result

def finish(path, gid, verified, inv):
    prep = json.loads((path / 'preparation.json').read_text())
    exceptions = prep['capability_exceptions']
    result = {'outcome': 'finite-limit' if exceptions else 'generated', 'knowledgePoint': KP, 'generator_path': SCRIPT, 'generator_id': gid, 'lineage': LINEAGE, 'verified_commit_basis': verified['basis_after'], 'new_questions': verified['new_questions'], 'by_level': verified['by_level'], 'supported_levels': list(LEVELS), 'unsupported_levels': [], 'unsupported_levels_filled': False, 'capability_exceptions': exceptions, 'remaining_shortages': prep['remaining_shortages'], 'inventory_recheck_basis': inv['basis'], 'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP], 'evidence': [str(p.relative_to(ROOT)) for p in (path / 'verification.json', path / 'commit-intent.json', path / 'commit.edn', path / 'preview.edn', path / 'preparation.json', path / 'generated.json', path / 'native-report.json', path / 'inventory-after.json', HERE / 'validation.json', HERE / 'classification.md', HERE / 'template-extraction.md', HERE / 'capabilities.json')]}
    save(path / 'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k: result[k] for k in ('outcome', 'verified_commit_basis', 'new_questions', 'by_level', 'remaining_jobs')}), flush=True)

def prepare_and_commit(preview):
    for path in sorted(OUT.glob('basis-*')):
        if (path / 'commit-intent.json').exists():
            intent = json.loads((path / 'commit-intent.json').read_text())
            assert intent['lineage'] == LINEAGE and intent['database'] == 'math' and intent['endpoint'] == DB.args.endpoint and intent['source'] == SOURCE
            assert intent['transaction_sha256'] == sha(path / 'transaction.edn')
            assert intent['generator_sha256'] == sha(HERE.with_suffix('.py'))
            assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
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
    assert str(kp[':knowledge-point/id']) == g.KP_UUID
    (path / 'before.edn').write_text(dumps(kp) + '\n')
    expected = json.loads((HERE / 'source.json').read_text())['record']
    current = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
    assert all(canonical(current[q[':db/id']]) == canonical(q) for q in expected[':knowledge-point/questions']), 'Source evidence changed; reclassify'
    assert canonical(kp[':knowledge-point/canonical-example']) == canonical(expected[':knowledge-point/canonical-example'])
    source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', basis)
    assert len(source) == 1
    gen = kp.get(':knowledge-point/question-generator')
    identity_path = HERE / 'generator-id.json'
    identity = json.loads(identity_path.read_text()) if identity_path.exists() else {}
    gid = str(gen[':question-generator/id']) if gen else identity.get('id', g.GENERATOR_UUID)
    assert not identity or identity['id'] == gid
    save(identity_path, {'id': gid, 'script': SCRIPT, 'knowledge_point': KP})
    jobs = {j['difficulty']: j for j in inv['jobs'] if j['knowledgePoint'] == KP}
    observed = {str(q.get(':question/difficulty', {}).get(':db/ident', '')).split('/')[-1] for q in kp[':knowledge-point/questions']}
    needed = {level: jobs.get(level, {}).get('missing', 5 if level not in observed else 0) for level in LEVELS}
    used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
    used.add(fingerprint(kp[':knowledge-point/canonical-example']))
    records, selected = [], {level: 0 for level in LEVELS}
    def consider(rec):
        v.check(rec)
        assert rec['knowledge_point']['db_id'] == KP and rec['knowledge_point']['id'] == g.KP_UUID
        assert not rec['generation']['raw_source_error']
        level = rec['question'][':question/difficulty'].split('/')[-1]
        assert level in LEVELS
        fp = fingerprint(rec['question'])
        assert fp == rec['generation']['parameter_fingerprint']
        if selected[level] < needed[level] and fp not in used:
            records.append(copy.deepcopy(rec))
            used.add(fp)
            selected[level] += 1
    supplied_path = JOB.with_suffix('.generated')
    supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances = supplied.get('instances', [])
    if isinstance(instances, dict):
        instances = [instances]
    assert isinstance(instances, list)
    for rec in instances:
        consider(rec)
    save(path / 'supplied-status.json', {'exists': supplied_path.exists(), 'instances_validated': len(instances), 'generator_error': supplied.get('generatorError')})
    seed = int(JOB.name[:8], 16)
    attempts = {}
    for level in LEVELS:
        attempts[level] = 0
        for i in range(512):
            if selected[level] >= needed[level]:
                break
            consider(g.generate(level, seed + i))
            attempts[level] += 1
    remaining = {level: needed[level] - selected[level] for level in LEVELS}
    exceptions = [{'level': level, 'requested': needed[level], 'produced': selected[level], 'shortage': remaining[level], 'bounded_seed_attempts': attempts[level], 'evidence': 'capabilities.json; complete-bank validation and exact tuple exclusion'} for level in LEVELS if remaining[level]]
    # Identity collisions never authorize overwriting an existing entity.
    for attr, ids in (
        ('question/id', [r['question'][':question/id'] for r in records]),
        ('answer-field/id', [f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),
        ('answer/id', [a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
        if ids:
            assert len(ids) == len(set(ids))
            assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :' + attr + ' ?id]]', [[uuid.UUID(x) for x in ids]], path, attr.replace('/', '-'), basis), 'Existing identity collision requires reconciliation'
    registered = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [uuid.UUID(gid)], path, 'generator-identity', basis)
    assert not registered or len(registered) == 1 and registered[0][0][':question-generator/script'] == SCRIPT
    save(path / 'generated.json', records)
    save(path / 'native-input.json', [v.engine_item(r, r['question'][':question/id']) for r in instances + records])
    subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(path / 'native-input.json'), str(path / 'native-report.json')], check=True)
    save(path / 'review.json', records)
    (path / 'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records))
    save(path / 'preparation.json', {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': source[0][0], 'generator_id': gid, 'missing_by_level': needed, 'selected_by_level': selected, 'remaining_shortages': remaining, 'capability_exceptions': exceptions, 'bounded_seed_attempts': attempts, 'source_evidence_unchanged': True, 'asset_hashes': [], 'inventory_count_evidence': jobs, 'distinctness': 'Canonical exact (c,a,b), excludes every current practice and canonical task; shift/seed/bank/order never inflate task count', 'native_grader_sha256': sha(ROOT / 'generate/runs/current/check-engine')})
    forms = transaction(records, kp, gid)
    assert forms, 'Already replenished and registered: reconcile prior evidence instead of making an empty commit'
    txpath = path / 'transaction.edn'
    tx = dumps(forms) + '\n'
    with txpath.open('w') as f:
        f.write(tx)
        f.flush()
        os.fsync(f.fileno())
    response = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, check=True, timeout=55)
    (path / 'preview.edn').write_text(response.stdout)
    pr = loads(response.stdout)
    assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == basis
    check_report(pr, path / 'preview-check', source[0][0])
    assert DB.basis() == basis
    intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': source[0][0], 'basis': basis, 'expected_basis': basis, 'request_key': 'cosine-periodicity-replenish-' + str(KP) + '-' + str(basis) + '-' + sha(txpath), 'transaction_sha256': sha(txpath), 'sha256': sha(txpath), 'exact_edn': tx, 'generator_id': gid, 'generator_path': SCRIPT, 'generator_sha256': sha(HERE.with_suffix('.py')), 'question_uuids': [r['question'][':question/id'] for r in records], 'connection_sha256': hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(LOCK)}
    save(path / 'commit-intent.json', intent)
    report = DB._commit(intent, txpath, path)
    verified = verify(path, intent, report)
    finish(path, gid, verified, inventory(path / 'inventory-after.json'))

def main():
    validation = json.loads((HERE / 'validation.json').read_text())
    assert validation['status'] == 'passed'
    frozen = json.loads((HERE / 'freeze-hashes.json').read_text())
    for name, digest in frozen.items():
        p = ROOT / 'generate/runs/current' / name if name.startswith('check-engine') else HERE.with_suffix('.py') if name == HERE.name + '.py' else HERE / name
        assert sha(p) == digest, 'Frozen artifact changed: ' + name
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    for attempt in range(3):
        try:
            with LOCK.open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                prepare_and_commit(preview)
            return
        except StaleBasis:
            if attempt == 2:
                raise

if __name__ == '__main__':
    main()

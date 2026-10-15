"""Validate and publish this KP's bounded vector-chain inventory only."""
import fcntl
import gzip
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
OUT = HERE/'reference/replenishment'
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture'), str(HERE)]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('vector_chain_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'8c7f59b912fee27ae92505cdfc09a2374ef5919964b97dc2a3ee971b74167d85'
LOCK = ROOT/'.local/learning/requests/math/api.lock'
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = Path(json.loads((OUT/'runtime.json').read_text())['learning_binary'])
QUERY = (ROOT/'generate/runs/current/sources-query.edn').read_text().replace(':knowledge-point/title', ':knowledge-point/title {:knowledge-point/question-generator [*]}', 1)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canonical(x, notation=False):
    if isinstance(x, dict): return {str(k): canonical(z, notation) for k, z in x.items()}
    if isinstance(x, (list, tuple)): return sorted([canonical(z, notation) for z in x], key=lambda z: json.dumps(z, sort_keys=True))
    if isinstance(x, uuid.UUID): return str(x)
    if notation and isinstance(x, str): return x.replace(r'\begin{bmatrix}', r'[\begin{aligned}').replace(r'\end{bmatrix}', r'\end{aligned}]')
    return x


def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]


def inventory(path):
    path.mkdir(parents=True, exist_ok=True)
    def call(action, extra=None):
        r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input=json.dumps({'action': action}), env={**DB.env, **(extra or {})}, capture_output=True, text=True, check=True, timeout=55)
        result = json.loads(r.stdout); assert result['ok'], result
        return result['data']
    inv = call('inventory'); assert inv['lineage'] == LINEAGE
    save(path/'inventory.json', inv)
    snapshot = path/'snapshot.json'
    call('export-test-snapshot', {'LEARNING_SNAPSHOT_PATH': str(snapshot)})
    subprocess.run([str(OUT/'inspect-inventory'), str(snapshot), str(path/'counts.json')], check=True, timeout=55)
    counts = json.loads((path/'counts.json').read_text())
    assert inv['basis'] == counts['basis'] == DB.basis(), 'Basis advanced during read; retry fresh inventory'
    save(path/'snapshot-evidence.json', {'sha256': sha(snapshot), 'basis': counts['basis'], 'lineage': LINEAGE, 'encoding': 'gzip'})
    with snapshot.open('rb') as src, gzip.open(snapshot.with_suffix('.json.gz'), 'wb') as dst:
        import shutil
        shutil.copyfileobj(src, dst)
    snapshot.unlink()
    return inv, counts


def normalized(q):
    return {':question/id': str(q[':question/id']), ':question/problem': q[':question/problem'],
            ':question/worked-solution': q[':question/worked-solution'],
            ':question/difficulty': str(q[':question/difficulty'][':db/ident']),
            ':question/answer-fields': [{':answer-field/id': str(f[':answer-field/id']), ':answer-field/key': f[':answer-field/key'],
                                       ':answer-field/type': str(f[':answer-field/type'][':db/ident']),
                                       ':answer-field/choices': [{':answer/id': str(a[':answer/id']), ':answer/type': str(a[':answer/type'][':db/ident']), ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']],
                                       ':answer-field/correct': [':answer/id', str(f[':answer-field/correct'][':answer/id'])]} for f in q[':question/answer-fields']]}


def task_key(q):
    # Both supplied functions and the resulting derivative matter. Cosmetic
    # notation, answer ordering and seed never create another mathematical task.
    F, H = v.read_prompt({'question': q})
    C = [g.S.simplify(g.S.diff(x, g.u).subs(g.u, H)*g.S.diff(H, g.t)) for x in F]
    return json.dumps([g.canonical(F), g.S.srepr(g.S.simplify(H)), g.canonical(C)], sort_keys=True)


def validate_records(records, path):
    checks = []
    for r in records:
        assert r['knowledge_point']['db_id'] == KP and r['generation']['version'] == g.VERSION
        v.check_record(r)
        f = r['question'][':question/answer-fields'][0]
        checks.append({'label': r['question'][':question/id'], 'record': r,
                       'checks': [{'submitted_answer_id': a[':answer/id'], 'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected', 'purpose': 'Actual owned radio choice'} for a in f[':answer-field/choices']]})
    save(path/'native-input.json', checks)
    subprocess.run([str(OUT/'check-engine'), str(path/'native-input.json'), str(path/'native-report.json')], check=True, timeout=55)


def source_check(kp):
    # Preserve the immutable old capture; independently reconcile the current
    # bmatrix repair, including every choice and all worked-solution text.
    omit = {':knowledge-point/question-generator'}
    assert canonical({k: x for k, x in kp.items() if k not in omit}, True) == canonical(g.SOURCE['record'], True), 'Source evidence changed beyond the verified matrix repair'


def prepare_candidates():
    if (OUT/'candidates.json').exists():
        return json.loads((OUT/'candidates.json').read_text())
    inv, counts = inventory(OUT/'before-generation')
    kp = read_kp(OUT/'before-generation', inv['basis']); source_check(kp)
    used = {task_key(normalized(q)) for q in kp[':knowledge-point/questions']}
    # Original derivative/domain fingerprints also prevent regenerating a task
    # through an algebraically changed function presentation.
    derivative_keys = {json.dumps(g.canonical([g.S.diff(x, g.u).subs(g.u, H)*g.S.diff(H, g.t) for x in F])) for q in kp[':knowledge-point/questions'] for F, H in [v.read_prompt({'question': normalized(q)})]}
    supplied = JOB.with_suffix('.generated')
    data = json.loads(supplied.read_text()) if supplied.exists() else {}
    instances = data.get('instances', []) if isinstance(data, dict) else data
    if isinstance(instances, dict): instances = [instances]
    records = []; selected = {level: 0 for level in ('easy', 'moderate', 'hard')}
    need = {level: max(0, 5-counts['available_by_level'][level]) for level in selected}
    supplied_report = []
    def accept(r):
        v.check_record(r)
        level = r['question'][':question/difficulty'].split('/')[-1]
        key = task_key(r['question']); dk = json.dumps(g.canonical([g.S.sympify(x, locals={'t': g.t, 'u': g.u}) for x in r['generation']['stages']['composition']]))
        if selected[level] >= need[level] or key in used or dk in derivative_keys: return False
        records.append(r); used.add(key); derivative_keys.add(dk); selected[level] += 1
        return True
    for r in instances:
        accepted = accept(r)
        supplied_report.append({'id': r['question'][':question/id'], 'validated': True, 'selected': accepted})
    # Execute the repository script through its supported reproducible CLI.
    for i, level in enumerate(selected):
        remaining = need[level]-selected[level]
        if not remaining: continue
        seed = int(JOB.name[:8], 16)+100*i
        r = subprocess.run([sys.executable, str(HERE.with_suffix('.py')), '--difficulty', level, '--count', str(remaining), '--seed', str(seed), '--format', 'json'], capture_output=True, text=True, check=True, timeout=180)
        (OUT/(level+'-cli.json')).write_text(r.stdout)
        batch = json.loads(r.stdout)
        for rec in batch if isinstance(batch, list) else [batch]: accept(rec)
    assert selected == need, {'needed': need, 'produced': selected}
    validate_records(records, OUT)
    save(OUT/'candidates.json', records)
    (OUT/'candidates.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
    save(OUT/'candidate-validation.json', {'passed': True, 'inventory_basis': inv['basis'], 'needed': need, 'produced': selected,
                                           'distinct_tasks': len({task_key(r['question']) for r in records}),
                                           'supplied_file_exists': supplied.exists(), 'supplied_instances': supplied_report,
                                           'generator_version': g.VERSION, 'generator_sha256': sha(HERE.with_suffix('.py')),
                                           'grader_sha256': sha(OUT/'check-engine'), 'source_snapshot_reconciled': 'Only bmatrix notation repairs',
                                           'authored_levels': ['moderate', 'hard'], 'plots': 'none', 'asset_hashes': []})
    return records


def transaction(records, kp, gid):
    forms = []
    for r in records:
        q = r['question']
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
    if records: forms.append({kw('db/id'): KP, kw('knowledge-point/questions'): [r['question'][':question/id'] for r in records]})
    if forms: forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms


def check_datoms(report, path, source):
    attrs = {e: str(a) for e, a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':answer/id', ':answer/type', ':answer/value', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':question-generator/id', ':question-generator/script'}
    for e, a, value, tx, s, added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP: assert name in {':knowledge-point/questions', ':knowledge-point/question-generator'}
        elif name != ':db/txInstant': assert e in new and name in allowed, 'Out-of-scope mutation'


def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_datoms(report, path/'receipt-check', intent['source_eid'])
    after = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']: q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']: q for q in after[':knowledge-point/questions']}
    assert all(canonical(q) == canonical(now[e]) for e, q in old.items())
    omit = {':knowledge-point/questions', ':knowledge-point/question-generator'}
    assert canonical({k: x for k, x in before.items() if k not in omit}) == canonical({k: x for k, x in after.items() if k not in omit})
    records = json.loads((path/'generated.json').read_text()); assert len(now) == len(old)+len(records)
    byid = {str(q[':question/id']): q for q in now.values()}
    for r in records:
        q = byid[r['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert canonical(normalized(q)) == canonical(r['question'])
    assert not transaction([], after, intent['generator_id']), 'Repeat preparation changes content'
    verified = {'passed': True, 'basis_before': intent['basis'], 'basis_after': report[':edb/db-after-t'], 'new_questions': len(records),
                'unchanged_source_questions': len(old), 'canonical_example_unchanged': True, 'learner_history_unchanged': True,
                'only_additive_requested_kp_datoms': True, 'attribution_verified': SOURCE, 'generator_registration_verified': True,
                'exact_question_field_answer_readback': True, 'repeat_preparation_content_changes': 0}
    save(path/'verification.json', verified)
    return verified


def finish(path, intent, verified):
    inv, counts = inventory(path/'after')
    shortages = {level: max(0, 5-n) for level, n in counts['available_by_level'].items()}
    result = {'outcome': 'generated', 'knowledgePoint': KP, 'topic': 17592186048233, 'generator_path': SCRIPT,
              'generator_id': intent['generator_id'], 'generator_registered': True, 'generator_version': g.VERSION,
              'lineage': LINEAGE, 'preparation_basis': intent['basis'], 'verified_commit_basis': verified['basis_after'],
              'new_questions': verified['new_questions'], 'available_by_level': counts['available_by_level'],
              'supported_levels': ['easy', 'moderate', 'hard'], 'source_observed_levels': ['easy'], 'authored_levels': ['moderate', 'hard'],
              'remaining_shortages': shortages, 'unsupported_levels': [], 'unsupported_levels_filled': False,
              'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP], 'inventory_recheck_basis': inv['basis'],
              'source_questions_and_learner_history_preserved': True,
              'evidence': [str(p.relative_to(ROOT)) for p in [HERE/'classification.md', HERE/'template-extraction.md', HERE/'validation.json', OUT/'candidate-validation.json', path/'preparation.json', path/'transaction.edn', path/'commit-intent.json', path/'preview.edn', path/'commit.edn', path/'verification.json', path/'after/counts.json', path/'after/inventory.json', OUT/'native-report.json']],
              'difficulty_note': 'Moderate and hard are the existing explicitly authored workload claims, not observed Math Academy ratings. Both retain one vector composition and five whole-vector radio choices; hard distributes the polynomial component.'}
    assert not any(shortages.values()) and not result['remaining_jobs']
    save(path/'outcome.json', result); save(JOB.with_suffix('.result'), result)
    print(json.dumps({k: result[k] for k in ('outcome', 'new_questions', 'verified_commit_basis', 'available_by_level')}), flush=True)


def main():
    validation = json.loads((HERE/'validation.json').read_text()); assert validation['status'] == 'pass'
    assert validation['engine_sha256'] == sha(OUT/'check-engine'), 'Revalidate with current native grader'
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    # Resolve unknown prior submissions before making any new content decisions.
    pending = [p for p in sorted(OUT.glob('basis-*')) if (p/'commit-intent.json').exists()]
    if not pending: candidates = prepare_candidates()
    with LOCK.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if pending:
            assert len(pending) == 1
            path = pending[0]; intent = json.loads((path/'commit-intent.json').read_text())
            assert intent['database'] == 'math' and intent['lineage'] == LINEAGE and intent['source'] == SOURCE
            assert intent['endpoint'] == DB.args.endpoint and intent['exact_edn'] == (path/'transaction.edn').read_text()
            assert intent['sha256'] == sha(path/'transaction.edn')
            assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report = DB._commit(intent, path/'transaction.edn', path)
            finish(path, intent, verify(path, intent, report)); return
        inv, counts = inventory(OUT/'locked-current'); b = inv['basis']
        assert LINEAGE in DB.command('status')
        path = OUT/('basis-'+str(b)); path.mkdir(exist_ok=True)
        kp = read_kp(path, b); source_check(kp)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        used = {task_key(normalized(q)) for q in kp[':knowledge-point/questions']}
        needed = {level: max(0, 5-n) for level, n in counts['available_by_level'].items()}
        records = []
        for r in candidates:
            level = r['question'][':question/difficulty'].split('/')[-1]; key = task_key(r['question'])
            if needed[level] and key not in used:
                records.append(r); used.add(key); needed[level] -= 1
        assert not any(needed.values()), 'New inventory state requires candidate preparation'
        contributor = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', b)
        assert len(contributor) == 1
        registered = DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]', [SCRIPT], path, 'generator-script', b)
        assert len(registered) <= 1
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else g.GENERATOR_ID
        collision = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [uuid.UUID(gid)], path, 'generator-identity', b)
        assert not collision or len(collision) == 1 and collision[0][0][':question-generator/script'] == SCRIPT
        for kind, ids in [('question', [uuid.UUID(r['question'][':question/id']) for r in records]), ('answer-field', [uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]), ('answer', [uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            assert len(ids) == len(set(ids))
            if ids: assert not DB.query('[:find ?e :in $ [?id ...] :where [?e :'+kind+'/id ?id]]', [ids], path, 'identity-'+kind, b)
        save(path/'generated.json', records)
        save(path/'preparation.json', {'basis': b, 'lineage': LINEAGE, 'source': SOURCE, 'generator_id': gid, 'generator_path': SCRIPT,
                                       'generator_version': g.VERSION, 'generator_sha256': sha(HERE.with_suffix('.py')),
                                       'available_before': counts['available_by_level'], 'new_questions': len(records), 'distinct_tasks': len(records),
                                       'source_reconciliation': 'All raw source facts unchanged except already-installed bmatrix notation repairs',
                                       'supported_levels': ['easy', 'moderate', 'hard'], 'authored_levels': ['moderate', 'hard'], 'asset_hashes': []})
        forms = transaction(records, kp, gid); assert forms
        txpath = path/'transaction.edn'; tx = dumps(forms)+'\n'
        with txpath.open('w') as stream: stream.write(tx); stream.flush(); os.fsync(stream.fileno())
        r = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, check=True, timeout=55)
        (path/'preview.edn').write_text(r.stdout); report = loads(r.stdout)
        assert report[':edb/committed'] is False and report[':edb/db-before-t'] == b
        check_datoms(report, path/'preview-check', contributor[0][0]); assert DB.basis() == b
        intent = {'database': 'math', 'lineage': LINEAGE, 'endpoint': DB.args.endpoint, 'source': SOURCE, 'source_eid': contributor[0][0],
                  'basis': b, 'expected_basis': b, 'sha256': sha(txpath), 'exact_edn': tx, 'request_key': 'vector-chain-'+str(KP)+'-'+str(b)+'-'+sha(txpath),
                  'question_uuids': [r['question'][':question/id'] for r in records], 'generator_id': gid, 'generator_path': SCRIPT,
                  'generator_sha256': sha(HERE.with_suffix('.py')), 'connection_sha256': hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(LOCK)}
        save(path/'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        finish(path, intent, verify(path, intent, report))


if __name__ == '__main__': main()

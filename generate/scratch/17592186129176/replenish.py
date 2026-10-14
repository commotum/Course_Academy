"""Scoped preparation, preview, guarded commit and exact-basis verification."""
import fcntl
import hashlib
import json
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
sys.path[:0] = [str(HERE), str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
import validate as v
from database import Database, StaleBasis
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment

g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'41609ed1006ec9b039df42ef3ab27e3d16785e75d017b13d712150a725f1506a'
LOCK = ROOT/'.local/learning/requests/math/api.lock'
OUT = HERE/'reference/replenishment'
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = ROOT/'.local/graph-explorer/learning-77cf2bd638861f3b'
QUERY = (HERE/'source-query.edn').read_text()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(x):
    if isinstance(x, dict):
        return {str(k): canonical(v) for k, v in sorted(x.items())}
    if isinstance(x, (list, tuple)):
        return sorted([canonical(v) for v in x], key=lambda v: json.dumps(v, sort_keys=True))
    return str(x) if isinstance(x, uuid.UUID) else x


def inventory(path):
    response = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint],
        input=json.dumps({'action': 'inventory'}), env=ENV, check=True,
        capture_output=True, text=True, timeout=55)
    data = json.loads(response.stdout)
    assert data['ok'], data
    inv = data['data']
    assert inv['lineage'] == g.LINEAGE
    save(path, inv)
    return inv


def read_kp(path, basis):
    result = DB.query(QUERY, [[KP]], path, 'kp', basis)
    assert len(result) == 1 and str(result[0][0][':knowledge-point/id']) == g.KP_UUID
    return result[0][0]


def grade(records, path):
    save(path/'native-input.json', [v.engine_entry(str(i), rec) for i, rec in enumerate(records)])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'), str(path/'native-input.json'), str(path/'native-report.json')], check=True)
    report = json.loads((path/'native-report.json').read_text())
    assert report['accepted_checks'] == len(records) and report['rejected_checks'] == 4*len(records)
    assert report['documented_unresolved_checks'] == 0


USAGE = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''


def counts(kp, path, basis):
    shown = {row[0] for row in DB.query(USAGE, [KP, LEARNER], path, 'ever-shown', basis, history=True)}
    reserved = {row[0] for row in DB.query(RESERVED, [KP, LEARNER], path, 'reserved', basis)}
    ids = [q[':db/id'] for q in kp[':knowledge-point/questions']]
    examples = {row[0] for row in DB.query('[:find ?q :in $ [?q ...] :where [_ :knowledge-point/canonical-example ?q]]', [ids], path, 'canonical-exclusions', basis)}
    available = set(); records = []; excluded = []
    for q in kp[':knowledge-point/questions']:
        level = q.get(':question/difficulty', {}).get(':db/ident')
        if level != ':question.difficulty/easy':
            excluded.append({'id': str(q[':question/id']), 'reason': 'Unrated with missing key/solution; preserved and excluded'})
            continue
        rec = {'knowledge_point': {'db_id': KP, 'id': g.KP_UUID, 'title': g.TITLE},
               'question': v.normalized(q), 'generation': {'template': 'existing_easy'}}
        v.inspect(rec); records.append(rec)
        if q[':db/id'] not in shown | reserved | examples:
            available.add(g.task_fingerprint(g.parse(q[':question/problem'])))
    if records:
        grade(records, path/'grading')
    result = {'basis': basis, 'distinct_available': {'easy': len(available), 'moderate': 0, 'hard': 0},
              'gradable_easy': len(records), 'shown_ids': sorted(shown), 'reserved_ids': sorted(reserved),
              'canonical_exclusions': sorted(examples), 'excluded_source_questions': excluded}
    save(path/'counts.json', result)
    return result


def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'): a[':answer/id'], kw('answer/id'): uuid.UUID(a[':answer/id']),
                    kw('answer/type'): kw(a[':answer/type']), kw('answer/value'): a[':answer/value'], kw('db/ensure'): kw('answer/validate')})
            forms.append({kw('db/id'): f[':answer-field/id'], kw('answer-field/id'): uuid.UUID(f[':answer-field/id']),
                kw('answer-field/key'): f[':answer-field/key'], kw('answer-field/type'): kw(f[':answer-field/type']),
                kw('answer-field/choices'): [a[':answer/id'] for a in f[':answer-field/choices']],
                kw('answer-field/correct'): f[':answer-field/correct'][1], kw('db/ensure'): kw('answer-field/validate')})
        forms.append({kw('db/id'): q[':question/id'], kw('question/id'): uuid.UUID(q[':question/id']),
            kw('question/problem'): q[':question/problem'], kw('question/worked-solution'): q[':question/worked-solution'],
            kw('question/difficulty'): kw(q[':question/difficulty']), kw('question/answer-fields'): [f[':answer-field/id'] for f in q[':question/answer-fields']],
            kw('db/ensure'): kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms += [{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid), kw('question-generator/script'): SCRIPT},
                  [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']]
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'): KP, kw('knowledge-point/questions'): [r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms


def check_report(report, path, source):
    attrs = dict(DB.attributes(path, report[':edb/db-before-t']))
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty',
        ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices',
        ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e, a, value, tx, contributor, added in report[':edb/tx-data']:
        name = str(attrs[a])
        assert contributor == source and added is True
        if e == KP:
            assert name in {':knowledge-point/question-generator', ':knowledge-point/questions'}
        elif name != ':db/txInstant':
            assert e in new and name in allowed, (e, name)


def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path/'receipt-check', intent['source_eid'])
    kp = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']: q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e]) == canonical(q) for e, q in old.items())
    assert canonical({k: v for k, v in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}) == canonical({k: v for k, v in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')})
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    byid = {str(q[':question/id']): q for q in now.values()}
    assert len(now) == len(old) + len(records)
    for rec in records:
        assert v.normalized(byid[rec['question'][':question/id']]) == v.normalized(rec['question'])
        v.inspect(rec)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed': True, 'committed': True, 'basis_before': intent['basis'], 'basis_after': report[':edb/db-after-t'],
        'new_questions': len(records), 'unchanged_source_questions': len(old), 'canonical_example_unchanged': True,
        'generator_registration_verified': True, 'contributor_verified': SOURCE, 'only_additive_scoped_content_datoms': True,
        'learner_history_unchanged': True, 'repeat_preparation_content_changes': 0}
    save(path/'verification.json', result)
    return result


def finish(path, intent, verified):
    inv = inventory(path/'inventory-after.json')
    stock = counts(read_kp(path/'final', inv['basis']), path/'final', inv['basis'])
    caps = json.loads((HERE/'capabilities.json').read_text())
    remaining = {level: max(0, 5-stock['distinct_available'][level]) for level in ('easy', 'moderate', 'hard')}
    result = {'outcome': 'generated' if remaining['easy'] == 0 else 'finite-limit', 'knowledgePoint': KP,
        'generator_path': SCRIPT, 'generator_id': intent['generator_id'], 'generator_registered': True,
        'verified_commit_basis': verified['basis_after'], 'preparation_basis': intent['basis'], 'lineage': g.LINEAGE,
        'new_questions': verified['new_questions'], 'new_questions_by_level': {'easy': verified['new_questions'], 'moderate': 0, 'hard': 0},
        'supported_levels': ['easy'], 'unsupported_levels': caps['unsupported_levels'], 'unsupported_levels_filled': False,
        'available_by_level': stock['distinct_available'], 'shortage_by_level': remaining,
        'supported_shortage_by_level': {'easy': remaining['easy']}, 'capability_exceptions': caps['capability_exceptions'],
        'excluded_source_questions': stock['excluded_source_questions'], 'inventory_recheck_basis': inv['basis'],
        'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP],
        'evidence': [str(p.relative_to(ROOT)) for p in [HERE/'classification.md', HERE/'template-extraction.md', HERE/'extraction.json',
            HERE/'source-fidelity.json', HERE/'validation.json', HERE/'review.md', HERE/'freeze.json', path/'preparation.json',
            path/'transaction.edn', path/'preview.edn', path/'commit-intent.json', path/'commit.edn', path/'verification.json',
            path/'inventory-after.json', path/'final/counts.json'] if p.exists()],
        'note': 'Classification and generator registered. No new questions needed: existing fresh gradable easy stock exceeds five. Unsupported bands are not filled.' if verified['new_questions'] == 0 else 'Fresh validated questions added only for a supported deficit.'}
    save(path/'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps(result, indent=2))


def run(preview):
    OUT.mkdir(parents=True, exist_ok=True)
    # Reconcile exact saved intent before reading/recomputing any new submission.
    for path in sorted(OUT.glob('basis-*')):
        if (path/'commit-intent.json').exists():
            intent = json.loads((path/'commit-intent.json').read_text())
            assert intent['database'] == 'math' and intent['lineage'] == g.LINEAGE and intent['endpoint'] == DB.args.endpoint
            assert intent['source'] == SOURCE and intent['exact_edn'] == (path/'transaction.edn').read_text()
            assert intent['sha256'] == sha(path/'transaction.edn') and intent['generator_sha256'] == sha(HERE.with_suffix('.py'))
            assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report = DB._commit(intent, path/'transaction.edn', path)
            finish(path, intent, verify(path, intent, report)); return
    inv = inventory(OUT/'inventory-before.json'); basis = inv['basis']
    assert DB.basis() == basis and g.LINEAGE in DB.command('status')
    path = OUT/('basis-'+str(basis)); path.mkdir(exist_ok=True)
    kp = read_kp(path, basis)
    source = g.SOURCE['record']
    current = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
    assert all(canonical(current[q[':db/id']]) == canonical(q) for q in source[':knowledge-point/questions'])
    assert canonical(kp[':knowledge-point/canonical-example']) == canonical(source[':knowledge-point/canonical-example'])
    (path/'before.edn').write_text(dumps(kp)+'\n')
    contributor = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', basis)
    assert len(contributor) == 1
    registrations = DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]', [SCRIPT], path, 'generator-by-script', basis)
    assert len(registrations) <= 1
    gen = kp.get(':knowledge-point/question-generator')
    saved = json.loads((HERE/'generator-id.json').read_text()) if (HERE/'generator-id.json').exists() else {}
    gid = str(gen[':question-generator/id']) if gen else str(registrations[0][0][':question-generator/id']) if registrations else saved.get('id', str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'question-generator')))
    assert not saved or saved['id'] == gid
    if gen:
        assert gen[':question-generator/script'] == SCRIPT
    save(HERE/'generator-id.json', {'id': gid, 'script': SCRIPT, 'knowledge_point': KP})
    identity = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [uuid.UUID(gid)], path, 'generator-identity', basis)
    assert not identity or len(identity) == 1 and identity[0][0][':question-generator/script'] == SCRIPT
    stock = counts(kp, path/'inventory-before', basis)
    needed = max(0, 5-stock['distinct_available']['easy'])
    used = {g.task_fingerprint(g.parse(q[':question/problem'])) for q in kp[':knowledge-point/questions']}
    used.add(g.task_fingerprint(json.loads((HERE/'canonical-assets.json').read_text())['parameters']))
    records = []
    supplied_path = JOB.with_suffix('.generated')
    supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances = supplied.get('instances', [])
    if isinstance(instances, dict):
        instances = [instances]
    def consider(rec):
        v.inspect(rec); meta = rec['generation']
        replay = g.generate('easy', meta['seed'], meta['template'], meta['parameters'], meta['bank_profile'])
        assert v.normalized(replay['question']) == v.normalized(rec['question'])
        fp = g.task_fingerprint(g.parse(rec['question'][':question/problem']))
        assert fp == meta['parameter_fingerprint']
        if len(records) < needed and fp not in used:
            records.append(rec); used.add(fp)
    for rec in instances:
        consider(rec)
    if instances:
        grade(instances, path/'supplied-validation')
    for i in range(1000):
        if len(records) == needed:
            break
        consider(g.generate(seed=int(JOB.name[:8], 16)+i))
    assert len(records) == needed, 'Bounded sampling could not fill supported deficit; retain explicit shortage'
    for attr, ids in [('question/id', [uuid.UUID(r['question'][':question/id']) for r in records]),
                      ('answer-field/id', [uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),
                      ('answer/id', [uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
        if ids:
            assert len(ids) == len(set(ids))
            assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]', [ids], path, attr.replace('/', '-')+'-identity', basis)
    save(path/'generated.json', records)
    if records:
        grade(records, path/'generated-validation')
    save(path/'preparation.json', {'basis': basis, 'lineage': g.LINEAGE, 'source': SOURCE, 'source_eid': contributor[0][0],
        'needed_easy': needed, 'selected_easy': len(records), 'source_questions_unchanged': True,
        'inventory': stock, 'supplied_generated_exists': supplied_path.exists(), 'supplied_instances_validated': len(instances),
        'asset_publication': [], 'generator_version': g.VERSION,
        'capability_exceptions': json.loads((HERE/'capabilities.json').read_text())['capability_exceptions']})
    forms = transaction(records, kp, gid)
    if not forms:
        raise RuntimeError('Already registered with no changes and no saved receipt; inspect existing registration provenance')
    txpath = path/'transaction.edn'; txpath.write_text(dumps(forms)+'\n')
    result = subprocess.run([str(preview), 'with', '--database', 'math', '--source', SOURCE, '--file', str(txpath)],
        env=DB.env, check=True, capture_output=True, text=True, timeout=55)
    (path/'preview.edn').write_text(result.stdout)
    report = loads(result.stdout)
    assert report[':edb/committed'] is False and report[':edb/db-before-t'] == basis
    check_report(report, path/'preview-check', contributor[0][0])
    assert DB.basis() == basis
    intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': g.LINEAGE, 'source': SOURCE,
        'source_eid': contributor[0][0], 'basis': basis, 'expected_basis': basis, 'sha256': sha(txpath),
        'request_key': 'leading-entry-generator-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),
        'exact_edn': txpath.read_text(), 'generator_id': gid, 'generator_path': SCRIPT,
        'generator_sha256': sha(HERE.with_suffix('.py')), 'lock': str(LOCK),
        'connection_sha256': hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
    save(path/'commit-intent.json', intent)
    report = DB._commit(intent, txpath, path)
    finish(path, intent, verify(path, intent, report))


def main():
    assert json.loads((HERE/'validation.json').read_text())['status'] == 'pass'
    for name, expected in json.loads((HERE/'freeze.json').read_text())['sha256'].items():
        assert sha(ROOT/name) == expected, 'Frozen artifact changed: '+name
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    for attempt in range(3):
        try:
            with LOCK.open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                run(preview)
            return
        except StaleBasis:
            if attempt == 2:
                raise


if __name__ == '__main__':
    main()

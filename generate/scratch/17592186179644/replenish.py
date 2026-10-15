"""Validate current finite stock and register this KP's generator additively."""
import fcntl
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import threading
import uuid
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts'))
from serve_graph_explorer import database_environment
from inventory_jobs import save
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database, StaleBasis
from edn import dumps, loads, kw
spec = importlib.util.spec_from_file_location('flux_validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g

KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '8f575949641909694c44bcdaf11c1ced6826a1b57f84502ddd06722fc6df26b7'
LOCK = ROOT / '.local/learning/requests/math/api.lock'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'),
                              database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env = ENV
NATIVE = ROOT / '.local/graph-explorer/learning-ef48cfde3a25d91e'
POOL = ROOT / 'generate/scratch/17592186110754/check-pool'
QUERY = (HERE / 'reference/source-query.edn').read_text()
LEVELS = ('easy', 'moderate', 'hard')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(x):
    if isinstance(x, dict):
        return {str(k): canonical(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return sorted([canonical(v) for v in x], key=lambda a: json.dumps(a, sort_keys=True))
    return str(x) if isinstance(x, uuid.UUID) else x


def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}',
                       env=ENV, text=True, capture_output=True, check=True, timeout=55)
    data = json.loads(r.stdout)
    assert data['ok'] and data['data']['lineage'] == LINEAGE
    save(path, data['data'])
    return data['data']


def read(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]


def scoped(kp, basis, excluded):
    entities, enums = {}, {}

    def enum(value):
        name = str(value[':db/ident']).lstrip(':')
        if name not in enums:
            e = len(enums) + 1
            enums[name] = e
            entities[str(e)] = {'db/ident': name}
        return enums[name]

    for q in kp[':knowledge-point/questions'] + [kp[':knowledge-point/canonical-example']]:
        row = {'question/id': str(q[':question/id']), 'question/problem': q[':question/problem'],
               'question/answer-fields': []}
        entities[str(q[':db/id'])] = row
        if ':question/difficulty' in q:
            row['question/difficulty'] = enum(q[':question/difficulty'])
        for f in q.get(':question/answer-fields', []):
            row['question/answer-fields'].append(f[':db/id'])
            field = {'answer-field/key': f[':answer-field/key'], 'answer-field/type': enum(f[':answer-field/type']),
                     'answer-field/choices': [a[':db/id'] for a in f.get(':answer-field/choices', [])]}
            entities[str(f[':db/id'])] = field
            if ':answer-field/correct' in f:
                field['answer-field/correct'] = f[':answer-field/correct'][':db/id']
            for a in f.get(':answer-field/choices', []):
                entities[str(a[':db/id'])] = {'answer/type': enum(a[':answer/type']), 'answer/value': a[':answer/value']}
    entities[str(KP)] = {'knowledge-point/id': str(kp[':knowledge-point/id']),
                         'knowledge-point/title': kp[':knowledge-point/title'],
                         'knowledge-point/questions': [q[':db/id'] for q in kp[':knowledge-point/questions']],
                         'knowledge-point/canonical-example': kp[':knowledge-point/canonical-example'][':db/id']}
    return {'basis_t': basis, 'knowledge_point': KP, 'entities': entities, 'seen': sorted(excluded)}


def counts(kp, path, basis):
    path.mkdir(parents=True, exist_ok=True)
    args = [KP, LEARNER]
    shown = DB.query('''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
      [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i]
      [?i :task-item/content ?q]]''', args, path, 'ever-shown', basis, history=True)
    reserved = DB.query('''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
      [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status]
      (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
      [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]''',
      args, path, 'reserved', basis)
    excluded = {r[0] for r in shown + reserved}
    save(path / 'scoped-snapshot.json', scoped(kp, basis, excluded))
    proc = subprocess.run([str(POOL), str(path / 'scoped-snapshot.json'), str(path / 'native-pool.json')],
                          capture_output=True, text=True, check=True, timeout=55)
    (path / 'native-pool.log').write_text(proc.stdout + proc.stderr)
    pool = json.loads((path / 'native-pool.json').read_text())
    available_ids = {e for xs in pool['available_ids_by_level'].values() for e in xs}
    fingerprints = {l: set() for l in LEVELS}
    ids = {l: [] for l in LEVELS}
    records = []
    for q in kp[':knowledge-point/questions']:
        t = q[':question/math-academy-id']
        assert t in g.TEMPLATES, 'New source evidence requires reclassification'
        level = g.TEMPLATES[t]
        r = g.generate(level, template=t)
        assert g.normalize(q) == r['question'], 'Existing question content changed'
        v.check(r)
        records.append(r)
        if q[':db/id'] in available_ids:
            fingerprints[level].add(g.fingerprint(t))
            ids[level].append(q[':db/id'])
    v.grade(records, path / 'native-grading')
    result = {'basis': basis, 'distinct_available': {l: len(fingerprints[l]) for l in LEVELS},
              'available_ids': ids, 'shown_ids': sorted(r[0] for r in shown),
              'reserved_ids': sorted(r[0] for r in reserved), 'canonical_example_excluded': True,
              'native_pool': pool, 'validated_source_questions': len(records)}
    save(path / 'available-counts.json', result)
    return result


def forms(kp, gid, generator_eid=None):
    gen = kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
        return []
    if generator_eid is None:
        out = [{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid),
                kw('question-generator/script'): SCRIPT}]
        ref = 'generator'
    else:
        out = []
        ref = generator_eid
    out += [[kw('db/add'), KP, kw('knowledge-point/question-generator'), ref],
            [kw('db/ensure'), KP, kw('knowledge-point/validate')]]
    for q in kp[':knowledge-point/questions']:
        out.append([kw('db/ensure'), q[':db/id'], kw('question/validate')])
        for f in q[':question/answer-fields']:
            out.append([kw('db/ensure'), f[':db/id'], kw('answer-field/validate')])
            out.extend([kw('db/ensure'), a[':db/id'], kw('answer/validate')] for a in f[':answer-field/choices'])
    return out


def check_report(report, path, source_eid):
    attrs = {e: str(a) for e, a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    for e, a, value, tx, source, added in report[':edb/tx-data']:
        assert added and source == source_eid, 'Unexpected retraction or contributor'
        name = attrs[a]
        if e == KP:
            assert name == ':knowledge-point/question-generator'
        elif name != ':db/txInstant':
            assert e in new and name in (':question-generator/id', ':question-generator/script')


def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path / 'receipt-check', intent['source_eid'])
    after = report[':edb/db-after-t']
    kp = read(path / 'readback', after)
    before = loads((path / 'before.edn').read_text())
    omit = ':knowledge-point/question-generator'
    assert canonical({k: z for k, z in before.items() if k != omit}) == canonical({k: z for k, z in kp.items() if k != omit})
    assert not forms(kp, intent['generator_id'])
    stock = counts(kp, path / 'readback', after)
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': after,
              'new_questions': 0, 'source_questions_unchanged': len(kp[':knowledge-point/questions']),
              'canonical_example_unchanged': True, 'learner_history_unchanged': True,
              'only_additive_generator_registration_datoms': True, 'generator_registration_verified': True,
              'repeat_preparation_content_changes': 0, 'available_after': stock}
    save(path / 'verification.json', result)
    return result


def finish(path, gid, verified, inv):
    stock = counts(read(path / 'current-inventory', inv['basis']), path / 'current-inventory', inv['basis'])
    caps = json.loads((HERE / 'capabilities.json').read_text())
    result = {'outcome': 'finite-limit', 'knowledgePoint': KP, 'generator_path': SCRIPT,
              'generator_id': gid, 'generator_registered': True, 'lineage': LINEAGE,
              'verified_commit_basis': verified.get('basis_after'), 'inventory_recheck_basis': inv['basis'],
              'new_questions': 0, 'new_questions_by_level': {l: 0 for l in LEVELS},
              'supported_levels': list(g.SUPPORTED_LEVELS), 'unsupported_levels': ['hard'],
              'unsupported_levels_filled': False, 'available_by_level': stock['distinct_available'],
              'shortage_by_level': {l: max(0, 5 - stock['distinct_available'][l]) for l in LEVELS},
              'finite_catalog': caps['finite_catalog'], 'additional_distinct_tasks': 0,
              'capability_exceptions': caps['capability_exceptions'],
              'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP],
              'evidence': [str(p.relative_to(ROOT)) for p in (
                  HERE / 'validation.json', HERE / 'freeze.json', HERE / 'capabilities.json', HERE / 'classification.md',
                  HERE / 'template-extraction.md', HERE / 'plot-extraction.md', HERE / 'source-components.json',
                  HERE / 'source-fidelity.json', path / 'generated.json', path / 'preparation.json',
                  path / 'transaction.edn', path / 'commit-intent.json', path / 'preview.edn', path / 'commit.edn',
                  path / 'verification.json', path / 'inventory-after.json', path / 'current-inventory/available-counts.json') if p.exists()],
              'note': 'Existing easy/moderate reserves are validated; no duplicate questions were committed. The bounded catalog has no fresh variants. Hard remains explicitly unsupported and unfilled.'}
    save(path / 'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k: result[k] for k in ('outcome', 'verified_commit_basis', 'new_questions', 'available_by_level', 'shortage_by_level', 'generator_id')}), flush=True)


def run_locked(preview):
    for path in sorted(OUT.glob('basis-*')):
        if not (path / 'commit-intent.json').exists():
            continue
        intent = json.loads((path / 'commit-intent.json').read_text())
        assert intent['database'] == 'math' and intent['lineage'] == LINEAGE and intent['endpoint'] == DB.args.endpoint and intent['source'] == SOURCE
        assert intent['exact_edn'] == (path / 'transaction.edn').read_text() and intent['transaction_sha256'] == sha(path / 'transaction.edn')
        assert intent['connection_sha256'] == hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
        assert LINEAGE in DB.command('status')
        report = DB._commit(intent, path / 'transaction.edn', path)
        verified = verify(path, intent, report)
        finish(path, intent['generator_id'], verified, inventory(path / 'inventory-after.json'))
        return
    inv = inventory(OUT / 'inventory-before.json')
    basis = inv['basis']
    assert DB.basis() == basis and LINEAGE in DB.command('status')
    path = OUT / ('basis-' + str(basis))
    path.mkdir(exist_ok=True)
    kp = read(path, basis)
    assert canonical({k: z for k, z in kp.items() if k != ':knowledge-point/question-generator'}) == canonical(g.SOURCE['record']), 'Source facts changed; reclassify'
    (path / 'before.edn').write_text(dumps(kp) + '\n')
    stock = counts(kp, path / 'current-stock', basis)
    reg = kp.get(':knowledge-point/question-generator')
    gid = str(reg[':question-generator/id']) if reg else g.GENERATOR_ID
    identities = DB.query('''[:find (pull ?g [*]) :in $ ?id ?script :where
       (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]''',
       [uuid.UUID(gid), SCRIPT], path, 'generator-identity', basis)
    generator_eid = None
    if identities:
        assert len(identities) == 1
        existing = identities[0][0]
        assert existing[':question-generator/script'] == SCRIPT
        if reg:
            assert str(existing[':question-generator/id']) == gid
        gid, generator_eid = str(existing[':question-generator/id']), existing[':db/id']
    save(HERE / 'registration.json', {'id': gid, 'script': SCRIPT, 'existing_identity_reused': bool(reg or identities)})
    contributors = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', basis)
    assert len(contributors) == 1
    supplied = JOB.with_suffix('.generated')
    package = json.loads(supplied.read_text()) if supplied.exists() else {}
    instances = package.get('instances', [])
    if isinstance(instances, dict):
        instances = [instances]
    for rec in instances:
        v.check(rec)
    proc = subprocess.run([str(ROOT / '.venv/bin/python'), str(HERE.with_suffix('.py')), '--difficulty', 'all',
                           '--count', '1000', '--seed', '20261015', '--format', 'json'],
                          capture_output=True, text=True, check=True, timeout=55)
    candidates = json.loads(proc.stdout)
    used = {g.fingerprint(q[':question/math-academy-id']) for q in kp[':knowledge-point/questions']}
    for rec in candidates:
        v.check(rec)
    assert all(r['generation']['mathematical_fingerprint'] in used for r in candidates)
    save(path / 'candidates.json', candidates)
    save(path / 'generated.json', [])
    assets = json.loads((HERE / 'reference/assets.json').read_text())
    for ref, asset in assets.items():
        assert sha(Path('/media/jake/SSD/EDB/math') / ref) == asset['sha256']
    save(path / 'preparation.json', {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE,
          'source_eid': contributors[0][0], 'available_before': stock,
          'candidate_tasks': len(candidates), 'duplicates_excluded': len(candidates), 'new_questions': 0,
          'supplied_generated_exists': supplied.exists(), 'supplied_instances_validated': len(instances),
          'asset_hashes': assets, 'capability_exceptions': json.loads((HERE / 'capabilities.json').read_text())['capability_exceptions']})
    txforms = forms(kp, gid, generator_eid)
    if not txforms:
        verified = {'passed': True, 'basis_after': None, 'no_change_basis': basis, 'new_questions': 0}
        save(path / 'verification.json', verified)
        finish(path, gid, verified, inv)
        return
    tx = dumps(txforms) + '\n'
    txpath = path / 'transaction.edn'
    with txpath.open('w') as stream:
        stream.write(tx)
        stream.flush()
        os.fsync(stream.fileno())
    proc = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE],
                          env=ENV, text=True, capture_output=True, check=True, timeout=55)
    (path / 'preview.edn').write_text(proc.stdout)
    report = loads(proc.stdout)
    assert report[':edb/committed'] is False and report[':edb/db-before-t'] == basis
    check_report(report, path / 'preview-check', contributors[0][0])
    if DB.basis() != basis:
        raise StaleBasis('Basis changed before submission; prepare again')
    intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE, 'source': SOURCE,
              'source_eid': contributors[0][0], 'basis': basis, 'expected_basis': basis,
              'request_key': 'flux-sign-finite-register-' + str(KP) + '-' + str(basis) + '-' + sha(txpath),
              'transaction_sha256': sha(txpath), 'exact_edn': tx, 'generator_id': gid,
              'generator_path': SCRIPT, 'generator_sha256': sha(HERE.with_suffix('.py')), 'question_uuids': [],
              'connection_sha256': hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(LOCK)}
    save(path / 'commit-intent.json', intent)
    verified = verify(path, intent, DB._commit(intent, txpath, path))
    finish(path, gid, verified, inventory(path / 'inventory-after.json'))


def main():
    freeze = json.loads((HERE / 'freeze.json').read_text())
    assert all(sha(ROOT / file) == digest for file, digest in freeze['sha256'].items())
    validation = json.loads((HERE / 'validation.json').read_text())
    assert validation['status'] == 'passed' and validation['script_sha256'] == sha(HERE.with_suffix('.py'))
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),
                                   repo_root=ROOT, preview_bin=None), threading.Event())
    with LOCK.open('a') as lock:
        print('Waiting for application api.lock', flush=True)
        fcntl.flock(lock, fcntl.LOCK_EX)
        print('Application api.lock acquired', flush=True)
        for attempt in range(3):
            try:
                run_locked(preview)
                return
            except StaleBasis:
                if attempt == 2:
                    raise
                print('Confirmed changed basis; preparing again under held lock', flush=True)


if __name__ == '__main__':
    main()

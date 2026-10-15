"""Register the finite generator, preserving all content and learner facts."""
import fcntl
import hashlib
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
sys.path[:0] = [str(HERE), str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
import validate as v
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment

g = v.g
KP = g.KP
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'644170d118a3338463ad6293ef9337273d219bfa3194bc0bcb47fbade5b2d9e2'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env = ENV
QUERY = (HERE/'reference/source-query.edn').read_text()
LOCK = ROOT/'.local/learning/requests/math/api.lock'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(directory, basis):
    return DB.query(QUERY, [KP], directory, 'kp', basis)[0][0]


def inventory(path):
    r = subprocess.run([str(ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'), 'math', LEARNER, DB.args.endpoint],
                       input='{"action":"inventory"}', env=ENV, capture_output=True, text=True, check=True, timeout=55)
    data = json.loads(r.stdout)
    assert data['ok'] and data['data']['lineage'] == LINEAGE
    save(path, data['data'])
    return data['data']


def counts(kp, basis, directory):
    shown = DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',
                     [KP, LEARNER], directory, 'ever-shown', basis, history=True)
    reserved = DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',
                        [KP, LEARNER], directory, 'reserved', basis)
    unavailable = {row[0] for row in shown+reserved}
    # Feed the captured scoped graph through the existing native pool helper.
    entities = {}; enums = {}
    def enum(value):
        name = str(value[':db/ident']).lstrip(':')
        if name not in enums:
            enums[name] = len(enums)+1
            entities[str(enums[name])] = {'db/ident': name}
        return enums[name]
    questions = kp[':knowledge-point/questions']
    for q in questions+[kp[':knowledge-point/canonical-example']]:
        r = {'question/id': str(q[':question/id']), 'question/problem': q[':question/problem'], 'question/answer-fields': []}
        entities[str(q[':db/id'])] = r
        if ':question/difficulty' in q: r['question/difficulty'] = enum(q[':question/difficulty'])
        for f in q.get(':question/answer-fields', []):
            r['question/answer-fields'].append(f[':db/id'])
            field = {'answer-field/key': f[':answer-field/key'], 'answer-field/type': enum(f[':answer-field/type']),
                     'answer-field/choices': [a[':db/id'] for a in f[':answer-field/choices']], 'answer-field/correct': f[':answer-field/correct'][':db/id']}
            entities[str(f[':db/id'])] = field
            for a in f[':answer-field/choices']:
                entities[str(a[':db/id'])] = {'answer/type': enum(a[':answer/type']), 'answer/value': a[':answer/value']}
    entities[str(KP)] = {'knowledge-point/id': str(kp[':knowledge-point/id']),
                         'knowledge-point/title': kp[':knowledge-point/title'],
                         'knowledge-point/questions': [q[':db/id'] for q in questions],
                         'knowledge-point/canonical-example': kp[':knowledge-point/canonical-example'][':db/id']}
    save(directory/'scoped-snapshot.json', {'basis_t': basis, 'knowledge_point': KP, 'entities': entities, 'seen': sorted(unavailable)})
    subprocess.run([str(ROOT/'generate/scratch/17592186110754/check-pool'), str(directory/'scoped-snapshot.json'), str(directory/'pool.json')],
                   capture_output=True, text=True, check=True, timeout=55)
    pool = json.loads((directory/'pool.json').read_text())
    eligible = {e for xs in pool['available_ids_by_level'].values() for e in xs}
    supported = [q for q in questions if q.get(':question/math-academy-id') in g.TARGETS and q[':db/id'] in eligible]
    tasks = sorted({g.TARGETS[q[':question/math-academy-id']] for q in supported})
    report = {'basis': basis, 'available_distinct_validated': {'easy': len(tasks), 'moderate': 0, 'hard': 0},
              'validated_available_source_profiles': [q[':question/math-academy-id'] for q in supported],
              'distinct_tasks': tasks, 'native_pool_counts': {l: len(xs) for l, xs in pool['available_ids_by_level'].items()},
              'excluded_source_profiles': g.EXCLUDED, 'shown_or_reserved': sorted(unavailable),
              'canonical_excluded': True, 'unrated_excluded': True}
    save(directory/'counts.json', report)
    return report


def verify(path, intent, receipt):
    assert receipt[':edb/committed'] is True and receipt[':edb/db-before-t'] == intent['basis']
    attrs = dict(DB.attributes(path/'attribution', intent['basis']))
    new_entities = set(receipt[':edb/tempids'].values())
    for e, a, value, tx, source, added in receipt[':edb/tx-data']:
        assert added and source == intent['source_eid']
        name = str(attrs[a])
        if e == KP:
            assert name == ':knowledge-point/question-generator'
        elif name != ':db/txInstant':
            assert (e in new_entities or e == intent.get('generator_eid_before')) and name in (':question-generator/id', ':question-generator/script')
    after_basis = receipt[':edb/db-after-t']
    before = loads((path/'before.edn').read_text())
    after = read(path/'readback', after_basis)
    exclude = ':knowledge-point/question-generator'
    assert {k: x for k, x in before.items() if k != exclude} == {k: x for k, x in after.items() if k != exclude}
    gen = after[exclude]
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    c = counts(after, after_basis, path/'readback/inventory')
    v.grading([g.replay(t) for t in g.TARGETS], path/'readback/grading')
    verified = {'passed': True, 'basis_before': intent['basis'], 'basis_after': after_basis,
                'registered_generator': str(gen[':question-generator/id']), 'generator_path': SCRIPT,
                'new_questions': 0, 'all_12_source_questions_unchanged': True,
                'canonical_example_unchanged': True, 'all_fields_answers_solutions_unchanged': True,
                'all_datoms_additive_and_attributed': True, 'learner_history_unchanged': True,
                'only_generator_registration_changed': True, 'repeat_preparation_content_changes': 0,
                'available_counts_after': c}
    save(path/'verification.json', verified)
    return verified


def finish(path, verified):
    inv = inventory(path/'inventory-after.json')
    c = verified['available_counts_after']['available_distinct_validated']
    result = {'outcome': 'finite-limit', 'knowledgePoint': KP, 'generator_path': SCRIPT,
              'generator_id': verified['registered_generator'], 'lineage': LINEAGE,
              'verified_commit_basis': verified['basis_after'], 'new_questions': 0,
              'supported_levels': ['easy'], 'unsupported_levels': g.UNSUPPORTED,
              'available_distinct_validated': c, 'shortage_remaining': {l: max(0, 5-n) for l,n in c.items()},
              'unsupported_levels_filled': False, 'lesson_minimum_met': c['easy'] >= 5,
              'finite_distinct_supported_tasks': 5, 'new_distinct_capacity_beyond_source': 0,
              'capability_exception': 'The bounded source-backed generator has five distinct validated targets, all already present. It returns no duplicate instances. Additional target contracts/banks or higher levels require new evidence or separately validated extensions.',
              'native_inventory_basis': inv['basis'], 'remaining_native_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP],
              'native_counts_are_not_mathematical_validation': True,
              'evidence': [str(p.relative_to(ROOT)) for p in [path/'verification.json', path/'commit-intent.json',
                   path/'transaction.edn', path/'preview.edn', path/'commit.edn', path/'preparation.json',
                   path/'generator-execution.json', path/'inventory-after.json',
                   HERE/'reference/validation/validation.json', HERE/'reference/classification.md',
                   HERE/'reference/template-extraction.json', HERE/'reference/template-extraction.md', HERE/'reference/review.md']]}
    save(path/'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps(result, indent=2), flush=True)


def main():
    v.main()
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    with LOCK.open('a') as lock:
        print('Waiting for application api.lock', flush=True)
        fcntl.flock(lock, fcntl.LOCK_EX)
        print('Application api.lock acquired', flush=True)
        # Resolve an existing exact intent before any new registration.
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists(): continue
            intent = json.loads((path/'commit-intent.json').read_text())
            assert intent['database'] == 'math' and intent['endpoint'] == DB.args.endpoint and intent['lineage'] == LINEAGE
            assert intent['sha256'] == sha(path/'transaction.edn') and intent['exact_edn'] == (path/'transaction.edn').read_text()
            assert intent['connection_sha256'] == hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
            finish(path, verify(path, intent, DB._commit(intent, path/'transaction.edn', path)))
            return
        inv = inventory(OUT/'inventory-under-lock.json')
        basis = inv['basis']; assert DB.basis() == basis
        path = OUT/f'basis-{basis}'; path.mkdir(exist_ok=True)
        kp = read(path, basis)
        initial = loads((HERE/'reference/initial/kp.edn').read_text())[0][0]
        assert kp == initial, 'Source or registration changed: reclassify before mutation'
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'source', basis)
        assert len(source) == 1
        gid = str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'question-generator'))
        existing = DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',
                            [uuid.UUID(gid), SCRIPT], path, 'generator-identity', basis)
        existing_eid = None
        if existing:
            assert len(existing) == 1
            entity = existing[0][0]
            assert entity[':question-generator/script'] == SCRIPT
            gid = str(entity[':question-generator/id'])
            existing_eid = entity[':db/id']
        c = counts(kp, basis, path/'current-inventory')
        needed = max(0, 5-c['available_distinct_validated']['easy'])
        execution = g.generate('easy', needed, seed=int(JOB.name[:8], 16))
        save(path/'generator-execution.json', execution)
        supplied = JOB.with_suffix('.generated')
        assert not supplied.exists(), 'Saved instances appeared: validate before preparing'
        save(path/'supplied-status.json', {'exists': False, 'validated_instances': 0})
        assert execution['instances'] == []
        save(path/'generated.json', [])
        forms = [] if existing_eid else [{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid), kw('question-generator/script'): SCRIPT}]
        forms += [[kw('db/add'), KP, kw('knowledge-point/question-generator'), existing_eid or 'generator'],
                  [kw('db/ensure'), KP, kw('knowledge-point/validate')]]
        tx = dumps(forms)+'\n'; txpath = path/'transaction.edn'
        with txpath.open('w') as stream:
            stream.write(tx); stream.flush(); os.fsync(stream.fileno())
        save(path/'preparation.json', {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE, 'inventory': c,
             'scope': 'generator registration only', 'new_questions': 0, 'asset_hashes': {},
             'source_identities_reused_without_republication': True, 'supported_easy_shortage': needed,
             'generator_sha256': sha(HERE.with_suffix('.py')), 'validation': 'reference/validation/validation.json'})
        response = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE],
                                  env=ENV, capture_output=True, text=True, check=True, timeout=55)
        (path/'preview.edn').write_text(response.stdout)
        pr = loads(response.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == basis
        assert DB.basis() == basis
        intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE,
                  'source': SOURCE, 'source_eid': source[0][0], 'basis': basis, 'expected_basis': basis,
                  'generator_id': gid, 'generator_eid_before': existing_eid, 'generator_path': SCRIPT, 'generator_sha256': sha(HERE.with_suffix('.py')),
                  'request_key': 'invertible-theorem-finite-generator-'+str(basis)+'-'+sha(txpath),
                  'sha256': sha(txpath), 'exact_edn': tx,
                  'connection_sha256': hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),
                  'lock': str(LOCK), 'new_question_uuids': []}
        save(path/'commit-intent.json', intent)
        verified = verify(path, intent, DB._commit(intent, txpath, path))
        save(HERE/'registration.json', {'id': gid, 'script': SCRIPT, 'verified_basis': verified['basis_after']})
        finish(path, verified)


if __name__ == '__main__':
    main()

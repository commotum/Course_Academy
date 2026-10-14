"""Register this source-backed generator; preserve explicit unsupported reserve."""
import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

H = Path(__file__).resolve().parent
ROOT = H.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.storage import atomic_json, atomic_text
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import loads, dumps, kw
spec = importlib.util.spec_from_file_location('validation', H / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
SOURCE = ':application/ca-engine'
SCRIPT = str(H.with_suffix('.py').relative_to(ROOT))
OUT = ROOT / 'reference/generated/17592186096701/job-7fb1f038'
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '7fb1f038e868ab9d9617002d604126eb985a2e024b5395fae566a3275b0c36ed'
LOCK = ROOT / '.local/learning/requests/math/api.lock'
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint='/tmp/edb-math/writer.sock'))
NATIVE = ROOT / '.local/graph-explorer/learning-ef48cfde3a25d91e'
QUESTION = '''[* {:question/difficulty [:db/ident]}
 {:knowledge-point/_canonical-example [:db/id]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]'''
QUERY = '[:find (pull ?k [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example ' + QUESTION + '} {[:knowledge-point/questions :limit nil] ' + QUESTION + '}]) :in $ ?k :where [?k :knowledge-point/id _]]'
USAGE = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(x):
    if isinstance(x, dict):
        return {str(k):canonical(z) for k,z in x.items() if str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(x, list):
        return sorted([canonical(z) for z in x], key=lambda z:json.dumps(z, sort_keys=True))
    if isinstance(x, uuid.UUID):
        return str(x)
    return x


def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=DB.env, text=True, capture_output=True, timeout=55, check=True)
    data = json.loads(r.stdout)
    assert data['ok'] and data['data']['lineage'] == LINEAGE
    atomic_json(path, data['data'])
    return data['data']


def kp(path, basis):
    rows = DB.query(QUERY, [KP], path, 'kp', basis)
    assert len(rows) == 1 and str(rows[0][0][':knowledge-point/id']) == g.KP_UUID
    return rows[0][0]


def counts(record, path, basis):
    unavailable = {r[0] for r in DB.query(USAGE, [KP, LEARNER], path, 'unavailable', basis)}
    unavailable.update(r[0] for r in DB.query(USAGE, [KP, LEARNER], path, 'historical-unavailable', basis, history=True))
    cases = {c['source_id']:c for c in json.loads((H / 'source-cases.json').read_text())}
    fresh = {level:set() for level in g.SUPPORTED_LEVELS}
    ids = {level:[] for level in g.SUPPORTED_LEVELS}
    for q in record[':knowledge-point/questions']:
        c = cases[q[':question/math-academy-id']]
        replay = g.generate(c['level'], profile=c['profile'], parameters=c['parameters'])
        v.fidelity(q, replay)
        if q[':db/id'] not in unavailable and not q.get(':knowledge-point/_canonical-example'):
            fresh[c['level']].add(replay['generation']['mathematical_fingerprint'])
            ids[c['level']].append(str(q[':question/id']))
    data = {'basis':basis, 'distinct_available_tasks':{level:len(tasks) for level,tasks in fresh.items()}, 'available_ids':ids, 'excluded_shown_or_reserved':sorted(unavailable), 'hard_available':0, 'hard_nominal_shortage':5}
    atomic_json(path / 'available-counts.json', data)
    return data


def report_check(report, path, source_eid):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    actual = []
    for e,a,value,tx,source,added in report[':edb/tx-data']:
        assert source == source_eid and added is True, 'Unexpected provenance or retraction'
        name = attrs[a]
        if name == ':db/txInstant':
            continue
        if e == KP:
            assert name == ':knowledge-point/question-generator'
        else:
            assert name in (':question-generator/id', ':question-generator/script')
        actual.append(name)
    assert sorted(actual) == sorted([':question-generator/id', ':question-generator/script', ':knowledge-point/question-generator'])


def registration_forms(record, generator_id):
    existing = record.get(':knowledge-point/question-generator')
    if existing:
        assert str(existing[':question-generator/id']) == generator_id and existing[':question-generator/script'] == SCRIPT
        return []
    return [{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(generator_id), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator'], [kw('db/ensure'), KP, kw('knowledge-point/validate')]]


def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    report_check(report, path / 'receipt-check', intent['source_eid'])
    after = report[':edb/db-after-t']
    record = kp(path / 'readback', after)
    before = loads((path / 'before.edn').read_text())
    assert {k:z for k,z in record.items() if k != ':knowledge-point/question-generator'} == before
    gen = record[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    assert registration_forms(record, intent['generator_id']) == [], 'Repeat preparation must produce no changes'
    available = counts(record, path / 'readback', after)
    check = {'passed':True, 'basis_before':intent['basis'], 'basis_after':after, 'generator_registration_verified':True, 'new_questions':0, 'all_14_source_questions_and_canonical_example_unchanged':True, 'learner_history_unchanged':True, 'only_three_generator_registration_facts_plus_txInstant':True, 'repeat_preparation_content_changes':0, 'available_counts':available}
    atomic_json(path / 'verification.json', check)
    inv = inventory(path / 'inventory-after.json')
    result = {'outcome':'unsupported', 'knowledgePoint':KP, 'generator_path':SCRIPT, 'generator_id':intent['generator_id'], 'verified_commit_basis':after, 'verified_commit_basis_before':intent['basis'], 'lineage':LINEAGE, 'new_questions':0, 'supported_levels':list(g.SUPPORTED_LEVELS), 'available_counts':available, 'shortage_remaining':{'easy':max(0,5-available['distinct_available_tasks']['easy']), 'moderate':max(0,5-available['distinct_available_tasks']['moderate']), 'hard':5}, 'unsupported_levels_filled':False, 'capability_exceptions':json.loads((H / 'capabilities.json').read_text())['exceptions'], 'inventory_recheck_basis':inv['basis'], 'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint'] == KP], 'note':'Easy and moderate already meet the five-question reserve; no new questions needed. Registered source-backed generator. Hard is a bounded unsupported capability and its nominal reserve remains explicit.', 'evidence':[str(p.relative_to(ROOT)) for p in [path / 'commit-intent.json', path / 'transaction.edn', path / 'preview.edn', path / 'commit.edn', path / 'verification.json', path / 'preparation.json', path / 'inventory-after.json', H / 'validation.json', H / 'capabilities.json']]}
    atomic_json(path / 'outcome.json', result)
    atomic_json(JOB.with_suffix('.result'), result)
    print(json.dumps({'outcome':result['outcome'], 'verified_commit_basis':after, 'available':available['distinct_available_tasks'], 'hard_shortage':5}), flush=True)


def main():
    validation = json.loads((H / 'validation.json').read_text())
    assert validation['passed'] and validation['current_generator_sha256'] == sha(H.with_suffix('.py'))
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path / 'commit-intent.json').exists():
                intent = json.loads((path / 'commit-intent.json').read_text())
                assert intent['lineage'] == LINEAGE and intent['database'] == 'math' and intent['source'] == SOURCE
                assert intent['exact_edn'] == (path / 'transaction.edn').read_text() and intent['sha256'] == sha(path / 'transaction.edn')
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                verify(path, intent, DB._commit(intent, path / 'transaction.edn', path))
                return
        assert not JOB.with_suffix('.generated').exists(), 'Supplied instances must be validated before a changed plan'
        inv = inventory(OUT / 'inventory-under-lock.json')
        basis = inv['basis']
        assert DB.basis() == basis
        path = OUT / ('basis-' + str(basis))
        path.mkdir(exist_ok=True)
        record = kp(path, basis)
        atomic_text(path / 'before.edn', dumps(record) + '\n')
        source = json.loads((H / 'source.json').read_text())['record']
        for key in (':knowledge-point/id', ':knowledge-point/title', ':knowledge-point/questions', ':knowledge-point/canonical-example'):
            assert canonical(record[key]) == canonical(source[key]), 'Source evidence changed; classification needs refresh: ' + key
        available = counts(record, path, basis)
        assert all(n >= 5 for n in available['distinct_available_tasks'].values()), 'A supported shortage now needs generation'
        assert not [j for j in inv['jobs'] if j['knowledgePoint'] == KP and j['difficulty'] in g.SUPPORTED_LEVELS]
        contributor = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', basis)
        assert len(contributor) == 1
        orphan = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [uuid.UUID(g.GENERATOR_UUID)], path, 'generator-identity', basis)
        assert not orphan, 'Existing generator identity must be reconciled and reused'
        forms = registration_forms(record, g.GENERATOR_UUID)
        tx = dumps(forms) + '\n'
        txpath = path / 'transaction.edn'
        atomic_text(txpath, tx)
        atomic_json(path / 'generated.json', [])
        atomic_json(path / 'preparation.json', {'basis':basis, 'lineage':LINEAGE, 'source':SOURCE, 'available_counts':available, 'new_questions':0, 'reason':'No current supported shortage; hard unsupported', 'supplied_generated_file_exists':False, 'source_evidence_unchanged':True, 'generator_sha256':sha(H.with_suffix('.py'))})
        r = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, timeout=55, check=True)
        atomic_text(path / 'preview.edn', r.stdout)
        pr = loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == basis
        report_check(pr, path / 'preview-check', contributor[0][0])
        assert DB.basis() == basis
        intent = {'database':'math', 'lineage':LINEAGE, 'endpoint':DB.args.endpoint, 'basis':basis, 'expected_basis':basis, 'source':SOURCE, 'source_eid':contributor[0][0], 'request_key':'inventory-positive-scalar-' + str(KP) + '-' + str(basis) + '-' + sha(txpath), 'sha256':sha(txpath), 'exact_edn':tx, 'generator_id':g.GENERATOR_UUID, 'generator_path':SCRIPT, 'generator_sha256':sha(H.with_suffix('.py')), 'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock':str(LOCK)}
        atomic_json(path / 'commit-intent.json', intent)
        verify(path, intent, DB._commit(intent, txpath, path))


if __name__ == '__main__':
    main()

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
from image_library import ImageLibrary
from serve_graph_explorer import database_environment

spec = importlib.util.spec_from_file_location('cosine_validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.CAPTURE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '04d1cb99388489bb7190caad0744a0d29eab57dee7b55fe63aef4e264a274f92'
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

def endpoints(q):
    text = q[':question/problem'].split('have coordinates ')[1]
    pairs = re.findall(r'\((-?\d+),\s*(-?\d+)\)',text)
    assert len(pairs)==2
    return sorted(tuple(map(int, p)) for p in pairs)

def fingerprint(q):
    # Conservative deduplication: even different diameters of one circle coalesce.
    (x1,y1),(x2,y2)=endpoints(q)
    return g.digest([str(v.sp.Rational(x1+x2,2)),str(v.sp.Rational(y1+y2,2)),str(v.sp.Rational((x1-x2)**2+(y1-y2)**2,4))])

def check(rec):
    assert rec['knowledge_point']['db_id'] == KP
    v.displayed(rec)
    q=rec['question']; level=q[':question/difficulty'].split('/')[-1]
    assert level in LEVELS and q.get(':question/worked-solution')
    assert rec['generation']['eligible_for_learning']
    replay=g.generate(level, rec['generation']['seed'], rec['generation']['template'],
        parameters=rec['generation']['parameters'], profile=rec['generation']['bank_profile'])
    rq=copy.deepcopy(q)
    for local,relative in rec['generation'].get('asset_rewrites',{}).items():
        rq[':question/problem']=rq[':question/problem'].replace(relative,local)
    assert normalized(replay['question']) == normalized(rq)

def engine_item(rec,label):
    return v.engine_fixture(label,rec)

USAGE_QUERY = """[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

def available_counts(path,kp,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    available={l:[] for l in LEVELS};excluded=[];fixtures=[]
    canonical_id=kp[':knowledge-point/canonical-example'][':db/id']
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        reason=None
        if q[':db/id'] in unavailable:reason='Shown or reserved, including retained history'
        elif q[':db/id']==canonical_id:reason='Canonical example'
        elif level not in LEVELS:reason='Unrated'
        elif not q.get(':question/worked-solution'):reason='Missing solution'
        else:
            try:
                nq=normalized(q)
                r={'question':nq,'generation':{'dependencies':{'plot':{'reused_original':True}}}}
                v.displayed(r)
                fixtures.append(engine_item(r,str(q[':db/id'])))
            except (AssertionError,ValueError,KeyError,TypeError) as e:reason='Incomplete or invalid: '+str(e)
        if reason:excluded.append({'db_id':q[':db/id'],'reason':reason})
        else:available[level].append(q)
    save(path/'available-native-input.json',fixtures)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True)
    result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fingerprint(q) for q in qs}),
        'available_questions':len(qs),'question_ids':[str(q[':question/id']) for q in qs]} for l,qs in available.items()},
        'excluded_questions':excluded,'shown_or_reserved':sorted(unavailable)}
    save(path/'available-counts.json',result)
    return result

def publish(rec):
    library=ImageLibrary(Path(ENV['EDB_MATH_ROOT']))
    mapping={};assets=[]
    for asset in rec['generation']['plots']:
        local=Path(asset) if Path(asset).is_absolute() else library.math_root/asset
        digest=sha(local);relative=library.put_file(local,expected_sha256=digest)
        assert sha(library.math_root/relative)==digest
        mapping[asset]=relative;assets.append({'local':str(local),'relative':relative,'sha256':digest})
        rec['question'][':question/problem']=rec['question'][':question/problem'].replace(asset,relative)
    rec['generation']['asset_rewrites']=mapping
    rec['generation']['published_assets']=assets
    return rec

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
        assert fp == fingerprint(rec['question']) and fp not in previous and fp not in fps
        fps.add(fp)
        check(rec)
        for a in rec['generation']['published_assets']:
            assert sha(Path(ENV['EDB_MATH_ROOT'])/a['relative'])==a['sha256']
    counts=available_counts(path/'readback',kp,report[':edb/db-after-t'])
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': report[':edb/db-after-t'], 'new_questions': len(records), 'by_level': {level: sum(r['question'][':question/difficulty'] == ':question.difficulty/' + level for r in records) for level in LEVELS}, 'unchanged_source_questions': len(old), 'unchanged_canonical_example': True, 'only_additive_scoped_content_datoms': True, 'learner_history_unchanged': True, 'generator_registration_verified': True, 'distinct_from_sources_and_each_other': True, 'repeat_preparation_content_changes': 0, 'available_counts_after':counts}
    save(path / 'verification.json', result)
    return result

def finish(path, gid, verified, inv):
    prep = json.loads((path / 'preparation.json').read_text())
    exceptions = prep['capability_exceptions']
    result = {'outcome': 'finite-limit' if exceptions else 'generated', 'knowledgePoint': KP, 'generator_path': SCRIPT, 'generator_id': gid, 'lineage': LINEAGE, 'verified_commit_basis': verified['basis_after'], 'new_questions': verified['new_questions'], 'by_level': verified['by_level'], 'supported_levels': list(LEVELS), 'unsupported_levels': [], 'unsupported_levels_filled': False, 'capability_exceptions': exceptions, 'remaining_shortages': {l:max(0,5-verified['available_counts_after']['levels'][l]['distinct_available_tasks']) for l in LEVELS}, 'available_counts_after': verified['available_counts_after'], 'inventory_recheck_basis': inv['basis'], 'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP], 'evidence': [str(p.relative_to(ROOT)) for p in (path / 'verification.json', path / 'commit-intent.json', path / 'commit.edn', path / 'preview.edn', path / 'preparation.json', path / 'generated.json', path / 'native-report.json', path / 'inventory-after.json', HERE / 'validation.json', HERE / 'classification.md', HERE / 'template-extraction.md', HERE / 'domain-catalog.json')]}
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
    assert str(kp[':knowledge-point/id']) == g.KP[':knowledge-point/id']
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
    gid = str(gen[':question-generator/id']) if gen else identity.get('id', str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']), 'question-generator')))
    assert not identity or identity['id'] == gid
    save(identity_path, {'id': gid, 'script': SCRIPT, 'knowledge_point': KP})
    jobs = {j['difficulty']: j for j in inv['jobs'] if j['knowledgePoint'] == KP}
    counts=available_counts(path,kp,basis)
    needed={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
    used.add(fingerprint(kp[':knowledge-point/canonical-example']))
    records, selected = [], {level: 0 for level in LEVELS}
    def consider(rec):
        check(rec)
        assert rec['knowledge_point']['db_id'] == KP and rec['knowledge_point']['id'] == g.KP[':knowledge-point/id']
        level = rec['question'][':question/difficulty'].split('/')[-1]
        assert level in LEVELS
        fp = fingerprint(rec['question'])
        if selected[level] < needed[level] and fp not in used:
            records.append(publish(copy.deepcopy(rec)))
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
    exceptions = [{'level': level, 'requested': needed[level], 'produced': selected[level], 'shortage': remaining[level], 'bounded_seed_attempts': attempts[level], 'evidence': 'domain-catalog.json; complete-bank validation and exact circle exclusion'} for level in LEVELS if remaining[level]]
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
    save(path / 'native-input.json', [engine_item(r, r['question'][':question/id']) for r in instances + records])
    subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(path / 'native-input.json'), str(path / 'native-report.json')], check=True)
    save(path / 'review.json', records)
    (path / 'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records))
    save(path / 'preparation.json', {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': source[0][0], 'generator_id': gid, 'missing_by_level': needed, 'selected_by_level': selected, 'remaining_shortages': remaining, 'capability_exceptions': exceptions, 'bounded_seed_attempts': attempts, 'source_evidence_unchanged': True, 'available_counts_before':counts, 'asset_hashes': [a for r in records for a in r['generation']['published_assets']], 'inventory_count_evidence': jobs, 'distinctness': 'Exact center and squared radius independent of diameter orientation, level, seed, bank and order; excludes all existing practice/canonical circles', 'native_grader_sha256': sha(ROOT / 'generate/runs/current/check-engine')})
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
    if '--prepare-only' in sys.argv:
        print(json.dumps({'prepared_basis':basis,'new_by_level':selected,'remaining':remaining,'review':str(path/'review.md')}),flush=True)
        return
    intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': source[0][0], 'basis': basis, 'expected_basis': basis, 'request_key': 'diameter-circle-replenish-' + str(KP) + '-' + str(basis) + '-' + sha(txpath), 'transaction_sha256': sha(txpath), 'sha256': sha(txpath), 'exact_edn': tx, 'generator_id': gid, 'generator_path': SCRIPT, 'generator_sha256': sha(HERE.with_suffix('.py')), 'question_uuids': [r['question'][':question/id'] for r in records], 'connection_sha256': hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(LOCK)}
    save(path / 'commit-intent.json', intent)
    report = DB._commit(intent, txpath, path)
    verified = verify(path, intent, report)
    finish(path, gid, verified, inventory(path / 'inventory-after.json'))

def main():
    validation = json.loads((HERE / 'validation.json').read_text())
    assert validation['status'] == 'pass'
    frozen = json.loads((HERE/'freeze.json').read_text())['hashes']
    for name,digest in frozen.items():
        assert sha(ROOT/name)==digest, 'Frozen artifact changed: '+name
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

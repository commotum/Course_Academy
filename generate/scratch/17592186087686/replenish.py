"""Scoped additive replenishment with retained requests and exact-basis readback."""
import copy
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
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '8c1d4812108d3a9c58833aea2ded10caf4c76ca8cc847edf7d2966f6337c1cf3'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = max((p for p in (ROOT / '.local/graph-explorer').glob('learning-*') if p.is_file() and os.access(p, os.X_OK) and 'tests' not in p.name), key=lambda p: p.stat().st_mtime)
QUERY = (HERE / 'reference/source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def validate_instance(rec):
    assert rec['question'][':question/difficulty']==':question.difficulty/easy'
    v.structural(rec)
    metadata=rec['generation']
    replay=g.generate('easy',seed=metadata['seed'],template=metadata['template'],parameters=metadata['parameters'],profile=metadata['bank_profile'])
    assert ordered(rec['question'])==ordered(replay['question']), 'Generated instance must replay exactly'
    assert rec['generation']==replay['generation']

USAGE_QUERY = """[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

def available_counts(path,kp,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    available=[]
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        if str(q.get(':question/difficulty',{}).get(':db/ident'))!=':question.difficulty/easy':continue
        if not q.get(':question/worked-solution') or not q.get(':question/answer-fields'):continue
        fields=q[':question/answer-fields']
        if not all(':answer-field/correct' in f and f.get(':answer-field/choices') and f[':answer-field/correct'][':answer/id'] in {a[':answer/id'] for a in f[':answer-field/choices']} for f in fields):continue
        available.append(q)
    counts={'basis':basis,'rated_gradable_unseen_unreserved_easy_questions':len(available),'distinct_available_easy_tasks':len({fingerprint(q) for q in available}),'excluded_shown_or_reserved':sorted(unavailable),'available_question_ids':[str(q[':question/id']) for q in available],'available_slopes':sorted({str(v.parse(q)[0]) for q in available})}
    save(path/'available-counts.json',counts)
    return counts

def fingerprint(q):
    return g.digest({'slope':str(v.parse(q)[0])})

def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x, sort_keys=True))
    if isinstance(value, uuid.UUID): return str(value)
    return value

def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path/'receipt-check', intent['source_eid'])
    kp = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')} == {k:v for k,v in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q) == ordered(rec['question'])
        assert fingerprint(q) == rec['generation']['parameter_fingerprint']
        validate_instance(rec)
    assert not transaction([], kp, intent['generator_id'])
    counts=available_counts(path/'readback',kp,report[':edb/db-after-t'])
    assert counts['distinct_available_easy_tasks']>=min(5, json.loads((path/'preparation.json').read_text())['available_counts']['distinct_available_easy_tasks']+len(records))
    result = {'available_counts_after':counts,'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def finish(path, gid, verified, inv):
    exceptions = [{'level':level, 'supported':False, 'available':0, 'nominal_quota':5, 'shortage':5, 'reason':json.loads((HERE/'capabilities.json').read_text())['reason'], 'evidence':[str((HERE/name).relative_to(ROOT)) for name in ('classification.md','template-extraction.md','capabilities.json')]} for level in ('moderate','hard')]
    preparation = json.loads((path/'preparation.json').read_text())
    remaining = preparation['easy_missing'] - verified['new_questions']
    result = {'outcome':'finite-limit' if remaining else 'generated', 'knowledgePoint':KP, 'generator_path':SCRIPT, 'generator_id':gid, 'lineage':LINEAGE, 'verified_commit_basis':verified['basis_after'], 'new_questions':verified['new_questions'], 'available_counts_before':preparation.get('available_counts'), 'supported_levels':['easy'], 'capability_exceptions':exceptions, 'finite_variant_limit':g.DOMAIN['distinct_tasks'], 'easy_shortage_remaining':remaining, 'unsupported_levels_filled':False, 'inventory_recheck_basis':inv['basis'], 'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP], 'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json', path/'commit-intent.json', path/'transaction.edn', path/'commit.edn', path/'preview.edn', path/'preparation.json', path/'inventory-after.json', HERE/'validation.json', HERE/'capabilities.json')], 'note':'Easy direct-slope generator validated and registered. Five distinct available slopes are required; moderate/hard remain unsupported bounded exceptions with nominal shortages five each. All original incomplete/unrated source records and learner history are preserved.'}
    save(path/'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','remaining_jobs')}), flush=True)

def main():
    validation = json.loads((HERE/'validation.json').read_text())
    assert validation['status']=='pass' and validation['hashes'][SCRIPT] == sha(HERE.with_suffix('.py'))
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent = json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage'] == LINEAGE and intent['source'] == SOURCE and intent['transaction_sha256'] == sha(path/'transaction.edn')
                assert intent['exact_edn'] == (path/'transaction.edn').read_text()
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report = DB._commit(intent, path/'transaction.edn', path)
                verified = verify(path, intent, report)
                finish(path, intent['generator_id'], verified, inventory(path/'inventory-after.json'))
                return
        inv = inventory(OUT/'inventory-before.json')
        b = inv['basis']
        assert DB.basis() == b
        path = OUT / ('basis-'+str(b))
        path.mkdir(exist_ok=True)
        kp = read_kp(path, b)
        assert str(kp[':knowledge-point/id']) == g.KP_UUID
        caps=json.loads((HERE/'capabilities.json').read_text());caps['current_recheck_basis']=b;save(HERE/'capabilities.json',caps)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured = json.loads((HERE/'source.json').read_text())['record']
        expected = {q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']}
        current = {q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        assert set(expected) <= set(current)
        for mid, q in expected.items():
            assert canonical(current[mid]) == canonical(q), 'Source evidence changed; reclassify '+mid
        assert canonical(captured[':knowledge-point/canonical-example']) == canonical(kp[':knowledge-point/canonical-example'])
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', b)
        assert len(source) == 1
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        jobs = {j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint'] == KP}
        counts=available_counts(path,kp,b)
        needed=max(jobs.get('easy',{}).get('missing',0),5-counts['distinct_available_easy_tasks'])
        used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
        example=kp[':knowledge-point/canonical-example'][':question/problem']
        import re
        known=re.findall(r'\$y=([0-9-]+)x[+-][0-9]+\$', example)
        assert len(known)==1, 'Canonical example slope parsing must be reviewed'
        used.add(g.digest({'slope':str(v.math(known[0]))}))
        records = []
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances', [])
        assert isinstance(instances, list)
        rejected = []
        eligible = []
        for rec in instances:
            if rec['question'][':question/difficulty'] != ':question.difficulty/easy':
                rejected.append({'question_id':rec['question'][':question/id'],'reason':'Unsupported difficulty; not committed'})
                continue
            validate_instance(rec)
            eligible.append(rec)
        save(path/'supplied-status.json', {'exists':supplied_path.exists(), 'instances_validated':len(instances), 'unsupported_rejected':rejected, 'generator_error':supplied.get('generatorError')})
        # Execute five or more distinct slopes. Review samples remain local if quota is full.
        local = g.batch('easy',min(g.DOMAIN['distinct_tasks'],max(15,needed+len(used))),2350817554,field_type='blank')
        for rec in eligible+local:
            validate_instance(rec)
            fp = fingerprint(rec['question'])
            if len(records) < needed and fp not in used:
                records.append(rec); used.add(fp)
        save(path/'local-preview.json', local)
        save(path/'generated.json', records)
        native = [{'label':r['question'][':question/id'], 'record':r, 'checks':v.checks(r)} for r in local+eligible]
        save(path/'native-input.json', native)
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'), str(path/'native-input.json'), str(path/'native-report.json')], check=True)
        native_report=json.loads((path/'native-report.json').read_text())
        assert native_report['documented_unresolved_checks']==0
        save(path/'preparation.json', {'basis':b, 'lineage':LINEAGE, 'source':SOURCE, 'generator_id':gid, 'easy_missing':needed, 'local_previews':len(local), 'new_questions':len(records), 'source_evidence_unchanged':True, 'asset_hashes':[], 'finite_variant_limit':g.DOMAIN['distinct_tasks'], 'used_tasks_before':len({fingerprint(q) for q in kp[':knowledge-point/questions']}), 'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}), 'available_counts':counts,'inventory_count_evidence':'Native inventory plus distinct-slope count at the same basis'})
        forms = transaction(records, kp, gid)
        if not forms:
            save(path/'verification.json', {'passed':True, 'basis_before':b, 'basis_after':b, 'new_questions':0, 'no_changes':True, 'generator_registration_verified':True})
            finish(path, gid, json.loads((path/'verification.json').read_text()), inv)
            return
        txpath = path/'transaction.edn'
        tx = dumps(forms)+'\n'
        with txpath.open('w') as f:
            f.write(tx); f.flush(); os.fsync(f.fileno())
        r = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, check=True, timeout=90)
        (path/'preview.edn').write_text(r.stdout)
        pr = loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == b
        check_report(pr, path/'preview-check', source[0][0])
        assert DB.basis() == b
        intent = {'database':'math', 'endpoint':DB.args.endpoint, 'lineage':LINEAGE, 'source':SOURCE, 'source_eid':source[0][0], 'basis':b, 'expected_basis':b, 'request_key':'parallel-slope-register-'+str(b)+'-'+sha(txpath), 'transaction_sha256':sha(txpath), 'sha256':sha(txpath), 'exact_edn':tx, 'generator_id':gid, 'generator_path':SCRIPT, 'generator_sha256':sha(HERE.with_suffix('.py')), 'question_uuids':[rec['question'][':question/id'] for rec in records], 'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        verified = verify(path, intent, report)
        finish(path, gid, verified, inventory(path/'inventory-after.json'))

if __name__ == '__main__':
    main()

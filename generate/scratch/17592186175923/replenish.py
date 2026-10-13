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
from serve_graph_explorer import database_environment, build_learning
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'cfe5ce9c11de6cbf0b61887546566c8fd20a64ac2955bf06aac627da8e8ffa1b'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = build_learning(ROOT.parent / 'EDB')
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
    assert rec['question'][':question/difficulty'].split('/')[-1] in g.SUPPORTED_LEVELS
    v.independent(rec)
    metadata=rec['generation']
    replay=g.generate(rec['question'][':question/difficulty'].split('/')[-1],seed=metadata['seed'],template=metadata['template'],parameters=metadata['parameters'],profile=metadata['bank_profile'])
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
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    available={level:[] for level in g.SUPPORTED_LEVELS}; rejected=[]; native=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example') or level not in available:continue
        fields=q.get(':question/answer-fields',[])
        if len(fields)!=1 or not q.get(':question/worked-solution') or not all(':answer-field/correct' in f and f.get(':answer-field/choices') and f[':answer-field/correct'][':answer/id'] in {a[':answer/id'] for a in f[':answer-field/choices']} for f in fields):
            rejected.append({'id':str(q[':question/id']),'reason':'Incomplete solution or fields'});continue
        try:v.solution_check(q)
        except (AssertionError,ValueError,KeyError,IndexError) as error:
            rejected.append({'id':str(q[':question/id']),'reason':str(error)});continue
        rec={'knowledge_point':{'title':g.TITLE},'question':normalize(q),'generation':{'template':'existing-source'}}
        f=rec['question'][':question/answer-fields'][0]
        if f[':answer-field/type'].endswith('/radio'):
            checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Existing source complete bank ID grading'} for a in f[':answer-field/choices']]
        else:checks=v.checks(rec)
        native.append({'label':str(q[':question/id']),'record':rec,'checks':checks})
        available[level].append(q)
    save(path/'existing-native-input.json',native)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'existing-native-input.json'),str(path/'existing-native-report.json')],check=True)
    assert json.loads((path/'existing-native-report.json').read_text())['documented_unresolved_checks']==0
    counts={'basis':basis,'distinct_available':{level:len({fingerprint(q) for q in qs}) for level,qs in available.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded_invalid':rejected,'available_question_ids':{level:[str(q[':question/id']) for q in qs] for level,qs in available.items()}}
    save(path/'available-counts.json',counts)
    return counts

def fingerprint(q):
    try:return v.fingerprint(q[':question/problem'])
    except ValueError:
        # Missing diagram still has a retained known answer line; do not generate its clone.
        f=q.get(':question/answer-fields',[{}])[0]
        correct=f.get(':answer-field/correct',{}).get(':answer/value')
        if correct:
            rhs=v.scalar(correct.split('=')[-1]);m=rhs.coeff(v.reader.x);b=rhs.subs(v.reader.x,0)
            return g.digest({'slope':str(m),'intercept':str(b)})
        raise

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
    assert all(counts['distinct_available'][level]>=5 for level in g.SUPPORTED_LEVELS)
    result = {'available_counts_after':counts,'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def finish(path, gid, verified, inv):
    exceptions=json.loads((HERE/'capabilities.json').read_text())['exceptions']
    prep=json.loads((path/'preparation.json').read_text())
    after=verified.get('available_counts_after',prep['available_counts'])['distinct_available']
    shortages={level:max(0,5-after[level]) for level in g.SUPPORTED_LEVELS}
    result={'outcome':'finite-limit' if any(shortages.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':prep['new_questions_by_level'],'supported_levels':list(g.SUPPORTED_LEVELS),'supported_shortages':shortages,'capability_exceptions':exceptions,'unsupported_levels_filled':False,'hard_shortage':5,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'choice-ledger.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'capabilities.json') if p.exists()],'note':'Easy and moderate validated and registered. Original incomplete/unrated/diagram questions remain preserved and excluded from available inventory. Unsupported radio generator families and hard remain explicit bounded exceptions.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','new_questions_by_level','remaining_jobs')}),flush=True)

def main():
    validation = json.loads((HERE/'validation.json').read_text())
    assert validation['status']=='pass' and all(sha(ROOT/name)==value for name,value in validation['hashes'].items())
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
        needed={level:max(jobs.get(level,{}).get('missing',0),5-counts['distinct_available'][level],0) for level in g.SUPPORTED_LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);assert isinstance(instances,list)
        rejected=[];eligible=[]
        for rec in instances:
            if rec['question'][':question/difficulty'].split('/')[-1] not in g.SUPPORTED_LEVELS:
                rejected.append({'question_id':rec['question'][':question/id'],'reason':'Unsupported difficulty; not committed'});continue
            validate_instance(rec);eligible.append(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(eligible),'unsupported_rejected':rejected,'generator_error':supplied.get('generatorError')})
        local=[r for level in g.SUPPORTED_LEVELS for r in g.batch(level,min(100,max(15,needed[level]+len(used))),1945)]
        records=[];by_level={level:0 for level in g.SUPPORTED_LEVELS}
        for rec in eligible+local:
            validate_instance(rec);level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if by_level[level]<needed[level] and fp not in used:
                records.append(rec);used.add(fp);by_level[level]+=1
        save(path/'local-preview.json',local);save(path/'generated.json',records)
        native=[{'label':r['question'][':question/id'],'record':r,'checks':v.checks(r)} for r in local+eligible]
        save(path/'native-input.json',native)
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
        # Batch all generated identities against the same basis; no collisions may overwrite source records.
        identities={attr:[] for attr in ('question/id','answer-field/id','answer/id')}
        for rec in records:
            q=rec['question'];identities['question/id'].append(uuid.UUID(q[':question/id']))
            for f in q[':question/answer-fields']:
                identities['answer-field/id'].append(uuid.UUID(f[':answer-field/id']))
                identities['answer/id'].extend(uuid.UUID(a[':answer/id']) for a in f[':answer-field/choices'])
        for attr,values in identities.items():
            if values:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[values],path,'identity-'+attr.split('/')[0],b),'Identity collision requires preparation reconciliation'
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing':needed,'local_previews':len(local),'new_questions':len(records),'new_questions_by_level':by_level,'source_evidence_unchanged':True,'asset_hashes':[],'available_counts':counts,'inventory_count_evidence':'Native inventory plus scoped validated distinct-line count at same captured basis','task_fingerprint':'Exact reduced target slope and intercept','bounded_attempts':2000})
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
        intent = {'database':'math', 'endpoint':DB.args.endpoint, 'lineage':LINEAGE, 'source':SOURCE, 'source_eid':source[0][0], 'basis':b, 'expected_basis':b, 'request_key':'perpendicular-point-line-register-17592186175923-'+str(b)+'-'+sha(txpath), 'transaction_sha256':sha(txpath), 'sha256':sha(txpath), 'exact_edn':tx, 'generator_id':gid, 'generator_path':SCRIPT, 'generator_sha256':sha(HERE.with_suffix('.py')), 'question_uuids':[rec['question'][':question/id'] for rec in records], 'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        verified = verify(path, intent, report)
        finish(path, gid, verified, inventory(path/'inventory-after.json'))

if __name__ == '__main__':
    main()

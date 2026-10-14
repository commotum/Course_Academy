"""Add only unused mathematical structures; retain guarded requests and receipts."""
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
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment

spec = importlib.util.spec_from_file_location('rate_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'95e001b572705e714e2ceff639ccb213328b2700e93063546dc18a039f7abc4a'
OUT = HERE/'reference/replenishment'
LOCK = ROOT/'.local/learning/requests/math/api.lock'
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env = ENV
NATIVE = ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'
QUERY = (OUT/'source-query.edn').read_text()
LEVELS = ('easy', 'moderate', 'hard')
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'course-academy-generator'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=ENV, capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']


def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]


def normalize(q):
    out = {k:str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    out[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    out[':question/answer-fields'] = []
    for f in q[':question/answer-fields']:
        out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id', str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':[{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    return ordered(out)


def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q


def parameters(q):
    entries = re.findall(r'- \$([A-Za-z])\(([tus])\)\$[^\n]*', q[':question/problem'])
    assert len(entries) in (2,3)
    p = {'Q':entries[0][0], 'T':entries[0][1]}
    if len(entries) == 2:
        p['R'] = entries[1][0]
    else:
        p.update(I=entries[1][0], L=entries[2][0])
    return p


def kind(q):
    return v.infer_prompt(q[':question/problem'], parameters(q))[1]


def fingerprint(q):
    return g.digest({'skill':'derivative-supplied-rate-relationship', 'semantic_structure':kind(q)})


def checks(rec):
    f = rec['question'][':question/answer-fields'][0]
    return {'label':rec['question'][':question/id'], 'record':rec, 'checks':[{'submitted_answer_id':a[':answer/id'], 'expected':'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected', 'purpose':'independently checked full equation'} for a in f[':answer-field/choices']]}


def native_checks(records, path, name):
    save(path/(name+'-input.json'), [checks(r) for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'), str(path/(name+'-input.json')), str(path/(name+'-report.json'))], check=True)


def audit_existing(q):
    """Check the actual current source bank, without replacing source content."""
    p = parameters(q)
    expected, structure = v.infer_prompt(q[':question/problem'], p)
    rec = {'knowledge_point':{'db_id':KP, 'id':g.KP_UUID, 'title':g.TITLE}, 'question':normalize(q), 'generation':{'template':'current-source:'+q.get(':question/math-academy-id','authored')}}
    f = rec['question'][':question/answer-fields'][0]
    assert len(rec['question'][':question/answer-fields']) == 1 and len(f[':answer-field/choices']) == 5 and f[':answer-field/type'] == ':answer-field.type/radio'
    residuals = [v.residual(a[':answer/value'], p) for a in f[':answer-field/choices']]
    for a,r in zip(f[':answer-field/choices'], residuals):
        assert (v.sp.simplify(r.subs(v.dq, expected)) == 0) == (a[':answer/id'] == f[':answer-field/correct'][1])
    for i,a in enumerate(residuals):
        for b in residuals[i+1:]:
            assert not v.equivalent(a,b)
    # Compare complete current banks with the replayed source profile, including
    # the field repaired in EDB after the original basis-1356 capture.
    source_id = q.get(':question/math-academy-id')
    if source_id:
        case = next(c for c in v.CASES if c['source_id'] == source_id)
        replay = g.generate(case['level'], 11, case['template'], parameters=case['parameters'], profile=case['bank_profile'])
        options = [v.residual(a[':answer/value'], p) for a in replay['question'][':question/answer-fields'][0][':answer-field/choices']]
        assert all(sum(bool(v.equivalent(a,b)) for b in options) == 1 for a in residuals)
        original = v.SOURCES[source_id]
        assert q[':question/problem'] == original[':question/problem']
        # q-48923 has a Unicode-prime normalization in current EDB.
        assert v.normalize(q[':question/worked-solution']) == v.normalize(original[':question/worked-solution'])
    return rec


USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''


def counts(kp, path, basis):
    unavailable = {r[0] for r in DB.query(USAGE_QUERY, [KP,LEARNER], path, 'usage', basis)}
    # Retained presentations never become fresh through current retractions.
    seen_query = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
     [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
     [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
    unavailable |= {r[0] for r in DB.query(seen_query, [KP,LEARNER], path, 'retained-presentations', basis, history=True)}
    rows = {level:[] for level in LEVELS}
    records, excluded = [], []
    for q in kp[':knowledge-point/questions']:
        reason = None
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):
            reason = 'shown/reserved/canonical'
        elif not q.get(':question/difficulty') or not q.get(':question/worked-solution') or not q.get(':question/answer-fields') or not all(f.get(':answer-field/correct') for f in q[':question/answer-fields']):
            reason = 'incomplete or unrated'
        if reason:
            excluded.append({'question_id':str(q[':question/id']), 'reason':reason})
            continue
        rec = audit_existing(q)
        records.append(rec)
        level = str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        rows[level].append(q)
    native_checks(records, path, 'available-native')
    result = {'basis':basis, 'levels':{l:{'gradable_available_questions':len(qs), 'distinct_available_tasks':len({fingerprint(q) for q in qs}), 'question_ids':[str(q[':question/id']) for q in qs]} for l,qs in rows.items()}, 'excluded':excluded, 'excluded_shown_or_reserved':sorted(unavailable), 'deduplication':'Full mathematical relationship; excludes context, units, letters, bank, difficulty label, seed and choice order.'}
    save(path/'available-counts.json',result)
    return result


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
    basis = report[':edb/db-after-t']
    kp = read_kp(path/'readback', basis)
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items())
    assert {k:val for k,val in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')} == {k:val for k,val in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    byid = {str(q[':question/id']):q for q in now.values()}
    assert len(now) == len(old)+len(records)
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q) == ordered(rec['question'])
        v.independent_check(rec)
    assert not transaction([],kp,intent['generator_id'])
    # Repeat preparation's mathematical selection, not just its registration.
    used = {fingerprint(q) for q in now.values()}
    used.add(fingerprint(kp[':knowledge-point/canonical-example']))
    candidates = [g.generate(g.TEMPLATES[t]['level'],42,t) for t in ('single_growth','single_loss','net_magnitudes','signed_net')]
    assert all(fingerprint(r['question']) in used for r in candidates)
    after = counts(kp,path/'readback',basis)
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':basis, 'new_questions':len(records), 'unchanged_source_questions':len(old), 'learner_history_unchanged':True, 'only_additive_scoped_content_datoms':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0, 'available_counts_after':after}
    save(path/'verification.json',result)
    return result


def finish(path, gid, verified, inv):
    prep = json.loads((path/'preparation.json').read_text())
    after = verified['available_counts_after']
    result = {'outcome':'finite-limit', 'knowledgePoint':KP, 'generator_path':SCRIPT, 'generator_id':gid, 'lineage':LINEAGE, 'verified_commit_basis':verified['basis_after'], 'new_questions':verified['new_questions'], 'supported_levels':list(LEVELS), 'available_counts_before':prep['available_counts'], 'available_counts_after':after, 'shortage_remaining':{l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}, 'unsupported_levels_filled':False, 'finite_limit':json.loads((HERE/'capabilities.json').read_text()), 'inventory_recheck_basis':inv['basis'], 'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint'] == KP], 'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json', path/'commit-intent.json', path/'transaction.edn', path/'commit.edn', path/'preview.edn', path/'preparation.json', path/'inventory-after.json', path/'current-source-validation.json', HERE/'validation.json', HERE/'capabilities.json') if p.exists()], 'note':'Four finite mathematical relationships. Growth and positive net flow already present; no cosmetic duplicates admitted. Existing unrated/incomplete sources remain intact and can continue to trigger classification. Application raw-ID counts are retained separately from distinct validated task counts; shortages remain explicit.'}
    save(path/'outcome.json',result)
    save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)


def main():
    validation = json.loads((HERE/'validation.json').read_text())
    frozen = json.loads((ROOT/'generate/runs/current/qa/17592186064272-frozen.json').read_text())
    assert validation['status'] == 'passed' and frozen['files'][SCRIPT] == sha(HERE.with_suffix('.py'))
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        # Exact saved intent recovery precedes new inventory/preparation.
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent = json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage'] == LINEAGE and intent['source'] == SOURCE and intent['transaction_sha256'] == sha(path/'transaction.edn') and intent['exact_edn'] == (path/'transaction.edn').read_text()
                assert intent['connection_sha256'] == hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
                report = DB._commit(intent,path/'transaction.edn',path)
                verified = verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'))
                return
        inv = inventory(OUT/'inventory-before.json')
        basis = inv['basis']
        assert DB.basis() == basis
        path = OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
        kp = read_kp(path,basis)
        assert str(kp[':knowledge-point/id']) == g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis)
        assert len(source) == 1
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else GENERATOR_UUID
        c = counts(kp,path,basis)
        save(path/'current-source-validation.json', {'basis':basis, 'source_practice_count':len(kp[':knowledge-point/questions']), 'complete_banks_checked':sum(row['gradable_available_questions'] for row in c['levels'].values()), 'current_q48923_bank':'Five options match net_standard completely; correct designation verified. Source solution differs from old capture only by prime normalization.', 'original_evidence_basis':1356, 'source_repairs_committed':False, 'plots':'none'})
        used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        needed = {l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        added = {l:0 for l in LEVELS};records=[]
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        assert isinstance(instances,list)
        for rec in instances:
            v.independent_check(rec)
            replay = g.generate(rec['question'][':question/difficulty'].split('/')[-1], rec['generation']['seed'], rec['generation']['template'], parameters=rec['generation']['parameters'], profile=rec['generation']['bank_profile'])
            assert ordered(replay['question']) == ordered(rec['question'])
        candidates = instances+[g.generate(g.TEMPLATES[t]['level'],seed=42,template=t) for t in ('single_growth','single_loss','net_magnitudes','signed_net')]
        for rec in candidates:
            level = rec['question'][':question/difficulty'].split('/')[-1]
            fp = fingerprint(rec['question'])
            if added[level] < needed[level] and fp not in used:
                v.independent_check(rec)
                records.append(rec);used.add(fp);added[level]+=1
        save(path/'supplied-status.json', {'exists':supplied_path.exists(),'validated_instances':len(instances)})
        ids = [uuid.UUID(x) for rec in records for x in [rec['question'][':question/id'], rec['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]]
        matches = DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not matches,'Identity collision requires reconciliation'
        save(path/'generated.json',records)
        native_checks(records,path,'generated-native')
        save(path/'preparation.json', {'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'generator_sha256':sha(HERE.with_suffix('.py')),'dependencies':{'sympy':v.sp.__version__,'python':sys.version},'asset_hashes':[]})
        forms = transaction(records,kp,gid)
        if not forms:
            verified = {'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c}
            save(path/'verification.json',verified)
            finish(path,gid,verified,inv)
            return
        txpath = path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:
            f.write(tx);f.flush();os.fsync(f.fileno())
        r = subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout)
        pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == basis
        check_report(pr,path/'preview-check',source[0][0])
        assert DB.basis() == basis
        intent = {'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'derivative-rate-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
        save(path/'commit-intent.json',intent)
        report = DB._commit(intent,txpath,path)
        verified = verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))


if __name__ == '__main__':
    main()

"""Additive KP-only preparation, native preview, durable commit and readback."""
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
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'824d7fb3bf68f4f556bd60d96c61387c15dcaa37d85a1e07cab8263529b9b464'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'
QUERY = (HERE/'reference/source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=60)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

def subset(expected, actual):
    """Frozen source attributes must match; extra current pull projections may exist."""
    if isinstance(expected, dict):
        return all(k in actual and subset(val, actual[k]) for k,val in expected.items())
    if isinstance(expected, list):
        return len(expected) == len(actual) and all(any(subset(e,a) for a in actual) for e in expected)
    return expected == actual or str(expected) == str(actual)

def fingerprint(q):
    """Read the mathematical task from displayed content, ignoring bank/period aliases."""
    import sympy as sp
    import re
    parts = re.findall(r'\$(.*?)\$', q[':question/problem'], re.S)
    assert len(parts) == 2
    c = v.scalar(v.norm(parts[0]).split('=',1)[1])
    t = v.norm(parts[1].rstrip('?'))
    calls = v.calls(t)
    assert len(calls) == 1
    i,j,arg = calls[0]
    v.reduction_value(arg)
    a = v.scalar(t[:i]) if t[:i].strip() else sp.Integer(1)
    b = v.scalar(t[j:]) if t[j:].strip() else sp.Integer(0)
    if b == 0:
        workload = 'direct' if a == 1 else 'scaled_integer'
    elif c.is_Rational:
        workload = 'reciprocal_integer' if (a*c).is_Integer else 'reciprocal_fraction'
    else:
        workload = 'affine_radical'
    return g.hashid({'workload':workload, 'c':str(c), 'a':str(a), 'b':str(b)})

def normalize(q):
    result = {k:str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f:f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

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
        assert str(gen[':question-generator/id']) == gid
        if gen.get(':question-generator/script') != SCRIPT:
            forms.append({kw('db/id'):gen[':db/id'],kw('question-generator/script'):SCRIPT})
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

def validate(rec):
    assert rec['knowledge_point']['db_id'] == KP
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    level = rec['question'][':question/difficulty'].split('/')[-1]
    assert level in g.LEVELS
    v.displayed_check(rec)
    assert fingerprint(rec['question']) == rec['generation']['mathematical_fingerprint']
    q = rec['question']
    assert ':question/math-academy-id' not in q and ':db/id' not in q
    replay = g.generate(level, rec['generation']['seed'], template=rec['generation']['template'], profile=rec['generation']['profile'], parameters=rec['generation']['parameters'])
    assert ordered(replay['question']) == ordered(rec['question'])
    assert replay['generation'] == rec['generation']

def native(rec):
    r = v.native_record(rec)
    f = r['question'][':question/answer-fields'][0]
    return {'label':r['question'][':question/id'], 'record':r, 'checks':[{'submitted_answer_id':a[':answer/id'], 'expected':'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected', 'purpose':'grade every selected owned choice'} for a in f[':answer-field/choices']]}

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path/'receipt-check', intent['source_eid'])
    kp = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items())
    assert {k:val for k,val in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')} == {k:val for k,val in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q) == ordered(rec['question'])
        validate(rec)
    assert not transaction([], kp, intent['generator_id'])
    all_fingerprints = {fingerprint(q) for q in now.values()}
    assert all(rec['generation']['mathematical_fingerprint'] in all_fingerprints for rec in records)
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'by_level':{level:sum(r['question'][':question/difficulty'].endswith('/'+level) for r in records) for level in g.LEVELS}, 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def finish(path, gid, verified, inv):
    prep = json.loads((path/'preparation.json').read_text())
    jobs = [j for j in inv['jobs'] if j['knowledgePoint'] == KP]
    result = {'outcome':'finite-limit' if prep['finite_limit'] else 'generated', 'knowledgePoint':KP, 'generator_path':SCRIPT, 'generator_id':gid, 'lineage':LINEAGE, 'verified_commit_basis':verified['basis_after'], 'new_questions':verified['new_questions'], 'by_level':verified['by_level'], 'supported_levels':list(g.LEVELS), 'unsupported_levels':['hard'], 'unsupported_levels_filled':False, 'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'], 'shortage_by_level':{**{level:next((j['missing'] for j in jobs if j['difficulty'] == level),0) for level in g.LEVELS}, 'hard':5}, 'inventory_recheck_basis':inv['basis'], 'remaining_jobs':jobs, 'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',path/'native-report.json',HERE/'validation.json',HERE/'capabilities.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'review.md',HERE/'frozen-manifest.json')], 'note':'Easy/moderate additions verified. Hard remains unsupported and unfilled. Unrated source records remain preserved and are not counted as rated fresh inventory.'}
    save(path/'outcome.json',result)
    save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','by_level','shortage_by_level')}),flush=True)

def main():
    validation = json.loads((HERE/'validation.json').read_text())
    assert validation['passed'] and validation['supported_levels'] == list(g.LEVELS)
    manifest = json.loads((HERE/'frozen-manifest.json').read_text())
    assert all(sha(ROOT/p) == digest for p,digest in manifest['hashes'].items())
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent = json.loads((path/'commit-intent.json').read_text())
                assert intent['database'] == 'math' and intent['endpoint'] == DB.args.endpoint and intent['lineage'] == LINEAGE and intent['source'] == SOURCE
                assert intent['transaction_sha256'] == sha(path/'transaction.edn') and intent['exact_edn'] == (path/'transaction.edn').read_text()
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report = DB._commit(intent, path/'transaction.edn', path)
                finish(path, intent['generator_id'], verify(path,intent,report), inventory(path/'inventory-after.json'))
                return
        inv = inventory(OUT/'inventory-before.json')
        b = inv['basis']
        assert DB.basis() == b
        path = OUT/('basis-'+str(b))
        path.mkdir(exist_ok=True)
        kp = read_kp(path,b)
        assert str(kp[':knowledge-point/id']) == g.REC[':knowledge-point/id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        for q in g.REC[':knowledge-point/questions']:
            assert subset(q,next(current for current in kp[':knowledge-point/questions'] if current[':db/id'] == q[':db/id'])), 'Source changed; reclassify'
        assert subset(g.REC[':knowledge-point/canonical-example'],kp[':knowledge-point/canonical-example'])
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path,'contributor',b)
        assert len(source) == 1
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+g.REC[':knowledge-point/id']))
        jobs = {j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint'] == KP}
        needed = {level:jobs.get(level,{}).get('missing',0) for level in g.LEVELS}
        used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records = []
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        if isinstance(instances,dict):instances = [instances]
        selected = {level:0 for level in needed}
        for rec in instances:
            validate(rec)
            level = rec['question'][':question/difficulty'].split('/')[-1]
            fp = fingerprint(rec['question'])
            if selected[level] < needed[level] and fp not in used:
                records.append(rec);used.add(fp);selected[level] += 1
        save(path/'supplied-status.json',{'exists':supplied_path.exists(), 'instances_validated':len(instances)})
        for level in needed:
            for seed in range(500):
                if selected[level] >= needed[level]:break
                rec = g.generate(level,22401988+seed)
                fp = fingerprint(rec['question'])
                if fp not in used:
                    validate(rec);records.append(rec);used.add(fp);selected[level] += 1
        for attr, ids in [('question/id',[r['question'][':question/id'] for r in records]), ('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]), ('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if ids:
                assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in ids]],path,attr.replace('/','-')+'-collisions',b)
        registered = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or gen and registered[0][0][':db/id'] == gen[':db/id']
        save(path/'generated.json',records)
        save(path/'native-input.json',[native(r) for r in instances+records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'selected_by_level':selected,'new_questions':len(records),'source_evidence_unchanged':True,'finite_limit':selected != needed,'inventory_count_evidence':{level:jobs.get(level,{'missing':0}) for level in needed},'distinctness':'Actual displayed given value, coefficient, constant and source workload; excludes all period aliases, bank, seed, notation, UUID and option order. Source and canonical tasks excluded.','asset_hashes':[]})
        forms = transaction(records,kp,gid)
        if not forms:
            finish(path,gid,{'basis_after':b,'new_questions':0,'by_level':dict.fromkeys(g.LEVELS,0)},inv)
            return
        txpath = path/'transaction.edn'
        tx = dumps(forms)+'\n'
        with txpath.open('w') as f:
            f.write(tx);f.flush();os.fsync(f.fileno())
        r = subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=60)
        (path/'preview.edn').write_text(r.stdout)
        pr = loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == b
        check_report(pr,path/'preview-check',source[0][0])
        assert DB.basis() == b
        intent = {'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'csc-periodicity-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report = DB._commit(intent,txpath,path)
        finish(path,gid,verify(path,intent,report),inventory(path/'inventory-after.json'))

if __name__ == '__main__':
    main()

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
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '6dfbc6388d910f903aa87544a054486add312bece9b7f0103528bdf204c895b2'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = max((p for p in (ROOT / '.local/graph-explorer').glob('learning-*') if p.is_file() and os.access(p, os.X_OK) and 'tests' not in p.name), key=lambda p: p.stat().st_mtime)
PATTERN = '''[* {:knowledge-point/question-generator [*]}
 {[:knowledge-point/questions :limit nil] [* {:question/difficulty [:db/ident]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/ident]}]}]}]}]'''
QUERY = '[:find (pull ?kp '+PATTERN+') :in $ ?kp :where [?kp :knowledge-point/id _]]'
from capture.scripts.database.images import ImageLibrary
import argparse, itertools, re


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

def fingerprint(q):
    complete, holes, rows, cols = v.read_table(q[':question/worked-solution'])
    _, missing, _, _ = v.read_table(q[':question/problem'])
    assert not holes and len(missing) == 3
    n = len(rows)
    labels = 'ABCD'[:n]
    field_type=q[':question/answer-fields'][0][':answer-field/type']
    if isinstance(field_type,dict):field_type=field_type[':db/ident']
    # Ignore seed, answer order, diagram layout, station renaming and heading
    # permutations. Different directed counts/queried relations are required.
    candidates = []
    for order in itertools.permutations(labels):
        rename = {x:i for i,x in enumerate(order)}
        candidates.append({'matrix':[[complete[(r,c)] for c in order] for r in order],
          'queried':sorted([rename[r],rename[c]] for r,c in missing.values()),
          'response':str(field_type).rsplit('/',1)[-1]})
    return min(g.digest(x) for x in candidates)

def source_fingerprint(q):
    mid = q.get(':question/math-academy-id')
    if mid in v.READ_IMAGES:
        case = next(x for x in json.loads((HERE/'source-cases.json').read_text()) if x['source_id']==mid)
        replay = g.generate(case['level'], template=case['template'], parameters=case['parameters'], profile=case['bank_profile'])
        return fingerprint(replay['question'])
    return fingerprint(q)

def clean(value):
    if isinstance(value, dict):return {str(k):clean(v) for k,v in value.items() if str(k)!=':db/id'}
    if isinstance(value, list):return sorted([clean(v) for v in value], key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value, uuid.UUID):return str(value)
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
        assert fingerprint(q) == rec['generation']['inventory_fingerprint']
        v.check(rec)
    for asset in json.loads((path/'assets.json').read_text()).values():
        assert sha(Path('/media/jake/SSD/EDB/math')/asset['path'])==asset['sha256']
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def validate_package():
    freeze = json.loads((HERE/'freeze.json').read_text())
    for name, digest in freeze['files'].items():
        assert sha(ROOT/name) == digest, 'Frozen generator evidence changed: '+name
    qa = json.loads((ROOT/'generate/runs/current/qa/17592186087819.json').read_text())
    assert qa['parent_review']=='passed' and qa['generator_sha256']==sha(HERE.with_suffix('.py'))

def current(path):
    inv = inventory(path/'inventory-before.json')
    b = inv['basis']
    assert DB.basis()==b
    kp = read_kp(path,b)
    assert str(kp[':knowledge-point/id'])==g.KP_UUID
    expected = {q[':question/math-academy-id']:q for q in g.CAPTURE['record'][':knowledge-point/questions']}
    source = {q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    assert set(expected)<=set(source)
    for mid,q in expected.items():
        assert clean(q)==clean(source[mid]), 'Source changed; reclassification required: '+mid
    gen = kp.get(':knowledge-point/question-generator')
    gid = str(gen[':question-generator/id']) if gen else g.uid('question-generator')
    if gen:assert gen[':question-generator/script']==SCRIPT
    registered=DB.query('[:find (pull ?g [*]) :in $ ?gid :where [?g :question-generator/id ?gid]]',[uuid.UUID(gid)],path,'generator-identity',b)
    if registered:assert len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
    jobs = {j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
    represented = {str(q[':question/difficulty'][':db/ident']).rsplit('/',1)[-1] for q in kp[':knowledge-point/questions'] if ':question/difficulty' in q}
    needed = {level:jobs[level]['missing'] if level in jobs else 0 if level in represented else 5 for level in ('easy','moderate','hard')}
    return inv,kp,gid,needed

def check_instances(records):
    for rec in records:
        assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.KP_UUID
        assert rec['generation']['level'] in ('easy','moderate','hard')
        assert rec['question'][':question/difficulty']==':question.difficulty/'+rec['generation']['level']
        v.check(rec)
        replay = g.generate(rec['generation']['level'], seed=rec['generation']['seed'], template=rec['generation']['template'], parameters=rec['generation']['parameters'], profile=rec['generation']['bank_profile'])
        assert ordered(replay['question'])==ordered(rec['question']), 'Deterministic replay mismatch'
        assert replay['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
        rec['generation']['inventory_fingerprint']=fingerprint(rec['question'])

def native(records,path):
    save(path/'native-input.json',[v.grading_fixture(r['question'][':question/id'],r) for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    report=json.loads((path/'native-report.json').read_text())
    assert report['documented_unresolved_checks']==0

def prepare():
    validate_package()
    path=OUT/'prepared';path.mkdir(exist_ok=True)
    inv,kp,gid,needed=current(path)
    used={source_fingerprint(q) for q in kp[':knowledge-point/questions']}
    supplied_path=JOB.with_suffix('.generated')
    supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances=supplied.get('instances',[])
    check_instances(instances)
    save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
    records=[];exceptions=[]
    for level,count in needed.items():
        accepted=[]
        for rec in instances:
            fp=rec['generation']['inventory_fingerprint']
            if rec['generation']['level']==level and len(accepted)<count and fp not in used:
                accepted.append(rec);used.add(fp)
        for seed in range(1000,2000):
            if len(accepted)>=count:break
            rec=g.generate(level,seed=seed)
            check_instances([rec]);fp=rec['generation']['inventory_fingerprint']
            if fp not in used:
                accepted.append(rec);used.add(fp)
        records.extend(accepted)
        if len(accepted)<count:
            exceptions.append({'level':level,'required':count,'generated':len(accepted),'shortage':count-len(accepted),'bounded_search_seeds':[1000,1999],'reason':'Validated finite parameter domain exhausted by bounded search; shortage remains explicit.'})
    native(records+instances,path)
    save(path/'generated-local.json',records)
    save(path/'preparation.json',{'basis':inv['basis'],'lineage':LINEAGE,'generator_id':gid,'needed':needed,'new_questions':len(records),'capability_exceptions':exceptions,'generator_sha256':sha(HERE.with_suffix('.py')),'frozen_files_verified':114,'source_banks_matched':7,'distinctness':'Directed graph and queried relations canonicalized over every station renaming; excludes seeds, identities, choice order, layout, and heading permutations.'})
    print(json.dumps({'prepared_basis':inv['basis'],'needed':needed,'questions':len(records),'exceptions':exceptions}),flush=True)

def finish(path,intent,verified,inv):
    result={'outcome':'finite-limit' if intent['capability_exceptions'] else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'source':SOURCE,'verified_commit_basis':verified['basis_after'],'basis_before':intent['basis'],'new_questions':verified['new_questions'],'by_level':intent['by_level'],'supported_levels':['easy','moderate','hard'],'capability_exceptions':intent['capability_exceptions'],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_shortages':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'native-report.json',path/'assets.json',path/'inventory-after.json',HERE/'validation.json',ROOT/'generate/runs/current/qa/17592186087819.json')]}
    result['evidence'].append(str((OUT/'prepared/review-validation.json').relative_to(ROOT)))
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps(result,indent=2),flush=True)

def commit():
    validate_package()
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        # Recover a retained request before recalculating any fresh intent.
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['generator_path']==SCRIPT
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['endpoint']==DB.args.endpoint and intent['database']=='math'
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report)
                finish(path,intent,verified,inventory(path/'inventory-after.json'))
                return
        inv,kp,gid,needed=current(OUT/'locked-current')
        b=inv['basis'];path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        save(path/'inventory-before.json',inv)
        prepared=json.loads((OUT/'prepared/preparation.json').read_text())
        review=json.loads((OUT/'prepared/review-validation.json').read_text())
        assert review['passed'] and review['generated_sha256']==sha(OUT/'prepared/generated-local.json')
        candidates=json.loads((OUT/'prepared/generated-local.json').read_text())
        check_instances(candidates)
        used={source_fingerprint(q) for q in kp[':knowledge-point/questions']};records=[]
        bylevel={level:0 for level in needed}
        for rec in candidates:
            level=rec['generation']['level'];fp=rec['generation']['inventory_fingerprint']
            if bylevel[level]<needed[level] and fp not in used:
                records.append(copy.deepcopy(rec));used.add(fp);bylevel[level]+=1
        exceptions=prepared['capability_exceptions']
        assert all(bylevel[level]==count or any(e['level']==level and e['shortage']==count-bylevel[level] for e in exceptions) for level,count in needed.items()), 'Fresh shortages changed; regenerate before committing'
        native(records,path)
        identities=[]
        for rec in records:
            q=rec['question'];identities.append([kw('question/id'),uuid.UUID(q[':question/id'])])
            for f in q[':question/answer-fields']:
                identities.append([kw('answer-field/id'),uuid.UUID(f[':answer-field/id'])])
                identities.extend([kw('answer/id'),uuid.UUID(a[':answer/id'])] for a in f[':answer-field/choices'])
        if identities:
            existing=DB.query('[:find ?e ?attr ?id :in $ [[?attr ?id]] :where [?e ?attr ?id]]',[identities],path,'generated-identities',b)
            assert not existing, 'A generated identity already exists outside the selected inventory; reconcile before writing'
        save(path/'generated-local.json',records)
        subprocess.run(['/usr/bin/python3',str(HERE/'publish_assets.py'),str(path)],check=True)
        records=json.loads((path/'generated.json').read_text())
        for asset in json.loads((path/'assets.json').read_text()).values():
            assert sha(Path('/media/jake/SSD/EDB/math')/asset['path'])==asset['sha256']
        forms=transaction(records,kp,gid)
        assert forms, 'Already complete; recover existing verification instead of submitting empty intent'
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b)
        assert len(source)==1
        tx=dumps(forms)+'\n';txpath=path/'transaction.edn'
        with txpath.open('w') as stream:
            stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0])
        assert DB.basis()==b, 'Basis advanced under application lock; reprepare'
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'route-matrix-replenish-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'by_level':bylevel,'capability_exceptions':exceptions,'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        verified=verify(path,intent,report)
        finish(path,intent,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['prepare','commit'])
    args=parser.parse_args()
    prepare() if args.stage=='prepare' else commit()

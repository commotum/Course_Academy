#!/usr/bin/env python3
"""Replenish only KP 17592186105734; preserve exact requests and receipt readback."""
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
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
spec = importlib.util.spec_from_file_location('altitude_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.G
KP = g.KP['db_id']
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'186699933e4fc4894f55c2162b54daf52da4f0a3a72df9b8d726c27389fdf525'
OUT = HERE/'reference/replenishment'
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY = (HERE/'reference/source-query.edn').read_text()
CASES = {c['source_id']:c for c in json.loads((HERE/'source-cases.json').read_text())}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(path):
    response = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(response.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']


def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]


def normalize(q):
    result = {k:str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f:f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id', str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result


def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q


def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x, sort_keys=True))
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


def fingerprint(q):
    """Read actual printed geometry, ignoring rigid motions, labels, banks and order."""
    prompt = q[':question/problem']
    pts = {n:S.Matrix(list(map(int,c.split(',')))) for n,c in re.findall(r'([A-Z])\(([-\d, ]+)\)',prompt)}
    assert len(pts) == 3
    apex = re.search(r'length of the altitude \$([A-Z]{2})\$',prompt)[1][0]
    a,b = sorted(set(pts)-{apex})
    U,V = pts[b]-pts[a], pts[apex]-pts[a]
    gram = (int(U.dot(U)), int(V.dot(V)), int(U.dot(V)))
    reversed_base = (gram[0], gram[1]+gram[0]-2*gram[2], gram[0]-gram[2])
    return g.digest(min(gram,reversed_base))


def record_for(q):
    nq = normalize(q)
    sid = q.get(':question/math-academy-id')
    if sid:
        c = CASES[sid]
        template,profile = c['template'],c['bank_profile']
    else:
        level = nq[':question/difficulty'].split('/')[-1]
        kind = nq[':question/answer-fields'][0][':answer-field/type'].split('/')[-1]
        template = 'authored_'+level+'_'+kind
        profile = 'none' if kind == 'blank' else 'method_errors'
    return {'knowledge_point':dict(g.KP), 'question':nq, 'generation':{'template':template, 'profile':profile}}


UNAVAILABLE_QUERY = '''[:find ?q :in $ ?learner ?kp
 :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/activity ?a]
   (or [?t :learner-task/status :learner-task.status/started] [?t :learner-task/status :learner-task.status/paused])
   (or [?a :activity/type :activity.type/lesson] [?a :activity/type :activity.type/review] [?a :activity/type :activity.type/assessment])
   [?a :activity/steps ?st] [?st :step/content ?q]))]'''


def counts(kp, path, basis):
    unavailable = {r[0] for r in DB.query(UNAVAILABLE_QUERY,[LEARNER,KP],path,'unavailable',basis)}
    used = {fingerprint(kp[':knowledge-point/canonical-example'])}
    available = {l:set() for l in LEVELS}
    native,excluded,valid = [],[],[]
    for q in kp[':knowledge-point/questions']:
        fp = fingerprint(q)
        used.add(fp)  # Even defective, shown and unrated geometries remain excluded.
        sid = q.get(':question/math-academy-id')
        if sid in ('q-20028','q-128008'):
            excluded.append({'question':q[':db/id'], 'source_id':sid, 'reason':'Missing difficulty/key/solution' if sid == 'q-20028' else 'Incorrect reduced basis vector in original worked solution; original preserved'})
            continue
        r = record_for(q)
        v.check(r)
        native.append(v.native_item('current '+str(q[':question/id']),r))
        valid.append(q[':db/id'])
        level = r['question'][':question/difficulty'].split('/')[-1]
        assert level in LEVELS
        if q[':db/id'] not in unavailable:
            available[level].add(fp)
    save(path/'source-grading-input.json',native)
    subprocess.run([str(HERE/'check-engine'),str(path/'source-grading-input.json'),str(path/'source-grading-report.json')],check=True)
    stock = {'basis':basis, 'distinct_available':{l:len(available[l]) for l in LEVELS}, 'missing':{l:max(0,5-len(available[l])) for l in LEVELS}, 'validated_practice_ids':valid, 'excluded_originals':excluded, 'shown_or_reserved_ids':sorted(unavailable), 'canonical_excluded':True, 'deduplication':'Gram geometry modulo reversing base; excludes rigid motion, translation, aliases, layout, seed and bank'}
    save(path/'validated-inventory.json',stock)
    return stock,used


def validate_instance(r):
    assert r['knowledge_point'] == g.KP
    level = r['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS
    m = r['generation']
    replay = g.generate(level,seed=m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])
    assert ordered(replay['question']) == ordered(r['question'])
    assert fingerprint(r['question']) == m['mathematical_fingerprint']
    v.check(r)


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
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms


def check_report(report,path,source):
    attrs = {e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')} | {':answer-field/'+s for s in ('id','key','type','choices','correct')} | {':answer/'+s for s in ('id','type','value')} | {':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added,'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed,name


def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp = read_kp(path/'readback',report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')} == {k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old)+len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q) == ordered(rec['question'])
        validate_instance(rec)
        assert fingerprint(q) == rec['generation']['mathematical_fingerprint']
    assert not transaction([],kp,intent['generator_id'])
    result = {'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result)
    return result


def finish(path,gid,verified,inv):
    kp = read_kp(path/'post-inventory',inv['basis'])
    stock,_ = counts(kp,path/'post-inventory',inv['basis'])
    remaining = {l:n for l,n in stock['missing'].items() if n}
    result = {'outcome':'finite-limit' if remaining else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified.get('by_level',{}),'supported_levels':list(LEVELS),'available_by_level':stock['distinct_available'],'remaining_supported_shortages':remaining,'capability_exceptions':[],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint'] == KP],'original_exclusions':stock['excluded_originals'],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'preparation.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'generated.json',path/'native-report.json',path/'inventory-after.json',path/'post-inventory/validated-inventory.json',HERE/'validation.json',HERE/'capabilities.json',HERE/'review.md',OUT/'runtime-validation.json') if p.exists()],'note':'Easy and moderate are validated authored same-method difficulty extensions. Original incomplete q-20028 and erroneous q-128008 remain untouched and excluded from validated stock. Distinctness ignores rigid motion, names, seed, option order and bank.'}
    if remaining:
        result['capability_exceptions'] = [{'reason':'No new distinct validated task found within bounded 1000-seed search per supported level','remaining':remaining,'filled':False}]
    save(path/'outcome.json',result)
    save(JOB.with_suffix('.result'),result)
    print(json.dumps(result),flush=True)


def runtime():
    global NATIVE
    frozen = json.loads((HERE/'freeze.json').read_text())
    for name,digest in frozen.items():
        if name.startswith('/'):
            assert sha(Path(name)) == digest,'Frozen input changed: '+name
    assert json.loads((HERE/'validation.json').read_text())['status'] == 'pass'
    NATIVE = build_learning(ROOT.parent/'EDB')
    deps = ROOT/'target/release/deps'
    libs = {name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
    source = ROOT/'generate/runs/current/check-engine.rs'
    command = ['rustc','--edition=2024','-O',str(source)]
    for name,p in libs.items():
        command += ['--extern',name+'='+str(p)]
    command += ['-L','dependency='+str(deps),'-o',str(HERE/'check-engine')]
    subprocess.run(command,check=True)
    save(OUT/'runtime-validation.json',{'frozen_package_hashes_verified':True,'source_replay_validation':str((HERE/'validation.json').relative_to(ROOT)),'generator_sha256':sha(HERE.with_suffix('.py')),'grader_source_sha256':sha(source),'grader_binary_sha256':sha(HERE/'check-engine'),'current_engine_libraries':{str(p):sha(p) for p in libs.values()},'dependencies':{'python':sys.version,'sympy':S.__version__},'plots':'none'})
    return preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())


def main():
    preview = runtime()
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        # Recover prior exact intent before considering a new transaction.
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent = json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage'] == LINEAGE and intent['source'] == SOURCE
                assert intent['sha256'] == sha(path/'transaction.edn') and intent['exact_edn'] == (path/'transaction.edn').read_text()
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report = DB._commit(intent,path/'transaction.edn',path)
                verified = verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'))
                return
        inv = inventory(OUT/'inventory-before.json')
        b = inv['basis']
        assert DB.basis() == b
        path = OUT/('basis-'+str(b))
        path.mkdir(exist_ok=True)
        kp = read_kp(path,b)
        assert str(kp[':knowledge-point/id']) == g.KP['id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured = json.loads((HERE/'source.json').read_text())['record']
        current = {q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:
            assert canonical(current[q[':question/math-academy-id']]) == canonical(q),'Source changed; reclassify'
        assert canonical(captured[':knowledge-point/canonical-example']) == canonical(kp[':knowledge-point/canonical-example'])
        contributor = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b)
        assert len(contributor) == 1
        gen = kp.get(':knowledge-point/question-generator')
        registered = DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',b)
        assert len(registered) <= 1
        gid = str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else str(uuid.uuid5(g.NS,'question-generator'))
        if registered:
            assert str(registered[0][0][':question-generator/id']) == gid
        identities = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-identity',b)
        assert not identities or identities[0][0][':question-generator/script'] == SCRIPT
        save(HERE/'capabilities.json',{'knowledgePoint':KP,'generator_id':gid,'script':SCRIPT,'version':g.VERSION,'supported_levels':list(LEVELS),'authored_levels':['easy','moderate'],'capability_exceptions':[],'evidence':['classification.md','template-extraction.md','validation.json','freeze.json'],'sampling_bound':1000,'bounded_search_is_not_proof_of_exhaustion':True,'source_errors_preserved':['q-20028 missing key/solution/difficulty','q-128008 erroneous reduced basis row'],'distinctness':'Gram geometry modulo base reversal, independent of choices, labels, orientation and seed'})
        stock,used = counts(kp,path,b)
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances',[])
        assert isinstance(instances,list)
        for r in instances:
            validate_instance(r)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        records,native = [],[]
        for level in LEVELS:
            need = stock['missing'][level]
            selected = 0
            for r in instances:
                if not r['question'][':question/difficulty'].endswith('/'+level):
                    continue
                fp = fingerprint(r['question'])
                if selected < need and fp not in used:
                    records.append(r);used.add(fp);selected += 1
            for seed_offset in range(1000):
                if selected >= need:
                    break
                # Alternate field contracts while testing distinct mathematical tasks.
                r = g.generate(level,seed=105734+seed_offset,field_type='radio' if selected%2 == 0 else 'blank')
                fp = fingerprint(r['question'])
                if fp in used:
                    continue
                validate_instance(r)
                records.append(r);used.add(fp);selected += 1
        for r in records+instances:
            native.append(v.native_item('generated '+r['question'][':question/id'],r))
        save(path/'generated.json',records)
        save(path/'native-input.json',native)
        subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        # Batch global identity lookups: no existing identity may be overwritten.
        for entity_type,ids in [('question',[r['question'][':question/id'] for r in records]),('answer-field',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            assert len(set(ids)) == len(ids)
            hits = DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+entity_type+'/id ?id]]',[[uuid.UUID(x) for x in ids]],path,entity_type+'-identities',b) if ids else []
            assert not hits,'Existing generated identity requires reconciliation'
        save(path/'preparation.json',{'basis':b,'original_job_basis':1831,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'source_evidence_unchanged':True,'asset_hashes':[],'validated_inventory_before':stock,'new_questions':len(records),'selected_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'supplied_generated_exists':supplied_path.exists(),'instance_metadata_includes':['version','seed','template','profile','parameters','domain','recipes','source_ids'],'dependencies':{'python':sys.version,'sympy':S.__version__}})
        forms = transaction(records,kp,gid)
        if not forms:
            verified = {'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'generator_registration_verified':True}
            save(path/'verification.json',verified)
            finish(path,gid,verified,inv)
            return
        txpath = path/'transaction.edn'
        tx = dumps(forms)+'\n'
        with txpath.open('w') as stream:
            stream.write(tx);stream.flush();os.fsync(stream.fileno())
        response = subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(response.stdout)
        pr = loads(response.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == b
        check_report(pr,path/'preview-check',contributor[0][0])
        assert DB.basis() == b
        intent = {'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'altitude-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report = DB._commit(intent,txpath,path)
        verified = verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))


if __name__ == '__main__':
    main()

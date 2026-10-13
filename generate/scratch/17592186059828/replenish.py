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
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'f37fd9f7051157240b59a62e91cce84f2063a908240b27527fa205bfe17d1760'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-80371ed6e5f3669c'
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

def fingerprint(q):
    return task_key(q)

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
        assert fingerprint(q) == task_key(rec['question'])
        v.displayed_check(rec); v.raster(rec)
        assert LIB.reference(image_path(q)) == image_path(q)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in ('easy','moderate','hard')}, 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

from image_library import ImageLibrary
import re
LIB=ImageLibrary('/media/jake/SSD/EDB/math')
LEVELS=('easy','moderate','hard')
GEOMETRIES={}

def image_path(q):
    return re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]

def geom_key(p):
    # Same assessed interval is one task even across bank, scale or difficulty.
    return (str(v.sp.Rational(str(p['left']))),str(v.sp.Rational(str(p['right']))),p['left_closed'],p['right_closed'])

def task_key(q):
    return geom_key(GEOMETRIES[image_path(q)])

def native(rec):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual native radio grading for committed instance'} for a in f[':answer-field/choices']]}

def init_geometry():
    capture=json.loads((HERE/'current-source.json').read_text())
    raw={'q-28850':(-1,2,False,True),'q-31762':(1,4,False,False),'q-154795':(-3,2,False,False),'q-31779':(2,4,True,False)}
    for q in capture[':knowledge-point/questions']:
        a,b,lc,rc=raw[q[':question/math-academy-id']]
        GEOMETRIES[image_path(q)]={'left':a,'right':b,'left_closed':lc,'right_closed':rc}
    GEOMETRIES[image_path(capture[':knowledge-point/canonical-example'])]={'left':-2,'right':2,'left_closed':True,'right_closed':False}
    for path in OUT.glob('basis-*/generated.json'):
        for rec in json.loads(path.read_text()):
            GEOMETRIES[image_path(rec['question'])]=rec['generation']['plots']['geometry']

def publish(rec):
    rec=copy.deepcopy(rec)
    asset=rec['generation']['plots'];old=asset['prompt'];digest=sha(Path(old))
    new=LIB.put_file(old,expected_sha256=digest)
    assert sha(LIB.math_root/new)==digest
    rec['question'][':question/problem']=rec['question'][':question/problem'].replace(old,new)
    rec['generation']['published_asset']={'path':new,'sha256':digest}
    GEOMETRIES[new]=asset['geometry']
    return rec

def finish(path,gid,verified,inv):
    jobs=[j for j in inv['jobs'] if j['knowledgePoint']==KP]
    outcome={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'by_level':verified['by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'supported_inventory_shortages':{l:next((j['missing'] for j in jobs if j['difficulty']==l),0) for l in LEVELS},'inventory_recheck_basis':inv['basis'],'remaining_jobs':jobs,'capability_exceptions':[],'unsupported_levels_filled':False,'finite_catalogs':json.loads((HERE/'validation.json').read_text())['finite_task_catalogs'],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',path/'native-report.json',HERE/'validation.json',HERE/'current-validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md']],'note':'Ratings are authored bounded extensions. Existing both-open sources are retained, excluded from half-open reserve counts. Existing unrated questions remain unrated and excluded; the unclassified scheduler job may remain visible.'}
    save(path/'outcome.json',outcome);save(JOB.with_suffix('.result'),outcome)
    print(json.dumps({k:outcome[k] for k in ('outcome','verified_commit_basis','new_questions','by_level','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'current-validation.json').read_text());assert validation['passed']
    assert all(sha(ROOT/p)==d for p,d in validation['hashes'].items())
    assert json.loads((HERE/'freeze.json').read_text())['generator_sha256']==sha(HERE.with_suffix('.py'))
    init_geometry()
    preview=preview_executable(SimpleNamespace(math_root=LIB.math_root,repo_root=ROOT,preview_bin=None),threading.Event())
    lock_path=ROOT/'.local/learning/requests/math/api.lock'
    with lock_path.open('a') as lock:
        print('Waiting for application commit lock',flush=True)
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application commit lock acquired',flush=True)
        # Recover exact saved intent before any fresh planning.
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                for rec in json.loads((path/'generated.json').read_text()):GEOMETRIES[image_path(rec['question'])]=rec['generation']['plots']['geometry']
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        # Compare every captured original, including missing facts, at one basis.
        prior=DB.query(QUERY,[KP],path,'classified-source',validation['capture_basis'])[0][0]
        old={q[':db/id']:q for q in prior[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(now[e]==q for e,q in old.items()) and prior[':knowledge-point/canonical-example']==kp[':knowledge-point/canonical-example'],'Current source evidence changed'
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        existing=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'registered-generator',b)
        assert len(existing)<=1
        gid=str(gen[':question-generator/id']) if gen else str(existing[0][0][':question-generator/id']) if existing else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        if gen:assert gen[':question-generator/script']==SCRIPT
        save(HERE/'generator-identity.json',{'id':gid,'script':SCRIPT})
        jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
        needed={l:jobs.get(l,{}).get('missing',5 if l not in jobs and not any(q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+l for q in now.values()) else 0) for l in LEVELS}
        # Inventory includes the rated both-open source. It is gradable but outside
        # this KP's scope, so conservatively add one easy half-open replacement.
        if any(q.get(':question/math-academy-id')=='q-154795' for q in now.values()):needed['easy']+=1
        used={task_key(q) for q in now.values()};used.add(task_key(kp[':knowledge-point/canonical-example']))
        records=[];selected={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        assert isinstance(instances,list)
        for rec in instances:
            assert rec['knowledge_point']['db_id']==KP and not rec['generation'].get('evidence_only')
            v.displayed_check(rec);v.raster(rec)
            l=rec['question'][':question/difficulty'].split('/')[-1];assert l in LEVELS
            key=geom_key(rec['generation']['plots']['geometry'])
            if key not in used and selected[l]<needed[l]:records.append(publish(rec));used.add(key);selected[l]+=1
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        for l in LEVELS:
            if selected[l]>=needed[l]:continue
            # Enumerate finite domains rather than treating seed changes as new tasks.
            params=g.catalog(l);import random;random.Random(4085160375).shuffle(params)
            for p in params:
                rec=g.generate(l,4085160375,parameters=p,profile='observed_right_ray' if selected[l]%2 else 'authored_left_shift')
                v.displayed_check(rec);v.raster(rec)
                key=geom_key(rec['generation']['plots']['geometry'])
                if key in used:continue
                records.append(publish(rec));used.add(key);selected[l]+=1
                if selected[l]>=needed[l]:break
        save(path/'generated.json',records)
        if selected!=needed:
            result={'outcome':'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'needed':needed,'produced':selected,'shortage':{l:needed[l]-selected[l] for l in LEVELS},'evidence':[str((path/'generated.json').relative_to(ROOT))],'bounded_exception':'Finite coordinate/orientation catalogs exhausted after excluding all existing assessed intervals; banks, scale, seeds and identities cannot supply new tasks.'}
            save(JOB.with_suffix('.result'),result);raise RuntimeError('Finite task limit; shortages explicit')
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        assert not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'question-identities',b)
        save(path/'native-input.json',[native(r) for r in instances+records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'needed':needed,'selected':selected,'new_questions':len(records),'authored_difficulty':True,'scope_exclusions':['q-154795 (both-open, rated easy)','q-31762 (both-open, unrated)'],'retained_unrated_sources':['q-28850','q-31762'],'asset_hashes':[r['generation']['published_asset'] for r in records],'distinctness':'Exact assessed interval and endpoint orientation, excluding all existing source, canonical and generated tasks regardless of bank, seed, choice order, labels or scale','finite_catalogs':validation['finite_task_catalogs'],'source_evidence_unchanged':True,'lock':str(lock_path)})
        forms=transaction(records,kp,gid);assert forms
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'half-open-numberlines-17592186059828-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(lock_path)}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

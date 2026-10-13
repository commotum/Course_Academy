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
spec = importlib.util.spec_from_file_location('generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.CAPTURE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'ae5d0af8ff9a131165bd880dfadad81cbb3db3361ab2071b63304003ea94e61d'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = build_learning(ROOT.parent/'EDB')
QUERY = (HERE / 'source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]

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


LEVELS = ('easy', 'moderate', 'hard')
TOPIC = 17592186049592

def counts(path):
    # Existing native batched inventory reader; no independent grading/count rules.
    sys.path.insert(0, str(ROOT/'generate/scripts'))
    import find_candidates
    binary = find_candidates.build(ROOT.parent/'EDB')
    request = {'database':'math', 'learner':LEARNER, 'after_basis':None, 'lineage':None, 'at':None, 'topics':[TOPIC], 'activity_type':'review'}
    response = subprocess.run([str(binary)], input=json.dumps(request), env=DB.env, text=True, capture_output=True, check=True, timeout=90)
    result = json.loads(response.stdout)
    assert result['cursor']['lineage'] == LINEAGE
    topic = next(t for t in result['topics'] if t['db/id'] == TOPIC)
    save(path, result)
    return result, topic['topic_inventory']['available']

def verify(path, intent, report):
    assert report[':edb/committed'] is True
    assert report[':edb/db-before-t'] == intent['basis']
    check_report(report, path/'receipt-check', intent['source_eid'])
    kp = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    assert {k:v for k,v in kp.items() if k != ':knowledge-point/question-generator'} == {k:v for k,v in before.items() if k != ':knowledge-point/question-generator'}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id']
    assert gen[':question-generator/script'] == SCRIPT
    assert not before.get(':knowledge-point/question-generator')
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':0,
              'unchanged_source_questions':len(before[':knowledge-point/questions']), 'unchanged_canonical_example':True,
              'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def finish(path, gid, verified):
    inv = inventory(path/'inventory-after.json')
    qualified, available = counts(path/'qualified-inventory-after.json')
    result = {'outcome':'generated', 'knowledgePoint':KP, 'topic':TOPIC, 'generator_path':SCRIPT, 'generator_id':gid,
              'verified_commit_basis':verified['basis_after'], 'lineage':LINEAGE, 'new_questions':0,
              'new_questions_by_level':{l:0 for l in LEVELS}, 'supported_levels':list(LEVELS), 'unsupported_levels':[],
              'unsupported_levels_filled':False, 'inventory_scope':'review topic pool', 'available_by_level':available,
              'inventory_recheck_basis':qualified['basis'], 'remaining_supported_shortages':{l:max(0,5-available[l]) for l in LEVELS},
              'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
              'note':'Current review reserves already satisfy the minimum. Executed and revalidated the existing generator; committed only its registration. Preview instances are retained locally, not added to an already stocked pool.',
              'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'qualified-inventory-after.json',path/'preparation.json',HERE/'reference/execution.json',HERE/'reference/native-current-report.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'capabilities.json')]}
    save(path/'outcome.json',result)
    save(JOB.with_suffix('.result'),result)
    print(json.dumps(result),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['status']=='passed' and validation['script_sha256']==sha(HERE.with_suffix('.py'))
    assert json.loads((HERE/'reference/native-current-report.json').read_text())['documented_unresolved_checks']==0
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                finish(path,intent['generator_id'],verify(path,intent,report))
                return
        inv=inventory(OUT/'inventory-before.json')
        qualified,available=counts(OUT/'qualified-inventory-before.json')
        basis=inv['basis']
        assert qualified['basis']==basis and DB.basis()==basis
        assert all(available[l]>=5 for l in LEVELS), 'Changed shortage requires new content preparation'
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
        kp=read_kp(path,basis)
        assert str(kp[':knowledge-point/id'])==g.SOURCE[':knowledge-point/id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
        for q in g.SOURCE[':knowledge-point/questions']:
            assert normalize(current[q[':question/math-academy-id']])==normalize(q), 'Source changed; reclassify'
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis)
        assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.SOURCE[':knowledge-point/id']),'question-generator'))
        collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not collision and gen is None, 'Existing registration requires reconciliation'
        forms=[{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},
               [kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator'],[kw('db/ensure'),KP,kw('knowledge-point/validate')]]
        save(path/'preparation.json',{'basis':basis,'original_job_basis':1831,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,
                                    'inventory_scope':'topic review pool','available_by_level':available,'new_questions':0,
                                    'source_evidence_unchanged':True,'asset_hashes':[],'reason':'No topic shortage remains; register validated generator only.'})
        tx=dumps(forms)+'\n';txpath=path/'transaction.edn'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],
                'basis':basis,'expected_basis':basis,'request_key':'autonomous-ode-registration-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),
                'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,
                'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[],
                'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),
                'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        finish(path,gid,verify(path,intent,report))

if __name__=='__main__':main()


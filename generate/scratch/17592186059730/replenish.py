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
KP = g.KP['db_id']
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '3c9267f7171f073eb215ff53f31d80940b90d262017914774969a9e30d109686'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-0ee7e7bd24d378f7'
DISCOVERY = ROOT / '.local/generate/find-candidates-b13a7928a9573a2f'
LEVELS = ('easy','moderate','hard')
Q = '''[* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]'''
QUERY = '[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+Q+'} {[:knowledge-point/questions :limit nil] '+Q+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'

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
    text=q[':question/problem']
    if q.get(':question/math-academy-id')=='q-168035':
        case=next(c for c in json.loads((HERE/'source-cases.json').read_text()) if c['source_id']=='q-168035')
        text=g.generate('easy',17,case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'][':question/problem']
    pairs = __import__('re').findall(r'(?:⟨|\\langle)\s*(.*?)(?:⟩|\\rangle)',text)
    assert len(pairs)==2, text
    vectors=[[v.eval_math(z) for z in t.split(',')] for t in pairs]
    return g.digest({'skill':'sum_corresponding_products','coordinate_pairs':sorted(tuple(sorted((str(x),str(y)))) for x,y in zip(*vectors))})

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
        assert fingerprint(q) == rec['generation']['mathematical_fingerprint']
        v.check_record(rec)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in LEVELS}, 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def counts(path):
    request={'database':'math','learner':LEARNER,'topics':[17592186048954],'activity_type':'lesson','after_basis':None,'lineage':None,'at':None}
    r=subprocess.run([str(DISCOVERY)],input=json.dumps(request),env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['cursor']['lineage']==LINEAGE
    save(path,x)
    pool=[kp for t in x['topics'] for kp in t['knowledge_points'] if kp['db/id']==KP]
    assert len(pool)==1
    return x['basis'],pool[0]['inventory']['available']


def source_projection(actual, expected):
    if isinstance(expected,dict):
        assert all(k in actual for k in expected), set(expected)-set(actual)
        return {k:source_projection(actual[k],val) for k,val in expected.items()}
    if isinstance(expected,list):
        assert len(actual)==len(expected)
        if expected and isinstance(expected[0],dict):
            key=next(k for k in (':db/id',':answer/id',':answer-field/id',':question/id') if k in expected[0])
            actual=sorted(actual,key=lambda a:str(a[key]));expected=sorted(expected,key=lambda a:str(a[key]))
        return [source_projection(a,e) for a,e in zip(actual,expected)]
    return str(actual) if isinstance(expected,str) else actual


def finish(path,gid,verified,inv,available):
    # The captured dependent source remains retained, but cannot count as standalone practice.
    validated=dict(available);validated['easy']=max(0,validated['easy']-1)
    result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'generated_by_level':verified['by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'capability_exceptions':[],'inventory_recheck_basis':inv['basis'],'available_by_level':available,'validated_available_by_level':validated,'remaining_shortages':{l:max(0,5-validated[l]) for l in LEVELS},'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'discovery-after.json',path/'preparation.json',path/'native-report.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'classification.md',HERE/'template-extraction.md')],'note':'Observed easy inventory meets the minimum even excluding q-168035 whose original prompt needs omitted part-1 context. Moderate/hard are documented arithmetic workload extensions. All original questions and learner history retained.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','generated_by_level','validated_available_by_level','remaining_shortages','remaining_jobs')}),flush=True)


def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']
    freeze=json.loads((HERE/'freeze.json').read_text())
    assert all(sha(ROOT/a['path'])==a['sha256'] for a in freeze['artifacts'])
    assert sha(HERE.with_suffix('.py'))==validation['generator_sha256']
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                inv=inventory(path/'inventory-after.json');_,available=counts(path/'discovery-after.json')
                finish(path,intent['generator_id'],verified,inv,available);return
        inv=inventory(OUT/'inventory-before.json');b,available=counts(OUT/'discovery-before.json')
        assert b==inv['basis']==DB.basis()
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP['id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        raw=g.RAW['record']
        for expected in raw[':knowledge-point/questions']:
            assert source_projection(current[expected[':db/id']],expected)==expected,'Source evidence changed'
        assert source_projection(kp[':knowledge-point/canonical-example'],raw[':knowledge-point/canonical-example'])==raw[':knowledge-point/canonical-example']
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        # Fresh registered generator identities are deterministic; subsequent calls reuse them.
        needed={l:max(0,5-(available[l]-(1 if l=='easy' else 0))) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        if kp.get(':knowledge-point/canonical-example'):used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];selected={l:0 for l in LEVELS};attempts={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        def check(rec):
            v.check_record(rec)
            meta=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
            assert meta['bank_profile'] in ('authored_operations','authored_blank')
            replay=g.generate(level,meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
            assert ordered(q)==ordered(replay['question'])
            assert fingerprint(q)==meta['mathematical_fingerprint']
            return level,fingerprint(q)
        for rec in instances:
            level,fp=check(rec)
            if selected[level]<needed[level] and fp not in used:
                records.append(rec);used.add(fp);selected[level]+=1
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        for l in LEVELS:
            for offset in range(1000):
                if selected[l]==needed[l]:break
                rec=g.generate(l,int(JOB.name[:8],16)+offset);level,fp=check(rec);attempts[l]+=1
                if fp not in used:
                    records.append(rec);used.add(fp);selected[l]+=1
        assert selected==needed,'Bounded sampling exhausted; retain explicit shortage'
        for attribute,ids in (('question/id',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attribute+' ?id]]',[ids],path,attribute.replace('/','-')+'-collisions',b),'Identity collision; reconcile'
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or (len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT)
        save(path/'generated.json',records)
        (path/'review.md').write_text('# Replenishment review\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        save(path/'native-input.json',[v.engine_item(r['question'][':question/id'],r) for r in instances+records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'available_by_level':available,'validated_easy_adjustment':{'excluded_question':'q-168035','reason':'Omitted part-1 context in retained source prompt'},'missing_by_level':needed,'selected_by_level':selected,'sampling_attempts':attempts,'source_evidence_unchanged':True,'assets':[],'difficulty_evidence':'Observed easy; documented authored moderate mixed-sign integer and hard exact decimal workloads','distinctness':'Sorted exact corresponding-component factor pairs; excludes factor order, coordinate order, labels, layout, choice order, profile and seed; checked against all current practice and canonical tasks','source_references':str((HERE/'source.json').relative_to(ROOT)),'dependency_versions':{'sympy':g.sp.__version__,'python':sys.version.split()[0]}})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'by_level':{l:0 for l in LEVELS}}
            save(path/'verification.json',{'passed':True,'no_change':True,**verified});finish(path,gid,verified,inv,available);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:
            stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0])
        b2,available2=counts(path/'discovery-precommit.json');assert b2==DB.basis()==b and available2==available
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'dot-product-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        inv=inventory(path/'inventory-after.json');after,available=counts(path/'discovery-after.json');assert after==inv['basis']==verified['basis_after']
        finish(path,gid,verified,inv,available)

if __name__=='__main__':main()

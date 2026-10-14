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
LEVELS = ('easy','moderate','hard')
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '512b744a3ad2d78713f1fe5da172157c1d83ba6bdbea476147bdf40cdff34f06'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = build_learning(ROOT.parent / 'EDB')
from image_library import ImageLibrary
Q = "[* {:question/difficulty [:db/id :db/ident]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]"
PATTERN = "[* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example "+Q+"} {[:knowledge-point/questions :limit nil] "+Q+"}]"
QUERY = '[:find (pull ?kp '+PATTERN+') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]'
SUPPORTED = LEVELS

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

def fingerprint(q):
    if q.get(':question/math-academy-id') in g.SPECS:
        t=q[':question/math-academy-id'];level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        return g.generate(level,template=t,parameters={'scale':1,'shift':0,'vertical':0})['generation']['mathematical_fingerprint']
    for package in OUT.glob('basis-*/generated.json'):
        for rec in json.loads(package.read_text()):
            if rec['question'][':question/id']==str(q[':question/id']):
                assert normalize(q)==ordered(rec['question']), 'Changed generated content needs reconciliation'
                return rec['generation']['mathematical_fingerprint']
    raise AssertionError('Unrecognized question cannot establish semantic distinctness')

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
    assert all(canonical(now[e]) == canonical(q) for e,q in old.items())
    assert canonical({k:v for k,v in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}) == canonical({k:v for k,v in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')})
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
        audit_published(rec)
    for asset in json.loads((path/'preparation.json').read_text())['asset_hashes']:
        assert sha(Path('/media/jake/SSD/EDB/math')/asset['database_path'])==asset['sha256']
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in LEVELS}, 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'assets_verified':True, 'repeat_preparation_content_changes':0}
    result['distinct_available_after']=counts(kp,path/'readback',report[':edb/db-after-t'])['distinct_available']
    save(path/'verification.json', result)
    return result


def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
    if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def source_equivalent(current, captured):
    return canonical(current)==canonical(captured)

USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def engine_item(rec):
    f=rec['question'][':question/answer-fields'][0]
    checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Generated owned radio choice'} for a in f[':answer-field/choices']]
    return {'label':rec['question'][':question/id'],'record':rec,'checks':checks}

def grade(records,path):
    path.mkdir(parents=True,exist_ok=True)
    save(path/'native-input.json',[v.native_item(r,r['question'][':question/id']) for r in records])
    subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,timeout=55)

def audit_published(rec):
    local=copy.deepcopy(rec)
    for asset in rec['generation'].get('published_assets',[]):
        for key in (':question/problem',':question/worked-solution'):
            local['question'][key]=local['question'][key].replace(asset['database_path'],asset['local_path'])
        for f in local['question'][':question/answer-fields']:
            for a in f[':answer-field/choices']:
                a[':answer/value']=a[':answer/value'].replace(asset['database_path'],asset['local_path'])
    v.audit(local)


def counts(kp,path,basis):
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
    available={level:set() for level in LEVELS};records=[];excluded=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if level not in SUPPORTED:continue
        t=q.get(':question/math-academy-id')
        if t=='q-48081':
            excluded.append({'source':t,'reason':'Two duplicate selection fields; first has no correct designation; original preserved'});continue
        if t=='q-48082':
            excluded.append({'source':t,'reason':'Worked solution plot reverses open and filled markers at its claimed discontinuity x=2; original preserved'});continue
        if t:
            rec=g.generate(level,template=t,parameters={'scale':1,'shift':0,'vertical':0},profile='current')
            rec['question']=normalize(q)
        else:
            found=[r for package in OUT.glob('basis-*/generated.json') for r in json.loads(package.read_text()) if r['question'][':question/id']==str(q[':question/id'])]
            assert len(found)==1 and normalize(q)==ordered(found[0]['question'])
            rec=found[0]
        audit_published(rec);records.append(rec)
        if q[':db/id'] not in shown|reserved:available[level].add(fingerprint(q))
    if records:grade(records,path/'inventory-grading')
    result={'basis':basis,'distinct_available':{l:len(z) for l,z in available.items()},'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'validated_practice_ids':[r['question'][':question/id'] for r in records],'excluded_source_questions':excluded}
    save(path/'available-counts.json',result);return result

def finish(path,gid,verified,inv):
    current=read_kp(path/'current-inventory',inv['basis'])
    stock=counts(current,path/'current-inventory',inv['basis'])
    remaining={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
    exceptions=[{'level':level,'type':'finite-catalog-limit','distinct_catalog_tasks':{'easy':4,'moderate':5,'hard':2}[level],'additional_unused_tasks':0,'remaining_shortage':remaining[level],'filled':False,'evidence':'Every declared template enumerated; affine coordinate transforms, seed, identities, option order and radio/checkbox response changes excluded as new tasks. Existing source tasks retained, even when invalid or previously shown.'} for level in LEVELS if remaining[level]]
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'requested_basis':2188,'topic':17592186050574,'database':'math','generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified.get('basis_after'),'commit_basis_before':verified.get('basis_before'),'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(SUPPORTED),'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':stock['distinct_available'],'shortage_by_level':remaining,'capability_exceptions':exceptions,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_questions_and_learner_history_preserved':True,'evidence':[str(p.relative_to(ROOT)) for p in (HERE/'validation.json',HERE/'current-replay.json',HERE/'freeze.json',HERE/'capabilities.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'review.md',path/'generated.json',path/'preparation.json',path/'transaction.edn',path/'commit-intent.json',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'native-report.json',path/'inventory-after.json',path/'current-inventory/available-counts.json') if p.exists()], 'note':'Only unused half-unit hard tasks can be added from this validated finite catalog. Source graph tasks are never duplicated through coordinate shifts or repaired widgets. Moderate uses the current three-checkbox contract. Additive request attributed to application/ca-engine and verified under api.lock.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed'
    assert all(sha(ROOT/p)==digest for p,digest in json.loads((HERE/'freeze-hashes.json').read_text())['hashes'].items())
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis']
        assert DB.basis()==b and LINEAGE in DB.command('status')
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        original=g.CURRENT_SOURCE['record'];current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(source_equivalent(current[q[':db/id']],q) for q in original[':knowledge-point/questions']), 'Current source changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(original[':knowledge-point/canonical-example'])
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        reg=kp.get(':knowledge-point/question-generator')
        gid=str(reg[':question-generator/id']) if reg else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        if reg:assert reg[':question-generator/script']==SCRIPT
        stock=counts(kp,path,b);needed={l:max(0,5-stock['distinct_available'][l]) for l in SUPPORTED}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        records=[];selected={l:0 for l in needed};attempts={l:0 for l in needed}
        def select(rec):
            audit_published(rec);meta=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
            assert rec['knowledge_point']['db_id']==KP and level in needed and meta['eligible_for_learning'] and not meta['evidence_only']
            replay=g.generate(level,meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
            assert ordered(rec['question'])==ordered(replay['question'])
            fp=replay['generation']['mathematical_fingerprint'];assert fp==meta['mathematical_fingerprint']
            if selected[level]<needed[level] and fp not in used:
                records.append(rec);used.add(fp);selected[level]+=1
        supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied if isinstance(supplied,list) else supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        if isinstance(supplied,list):instances=supplied
        for rec in instances:select(rec)
        # Enumerate the whole finite catalog; do not pad it with parameter changes.
        candidates=[]
        for level in needed:
            templates=['q-78133','q-102115'] if level=='hard' else [t for t,z in g.SPECS.items() if z['level']==level]
            for i,t in enumerate(templates):
                rec=g.generate(level,20261014068695+i,template=t,parameters={'scale':'1/2' if level=='hard' else 1,'shift':-1,'vertical':1})
                candidates.append(rec);attempts[level]+=1;select(rec)
        save(path/'catalog-candidates.json',candidates)
        exceptions=[{'level':level,'type':'finite-catalog-limit','enumerated_tasks':attempts[level],'missing':needed[level]-selected[level],'filled':False} for level in needed if selected[level]<needed[level]]
        for attr,label,ids in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],path,'identity-'+label,b),'Existing identity requires reconciliation'
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
        assets=[];library=ImageLibrary(Path('/media/jake/SSD/EDB/math'))
        for rec in records:
            rec['generation']['published_assets']=[]
            for local_path in rec['generation']['graphs']:
                if local_path.startswith('images/'):continue
                data=Path(local_path).read_bytes();relative=library.put_bytes(data)
                assert (library.math_root/relative).read_bytes()==data
                asset={'local_path':local_path,'database_path':relative,'sha256':hashlib.sha256(data).hexdigest()}
                rec['generation']['published_assets'].append(asset);assets.append(asset)
                for key in (':question/problem',':question/worked-solution'):
                    rec['question'][key]=rec['question'][key].replace(local_path,relative)
                for f in rec['question'][':question/answer-fields']:
                    for answer in f[':answer-field/choices']:answer[':answer/value']=answer[':answer/value'].replace(local_path,relative)
            audit_published(rec)
        save(path/'generated.json',records)
        if records:grade(records,path)
        (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'generator_id':gid,'generator_path':SCRIPT,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'available_before':stock,'needed':needed,'selected':selected,'new_questions':len(records),'distinct_mathematical_tasks':len({r['generation']['mathematical_fingerprint'] for r in records}),'attempts':attempts,'capability_exceptions':exceptions,'supplied_generated_exists':supplied_path.exists(),'supplied_instances_validated':len(instances),'source_evidence_unchanged':True,'asset_hashes':assets})
        save(HERE/'freeze.json',{'generator_id':gid,'generator_path':SCRIPT,'version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'validation':str((HERE/'validation.json').relative_to(ROOT)),'classification_source_basis':g.CURRENT_SOURCE['basis'],'historical_source_basis':g.SOURCE['basis'],'rechecked_basis':b})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'new_questions':0,'by_level':selected,'basis_after':None,'no_change_basis':b}
            save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        p=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(p.stdout);pr=loads(p.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'continuity-graph-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()

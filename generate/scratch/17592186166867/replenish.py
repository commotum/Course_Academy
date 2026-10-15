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
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate-current.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
audit = v
LEVELS = ('easy','moderate','hard')
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'question-generator'))
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '85b34a4c57e9ac2b4285b5d6e1d13c82fee721f3c448ff1c829111d9a30e5986'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-c9743ced043e1fd7'
QUERY = (HERE / 'reference/initial/kp-query.edn').read_text()

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
    return v.fingerprint(q)

def validate_record(rec):
    local=copy.deepcopy(rec)
    published=local['generation'].get('published_plot')
    if published:
        local['question'][':question/problem']=local['question'][':question/problem'].replace(published,local['generation']['plot'])
    v.validate(local)
    assert fingerprint(rec['question'])==rec['generation']['mathematical_fingerprint']

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

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    audited={r['entity']:r for r in json.loads((HERE/'reference/initial/source-audit.json').read_text())['rows']}
    known={r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())}
    rows={l:[] for l in LEVELS};excluded=[]
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        row=audited.get(q[':db/id'])
        if row:
            if not row['eligible']:
                excluded.append({'entity':q[':db/id'],'reason':row['exclusion']});continue
            fp=row['fingerprint']
        elif str(q[':question/id']) in known:
            rec=known[str(q[':question/id'])];assert normalize(q)==ordered(rec['question']);validate_record(rec)
            fp=rec['generation']['mathematical_fingerprint']
        else:
            excluded.append({'entity':q[':db/id'],'reason':'Not in current validated source/generation audit'});continue
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        rows[level].append((q,fp))
    result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fp for _,fp in qs}),'available_question_ids':[str(q[':question/id']) for q,_ in qs]} for l,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded_invalid_or_incomplete':excluded}
    save(path/'available-counts.json',result);return result

def candidate_records(needed,added):
    for level in LEVELS:
        if not needed[level]:continue
        for seed in range(1000):
            if added[level]>=needed[level]:break
            yield g.generate(level,seed=166867+seed,field_type='blank' if seed%2 else 'radio')

def publish(records,path):
    hashes=[]
    for rec in records:
        old=rec['generation']['plot'];source=Path(old)
        if old.startswith('images/'):
            source=Path('/media/jake/SSD/EDB/math')/old
        digest=sha(source);target=Path('/media/jake/SSD/EDB/math/images')/digest[:2]/(digest+'.png')
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():
            with target.open('xb') as f:f.write(source.read_bytes());f.flush();os.fsync(f.fileno())
        assert sha(target)==digest
        rel=str(target.relative_to('/media/jake/SSD/EDB/math'))
        rec['question'][':question/problem']=rec['question'][':question/problem'].replace(old,rel)
        rec['generation']['published_plot']=rel
        hashes.append({'local':str(source),'reference':rel,'sha256':digest,'verified_available':True})
    save(path/'assets.json',hashes);return hashes


def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(rec['question']);validate_record(rec)
    save(path/'native-readback-input.json',[{'label':r['question'][':question/id'],'record':{'question':normalize(byid[r['question'][':question/id']]),'knowledge_point':r['knowledge_point'],'generation':r['generation']},'checks':audit.checks(r)} for r in records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-readback-input.json'),str(path/'native-readback-report.json')],check=True)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());after=verified.get('available_counts_after',prep['available_counts'])
    remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    evidence=[str(p.relative_to(ROOT)) for p in [HERE/'freeze.json',HERE/'validation.json',HERE/'validation-current.json',HERE/'capabilities.json',HERE/'classification-current.md',HERE/'reference/initial/source-audit.json',HERE/'reference/initial/native-report.json',path/'generated.json',path/'preparation.json',path/'assets.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json',path/'native-report.json'] if p.exists()]
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'observed_levels':['moderate','hard'],'authored_levels':['easy'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':evidence,'note':'All 11 current source questions preserved. One incomplete unrated source and one source with erroneous vertex prose excluded from validated counts. Generated tasks deduplicate by assessed information demand and full curve coefficient, excluding seeds, point aliases, choice order, banks and field layout. Easy is an explicitly authored supplied-equation variant. No learner facts modified.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)


def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def main():
    validation=json.loads((HERE/'validation-current.json').read_text());assert validation['status']=='passed' and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=loads((HERE/'reference/initial/kp.edn').read_text())[0][0]
        current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:
            assert canonical(current[q[':db/id']])==canonical(q),'Source changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(captured[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else GENERATOR_UUID
        existing_gen=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],path,'generator-identity',basis)
        if existing_gen:
            assert len(existing_gen)==1 and existing_gen[0][0][':question-generator/script']==SCRIPT
            gid=str(existing_gen[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT})
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']));records=[];added={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:
            assert rec['knowledge_point']['db_id']==KP and rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only'];validate_record(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        from itertools import chain
        for rec in chain(instances,candidate_records(needed,added)):
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=rec['generation']['mathematical_fingerprint']
            if added[level]<needed[level] and fp not in used:
                validate_record(rec);records.append(rec);used.add(fp);added[level]+=1
            if added==needed:break
        # Batch lookup stable question/field/answer identities before creating entities.
        ids=[uuid.UUID(qid) for rec in records for qid in [rec['question'][':question/id'],rec['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]]
        existing=DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing,'Existing identities require reconciliation'
        asset_hashes=publish(records,path)
        save(path/'generated.json',records)
        save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':audit.checks(r)} for r in records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({r['generation']['mathematical_fingerprint'] for r in records}),'asset_hashes':asset_hashes,'source_evidence_unchanged':True,'source_basis':g.CURRENT_SOURCES['basis']})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'parabola-slope-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

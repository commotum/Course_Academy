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
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'fec6b80bbac16ad83346913f6e00d00d96c6aecfccb40901a062a9265a03074c'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-1275f16a95dc6372'
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
    return v.fingerprint(q)

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
    rows={level:[] for level in g.SUPPORTED_LEVELS}
    recognized={r['question'][':question/id']:r for r in candidate_records()}
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        mid=q.get(':question/math-academy-id')
        if mid in g.EXCLUDED_PROFILES:continue
        if mid in g.DEFAULTS:
            rec=g.generate(str(q[':question/difficulty'][':db/ident']).split('/')[-1],template=mid,parameters=g.DEFAULTS[mid])
            # Captured originals preserve source identities; values/layout must replay exactly.
            assert q[':question/problem']==rec['question'][':question/problem'] and q[':question/worked-solution']==rec['question'][':question/worked-solution']
            f=q[':question/answer-fields'][0];rf=rec['question'][':question/answer-fields'][0]
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
            assert f[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
        elif str(q[':question/id']) in recognized:
            rec=recognized[str(q[':question/id'])];assert normalize(q)==ordered(rec['question'])
        else:continue
        level=rec['question'][':question/difficulty'].split('/')[-1]
        rows[level].append(q)
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({fingerprint(q) for q in qs}), 'available_question_ids':[str(q[':question/id']) for q in qs]} for level,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'contextual_and_incomplete_sources_excluded':True}
    save(path/'available-counts.json',result);return result

def candidate_records():
    return [r for level in g.SUPPORTED_LEVELS for r in g.candidates(level,59775)]

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
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(rec['question']);v.independent(rec)
    save(path/'readback/native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':v.checks(r)} for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'readback/native-input.json'),str(path/'readback/native-report.json')],check=True)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());caps=json.loads((HERE/'capabilities.json').read_text())
    after=verified.get('available_counts_after',prep['available_counts']);remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(g.SUPPORTED_LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'unsupported_levels_filled':False,'unsupported_levels':['hard'],'unsupported_nominal_shortage':{'hard':5},'capability_exceptions':caps['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'classification.json',HERE/'template-extraction.md',HERE/'validation.json',HERE/'capabilities.json'] if p.exists()],'note':'Easy and moderate distinct standalone inventory checked; hard remains unsupported. Legacy unclassified job can remain because incomplete originals are preserved. No source or learner facts modified.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass'
    assert all(sha(ROOT/p)==digest for p,digest in validation['hashes'].items()),'Validated package changed; revalidate'
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=json.loads((HERE/'source.json').read_text());current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:assert canonical(current[q[':question/math-academy-id']])==canonical(q),'Source changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(captured[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        assert gid==g.GENERATOR_UUID
        registered=DB.query('[:find (pull ?g [:db/id :question-generator/id :question-generator/script]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not registered or gen and registered[0][0][':db/id']==gen[':db/id'],'Unlinked generator identity requires reconciliation'
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']));records=[];added={l:0 for l in g.SUPPORTED_LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:v.independent(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        for rec in instances+candidate_records():
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                v.independent(rec);records.append(rec);used.add(fp);added[level]+=1
        # Batch lookup stable question/field/answer identities before creating entities.
        ids=[uuid.UUID(qid) for rec in records for qid in [rec['question'][':question/id'],rec['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]]
        existing=DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing,'Existing identities require reconciliation'
        save(path/'generated.json',records)
        save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':v.checks(r)} for r in records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':[],'source_evidence_unchanged':True,'source_basis':g.SOURCE_BASIS})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'gaussian-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

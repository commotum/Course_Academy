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
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate_current.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '1419f4892a48b575ca6d8dda7234e5c272860de6264458281dadf0c903aae2ae'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = Path((HERE/'reference/native-path.txt').read_text())
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

LEVELS = ('easy', 'moderate', 'hard')
USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k)!=':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x,sort_keys=True))
    return str(value) if isinstance(value, uuid.UUID) else value

def available_counts(path, kp, basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    available={level:[] for level in LEVELS}
    fixtures=[]; excluded=[]
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'): continue
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if level not in LEVELS: continue
        # q-32242 retains an incorrect printed first-row sign flip. Preserve its
        # record; it is not counted as mathematically validated inventory.
        if q.get(':question/math-academy-id')=='q-32242':
            excluded.append({'question':str(q[':question/id']),'reason':'Source unstated first-row negation; retained unchanged'})
            continue
        nq=normalize(q)
        m=v.v.system(nq[':question/problem'])
        rec={'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':nq,
             'generation':{'template':q.get(':question/math-academy-id','committed'), 'response_layout':nq[':question/answer-fields'][0][':answer-field/type'].split('/')[-1], 'classification':v.v.independent_class(m), 'mathematical_fingerprint':fingerprint(nq)}}
        checked=copy.deepcopy(rec)
        for attr in (':question/problem',':question/worked-solution'):
            checked['question'][attr]=v.v.normalize(checked['question'][attr])
        v.validate(checked,replay=False)
        fixtures.append({'label':str(q[':question/id']),'record':rec,'checks':v.native_checks(rec)})
        available[level].append(q)
    save(path/'existing-native-input.json',fixtures)
    subprocess.run([str(HERE/'reference/check-engine'),str(path/'existing-native-input.json'),str(path/'existing-native-report.json')],check=True,capture_output=True)
    result={'basis':basis,'levels':{level:{'rated_gradable_unseen_unreserved':len(rows),'distinct_available_tasks':len({fingerprint(q) for q in rows}),'question_ids':[str(q[':question/id']) for q in rows]} for level,rows in available.items()},'excluded_shown_or_reserved':sorted(unavailable),'source_errors_excluded':excluded}
    save(path/'available-counts.json',result)
    return result

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    after=report[':edb/db-after-t']; kp=read_kp(path/'readback',after)
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text())
    assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question'])
        v.validate(rec)
    assert not transaction([],kp,intent['generator_id'])
    counts=available_counts(path/'readback',kp,after)
    prep=json.loads((path/'preparation.json').read_text())
    for level in LEVELS:
        assert counts['levels'][level]['distinct_available_tasks']>=min(5,prep['available_counts']['levels'][level]['distinct_available_tasks']+prep['new_by_level'][level])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':after,'new_questions':len(records),'by_level':prep['new_by_level'],'available_counts_after':counts,'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result)
    return result

def finish(path, gid, verified, inv):
    prep=json.loads((path/'preparation.json').read_text())
    remaining={l:max(0,5-verified['available_counts_after']['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'by_level':verified['by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'capability_exceptions':prep['capability_exceptions'],'remaining_shortages':remaining,'available_counts_after':verified['available_counts_after'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'generated.json',path/'native-report.json',path/'inventory-after.json',HERE/'validation-current.json',HERE/'classification-current.md',HERE/'capabilities.json')], 'note':'Historical radio evidence retained. Current 14 checkbox layouts and added radio source replayed. New questions are distinct normalized equation systems; source q-32242 error is preserved and excluded from validated counts.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','by_level','remaining_shortages','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'validation-current.json').read_text())
    assert validation['passed'] and all(sha(ROOT/p)==digest for p,digest in validation['hashes'].items())
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists(): continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            recovery=inventory(path/'recovery-inventory-before.json');assert DB.basis()==recovery['basis']
            report=DB._commit(intent,path/'transaction.edn',path)
            finish(path,intent['generator_id'],verify(path,intent,report),inventory(path/'inventory-after.json'))
            return
        inv=inventory(OUT/'inventory-before.json'); b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=json.loads((HERE/'source-current.json').read_text())['record']
        expected={q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']}
        current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        assert set(expected)<=set(current)
        for mid,q in expected.items(): assert canonical(q)==canonical(current[mid]), 'Source changed; reclassify '+mid
        assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        schema=DB.query('[:find ?a ?i :in $ [?i ...] :where [?a :db/ident ?i]]',[[kw(x) for x in ['question-generator/id','question-generator/script','knowledge-point/question-generator','answer/validate','answer-field/validate','question/validate','knowledge-point/validate']]],path,'installed-schema',b);assert len(schema)==7
        registered=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b);assert len(registered)<=1
        gen=kp.get(':knowledge-point/question-generator') or (registered[0][0] if registered else None)
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        if gen: assert gen[':question-generator/script']==SCRIPT
        counts=available_counts(path,kp,b)
        jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
        needed={l:max(0,5-counts['levels'][l]['distinct_available_tasks'],jobs.get(l,{}).get('missing',0)) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated'); supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        assert isinstance(instances,list)
        for rec in instances: v.validate(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        records=[];added={l:0 for l in LEVELS};local=[]
        def select(rec):
            level=rec['question'][':question/difficulty'].split('/')[-1]
            assert level in LEVELS
            fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                v.validate(rec);records.append(rec);used.add(fp);added[level]+=1
        for rec in instances: select(rec)
        # Each level stops after filling its fresh current shortage. A bounded
        # search failure stays explicit rather than counting cosmetic variants.
        for level in LEVELS:
            for i in range(1000):
                rec=g.generate(level,int(JOB.name[:8],16)+i)
                if i<3: v.validate(rec);local.append(rec)
                select(rec)
                if added[level]==needed[level] and i>=2: break
        exceptions=[{'difficulty':l,'requested':needed[l],'produced':added[l],'bounded_search_attempts':1000,'reason':'No further distinct eligible task found in the bounded search; shortage remains explicit'} for l in LEVELS if added[l]<needed[l]]
        save(path/'generated.json',records);save(path/'local-preview.json',local)
        for attr,ids in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            assert len(ids)==len(set(ids))
            if ids: assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(x) for x in ids]],path/'identities',attr.replace('/','-'),b)
        fixtures=[{'label':r['question'][':question/id'],'record':r,'checks':v.native_checks(r)} for r in instances+local+records]
        save(path/'native-input.json',fixtures)
        subprocess.run([str(HERE/'reference/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_counts':counts,'missing_by_level':needed,'new_by_level':added,'new_questions':len(records),'capability_exceptions':exceptions,'asset_hashes':[],'distinctness':'Sorted equations normalized up to nonzero row scale; ignores bank/layout, seed, statement/choice order, identities and row order. Arbitrary row combinations change assessed arithmetic.','source_evidence_unchanged':True})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'by_level':added,'available_counts_after':counts,'no_changes':True}
            save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f: f.write(tx);f.flush();os.fsync(f.fileno())
        preview_result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(preview_result.stdout)
        pr=loads(preview_result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'classification-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__': main()


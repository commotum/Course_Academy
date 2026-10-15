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
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'c5c29fedd7ecd7b0202ac2bfe89879f056870ccc9444d9771bad4f7a27a3d252'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env = database_environment('math')
NATIVE = ROOT / '.local/graph-explorer/learning-64e7aa312fccadb0'
ENGINE = HERE / 'reference/check-engine-current'
QUERY = (HERE / 'reference/source-query.edn').read_text()

def read_kp(path,basis):
    return DB.query(QUERY,[[KP]],path,'kp',basis)[0][0]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

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

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t']
    kp=read_kp(path/'readback',basis)
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
        check(rec)
    assert not transaction([],kp,intent['generator_id'])
    stock=counts(kp,path/'after-stock',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in g.LEVELS},'available_after':stock['available'],'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result)
    return result

def semantics(value):
    if isinstance(value,dict):return {str(k):semantics(x) for k,x in value.items() if str(k)!=':db/id'}
    if isinstance(value,(list,tuple)):return sorted((semantics(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def task_key(p):
    # Ignore orientation, units, side order, field layout, bank, seed and level.
    return g.digest({'supplied_outer':p['outer'],'Q':p['quadrilateral']} if 'outer' in p else {'sides':sorted([p['a'],p['b']]),'angle':p['angle'],'Q':p['quadrilateral']})

def published(rec):
    rec=copy.deepcopy(rec)
    library=ImageLibrary()
    for asset in rec['generation']['plot_assets'].values():
        ref=library.put_file(asset,expected_sha256=sha(Path(asset)))
        assert (library.math_root/ref).read_bytes()==Path(asset).read_bytes()
        rec['question'][':question/problem']=rec['question'][':question/problem'].replace(asset,ref)
    return rec

def check(rec):
    assert rec['knowledge_point']['db_id']==KP
    meta=rec['generation'];assert meta['eligible_for_learning'] and not meta['evidence_only'] and meta['bank_profile']=='method'
    v.check(rec)
    level=rec['question'][':question/difficulty'].split('/')[-1]
    expected=g.generate(level,meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
    assert ordered(rec['question']) in (ordered(expected['question']),ordered(published(expected)['question']))
    assert meta['parameter_fingerprint']==expected['generation']['parameter_fingerprint']

def native(rec):
    f=rec['question'][':question/answer-fields'][0]
    if f[':answer-field/type']==':answer-field.type/radio':
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every owned choice'} for a in f[':answer-field/choices']]
    else:
        value=f[':answer-field/choices'][0][':answer/value']
        checks=[{'submitted':value,'expected':'accepted','purpose':'canonical integer'},{'submitted':str(int(value)+1),'expected':'rejected','purpose':'wrong area'},{'submitted':value+'+0','expected':'rejected','purpose':'rounding form requirement'},{'submitted':' '+value+' ','expected':'accepted','purpose':'whitespace normalization'}]
    return {'label':rec['question'][':question/id'],'record':rec,'checks':checks}

USAGE_QUERY='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historical-usage',basis,history=True))
    known={r['question'][':question/id']:r for file in OUT.glob('basis-*/generated.json') for r in json.loads(file.read_text())}
    groups={level:{} for level in g.LEVELS};eligible=[];excluded=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if sid in g.QS and sid not in ('q-18192','q-285754','q-285769','q-285786'):
            assert semantics(q)==semantics(g.QS[sid]),'Source changed; reclassify'
            p=g.CFG[sid]['parameters'];correct=q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
            assert int(__import__('re').match(r'\d+',correct).group())==g.calculation(p)[2]
            rec=g.generate('hard',template=sid,parameters=p,profile='raw_'+sid)
            assert all(rec['question'].get(k)==q.get(k) for k in (':question/problem',':question/worked-solution'))
        elif str(q[':question/id']) in known:
            rec=known[str(q[':question/id'])];assert normalize(q)==ordered(rec['question']);check(rec);p=rec['generation']['parameters']
        else:
            excluded.append({'source_id':sid,'question_id':str(q[':question/id']),'reason':'unrated with no key or worked solution' if sid=='q-18192' else 'known source unit typo or side-label mismatch; preserved as evidence' if sid in ('q-285754','q-285769','q-285786') else 'unverified content'})
            continue
        eligible.append(rec)
        if q[':db/id'] not in unavailable and q[':db/id']!=kp[':knowledge-point/canonical-example'][':db/id']:
            level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
            groups[level].setdefault(task_key(p),[]).append(q[':db/id'])
    save(path/'stock-native-input.json',[native(r) for r in eligible])
    subprocess.run([str(ENGINE),str(path/'stock-native-input.json'),str(path/'stock-native-report.json')],check=True)
    result={'basis':basis,'available':{level:len(tasks) for level,tasks in groups.items()},'tasks':groups,'excluded_shown_or_reserved':sorted(unavailable),'excluded_unusable':excluded}
    save(path/'available-counts.json',result);return result

def finish(path,gid,verified,inv):
    remaining={l:max(0,5-n) for l,n in verified['available_after'].items()}
    result={'outcome':'generated' if not any(remaining.values()) else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'by_level':verified['by_level'],'available_after':verified['available_after'],'supported_levels':list(g.LEVELS),'unsupported_levels':[],'remaining_shortage':remaining,'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'inventory_recheck_basis':inv['basis'],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',HERE/'validation.json',HERE/'capabilities.json')],'limitations':json.loads((HERE/'validation.json').read_text())['limitations'],'note':'Easy and moderate are documented same-area-difference scaffolds. Opaque historical banks and the incomplete unrated q-18192 remain source evidence only. All source questions and learner history preserved.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
    assert json.loads((HERE/'validation.json').read_text())['status']=='passed'
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                assert intent['exact_edn']==(path/'transaction.edn').read_text()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.REC[':knowledge-point/id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        assert set(current)==set(g.QS),'New sources require reclassification'
        assert all(semantics(current[sid])==semantics(q) for sid,q in g.QS.items())
        assert semantics(kp[':knowledge-point/canonical-example'])==semantics(g.REC[':knowledge-point/canonical-example'])
        stock=counts(kp,path/'before-stock',b);needed={level:max(0,5-n) for level,n in stock['available'].items()}
        print(json.dumps({'basis':b,'available':stock['available'],'needed':needed}),flush=True)
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        used={task_key(c['parameters']) for c in g.CFG.values()}
        used.add(task_key({'a':25,'b':32,'angle':70,'quadrilateral':300}))
        records=[];selected={level:0 for level in needed}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        for rec in instances:
            check(rec);level=rec['question'][':question/difficulty'].split('/')[-1];fp=task_key(rec['generation']['parameters'])
            if selected[level]<needed[level] and fp not in used:records.append(rec);used.add(fp);selected[level]+=1
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated':len(instances)})
        for level in g.LEVELS:
            for seed in range(1000):
                if selected[level]>=needed[level]:break
                rec=g.generate(level,seed=615000+seed);fp=task_key(rec['generation']['parameters'])
                if fp in used:continue
                check(rec);records.append(rec);used.add(fp);selected[level]+=1
        # Bounded generation; a genuine exception remains explicit in the result.
        save(path/'capability-exception.json',{'bounded_attempts_per_level':1000,'remaining':{l:needed[l]-selected[l] for l in g.LEVELS}})
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        assert not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'generated-identities',b) if ids else True
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or (gen and len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT)
        records=[published(r) for r in records]
        for rec in records:check(rec)
        assets=[{'source_path':asset,'reference':ImageLibrary().put_file(asset),'sha256':sha(Path(asset))} for r in records for asset in r['generation']['plot_assets'].values()]
        save(path/'generated.json',records);save(path/'native-input.json',[native(rec) for rec in instances+records])
        subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records))
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_before':stock['available'],'missing_by_level':needed,'selected_by_level':selected,'new_questions':len(records),'asset_hashes':assets,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'native_engine_sha256':sha(ENGINE),'distinctness':'Assessed inputs (supplied outer/Q or sides/included angle/Q), ignoring unit, orientation, seed, level, bank and order; source and canonical tasks excluded.'})
        if '--prepare-only' in sys.argv:print(str(path),flush=True);return
        forms=transaction(records,kp,gid);assert forms
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        previewed=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(previewed.stdout);pr=loads(previewed.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'inventory-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path)
        verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()

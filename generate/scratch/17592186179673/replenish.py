"""This KP only: validated additive content, registered generator, exact durable receipts."""
import copy, fcntl, hashlib, importlib.util, json, os, subprocess, sys, threading, uuid
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
g=v.G;C=v.C;S=g.S
KP=g.KP_ID;LEVELS=('easy','moderate','hard')
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE=g.SNAPSHOT['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'ad92d23f231f39da07bbc49b102301cd5f3907c03d8f76bbcab8ff05beb1f652'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'
GRADER=HERE/'reference/check-engine'
QUERY=(OUT/'source-query.edn').read_text()
EXCLUDED_SOURCES={'q-124656':'Two distinct displayed integral choices both evaluate to zero; preserve original, exclude from usable stock.',
'q-124657':'Source omits endpoint improper-integral qualification; conservative exclusion from validated regular practice.',
'q-124665':'Source omits endpoint improper-integral qualification; conservative exclusion from validated regular practice.'}
USAGE_QUERY="""[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

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

def canonical(value):
    if isinstance(value,dict) and ':db/ident' in value:return {':db/ident':str(value[':db/ident'])}
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items() if str(k) not in (':knowledge-point/_questions',':knowledge-point/_canonical-example')}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def native_record(rec):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':rec['question'][':question/id'],'record':rec,'checks':[
        {'submitted_answer_id':a[':answer/id'],
         'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
         'purpose':'every field-owned radio choice'} for a in f[':answer-field/choices']]}

def fingerprint(q):
    if q.get(':question/math-academy-id')=='e-7035':
        P=C.y/(C.x**2+C.y**2);Q=-C.x/(C.x**2+C.y**2)
        a=b=S.Integer(2);lo=S.Integer(0);hi=S.pi/2;assessment='value'
    else:
        P,Q=C.printed_oneform(q[':question/problem'])
        a,b,lo,hi=C.printed_geometry(q[':question/problem'])
        d=q.get(':question/difficulty')
        if isinstance(d,dict):d=str(d[':db/ident'])
        assessment='setup' if d==':question.difficulty/easy' else 'value'
    # Normalize mathematical objects, ignoring spelling, seed, bank and identities.
    # Angles are already the unique CCW arc at the displayed endpoint pair.
    return hashlib.sha256(json.dumps([assessment]+[S.srepr(S.simplify(z)) for z in (P,Q,a,b,lo,hi)]).encode()).hexdigest()

def check(rec):
    assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.KP_UUID
    assert not rec['generation']['raw_ambiguous_bank'],'Ambiguous raw replay is evidence only'
    assert rec['question'][':question/difficulty'].split('/')[-1] in LEVELS
    if rec['generation']['authored']:
        level=rec['question'][':question/difficulty'].split('/')[-1]
        g.guard(level,rec['generation']['parameters'])
    else:
        assert not set(rec['generation']['source_ids'])&{'q-124657','q-124665'},'Omitted endpoint qualification'
    v.check(rec)
    # The saved instance must be reproducible from its declared parameters.
    regenerated=g.generate(rec['question'][':question/difficulty'].split('/')[-1],
        seed=rec['generation']['seed'],template=rec['generation']['template'],
        parameters=rec['generation']['parameters'],profile=rec['generation']['profile'])
    assert ordered(regenerated['question'])==ordered(rec['question'])
    return fingerprint(rec['question'])

def counts(kp,path,basis,known=()):
    unavailable={row[0] for row in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    known={r['question'][':question/id']:r for r in known}
    rows={level:[] for level in LEVELS};excluded=[];fixtures=[]
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id');qid=str(q[':question/id'])
        if q[':db/id'] in unavailable:
            excluded.append({'question':qid,'reason':'shown or reserved'});continue
        if q.get(':knowledge-point/_canonical-example') or ':question/difficulty' not in q:
            excluded.append({'question':qid,'reason':'canonical or unrated'});continue
        if mid in EXCLUDED_SOURCES:
            excluded.append({'question':qid,'source':mid,'reason':EXCLUDED_SOURCES[mid]});continue
        if mid in g.SOURCES:
            level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
            rec=g.generate(level,template=mid,parameters={'c':1})
            # Full source equality is verified before this count and at readback.
        elif qid in known:
            rec=known[qid];assert normalize(q)==ordered(rec['question'])
        else:
            excluded.append({'question':qid,'reason':'not independently validated by this package'});continue
        level=rec['question'][':question/difficulty'].split('/')[-1]
        rows[level].append((fingerprint(q),qid));fixtures.append(native_record(rec))
    save(path/'inventory-native-input.json',fixtures)
    subprocess.run([str(GRADER),str(path/'inventory-native-input.json'),str(path/'inventory-native-report.json')],check=True)
    result={'basis':basis,'distinct_available':{l:len({fp for fp,_ in rows[l]}) for l in LEVELS},
            'available_ids':{l:[qid for _,qid in rows[l]] for l in LEVELS},'excluded':excluded,
            'shown_or_reserved':sorted(unavailable),'canonical_excluded':True}
    save(path/'available-counts.json',result);return result

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items()),'Existing questions changed'
    assert {k:z for k,z in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:z for k,z in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    assert len({fingerprint(rec['question']) for rec in records})==len(records)
    old_tasks={fingerprint(q) for q in old.values()};old_tasks.add(fingerprint(before[':knowledge-point/canonical-example']))
    for rec in records:
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q)==ordered(rec['question'])
        assert fingerprint(q) not in old_tasks
        check(rec)
    assert not transaction([],kp,intent['generator_id'])
    stock=counts(kp,path/'readback',basis,records)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),
            'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},
            'unchanged_source_questions':len(old),'learner_history_unchanged':True,
            'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,
            'repeat_preparation_content_changes':0,'available_counts_after':stock}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['distinct_available'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,
        'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,
        'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],
        'new_by_level':verified.get('new_by_level',{}),'supported_levels':list(LEVELS),
        'observed_levels':['easy','moderate'],'authored_levels':['hard'],'unsupported_levels':[],
        'capability_exceptions':[],'available_by_level':after['distinct_available'],
        'shortage_by_level':remaining,'source_exclusions':EXCLUDED_SOURCES,
        'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
        'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',
            path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',
            path/'inventory-after.json',path/'native-report.json',path/'generated.json',
            HERE/'validation.json',HERE/'revalidation.log',HERE/'capabilities.json',HERE/'classification.md',
            HERE/'template-extraction.md',HERE/'reference/freeze.json',HERE/'reference/engine-build.json',
            path/'native-input-current-engine-report.json',path/'inventory-native-input-current-engine-report.json',
            path/'generated-review.md') if p.exists()],
        'note':'Validated existing generator reused. Exact basis-guarded application-contributor request and receipt retained. All source questions and learner history preserved. Ambiguous and endpoint-singular raw source profiles excluded from usable stock.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['passed'] and validation['script_sha256']==sha(HERE.with_suffix('.py'))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application api.lock acquired; rechecking inventory and basis',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=g.SNAPSHOT['record'];current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:
            assert canonical(current[q[':question/math-academy-id']])==canonical(q),'Source changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(captured[':knowledge-point/canonical-example'])
        sources=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(sources)==1
        registration=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',basis)
        assert len(registration)<=1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(registration[0][0][':question-generator/id']) if registration else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not collision or collision[0][0][':question-generator/script']==SCRIPT
        if gen:assert gen[':question-generator/script']==SCRIPT
        stock=counts(kp,path,basis);needed={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:check(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        records=[];added={l:0 for l in LEVELS}
        for rec in instances:
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:records.append(rec);used.add(fp);added[level]+=1
        seedbase=int(JOB.name[:8],16)
        for level in LEVELS:
            for offset in range(100):
                if added[level]>=needed[level]:break
                rec=g.generate(level,seed=seedbase+offset);fp=fingerprint(rec['question'])
                if fp in used:continue
                check(rec);records.append(rec);used.add(fp);added[level]+=1
        ids=[uuid.UUID(z) for r in records for z in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        matches=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not matches,'Existing generated identities require reconciliation'
        save(path/'generated.json',records)
        save(path/'native-input.json',[native_record(r) for r in records])
        subprocess.run([str(GRADER),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'source_eid':sources[0][0],
            'available_counts':stock,'missing_by_level':needed,'new_by_level':added,'assets':[],
            'source_exclusions':EXCLUDED_SOURCES,'source_evidence_unchanged':True,
            'source_basis':g.SNAPSHOT['basis'],'validation_sha256':sha(HERE/'validation.json'),
            'distinctness':'Simplified one-form P,Q, ellipse axes, directed arc and setup/value response; ignores seed, UUIDs, bank and option order.'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_after':basis,'new_questions':0,'available_counts_after':stock}
            save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis
        check_report(pr,path/'preview-check',sources[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':ENV['EDB_ENDPOINT'],'lineage':LINEAGE,'source':SOURCE,'source_eid':sources[0][0],
            'basis':basis,'expected_basis':basis,'request_key':'circle-ellipse-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),
            'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,
            'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),
            'question_uuids':[r['question'][':question/id'] for r in records],
            'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),
            'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()

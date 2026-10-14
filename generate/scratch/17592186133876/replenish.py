"""Additive, locked replenishment for the validated 2D divergence package."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'))
from serve_graph_explorer import database_environment
from inventory_jobs import save
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps,loads,kw
spec=importlib.util.spec_from_file_location('divergence_validation',HERE/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard')
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'050ab4de4a3f6dbf9f2e50f341c7e2f683dfa930d122e7c1156232e0419571fb'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env=database_environment('math')
NATIVE=ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'
QUERY=(HERE/'reference/source-query.edn').read_text()
POOL=ROOT/'generate/scratch/17592186110754/check-pool'
ENGINE=ROOT/'generate/runs/current/check-engine'


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
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def source_shape(current, captured):
    # Source projections did not include all optional reverse refs or enum entity IDs.
    if isinstance(captured,dict):
        assert set(captured)<=set(current), 'Captured fact disappeared'
        return {k:source_shape(current[k],v) for k,v in captured.items()}
    if isinstance(captured,list):
        if captured and isinstance(captured[0],dict) and ':db/id' in captured[0]:
            byid={v[':db/id']:v for v in current}
            assert len(current)==len(captured)
            return canonical([source_shape(byid[v[':db/id']],v) for v in captured])
        return canonical(current)
    return canonical(current)

def scoped(kp,b,seen):
    entities={};enums={};next_enum=1
    def enum(value):
        nonlocal next_enum
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            enums[name]=next_enum;entities[str(next_enum)]={'db/ident':name};next_enum+=1
        return enums[name]
    def question(q):
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]}
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        entities[str(q[':db/id'])]=r
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id'])
            field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]}
            if ':answer-field/correct' in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            entities[str(f[':db/id'])]=field
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:question(q)
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}

def available(kp,b,path):
    path.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],path,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],path,'reserved',b)
    seen={row[0] for row in shown+reserved};save(path/'scoped-snapshot.json',scoped(kp,b,seen))
    subprocess.run([str(POOL),str(path/'scoped-snapshot.json'),str(path/'available-counts.json')],check=True,timeout=55,capture_output=True,text=True)
    return json.loads((path/'available-counts.json').read_text())

def fingerprint(q):
    q=copy.deepcopy(q)
    q[':question/problem']=re.sub(r'\\mathbf\s*\{([Fij])\}',r'\1',q[':question/problem'])
    P,Q,pt=v.displayed_object(q,True)
    data=[sp.srepr(sp.simplify(sp.diff(P,v.x))),sp.srepr(sp.simplify(sp.diff(Q,v.y))),None if pt is None else [sp.srepr(sp.simplify(z)) for z in pt]]
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()

def validate_instance(rec):
    meta=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS and meta['eligible_for_learning'] and not meta['evidence_only']
    assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.SOURCE[':knowledge-point/id']
    v.audit_record(rec)
    replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
    assert ordered(replay['question'])==ordered(rec['question']) and replay['generation']==meta
    assert fingerprint(replay['question'])==fingerprint(rec['question'])

def native_checks(records,path):
    path.mkdir(parents=True,exist_ok=True)
    save(path/'native-input.json',[v.engine_checks(r,r['question'][':question/id']) for r in records])
    r=subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],text=True,capture_output=True,check=True,timeout=55)
    (path/'native.log').write_text(r.stdout+r.stderr)
    report=json.loads((path/'native-report.json').read_text())
    assert report['documented_unresolved_checks']==0
    save(path/'runtime.json',{'binary':str(ENGINE.relative_to(ROOT)),'sha256':sha(ENGINE),'sympy':sp.__version__,'python':sys.version})
    return report

def counts(kp,path,basis):
    engine=available(kp,basis,path/'engine-pool')
    pool_ids={e for ids in engine['available_ids_by_level'].values() for e in ids}
    known={r['question'][':question/id']:r for file in OUT.glob('basis-*/generated.json') for r in json.loads(file.read_text())}
    rows={l:[] for l in LEVELS};excluded=[];grade=[]
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id')
        if q[':db/id'] not in pool_ids:
            excluded.append({'id':str(q[':question/id']),'source_id':mid,'reason':'native pool excludes unrated, ungradable, canonical, shown or reserved question'})
            continue
        if mid in g.SOURCE_BY_ID:
            if mid=='q-123175':
                excluded.append({'source_id':mid,'reason':'real logarithm undefined at supplied point'});continue
            try:v.displayed_object(q,False)
            except AssertionError:
                excluded.append({'source_id':mid,'reason':'standalone prompt lacks supplied vector field'});continue
            level,f,_=g.FAMILIES[mid]
            rec=g.generate(level,template=f,parameters={'c':1},profile='raw:'+mid)
            v.audit_record(rec,True)
        else:
            rec=known[str(q[':question/id'])]
            assert normalize(q)==ordered(rec['question']);validate_instance(rec)
        grade.append(rec)
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1];rows[level].append(q)
    native_checks(grade,path/'available-grading')
    result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fingerprint(q) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]} for l,qs in rows.items()},'excluded':excluded,'engine_pool':engine,'deduplication':'ordered simplified component derivatives and exact evaluation point; no bank, seed or choice order'}
    save(path/'available-counts.json',result)
    return result

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read_kp(path/'readback',b)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:x for k,x in before.items() if k not in excluded}=={k:x for k,x in kp.items() if k not in excluded}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question']);validate_instance(rec)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',b)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());after=verified['available_counts_after']
    remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'unsupported_levels':[],'unsupported_levels_filled':False,'capability_exceptions':prep['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'native-report.json',path/'generated.json',HERE/'registration.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',OUT/'readiness.json'] if p.exists()],'note':'Hard is a validated same-method authored extension; source difficulty absence is not treated as unsupported. Incomplete/context-dependent and real-domain-invalid sources are preserved and excluded from validated standalone reserves. The original unrated record remains unchanged, so the application may still report its classification job.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def main():
    qa=json.loads((ROOT/'generate/runs/current/qa'/f'{KP}.json').read_text())
    assert qa['parent_review']=='passed' and qa['generator_sha256']==sha(HERE.with_suffix('.py'))
    for rel,digest in qa['root_artifact_sha256'].items():assert sha(ROOT/rel)==digest, 'Frozen artifact changed: '+rel
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed with documented source anomalies' and validation['native_unresolved']==0
    save(OUT/'readiness.json',{'generator_sha256':sha(HERE.with_suffix('.py')),'frozen_hashes_verified':True,'prior_parent_review':'passed','validation':validation,'plot_requirements':'none','native_pool_binary':str(POOL.relative_to(ROOT)),'native_pool_sha256':sha(POOL)})
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True)
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application api.lock acquired',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['lineage']==LINEAGE and intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
            assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path))
            finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis)
        assert str(kp[':knowledge-point/id'])==g.SOURCE[':knowledge-point/id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for mid,q in g.SOURCE_BY_ID.items():assert source_shape(current[mid],q)==canonical(q),'Source changed; reclassify'
        assert source_shape(kp[':knowledge-point/canonical-example'],g.SOURCE[':knowledge-point/canonical-example'])==canonical(g.SOURCE[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        registration=HERE/'registration.json'
        saved_id=json.loads(registration.read_text())['id'] if registration.exists() else str(uuid.uuid5(uuid.UUID(g.SOURCE[':knowledge-point/id']),'question-generator'))
        gid=str(gen[':question-generator/id']) if gen else saved_id
        by_script=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-script',basis)
        assert len(by_script)<=1
        if by_script:
            assert not gen or by_script[0][0][':db/id']==gen[':db/id'];gid=str(by_script[0][0][':question-generator/id'])
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not existing or len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT
        save(registration,{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing),'generator_sha256':sha(HERE.with_suffix('.py'))})
        c=counts(kp,path/'current-inventory',basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        print(json.dumps({'basis':basis,'available':{l:c['levels'][l]['distinct_available_tasks'] for l in LEVELS},'missing':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances;assert isinstance(instances,list)
        for rec in instances:validate_instance(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];added={l:0 for l in LEVELS};attempts={l:0 for l in LEVELS}
        for rec in instances:
            l=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if added[l]<needed[l] and fp not in used:records.append(rec);used.add(fp);added[l]+=1
        for level in LEVELS:
            # Bounded reserve refill, using the existing validated sampler and its documented parameter limits.
            for i in range(256):
                if added[level]>=needed[level]:break
                attempts[level]+=1
                rec=g.generate(level,seed=int(JOB.name[:8],16)+i)
                fp=fingerprint(rec['question'])
                if fp in used:continue
                validate_instance(rec);records.append(rec);used.add(fp);added[level]+=1
        exceptions=[{'level':l,'reason':'bounded 256 validated sampling attempts exhausted','requested':needed[l],'produced':added[l],'remaining':needed[l]-added[l]} for l in LEVELS if added[l]<needed[l]]
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        matched=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'content-identities',basis) if ids else []
        assert not matched,'Existing identities require reconciliation'
        save(path/'generated.json',records)
        (path/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records))+'\n')
        native_checks(records,path)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'sampling_attempts':attempts,'capability_exceptions':exceptions,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':[],'source_evidence_unchanged':True,'source_basis':g.CAPTURE['basis'],'all_selected_instances_mathematically_validated':True,'all_selected_instances_actual_grader_validated':True})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'divergence-2d-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

"""Scoped line-integral inventory replenishment through the installed EDB integration."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.storage import atomic_json,atomic_text
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture'),str(HERE)]
from serve_graph_explorer import database_environment
from database import Database
from edn import dumps,loads,kw
spec=importlib.util.spec_from_file_location('parametric_potential_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'4fbbeb397bf4c6efd4375359fbf24abae43f14be0ecd7693ce844b5fbb4bb3e0'
LOCK=ROOT/'.local/learning/requests/math/api.lock';OUT=ROOT/'reference/generated'/str(KP)/'job-4fbbeb39'
OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
NATIVE=ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e';POOL=ROOT/'generate/scratch/17592186110754/check-pool';ENGINE=ROOT/'generate/runs/current/check-engine'
QUERY=(ROOT/'generate/scratch/17592186133876/reference/source-query.edn').read_text()
CASES={c['source_id']:c for c in json.loads((HERE/'source-cases.json').read_text())}
RAW=json.loads((HERE/'source.json').read_text())['record']
save=atomic_json

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,text=True,capture_output=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read_kp(path,basis):
 rows=DB.query(QUERY,[KP],path,'kp',basis);assert len(rows)==1 and str(rows[0][0][':knowledge-point/id'])==g.KP_UUID;return rows[0][0]

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

def mathematical_key(f,curve,a,b):
    values=[sp.srepr(sp.simplify(value)) for value in (f,*curve,sp.sympify(a),sp.sympify(b))]
    return hashlib.sha256(json.dumps(values).encode()).hexdigest()

def fingerprint(q):
    sid=q.get(':question/math-academy-id')
    if sid in CASES:
        c=CASES[sid];p=c['parameters'];f,curve,a,b=g.components(c['template'],p)
        return mathematical_key(p['scale']*f,curve,a,b)
    if sid=='e-8759':
        return mathematical_key(g.x*g.y**2+2*g.x*g.z,(sp.exp(g.t),g.t,sp.exp(-g.t)),0,1)
    question=normalize(q) if ':db/id' in q else q
    f,curve,a,b,*_=v.displayed_math({'question':question,'generation':{'template':template_for(question)}})
    return mathematical_key(f,curve,a,b)

def template_for(q):
    # Exact generated identity is bound to its reproducible evidence, not guessed
    # from surface notation. Include prepared and committed instances on retry.
    for file in OUT.glob('basis-*/generated.json'):
        for r in json.loads(file.read_text()):
            if r['question'][':question/id']==str(q[':question/id']):return r['generation']['template']
    raise AssertionError('Generated question lacks retained reproducibility evidence')

def validate_instance(rec):
    meta=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
    assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.KP_UUID
    v.check_record(rec)
    f,curve,a,b,*_=v.displayed_math(rec)
    replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
    assert ordered(replay['question'])==ordered(q) and replay['generation']==meta
    return mathematical_key(f,curve,a,b)

def native_record(r):
    field=r['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
    return {'label':r['question'][':question/id'],'record':r,'checks':[
        {'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected',
         'purpose':'complete displayed option selection'} for a in field[':answer-field/choices']]}

def native_checks(records,path):
    path.mkdir(parents=True,exist_ok=True)
    save(path/'native-input.json',[native_record(r) for r in records])
    if not records:return {'accepted_checks':0,'rejected_checks':0,'documented_unresolved_checks':0}
    r=subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True,capture_output=True,text=True,timeout=55)
    atomic_text(path/'native.log',r.stdout+r.stderr)
    report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    return report

def counts(kp,path,basis):
    pool=available(kp,basis,path/'engine-pool')
    eligible={e for ids in pool['available_ids_by_level'].values() for e in ids}
    rows={l:[] for l in LEVELS};excluded=[];checks=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id');qid=str(q[':question/id'])
        if q[':db/id'] not in eligible:
            excluded.append({'id':qid,'source_id':sid,'reason':'native pool excludes shown, reserved, unrated, canonical or ungradable question'});continue
        if sid in ('q-99008','q-104637'):
            excluded.append({'id':qid,'source_id':sid,'reason':'documented source solution typo; preserved unchanged, excluded from validated reserve'});continue
        if sid in CASES:
            c=CASES[sid]
            rec=g.generate(c['difficulty'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
            v.check_record(rec)
            # Grade original identities and values, including historical TeX.
            rec=copy.deepcopy(rec);rec['question']=normalize(q)
        else:
            rec=next(r for file in OUT.glob('basis-*/generated.json') for r in json.loads(file.read_text()) if r['question'][':question/id']==qid)
            assert normalize(q)==ordered(rec['question']);validate_instance(rec)
        checks.append(rec)
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1];rows[level].append(q)
    native_checks(checks,path/'available-grading')
    data={'basis':basis,'distinct_available':{l:len({fingerprint(q) for q in qs}) for l,qs in rows.items()},'available_ids':{l:[str(q[':question/id']) for q in qs] for l,qs in rows.items()},'excluded':excluded,'native_pool':pool,'distinctness':'simplified supplied potential, parametric curve and oriented interval; ignores seed, identities, bank and choice order'}
    data['remaining_shortage']={l:max(0,5-data['distinct_available'][l]) for l in LEVELS}
    save(path/'available-counts.json',data);return data

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read_kp(path/'readback',b)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    omitted={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:x for k,x in before.items() if k not in omitted}=={k:x for k,x in kp.items() if k not in omitted}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question']);validate_instance(rec)
    native_checks(records,path/'readback-grading')
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',b)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());after=verified['available_counts_after'];remaining=after['remaining_shortage']
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_by_level':verified.get('new_by_level',{}),'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'available_counts_before':prep['available_counts']['distinct_available'],'available_counts_after':after['distinct_available'],'remaining_shortage':remaining,'capability_exceptions':prep['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'preparation.json',path/'generated.json',path/'generated.md',path/'native-report.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'readback/available-counts.json',path/'inventory-after.json',HERE/'registration.json',OUT/'readiness.json',OUT/'revalidation.json',OUT/'candidate-review.json',OUT/'candidate-review.md',OUT/'review-assessment.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json') if p.exists()],'note':'Two source solution typos are retained unchanged and excluded from validated reserves. All three supported difficulties meet the five-question reserve only when verified counts say so.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','new_by_level','available_counts_after','remaining_shortage')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass' and validation['native_grading']['unresolved']==0
    qa=json.loads((ROOT/'generate/runs/current/qa'/f'{KP}.json').read_text());assert qa['parent_review']=='passed' and qa['script_sha256']==sha(HERE.with_suffix('.py'))
    assert validation['native_grading']['binary_sha256']==sha(ENGINE)
    save(OUT/'readiness.json',{'parent_review':'passed','validation':validation,'generator_sha256':sha(HERE.with_suffix('.py')),'native_pool_binary':str(POOL.relative_to(ROOT)),'native_pool_sha256':sha(POOL),'sympy':sp.__version__,'python':sys.version,'plots':'none','hard_classification':'Authored bounded extension reviewed in existing parent QA; supplied potential, three variable curve, two nonzero endpoint terms, exact exponential arithmetic.'})
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    if '--inspect' in sys.argv:
        inv=inventory(OUT/'initial-inventory.json');b=inv['basis'];kp=read_kp(OUT/'initial',b);c=counts(kp,OUT/'initial',b);print(json.dumps(c,default=str));return
    with LOCK.open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['lineage']==LINEAGE and intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);atomic_text(path/'before.edn',dumps(kp)+'\n')
        current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for sid,c in CASES.items():assert source_shape(current[sid],g.QS[sid])==canonical(g.QS[sid]),'Source changed; reclassify'
        assert source_shape(kp[':knowledge-point/canonical-example'],RAW[':knowledge-point/canonical-example'])==canonical(RAW[':knowledge-point/canonical-example'])
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        gen=kp.get(':knowledge-point/question-generator');registration=HERE/'registration.json'
        byscript=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-script',b);assert len(byscript)<=1
        saved=json.loads(registration.read_text())['id'] if registration.exists() else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        gid=str(gen[':question-generator/id']) if gen else str(byscript[0][1]) if byscript else saved
        matched=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not matched or len(matched)==1 and matched[0][0][':question-generator/script']==SCRIPT
        save(registration,{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or matched or registration.exists()),'generator_sha256':sha(HERE.with_suffix('.py'))})
        c=counts(kp,path/'current-inventory',b);needed=c['remaining_shortage']
        print(json.dumps({'basis':b,'available':c['distinct_available'],'missing':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances;assert isinstance(instances,list)
        for rec in instances:validate_instance(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];added={l:0 for l in LEVELS};attempts={l:0 for l in LEVELS}
        for rec in instances:
            l=rec['question'][':question/difficulty'].split('/')[-1];fp=validate_instance(rec)
            if added[l]<needed[l] and fp not in used:records.append(rec);used.add(fp);added[l]+=1
        for level in LEVELS:
            for i in range(256):
                if added[level]>=needed[level]:break
                attempts[level]+=1;rec=g.generate(level,seed=int(JOB.name[:8],16)+i)
                key=validate_instance(rec)
                if key in used:continue
                records.append(rec);used.add(key);added[level]+=1
        exceptions=[{'level':l,'reason':'Bounded 256 sampling attempts exhausted inside the validated parameter domain. This is a sampler capability bound, not a proof of mathematical exhaustion.','requested':needed[l],'produced':added[l],'remaining':needed[l]-added[l],'filled':False} for l in LEVELS if added[l]<needed[l]]
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        assert len(ids)==len(set(ids))
        collisions=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'content-identities',b) if ids else []
        assert not collisions,'Existing identity requires reconciliation'
        save(path/'generated.json',records);atomic_text(path/'generated.md','\n\n---\n\n'.join(map(g.markdown,records))+'\n')
        native_checks(instances+records,path)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'sampling_attempts':attempts,'capability_exceptions':exceptions,'distinct_generated_tasks':len(records),'assets':[],'source_evidence_unchanged':True,'generator_sha256':sha(HERE.with_suffix('.py')),'all_selected_instances_mathematically_validated':True,'all_selected_instances_actual_grader_validated':True,'source_basis':g.SOURCE['basis']})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n';atomic_text(txpath,tx)
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        atomic_text(path/'preview.edn',r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'potential-endpoint-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
        save(path/'commit-intent.json',intent)
        verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()

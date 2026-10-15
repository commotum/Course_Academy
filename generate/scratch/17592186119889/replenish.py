"""KP-scoped additive publication through existing EDB integration."""
import copy, fcntl, hashlib, importlib.util, json, os, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from inventory_jobs import save
from serve_graph_explorer import database_environment
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import dumps,loads,kw

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
d=module('surface_db',HERE/'db_support.py');DB=d.DB;DB.env=database_environment('math')
g=module('surface_generator',HERE.with_suffix('.py'))
KP=g.KP_ID;SOURCE=':application/ca-engine'
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'b3655a3a0c623f7ac29e96c42e0ae5e6e34dc7df41d31c23ec9fce392e81acf6'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
NATIVE=Path((ROOT/'generate/scratch/17592186119744/reference/replenishment/native-path.txt').read_text().strip())
LEVELS=('easy','moderate','hard');SUPPORTED=('moderate','hard')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inventory(p):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,text=True,capture_output=True,timeout=55,check=True)
 v=json.loads(r.stdout);assert v['ok'] and v['data']['lineage']==LINEAGE
 save(p,v['data']);return v['data']
def read(p,b):
 k=DB.query('[:find (pull ?k '+d.PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],p,'kp',b)[0][0]
 return k
def normalize(q):
    return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}

def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def scoped(kp,b,seen):
    entities={};enums={}
    def enum(value):
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            e=len(enums)+1;enums[name]=e;entities[str(e)]={'db/ident':name}
        return enums[name]
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]};entities[str(q[':db/id'])]=r
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id']);field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]};entities[str(f[':db/id'])]=field
            if ':answer-field/correct'in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}

def transaction(records,kp,gid):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    else:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,p,source):
    attrs=dict(DB.attributes(p,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution/retraction'
        name=str(attrs[a])
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name

def counts(kp,b,p):
    p.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    save(p/'pool-input.json',scoped(kp,b,{x[0] for x in shown+reserved}))
    subprocess.run([str(ROOT/'generate/scratch/17592186083240/reference/native/check-pool'),str(p/'pool-input.json'),str(p/'pool-report.json')],check=True,capture_output=True,timeout=55)
    pool=json.loads((p/'pool-report.json').read_text())
    result={l:len(pool['available_ids_by_level'].get(l,[])) for l in LEVELS}
    save(p/'counts.json',{'basis':b,'counts':result,'excluded_shown_or_reserved':sorted({x[0] for x in shown+reserved})})
    return result

def validate(records,p):
    p.mkdir(parents=True,exist_ok=True)
    qa=module('surface_validation',HERE/'validate.py');qa.run(records,p)
    for r in records:
        m=r['generation'];q=r['question']
        replay=g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],m['template'],m['parameters'],m['bank_profile'])
        assert ordered(replay['question'])==ordered(q)

def integrand(q):
    qa=module('surface_content_readback',HERE/'validate.py')
    import re,sympy as S
    r=qa.vector(re.search(r'\\langle.*?\\rangle',q[':question/problem']).group()) if r'\langle' in q[':question/problem'] else S.Matrix([qa.scalar(z) for z in re.search('⟨(.*?)⟩',q[':question/problem']).group(1).replace(r'\,','').split(',')])
    cross=r.diff(qa.u).cross(r.diff(qa.v));return S.trigsimp(cross.dot(cross))

def select(candidates,kp,needed):
    qa=module('surface_dedup',HERE/'validate.py');existing=[integrand(q) for q in kp[':knowledge-point/questions']]
    records=[];new={l:0 for l in LEVELS}
    for r in candidates:
        level=r['question'][':question/difficulty'].split('/')[-1];square=integrand(r['question'])
        if new[level]>=needed[level] or any(qa.same(square,x) for x in existing):continue
        records.append(copy.deepcopy(r));existing.append(square);new[level]+=1
    return records,new

def prepare():
    freeze=json.loads((HERE/'reference/validation/validation.json').read_text())
    assert freeze['passed'] and freeze['generator_sha256']==sha(HERE.with_suffix('.py'))
    inv=inventory(OUT/'inventory-before-generation.json');b=inv['basis'];kp=read(OUT/'before-generation',b)
    c=counts(kp,b,OUT/'before-generation');needed={l:max(0,5-c[l]) if l in SUPPORTED else 0 for l in LEVELS}
    old={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
    current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    assert set(old)==set(current)
    for sid in old:assert normalize(old[sid])==normalize(current[sid]),sid
    save(OUT/'source-refresh.json',{'basis':b,'source_basis':g.SOURCE['basis'],'all_source_records_unchanged':True,'source_count':len(old)})
    supplied=JOB.with_suffix('.generated');save(OUT/'supplied-status.json',{'path':str(supplied),'exists':supplied.exists()})
    records=[]
    if supplied.exists():
        obj=json.loads(supplied.read_text());rs=obj.get('instances',[])
        if isinstance(rs,dict):rs=[rs]
        if rs:validate(rs,OUT/'supplied-validation');records.extend(rs)
    # Different integrands, including both observed moderate methods. All other
    # certified domain members remain available for later replenishment.
    for sid,params in [('q-109943',{'a':3,'b':5}),('q-109943',{'a':5,'b':7}),('q-109941',{'a':2})]:
        records.append(g.generate('moderate',seed=100+len(records),template=sid,parameters=params))
    # Fall back to the rest of the finite domain if live state needs more.
    for sid,t in g.TEMPLATES.items():
        if needed[t['level']]>0:
            for params in t['domain']:records.append(g.generate(t['level'],seed=200+len(records),template=sid,parameters=params))
    selected,new=select(records,kp,needed);validate(selected,OUT/'candidate-validation');save(OUT/'candidates.json',selected)
    save(OUT/'pre-generation.json',{'basis':b,'counts':c,'needed_supported':needed,'selected':new,'unsupported_shortage':{'easy':max(0,5-c['easy'])}})
    print(json.dumps({'basis':b,'counts':c,'selected':new}),flush=True)


def finish(p,gid,report,kp):
    b=report[':edb/db-after-t'];before=loads((p/'before.edn').read_text())
    check_report(report,p/'receipt-check',json.loads((p/'commit-intent.json').read_text())['source_eid'])
    prior={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in prior.items()),'Preexisting question changed'
    ignore={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in ignore}=={k:v for k,v in kp.items() if k not in ignore}
    rows=json.loads((p/'generated-published.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    for r in rows:assert normalize(byid[r['question'][':question/id']])==ordered(r['question'])
    assert len(now)==len(prior)+len(rows)
    assert not transaction([],kp,gid),'Repeat preparation must be no-change'
    assert not select(rows,kp,{l:5 for l in LEVELS})[0],'Mathematical dedup must reject committed instances'
    c=counts(kp,b,p/'verified-inventory');inv=inventory(p/'inventory-after.json')
    remaining={l:max(0,5-c[l]) for l in LEVELS}
    verified={'passed':True,'basis_before':report[':edb/db-before-t'],'basis_after':b,'new_questions':len(rows),'counts':c,'source_questions_preserved':len(prior),'learner_changes':0,'source':SOURCE,'repeat_preparation_changes':0,'all_question_field_answer_values_readback_exact':True,'all_datoms_additive_and_scoped':True,'verified_at_exact_db_after':True}
    save(p/'verification.json',verified)
    outcome={'outcome':'generated' if all(c[l]>=5 for l in SUPPORTED) else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'verified_commit_basis':b,'preparation_basis':report[':edb/db-before-t'],'lineage':LINEAGE,'new_questions':len(rows),'supported_levels':list(SUPPORTED),'unsupported_levels':['easy'],'available':c,'shortage_remaining':remaining,'unsupported_shortage':{'easy':remaining['easy']},'capability_exception':{'easy':'No source-backed easy template has been validated; source affine questions are moderate. Bounded capability exception, not evidence of mathematical impossibility. Reopen with new source evidence.'},'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'application_contributor':SOURCE,'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',OUT/'candidate-validation/validation.json',OUT/'candidate-validation/grading-report.json',OUT/'source-refresh.json',HERE/'capabilities.json',HERE/'reference/validation/validation.json',HERE/'reference/validation/source-bank-fidelity.json']]}
    save(p/'outcome.json',outcome);save(JOB.with_suffix('.result'),outcome);print(json.dumps(outcome,indent=2),flush=True)

def commit():
    frozen=json.loads((HERE/'freeze.json').read_text());assert frozen['script_sha256']==sha(HERE.with_suffix('.py'))
    candidates=json.loads((OUT/'candidates.json').read_text())
    validate(candidates,OUT)
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Acquired application api.lock',flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
            assert intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,p/'transaction.edn',p)
            finish(p,intent['generator_id'],report,read(p/'readback',report[':edb/db-after-t']));return
        inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b
        p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True)
        kp=read(p,b);(p/'before.edn').write_text(dumps(kp)+'\n')
        captured={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
        current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
        assert set(captured)==set(current) and all(normalize(captured[sid])==normalize(current[sid]) for sid in captured),'Source evidence changed; reclassify before submission'
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c[l]) if l in SUPPORTED else 0 for l in LEVELS}
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT
            gid=str(existing[0][0][':question-generator/id'])
        source=DB.query('[:find ?s :where [?s :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        records,new=select(candidates,kp,needed)
        validate(records,p/'selected-validation')
        identities=[uuid.UUID(x) for r in records for x in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if identities:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[identities],p,'identities',b)
        assets=[]
        save(p/'assets.json',assets);save(p/'generated-published.json',records)
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'current_available':c,'needed':needed,'new':new,'supported_levels':list(SUPPORTED),'unsupported_levels':['easy'],'source':SOURCE,'generator_sha256':sha(HERE.with_suffix('.py')),'grading_and_math_evidence':str(OUT/'candidate-validation/validation.json')})
        forms=transaction(records,kp,gid);assert forms,'No transaction needed; reconcile existing registration'
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        assert DB.basis()==b
        run=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,timeout=55)
        (p/'preview.log').write_text(run.stderr)
        if run.returncode:raise RuntimeError(run.stderr)
        (p/'preview.edn').write_text(run.stdout);pr=loads(run.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'basis':b,'expected_basis':b,'source':SOURCE,'source_eid':source[0][0],'request_key':'surface-integrand-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(p/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,p)
        finish(p,gid,report,read(p/'readback',report[':edb/db-after-t']))

if __name__=='__main__':
    if '--commit' in sys.argv:commit()
    else:prepare()

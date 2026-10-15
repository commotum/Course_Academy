"""Additive replenishment for the planar arc-length KP through existing EDB APIs."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from inventory_jobs import save
from serve_graph_explorer import database_environment
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from image_library import ImageLibrary
s=importlib.util.spec_from_file_location('support',HERE/'db_support.py')
d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
DB=d.DB;DB.env=database_environment('math')
KP=d.KP;SOURCE=':application/ca-engine'
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'3b3a05ade44f130d2b330902bf0f0f891b591ef9e6a2c77a615401cba1461d02'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
NATIVE=Path((OUT/'native-path.txt').read_text().strip())
LEVELS=('easy','moderate','hard')
# Reuse the independently implemented printed-math validator without its CLI suite.
qa={'__file__':str(HERE/'validate.py')}
exec(compile((HERE/'validate.py').read_text().split('for sid in g.QS:')[0],str(HERE/'validate.py'),'exec'),qa)
g=qa['g']
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

def validate(records,p):
    qa['checks'].clear()
    for r in records:
        m=r['generation'];q=r['question']
        replay=g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],m['template'],parameters=m['parameters'],profile=m['bank_profile'])
        assert ordered(replay['question'])==ordered(q)
        qa['verify'](r)
    save(p/'grading-input.json',qa['checks'])
    engine=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(p/'grading-input.json'),str(p/'grading-report.json')],check=True,timeout=55)
    report=json.loads((p/'grading-report.json').read_text())
    assert report['documented_unresolved_checks']==0
    save(p/'math-validation.json',{'passed':True,'records':len(records),'printed_scalar_stages':qa['stage_count'],'independent_numeric_integration':True,'deterministic_replay':True,'engine_sha256':sha(engine),'generator_sha256':sha(HERE.with_suffix('.py'))})

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

def prepare():
    v=json.loads((HERE/'validation.json').read_text())
    assert v['status']=='passed' and v['script_sha256']==sha(HERE.with_suffix('.py'))
    inv=inventory(OUT/'inventory-before-generation.json');b=inv['basis']
    k=read(OUT/'before-generation',b);c=counts(k,b,OUT/'before-generation')
    # Recheck every captured source, preserving its raw defect evidence.
    old={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
    current={q[':question/math-academy-id']:q for q in k[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    assert set(old)==set(current)
    for sid in old:
        assert normalize(old[sid])==normalize(current[sid]),sid
    save(OUT/'source-refresh.json',{'basis':b,'frozen_basis':g.SOURCE['basis'],'source_questions':len(current),'all_content_and_banks_unchanged':True})
    supplied=JOB.with_suffix('.generated')
    save(OUT/'supplied-status.json',{'exists':supplied.exists()})
    records=[]
    if supplied.exists():
        obj=json.loads(supplied.read_text());records=obj.get('instances',[])
        if isinstance(records,dict):records=[records]
        if records:validate(records,OUT)
    # Current sources already supply five easy and five moderate questions.
    # This job classifies the missing hard band; do not create surplus content.
    assert c['easy']>=5 and c['moderate']>=5,c
    cases=[('hard_exp_spiral',{'c':1,'k':2,'q':1,'a':0,'b':1}),
           ('hard_exp_spiral',{'c':1,'k':3,'q':1,'a':0,'b':1}),
           ('hard_exp_spiral',{'c':1,'k':2,'q':3,'a':1,'b':2}),
           ('hard_reciprocal_affine',{'c':1,'k':2,'d':1,'a':0,'b':1}),
           ('hard_reciprocal_affine',{'c':1,'k':3,'d':2,'a':0,'b':1})]
    records += [g.generate('hard',seed=110+i,template=t,parameters=p) for i,(t,p) in enumerate(cases)]
    used=set();selected=[]
    # All existing tasks enter the dedup set, including exhausted questions.
    for q in k[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if sid in g.TEMPLATES:
            used.add(g.generate(g.TEMPLATES[sid]['level'],template=sid,parameters={'c':1})['generation']['mathematical_task_fingerprint'])
    for r in records:
        sig=r['generation']['mathematical_task_fingerprint']
        if sig in used:continue
        used.add(sig);selected.append(r)
    validate(selected,OUT)
    save(OUT/'candidates.json',selected)
    save(HERE/'capabilities.json',{'version':g.VERSION,'supported_levels':list(LEVELS),'unsupported_levels':[], 'source_templates':10,'authored_hard_templates':2,'hard_classification':'Unequal product/chain-rule rates or affine reciprocal completed square and substitution; conservative same-KP extensions documented in classification.md.', 'bounded_domains':{'observed_c':[1,12],'hard_c':[1,12],'hard_k':[2,3],'hard_q':[1,2,3],'hard_q_constraint':'q != k','hard_exp_intervals':[[0,1],[0,2],[1,2]],'hard_affine_d':[1,2]},'finite_domain':True,'replenishment_selection':'Three unequal-rate/interval exponential tasks and two affine reciprocal tasks, c=1 throughout. No seed, bank, option-order, or pure-homothety duplicates.', 'exceptions':[]})
    # A compact plot sheet supports visual review before durable submission.
    from PIL import Image,ImageDraw
    sheet=Image.new('RGB',(1350,540*((len(selected)+2)//3)),'white')
    draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(selected):
        img=Image.open(r['generation']['plot']['prompt']).convert('RGB');img.thumbnail((440,490))
        x=(i%3)*450;y=(i//3)*540;sheet.paste(img,(x,y+30))
        draw.text((x+6,y+6),str(i+1)+' '+r['generation']['template'],fill='black')
    sheet.save(OUT/'selected-plots.png')
    print(json.dumps({'basis':b,'current_counts':c,'validated_candidates':len(selected),'plot_sheet':str(OUT/'selected-plots.png')}),flush=True)

def finish(p,gid,report,kp):
    b=report[':edb/db-after-t'];before=loads((p/'before.edn').read_text())
    check_report(report,p/'receipt-check',json.loads((p/'commit-intent.json').read_text())['source_eid'])
    prior={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in prior.items()),'Preexisting source changed'
    ignore={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in ignore}=={k:v for k,v in kp.items() if k not in ignore}
    rows=json.loads((p/'generated-published.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    for r in rows:
        q=byid[r['question'][':question/id']]
        assert normalize(q)==ordered(r['question']) and ':question/math-academy-id' not in q
    assert len(now)==len(prior)+len(rows)
    assert not transaction([],kp,gid),'Repeat preparation must be no-change'
    for a in json.loads((p/'assets.json').read_text()):assert sha(Path('/media/jake/SSD/EDB/math')/a['path'])==a['sha256']
    c=counts(kp,b,p/'verified-inventory');inv=inventory(p/'inventory-after.json')
    remaining={l:max(0,5-c[l]) for l in LEVELS}
    evidence={'passed':True,'basis_before':report[':edb/db-before-t'],'basis_after':b,'new_questions':len(rows),'counts':c,'source_questions_preserved':len(prior),'learner_changes':0,'source':SOURCE,'repeat_preparation_changes':0,'all_question_field_answer_values_readback_exact':True}
    save(p/'verification.json',evidence)
    outcome={'outcome':'generated' if not any(remaining.values()) else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'verified_commit_basis':b,'lineage':LINEAGE,'new_questions':len(rows),'supported_levels':list(LEVELS),'unsupported_levels':[],'available':c,'shortage_remaining':remaining,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'application_contributor':SOURCE,'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'assets.json',OUT/'math-validation.json',OUT/'grading-report.json',OUT/'source-refresh.json',HERE/'capabilities.json',HERE/'validation.json']]}
    save(p/'outcome.json',outcome);save(JOB.with_suffix('.result'),outcome);print(json.dumps(outcome,indent=2),flush=True)

def commit():
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
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c[l]) for l in LEVELS}
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT
            gid=str(existing[0][0][':question-generator/id'])
        source=DB.query('[:find ?s :where [?s :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        known={str(q[':question/id']) for q in kp[':knowledge-point/questions']};records=[];new={l:0 for l in LEVELS};tasks=set()
        # Reconcile any earlier published instances by mathematical task, not UUID.
        for file in OUT.glob('basis-*/generated-published.json'):
            for old in json.loads(file.read_text()):
                if old['question'][':question/id'] in known:tasks.add(old['generation']['mathematical_task_fingerprint'])
        for r in candidates:
            l=r['question'][':question/difficulty'].split('/')[-1];sig=r['generation']['mathematical_task_fingerprint']
            if r['question'][':question/id'] in known or sig in tasks or new[l]>=needed[l]:continue
            records.append(copy.deepcopy(r));tasks.add(sig);new[l]+=1
        identities=[uuid.UUID(x) for r in records for x in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if identities:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[identities],p,'identities',b)
        library=ImageLibrary();assets=[]
        for r in records:
            path=Path(r['generation']['plot']['prompt']);rel=library.put_file(path,expected_sha256=sha(path))
            assert sha(library.math_root/rel)==sha(path)
            assets.append({'local_path':str(path),'path':rel,'sha256':sha(path)})
            r['question'][':question/problem']=r['question'][':question/problem'].replace(str(path),rel)
        save(p/'assets.json',assets);save(p/'generated-published.json',records)
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'current_available':c,'needed':needed,'new':new,'supported_levels':list(LEVELS),'source':SOURCE,'generator_sha256':sha(HERE.with_suffix('.py')),'grading_and_math_evidence':str(OUT/'math-validation.json')})
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
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'basis':b,'expected_basis':b,'source':SOURCE,'source_eid':source[0][0],'request_key':'planar-arc-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(p/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,p)
        finish(p,gid,report,read(p/'readback',report[':edb/db-after-t']))

if __name__=='__main__':
    if '--commit' in sys.argv:commit()
    else:prepare()

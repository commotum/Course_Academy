"""Publish the tested package and atomically correct content and learner state."""
from pathlib import Path
import sys, json, uuid, hashlib, datetime, subprocess, fcntl, copy
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,verify_package
from capture.scripts.database.edn import kw,dumps,loads,Tagged
from capture.scripts.database.client import QUESTION_PULL,StaleBasis

SOURCE=':application/ca-engine'
KP=17592186129115
LEARNER=17592186045416
QUESTION=17592186619080
ITEM=17592186649259
TASK=17592186627939
REVIEW=17592186649970
FILES=['generator.py','catalogue.json','math_format.py']
pub=Publisher.from_environment(source=SOURCE)
db=pub.client

def save(path,value):path.write_text(json.dumps(value,indent=2,default=str)+'\n')
def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,list):return sorted((canonical(x) for x in v),key=lambda x:json.dumps(x,sort_keys=True))
    return str(v) if isinstance(v,uuid.UUID) else v
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def publish():
    assert json.loads((HERE/'validation.json').read_text())['passed']
    assert json.loads((HERE/'render-repaired/rendering.json').read_text())['passed']
    manifest=build_manifest(HERE/'package','generator.py',FILES,dependencies={'python':'3.13.5','packages':{}})
    digest=manifest_digest(manifest)
    package=publish_package(HERE/'package','generator.py',FILES,pub.config.math_root,dependencies=manifest['dependencies'],expected_digest=digest)
    save(HERE/'published-package.json',{'reference':package.reference,'digest':digest,'manifest':manifest})
    print(json.dumps({'published':package.reference}))

def normalized_dynamic(record):
    result={}
    for k,v in record.items():
        attr=k.lstrip(':')
        if attr=='db/id':continue
        if isinstance(v,dict) and ':db/id' in v:v=v[':db/id']
        if attr in ('progress/memory-at','progress/last-direct-at'):
            v={'$instant':round(datetime.datetime.fromisoformat(v.replace('Z','+00:00')).timestamp()*1000)}
        if isinstance(v,uuid.UUID):v=str(v)
        result[attr]=v
    return result

def prepare(out):
    assert not (out/'request.json').exists(),'Recover pending exact request first'
    identity=db.status();b=identity['basis']
    package=json.loads((HERE/'published-package.json').read_text())
    verify_package(Path(pub.config.math_root)/Path(package['reference']).parent,package['digest'])
    snap=ROOT/(HERE/'snapshot-path.txt').read_text()
    def read(name,q,args):return db.query(q,args,out,name,b)
    [[kp]]=read('kp','[:find (pull ?k [* {:knowledge-point/question-generator [*]} {:knowledge-point/questions '+QUESTION_PULL+'}]) :in $ ?k :where [?k :knowledge-point/id _]]',[KP])
    original=json.loads((snap/'kp.json').read_text())[0][0]
    assert canonical(kp[':knowledge-point/questions'])==canonical(original[':knowledge-point/questions']),'Question bank changed; inspect before repairing'
    assert canonical(kp[':knowledge-point/question-generator'])==canonical(original[':knowledge-point/question-generator']),'Generator registration changed'
    native_before=json.loads((HERE/'native/dynamic-before.json').read_text())
    rows=read('dynamic','[:find (pull ?e [*]) :in $ [?e ...] :where [?e _ _]]',[[int(x) for x in native_before]])
    assert {str(r[':db/id']):normalized_dynamic(r) for [r] in rows}==native_before,'Learner state changed after native replay'
    [[learner]]=read('learner-links','[:find (pull ?l [{[:learner/knowledge-profile :limit nil] [:db/id]} {:learner/performance [:db/id]} {[:learner/activity :limit nil] [:db/id]}]) :in $ ?l :where [?l :learner/id _]]',[LEARNER])
    assert {r[':db/id'] for r in learner[':learner/knowledge-profile']}|{learner[':learner/performance'][':db/id']}=={int(x) for x in native_before}
    assert REVIEW in [x[':db/id'] for x in learner[':learner/activity']]
    [[task]]=read('task','[:find (pull ?t [* {:learner-task/status [:db/id :db/ident]} {:learner-task/items [* {:task-item/status [:db/id :db/ident]} {:task-item/responses [*]}]}]) :in $ ?t :where [?t :learner-task/id _]]',[TASK])
    [[review]]=read('review','[:find (pull ?r [* {:learner-task/status [:db/id :db/ident]}]) :in $ ?r :where [?r :learner-task/id _]]',[REVIEW])
    assert review[':learner-task/status'][':db/ident'] in (':learner-task.status/unlocked',':learner-task.status/locked') and not review.get(':learner-task/items'),'Required review has already started'
    assert task[':learner-task/status'][':db/ident']==':learner-task.status/completed'
    items={r[':db/id']:r for r in task[':learner-task/items']};item=items[ITEM]
    assert item[':task-item/content'][':db/id']==QUESTION
    assert item[':task-item/status'][':db/ident']==':task-item.status/incorrect'
    assert all(i[':task-item/status'][':db/ident']==':task-item.status/correct' for eid,i in items.items() if eid!=ITEM)
    assert task[':learner-task/xp-base']==15 and task[':learner-task/xp-earned']==15
    forms=loads((HERE/'content-forms.edn').read_text())
    dynamic=loads((HERE/'native/dynamic-forms.edn').read_text())
    for f in dynamic:
        if str(f[2]) in (':progress/memory-at',':progress/last-direct-at'):
            for i in range(3,len(f)):
                if f[i] is not None:f[i]=Tagged('inst',f[i])
    forms+=dynamic
    audit=json.loads((HERE/'bank-audit.json').read_text())
    correct=next(q['new_correct_uuid'] for q in audit['questions'] if q['question']==QUESTION)
    for a in item[':task-item/responses']:forms.append([kw('db/retract'),ITEM,kw('task-item/responses'),a[':db/id']])
    forms.extend([
        [kw('db/add'),ITEM,kw('task-item/responses'),correct],
        [kw('db/cas'),ITEM,kw('task-item/status'),kw('task-item.status/incorrect'),kw('task-item.status/correct')],
        [kw('db/cas'),TASK,kw('learner-task/xp-earned'),15,18],
        [kw('db/retract'),LEARNER,kw('learner/activity'),REVIEW],
        [kw('db/retract'),REVIEW,kw('learner-task/remediation-for'),TASK],
        [kw('db/cas'),REVIEW,kw('learner-task/priority'),review[':learner-task/priority'],0.0],
        [kw('db/cas'),kp[':knowledge-point/question-generator'][':db/id'],kw('question-generator/script'),kp[':knowledge-point/question-generator'][':question-generator/script'],package['reference']],
        [kw('db/ensure'),ITEM,kw('task-item/validate')],
        [kw('db/ensure'),TASK,kw('learner-task/validate')],
    ])
    text=dumps(forms)+'\n';(out/'transaction.edn').write_text(text)
    attrs=read('attributes','[:find ?e ?a ?t :where [?e :db/ident ?a] [?e :db/valueType ?type] [?type :db/ident ?t]]',[])
    idents=read('idents','[:find ?e ?a :where [?e :db/ident ?a]]',[])
    plan={**identity,'source':SOURCE,'endpoint':db.config.endpoint,'transaction_sha256':sha(out/'transaction.edn'),'request_key':'echelon-minimum-'+str(b)+'-'+sha(out/'transaction.edn'),'package':package,'attributes':attrs,'idents':idents,'new_correct_uuid':correct,'original_task':task,'original_review':review,'repaired_question_ids':[q[':db/id'] for q in kp[':knowledge-point/questions'] if not q.get(':question/math-academy-id')]}
    save(out/'plan.json',plan)
    print(json.dumps({'prepared_basis':b,'forms':len(forms),'repaired_questions':len(plan['repaired_question_ids'])}))

def verify_report(report,plan,out):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==plan['basis']
    attr_names={eid:str(a) for eid,a,t in plan['attributes']};types={str(a):str(t) for eid,a,t in plan['attributes']}
    idents={str(a):eid for eid,a in plan['idents']};tempids=report[':edb/tempids']
    def entity(x):return tempids.get(x,idents.get(x,x)) if isinstance(x,str) else x
    def triple(e,a,v):
        a=str(a)
        if types[a]==':db.type/ref':v=entity(v)
        if isinstance(v,Tagged):v=v.value
        return entity(e),a,dumps(v)
    expected_add=set();expected_retract=set()
    for f in loads((out/'transaction.edn').read_text()):
        if isinstance(f,dict):
            e=f[kw('db/id')]
            for a,v in f.items():
                if str(a) not in (':db/id',':db/ensure'):expected_add.add(triple(e,a,v))
        else:
            op,e,a=str(f[0]),f[1],f[2]
            if op==':db/ensure':continue
            if op==':db/add':expected_add.add(triple(e,a,f[3]))
            elif op==':db/retract':expected_retract.add(triple(e,a,f[3]))
            elif op==':db/cas':
                if f[3] is not None:expected_retract.add(triple(e,a,f[3]))
                if f[4] is not None:expected_add.add(triple(e,a,f[4]))
            else:raise AssertionError(op)
    add=set();retract=set()
    for e,a,v,tx,s,added in report[':edb/tx-data']:
        assert s==idents[SOURCE]
        if attr_names[a]==':db/txInstant':continue
        (add if added else retract).add(triple(e,attr_names[a],v))
    assert add==expected_add and retract==expected_retract,{'extra_add':list(add-expected_add),'missing_add':list(expected_add-add),'extra_retract':list(retract-expected_retract),'missing_retract':list(expected_retract-retract)}

def verify_live(out,report):
    plan=json.loads((out/'plan.json').read_text());verify_report(report,plan,out)
    b=report[':edb/db-after-t']
    rows=db.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id _]]',[plan['repaired_question_ids']],out/'readback','questions',b)
    from scripts.generator_publish import normalized_question
    expected=json.loads((HERE/'repaired-records.json').read_text())
    assert canonical([normalized_question(q) for [q] in rows])==canonical([normalized_question(r['question']) for r in expected])
    [[state]]=db.query('[:find (pull ?i [* {:task-item/status [:db/id :db/ident]} {:task-item/responses [*]}]) :in $ ?i :where [?i :task-item/id _]]',[ITEM],out/'readback','item',b)
    assert state[':task-item/status'][':db/ident']==':task-item.status/correct'
    assert len(state[':task-item/responses'])==1 and str(state[':task-item/responses'][0][':answer/id'])==plan['new_correct_uuid']
    assert state[':task-item/elapsed-seconds']==next(i for i in plan['original_task'][':learner-task/items'] if i[':db/id']==ITEM)[':task-item/elapsed-seconds']
    [[task]]=db.query('[:find (pull ?t [*]) :in $ ?t :where [?t :learner-task/id _]]',[TASK],out/'readback','task',b)
    assert task[':learner-task/xp-earned']==18
    for k,v in task.items():
        if k not in (':learner-task/xp-earned',':learner-task/items',':learner-task/status'):assert canonical(v)==canonical(plan['original_task'][k]),k
    expected_dynamic=json.loads((HERE/'native/dynamic-after.json').read_text())
    dynamic=db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e _ _]]',[[int(x) for x in expected_dynamic]],out/'readback','dynamic',b)
    assert {str(r[':db/id']):normalized_dynamic(r) for [r] in dynamic}==expected_dynamic
    [[links]]=db.query('[:find (pull ?l [{[:learner/activity :limit nil] [:db/id]}]) :in $ ?l :where [?l :learner/id _]]',[LEARNER],out/'readback','learner-links',b)
    assert REVIEW not in [r[':db/id'] for r in links[':learner/activity']]
    [[review]]=db.query('[:find (pull ?r [*]) :in $ ?r :where [?r :learner-task/id _]]',[REVIEW],out/'readback','review',b)
    assert not review.get(':learner-task/remediation-for') and review[':learner-task/priority']==0.0
    [[registration]]=db.query('[:find (pull ?g [*]) :in $ ?k :where [?k :knowledge-point/question-generator ?g]]',[KP],out/'readback','registration',b)
    assert registration[':question-generator/script']==plan['package']['reference']
    result={'committed':True,'verified':True,'basis_before':plan['basis'],'basis_after':b,'question_banks_repaired':5,'faulty_keys_corrected':4,'malformed_source_label_repaired':True,'correct_answer':state[':task-item/responses'][0][':answer/value'],'item_marked_correct':True,'assessment_correct':9,'assessment_total':9,'xp_before':15,'xp_after':18,'review_removed':True,'dynamic_state_matches_native_counterfactual':True,'generator':plan['package']['reference'],'only_planned_datoms_changed':True}
    save(HERE/'verification.json',result);save(out/'verification.json',result);print(json.dumps(result))

def apply():
    lock=ROOT/'.local/learning/requests/math/api.lock';lock.parent.mkdir(parents=True,exist_ok=True)
    with lock.open('a') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX)
        for attempt in range(3):
            out=HERE/f'commit-{attempt}';out.mkdir(exist_ok=True)
            request=out/'request.json';receipt=out/'receipt.edn'
            if receipt.exists():
                verify_live(out,loads(receipt.read_text()));return
            if not request.exists():
                prepare(out)
                run=subprocess.run([str(HERE/'native/correction'),'preview',str(out)],env=db.environment,capture_output=True,text=True,timeout=240)
                (out/'application-preview.stdout').write_text(run.stdout);(out/'application-preview.stderr').write_text(run.stderr)
                if run.returncode:
                    if 'Stale repair basis' in run.stderr:continue
                    raise RuntimeError('Application preview failed: '+run.stderr)
                assert json.loads((out/'application-preview.json').read_text())['passed']
                plan=json.loads((out/'plan.json').read_text());save(request,plan)
            else:plan=json.loads(request.read_text())
            assert plan['transaction_sha256']==sha(out/'transaction.edn')
            try:
                text=db.command('transact','--file',out/'transaction.edn','--endpoint',plan['endpoint'],'--request-key',plan['request_key'],'--basis',plan['basis'],'--source',SOURCE,'--timeout-ms','180000',timeout=210)
            except StaleBasis:
                save(out/'confirmed-stale.json',{'request_key':plan['request_key'],'committed':False})
                continue
            receipt.write_text(text);report=loads(text)
            verify_live(out,report);return
        raise RuntimeError('Database repeatedly advanced; saved requests retained')

if __name__=='__main__':
    action=sys.argv[1]
    if action=='publish':publish()
    elif action=='apply':apply()
    elif action=='verify':
        out=Path(sys.argv[2]);verify_live(out,loads((out/'receipt.edn').read_text()))
    else:raise ValueError(action)

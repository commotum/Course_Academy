"""Scoped additive replenishment; exact retained EDB requests and locked readback."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('current_validation',HERE/'validate-current.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
g=v.g;KP=g.KP_ID;SOURCE=':application/ca-engine';LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'0f3844f68aaa322a348dfd3eae92ae8bcfe3262541b0c7a2e6c846081bbf0358'
OUT=HERE/'replenishment';OUT.mkdir(exist_ok=True)
DB=Database(SimpleNamespace(database='math',edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY='''[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example [*]} {[:knowledge-point/questions :limit nil] [* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'''
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l] (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
HISTORY='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q _ _ true] [?kp :knowledge-point/questions ?q]]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(vv) for k,vv in x.items() if str(k) not in (':knowledge-point/_questions',':knowledge-point/_canonical-example')}
    if isinstance(x,(list,tuple,set)):return sorted([canonical(vv) for vv in x],key=lambda vv:json.dumps(vv,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def inventory(path):
    r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-17e1b9defebc55b9'),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
    data=json.loads(r.stdout);assert data['ok'] and data['data']['lineage']==LINEAGE
    save(path,data['data']);return data['data']
def read(path,basis):
    return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def existing_record(q):
    normal=v.normalize(q);level=normal[':question/difficulty'].split('/')[-1]
    rec={'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':normal,'generation':{'difficulty':level,'mathematical_fingerprint':v.fingerprint(q)}}
    v.inspect(rec);return rec

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'shown-reserved',basis)}
    unavailable|={r[0] for r in DB.query(HISTORY,[KP,LEARNER],path,'historical-presentations',basis,history=True)}
    pools={l:{} for l in g.LEVELS};gradable=[];excluded=[]
    for q in kp.get(':knowledge-point/questions',[]):
        if ':question/difficulty' not in q or ':question/worked-solution' not in q or any(':answer-field/correct' not in f for f in q.get(':question/answer-fields',[])):
            excluded.append(str(q[':question/id']));continue
        rec=existing_record(q);gradable.append(rec)
        if q[':db/id'] not in unavailable:pools[rec['generation']['difficulty']][v.fingerprint(q)]=str(q[':question/id'])
    if gradable:
        native_path=path/'available-native';native_path.mkdir(exist_ok=True);v.native(gradable,native_path)
    result={'basis':basis,'available':{l:len(p) for l,p in pools.items()},'question_ids':{l:list(p.values()) for l,p in pools.items()},'excluded_shown_reserved':sorted(unavailable),'excluded_incomplete':excluded}
    save(path/'counts.json',result);return result

def forms(records,kp,gid):
    tx=[]
    for rec in records:
        q=rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:tx.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            tx.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/correct'):f[':answer-field/correct'][1],kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('db/ensure'):kw('answer-field/validate')})
        tx.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    else:tx.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:tx.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if tx:tx.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return tx

def check_report(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,val,t,s,added in report[':edb/tx-data']:
        assert added and s==source,'Unexpected retraction or attribution'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected change '+name

def verify(path,intent,receipt):
    assert receipt[':edb/committed'] and receipt[':edb/db-before-t']==intent['basis']
    check_report(receipt,path/'receipt-check',intent['source_eid']);basis=receipt[':edb/db-after-t'];kp=read(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items()),'Existing source question changed'
    assert canonical({k:x for k,x in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:x for k,x in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and v.normalize(q)==v.normalize(r['question']);v.inspect(r)
    assert not forms([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'source_questions_preserved':len(old),'learner_history_unchanged':True,'only_scoped_additive_content_changes':True,'application_source_verified':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,verified,inv,gid):
    c=verified['counts_after'];shortage={l:max(0,5-c['available'][l]) for l in g.LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(g.LEVELS),'available_after':c['available'],'shortage_remaining':shortage,'capability_exceptions':[],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source':'application/ca-engine','evidence':[str(p.relative_to(ROOT)) for p in [HERE/'current-validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'capabilities.json',path/'verification.json',path/'preparation.json',path/'generated.json',path/'native-report.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'inventory-after.json'] if p.exists()],'note':'Original unrated incomplete questions are preserved and excluded; their classify job may remain. Hard is authored, canonical-anchored surd endpoint translation; observed rated sources cover easy and moderate.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_after','shortage_remaining')}),flush=True)

def main():
    validation=json.loads((HERE/'current-validation.json').read_text());assert validation['passed']
    for n,h in validation['hashes'].items():assert sha(HERE/n)==h,'Validation artifact changed '+n
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                fresh=inventory(path/'recovery-inventory.json');assert fresh['lineage']==intent['lineage']
                receipt=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,receipt);finish(path,verified,inventory(path/'inventory-after.json'),intent['generator_id']);return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=json.loads((HERE/'current-source.json').read_text())['record'];current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
        assert set(current)=={q[':question/math-academy-id'] for q in captured[':knowledge-point/questions']},'New source requires reclassification'
        for q in captured[':knowledge-point/questions']:assert canonical(current[q[':question/math-academy-id']])==canonical(q)
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(captured[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gid=str(kp[':knowledge-point/question-generator'][':question-generator/id']) if kp.get(':knowledge-point/question-generator') else g.GENERATOR_UUID
        c=counts(kp,path,basis);needed={l:max(0,5-c['available'][l]) for l in g.LEVELS}
        used={v.fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(g.digest({'a':'-4','b':'sqrt(2)','left_closed':False,'direction':'interval_to_inequality'}));added={l:0 for l in g.LEVELS};records=[]
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        assert isinstance(instances,list)
        for r in instances:
            v.inspect(r);d=r['generation'];replay=g.generate(d['difficulty'],d['seed'],template=d['template'],parameters=d['parameters'],profile=d['profile']);assert v.normalize(replay['question'])==v.normalize(r['question'])
        save(path/'supplied-validation.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
        candidates=instances+[g.generate(l,seed,template=g.TEMPLATES[seed%2]) for l in g.LEVELS for seed in range(100,160)]
        for r in candidates:
            v.inspect(r);level=r['generation']['difficulty'];fp=v.fingerprint(r['question'])
            if added[level]<needed[level] and fp not in used:records.append(r);used.add(fp);added[level]+=1
        ids=[uuid.UUID(x) for r in records for x in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        matches=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identities',basis) if ids else []
        assert not matches,'Identity reconciliation required'
        save(path/'generated.json',records);v.native(records,path)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'counts_before':c,'needed':needed,'added':added,'distinct_mathematical_tasks':len({v.fingerprint(r['question']) for r in records}),'generator_hash':sha(HERE.with_suffix('.py')),'validation_hash':sha(HERE/'current-validation.json'),'assets':[]})
        tx=forms(records,kp,gid)
        if not tx:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'counts_after':c};save(path/'verification.json',verified);finish(path,verified,inv,gid);return
        txpath=path/'transaction.edn';text=dumps(tx)+'\n'
        with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
        result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=90)
        (path/'preview.edn').write_text(result.stdout);pr=loads(result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'basis':basis,'expected_basis':basis,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'request_key':'half-open-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':text,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);receipt=DB._commit(intent,txpath,path);verified=verify(path,intent,receipt);finish(path,verified,inventory(path/'inventory-after.json'),gid)
if __name__=='__main__':main()

"""Additive scoped inventory preparation, application-lock commit and readback."""
import copy,fcntl,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import validate_current as cv;v=cv.v;g=cv.g
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment
from inventory_jobs import save
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database
from edn import dumps,loads,kw
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.CAPTURE['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'9f9b5b80ac0ea3cbd5462689849713b90b8e1b2cc23133373d2f3d32ffb50eaa'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'reference/initial/kp-query.edn').read_text()
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7';POOL=ROOT/'generate/scratch/17592186068841/check-pool'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(p):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']

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

def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]

def native(records,p):
    p.mkdir(parents=True,exist_ok=True)
    save(p/'input.json',[{'label':r['question'][':question/id'],'record':r,'checks':cv.checks(r)} for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,timeout=55)

UNSAFE={
 'q-39481':'Duplicate selection fields, a missing correct ref and flattened legacy mathematical values.',
 'q-161612':'Worked solution multiplies by the radial Jacobian twice in its expanded middle stage.',
 'q-161603':'A distractor upper height sqrt(25-r^2) extends to r=16, outside its real domain.',
 'q-161609':'Two complete distractor integrals over 0<=theta<=pi are both zero: sin(2theta) with radial-only heights.',
 'q-161602':'The purported upper height 4+y lies below lower height 2 near y=-sqrt(5); converted region needs a split.'
}

def record(q,kp):
    nq=normalize(q)
    return {'question':nq,'knowledge_point':{'db_id':KP,'id':str(kp[':knowledge-point/id']),'title':kp[':knowledge-point/title']},'generation':{'template':q.get(':question/math-academy-id','committed-generated')}}

def counts(kp,b,p):
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    seen={r[0] for r in shown+reserved};save(p/'scoped-snapshot.json',scoped(kp,b,seen))
    subprocess.run([str(POOL),str(p/'scoped-snapshot.json'),str(p/'native-pool.json')],check=True,capture_output=True,text=True,timeout=55)
    pool=json.loads((p/'native-pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs}
    known={r['question'][':question/id']:r for path in OUT.glob('basis-*/generated.json') for r in json.loads(path.read_text())}
    levels={l:[] for l in LEVELS};fps={l:set() for l in LEVELS};excluded=[];records=[]
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id');qid=str(q[':question/id'])
        if q[':db/id'] not in ids or mid in UNSAFE:
            excluded.append({'id':qid,'source_id':mid,'reason':UNSAFE.get(mid,'native pool excludes ungradable, unrated, canonical, ever shown or reserved')});continue
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert level in LEVELS
        if mid:
            rec=record(q,kp);fp=cv.validate(rec,generated=False)
            # Full original template/stage checks also run for every safe source.
            t=next(t for t,(l,sid,params) in g.TEMPLATES.items() if sid==mid)
            rec['generation']={'template':t,'parameters':g.TEMPLATES[t][2]}
            v.verify(rec)
        else:
            rec=copy.deepcopy(known[qid]);assert normalize(q)==ordered(rec['question']);fp=cv.validate(rec)
        records.append(rec);levels[level].append(qid);fps[level].add(fp)
    native(records,p/'available-grading')
    result={'basis':b,'levels':{l:{'distinct_available_tasks':len(fps[l]),'available_question_ids':levels[l]} for l in LEVELS},'excluded':excluded,'native_pool':pool,'deduplication':'complete requested cylindrical bounds and integrand; excludes IDs, seed, difficulty, profile, solution and choice order'}
    save(p/'available-counts.json',result);return result

def publish(records,p):
    assets={};mathroot=Path(DB.env['EDB_MATH_ROOT'])
    for rec in records:
        q=rec['question']
        for key in (':question/problem',':question/worked-solution'):
            def asset(m):
                raw=m[1];src=Path(raw)
                if not src.is_absolute():src=ROOT/src
                assert src.is_file(),raw
                data=src.read_bytes();digest=hashlib.sha256(data).hexdigest();relative=Path('images')/digest[:2]/(digest+'.png');dest=mathroot/relative
                dest.parent.mkdir(parents=True,exist_ok=True)
                if dest.exists():assert dest.read_bytes()==data
                else:
                    tmp=dest.with_name('.'+digest+'.'+str(uuid.uuid4())+'.tmp')
                    with tmp.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
                    os.replace(tmp,dest)
                assert dest.is_file() and sha(dest)==digest
                assets[str(relative)]={'sha256':digest,'original':raw,'bytes':len(data)}
                return '![]('+str(relative)+')'
            q[key]=re.sub(r'!\[\]\(([^)]+)\)',asset,q[key])
    save(p/'asset-hashes.json',assets);return assets

def verify(p,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items());exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(rec['question']);cv.validate(rec)
    for relative,a in json.loads((p/'asset-hashes.json').read_text()).items():assert sha(Path(DB.env['EDB_MATH_ROOT'])/relative)==a['sha256']
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,b,p/'readback')
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS};prep=json.loads((p/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'observed_levels':['easy','moderate'],'authored_levels':['hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'shortage_remaining':remaining,'available_counts_before':prep['available_counts'],'available_counts_after':after,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':['Generator source replay covers the frozen basis-1356 bank; three later source families remain classified separately and are excluded for evidenced mathematical defects.','Hard is an explicitly authored combined-workload extension within this KP, not a recovered source rating.','Finite documented parameter domains; no claim of unlimited valid variants.'],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'generated.md',p/'asset-hashes.json',p/'inventory-after.json',HERE/'reference/current-classification.md',HERE/'validation.json',HERE/'freeze.json',p/'readback/available-grading/report.json'] if f.exists()]}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','shortage_remaining')}),flush=True)

def stable(value):
    if isinstance(value,dict):return {str(k):stable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return sorted((stable(v) for v in value),key=lambda a:json.dumps(a,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def main():
    freeze=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/p)==h for p,h in freeze['sha256'].items()),'Frozen package changed'
    assert json.loads((HERE/'validation.json').read_text())['status']=='passed'
    # Initial inventory recheck precedes generation; durable preparation rechecks
    # again while holding the application's serialization lock.
    initial=inventory(OUT/'inventory-before.json');assert initial['lineage']==LINEAGE
    preview=preview_executable(SimpleNamespace(math_root=Path(DB.env['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if (p/'commit-intent.json').exists():
                intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['transaction_sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,p/'transaction.edn',p);verified=verify(p,intent,report);finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True)
        kp=read(p,b);assert str(kp[':knowledge-point/id'])==g.SOURCE[':knowledge-point/id'];(p/'before.edn').write_text(dumps(kp)+'\n')
        captured=loads((HERE/'reference/initial/kp.edn').read_text())[0][0]
        assert stable(kp[':knowledge-point/questions'])==stable(captured[':knowledge-point/questions']),'Current source bank changed; refresh classification'
        assert stable(kp[':knowledge-point/canonical-example'])==stable(captured[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+str(KP)))
        save(HERE/'generator-registration.json',{'id':gid,'script':SCRIPT,'existing_reference':gen is not None})
        c=counts(kp,b,p);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS};print('Validated shortages',needed,flush=True)
        used={cv.task(q) for q in kp[':knowledge-point/questions']};used.add(cv.task(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        for r in instances:cv.validate(r)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
        records=[];added={l:0 for l in LEVELS}
        def take(rec):
            l=rec['question'][':question/difficulty'].split('/')[-1];fp=cv.task(rec['question'])
            if added[l]<needed[l] and fp not in used:
                cv.validate(rec);records.append(copy.deepcopy(rec));used.add(fp);added[l]+=1;print('Validated',l,rec['generation']['template'],rec['generation']['parameters'],flush=True)
        for rec in instances:take(rec)
        families={'easy':['full_z2radial','full_cone_radial'],'moderate':['half_difference','quarter_sphere_volume','half_zdifference'],'hard':['quarter_zdifference']}
        for level in LEVELS:
            for i in range(80):
                if added[level]>=needed[level]:break
                take(g.generate(level,seed=292670+i,template=families[level][i%len(families[level])]))
            assert added[level]==needed[level],('bounded generation shortage',level,needed[level],added[level])
        assets=publish(records,p)
        for rec in records:cv.validate(rec)
        ids=[uuid.UUID(qid) for rec in records for qid in [rec['question'][':question/id']]+[i for f in rec['question'][':question/answer-fields'] for i in [f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]]]
        existing=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'identity-matches',b) if ids else []
        assert not existing,'Existing identities require reconciliation'
        # Check bank-wide task duplicates against every source and canonical, not
        # just those eligible in the fresh practice pool.
        assert len({cv.task(r['question']) for r in records})==len(records)
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records))
        native(records,p/'generated-grading')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'asset_hashes':assets,'source_evidence_unchanged':True,'generator_sha256':sha(HERE.with_suffix('.py')),'generator_replay_basis':1356,'current_classification_basis':2696})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
        txpath=p/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        assert DB.basis()==b,'Basis changed under application lock; return to preparation'
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert not pr[':edb/committed'] and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'cylindrical-setup-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[rec['question'][':question/id'] for rec in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(p/'commit-intent.json',intent);print('Submitting exact prepared request at basis',b,flush=True)
        report=DB._commit(intent,txpath,p);verified=verify(p,intent,report);finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()

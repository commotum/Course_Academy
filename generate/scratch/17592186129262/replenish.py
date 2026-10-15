"""KP-scoped validated area inventory; durable guarded EDB commit and exact readback."""
import copy,fcntl,hashlib,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT)]
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
import current_audit as audit
v=audit.v;g=v.g
from serve_graph_explorer import database_environment
from inventory_jobs import save
from database import Database
from edn import dumps,loads,kw
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LEVELS=('easy','moderate','hard')
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'a22032fe284e800e7dd99ae6434ed8e66eb261c597e2e40d109e00b9c7f2b438'
OUT=HERE/'reference/replenishment';LOCK=ROOT/'.local/learning/requests/math/api.lock'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
BUILD=json.loads((OUT/'native-build.json').read_text());NATIVE=Path(BUILD['learning'])
QUERY=(HERE/'source-query.edn').read_text()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,b):return DB.query(QUERY,[[KP]],p,'kp',b)[0][0]

def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def normalize(q):
    return ordered({':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':[{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]} for f in q[':question/answer-fields']]})

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

def check_datoms(report,p,source):
    attrs=dict(DB.attributes(p,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction'
        name=str(attrs[a])
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name

def inventory(p):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
    save(p,x['data']);return x['data']

def validate(rec):
    meta=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS and meta['eligible_for_learning'] and not meta['evidence_only'] and meta['profile']=='method'
    assert rec['knowledge_point']=={'db_id':KP,'id':g.KP_UUID,'title':g.TITLE}
    replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
    local=copy.deepcopy(rec['question'])
    for a in meta.get('published_assets',[]):
        local[':question/worked-solution']=local[':question/worked-solution'].replace(a['reference'],a['original'])
        path=Path('/media/jake/SSD/EDB/math')/a['reference'];assert sha(path)==a['sha256']
    assert ordered(replay['question'])==ordered(local),'Generator replay differs'
    v.format_check(rec);v.read_prompt(rec)
    return audit.fingerprint(rec['question'])

def native(records,p):
    p.mkdir(parents=True,exist_ok=True)
    fixtures=[]
    for r in records:
        f=r['question'][':question/answer-fields'][0]
        fixtures.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'real learner radio grading, independently checked math'} for a in f[':answer-field/choices']]})
    save(p/'input.json',fixtures)
    subprocess.run([str(OUT/'check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,timeout=55)
    report=json.loads((p/'report.json').read_text());assert report['documented_unresolved_checks']==0

# Capture only this KP with the native inventory predicate; never export or edit
# other KPs or learner content. Historical item reads exclude ever-shown questions.
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
            if ':answer-field/correct' in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}

def counts(kp,b,p):
    p.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    seen={row[0] for row in shown+reserved};save(p/'scoped-snapshot.json',scoped(kp,b,seen))
    subprocess.run([str(OUT/'check-pool'),str(p/'scoped-snapshot.json'),str(p/'native-pool.json')],capture_output=True,text=True,check=True,timeout=55)
    pool=json.loads((p/'native-pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs}
    known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    levels={l:[] for l in LEVELS};fps={l:set() for l in LEVELS};excluded=[];records=[];source_audit=[]
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id');valid=True
        if mid:
            try:proof=audit.source_math(q);source_audit.append({'id':mid,'passed':True,**proof})
            except AssertionError as e:
                valid=False;reason=str(e);source_audit.append({'id':mid,'passed':False,'reason':reason})
        else:
            rec=known[str(q[':question/id'])];assert normalize(q)==ordered(rec['question']);validate(rec)
        if not valid or q[':db/id'] not in ids:
            excluded.append({'id':str(q[':question/id']),'source_id':mid,'reason':reason if not valid else 'native pool excludes unrated, ungradable, canonical, shown or reserved'});continue
        l=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        rec={'question':normalize(q),'knowledge_point':{'title':g.TITLE},'generation':{'template':mid or 'generated'}}
        records.append(rec);levels[l].append(str(q[':question/id']));fps[l].add(audit.fingerprint(q))
    native(records,p/'available-grading')
    result={'basis':b,'levels':{l:{'distinct_available_tasks':len(fps[l]),'available_question_ids':levels[l]} for l in LEVELS},'excluded':excluded,'native_pool':pool,'source_math':source_audit,'deduplication':'canonical sorted supplied boundary zero-sets; ignores level, seed, UUID, bank and option order'}
    save(p/'available-counts.json',result);return result

def publish(rec):
    assets=[];q=rec['question']
    for ref in re.findall(r'!\[\]\(([^)]+)\)',q[':question/worked-solution']):
        path=Path(ref);digest=sha(path);relative='images/'+digest[:2]+'/'+digest+'.png';target=Path('/media/jake/SSD/EDB/math')/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():
            with target.open('xb') as stream:stream.write(path.read_bytes());stream.flush();os.fsync(stream.fileno())
        assert sha(target)==digest
        assets.append({'original':ref,'reference':relative,'sha256':digest,'bounds':rec['generation']['parameters']})
        q[':question/worked-solution']=q[':question/worked-solution'].replace(ref,relative)
    rec['generation']['published_assets']=assets
    validate(rec)

def verify(p,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_datoms(report,p/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items());skip={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in skip}=={k:v for k,v in kp.items() if k not in skip}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
    used={audit.fingerprint(q) for q in old.values()};used.add(audit.fingerprint(before[':knowledge-point/canonical-example']))
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);fp=validate(r);assert fp not in used;used.add(fp)
    native(records,p/'readback/grading');assert not transaction([],kp,intent['generator_id'])
    after=counts(kp,b,p/'readback/inventory')
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after};save(p/'verification.json',result);return result

def finish(p,intent,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS};prep=json.loads((p/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'topic':17592186050705,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'preparation_basis':intent['basis'],'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'observed_levels':['moderate','hard'],'authored_levels':['easy'],'unsupported_levels':[],'unsupported_levels_filled':False,'remaining_shortages':remaining,'available_counts_before':{l:prep['available_counts']['levels'][l]['distinct_available_tasks'] for l in LEVELS},'available_counts_after':{l:after['levels'][l]['distinct_available_tasks'] for l in LEVELS},'source_questions_and_learner_history_preserved':True,'inventory_recheck_basis':inv['basis'],'remaining_application_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capabilities':json.loads((HERE/'capabilities.json').read_text()),'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'generated.md',p/'inventory-after.json',p/'current-inventory/available-counts.json',p/'readback/inventory/available-counts.json',HERE/'classification.md',HERE/'current-classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'freeze.json',OUT/'native-build.json'] if f.exists()],'note':'Distinct supported reserves filled. Legacy unrated/incomplete q-160373 and incorrect transformed-boundary q-160654 remain unchanged and excluded from validated availability. The application may retain classification work for the legacy unrated record. Application api.lock held from current basis recheck through submission and readback.'}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ['outcome','new_questions','new_by_level','verified_commit_basis','available_counts_after','remaining_shortages']},indent=2),flush=True)

def main():
    for f,expected in BUILD['executables'].items():assert sha(Path(f))==expected
    frozen=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/p)==digest for p,digest in frozen['sha256'].items())
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed'] and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            assert intent['exact_edn']==(p/'transaction.edn').read_text() and intent['sha256']==sha(p/'transaction.edn')
            verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent,verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
        captured=loads((OUT/'initial/kp.edn').read_text())[0][0]
        assert kp==captured,'Sources or registration changed since current classification; reopen before writing'
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (p/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS};print(json.dumps({'basis':b,'missing':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied;instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:validate(r)
        native(instances,p/'supplied-grading');save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError') if isinstance(supplied,dict) else None})
        used={audit.fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(audit.fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];added={l:0 for l in LEVELS};rejected=0
        for l in LEVELS:
            candidates=[r for r in instances if r['question'][':question/difficulty']==':question.difficulty/'+l]
            for i in range(1000):
                if added[l]>=needed[l]:break
                r=candidates.pop(0) if candidates else g.generate(l,seed=int(JOB.name[:8],16)+i)
                fp=validate(r)
                if fp in used:rejected+=1;continue
                publish(r);records.append(r);used.add(fp);added[l]+=1
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)));native(records,p/'selected-grading')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'duplicate_candidates_rejected':rejected,'asset_hashes':[a for r in records for a in r['generation']['published_assets']],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{l:needed[l]-added[l] for l in LEVELS if needed[l]>added[l]}})
        if '--prepare-only' in sys.argv:return
        forms=transaction(records,kp,gid);assert forms
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout)
        pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_datoms(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'rectangular-area-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK)}
        save(p/'commit-intent.json',intent)
        verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,intent,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()

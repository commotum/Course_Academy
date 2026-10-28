"""Scoped Green/polar replenishment with exact EDB request recovery and readback."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import validate as v;g=v.g
import live_validate as lv
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment,build_learning
from inventory_jobs import save
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database
from edn import dumps,loads,kw
KP=17592186176024;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SNAPSHOT['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'ca287c579557532d322ea65de079b3ea7bcb2b46960deeeaf958346424d9e653'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'source-query.edn').read_text()
NATIVE=Path('/home/jake/Developer/Course_Academy/.local/graph-explorer/learning-c9743ced043e1fd7');POOL=HERE/'reference/native/check-pool'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(p):
    # Invoke the existing native read directly while holding api.lock; the HTTP
    # inventory endpoint takes that same lock and would recursively wait.
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def read(p,b):return DB.query(QUERY,[[KP]],p,'kp',b)[0][0]
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

def verify(p,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items());exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
    import re
    assets=json.loads((p/'asset-manifest.json').read_text())
    for item in assets.values():
        target=Path(DB.env['EDB_MATH_ROOT'])/item['path'];assert target.is_file() and sha(target)==item['sha256']
    for record in records:
        for ref in re.findall(r'!\[.*?\]\(([^)]+)\)',record['question'][':question/worked-solution']):
            assert ref.startswith('images/') and (Path(DB.env['EDB_MATH_ROOT'])/ref).is_file()
    assert not transaction([],kp,intent['generator_id'])
    after=counts(kp,b,p/'readback');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'content_addressed_assets_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after};save(p/'verification.json',result);return result


def validate(rec):
    assert not rec['generation']['evidence_only']
    assert rec['generation']['eligible_for_learning'];v.validate_record(rec);lv.check(rec['question']);return True

def fingerprint(q):return lv.fingerprint(normalize(q) if isinstance(q.get(':question/difficulty'),dict) else q)

def native(records,p):
    p.mkdir(parents=True,exist_ok=True)
    save(p/'input.json',[v.engine_item(r,r['question'][':question/id']) for r in records])
    subprocess.run([str(HERE/'reference/native/check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,timeout=55)

def counts(kp,b,p):
    p.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    seen={row[0] for row in shown+reserved};save(p/'scoped-snapshot.json',scoped(kp,b,seen))
    subprocess.run([str(POOL),str(p/'scoped-snapshot.json'),str(p/'native-pool.json')],capture_output=True,text=True,check=True,timeout=55)
    pool=json.loads((p/'native-pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs}
    known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    levels={l:[] for l in LEVELS};excluded=[];records=[];fps={l:set() for l in LEVELS}
    unsafe={'q-125716'}  # live solution changes e^(cos y) to e^(cos x) in a later row
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id')
        if q[':db/id'] not in ids or mid in unsafe:
            excluded.append({'id':str(q[':question/id']),'source_id':mid,'reason':'source worked-solution transcription error; retained unchanged' if mid in unsafe else 'native pool excludes unrated, ungradable, canonical, shown or reserved'});continue
        l=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert l in LEVELS
        normal=normalize(q);lv.check(normal)
        if mid:
            r={'question':normal,'knowledge_point':{'title':kp[':knowledge-point/title']},'generation':{'template':'live-source-'+mid}}
        else:
            r=known[str(q[':question/id'])];assert normal==ordered(r['question'])
            try:validate(r)
            except AssertionError as error:
                excluded.append({'id':str(q[':question/id']),'source_id':None,'reason':'generated solution fails current validation; retained unchanged','validation_error':str(error)})
                continue
        records.append(r);levels[l].append(str(q[':question/id']));fps[l].add(fingerprint(q))
    native(records,p/'available-grading')
    result={'basis':b,'levels':{l:{'distinct_available_tasks':len(fps[l]),'available_question_ids':levels[l]} for l in LEVELS},'excluded':excluded,'native_pool':pool,'deduplication':'reduced symbolic curl; ignores radius, common cancelled offsets, seed, bank profile, identities, field-insensitive terms and choice order'}
    save(p/'available-counts.json',result);return result


def finish(p,gid,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    prep=json.loads((p/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'observed_levels':['easy','moderate'],'authored_levels':['hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'shortage_remaining':remaining,'available_counts_before':prep['available_counts'],'available_counts_after':after,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text()),'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'generated.md',p/'inventory-after.json',HERE/'classification-current.md',HERE/'validation.json',HERE/'freeze.json',HERE/'reference/current-source-audit/audit.json',HERE/'reference/native/build.json'] if f.exists()],'note':'All source questions and learner history preserved. Historical fixture fidelity and live-source correctness are separate. Hard is an authored unequal-cubic same-method extension. Exact requests and receipts retained; application api.lock held through recheck, submission and readback.'}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','shortage_remaining')}),flush=True)


def main():
    global NATIVE
    freeze=json.loads((HERE/'freeze.json').read_text());validation=json.loads((HERE/'validation.json').read_text())
    assert all(sha(ROOT/path)==digest for path,digest in freeze.get('sha256',{}).items()),'Frozen package changed; validate again'
    assert validation['status']=='passed' and validation['source_options_matched']==40
    assert json.loads((HERE/'reference/current-source-audit/audit.json').read_text())['source_options_checked']==55
    assert all(sha(ROOT/path)==digest for path,digest in freeze['sha256'].items() if path.endswith('.py'))
    NATIVE=build_learning(Path(os.environ.get('EDB_ROOT',ROOT.parent/'EDB')))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Application commit serialization',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        # Reconcile the identical saved request before making any new content plan.
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            assert inventory(p/'recovery-inventory.json')['lineage']==intent['lineage']
            report=DB._commit(intent,p/'transaction.edn',p)
            # A verified historical request must not terminate replenishment at
            # an old basis. Reconcile exact content without rewriting its evidence.
            if (p/'verification.json').exists():
                prior=json.loads((p/'verification.json').read_text());assert prior['passed'] and prior['basis_after']==report[':edb/db-after-t']
                check_report(report,p/'recovery-receipt-check',intent['source_eid'])
                recovered=read(p/'recovery-readback',report[':edb/db-after-t']);byid={str(q[':question/id']):q for q in recovered[':knowledge-point/questions']};defects=[]
                for rec in json.loads((p/'generated.json').read_text()):
                    assert normalize(byid[rec['question'][':question/id']])==ordered(rec['question'])
                    try:validate(rec)
                    except AssertionError as error:defects.append({'question':rec['question'][':question/id'],'error':str(error),'action':'preserved; excluded from validated inventory'})
                save(p/'recovery-current.json',{'exact_receipt_verified':True,'basis':report[':edb/db-after-t'],'validation_defects':defects})
            else:verify(p,intent,report)
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
        captured=loads((HERE/'reference/initial/source.edn').read_text())[0][0]
        current_questions={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(current_questions[q[':db/id']]==q for q in captured[':knowledge-point/questions']),'Source changed; reclassify before writing'
        assert kp[':knowledge-point/canonical-example']==captured[':knowledge-point/canonical-example']
        assert str(kp[':knowledge-point/id'])==g.KP[':knowledge-point/id']
        (p/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS};print(json.dumps({'basis':b,'missing':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:validate(r)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(lv.hashlib.sha256(g.sp.srepr(g.Y).encode()).hexdigest())  # canonical curl=y
        records=[];added={l:0 for l in LEVELS};candidates=list(instances)
        # Execute the frozen public API. Reject duplicate assessed tasks, regardless
        # of seed, ambient, option order or different rendered bank identities.
        for l in LEVELS:
            for i in range(1000):
                if added[l]>=needed[l]:break
                if candidates:r=candidates.pop(0)
                else:
                    try:r=g.generate(l,seed=int(JOB.name[:8],16)+i)
                    except ValueError:continue
                level=r['question'][':question/difficulty'].split('/')[-1]
                if level!=l:
                    if level in LEVELS and added[level]<needed[level] and fingerprint(r['question']) not in used:
                        validate(r);records.append(r);used.add(fingerprint(r['question']));added[level]+=1
                    continue
                fp=fingerprint(r['question'])
                if fp in used:continue
                validate(r);records.append(r);used.add(fp);added[l]+=1
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        library=ImageLibrary(Path(DB.env['EDB_MATH_ROOT']),HERE)
        for r in records:
            q=r['question']
            for key in (':question/problem',':question/worked-solution'):q[key]=library.text(q[key])
        save(p/'asset-manifest.json',library.saved)
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)));native(records,p/'selected-grading')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':list(library.saved.values()),'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{l:needed[l]-added[l] for l in LEVELS if needed[l]>added[l]}})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'green-circular-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
        verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()

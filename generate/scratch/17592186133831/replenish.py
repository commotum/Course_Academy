"""Scoped vector-line-integral replenishment with exact EDB request recovery and readback."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import validate as v;g=v.g
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment
from inventory_jobs import save
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database
from edn import dumps,loads,kw
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'b9ecae50860c663ee64b785d460079401e9de22d417458638436a0bca0532da9'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'source-query.edn').read_text()
NATIVE=Path(json.loads((HERE/'reference/native-build.json').read_text())['learning']);POOL=HERE/'reference/check-pool'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(p):
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
    assert not transaction([],kp,intent['generator_id'])
    after=counts(kp,b,p/'readback');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after};save(p/'verification.json',result);return result


def validate(rec):
    assert not rec['generation']['evidence_only']
    v.contract(rec);v.balanced(rec['question'][':question/problem']);v.balanced(rec['question'][':question/worked-solution']);return v.mathcheck(rec)

def fingerprint(q):
    if str(q[':question/id'])==g.SOURCE['record'][':knowledge-point/canonical-example'][':question/id']:
        assert source_matches(q,g.SOURCE['record'][':knowledge-point/canonical-example'])
        return g.digest([g.s.srepr(e) for e in (v.mp.T**7,g.s.Integer(0),g.s.Integer(1))]+['supplied-parameterization-dot-product-setup'])
    P,Q,u,w,lo,hi=v.mp.prompt(q[':question/problem']);t=v.mp.T
    integrand=g.s.trigsimp(g.s.expand(P.subs({v.mp.X:u,v.mp.Y:w})*g.s.diff(u,t)+Q.subs({v.mp.X:u,v.mp.Y:w})*g.s.diff(w,t)))
    return g.digest([g.s.srepr(e) for e in (integrand,lo,hi)]+['supplied-parameterization-dot-product-setup'])

def native_record(label,r):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual learner radio grading'} for a in f[':answer-field/choices']]}


def native(records,p):
    p.mkdir(parents=True,exist_ok=True)
    save(p/'input.json',[native_record(r['question'][':question/id'],r) for r in records])
    subprocess.run([str(HERE/'reference/check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,timeout=55)

def counts(kp,b,p):
    p.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    seen={row[0] for row in shown+reserved};save(p/'scoped-snapshot.json',scoped(kp,b,seen))
    subprocess.run([str(POOL),str(p/'scoped-snapshot.json'),str(p/'native-pool.json')],capture_output=True,text=True,check=True,timeout=55)
    pool=json.loads((p/'native-pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs}
    known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    levels={l:[] for l in LEVELS};excluded=[];records=[];fps={l:set() for l in LEVELS}
    unsafe={'q-124679','q-124680','q-124685'}
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id')
        if q[':db/id'] not in ids or mid in unsafe:
            excluded.append({'id':str(q[':question/id']),'source_id':mid,'reason':'documented ambiguous bank or malformed source solution; retained unchanged' if mid in unsafe else 'native pool excludes unrated, ungradable, canonical, shown or reserved'});continue
        l=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert l in LEVELS
        if mid:
            family=next(f for f,qsrc in g.SOURCE_BY_FAMILY.items() if qsrc[':question/math-academy-id']==mid)
            r=g.generate('easy',template=family,profile='observed_'+family)
            assert ordered(normalize(q))==ordered(r['question']) or source_matches(q,g.SOURCE_BY_FAMILY[family])
            v.mathcheck(r,raw=True);r['question']=normalize(q)
        else:
            r=known[str(q[':question/id'])];assert normalize(q)==ordered(r['question']);validate(r)
        records.append(r);levels[l].append(str(q[':question/id']));fps[l].add(fingerprint(q))
    native(records,p/'available-grading')
    result={'basis':b,'levels':{l:{'distinct_available_tasks':len(fps[l]),'available_question_ids':levels[l]} for l in LEVELS},'excluded':excluded,'native_pool':pool,'deduplication':'exact constructed integrand and supplied bounds; excludes seed, bank profile, identities and choice order'}
    save(p/'available-counts.json',result);return result


def source_matches(a,b):
    # Preserve original ownership identities as well as all source math and prose.
    if ':question/answer-fields' not in a and ':question/answer-fields' not in b:
        return set(a)==set(b) and all(str(a[k])==str(b[k]) for k in a)
    return normalize(a)==normalize(b)

def finish(p,gid,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    prep=json.loads((p/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'observed_levels':['easy'],'authored_levels':['moderate','hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'shortage_remaining':remaining,'available_counts_before':prep['available_counts'],'available_counts_after':after,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text()),'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'generated.md',p/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'freeze.json',HERE/'reference/native-build.json'] if f.exists()],'note':'Counts include only distinct validated gradable unshown/unreserved tasks. Source ambiguity and notation anomalies are preserved and excluded. Moderate/hard are documented same-method authored extensions. Exact requests and verified receipts retained; commit and readback serialized with the application api.lock.'}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','shortage_remaining')}),flush=True)


def main():
    freeze=json.loads((HERE/'freeze.json').read_text());validation=json.loads((HERE/'validation.json').read_text())
    assert all(sha(ROOT/path)==digest for path,digest in freeze.get('sha256',{}).items()),'Frozen package changed; validate again'
    assert validation['complete_source_banks_exact']==5 and validation['source_values_exact']==25 and validation['normal_generated_checks']==42
    assert all(sha(ROOT/path)==digest for path,digest in freeze['sha256'].items() if path.endswith('.py'))
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
            verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
        captured=g.SOURCE['record']
        assert {str(q[':question/id']) for q in captured[':knowledge-point/questions']} <= {str(q[':question/id']) for q in kp[':knowledge-point/questions']}
        current={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
        assert all(source_matches(current[str(q[':question/id'])],q) for q in captured[':knowledge-point/questions']), 'Source changed; reclassify'
        assert source_matches(kp[':knowledge-point/canonical-example'],captured[':knowledge-point/canonical-example'])
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (p/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS};print(json.dumps({'basis':b,'missing':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:validate(r)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
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
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)));native(records,p/'selected-grading')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':[],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{l:needed[l]-added[l] for l in LEVELS if needed[l]>added[l]}})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'vector-line-setup-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
        verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()

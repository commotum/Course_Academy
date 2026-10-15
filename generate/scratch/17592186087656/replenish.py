"""KP-scoped additive replenishment using existing EDB transport and validation."""
import argparse,copy,fcntl,hashlib,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import validate as v;g=v.g
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment,build_learning
from inventory_jobs import save
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database
from edn import dumps,loads,kw
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'970f9109d814c4940397ddd3f07be4b289c3a68521c2f57b0b976bde0a4f80b7'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'reference/initial/kp-query.edn').read_text()
RUNTIME=Path('/tmp/course-academy-circle-17592186087656');RUNTIME.mkdir(exist_ok=True)
ENGINE=RUNTIME/'check-engine';POOL=RUNTIME/'check-pool';NATIVE=None

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def setup():
    global NATIVE
    NATIVE=build_learning(ROOT.parent/'EDB')
    deps=ROOT/'target/release/deps';lib=max(deps.glob('libcourse_academy_engine-*.rlib'),key=lambda p:p.stat().st_mtime_ns);serde=max(deps.glob('libserde_json-*.rlib'),key=lambda p:p.stat().st_mtime_ns)
    sources={'check-engine':ROOT/'generate/runs/current/check-engine.rs','check-pool':ROOT/'generate/scratch/17592186110754/check-pool.rs'}
    evidence={'libraries':{str(p.relative_to(ROOT)):sha(p) for p in (lib,serde)},'native_inventory':{'path':str(NATIVE.relative_to(ROOT)),'sha256':sha(NATIVE)},'tools':{}}
    for name,src in sources.items():
        target=RUNTIME/name;fingerprint=sha(src)+sha(lib)+sha(serde);key=target.with_suffix('.hash')
        if not target.exists() or not key.exists() or key.read_text()!=fingerprint:
            subprocess.run(['rustc','--edition=2024','-O',str(src),'--extern','course_academy_engine='+str(lib),'--extern','serde_json='+str(serde),'-L','dependency='+str(deps),'-o',str(target)],check=True,capture_output=True,text=True,timeout=55);key.write_text(fingerprint)
        evidence['tools'][name]={'source':str(src.relative_to(ROOT)),'source_sha256':sha(src),'binary':str(target),'sha256':sha(target)}
    save(HERE/'reference/runtime.json',evidence)
def inventory(p):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]
def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def normalize(q):
    r={k:str(q[k]) for k in (':question/id',':question/problem',':question/worked-solution') if k in q}
    if ':question/difficulty' in q:r[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    r[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        ff={':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f.get(':answer-field/choices',[])]}
        if ':answer-field/correct' in f:ff[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
        r[':question/answer-fields'].append(ff)
    return ordered(r)

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

def validate(r):
    meta=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS and meta['eligible_for_learning'] and not meta['evidence_only']
    assert r['knowledge_point']=={'db_id':KP,'id':g.KP_UUID,'title':g.TITLE}
    replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
    assert ordered(replay['question'])==ordered(r['question']) and replay['generation']==meta
    v.check(r)
def wrap(q):
    q=normalize(q)
    poly=v.eq(__import__('re').findall(r'\$(.*?)\$',q[':question/problem'])[0]);P=v.s.Poly(poly,v.X,v.Y)
    a=-P.coeff_monomial(v.X)/2;b=-P.coeff_monomial(v.Y)/2;S=a*a+b*b-P.coeff_monomial(1)
    params={k:str(val) for k,val in zip(('a','b','S'),(a,b,S))}
    return {'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':q,'generation':{'evidence_only':False,'parameters':params,'parameter_fingerprint':g.digest(params),'template':'standard_circle_radio'}}
def fingerprint(q):return wrap(q)['generation']['parameter_fingerprint']
def native(records,p):
    p.mkdir(parents=True,exist_ok=True);cases=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0]
        cases.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all five owned choices through actual learner grader'} for a in f[':answer-field/choices']]})
    save(p/'input.json',cases)
    if records:subprocess.run([str(ENGINE),str(p/'input.json'),str(p/'result.json')],capture_output=True,text=True,check=True,timeout=55)
def audit_sources(kp,p):
    originals=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions'];byid={q[':question/math-academy-id']:q for q in originals};found=set()
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if not sid:continue
        assert sid in byid,'New source evidence requires reclassification';found.add(sid);assert normalize(q)==normalize(byid[sid]),sid
    assert found==set(byid)
    save(p/'source-refresh-validation.json',{'basis':int(p.name.split('-')[-1]),'frozen_generator_basis':g.SOURCE['basis'],'unchanged_source_questions':len(found),'full_prompts_banks_solutions_designations_difficulties_match':True,'legacy_unrated_excluded':'q-7527 lacks key and solution; retained unchanged'})
def counts(kp,b,p):
    p.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    seen={row[0] for row in shown+reserved};save(p/'scoped-snapshot.json',scoped(kp,b,seen))
    subprocess.run([str(POOL),str(p/'scoped-snapshot.json'),str(p/'native-pool.json')],capture_output=True,text=True,check=True,timeout=55)
    pool=json.loads((p/'native-pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs};levels={l:[] for l in LEVELS};used=set();records=[];excluded=[]
    # Mathematical task fingerprints ignore seed, identity, profile and order.
    # Any unavailable alias makes its mathematical task unavailable as well.
    unavailable_fps={fingerprint(q) for q in kp[':knowledge-point/questions'] if q[':db/id'] in seen}
    for q in kp[':knowledge-point/questions']:
        fp=fingerprint(q)
        if q[':db/id'] not in ids or fp in unavailable_fps or fp in used:
            excluded.append({'id':str(q[':question/id']),'source_id':q.get(':question/math-academy-id'),'reason':'unrated, ungradable, shown, reserved, or mathematical duplicate'});continue
        r=wrap(q);v.check(r);level=q[':question/difficulty'][':db/ident'].split('/')[-1];levels[level].append(str(q[':question/id']));used.add(fp);records.append(r)
    native(records,p/'available-grading')
    result={'basis':b,'levels':{l:{'distinct_available_tasks':len(levels[l]),'available_question_ids':levels[l]} for l in LEVELS},'excluded':excluded,'native_pool':pool,'deduplication':'Exact reduced (a,b,S), independent of seed, identity, option order, bank or notation; previously served aliases excluded.'};save(p/'available-counts.json',result);return result

def finish(p,gid,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS};prep=json.loads((p/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'shortage_remaining':remaining,'available_counts_before':prep['available_counts'],'available_counts_after':after,'capability_exceptions':{'bounded_domain':{'easy':7480,'moderate':7040,'hard':7744},'authored_difficulties':'Moderate: one rational shift. Hard: two rational shifts and familiar radical simplification. Same direct standard-form extraction method. These are authored ratings, not captured source labels.','excluded_source':'Unrated q-7527 lacks key/solution and remains unchanged.'},'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'inventory-after.json',p/'source-refresh-validation.json',HERE/'reference/runtime.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json'] if f.exists()]}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','shortage_remaining')}),flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--inspect',action='store_true');args=ap.parse_args()
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass' and validation['freeze']['script_sha256']==sha(HERE.with_suffix('.py'))
    setup();preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        audit_sources(kp,p);(p/'before.edn').write_text(dumps(kp)+'\n')
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS};print(json.dumps({'basis':b,'missing':needed,'counts':{l:c['levels'][l]['distinct_available_tasks'] for l in LEVELS}}),flush=True)
        if args.inspect:return
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:validate(r)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};records=[];added={l:0 for l in LEVELS};seed=int(JOB.name[:8],16)
        for l in LEVELS:
            candidates=[r for r in instances if r['question'][':question/difficulty']==':question.difficulty/'+l]
            i=0
            while added[l]<needed[l] and i<1000:
                rec=candidates[i] if i<len(candidates) else g.generate(l,seed=seed+i);i+=1;fp=rec['generation']['parameter_fingerprint']
                if fp in used:continue
                validate(rec);records.append(rec);used.add(fp);added[l]+=1
            assert added[l]==needed[l],'Sampling bound reached: requires domain enumeration before declaring finite limit'
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)));native(records,p/'selected-grading')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'asset_hashes':[],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{},'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py'))})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'circle-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
        verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()

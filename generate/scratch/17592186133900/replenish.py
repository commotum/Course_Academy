"""Scoped advanced Green theorem inventory; additive writes under application api.lock."""
import copy,fcntl,hashlib,json,os,re,subprocess,sys,threading,uuid
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
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'b2aef2387cfc3383a05c6eb951afee8fc596c2a13728054d8fc344bc3379c85d'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'reference/source-query.edn').read_text()
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7';POOL=HERE/'reference/native/check-pool';ENGINE=HERE/'reference/native/check-engine'
EXCLUDED={'q-126645':'Duplicate legacy selection field lacks a correct answer; retained unchanged',
'q-126937':'ln(sin(y)^2) is undefined on lines intersecting the region; Green theorem premise invalid',
'q-126939':'Displayed antiderivative of sin(theta) has wrong sign',
'q-126938':'Displayed radial upper bound 2 contradicts radius 3'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,b):return DB.query(QUERY,[[KP]],p,'kp',b)[0][0]
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

def validate(rec):
    meta=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS and not meta['evidence_only'] and not meta['profile'].startswith('raw:')
    assert rec['knowledge_point']['db_id']==KP
    replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
    # Publication changes only the image reference, retaining the original instance.
    if meta.get('published_plot'):
        replay['question'][':question/problem']=replay['question'][':question/problem'].replace(meta['plot'],meta['published_plot'])
    assert ordered(replay['question'])==ordered(rec['question'])
    v.check_math(rec)

def fingerprint_source(q):
    sid=q.get(':question/math-academy-id')
    if sid in g.BY_SOURCE:
        f=g.BY_SOURCE[sid];d=g.FAMILIES[f]
        p={'c':1,'inner':d[4],'outer':d[5]} if f.startswith('annulus') else {'c':1,'outer':d[4],'hole':d[5]}
        Py=g.S.diff(d[2],g.y);Qx=g.S.diff(d[3],g.x)
        return g.digest(g.task_key(d[0],f,p,Py,Qx,g.S.factor(Qx-Py)))
    # Distinct newly captured mathematical families and canonical evidence.
    return g.digest(['source-family',sid])

def native(records,p):
    p.mkdir(parents=True,exist_ok=True);cases=[]
    for rec in records:
        checks=[]
        for i,f in enumerate(rec['question'][':question/answer-fields']):
            if f[':answer-field/type'].endswith('/blank'):
                checks.extend({'field_index':i,'submitted':a,'expected':expected,'purpose':'canonical/equivalent/incorrect'} for a,expected in [('0','accepted'),('1-1','accepted'),('1','rejected')])
            else:
                checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank designation'} for a in f[':answer-field/choices'])
        cases.append({'label':rec['question'][':question/id'],'record':rec,'checks':checks})
    save(p/'input.json',cases)
    subprocess.run([str(ENGINE),str(p/'input.json'),str(p/'report.json')],check=True,timeout=55)

def source_math(q):
    sid=q[':question/math-academy-id'];S=g.S;x,y=g.x,g.y
    if sid in g.BY_SOURCE:
        f=g.BY_SOURCE[sid];d=g.FAMILIES[f];C=S.diff(d[3],x)-S.diff(d[2],y)
        if f.startswith('annulus'):
            z=S.trigsimp(C.subs({x:g.r*S.cos(g.t),y:g.r*S.sin(g.t)})*g.r)
            answer=S.integrate(S.integrate(z,(g.r,d[4],d[5])),(g.t,0,2*S.pi))
        else:
            def integ(B):return S.integrate(C,(x,B[0],B[1]),(y,B[2],B[3]))
            answer=integ(d[4])-integ(d[5])
    elif sid=='q-126936':
        # x=r cos(theta), sqrt(x²+y²)=r for r in [4,8].
        C=3*x*S.sqrt(x*x+y*y)
        answer=S.integrate(S.integrate(3*g.r**3*S.cos(g.t),(g.r,4,8)),(g.t,0,2*S.pi))
    elif sid=='q-126947':
        C=4*x*y*y
        answer=S.integrate(C,(x,-1,2),(y,-2,1))-S.integrate(C,(x,0,1),(y,-1,0))
    else:raise ValueError('Unclassified new source '+str(sid))
    for f in q[':question/answer-fields']:
        assert ':answer-field/correct' in f
        values=[v.parse(a[':answer/value'].replace('\\,','').replace(',','')) for a in f[':answer-field/choices']]
        assert all(S.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[i+1:])
        correct=v.parse(f[':answer-field/correct'][':answer/value'].replace('\\,','').replace(',',''))
        assert S.simplify(correct-answer)==0,(sid,correct,answer)
    return str(answer)

def counts(kp,b,p):
    p.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    seen={r[0] for r in shown+reserved};save(p/'scoped-snapshot.json',scoped(kp,b,seen))
    subprocess.run([str(POOL),str(p/'scoped-snapshot.json'),str(p/'native-pool.json')],capture_output=True,text=True,check=True,timeout=55)
    pool=json.loads((p/'native-pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs}
    known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    levels={l:[] for l in LEVELS};fps={l:set() for l in LEVELS};excluded=[];records=[];mathchecks=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if q[':db/id'] not in ids or sid in EXCLUDED:
            excluded.append({'id':str(q[':question/id']),'source_id':sid,'reason':EXCLUDED.get(sid,'Native pool excludes ungradable, unrated, shown or reserved')});continue
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert level in LEVELS
        if sid:
            answer=source_math(q);fp=fingerprint_source(q)
            rec={'knowledge_point':{'title':kp[':knowledge-point/title']},'question':normalize(q),'generation':{'template':'source:'+sid}}
            mathchecks.append({'source_id':sid,'answer':answer,'full_bank_distinct':True,'worked_solution_review':'source stage review; four known defective sources excluded'})
        else:
            rec=known[str(q[':question/id'])];assert normalize(q)==ordered(rec['question']);validate(rec);fp=rec['generation']['mathematical_fingerprint']
        records.append(rec);fps[level].add(fp);levels[level].append(str(q[':question/id']))
    native(records,p/'grading')
    result={'basis':b,'levels':{l:{'distinct_available_tasks':len(fps[l]),'available_question_ids':levels[l]} for l in LEVELS},'excluded':excluded,'source_mathematics':mathchecks,'native_pool':pool,'deduplication':'exact assessed partials/curl and geometry; full-turn cancellation one task per angular method; excludes seed, identities and option order'}
    save(p/'available-counts.json',result);return result

def publish(records,p):
    assets=[];image_root=Path(DB.env['EDB_MATH_ROOT'])/'images'
    for rec in records:
        meta=rec['generation'];source=Path(meta['plot']);h=sha(source);relative=Path('images')/h[:2]/(h+'.png');dest=image_root/h[:2]/(h+'.png');dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():
            with dest.open('xb') as f:f.write(source.read_bytes());f.flush();os.fsync(f.fileno())
        assert sha(dest)==h
        meta['published_plot']=str(relative);meta['plot_sha256']=h
        rec['question'][':question/problem']=rec['question'][':question/problem'].replace(meta['plot'],str(relative));validate(rec)
        assets.append({'source':str(source.relative_to(ROOT)),'published':str(relative),'sha256':h,'bytes':dest.stat().st_size,'verified':True})
    save(p/'assets.json',assets);return assets

def verify(p,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items());exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(rec['question']);validate(rec)
        assert sha(Path(DB.env['EDB_MATH_ROOT'])/rec['generation']['published_plot'])==rec['generation']['plot_sha256']
    assert not transaction([],kp,intent['generator_id'])
    after=counts(kp,b,p/'readback');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after};save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS};prep=json.loads((p/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'authored_levels':['easy'],'unsupported_levels':[],'unsupported_levels_filled':False,'shortage_remaining':remaining,'available_counts_before':prep['available_counts'],'available_counts_after':after,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':json.loads((HERE/'capabilities.json').read_text()),'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'assets.json',p/'inventory-after.json',HERE/'reference/source-refresh.md',HERE/'validation.json',HERE/'freeze.json'] if f.exists()],'note':'Only distinct, fresh, mathematically checked, actually gradable questions count. Four defective source records remain unchanged and excluded. The application unclassified job can persist because it classifies source-level evidence rather than this narrower validated inventory.'}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','shortage_remaining')}),flush=True)

def main():
    assert json.loads((HERE/'validation.json').read_text())['pass']
    freeze=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/p)==h for p,h in freeze['sha256'].items())
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            assert inventory(p/'recovery-inventory.json')['lineage']==LINEAGE
            verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
        captured=loads((HERE/'reference/initial/kp.edn').read_text())[0][0]
        assert kp==captured,'Source or generator changed; reclassify before writing'
        (p/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.REC[':knowledge-point/id']),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS};print(json.dumps({'basis':b,'missing':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied;instances=[instances] if isinstance(instances,dict) else instances
        for rec in instances:validate(rec)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError') if isinstance(supplied,dict) else None})
        used={fingerprint_source(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint_source(kp[':knowledge-point/canonical-example']))
        records=[];added={l:0 for l in LEVELS}
        for level in LEVELS:
            for i in range(300):
                if added[level]>=needed[level]:break
                rec=next((r for r in instances if r['question'][':question/difficulty']==':question.difficulty/'+level and r['generation']['mathematical_fingerprint'] not in used),None)
                if rec is None:rec=g.generate(level,seed=int(JOB.name[:8],16)+i)
                fp=rec['generation']['mathematical_fingerprint']
                if fp in used:continue
                validate(rec);records.append(rec);used.add(fp);added[level]+=1
        ids=[uuid.UUID(uid) for rec in records for uid in [rec['question'][':question/id']]+[f[':answer-field/id'] for f in rec['question'][':question/answer-fields']]+[a[':answer/id'] for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        assets=publish(records,p);save(p/'generated.json',records);native(records,p/'selected-grading')
        (p/'generated.md').write_text('\n\n---\n\n'.join(rec['question'][':question/problem']+'\n\n'+rec['question'][':question/worked-solution'] for rec in records))
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'asset_hashes':assets,'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{l:needed[l]-added[l] for l in LEVELS if needed[l]>added[l]}})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'advanced-green-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[rec['question'][':question/id'] for rec in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
        verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()

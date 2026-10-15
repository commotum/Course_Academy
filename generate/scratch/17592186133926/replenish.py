"""Additive circulation replenishment through the configured EDB integration."""
import copy,fcntl,hashlib,json,os,random,subprocess,sys,threading,uuid
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
KP=g.DB_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'9624a7cde2bc0f1ad481e23a68e9f669ad634f71347479733e7f956222ec9226'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'reference/source-query.edn').read_text().replace('{:knowledge-point/questions','{[:knowledge-point/questions :limit nil]')
NATIVE=Path((HERE/'reference/learning-executable.txt').read_text());POOL=HERE/'reference/current-runtime/check-pool';ENGINE=HERE/'reference/current-runtime/check-engine'
EXCLUDED={'q-162230':'Source intermediate cos-square argument error; preserved unchanged.', 'q-162235':'Source negative z-force sign error in intermediate stages; preserved unchanged.', 'q-162238':'Source is unrated and lacks a key and worked solution; preserved unchanged.'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
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
def validate(rec):
    meta=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS and meta['eligible_for_learning'] and not meta['evidence_only']
    assert rec['knowledge_point']=={'db_id':KP,'id':g.KP[':knowledge-point/id'],'title':g.KP[':knowledge-point/title']}
    replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
    assert ordered(replay['question'])==ordered(rec['question']) and replay['generation']==meta
    v.normal(rec)
def native(records,p):
    p.mkdir(parents=True,exist_ok=True);save(p/'input.json',[v.native_case(r,str(i)) for i,r in enumerate(records)])
    if records:subprocess.run([str(ENGINE),str(p/'input.json'),str(p/'result.json')],capture_output=True,text=True,check=True,timeout=55)
def supplemental(q):
    # New source at 2686: direct substitution, polynomial product and a square primitive.
    assert q[':question/math-academy-id']=='q-162232'
    assert q[':question/problem']==r'Calculate the circulation $Γ$ of the vector field $F(x,y,z)=x\,i-z\,k$ along the closed curve $C$ given by $r(t)=({t}^{2}-t)\,i+({t}^{3}-{t}^{2})\,j+k$ for $t\in [0,1).$'
    t=v.t;curve=[t*t-t,t**3-t*t,v.sp.S.One];F=[curve[0],v.sp.S.Zero,-curve[2]];dr=[v.sp.diff(e,t) for e in curve]
    assert all(v.eq(e.subs(t,1),e.subs(t,0)) for e in curve)
    product=sum(a*b for a,b in zip(F,dr));primitive=(t*t-t)**2/2
    assert v.eq(v.sp.diff(primitive,t),product) and v.sp.integrate(product,(t,0,1))==0
    rr=v.rows(q[':question/worked-solution']);assert list(map(len,rr))==[2,2,3,5]
    assert v.eq(v.parse(rr[2][-1]),product)
    lo,hi,body=v.bounds(rr[3][1].replace(r'{\int }',r'\int'));assert lo==0 and hi==1
    assert v.eq(v.parse(body.removesuffix(r'\,\text{d}t')),product)
    assert rr[3][2]==r'{[\frac{({t}^{2}-t)^{2}}{2}]}_{0}^{1}' and rr[3][-2]=='(0-0)' and rr[3][-1]=='0'
    f=q[':question/answer-fields'][0];values=[v.parse(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(set(values))==5 and v.parse(f[':answer-field/correct'][':answer/value'])==0
    return {'source_id':'q-162232','difficulty':'easy','fields':'one radio, five math choices','template':'polynomial conservative x force, constant z, closed polynomial xy curve','plot_rating':'none','source_choices':{str(a[':answer/id']):a[':answer/value'] for a in f[':answer-field/choices']},'choice_profile':'exact source evidence only; distractor intentions unresolved; no new generator family claimed','normal_generation_extension':False,'independent_integral':str(product),'primitive':str(primitive),'correct':0,'validated':True}
def audit_sources(kp,p):
    originals=g.ORIGINALS;found=set();rows=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if sid in originals:
            o=originals[sid];found.add(sid)
            for key in (':question/problem',':question/worked-solution'):
                assert q.get(key)==o.get(key),(sid,key,'source evidence changed')
            assert g.enum(q.get(':question/difficulty'))==g.enum(o.get(':question/difficulty'))
            f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0]
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
            assert f.get(':answer-field/correct',{}).get(':answer/value')==of.get(':answer-field/correct',{}).get(':answer/value')
            rows.append(v.audit_source(sid))
        elif sid:rows.append(supplemental(q))
    assert found==set(originals)
    save(p/'source-refresh-validation.json',{'basis':int(p.name.split('-')[-1]),'frozen_generator_basis':1356,'unchanged_sources':8,'additional_source':1,'audits':rows,'excluded_from_validated_inventory':EXCLUDED,'generator_scope':'Existing six authored families retained. Additional easy polynomial source is separately validated; no new family or source bank fidelity claim.'})
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
def counts(kp,b,p):
    p.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    seen={row[0] for row in shown+reserved};save(p/'scoped-snapshot.json',scoped(kp,b,seen))
    subprocess.run([str(POOL),str(p/'scoped-snapshot.json'),str(p/'native-pool.json')],capture_output=True,text=True,check=True,timeout=55)
    pool=json.loads((p/'native-pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs}
    known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    levels={l:[] for l in LEVELS};excluded=[];records=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if q[':db/id'] not in ids or sid in EXCLUDED:
            excluded.append({'id':str(q[':question/id']),'source_id':sid,'reason':EXCLUDED.get(sid,'native pool excludes unrated, ungradable, canonical, shown or reserved')});continue
        l=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert l in LEVELS
        if sid in g.ORIGINALS:
            assert not v.audit_source(sid)['failed_stages'];r={'question':normalize(q)}
        elif sid=='q-162232':supplemental(q);r={'question':normalize(q)}
        else:r=known[str(q[':question/id'])];assert normalize(q)==ordered(r['question']);validate(r)
        records.append(r);levels[l].append(str(q[':question/id']))
    native(records,p/'available-grading')
    result={'basis':b,'levels':{l:{'distinct_available_tasks':len(levels[l]),'available_question_ids':levels[l]} for l in LEVELS},'excluded':excluded,'native_pool':pool,'deduplication':'Source tasks retain distinct curve/field calculations; generated tasks use primitive axis ratios and template identities, ignoring seed and option order. Source-equivalent base pairs excluded from generation.'}
    save(p/'available-counts.json',result);return result

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

def finish(p,gid,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    prep=json.loads((p/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'shortage_remaining':remaining,'available_counts_before':prep['available_counts'],'available_counts_after':after,'capability_exceptions':{'finite_domain':{'easy':66,'moderate':22,'hard':23},'excluded_source_records':EXCLUDED,'new_source_family':'q-162232 is validated as existing inventory only; its opaque bank is not extended.','authored_hard_rating':'Same direct polynomial circulation as unrated q-162238; three-term exact polynomial integration. Not an observed source label.'},'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'inventory-after.json',p/'source-refresh-validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json'] if f.exists()],'note':'All three validated reserves reach five. Legacy source questions remain unchanged, including the unrated incomplete q-162238; the incomplete unrated source is excluded from validated inventory.'}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','shortage_remaining')}),flush=True)
def main():
    assert sha(HERE.with_suffix('.py'))=='ddf47d228f857c5ebf7abeee0d052ff620e30f0cb9db72cf89fff1df1acd5018'
    validation=json.loads((HERE/'validation.json').read_text());assert validation['pass'] and validation['normal_math_instances']==111 and validation['runtime_hashes']['generator']==sha(HERE.with_suffix('.py'))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        # Exact saved outcomes are resolved before reading fresh intent.
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
        assert kp==loads((HERE/'reference/initial/kp.edn').read_text())[0][0],'Source or generator changed since initial read'
        assert str(kp[':knowledge-point/id'])==g.KP[':knowledge-point/id']
        audit_sources(kp,p);(p/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS};print(json.dumps({'basis':b,'missing':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:validate(r)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        used=set();known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
        for q in kp[':knowledge-point/questions']:
            if ':question/math-academy-id' not in q:used.add(known[str(q[':question/id'])]['generation']['mathematical_fingerprint'])
        # All originals include unit-axis tasks. Avoid them even if unrated,
        # served, defective, or expressed through a different parametrization.
        source_slots={('xy_rotation',1,1,-1),('xy_rotation',2,1,1),('xy_rotation_z',1,1,1),('yz_rotation',1,1,-1),('yz_rotation',1,1,1),('xy_symmetric',1,1,1),('polynomial_sine',1,1,1),('polynomial_loop',1,1,1)}
        records=[];added={l:0 for l in LEVELS};seed=int(JOB.name[:8],16)
        for l in LEVELS:
            candidates=list(instances)
            domain=[(template,params) for template,(level,_) in g.TEMPLATES.items() if level==l for params in g.domains(template)]
            random.Random(seed).shuffle(domain)
            candidates.extend(g.generate(l,seed=seed+i,template=template,parameters=params) for i,(template,params) in enumerate(domain))
            for rec in candidates:
                if added[l]>=needed[l]:break
                if rec['question'][':question/difficulty']!=':question.difficulty/'+l:continue
                meta=rec['generation'];params=meta['parameters'];slot=(meta['template'],params['a'],params['b'],params.get('sign',1));fp=meta['mathematical_fingerprint']
                if fp in used or slot in source_slots:continue
                validate(rec);records.append(rec);used.add(fp);added[l]+=1
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)));native(records,p/'selected-grading')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'asset_hashes':[],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{l:needed[l]-added[l] for l in LEVELS if needed[l]>added[l]},'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'validated_source_equivalence_exclusions':[list(x) for x in sorted(source_slots)]})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'circulation-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
        verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()

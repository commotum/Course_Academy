"""Scoped ellipse replenishment using existing native pool, grader and EDB writer."""
import copy,fcntl,hashlib,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import validate as v;g=v.g
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'64c450af184b68a296ab1eb61c2c2f39a23bada90eee09e82007bb07f6cf15ba'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'reference/source-query.edn').read_text()
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7';POOL=ROOT/'generate/scratch/17592186110754/check-pool'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]

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

def fingerprint(q):
    q=copy.deepcopy(q);q[':question/problem']=q[':question/problem'].replace(r'\dfrac',r'\frac')
    dx,dy,_=v.formula_from_prompt(q)
    return g.digest(sorted([str(dx),str(dy)]))

def validate(rec):
    m=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS and m['eligible_for_learning'] and not m['evidence_only']
    replay=g.generate(level,m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])
    assert m==replay['generation'] and ordered(rec['question'])==ordered(replay['question'])
    v.inspect_record(rec)
    assert fingerprint(rec['question'])==m['mathematical_fingerprint']

def native(records,p):
    p.mkdir(parents=True,exist_ok=True)
    fixtures=[v.engine_item(r,r['question'][':question/id']) for r in records]
    assert all(fixtures)
    save(p/'input.json',fixtures)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,capture_output=True,text=True,timeout=55)

def as_record(q):
    nq=normalize(q);dx,dy,_=v.formula_from_prompt(nq)
    return {'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':nq,
            'generation':{'parameters':{'dx':str(dx),'dy':str(dy)},'template':'source_readback','source_id':q.get(':question/math-academy-id'),'evidence_only':bool(q.get(':question/math-academy-id')),'eligible_for_learning':not bool(q.get(':question/math-academy-id'))}}

def counts(kp,b,p):
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    save(p/'scoped-snapshot.json',scoped(kp,b,{r[0] for r in shown+reserved}))
    subprocess.run([str(POOL),str(p/'scoped-snapshot.json'),str(p/'pool.json')],check=True,capture_output=True,text=True,timeout=55)
    pool=json.loads((p/'pool.json').read_text());available={e for xs in pool['available_ids_by_level'].values() for e in xs}
    levels={l:set() for l in LEVELS};records=[];excluded=[]
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] not in available:
            excluded.append({'id':str(q[':question/id']),'reason':'Native pool excludes unrated, canonical, ungradable, shown or reserved'});continue
        try:
            rec=as_record(q);v.inspect_record(rec)
            native([rec],p/('grade-'+str(q[':db/id'])))
        except (AssertionError,ValueError,KeyError,subprocess.CalledProcessError) as e:
            excluded.append({'id':str(q[':question/id']),'reason':'Source content fails mathematical/rendering/grading validation: '+str(e)[:300]});continue
        level=rec['question'][':question/difficulty'].split('/')[-1]
        levels[level].add(fingerprint(q));records.append(rec)
    result={'basis':b,'levels':{l:len(fps) for l,fps in levels.items()},'excluded':excluded,'native_pool':pool,'deduplication':'unordered exact squared-radius pairs, ignoring orientation, bank, field shape, identity, seed and order'}
    save(p/'counts.json',result);return result

def source_audit(kp,p):
    old=json.loads((HERE/'source.json').read_text())['record'];before={q[':question/math-academy-id']:q for q in old[':knowledge-point/questions']}
    def canonical(q):
        x=v.source_normalized(q);x['fields'].sort(key=lambda f:f['key']);return x
    current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id'in q}
    assert before.keys()<=current.keys()
    for mid,q in before.items():assert canonical(q)==canonical(current[mid]),mid
    additions=[]
    for mid in current.keys()-before.keys():
        q=current[mid];dx,dy,_=v.formula_from_prompt(q)
        replay=g.generate('easy',parameters={'dx':str(dx),'dy':str(dy)},field_type='blank')
        a=canonical(q);z=canonical(replay['question']);bad=[]
        for f in a['fields']:
            # Preserve doubled-backslash source errors; compare corrected evidence only.
            for i,(typ,value) in enumerate(f['choices']):
                if '\\\\' in value:
                    bad.append({'field':f['key'],'original':value,'supported_value':value.replace('\\\\','\\')})
                    f['choices'][i]=(typ,value.replace('\\\\','\\'))
            if f['correct'] and '\\\\' in f['correct']:f['correct']=f['correct'].replace('\\\\','\\')
        assert a==z,mid
        additions.append({'source_id':mid,'parameters':{'dx':str(dx),'dy':str(dy)},'template':'blank','difficulty':'easy','plots':'none','source_errors_preserved':bad,'complete_bank_and_solution_replay':'matched after documented evidence correction'})
    report={'basis':DB.basis(),'original_21_source_questions_unchanged':True,'additional_source_cases':additions,'generator_change_needed':False,'classification':'New sources use existing easy paired-blank template; no new banks, plots, roles or method.'}
    save(p/'source-audit.json',report)

def verify(p,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_report(report,p/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    ignore={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in kp.items() if k not in ignore}=={k:v for k,v in before.items() if k not in ignore}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,b,p/'readback')
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
    c=verified['available_counts_after'];remaining={l:max(0,5-c['levels'][l]) for l in LEVELS}
    assert not any(remaining.values()),remaining
    result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'shortage_remaining':remaining,'available_counts_after':c['levels'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':[],'finite_task_limits':{'easy_blank':4950,'easy_radio':4949,'moderate':11700,'hard':153},'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'inventory-after.json',p/'source-audit.json',HERE/'reference/package-validation.json']]}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
    qa=json.loads((ROOT/'generate/runs/current/qa/17592186087841.json').read_text());assert qa['parent_review']=='passed' and sha(HERE.with_suffix('.py'))==qa['generator_sha256']
    assert all(sha(ROOT/p)==d for p,d in qa['root_artifact_sha256'].items())
    save(HERE/'reference/package-validation.json',{'parent_review':'passed','all_frozen_artifact_hashes_verified':True,'generator_sha256':sha(HERE.with_suffix('.py')),'qa_report':'generate/runs/current/qa/17592186087841.json','sympy_version':str(v.sp.__version__)})
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b);source_audit(kp,p)
        (p/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]) for l in LEVELS}
        print(json.dumps({'basis':b,'available':c['levels'],'needed':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:validate(r)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
        used={fingerprint(q) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]}
        records=[];added={l:0 for l in LEVELS};seed=int(JOB.name[:8],16)
        for l in LEVELS:
            candidates=[r for r in instances if r['question'][':question/difficulty']==':question.difficulty/'+l]
            for n in range(1000):
                if added[l]>=needed[l]:break
                rec=candidates[n] if n<len(candidates) else g.generate(l,seed=seed+n,field_type='blank' if n%2 else 'radio')
                fp=fingerprint(rec['question'])
                if fp in used:continue
                validate(rec);records.append(rec);used.add(fp);added[l]+=1
            assert added[l]==needed[l], 'Bounded sampling exhausted: leave explicit shortage'
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)));native(records,p/'selected-grading')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'asset_hashes':{},'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True})
        forms=transaction(records,kp,gid);assert forms
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        # Final inventory and basis check precede preview/submission under the same lock.
        assert DB.basis()==b
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55)
        (p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'ellipse-axes-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(p/'commit-intent.json',intent);print('Validated and previewed; submitting exact durable request',flush=True)
        verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))

if __name__=='__main__':main()

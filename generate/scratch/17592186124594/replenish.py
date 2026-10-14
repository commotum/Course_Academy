"""KP-scoped polar-derivative replenishment through existing EDB integration."""
import copy, fcntl, hashlib, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
import validate as v
import current_sources as cs
g=v.g
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment,build_learning
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.CAPTURE['lineage']
SOURCE=':application/ca-engine';SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'18bcc17e922f30bfd78cde35301f27ca264012af6de81609aea6222053ec72b6'
OUT=HERE/'reference/replenishment';LEVELS=('easy','moderate','hard')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'reference/source-query.edn').read_text()
POOL=ROOT/'generate/scratch/17592186110754/check-pool'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    return str(value) if isinstance(value,uuid.UUID) else value

def normalize(q):
    result={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    level=q[':question/difficulty'];result[':question/difficulty']=str(level[':db/ident']) if isinstance(level,dict) else level
    result[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        typ=f[':answer-field/type'];correct=f[':answer-field/correct']
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(typ[':db/ident']) if isinstance(typ,dict) else typ,':answer-field/correct':[':answer/id',str(correct[':answer/id']) if isinstance(correct,dict) else correct[1]],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']) if isinstance(a[':answer/type'],dict) else a[':answer/type'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    result[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in result[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return result

def native(r):
    f=r['question'][':question/answer-fields'][0]
    return {'label':str(r['question'][':question/id']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual learner radio grading'} for a in f[':answer-field/choices']]}

def inventory(binary,path):
    proc=subprocess.run([str(binary),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    response=json.loads(proc.stdout);assert response['ok'] and response['data']['lineage']==LINEAGE
    save(path,response['data']);return response['data']

def transaction(records,kp,gid):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_datoms(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')}|{':answer-field/'+s for s in ('id','key','type','choices','correct')}|{':answer/'+s for s in ('id','type','value')}|{':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected existing entity change'

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

def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]

def validate(r):
    meta=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS
    replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
    assert canonical(replay)==canonical(r),'Stored generation differs from deterministic replay'
    v.check_record(r)
    assert cs.fingerprint(r['question'])==meta['mathematical_fingerprint']

def normalize_for_native(q):return normalize(q)

def native_check(records,path):
    path.mkdir(parents=True,exist_ok=True)
    save(path/'native-input.json',[native(r) for r in records])
    if not records:
        save(path/'native-report.json',{'questions':0,'accepted_checks':0,'rejected_checks':0,'documented_unresolved_checks':0});return
    proc=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,capture_output=True,text=True,timeout=55)
    (path/'native.log').write_text(proc.stdout+proc.stderr)
    report=json.loads((path/'native-report.json').read_text())
    assert report['accepted_checks']==len(records) and report['rejected_checks']==4*len(records) and report['documented_unresolved_checks']==0

def validate_sources(kp):
    before=loads((OUT/'initial-snapshot.edn').read_text())
    sources=lambda x:{q[':question/math-academy-id']:q for q in x[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    assert canonical(sources(kp))==canonical(sources(before)),'Current source evidence changed: reopen classification'
    assert canonical(kp[':knowledge-point/canonical-example'])==canonical(before[':knowledge-point/canonical-example'])

def counts(kp,path,basis,records=()):
    path.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],path,'ever-shown',basis,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],path,'reserved',basis)
    unavailable={row[0] for row in shown+reserved}
    save(path/'scoped-snapshot.json',scoped(kp,basis,unavailable))
    subprocess.run([str(POOL),str(path/'scoped-snapshot.json'),str(path/'native-pool.json')],capture_output=True,text=True,check=True,timeout=55)
    pool=json.loads((path/'native-pool.json').read_text());available_ids={e for ids in pool['available_ids_by_level'].values() for e in ids}
    known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    known.update({r['question'][':question/id']:r for r in records})
    source_reports={r['source_id']:r for r in json.loads((OUT/'current-source-audit.json').read_text())}
    available={l:{} for l in LEVELS};excluded=[];used={cs.canonical_fp()};fixtures=[]
    for q in kp[':knowledge-point/questions']:
        fp=cs.fingerprint(q);used.add(fp)
        sid=q.get(':question/math-academy-id');ident=str(q[':question/id'])
        if sid:
            audit=source_reports[sid];assert fp==audit['mathematical_fingerprint']
            valid=audit['validated_practice']
            reason='; '.join(audit['errors'])
        else:
            assert ident in known,'Unknown generated record: reconcile before writing'
            r=known[ident];validate(r);assert normalize(q)==normalize(r['question']);valid=True;reason=''
        if not valid or q[':db/id'] not in available_ids:
            excluded.append({'id':q[':db/id'],'question_id':ident,'source_id':sid,'reason':reason or 'native pool excludes shown/reserved/unrated/ungradable/canonical'});continue
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        assert level in LEVELS
        available[level][fp]=ident;fixtures.append({'question':normalize(q)})
    native_check(fixtures,path/'available-grading')
    result={'basis':basis,'available_by_level':{l:len(a) for l,a in available.items()},'available_question_ids':{l:sorted(a.values()) for l,a in available.items()},'excluded':excluded,'shown_or_reserved':sorted(unavailable),'native_pool':pool,'deduplication':'Exact Cartesian partial pair and derivative target, excluding additive constants, common log-argument scale, seed, labels, identities, profiles and option order.'}
    save(path/'available-counts.json',result);return result,used

def verify(path,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_datoms(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());validate_sources(kp)
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    omit={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:z for k,z in before.items() if k not in omit}=={k:z for k,z in kp.items() if k not in omit}
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        validate(r);q=byid[r['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q)==normalize(r['question'])
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    assert not transaction([],kp,intent['generator_id'])
    stock,_=counts(kp,path/'readback',basis,records)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'all_datoms_from_configured_contributor':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'inventory':stock}
    save(path/'verification.json',result);return result

def finish(path,intent,verified,binary):
    inv=inventory(binary,path/'inventory-after.json');kp=read_kp(path/'final-inventory',inv['basis']);validate_sources(kp)
    stock,_=counts(kp,path/'final-inventory',inv['basis'])
    shortage={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['new_by_level'],'supported_levels':list(LEVELS),'authored_difficulties':['moderate','hard'],'available_by_level':stock['available_by_level'],'shortage_remaining':shortage,'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':json.loads((HERE/'capabilities.json').read_text()),'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'selected-grading/native-report.json',path/'inventory-after.json',path/'final-inventory/available-counts.json',HERE/'validation.json',OUT/'current-source-audit.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-spec.md') if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions_by_level','available_by_level','shortage_remaining','remaining_jobs')}),flush=True)

def main():
    frozen=json.loads((HERE/'freeze.json').read_text());validation=json.loads((HERE/'validation.json').read_text())
    assert frozen['generator_sha256']==sha(HERE.with_suffix('.py'))==validation['generator_sha256'] and validation['passed']
    parent=json.loads((ROOT/'generate/runs/current/qa'/f'{KP}.json').read_text());assert parent['parent_review']=='passed' and parent['generator_sha256']==sha(HERE.with_suffix('.py'))
    save(OUT/'frozen-generator-validation.json',parent)
    binary=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path(DB.env['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    # Recheck current inventory before executing the validated generator.
    initial=inventory(binary,OUT/'inventory-before.json');before=read_kp(OUT/'pre-generation',initial['basis']);validate_sources(before)
    initial_stock,initial_used=counts(before,OUT/'pre-generation',initial['basis'])
    supplied_path=JOB.with_suffix('.generated');supplied_exists=supplied_path.exists()
    supplied=json.loads(supplied_path.read_text()) if supplied_exists else {}
    instances=supplied.get('instances',[]);assert isinstance(instances,list)
    for r in instances:validate(r)
    staged=list(instances);new_staged={l:0 for l in LEVELS};used=set(initial_used)
    for r in instances:used.add(r['generation']['mathematical_fingerprint'])
    seed=int(JOB.name[:8],16)
    for l in LEVELS:
        need=max(0,5-initial_stock['available_by_level'][l])
        for i in range(200):
            if new_staged[l]>=need:break
            r=g.generate(l,seed=seed+i)
            fp=r['generation']['mathematical_fingerprint']
            if fp in used:continue
            validate(r);staged.append(r);used.add(fp);new_staged[l]+=1
    save(OUT/'staged.json',staged)
    if not supplied_exists:save(supplied_path,{'request':json.loads(JOB.with_suffix('.json').read_text())['request'],'instances':staged,'preparation_basis':initial['basis'],'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py'))})
    print(json.dumps({'pre_generation_basis':initial['basis'],'available':initial_stock['available_by_level'],'staged':new_staged,'supplied_instances_validated':len(instances)}),flush=True)
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn') and intent['generator_sha256']==sha(HERE.with_suffix('.py'))
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent,verify(path,intent,report),binary);return
        inv=inventory(binary,OUT/'inventory-locked.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);validate_sources(kp)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n');stock,used=counts(kp,path/'current-inventory',b)
        needed={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],path,'generator-identity',b)
        if registered:
            assert len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
            gid=str(registered[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or registered)})
        selected={l:0 for l in LEVELS};records=[]
        for r in staged:
            validate(r);l=r['question'][':question/difficulty'].split('/')[-1];fp=r['generation']['mathematical_fingerprint']
            if selected[l]<needed[l] and fp not in used:records.append(copy.deepcopy(r));used.add(fp);selected[l]+=1
        # A changed inventory basis can need additional distinct variants.
        for l in LEVELS:
            for i in range(200,400):
                if selected[l]>=needed[l]:break
                r=g.generate(l,seed=seed+i);fp=r['generation']['mathematical_fingerprint']
                if fp in used:continue
                validate(r);records.append(r);used.add(fp);selected[l]+=1
        assert all(selected[l]==needed[l] for l in LEVELS),'Bounded search failed; document explicit finite-limit rather than submit incomplete claims'
        save(path/'generated.json',records)
        (path/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)))
        native_check(records,path/'selected-grading')
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'generated-identities',b)
        save(path/'preparation.json',{'basis':b,'original_job_basis':1831,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'selected_by_level':selected,'unproduced_by_level':{l:needed[l]-selected[l] for l in LEVELS},'available_before':stock,'source_evidence_unchanged':True,'asset_hashes':[],'supplied_generated_existed':supplied_exists,'supplied_instances_validated':len(instances),'generator_sha256':sha(HERE.with_suffix('.py')),'mathematics_validated':True,'actual_grader_validated':True,'distinctness':stock['deduplication']})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'new_by_level':selected};save(path/'verification.json',{'passed':True,'no_changes':True,**verified});finish(path,{'generator_id':gid},verified,binary);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        proc=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(proc.stdout);pr=loads(proc.stdout);assert not pr[':edb/committed'] and pr[':edb/db-before-t']==b
        check_datoms(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'polar-derivative-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        print(json.dumps({'prepared_basis':b,'needed':needed,'selected':selected,'request_key':intent['request_key']}),flush=True)
        report=DB._commit(intent,txpath,path);finish(path,intent,verify(path,intent,report),binary)
if __name__=='__main__':main()

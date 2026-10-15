"""Scoped additive replenishment; serialize with the application's durable worker."""
import copy, fcntl, hashlib, importlib.util, json, os, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'a49b15988c4d0c389ef8d72a2e40bc5a2cac39b6f24be51c91d15513969da119'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=Path(json.loads((HERE/'native-runtime.json').read_text())['binary'])
QUERY=(HERE/'source-query.edn').read_text()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(path):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),text=True,capture_output=True,check=True,timeout=55)
    data=json.loads(r.stdout);assert data['ok'] and data['data']['lineage']==LINEAGE
    save(path,data['data']);return data['data']
def read_kp(path,b):return DB.query(QUERY,[[KP]],path,'kp',b)[0][0]
def scoped(kp,b,seen):
    entities={};enums={};next_enum=1
    def enum(value):
        nonlocal next_enum
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            enums[name]=next_enum;entities[str(next_enum)]={'db/ident':name};next_enum+=1
        return enums[name]
    def question(q):
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]}
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        entities[str(q[':db/id'])]=r
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id'])
            field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]}
            if ':answer-field/correct' in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            entities[str(f[':db/id'])]=field
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:question(q)
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}
def available(kp,b,path):
    path.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],path,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],path,'reserved',b)
    seen={row[0] for row in shown+reserved}
    # Read the native pool only after independent mathematical validation.
    # Retain excluded originals in EDB; this is a read-only scoped inventory.
    filtered=copy.deepcopy(kp);accepted=[];excluded=[];duplicates=[]
    used={v.fingerprint(kp[':knowledge-point/canonical-example'])}
    for q in sorted(kp[':knowledge-point/questions'],key=lambda q:q[':db/id']):
        try:v.source_valid(q)
        except (AssertionError,KeyError,ValueError,TypeError,StopIteration) as error:
            excluded.append({'id':q[':db/id'],'reason':repr(error)});continue
        fp=v.fingerprint(q)
        if fp in used:duplicates.append(q[':db/id']);continue
        used.add(fp);accepted.append(q)
    # Equivalent content shown under another identity remains exhausted.
    shown_fps={v.fingerprint(q) for q in kp[':knowledge-point/questions'] if q[':db/id'] in seen}
    seen.update(q[':db/id'] for q in accepted if v.fingerprint(q) in shown_fps)
    filtered[':knowledge-point/questions']=accepted
    save(path/'mathematical-filter.json',{'excluded':excluded,'duplicate_or_canonical_equivalent_ids':duplicates,'validated_distinct_ids':[q[':db/id'] for q in accepted],'source_questions_modified':0})
    save(path/'scoped-snapshot.json',scoped(filtered,b,seen))
    subprocess.run([str(HERE/'check-pool'),str(path/'scoped-snapshot.json'),str(path/'available-counts.json')],check=True,timeout=55)
    return json.loads((path/'available-counts.json').read_text())
def normalize(q):
    r={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    r[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);r[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        r[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
    return r
def transaction(records,kp,gid):
    forms=[]
    for rec in records:
        q=rec['question']
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
def check_report(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected contributor or retraction';name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected or unscoped datom'
def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    b=report[':edb/db-after-t'];check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',b);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in excluded}=={k:v for k,v in kp.items() if k not in excluded}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        expected=copy.deepcopy(rec['question'])
        for f in expected[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
        assert normalize(q)==expected;v.check(rec)
    assert not transaction([],kp,intent['generator_id'])
    counts=available(kp,b,path/'readback/inventory')
    shortfalls=json.loads((path/'preparation.json').read_text())['shortfalls']
    assert shortfalls or len(counts['available_ids_by_level'].get('hard',[]))>=5
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_by_level':{level:len(ids) for level,ids in counts['available_ids_by_level'].items()}}
    save(path/'verification.json',result);return result
def finish(path,verified,inv,gid,shortfalls):
    result={'outcome':'finite-limit' if shortfalls else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'available_by_level':verified['available_by_level'],'supported_levels':['hard'],'unsupported_levels':['easy','moderate'],'unsupported_levels_filled':False,'unfilled_reserves':{'easy':5,'moderate':5},'finite_shortfalls':shortfalls,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
        'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'native-grading.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'review.json',HERE/'review.md',HERE/'capabilities.json')],
        'note':'Validated hard RREF generator; five complete source banks and all 50 bounded instances pass exact mathematics and native grading. Source questions, canonical example and learner history preserved. Easy/moderate unsupported reserves explicitly unfilled.'}
    result['remaining_supported_shortages']=[j for j in result['remaining_jobs'] if j['difficulty']=='hard']
    assert shortfalls or not result['remaining_supported_shortages']
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    save(HERE/'freeze.json',{'version':g.VERSION,'generator_id':gid,'script':SCRIPT,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'verified_commit_basis':verified['basis_after'],'validation_hashes':json.loads((HERE/'validation.json').read_text())['hashes'],'supported_levels':['hard'],'unsupported_levels':['easy','moderate'],'unsupported_levels_filled':False})
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','remaining_jobs')}),flush=True)
def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed'] and json.loads((HERE/'review.json').read_text())['passed']
    assert all(sha(ROOT/p)==digest for p,digest in validation['hashes'].items())
    assert json.loads((HERE/'native-build.json').read_text())['engine_library_newer_than_grader_sources']
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        prior=[]
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['lineage']==LINEAGE and intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
            assert intent['sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            prior.append((path,intent,verify(path,intent,DB._commit(intent,path/'transaction.edn',path))))
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        evidence=loads((HERE/'source.edn').read_text())[0][0];current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(current[q[':db/id']]==q for q in evidence[':knowledge-point/questions']),'Source changed: reclassify'
        assert kp[':knowledge-point/canonical-example']==evidence[':knowledge-point/canonical-example']
        counts=available(kp,b,path/'current-inventory');count=len(counts['available_ids_by_level'].get('hard',[]));needed=max(0,5-count)
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or (len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT)
        byscript=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-script',b)
        assert not byscript or len(byscript)==1 and str(byscript[0][0][':question-generator/id'])==gid,'Existing script identity requires reconciliation; never allocate another'
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=instances.get('instances',[instances])
        valid=[];invalid=[]
        for i,rec in enumerate(instances):
            try:
                v.check(rec);assert not rec['generation']['replay'];valid.append(rec)
            except (ValueError,AssertionError,KeyError,TypeError) as error:invalid.append({'index':i,'reason':repr(error)})
        assert not invalid,'Supplied generated instances failed validation; retained for correction'
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated':len(valid),'invalid':invalid,'generator_error':supplied.get('generatorError')})
        used={v.fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(v.fingerprint(kp[':knowledge-point/canonical-example']))
        records=[]
        if needed:
            domain=list(g.candidates('hard'));seen=set()
            for rec in valid+[g.generate('hard',b,entry['profile'],{k:v for k,v in entry.items() if k!='profile'}) for entry in domain]:
                v.check(rec);fp=v.fingerprint(rec['question'])
                if fp not in used and fp not in seen and len(records)<needed:records.append(rec);seen.add(fp)
        save(path/'generated.json',records)
        if records or valid:
            save(path/'native-input.json',[v.native(str(i),r) for i,r in enumerate(records+valid)])
            subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,timeout=55)
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        if ids:assert not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'identities',b)
        shortfalls=[] if len(records)==needed else [{'level':'hard','status':'finite-limit','missing':needed,'generated':len(records),'unfilled':needed-len(records),'evidence':'Exhausted 50 bounded augmented row spaces after excluding existing/source/canonical systems; seed and bank order do not create fresh mathematics.'}]
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_hard':count,'needed_hard':needed,'new_questions':len(records),'source_evidence_unchanged':True,'distinctness':'Exact augmented RREF; equivalent equation systems and all seed/bank/order changes excluded','asset_hashes':[],'shortfalls':shortfalls})
        forms=transaction(records,kp,gid)
        if not forms:
            assert prior,'Registration lacks a saved receipt; reconcile'
            last,intent,verified=prior[-1];finish(last,verified,inventory(last/'inventory-after.json'),gid,shortfalls);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'two-pivot-rref-replenish-17592186096745-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        verified=verify(path,intent,DB._commit(intent,txpath,path))
        finish(path,verified,inventory(path/'inventory-after.json'),gid,shortfalls)
if __name__=='__main__':main()

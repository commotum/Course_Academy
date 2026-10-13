"""Additive scoped EDB commit; application lock held through exact-basis readback."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('v',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'cf15bdf39c8f07e5814e293eb30edf20e454643a1bf9d99088e2bfba71feb12e'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
CLIENT=EDBClient(Config(postgres_url=ENV['EDB_POSTGRES_URL']),threading.Event())
NATIVE=ROOT/'.local/graph-explorer/learning-80371ed6e5f3669c'
QUERY=(HERE/'reference/source-query.edn').read_text()
USAGE='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(path):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def normalize(q):
    result={k:str(q[k])if k==':question/id'else q[k]for k in (':question/id',':question/problem',':question/worked-solution')}
    result[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);result[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']}for a in f[':answer-field/choices']]})
    return ordered(result)
def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q
def available(path,kp,b):
    unavailable={r[0]for r in DB.query(USAGE,[KP,LEARNER],path,'unavailable',b)}
    unavailable.update(r[0]for r in DB.query(USAGE,[KP,LEARNER],path,'historically-unavailable',b,history=True))
    pools={level:[]for level in g.SUPPORTED_LEVELS};excluded=[];native=[]
    for q in kp[':knowledge-point/questions']:
        try:
            assert q[':db/id']not in unavailable,'shown/reserved (including retained history)'
            assert not q.get(':knowledge-point/_canonical-example'),'canonical example'
            level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1];assert level in pools,'unrated/unsupported'
            nq=normalize(q);assert nq[':question/worked-solution'] and len(nq[':question/answer-fields'])==1,'incomplete'
            v.validate_current(nq,False,q.get(':question/math-academy-id'))
            fp=g.fingerprint(nq);pools[level].append((str(q[':question/id']),fp))
            native.append({'label':str(q[':question/id']),'record':{'knowledge_point':{'title':g.TITLE},'question':nq,'generation':{'template':'current-source'}},'checks':v.checks_for(nq)})
        except (AssertionError,ValueError,KeyError,StopIteration)as e:excluded.append({'question':str(q[':question/id']),'reason':str(e)})
    save(path/'available-native-input.json',native)
    if native:subprocess.run([str(HERE/'check-current-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True)
    counts={'basis':b,'levels':{level:{'distinct_available_tasks':len({fp for _,fp in rows}),'question_ids':[qid for qid,_ in rows]}for level,rows in pools.items()},'excluded':excluded,'shown_reserved':sorted(unavailable)};save(path/'available-counts.json',counts);return counts
def transaction(records,kp,gid):
    forms=[]
    for rec in records:
        q=rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id']for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id']for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen is None:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id']for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms
def check_report(report,path,source):
    attrs={e:str(a)for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':'+s for s in ('question/id','question/problem','question/worked-solution','question/difficulty','question/answer-fields','answer-field/id','answer-field/key','answer-field/type','answer-field/choices','answer-field/correct','answer/id','answer/type','answer/value','question-generator/id','question-generator/script')}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'unexpected source/retraction';name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,(e,name)
def verify(path,intent,report):
    assert report[':edb/committed']is True and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read_kp(path/'readback',b);before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(now[e]==q for e,q in old.items())
    assert {k:x for k,x in before.items()if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:x for k,x in kp.items()if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id']and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id'not in q and normalize(q)==ordered(rec['question']);v.validate(rec,False)
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_scoped_additive_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_changes':0,'available_counts_after':available(path/'readback',kp,b)};save(path/'verification.json',result);return result
def finish(path,gid,verified,inv):
    shortages={level:max(0,5-verified['available_counts_after']['levels'][level]['distinct_available_tasks'])for level in g.SUPPORTED_LEVELS};shortages['hard']=5
    result={'outcome':'finite-limit'if any(shortages[l]for l in g.SUPPORTED_LEVELS)else'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'lineage':LINEAGE,'supported_levels':list(g.SUPPORTED_LEVELS),'shortage_remaining':shortages,'unsupported_levels_filled':False,'finite_distinct_variant_limits':json.loads((HERE/'validation.json').read_text())['finite_distinct_tasks'],'commit_status':'no-changes'if verified.get('no_changes')else'verified','capability_exceptions':[{'level':'hard','supported':False,'shortage':5,'reason':json.loads((HERE/'capabilities.json').read_text())['reason']}]+[{'level':l,'supported':True,'shortage':shortages[l],'reason':'All frozen r=2..6 mathematical tasks are already present or duplicates; bounded finite pool exhausted.'}for l in g.SUPPORTED_LEVELS if shortages[l]],'available_counts_after':verified['available_counts_after'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs']if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT))for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'transaction.edn',path/'preparation.json',path/'inventory-after.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'review.md',HERE/'classification.md',HERE/'capabilities.json')if p.exists()]};save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2))
def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']and all(sha(ROOT/f)==digest for f,digest in validation['hashes'].items())
    freeze=json.loads((HERE/'freeze.json').read_text());assert freeze['side_by_side_review']=='passed'and all(sha(ROOT/f)==digest for f,digest in freeze['files'].items())
    preview=preview_executable(Config(),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a')as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math'and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
                assert intent['exact_edn']==(path/'transaction.edn').read_text()and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert CLIENT.status()['lineage']==LINEAGE
                report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent['generator_id'],verify(path,intent,report),inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];status=CLIENT.status();assert status['basis']==b and status['lineage']==LINEAGE
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n');original=loads((HERE/'reference/source.edn').read_text())[0][0]
        old={q[':db/id']:q for q in original[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(now[e]==q for e,q in old.items())and original[':knowledge-point/canonical-example']==kp[':knowledge-point/canonical-example']
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id'])if gen else g.GENERATOR_UUID
        counts=available(path,kp,b);needed={l:max(0,5-counts['levels'][l]['distinct_available_tasks'])for l in g.SUPPORTED_LEVELS}
        used=set()
        for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:used.add(g.fingerprint(q))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text())if supplied_path.exists()else{};instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=instances.get('instances',[])
        assert isinstance(instances,list);eligible=[];rejected=[]
        for rec in instances:
            try:v.validate(rec);eligible.append(rec)
            except (AssertionError,ValueError,KeyError)as e:rejected.append({'reason':str(e),'question_id':rec.get('question',{}).get(':question/id')})
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated':len(eligible),'rejected':rejected,'generator_error':supplied.get('generatorError')})
        records=[];v.native.clear()
        for level in g.SUPPORTED_LEVELS:
            remaining=needed[level]
            local=g.batch(level,1000,int(JOB.name[:8],16))if remaining else[];save(path/('preview-'+level+'.json'),local)
            for rec in eligible+local:
                if rec['question'][':question/difficulty']!=':question.difficulty/'+level:continue
                v.validate(rec,False);fp=g.fingerprint(rec['question'])
                if remaining and fp not in used:records.append(rec);used.add(fp);remaining-=1;v.validate(rec)
        save(path/'generated.json',records);save(path/'native-input.json',v.native);subprocess.run([str(HERE/'check-current-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        for kind in ('question','answer-field','answer'):
            ids=[item[':'+kind+'/id']for rec in records for item in ([rec['question']]if kind=='question'else rec['question'][':question/answer-fields']if kind=='answer-field'else[a for f in rec['question'][':question/answer-fields']for a in f[':answer-field/choices']])];assert len(ids)==len(set(ids))
            if ids:assert not DB.query('[:find ?e :in $ [?id ...] :where [?e :'+kind+'/id ?id]]',[list(map(uuid.UUID,ids))],path,'identity-'+kind,b)
        if not gen:assert not DB.query('[:find ?e :in $ ?id :where [?e :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'needed':needed,'new_questions':len(records),'distinct_generated_tasks':len({g.fingerprint(r['question'])for r in records}),'available_counts':counts,'asset_hashes':[],'source_preserved':True})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'available_counts_after':counts,'no_changes':True};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w')as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed']is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source[0][0]);assert CLIENT.status()==status
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'trig-quotient-frequency-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id']for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

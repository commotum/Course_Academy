"""Scoped registration/replenishment through existing EDB integration."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
sp=importlib.util.spec_from_file_location('validate_arc',HERE/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);g=v.g
KP=g.KP_ID;SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));SOURCE=':application/ca-engine';LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'7a46071c958dfdbfbd6e9b6ee918e739a0d61424937f6d99efc3f653c4fda86a'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'
QUERY=(HERE/'reference/source-query.edn').read_text()
USAGE='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return sorted([canonical(v) for v in x],key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def inventory(path):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],env=ENV,input='{"action":"inventory"}',capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']

def read(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def records():return g.batch('easy',126,92375)

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'unavailable',basis)};allrecs={r['question'][':question/id']:r for r in records()};available=[];inputs=[]
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        sid=q.get(':question/math-academy-id')
        if sid in g.CASES:
            assert canonical(q)==canonical(g.CASES[sid]),'Source changed; reclassify'
            a,b=g.CURVES[sid][2:];r=v.independent(g.generate('easy',0,sid,[sid,a,b]))
        elif str(q.get(':question/id')) in allrecs:
            r=allrecs[str(q[':question/id'])];v.independent(r);assert normalize(q)==ordered(r['question'])
        else:continue
        available.append(q);inputs.append(v.native(r))
    save(path/'inventory-grade-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'inventory-grade-input.json'),str(path/'inventory-grade-report.json')],check=True)
    c={'basis':basis,'available':{'easy':len({g.fingerprint(q) for q in available}),'moderate':0,'hard':0},'available_question_ids':[str(q[':question/id']) for q in available],'unavailable':sorted(unavailable),'unrated_and_canonical_excluded':True};save(path/'available-counts.json',c);return c

def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def normalize(q):
    out={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')};out[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);out[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    return ordered(out)

def forms(kp,recs):
    tx=[]
    for r in recs:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:tx.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            tx.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        tx.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen is None:tx += [{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(g.GENERATOR_UUID),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']]
    else:assert str(gen[':question-generator/id'])==g.GENERATOR_UUID and gen[':question-generator/script']==SCRIPT
    if recs:tx.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in recs]})
    if tx:tx.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return tx

def inspect(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values());allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction';name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed

def verify(path,intent,receipt):
    assert receipt[':edb/committed'] is True and receipt[':edb/db-before-t']==intent['basis'];inspect(receipt,path/'receipt-check',intent['source_eid'])
    after=receipt[':edb/db-after-t'];now=read(path/'readback',after);before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};current={q[':db/id']:q for q in now[':knowledge-point/questions']}
    assert all(current[e]==q for e,q in old.items());assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in now.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=now[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    recs=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in current.values()};assert len(current)==len(old)+len(recs)
    for r in recs:assert normalize(byid[r['question'][':question/id']])==ordered(r['question']);v.independent(r)
    assert not forms(now,[])
    c=counts(now,path/'readback',after);verification={'passed':True,'basis_before':intent['basis'],'basis_after':after,'new_questions':len(recs),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'additive_scoped_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c};save(path/'verification.json',verification);return verification

def finish(path,verified,inv):
    after=verified['available_counts_after'];result={'outcome':'generated' if after['available']['easy']>=5 else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':g.GENERATOR_UUID,'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'available_counts':after['available'],'supported_levels':['easy'],'supported_shortage_remaining':{'easy':max(0,5-after['available']['easy'])},'unsupported_levels':['moderate','hard'],'unsupported_nominal_shortage':{'moderate':5,'hard':5},'unsupported_levels_filled':False,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'note':'Classification and validated generator registration completed. No surplus questions added when current easy inventory already meets five. Unsupported bands remain unfilled. Original sources and learner history preserved.','evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'preparation.json',path/'inventory-after.json',HERE/'classification.json',HERE/'template-extraction.md',HERE/'validation.json',HERE/'capabilities.json',HERE/'native-grading.json']]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_counts','unsupported_levels')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass' and validation['hashes'][SCRIPT]==sha(HERE.with_suffix('.py'))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn') and intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest();receipt=DB._commit(intent,path/'transaction.edn',path);finish(path,verify(path,intent,receipt),inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read(path,basis);assert canonical(kp)==canonical(g.SOURCE['record']),'Source changed since classification; reclassify'
        (path/'before.edn').write_text(dumps(kp)+'\n');c=counts(kp,path,basis);needed=max(0,5-c['available']['easy']);used={g.fingerprint(q) for q in kp[':knowledge-point/questions']};recs=[]
        supplied=JOB.with_suffix('.generated');assert not supplied.exists(),'New supplied instances need validation before proceeding'
        for r in records():
            if len(recs)>=needed:break
            fp=g.fingerprint(r['question'])
            if fp not in used:v.independent(r);recs.append(r);used.add(fp)
        save(path/'generated.json',recs)
        if recs:
            save(path/'native-input.json',[v.native(r) for r in recs]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
            ids=[uuid.UUID(z) for r in recs for z in [r['question'][':question/id'],r['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]]
            assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identities',basis),'Existing identity requires reconciliation'
        source=DB.query('[:find ?s :where [?s :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        # Identity check is batched with the lock-held preparation reads.
        registered=DB.query('[:find ?g ?p :in $ ?id :where [?g :question-generator/id ?id] [?g :question-generator/script ?p]]',[uuid.UUID(g.GENERATOR_UUID)],path,'generator-identity',basis);assert not registered,'Unexpected existing generator identity needs reconciliation'
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'new_questions':len(recs),'needed_easy':needed,'generator_sha256':sha(HERE.with_suffix('.py')),'asset_hashes':[],'all_source_records_unchanged':True,'lock_held':True})
        tx=dumps(forms(kp,recs))+'\n';txpath=path/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;inspect(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'arc-integral-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':g.GENERATOR_UUID,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in recs],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);receipt=DB._commit(intent,txpath,path);finish(path,verify(path,intent,receipt),inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

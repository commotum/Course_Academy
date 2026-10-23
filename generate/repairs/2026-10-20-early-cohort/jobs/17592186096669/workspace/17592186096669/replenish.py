"""Scoped additive inventory preparation and locked, guarded durable commit."""
import copy, fcntl, hashlib, importlib.util, json, os, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import kw,dumps,loads
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('backsub_validation',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
from db_support import plain,PATTERN
KP=g.KP;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(H.with_suffix('.py').relative_to(ROOT));LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'175cef7bc6b8cace7b109305fcc1f3f230df0b1034586686341629b27549b9ec'
OUT=H/'reference/replenishment';ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-1275f16a95dc6372';DISCOVERY=ROOT/'.local/generate/find-candidates-7788c5784f60947f'
LEVELS=('easy','moderate','hard')
USAGE='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(path,basis):return DB.query('[:find (pull ?k '+PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],path,'kp',basis)[0][0]
def sorted_data(x):
    if isinstance(x,dict):return {str(k):sorted_data(val) for k,val in x.items()}
    if isinstance(x,list):return sorted([sorted_data(val) for val in x],key=lambda val:json.dumps(val,sort_keys=True))
    return plain(x)
def normalize(q):
    return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':[
      {':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[
      {':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]} for f in q[':question/answer-fields']]}
def assert_sources(kp):
    before=g.SOURCE['record'];now=plain(kp)
    current={q.get(':question/math-academy-id'):q for q in now[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    originals={q[':question/math-academy-id']:q for q in before[':knowledge-point/questions']}
    assert sorted_data(current)==sorted_data(originals),'Source evidence changed; classification must be reopened'
    assert sorted_data(now[':knowledge-point/canonical-example'])==sorted_data(before[':knowledge-point/canonical-example'])
def inventory(path):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input=json.dumps({'action':'inventory'}),text=True,capture_output=True,env=ENV,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def discovery(path):
    r=subprocess.run([str(DISCOVERY)],input=json.dumps({'database':'math','learner':LEARNER,'topics':[17592186050267],'activity_type':'lesson','after_basis':None,'lineage':None,'at':None}),text=True,capture_output=True,env=ENV,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['cursor']['lineage']==LINEAGE;save(path,x)
    rows=[k for t in x['topics'] for k in t['knowledge_points'] if k['db/id']==KP];assert len(rows)==1
    return x['basis'],rows[0]['inventory']
def available(kp,path,basis):
    unavailable={row[0] for row in DB.query(USAGE,[KP,LEARNER],path,'usage',basis)}
    records=[];valid=[];excluded=[]
    known={r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())}
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if q[':db/id'] in unavailable:excluded.append({'id':q[':db/id'],'reason':'shown or reserved'});continue
        if sid in g.PARAMETERS:
            rec=g.generate(profile=sid,scale=1)
            A,B=v.read_system(q[':question/problem']);assert tuple(A.inv()*B)==g.read_vector(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])
            assert str(q[':question/difficulty'][':db/ident'])==':question.difficulty/easy'
            rec['question']=normalize(q)
        elif str(q[':question/id']) in known:
            rec=copy.deepcopy(known[str(q[':question/id'])]);v.check_record(rec);assert sorted_data(normalize(q))==sorted_data(rec['question'])
        else:excluded.append({'id':q[':db/id'],'reason':'incomplete or unrecognized validation provenance'});continue
        records.append(v.native(rec));valid.append((v.rendered_fingerprint(q),q[':db/id']))
    save(path/'native-available-input.json',records)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-available-input.json'),str(path/'native-available-report.json')],check=True)
    grade=json.loads((path/'native-available-report.json').read_text());assert grade['documented_unresolved_checks']==0
    result={'easy':len({fp for fp,_ in valid}),'moderate':0,'hard':0}
    save(path/'validated-available-counts.json',{'basis':basis,'available_by_level':result,'included':[e for _,e in valid],'excluded':excluded,'canonical_excluded':True,'distinctness':'normalized coefficient matrix and RHS, no bank/order/identity/seed'})
    return result

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
    if gen:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    else:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected source or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected changed existing entity or non-content attribute'

def verify(path,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    before=loads((path/'before.edn').read_text());after=read(path/'readback',report[':edb/db-after-t'])
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']}
    assert all(sorted_data(now[e])==sorted_data(q) for e,q in old.items())
    assert sorted_data({k:val for k,val in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==sorted_data({k:val for k,val in after.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
    gen=after[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert sorted_data(normalize(q))==sorted_data(rec['question']);v.check_record(rec)
    assert not transaction([],after,intent['generator_id'])
    verified={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{'easy':len(records),'moderate':0,'hard':0},'source_questions_preserved':len(old),'canonical_example_preserved':True,'learner_history_unchanged':True,'other_kps_unchanged':True,'all_datoms_additive_scoped_content_and_declared_contributor':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',verified);return verified

def finish(path,gid,verified,inv,counts):
    shortage={l:max(0,5-counts[l]) for l in LEVELS}
    result={'outcome':'finite-limit' if shortage['easy'] else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'validated_generator_variants':99,'available_by_level':counts,'shortage_by_level':shortage,'supported_shortage_by_level':{'easy':shortage['easy']},'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
      'capability_exceptions':[{'levels':['moderate','hard'],'reason':'No source evidence at those levels; version 1 supports the observed Easy backbone only. Zero availability remains explicit. New evidence reopens classification.'},{'level':'easy','finite_variant_limit':99,'reason':'Narrow validated homothetic domain: eleven complete source banks times nine positive integer scales. Existing/shown tasks excluded; no seed/order aliases.'}],
      'evidence':[str(p.relative_to(ROOT)) for p in (H/'validation.json',H/'source-bank-replay.json',H/'engine-report.json',H/'classification.md',H/'template-extraction.json',H/'template-extraction.md',H/'review.md',H/'freeze.json',path/'preparation.json',path/'commit-intent.json',path/'preview.edn',path/'transaction.edn',path/'commit.edn',path/'verification.json',path/'inventory-after.json',path/'available-readback/validated-available-counts.json')],
      'note':'Supported Easy inventory rechecked at nine fresh validated questions; no shortage and no redundant question insertion. Registered the validated generator for later replenishment. Generated previews stay local. Source questions and learner history preserved.' if verified['new_questions']==0 else 'Inserted only genuinely distinct validated Easy tasks needed by the locked inventory recheck.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','unsupported_levels')}),flush=True)

def main():
    frozen=json.loads((H/'freeze.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen['files'].items())
    validation=json.loads((H/'validation.json').read_text());assert validation['generator_sha256']==sha(H.with_suffix('.py')) and validation['fidelity']['matched_source_choices']==55 and validation['native_grading']['documented_unresolved_checks']==0
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    OUT.mkdir(parents=True,exist_ok=True)
    print('Acquiring application api.lock for inventory recheck through durable readback',flush=True)
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
                assert sha(path/'transaction.edn')==intent['transaction_sha256'] and (path/'transaction.edn').read_text()==intent['exact_edn']
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                inv=inventory(path/'inventory-after.json');b,_=discovery(path/'discovery-after.json');assert inv['basis']==b
                counts=available(read(path/'available-readback',b),path/'available-readback',b);finish(path,intent['generator_id'],verified,inv,counts);return
        inv=inventory(OUT/'inventory-before.json');b,scheduler_counts=discovery(OUT/'discovery-before.json');assert DB.basis()==inv['basis']==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read(path,b);assert_sources(kp)
        counts=available(kp,path,b);(path/'before.edn').write_text(dumps(kp)+'\n')
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KPID),'question-generator'))
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or gen and registered[0][0][':db/id']==gen[':db/id']
        needed=max(0,5-counts['easy']);records=[];used={v.rendered_fingerprint(q) for q in kp[':knowledge-point/questions']}
        # Canonical equation asset was independently decoded during extraction.
        used.add(hashlib.sha256(json.dumps([1,1,1,'3','2','2']).encode()).hexdigest())
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        for rec in instances:v.check_record(rec)
        candidates=instances+json.loads((H/'previews.json').read_text())
        for rec in candidates:
            if len(records)>=needed:break
            v.check_record(rec);fp=v.rendered_fingerprint(rec['question'])
            if fp not in used:records.append(rec);used.add(fp)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        for attr,ids in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in ids]],path,attr.replace('/','-')+'-collisions',b)
        save(path/'generated.json',records);save(path/'native-input.json',[v.native(r) for r in records+instances])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'available_by_level':counts,'scheduler_inventory':scheduler_counts,'supported_missing':{'easy':needed},'selected_by_level':{'easy':len(records)},'assets':[],'source_evidence_unchanged':True,'finite_unfilled_easy':max(0,needed-len(records)),'unsupported_levels':['moderate','hard'],'stage':'generator_registration_only' if not records else 'additive_generated_content'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'by_level':dict.fromkeys(LEVELS,0)};save(path/'verification.json',{'passed':True,'no_change':True,**verified});finish(path,gid,verified,inv,counts);return
        tx=dumps(forms)+'\n';txpath=path/'transaction.edn'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',contributor[0][0])
        b2,counts2=discovery(path/'discovery-precommit.json');assert DB.basis()==b2==b and counts2==scheduler_counts
        assert available(read(path/'precommit',b),path/'precommit',b)==counts
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'backsub-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
        save(path/'commit-intent.json',intent);print('Submitting exact saved request at locked basis '+str(b),flush=True)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        inv=inventory(path/'inventory-after.json');after,_=discovery(path/'discovery-after.json');assert after==inv['basis']==verified['basis_after']
        counts=available(read(path/'available-readback',after),path/'available-readback',after);finish(path,gid,verified,inv,counts)
if __name__=='__main__':main()

"""Scoped inventory preparation, durable receipt recovery, and additive commit."""
import ast, copy, fcntl, hashlib, importlib.util, json, os, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Reuse the independently authored validator functions without executing its
# report-writing source-replay runner during each replenishment.
tree=ast.parse((HERE/'validate.py').read_text())
v={'ROOT':HERE,'REPO':ROOT,'m':g}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef))],type_ignores=[]),str(HERE/'validate.py'),'exec'),v)
KP=g.KP_ID
LEVELS=('easy','moderate','hard')
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE=g.SOURCE['lineage']
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'de8771bf0ed2a04f12c3e21b4352695d44509d4db5da585b6cc75b2a5fdebad4'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-80371ed6e5f3669c'
QUERY=(HERE/'reference/source-current-query.edn').read_text()

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(x):return json.loads(json.dumps(x,default=str))
def inventory(path):
    p=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
    r=json.loads(p.stdout);assert r['ok'] and r['data']['lineage']==LINEAGE
    save(path,r['data']);return r['data']
def read_kp(path,basis):return DB.query(QUERY,[[KP]],path,'kp',basis)[0][0]
def fingerprint(q):
    a,b,N=v['from_prompt'](q[':question/problem'])
    kind='cardinal' if 'has magnitude' in q[':question/problem'] else 'compass'
    return g.digest({'method':kind,'unordered_magnitudes':sorted([a,b])})
def normalize(q):
    r={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    r[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    r[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        r[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    return ordered(r)
def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

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

def check_datoms(report,path,source):
    attrs={a:str(k) for a,k in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,val,tx,s,added in report[':edb/tx-data']:
        assert added and s==source,'Unexpected retraction or source'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected entity or attribute'

def verify(path,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_datoms(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question']) and fingerprint(q)==rec['generation']['parameter_fingerprint']
        v['check'](rec)
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    qualified=json.loads((path/'qualified-inventory.json').read_text())
    counts={level:qualified['validated_distinct_available'][level]+verified['by_level'][level] for level in LEVELS}
    shortage={level:max(0,5-counts[level]) for level in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'generated_by_level':verified['by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'validated_distinct_available':counts,'remaining_shortage':shortage,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_evidence':str((HERE/'capabilities.json').relative_to(ROOT)),'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',path/'qualified-inventory.json',path/'native-report.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md')],'note':'Original unrated questions and learner history preserved; only authored eligible banks count. Difficulty policies are authored classifications, not recovered source ratings.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','validated_distinct_available','remaining_shortage')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed'
    freeze=json.loads((HERE/'freeze.json').read_text())
    assert all(sha(ROOT/p)==h for p,h in freeze['sha256'].items()),'Frozen package changed'
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        original=json.loads((HERE/'source.json').read_text())['record']
        current={str(q[':question/id']):js(q) for q in kp[':knowledge-point/questions']}
        assert all(current[q[':question/id']]==q for q in original[':knowledge-point/questions']),'Source questions changed: reclassify'
        assert js(kp[':knowledge-point/canonical-example'])==original[':knowledge-point/canonical-example']
        source=DB.query('[:find ?s :where [?s :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.uid('question-generator')
        historical=DB.query('[:find ?q :in $ ?learner ?kp :where [?l :learner/id ?learner] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q _ _ true] [?kp :knowledge-point/questions ?q]]',[LEARNER,KP],path,'historical-presentations',b,history=True)
        presented=DB.query('[:find ?q :in $ ?learner ?kp :where [?l :learner/id ?learner] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q] [?kp :knowledge-point/questions ?q]]',[LEARNER,KP],path,'presentations',b)
        reserved=DB.query('[:find ?q :in $ ?learner ?kp :where [?l :learner/id ?learner] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q] [?kp :knowledge-point/questions ?q]]',[LEARNER,KP],path,'reservations',b)
        unavailable={r[0] for r in historical+presented+reserved}
        complete={l:set() for l in LEVELS};used=set();excluded=[]
        for q in kp[':knowledge-point/questions']:
            fp=fingerprint(q);used.add(fp)
            if ':question/difficulty' not in q or ':question/worked-solution' not in q or any(':answer-field/correct' not in f for f in q[':question/answer-fields']):
                excluded.append({'question':str(q[':question/id']),'reason':'Unrated/incomplete original evidence'});continue
            level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
            if q[':db/id'] not in unavailable:complete[level].add(fp)
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        needed={l:max(0,5-len(complete[l])) for l in LEVELS}
        save(path/'qualified-inventory.json',{'basis':b,'validated_distinct_available':{l:len(complete[l]) for l in LEVELS},'required':needed,'excluded':excluded,'unavailable':sorted(unavailable),'native_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP]})
        records=[];selected={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        def select(rec):
            v['check'](rec);assert rec['knowledge_point']['db_id']==KP and rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question']);assert fp==rec['generation']['parameter_fingerprint']
            if fp not in used and selected[level]<needed[level]:records.append(rec);used.add(fp);selected[level]+=1
        for rec in instances:select(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        for l,kind,lo,hi in [('easy','cardinal',2,30),('moderate','cardinal',2,12),('hard','compass',10,25)]:
            for a in range(lo,hi+1):
                for bb in range(a+1,hi+1):
                    if selected[l]>=needed[l]:break
                    p={'a':a,'b':bb,'orientation':0}
                    try:g.valid(l,kind,p)
                    except ValueError:continue
                    select(g.generate(l,int(JOB.name[:8],16),parameters=p))
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        assert not ids or not DB.query('[:find ?q :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'identity-collisions',b)
        identity=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not identity or (gen and str(identity[0][0][':question-generator/id'])==gid)
        save(path/'generated.json',records)
        checks=[]
        for rec in records+instances:
            correct=v['check'](rec)
            checks.append({'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'All generated bank options through actual learner grader'} for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]})
        save(path/'native-input.json',checks)
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'review.json',records);(path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'required':needed,'selected':selected,'asset_hashes':[],'finite_shortage':{l:needed[l]-selected[l] for l in LEVELS},'distinctness':'Recognition family and unordered magnitude pairs; excludes rotation, swap, seed, identity and bank ordering'})
        forms=transaction(records,kp,gid);assert forms,'Already replenished: retain verified prior receipt'
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        p=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(p.stdout);pr=loads(p.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_datoms(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'unit-vector-sum-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

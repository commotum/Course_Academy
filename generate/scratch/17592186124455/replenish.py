"""Scoped tangent-vector inventory publisher using the application's EDB integration."""
import copy, fcntl, hashlib, importlib.util, json, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.storage import atomic_json,atomic_text
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database,QUESTION_PULL
from edn import dumps,loads,kw
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('tangent_validation',HERE/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID; LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'; LINEAGE=g.SNAP['lineage']
SOURCE=':application/ca-engine'; SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'586bf844f40150fa23d3d953b1b191c235bf2abb4939dfa0927e88dd51196a31'
OUT=ROOT/'reference/generated/17592186124455/job-586bf844'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env.update(database_environment('math'))
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
SHOWN='[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]'
RESERVED='[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?s] (or [?s :db/ident :learner-task.status/started] [?s :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'
save=atomic_json
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(path):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    result=json.loads(r.stdout);assert result['ok'];inv=result['data'];assert inv['lineage']==LINEAGE
    save(path,inv);return inv
def read_kp(path,basis):
    rows=DB.query(QUERY,[KP],path,'kp',basis);assert len(rows)==1
    kp=rows[0][0];assert str(kp[':knowledge-point/id'])==g.KP_UUID;return kp
def fingerprint(q):
    lhs,rhs=q[':question/problem'].split('$')[1].rstrip('.').split('=')
    residual=g.s.expand(g.parse(lhs)-g.parse(rhs));point=re.findall(r'\$\(([^$]*?)\)\.?\$',q[':question/problem'])[-1]
    a,b=map(g.parse,point.split(','));scale=residual.as_ordered_terms()[0].as_coeff_Mul()[0]
    return g.digest([g.s.srepr(g.s.expand(residual/scale)),str(a),str(b)])
def current_audit(q):
    """Audit displayed math and every bank without changing source records."""
    normalized=normalize(q);qid='current:'+q.get(':question/math-academy-id',str(q[':question/id']))
    g.QUESTIONS[qid]=normalized
    rec=g.wrap(normalized,0,qid,{},'current-source',False)
    audit=v.inspect(rec)
    assert rec['generation']['domain']['point_membership_verified']
    return rec,audit
def native_check(records,path):
    checks=[]
    for n,r in enumerate(records):
        cs=[]
        for fi,f in enumerate(r['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:
                cs.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete field-owned bank'})
        checks.append({'label':'tangent-'+str(n),'record':r,'checks':cs})
    path.mkdir(parents=True,exist_ok=True);save(path/'input.json',checks)
    subprocess.run([str(GRADER),str(path/'input.json'),str(path/'report.json')],check=True)
def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(SHOWN,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    unavailable.update(r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis))
    fresh={lv:set() for lv in ('easy','moderate','hard')};recs=[];audits=[];excluded=[]
    for q in kp[':knowledge-point/questions']:
        lv=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if lv not in fresh:continue
        try:rec,audit=current_audit(q)
        except Exception as error:
            excluded.append({'id':str(q[':question/id']),'source':q.get(':question/math-academy-id'),'reason':str(error)[:600]});continue
        recs.append(rec);audits.append({'id':str(q[':question/id']),**audit})
        if q[':db/id'] not in unavailable and not q.get(':knowledge-point/_canonical-example'):fresh[lv].add(fingerprint(q))
    native_check(recs,path/'grading')
    data={'basis':basis,'distinct_available':{lv:len(fs) for lv,fs in fresh.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded_invalid':excluded,'mathematical_audits':audits,'nominal_shortage':{lv:max(0,5-len(fs)) for lv,fs in fresh.items()}}
    save(path/'available-counts.json',data);return data

def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q


def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-audit',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items()),'Existing source record changed'
    assert {k:x for k,x in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:x for k,x in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question'])
        assert fingerprint(q)==fingerprint(rec['question']);v.inspect(rec)
    native_check(records,path/'readback-grading')
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{lv:sum(r['question'][':question/difficulty']==':question.difficulty/'+lv for r in records) for lv in ('easy','moderate','hard')},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result);return result

def finish(path,gid,verified):
    inv=inventory(path/'inventory-after.json');kp=read_kp(path/'final-pool',verified['basis_after'])
    available=counts(kp,path/'final-pool',verified['basis_after'])
    result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'generated_by_level':verified['by_level'],'supported_levels':['easy','moderate','hard'],'unsupported_levels':[],'available_counts':available['distinct_available'],'remaining_shortage':available['nominal_shortage'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_preservation_verified':True,'evidence':[str(p.relative_to(ROOT)) for p in (path/'preparation.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'final-pool/available-counts.json',path/'inventory-after.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',OUT/'current-classification.md')]}
    assert not any(result['remaining_shortage'].values())
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','available_counts','remaining_shortage')}),flush=True)

def prepare_candidates(kp,available,path):
    used={fingerprint(q) for q in kp[':knowledge-point/questions']}
    used.add(fingerprint(kp[':knowledge-point/canonical-example']))
    supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
    if isinstance(instances,dict):instances=[instances]
    assert isinstance(instances,list)
    records=[];need=available['nominal_shortage'].copy()
    for rec in instances:
        assert rec['knowledge_point']['db_id']==KP and rec['generation']['eligible_for_learning']
        v.inspect(rec);lv=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
        if need.get(lv,0)>0 and fp not in used:records.append(rec);used.add(fp);need[lv]-=1
    save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances)})
    for lv in ('easy','moderate','hard'):
        for seed in range(int(JOB.name[:8],16),int(JOB.name[:8],16)+500):
            if need[lv]==0:break
            rec=g.generate(lv,seed);fp=fingerprint(rec['question'])
            if fp in used:continue
            assert g.generate(lv,seed)['question']==rec['question'];v.inspect(rec)
            twin=g.generate(lv,seed+1,parameters=rec['generation']['parameters'])
            assert twin['question'][':question/id']==rec['question'][':question/id']
            records.append(rec);used.add(fp);need[lv]-=1
        assert need[lv]==0,('Bounded generator supply exhausted',lv,need[lv])
    assert len({fingerprint(r['question']) for r in records})==len(records)
    save(path/'generated.json',records);atomic_text(path/'generated.md','\n'.join(g.markdown(r) for r in records))
    native_check(records,path/'prepared-grading');return records

def main():
    global NATIVE,GRADER
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass'
    freeze=json.loads((HERE/'freeze.json').read_text())
    assert sha(HERE.with_suffix('.py'))==freeze['files'][SCRIPT]
    # Reuse the already built current application and compile the existing grader
    # harness against its current release engine, without changing application code.
    from serve_graph_explorer import build_learning
    NATIVE=build_learning(ROOT.parent/'EDB')
    GRADER=ROOT/'.local/edb/capture-runtime/tangent-17592186124455-grader'
    deps=ROOT/'target/release/deps';engine=max(deps.glob('libcourse_academy_engine-*.rlib'),key=lambda p:p.stat().st_mtime_ns);serde=max(deps.glob('libserde_json-*.rlib'),key=lambda p:p.stat().st_mtime_ns)
    subprocess.run(['rustc','--edition=2024','-O',str(ROOT/'generate/runs/current/check-engine.rs'),'--extern','course_academy_engine='+str(engine),'--extern','serde_json='+str(serde),'-L','dependency='+str(deps),'-o',str(GRADER)],check=True)
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    # Reconcile any exact saved submission before creating new intent.
    saved=[p for p in sorted(OUT.glob('basis-*')) if (p/'commit-intent.json').exists()]
    if not saved:
        inv=inventory(OUT/'pre-generation-inventory.json');b=inv['basis'];kp=read_kp(OUT/'pre-generation',b)
        available=counts(kp,OUT/'pre-generation',b)
        records=prepare_candidates(kp,available,OUT/'candidates')
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        if saved:
            assert len(saved)==1;path=saved[0];intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent['generator_id'],verified);return
        inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(parents=True,exist_ok=True)
        kp=read_kp(path,b);atomic_text(path/'before.edn',dumps(kp)+'\n')
        available=counts(kp,path/'current-pool',b);need=available['nominal_shortage'].copy();used={fingerprint(q) for q in kp[':knowledge-point/questions']};selected=[]
        for rec in records:
            lv=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if need[lv]>0 and fp not in used:selected.append(rec);used.add(fp);need[lv]-=1
        assert not any(need.values()),'Inventory changed; return to preparation'
        records=selected;save(path/'generated.json',records)
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+g.KP_UUID))
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or gen and registered[0][0][':db/id']==gen[':db/id']
        # Do not create a second generator identity for an already registered path.
        matching=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-path',b)
        if matching:
            assert len(matching)==1
            gid=str(matching[0][0][':question-generator/id'])
            if gen:assert gen[':db/id']==matching[0][0][':db/id']
        for attr,ids in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in ids]],path,attr.replace('/','-')+'-collisions',b)
        native_check(records,path/'selected-grading')
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'validation_sha256':sha(HERE/'validation.json'),'available_counts':available,'new_questions':len(records),'assets':[],'distinctness':'Implicit residual normalized up to nonzero constant scale plus exact evaluation point; seed, UUID, bank order and bank profile are ignored.','difficulty_evidence':'Moderate observed; easy canonical quadratic workload and hard logarithm/reciprocal workload are bounded authored extensions of the same partial-derivative method.'})
        forms=transaction(records,kp,gid);assert forms
        tx=dumps(forms)+'\n';txpath=path/'transaction.edn';atomic_text(txpath,tx)
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        atomic_text(path/'preview.edn',r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-audit',contributor[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'inventory-tangent-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
        save(path/'commit-intent.json',intent)
        verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,gid,verified)

if __name__=='__main__':main()


"""Scoped scalar-projection inventory publication; immutable retained requests."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP['db_id'];LEVELS=('easy','moderate','hard')
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'95e32fa9b31519a37bd3cb6bbbcd35fe46685d608f4ec887732df7102c8231a4'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'
ENGINE=HERE/'reference/check-engine-current'
QUERY=(HERE/'reference/source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

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

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value
USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''


def parameters(q):
    vector_text=q[':question/problem'].replace(r'\langle','⟨').replace(r'\rangle','⟩')
    vs=re.findall('⟨([^⟩]+)⟩',vector_text);assert len(vs)==2
    a,b=[[str(v.mathparse(x)) for x in part.split(',')] for part in vs]
    prompt=q[':question/problem']
    if 'scalar projection' in prompt:op='single'
    else:
        request=prompt[prompt.index('Find'):]
        assert 'comp' in request
        op='sum' if '+' in request else 'difference'
    return {'a':a,'b':b,'operation':op}

def task(q):return g.mathematical_fingerprint(parameters(q))

def source_projection(now,old):
    """Compare all frozen source facts, allowing extra pull navigation only."""
    if isinstance(old,dict):
        assert isinstance(now,dict)
        return {k:source_projection(now[k],x) for k,x in old.items()}
    if isinstance(old,list):
        assert isinstance(now,(list,tuple)) and len(now)==len(old)
        if old and isinstance(old[0],dict):
            key=next(k for k in (':db/id',':question/id',':answer-field/id',':answer/id') if k in old[0])
            index={str(x[key]):x for x in now}
            return [source_projection(index[str(x[key])],x) for x in old]
        return [source_projection(a,b) for a,b in zip(now,old)]
    return canonical(now)

def source_check(kp):
    old=json.loads((HERE/'source.json').read_text())['record']
    current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    assert set(current)=={q[':question/math-academy-id'] for q in old[':knowledge-point/questions']},'New source evidence requires classification'
    for q in old[':knowledge-point/questions']:
        assert canonical(source_projection(current[q[':question/math-academy-id']],q))==canonical(q),'Source facts changed; reclassify'
    assert canonical(source_projection(kp[':knowledge-point/canonical-example'],old[':knowledge-point/canonical-example']))==canonical(old[':knowledge-point/canonical-example'])

def check_generated(rec):
    assert rec['knowledge_point']==g.KP
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    assert rec['generation']['lineage']==LINEAGE
    q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
    p=parameters(q);assert g.compact_parameters(p)==rec['generation']['parameters']
    assert task(q)==rec['generation']['mathematical_fingerprint']
    g.check_parameters(level,p);v.check(rec)
    f=q[':question/answer-fields'][0]
    replay=g.generate(level,rec['generation']['seed'],template=rec['generation']['template'],field_type=f[':answer-field/type'].split('/')[-1],parameters=p,profile=rec['generation']['bank_profile'])
    assert ordered(q)==ordered(replay['question']),'Generator replay differs'
    assert ':question/math-academy-id' not in q

def stock(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    # Preserve never-shown status even if a presentation was later retracted.
    history=DB.query('''[:find ?q :in $ ?kp ?learner :where
     [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
     [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]''',[KP,LEARNER],path,'retained-presentations',basis,history=True)
    unavailable.update(r[0] for r in history)
    rows={l:[] for l in LEVELS};excluded=[];entries=[]
    cases={r['source_id']:r for r in json.loads((HERE/'source-cases.json').read_text())}
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        if ':question/difficulty' not in q or ':question/worked-solution' not in q:
            excluded.append({'id':str(q[':question/id']),'reason':'unrated or incomplete preserved source'});continue
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        if level not in rows:continue
        mid=q.get(':question/math-academy-id')
        if mid in cases:
            case=cases[mid];rec=g.generate(case['level'],17,case['template'],parameters=case['parameters'],profile=case['bank_profile'])
            assert q[':question/problem']==rec['question'][':question/problem']
            assert q[':question/worked-solution']==rec['question'][':question/worked-solution']
            f=q[':question/answer-fields'][0];rf=rec['question'][':question/answer-fields'][0]
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
            actual=f[':answer-field/correct'][':answer/value'];expected=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert actual==expected
            v.check(rec)
        else:
            rec=g.generate(level,parameters=parameters(q),field_type=str(q[':question/answer-fields'][0][':answer-field/type'][':db/ident']).split('/')[-1])
            assert normalize(q)==ordered(rec['question']),'Unrecognized existing content requires reconciliation'
            check_generated(rec)
        rows[level].append(q);entries.append(v.engine_entry(rec,'available '+str(q[':question/id'])))
    save(path/'stock-native-input.json',entries)
    subprocess.run([str(ENGINE),str(path/'stock-native-input.json'),str(path/'stock-native-report.json')],check=True,capture_output=True,text=True)
    c={'basis':basis,'distinct_available':{l:len({task(q) for q in qs}) for l,qs in rows.items()},'question_ids':{l:[str(q[':question/id']) for q in qs] for l,qs in rows.items()},'excluded_unavailable':sorted(unavailable),'excluded_incomplete':excluded,'canonical_examples_excluded':True}
    save(path/'available-counts.json',c);return c

def choose(kp,needed,path):
    supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances=supplied.get('instances',[]);assert isinstance(instances,list)
    for r in instances:check_generated(r)
    save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
    used={task(q) for q in kp[':knowledge-point/questions']};used.add(task(kp[':knowledge-point/canonical-example']))
    selected=[];added={l:0 for l in LEVELS}
    for rec in instances:
        l=rec['question'][':question/difficulty'].split('/')[-1];fp=task(rec['question'])
        if added[l]<needed[l] and fp not in used:selected.append(rec);used.add(fp);added[l]+=1
    for level in LEVELS:
        for seed in range(1000):
            if added[level]>=needed[level]:break
            rec=g.generate(level,268500+seed);fp=task(rec['question'])
            if fp in used:continue
            check_generated(rec);selected.append(rec);used.add(fp);added[level]+=1
    return selected,added

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items()),'Existing source changed'
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(rec['question']);check_generated(rec)
    assert not transaction([],kp,intent['generator_id'])
    c=stock(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());after=verified['available_counts_after'];remaining={l:max(0,5-after['distinct_available'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'observed_levels':['easy','moderate'],'authored_levels':['hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':after['distinct_available'],'shortage_by_level':remaining,'capability_exceptions':prep['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'generator_sha256':sha(HERE.with_suffix('.py')),'evidence':[str(p.relative_to(ROOT)) for p in (HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'domain-audit.json',HERE/'reference/stock-validation.json',path/'generated.json',path/'preparation.json',path/'commit-intent.json',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'native-report.json',path/'inventory-after.json',path/'supplied-status.json',path/'readback/available-counts.json') if p.exists()],'note':'Reused scalar-projection generator. Hard is the documented same-method authored radical-arithmetic workload. Opaque historical bank profiles are evidence-only for generation; exact valid originals are validated for stock. Unrated incomplete original remains unchanged and excluded. Exact request and additive contributor-attributed receipt verified under api.lock.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed'
    assert all(sha(HERE.with_suffix('.py') if name==HERE.name+'.py' else HERE/name)==digest for name,digest in validation['frozen_sha256'].items() if name!='check-engine')
    assert ENGINE.exists()
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP['id'];source_check(kp)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        matches=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-identity',basis)
        gen=kp.get(':knowledge-point/question-generator');assert len(matches)<=1
        gid=str(gen[':question-generator/id']) if gen else str(matches[0][0][':question-generator/id']) if matches else str(uuid.uuid5(g.NS,'generator'))
        if gen:assert gen[':question-generator/script']==SCRIPT
        c=stock(kp,path,basis);needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS}
        records,added=choose(kp,needed,path)
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]+[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]+[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]
        existing=DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing,'Existing content identities require reconciliation'
        save(path/'generated.json',records)
        save(path/'native-input.json',[v.engine_entry(r,r['question'][':question/id']) for r in records])
        subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        exceptions=[{'difficulty':l,'requested':needed[l],'produced':added[l],'reason':'Bounded 1000 deterministic candidate scan exhausted distinct validated tasks'} for l in LEVELS if added[l]<needed[l]]
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({task(r['question']) for r in records}),'asset_hashes':[],'source_evidence_unchanged':True,'source_basis':1356,'capability_exceptions':exceptions,'lock':str(ROOT/'.local/learning/requests/math/api.lock')})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'scalar-projection-replenish-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

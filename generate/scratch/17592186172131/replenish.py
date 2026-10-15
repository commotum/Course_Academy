"""Requested surface-integral KP replenishment; additive, locked, basis guarded."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid
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
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=17592186172131;LEVELS=['easy','moderate','hard']
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SNAPSHOT['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));GENERATOR_ID=str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'56c740fd2ffdadfad2dfccc8db5a7d7edfa252df9599170bcdea25e440948fe7'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=Path((HERE/'reference/learning-binary.txt').read_text())
QUERY=(HERE/'reference/source-query.edn').read_text()
ENGINE=ROOT/'generate/runs/current/check-engine'
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

def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x, sort_keys=True))
    if isinstance(value, uuid.UUID): return str(value)
    return value

def source_canonical(value):
    """Only literal set-brace escaping changed since frozen capture; retain both."""
    if isinstance(value,str):return value.replace(r'\{', '{').replace(r'\}', '}')
    if isinstance(value,dict):return {k:source_canonical(x) for k,x in canonical(value).items()}
    if isinstance(value,list):return [source_canonical(x) for x in value]
    return value

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


def engine_item(rec):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        cid=f[':answer-field/correct'][1]
        if f[':answer-field/type'].endswith('/radio'):
            checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'all bank selections'} for a in f[':answer-field/choices'])
        else:
            value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
            checks.extend({'field_index':i,'submitted':x,'expected':expect,'purpose':why} for x,expect,why in [(value,'accepted','exact blank'),('('+value+')+0','accepted','equivalent blank'),('('+value+')+1','rejected','incorrect blank')])
    return {'label':rec['question'][':question/id'],'record':rec,'checks':checks}

def native_check(records,path):
    save(path/'native-input.json',[engine_item(r) for r in records])
    subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0

def validate_instance(rec):
    meta=rec['generation'];assert meta['eligible_for_learning'] and not meta['evidence_only']
    level=rec['question'][':question/difficulty'].rsplit('/',1)[1]
    expected=g.generate(level,meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
    assert ordered(rec['question'])==ordered(expected['question']),'Supplied instance differs from stable generator replay'
    v.independent(rec)

def fingerprint_rec(rec):
    meta=rec['generation'];p=meta['parameters'];t=meta['template'];level=rec['question'][':question/difficulty'].rsplit('/',1)[1]
    if t=='canonical_hint':
        a,b,c,A,B=[p[k] for k in ('a','b','c','U','V')]
        R=[a*g.u+b*g.v,a*g.u-b*g.v,c*g.v];F=g.x-g.y;bounds=[0,A,0,B]
    else:
        m=g.mathematics(t,p);R=m['R'];F=m['F'];bounds=m['bounds']
    # Mathematical objects and domain, independent of seed, IDs, bank and choice order.
    return hashlib.sha256(json.dumps({'R':list(map(str,R)),'F':str(F),'bounds':list(map(str,bounds)),'metric_supplied':level!='hard'},sort_keys=True).encode()).hexdigest()

USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def counts(kp,path,basis):
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
    assert not DB.query('[:find ?i :in $ [?i ...] :where [?a :db/ident ?i] [?a :db/noHistory true]]',[[kw(x) for x in ['task-item/content','learner-task/items','learner/activity']]],path,'retention',basis)
    saved={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    available={l:set() for l in LEVELS};used=set();excluded=[];validated=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id');qid=str(q[':question/id'])
        if sid in g.DATA:
            rec=g.generate(g.LEVEL[sid],template=sid,parameters=g.ORIGINAL[sid],profile='observed')
        else:
            assert qid in saved,'Unknown generated question needs reconciliation: '+qid
            rec=saved[qid];assert normalize(q)==ordered(rec['question'])
        fp=fingerprint_rec(rec);used.add(fp)
        if q[':db/id'] in shown|reserved:
            excluded.append({'question':qid,'reason':'Previously presented or reserved'});continue
        if q.get(':knowledge-point/_canonical-example'):
            excluded.append({'question':qid,'reason':'Canonical example'});continue
        if sid in ('q-160834','q-161127','q-167649'):
            excluded.append({'question':qid,'source_id':sid,'reason':'Documented source primitive variable error, ungrouped negative squares, or inherited shell context; source preserved'});continue
        if sid:
            assert source_canonical(normalize(q))==source_canonical(ordered({**rec['question'],':question/id':qid,':question/answer-fields':normalize(q)[':question/answer-fields']})),'Source prompt, solution or difficulty changed'
            rec=copy.deepcopy(rec);rec['question']=normalize(q)
        v.independent(rec)
        level=rec['question'][':question/difficulty'].rsplit('/',1)[1]
        available[level].add(fp);validated.append(rec)
    # The canonical task itself never becomes fresh practice by removing its example ID.
    used.add(fingerprint_rec(g.generate_easy(parameters={'a':1,'b':1,'c':1,'U':3,'V':3})))
    native_check(validated,path/'available-grading')
    result={'basis':basis,'distinct_available':{l:len(x) for l,x in available.items()},'shown_or_reserved':sorted(shown|reserved),'excluded':excluded}
    save(path/'available-counts.json',result)
    return result,used

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items()),'Existing source or generated content changed'
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question']);validate_instance(rec)
    assert not transaction([],kp,intent['generator_id'])
    after,_=counts(kp,path/'readback',report[':edb/db-after-t'])
    assert all(after['distinct_available'][l]>=5 for l in LEVELS)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'available_counts_after':after,'unchanged_existing_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result);return result

def finish(path,intent,verification):
    inv=inventory(path/'inventory-after.json')
    result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verification['basis_after'],'new_questions':verification['new_questions'],'supported_levels':LEVELS,'capability_exceptions':[],'shortage_remaining':{l:0 for l in LEVELS},'unsupported_levels_filled':False,'available_counts_after':verification['available_counts_after'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',HERE/'validation.json',HERE/'source-fidelity.json']]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
    assert json.loads((HERE/'validation.json').read_text())['status']=='pass'
    assert all(sha(ROOT/name)==digest for name,digest in json.loads((HERE/'reference/frozen-hashes.json').read_text()).items())
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent,verify(path,intent,report));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=g.KP;expected={q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']};current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        assert set(expected)<=set(current)
        for sid,q in expected.items():assert source_canonical(current[sid])==source_canonical(q),'Source evidence changed beyond set-brace escaping: '+sid
        assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else GENERATOR_ID
        if gen:assert gen[':question-generator/script']==SCRIPT
        available,used=counts(kp,path,basis);needed={l:max(0,5-available['distinct_available'][l]) for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for r in instances:validate_instance(r)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        records=[];added={l:0 for l in LEVELS};attempts={l:0 for l in LEVELS}
        for r in instances:
            level=r['question'][':question/difficulty'].rsplit('/',1)[1];fp=fingerprint_rec(r)
            if added[level]<needed[level] and fp not in used:records.append(r);used.add(fp);added[level]+=1
        for level in LEVELS:
            for seed in range(int(JOB.name[:8],16),int(JOB.name[:8],16)+500):
                if added[level]>=needed[level]:break
                attempts[level]+=1;r=g.generate(level,seed);validate_instance(r);fp=fingerprint_rec(r)
                if fp in used:continue
                records.append(r);used.add(fp);added[level]+=1
            assert added[level]==needed[level],'Bounded search failed; shortage remains explicit'
        save(path/'generated.json',records);native_check(records,path)
        for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if values:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(x) for x in values]],path/'identities',attr.replace('/','-'),basis)
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'new_by_level':added,'attempts':attempts,'available_counts':available,'source_evidence_unchanged':True,'asset_hashes':[],'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(HERE/'validate.py'),'source_sha256':sha(HERE/'source.json'),'distinct_generated_mathematical_tasks':len({fingerprint_rec(r) for r in records}),'capability_exceptions':[]})
        tx=dumps(transaction(records,kp,gid))+'\n';txpath=path/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        pr=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(pr.stdout);preview_report=loads(pr.stdout)
        assert preview_report[':edb/committed'] is False and preview_report[':edb/db-before-t']==basis
        check_report(preview_report,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'surface-integral-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);finish(path,intent,verify(path,intent,report))

if __name__=='__main__':main()

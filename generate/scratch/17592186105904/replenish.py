"""Scoped triangle-area replenishment via the configured EDB integration."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('triangle_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;KP_UUID=g.KP_UUID;LEVELS=('easy','moderate','hard')
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.CAP['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'a127d0ea66f9c5653c10dae8ef7e9ae65108be9c8ab39ffbd987240b33a20579'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
NATIVE=Path((HERE/'reference/native-path.txt').read_text().strip())
QUERY=(HERE/'reference/initial/source-query.edn').read_text()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]

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

def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
    if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def source_equivalent(current, captured):
    # Source facts are immutable evidence; compare captured keys recursively,
    # allowing only extra fields already installed by unrelated source imports.
    if isinstance(captured,dict):
        return all(k in current and source_equivalent(current[k],value) for k,value in captured.items())
    if isinstance(captured,list):
        if not isinstance(current,list) or len(current)!=len(captured):return False
        if captured and isinstance(captured[0],dict):
            key=':db/id' if ':db/id' in captured[0] else ':answer/id'
            now={str(x[key]):x for x in current}
            return all(str(x[key]) in now and source_equivalent(now[str(x[key])],x) for x in captured)
        return canonical(current)==canonical(captured)
    return str(current)==str(captured)

def build_grader():
    # Link the unchanged generic harness to the current application grading code.
    deps=ROOT/'target/release/deps'
    libraries={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns)
               for name in ('course_academy_engine','serde_json')}
    output=HERE/'reference/check-engine-current'
    cmd=['rustc','--edition=2024','-O',str(ROOT/'generate/runs/current/check-engine.rs')]
    for name,p in libraries.items():cmd.extend(['--extern',name+'='+str(p)])
    cmd.extend(['-L','dependency='+str(deps),'-o',str(output)])
    subprocess.run(cmd,check=True,capture_output=True,text=True)
    save(HERE/'reference/grader-build.json',{'source':'generate/runs/current/check-engine.rs',
        'source_sha256':sha(ROOT/'generate/runs/current/check-engine.rs'),
        'libraries':{name:{'path':str(p),'sha256':sha(p)} for name,p in libraries.items()}})

USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''
def task(meta):
    p=meta['parameters'];return g.digest({'kind':g.TEMPLATES[meta['template']][1],'b':str(g.exact(p['b'])),'c':str(g.exact(p['c'])),'theta':p['theta']})
def source_record(q):
    sid=q[':question/math-academy-id'];r=g.generate_moderate(template=sid,profile='raw_'+sid)
    r['question']=normalize(q);return r

def grade(records,path):
    path.mkdir(parents=True,exist_ok=True)
    items=[]
    for r in records:
        # Derive expected scalar from independently parsed rendered mathematics.
        items.append(v.engine(r,r['question'][':question/id']))
    save(path/'native-input.json',items)
    subprocess.run([str(HERE/'reference/check-engine-current'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,timeout=55)
    report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0

def saved_records():
    return {r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())}

def counts(kp,path,basis):
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
    available={l:set() for l in LEVELS};valid=[];excluded=[];saved=saved_records()
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id');level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if sid in ('q-43310','q-43343','q-280282'):
            excluded.append({'id':q[':db/id'],'source':sid,'reason':'unrated and missing correct ref/solution' if sid!='q-280282' else 'false whole-triangle acute claim; source preserved'});continue
        if level not in LEVELS or not q.get(':question/worked-solution'):
            excluded.append({'id':q[':db/id'],'reason':'unrated or incomplete'});continue
        if sid in g.SOURCES:r=source_record(q)
        else:
            assert str(q[':question/id']) in saved,'Unrecognized generated question needs reconciliation'
            r=saved[str(q[':question/id'])]
            prepared=publish([r],path/'inventory-assets')[0]
            assert normalize(q)==ordered(prepared['question'])
        v.verify(r);valid.append(r)
        if q[':db/id'] not in shown|reserved:available[level].add(task(r['generation']))
    if valid:grade(valid,path/'inventory-grading')
    result={'basis':basis,'distinct_available':{l:len(s) for l,s in available.items()},'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'validated_ids':[r['question'][':question/id'] for r in valid],'excluded':excluded}
    save(path/'available-counts.json',result);return result

def publish(records,path):
    path.mkdir(parents=True,exist_ok=True);lib=ImageLibrary(Path('/media/jake/SSD/EDB/math'),HERE);result=copy.deepcopy(records)
    for r in result:
        for key in (':question/problem',':question/worked-solution'):
            def replace(m):
                local=Path(m[1]);assert local.is_absolute() and local.is_relative_to(HERE)
                data=local.read_bytes();relative=lib.store(data,str(local));assert sha(Path('/media/jake/SSD/EDB/math')/relative)==hashlib.sha256(data).hexdigest()
                return '![]('+relative+')'
            r['question'][key]=re.sub(r'!\[\]\(([^)]+)\)',replace,r['question'][key])
    save(path/'asset-manifest.json',lib.saved);return result

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid']);b=report[':edb/db-after-t'];kp=read_kp(path/'readback',b)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items())
    strip=lambda k:{a:z for a,z in k.items() if a not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    assert canonical(strip(before))==canonical(strip(kp))
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    raw=json.loads((path/'generated.json').read_text());durable=json.loads((path/'durable-records.json').read_text());assert len(now)==len(old)+len(raw)
    byid={str(q[':question/id']):q for q in now.values()}
    for local,prepared in zip(raw,durable):
        v.verify(local);q=byid[prepared['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(prepared['question'])
    assert publish(raw,path/'readback-assets')==durable
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(raw),'by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in raw) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    stock=counts(read_kp(path/'current-inventory',inv['basis']),path/'current-inventory',inv['basis'])
    remaining={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS};prep=json.loads((path/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified.get('basis_after'),'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'observed_levels':['moderate'],'authored_levels':['easy','hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':stock['distinct_available'],'shortage_by_level':remaining,'capability_exceptions':prep['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'freeze.json',HERE/'registration.json',path/'generated.json',path/'preparation.json',path/'assets/asset-manifest.json',path/'transaction.edn',path/'commit-intent.json',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'native-report.json',path/'inventory-after.json',path/'current-inventory/available-counts.json'] if p.exists()],'note':'Existing validated package executed. Source omissions and prose error preserved and excluded. Mathematical task keys omit seeds, unit labels, bank/choice order, template layout and difficulty. Exact request/receipt/readback retained under application lock.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','remaining_jobs')}),flush=True)

def main():
    assert json.loads((HERE/'validation.json').read_text())['passed']
    build_grader()
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    if '--inspect' in sys.argv:
        inv=inventory(OUT/'inventory-inspect.json');p=OUT/'inspect';kp=read_kp(p,inv['basis']);stock=counts(kp,p,inv['basis']);print(json.dumps(stock));return
    print('Waiting for application api.lock',flush=True)
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);print('Acquired application api.lock',flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if (p/'commit-intent.json').exists():
                intent=json.loads((p/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
                assert intent['exact_edn']==(p/'transaction.edn').read_text() and intent['sha256']==sha(p/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                assert LINEAGE in DB.command('status')
                save(p/'submission-basis-recheck.json',{'current_basis':DB.basis(),'expected_basis':intent['basis'],'application_lock_held':True})
                report=DB._commit(intent,p/'transaction.edn',p);verified=verify(p,intent,report);finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
        p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read_kp(p,b);assert str(kp[':knowledge-point/id'])==KP_UUID
        current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(source_equivalent(current[q[':db/id']],q) for q in g.REC[':knowledge-point/questions'])
        (p/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(source)==1
        reg=kp.get(':knowledge-point/question-generator');gid=str(reg[':question-generator/id']) if reg else str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
        if reg:assert reg[':question-generator/script']==SCRIPT
        stock=counts(kp,p,b);needed={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
        used={task(g.generate_moderate(template=sid,profile='raw_'+sid)['generation']) for sid in g.SOURCES}
        used.add(g.digest({'kind':'side','b':'8','c':'12','theta':45})) # canonical AB=8, AC=12, same side-isolation task
        used.update(task(r['generation']) for r in saved_records().values())
        records=[];selected={l:0 for l in LEVELS};attempts={l:0 for l in LEVELS}
        def select(r):
            v.verify(r);m=r['generation'];l=r['question'][':question/difficulty'].split('/')[-1]
            assert m['eligible_for_learning'] and not m['evidence_only'] and r['knowledge_point']['db_id']==KP
            replay=g.generate(l,m['seed'],m['template'],parameters=m['parameters'],profile=m['profile']);assert ordered(r['question'])==ordered(replay['question'])
            fp=task(m)
            if selected[l]<needed[l] and fp not in used:records.append(r);used.add(fp);selected[l]+=1
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied if isinstance(supplied,list) else supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        for r in instances:select(r)
        for l in LEVELS:
            for i in range(100):
                if selected[l]>=needed[l]:break
                attempts[l]+=1;select(g.generate(l,seed=2026101505904+i))
        exceptions=[{'level':l,'type':'bounded-sampling-limit','attempt_budget':100,'missing':needed[l]-selected[l],'filled':False} for l in LEVELS if selected[l]<needed[l]]
        for attr,label,ids in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],p,'identity-'+label,b)
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],p,'generator-identity',b)
        assert not registered or reg and registered[0][0][':db/id']==reg[':db/id']
        save(p/'generated.json',records)
        if records:grade(records,p)
        durable=publish(records,p/'assets');save(p/'durable-records.json',durable)
        (p/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'generator_id':gid,'generator_path':SCRIPT,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'available_before':stock,'needed':needed,'selected':selected,'attempts':attempts,'new_questions':len(records),'distinct_mathematical_tasks':len({task(r['generation']) for r in records}),'capability_exceptions':exceptions,'supplied_generated_exists':supplied_path.exists(),'supplied_instances_validated':len(instances),'source_evidence_unchanged':True})
        save(HERE/'registration.json',{'generator_id':gid,'generator_path':SCRIPT,'version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'classification_source_basis':g.CAP['basis'],'rechecked_basis':b})
        save(HERE/'freeze.json',{'version':g.VERSION,'source_basis':g.CAP['basis'],'rechecked_basis':b,'sha256':{str(f.relative_to(ROOT)):sha(f) for f in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md']}})
        forms=transaction(durable,kp,gid)
        if not forms:
            verified={'passed':True,'new_questions':0,'by_level':selected,'basis_after':None,'no_change_basis':b};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
        txpath=p/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        prun=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (p/'preview.edn').write_text(prun.stdout);pr=loads(prun.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'inverse-triangle-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(p/'commit-intent.json',intent)
        if '--prepare-only' in sys.argv:print('Prepared',p,flush=True);return
        report=DB._commit(intent,txpath,p);verified=verify(p,intent,report);finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()

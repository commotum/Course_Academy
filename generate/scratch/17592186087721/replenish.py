"""Scoped parametric-graph inventory preparation and serialized additive commit."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
spec = importlib.util.spec_from_file_location('parametric_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'3db49852e3207791b094ebff49164d0bc6a94a43a71b77e52139e1e6ec64d1bf'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env = ENV
QUERY = (OUT/'source-query.edn').read_text()
USAGE = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def canonical(x):
    if isinstance(x, dict): return {str(k):canonical(z) for k,z in x.items()}
    if isinstance(x, (list,tuple)): return sorted([canonical(z) for z in x], key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x, uuid.UUID) else x

def read(path, b): return DB.query(QUERY, [[KP]], path, 'kp', b)[0][0]

def inventory(path):
    r = subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint], input='{"action":"inventory"}', env=ENV, text=True, capture_output=True, check=True, timeout=55)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage']==LINEAGE
    save(path, x['data']); return x['data']

def ordered(q):
    q=copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']: f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def normalize(q):
    result={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    result[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields']=[{':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':[{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]} for f in q[':question/answer-fields']]
    return ordered(result)

def localize(q):
    q=copy.deepcopy(q)
    q[':question/worked-solution']=re.sub(r'!\[\]\((images/[^)]+)\)',lambda m:'![]('+str(g.ASSET_ROOT/m[1])+')',q[':question/worked-solution'])
    for f in q[':question/answer-fields']:
        for a in f[':answer-field/choices']:
            if a[':answer/type']==':answer.type/image' and a[':answer/value'].startswith('images/'):
                a[':answer/value']=str(g.ASSET_ROOT/a[':answer/value'])
    return q

def grade(records, path):
    path.mkdir(parents=True,exist_ok=True)
    cases=[]
    for r in records:
        f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
        cases.append({'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'complete mathematically validated graph bank'} for a in f[':answer-field/choices']]})
    save(path/'input.json',cases)
    subprocess.run([str(HERE/'reference/native/check-engine'),str(path/'input.json'),str(path/'report.json')],check=True,timeout=55)
    report=json.loads((path/'report.json').read_text()); assert report['documented_unresolved_checks']==0

def counts(kp,path,b):
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',b,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',b)}
    known={r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())}
    published={r['question'][':question/id']:r for p in OUT.glob('basis-*/generated-published.json') for r in json.loads(p.read_text())}
    available={l:set() for l in LEVELS}; allfp=set(); records=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if sid in g.SPECS:
            r=g.generate('easy',template=sid,parameters={'m':1,'n':1,'h':0,'k':0},profile='observed:'+sid)
            r['question']=localize(normalize(q))
        else:
            r=copy.deepcopy(known[str(q[':question/id'])])
            assert normalize(q)==ordered(published[str(q[':question/id'])]['question'])
        v.assess(r);records.append(r)
        fp=r['generation']['mathematical_fingerprint']; allfp.add(fp)
        level=r['question'][':question/difficulty'].split('/')[-1]
        if q[':db/id'] not in shown|reserved: available[level].add(fp)
    if records: grade(records,path/'grading')
    result={'basis':b,'distinct_available':{l:len(s) for l,s in available.items()},'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'validated_practice_questions':len(records),'mathematical_fingerprints':sorted(allfp)}
    save(path/'available-counts.json',result);return result

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
    if gen: assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    else: forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records: forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms: forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,path,source):
    attrs=dict(DB.attributes(path,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        name=str(attrs[a]);assert s==source and added,'Unexpected attribution/retraction'
        if e==KP: assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant': assert e in new and name in allowed,name

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items())
    assert canonical(before[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
    records=json.loads((path/'generated-published.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(r['question'])
    assert not transaction([],kp,intent['generator_id'])
    stock=counts(kp,path/'verified-inventory',report[':edb/db-after-t'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'distinct_available_after':stock['distinct_available']}
    save(path/'verification.json',result);return result

def finish(path,gid,verified):
    inv=inventory(path/'inventory-after.json');stock=counts(read(path/'current',inv['basis']),path/'current',inv['basis'])
    shortage={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified.get('basis_after'),'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'observed_levels':['easy'],'authored_levels':['moderate','hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':stock['distinct_available'],'shortage_by_level':shortage,'capability_exceptions':json.loads((path/'preparation.json').read_text())['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'capabilities.json',HERE/'freeze.json',path/'generated.json',path/'generated-published.json',path/'preparation.json',path/'asset-publication.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'current/available-counts.json',path/'inventory-after.json')],'note':'Reused the existing validated graph generator. Moderate/hard are documented authored graph-recognition levels, not observed source labels. Opaque source distractors remain unchanged and replay-only. Complete loci and domains deduplicate questions across identities, seeds and banks. Original practice, canonical example and learner history preserved.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2))

def main():
    global NATIVE
    assert json.loads((HERE/'validation.json').read_text())['status']=='pass'
    NATIVE=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=g.ASSET_ROOT,repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application lock acquired',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified);return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis']
        assert DB.basis()==b and LINEAGE in DB.command('status')
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read(path,b)
        original=g.SOURCE['record'];current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        for q in original[':knowledge-point/questions']: assert canonical(current[q[':db/id']])==canonical(q),'Source evidence changed'
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(original[':knowledge-point/canonical-example'])
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        reg=kp.get(':knowledge-point/question-generator');gid=str(reg[':question-generator/id']) if reg else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        if reg: assert reg[':question-generator/script']==SCRIPT
        stock=counts(kp,path/'stock',b);needed={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
        print('Current distinct availability',stock['distinct_available'],'needed',needed,flush=True)
        used=set(stock['mathematical_fingerprints']);records=[];selected={l:0 for l in LEVELS};attempts={l:0 for l in LEVELS}
        def select(r):
            v.assess(r);meta=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
            assert r['knowledge_point']['db_id']==KP and not meta['bank_profile'].startswith('observed:')
            replay=g.generate(level,meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
            assert ordered(r['question'])==ordered(replay['question']) and meta['mathematical_fingerprint']==replay['generation']['mathematical_fingerprint']
            fp=meta['mathematical_fingerprint']
            if fp not in used and selected[level]<needed[level]: records.append(r);used.add(fp);selected[level]+=1
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        if isinstance(instances,dict): instances=[instances]
        for r in instances: select(r)
        for level in LEVELS:
            for i in range(40):
                if selected[level]>=needed[level]:break
                attempts[level]+=1;select(g.generate(level,2026101487721+i))
        exceptions=[{'level':l,'type':'bounded-sampling-limit','attempt_budget':40,'missing':needed[l]-selected[l],'filled':False} for l in LEVELS if selected[l]<needed[l]]
        save(path/'generated.json',records)
        if records: grade(records,path/'selected-grading')
        library=ImageLibrary(g.ASSET_ROOT,path);published=copy.deepcopy(records)
        for r in published:
            q=r['question'];q[':question/worked-solution']=library.text(q[':question/worked-solution'])
            for f in q[':question/answer-fields']:
                for a in f[':answer-field/choices']: a[':answer/value']=library.resolve(a[':answer/value'])
        save(path/'asset-publication.json',library.saved)
        for entry in library.saved.values(): assert sha(g.ASSET_ROOT/entry['path'])==entry['sha256']
        save(path/'generated-published.json',published)
        if published: grade(published,path/'published-grading')
        for attr,label,ids in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if ids: assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],path,'identity-'+label,b),'Identity requires reconciliation'
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'generator_id':gid,'generator_path':SCRIPT,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'available_before':stock['distinct_available'],'needed':needed,'selected':selected,'new_questions':len(records),'distinct_loci':len({r['generation']['mathematical_fingerprint'] for r in records}),'attempts':attempts,'capability_exceptions':exceptions,'supplied_generated_exists':supplied_path.exists(),'supplied_instances_validated':len(instances),'source_evidence_unchanged':True})
        save(HERE/'freeze.json',{'generator_id':gid,'generator_path':SCRIPT,'version':g.VERSION,'source_basis':g.SOURCE['basis'],'rechecked_basis':b,'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'render.py',HERE/'templates.json',HERE/'source-cases.json',HERE/'validation.json',HERE/'capabilities.json']}})
        forms=transaction(published,kp,gid)
        if not forms:
            verified={'new_questions':0,'by_level':selected,'basis_after':None};save(path/'verification.json',verified);finish(path,gid,verified);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f: f.write(tx);f.flush();os.fsync(f.fileno())
        pr=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,text=True,capture_output=True,check=True,timeout=55)
        (path/'preview.edn').write_text(pr.stdout);report=loads(pr.stdout)
        assert report[':edb/committed'] is False and report[':edb/db-before-t']==b
        check_report(report,path/'preview-check',source[0][0]);assert DB.basis()==b
        if '--commit' not in sys.argv: print('Prepared and previewed at basis',b,'without submission',flush=True);return
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'parametric-graph-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified)

if __name__=='__main__': main()

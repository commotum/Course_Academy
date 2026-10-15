"""Additive dependent-line inventory, guarded by application lock and EDB basis."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.storage import atomic_json as save, atomic_text
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment
from database import Database
from edn import dumps, loads, kw
from capture.scripts.storage import atomic_json as save, atomic_text
from capture.scripts.database.preview import preview_executable
spec=importlib.util.spec_from_file_location('line_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID; LEVELS=g.LEVELS; LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE=g.SOURCE['lineage']; SOURCE=':application/ca-engine'; SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
OUT=HERE/'reference/replenishment'; LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'61879575e632c90fe5ccec930beb4ea063a8d9407e694520a01e8fdd72a7e60e'
ENV=database_environment('math'); DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT'])); DB.env=ENV
NATIVE=Path(json.loads((HERE/'native-runtime.json').read_text())['binary']); ENGINE=HERE/'check-engine'
QUERY=(OUT/'kp-query.edn').read_text()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(o):
    if isinstance(o,dict):return {str(k):canonical(v) for k,v in o.items()}
    if isinstance(o,(tuple,list,set)):return sorted((canonical(z) for z in o),key=lambda z:json.dumps(z,sort_keys=True))
    if isinstance(o,uuid.UUID):return str(o)
    return o

def inventory(path):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,text=True,capture_output=True,check=True,timeout=55)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read_kp(path,b):return DB.query(QUERY,[[KP]],path,'kp',b)[0][0]
def fingerprint(q):
    equations=re.findall(r'\$([^$]*=[^$]*)\$',q[':question/problem'])[:2];assert len(equations)==2
    a,b,c=v.coeff(v.eq(equations[0]));d,e,f=v.coeff(v.eq(equations[1]));assert all((a,b,c)) and a*e==b*d and a*f==c*d
    return tuple(str(z/a) for z in (a,b,c))
def ordered(q):
    q=copy.deepcopy(q)
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def validate(rec):
    v.check(rec);m=rec['generation'];assert not m['raw_evidence'] and m['bank_profile']=='method'
    replay=g.generate(m['authored_level'],m['seed'],template=m['template'],parameters=m['parameters'],profile=m['bank_profile'])
    assert ordered(replay['question'])==ordered(rec['question']) and replay['generation']==m
    return fingerprint(rec['question'])
def grade(records,path):
    if not records:return
    save(path/'native-input.json',[v.native(r,str(i)) for i,r in enumerate(records)])
    subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True,timeout=55)
    report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0

def counts(kp,b,path):
    path.mkdir(parents=True,exist_ok=True)
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],path,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],path,'reserved',b)
    unavailable={r[0] for r in shown+reserved};used={fingerprint(kp[':knowledge-point/canonical-example'])};available={l:set() for l in LEVELS};gradable=[];excluded=[]
    saved={r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())}
    for q in kp[':knowledge-point/questions']:
        fp=fingerprint(q);used.add(fp);level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if level not in LEVELS:
            excluded.append({'id':q[':db/id'],'source':q.get(':question/math-academy-id'),'reason':'Unrated incomplete source; preserved'});continue
        rec=copy.deepcopy(saved[str(q[':question/id'])]);assert ordered(rec['question'])==normalize(q);validate(rec);gradable.append(rec)
        if q[':db/id'] not in unavailable:available[level].add(fp)
    grade(gradable,path)
    x={'basis':b,'available_by_level':{l:len(z) for l,z in available.items()},'excluded':excluded,'ever_shown':[r[0] for r in shown],'reserved':[r[0] for r in reserved]};save(path/'available-counts.json',x);return x,used

def check_report(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution/retraction';name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected unscoped datom'

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];b=report[':edb/db-after-t']
    check_report(report,path/'receipt-check',intent['source_eid']);kp=read_kp(path/'readback',b);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items())
    excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert canonical({k:z for k,z in kp.items() if k not in excluded})==canonical({k:z for k,z in before.items() if k not in excluded})
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
    assert not transaction([],kp,intent['generator_id'])
    stock,_=counts(kp,b,path/'readback/inventory')
    x={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'by_level':{l:sum(r['generation']['authored_level']==l for r in records) for l in LEVELS},'available_by_level':stock['available_by_level'],'unchanged_source_questions':len(old),'canonical_unchanged':True,'learner_history_unchanged':True,'attribution_verified':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0};save(path/'verification.json',x);return x

def finish(path,gid,verified):
    inv=inventory(path/'inventory-after.json');kp=read_kp(path/'final-counts',inv['basis']);stock,_=counts(kp,inv['basis'],path/'final-counts');missing={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
    exceptions=json.loads((path/'preparation.json').read_text())['capability_exceptions']
    assert not any(missing.values()) or exceptions
    result={'outcome':'finite-limit' if any(missing.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'verified_commit_basis':verified['basis_after'],'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'available_by_level':stock['available_by_level'],'shortage_by_level':missing,'supported_levels':list(LEVELS),'authored_difficulty_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'capability_exceptions':exceptions,'finite_mathematical_domain':json.loads((HERE/'validation.json').read_text())['finite_base_domain_distinct_lines'],'lineage':LINEAGE,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'native-build.json',HERE/'freeze.json',OUT/'rendering-validation.json',OUT/'hard-render.png']+list(path.glob('*')) if p.is_file()],'note':'Unrated sources and canonical preserved. Distinct primitive real lines exclude row scaling, seed, aliases, field layout and choice order. api.lock held through current inventory, guarded commit and exact-basis readback.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    save(HERE/'freeze.json',{'generator_id':gid,'script':SCRIPT,'version':g.VERSION,'sha256':sha(HERE.with_suffix('.py')),'supported_levels':list(LEVELS),'verified_commit_basis':verified['basis_after'],'validation_sha256':sha(HERE/'validation.json'),'finite_domain':result['finite_mathematical_domain']})
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level','remaining_jobs')}),flush=True)

def main():
    assert json.loads((HERE/'validation.json').read_text())['passed']
    preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
            assert intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent['generator_id'],verified);return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);atomic_text(path/'before.edn',dumps(kp)+'\n');assert str(kp[':knowledge-point/id'])==g.KP_UUID
        # The raw frozen sources are unchanged; the wider live pull adds optional attributes only.
        frozen=json.loads((HERE/'source.json').read_text())['record'];current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        def captured_shape(live,old):
            if isinstance(old,dict):return {k:captured_shape(live[k],z) for k,z in old.items()}
            if isinstance(old,list):
                byid={z.get(':db/id',str(z.get(':answer/id'))):z for z in live};return [captured_shape(byid[z.get(':db/id',str(z.get(':answer/id')))],z) for z in old]
            return str(live) if isinstance(live,uuid.UUID) else live
        for q in frozen[':knowledge-point/questions']:assert captured_shape(current[q[':db/id']],q)==q
        assert captured_shape(kp[':knowledge-point/canonical-example'],frozen[':knowledge-point/canonical-example'])==frozen[':knowledge-point/canonical-example']
        stock,used=counts(kp,b,path/'current-inventory');needed={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        gen=kp.get(':knowledge-point/question-generator');byscript=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-script',b);assert len(byscript)<=1
        gid=str(gen[':question-generator/id']) if gen else str(byscript[0][1]) if byscript else g.GENERATOR_UUID
        if gen:assert gen[':question-generator/script']==SCRIPT
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or registered[0][0][':question-generator/script']==SCRIPT
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        if isinstance(instances,dict):instances=[instances]
        valid=[];invalid=[]
        for i,r in enumerate(instances):
            try:validate(r);valid.append(r)
            except (AssertionError,ValueError,KeyError,TypeError) as error:invalid.append({'index':i,'reason':repr(error)})
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated':len(valid),'invalid':invalid});records=[];selected={l:0 for l in LEVELS};attempts={l:0 for l in LEVELS}
        def select(r):
            fp=validate(r);l=r['generation']['authored_level']
            if fp not in used and selected[l]<needed[l]:records.append(r);used.add(fp);selected[l]+=1
        for r in valid:select(r)
        for l in LEVELS:
            while selected[l]<needed[l] and attempts[l]<5000:
                n=attempts[l];attempts[l]+=1;select(g.generate(l,b*1000+n,template=g.TEMPLATES[n%len(g.TEMPLATES)]))
        save(path/'generated.json',records);grade(records+valid,path)
        exceptions=[{'level':l,'unfilled':needed[l]-selected[l],'status':'bounded-sampler-exhausted','attempts':attempts[l]} for l in LEVELS if selected[l]<needed[l]]
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_sha256':sha(HERE.with_suffix('.py')),'needed':needed,'selected':selected,'attempts':attempts,'source_evidence_unchanged':True,'distinctness':'Primitive real-line coefficients; excludes seed/row multiples/sign/alias/choice order/layout','assets':[],'capability_exceptions':exceptions})
        for attr,ids in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in ids]],path,attr.replace('/','-')+'-identities',b)
        forms=transaction(records,kp,gid);assert forms,'Existing sufficient pool requires receipt reconciliation'
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n';atomic_text(txpath,tx)
        if '--prepare-only' in sys.argv:
            save(JOB.with_suffix('.generated'),{'instances':records,'basis':b,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py'))})
            print(json.dumps({'prepared':len(records),'by_level':selected,'basis':b}),flush=True);return
        render=json.loads((OUT/'rendering-validation.json').read_text())
        assert render['input_sha256']==sha(supplied_path) and not render['page_errors']
        assert {r['question'][':question/id'] for r in records}<={r['id'] for r in render['records']}
        assert all(not r['errors'] and not r['exposed'] for r in render['records'])
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,text=True,capture_output=True,check=True,timeout=55)
        atomic_text(path/'preview.edn',r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'dependent-line-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
        save(path/'commit-intent.json',intent);verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,gid,verified)

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

if __name__=="__main__":main()

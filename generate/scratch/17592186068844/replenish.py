"""Scoped implicit separable ODE replenishment; additive, locked and exact-basis verified."""
import copy, re, fcntl, hashlib, importlib.util, json, os, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('implicit_validation',HERE/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE=g.SOURCE['lineage']
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'d0524bb9e95e4a00ab20122d66fbfe25c9b00fd56968f47bd84b85496c8bb951'
OUT=ROOT/'reference/generated'/str(KP);OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env=database_environment('math')
NATIVE=max((ROOT/'.local/graph-explorer').glob('learning-*'),key=lambda p:p.stat().st_mtime if p.is_file() and os.access(p,os.X_OK) else 0)
QUERY=(HERE/'reference/source-query.edn').read_text()
LEVELS=['easy','moderate','hard']

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

def scoped(kp,b,seen):
    entities={};enums={}
    def enum(value):
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            e=len(enums)+1;enums[name]=e;entities[str(e)]={'db/ident':name}
        return enums[name]
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]};entities[str(q[':db/id'])]=r
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id']);field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]};entities[str(f[':db/id'])]=field
            if ':answer-field/correct'in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}


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

# Use the assessed Cartesian point to deduplicate degree/radian, layout and bank aliases.
def fingerprint(q):
    q=copy.deepcopy(q)
    q[':question/problem']=re.sub(r'\s*=\s*','=',q[':question/problem'].replace(r'\dfrac',r'\frac').replace(r'\textrm',r'\text'))
    rhs=v.ode({'question':q})
    return hashlib.sha256(g.sp.srepr(g.sp.simplify(g.sp.trigsimp(rhs))).encode()).hexdigest()


def source_canonical(x):
    if isinstance(x,dict):return {str(k):source_canonical(y) for k,y in x.items() if str(k)!=':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(x,(list,tuple)):return sorted((source_canonical(y) for y in x),key=lambda y:json.dumps(y,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def native(records,path,name):
    path.mkdir(parents=True,exist_ok=True)
    rows=[{'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every owned radio selection'} for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]} for r in records]
    save(path/(name+'-input.json'),rows)
    subprocess.run([str(HERE/'check-engine'),str(path/(name+'-input.json')),str(path/(name+'-report.json'))],check=True)
    report=json.loads((path/(name+'-report.json')).read_text());assert report['documented_unresolved_checks']==0
    return report

USAGE_QUERY='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

CHECKED=set()
def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'ever-used',basis,history=True))
    save(path/'scoped-snapshot.json',scoped(kp,basis,unavailable))
    subprocess.run([str(HERE/'check-pool'),str(path/'scoped-snapshot.json'),str(path/'native-pool.json')],capture_output=True,text=True,check=True)
    pool=json.loads((path/'native-pool.json').read_text());pool_ids={q for qs in pool['available_ids_by_level'].values() for q in qs}
    rows={l:[] for l in LEVELS};excluded=[];graded=[]
    known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).rsplit('/',1)[-1]
        reason=None
        if q[':db/id'] in unavailable:reason='Previously shown or reserved, including retained history'
        elif q.get(':knowledge-point/_canonical-example'):reason='Canonical example'
        elif level not in rows:reason='Unrated or unsupported'
        elif q[':db/id'] not in pool_ids:reason='Excluded by actual assessment_sampling::pool'
        elif q.get(':question/math-academy-id')=='q-158116':reason='Original omits y=0 exclusion in sec(y)tan(y) denominator; preserved and conservatively excluded'
        else:
            mid=q.get(':question/math-academy-id')
            if mid in g.QS:
                template=next(t for t,(l,sid) in g.TEMPLATES.items() if sid==mid)
                rec=g.generate(level,template=template,parameters={'h':0,'k':0},profile='observed')
                rec['question']=normalize(q)
            else:
                rec=known[str(q[':question/id'])]
                assert normalize(q)==ordered(rec['question'])
            checkkey=json.dumps(ordered(rec['question']),sort_keys=True)
            if checkkey not in CHECKED:v.check(rec);CHECKED.add(checkkey)
            graded.append(rec)
        if reason:excluded.append({'db_id':q[':db/id'],'reason':reason})
        else:rows[level].append(q)
    native(graded,path,'inventory-grade')
    result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fingerprint(q) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]} for l,qs in rows.items()},'native_pool':pool,'excluded_shown_or_reserved':sorted(unavailable),'excluded_questions':excluded,'deduplication':'simplified displayed ODE, ignoring seed, bank, identity, choice order and cosmetic domain variants'}
    save(path/'available-counts.json',result);return result


def candidates():
    for seed in range(int(JOB.name[:8],16),int(JOB.name[:8],16)+1000):
        for level in LEVELS:yield g.generate(level,seed)


def validate_instance(rec):
    assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.KP_UUID
    m=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS and m['bank_profile']=='standard'
    replay=g.generate(level,m['seed'],template=m['template'],parameters=m['parameters'],profile=m['bank_profile'])
    assert ordered(rec['question'])==ordered(replay['question']) and m==replay['generation']
    key=json.dumps(ordered(rec['question']),sort_keys=True)
    if key not in CHECKED:v.check(rec);CHECKED.add(key)


def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items()),'Existing questions changed'
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question']);validate_instance(rec)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    caps=json.loads((HERE/'capabilities.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':LEVELS,'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'new_by_level':prep['new_by_level'],'observed_levels':['easy'],'authored_levels':['moderate','hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'capability_exceptions':caps['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'capabilities.json',HERE/'reference/native-build.json'] if p.exists()],'note':'Observed easy and bounded authored moderate/hard domains validated. Original sec_log domain defect preserved and excluded from verified stock. No existing question, learner, or scheduler facts modified.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass' and validation['complete_source_banks']==11
    freeze=json.loads((HERE/'freeze.json').read_text());assert freeze['generator_sha256']==sha(HERE.with_suffix('.py'))
    # Repeat the complete validation fixture against the current release grader.
    subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'reference/current-engine-report.json')],check=True)
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Acquiring application api.lock',flush=True)
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application api.lock acquired',flush=True)
        assert 'lineage='+LINEAGE in DB.command('status')
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=json.loads((HERE/'source.json').read_text())['record'];current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:assert normalize(current[q[':question/math-academy-id']])==normalize(q),'Source changed; reclassify'
        assert all(str(kp[':knowledge-point/canonical-example'][k])==str(captured[':knowledge-point/canonical-example'][k]) for k in (':question/id',':question/problem',':question/worked-solution'))
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        existing=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',basis);assert len(existing)<=1
        gid=str(gen[':question-generator/id']) if gen else str(existing[0][0][':question-generator/id']) if existing else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        identity=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not identity or gen and identity[0][0][':db/id']==gen[':db/id'] or existing and identity[0][0][':question-generator/script']==SCRIPT
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:validate_instance(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        records=[];added={l:0 for l in LEVELS}
        import itertools
        for rec in itertools.chain(instances,candidates()):
            if all(added[l]>=needed[l] for l in LEVELS):break
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                validate_instance(rec);records.append(rec);used.add(fp);added[level]+=1
        save(path/'generated.json',records)
        ids=[uuid.UUID(x) for rec in records for x in [rec['question'][':question/id']]+[f[':answer-field/id'] for f in rec['question'][':question/answer-fields']]+[a[':answer/id'] for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        collisions=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not collisions,'Existing identity requires reconciliation'
        native(records,path,'generated-grade')
        (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':[],'source_evidence_unchanged':True,'source_basis':g.SOURCE['basis'],'bounded_capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions']})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'implicit-separable-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

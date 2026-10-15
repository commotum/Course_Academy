"""Scoped additive replenishment with retained requests and exact-basis readback."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'c2e69a39972d23af82871225aaae5370434066bf718239ef27d432a9b7ceb60e'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-64e7aa312fccadb0'
ENGINE = HERE / 'reference/check-engine-current'
QUERY = (HERE / 'source-query.edn').read_text()

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

def fingerprint(q):
    """Read the displayed task independently; ignore level, banks and output scale."""
    d = v.definitions(q[':question/problem'])
    F, X, Y = (d[k] for k in ('f', 'x', 'y'))
    xx, yy = v.sp.symbols('x y', positive=True)
    vv = next(z for z in X.free_symbols | Y.free_symbols if z.name in ('t', 's'))
    u = v.sp.Symbol('u', positive=True)
    composite = v.sp.factor_terms(F.subs({xx:X, yy:Y}, simultaneous=True).subs(vv,u))
    if F == xx*v.sp.exp(xx*yy):
        pref = v.sp.Poly(X.subs(vv,u),u)
        exponent = v.sp.Poly(v.sp.expand((X*Y).subs(vv,u)),u)
        composite = v.sp.Mul(v.sp.expand(pref.as_expr()/pref.LC()), v.sp.exp(v.sp.expand(exponent.as_expr()-exponent.TC())), evaluate=False)
    _, core = composite.as_independent(u, as_Add=False)
    return g.digest([v.sp.srepr(core), 'differentiate two-branch dependency'])

def native(record):
    f=record['question'][':question/answer-fields'][0]
    return {'label':record['question'][':question/id'], 'record':record, 'checks':[{'submitted_answer_id':a[':answer/id'], 'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected', 'purpose':'Actual native owned radio selection'} for a in f[':answer-field/choices']]}

def check(record):
    assert record['knowledge_point']['db_id']==KP
    assert record['generation']['eligible_for_learning'] and record['generation']['profile']=='method_branches'
    g.validate_generated_record(record)
    v.displayed_check(record)
    assert fingerprint(record['question'])==record['generation']['mathematical_fingerprint']
    m=record['generation']
    assert record==g.generate(record['question'][':question/difficulty'].split('/')[-1], m['seed'], m['template'], parameters=m['parameters'], profile=m['profile'])

USAGE_QUERY='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def source_record(q):
    by_eid={s[':db/id']:name for name,s in g.QMAP.items()}
    template=by_eid.get(q[':db/id'], 'authored_'+str(q[':question/difficulty'][':db/ident']).split('/')[-1])
    return {'knowledge_point':{'db_id':KP,'title':g.TITLE},'question':normalize(q), 'generation':{'template':template,'profile':'observed_raw'}}

def counts(kp,path,basis):
    unavailable={row[0] for row in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    unavailable.update(row[0] for row in DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q ?tx ?s true]]',[KP,LEARNER],path,'ever-shown',basis,history=True))
    groups={level:{} for level in g.LEVELS}
    records=[]
    for q in kp[':knowledge-point/questions']:
        record=source_record(q)
        v.displayed_check(record)
        records.append(record)
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        if q[':db/id'] not in unavailable and q[':db/id']!=kp[':knowledge-point/canonical-example'][':db/id']:
            groups[level].setdefault(fingerprint(q),[]).append(q[':db/id'])
    save(path/'stock-native-input.json',[native(r) for r in records])
    subprocess.run([str(ENGINE),str(path/'stock-native-input.json'),str(path/'stock-native-report.json')],check=True)
    result={'basis':basis,'available':{level:len(tasks) for level,tasks in groups.items()},'tasks':groups,'excluded_shown_or_reserved':sorted(unavailable)}
    save(path/'available-counts.json',result)
    return result

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t']
    kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text())
    assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question'])
        check(rec)
    assert not transaction([],kp,intent['generator_id'])
    stock=counts(kp,path/'after-stock',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in g.LEVELS},'available_after':stock['available'],'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result)
    return result

def finish(path,gid,verified,inv):
    result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'by_level':verified['by_level'],'available_after':verified['available_after'],'supported_levels':list(g.LEVELS),'unsupported_levels':[],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'inventory_recheck_basis':inv['basis'],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',HERE/'validation.json',HERE/'capabilities.json')],'note':'Historical and current source snapshots preserved. Moderate/hard are explicitly authored within the same two-path chain rule. No source question or learner facts modified.'}
    assert all(n>=5 for n in verified['available_after'].values())
    assert not result['remaining_jobs']
    save(path/'outcome.json',result)
    save(JOB.with_suffix('.result'),result)
    print(json.dumps(result),flush=True)

def main():
    assert json.loads((HERE/'validation.json').read_text())['status']=='passed'
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                assert intent['exact_edn']==(path/'transaction.edn').read_text()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'))
                return
        inv=inventory(OUT/'inventory-before.json')
        b=inv['basis']
        assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.REC[':knowledge-point/id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        stock=counts(kp,path/'before-stock',b)
        needed={level:max(0,5-n) for level,n in stock['available'].items()}
        print(json.dumps({'basis':b,'available':stock['available'],'needed':needed}),flush=True)
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b)
        assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];selected={level:0 for level in needed}
        supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        for rec in instances:
            check(rec)
            level=rec['question'][':question/difficulty'].split('/')[-1]
            fp=fingerprint(rec['question'])
            if selected[level]<needed[level] and fp not in used:
                records.append(rec);used.add(fp);selected[level]+=1
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated':len(instances),'generator_error':supplied.get('generatorError')})
        for level in g.LEVELS:
            for seed in range(1000):
                if selected[level]>=needed[level]:break
                rec=g.generate(level,seed=326000+seed)
                fp=fingerprint(rec['question'])
                if fp in used:continue
                check(rec)
                records.append(rec);used.add(fp);selected[level]+=1
        assert selected==needed,'Bounded sampler exhausted; leave shortage explicit'
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        assert not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'generated-identities',b) if ids else True
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or (gen and len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT)
        assets=[]
        for a in json.loads((HERE/'asset-provenance.json').read_text()):
            assert sha(Path(a['source_path']))==a['sha256']
            assets.append({'reference':a['reference'],'sha256':a['sha256'],'reused_unchanged':True})
        save(path/'generated.json',records)
        save(path/'native-input.json',[native(rec) for rec in instances+records])
        subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records))
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_before':stock['available'],'missing_by_level':needed,'selected_by_level':selected,'new_questions':len(records),'asset_hashes':assets,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'native_engine_sha256':sha(ENGINE),'distinctness':'Independently parsed composite function, ignoring independent-symbol alias, level, seed, output scaling, bank and choice order; exponential-product canonicalization also removes constant exponent shifts. Existing practice and canonical examples excluded.'})
        forms=transaction(records,kp,gid)
        assert forms,'Existing verified registration needs no new transaction'
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:
            f.write(tx);f.flush();os.fsync(f.fileno())
        previewed=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(previewed.stdout)
        pr=loads(previewed.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0])
        assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'one-independent-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':
    main()


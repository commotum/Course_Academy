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
from inventory_jobs import save
from serve_graph_explorer import database_environment
# Load the independent per-record validators without rerunning the full suite.
v = SimpleNamespace(__file__=str(HERE/'validate.py'))
exec(compile((HERE/'validate.py').read_text().split('# Independently verify extracted source raster')[0],str(HERE/'validate.py'),'exec'),v.__dict__)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'e6206544405101a376c09860a79e648a63b149aa8cbdd04f58810b1e5532f99a'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-ef48cfde3a25d91e'
QUERY = (HERE / 'reference/replenishment/source-query.edn').read_text()
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'course-academy-generator'))

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

def fingerprint(q):
    import re
    text=q[':question/problem'].replace(' ','').replace('{','').replace('}','')
    m=re.search(r'y=([\d.]+)\(([\d.]+)\^x\)([+-][\d.]+)',text)
    assert m, q[':question/problem']
    k,b,c=map(v.sp.Rational,m.groups())
    kind='intercept' if 'point of intersection' in q[':question/problem'] else 'graph'
    return g.digest({'kind':kind,'k':str(k),'c':str(c)})

def grading_item(rec):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete owned radio bank'} for a in f[':answer-field/choices']]}

def native(records,path,prefix):
    save(path/(prefix+'-input.json'),[grading_item(r) for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/(prefix+'-input.json')),str(path/(prefix+'-report.json'))],check=True,capture_output=True,text=True)

def audit(rec):
    assert rec['knowledge_point']['db_id']==KP
    v.record(rec)
    import re
    plots={Path(a[':answer/value']) for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices'] if a[':answer/type']==':answer.type/image' and a[':answer/value'].startswith('/')}
    plots|={Path(p) for p in re.findall(r'!\[\]\((.*?)\)',rec['question'].get(':question/worked-solution','')) if p.startswith('/')}
    for p in plots:v.raster(p)

def publish(records,path):
    from capture.scripts.database.images import ImageLibrary
    import re
    lib=ImageLibrary(Path('/media/jake/SSD/EDB/math'),path)
    result=copy.deepcopy(records)
    def asset(value):
        if value.startswith('images/'):
            assert (lib.root/value).is_file();return value
        p=Path(value);assert p.is_relative_to(HERE/'plots')
        relative=lib.store(p.read_bytes(),str(p))
        assert sha(lib.root/relative)==sha(p)
        return relative
    for rec in result:
        q=rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                if a[':answer/type']==':answer.type/image':a[':answer/value']=asset(a[':answer/value'])
        q[':question/worked-solution']=re.sub(r'!\[\]\((.*?)\)',lambda m:'![]('+asset(m[1])+')',q[':question/worked-solution'])
    save(path/'asset-manifest.json',list(lib.saved.values()))
    return result

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

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

LEVELS=('easy','moderate','hard')

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    rows={level:[] for level in LEVELS};checks=[]
    captured={q[':question/math-academy-id']:q for q in g.QUESTIONS}
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        if not q.get(':question/difficulty') or not q.get(':question/worked-solution') or not q.get(':question/answer-fields'):continue
        if not all(f.get(':answer-field/correct') for f in q[':question/answer-fields']):continue
        mid=q.get(':question/math-academy-id')
        if mid:
            assert source_forward(q)==source_forward(captured[mid])
            profile=next(p for p,val in g.PROFILES.items() if val[1]==mid)
            level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
            rec=g.generate(level,profile=profile);v.record(rec)
        else:
            known={r['question'][':question/id']:r for saved in OUT.glob('basis-*/generated.json') for r in json.loads(saved.read_text())}
            rec=known[str(q[':question/id'])];assert normalize(q)==ordered(rec['question'])
            level=q[':question/difficulty'][':db/ident'].split('/')[-1]
        checks.append(rec);rows[level].append(q)
    if checks:native(checks,path,'available-native')
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({fingerprint(q) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]} for level,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'incomplete_or_unrated_sources_excluded':True}
    save(path/'available-counts.json',result);return result


def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(rec['question'])
    assert not transaction([],kp,intent['generator_id'])
    for r in json.loads((path/'generated-raw.json').read_text()):audit(r)
    for a in json.loads((path/'asset-manifest.json').read_text()):
        assert sha(Path('/media/jake/SSD/EDB/math')/a['path'])==a['sha256']
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());caps={'exceptions': [{'level':'unclassified','source_id':'q-26910','reason':'Original lacks difficulty, solution and correct reference; preserved and excluded from usable inventory.'}]}
    after=verified.get('available_counts_after',prep['available_counts']);remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'unsupported_levels_filled':False,'unsupported_nominal_shortage':{},'capability_exceptions':caps['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'freeze.json'] if p.exists()],'note':'Three supported bands replenished with distinct tasks. Hard is a documented authored fractional graph extension. Legacy unclassified source remains incomplete and excluded; no source or learner facts modified.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def source_forward(value):
    if isinstance(value,dict):
        if ':db/ident' in value:return str(value[':db/ident'])
        return {str(k):source_forward(x) for k,x in value.items() if '/_' not in str(k)}
    if isinstance(value,(list,tuple)):
        return sorted((source_forward(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']; frozen=json.loads((HERE/'freeze.json').read_text()); assert all(sha(HERE.parent/p)==h for p,h in frozen['sha256'].items())
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=json.loads((HERE/'source.json').read_text())['record'];current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:assert source_forward(current[q[':question/math-academy-id']])==source_forward(q),'Source changed; reclassify'
        assert all(canonical(kp[':knowledge-point/canonical-example'][k])==canonical(val) for k,val in captured[':knowledge-point/canonical-example'].items())
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else GENERATOR_UUID
        matches=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-identity',basis)
        assert len(matches)<=1
        if matches:gid=str(matches[0][1])
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']));records=[];added={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:
            audit(rec);assert rec['knowledge_point']['db_id']==KP and rec['generation']['eligible_for_learning']
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        def candidates():
            yield from instances
            for level in LEVELS:
                for seed in range(1000):
                    if added[level]>=needed[level]:break
                    yield g.generate(level,seed=seed+int(JOB.name[:8],16))
        for rec in candidates():
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
                audit(rec);records.append(rec);used.add(fp);added[level]+=1
        # Batch lookup stable question/field/answer identities before creating entities.
        ids=[uuid.UUID(qid) for rec in records for qid in [rec['question'][':question/id'],rec['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]]
        existing=DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing,'Existing identities require reconciliation'
        visual=json.loads((OUT/'visual-reviewed.json').read_text());assert visual['passed']
        assert {r['question'][':question/id'] for r in records} <= set(visual['question_ids']), 'New instances need visual review'
        assert all(sha(Path(p))==hh for p,hh in visual['png_sha256'].items())
        save(path/'generated-raw.json',records)
        native(records,path,'raw-native')
        records=publish(records,path)
        save(path/'generated.json',records)
        native(records,path,'native')
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':json.loads((path/'asset-manifest.json').read_text()),'dependencies':{'sympy':v.sp.__version__,'python':sys.version},'source_evidence_unchanged':True,'source_basis':1356})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        if '--prepare-only' in sys.argv:
            print(json.dumps({'prepared_at':basis,'new_by_level':added,'path':str(path)}),flush=True);return
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'shift-stretch-growth-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

"""Scoped additive replenishment, serialized exact requests and exact-basis readback."""
import copy,fcntl,hashlib,importlib.util,json,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.storage import atomic_json,atomic_text
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database,QUESTION_PULL
from edn import dumps,loads,kw
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'51ab3188d40c335fd6d8899ccd99ac062749560f0f5908a933fc0dfd8d95f1ec'
OUT=ROOT/'reference/generated/17592186119848/job-51ab3188'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'
QUERY=(HERE/'reference/source-query.edn').read_text()
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] (or-join [?q ?l] (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]) (and [?l :learner/activity ?t] [?t :learner-task/status ?s] (or [?s :db/ident :learner-task.status/started] [?s :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
save=atomic_json

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,text=True,capture_output=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read_kp(path,basis):
 rows=DB.query(QUERY,[KP],path,'kp',basis);assert len(rows)==1 and str(rows[0][0][':knowledge-point/id'])==g.KP_UUID;return rows[0][0]
def fingerprint(q):return v.fingerprint(q)

def counts(kp,path,basis):
 unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'unavailable',basis)}
 unavailable.update(r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'historical-unavailable',basis,history=True))
 fresh=set();all_tasks=set();ids=[]
 for q in kp[':knowledge-point/questions']:
  if q.get(':question/difficulty',{}).get(':db/ident')!=':question.difficulty/easy':continue
  sid=q.get(':question/math-academy-id')
  if sid in g.CASES:
   rec=g.generate('easy',0,sid,{'matches':list(g.original_matches(sid))});v.fidelity(q,rec)
  else:
   normalized=normalize(q);rec=next((r for r in g.catalog() if r['question'][':question/id']==str(q[':question/id'])),None);assert rec is not None and ordered(rec['question'])==normalized;v.check(rec)
  fp=fingerprint(q);all_tasks.add(fp)
  if q[':db/id'] not in unavailable and not q.get(':knowledge-point/_canonical-example'):fresh.add(fp);ids.append(str(q[':question/id']))
 data={'basis':basis,'distinct_available':{'easy':len(fresh)},'available_ids':ids,'excluded_shown_or_reserved':sorted(unavailable),'excluded_unrated_incomplete':['q-34807','q-35270'],'nominal_shortage':{'easy':max(0,5-len(fresh)),'moderate':5,'hard':5}}
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

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path/'receipt-check', intent['source_eid'])
    kp = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')} == {k:v for k,v in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    for rec in records:
        for asset in rec['generation']['assets']:
            assert sha(Path('/media/jake/SSD/EDB/math')/asset['path'])==asset['sha256']
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q) == ordered(rec['question'])
        assert fingerprint(q) == rec['generation']['mathematical_fingerprint']
        v.check(rec)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in ('easy',)}, 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'asset_bytes_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def finish(path,gid,verified,inv):
 after=verified['basis_after'];record=read_kp(path/'final-counts',after);available=counts(record,path/'final-counts',after)
 caps=json.loads((HERE/'capabilities.json').read_text());prep=json.loads((path/'preparation.json').read_text())
 result={'outcome':'finite-limit' if prep.get('finite_limit') else 'unsupported','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':after,'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'unsupported_levels_filled':False,'available_counts':available['distinct_available'],'remaining_shortage':available['nominal_shortage'],'capability_exceptions':caps['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'note':'Validated rank-inspection generator registered. Ten source questions are fresh and easy reserve is met; no questions are added without a current shortage. Moderate/hard remain unsupported and explicitly unfilled in this bounded package.','evidence':[str(p.relative_to(ROOT)) for p in (path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'preparation.json',path/'inventory-after.json',path/'final-counts/available-counts.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'native-grading.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'capabilities.json')]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
 print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_counts','remaining_shortage')}),flush=True)

def main():
 validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']
 assert all(sha(ROOT/p)==digest for p,digest in validation['hashes'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text())
    assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
    assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b
  path=OUT/('basis-'+str(b));path.mkdir(parents=True,exist_ok=True)
  kp=read_kp(path,b);atomic_text(path/'before.edn',dumps(kp)+'\n')
  evidence=loads((HERE/'reference/source.edn').read_text())[0][0]
  expected={q[':db/id']:q for q in evidence[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
  assert all(now[e]==q for e,q in expected.items()),'Source evidence changed; reclassify'
  assert kp[':knowledge-point/canonical-example']==evidence[':knowledge-point/canonical-example']
  available=counts(kp,path,b);needed=available['nominal_shortage']['easy']
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
  contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
  registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
  assert not registered or len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
  used={fingerprint(q) for q in kp[':knowledge-point/questions'] if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy'}
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
  instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances;assert isinstance(instances,list)
  records=[]
  for rec in instances:
   v.check(rec);fp=fingerprint(rec['question'])
   if len(records)<needed and fp not in used:records.append(rec);used.add(fp)
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
  for rec in g.batch('easy',len(g.catalog()),int(JOB.name[:8],16)):
   fp=fingerprint(rec['question'])
   if len(records)<needed and fp not in used:v.check(rec);records.append(rec);used.add(fp)
  for attr,ids in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in ids]],path,attr.replace('/','-')+'-collisions',b),'Existing identity requires reconciliation'
  if instances or records:
   save(path/'native-input.json',[v.native('prepared '+str(i),rec) for i,rec in enumerate(instances+records)])
   subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  save(path/'generated.json',records)
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'source_evidence_unchanged':True,'available_counts':available,'new_questions':len(records),'missing_easy':needed,'finite_limit':len(records)<needed,'generator_sha256':sha(HERE.with_suffix('.py')),'assets':[],'distinctness':'target rank, matrix dimensions, ranks and zero patterns; ignores coefficients, seed, choice order, profile identity and labels','validation_sha256':sha(HERE/'validation.json')})
  forms=transaction(records,kp,gid)
  if not forms:
   # Existing registration and sufficient inventory: no durable empty transaction.
   verified={'basis_before':b,'basis_after':b,'new_questions':0,'passed':True,'repeat_preparation_content_changes':0}
   save(path/'verification.json',verified);finish(path,gid,verified,inv);return
  tx=dumps(forms)+'\n';txpath=path/'transaction.edn';atomic_text(txpath,tx)
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  atomic_text(path/'preview.edn',r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
  check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'inventory-rank-inspection-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
  save(path/'commit-intent.json',intent)
  verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()

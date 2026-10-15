"""Register the validated scoped generator only when current inventory needs no additions."""
import fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
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
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'8fbeb7b384edc313372d2b92c037882890b60525459ab2fcfa2bf426e35666bc'
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
NATIVE=max((p for p in (ROOT/'.local/graph-explorer').glob('learning-*') if p.is_file() and p.stat().st_mode&0o111),key=lambda p:p.stat().st_mtime)
QUERY=(HERE/'reference/source-query.edn').read_text()
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
 (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,ENV['EDB_ENDPOINT']],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def current_counts(record,path,basis):
 used={z[0] for z in DB.query(USAGE,[KP,LEARNER],path,'unavailable',basis)}
 valid={q[':db/id']:q for q in record[':knowledge-point/questions'] if len(q.get(':question/answer-fields',[]))==1 and all(':answer-field/correct' in f for f in q[':question/answer-fields'])}
 available=[q for eid,q in valid.items() if eid not in used and not q.get(':knowledge-point/_canonical-example')]
 assert all(q[':question/difficulty'][':db/ident']==':question.difficulty/easy' for q in available)
 assert len({q[':question/problem'] for q in available})==len(available)
 result={'basis':basis,'easy':len(available),'moderate':0,'hard':0,'available_ids':[str(q[':question/id']) for q in available],'unavailable_ids':sorted(used),'excluded_malformed':['q-122407'],'native_grading_evidence':str((HERE/'reference/native-report.json').relative_to(ROOT))}
 save(path/'counts.json',result);return result
def check_report(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 for e,a,val,tx,src,added in report[':edb/tx-data']:
  assert src==source and added,'Unexpected source or retraction'
  name=attrs[a]
  if e==KP:assert name==':knowledge-point/question-generator'
  elif name!=':db/txInstant':assert e in new and name in (':question-generator/id',':question-generator/script')
def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'receipt-check',intent['source_eid']);after=report[':edb/db-after-t'];record=kp(path/'readback',after)
 before=loads((path/'before.edn').read_text());exclude=':knowledge-point/question-generator'
 assert {k:x for k,x in before.items() if k!=exclude}=={k:x for k,x in record.items() if k!=exclude}
 gen=record[exclude];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 counts=current_counts(record,path/'readback',after);assert counts['easy']>=5
 verified={'passed':True,'basis_before':intent['basis'],'basis_after':after,'new_questions':0,'existing_questions_preserved':len(before[':knowledge-point/questions']),'canonical_example_preserved':True,'learner_and_engine_facts_unchanged':True,'only_scoped_additive_registration_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts':counts}
 save(path/'verification.json',verified);return verified
def finish(path,intent,verified):
 inv=inventory(path/'inventory-after.json');caps=json.loads((HERE/'capabilities.json').read_text())
 result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'verified_commit_basis':verified['basis_after'],'preparation_basis':intent['basis'],'lineage':LINEAGE,'new_questions':0,'reason':'Created, executed, exhaustively validated and registered a bounded easy generator. Rechecked current easy inventory is already above target; no surplus practice was committed.','supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'unsupported_levels_filled':False,'nominal_unfilled':{'moderate':5,'hard':5},'supported_level_shortage':{'easy':max(0,5-verified['available_counts']['easy'])},'capability_exceptions':caps['exceptions'],'available_counts':verified['available_counts'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'validation.json',HERE/'capabilities.json',HERE/'reference/source-bank-mapping.json',HERE/'reference/native-report.json',HERE/'reference/visual-review.json',HERE/'reference/freeze.json',path/'preparation.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json']]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result))
def main():
 validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass' and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
 frozen=json.loads((HERE/'reference/freeze.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen['hashes'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent,verify(path,intent,report));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
  path=OUT/f'basis-{b}';path.mkdir(exist_ok=True);record=kp(path,b);(path/'before.edn').write_text(dumps(record)+'\n')
  assert record==loads((HERE/'reference/initial/kp.edn').read_text())[0][0],'Source changed; reclassification needed'
  counts=current_counts(record,path,b);assert counts['easy']>=5,'Inventory now needs generated questions; return to preparation'
  assert not any(j['knowledgePoint']==KP and j['difficulty']=='easy' for j in inv['jobs'])
  assert not JOB.with_suffix('.generated').exists(),'Supplied instances now present; validate before preparation'
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'source',b);assert len(source)==1
  registration=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'existing-generator',b);assert len(registration)<=1
  existing=record.get(':knowledge-point/question-generator');assert not existing
  gid=str(registration[0][0][':question-generator/id']) if registration else str(uuid.uuid5(uuid.UUID(str(record[':knowledge-point/id'])),'question-generator'))
  byid=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-id',b)
  assert not byid or byid[0][0][':question-generator/script']==SCRIPT
  forms=[{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator'],[kw('db/ensure'),KP,kw('knowledge-point/validate')]]
  tx=dumps(forms)+'\n';txpath=path/'transaction.edn'
  with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'available_counts':counts,'new_questions':0,'new_assets':[],'supplied_generated_file':False,'source_preserved':True,'validation_sha256':sha(HERE/'validation.json'),'unsupported_levels_filled':False})
  r=subprocess.run([str(preview),'with','--database','math','--source',SOURCE,'--file',str(txpath)],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
  (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
  check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':ENV['EDB_ENDPOINT'],'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':f'gradient-vector-generator-{KP}-{b}-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);finish(path,intent,verify(path,intent,report))
if __name__=='__main__':main()

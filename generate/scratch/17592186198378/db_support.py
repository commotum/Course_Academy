"""Scoped EDB reads through the existing application integration."""
import hashlib,importlib.util,json,os,subprocess,sys,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT));sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('flux_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEVELS=('easy','moderate','hard');LINEAGE=g.PROVENANCE['lineage'];SOURCE=':application/ca-engine';LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'9e78a07fde0db144e4adbeff494072123f980d7d465d93dbec1b2dc8043efed4'
LOCK=ROOT/'.local/learning/requests/math/api.lock';ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
QUESTION='''[:db/id :question/id :question/math-academy-id :question/problem :question/worked-solution
 {:question/difficulty [:db/ident]}
 {[:question/answer-fields :limit nil] [:db/id :answer-field/id :answer-field/key
 {:answer-field/type [:db/ident]}
 {:answer-field/correct [:db/id :answer/id :answer/value :answer/feedback {:answer/type [:db/ident]}]}
 {[:answer-field/choices :limit nil] [:db/id :answer/id :answer/value :answer/feedback {:answer/type [:db/ident]}]}]}]'''
PATTERN='''[:db/id :knowledge-point/id :knowledge-point/title
 {:knowledge-point/question-generator [:db/id :question-generator/id :question-generator/script]}
 {:knowledge-point/canonical-example '''+QUESTION+'''}
 {[:knowledge-point/questions :limit nil] '''+QUESTION+'''}
 {[:knowledge-point/key-prerequisites :limit nil] [:db/id :topic/math-academy-id :topic/title]}]'''
QUERY='[:find (pull ?kp '+PATTERN+') :in $ ?kp :where [?kp :knowledge-point/id _]]'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plain(x):
 if isinstance(x,dict):return {str(k):plain(z) for k,z in x.items()}
 if isinstance(x,(list,tuple,set)):return [plain(z) for z in x]
 return str(x) if isinstance(x,uuid.UUID) else x
def canonical(x):
 if isinstance(x,dict):
  if ':db/ident' in x:return {':db/ident':str(x[':db/ident'])}
  return {str(k):canonical(z) for k,z in x.items()}
 if isinstance(x,(list,tuple,set)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x
def read(path,b):return DB.query(QUERY,[KP],path,'kp',b)[0][0]
def inventory(path):
 native=max((p for p in (ROOT/'.local/graph-explorer').glob('learning-*') if p.is_file() and os.access(p,os.X_OK) and 'tests' not in p.name),key=lambda p:p.stat().st_mtime_ns)
 r=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
if __name__=='__main__':
 inv=inventory(OUT/'initial-inventory.json');b=inv['basis'];kp=read(OUT/'initial',b)
 save(OUT/'initial/kp.json',plain(kp))
 print(json.dumps({'basis':b,'generator':plain(kp.get(':knowledge-point/question-generator')),'questions':[{k:plain(q.get(k)) for k in (':db/id',':question/id',':question/math-academy-id',':question/difficulty')} for q in kp[':knowledge-point/questions']],'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP]},indent=2))

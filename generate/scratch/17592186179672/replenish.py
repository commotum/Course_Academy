"""Register this finite generator under the application lock; preserve all content."""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import fcntl,hashlib,importlib.util,json,os,subprocess,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture'),str(HERE)]
from serve_graph_explorer import database_environment
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from pool_helpers import scoped,norm
spec=importlib.util.spec_from_file_location('validated_triangle',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine';SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
LOCK=ROOT/'.local/learning/requests/math/api.lock';OUT=HERE/'reference/replenishment';OUT.mkdir(exist_ok=True)
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'bfc9ddc574b3eb191160c4291c1ddd9bb5534e1d86fe1dc79a1cd942fed6d7a4'
QUERY=(HERE/'reference/source-query.edn').read_text();USAGE=(HERE/'reference/usage-query.edn').read_text();NATIVE=Path((HERE/'reference/learning-executable.txt').read_text().strip())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(path,b):return DB.query(QUERY,[KP],path,'kp',b)[0][0]
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,ENV['EDB_ENDPOINT']],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=55);x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def count(kp,b,path):
 path.mkdir(parents=True,exist_ok=True)
 unavailable={r[0] for hist in (False,True) for r in DB.query(USAGE,[KP,LEARNER],path,'historical-usage' if hist else 'current-usage',b,history=hist)}
 save(path/'snapshot.json',scoped(kp,b,unavailable));subprocess.run([str(HERE/'reference/check-pool'),str(path/'snapshot.json'),str(path/'pool.json')],capture_output=True,text=True,check=True,timeout=55);pool=json.loads((path/'pool.json').read_text());ids=set(pool['available_ids_by_level'].get('easy',[]));patterns=set();native=[]
 for q in kp[':knowledge-point/questions']:
  mid=q[':question/math-academy-id'];original=g.SOURCES[mid];assert norm(q)==norm(original)
  if q[':db/id'] in ids:
   path_name,edges=v.EDGES[mid];walk=[path_name[i:i+2] for i in range(3)];signs=tuple(1 if e==t else -1 for e,t in zip(edges,walk));assert signs==g.signs(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']);patterns.add(signs);native.append(v.engine_item(mid,{'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':norm(q),'generation':{'template':mid}}))
 save(path/'native-input.json',native);subprocess.run([str(HERE/'reference/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,timeout=55)
 c={'basis':b,'native_available':{l:len(pool['available_ids_by_level'].get(l,[])) for l in ('easy','moderate','hard')},'mathematically_distinct_available':{'easy':len(patterns),'moderate':0,'hard':0},'sign_patterns':sorted(patterns),'fresh_native_pool_and_grading_verified':True};save(path/'counts.json',c);return c

def registration(kp,gid):
 gen=kp.get(':knowledge-point/question-generator')
 if gen:
  assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT;return []
 return [{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator'],[kw('db/ensure'),KP,kw('knowledge-point/validate')]]
def check_datoms(report,path,source):
 attrs=dict(DB.attributes(path,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values());datoms=report[':edb/tx-data'];seen=set()
 for e,a,value,tx,s,added in datoms:
  name=str(attrs[a]);assert s==source and added
  if name==':db/txInstant':continue
  if e==KP:assert name==':knowledge-point/question-generator'
  else:assert e in new and name in (':question-generator/id',':question-generator/script')
  seen.add(name)
 assert seen=={':knowledge-point/question-generator',':question-generator/id',':question-generator/script'}

def verify(path,intent,receipt):
 assert receipt[':edb/committed'] and receipt[':edb/db-before-t']==intent['basis'];b=receipt[':edb/db-after-t'];check_datoms(receipt,path/'datom-check',intent['source_eid']);kp=read(path/'readback',b);before=loads((path/'before.edn').read_text());assert {k:x for k,x in kp.items() if k!=':knowledge-point/question-generator'}==before
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT;assert not registration(kp,intent['generator_id'])
 c=count(kp,b,path/'readback/inventory');assert c['mathematically_distinct_available']['easy']>=5
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'registered_generator':json.loads(json.dumps(gen,default=str)),'content_changes':0,'new_questions':0,'all_ten_source_questions_unchanged':True,'canonical_example_unchanged':True,'learner_history_unchanged':True,'other_kps_unchanged':True,'only_registration_and_tx_metadata_datoms':True,'all_datoms_attributed_to_configured_contributor':True,'repeat_preparation_changes':0,'inventory_after':c};save(path/'verification.json',result);return result

def finish(path,intent,verified,inv):
 counts=verified['inventory_after'];caps=json.loads((HERE/'capabilities.json').read_text());r={'outcome':'finite-limit','reason':'Easy inventory already exceeds its target; classification and finite generator registration verified. Moderate and hard remain unsupported within the source backbone.','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'source':SOURCE,'new_questions':0,'generated_review_instances':80,'available_after':counts['mathematically_distinct_available'],'native_available_after':counts['native_available'],'shortage_remaining':{'easy':0,'moderate':5,'hard':5},'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'unsupported_levels_filled':False,'finite_variant_limit':8,'source_distinct_variants':6,'potential_new_easy_variants':2,'no_extra_easy_content_imported_because_current_target_met':True,'capability_exceptions':caps,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'recipes.json',HERE/'source-replay.json',HERE/'validation.json',HERE/'freeze.json',HERE/'reference/engine-report.json',HERE/'reference/visual-review.json',path/'preparation.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json']]};save(path/'outcome.json',r);save(JOB.with_suffix('.result'),r);print(json.dumps({k:r[k] for k in ('outcome','verified_commit_basis','new_questions','available_after','shortage_remaining')},indent=2),flush=True)

def prepare(preview):
 for path in sorted(OUT.glob('basis-*')):
  if not (path/'commit-intent.json').exists():continue
  intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest();assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn');inventory(path/'recovery-inventory.json');report=DB._commit(intent,path/'transaction.edn',path);result=verify(path,intent,report);finish(path,intent,result,inventory(path/'inventory-after.json'));return
 inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read(path,b);original=loads((HERE/'reference/initial/kp.edn').read_text())[0][0];assert kp==original,'Source state changed: return to classification';(path/'before.edn').write_text(dumps(kp)+'\n')
 c=count(kp,b,path/'inventory-before');assert c['mathematically_distinct_available']['easy']>=5,'Supported pool now short: prepare validated unused sign states before registering';print(json.dumps({'basis':b,'current_inventory':c}),flush=True)
 supplied=JOB.with_suffix('.generated');assert not supplied.exists(),'A generated file appeared: validate before submission';save(path/'supplied-status.json',{'exists':False,'validated_instances':0})
 source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
 existing=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'existing-script',b);assert len(existing)<=1
 stored=json.loads((HERE/'registration.json').read_text()) if (HERE/'registration.json').exists() else {};gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(existing[0][0][':question-generator/id']) if existing else stored.get('id',str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator')))
 collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'existing-id',b);assert not collision or collision[0][0][':question-generator/script']==SCRIPT
 save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'identity_reused_if_existing':True});forms=registration(kp,gid);assert forms
 save(path/'generated.json',[]);save(path/'asset-manifest.json',{'published_assets':[],'reason':'no easy shortage; all generated assets remain local review artifacts'})
 save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'current_inventory':c,'required_new_supported_questions':0,'new_questions':0,'only_registration':True,'unsupported_shortages':{'moderate':5,'hard':5},'generator_sha256':sha(HERE.with_suffix('.py'))})
 tx=dumps(forms)+'\n';txpath=path/'transaction.edn'
 with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
 p=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,capture_output=True,text=True,check=True,timeout=55);(path/'preview.edn').write_text(p.stdout);report=loads(p.stdout);assert report[':edb/committed'] is False and report[':edb/db-before-t']==b;check_datoms(report,path/'preview-check',source[0][0]);assert DB.basis()==b
 intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'triangle-orientation-register-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK),'new_question_uuids':[]};save(path/'commit-intent.json',intent)
 receipt=DB._commit(intent,txpath,path);result=verify(path,intent,receipt);finish(path,intent,result,inventory(path/'inventory-after.json'))

def main():
 frozen=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen['files'].items());assert json.loads((HERE/'validation.json').read_text())['status']=='passed'
 preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Acquiring application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired; checking current inventory and basis',flush=True);prepare(preview)
if __name__=='__main__':main()

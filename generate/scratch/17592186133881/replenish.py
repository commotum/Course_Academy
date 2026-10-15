"""Serialized scoped generation, additive EDB commit and exact-basis readback."""
import fcntl,hashlib,importlib.util,json,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
from capture.scripts.storage import atomic_json,atomic_text
sys.path[:0]=[str(P),str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
import validate as v
import check_inventory as ci
import commit_helpers as h
from edn import kw,dumps,loads
from database import StaleBasis
g=v.g;KP=g.KP_ID;DB=ci.DB;LINEAGE=g.PROVENANCE['lineage'];SOURCE=':application/ca-engine';SCRIPT=str(P.with_suffix('.py').relative_to(ROOT));LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/ci.LEARNER/'32652f5a8463f21c91a91a0d4e60ffdbe384319db7f9be53436ff6064466a522'
OUT=P/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
h.DB=DB;h.KP=KP;h.SCRIPT=SCRIPT
save=atomic_json

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'),'math',ci.LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,text=True,capture_output=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read_kp(path,b):return DB.query(ci.QUERY,[KP],path,'kp',b)[0][0]
def retained():
 byid={}
 for file in OUT.glob('basis-*/generated.json'):
  for r in json.load(open(file)):byid[r['question'][':question/id']]=r
 return byid

def fingerprint(q,known):
 sid=q.get(':question/math-academy-id')
 if sid in g.REALIZATIONS:return g.canonical_key(g.REALIZATIONS[sid])
 if sid=='e-8929':return g.canonical_key((0,-1,1,0,0,0))
 rec=known[str(q[':question/id'])];assert h.normalize(q)==h.ordered(rec['question']);return v.validate(rec)

def counts(kp,b,path):
 pool=ci.available(kp,b,path);known=retained();byid={q[':db/id']:q for q in kp[':knowledge-point/questions']};result={l:[] for l in ('easy','moderate','hard')};exclusions=[];checks=[]
 for level,ids in pool['available_ids_by_level'].items():
  for eid in ids:
   q=byid[eid];sid=q.get(':question/math-academy-id')
   if sid=='q-105664':
    exclusions.append({'id':eid,'source':sid,'reason':'Contradictory clockwise/counterclockwise source solution; retained unchanged and excluded from validated reserve'});continue
   if sid in g.SOURCES:
    rec=g.generate(level,template=sid,replay=True);rec['question']=h.normalize(q)
   else:rec=known[str(q[':question/id'])];v.validate(rec);assert h.normalize(q)==h.ordered(rec['question'])
   checks.append(rec);result[level].append(fingerprint(q,known))
 v.native(checks,path/'grading')
 data={'basis':b,'native_pool':pool,'distinct_available':{l:len(set(keys)) for l,keys in result.items()},'remaining_shortage':{l:max(0,5-len(set(keys))) for l,keys in result.items()},'exclusions':exclusions,'distinctness':'normalized affine field; original unscaled diagrams conservatively collapse to same qualitative family; source profile, seed, choice order and positive overall scale ignored'}
 save(path/'validated-counts.json',data);return data

def verify(path,intent,receipt):
 assert receipt[':edb/committed'] is True and receipt[':edb/db-before-t']==intent['basis'];h.check_report(receipt,path/'receipt-check',intent['source_eid'])
 b=receipt[':edb/db-after-t'];kp=read_kp(path/'readback',b);before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(now[eid]==q for eid,q in old.items())
 omitted={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:x for k,x in before.items() if k not in omitted}=={k:x for k,x in kp.items() if k not in omitted}
 generator=kp[':knowledge-point/question-generator'];assert str(generator[':question-generator/id'])==intent['generator_id'] and generator[':question-generator/script']==SCRIPT
 records=json.load(open(path/'generated.json'));assert len(now)==len(old)+len(records)
 byid={str(q[':question/id']):q for q in now.values()}
 for r in records:assert h.normalize(byid[r['question'][':question/id']])==h.ordered(r['question']);v.validate(r)
 v.native(records,path/'readback-grading');assert h.transaction([],kp,intent['generator_id'])==[]
 c=counts(kp,b,path/'readback/inventory');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in g.SUPPORTED},'source_questions_preserved':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'additive_scoped_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c};save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
 before=json.load(open(path/'preparation.json'));after=verified['available_counts_after'];missing=after['remaining_shortage'];supported_missing={l:missing[l] for l in g.SUPPORTED}
 result={'outcome':'finite-limit' if any(supported_missing.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_by_level':verified['new_by_level'],'supported_levels':list(g.SUPPORTED),'unsupported_levels':['easy'],'unsupported_levels_filled':False,'available_counts_before':before['available_counts']['distinct_available'],'available_counts_after':after['distinct_available'],'remaining_shortage':missing,'capability_exceptions':before['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [P/'classification.md',P/'template-extraction.md',P/'plot-extraction.md',P/'source-components.json',P/'source-fidelity.json',P/'validation.json',P/'coverage.json',P/'review.md',P/'freeze.json',P/'registration.json',path/'preparation.json',path/'generated.json',path/'native-report.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json'] if p.exists()],'note':'Supported reserve counts use conservative mathematical deduplication. Easy remains explicitly unsupported, not filled; its five-question shortage is retained. Source diagram coefficients were unscaled and are not claimed as recovered.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 frozen=json.load(open(P/'freeze.json'))
 for rel,digest in frozen['files'].items():assert sha(ROOT/rel)==digest,'Frozen artifact changed: '+rel
 assert json.load(open(P/'validation.json'))['passed'];assert sha(v.ENGINE)==json.load(open(P/'validation.json'))['grader_executable_sha256']
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  for path in sorted(OUT.glob('basis-*')):
   if not (path/'commit-intent.json').exists():continue
   intent=json.load(open(path/'commit-intent.json'));assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
   assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);atomic_text(path/'before.edn',dumps(kp)+'\n')
  current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
  for sid,old in g.SOURCES.items():assert h.source_shape(current[sid],old)==h.canonical(old),'Source changed; reclassification required'
  assert h.source_shape(kp[':knowledge-point/canonical-example'],g.SOURCE['record'][':knowledge-point/canonical-example'])==h.canonical(g.SOURCE['record'][':knowledge-point/canonical-example'])
  contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
  gen=kp.get(':knowledge-point/question-generator');byscript=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-script',b);assert len(byscript)<=1
  registration=P/'registration.json';saved=json.load(open(registration))['id'] if registration.exists() else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'));gid=str(gen[':question-generator/id']) if gen else str(byscript[0][1]) if byscript else saved
  matched=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-id',b);assert not matched or len(matched)==1 and matched[0][0][':question-generator/script']==SCRIPT
  save(registration,{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or byscript or registration.exists()),'generator_sha256':sha(P.with_suffix('.py'))})
  c=counts(kp,b,path/'current-inventory');needed={l:c['remaining_shortage'][l] for l in g.SUPPORTED};print(json.dumps({'basis':b,'validated_available':c['distinct_available'],'missing_supported':needed}),flush=True)
  supplied_path=JOB.with_suffix('.generated');supplied=json.load(open(supplied_path)) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances;assert isinstance(instances,list)
  for r in instances:v.validate(r)
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
  known=retained();used={fingerprint(q,known) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example'],known));records=[];added={l:0 for l in g.SUPPORTED};attempts={l:0 for l in g.SUPPORTED}
  candidates=instances[:]
  # Review candidate differs from the source outward spiral in radial/angular
  # ratio (3:1 rather than baseline 1:1), visibly changing quadrant directions.
  candidates.append(g.generate('moderate',seed=int(JOB.name[:8],16),template='q-105692',params=(3,-1,1,3,0,0)))
  for level in g.SUPPORTED:
   for i in range(512):
    if added[level]>=needed[level]:break
    rec=candidates.pop(0) if candidates else g.generate(level,seed=int(JOB.name[:8],16)+i)
    actual=rec['question'][':question/difficulty'].split('/')[-1]
    if actual not in needed or added[actual]>=needed[actual]:continue
    attempts[actual]+=1;key=v.validate(rec)
    if key in used:continue
    used.add(key);records.append(rec);added[actual]+=1
  exceptions=[{'level':'easy','requested':5,'produced':0,'remaining':5,'filled':False,'reason':'Bounded evidence: no rated easy source or supported calibration in the captured 14-question source bank; no artificial downgrade.'}]+[{'level':l,'requested':needed[l],'produced':added[l],'remaining':needed[l]-added[l],'filled':False,'reason':'Bounded 512 sampler attempts exhausted; normalized affine domain only, not proof of global mathematical exhaustion.'} for l in g.SUPPORTED if added[l]<needed[l]]
  # Publish only validated selected assets through existing content-addressed store.
  library=ImageLibrary(Path('/media/jake/SSD/EDB/math'),path)
  for r in records:
   for a in r['generation']['assets']:
    local=Path(a['prompt']);relative=library.store(local.read_bytes(),str(local));r['question'][':question/problem']=r['question'][':question/problem'].replace(str(local),relative);assert sha(library.root/relative)==a['sha256'];v.validate(r)
  ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]];assert len(ids)==len(set(ids))
  collisions=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identities',b) if ids else [];assert not collisions,'Existing identity needs reconciliation'
  save(path/'generated.json',records);atomic_text(path/'generated.md','\n\n---\n\n'.join(map(g.markdown,records))+'\n');v.native(records,path)
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'sampling_attempts':attempts,'capability_exceptions':exceptions,'assets':library.saved,'generator_sha256':sha(P.with_suffix('.py')),'all_selected_instances_mathematically_validated':True,'all_selected_instances_actual_grader_validated':True,'source_basis':g.PROVENANCE['basis']})
  forms=h.transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'new_by_level':added,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
  txpath=path/'transaction.edn';atomic_text(txpath,dumps(forms)+'\n');r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55);atomic_text(path/'preview.edn',r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;h.check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'visual-curl-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':txpath.read_text(),'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(P.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)};save(path/'commit-intent.json',intent)
  verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()

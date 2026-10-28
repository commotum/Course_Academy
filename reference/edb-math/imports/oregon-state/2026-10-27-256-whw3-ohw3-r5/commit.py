"""Commit the reviewed additive assignment import and verify exact db-after."""
import collections,hashlib,json,subprocess,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,loads,kw
from f26_assignment_content import LEGACY_SEEDS
from import_school_assignments import stable_id

def save(name,value):(H/name).write_text(json.dumps(value,default=str,indent=2)+'\n')
def main():
 assert sys.argv[1:]==['--apply-user-authorized']
 a=json.loads((H/'source-audit.json').read_text());entities=json.loads((H/'entities.json').read_text());payload=H/'transaction.edn';sha=hashlib.sha256(payload.read_bytes()).hexdigest();assert sha==a['sha256']
 render=json.loads((H/'render-verification.json').read_text());assert render['passed'] and render['questions']==39
 assert render['source_sha256']==sha
 assert json.loads((H/'grading-verification.json').read_text())['source_sha256']==sha
 assert len(entities)==211 and len(a['added_targets'])==12
 assert json.loads((H/'native-preview-verification.json').read_text())['sha256']==sha
 assert json.loads((H/'grading-verification.json').read_text())['accepted_checks']==36
 for asset in a['assets']:assert hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest()==asset['sha256']
 for source in a['activities']:assert hashlib.sha256((Path('/home/jake/Developer/study/vault')/source['source']).read_bytes()).hexdigest()==source['sha256']
 db=connection();intent_path=H/'commit-intent.json'
 identities=[]
 for r in entities:
  attr=next(k for k in r if k.endswith('/id') and k!=':db/id');identities.append([kw(attr),uuid.UUID(r[attr]['$uuid'])])
 if intent_path.exists():intent=json.loads(intent_path.read_text());assert intent['sha256']==sha
 else:
  basis=db.basis();present=db.query('[:find ?a ?id ?e :in $ [[?a ?id]] :where [?e ?a ?id]]',[identities],H,'identities-before',basis);assert not present,'Assignment content now exists; do not overwrite it'
  learner=db.query('[:find (pull ?l [:db/id :learner/assignments :learner/targets]) :in $ ?id :where [?l :learner/id ?id]]',[a['learner_uuid']],H,'learner-before',basis)[0][0]
  assert {r[':db/id'] for r in learner[':learner/assignments']}==set(a['old_assignment_eids'])
  assert {r[':db/id'] for r in learner[':learner/targets']}==set(a['old_target_eids'])
  # An immutable optimistic guard protects every absence and learner-set check.
  intent={'database':'math','basis':basis,'source':a['source'],'endpoint':'/tmp/edb-math/writer.sock','file':str(payload),'sha256':sha,'request_key':'f26-256-whw3-ohw3-r5-'+sha[:24]+'-b'+str(basis)};save('commit-intent.json',intent)
 receipt=None
 if (H/'receipt.edn').exists():
  try:receipt=loads((H/'receipt.edn').read_text())
  except (IndexError,ValueError):pass
 if not isinstance(receipt,dict) or receipt.get(':edb/committed') is not True:
  command=[db.args.edb_bin,'transact','--database',intent['database'],'--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--basis',str(intent['basis']),'--timeout-ms','120000']
  with (H/'receipt.edn').open('w') as out,(H/'submit.stderr').open('w') as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,timeout=160,check=True)
  receipt=loads((H/'receipt.edn').read_text())
 assert receipt[':edb/committed'] is True;basis=receipt[':edb/db-after-t'];assert receipt[':edb/db-before-t']==intent['basis']
 rows=db.query('[:find ?a ?id (pull ?e [*]) :in $ [[?a ?id]] :where [?e ?a ?id]]',[identities],H,'entities-after',basis);assert len(rows)==len(entities)
 ids={(str(attr),str(identity)):r[':db/id'] for attr,identity,r in rows};byuid={r[':db/id']:ids[next(k for k in r if k.endswith('/id') and k!=':db/id'),next(r[k]['$uuid'] for k in r if k.endswith('/id') and k!=':db/id')] for r in entities}
 external={}
 def resolve(value):
  if isinstance(value,dict):
   if '$uuid' in value:return uuid.UUID(value['$uuid'])
   if '$inst' in value:return value['$inst']
   if '$ref' in value:
    attr,v=value['$ref'];key=str(value['$ref'])
    if key not in external:
     v=resolve(v);q=db.query('[:find ?e :in $ ?a ?v :where [?e ?a ?v]]',[kw(attr),v],H,'external-'+hashlib.sha256(key.encode()).hexdigest()[:12],basis);assert len(q)==1;external[key]=q[0][0]
    return external[key]
  if isinstance(value,list):return sorted([resolve(v) for v in value],key=str)
  if isinstance(value,str):
   if value in byuid:return byuid[value]
   if value.startswith(':'):
    key=value
    if key not in external:
     q=db.query('[:find ?e :in $ ?ident :where [?e :db/ident ?ident]]',[kw(value)],H,'enum-'+value[1:].replace('/','-'),basis);assert len(q)==1;external[key]=q[0][0]
    return external[key]
  return value
 actual={r[':db/id']:r for _,_,r in rows};comparisons=0
 from datetime import datetime,timezone
 for r in entities:
  got=actual[byuid[r[':db/id']]]
  for attr,value in r.items():
   if attr in (':db/id',':db/ensure'):continue
   expected=resolve(value);current=got[attr]
   def norm(v):
    if isinstance(v,dict) and ':db/id' in v:return v[':db/id']
    if isinstance(v,list):return sorted([norm(x) for x in v],key=str)
    return v
   current=norm(current)
   if isinstance(value,dict) and '$inst' in value:assert datetime.fromisoformat(current.replace('Z','+00:00'))==datetime.fromisoformat(expected.replace('Z','+00:00')),(attr,current,expected)
   else:assert current==expected,(r[':db/id'],attr,current,expected)
   comparisons+=1
 learner=db.query('[:find (pull ?l [:db/id :learner/assignments :learner/targets]) :in $ ?id :where [?l :learner/id ?id]]',[a['learner_uuid']],H,'learner-after',basis)[0][0]
 assignments={r[':db/id'] for r in learner[':learner/assignments']};targets={r[':db/id'] for r in learner[':learner/targets']}
 assert assignments==set(a['old_assignment_eids'])|{byuid[x] for x in a['activity_ids']}
 assert targets==set(a['old_target_eids'])|{x['entity'] for x in a['all_requested_targets']}
 ds=receipt[':edb/tx-data'];source_id=resolve(a['source']);assert all(d[-2]==source_id for d in ds)
 assert all(d[-1] is True for d in ds),'An import must not retract existing data'
 newids=set(byuid.values());assert newids.isdisjoint(set(a['old_assignment_eids']))
 # Every changed pre-existing entity must be precisely the additive assignment and target sets
 # on the learner. Other datoms are the new assignment content records and transaction metadata.
 old=[d for d in ds if d[0] not in newids and d[0]!=receipt.get(':edb/tx')]
 allowedattrs=db.query('[:find ?a ?i :in $ [?i ...] :where [?a :db/ident ?i]]',[[kw('learner/assignments'),kw('learner/targets'),kw('db/txInstant')]],H,'changed-attributes',basis);attrs={str(i):e for e,i in allowedattrs}
 learnerchanges=[d for d in ds if d[0]==a['learner_entity']]
 assert len(learnerchanges)==3+len(a['added_targets']) and all(d[1] in [attrs[':learner/assignments'],attrs[':learner/targets']] for d in learnerchanges)
 assert all(d[0] in newids or d[0]==a['learner_entity'] or d[1]==attrs[':db/txInstant'] for d in ds)
 report={'committed':True,'basis_t':basis,'request_key':intent['request_key'],'source':intent['source'],'sha256':sha,'assignments_imported':3,'questions_imported':39,'entities_verified':len(entities),'attributes_verified':comparisons,'total_assignments':len(assignments),'new_targets':len(a['added_targets']),'total_targets':len(targets),'topic_links_and_prerequisites_verified':True,'all_existing_assignments_targets_and_learner_history_preserved':True,'only_new_content_and_additive_learner_links_changed':True,'no_retractions':True,'activity_entity_ids':{x:byuid[x] for x in a['activity_ids']}}
 save('verification.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()

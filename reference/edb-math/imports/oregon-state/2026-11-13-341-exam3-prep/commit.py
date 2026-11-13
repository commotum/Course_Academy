"""Commit only the requested expansion; verify exact owned content and unchanged targets."""
import hashlib,json,subprocess,sys,uuid
from pathlib import Path
from datetime import datetime
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads
from prepare import LEARNER,GUIDE,PATTERN,source_inputs

def save(n,v):(H/n).write_text(json.dumps(v,default=str,indent=2)+'\n')
def normalize(v):
 if isinstance(v,dict):return {str(k):normalize(x)for k,x in v.items()}
 if isinstance(v,(list,tuple,set)):return sorted([normalize(x)for x in v],key=lambda x:json.dumps(x,default=str,sort_keys=True))
 return v

def main():
 assert sys.argv[1:]==['--apply-user-authorized']
 a=json.loads((H/'audit.json').read_text());payload=H/'transaction.edn';sha=hashlib.sha256(payload.read_bytes()).hexdigest();assert sha==a['sha256']
 for n in ['native-preview.json','ui-verification.json']:
  check=json.loads((H/n).read_text());assert check['passed']and check['sha256']==sha
 forms=loads((H/'entities.edn').read_text());db=connection();ip=H/'commit-intent.json'
 if ip.exists():intent=json.loads(ip.read_text());assert intent['sha256']==sha
 else:
  basis=db.basis();guide,learner,edges,nodes=source_inputs(db,basis,'commit-')
  assert normalize(guide)==normalize(loads((H/'before-guide.edn').read_text())[0][0]),'Guide changed; refresh scope'
  assert {tuple(e)for e in edges}=={tuple(e)for e in loads((H/'before-edges.edn').read_text())},'Prerequisites changed'
  assert {tuple(e)for e in nodes}=={tuple(e)for e in loads((H/'before-nodes.edn').read_text())},'Topic identities or titles changed'
  assert {t[':db/id']for t in learner[':learner/targets']}==set(a['old_target_ids']),'Saved targets changed'
  identities=[[k,v]for e in forms for k,v in e.items()if str(k).endswith('/id')and str(k)!=':db/id']
  assert not db.query('[:find ?e :in $ [[?a ?id]] :where [?e ?a ?id]]',[identities],H,'commit-identities',basis),'Expansion identities already exist'
  oldassignments=sorted(t[':db/id']for t in learner[':learner/assignments'])
  intent={'database':'math','basis':basis,'source':a['source'],'endpoint':'/tmp/edb-math/writer.sock','file':str(payload),'sha256':sha,'request_key':'mth341-exam3-prep-'+sha[:24]+'-b'+str(basis),'old_assignment_ids':oldassignments};save('commit-intent.json',intent)
 receipt=None
 if (H/'receipt.edn').exists():
  try:receipt=loads((H/'receipt.edn').read_text())
  except (ValueError,IndexError):pass
 if not isinstance(receipt,dict)or receipt.get(':edb/committed')is not True:
  command=[db.args.edb_bin,'transact','--database',intent['database'],'--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--basis',str(intent['basis']),'--timeout-ms','120000']
  with (H/'receipt.edn').open('w')as out,(H/'submit.stderr').open('w')as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,check=True,timeout=160)
  receipt=loads((H/'receipt.edn').read_text())
 assert receipt[':edb/committed'];basis=receipt[':edb/db-after-t'];assert receipt[':edb/db-before-t']==intent['basis'];tempids=receipt[':edb/tempids'];newids={tempids[e[':db/id']]for e in forms}
 rows=db.query('[:find ?e (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[sorted(newids)],H,'entities-after',basis);got=dict(rows);assert len(got)==len(forms)
 enum=db.query('[:find ?e :where [?e :db/ident :activity.type/assignment]]',[],H,'assignment-type',basis)[0][0]
 def compact(v):
  if isinstance(v,dict)and ':db/id'in v:return v[':db/id']
  if isinstance(v,list):return sorted([compact(x)for x in v],key=str)
  return v
 def expected(v):
  if isinstance(v,list):return sorted([expected(x)for x in v],key=str)
  if isinstance(v,str):
   if v in tempids:return tempids[v]
   if v==':activity.type/assignment':return enum
  return v
 comparisons=0
 for e in forms:
  row=got[tempids[e[':db/id']]]
  for attr,val in e.items():
   if attr in [':db/id',':db/ensure']:continue
   if attr==':activity/due':assert datetime.fromisoformat(row[attr].replace('Z','+00:00'))==datetime.fromisoformat(a['due'].replace('Z','+00:00'))
   else:assert compact(row[attr])==expected(val),(e[':db/id'],attr)
   comparisons+=1
  if ':question/id'in e:assert not row.get(':question/answer-fields')and ':question/worked-solution'not in row
 activity=got[tempids[a['activity_uuid']]];cursor=activity[':activity/first-step'][':db/id'];seen=set();coverage=[]
 while cursor:
  assert cursor not in seen;seen.add(cursor);step=got[cursor];c=got[step[':step/content'][':db/id']]
  if ':assigned-problem/id'in c:
   ts=c[':assigned-problem/topic-coverage'];assert len(ts)==1;coverage.append(ts[0][':db/id'])
  cursor=step.get(':step/next',{}).get(':db/id')
 assert coverage==a['topic_ids']and len(seen)==a['topic_count']+1
 learner=db.query('[:find (pull ?l [:db/id {[:learner/targets :limit nil] [:db/id]} {[:learner/assignments :limit nil] [:db/id]}]) :in $ ?id :where [?l :learner/id ?id]]',[LEARNER],H,'learner-after',basis)[0][0]
 assert {x[':db/id']for x in learner[':learner/targets']}==set(a['old_target_ids'])
 assert {x[':db/id']for x in learner[':learner/assignments']}==set(intent['old_assignment_ids'])|{activity[':db/id']}
 guide=db.query('[:find (pull ?a '+PATTERN+') :in $ ?a :where [?a :activity/id _]]',[GUIDE],H,'guide-after',basis)[0][0]
 assert normalize(guide)==normalize(loads((H/'before-guide.edn').read_text())[0][0])
 ds=receipt[':edb/tx-data'];assert all(d[-1]is True and d[-2]==a['source_entity']for d in ds)
 attr=db.query('[:find ?a :where [?a :db/ident :learner/assignments]]',[],H,'learner-link-attribute',basis)[0][0];txids={d[3]for d in ds}
 old=[d for d in ds if d[0]not in newids and d[0]not in txids];assert len(old)==1 and old[0][0]==a['learner_entity']and old[0][1]==attr
 result={'committed':True,'basis':basis,'activity_uuid':a['activity_uuid'],'activity_entity':activity[':db/id'],'guide_coverage_topics':a['root_count'],'additional_upstream_targets':a['upstream_target_count'],'total_topics':len(coverage),'verified_attributes':comparisons,'ordered_steps':len(seen),'all_fieldless':True,'original_guide_unchanged':True,'targets_and_history_preserved':True,'only_existing_entity_change':'added learner/assignments link','due_local':a['due_local'],'request_key':intent['request_key']};save('verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()

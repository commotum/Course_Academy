"""Commit and verify the user-authorized study assignment with a stable request."""
import hashlib,json,subprocess,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads
from prepare import LEARNER

def save(name,v):(H/name).write_text(json.dumps(v,default=str,indent=2)+'\n')
def main():
 assert sys.argv[1:]==['--apply-user-authorized']
 a=json.loads((H/'audit.json').read_text());sha=hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest();assert sha==a['sha256']
 preview=loads((H/'preview.edn').read_text());assert preview[':edb/committed'] is False and preview[':edb/db-before-t']==a['basis']
 db=connection();ip=H/'commit-intent.json'
 if ip.exists():intent=json.loads(ip.read_text());assert intent['sha256']==sha
 else:
  assert db.basis()==a['basis'],'Database advanced: recheck the prepared scope before committing.'
  intent={'database':'math','basis':a['basis'],'source':a['source'],'endpoint':'/tmp/edb-math/writer.sock','file':str(H/'transaction.edn'),'sha256':sha,'request_key':'mth256-quiz3-prep-'+sha[:24]+'-b'+str(a['basis'])};save('commit-intent.json',intent)
 receipt=None
 if (H/'receipt.edn').exists():
  try:receipt=loads((H/'receipt.edn').read_text())
  except (IndexError,ValueError):pass
 if not isinstance(receipt,dict) or receipt.get(':edb/committed') is not True:
  command=[db.args.edb_bin,'transact','--database',intent['database'],'--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--basis',str(intent['basis']),'--timeout-ms','120000']
  with (H/'receipt.edn').open('w') as out,(H/'submit.stderr').open('w') as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,timeout=160,check=True)
  receipt=loads((H/'receipt.edn').read_text())
 assert receipt[':edb/committed'] is True;basis=receipt[':edb/db-after-t'];assert receipt[':edb/db-before-t']==intent['basis']
 assert all(d[-1] is True for d in receipt[':edb/tx-data'])
 pattern='''[:db/id :activity/id :activity/title :activity/due :activity/course :activity/type :activity/first-step
 {:activity/steps [:db/id :step/id :step/next {:step/content [:db/id :tutorial/id :tutorial/title :tutorial/content :assigned-problem/id
 {:assigned-problem/topic-coverage [:db/id :topic/id :topic/title]}
 {:assigned-problem/content [:db/id :question/id :question/problem :question/answer-fields]}]}]}]'''
 got=db.query('[:find (pull ?a '+pattern+') :in $ ?id :where [?a :activity/id ?id]]',[uuid.UUID(a['activity_uuid'])],H,'assignment-after',basis);assert len(got)==1;activity=got[0][0]
 forms=loads((H/'transaction.edn').read_text());bytemp={r[':db/id']:r for r in forms if isinstance(r,dict)};intents=receipt[':edb/tempids']
 assert activity[':db/id']==intents[a['activity_uuid']]
 assert activity[':activity/title']=='MTH 256 — Quiz 3 Preparation';assert activity[':activity/due']==a['due'];assert activity[':activity/course'][':db/id']==a['course_entity']
 steps={r[':db/id']:r for r in activity[':activity/steps']};assert len(steps)==106
 cursor=activity[':activity/first-step'][':db/id'];seen=set();coverage=[]
 while cursor is not None:
  assert cursor not in seen;seen.add(cursor);step=steps[cursor];c=step[':step/content']
  if ':tutorial/id' in c:
   assert len(seen)==1 and a['announcement'].splitlines()[2] in c[':tutorial/content']
   expected=next(r[':tutorial/content'] for r in bytemp.values() if ':tutorial/id' in r);assert c[':tutorial/content']==expected
  else:
   assert len(c[':assigned-problem/topic-coverage'])==1;topic=c[':assigned-problem/topic-coverage'][0][':db/id'];coverage.append(topic)
   q=c[':assigned-problem/content'];assert not q.get(':question/answer-fields')
   expected=next(r[':question/problem'] for r in bytemp.values() if r.get(':question/id')==q[':question/id']);assert q[':question/problem']==expected
  cursor=step.get(':step/next',{}).get(':db/id')
 assert seen==set(steps) and coverage==a['topic_ids']
 learner=db.query('[:find (pull ?l [:db/id {[:learner/targets :limit nil] [:db/id]} {[:learner/assignments :limit nil] [:db/id]}]) :in $ ?id :where [?l :learner/id ?id]]',[LEARNER],H,'learner-after',basis)[0][0]
 assert {t[':db/id'] for t in learner[':learner/targets']}==set(a['old_target_ids'])
 assert {t[':db/id'] for t in learner[':learner/assignments']}==set(a['old_assignment_ids'])|{activity[':db/id']}
 source=loads((H/'source-before.edn').read_text())[0][0];assert all(d[-2]==source for d in receipt[':edb/tx-data'])
 attr=db.query('[:find ?a :where [?a :db/ident :learner/assignments]]',[],H,'assignment-link-attribute',basis)[0][0]
 newids=set(intents.values());txids={d[3] for d in receipt[':edb/tx-data']};assert len(txids)==1
 oldchanges=[d for d in receipt[':edb/tx-data'] if d[0] not in newids and d[0] not in txids]
 assert len(oldchanges)==1 and oldchanges[0][0]==a['learner_entity'] and oldchanges[0][1]==attr
 report={'committed':True,'basis':basis,'activity_uuid':a['activity_uuid'],'activity_entity':activity[':db/id'],'topics':len(coverage),'ordered_steps':len(seen),'due_local':a['due_local'],'announcement_verified':True,'all_topic_links_verified':True,'existing_targets_and_progress_preserved':True,'only_existing_entity_change':'added learner/assignments link','request_key':intent['request_key']};save('verification.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()

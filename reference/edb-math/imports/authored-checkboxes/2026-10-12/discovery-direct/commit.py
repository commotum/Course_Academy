"""Submit the user-authorized, previewed batches and verify exact receipts."""
import argparse,hashlib,json,shutil
from pathlib import Path
import prepare as migration
edb=migration.edb
OUT=migration.OUT

def commit():
 plan=json.loads((OUT/'plan.json').read_text());preview=json.loads((OUT/'preview.json').read_text())
 assert preview['passed']and preview['committed']is False and preview['basis']==plan['basis']
 assert plan['counts']['questions']==780 and plan['counts']['batches']==4
 assert preview['source']==plan['source']==migration.SOURCE
 root_intent=OUT/'commit-intent.json'
 if not root_intent.exists():
  assert edb.DB.basis()==plan['basis'],'Database advanced before any submission; refresh and preview again'
  edb.save('commit-intent.json',{'state':'submission_authorized','basis':plan['basis'],'source':migration.SOURCE,'batches':plan['batches'],'counts':plan['counts']})
 root=json.loads(root_intent.read_text());assert root['batches']==plan['batches']
 receipts=[]
 for b in plan['batches']:
  directory=Path(b['directory']);m=json.loads((directory/'plan.json').read_text());req=json.loads((directory/'prepared-request.json').read_text());p=json.loads((directory/'preview.json').read_text());tx=directory/'transaction.edn'
  assert hashlib.sha256(tx.read_bytes()).hexdigest()==req['sha256']==m['transaction_sha256']==p['transaction_sha256']==b['sha256']
  assert req['basis']==m['basis']==p['basis']==b['basis_guard']
  assert p['passed']and p['committed']is False and req['source']==m['source']==migration.SOURCE
  if receipts:assert receipts[-1]['basis_after']==req['basis']
  edb.OUT=directory;intent_path=directory/'commit-intent.json'
  if not intent_path.exists():edb.save('commit-intent.json',{**req,'state':'submission_requested'})
  intent=json.loads(intent_path.read_text());assert {k:v for k,v in intent.items()if k!='state'}=={k:v for k,v in req.items()if k!='state'}
  report=edb.DB._commit(intent,tx,directory)
  assert report[':edb/committed']is True
  receipt={'committed':True,'batch':b['number'],'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],'source':migration.SOURCE,'request_key':intent['request_key'],'transaction_sha256':intent['sha256'],'tx_hash':report.get(':edb/tx-hash'),'replayed':report.get(':edb/replayed'),'datoms':len(report[':edb/tx-data']),'counts':m['counts']}
  # Persist confirmed success before any local formatting/validation can fail.
  edb.save('commit-receipt.json',receipt)
  edb.verify_preview(report,committed=True)
  receipts.append(receipt)
  print(json.dumps({'batch_committed_and_validated':b['number'],'basis_before':receipt['basis_before'],'basis_after':receipt['basis_after'],'questions':m['counts']['questions']}),flush=True)
 edb.OUT=OUT
 edb.save('commit-receipt.json',{'committed':True,'basis_before':plan['basis'],'basis_after':receipts[-1]['basis_after'],'source':migration.SOURCE,'counts':plan['counts'],'batches':receipts})
 print(json.dumps({'all_batches_committed':True,'basis_before':plan['basis'],'basis_after':receipts[-1]['basis_after'],**plan['counts']}),flush=True)

def verify():
 plan=json.loads((OUT/'plan.json').read_text());summary=json.loads((OUT/'commit-receipt.json').read_text());snapshot=edb.loads((OUT/'snapshot.edn').read_text());basis=summary['basis_after']
 assert summary['committed']and len(summary['batches'])==4
 before={r[0][':db/id']:r[0]for r in snapshot['questions']};changes={};ids={}
 for b in plan['batches']:
  directory=Path(b['directory']);m=json.loads((directory/'plan.json').read_text());report=edb.loads((directory/'commit.edn').read_text())
  assert report[':edb/committed']
  changes.update({q['id']:q for q in m['questions']});ids.update(report[':edb/tempids'])
 query='[:find (pull ?q '+edb.QUESTION+') :in $ [?q ...] :where [?q :question/id _]]'
 after={r[0][':db/id']:r[0]for r in edb.batches(query,sorted(changes),'questions-after',basis,64)}
 assert set(after)==set(changes)==set(before)
 original={};total_fields=0
 for qid,change in changes.items():
  old,current=before[qid],after[qid]
  exempt={':question/problem',':question/answer-fields'}
  assert {k:v for k,v in old.items()if k not in exempt}=={k:v for k,v in current.items()if k not in exempt},('Unrelated question content changed',qid)
  assert current[':question/problem']==change['problem_after']
  fs=current[':question/answer-fields'];fields={f[':answer-field/key']:f for f in fs}
  assert len(fs)==len(fields)==len(change['labels'])and set(fields)==set(change['labels'])
  assert {f[':db/id']for f in fs}=={ids[t]for t in change['new_field_tempids']}
  for label,f in fields.items():
   token=change['ma_id']+'/authored-checkbox-v1/'+label
   assert f[':answer-field/id']==edb.stable_id('field',token)and f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'
   bank={a[':answer/value']:a for a in f[':answer-field/choices']};assert len(f[':answer-field/choices'])==2 and set(bank)=={'false','true'}
   for value,a in bank.items():assert a[':answer/id']==edb.stable_id('answer',token+'/'+value)and a[':answer/type'][':db/ident']==':answer.type/text'
   assert f[':answer-field/correct']==bank[str(label in change['correct']).lower()];total_fields+=1
  for f in old[':question/answer-fields']:original[f[':db/id']]=f;original.update({a[':db/id']:a for a in f[':answer-field/choices']})
 assert total_fields==plan['counts']['new_checkbox_fields']==2417
 pattern='''[* {:answer/type [:db/id :db/ident]} {:answer-field/type [:db/id :db/ident]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]'''
 retained={r[0][':db/id']:r[0]for r in edb.batches('[:find (pull ?e '+pattern+') :in $ [?e ...] :where (or [?e :answer/id _] [?e :answer-field/id _])]',sorted(original),'originals-after',basis,128)}
 assert retained==original,'Original field/answer entities changed or disappeared'
 # Check the exact prior historical question view, not today's head.
 historical={r[0][':db/id']:r[0]for r in edb.batches(query,sorted(before),'questions-historical',plan['basis'],128)}
 assert historical==before
 items=edb.batches('[:find ?q (pull ?item '+edb.ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',sorted(changes),'items-after',basis,128)
 old_items={i[':db/id']:(qid,i)for qid,i in snapshot['items']};new_items={i[':db/id']:(qid,i)for qid,i in items};assert set(new_items)==set(old_items)
 mapped={r['item']:r for b in plan['batches']for r in json.loads((Path(b['directory'])/'plan.json').read_text())['responses']}
 for itemid,(qid,old)in old_items.items():
  current_qid,current=new_items[itemid];assert current_qid==qid
  if itemid not in mapped:assert current==old
  else:
   assert {k:v for k,v in current.items()if k!=':task-item/responses'}=={k:v for k,v in old.items()if k!=':task-item/responses'}
   assert {a[':db/id']for a in current[':task-item/responses']}=={ids[t]for t in mapped[itemid]['new_answer_tempids']}
 edb.save('verification.json',{'passed':True,'committed':True,'basis_before':plan['basis'],'basis_after':basis,'source':migration.SOURCE,'counts':plan['counts'],'retained_original_entities':len(original),'checks':['Every question, checkbox field, owned Boolean bank, stored answer subset, and prompt read back at the confirmed final basis.','Worked solutions, difficulty, KP membership and all unrelated question attributes preserved.','Original field/answer entities retained unchanged; original historical question snapshot reproduced.','Learner presentations and response mappings preserved.','Each exact committed receipt validated for source, expected retractions and permitted datoms before submitting the next batch.']})
 print(json.dumps({'final_readback_verified':True,'basis_after':basis,'questions':len(changes),'checkbox_fields':total_fields,'retained_original_entities':len(original)}),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['commit','verify']);globals()[parser.parse_args().action]()

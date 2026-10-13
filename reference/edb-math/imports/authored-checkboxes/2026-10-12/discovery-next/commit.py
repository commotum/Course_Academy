"""Submit authorized exact prepared requests; retain receipts and verify confirmed state."""
import argparse,json,re,subprocess
from pathlib import Path
import prepare as migration
edb=migration.edb
OUT=migration.OUT
read=lambda path:json.loads(path.read_text())

def save(path,value):edb.atomic_json(path,value)

def check_preparation():
 plan=read(OUT/'plan.json');preview=read(OUT/'preview.json')
 assert preview['passed']and not preview['committed']and preview['captured_basis']==plan['basis']
 assert plan['counts']['questions']==1695 and len(plan['batches'])==9
 assert plan['source']==edb.SOURCE and plan['retained_original_entities']==10170
 assert migration.digest(OUT/'snapshot.edn')==plan['snapshot_sha256']
 for r in plan['review_files']:assert migration.digest(Path(r['path']))==r['sha256']
 prior=OUT/'superseded-preparations/basis-1694'
 if plan['basis']!=1694:
  assert read(prior/'snapshot.json')['questions']==read(OUT/'snapshot.json')['questions'],'Changed question facts require re-review'
  for b in plan['batches']:
   assert migration.digest(Path(b['directory'])/'transaction.edn')==migration.digest(prior/f"batch-{b['number']:02d}/transaction.edn")
  assert migration.digest(OUT/'optional-solution-repairs/transaction.edn')==migration.digest(prior/'optional-solution-repairs/transaction.edn')
 fixture=read(OUT/'engine-fixture-verification.json')
 assert fixture['passed']and migration.digest(OUT/'engine-input.json')==fixture['engine_input_sha256']and migration.digest(OUT/'engine-report.json')==fixture['engine_report_sha256']
 fixture.update({'prepared_basis':plan['basis'],'logical_forms_identical_to_previous':True,'source_facts_identical_to_previous':True})
 save(OUT/'engine-fixture-verification.json',fixture)
 assert read(OUT/'optional-solution-repairs/preview.json')['passed']
 assert read(OUT/'optional-solution-repairs/plan.json')['counts']['questions']==14
 return plan

def progress(plan,receipts,*,pending=None,solution_receipt=None):
 current=read(OUT/'status.json')
 current.update({'state':'committed_pending_readback'if solution_receipt else'conversions_committed_pending_solution_repairs'if len(receipts)==9 else'partially_committed','source':plan['source'],'database_writes':len(receipts)+bool(solution_receipt),'confirmed_conversions_in_this_tier':sum(r['counts']['questions']for r in receipts),'confirmed_batches':receipts,'pending_request':pending,'solution_receipt':solution_receipt,'retained_radio_ids':[17592186329885]})
 save(OUT/'status.json',current)
 ledger=read(OUT/'resolutions.json');done={q['id']:r for b,r in zip(plan['batches'],receipts)for q in read(Path(b['directory'])/'plan.json')['questions']}
 for q in ledger['questions']:
  if q['id']in done:q.update({'commit_status':'committed','commit_basis':done[q['id']]['basis_after'],'commit_request_key':done[q['id']]['request_key']})
  elif q['decision']=='retain_radio':q['commit_status']='not_planned_retained_radio'
  else:q['commit_status']='not_submitted'
 ledger['state']=current['state'];ledger['database_writes']=current['database_writes'];save(OUT/'resolutions.json',ledger)

def submit(directory,snapshot,*,number,solutions=False):
 manifest=read(directory/'plan.json');request=read(directory/'prepared-request.json');preview=read(directory/'preview.json');tx=directory/'transaction.edn'
 assert migration.digest(tx)==request['sha256']==manifest['transaction_sha256']==preview['sha256']
 assert preview['passed']and not preview['committed']and request['must_use_basis_guard']
 assert request['basis']==manifest['basis']==preview['basis']and request['source']==manifest['source']==edb.SOURCE
 assert request['database']==edb.DB.args.database and request['endpoint']==edb.DB.args.endpoint and request['lineage']==snapshot['lineage']
 intent_path=directory/'commit-intent.json';intent={**request,'state':'submission_requested'}
 if intent_path.exists():assert read(intent_path)==intent,'Recover original request; do not alter intent'
 else:save(intent_path,intent)
 # Retry only this complete saved request. Never refresh an unknown outcome.
 report=None
 for attempt in range(3):
  try:report=edb.DB._commit(intent,tx,directory);break
  except (subprocess.TimeoutExpired,ConnectionError):
   if attempt==2:raise
 assert report[':edb/committed']is True
 receipt={'committed':True,'batch':number,'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],'source':edb.SOURCE,'request_key':intent['request_key'],'transaction_sha256':intent['sha256'],'tx_hash':report.get(':edb/tx-hash'),'replayed':report.get(':edb/replayed'),'datoms':len(report[':edb/tx-data']),'counts':manifest['counts']}
 # Record success before any local verification or rendering that could fail.
 save(directory/'commit-receipt.json',receipt)
 migration.verify_report(directory,report,snapshot,committed=True,solution_repairs=solutions)
 print(json.dumps({'committed_and_validated':number,'basis_before':receipt['basis_before'],'basis_after':receipt['basis_after'],'questions':manifest['counts']['questions']}),flush=True)
 return receipt

def commit_chain():
 plan=check_preparation();snapshot=edb.loads((OUT/'snapshot.edn').read_text());status=edb.DB.command('status');assert 'lineage='+plan['lineage']in status
 root_path=OUT/'commit-intent.json';root={'state':'submission_authorized','basis':plan['basis'],'source':plan['source'],'batches':plan['batches'],'counts':plan['counts'],'include_solution_corrections':True}
 if root_path.exists():assert read(root_path)==root
 else:
  assert edb.DB.basis()==plan['basis'],'Database advanced before submission; refresh and preview unsubmitted work'
  save(root_path,root)
 edb.DB.args.capture_only=False
 receipts=[]
 try:
  for b in plan['batches']:
   request=read(Path(b['directory'])/'prepared-request.json')
   assert request['basis']==b['basis_guard']and request['request_key']==b['request_key']and request['sha256']==b['sha256']
   if receipts:assert receipts[-1]['basis_after']==request['basis']
   receipt=submit(Path(b['directory']),snapshot,number=b['number']);receipts.append(receipt);progress(plan,receipts)
  summary={'committed':True,'basis_before':plan['basis'],'basis_after':receipts[-1]['basis_after'],'source':plan['source'],'counts':plan['counts'],'batches':receipts}
  save(OUT/'commit-receipt.json',summary)
  directory=OUT/'optional-solution-repairs';assert read(directory/'plan.json')['basis']==summary['basis_after']
  solution_receipt=submit(directory,snapshot,number='solution-corrections',solutions=True)
  summary['basis_after_conversions']=summary['basis_after'];summary['basis_after']=solution_receipt['basis_after'];summary['solution_corrections']=solution_receipt;save(OUT/'commit-receipt.json',summary);progress(plan,receipts,solution_receipt=solution_receipt)
  print(json.dumps({'all_prepared_transactions_committed':True,'basis_before':plan['basis'],'basis_after':summary['basis_after'],'conversion_batches':len(receipts),'solution_corrections':14,'questions':1695}),flush=True)
 except Exception:
  progress(plan,receipts,pending='Inspect exact retained requests/receipts; no unknown request may be rebuilt.')
  raise
 finally:edb.DB.args.capture_only=True

def commit():
 from one_at_a_time import run
 run()
 verify()

def verify():
 plan=read(OUT/'plan.json');summary=read(OUT/'commit-receipt.json');snapshot=edb.loads((OUT/'snapshot.edn').read_text());basis=summary['basis_after']
 assert summary['committed']and len(summary['batches'])==9 and summary['solution_corrections']['committed']
 before={q[':db/id']:q for q, in snapshot['questions']};initial=dict(before);changes={};ids={};batch_snapshots=[]
 for b in plan['batches']:
  directory=Path(b['directory']);manifest=read(directory/'plan.json');report=edb.loads((directory/'commit.edn').read_text());assert report[':edb/committed']
  captured=edb.loads((directory/'snapshot.edn').read_text());batch_snapshots.append((directory,captured))
  migration.verify_report(directory,report,captured,committed=True)
  before.update({q[':db/id']:q for q, in captured['questions']})
  changes.update({q['id']:q for q in manifest['questions']});ids.update(report[':edb/tempids'])
 repair_manifest=read(OUT/'optional-solution-repairs/plan.json');solutions={q['id']:q['solution_after']for q in repair_manifest['questions']}
 migration.verify_report(OUT/'optional-solution-repairs',edb.loads((OUT/'optional-solution-repairs/commit.edn').read_text()),edb.loads((OUT/'optional-solution-repairs/snapshot.edn').read_text()),committed=True,solution_repairs=True)
 query='[:find (pull ?q '+edb.QUESTION+') :in $ [?q ...] :where [?q :question/id _]]'
 after={q[':db/id']:q for q, in edb.batches(query,sorted(before),'questions-after',basis,96)}
 assert set(after)==set(before)and len(changes)==1695
 original={};total_fields=0
 for qid,change in changes.items():
  old,current=before[qid],after[qid];exempt={':question/problem',':question/answer-fields',':question/worked-solution'}
  assert {k:v for k,v in old.items()if k not in exempt}=={k:v for k,v in current.items()if k not in exempt},('Unrelated question content changed',qid)
  assert current[':question/worked-solution']==solutions.get(qid,old[':question/worked-solution'])
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
 assert total_fields==5178 and len(original)==10170
 retained_q=17592186329885;assert after[retained_q]==before[retained_q]
 pattern='''[* {:answer/type [:db/id :db/ident]} {:answer-field/type [:db/id :db/ident]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]'''
 retained={q[':db/id']:q for q, in edb.batches('[:find (pull ?e '+pattern+') :in $ [?e ...] :where (or [?e :answer/id _] [?e :answer-field/id _])]',sorted(original),'originals-after',basis,128)}
 assert retained==original,'Original field/answer entities changed or disappeared'
 historical={q[':db/id']:q for q, in edb.batches(query,sorted(initial),'questions-historical',plan['basis'],128)};assert historical==initial
 for directory,captured in batch_snapshots:
  scoped={q[':db/id']:q for q, in captured['questions']}
  historical={q[':db/id']:q for q, in edb.batches(query,sorted(scoped),'questions-historical-'+directory.name,captured['basis'],128)}
  assert historical==scoped
 items=edb.batches('[:find ?q (pull ?item '+edb.ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',sorted(changes),'items-after',basis,128)
 old_items={i[':db/id']:(qid,i)for _,captured in batch_snapshots for qid,i in captured['items']};new_items={i[':db/id']:(qid,i)for qid,i in items};assert set(new_items)==set(old_items)
 mapped={r['item']:r for b in plan['batches']for r in read(Path(b['directory'])/'plan.json')['responses']}
 for itemid,(qid,old)in old_items.items():
  current_qid,current=new_items[itemid];assert current_qid==qid
  if itemid not in mapped:assert current==old
  else:
   assert {k:v for k,v in current.items()if k!=':task-item/responses'}=={k:v for k,v in old.items()if k!=':task-item/responses'}
   assert {a[':db/id']for a in current[':task-item/responses']}=={ids[t]for t in mapped[itemid]['new_answer_tempids']}
 result={'passed':True,'committed':True,'basis_before':summary['basis_before'],'basis_after_conversions':summary['basis_after_conversions'],'basis_after':basis,'source':plan['source'],'counts':plan['counts'],'solution_corrections':len(solutions),'retained_original_entities':len(original),'retained_radio_ids':[retained_q],'mode':summary['mode'],'checks':['Every converted question and owned Boolean answer bank read back at the confirmed final basis.','Correct subsets and all prompts match the prepared plans.','Only the fourteen reviewed worked solutions changed; difficulty and KP membership preserved.','All original field/answer entities and the retained ordered radio unchanged.','Original historical question snapshot and every independently captured batch snapshot reproduced.','Learner presentations and mapped responses preserved.','Each receipt matches exact logical forms, guarded basis, identity allocations and every datom source.']}
 save(OUT/'verification.json',result)
 status=read(OUT/'status.json');status.update({'state':'committed_verified','verification':'verification.json','basis_before':summary['basis_before'],'basis_after':basis,'confirmed_conversions_in_this_tier':1695,'database_writes':10,'solution_corrections_committed':14,'pending_request':None,'execution_mode':summary['mode']});save(OUT/'status.json',status)
 ledger=read(OUT/'resolutions.json');ledger['state']='committed_verified';ledger['database_writes']=10
 for q in ledger['questions']:
  q['verification_status']='passed_at_basis_'+str(basis)
  if q['id']in solutions:q['solution_repair_status']='committed_verified'
 save(OUT/'resolutions.json',ledger)
 print(json.dumps({'final_readback_verified':True,'basis_after':basis,'questions':len(changes),'checkbox_fields':total_fields,'retained_original_entities':len(original),'solution_corrections':len(solutions),'retained_radio':retained_q}),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['commit','verify']);globals()[parser.parse_args().action]()

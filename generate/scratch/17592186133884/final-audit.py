"""Reconcile conservative source exclusions against the exact successful receipt.
No new transaction: recover the saved request, recheck basis under api.lock, and
verify the committed content with the final complete-value source audit.
"""
import fcntl,json
from pathlib import Path
import replenish as r

def main():
 validation=json.loads((r.HERE/'validation.json').read_text());assert validation['passed'] and validation['generator_sha256']==r.sha(r.HERE.with_suffix('.py'))
 path=r.OUT/'basis-2677';intent=json.loads((path/'commit-intent.json').read_text())
 assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==r.sha(path/'transaction.edn')
 with r.LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  assert 'lineage='+r.LINEAGE in r.DB.command('status')
  current=r.inventory(path/'final-audit-current-inventory.json');assert r.DB.basis()==current['basis']
  kp=r.read_kp(path/'preparation-audit-read',intent['basis'])
  counts=r.counts(kp,intent['basis'],path/'preparation-audit-counts')
  prep=json.loads((path/'preparation.json').read_text());original=path/'preparation-original.json'
  if not original.exists():r.atomic_text(original,(path/'preparation.json').read_text())
  old=prep['available_counts'];prep['available_counts']=counts
  prep['postcommit_source_value_audit']={'reason':'Complete integral value checks identify equivalent source answers/distractors. Original source records remain untouched. No effect on needed new questions: moderate 0, hard 4.','original_preparation':'preparation-original.json','old_validated_counts':old['distinct_available'],'corrected_counts':counts['distinct_available'],'audit':'generate/scratch/17592186133884/source-value-audit.json','audited_at_current_basis':current['basis'],'evaluated_preparation_basis':intent['basis']}
  r.save(path/'preparation.json',prep)
  verify_original=path/'verification-original.json'
  if not verify_original.exists():r.atomic_text(verify_original,(path/'verification.json').read_text())
  receipt=r.DB._commit(intent,path/'transaction.edn',path)
  assert receipt[':edb/committed'] and receipt[':edb/db-after-t']==2678
  verified=r.verify(path,intent,receipt)
  verified['final_source_audit']='generate/scratch/17592186133884/source-value-audit.json';verified['new_durable_transactions_in_final_audit']=0
  r.save(path/'verification.json',verified)
  inv=r.inventory(path/'inventory-after.json');r.finish(path,intent,verified,inv)
if __name__=='__main__':main()

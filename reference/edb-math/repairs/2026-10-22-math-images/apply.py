"""Submit the user-authorized exact CAS request, journal it, and verify db-after."""
import collections,hashlib,json,os,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection,kw,loads,dumps
SOURCE=':agent/codex';ENDPOINT='/tmp/edb-math/writer.sock'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def read(db,basis,name):
 result=db.command('query','--as-of',basis,'--file',HERE/'read-query.edn','--inputs',HERE/'read-inputs.edn','--max-value-bytes','2147483648','--max-join-bytes','536870912');(HERE/name).write_text(result);return {(e,str(a).removeprefix(':')):v for e,a,v in loads(result)}
def main():
 assert sys.argv[1:]==['--apply-user-authorized']
 fields=json.loads((HERE/'fields.json').read_text());expected={(f['entity'],f['attribute']):f['after'] for f in fields};before={(f['entity'],f['attribute']):f['before'] for f in fields}
 render=json.loads((HERE/'field-render-verification.json').read_text());assert render['fields']==len(fields) and not render['failures'] and not render['page_errors'];assert render['new_math_expressions']==6919
 checks={(r['entity'],r['attribute']):r for r in render['records']}
 for f in fields:assert checks[f['entity'],f['attribute']]['after_sha256']==f['after_sha256']==hashlib.sha256(f['after'].encode()).hexdigest()
 assert json.loads((HERE/'remaining-assets.json').read_text())==[]
 forms=loads((HERE/'transaction.edn').read_text());assert len(forms)==len(fields)
 assert all(str(form[0])==':db/cas' and form[3]==before[form[1],str(form[2])[1:]] and form[4]==expected[form[1],str(form[2])[1:]] for form in forms)
 preview=loads((HERE/'preview.edn').read_text());assert preview[':edb/committed'] is False and preview[':edb/speculative'] is True;assert len(preview[':edb/tx-data'])==2*len(fields)+1
 assert collections.Counter((d[0],d[2],d[-1]) for d in preview[':edb/tx-data'] if d[0] in {e for e,a in expected})==collections.Counter([(e,v,True) for (e,a),v in expected.items()]+[(e,v,False) for (e,a),v in before.items()])
 preparation=json.loads((HERE/'preparation.json').read_text());sha=digest(HERE/'transaction.edn');assert sha==preparation['transaction_sha256']
 db=connection();intent_path=HERE/'commit-intent.json';started=HERE/'submission-started.json'
 if intent_path.exists():
  intent=json.loads(intent_path.read_text());assert intent['sha256']==sha and intent['source']==SOURCE and intent['endpoint']==ENDPOINT
 else:
  intent={'database':'math','source':SOURCE,'endpoint':ENDPOINT,'file':str(HERE/'transaction.edn'),'sha256':sha,'request_key':'repair-math-images-2026-10-22-'+sha[:24],'entities':preparation['entities'],'fields':len(fields),'created_at':datetime.now(timezone.utc).isoformat(),'user_authorization':"use $edb to prepare a transaction repair to fix all of those and then push it to the database. Don't wait for me."};save('commit-intent.json',intent)
 receipt_path=HERE/'receipt.edn';receipt=loads(receipt_path.read_text()) if receipt_path.exists() and receipt_path.stat().st_size else {}
 if not receipt.get(':edb/committed'):
  if not started.exists():
   basis=db.basis();actual=read(db,basis,'preapply.edn');conflicts=[{'entity':e,'attribute':a,'expected_before_sha256':hashlib.sha256(v.encode()).hexdigest(),'actual':actual.get((e,a))} for (e,a),v in before.items() if actual.get((e,a))!=v]
   save('preapply-check.json',{'basis':basis,'fields':len(actual),'conflicts':conflicts});assert not conflicts,'Concurrent edits; transaction not submitted'
   save('submission-started.json',{'request_key':intent['request_key'],'sha256':sha,'at':datetime.now(timezone.utc).isoformat()})
  # If a prior submission lost its reply, this is the exact same key and intent.
  command=[db.args.edb_bin,'transact','--database','math','--source',SOURCE,'--file',intent['file'],'--endpoint',ENDPOINT,'--request-key',intent['request_key'],'--timeout-ms','120000']
  with receipt_path.open('w') as out,(HERE/'submit.stderr').open('w') as err:
   result=subprocess.run(command,env=db.env,stdout=out,stderr=err,text=True,timeout=160)
  assert receipt_path.stat().st_size,('Outcome not confirmed; retain and retry the same request',result.returncode)
  receipt=loads(receipt_path.read_text());assert receipt[':edb/committed'],receipt
 basis=receipt[':edb/db-after-t'];actual=read(db,basis,'after.edn');assert actual==expected,'Committed values differ from the exact request'
 datoms=receipt[':edb/tx-data'];assert len(datoms)==2*len(fields)+1
 target_entities={e for e,a in expected};unexpected=[d for d in datoms if d[0] not in target_entities and d[1]!=50];assert not unexpected,unexpected
 assert len([d for d in datoms if d[-1] and d[0] in target_entities])==len(fields)
 protected_images={edit['asset'] for f in fields for edit in f['edits']};remaining=[(e,a,p) for (e,a),v in actual.items() for p in re.findall(r'images/[0-9a-f]{2}/[0-9a-f]{64}\.(?:svg|png)',v) if p in protected_images];assert not remaining
 report={'committed':True,'basis':basis,'request_key':intent['request_key'],'source':SOURCE,'transaction_sha256':sha,'verified_fields':len(actual),'entities':len(target_entities),'replaced_formula_image_occurrences':sum(len(f['edits']) for f in fields),'distinct_formula_assets':len(protected_images),'genuine_image_references_preserved':preparation['preserved_genuine_image_references'],'exact_readback_matches':True,'remaining_audited_formula_image_references':0,'tx_data_count':len(datoms),'only_content_cas_and_transaction_metadata_changed':True}
 save('verification.json',report);print(json.dumps(report))
if __name__=='__main__':main()

"""Commit exact source-backed presentation-only CAS batches under persisted request identities."""
import collections,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/html-table-repair';sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,loads
SOURCE=':agent/codex';SOURCE_ID=17592186576411;ENDPOINT='/tmp/edb-math/writer.sock'
def save(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(db,folder,basis,name):
 text=db.command('query','--as-of',basis,'--file',folder/'read-query.edn','--inputs',folder/'read-inputs.edn','--max-value-bytes','2147483648','--max-join-bytes','536870912');(folder/name).write_text(text);return {(e,str(a)[1:]):v for e,a,v in loads(text)}
def receipt(path):
 try:r=loads(path.read_text())
 except (FileNotFoundError,ValueError,IndexError):return None
 return r if isinstance(r,dict)and r.get(':edb/committed')is True else None
def main():
 assert sys.argv[1:]==['--apply-user-authorized'];fields=json.loads((H/'fields.json').read_text());batches=json.loads((H/'batches.json').read_text());prep=json.loads((H/'preparation.json').read_text());bykey={(f['entity'],f['attribute']):f for f in fields}
 assert prep['all_current_cell_bytes_preserved']and prep['field_markers_preserved']and prep['answer_value_changes_only_id_graded_choices']
 render=json.loads((H/'render-verification.json').read_text());assert render['passed']and render['fields']==len(fields);checked={(r[0],r[1]):r[2:]for r in render['verified_hashes']};assert all(checked[k]==[f['before_sha256'],f['after_sha256']]for k,f in bykey.items())
 grading=json.loads((H/'grading-verification.json').read_text());assert grading['database_writes']==0 and grading['accepted_checks']>0 and grading['rejected_checks']>0 and grading['documented_unresolved_checks']>=0
 assert json.loads((H/'importer-verification.json').read_text())['passed']
 assert json.loads((H/'layout-verification.json').read_text())['passed']
 idents={v:int(k)for k,v in json.loads((W/'idents.json').read_text()).items()};states={}
 for b in batches:
  folder=H/b['name'];assert sha(folder/'transaction.edn')==b['sha256'];p=json.loads((folder/'preview-check.json').read_text());assert p['sha256']==b['sha256']and p['native_validation_passed']and p['exact_proposed_values_verified']and not p['committed']
  for s in p['field_validity']:
   assert s['valid_before']==s['valid_after']and s['preexisting_missing_correct']==(not s['valid_before']);states[s['field']]=s
  cas=[f for f in loads((folder/'transaction.edn').read_text())if isinstance(f,list)and str(f[0])==':db/cas'];assert len(cas)==b['fields']
  for f in cas:
   k=f[1],str(f[2])[1:];assert k in bykey and f[3]==bykey[k]['before']and f[4]==bykey[k]['after']
 assert len(states)==prep['answer_fields']
 db=connection();preflight=H/'preapply-check.json';hashes={b['name']:b['sha256']for b in batches}
 if not preflight.exists():
  basis=db.basis();conflicts=[]
  for b in batches:
   current=read(db,H/b['name'],basis,'preapply.edn')
   conflicts.extend({'entity':k[0],'attribute':k[1]}for k in map(tuple,b['field_keys'])if current.get(k)!=bykey[k]['before'])
  save(preflight,{'basis':basis,'fields':len(fields),'conflicts':conflicts,'payloads':hashes})
 p=json.loads(preflight.read_text());assert p['payloads']==hashes and not p['conflicts'],'Concurrent content changes require reviewed rebasing before submission'
 outcomes=[]
 for b in batches:
  folder=H/b['name'];intent={'database':'math','source':SOURCE,'endpoint':ENDPOINT,'file':str(folder/'transaction.edn'),'sha256':b['sha256'],'request_key':'repair-html-table-fidelity-2026-10-24-'+b['name']+'-'+b['sha256'][:20]};ip=folder/'commit-intent.json'
  if ip.exists():assert json.loads(ip.read_text())==intent
  else:save(ip,intent)
  path=folder/'receipt.edn';report=receipt(path)
  if not report:
   save(folder/'submission-started.json',{'at':datetime.now(timezone.utc).isoformat(),'request_key':intent['request_key'],'sha256':intent['sha256'],'authorization':'Go ahead and fix the source-table import/display problem throughout the database; do not wait.'})
   command=[db.args.edb_bin,'transact','--database','math','--source',SOURCE,'--file',intent['file'],'--endpoint',ENDPOINT,'--request-key',intent['request_key'],'--timeout-ms','120000']
   for attempt in range(2):
    if path.exists():path.replace(folder/f'receipt-before-retry-{attempt}.edn')
    try:
     with path.open('w')as out,(folder/f'submit-{attempt}.stderr').open('w')as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,text=True,timeout=160)
    except subprocess.TimeoutExpired:pass
    report=receipt(path)
    if report:break
    stderr=(folder/f'submit-{attempt}.stderr').read_text()
    if any(s in stderr for s in ['cas-failed','request-key-conflict','type-mismatch','transaction/rejected','entity-predicate']):raise RuntimeError('Confirmed rejection '+b['name']+': '+stderr)
   assert report,'Unknown outcome: preserve payload and reconcile this exact request key'
  basis=report[':edb/db-after-t'];expected={tuple(k):bykey[tuple(k)]['after']for k in b['field_keys']};assert read(db,folder,basis,'after.edn')==expected
  data=report[':edb/tx-data'];assert len(data)==b['fields']*2+1 and all(d[4]==SOURCE_ID for d in data)
  wanted=collections.Counter((e,idents[':'+a],bykey[e,a][side],added)for e,a in expected for side,added in [('before',False),('after',True)]);assert collections.Counter((d[0],d[1],d[2],d[5])for d in data if d[1]!=idents[':db/txInstant'])==wanted
  outcomes.append({'batch':b['name'],'basis':basis,'fields':b['fields'],'sha256':b['sha256'],'request_key':intent['request_key'],'committed':True,'exact_readback_matches':True,'only_intended_datoms':True});save(H/'commit-progress.json',outcomes);print('Committed and verified',b['name'],'T'+str(basis),flush=True)
 final=outcomes[-1]['basis']
 for b in batches:assert read(db,H/b['name'],final,'final-basis.edn')=={tuple(k):bykey[tuple(k)]['after']for k in b['field_keys']}
 result={'database':'math','source':SOURCE,'first_commit_basis':outcomes[0]['basis'],'final_commit_basis':final,'batches':len(batches),'fields':len(fields),'entities':prep['entities'],'table_locations':prep['tables'],'all_batches_committed':True,'exact_readback_at_final_basis':True,'only_reviewed_presentation_cas_and_transaction_metadata_changed':True,'preexisting_missing_correct_links_preserved':sum(not state['valid_before']for state in states.values()),'outcomes':outcomes};save(H/'verification.json',result);print(json.dumps({k:v for k,v in result.items()if k!='outcomes'}))
if __name__=='__main__':main()

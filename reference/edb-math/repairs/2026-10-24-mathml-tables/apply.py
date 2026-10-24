"""Submit the user's authorized repair with exact payloads and durable receipts."""
import collections,hashlib,json,subprocess,sys,uuid
from datetime import datetime,timezone
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads
SOURCE=':agent/codex';SOURCE_ID=17592186576411;ENDPOINT='/tmp/edb-math/writer.sock'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def read(db,folder,basis,name):
 text=db.command('query','--as-of',basis,'--file',folder/'read-query.edn','--inputs',folder/'read-inputs.edn','--max-value-bytes','2147483648','--max-join-bytes','536870912');(folder/name).write_text(text)
 return {(e,str(a)[1:]):v for e,a,v in loads(text)}
def receipt(path):
 try:r=loads(path.read_text())
 except (FileNotFoundError,ValueError,IndexError):return None
 return r if isinstance(r,dict) and r.get(':edb/committed') is True else None
def extra_read(db,basis,name,extra):
 rows=db.query('[:find (pull ?a [* {:answer/type [:db/ident]}]) (pull ?f [:db/id {:answer-field/choices [:db/id :answer/id]} {:answer-field/correct [:db/id :answer/id]}]) :in $ ?u ?f :where [?a :answer/id ?u]]',[uuid.UUID(extra['answer_uuid']),extra['field_entity']],H,name,basis)
 assert len(rows)==1
 a,f=rows[0];assert str(a[':answer/id'])==extra['answer_uuid'] and a[':answer/value']==extra['value'] and str(a[':answer/type'][':db/ident'])==extra['type']
 assert f[':answer-field/correct'][':db/id']==extra['correct_answer_entity_unchanged']
 assert a[':db/id'] in {c[':db/id'] for c in f[':answer-field/choices']} and len(f[':answer-field/choices'])==5
 return a[':db/id']
def main():
 assert sys.argv[1:]==['--apply-user-authorized']
 batches=json.loads((H/'batches.json').read_text());fields=json.loads((H/'fields.json').read_text());bykey={(f['entity'],f['attribute']):f for f in fields}
 render=json.loads((H/'render-verification.json').read_text());assert render['passed'] and render['fields']==len(fields)
 checked={(r[0],r[1]):r[2:] for r in render['verified_hashes']};assert all(checked[k]==[f['before_sha256'],f['after_sha256']] for k,f in bykey.items())
 prep=json.loads((H/'preparation.json').read_text());assert prep['all_cell_bytes_preserved']
 grading=json.loads((H/'grading-verification.json').read_text());assert grading['database_writes']==0 and not grading['documented_unresolved_checks']
 assert json.loads((H/'importer-verification.json').read_text())['passed']
 extra=json.loads((H/'restored-choice.json').read_text())
 idents={r['v']:r['e'] for line in (R/'.local/edb/mathml-tables-work/field-types.jsonl').read_text().splitlines() if (r:=json.loads(line))['a']=='db/ident'}
 for b in batches:
  folder=H/b['name'];assert sha(folder/'transaction.edn')==b['sha256']
  proof=json.loads((folder/'preview-check.json').read_text());assert proof['sha256']==b['sha256'] and proof['native_validation_passed'] and proof['exact_proposed_values_verified'] and not proof['committed']
  forms=loads((folder/'transaction.edn').read_text());cas=[f for f in forms if isinstance(f,list) and str(f[0])==':db/cas'];assert len(cas)==b['fields']
  assert all((f[1],str(f[2])[1:]) in bykey and f[3]==bykey[f[1],str(f[2])[1:]]['before'] and f[4]==bykey[f[1],str(f[2])[1:]]['after'] for f in cas)
 db=connection();preflight=H/'preapply-check.json'
 if not preflight.exists():
  basis=db.basis();conflicts=[]
  for b in batches:
   current=read(db,H/b['name'],basis,'preapply.edn')
   for pair in b['field_keys']:
    k=tuple(pair)
    if current.get(k)!=bykey[k]['before']:conflicts.append({'entity':k[0],'attribute':k[1],'actual_sha256':hashlib.sha256(current[k].encode()).hexdigest() if k in current else None})
  save(preflight,{'basis':basis,'fields':len(fields),'conflicts':conflicts,'payloads':{b['name']:b['sha256'] for b in batches}})
 else:
  p=json.loads(preflight.read_text());assert p['payloads']=={b['name']:b['sha256'] for b in batches};conflicts=p['conflicts']
 assert not conflicts,'Concurrent content edits require reviewed rebasing before submission'
 outcomes=[]
 for b in batches:
  folder=H/b['name'];intent={'database':'math','source':SOURCE,'endpoint':ENDPOINT,'file':str(folder/'transaction.edn'),'sha256':b['sha256'],'request_key':'repair-mathml-tables-2026-10-24-'+b['name']+'-'+b['sha256'][:20]}
  intent_path=folder/'commit-intent.json'
  if intent_path.exists():assert json.loads(intent_path.read_text())==intent
  else:save(intent_path,intent)
  path=folder/'receipt.edn';report=receipt(path)
  if not report:
   save(folder/'submission-started.json',{'request_key':intent['request_key'],'sha256':intent['sha256'],'at':datetime.now(timezone.utc).isoformat(),'authorization':'Use the root cause to locate all instances across the database, prepare a repair transaction, and push it. Do not wait.'})
   command=[db.args.edb_bin,'transact','--database','math','--source',SOURCE,'--file',intent['file'],'--endpoint',ENDPOINT,'--request-key',intent['request_key'],'--timeout-ms','120000']
   for attempt in range(2):
    if path.exists():path.replace(folder/f'receipt-before-retry-{attempt}.edn')
    try:
     with path.open('w') as out,(folder/f'submit-{attempt}.stderr').open('w') as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,text=True,timeout=160)
    except subprocess.TimeoutExpired:pass
    report=receipt(path)
    if report:break
    stderr=(folder/f'submit-{attempt}.stderr').read_text()
    if any(s in stderr for s in ['cas-failed','request-key-conflict','type-mismatch','transaction/rejected']):raise RuntimeError('Confirmed rejection '+b['name']+': '+stderr)
   assert report,'Unknown outcome: preserve and reconcile the identical request'
  basis=report[':edb/db-after-t'];expected={tuple(k):bykey[tuple(k)]['after'] for k in b['field_keys']};assert read(db,folder,basis,'after.edn')==expected
  datoms=report[':edb/tx-data'];assert all(d[4]==SOURCE_ID for d in datoms)
  wanted=collections.Counter((e,idents[':'+a],bykey[e,a][side],added) for e,a in expected for side,added in [('before',False),('after',True)])
  if b['restores_choice']:
   new_id=extra_read(db,basis,'restored-choice-after',extra)
   wanted.update([(new_id,idents[':answer/id'],uuid.UUID(extra['answer_uuid']),True),(new_id,idents[':answer/type'],idents[extra['type']],True),(new_id,idents[':answer/value'],extra['value'],True),(extra['field_entity'],idents[':answer-field/choices'],new_id,True)])
  actual=collections.Counter((d[0],d[1],d[2],d[5]) for d in datoms if d[1]!=idents[':db/txInstant'])
  assert actual==wanted,'Unexpected committed datoms in '+b['name']
  assert len(datoms)==sum(wanted.values())+1
  outcomes.append({'batch':b['name'],'basis':basis,'fields':b['fields'],'request_key':intent['request_key'],'sha256':b['sha256'],'committed':True,'exact_readback_matches':True,'only_intended_datoms':True});save(H/'commit-progress.json',outcomes);print('Committed and verified',b['name'],'T'+str(basis),flush=True)
 final=outcomes[-1]['basis']
 for b in batches:assert read(db,H/b['name'],final,'final-basis.edn')=={tuple(k):bykey[tuple(k)]['after'] for k in b['field_keys']}
 extra_read(db,final,'restored-choice-final',extra)
 result={'database':'math','source':SOURCE,'first_commit_basis':outcomes[0]['basis'],'final_commit_basis':final,'batches':len(batches),'fields':len(fields),'entities':prep['entities'],'table_edits':prep['table_edits'],'restored_choices':1,'all_batches_committed':True,'exact_readback_at_final_basis':True,'only_content_cas_restored_choice_and_transaction_metadata_changed':True,'outcomes':outcomes}
 save(H/'verification.json',result);print(json.dumps({k:v for k,v in result.items() if k!='outcomes'}))
if __name__=='__main__':main()

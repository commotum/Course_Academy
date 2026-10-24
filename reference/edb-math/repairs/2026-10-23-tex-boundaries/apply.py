"""Commit user-authorized exact CAS batches, reconcile retries, verify db-after."""
import collections,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'));from migrate_learner_history import connection,kw,loads
SOURCE=':agent/codex';ENDPOINT='/tmp/edb-math/writer.sock'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def read(db,folder,basis,name):
 text=db.command('query','--as-of',basis,'--file',folder/'read-query.edn','--inputs',folder/'read-inputs.edn','--max-value-bytes','2147483648','--max-join-bytes','536870912');(folder/name).write_text(text);return {(e,str(a)[1:]):v for e,a,v in loads(text)}
def committed(path):
 try:r=loads(path.read_text())
 except (FileNotFoundError,ValueError,IndexError):return None
 return r if isinstance(r,dict) and r.get(':edb/committed') is True else None

def main():
 fidelity=json.loads((HERE/'fidelity-verification.json').read_text());assert not fidelity['unexpected_changes']
 processes=json.loads((HERE/'process-verification.json').read_text());assert processes['historical_html_import_verified'] and processes['current_capture_import_verified'] and processes['shared_publication_normalizes_before_identity']
 assert sys.argv[1:]==['--apply-user-authorized'];batches=json.loads((HERE/'batches.json').read_text());fields=json.loads((HERE/'fields.json').read_text());bykey={(f['entity'],f['attribute']):f for f in fields};render=json.loads((HERE/'render-verification.json').read_text());prep=json.loads((HERE/'preparation.json').read_text());assert not render['failed_fields'] and not render['page_errors'] and render['fields']==len(fields)
 checked={(r[0],r[1]):r[2:] for r in render['verified_field_hashes']}
 assert all(checked[f['entity'],f['attribute']]==[f['before_sha256'],f['after_sha256']] for f in fields)
 allowed={'question/problem','question/worked-solution','tutorial/content','multistep/context','answer/feedback','answer-field/feedback','assigned-problem/instructions'}
 for b in batches:
  folder=HERE/b['name'];assert sha(folder/'transaction.edn')==b['sha256'];p=json.loads((folder/'preview-check.json').read_text());assert p['sha256']==b['sha256'] and p['exact_content_diff_verified'] and not p['committed']
  forms=loads((folder/'transaction.edn').read_text());assert len(forms)==b['fields']
  for form in forms:
   assert str(form[0])==':db/cas';key=form[1],str(form[2])[1:];assert key[1] in allowed and form[3]==bykey[key]['before'] and form[4]==bykey[key]['after']
 db=connection();preflight=HERE/'preapply-check.json'
 if not preflight.exists():
  basis=db.basis();conflicts=[]
  for b in batches:
   actual=read(db,HERE/b['name'],basis,'preapply.edn')
   for pair in b['field_keys']:
    key=tuple(pair);f=bykey[key]
    if actual.get(key)!=f['before']:conflicts.append({'entity':key[0],'attribute':key[1],'expected':f['before_sha256'],'actual':hashlib.sha256(actual[key].encode()).hexdigest() if key in actual else None})
  save(preflight,{'basis':basis,'fields':len(fields),'conflicts':conflicts,'payloads':{b['name']:b['sha256'] for b in batches}});assert not conflicts,'Concurrent edits; no new request submitted'
 else:
  p=json.loads(preflight.read_text());assert not p['conflicts'] and p['payloads']=={b['name']:b['sha256'] for b in batches}
 outcomes=[]
 for b in batches:
  folder=HERE/b['name'];intent_path=folder/'commit-intent.json';intent={'database':'math','source':SOURCE,'endpoint':ENDPOINT,'file':str(folder/'transaction.edn'),'sha256':b['sha256'],'request_key':'repair-tex-boundaries-2026-10-23-'+b['name']+'-'+b['sha256'][:20]}
  if intent_path.exists():assert json.loads(intent_path.read_text())==intent
  else:save(intent_path,intent)
  receipt_path=folder/'receipt.edn';receipt=committed(receipt_path)
  if not receipt:
   save(folder/'submission-started.json',{'request_key':intent['request_key'],'sha256':intent['sha256'],'at':datetime.now(timezone.utc).isoformat(),'authorization':"Find related TeX causes throughout the database, prepare the repair transaction and push it; also prepare external processes, generators and importers."})
   command=[db.args.edb_bin,'transact','--database','math','--source',SOURCE,'--file',intent['file'],'--endpoint',ENDPOINT,'--request-key',intent['request_key'],'--timeout-ms','120000']
   for attempt in range(2):
    if receipt_path.exists():receipt_path.replace(folder/f'receipt-before-retry-{attempt}.edn')
    try:
     with receipt_path.open('w') as out,(folder/f'submit-{attempt}.stderr').open('w') as err:result=subprocess.run(command,env=db.env,stdout=out,stderr=err,text=True,timeout=160)
    except subprocess.TimeoutExpired:result=None
    receipt=committed(receipt_path)
    if receipt:break
    stderr=(folder/f'submit-{attempt}.stderr').read_text()
    if any(s in stderr for s in ('cas-failed','request-key-conflict','type-mismatch','transaction/rejected')):raise RuntimeError('Confirmed rejection in '+b['name']+': '+stderr)
   assert receipt,'Unconfirmed outcome: preserve payload and reconcile the same request key'
  basis=receipt[':edb/db-after-t'];expected={tuple(k):bykey[tuple(k)]['after'] for k in b['field_keys']};actual=read(db,folder,basis,'after.edn');assert actual==expected,'Exact committed values differ in '+b['name']
  datoms=receipt[':edb/tx-data'];assert len(datoms)==2*b['fields']+1
  wanted=collections.Counter([(e,bykey[e,a]['before'],False) for e,a in expected]+[(e,v,True) for (e,a),v in expected.items()]);ids={e for e,a in expected};assert collections.Counter((d[0],d[2],d[-1]) for d in datoms if d[0] in ids)==wanted
  outcomes.append({'batch':b['name'],'basis':basis,'fields':b['fields'],'request_key':intent['request_key'],'sha256':b['sha256'],'committed':True,'exact_readback_matches':True});save(HERE/'commit-progress.json',outcomes);print('Committed and verified',b['name'],'T'+str(basis),flush=True)
 final_basis=outcomes[-1]['basis']
 for b in batches:
  actual=read(db,HERE/b['name'],final_basis,'final-basis.edn');assert actual=={tuple(k):bykey[tuple(k)]['after'] for k in b['field_keys']}
 report={'database':'math','source':SOURCE,'first_commit_basis':outcomes[0]['basis'],'final_commit_basis':final_basis,'batches':len(outcomes),'fields':len(fields),'entities':len({f['entity'] for f in fields}),'actions':prep['actions'],'all_batches_committed':True,'exact_readback_at_final_basis':True,'only_content_cas_and_transaction_metadata_changed':True,'outcomes':outcomes};save(HERE/'verification.json',report);print(json.dumps({k:v for k,v in report.items() if k!='outcomes'}))
if __name__=='__main__':main()

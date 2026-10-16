"""Apply only the exact user-authorized prepared transaction and verify db-after."""
import hashlib,json,os,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'))
from edn import loads,dumps
assert sys.argv[1:]==['--apply-user-authorized'],'Requires the user-authorized apply invocation'
intent=json.loads((H/'commit-intent.json').read_text());ready=json.loads((H/'readiness.json').read_text())
for name,digest in ready['files'].items():assert hashlib.sha256((H/name).read_bytes()).hexdigest()==digest,(name,'reviewed evidence changed')
assert hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest()==intent['sha256']==ready['transaction_sha256']
for file in ['rendering-validation.json','mobile-rendering-validation.json']:
 v=json.loads((H/file).read_text());assert not v['page_errors'];assert all(not x['errors'] and not x['exposed'] and not x['missingMatrices'] and not x['cardOverflow'] for x in v['records'])
B='/home/jake/Developer/EDB/target/release/edb';E={**os.environ,'EDB_POSTGRES_URL':'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
def cli(*args):return subprocess.check_output([B,*args],env=E,text=True,timeout=160)
def save(name,x):(H/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
forms=loads((H/'transaction.edn').read_text());expected={(f[1],f[2]):f[4] for f in forms};old={(f[1],f[2]):f[3] for f in forms}
receipt=H/'receipt.edn';saved=loads(receipt.read_text()) if receipt.exists() and receipt.stat().st_size else {}
if not receipt.exists():
 basis=int(re.search(r'basis_t=(\d+)',cli('status','--database','math'))[1]);text=cli('query','--database','math','--as-of',str(basis),'--file',str(H/'read-query.edn'),'--inputs',str(H/'read-inputs.edn'),'--max-value-bytes','2147483648');(H/'preapply.edn').write_text(text)
 actual={(e,a):v for e,a,v in loads(text)}
 conflicts=[{'entity':e,'attribute':str(a),'prepared_before':old[e,a],'current':actual.get((e,a)),'prepared_after':expected[e,a]} for e,a in old if actual.get((e,a))!=old[e,a]]
 save('preapply-check.json',{'basis':basis,'fields':len(old),'conflicts':conflicts})
 assert not conflicts,'Concurrent changes found; exact prepared transaction has not been submitted'
 with (H/'preapply-preview.edn').open('w') as output:subprocess.run([B,'with','--database','math','--source',intent['source'],'--file',intent['file']],env=E,stdout=output,check=True,timeout=160)
assert loads((H/'preapply-preview.edn').read_text())[':edb/committed'] is False
save('authorization.json',{'user_instruction':'Go ahead and push the prepared transaction and then dig into the other stuff more and tell me about it.','authorized_scope':'Exact prepared visual repair only','request_key':intent['request_key'],'transaction_sha256':intent['sha256']})
if not saved.get(':edb/committed'):
 with receipt.open('w') as output:
  subprocess.run([B,'transact','--database',intent['database'],'--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000'],env=E,stdout=output,timeout=160)
assert receipt.stat().st_size,'Outcome not confirmed: retain exact payload and request key'
saved=loads(receipt.read_text());assert saved[':edb/committed'],saved
basis=saved.get(':edb/db-after-t',saved.get(':edb/basis-t'));assert basis
text=cli('query','--database','math','--as-of',str(basis),'--file',str(H/'read-query.edn'),'--inputs',str(H/'read-inputs.edn'),'--max-value-bytes','2147483648');(H/'after.edn').write_text(text)
actual={(e,a):v for e,a,v in loads(text)};assert actual==expected,'Exact committed values differ'
report={'committed':True,'basis':basis,'verified_fields':len(actual),'entities':intent['entities'],'request_key':intent['request_key'],'exact_readback_matches':True}
save('verification.json',report);print(json.dumps(report))

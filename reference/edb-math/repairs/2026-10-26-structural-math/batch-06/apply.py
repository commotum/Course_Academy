"""Commit only the exact reviewed payload; recover a saved receipt first."""
import hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads
fields=json.loads((H/'fields.json').read_text());payload=H/'transaction.edn';sha=hashlib.sha256(payload.read_bytes()).hexdigest();render=json.loads((H/'render-verification.json').read_text());assert render['passed']and render['fields']==len(fields)and all(not r['after']['errors']for r in render['checks']);assert[(r['entity'],r['attribute'],r['before_sha256'],r['after_sha256'])for r in render['checks']]==[(r['entity'],r['attribute'],r['before_sha256'],r['after_sha256'])for r in fields]
forms=loads(payload.read_text());assert forms==[[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in fields];db=connection();intent_path=H/'commit-intent.json'
if not intent_path.exists():
 subprocess.run([str(R/'.local/edb/percent-escaping/preview'),str(payload),str(H/'fields.json'),str(H/'native-preview.json')],env=db.env,check=True,capture_output=True,text=True)
 intent={'database':'math','source':':agent/codex','sha256':sha,'request_key':'structural-math-2026-10-26-'+sha[:24],'file':str(payload.resolve()),'endpoint':'/tmp/edb-math/writer.sock'};intent_path.write_text(json.dumps(intent,indent=2)+'\n')
else:intent=json.loads(intent_path.read_text());assert intent['sha256']==sha
receipt=H/'receipt.edn';r=None
if receipt.exists():
 try:r=loads(receipt.read_text())
 except(IndexError,ValueError):pass
if not isinstance(r,dict)or r.get(':edb/committed')is not True:
 cmd=[db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000']
 with receipt.open('w')as out,(H/'submit.stderr').open('w')as err:subprocess.run(cmd,env=db.env,stdout=out,stderr=err,check=True,timeout=160)
 r=loads(receipt.read_text())
assert r[':edb/committed']is True;print('Committed T'+str(r[':edb/db-after-t']),flush=True)
subprocess.run([sys.executable,str(H/'verify_db.py')],check=True)

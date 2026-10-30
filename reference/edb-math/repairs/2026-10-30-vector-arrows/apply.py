"""Apply the authorized, persisted CAS repair and verify its exact db-after."""
import hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import loads
assert sys.argv[1:]==['--apply-user-authorized']
assert json.loads((HERE/'render-verification.json').read_text())['passed']
assert len(json.loads((HERE/'source-render-verification.json').read_text()))==22
fields=json.loads((HERE/'fields.json').read_text());forms=loads((HERE/'transaction.edn').read_text())
assert len(forms)==len(fields)==6
for form,f in zip(forms,fields):
 assert form==[':db/cas',f['entity'],':'+f['attribute'],f['before'],f['after']]
 assert f['after']==f['before'].replace(r'\overset{\to -}',r'\overrightarrow')
db=Publisher.from_environment(source=':agent/codex').client
status=json.loads((HERE/'status.json').read_text());assert db.status()['lineage']==status['lineage']
cli=ROOT.parent/'EDB/target/release/edb'
sha=hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()
intent={'database':'math','lineage':status['lineage'],'source':':agent/codex','endpoint':'/tmp/edb-math/writer.sock','file':str(HERE/'transaction.edn'),'sha256':sha,'request_key':'repair-vector-arrows-2026-10-30-'+sha[:24]}
intent_path=HERE/'commit-intent.json'
if intent_path.exists():assert json.loads(intent_path.read_text())==intent
else:intent_path.write_text(json.dumps(intent,indent=2))
def run(command,name,*extra):
 result=subprocess.run([str(cli),command,'--database','math','--file',intent['file'],'--source',intent['source'],*extra],env=db.environment,text=True,capture_output=True,timeout=150)
 (HERE/(name+'.edn')).write_text(result.stdout);(HERE/(name+'.stderr')).write_text(result.stderr)
 assert result.returncode==0,result.stderr
 return loads(result.stdout)
receipt_path=HERE/'receipt.edn'
if receipt_path.exists() and receipt_path.stat().st_size:
 receipt=loads(receipt_path.read_text());assert receipt[':edb/committed']
else:
 if not (HERE/'submission-started.json').exists():
  preview=run('with','preview');assert preview[':edb/committed'] is False
  assert len(preview[':edb/tx-data'])==13
  (HERE/'submission-started.json').write_text(json.dumps(intent))
 receipt=run('transact','receipt','--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000')
 assert receipt[':edb/committed']
basis=receipt[':edb/db-after-t']
actual=loads(db.command('query','--as-of',basis,'--file',HERE/'read-query.edn','--inputs',HERE/'read-inputs.edn'))
(HERE/'after.edn').write_text(__import__('capture.scripts.database.edn',fromlist=['dumps']).dumps(actual))
assert {(e,str(a)[1:]):v for e,a,v in actual}=={(f['entity'],f['attribute']):f['after'] for f in fields}
assert len(receipt[':edb/tx-data'])==13
report={'committed':True,'basis':basis,'fields':len(fields),'arrows':sum(f['arrows'] for f in fields),'source':intent['source'],'request_key':intent['request_key'],'exact_readback_matches':True,'remaining_malformed_arrows_in_repaired_fields':sum(v.count(r'\overset{\to -}') for e,a,v in actual)}
(HERE/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

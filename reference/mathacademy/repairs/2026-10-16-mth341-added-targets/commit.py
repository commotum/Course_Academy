"""Preview, submit an immutable format-only repair, and verify its exact basis."""
import hashlib,json,os,subprocess,sys,threading
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT))
from capture.scripts.config import Config
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import loads,dumps,kw
BIN='/home/jake/Developer/EDB/target/release/edb'
ENV={**os.environ,'EDB_POSTGRES_URL':'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
def run(*args):return subprocess.check_output(list(args),env=ENV,text=True,timeout=180)
validation=json.loads((HERE/'preview-render/summary.json').read_text())
assert validation['fields']==2068 and not validation['page_errors']
assert all(validation[k]==0 for k in ['parse_error_fields','raw_tex_fields','red_command_fields','code_block_fields'])
for name, expected_hash in json.loads((HERE/'prepared-hashes.json').read_text()).items():
 assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==expected_hash, name
transaction=HERE/'transaction.edn';digest=hashlib.sha256(transaction.read_bytes()).hexdigest();intent_path=HERE/'commit-intent.json'
guard=json.loads((HERE/'precommit-safety.json').read_text())
assert guard['transaction_sha256']==digest and guard['all_fields_unchanged_since_snapshot'] and guard['response_references']==0
if intent_path.exists():
 intent=json.loads(intent_path.read_text());assert intent['sha256']==digest
else:
 # Every current field is CAS-guarded. The basis guard additionally protects
 # the read showing that none of the changed answers belongs to a response.
 intent={'database':'math','source':':application/ca-engine','endpoint':'/tmp/edb-math/writer.sock','basis':guard['basis'],'file':str(transaction),'sha256':digest,'request_key':'mth341-added-targets-display-v1-'+digest+'-b'+str(guard['basis'])}
 intent_path.write_text(json.dumps(intent,indent=2)+'\n')
receipt=HERE/'receipt.edn'
if not receipt.exists():
 preview=preview_executable(Config(),threading.Event())
 (HERE/'preview.edn').write_text(run(str(preview),'with','--database','math','--source',intent['source'],'--file',str(transaction)))
 previous=loads((HERE/'preview.edn').read_text());assert previous[':edb/committed'] is False
if '--preview-only' in sys.argv:
 print('Speculative preview passed; no database writes');sys.exit(0)
saved=loads(receipt.read_text()) if receipt.exists() and receipt.stat().st_size else {}
if not saved.get(':edb/committed'):
 result=run(BIN,'transact','--database','math','--source',intent['source'],'--file',str(transaction),'--basis',str(intent['basis']),'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000')
 receipt.write_text(result);saved=loads(result)
assert saved.get(':edb/committed'),'Unknown commit outcome; retain exact request'
basis=saved[':edb/basis-t']
after=run(BIN,'query','--database','math','--as-of',str(basis),'--file',str(HERE/'read-query.edn'),'--inputs',str(HERE/'read-inputs.edn'))
(HERE/'after.edn').write_text(after)
actual={(eid,attr):v for eid,attr,v in loads(after)};expected={(eid,attr):v for eid,attr,v in loads((HERE/'expected.edn').read_text())};assert actual==expected
fields=json.loads((HERE/'expected-fields.json').read_text())
for f in fields:
 key=f['entity'],f['attribute']
 if key in actual:f['value']=actual[key]
(HERE/'committed-fields.json').write_text(json.dumps(fields,indent=2)+'\n')
report={'basis':basis,'fields':len(actual),'entities':len({k[0] for k in actual}),'exact_readback_matches':True,'request_key':intent['request_key']}
(HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

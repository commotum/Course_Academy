"""Submit or reconcile this one preserved, user-authorized EDB request."""
from pathlib import Path
import os,sys,json,hashlib,subprocess
p=Path(__file__).resolve().parent;root=p.parents[4]
sys.path.insert(0,str(root/'scripts/question_capture'))
from edn import loads
intent=json.loads((p/'intent.json').read_text());tx=p/'transaction.edn'
assert hashlib.sha256(tx.read_bytes()).hexdigest()==intent['transaction_sha256']
source=intent['source_entity'];idents={str(r[1]):r[0] for r in loads((p/'sources.edn').read_text())}
expected={(r['entity'],idents[r['attribute']],r['after'],True) for r in intent['expected']}
expected.update((r['entity'],idents[r['attribute']],r['before'],False) for r in intent['expected'] if r['before']!=r['after'])
preview=loads((p/'preview.edn').read_text());assert preview[':edb/committed'] is False
assert all(d[4]==source for d in preview[':edb/tx-data'])
assert {(d[0],d[1],d[2],d[5]) for d in preview[':edb/tx-data'] if d[1]!=idents[':db/txInstant']}==expected
env=os.environ.copy();env['EDB_POSTGRES_URL']="host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"
cmd=[str(root/'.local/edb/capture-runtime/math-edb'),'transact','--database',intent['database'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--source',intent['source'],'--file',str(tx),'--timeout-ms','30000']
r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=60)
(p/'commit.stdout.edn').write_text(r.stdout);(p/'commit.stderr.txt').write_text(r.stderr)
if r.returncode:raise RuntimeError('Submission returned an error; preserve this exact request and reconcile before another write. '+r.stderr)
receipt=loads(r.stdout);assert receipt[':edb/committed'] is True
(p/'receipt.edn').write_text(r.stdout)
assert all(d[4]==source for d in receipt[':edb/tx-data'])
assert {(d[0],d[1],d[2],d[5]) for d in receipt[':edb/tx-data'] if d[1]!=idents[':db/txInstant']}==expected
print('COMMITTED basis',receipt[':edb/db-after-t'],'source',intent['source'],'datoms',len(receipt[':edb/tx-data']),flush=True)
basis=receipt[':edb/db-after-t']
r=subprocess.run([str(root/'.local/edb/capture-runtime/math-edb'),'query','--database',intent['database'],'--as-of',str(basis),'--file',str(p/'before-query.edn')],env=env,capture_output=True,text=True,check=True,timeout=30)
(p/'after.edn').write_text(r.stdout)
policies=loads(r.stdout);assert len(policies)==1
children={c[':db/id']:c for c in policies[0][0][':policy/question-selection-weights']}
for row in intent['expected']:assert children[row['entity']][row['attribute']]==row['after']
query='[:find ?e ?a ?v ?tx ?s :in $ [?e ...] :where [?e ?a ?v ?tx ?s]]'
(p/'provenance-query.edn').write_text(query+'\n');(p/'provenance-inputs.edn').write_text('[[17592186409232 17592186409233]]\n')
r=subprocess.run([str(root/'.local/edb/capture-runtime/math-edb'),'query','--database',intent['database'],'--as-of',str(basis),'--file',str(p/'provenance-query.edn'),'--inputs',str(p/'provenance-inputs.edn')],env=env,capture_output=True,text=True,check=True,timeout=30)
(p/'provenance.edn').write_text(r.stdout)
provenance=loads(r.stdout)
for row in intent['expected']:
 assert any(e==row['entity'] and a==idents[row['attribute']] and v==row['after'] and s==source for e,a,v,t,s in provenance)
verification={'committed':True,'verified':True,'database':intent['database'],'basis_before':receipt[':edb/db-before-t'],'basis_after':basis,'source':intent['source'],'source_entity':source,'updated_weight_facts':12,'changed_values':10,'reasserted_values':2,'all_weight_facts_have_requested_source':True,'receipt_datoms_match_exact_scope':True,'current_values_match_requested_distributions':True,'request_key':intent['request_key']}
(p/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps(verification,indent=2));print(r.stdout)

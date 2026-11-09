import sys,json,hashlib,subprocess,re
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');H=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection,loads
p=H/'transaction.edn';digest=hashlib.sha256(p.read_bytes()).hexdigest();db=connection()
if (H/'commit-intent.json').exists():
 intent=json.loads((H/'commit-intent.json').read_text());assert intent['sha256']==digest
else:
 preview=subprocess.run([sys.executable,str(H/'preview.py')],env=db.env,capture_output=True,text=True);assert preview.returncode==0,preview.stdout+preview.stderr
 report=loads((H/'preview.edn').read_text());intent={'database':'math','source':':course-academy.source/editor','endpoint':'/tmp/edb-math/writer.sock','file':str(p),'sha256':digest,'request_key':'quiz3-ode-concepts-quality-'+digest[:24],'preview_basis':report[':edb/db-before-t'],'guards':'CAS every changed cardinality-one old value; source-proven membership retractions with retained entities; installed question/field/answer specs; no global basis guard'}
 (H/'commit-intent.json').write_text(json.dumps(intent,indent=2)+'\n')
r=subprocess.run([db.args.edb_bin,'transact','--database','math','--file',intent['file'],'--source',intent['source'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','180000'],env=db.env,text=True,capture_output=True,timeout=210)
(H/'receipt.edn').write_text(r.stdout);(H/'submit.stderr').write_text(r.stderr)
if r.returncode:print('Outcome requires same-key reconciliation',r.returncode,r.stderr);sys.exit(r.returncode)
report=loads(r.stdout);print(json.dumps({'committed':True,'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],'receipt_keys':list(report),'request_key':intent['request_key']}))

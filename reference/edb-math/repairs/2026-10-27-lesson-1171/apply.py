import collections,hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection,kw,loads
payload=H/'transaction.edn';sha=hashlib.sha256(payload.read_bytes()).hexdigest();forms=loads(payload.read_text());db=connection();cas=[f for f in forms if str(f[0])==':db/cas'];assert len(cas)==18
assert json.loads((H/'all-rendering.json').read_text())['passed'];assert json.loads((H/'grading.json').read_text())['documented_unresolved_checks']==0
intent_path=H/'commit-intent.json'
if not intent_path.exists():
 subprocess.run([sys.executable,str(H/'preview.py')],check=True);intent={'sha256':sha,'request_key':'lesson-1171-2026-10-27-'+sha[:24],'source':':agent/codex','database':'math'};intent_path.write_text(json.dumps(intent,indent=2)+'\n')
else:intent=json.loads(intent_path.read_text());assert intent['sha256']==sha
receipt=H/'receipt.edn'
if not receipt.exists():
 p=subprocess.run([db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',str(payload),'--endpoint','/tmp/edb-math/writer.sock','--request-key',intent['request_key'],'--timeout-ms','120000'],env=db.env,capture_output=True,text=True,timeout=160);receipt.write_text(p.stdout);(H/'submit.stderr').write_text(p.stderr);p.check_returncode()
r=loads(receipt.read_text());assert r[':edb/committed']is True;t=r[':edb/db-after-t'];want={(e,str(a).lstrip(':')):after for _,e,a,before,after in cas}
rows=db.query('[:find ?e ?name ?v :in $ [[?e ?name]] :where [?a :db/ident ?name] [?e ?a ?v]]',[[[e,kw(a)]for e,a in want]],H,'after',t);assert {(e,str(a).lstrip(':')):v for e,a,v in rows}==want
attrs=db.query('[:find ?a ?name :in $ [?name ...] :where [?a :db/ident ?name]]',[[kw(a)for a in {a for e,a in want}|{'db/txInstant'}]],H,'attribute-ids',t);ids={str(name).lstrip(':'):a for a,name in attrs}
expected=collections.Counter((e,ids[str(a).lstrip(':')],v,op)for _,e,a,before,after in cas for v,op in [(before,False),(after,True)]if v is not None);actual=collections.Counter((d[0],d[1],d[2],d[5])for d in r[':edb/tx-data']if d[1]!=ids['db/txInstant']);assert actual==expected and all(d[4]==17592186576411 for d in r[':edb/tx-data'])
out={'committed':True,'basis_t':t,'content_fields':16,'correct_links_completed':2,'datoms':len(r[':edb/tx-data']),'exact_readback':True,'only_reviewed_content_and_key_links_changed':True,'learner_history_preserved':True,'sha256':sha};(H/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

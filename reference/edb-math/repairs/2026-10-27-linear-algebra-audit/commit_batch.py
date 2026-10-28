"""Commit a reviewed CAS-only repair batch, reconcile its receipt, verify exact datoms."""
import collections,hashlib,json,subprocess,sys,threading
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R),str(R/'scripts')]
from capture.scripts.config import Config
from capture.scripts.database.preview import preview_executable
from migrate_learner_history import connection,kw,loads,dumps
D=Path(sys.argv[1]);proposals=json.loads((D/'approved-proposals.json').read_text());assert proposals
assert len({(p['entity'],p['attribute'])for p in proposals})==len(proposals)
forms=[];ensures=set()
for p in proposals:
 assert p['before']!=p['after'];forms.append([kw('db/cas'),p['entity'],kw(p['attribute']),p['before'],p['after']])
 if p['attribute'].startswith('question/'):ensures.add((p['entity'],'question/validate'))
 elif p['attribute'].startswith('tutorial/'):ensures.add((p['entity'],'tutorial/validate'))
 elif p['attribute'].startswith('answer-field/'):
  ensures.add((p['entity'],'answer-field/validate'))
  if p['attribute']=='answer-field/correct':ensures.add((p['after'],'answer/validate'))
for e,spec in sorted(ensures):forms.append([kw('db/ensure'),e,kw(spec)])
payload=dumps(forms)+'\n';file=D/'transaction.edn'
if file.exists():assert file.read_text()==payload,'Existing transaction payload differs; never change a saved request'
else:file.write_text(payload)
sha=hashlib.sha256(payload.encode()).hexdigest();db=connection();intentpath=D/'commit-intent.json';receipt=D/'receipt.edn'
if not intentpath.exists():
 binary=preview_executable(Config(),threading.Event());p=subprocess.run([str(binary),'with','--database','math','--file',str(file),'--source',':agent/codex'],env=db.env,capture_output=True,text=True)
 (D/'preview.edn').write_text(p.stdout);(D/'preview.stderr').write_text(p.stderr);p.check_returncode();assert loads(p.stdout).get(':edb/speculative')is True
 intent={'sha256':sha,'request_key':'linear-algebra-audit-2026-10-27-'+sha[:32],'source':':agent/codex','database':'math'};intentpath.write_text(json.dumps(intent,indent=2)+'\n')
else:intent=json.loads(intentpath.read_text());assert intent['sha256']==sha
if not receipt.exists()or not receipt.read_text().strip():
 p=subprocess.run([db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',str(file),'--endpoint','/tmp/edb-math/writer.sock','--request-key',intent['request_key'],'--timeout-ms','120000'],env=db.env,capture_output=True,text=True,timeout=160)
 receipt.write_text(p.stdout);(D/'submit.stderr').write_text(p.stderr);p.check_returncode()
r=loads(receipt.read_text());assert r[':edb/committed']is True;t=r[':edb/db-after-t'];want={(p['entity'],p['attribute']):p['after']for p in proposals}
rows=[];pairs=list(want)
for offset in range(0,len(pairs),30):rows.extend(db.query('[:find ?e ?name ?v :in $ [[?e ?name]] :where [?a :db/ident ?name] [?e ?a ?v]]',[[[e,kw(a)]for e,a in pairs[offset:offset+30]]],D,'after-'+str(offset),t))
assert {(e,str(a).lstrip(':')):v for e,a,v in rows}==want
attrs=db.query('[:find ?a ?name :in $ [?name ...] :where [?a :db/ident ?name]]',[[kw(a)for a in {a for e,a in want}|{'db/txInstant'}]],D,'attribute-ids',t);ids={str(name).lstrip(':'):a for a,name in attrs}
expected=collections.Counter((p['entity'],ids[p['attribute']],v,op)for p in proposals for v,op in [(p['before'],False),(p['after'],True)]if v is not None);actual=collections.Counter((d[0],d[1],d[2],d[5])for d in r[':edb/tx-data']if d[1]!=ids['db/txInstant']);assert actual==expected and all(d[4]==17592186576411 for d in r[':edb/tx-data'])
summary={'committed':True,'basis_t':t,'changed_fields':len(proposals),'entities':len({p['entity']for p in proposals}),'datoms':len(r[':edb/tx-data']),'exact_readback':True,'only_reviewed_content_and_correct_links_changed':True,'learner_history_preserved':True,'sha256':sha};(D/'verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)

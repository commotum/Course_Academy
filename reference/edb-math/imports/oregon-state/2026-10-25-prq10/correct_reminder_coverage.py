"""Keep the separate reading reminder's topic out of Problem 6's coverage."""
import hashlib,json,subprocess,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,dumps,loads
p=H/'reminder-coverage';p.mkdir(exist_ok=True);db=connection();intent_path=p/'intent.json'
if intent_path.exists():intent=json.loads(intent_path.read_text())
else:
 basis=db.basis();rows=db.query('[:find ?p ?t :in $ ?id ?topic :where [?p :assigned-problem/id ?id] [?t :topic/math-academy-id ?topic] [?p :assigned-problem/topic-coverage ?t]]',[uuid.UUID('6bd94823-2af8-5542-bb42-dd8f8802d886'),1853],p,'before',basis);assert len(rows)==1;eid,topic=rows[0];forms=[[kw('db/retract'),eid,kw('assigned-problem/topic-coverage'),topic],[kw('db/ensure'),eid,kw('assigned-problem/validate')]];payload=dumps(forms)+'\n';(p/'transaction.edn').write_text(payload);sha=hashlib.sha256(payload.encode()).hexdigest();intent={'basis':basis,'entity':eid,'topic':topic,'sha256':sha,'request_key':'prq10-reminder-coverage-'+sha[:24]+'-b'+str(basis),'reason':'The Subspace Test reading reminder is a separate noninteractive tutorial, not part of Problem 6. Its topic remains covered by Problems 1 and 2 and remains a learner target.'};intent_path.write_text(json.dumps(intent,indent=2)+'\n')
assert hashlib.sha256((p/'transaction.edn').read_bytes()).hexdigest()==intent['sha256']
receipt=p/'receipt.edn'
if not receipt.exists():
 preview=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(p/'transaction.edn')],env=db.env,text=True,capture_output=True,check=True);(p/'preview.log').write_text(preview.stdout)
 command=[db.args.edb_bin,'transact','--database','math','--source',':course-academy.source/editor','--file',str(p/'transaction.edn'),'--endpoint','/tmp/edb-math/writer.sock','--basis',str(intent['basis']),'--request-key',intent['request_key'],'--timeout-ms','120000']
 with receipt.open('w')as out,(p/'submit.stderr').open('w')as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,check=True,timeout=160)
r=loads(receipt.read_text());assert r[':edb/committed'];after=db.query('[:find ?n :in $ ?p :where [?p :assigned-problem/topic-coverage ?t] [?t :topic/math-academy-id ?n]]',[intent['entity']],p,'after',r[':edb/db-after-t']);assert sorted(x[0]for x in after)==[1861,1866,1909];assert len(r[':edb/tx-data'])==2
proof={'committed':True,'basis_t':r[':edb/db-after-t'],'only_removed_topic_link':[intent['entity'],intent['topic']],'final_problem_6_topic_ids':[1861,1866,1909],'all_questions_answers_history_and_targets_unchanged':True};(p/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)

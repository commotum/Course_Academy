import hashlib,json,subprocess,sys,threading
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R),str(R/'scripts')]
from capture.scripts.config import Config
from capture.scripts.database.preview import preview_executable
from migrate_learner_history import connection,loads,kw
from question_capture.database import QUESTION_PULL
h=H/'completion';payload=h/'transaction.edn';sha=hashlib.sha256(payload.read_bytes()).hexdigest();db=connection();render=json.loads((H/'final-render.json').read_text());assert not render['page_errors']and all(not r['errors']for r in render['checks']);grading=json.loads((H/'native-grading.json').read_text());assert grading['documented_unresolved_checks']==0
fields=json.loads((h/'fields.json').read_text());checks={(r['entity'],r['attribute']):r for r in render['checks']};assert all(not checks[f['entity'],f['attribute']]['errors']for f in fields)
intent_file=h/'commit-intent.json'
if not intent_file.exists():
 preview=preview_executable(Config(),threading.Event());r=subprocess.run([str(preview),'with','--database','math','--file',str(payload),'--source',':agent/codex'],env=db.env,text=True,capture_output=True,check=True);(h/'native-preview.edn').write_text(r.stdout);p=loads(r.stdout);assert p[':edb/committed']is False
 # Confirm the only newly authored control still has no existing competitors.
 before=db.query('[:find ?f :in $ ?q :where [?q :question/answer-fields ?f]]',[17592186233379],h,'new-control-preflight');assert before==[]
 intent={'database':'math','source':':agent/codex','file':str(payload.resolve()),'sha256':sha,'request_key':'determinant-question-completion-2026-10-26-'+sha[:24],'endpoint':'/tmp/edb-math/writer.sock'};intent_file.write_text(json.dumps(intent,indent=2)+'\n')
else:intent=json.loads(intent_file.read_text());assert intent['sha256']==sha
receipt=h/'receipt.edn';r=loads(receipt.read_text())if receipt.exists()and receipt.stat().st_size else None
if not isinstance(r,dict)or r.get(':edb/committed')is not True:
 with receipt.open('w')as out,(h/'submit.stderr').open('w')as err:subprocess.run([db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000'],env=db.env,stdout=out,stderr=err,check=True,timeout=160)
 r=loads(receipt.read_text())
assert r[':edb/committed']is True;basis=r[':edb/db-after-t'];ids=[17592186059981,17592186060000,17592186060001,17592186060195,17592186233379];rows=db.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id ?id]]',[ids],h,'after',basis);actual={q[0][':db/id']:q[0]for q in rows};expected={q[':db/id']:q for q in json.loads((H/'repaired-questions.json').read_text())if q[':db/id']in ids}
for e,q in actual.items():
 assert q[':question/problem']==expected[e][':question/problem']and q[':question/worked-solution']==expected[e][':question/worked-solution']
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];ef=expected[e][':question/answer-fields'][0];assert str(f[':answer-field/correct'][':answer/id'])==str(ef[':answer-field/correct'][':answer/id']);assert sorted((str(a[':answer/id']),a[':answer/value'])for a in f[':answer-field/choices'])==sorted((str(a[':answer/id']),a[':answer/value'])for a in ef[':answer-field/choices'])
 if e!=17592186233379:assert f[':db/id']==ef[':db/id']
attrs=db.query('[:find ?a ?id :in $ [?id ...] :where [?a :db/ident ?id]]',[[kw(a)for a in ['db/txInstant','question/worked-solution','question/problem','question/answer-fields','answer-field/correct','answer-field/id','answer-field/type','answer-field/key','answer-field/choices','answer/id','answer/type','answer/value']]],h,'attribute-ids',basis);attrs={e:str(i).lstrip(':')for e,i in attrs};data=r[':edb/tx-data'];assert len(data)==20 and all(d[4]==17592186576411 for d in data);assert all(d[1]in attrs for d in data);allowed=set(ids)|{f[':db/id']for q in actual.values()for f in q[':question/answer-fields']}|{a[':db/id']for q in actual.values()for f in q[':question/answer-fields']for a in f[':answer-field/choices']};assert all(d[0]in allowed or attrs[d[1]]=='db/txInstant'for d in data)
report={'committed':True,'basis_t':basis,'questions_completed':5,'solutions_added':4,'existing_correct_links_added':4,'new_math_blank_added':1,'exact_readback_verified':True,'existing_answer_values_and_ids_preserved':True,'learner_history_unchanged':True,'datoms':len(data),'sha256':sha};(h/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

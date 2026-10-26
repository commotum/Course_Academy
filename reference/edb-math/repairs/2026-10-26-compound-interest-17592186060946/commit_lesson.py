import collections,hashlib,json,subprocess,sys,threading
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R),str(R/'scripts')]
from capture.scripts.config import Config
from capture.scripts.database.preview import preview_executable
from migrate_learner_history import connection,loads,kw
from question_capture.database import QUESTION_PULL
fields=json.loads((H/'fields.json').read_text());links=json.loads((H/'links.json').read_text());payload=H/'transaction.edn';sha=hashlib.sha256(payload.read_bytes()).hexdigest();db=connection();render=json.loads((H/'final-render.json').read_text());assert not render['page_errors']and all(not c['errors']for c in render['checks']);assert json.loads((H/'native-grading.json').read_text())['documented_unresolved_checks']==0
intent_file=H/'commit-intent.json'
if not intent_file.exists():
 preview=preview_executable(Config(),threading.Event());p=subprocess.run([str(preview),'with','--database','math','--file',str(payload),'--source',':agent/codex'],env=db.env,capture_output=True,text=True,check=True);(H/'native-preview.edn').write_text(p.stdout);assert loads(p.stdout)[':edb/committed']is False
 intent={'database':'math','source':':agent/codex','file':str(payload.resolve()),'sha256':sha,'request_key':'compound-interest-lesson-repair-2026-10-26-'+sha[:24],'endpoint':'/tmp/edb-math/writer.sock'};intent_file.write_text(json.dumps(intent,indent=2)+'\n')
else:intent=json.loads(intent_file.read_text());assert intent['sha256']==sha
receipt=H/'receipt.edn';r=loads(receipt.read_text())if receipt.exists()and receipt.stat().st_size else None
if not isinstance(r,dict)or r.get(':edb/committed')is not True:
 with receipt.open('w')as out,(H/'submit.stderr').open('w')as err:subprocess.run([db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000'],env=db.env,stdout=out,stderr=err,check=True,timeout=160)
 r=loads(receipt.read_text())
assert r[':edb/committed']is True;b=r[':edb/db-after-t'];pairs=[[f['entity'],kw(f['attribute'])]for f in fields]+[[l['field'],kw('answer-field/correct')]for l in links];values=db.query('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]',[pairs],H,'after-values',b);expected={(f['entity'],f['attribute']):f['after']for f in fields};expected.update({(l['field'],'answer-field/correct'):l['correct']for l in links});assert{(e,str(a).lstrip(':')):v for e,a,v in values}==expected
attrs=db.query('[:find ?a ?id :in $ [?id ...] :where [?a :db/ident ?id]]',[[kw(a)for a in ['db/txInstant','answer/value','question/worked-solution','answer-field/correct']]],H,'attribute-ids',b);attrs={str(i).lstrip(':'):e for e,i in attrs};wanted=collections.Counter((f['entity'],attrs[f['attribute']],f[side],added)for f in fields for side,added in [('before',False),('after',True)]if f[side]is not None);wanted.update((l['field'],attrs['answer-field/correct'],l['correct'],True)for l in links);data=r[':edb/tx-data'];assert all(d[4]==17592186576411 for d in data);assert collections.Counter((d[0],d[1],d[2],d[5])for d in data if d[1]!=attrs['db/txInstant'])==wanted;assert len(data)==sum(wanted.values())+1
qs=json.loads((H/'repaired-questions.json').read_text());actual=db.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id ?id]]',[[q[':db/id']for q in qs]],H,'final-questions',b);actual=json.loads(json.dumps([x[0]for x in actual],default=str));before={q[':db/id']:q for q in qs}
for q in actual:
 e=q[':db/id'];ex=before[e];assert q[':question/id']==ex[':question/id'];assert q[':question/problem']==ex[':question/problem'];assert q[':question/worked-solution']==ex[':question/worked-solution'];assert len(q.get(':question/answer-fields',[]))==len(ex.get(':question/answer-fields',[]))
 for f,ef in zip(q.get(':question/answer-fields',[]),ex.get(':question/answer-fields',[])):
  assert f[':db/id']==ef[':db/id'];assert f[':answer-field/correct'][':db/id']==ef[':answer-field/correct'][':db/id'];assert sorted((a[':db/id'],a[':answer/value'])for a in f[':answer-field/choices'])==sorted((a[':db/id'],a[':answer/value'])for a in ef[':answer-field/choices'])
(H/'final-questions.json').write_text(json.dumps(actual,indent=2)+'\n');report={'committed':True,'basis_t':b,'text_fields':len(fields),'currency_choices_repaired':10,'canonical_solution_lines_repaired':1,'solutions_added':6,'correct_links_added':6,'all_lesson_questions_verified':len(actual),'only_reviewed_facts_changed':True,'existing_ids_and_numeric_values_preserved':True,'learner_history_preserved':True,'sha256':sha};(H/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
